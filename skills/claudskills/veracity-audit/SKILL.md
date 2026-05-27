---
id: veracity-audit
name: veracity-audit
type: skill
version: 1.0.0
domain: [devex]
platform: [none]
task: [review, testing]
maturity: draft
description: >
  Audit a data pipeline for Veracity and Value. Dispatches data-scientist,
  compliance-auditor, and data-engineer agents with project context injected
  at dispatch time. All source paths are supplied via flags — no defaults,
  no project assumptions.
  Subcommands: audit (full pipeline walk), score-check (scoring math only),
  gate-check (gate coverage only), source-trace <label> (single source end-to-end).
  Invoke when: "audit pipeline", "veracity check", "scoring math correct?",
  "check gates", "trace source", "verify quality gates", "formula correct?".
argument-hint: "audit | score-check | gate-check | source-trace <label> --config <path> --quality-config <path> --pipeline-dir <path> --scoring-dir <path>"
effort: max
model: opus
tools: Read, Grep, Glob, Bash
---

# Veracity Audit

Orchestrating audit skill for data pipelines. Dispatches specialized sub-agents
(`data-scientist`, `compliance-auditor`, `data-engineer`) with project context
injected at dispatch time. Produces inline findings; `--save` writes to `docs/audits/`.

**Covers:**

- **Veracity** — source reliability, scoring math integrity, quality gate completeness
- **Value** — primary score vs. legacy output correctness, blend-config wiring

---

## Required Arguments

All paths must be provided explicitly. The skill has no built-in defaults.

| Flag                      | Required                  | Description                                                     |
| ------------------------- | ------------------------- | --------------------------------------------------------------- |
| `--config <path>`         | yes (score-check, audit)  | Scoring/rating config file (YAML or JSON)                       |
| `--quality-config <path>` | yes (gate-check, audit)   | Data quality gate declarations file                             |
| `--pipeline-dir <path>`   | yes (audit, source-trace) | Directory containing pipeline step source files                 |
| `--scoring-dir <path>`    | yes (score-check, audit)  | Directory containing scoring/math source files                  |
| `--save`                  | no                        | Write findings to `docs/audits/veracity-<YYYY-MM-DD>.md`        |
| `--since <spec>`          | no, gate-check only       | Focus on checks added within this window (e.g. `"30 days ago"`) |

If a required flag is missing, print which flags are needed and halt.

---

## Pre-flight (always runs first)

Confirm the three required agents are installed:

```
~/.claude/agents/data-engineer.md
~/.claude/agents/data-scientist.md
~/.claude/agents/compliance-auditor.md
```

If any are missing, halt:

```
Missing agent(s): <list>
Run: dotclaude bootstrap
Then re-invoke this skill.
```

---

## Subcommand: `audit`

Full pipeline walk. Dispatches three agents in parallel, then synthesizes.

**Required flags:** `--config`, `--quality-config`, `--pipeline-dir`, `--scoring-dir`

### Step 1 — Read shared context

Read both config files in full. Retain their content to inject as a preamble into every agent prompt so all agents share the same source of truth.

### Step 2 — Dispatch three agents in parallel

#### Agent: data-engineer

```
Task: Audit source reliability across all pipeline steps.
Scope: <--pipeline-dir> (all step/stage source files), provider or adapter directories nearby
Preamble: [inject --config and --quality-config content]
Checks:
  - Ingestion steps: how are missing/null entity IDs handled? What happens on HTTP 429/503?
  - Time-windowed queries: is the cutoff calendar or epoch-based? Any timezone assumptions?
  - For each external source: schema version check? Fallback when unavailable? IDs validated before use?
  - Last-resort fallback case: when does it trigger silently vs. with a logged warning?
Output: P0/P1/P2 findings table per source, file:line.
  P0 = data loss/corruption, P1 = reliability gap, P2 = efficiency improvement.
Constraints: read-only
```

#### Agent: data-scientist

```
Task: Validate scoring math integrity.
Scope: <--scoring-dir> (rating/math source files), <--pipeline-dir> (transform and aggregation steps)
Preamble: [inject --config content in full]
Checks:
  - Tier/exponent selection: boundary conditions match config exactly (strict vs. loose comparisons).
  - Core adjustment formula: matches declared mathematical intent.
  - Credibility-weighting formula: trust horizon, curve shape, and [0,1] clamp.
  - Multi-source cap: applied in the correct order relative to other adjustments; cite the line.
  - Fallback case chain: for each case, state trigger condition, rating produced, and whether output
    is bounded to a sane range. Flag any case that can produce an out-of-range value.
  - Empty-collection edge case in aggregation: division-by-zero risk?
  - Primary score vs. legacy output: does any export path still apply a scale conversion
    (e.g. ×10 or /10) from the old output range? Grep service, export, and handler files.
Output: math integrity table (Formula | Expected | Code Behavior | Verdict | File:Line).
  Verdict: PASS / FAIL / AMBIGUOUS. FAIL entries include a one-line fix.
Constraints: read-only
```

#### Agent: compliance-auditor

```
Task: Gate completeness — coverage matrix of --quality-config declarations vs. enforcement code.
Scope: <--quality-config>, <--pipeline-dir> (gate/validation step), <--scoring-dir> (gate helpers)
Preamble: [inject both config file contents]
Checks:
  - Build coverage matrix for all named checks in quality config.
  - Flag DECLARED-NOT-ENFORCED (CRITICAL) and ENFORCED-NOT-DECLARED (WARNING).
  - Per-entity gate function: verify it is called for every entity in every run
    (trace call site in pipeline gate step, not just in unit tests).
  - Gate outcome persistence: verify pass/fail and reason are written to a durable store.
  - Threshold mismatch: compare threshold values in quality config vs. hardcoded literals in gate step.
  - Test coverage: flag any check with no corresponding test in the gate test file.
Output: coverage matrix (Check | Declared | Enforced | Blocking | Threshold Match | Test | File:Line)
  + gap list (Severity | Gap Type | Check Name | Detail | File:Line).
Constraints: read-only
```

### Step 3 — Synthesize

1. Deduplicate findings that share the same `file:line`.
2. Assign the highest severity from any agent that flagged the same location.
3. Output:

```
## Source Reliability
[data-engineer P0/P1/P2 table]

## Scoring Math
[data-scientist PASS/FAIL/AMBIGUOUS table]

## Gate Coverage
[compliance-auditor matrix + gap list]

## Summary
N CRITICAL · N WARNING · N INFO
Top action: <highest-severity finding's recommended fix>
```

If `--save`: write to `docs/audits/veracity-<YYYY-MM-DD>.md`.

---

## Subcommand: `score-check`

**Required flags:** `--config`, `--scoring-dir`

1. Read `--config` in full.
2. Dispatch `data-scientist` with Agent B spec above, config injected as preamble.
3. Output the math integrity table directly — no synthesis.

---

## Subcommand: `gate-check`

**Required flags:** `--quality-config`, `--pipeline-dir`

1. Read `--quality-config` and the pipeline gate step files in full.
2. If `--since` is present:
   - Run: `git log --since="<value>" --oneline -- <--quality-config>`
   - Extract check names added in recent commits.
   - Prepend to agent prompt: "Focus on these recently added checks: `[check-names]`. Verify each has enforcement AND a test."
3. Dispatch `compliance-auditor` with Agent C spec above.
4. Output coverage matrix and gap list directly — no synthesis.

---

## Subcommand: `source-trace <label>`

**Required flags:** `--pipeline-dir`, `--config`

1. Require one positional argument: the source label to trace. If missing, grep `--pipeline-dir` for provider/adapter import names and print a list, then halt.
2. Build a targeted file list by grepping `--pipeline-dir` and nearby adapter/service directories for the label.
3. Dispatch `data-engineer`:
   ```
   Task: Trace <label> end-to-end through the pipeline.
   Scope: [targeted file list] + --config for scoring context
   For each file:
     (a) Where does this source's data enter?
     (b) What schema fields are consumed?
     (c) What happens when the source returns stale, null, or out-of-schema data?
     (d) Is the source ID space validated against a reference set before use?
     (e) What is the downstream scoring impact if this source fails silently?
   Output: Stage | File:Line | Fields consumed | Failure mode | Mitigation (Y/N).
   Constraints: read-only
   ```

---

## Key Principles

1. **Audit, don't fix.** Findings only — let the user decide what to act on.
2. **Inject context.** Always read and inject the config files into agent prompts. Never let agents re-read them independently — shared preamble is the source of truth.
3. **Parallel where independent.** `audit` runs three agents concurrently; the other subcommands are single-agent.
4. **Evidence before verdict.** Every FAIL/CRITICAL must cite `file:line`. AMBIGUOUS is a valid verdict — do not guess.
5. **No project assumptions.** All paths come from flags. The skill works for any pipeline that has a scoring config, a quality gate config, and a multi-step pipeline directory.
