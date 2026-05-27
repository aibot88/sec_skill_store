---
name: validation-pipeline
domain: meta
description: |
  [PROTOCOL] Cross-cutting validation chains. Defines which
  validators to run, in what order, with which triggers, across marketing /
  dev / design domains. Preloaded by lead agents (marketing-lead, dev-lead,
  design-lead). Pure reference — no triggers, not invoked by secretary.
---

# validation-pipeline

Shared validator-orchestration playbook for the three agency domains. Tells the lead WHICH validator to run WHEN and HOW to record it in `engagement/validation-log.md`. Leads invoke validators via the Task tool; this skill is read, not called.

## Core principles

1. **Validators run before handoff, not after.** On M/L tier, adversary (`adversary.py --consilium {M|L}`) provides the second-opinion check at acceptance time, but it does NOT replace lead's pre-handoff validator pass. Lead's first pass must already be complete and logged.
2. **Validation log is append-only.** One entry per validator per run, with verdict + findings count + resolution if findings addressed.
3. **Findings trigger re-dispatch, not hand-wave.** If validator flags ≥1 issue above "minor", dispatch the specialist who produced the artefact for fix, then re-run the validator on the fix ONLY.
4. **Scope to what changed.** Don't re-validate artefacts untouched by the engagement. Cost-efficiency matters — adversary on M/L is the second-opinion safety net, not a substitute for missing pre-handoff validator runs.

## Log format

Two artefacts work together: a per-validator JSON output (proof of run) and a markdown log indexing them.

### `engagement/validation-outputs/{validator}-iter-{N}-{timestamp}.json` (mandatory)

Every validator run produces an output file in this directory. The file is the validator's actual output (verdict, findings, metrics). Without this file, the run is presumed not to have happened — director rejects with `validator output missing — likely not run`.

Naming: `{validator-name}-iter-{N}-{YYYYMMDD-HHMMSS}.json` (e.g. `code-reviewer-iter-1-20260506-143211.json`).

Contents are the validator agent's JSON return value, captured verbatim.

### `engagement/validation-log.md` (index, append-only)

```markdown
# Validation log — {engagement-name}

## Iteration 1

### {validator-name}
- Ran on: {artefact path(s)}
- Triggered by: {reason — mandatory rule / risk flag / user criteria}
- Verdict: {clean | N findings}
- Findings summary: {short bullet list if any}
- Resolution: {specialist re-dispatched + fix applied + re-run clean | deferred with justification}
- **Output file**: `engagement/validation-outputs/{validator}-iter-1-{timestamp}.json` (REQUIRED — director cross-checks file exists)

### {next validator}
...

## Iteration 2
(appended after director reject + rework)
...
```

### Lead duty: capture validator output to file

Every Task-tool dispatch to a validator agent must end with the lead writing the agent's JSON return value to `engagement/validation-outputs/{name}-iter-{N}-{timestamp}.json`. This is non-optional. The lead's prompt to the validator should explicitly ask for JSON return value (matching the agent's documented schema).

If a validator returns text instead of JSON (older agent / human-readable mode) — wrap it: `{"format": "text", "verdict": "...", "raw": "..."}` and save. The wrapper is acceptable; missing file is not.

### Concurrency rules (preventing race corruption)

`validation-log.md` is written by the **lead only**. Specialists do NOT append to it directly — the lead aggregates after each Task return. This avoids POSIX `O_APPEND` non-atomicity for messages > 4 KB.

`validation-outputs/{name}-iter-N-{timestamp}.json` is per-validator-per-iteration with timestamp suffix → collision-free even under parallel dispatch. Each lead-side write is a single `Path.write_text(...)`, atomic.

`executor-reports/{name}.md` is per-specialist (one file per specialist). When the lead re-dispatches the same specialist for iter N+1, the specialist appends `## Iteration N+1` section — never overwrites prior. Reads happen between dispatches, so concurrent writes from the same specialist do not occur.

If the lead must dispatch ≥2 specialists in parallel that both touch the same artefact (rare, usually a project-side file like `tech-spec.md` lock), explicitly serialise — protocol does not currently model file-level locks. For pipeline parallelism, ensure each specialist's outputs land in disjoint paths.

### Director duty: cross-check files exist

For every validator listed in `validation-log.md`:
- File exists at the cited path? If no → REJECT `validator output missing — likely not run`.
- File parses as JSON? If no → REJECT `validator output corrupted`.
- File's `verdict` field matches what the log claims? If diverges → REJECT `validator-log discrepancy: log says {X}, output file says {Y}`.

Mechanical check is part of `handoff-precheck.py` (sub-check `validator-outputs`).

### Lead self-recovery from broken validator output (Tier 14)

If lead writes a malformed validator JSON (truncated, missing `verdict`, missing `methodology` for the numerical validators), there's no need to wait for director REJECT. Run before handoff:

```bash
python ~/.claude/scripts/validator-retry.py engagement/ --check --auto-quarantine
```

The script:
1. Reads every `validation-outputs/*-iter-{currentN}-*.json`.
2. For each file: confirms parseable JSON, presence of `verdict` (or `status`), and — for `accessibility-validator | performance-validator | security-auditor | ux-review | anti-pattern-detector` — `methodology`.
3. Broken files are moved to `validation-outputs/.quarantine/{name}.broken-{ts}.json` (audit trail preserved).
4. Stdout prints a Task-tool re-dispatch payload the lead can paste back to re-run only the broken validators.

Up to 2 retry rounds per validator per iteration before the lead must escalate (per re-dispatch loop cap below). The retry budget is per-validator-per-iter, not per-engagement: a broken file → quarantine → re-dispatch → new clean file = round 1 used.

Anti-pattern: editing the JSON file by hand to "fix" it. Quarantine + re-dispatch is the only valid recovery — hand-edits hide the original validator's actual finding.

## Domain matrix — mandatory validators

### Marketing

| Condition | Validator | Owner |
|---|---|---|
| ANY data claim (numbers, rankings, CTR, share) | `reality-checker` | always |
| ANY campaign recommendation / assumption | `skeptic` | always |
| Copy deliverable (landing, ad, email) | Implicit review by `marketing-content-lead`; log that it happened | always |

### Dev

| Condition | Validator | Owner |
|---|---|---|
| Auth / data access / external API / secrets / dependencies touched | `security-auditor` | mandatory |
| Any code-producing wave | `code-reviewer` | mandatory |
| Any code-producing wave's diff | `anti-pattern-detector` | mandatory |
| Tech-spec or tasks produced | `reality-checker` + `skeptic` | mandatory |
| User-spec + tech-spec + tasks produced | `completeness-validator` | mandatory |
| Tech-spec claims existing patterns/code | `skeptic` (additional sweep) | mandatory |
| Tasks reference files/functions | `reality-checker` on hallucinations | mandatory |
| Migration file present | `migration-validator` | mandatory |
| Deploy boundary crossed | `pre-deploy-qa` / `post-deploy-qa` | mandatory |
| `ux_heavy: true` | `ux-review` on screens + traces + handoff §6 | mandatory |
| Tests written | `test-reviewer` | recommended |
| Infrastructure change | `infrastructure-reviewer` | mandatory if infra work |
| CI/CD change | `deploy-reviewer` | mandatory if CI/CD touched |
| ≥2 specialists touch shared contract (API/type/schema) | Cross-validation note in handoff §4 | mandatory |

### Design

| Condition | Validator | Owner |
|---|---|---|
| Any UI deliverable | `/critique` (from `ui-ux-methodology`) | mandatory |
| Full UI flow (landing, multi-screen) | `/design-review` | mandatory |
| Any interactive surface (form, nav, CTA, modal) | `accessibility-validator` | mandatory |
| Brand claims / competitor claims | `reality-checker` | mandatory |
| Multi-screen consistency | Token propagation audit by `design-lead` manually | mandatory |
| `ux_heavy: true` (almost always for design) | `ux-review` on screens + traces + handoff §6 | mandatory |
| Brand-lead and product-lead share tokens | Cross-validation note in handoff §4 | mandatory |

## Execution patterns

### Parallel (default)

Independent validators run via parallel Task dispatches to save wall-clock time. Examples:
- dev: `code-reviewer` + `security-auditing` + `reality-checker` (different artefacts)
- design: `/critique` + `accessibility-validator` (different surfaces)

### Sequential (when validator input depends on prior validator)

Only when output of validator A is explicit input to validator B:
- `completeness-validator` AFTER `userspec-quality-validator` (needs validated user-spec)
- `post-deploy-qa` AFTER `pre-deploy-qa` (needs deferred criteria list)

### Re-dispatch loop

```
validator → finding → re-dispatch specialist → fix → re-run validator on fix only → record in log
```

Cap at 2 re-dispatches per finding per iteration. If 3rd re-dispatch needed, escalate: "finding cannot be resolved; defer with scope note OR mark as blocker and surface to director".

## When to skip (explicit permission)

You may skip a mandatory validator ONLY if:
- Criteria.md "Explicitly out of scope" covers it.
- User scope-sync waived it in writing.

Never skip silently. Log the waiver in validation-log.md:

```markdown
### security-auditing (SKIPPED)
- Reason: criteria.md §out-of-scope — "auth is unchanged, skip security audit"
- Waived by: user scope-sync 2026-04-20
```

Director will verify the waiver exists.

## Anti-patterns

- **Don't run validators after handoff.** Adversary at M/L acceptance provides cross-perspective second opinion, but does NOT substitute for lead's pre-handoff validator run — your first pass is your credibility.
- **Don't hide findings.** Every finding → resolution or deferral with justification.
- **Don't re-run the entire validator on partial fix.** Re-run on the fixed artefact only.
- **Don't skip `reality-checker` / `skeptic` because "the specialist is trustworthy".** Trust applies to humans; these validators exist because LLM specialists hallucinate.
- **Don't parallelize sequential dependencies.** Order matters when validator B needs A's output.
- **Don't skip `ux-review` on `ux_heavy: true` engagements** — that's the validator that keeps Wave-2-style visual regressions from making it past handoff.
- **Don't skip `anti-pattern-detector` on code waves** — catches skipped tests / dead code / hidden-tab fakes that other validators miss.
- **Don't accept Cross-validation as "all match" without the actual list.** The list is the proof; "trust me, they match" = phantom claim.
