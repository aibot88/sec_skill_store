---
name: ceratops-gh-repo-dependency-update
description: Process Dependabot, Renovate, security, and manual dependency update work through GitHub with Ceratops defaults, using scripted live repo and PR checks before merge decisions.
---

# Ceratops GH Repo Dependency Update

Handle dependency updates as an end-to-end maintenance loop. Prefer safe automation for security, patch, and minor updates, stop on ambiguous major upgrades, production risk, unavailable credentials, or paid requirements, and ground queue handling and merge decisions in the bundled GitHub helper scripts first.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target

<!-- SECTION SOURCE: templates/sections/gh-current-state.md -->

## GH Current State

- Use the shared helper package `ceratops_gh_current_state` for bundled GitHub current-state checks when it covers the next decision.
- Use `gh`, GitHub API, and `ceratops_gh_current_state` as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.

<!-- SECTION SOURCE: templates/sections/gh-artifact-contract.md -->

## GH Artifact Contract

- Apply this contract only when the repo has an external artifact, the current change affects a releasable artifact, or the final answer makes an artifact or no-artifact claim.
- Identify the real deliverable from the project instead of forcing Docker, PyPI, or any other registry by default.
- Capture or verify the artifact identity, registry target, version source, release policy, tag style, changelog or release-note source, and post-publish consumer check.
- In audit-only flows, verify and classify artifact state; do not publish or mutate registry artifacts unless the workflow explicitly moves into a ship or publish skill.
- Build, package, install, pull, run, or consume local artifacts enough to catch packaging and runtime failures before publishing or before making a local artifact-health claim.
- Publish external artifacts only when repo policy and the merged change require a release, tag, package, image, module, binary, or other public artifact.
- Derive versions from trustworthy project metadata and tag history instead of inventing semantics.
- Verify live release and registry endpoints after publishing or when auditing artifact state, including tags, digests, package pages, release pages, and published artifacts.
- Prefer registry-supported trusted publishing, OIDC, or another short-lived identity path over repository-stored long-lived publish tokens when supported by the real registry; keep any token-based fallback explicit and scoped.
- For PyPI publishes, prefer Trusted Publishing or another short-lived identity path over repository-stored long-lived tokens when supported, build the intended sdist and wheel, publish the intended version, verify the live PyPI version, install that exact version from PyPI locally, and run the smoke or documented consumer check against the published artifact instead of an editable checkout.
- For PyPI publishes that emit attestations or provenance, verify the metadata through PyPI or the selected verifier instead of relying only on upload success.
- For npm publishes, prefer trusted publishing when the package and runner meet current npm prerequisites, run the package's build and test path, publish the intended version, verify the live npm package and version, and verify provenance when npm generated it.
- For Docker or OCI image publishes, build locally, run a smoke test, publish the intended tags or digests, verify the live registry state, pull or consume the published image when relevant, and verify provenance or SBOM attestations when the selected publish flow emits them.

<!-- SECTION SOURCE: templates/sections/gh-findings.md -->

## GH Findings

- Classify only findings actually inspected in this run. Do not expand reporting to untouched queues unless they become the next actionable work or the user explicitly asked for full coverage.
- For each inspected finding, decide whether it is safe, fix low-risk items directly when in scope, and for every finding left open report its name or id, whether it is blocking, why it remains open, and the concrete work needed to clear it.
- Do not collapse retained findings into a generic healthy result.
- Re-check findings whose status may have changed because of actions taken in this run.
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Script Bundle

- Repo settings check: `python -m ceratops_gh_current_state repo-health --repo OWNER/REPO`
- PR readiness check: `python -m ceratops_gh_current_state pr-readiness --pr NUMBER_OR_URL`

## Inputs To Capture

- Target repo, branch, dependency PRs, package-manager ecosystems, and whether security updates are priority-only.
- Release policy, changelog expectations, local verification commands, and any missing inputs required by the GH artifact contract.
- Branch protection, required checks, code scanning, vulnerability alerts, auto-merge policy, and delete-branch policy.
- Whether `github-actions` updates are in scope and whether the repo enforces SHA pinning.

Infer missing inputs from local files and live GitHub state before asking.

## Boundaries

- Use this skill when the work is primarily dependency updates, alert cleanup, or dependency bot PR processing.
- If the repo is not yet published or lacks a usable remote, stop and use `$ceratops-gh-repo-create-and-publish`.
- If the work is broader than dependency maintenance or includes substantial non-dependency code changes, stop and use `$ceratops-gh-ship-change`.
- If only PR finalization remains for already-prepared dependency PRs, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect queue and risk

- Inspect git state, open PRs, dependency alerts, bot config, manifests, lockfiles, CI, security settings, tags, releases, and registry metadata.
- Check GitHub auth, registry auth, and connected tooling before asking for credentials.
- Build an update queue from live PRs, alerts, and local manifests, and classify each update by risk.

### 2. Research update evidence

- Use official package metadata, release notes, changelogs, advisories, compatibility notes, migration guides, and package-manager docs before merging meaningful updates.
- Use strong current reference repos only when ecosystem-specific update patterns are unclear and comparison will reduce risk.
- Do not infer that an update is safe from version number alone.

### 3. Re-check each candidate with scripts

- Run the bundled PR-readiness script before enabling auto-merge or merging a dependency PR.
- Run the repo-health script only when the queue changes or explicitly verifies repo posture surfaces such as branch protection assumptions, review-policy expectations, Actions permissions or SHA pinning, moderation or community-health claims, code-scanning posture, or other live GitHub settings the final result will rely on.
- Do not run the repo-health script for ordinary dependency PRs whose only moving parts are manifests, lockfiles, tests, CI results, and PR readiness.
- Re-run the relevant script after each merge or settings change instead of carrying stale queue assumptions forward.

### 4. Process updates recursively

- Prioritize security and low-risk updates unless ordering constraints require otherwise.
- Inspect the diff, manifest changes, lockfile changes, transitive changes, CI impact, and release impact for each update.
- Refresh lockfiles or generated dependency metadata using the project package manager unless the ecosystem explicitly expects manual edits.
- For `github-actions` updates, keep action refs on full commit SHAs with same-line version comments so Dependabot can keep updating them. If the repo enforces SHA pinning, do not merge a PR that downgrades a workflow back to tag-only refs.
- Run targeted tests first when useful, then full required checks before merge.
- Fix in-scope failures. If a failure is flaky, unrelated, or upstream, prove that classification with evidence.
- Decide from the fresh readiness check plus live GitHub state whether to merge now, enable auto-merge, or stop on a blocker.
- When this skill merges a dependency PR directly, use `gh pr merge --admin` with the allowed merge-method flag and `--delete-branch` when cleanup is intended and allowed.
- If checks, mergeability, and conversations are good and the only remaining blocker is the acting maintainer's own required review, follow the same documented self-merge exception as `$ceratops-gh-merge-pr` and use `gh pr merge --admin` instead of stopping.
- Use `gh pr merge --auto` only when GitHub should wait for remaining requirements instead of closing the PR immediately.
- After each merge, sync the default branch, re-check the queue, and continue until no actionable update remains, no progress is being made, or a real blocker is reached.

### 5. Publish and verify when required

- Execute the GH artifact contract when merged dependency updates require a release or artifact publish under the repo's policy.

### 6. Cleanup

- Close or classify stale, superseded, duplicate, or blocked dependency PRs only when the reason is proven.
- Delete merged branches when safe and allowed, sync the local default branch, and prune stale refs.

## Completion Gate

- Verify every dependency PR decision is backed by a fresh `python -m ceratops_gh_current_state pr-readiness` run.
- Verify live repo settings with `python -m ceratops_gh_current_state repo-health` when repo posture was part of the run.
- Verify live GitHub state for every dependency PR, alert, merge, check, branch, release, code scanning result, and branch protection gate touched.
- Verify local state: default branch, worktree, remotes, refs, lockfiles, generated files, temp paths, caches, credentials, and retained branches.

## Output Contract

Report only:

- dependency updates applied
- dependency updates skipped, retained, or blocked with exact reasons
- released or published artifact details when materially relevant to downstream use
- unresolved blockers or non-blocking debt
- anything important not verified
- exact credential step or paid requirement if blocked

## Example Invocation

`Use $ceratops-gh-repo-dependency-update. Process dependency PRs with the bundled live checks, merge safe updates, and stop only on real blockers.`
