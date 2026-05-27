---
name: merge-innocent-pull-requests
description: |
  Use this skill to merge low-risk pull requests opened
  by automation bots across a list of GitHub repository
  owners: walk every repository, pick the open pull
  requests authored by `renovate`, `renovate[bot]`, or
  `github-actions[bot]`, keep only the ones where every
  required CI check has finished successfully, and merge
  them one by one. Stop after merging two hundred pull
  requests or after spending thirty minutes of wall-clock
  time on the run, whichever happens first. One run, one
  budget — then stop.
---

Treat the input as a list of GitHub account names —
  the OWNERS — supplied by the user or read from the
  current context; refuse to run if no owners are given,
  and do not invent owners from memory.

Use the `gh` CLI for every read and write against
  GitHub, so authentication, rate limits, and pagination
  are handled by the official tool rather than by ad hoc
  HTTP calls.

Record the wall-clock start time at the very beginning
  of the run and recheck it before every merge, because
  the run must stop as soon as thirty minutes have
  elapsed even if the merge counter is still below two
  hundred.

Maintain a merge counter that starts at zero and is
  incremented by one after every successful merge, and
  stop the run as soon as the counter reaches two
  hundred even if the time budget is not yet exhausted.

Iterate over the OWNERS in the order given, and for
  each owner list the public, non-archived, non-fork
  repositories (for example with
  `gh repo list <owner> --no-archived --source --visibility public --limit 1000 --json name,defaultBranchRef`),
  discarding mirrors, template repos, and repos whose
  description or topics mark them as deprecated,
  read-only, or moved.

For every surviving repository, list the open pull
  requests authored by an automation bot (for example
  with
  `gh pr list --repo <owner>/<repo> --state open --json number,author,isDraft,mergeable,mergeStateStatus,headRefName,baseRefName,reviewDecision`),
  and keep only the ones whose author login is exactly
  `renovate`, `renovate[bot]`, `github-actions`, or
  `github-actions[bot]`.

Discard every pull request that is a draft, that has
  merge conflicts (`mergeable` is `CONFLICTING`), that
  is blocked by required reviews (`reviewDecision` is
  `REVIEW_REQUIRED` or `CHANGES_REQUESTED`), or whose
  `mergeStateStatus` is `BLOCKED`, `BEHIND`, or
  `DIRTY`, because none of those states permit a clean
  merge.

For every remaining pull request, fetch the combined
  status of the head commit (for example with
  `gh pr checks <number> --repo <owner>/<repo> --json name,status,conclusion`),
  and keep the pull request only when every check has
  `status` equal to `completed` and `conclusion` equal
  to `success`, `neutral`, or `skipped`; treat any
  `failure`, `cancelled`, `timed_out`, `action_required`,
  `stale`, or still-running check as a hard reject.

Refuse to merge a pull request that has zero CI
  checks attached, because the contract of this skill
  is to merge only pull requests with all CI jobs
  green, and a pull request with no checks has no
  green signal at all.

Merge each surviving pull request with the merge
  method allowed by the repository, preferring squash
  when squash is enabled, otherwise rebase, otherwise
  a regular merge commit (for example with
  `gh pr merge <number> --repo <owner>/<repo> --squash --delete-branch`),
  and never override repository branch-protection
  rules to force a merge through.

If the merge call fails for any reason — branch
  protection, missing permissions, late-arriving check,
  network error — log the failure with the pull request
  URL and the exact error message, do not retry inside
  the same run, and continue with the next pull request.

Do not approve, comment on, label, assign, rebase,
  update, or close any pull request as part of this
  skill; the only write action permitted is the merge
  itself.

Do not open new pull requests, do not push commits to
  any branch, do not edit any file in any repository,
  and do not run any build; the skill exists purely to
  merge pull requests that automation bots already
  prepared.

Recheck the wall-clock budget and the merge counter
  after every merge attempt — successful or not — and
  break out of all loops the moment either limit is
  reached, so the run never overshoots its budget by
  more than one pull request.

Move on to the next repository in the current owner
  once every eligible pull request in the current
  repository is either merged or rejected, and move on
  to the next owner once every repository of the
  current owner has been processed.

Report at the end of the run a short factual summary:
  the number of pull requests merged, the number
  rejected with the dominant rejection reason, the
  wall-clock time spent, and the owner-and-repository
  pair where the run stopped, so the next run can
  resume from a known point.

Do not pick up a pull request that this skill rejected
  earlier in the same run, even if its CI turns green
  before the budget is exhausted, because re-evaluation
  inside a single run risks unbounded loops on flaky
  checks; let the next run of this skill reconsider it.
