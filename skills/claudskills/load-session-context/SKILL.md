---
name: load-session-context
type: skill
tags: [agents, "11.11", memgpt, virtual-context, semantic-fetch, ko-db]
trigger_keywords: [load-context, session-start, 11.11start, project-context, virtual-context, semantic-load]
created: 2026-04-30
updated: 2026-05-20
description: |
  MemGPT-style virtual context-load egy 11.11 session indulásakor.
  B-2 sprint Week 3 rewrite (2026-05-13): a klasszikus aggressive 15-20K token-os
  cat-jel helyett **lean ~5K token** working+top-K episodic + semantic on-demand.
  B-1 Week 3-4 bővítés (2026-05-17): **KO-DB Top-K structured facts** réteg
  (13K+ fact, cross-source-corroboration ranking, instant SQLite).
  Production-stack v2 (2026-05-20): **RRF hybrid-fusion** retrieval (vault-search +
  agentmemory), 77.5% avg R@5 (+23pp), drop-in via `vault-search-fusion` CLI.
  Triggers: amikor a user 11.11start-ot használ, vagy "load context for <projekt>" kérés.
---

# load-session-context (B-2 Week 3 rewrite)

A 11.11 session indulása utáni perceket optimalizálja: az agent **lean ~5K token** kontextust kap working + top-K episodic-ról, plus **on-demand semantic-fetch** ha mélyebb infó kell. **75% token-megtakarítás** a régi aggressive 15-20K-hoz képest, **3× gyorsabb context-load** (Memgraph bge-m3 vs file-grep).

## Mikor triggereljen

- Amikor a user `/11.11start "<név>"` parancsot adott — automatikusan a következő agent-interakcióban
- Amikor a session-fájlban a `## Pre-loaded context` szekció üres TODO-blokkot tartalmaz
- Amikor a user explicitly kéri: "load context for kgc-berles" vagy "tölts be mindent a foxxi-ról"

## MemGPT virtual context: 3-rétegű memory + KO-DB structured layer

A [[11-wiki/sv-01-memory-architecture]] szerint 3 memory-szint, plusz a B-1 Week 3-4 óta KO-DB structured layer:

| Réteg | Forrás | Kontextusba teszi |
|---|---|---|
| **Working** | `08-Sessions/<focused>` (most aktív session) | ✅ Mindig (direct file-read) |
| **Episodic** | `01-Daily/+10-raw/+08-Sessions/_archive/` (utolsó 14 nap) | ✅ Top-K=3 semantic-fetch (`vault-search-fusion`) |
| **Semantic** | `11-wiki/+07-Decisions/+05-Memory/+02-Projects/` (evergreen tudás) | ⏳ On-demand `vault-search-fusion` tool-call-lal |
| **KO-DB structured** ⭐NEW | `.vault-ko/facts.db` (13K+ fact, multi-source) | ✅ Top-K=5–8 `vault-ko-query --top-k` (cross-source ranking) |

**Régi pattern (DEPRECATED, ~15-20K token):**
```
cat 02-Projects/<slug>.md           # ~3K
cat 08-Sessions/<utolsó-5>.md       # ~6K
grep + cat 07-Decisions/*.md        # ~4K
cat 05-Memory/Infrastructure.md     # ~2K
cat 04-Tasks/Backlog.md (filtered)  # ~3K
```

**Új pattern (~5K token):**
```
cat 08-Sessions/<focused>.md                 # working: ~1K (csak az aktív session)
vault-search-fusion --top-k 3 "<projekt-slug>" # episodic+semantic: ~2.5K (top-3 chunk, RRF fusion)
vault-ko-query "<slug>" --top-k 6            # KO-DB structured: ~0.8K (top-6 multi-source subject)
vault-context-meta <slug>                    # working metadata: ~0.7K (projekt-file 1-line + top-3 task)
```

A többi (deep ADR-tartalom, infra-gotchák, régebbi session-Learning) **on-demand**: ha a user kérdés specifikus témára mélyül, az agent `vault-search-fusion "<kérdés>"` tool-call-t hív (RRF fusion vault-search + agentmemory, +23pp R@5 vs vault-search alone), és a top-K-t bevonja a kontextusba.

## Hogyan működik (új flow)

### 1. Projekt-detektálás (változatlan)

A session-névből deduktálj projekt-slug-ot a [[11-wiki/Auto-context-loading|detektálási tábla]] szerint. Ambiguity → user-kérdés.

### 2a. KO-DB Top-K structured facts ⭐NEW (2026-05-17)

A 13K+ fact KO-DB **instant SQLite** — gyorsabb mint Memgraph, kiegészíti a semantic chunkokat strukturált multi-source-corroborated state-tel:

```bash
# DEFAULT — text mode (~400 token), kontextusba közvetlen beilleszthető:
vault-ko-query "<projekt-slug>" --top-k 6 --facts-per-subject 3

# Csak strukturált programatikus feldolgozáshoz (~1200 token):
vault-ko-query "<projekt-slug>" --top-k 6 --json
```

**Default `--text` mód** lean ~5K budget-be való. JSON csak script-pipeline-ban érdemes.

Output (JSON tömb subject-objektumokkal):
```json
[
  {
    "subject": "kgc-berles",
    "source_count": 8,            // hány distinct provenance említi
    "max_confidence": 0.98,
    "fact_count": 28,             // teljes fact-count erre a subject-re
    "facts": [
      {"predicate": "uses", "object": "Next.js 16.2.3", "provenance": "08-Sessions/...", "confidence": 0.98, "source_type": "session"},
      {"predicate": "has_value", "object": "port 3004", ...},
      {"predicate": "depends_on", "object": "kgc-postgres", ...}
    ]
  },
  ...
]
```

**Rangsor:** `(distinct sources DESC, max confidence DESC, total fact count DESC)` — a leg-cross-source-validáltabb subject-ek elöl. A multi-source ranking azt jelenti: ha 8 forrás (3 ADR + 4 session + 1 wiki) említ valamit, akkor az **konszenzus**, nem egyszeri kijelentés.

**Mikor ér többet a Memgraph semantic-fetch-nél:**
- amikor pontos entity-fact kell (port-szám, version, file-path, dependency)
- amikor "mit tudunk X-ről?" típusú kérdés van
- amikor cross-source consistency-t akarsz látni (egyszerre több projektből konszenzust)

**Mikor Memgraph jobb:**
- amikor szöveges narrative kell (long-form kontextus, multi-paragraph cikk-részlet)
- amikor a kérdés bizonytalan kulcsszavakkal jön (semantic > LIKE)

A kettő **komplementer**: Top-K KO-DB strukturált alap + semantic-fetch szöveges narratíva.

### 2b. Lean fetch (vault-context-load script)

```bash
vault-context-load <slug>
```

Output JSON:
```json
{
  "working": {
    "session_file": "08-Sessions/2026-05-13-...",
    "first_120_lines": "..."
  },
  "episodic_top_k": [
    {"file": "...", "title": "...", "snippet": "...", "score": 0.74},
    ...
  ],
  "project_meta": {
    "file": "02-Projects/<slug>.md",
    "status_line": "🟢 active — ...",
    "open_tasks_count": 7,
    "top_3_tasks": [...]
  }
}
```

### 3. Pre-loaded context szekció (lean format)

```markdown
## Pre-loaded context

> Auto-load YYYY-MM-DDTHH:MM — MemGPT virtual + KO-DB structured (lean ~5K token).

**Projekt:** [[02-Projects/<slug>]] — <status egy mondatban>

**Top-3 releváns episodic-emlék** (vault-search-fusion RRF, score>0.04):
- [<rrf-score>] [[<file>]] — <title>  (src: vault+agentmem / vault / agentmem)
- ...

**Vault-konszenzus a slug-ról** (KO-DB Top-K, multi-source ranking):
- ▸ `<subject>`  ·  <N> source · max conf <C>
  - <predicate> → <object> *(<source_type>, conf=<c>)*
  - ... (max 3 fact)
- ▸ `<subject-2>` ... (max 6 subject)

**Top-3 aktív task** (#project/<slug>):
- [ ] ...

**Mélyítés on-demand:**
- `vault-search-fusion "<query>" --top-k 5`            — **production-default**: RRF fusion vault-search + agentmemory, ~540ms, 77.5% avg R@5
- `vault-search "<query>" --top-k 5`                   — single-source, ~400ms, 54.5% avg R@5 (compat / agentmemory down)
- `vault-ko-query "<entity>" --top-k 5`                — strukturált multi-source fact (KO-DB)
- `vault-ko-query "<query>" --top-k 5 --semantic`      — **bridge** (B-1 ↔ B-2): semantic-search → KO-DB subject lookup; fallback LIKE-re ha Memgraph down

> Ready (~5K token).
```

### 4. On-demand semantic fetch (agent-flow)

Ha a session során a user kérdés specifikus témát érint (pl. "milyen Memgraph-konfigot használtunk?"), az agent **NE találja ki**, hanem hívja:

```bash
vault-search-fusion "Memgraph config docker-compose" --top-k 5
```

A returned chunk-okat foglalja bele a kontextusba, válaszoljon a citation-okkal.

### 5. Fallback (Memgraph down vagy chunks=0)

Ha `vault-search-fusion` üres / Memgraph + agentmemory mindkettő nem fut, **visszaesik a régi aggressive pattern-re** (SKILL.md.bak.20260513-pre-memgpt elérhető reference-ként). ENV-flag: `VAULT_SEARCH_MODE=grep` explicit override. Ha CSAK agentmemory down, a `vault-search-fusion` graceful-fallback-el vault-search-only mode-ra esik (`--no-fusion`-ekvivalens).

## Tokenmegtakarítás (mért, 2026-05-13 + 2026-05-17 KO-DB bővítés)

| Pattern | Token-budget | Latency | Recall (R@5 measured) |
|---|---|---|---|
| Régi aggressive (file-cat 5-7 fájl) | ~15-20K | ~30 sec olvasás | 100% (mindent betölt) |
| Lean v1 (working + vault-search) | ~5K | <10 sec semantic-fetch | **54.5%** measured (vault-search alone) |
| Lean v2 (working + vault-search + KO-DB Top-K) | ~5K | <10 sec (KO-DB ~50ms) | **~60-65%** estimated (KO-DB structured fact lift) |
| **Lean v3 (working + vault-search-fusion + KO-DB Top-K)** | **~5K** | **<10 sec** (~540ms semantic-fetch) | **77.5% avg measured** (RRF fusion vault-search + agentmemory, +23pp vs v1) |

A KO-DB-bővítés **nem növeli** a token-budgetet (cseréli a régi grep-fetch-et). Hozzáad:
- multi-source-corroboration jelzést (8 source ≠ 1 source)
- precise entity-fact lookup (port, version, file-path, dependency)
- cross-project consistency check egyszeri lekérdezésben

A v3 `vault-search-fusion` upgrade (2026-05-20) **nem növeli** a token-budgetet, csak a recall-t:
- +23pp R@5 vs v1 (54.5% → 77.5% measured average)
- +140ms latency-cost vault-search-höz képest (~400ms → ~540ms, parallel-call vault + agentmemory + <1ms RRF)
- ~570 MB disk-cost (agentmemory persistent storage `/var/lib/agentmemory/data/`)
- agentmemory.service systemd-managed, mirror-cron */10 min auto-ingestál új vault-fájlokat
- Graceful fallback ha agentmemory down (REST timeout) → vault-search-only mode
- Audit: [[../../../obsidian-vault/06-Audits/2026-05-20 Production-stack v2 — RRF fusion CLI + systemd + cron-mirror + cross-validation]]

A **3-5K token megtakarítás per session** + **3× gyorsabb startup** = 8 párhuzamos session-en heti ~80-100K token spórolva, **session-pickup time fele**.

## Kapcsolódó

- [[11-wiki/Auto-context-loading]] — DEPRECATED protokoll (a régi aggressive)
- [[11-wiki/sv-01-memory-architecture]] — 3-rétegű memory ADR
- [[11-wiki/11.11-session-protokoll]] — parancs-család
- [[00-Meta/Glossary]] — slug feloldás
- [[02-Projects/superintelligent-vault]] — B-2 sprint host
- [[.vault-memory/scripts/vault-search.py]] — semantic-fetch impl
- `vault-context-load` — Week 3 Day 2 új script (lásd lent)
