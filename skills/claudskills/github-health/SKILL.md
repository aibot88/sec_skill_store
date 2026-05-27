---
name: github-health
description: >-
  GitHub platform health assessment with 7 phases, per-finding triage
  (Fix/Defer/Skip/Suppress), scoped single-phase mode, session-begin quick
  check, and inline fix execution. Covers security alerts, CI/CD, dependencies,
  config, releases, insights, and PR health.
---

<!-- prettier-ignore-start -->
**Document Version:** 1.1
**Last Updated:** 2026-04-04
**Status:** ACTIVE
<!-- prettier-ignore-end -->

# GitHub Health -- Assessment & Resolution

**Decisions:** 28 (see `.planning/github-health-skill/DECISIONS.md`)
**Research:** `.research/github-health/RESEARCH_OUTPUT.md`

## Critical Rules (MUST follow)

1. **MUST** check `gh auth status` scopes before running any phase
2. **MUST** present findings before proposing fixes (assessment first)
3. **MUST** use per-finding triage — NEVER batch-apply fixes (Guardrail #2)
4. **MUST** report every API failure — NO SILENT FAILURES (Decision #22)
5. **MUST** check dedup guard (<30min) before running (Decision #9)
6. **MUST** check suppressions.json and skip suppressed findings
7. **MUST** follow CLAUDE.md Section 5 anti-patterns and Section 2 security
   rules
8. **SHOULD** read history JSONL for warm-up context (Decision #15)
9. **SHOULD** check ROADMAP.md before presenting fix options

## Routing Guide

| I want to...                  | Use                              |
| ----------------------------- | -------------------------------- |
| Quick status in session-begin | `--quick` (automatic)            |
| Full assessment with fixes    | `/github-health`                 |
| Single phase deep dive        | `/github-health --scope <phase>` |
| Check internal repo health    | `/ecosystem-health`              |
| Quick alert triage            | `/alerts`                        |
| Fix failing CI                | `/gh-fix-ci`                     |

## When to Use

- User explicitly invokes `/github-health`
- User asks about GitHub repo health, security alerts, or CI status
- Session-begin surfaces RED/YELLOW github-health quick check

## When NOT to Use

- For internal code quality metrics: use `/ecosystem-health`
- For quick alert triage: use `/alerts`
- For deep CI failure diagnosis: use `/gh-fix-ci`
- For SonarCloud issues: use `/sonarcloud`

## Modes

| Mode               | Scope argument | Phase                       |
| ------------------ | -------------- | --------------------------- |
| `--full` (default) | —              | All 7 phases                |
| `--quick`          | —              | Script only (session-begin) |
| `--scope security` | security       | Phase 1: Security           |
| `--scope actions`  | actions        | Phase 2: Actions            |
| `--scope deps`     | deps           | Phase 3: Dependencies       |
| `--scope config`   | config         | Phase 4: Config             |
| `--scope release`  | release        | Phase 5: Release            |
| `--scope insights` | insights       | Phase 6: Insights           |
| `--scope prs`      | prs            | Phase 7: PR Health          |

---

## Workflow

### Phase 0: Pre-Flight (MUST)

**Step 0a: Token Scope Check (Decision #25)**

Run `gh auth status`. Present coverage summary. If `repo` scope is missing:
offer limited assessment (community profile, topics, traffic for public repos
still work). Let user choose available phases or abort.

**Step 0b: Dedup Guard (Decision #9)**

Read last entry from `.claude/state/github-health-history.jsonl`. If <30min ago:
"Last run: [grade], [N]m ago. Re-run? [Y/n]". If declined, show last results.

**Step 0c: Warm-Up Context (Decision #15)**

```
GitHub Health Check
Last run: [grade] ([color]), [time ago]
Previous issues: [P0: N, P1: N, P2: N, P3: N]
Full assessment with triage: ~5-10 min. Single phase: ~2-3 min.
Running [mode] now...
```

**Done when:** Token scopes verified, dedup checked, warm-up displayed.

### Phases 1-7: Assessment

> Read REFERENCE.md for full check lists, API endpoints, and fix recipes per
> phase. Each phase: report ALL API failures (Rule #4). Announce progress:
> "Phase [name] complete (N of 7)."

| Phase           | Scope    | Key checks                                                                                                                 | Fixes                                                         | Delegation   |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ------------ |
| 1. Security     | security | Dependabot alerts, secret scanning, code scanning, validity checks, push protection, commit signing                        | Close false-positive alerts, enable validity checks (UI)      | —            |
| 2. Actions      | actions  | Workflow failures on main, TokenPermissions, PinnedDependencies, auto-merge approval, cache usage, CI trending             | Add permissions, pin SHAs, delete caches, add approval step   | `/gh-fix-ci` |
| 3. Dependencies | deps     | dependabot.yml coverage, ecosystem gaps, overrides, cooldown, security-update grouping, SBOM licenses                      | Update dependabot.yml                                         | —            |
| 4. Config       | config   | Rulesets, tag protection, environments, labels, community profile, topics, deleteBranchOnMerge, branches, issues, webhooks | Add topics/labels/templates, enable settings, create rulesets | —            |
| 5. Release      | release  | Release Please runs, config validation, manifest, tags                                                                     | —                                                             | `/gh-fix-ci` |
| 6. Insights     | insights | Traffic, commit activity                                                                                                   | None (display only, grade always A)                           | —            |
| 7. PR Health    | prs      | Stale PRs (>7d human, >3d bot), CI-blocked, merge conflicts, draft >14d, auto-merge stalls                                 | Close stale PRs                                               | `/gh-fix-ci` |

**Grading (Decision #10):** A=0 issues, B=P3 only, C=1-2 P2, D=any P1 or 3+ P2,
F=any P0.

**License flags (Decision #12):** WARNING: copyleft + unknown. INFO: FSL.
Ignore: MIT, Apache, BSD, ISC. See REFERENCE.md.

**Done when:** All phases (or scoped phase) graded, findings collected.

---

## Dashboard Display (MUST)

```
/github-health assessment -- [repo] -- [date]

SECURITY          [grade]  [N issues]
ACTIONS           [grade]  [N issues]
DEPENDENCIES      [grade]  [N issues]
CONFIG            [grade]  [N issues]
RELEASE           [grade]  [N issues]
INSIGHTS          [grade]  (informational)
PR HEALTH         [grade]  [N issues]

Total: [N] issues | P0: [n] | P1: [n] | P2: [n] | P3: [n]
```

If `--scope` was used, note which phases were skipped.

**Done when:** Dashboard shown, user acknowledges.

---

## Triage Loop (MUST for non-quick modes)

> Reminder: per-finding confirmation required (Guardrail #2). NEVER batch.

**ROADMAP check (MUST):** Before presenting findings, read ROADMAP.md. If a
finding is already tracked, note: "Already tracked: [location]."

**Triage mode selection:** Before entering the loop, ask: "Triage mode: (1)
Review each finding [default], (2) Fix all fixable / defer rest, (3) You decide
by severity. Choose [1/2/3]:" Mode 2: auto-fix all with available fixes, defer
everything else. Mode 3: fix P0/P1, defer P2, skip P3.

**Suppression check (Decision #11):** Read suppressions.json. Skip suppressed
findings (log: "Suppressed: [finding] (reason)").

**Per-finding presentation (mode 1):**

```
Finding [N] of [M] | Progress: [X] fixed, [Y] deferred, [Z] skipped

[SEVERITY] [Phase]: [description]
  Evidence: [source]
  Fix: [available fix or "manual steps required"]
  Recommendation: [Fix/Defer/Skip] because [rationale]

  [F]ix  [D]efer  [S]kip  [Su]ppress
```

**P0 suppression warning:** If user chooses Suppress on a P0: "Warning:
Suppressing a P0 finding is an anti-pattern. Confirm? [Y/n] If yes, expiry date
required."

**Decision revision:** User says "revise N" → re-present finding N for new
decision. Update state file.

**Fix execution (Decision #24):**

1. On first fix, create `github-health-fixes` branch from current HEAD
2. Each fix: execute + atomic commit. Report all API failures (Rule #4).
3. After all fixes: push branch (with user approval — Guardrail #7), create PR

**Defer collection (Decision #17):** Batch all deferred items → route to
`/add-debt` once after triage.

**Suppress writes (Decision #11):** Update suppressions.json with ID, reason,
expiry.

**UI-only fixes (Decision #23):** Step-by-step layman instructions with URLs.
See REFERENCE.md Recipe 14.

**Done when:** All findings triaged, fixes committed, deferred items batched.

---

## Verification (MUST)

Before presenting the summary, verify:

1. **Completeness:** All phases ran (or were explicitly scoped out). Report any
   that errored.
2. **Fix integrity:** Compare triage "Fix" decisions against commits on the fix
   branch. Flag any fix without a corresponding commit.
3. **Orphan check:** If fix branch exists but no PR was created, warn: "Branch
   `github-health-fixes` has N commits but no PR. Create PR? [Y/n]"
4. **Defer routing:** Verify deferred item count matches what will be sent to
   `/add-debt`.

**Done when:** All 4 checks pass or issues surfaced to user.

---

## Post-Triage Summary (MUST)

```
GitHub Health Triage Complete
  Fixed: [N] items ([list])
  Deferred: [N] items (routing to /add-debt)
  Skipped: [N] items
  Suppressed: [N] items
  PR: [URL if fixes were committed]
```

Update history JSONL with full run results including `phases` object (per-phase
letter grades). Triage state file persists for `/session-end` to report: "GitHub
health: N findings triaged (M fixed, K deferred)."

**Retro prompt:** "Any observations? (Inaccurate findings, fix recipes that need
updating, missing checks.) Enter feedback or 'none'." Save to state file
`process_feedback` field.

**Done when:** Summary displayed, history updated, feedback captured.

---

## Guard Rails

- **API failure:** Report which call failed and why. Continue with remaining
  phases. NEVER abort entire assessment for one phase failure.
- **Scope explosion:** If a fix requires >1 commit or >10 minutes, defer.
- **Duplicate runs:** Warn if <30 min since last run. Offer override.
- **Batch fixes prohibited:** Every fix requires individual user confirmation
  (Guardrail #2).
- **Push protocol:** NEVER push to remote without explicit user approval
  (Guardrail #7).
- **Graceful degradation:** If token scopes are insufficient, offer limited
  assessment with available phases rather than aborting entirely.
- **Pause/resume:** User says "pause" → save all triage decisions to state file,
  print progress ("N of M findings triaged, K fixes applied"), exit. On next
  invocation, offer to resume from state file.
- **Disengagement:** User says "stop" or "cancel" → save state, print summary of
  what was done, note incomplete status. Next invocation offers resume.

## Anti-Patterns

- Batch auto-fixing without per-item confirmation (violates Guardrail #2)
- Running during PR review (health reflects repo state, not PR diff)
- Suppressing P0 findings without resolution
- Re-running repeatedly to pollute trend data

---

## Compaction Resilience

- **State file:** `.claude/state/task-github-health-triage.state.json`
- **Update frequency:** After each finding triage decision
- **Recovery:** On resume, re-read state, skip triaged findings
- **Schema:**
  ```json
  {
    "findings": [{ "id": "str", "severity": "P0-P3", "phase": "str",
                    "action": "fix|defer|skip|suppress", "timestamp": "ISO" }],
    "mode": "full|scope",
    "grades": { "security": "A-F", ... },
    "started": "ISO",
    "process_feedback": "str|null"
  }
  ```

---

## Data & Artifact Contracts

| File                                                 | Purpose              | Writer              | Consumers                                |
| ---------------------------------------------------- | -------------------- | ------------------- | ---------------------------------------- |
| `.claude/state/github-health-history.jsonl`          | Run history + trends | Script + this skill | `/alerts`, session-begin, `/session-end` |
| `.claude/state/github-health-suppressions.json`      | Suppressed findings  | This skill (triage) | This skill (pre-triage filter)           |
| `.claude/state/task-github-health-triage.state.json` | Triage decisions     | This skill (triage) | `/session-end` (session summary)         |
| `scripts/run-github-health.js`                       | Quick mode script    | Manual              | session-begin hook                       |

---

## Version History

| Version | Date       | Description                                          |
| ------- | ---------- | ---------------------------------------------------- |
| 1.1     | 2026-04-04 | Skill audit: 19 decisions applied (verification, UX) |
| 1.0     | 2026-04-04 | Initial implementation from deep-plan                |
