---
name: repo-analysis
description: >-
  Dual-lens repo analysis: Creator View (knowledge, insights, home-repo
  comparison) + Engineer View (health, security, process). Two user-invokable
  depths (Standard / Deep); Quick Scan is triage-only. Link mining for curated
  lists. Fit separation via dual scoring lenses. Outputs to
  .research/analysis/<repo-slug>/.
---

<!-- prettier-ignore-start -->
**Document Version:** 5.0
**Last Updated:** 2026-04-15
**Status:** ACTIVE
<!-- prettier-ignore-end -->

**Shared conventions:** See `.claude/skills/shared/CONVENTIONS.md`

**`/analyze` router:** This skill is the repo-handler arm of `/analyze` — direct
invocation and router dispatch both supported. Handoff contract: the router
passes `{target, auto_detected_type: "repo"}` as if the skill were invoked
directly.

# Repo Analysis

Dual-lens analysis of external GitHub repositories. **Creator View** surfaces
what the repo understands, how it compares to your work, and where you should be
challenged. **Engineer View** assesses health, security, process, and adoption
fitness. Both views are always produced; Creator View comes first.

## Warm-up (shown at invocation)

Before any work begins, display:

```
/repo-analysis <target>
  depth:         <quick | standard | deep>  (default: standard)
  phases:        PHASE N of M  (M = 9 Standard, 10 Deep, 1 Quick)
  est. time:     Standard ~8-15 min | Deep ~20-30 min | Quick <30s
  output:        .research/analysis/<slug>/
  prior feedback: {replay per CONVENTIONS §18 if prior state file exists}
```

## Routing Guide

| You want to…                             | Use this                |
| ---------------------------------------- | ----------------------- |
| Analyze one external GitHub repo         | `/repo-analysis` (here) |
| Let router auto-pick repo vs site vs PDF | `/analyze <target>`     |
| Cross-repo synthesis across 3+ analyses  | `/synthesize`           |
| Audit the home repo (SoNash itself)      | `/audit-comprehensive`  |
| Research a domain or technology broadly  | `/deep-research`        |
| Explore design space before planning     | `/brainstorm`           |

## Critical Rules (MUST follow)

1. **Standard is the default user depth.** Full artifact set: clone + repomix
   - dimension wave + Deep Read + Content Eval + Creator View + Engineer View
   - Value Map + Coverage Audit + Tag Suggestion + Retro + Routing Menu. Deep
     adds the History Wave. **Quick Scan (`--depth=quick`) is triage state, not
     a peer user tier** — Standard and Deep are the user-invokable depths.
2. **Write-to-disk-first.** Every phase writes its output file before
   proceeding. Orchestrator verifies file existence, not return values.
3. **Bands over numbers.** Display categorical bands with score in parens.
4. **No silent skips.** After every SHOULD step, verify the expected output
   exists. If missing: retry once with mitigation, then report to user.
5. **Home repo guard.** If target matches
   `jasonmichaelbell78-creator/sonash-v0`, redirect to `/audit-comprehensive`.
6. **Rate limit safety.** Check `gh api rate_limit` before every API batch.
   Abort if `remaining < 200`.
7. **State file on every phase transition.** Long analyses WILL hit compaction.
8. **No TDMS auto-pollution.** TDMS intake is opt-in via routing menu only.
9. **Creator View is mandatory** for Standard/Deep. Quick Scan includes a
   lightweight creator lens. The creator lens captures what the repo KNOWS, not
   just its health.
10. **Conversational, not clinical.** Creator View MUST be written in
    conversational prose. Anti-goal: must NOT read like a technical manual.

## When to Use

- User invokes `/repo-analysis` with a GitHub URL
- Evaluate an external repo for adoption, learning, or inspiration
- Understand what a repo knows or teaches
- Structured health report for a dependency decision
- Triage of multiple candidates (Quick Scan each, then promote to Standard)

## When NOT to Use

- Cross-repo synthesis → `/synthesize`
- Home repo audit → `/audit-comprehensive`
- Domain / technology research → `/deep-research`
- Quick dependency check → `gh api` directly

> See [REFERENCE.md](./REFERENCE.md) for dimension catalog, tool stack, output
> schemas, absence patterns, Creator View specification (§14), process details
> (§15), and full guard rails (§9).

## Input

**Argument:** `/repo-analysis <github-url>`

**Flags:** `--depth=standard` (default) | `--depth=quick` | `--depth=deep` |
`--lens=adoption|creator` (override auto-detected primary lens)

**Output:** `.research/analysis/<repo-slug>/` — analysis.json (unified schema
v3.0, validated by `scripts/lib/analysis-schema.js`), findings.jsonl,
value-map.json, creator-view.md, summary.md, deep-read.md, content-eval.jsonl,
coverage-audit.jsonl, extraction-journal.jsonl entries. Handler-specific:
repomix-output.txt (gitignored), mined-links.jsonl (curated-list only),
trends.jsonl (re-analysis comparison).

**Schema contract:** analysis.json MUST validate against the unified Zod schema
in `scripts/lib/analysis-schema.js`. See CONVENTIONS.md §12.

---

## Process Overview

Standard (default) and Deep share the main pipeline; Quick is standalone triage.
There is no interactive gate between Quick and Standard/Deep — depth is picked
up-front via the `--depth` flag.

**Standard flow (M=9):**

```
VALIDATE    Guards         -> Home repo? Archived? Rate limits? Fork? Prior feedback replay (§18)?
PHASE 1 of 9  Clone+Repomix   -> Blobless clone, generate repomix IMMEDIATELY, verify
PHASE 2 of 9  Dimension Wave  -> Inline (<20 files) or agents (large repos)
PHASE 2b of 9 Deep Read       -> Read internal artifacts beyond code
PHASE 3.5 of 9 Content Eval   -> Evaluate embedded content (links, APIs, refs) — BEFORE Creator View
PHASE 4 of 9   Creator View   -> Load home context + Deep Read + Content Eval, compare, challenge
PHASE 5 of 9   Engineer View  -> Merge dimensions, compute bands, dual-lens scoring
PHASE 6 of 9   Value Map      -> Pattern + knowledge + content + anti-pattern candidates
PHASE 6b of 9  Coverage Audit -> Scan for unexplored content (interactive)
PHASE 6c of 9  Tag Suggestion -> Per _shared/TAG_SUGGESTION.md
SELF-AUDIT + ROUTING
```

**Deep flow (M=10):** inserts `PHASE 3 of 10 History Wave` (12-month temporal
analysis) between Phase 2b and Phase 3.5.

**Quick flow (M=1):**

```
VALIDATE   Guards       -> Home repo? Archived? Rate limits? Fork? Prior feedback?
PHASE 0 of 1 Quick Scan -> API-only, <30s, 18 dimensions + lightweight creator lens
ROUTING                 -> Queue for Standard | Extract | Done
```

---

## Quick Scan (Phase 0 — `--depth=quick` only)

API-only, under 30 seconds. 18 dimensions (QS-01 through QS-18). See
REFERENCE.md §1.1. Quick is triage, not a user tier.

**Process:** Validate → 3 parallel API batches → classify repo type (§5b) →
compute dimensions → score 6 summary bands → absence pattern classifier → write
artifacts → present inline.

**Lightweight creator lens (MUST):** After computing health dimensions, read the
repo description and README (Contents API, first 200 lines). Write 2-3
sentences: "This repo appears to understand/demonstrate/teach X." Teaser only,
not full Creator View.

**source_tier:** Repos emit `source_tier: "T1"` (first-party artifacts).

**Done when:** analysis.json exists AND creator lens sentences written.

---

## Clone + Repomix (Phase 1 of M)

1. Clone: `git clone --filter=blob:none --depth=1 <url>` to `/tmp/`
2. **Generate repomix IMMEDIATELY (MUST).** Run `npx repomix@latest --compress`
   and save to output directory. Verify file exists before proceeding. If
   repomix fails: retry once, then report. Do NOT silently skip — repomix is
   required for Extract routing.
3. For Deep: `git fetch --unshallow` or `--shallow-since="1 year ago"`.
4. Update state file.

**Done when:** clone path recorded AND repomix-output.txt exists and is
non-empty.

> See REFERENCE.md §15.1 for LFS, monorepo detection, tool availability.

---

## Dimension Wave (Phase 2 of M)

**Small repos (<20 files):** Analyze inline via Bash. Subagents cannot access
temp directories.

**Large repos (20+ files):** Copy clone to project workspace
(`.research/analysis/<slug>/source/`), spawn up to 4 concurrent agents. Verify
each agent's output file exists after completion; on 0-byte or missing, capture
task-notification result text and write it to the dimension file.

**Dimensions:** Security audit, architecture analysis, documentation quality,
test infrastructure. See REFERENCE.md §1.2.

**Done when:** all dimension files exist and are non-empty, with agent failures
logged (if any).

---

## Deep Read (Phase 2b of M — MUST for Standard/Deep)

A repo's knowledge lives in docs, examples, guides, notebooks, and referenced
resources — not just code. Skipping these is like reviewing a library by looking
at the building and ignoring the books.

**Artifact discovery (MUST):** Scan the clone for:

- Guide/tutorial documents (`guides/`, `docs/`, `examples/`, non-README `*.md`)
- Notebooks (`.ipynb` — methodology, not just code)
- Embedded SKILL.md / instruction files (monorepos with per-module docs)
- SOP/methodology documents (HARNESS.md, CONTRIBUTING.md details, architecture
  docs)
- Referenced external resources (arXiv papers, linked repos, datasets) —
  cataloged for Phase 3.5 evaluation

**Output:** `deep-read.md` listing what was found, read, and cataloged for Phase
3.5. For each read artifact, note knowledge not visible from code.

**Feed forward:** Deep Read findings feed into Creator View (Phase 4). The
Creator View's "What's Relevant To Your Work" section MUST reference specific
internal artifacts, not category-level observations.

**Done when:** deep-read.md exists AND all internal artifacts are cataloged
(read or deferred to Phase 3.5).

---

## History Wave (Phase 3 of 10 — Deep only)

12-month temporal analysis: commit velocity, contributor health, churn hotspots.
See REFERENCE.md §1.4 and §7 for temporal fingerprint spec.

**Done when:** history.jsonl exists AND temporal fingerprint written to
analysis.json.

---

## Content Evaluation (Phase 3.5 of M — MUST for Standard/Deep)

> **Phase renumbered from 4b to 3.5 in v5.0** (breaking change for existing
> state files — see Version History migration note). Execution order is
> unchanged; the number now matches the execution slot.

Evaluate the repo's embedded content for specific relevance to home context.
Runs BEFORE Creator View and feeds into it. A repo's value often lives in its
references, not its code.

Applies to ALL repo types (not just curated-list). For curated-list repos,
content IS the repo; for framework/library repos, content is internal docs; for
research repos, content is external papers and datasets.

Writes `content-eval.jsonl` (or `mined-links.jsonl` for curated-list) with one
entry per evaluated item:
`{category, name, url, relevance, applicability, home_connection}`. This output
feeds Creator View §2.

**Done when:** content-eval.jsonl (or mined-links.jsonl) exists AND every item
has a relevance rating AND the "feed to Creator View §2" handoff is ready.

> **Full detail** — depth tiers, structured-metadata filtering, fetch failure
> handling, per-type evaluation rubrics — see REFERENCE.md §15.4.

---

## Creator View (Phase 4 of M — MUST for Standard/Deep)

The primary analytical output. Written in conversational prose, not tables.
Informed by THREE upstream inputs: home repo context, Deep Read artifacts (Phase
2b), and Content Eval results (Phase 3.5). Do not write Creator View until Phase
3.5 completes.

**Home repo context loading (MUST):** `SESSION_CONTEXT.md`, `ROADMAP.md`,
`CLAUDE.md`, `.claude/skills/`, MEMORY.md entries. See REFERENCE.md §14.2.

**6 MUST-produce sections** (Section 2b required only for product repos):

1. What This Repo Understands (+ Blindspots)
2. What's Relevant To Your Work
   - 2b. Use-As-Is Verdict (product repos only — Adopt/Trial/Extract-only/Avoid)
3. Where Your Approach Differs (Ahead / Different / Behind)
4. The Challenge
5. Knowledge Candidates (T1 active / T2 systems / T3 lower)
6. What's Worth Avoiding

Write output to `creator-view.md`. **Self-verify:** re-read generated Creator
View; verify each home repo claim references something that exists.

**Done when:** creator-view.md exists AND all MUST sections written AND Section
2 references specific items from Deep Read + Content Eval.

> **Full specification** — style guide, section prompts, fit-badge derivation,
> anti-pattern rules — see REFERENCE.md §14.

---

## Engineer View (Phase 5 of M)

Health tables, scoring bands, absence patterns, adoption assessment. 6 summary
dimensions: Security, Reliability, Maintainability, Documentation, Process,
Velocity. Adoption: Adopt/Trial/Extract/Avoid.

Two scoring lenses computed (adoption + creator); both shown, primary marked.
Override with `--lens`. See REFERENCE.md §4.

**Done when:** engineer-view.md OR summary.md contains all 6 bands + absence
pattern verdict + adoption classification.

---

## Value Map (Phase 6 of M)

Generate `value-map.json` with four candidate types:

- **Pattern** — code, architecture, tooling to extract
- **Knowledge** — understanding, methodology, insights to learn (E0-E1)
- **Content** — specific items FROM the repo's content (tutorials, APIs, guides,
  papers) with direct home applicability. Promoted from `content-eval.jsonl`:
  any `high` relevance item MUST become a content candidate AND an extraction
  entry.
- **Anti-pattern** — cautionary lessons from Creator View §6. Each actionable
  warning MUST become an anti-pattern candidate.

All four use the same ranking fields (novelty, effort, relevance). Content
candidates include a `url`. Knowledge candidates use E0-E1. Anti-pattern
candidates use E0.

**Scope-explosion prompt:** For curated-list repos with **>100 entries**,
prompt:
`"Curated list has N entries. Evaluate all / top 50 by signal / custom scope?"`.
Soft user-confirmation; never hard-block.

Append relationships to `.research/reading-chain.jsonl`. Populate
`related_repos[]` and `cross_repo_connections[]` in value-map.json.

**Done when:** value-map.json exists AND all 4 candidate arrays present AND
content + anti-pattern promotion rules applied.

---

## Coverage Audit (Phase 6b of M — MUST for Standard/Deep)

After all artifacts are written, scan for content that exists in the repo but
was NOT analyzed. The safety net that catches edge cases. Interactive prompt:
Analyze all / Select categories / Skip. Record user decision in
`coverage-audit.jsonl` — never silently discard.

**Done when:** coverage-audit.jsonl exists AND every item has a `user_decision`
field (`analyze` / `skip`) or `status: "analyzed"`.

> **Full detail** — categories scanned, output format, re-analysis triggering —
> see REFERENCE.md §15.5.

---

## Tag Suggestion (Phase 6c of M — MUST for Standard/Deep)

Follow the canonical protocol in
[`.claude/skills/_shared/TAG_SUGGESTION.md`](../_shared/TAG_SUGGESTION.md). Per
CONVENTIONS §14: at least 3 semantic tags per entry, 8 categories, no upper
bound.

**Signal sources for repo-analysis**: `creator-view.md`, entry `notes`,
`engineer-view.md`, `mined-links.jsonl`, top dependencies from repomix output.

**Done when:** user-approved tags written to `analysis.json.tags` AND each
`extraction-journal.jsonl` row.

---

## Cross-Repo Extraction Tracking (MUST for Standard/Deep)

After Phase 6, update both files:

1. **`.research/extraction-journal.jsonl`** (machine-readable, unified v2.0
   schema shared with website-analysis). Remove stale entries for the repo;
   write fresh entries for all candidates.
2. **`.research/EXTRACTIONS.md`** (human-readable, generated). **Do NOT edit
   manually.** Run: `node scripts/cas/generate-extractions-md.js`.

Both are canonical: journal is the data source; EXTRACTIONS.md is the
regenerated reading interface.

**Done when:** `grep -c "$SOURCE" .research/extraction-journal.jsonl` >= 1 AND
script output confirms the source in EXTRACTIONS.md.

> **Full record schema + regeneration detail** — see REFERENCE.md §15.6.

---

## Delegation & Defaults

At every interactive gate, a default applies if the user does not choose. Record
the default explicitly in state so self-audit can verify.

| Gate                             | Default                                     |
| -------------------------------- | ------------------------------------------- |
| `--depth` unspecified            | `standard`                                  |
| Coverage Audit unanswered        | `skip all` (logged in coverage-audit.jsonl) |
| Tag Suggestion unanswered        | **never auto-approve** — block with prompt  |
| Scope-explosion prompt           | `top 50 by signal`                          |
| Routing menu unanswered          | `7. Done` (cleanup + invocation track)      |
| Prior Feedback Replay (CONV §18) | `continue unchanged` (logged as shown)      |

Auto-approve is forbidden for Tag Suggestion — tags require explicit user
judgment (CONVENTIONS §14.6).

---

## Per-Phase Artifact Gate (MUST)

After every phase, verify the output file exists and is non-empty before
proceeding. If a Write is rejected by a hook (security hook false positive on
analysis prose), immediately retry via Bash/Python heredoc.

**Verification:**
`[ -s ".research/analysis/<slug>/<artifact>" ] && echo PASS || echo FAIL`

---

## Guard Rails (top 5)

1. **Rate limit safety** — `gh api rate_limit` before every API batch; abort if
   `remaining < 200`.
2. **Home repo guard** — target matches `jasonmichaelbell78-creator/sonash-v0` →
   redirect to `/audit-comprehensive`.
3. **Large repo safety** — >5000 files or >500MB clone → confirm with user
   before proceeding.
4. **Fork detection** — archive + fork + low stars → flag as low-signal before
   Deep.
5. **Write-rejection bypass** — hook-rejected prose writes → retry via
   Bash/Python, never silently skip.

> **Full guard catalog** — LFS, monorepo, clone safety, framework detection,
> error handling — see REFERENCE.md §9.

---

## Self-Audit (MUST, before routing)

Run minimum floor per CONVENTIONS §8 plus domain checks:

1. Artifact presence (analysis.json, findings.jsonl, value-map.json,
   creator-view.md, summary.md, deep-read.md, content-eval.jsonl OR
   mined-links.jsonl, coverage-audit.jsonl, extraction-journal.jsonl)
2. Schema contract — analysis.json validates
3. Completeness — all ran phases produced output
4. Schema drift — `skillVersion` matches expected
5. Regression check — compare finding count delta vs prior analysis
6. REFERENCE.md contract — structure matches
7. Extraction journal — `grep -c "$SOURCE"` >= 1, EXTRACTIONS.md rebuilt
8. Tags populated — `analysis.json.tags` non-empty (user-approved)
9. Coverage audit decisions — every item has `user_decision` or `analyzed`
10. Phase ordering — state file `phases_completed` shows
    `phase-3.5-content-eval` before `phase-4-creator-view`, `phase-6c-tags`
    before `self-audit`
11. Prior feedback replay — `prior_feedback_shown: true` if prior state existed
    (CONVENTIONS §18)

Report failures to user before routing.

---

## Routing Menu

Presented after Standard or Deep. 8 options:

| Option                  | Action                                        |
| ----------------------- | --------------------------------------------- |
| 1. Extract value        | Load repomix + value-map. Present candidates. |
| 2. Send to TDMS         | Transform findings to TDMS. Opt-in only.      |
| 3. Deep-plan this       | Inject analysis as research context.          |
| 4. Save to memory       | Persist key findings as project memory.       |
| 5. Adoption verdict     | Full WR-01 through WR-06 assessment.          |
| 6. Explore insights     | Deeper conversation about Creator View.       |
| 7. Done                 | Cleanup, confirm artifacts, track invocation. |
| 8. Cross-repo synthesis | If 3+ repos analyzed, offer `/synthesize`.    |

---

## State File & Resume

State file: `.claude/state/repo-analysis.<repo-slug>.state.json`

Update after every phase. On re-invocation: offer Resume/Re-run/Compare. See
REFERENCE.md §8 for schema.

**v5.0 migration note:** Existing state files with `phases_completed` containing
`phase-4b-content-eval` will be auto-migrated to `phase-3.5-content-eval` on
next resume. Self-audit phase-ordering check accepts either label during
transition window (through v5.2).

## Compaction Resilience

Artifacts as checkpoints: analysis.json, findings.jsonl, summary.md,
value-map.json, dimension files all persist independently. State file enables
phase-level resume.

## Integration

- **Upstream:** `/deep-research`, `/brainstorm`, `/analyze` (router)
- **Downstream:** `/deep-plan`, `/synthesize`, TDMS, project memory
- **Neighbors:** `/audit-comprehensive` (home repo), dimension agents
- **Cross-skill contract:** MUST preserve `last_synthesized_at` field on
  `analysis.json` when writing — this field is set by `/synthesize` Phase 5 and
  must not be dropped by handler re-runs (v2.0 contract, Session #284).
- **References:** [REFERENCE.md](./REFERENCE.md), [ARCHIVE.md](./ARCHIVE.md),
  [\_shared/TAG_SUGGESTION.md](../_shared/TAG_SUGGESTION.md)

## Retro & Prior Feedback Replay

**Retro (per CONVENTIONS §10):** Before presenting the routing menu, ask: "What
worked well? What would you change next time?" Save to `process_feedback` in the
state file. Optional structured dimensions: `worked_well`, `would_change`,
`longest_phase`, `signal_quality`.

**Prior Feedback Replay (per CONVENTIONS §18):** On re-invocation for the same
target, replay prior `process_feedback` during VALIDATE and ask whether to
adjust approach. Log `prior_feedback_shown: true` in the new state file.

**Invocation tracking** — on Done routing, capture enriched context:

```bash
cd scripts/reviews && npx tsx write-invocation.ts --data '{
  "skill":"repo-analysis","type":"skill","success":true,
  "schema_version":1,"completeness":"stub",
  "origin":{"type":"manual"},
  "context":{"target":"TARGET_REPO","mode":"repo","depth":"DEPTH",
             "lens":"LENS","score":SCORE,"decisions":DECISION_COUNT,
             "candidates":CANDIDATE_COUNT}
}'
```

---

_v5.0 | 2026-04-15 | Skill-audit batch 2026-04-15-analysis-quartet Wave 2.
**Breaking:** Phase 4b → 3.5 (Content Eval) — state files with
`phase-4b-content-eval` in `phases_completed` auto-migrate on resume.
Structural: /analyze router ack, Warm-up block, Routing Guide, Delegation &
Defaults, consolidated top-5 Guard Rails, scope-explosion soft prompt, Done-when
gates per phase, PHASE N of M markers, enriched invocation tracking, Prior
Feedback Replay per CONVENTIONS §18, Tag Suggestion body replaced with
`_shared/TAG_SUGGESTION.md` reference. Detail extractions to REFERENCE.md §14
(Creator View full spec already present), §15.4 (Content Eval detail), §15.5
(Coverage Audit detail), §15.6 (Extraction Tracking detail). v4.2 footer moved
to ARCHIVE.md in Wave 1._

_v4.6 | 2026-04-13 | Session #278: Creator View Section 2b Use-As-Is Verdict as
MUST-produce for product repos. Populates analysis.json adoption_verdict /
adoption_blockers / adoption_recommendation._

_v4.5 | 2026-04-12 | Session #276: Per-phase artifact gate, self-audit +4 checks
(EXTRACTIONS.md presence, tags non-empty, coverage decisions recorded, phase
ordering in state file)._

_v4.4 | 2026-04-10 | PR #505 Gemini review: split Process Overview into
Standard/Deep and Quick Scan flows; removed stale "GATE Interactive" row._

_v4.3 | 2026-04-06 | Convergence: CONVENTIONS.md ref, self-audit phase, schema
drift fix, artifact path alignment, agent_budget removal, retro persistence,
invocation tracking. Per DECISIONS.md #1-20._

_v4.2 and earlier — see [ARCHIVE.md](./ARCHIVE.md)._

## Version History

| Version         | Date       | Description                                                                                  |
| --------------- | ---------- | -------------------------------------------------------------------------------------------- |
| 5.0             | 2026-04-15 | Skill-audit batch Wave 2 rewrite — phase renumber 4b → 3.5 (breaking).                       |
| 4.6             | 2026-04-13 | Creator View §2b Use-As-Is Verdict MUST for product repos (application/framework/tool-demo). |
| 4.5             | 2026-04-12 | Per-phase artifact gate + self-audit +4 checks.                                              |
| 4.4             | 2026-04-10 | Split Process Overview into Standard/Deep + Quick Scan.                                      |
| 4.3             | 2026-04-06 | Convergence: CONVENTIONS.md ref, self-audit phase, schema drift fix.                         |
| 4.2 and earlier | —          | See [ARCHIVE.md](./ARCHIVE.md).                                                              |
