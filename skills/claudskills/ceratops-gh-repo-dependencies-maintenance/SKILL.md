---
name: ceratops-gh-repo-dependencies-maintenance
description: Process Dependabot, Renovate, security, and manual dependency maintenance work through GitHub with Ceratops defaults, using scripted live repo and PR checks before merge decisions.
---

# Ceratops GH Repo Dependencies Maintenance

## Goal

Handle repository dependencies as an end-to-end maintenance loop. Prefer safe automation for security, patch, and minor updates, stop on ambiguous major upgrades, production risk, unavailable credentials, or paid requirements, and ground queue handling and merge decisions in the bundled GitHub helper scripts first.

## Context

### Script Bundle

- Dependency/security posture check when live GitHub queue, alert, label, security-setting, Dependabot config, workflow ref, manifest, lockfile, or local file posture is in scope: `python scripts/validation/github-validate-repo-artifact-contract.py --repo OWNER/REPO --select repo:dependency --select code:dependency --local-repo-path PATH`
- PR readiness contract check: `python scripts/validation/github-validate-pr-readiness-contract.py --pr NUMBER_OR_URL`

### Inputs To Capture

- Target repo, branch, dependency PRs, package-manager ecosystems, and whether security updates are priority-only, security-only, or part of a full dependency PR queue.
- Release policy, changelog expectations, local verification commands, and artifact-contract inputs only when a dependency update requires a release or publish.
- Branch protection, required checks, code scanning, vulnerability alerts, auto-merge policy, and delete-branch policy.
- Whether `github-actions` updates are in scope and whether the repo enforces SHA pinning.

Infer missing inputs from local files and live GitHub state before asking.

## Constraints

### Boundaries

- Use this skill when the work is primarily dependency updates, alert cleanup, or dependency bot PR processing.
- If the repo is not yet published, lacks a usable remote, needs substantial non-dependency code changes, or only needs PR finalization, stop because that work is outside this skill's scope.

### Workflow

#### 1. Inspect queue and risk

- Inspect git state, open dependency-bot PRs, dependency alerts, bot config, manifests, lockfiles, CI, security settings, tags, releases, and registry metadata.
- Check GitHub auth, registry auth, and connected tooling before asking for credentials.
- Build an update queue from live dependency-bot PRs, alerts, alert-linked update PRs, and local manifests, and classify each update by risk.
- Treat Dependabot or Renovate PRs as first-class queue items even when no security alert is open; do not report a dependency queue as clean from an alert-only check unless the task explicitly excludes routine dependency PRs.
- When the task spans multiple repositories, enumerate dependency-bot PRs and dependency alerts for every included repository before reporting that no actionable dependency work exists.
- For each queued PR or alert, capture whether it is security-linked or routine, the affected package or action, ecosystem, manifest or workflow path, update size, branch freshness, checks, review state, mergeability, and whether the change stays within the repo's dependency policy.

#### 2. Research update evidence

- Use official package metadata, release notes, changelogs, advisories, compatibility notes, migration guides, and package-manager docs before merging meaningful updates.
- Use strong current reference repos only when ecosystem-specific update patterns are unclear and comparison will reduce risk.
- Do not infer that an update is safe from version number alone.

#### 3. Re-check each candidate with scripts

- Run the bundled PR-readiness script before enabling auto-merge or merging a dependency PR.
- Include the live repo dependency selection only when the queue changes or explicitly verifies GitHub dependency/security posture such as vulnerability alerts, Dependabot security updates, Dependabot PR queue, code-scanning posture, dependency-review availability, or dependency labels.
- Include the code dependency selection only when explicitly verifying Dependabot config, workflow SHA pinning, manifests, lockfiles, local secret-pattern posture, or other repository-content dependency posture.
- Do not run broader GitHub, code, or artifact contract checks for ordinary dependency PRs whose only moving parts are manifests, lockfiles, tests, CI results, and PR readiness.
- Re-run the relevant script after each merge or settings change only when queue, alert, or PR readiness state is asynchronous or not already proven by the successful command result.

#### 4. Process updates recursively

- Prioritize security and low-risk updates unless ordering constraints require otherwise.
- Process already-open routine dependency PRs when they are in scope and low-risk; if the task is security-only, classify routine dependency PRs as intentionally retained with that exact scope reason instead of silently ignoring them.
- Inspect the diff, manifest changes, lockfile changes, transitive changes, CI impact, and release impact for each update.
- Refresh lockfiles or generated dependency metadata using the project package manager unless the ecosystem explicitly expects manual edits.
- For `github-actions` updates, keep action refs on full commit SHAs with same-line version comments so Dependabot can keep updating them. If the repo enforces SHA pinning, do not merge a PR that downgrades a workflow back to tag-only refs.
- Run targeted tests first when useful, then full required checks before merge.
- Fix in-scope failures. If a failure is flaky, unrelated, or upstream, prove that classification with evidence.
- Decide from the fresh readiness check plus live GitHub state whether to merge now, enable auto-merge, or stop on a blocker.
- When this skill merges a dependency PR directly, use `gh pr merge --admin` with the allowed merge-method flag and `--delete-branch` when cleanup is intended and allowed.
- If checks, mergeability, and conversations are good and the only remaining blocker is the acting maintainer's own required review, use the documented self-merge exception and `gh pr merge --admin` instead of stopping.
- Use `gh pr merge --auto` only when GitHub should wait for remaining requirements instead of closing the PR immediately.
- After each merge, sync the default branch, re-check open dependency-bot PRs and dependency alerts, and continue until no actionable update remains, no progress is being made, or a real blocker is reached.

#### 5. Publish and verify when required

- Execute the artifact contract when merged dependency updates require a release or artifact publish under the repo's policy.

#### 6. Cleanup

- Close or classify stale, superseded, duplicate, or blocked dependency PRs only when the reason is proven.
- Delete merged branches when safe and allowed, sync the local default branch, and prune stale refs.

## Done When

### Completion Gate

- Verify every dependency PR decision is backed by a fresh `python scripts/validation/github-validate-pr-readiness-contract.py` run.
- Verify dependency/security posture with `scripts/validation/github-validate-repo-artifact-contract.py --select repo:dependency --select code:dependency --local-repo-path PATH` when live GitHub queue, alert, label, security-setting, Dependabot config, workflow ref, manifest, lockfile, or local file posture was part of the run.
- Verify live GitHub state for dependency PRs, alerts, checks, and branch protection gates before decisions; after a successful mutation command, reread only asynchronous state or broader claims not proven by that command.
- Verify every dependency-bot PR and dependency alert in the inspected scope is either resolved, merged, blocked, out of scope by explicit task boundary, or intentionally retained with a concrete reason.
- Verify local state: default branch, worktree, remotes, refs, lockfiles, generated files, temp paths, caches, credentials, and retained branches.

### Output Contract

Report only:

- dependency updates applied
- dependency updates skipped, retained, or blocked with exact reasons
- released or published artifact details when materially relevant to downstream use
- unresolved blockers or non-blocking debt
- anything important not verified
- exact credential step or paid requirement if blocked

### Example Invocation

`Use $ceratops-gh-repo-dependencies-maintenance. Maintain dependency PRs with the bundled live checks, merge safe updates, and stop only on real blockers.`
