---
name: snap-review
description: >
  Review a GitHub pull request in read-only mode for material bugs,
  regressions, missing tests, architecture drift, security/privacy risk,
  performance risk, and merge blockers. Use when the user wants a PR reviewed
  before merge or before posting feedback.
---

Review a GitHub pull request in read-only mode. Findings first; no code edits.

## Process

1. Find the PR from current branch/session context, or ask for one.

2. Gather full review context: PR title/body, base/head refs, changed files, commits, checks, diff, comments, reviews, review threads, and all comment replies. Follow linked issues, specs, PRDs, breakdown comments, parent issues, and links found inside their bodies/comments/replies recursively when they affect scope, acceptance, blockers, or intent.

3. Review deeply:

   - Compare the diff against gathered intent, linked context, existing contracts, and repo conventions.
   - Account for prior review state. Do not duplicate findings already raised in PR reviews, comments, or threads unless the issue is still present and unresolved. If a prior finding was replied to or addressed, verify the current diff before repeating it.
   - Trace changed paths through callers, inputs, validation, errors, auth, permissions, persistence, concurrency, migrations, compatibility, runtime behavior, docs, and tests.
   - Inspect tests for real regression value. Good tests verify public behavior and would fail if the bug returned. Flag shallow tests, implementation-detail tests, excessive internal mocks, coverage padding, and tests that assert code shape instead of user-visible behavior.
   - Inspect architecture as a first-class review surface. Look for shallow wrappers, pass-through services, anemic public APIs, leaky adapter/domain coupling, vendor/framework/database shapes crossing into business logic, duplicated policy, local-port violations, brittle seams, and interfaces that make future changes harder.
   - File architecture findings when they create concrete future-change, correctness, testability, or maintainability risk.
   - Bad-pattern findings need evidence: violated local convention, repeated brittle shape, avoidable coupling, wrong abstraction boundary, or runtime/tooling mismatch.
   - Cite file/line refs where possible. If exact line refs are unavailable, cite file + changed function/section.
   - Do not invent findings. If impact is speculative, put it in `Risks / Unknowns`.
   - One finding per root cause. Deduplicate symptoms across files, tests, and CI.
   - Produce priority-labeled review findings with concrete impact and evidence. Look for material bugs, regressions, missing tests, security/privacy risk, performance risk, and merge blockers.

4. Report findings first using `references/template.md`. Use `No Findings` only when no material issue is found.

5. Ask before posting. If approved, post the same review body to GitHub and show the review/comment URL.
