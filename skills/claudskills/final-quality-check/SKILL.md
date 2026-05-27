---
name: final-quality-check
description: Install the quality line every pie passes through before going on display — wire CI/CD, E2E testing, design-system compliance, and visual-regression gates. Run once before /sell-slice; also invocable standalone on any project.
user-invocable: true
triggers: ["/bytheslice:final-quality-check", "/final-quality-check", "install the quality line", "wire the inspection station", "/bytheslice:scaffold-ci-cd", "/scaffold-ci-cd", "scaffold ci/cd", "set up ci", "bootstrap quality gates", "ci-cd stage"]
---
<!-- skills/final-quality-check/SKILL.md -->
<!-- Daily-prep skill (run before /sell-slice). Pizza-shop framing: install the quality line every pie crosses before landing on the display tray. Orchestrator-only: dispatches eight specialized agents to bootstrap the production-grade CI/CD + E2E + design-system-compliance + visual-regression baseline on a dedicated chore branch. Mode-detected (standalone vs sequential). -->

# Final Quality Check — CI/CD + Verification Baseline

This skill is the orchestrator for the CI/CD baseline. It does not write workflows itself — it **dispatches eight specialized agents** that each own one slice of the scaffold work. The orchestrator's job is detection, sequencing, user-input gating, and walking the completion checklist.

## Mode detection

This skill runs in one of two modes, auto-detected at startup:

- **Standalone** — no `docs/plans/00_master_checklist.md` at the project root. Adds CI/CD + E2E + design-system-compliance + visual-regression baseline to any project. Runs end-to-end, exits. No checklist coordination.
- **Sequential** — master checklist exists with a `## Prep` section. On completion, flip the `[ ] Quality line installed` row to `[x]` and surface: *"Quality line ready. Next prep step: `/open-the-shop`."*

Honor an explicit `--standalone` or `--sequential` flag if passed; otherwise auto-detect from disk state.

## Reference Files

| File | Purpose |
| --- | --- |
| [references/scaffold-artifact-templates.md](references/scaffold-artifact-templates.md) | Verbatim file templates for every CI/CD artifact (workflows, husky hook, PR template, regex sweep script, etc.). Every implementer agent reads this before writing. |
| [references/prd-ci-cd-checklist.md](references/prd-ci-cd-checklist.md) | **Project-wide runtime guardrails**, not scaffold-time setup. Master-checklist updates, CI gate alignment, deterministic pipelines, slice-per-PR rule, failure-artifact upload — these apply to every agent on every PR. Sub-block G of Phase 3 appends this content into the project rules file (CLAUDE.md / AGENTS.md) so every later stage skill picks it up automatically. |

## Subagent Roster

Each agent lives in its own file under `./agents/`. Read the file before dispatching.

| Phase | Agent file | Model | Effort | Mode |
|-------|-----------|-------|--------|------|
| 0 | [agents/scaffold-discovery.md](agents/scaffold-discovery.md) | haiku | medium | readonly |
| 0 | [agents/framework-detector.md](agents/framework-detector.md) | haiku | low | readonly |
| 3A | [agents/e2e-installer.md](agents/e2e-installer.md) | sonnet | medium | write |
| 3B | [agents/workflow-writer.md](agents/workflow-writer.md) | sonnet | medium | write |
| 3C | [agents/husky-installer.md](agents/husky-installer.md) | haiku | low | write |
| 3E | [agents/lint-config-writer.md](agents/lint-config-writer.md) | haiku | low | write |
| 3F | [agents/branch-protection-writer.md](agents/branch-protection-writer.md) | haiku | low | write |
| 4 | [agents/local-gates-runner.md](agents/local-gates-runner.md) | sonnet | medium | write |

The PR template (Phase 3D) is small enough that the orchestrator writes it directly from the templates file — no agent is needed.

## Inputs and Preconditions

- Repository exists with at least one app or package directory.
- Clean git working tree on `main`, OR explicit user OK to proceed dirty.
- `gh` CLI installed and authenticated (needed for PR + branch protection).
- A package manager (`pnpm` preferred) installed.

## Scenarios

| State | Action |
|---|---|
| Fully built (every scaffold artifact present and CI green) | Stop. Report "baseline already in place". Recommend `/bytheslice:sell-slice` for the next slice. |
| Partially built (some artifacts present, others missing) | Run discovery, dispatch only the agents that fill the gaps; never overwrite existing artifacts without surfacing to the user. |
| Not yet started (clean repo, no `.github/workflows/`) | Run the full pipeline end-to-end. |

`scaffold-discovery` reports `already_present_scaffold_artifacts`; the orchestrator uses that list to decide which Phase 3 sub-blocks to dispatch.

## Workflow

### Phase 0 — Discovery (parallel)

Dispatch in one batch:

1. `scaffold-discovery` — package manager, framework, monorepo tooling, existing workflows, DB presence
2. `framework-detector` — E2E framework choice + target apps

### Phase 1 — Clarifying Questions (Plan Mode)

Before any write, switch to **Plan Mode** and ask up to 5 focused questions:

1. Which app(s) are critical paths for E2E?
2. Should CI run on PR only, or PR + push to `main`?
3. Which suites are required blockers (`@feature`, `@regression-core`, `@visual`, full)?
4. Are deployments gated on green E2E checks?
5. Any restricted environments/secrets needed in CI?

**Always provide a recommended answer in available options.**

Wait for answers before continuing.

### Phase 2 — Branch Setup

- Create a dedicated branch: `chore/final-quality-check`.
- Never scaffold CI directly on `main` / `master`.
- Keep this PR minimal: baseline quality + smoke E2E only. No product features.

### Phase 3 — Implementation (sub-blocks A–F, sequential)

Each sub-block dispatches its agent, waits for the structured return, and commits before moving to the next.

| Block | Agent | What it produces |
|---|---|---|
| A | `e2e-installer` | Playwright installed, scripts in package.json, baseline @feature/@regression-core/@visual specs, `tests/visual/baselines/` |
| B | `workflow-writer` | `.github/workflows/{ci,e2e,e2e-coverage,design-system-compliance,db-schema-drift}.yml` |
| C | `husky-installer` | `.husky/pre-push` with the canonical gate chain |
| D | (orchestrator direct) | `.github/pull_request_template.md` from the templates file |
| E | `lint-config-writer` | eslint-plugin-tailwindcss config additions, `.stylelintrc.json`, `.gitignore` updates |
| F | `branch-protection-writer` | `scripts/setup-branch-protection.sh` (executable) |
| G | (orchestrator direct) | Project rules file (CLAUDE.md / AGENTS.md) "CI/CD Operational Rules" section populated from `references/prd-ci-cd-checklist.md` |

After each sub-block A–F, run a spec-compliance + code-quality review pass (reuse `sell-slice/agents/spec-reviewer.md` and `sell-slice/agents/quality-reviewer.md`). Fix findings before moving to the next sub-block. Sub-block G is a deterministic file write and does not need a review pass.

#### Sub-block G — Append CI/CD operational rules to the project rules file

The orchestrator (no subagent dispatch — this is a small, deterministic write similar to sub-block D's PR template):

1. Locate the project rules file. If `cook-pizzas` ran first, the file already exists at `CLAUDE.md` or `AGENTS.md` per Q12, with a placeholder section labeled "CI/CD Operational Rules — populated by `final-quality-check`" written by the `rules-assembler` agent.
2. If the placeholder is present, replace its body with the contents of `references/prd-ci-cd-checklist.md` (preserving the `[ ]` checkbox format verbatim — these are runtime gates the user and every agent walk on every PR, not one-time scaffold checks).
3. If the placeholder is absent (e.g. the project skipped `cook-pizzas` and ran `/final-quality-check` directly as an escape hatch), append a new section to the project rules file:
   ```markdown
   <!-- bytheslice: ci-cd-operational-rules-start -->
   ## CI/CD Operational Rules

   These rules govern how master-checklist updates, CI gates, and PR shape interact across every ByTheSlice run. They apply to every agent on every PR — not only to the one-time CI/CD scaffolding.

   <!-- contents of references/prd-ci-cd-checklist.md, verbatim -->
   <!-- bytheslice: ci-cd-operational-rules-end -->
   ```
4. **Idempotent re-runs.** If the section markers already exist, replace the body in place; never duplicate the section. User-edited content between the markers should be surfaced as a conflict via HITL `destructive_operation` rather than overwritten silently.
5. If neither `CLAUDE.md` nor `AGENTS.md` exists at the project root, create `CLAUDE.md` with just this section plus a one-line precedence header. Surface to the user that a fuller rules file should ideally be assembled by `/cook-pizzas`.

### Phase 4 — Local Verification Gates

Dispatch `local-gates-runner` to run lint, typecheck, design-system check, unit/integration, and all three E2E suites. The first run also generates initial visual baselines.

If any gate fails, fix on the same branch before proceeding. The Husky `pre-push` hook will enforce these on push automatically.

### Phase 5 — PR + CI/CD

1. Push `chore/final-quality-check` to remote.
2. Open the PR via `git-commit-push-pr` / `new-branch-and-pr` skill if available; otherwise `gh pr create`. PR description must list every artifact created.
3. Wait for CI to complete. If any required check fails, patch on the same branch and push until green.
4. Once CI is green, merge.

### Phase 6 — Closeout

1. After merge, update local `main`: `git checkout main && git pull --ff-only origin main`.
2. Delete the local branch: `git branch -d chore/final-quality-check`.
3. Delete the remote branch if not auto-deleted: `git push origin --delete chore/final-quality-check`.
4. Verify `git status` is clean on `main`.
5. Remind the user (once) to run `scripts/setup-branch-protection.sh` to enable required status checks on `main`.
6. Walk the **Completion Checklist** below and confirm every box is `[x]`.

## Final Output Format

After Phase 6, report:

1. Files created / updated (grouped: workflows, husky, pr template, scripts, tests, eslint/stylelint, package.json scripts).
2. CI triggers and required status checks.
3. Local verification commands and outcomes.
4. Confirmed presence of all scaffold artifacts (see checklist below).
5. PR URL and merged commit SHA.
6. Recommended next E2E flows to add (handed to `sell-slice`).
7. Reminder: run `scripts/setup-branch-protection.sh` once to enable required status checks on `main`.

## Hard Constraints

- **Never scaffold CI directly on `main` / `master`.** Always use `chore/final-quality-check`.
- **Never weaken or remove existing workflows.** This skill adds; it does not subtract. If existing workflows conflict, surface to the user and stop.
- **Completion checklist is mandatory.** The scaffold is not "done" until every box is `[x]`.
- **Sub-skill contract.** When invoked as a `type: ci-cd` stage by `sell-slice`, this skill is the entire stage. After completion, mark the stage `Completed` in `docs/plans/00_master_checklist.md`.
- **Subagent prompts live in `./agents/*.md`.** This SKILL.md is workflow only — never inline subagent prompts here.
- **No platform-specific rule references.** Do not write "cursor rules" or "claude rules" — use "rules file (cursor or claude)" if the distinction matters, or simply "project rules file".

## Triggers

Follow this skill whenever the user:

- runs `/final-quality-check` (escape hatch)
- says "scaffold ci/cd", "set up CI", "bootstrap quality gates", "set up Playwright + GitHub Actions"
- has `sell-slice` reach a `type: ci-cd` stage in the master checklist (auto-dispatch)

If the repo already has the baseline, stop and recommend `/bytheslice:sell-slice` instead.

---

## Completion Checklist

Run this checklist at the end of every run. Do **not** consider the scaffold "done" until every box is `[x]`.

### 1. Scaffold Artifacts Present

[ ] `.husky/pre-push` exists and is executable (includes `check:design-system` in gate chain).
[ ] `.github/pull_request_template.md` exists with E2E attestation, design-system-compliance, and visual-diff checklist items.
[ ] `.github/workflows/ci.yml` exists (full job order: typecheck → lint → design-system-compliance → unit tests → integration tests → @feature → @regression-core → @visual → db-schema-drift if applicable → build).
[ ] `.github/workflows/design-system-compliance.yml` exists (regex sweep → eslint-plugin-tailwindcss → stylelint).
[ ] `.github/workflows/e2e.yml` exists (`@feature` + `@regression-core` + `@visual` jobs with artifact upload on failure).
[ ] `.github/workflows/e2e-coverage.yml` exists (path-diff job named `E2E / coverage-check`; blocks on unreviewed visual diffs).
[ ] `.github/workflows/db-schema-drift.yml` exists IF project has DB, is absent if no DB detected.
[ ] `scripts/setup-branch-protection.sh` exists and is executable (includes all new required checks).
[ ] `.eslintrc.json` (or equivalent) has `eslint-plugin-tailwindcss` config additions.
[ ] `.stylelintrc.json` exists with CSS-file token checks.
[ ] `.gitignore` excludes `playwright-report/`, `test-results/`, `.playwright/`, and Vizzly diff artifacts.
[ ] Project rules file (`CLAUDE.md` or `AGENTS.md`) has a "CI/CD Operational Rules" section populated verbatim from `references/prd-ci-cd-checklist.md`, delimited by the `<!-- bytheslice: ci-cd-operational-rules-{start,end} -->` markers, so every later stage skill picks up the runtime guardrails automatically.

### 2. Test Suites and Scripts Present

[ ] `package.json` (root) has scripts: `test:e2e`, `test:e2e:feature`, `test:e2e:regression`, `test:e2e:visual`, `check:design-system`.
[ ] At least one `@feature`-tagged smoke spec exists.
[ ] At least one `@regression-core`-tagged sentinel spec exists.
[ ] Canary `@visual` tests exist — one per viewport (375 / 768 / 1280 / 1920).
[ ] `tests/visual/baselines/` directory is committed (may be empty on first scaffold; Vizzly populates on first run).
[ ] Playwright (or detected E2E framework) is installed and lockfile updated.
[ ] If a monorepo task runner exists (`turbo.json` / `nx.json`), the new E2E tasks are wired into it.

### 3. Local Gates Green

[ ] `pnpm lint` (or detected equivalent) passes.
[ ] `pnpm typecheck` passes.
[ ] `pnpm check:design-system` passes.
[ ] `pnpm test` (unit/integration) passes.
[ ] `pnpm test:e2e:feature` passes locally.
[ ] `pnpm test:e2e:regression` passes locally.
[ ] `pnpm test:e2e:visual` passes locally (baselines generated or confirmed up-to-date).
[ ] Husky `pre-push` hook fires on push (verify with a dry-run or trial push).

### 4. PR Created and Submitted

[ ] All work happened on branch `chore/final-quality-check` — never on `main`.
[ ] PR opened via `git-commit-push-pr` / `new-branch-and-pr` skill or `gh pr create`.
[ ] PR description lists every artifact created.
[ ] PR is targeted at `main` and is **not** draft.

### 5. CI/CD Passing on the PR

[ ] All required GitHub Actions checks have completed (no `pending` / `queued`).
[ ] Every required check is green. No skipped checks counted as passing.
[ ] If any check failed: read failing job logs, patch on `chore/final-quality-check`, push, repeat until all checks pass.
[ ] Final CI run reflects the latest commit on the PR head, not a stale SHA.

### 6. Branch Cleanup and Return to Main

Only after CI is fully green and the PR is merged.

[ ] PR merged into `main`.
[ ] Local `main` updated: `git checkout main && git pull --ff-only origin main`.
[ ] Confirm scaffold commits are present on `main` (`git log --oneline | head`).
[ ] Local `chore/final-quality-check` branch deleted: `git branch -d chore/final-quality-check`.
[ ] Remote `chore/final-quality-check` deleted: `git push origin --delete chore/final-quality-check` (skip if auto-deleted).
[ ] If a worktree was used: `git worktree remove <path>` and `git worktree prune`.
[ ] Final `git status` shows clean tree on `main`.
[ ] User reminded once to run `scripts/setup-branch-protection.sh`.
[ ] If invoked as a `type: ci-cd` stage by `sell-slice`, `docs/plans/00_master_checklist.md` row flipped to `Completed`.

### Done Criteria

The scaffold is delivered **only** when:

1. All six sections above are fully checked.
2. The orchestrator is back on `main` with a clean working tree.
3. All scaffold artifacts are present and committed on `main`.
4. CI passed on the merged PR head SHA.
