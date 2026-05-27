---
name: workflow-codebase-audit
description: Use for cold-start, time-boxed, multi-axis audits of unfamiliar codebases — take-home assessments, post-acquisition or due-diligence reviews, inherited-service onboarding, pre-refactor tech-debt sweeps. Dispatches the auditor subagent for the broad sweep, optionally fans out to security-auditor / debugger on top findings (only when --depth=deep), and renders ranked findings with reasoning chains and counter-evidence fields.
orchestrator: true
---

# Workflow: Codebase Audit (cold-start multi-domain sweep)

**Announce at start:** "Activating `workflow-codebase-audit` to run the cold-start audit sweep."

## When to invoke

- Take-home or technical assessment requiring a broad codebase review.
- Post-acquisition or due-diligence review of an unfamiliar repo.
- Inherited-service onboarding: "I just took ownership of this, what's the state of it?"
- Pre-refactor tech-debt sweep across a monorepo or service.

## When NOT to invoke

- Single-domain security audit → use `security-auditor` directly (depth-first, OWASP-focused).
- Known bug with a repro → use `/swe-workbench:debug` (root-cause + fix lifecycle).
- PR diff review → use `/swe-workbench:review` or `workflow-pr-review`.
- Code already familiar; you know what to look for → run targeted tools directly.

## Composition

This skill orchestrates; domain analysis is delegated to:

- `swe-workbench:auditor` subagent — broad multi-domain sweep (security, perf, reliability, tooling, testing).
- `swe-workbench:security-auditor` subagent — depth-first CVE + threat review; **deep mode only**, top-N security findings.
- `swe-workbench:debugger` subagent — root-cause + fix path on top-N reliability findings by rank; **deep mode only**.
- `swe-workbench:ticket-context` skill — prepended when a ticket ref is present in `$ARGUMENTS`.

## Phases

### Phase 1 — Clarify (only when --scope is absent)

Skip this phase entirely if `--scope` appears explicitly in `$ARGUMENTS` — including `--scope=all`, which means "all domains, no clarification needed."

Only when `--scope` is completely absent: ask the user which domains matter most (security, perf, reliability, tooling, testing), then proceed. If `superpowers:brainstorming` is available, invoke it to surface assumptions about the codebase before sweeping. If unavailable, ask directly: "Which audit domains do you want covered? (security, perf, reliability, tooling, testing — or all?)"

### Phase 2 — Dispatch auditor

Build a plain-prose prompt from the parsed flags:

> "Time-box: `<time-box>`. Scope: `<scope>`. Depth: `<depth>`. Top-N: `<top-n>`.
> Run a cold-start multi-domain audit of this codebase. Return findings in the full 11-field schema."

Pass this to the `auditor` subagent. The agent is read-only and self-paces to the time-box.

### Phase 3 — Schema validation

Every finding returned by the auditor must include all three reasoning fields:

- `root_cause` — the underlying code-level cause, not just the symptom.
- `reasoning_chain` — the step-by-step path from evidence to conclusion.
- `counter_evidence_considered` — what would falsify this finding, and why it doesn't.

**Drop any finding missing one or more of these three fields.** Surface the count: "Dropped N/M findings for incomplete reasoning schema."

### Phase 4 — Fan-out (depth=deep only)

Skip this phase entirely for `--depth=quick` and `--depth=standard`.

For `--depth=deep`:

1. Take the top-N security findings → invoke `security-auditor` subagent for depth-first CVE + threat analysis.
2. Take the top-N reliability findings by rank → invoke `debugger` subagent for root-cause + fix recommendation.

Wait for both agents to complete before proceeding to Phase 5.

### Phase 5 — Rank and render

**Ranking formula:** `severity_score × confidence × (1 / effort_score)` where:
- `severity_score`: Critical=4, High=3, Medium=2, Low=1
- `confidence`: 0.0–1.0 as declared by auditor
- `effort_score`: low=1, medium=2, high=3

**Output structure:**

1. **Ranked summary table** — one row per finding, columns: Rank | Severity | Domain | Title | File:Line | Confidence
2. **Per-finding `<details>` block** — full 11-field schema (see rendering template below)
3. **Tally** — `Critical: N | High: N | Medium: N | Low: N | Dropped: N`
4. **Fan-out addendum** (deep mode only) — security-auditor and debugger findings appended after the main table.

## Rendering template

```markdown
## Codebase Audit — <repo> — <date>

**Tally:** Critical: N | High: N | Medium: N | Low: N | Dropped: N (missing reasoning schema)

| Rank | Severity | Domain | Title | File:Line | Confidence |
|------|----------|--------|-------|-----------|------------|
| 1    | Critical | security | Unescaped user input in SQL query | src/db.ts:88 | 0.95 |
| 2    | High     | reliability | No timeout on outbound HTTP calls | src/client.ts:42 | 0.87 |

<details>
<summary>Finding #1 — Critical / security: Unescaped user input in SQL query</summary>

| Field | Value |
|-------|-------|
| **title** | Unescaped user input in SQL query |
| **severity** | Critical |
| **domain** | security |
| **file_line** | src/db.ts:88 |
| **symptom** | Attacker-controlled string interpolated directly into SQL |
| **root_cause** | `queryBuilder` skips parameterized binding when `rawMode=true` |
| **reasoning_chain** | 1. `req.query.id` flows into `queryBuilder(rawMode=true)` at line 42. 2. Raw mode bypasses `pg.escape()`. 3. Query executed at line 88 with unsanitized string. |
| **counter_evidence_considered** | Checked whether middleware pre-sanitizes input — it does not; `validateInput()` at line 20 only checks type, not content. |
| **confidence** | 0.95 |
| **effort** | low |
| **suggested_fix** | Replace `queryBuilder(rawMode=true)` with parameterized `queryBuilder({ params: [id] })` |

</details>
```

## Absolute rules

- **No edits.** This workflow is read-only. Never invoke `Edit`, `Write`, or any shell command that writes to disk.
- **Soft time-box.** The auditor self-paces. There is no hard kill; findings reported at natural completion.
- **Schema enforcement is non-negotiable.** Drop findings that lack `root_cause`, `reasoning_chain`, or `counter_evidence_considered`. Never invent or infer these fields from partial evidence.
- **Never invent findings.** If evidence is absent, omit the finding. Silence is correct; false positives erode trust faster than missed findings.
- **Fan-out only on deep.** Quick and standard modes stay single-pass. Do not invoke `security-auditor` or `debugger` unless `--depth=deep`.
