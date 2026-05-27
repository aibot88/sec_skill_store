---
name: website-analysis
description: >-
  Creator-first website analysis skill. Dual-lens (Creator View + Engineer View)
  three-tier (Quick/Standard/Deep) analysis of arbitrary websites with
  superpowers-chrome extraction, compliance gates, and multi-mode operation
  (Page/Site/Expedition/Cross-site).
---

<!-- prettier-ignore-start -->
**Document Version:** 2.0
**Last Updated:** 2026-04-15
**Status:** ACTIVE
<!-- prettier-ignore-end -->

**Shared conventions:** See `.claude/skills/shared/CONVENTIONS.md`

**`/analyze` router:** This skill is the website-handler arm of `/analyze` —
direct invocation and router dispatch both supported. Handoff contract: the
router passes `{target, auto_detected_type: "website"}` as if the skill were
invoked directly.

# Website Analysis

Creator-first analysis of websites as knowledge artifacts. Mirrors
`/repo-analysis` architecture but designed for web content — what a site KNOWS,
ARGUES, and LINKS TO.

## Warm-up (shown at invocation)

```
/website-analysis <URL> [--mode=page|site|expedition] [--depth=...]
  mode:          page (default) | site | expedition | cross-site
  depth:         quick | standard (default) | deep
  phases:        PHASE N of M  (M = 6 Standard / Deep; 1 Quick; variable Expedition)
  est. time:     Quick ~30s | Standard 2-4m | Deep 5-10m | Expedition open-ended
  output:        .research/analysis/<site-slug>/
  prior feedback: {replay per CONVENTIONS §18 if prior state file exists}
```

## Routing Guide

| You want to…                                | Use this                   |
| ------------------------------------------- | -------------------------- |
| Analyze one website / page                  | `/website-analysis` (here) |
| Let router auto-pick repo vs site vs PDF    | `/analyze <target>`        |
| Cross-site synthesis across 3+ analyses     | `/synthesize`              |
| Test OUR webapp (local)                     | `/webapp-testing`          |
| Library / package documentation             | `context7` MCP             |
| Domain / technology research (query-driven) | `/deep-research`           |

## Critical Rules (MUST follow)

1. **Compliance check before ANY extraction.** Pre-flight runs first. HARD_BLOCK
   stops the skill with a minimal analysis.json explaining why.
2. **superpowers-chrome is primary extractor.** If unavailable, fall back to
   WebFetch + Playwright MCP + curl. Log a warning.
3. **Write-to-disk-first.** Every phase writes output before proceeding. Do not
   hold results in memory across phases.
4. **State file on every phase transition.** Update
   `.claude/state/website-analysis.<site-slug>.state.json` after each phase.
5. **Creator View is mandatory** for Standard/Deep. Written as conversational
   prose, NOT tables or clinical output.
6. **No silent skips.** If a SHOULD step fails, retry once, then report.
7. **Bands over numbers.** Display categorical bands with scores in parens.
8. **Home context MUST be loaded** for Creator View — SESSION_CONTEXT.md,
   ROADMAP.md, CLAUDE.md, `.claude/skills/`, MEMORY.md user entries.

## When to Use

- User provides a URL and wants to understand what the site knows
- Domain/technology scouting (JASON-OS Domain 02a)
- Evaluating a website as a knowledge source for ongoing work
- Comparing a site's perspective to our documented approach

## When NOT to Use

- Testing OUR webapp → `/webapp-testing`
- Package docs → `context7` MCP
- Simple URL fetch → `WebFetch`
- GitHub repo → `/repo-analysis`
- Cross-site synthesis → `/synthesize`
- Topic research → `/deep-research`

## Input

```
/website-analysis <URL>                        # Page mode, Quick Scan default
/website-analysis <URL> --depth=standard       # Standard depth
/website-analysis <URL> --depth=deep           # Deep depth
/website-analysis <URL> --depth=quick          # Explicit Quick Scan
/website-analysis --urls=URL1,URL2,...         # Site mode, explicit pages
/website-analysis <URL> --site                 # Site mode, auto-discovery
/website-analysis <URL> --expedition           # Expedition mode (HITL)
```

Re-invoking with the same URL auto-resumes from last completed phase.

## Output

`.research/analysis/<site-slug>/` produces these artifacts:

| Artifact                   | Phase     | Format / Notes                       |
| -------------------------- | --------- | ------------------------------------ |
| `analysis.json`            | 0+        | Core record (schema v3.0)            |
| `meta.json`                | 0         | Metadata snapshot (handler-specific) |
| `findings.jsonl`           | 2/3       | One JSON object per line             |
| `creator-view.md`          | 2         | Conversational prose, 7 sections     |
| `summary.md`               | 3         | Health bands                         |
| `value-map.json`           | 4         | Knowledge candidates ranked          |
| `deep-read.md`             | 1b        | Multi-page only                      |
| `content-eval.jsonl`       | 2         | One entry per evaluated link         |
| `coverage-audit.jsonl`     | pre-audit | Unexplored items + user decisions    |
| `extraction-journal.jsonl` | routing   | Append-only cross-source record      |

Full schemas in REFERENCE.md §1.

---

## Process Overview

```
VALIDATE      URL valid? Prior analysis? Tool check? Prior feedback replay (§18)?
PREFLIGHT     Compliance (robots.txt, cf-mitigated, RSS, HARD_BLOCK/WARN/PROCEED)
PHASE 0 of M  Quick Scan (navigate + eval + screenshot analysis)
GATE          Interactive "Run Standard/Deep?" — flags bypass
PHASE 1 of 6  Content extraction (WebFetch processed content)
PHASE 1b of 6 Multi-page (replaces Phase 1 in Site/Expedition mode)
PHASE 2 of 6  Creator View (7 sections, home context, 13 value axes)
PHASE 3 of 6  Engineer View (6 dimensions, 4-band scoring)
PHASE 4 of 6  Value Map (knowledge candidates ranked)
SELF-AUDIT    Verify artifacts, schema, completeness (9 dimensions)
ROUTING       Menu (7 options)
```

`M = 1` for Quick Scan only, `M = 6` for Standard/Deep, variable for Expedition.
Phase markers: `========== PHASE N of M: [NAME] ==========`

---

## Compliance Pre-flight (MUST — runs before extraction)

1. Fetch robots.txt via WebFetch (cache for session)
2. Check Anthropic user agents (ClaudeBot, Claude-User, Claude-SearchBot)
3. Check `cf-mitigated` header — WARN if Cloudflare detected
4. Check for RSS/Atom feeds — surface as option if found
5. Check `X-Robots-Tag` headers
6. Classify: `HARD_BLOCK` | `WARN` | `PROCEED`
7. HARD_BLOCK → minimal analysis.json with compliance reason, stop.
8. WARN → surface to user, require acknowledgment before continuing.

**Done when:** compliance status written to analysis.json AND either PROCEED
path taken OR HARD_BLOCK recorded.

> Full robots/UA handling, feed discovery, and error triage — REFERENCE §7.

---

## Extraction (Phase 1 of 6 / 1b of 6)

**Primary (superpowers-chrome available):** `use_browser navigate` →
`use_browser eval` → `WebFetch` → `curl -sI` (Deep).

**Fallback (no superpowers-chrome):** `WebFetch` → Playwright
`navigate + run_code` → `curl -sI` (Deep).

**Multi-page (1b):** Site or Expedition mode; extract per discovered/listed URL,
aggregate into `deep-read.md`.

**Done when:** raw extraction artifacts exist per analyzed URL AND
`content-eval.jsonl` seeded from outbound-link scoring.

---

## Modes

| Mode       | Flag           | Default behavior                                     |
| ---------- | -------------- | ---------------------------------------------------- |
| Page       | (default)      | Single URL; all three depths available               |
| Site       | `--site`       | Auto-discovery from root + top-scored internal links |
| Site       | `--urls=...`   | Explicit URL list; no per-page gates                 |
| Expedition | `--expedition` | HITL multi-hop (5-option gate per hop)               |
| Cross-site | (routing only) | Offered at routing menu if 3+ sites analyzed         |

**Site-mode scope-explosion soft prompt:** At **>50 pages** (auto-discovery or
explicit list), pause and prompt:
`"Site scope reached N pages. Continue / Limit to first 50 / Stop?"` User
decides; never hard-block.

**Auto-discovery 5-page gate:** No hard cap. Pause every 5 pages showing themes
/ links scored / knowledge candidates. User continues or wraps up. At page 20+,
advisory: `"Extensive coverage reached."`

> Full mode specs: Site → REFERENCE §11, Expedition → REFERENCE §10.

---

## Quick Scan (Phase 0 of M)

Runs on every invocation. Produces metadata snapshot, structural counts,
screenshot analysis (SHOULD), compliance status, absence-pattern detection
(detectable at Quick tier), lightweight Creator View teaser (2-3 sentences).

**Writes:** meta.json, analysis.json (Quick tier). Write to disk before gate.

**Gate:** Quick Scan is a **preview — not a peer user tier**. Standard produces
the full artifact set needed for `/synthesize` cross-source intelligence.
Prompt: `"Run Standard? (~5-10 min) [Y/n]"`. All depth / mode flags bypass this
gate.

**source_tier:** Websites span `T1`-`T4` based on editorial authority. Default
`T2`; handler may suggest a different tier from content signals.

**Done when:** meta.json AND partial analysis.json exist; creator-lens teaser
written.

---

## Creator View (Phase 2 of 6 — MUST for Standard/Deep)

Seven sections, conversational prose. Write creator-view.md before Engineer
View. Full spec in REFERENCE §4.

1. **What's Relevant To Your Work** — map to active projects
2. **What This Site Understands** — 13 value axes as backbone
3. **Voice and Editorial POV** — editorial stance, implied author
4. **Where Your Approach Differs** — productive vs fundamental divergence
5. **The Challenge** — what makes this site hard to use as knowledge
6. **The Warning** (OPTIONAL) — genuine risks only (ToS, bias, misinfo)
7. **Knowledge Candidates** — extractable items with type, confidence, effort

**Done when:** creator-view.md exists AND all MUST sections written AND
home-context claims reference actual files in SoNash.

---

## Engineer View (Phase 3 of 6 — SHOULD for Standard/Deep)

Six dimensions, 4-band scoring: Performance | Security Headers | Accessibility |
SEO | Technical Stack | Mobile Readiness. See REFERENCE §5.

**Done when:** summary.md contains all 6 bands AND findings.jsonl populated.

---

## Value Map (Phase 4 of 6)

Knowledge candidates ranked. Content candidates promoted from content-eval.jsonl
`high` relevance items. Anti-pattern candidates from Creator View §5 "The
Challenge". High-link-density trigger (SHOULD): when >40 unique external links,
suggest Expedition or cross-site synthesis.

**Done when:** value-map.json exists AND promotion rules applied.

---

## Tag Suggestion (MUST for Standard/Deep)

Follow the canonical protocol in
[`.claude/skills/_shared/TAG_SUGGESTION.md`](../_shared/TAG_SUGGESTION.md). Per
CONVENTIONS §14: at least 3 semantic tags per entry, 8 categories, no upper
bound.

**Signal sources for website-analysis**: `creator-view.md`, entry `notes`,
`engineer-view.md`, `meta.json`, outbound-link ecosystem.

**Done when:** user-approved tags written to `analysis.json.tags` AND each
`extraction-journal.jsonl` row.

---

## Delegation & Defaults

| Gate                             | Default                                |
| -------------------------------- | -------------------------------------- |
| `--depth` unspecified            | `standard`                             |
| Quick → Standard gate unanswered | `proceed to Standard`                  |
| Site scope-explosion (>50 pages) | `limit to first 50`                    |
| Coverage Audit unanswered        | `skip all` (logged in audit file)      |
| Tag Suggestion unanswered        | **never auto-approve** — block         |
| Routing menu unanswered          | `6. Done` (cleanup + invocation track) |
| Prior Feedback Replay (CONV §18) | `continue unchanged` (logged as shown) |

Tag Suggestion auto-approve is forbidden (CONVENTIONS §14.6).

---

## Guard Rails (top 5)

1. **Compliance first** — HARD_BLOCK stops extraction; no data collection.
2. **Rate limit safety** — respect `Retry-After`; back off on 429/503.
3. **Scope guards** — Site >50 pages → soft prompt; no silent auto-expand.
4. **superpowers-chrome fallback** — if primary fails, fall back gracefully with
   a WARN; never silently lose extraction fidelity.
5. **Write-rejection bypass** — hook-rejected prose writes → retry via
   Bash/Python, never silently skip.

> Full guard catalog — REFERENCE §7 (compliance), §15 (tool fallback).

---

## Self-Audit (MUST — penultimate phase)

Before presenting results, verify all 9 dimensions:

1. **Completeness** — all requested artifacts exist on disk
2. **Orphan detection** — no references to files that weren't written
3. **Schema integrity** — all JSON artifacts have `schema_version`
4. **Gap analysis** — Creator View sections reference actual content
5. **Functional verification** — state file updated to current phase
6. **Multi-agent** — dispatch code-reviewer on creator-view.md
7. **Regression** — if prior analysis exists, compare count deltas
8. **Contract** — analysis.json matches REFERENCE §1 schema
9. **Partial recovery** — detect stale artifacts from interrupted runs
10. **Prior feedback replay** — `prior_feedback_shown: true` if prior state
    existed (CONVENTIONS §18)

---

## Routing Menu

After Standard/Deep, present:

1. **Extract knowledge** — pick from value-map, write to
   extraction-journal.jsonl, regenerate EXTRACTIONS.md
2. **Start Expedition** — launch Expedition from analyzed page
3. **Deep-plan this** — inject analysis + creator-view as research context
4. **Save to memory** — persist key findings
5. **Explore insights** — deeper Creator View conversation
6. **Done** — list output files, remove state file, run retro
7. **Cross-site synthesis** — if 3+ sites analyzed, suggest `/synthesize`

> See REFERENCE §12.

---

## State File & Resume

Location: `.claude/state/website-analysis.<site-slug>.state.json`. Update after
every phase. State file stores `process_feedback` (nullable) from retro.
Artifacts as checkpoints: analysis.json, creator-view.md, meta.json persist
independently.

---

## Retro & Prior Feedback Replay

**Retro (CONVENTIONS §10):** Before the routing menu, ask: "What worked well?
What would you change next time?" Save to `process_feedback` in the state file.
Optional structured dimensions: `worked_well`, `would_change`, `longest_phase`,
`signal_quality`.

**Prior Feedback Replay (CONVENTIONS §18):** On re-invocation for the same URL,
replay prior `process_feedback` during VALIDATE and ask whether to adjust
approach. Log `prior_feedback_shown: true`.

**Invocation tracking** — at Done routing:

```bash
cd scripts/reviews && npx tsx write-invocation.ts --data '{
  "skill":"website-analysis","type":"skill","success":true,
  "schema_version":1,"completeness":"stub",
  "origin":{"type":"manual"},
  "context":{"target":"SITE_SLUG","mode":"MODE","depth":"DEPTH",
             "score":SCORE,"decisions":DECISION_COUNT,
             "candidates":CANDIDATE_COUNT}
}'
```

---

## Integration

- **Siblings:** `/repo-analysis`, `/document-analysis`, `/media-analysis`
- **Router:** `/analyze` (auto-detects website sources)
- **Companion:** `/synthesize` (cross-site, requires 3+ sites)
- **Consumers:** JASON-OS Domain 02a, `/deep-plan` (as research context)
- **Cross-skill contract:** MUST preserve `last_synthesized_at` field on
  `analysis.json` when writing — this field is set by `/synthesize` Phase 5 and
  must not be dropped by handler re-runs (v2.0 contract, Session #284).
- **Shared artifacts:** `.research/extraction-journal.jsonl`,
  `.research/EXTRACTIONS.md`, `.research/reading-chain.jsonl`

---

## Version History

| Version | Date       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.0     | 2026-04-15 | Skill-audit batch 2026-04-15-analysis-quartet Wave 2: /analyze router ack, Warm-up, Routing Guide, Delegation & Defaults, consolidated Guard Rails top-5, site-mode scope-explosion soft prompt (>50 pages), Done-when gates, PHASE N of M, Tag Suggestion → \_shared ref, Prior Feedback Replay per CONVENTIONS §18, structured retro dimensions, enriched invocation tracking (mode/depth/score/decisions/candidates), output list reformatted as table, mode section condensed to table + REFERENCE pointers, compliance pre-flight condensed to 8 steps + pointer to §7 |
| 1.2     | 2026-04-09 | CONVENTIONS alignment: SITE-ANALYSIS.md→creator-view.md, add summary.md, remove links.json from output list (Session #270 E2E test)                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 1.1     | 2026-04-06 | Convergence: CONVENTIONS.md ref, --depth= flags, retro persistence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 1.0     | 2026-04-06 | Initial implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
