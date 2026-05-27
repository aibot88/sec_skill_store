---
name: multi-source-research
description: "Pipeline for grounded research: gather (≥2 sources) → conflict-detect → synthesize-with-provenance. Cites K2 §3.1 (provenance per claim) + K2 §3.2 (multiview retrieval). Reuses the brainstorming <PROVENANCE-CONTRACT> (commit ebd136a) as the canonical provenance shape; reuses conflict-detector agent (this plugin) as the contradiction step. 多源研究管道：採集（≥2源）→衝突檢測→帶溯源綜合。 Use when: synthesizing claims from multiple docs/repos/papers, before writing a load-bearing assertion in a spec or design doc, fact-checking a load-bearing PR description, gathering evidence for an architectural decision, validating a claim that contradicts a Phase 0 high-confidence bullet. Skip when: a single authoritative source is sufficient (e.g., 'what is this function's signature' answered by lci:get_context alone), or the claim is non-load-bearing (typo fix, comment update)."
---

# Multi-Source Research Skill

Grounded-research pipeline. Default to **prefer ≥2 sources** for any load-bearing claim; route them through the conflict-detector before synthesizing; carry provenance through to the output. The pipeline is the value — single-source shortcuts are the failure mode this skill exists to prevent.

## Provenance

- **K2 design doc:** `docs/research/K2-knowledge-hygiene-from-papers.md` §3.1 (provenance per claim) + §3.2 (multiview retrieval rationale)
- **Source papers:** OmniMEM (`2604.01007`) for provenance-per-claim; RAGSearch (`2604.09666`) for multiview retrieval complementary-roles finding
- **Reused contract:** brainstorming `<PROVENANCE-CONTRACT>` block (commit `ebd136a`) defines the 5 provenance value forms — this skill emits the same shape, no parallel schema.
- **Reused agent:** `conflict-detector` (this plugin, `agents/conflict-detector.md`) is the contradiction step.

## Pipeline

```
                ┌───────────────────────────┐
                │  Step 1 — Gather sources  │
                │  prefer ≥2; minimum 2     │
                │  for load-bearing claims  │
                └──────────────┬────────────┘
                               │
                               ▼
                ┌───────────────────────────┐
                │ Step 2 — Conflict-detect  │
                │ invoke conflict-detector  │
                │ agent on the source set   │
                └──────────────┬────────────┘
                               │
                               ▼
              ┌───────────────────────────────┐
              │ Step 3 — Synthesize           │
              │ with-provenance               │
              │ each output claim carries the │
              │ <PROVENANCE-CONTRACT> tag(s)  │
              │ that ground it                │
              └───────────────────────────────┘
```

## Step 1 — Gather

**Input contract:** the topic / claim to ground, plus the load-bearing-ness signal (load-bearing → ≥2 sources required; non-load-bearing → escape valve below).

**Process:**

1. Decide the **source classes** appropriate for the claim:
   - **Code claims** → `mcp__plugin_lci_lci__search` for symbols + `Read` for context lines.
   - **Behavioral / runtime claims** → code source + at least one doc / test source.
   - **External / API / library claims** → official docs + at least one usage example in this codebase (or a second authoritative source if not used here).
   - **Decision / preference claims** → memory entries (`.dartai/memory/`, `CLAUDE.md`) + commit history (`git log`).
2. Gather **at least 2 sources** unless the escape valve applies.
3. For each gathered source, record the source record per the conflict-detector input contract:
   ```json
   {
     "id": "<stable id>",
     "source_text": "<verbatim or trimmed excerpt>",
     "provenance": "<file:path:line | memory:id | git:sha | web:url | guess>",
     "confidence": "<high | med | low>"
   }
   ```

**Escape valve — single source acceptable when:**

- The claim is **non-load-bearing** (won't change a downstream decision; e.g., "what's the function signature" before a typo fix).
- A single source is **structurally authoritative and uncontested** (e.g., the language spec for a syntax question; the source-of-truth schema file for a field type).

When the escape valve fires, emit a `single-source-by-design` note in the output so reviewers can audit the choice. Do NOT silently degrade.

**Output contract of Step 1:** an array of source records, length ≥ 2 (or length 1 with `single-source-by-design` note).

## Step 2 — Conflict-detect

**Input contract:** the source-records array from Step 1.

**Process:**

1. If length < 2 (escape-valve case), skip Step 2; record `conflict_check: skipped, reason: single-source-by-design`.
2. Otherwise, invoke the `conflict-detector` agent (this plugin, `agents/conflict-detector.md`) with the source-records array.
3. Receive the structured JSON output (see conflict-detector's Output Contract).

**Branching on the result:**

| `conflict_type` | Step 3 behavior |
|---|---|
| `no-conflict` | Proceed to synthesize. Carry all source provenance into the output. |
| `direct-contradiction`, `numeric-mismatch`, `temporal-mismatch`, `scope-mismatch` | Apply the agent's `recommended_resolution`. If `escalate-to-user`, **stop and surface the conflict-detector output verbatim** before any synthesize attempt. |
| `no-entity-match` | Treat as Step-1 error (caller selected non-overlapping sources). Re-gather with tighter entity selection. |
| `insufficient-sources` | Should not occur here (Step 1 enforces ≥2). If it does, treat as a contract bug — log and re-gather. |

**Output contract of Step 2:** the conflict-detector JSON output (or the skipped-marker for the escape-valve case).

## Step 3 — Synthesize-with-provenance

**Input contract:** the source-records array (Step 1) + the conflict-detector output (Step 2).

**Process:**

1. Write the synthesized claim(s) as **bullets**, mirroring the Phase 0 architect-summary shape from `ebd136a`.
2. Each bullet carries a `provenance` field per the `<PROVENANCE-CONTRACT>` (one of: `file:<path>:<line>` | `memory:<id>` | `git:<sha>` | `web:<url>` | literal `guess`). Multi-source bullets may carry multiple provenance tags as a list.
3. **Empty-handling rule (mirrors `<PROVENANCE-CONTRACT>`):** never omit `provenance`. If a bullet is unsupported by any gathered source — i.e., it is your synthesis-level inference — label it literal `guess`. Do not silently elevate inference to grounded claim.
4. If Step 2 returned a contradiction with `recommended_resolution: prefer-recent` or `prefer-authoritative`, the synthesized bullet:
   - Carries the winning source's provenance.
   - Adds an `overridden` field naming the losing source's id and the driving signal (one sentence).
   - Mirrors the brainstorming `Conflict-Detect Integration` audit-trail subsection from `ebd136a`: spec-level conflicts get an explicit "conflicting signal acknowledged and overridden" note, never a silent drop.

**Output shape (canonical):**

```json
{
  "synthesis": [
    {
      "claim": "<the synthesized assertion>",
      "provenance": ["file:src/cache.ts:42", "git:abc1234"],
      "overridden": null
    },
    {
      "claim": "<another synthesized assertion>",
      "provenance": "guess",
      "overridden": null
    },
    {
      "claim": "<an assertion that resolved a conflict>",
      "provenance": ["file:src/cache.ts:42"],
      "overridden": {
        "loser_id": "docs/cache.md",
        "signal": "implementation file authoritative over docs for runtime behavior"
      }
    }
  ],
  "sources_consulted": [
    {"id": "src/cache.ts:42", "provenance": "file:src/cache.ts:42", "confidence": "high"},
    {"id": "docs/cache.md", "provenance": "file:docs/cache.md:14", "confidence": "high"}
  ],
  "conflict_check": {
    "ran": true,
    "result": "<echo conflict_type from Step 2, or 'skipped:single-source-by-design'>"
  }
}
```

The `synthesis[].provenance` shape may be either a single string (single source) or an array (multi-source). The `<PROVENANCE-CONTRACT>` tag-vocabulary is identical; only cardinality differs.

## When This Skill Invokes the Conflict-Detector

| Trigger | What flows to conflict-detector |
|---|---|
| Step 2 with ≥2 sources | the Step 1 source-records array |
| Caller's escape-valve overrides single-source default | conflict-detector NOT invoked; `conflict_check: skipped` recorded |
| Caller is `verify-claims` command | one invocation per load-bearing claim in the target doc/PR |
| Caller is brainstorming Phase 1/2 surface-then-proceed | one invocation with the user's strategy pick + the conflicting Phase 0 bullet packaged as 2 sources |

## Anti-Patterns

- **Single-source synthesis without escape-valve declaration** — if the claim is load-bearing and you skipped the gather-≥2 step, you have shipped an ungrounded assertion. Either gather more sources or explicitly invoke the escape valve with a recorded note.
- **Provenance omission** — every synthesis bullet must carry `provenance`. Literal `guess` is the soft-fail; omission is the hard-fail.
- **Silent override** — if conflict-detector returned `prefer-recent` / `prefer-authoritative`, the losing source must appear in the bullet's `overridden` field. Dropping it without acknowledgement is the brainstorming `Silent Rationalization Through Conflict` anti-pattern reified at the research layer.
- **Skipping Step 2 because "the sources obviously agree"** — they may. Run Step 2 anyway when length ≥ 2; the cost is one agent call and the audit trail is worth it.

## Soft Guidance — Per-Claim Source Counts

Default toward **2 sources** for load-bearing claims. Prefer **3+ sources** when the claim is high-stakes (security-sensitive, breaking-change-implying, or contradicts a Phase 0 high-confidence bullet). The agent never enforces a hard maximum — gather what the claim warrants, but document why you stopped.

## Forward References

- **Multiview retrieval skill** (`TPqYid2TykLc`, deferred Tier-3) — will provide source-class diversity (dense + bm25 + symbolic + KG) for Step 1's gather. Until it lands, Step 1's source-class menu above is the baseline.
- **Citation-verifier agent** (`qvd3VBUROdw2`, deferred Tier-3) — will retroactively verify the `provenance` tags emitted by Step 3 (file:line still resolves, web:url still loads, git:sha still in history).
