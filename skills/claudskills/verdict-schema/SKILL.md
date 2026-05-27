---
name: dartai-verdict-schema
description: "Canonical verdict-only return schema for adversarial reviewer subagents. Reviewers emit compact ≤30-line verdict block; main loop parses verdict + blockers only. Use when: authoring or updating reviewer agent, building verdict consumer, debugging reviewer report parsing."
---

# Reviewer Verdict Schema (Canonical)

This document defines the **single source of truth** for the return shape every adversarial reviewer subagent emits. The main loop and orchestrator skills (e.g. `dartai:adversarial-quality-loop`, `workflow:loop-orchestration`) read **only** the fields defined here. Anything outside the schema is dropped at the boundary.

**Why verdict-only**: prose narrative across N reviewers per loop iteration bloats the main-thread context. The verdict block carries the same decision signal at ~80% token reduction. Detail still has a home — see `evidence_path`.

## Schema

| field          | type                  | required               | notes                                                              |
| -------------- | --------------------- | ---------------------- | ------------------------------------------------------------------ |
| verdict        | `pass` \| `fail` \| `warn` | yes               | single-token decision; `fail` blocks the gate, `warn` does not    |
| blockers       | `list[str]`           | required when `fail`   | one line each; include `file:line` refs when applicable           |
| advisories     | `list[str]`           | no                     | non-blocking nits, suggestions, follow-ups                         |
| confidence     | `high` \| `med` \| `low` | yes                 | reviewer self-rating; `low` is a signal to escalate or re-dispatch |
| evidence_path  | `str` (relative path) | no                     | path to a longer report file when depth is needed                  |

### Verdict values

- `pass` — no blockers, gate may proceed.
- `fail` — at least one blocker; gate must not proceed; `blockers` MUST be non-empty.
- `warn` — no blockers but advisories warrant attention; gate proceeds; orchestrator may surface advisories to the operator.

### Confidence values

- `high` — reviewer is sure; finding/no-finding is well-grounded.
- `med` — reviewer is reasonably sure; one or two ambiguities exist.
- `low` — reviewer is uncertain; orchestrator should consider re-dispatch with a different model or a tighter prompt, or escalate to a human.

### Optional `evidence_path`

When a finding genuinely needs more than a one-liner (e.g. a long stack-trace, a multi-step exploit chain, or a table of duplicate sites), write the detail to a file under `.dartai/reports/<task-id>/<reviewer-name>.md` and put the relative path here. The main loop will not read it; downstream tools or operators may.

## Wire format

Reviewer agents emit a single fenced YAML block as the **final message body**. No preamble, no postamble, no prose around it. Keep the entire block ≤30 lines.

````
```yaml
verdict: pass | fail | warn
confidence: high | med | low
blockers:
  - "<file:line> — <one-line description>"
advisories:
  - "<one-line nit or follow-up>"
evidence_path: ".dartai/reports/<task-id>/<reviewer-name>.md"  # optional
```
````

### Examples

**Pass with no notes:**

```yaml
verdict: pass
confidence: high
blockers: []
advisories: []
```

**Pass with advisories:**

```yaml
verdict: pass
confidence: med
blockers: []
advisories:
  - "src/auth.ts:42 — consider extracting role-check helper (used 3×)"
  - "no test for 0-length input on parseToken; happy path only"
```

**Fail with blockers:**

```yaml
verdict: fail
confidence: high
blockers:
  - "src/handler.ts:88 — SQL string-concat with user input (A03 injection)"
  - "test/handler.test.ts — missing assertion on error message"
advisories:
  - "src/handler.ts:120 — duplicate of util/parseQuery (LCI hit)"
evidence_path: ".dartai/reports/RXB0s0OPWWZF/code-quality-reviewer.md"
```

**Warn (advisory-only):**

```yaml
verdict: warn
confidence: med
blockers: []
advisories:
  - "test distribution 70/20/10 — slightly under target on adversarial cases"
```

## Length budget

The full block — including header, lists, and `evidence_path` — must be **≤30 lines**. If you cannot fit findings in that budget:

1. Collapse multiple related findings into one line with a count (e.g. "3× weak assertions in test/foo.test.ts").
2. Move detail into `evidence_path` and reference it.
3. Never split a single reviewer's output across multiple blocks.

## Consumer contract

The main loop and orchestrator skills:

- Parse `verdict` and `blockers` only.
- Treat `advisories` as informational; may surface or drop based on telemetry settings.
- Use `confidence: low` as a re-dispatch signal (per orchestrator policy).
- Read `evidence_path` only when explicitly requested by an operator.

Pass/fail gate semantics (preserved from prior prose-format reports):

- Any reviewer `verdict: fail` → gate fails; orchestrator collects `blockers` from all failing reviewers and routes them back to the implementer.
- All reviewers `verdict: pass` (or `warn`) → gate passes.
- Reviewers gated by `enabled_when` predicates are skipped when the diff does not match; skipped reviewers do not contribute to the AND.

## Authoring rules for reviewer agents

When updating a reviewer agent's "Report Format" / "Return" section:

1. Replace any prose-narrative template (`qa_report:`, `code_quality_report:`, `post_task_report:`, etc.) with a reference to this schema.
2. Specify in the agent's instructions: emit the YAML block defined above as the final message body, no preamble.
3. Keep the agent's *internal* analysis structure (review areas, attack vectors, etc.) — that shapes how the reviewer thinks. Only the *output* shape is constrained by this schema.
4. Map the reviewer's old verdict tokens to the new ones:
   - `PASS` / `pass` → `pass`
   - `FAIL` / `fail` / `REJECT` / `STOP` → `fail`
   - `NEEDS_WORK` / `WARNING` → `warn` (when no blocker is gate-breaking) or `fail` (when it is)
5. If the reviewer needs to express depth beyond ≤30 lines, write to `.dartai/reports/<task-id>/<reviewer-name>.md` and set `evidence_path`.

## Backward compatibility

Legacy reviewers emitting the old prose `*_report:` blocks remain readable but are deprecated. Orchestrators may log a one-time deprecation note and proceed by extracting `verdict` from the legacy block. New reviewer authors and edits MUST use the schema above.

## Reviewers using this schema

Always-dispatched (dartai plugin):
- `plugins/dartai/agents/qa-reviewer.md`
- `plugins/dartai/agents/code-quality-reviewer.md`
- `plugins/dartai/agents/post-task-reviewer.md`

Always-dispatched (workflow plugin mirrors):
- `plugins/workflow/agents/qa-reviewer.md`
- `plugins/workflow/agents/code-quality-reviewer.md`
- `plugins/workflow/agents/post-task-reviewer.md`

Always-dispatched (compound-review plugin):
- `plugins/compound-review/agents/correctness-reviewer.md`
- `plugins/compound-review/agents/maintainability-reviewer.md`
- `plugins/compound-review/agents/testing-reviewer.md`

Conditional (compound-review plugin — dispatched when diff matches):
- `plugins/compound-review/agents/typescript-strict-reviewer.md` (when diff touches `*.ts`/`*.tsx`)
- `plugins/compound-review/agents/cli-readiness-reviewer.md` (when diff touches CLI paths)

Not yet migrated (rationalization-trap-reviewer) — still emits structured JSON per its bespoke schema. Orchestrators treat absence of `verdict-file:` on stdout line 1 as legacy format and read the JSON body directly.

---

## Verdict File Delivery (file-streaming channel) 裁決檔派送

Reviewer subagents return their decision via a **verdict file written to disk**, not via stdout body. The loop driver consumes the file content (read fresh, parse line-oriented), not the subagent transcript. This eliminates per-iteration child-context bloat and lets the driver replay any gate decision from the verdict file alone.

### File layout 檔案佈局

| path                                            | written by                  | read by               |
| ----------------------------------------------- | --------------------------- | --------------------- |
| `.dartai/reports/<task-id>/qa.md`               | qa-reviewer                 | loop driver (Monitor) |
| `.dartai/reports/<task-id>/quality.md`          | code-quality-reviewer       | loop driver (Monitor) |
| `.dartai/reports/<task-id>/correctness.md`      | correctness-reviewer        | loop driver (Monitor) |
| `.dartai/reports/<task-id>/maintainability.md`  | maintainability-reviewer    | loop driver (Monitor) |
| `.dartai/reports/<task-id>/testing.md`          | testing-reviewer            | loop driver (Monitor) |
| `.dartai/reports/<task-id>/ts-strict.md`        | typescript-strict-reviewer  | loop driver (Monitor) |
| `.dartai/reports/<task-id>/cli-readiness.md`    | cli-readiness-reviewer      | loop driver (Monitor) |
| `.dartai/reports/<task-id>/security.md`         | post-task-reviewer          | loop driver (Monitor) |
| `.dartai/reports/<task-id>/verdict-summary.kdl` | aggregator                  | final gate decision   |

The directory is `.dartai/reports/<task-id>/` (consistent with existing `evidence_path` references). Filenames are fixed per reviewer role so the driver can scan a known set without listing.

`workflow:` orchestrator mirrors substitute `.workflow/reports/<task-id>/` for its own state dir but the file shapes are identical.

### File format (line-oriented, parseable by the loop driver)

Each verdict file is plain text, line-oriented:

```
verdict: pass|fail|warn
confidence: high|med|low
blocker: <file:line> <one-line description>
blocker: <file:line> <one-line description>
advisory: <one-line nit>
evidence: <inline body or relative path>
```

Rules:

- **Line 1** MUST be `verdict: <pass|fail|warn>` — single token after the colon.
- **Line 2** MUST be `confidence: <high|med|low>`.
- **Lines 3+** are zero or more `blocker:` lines (required when `verdict: fail`), followed by zero or more `advisory:` lines.
- **Trailing** `evidence:` line is optional. If the value starts with `./` or is a path (no spaces, no leading prose), the driver treats it as a path reference; otherwise the rest of the file (after `evidence:`) is the inline evidence body.
- Lines starting with `#` are comments and ignored.
- Trailing whitespace and blank lines are ignored.

Example (`.dartai/reports/abc123/quality.md`):

```
verdict: fail
confidence: high
blocker: src/handler.ts:88 SQL string-concat with user input
blocker: src/handler.ts:120 duplicate of util/parseQuery (LCI hit)
advisory: src/auth.ts:42 consider extracting role-check helper
evidence: ./quality-evidence.md
```

Example (pass with no notes):

```
verdict: pass
confidence: high
```

### Stdout contract 標準輸出契約

When a reviewer subagent uses the verdict-file channel, its stdout body MUST be **≤5 lines** and serve only as a pointer plus a one-line summary:

```
verdict-file: .dartai/reports/<task-id>/<filename>.md
verdict: <pass|fail|warn> (<short reason if fail/warn, else empty>)
```

The first line is the file path; the second is the one-line verdict for human-readable progress logs. Reviewers MUST NOT inline the YAML block from the wire format above when delivering via file — the file is the canonical channel. The ≤5-line cap leaves room for an optional `confidence:` line and one advisory headline if the reviewer chooses, but no more.

### Loop driver semantics 循環驅動語義

Drivers consuming the verdict-file channel:

1. **Clear the reports dir at task start**. Before dispatching reviewers for a new task, remove `.dartai/reports/<task-id>/` (if present) and re-create it empty. This is the **stale-verdict mitigation** — a previous run's verdict file in the same path would otherwise be read as the current run's gate decision.

2. **React to verdict files via Monitor, not stdout consumption**. Spawn each reviewer subagent in the background; use `Monitor` over the verdict-file path (or the parent reports dir) to detect file changes. Parse the file fresh on each notification — do NOT consume the subagent's stdout body into driver context.

3. **Prefer parse-on-completion over event polling**. When the harness emits a subagent-completion notification, parse the verdict file at that point. File-system event polling is a fallback for harnesses without completion notifications. This is the **missed-event mitigation** — completion notifications are the durable signal; file-system events alone can drop under load. If both are available, parse on completion AND keep the Monitor stream open for late writes.

4. **Gate on file content, not stdout body**. The gate decision is `verdict:` from line 1 of the file. The subagent's transcript is discarded after parsing. Replay is possible from the file alone — re-running a gate decision means re-reading the verdict file, no need to re-dispatch the reviewer.

5. **Aggregate to `verdict-summary.kdl`** after all reviewers report. Run `node ${CLAUDE_PLUGIN_ROOT}/scripts/aggregate-verdicts.js <task-id>` (or the equivalent relative path). The aggregator reads all role-fixed verdict files, computes the overall gate verdict (any `fail` → `fail`; any `warn` and no `fail` → `warn`; else `pass`), and writes `.dartai/reports/<task-id>/verdict-summary.kdl`. The aggregator is the only consumer that reads multiple verdict files at once.

### Backward compatibility 向後兼容

- Reviewers still implementing the in-stdout YAML wire format (above) remain readable. Orchestrators MUST accept either shape: file-channel reviewers expose `verdict-file:` on line 1 of stdout; legacy reviewers emit the fenced YAML block. The driver detects which by checking line 1 of stdout.
- Existing `evidence_path` references in agent files continue to work — `evidence_path` is the YAML-block field name; `evidence:` is the line-oriented field name in the verdict file. They carry the same payload.
- The fixed per-role filenames (`qa.md`, `quality.md`, `security.md`) replace the older `<reviewer-name>.md` convention for new gate decisions. Legacy paths are still readable for replay; new writes use the role-fixed names.
