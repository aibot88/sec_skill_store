---
name: ceratops-contract-review
description: Review the Ceratops org, repo, code, PR readiness, and artifact health contracts against current GitHub, repo-content, and registry standards, then report proposed contract or checker updates for explicit approval.
---

# Ceratops Contract Review

## Goal

Review the Ceratops GitHub, code, PR readiness, and artifact health contracts deliberately instead of letting normal task skills drift into generalized upkeep. Compare current official GitHub, repo-content, and registry behavior against `contracts/`, then report proposed contract or checker deltas for explicit approval before any repo changes are applied.

## Context

### Script Bundle

- Org contract checker: `python scripts/validation/github-validate-org-contract.py --help`
- GitHub, code, and artifact contract checker: `python scripts/validation/github-validate-repo-artifact-contract.py --help`
- PR readiness contract checker: `python scripts/validation/github-validate-pr-readiness-contract.py --help`

### References

- Source-doc registry: `contracts/source-docs.json`
- Org deterministic contract: `contracts/github/github-org-deterministic-contract.json`
- GitHub repo deterministic contract: `contracts/github/github-repo-deterministic-contract.json`
- GitHub PR readiness deterministic contract: `contracts/github/github-pr-readiness-deterministic-contract.json`
- Code repo deterministic contract: `contracts/code/code-repo-deterministic-contract.json`
- Artifact deterministic contract: `contracts/artifacts/artifact-deterministic-contract.json`
- Non-deterministic review prompts: `contracts/github/*-nondeterministic-contract.md`, `contracts/code/*-nondeterministic-contract.md`, and `contracts/artifacts/*-nondeterministic-contract.md`

### Inputs To Capture

- Whether the run is routine automation upkeep or an explicit user-requested contract refresh.
- Current target scope inside the skills repo: `contracts/`, `scripts/validation/github-validate-org-contract.py`, `scripts/validation/github-validate-repo-artifact-contract.py`, `scripts/validation/github-validate-pr-readiness-contract.py`, `scripts/validation/github-collect-nd-evidence.py`, and repo docs that describe the contract structure.
- Which contract surfaces are actually in scope: GitHub org settings, live GitHub repo state, repo-content expectations, workflow hardening, release posture, artifact types supported by `ceratops-gh-repo-create-and-publish` or `ceratops-gh-ship-change`, or a documented no-artifact posture.
- The reference repositories used for standards comparison and which specific standards question each one informed.
- Which proposed changes require explicit approval and which findings require no repo change.
- Whether the current task should only stage updates into the active local `release/*` batch or also ship them through GitHub now.

Infer missing inputs from local repo state, live GitHub evidence, and the active automation prompt before asking.

## Constraints

### Skill-Specific Rules

- Routine runs must perform a bounded contract review across GitHub org, GitHub repo state, repo-content, workflow, security, and artifact-publishing surfaces already represented in `contracts/`.
- Do not use this skill to audit or repair the health of a specific repository. Use live GitHub, registry, official-doc, or reference-repo evidence here only when needed to decide whether a contract claim is current.
- Review current official docs, live product behavior, official API or registry metadata, and at most 2-3 current public third-party GitHub reference repositories relevant to the standards question. Use reference repositories only as pattern examples, not as health-audit targets, and separate no-extra-cost defaults from paid GitHub Code Security or Secret Protection features.
- Treat artifact surfaces as in scope only when `contracts/artifacts/artifact-deterministic-contract.json`, `ceratops-gh-repo-create-and-publish`, or `ceratops-gh-ship-change` claims to cover them.
- Keep durable standards in the contracts and `contracts/source-docs.json`; do not recreate a separate standards checklist file.

### Boundaries

- Use this skill when the work is to refresh the Ceratops GitHub, code, or artifact health contracts against current GitHub repository-management, repo-content, workflow, release, or artifact-publishing best practices.
- If the task is normal repo shipping, PR handling, dependency updates, repo-health work, or already-prepared skill shipping rather than contract upkeep, stop because it is outside this skill's scope.
- If the requested change would widen contract scope beyond the supported GH health surfaces, change default GitHub policy, change merge or review posture, change security posture, add mandatory paid features, or materially alter checker behavior, report the recommendation as approval-required and do not apply it without explicit approval.

### Workflow

#### 1. Inspect local contract state

- (D) Inspect current repo branch, worktree state, `contracts/`, the contract checker scripts, repo docs that describe contract structure, and the installed automation prompt when this run came from automation.
- Check GitHub auth, local git auth, and installed tooling before asking for credentials.
- Classify current differences as stale local dirt, proposed in-scope change, approval-required change, or not applicable.

#### 2. Refresh current source evidence

- Read `contracts/source-docs.json` and the affected contract files at the start of the audit and use them as the bounded checklist for the next evidence-gathering steps.
- Use local files, `gh`, GitHub API, `gh` help, package metadata, release metadata, and registry endpoints as the first-pass evidence for the GitHub or artifact behavior that the contracts encode.
- Check current official GitHub docs for repository-management settings, workflow policy, rulesets, actions, security, release behavior, and repository-content expectations wherever the next contract decision depends on them.
- Check current official Docker, GHCR, PyPI, or Python packaging docs only for artifact surfaces that are actually in scope.
#### 3. Audit the contracts

- Review `contracts/` and the checker scripts only where a contract claim depends on them.
- Look for duplicate guidance, contradictory defaults, stale GitHub setting names, stale required-file assumptions, stale repository-health expectations, stale workflow hardening guidance, stale artifact-publishing guidance, partial follow-through, or logic that belongs in a contract rather than prose.
- Keep repo docs aligned when stale: `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.

#### 4. Prepare approval request

- Prepare exact proposed contract or checker updates that align behavior with current official GitHub or registry terms.
- Prepare exact proposed file-reference updates when standard repo files, GitHub settings, workflow surfaces, or artifact-publish expectations were added, removed, or renamed.
- Prepare exact proposed low-risk deduplication or refactoring inside the contracts that preserves behavior and clarifies ownership between deterministic JSON, non-deterministic review prompts, contract-structure docs, and checker scripts.
- Prepare exact proposed source-doc registry updates when the contract needs a durable source that would otherwise bloat contract prose.
- Do not edit the skills repo checkout directly. For repo changes, use the worktree path required by the active repo-level instructions for the skills repo checkout.
- Do not apply any proposed change until the user explicitly approves that change.

#### 5. Align touched references

- If explicitly approved changes alter `contracts/`, contract checker scripts, `contracts/source-docs.json`, or repo docs that describe contract structure, use targeted readback, stale-reference search, and diff review for the touched scope.
- (D) If explicitly approved changes alter copied helper scripts or helper-runtime claims, run only the touched helper's own smoke command when that helper supports one.
- Verify changed contracts, contract checker scripts, `contracts/source-docs.json`, and repo docs that describe contract structure point at the current source of truth.

#### 6. Report approved local changes

- If explicitly approved updates were applied, report the ready worktree branch and any requested staging or publication as follow-up work rather than performing it here.
- If approval-required changes were found, report them without applying them.
- For routine automation runs with no repo change and no recommendation, complete without opening an inbox item.

## Done When

### Completion Gate

- Verify every changed in-scope contract artifact has targeted same-surface evidence.
- Verify repo changes remain in the worktree unless this contract-review task explicitly included another approved local mutation.
- Verify changed contracts, checker scripts, source-doc registry, and contract-structure docs remain aligned.

### Output Contract

Report only:

- applied explicitly approved contract or checker updates
- approval-required recommendations, blockers, or non-blocking debt
- intentionally retained leftovers or exceptions with reasons
- anything important not verified

For routine automation runs with no repo change and no recommendation, do not open an inbox item.

### Example Invocation

`Use $ceratops-contract-review to review the GitHub, code, PR readiness, and artifact health contracts against current GitHub, repo-content, and registry standards, then report proposed contract or checker updates for explicit approval.`
