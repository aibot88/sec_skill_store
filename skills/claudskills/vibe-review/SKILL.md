---
name: vibe-review
description: Use when a PR is open and CI green - dispatches a fresh subagent for two-stage code review (spec compliance then quality), posts findings to the GitHub PR as review comments with severity classification
---

# vibe-review

## Overview

Fresh subagent with isolated context reviews the PR diff. Two-stage: does it meet the spec? Then, is the code good? Output is posted to GitHub as a formal review.

**Core principle:** Review early, review strict, preserve main-thread context.

**Announce at start:** "I'm using the vibe-review skill to review the PR."

## When to use

- A PR is open (linked via `vibe-link`)
- CI is green (or `config.review_before_ci: true`)
- Before merge

Do NOT use if:
- Issue is tagged `hotfix` with ≥2 human approvals → skip to merge, review async after
- PR is from a human (not an agent workspace) — this skill is for agent-authored code

## Required

- PR URL + number
- Issue ID (for spec context)
- `gh` CLI authenticated
- Subagent capability — use Agent tool with `vibe-flow:vibe-reviewer`

## The process

### Step 1: Gather context

Fetch:
```bash
BASE_SHA=$(gh pr view <PR> --json baseRefOid --jq '.baseRefOid')
HEAD_SHA=$(gh pr view <PR> --json headRefOid --jq '.headRefOid')
```

Get issue spec:
- MCP `get_issue(issue_id)` → title, description, acceptance criteria

Get diff size:
```bash
gh pr diff <PR> --name-only | wc -l  # file count
gh pr view <PR> --json additions,deletions
```

If diff > 1500 LoC → flag to user, ask if they want to split review or proceed anyway.

### Step 2: Dispatch reviewer subagent

Use Agent tool with subagent_type `vibe-flow:vibe-reviewer`. Pass:

- Issue title + description + acceptance criteria
- PR URL, number, base/head SHAs
- Prompt from `references/prompt-templates.md` section 5 (code review prompt)

The reviewer gets ONLY this context — no session history, no prior decisions. This is the superpowers principle.

### Step 3: Parse review output

Reviewer returns `<VIBE-REVIEW>` block:
```
spec_compliance: pass|fail
quality_rating: approve|approve-with-minor|request-changes|reject
critical: [...]
important: [...]
minor: [...]
```

### Step 4: Post to GitHub

**Reviewer identity.** GitHub rejects `addPullRequestReview` with `APPROVE` or
`REQUEST_CHANGES` when the auth user is the PR author (error: *"Can not request
changes on your own pull request"*). Resolve the auth token before calling `gh`:

```bash
REVIEWER_ENV=$(yq '.review.reviewer_token_env // ""' .vibe-flow.yaml)
if [ -n "$REVIEWER_ENV" ] && [ -n "${!REVIEWER_ENV}" ]; then
  GH="GH_TOKEN=${!REVIEWER_ENV} gh"   # use bot PAT (e.g. vibeflow-reviewer)
else
  GH="gh"                              # default auth; may fail on own PR
fi
```

**A. If `approve` or `approve-with-minor`:**
```bash
eval "$GH pr review <PR> --approve --body \"\$BODY\"" 2>/tmp/gh_err || _fallback_comment
```
where `$BODY` contains the overall summary + minor items as nits.

**B. If `request-changes` or `reject` (any critical or spec fail):**
```bash
eval "$GH pr review <PR> --request-changes --body \"\$BODY\"" 2>/tmp/gh_err || _fallback_comment
```
Body includes:
- Spec compliance status
- All critical items (with file:line refs)
- All important items
- Minor items

**Fallback** (`_fallback_comment`): if the error matches `Can not (request changes|approve) (on )?your own pull request`, post the body as a plain comment instead — the review state on the PR will not change, but findings are still visible:
```bash
gh pr comment <PR> --body "$BODY"
```
Any other `gh` error → propagate, do not swallow.

Use `gh pr comment` or multiple inline `gh api` calls for file-level comments:
```bash
gh api repos/<owner>/<repo>/pulls/<PR>/comments \
  -f body="<comment>" -f commit_id="<HEAD_SHA>" \
  -f path="<file>" -F line=<N>
```

### Step 5: Update vibe-kanban issue

Post comment with review summary:
```
[vibe-flow] Review complete: <rating>
Critical: <count> | Important: <count> | Minor: <count>
Full review: <PR_URL>#pullrequestreview-<ID>
```

### Step 6: Update state.json, transition board, signal next

Based on rating, update BOTH `state.json` AND the vibe-kanban board status (via `update_issue`):

| Rating | state.json status | Board status | Next action |
|---|---|---|---|
| approve | `approved` | `ready_to_merge` if configured, else stay `in_review` | `vibe-merge` |
| approve-with-minor | `approved` | `ready_to_merge` if configured, else stay `in_review` | `vibe-merge` (minor items → follow-up issue, optional) |
| request-changes | `review_critical` | back to `in_progress` | `vibe-dispatch-fix` |
| reject | `review_critical` | back to `in_progress` | `vibe-dispatch-fix` (escalate tier) |
| spec fail | `review_critical` | back to `in_progress` | `vibe-dispatch-fix` (with spec gap summary) |

> vibe-kanban does not ship `ready_to_merge` out of the box, but projects can add custom columns. Read `.vibe-flow.yaml` → `statuses.ready_to_merge`:
> - If set → transition to that status on approve.
> - If unset → leave the issue in `in_review`; the signal for `vibe-merge` is `state.json.status = approved` + GitHub review APPROVED.
>
> Same for `statuses.in_progress` / `statuses.in_review` — never hardcode names, always resolve through config (or `list_issues` as last resort).

## Reviewer discipline (for the subagent)

The reviewer subagent is instructed (via prompt template) to:
- Be technical, direct, terse
- NEVER say "Great work!" / performative praise
- Classify every finding as critical / important / minor
- Reference specific file:line
- Push back with reasoning on critical only if it's technically justified (not aesthetic)
- Output in exact `<VIBE-REVIEW>` format

See `agents/vibe-reviewer.md` for agent definition.

## Cost optimization

Use a cheaper model for the reviewer when appropriate:
- T0/T1 issue → reviewer can be `sonnet-4.6-medium` (cheap, small diff)
- T2 issue → reviewer `sonnet-4.6-high`
- T3/T4 issue → reviewer `opus-4.6` (critical work needs strong review)

**Never review with a weaker model than the implementer.** Use `max(tier, T2)` as reviewer model.

## Cross-PR review (multi-repo)

If issue spans multiple PRs (different repos):
- Dispatch one reviewer per PR
- OR dispatch one reviewer with cross-repo diff context (preferred for coherence)
- Aggregate ratings: all must be `approve*` for merge

## Verification

Before claiming review done:
```bash
gh pr view <PR> --json reviews --jq '.reviews[-1].state'
# should be APPROVED or CHANGES_REQUESTED
# (skip this check if the fallback comment path was taken — there will be no
#  new review entry, only a new comment)
```

## Output

```
Review posted for PR #<N>:
  Rating: <rating>
  Critical: <count>
  Important: <count>
  Minor: <count>
  Next: <merge | dispatch-fix>
```

## Sub-skills

- Invokes `vibe-flow:vibe-reviewer` agent (via Agent tool)
- Passes to `vibe-flow:vibe-merge` on approve
- Passes to `vibe-flow:vibe-dispatch-fix` on request-changes

## Remember

- Fresh subagent, isolated context
- Two-stage: spec first, then quality
- Classify every finding
- Post review to GitHub via `gh`, not just in chat
- Update issue + state.json after review
- On approve: move to `ready_to_merge` if the project configured that column (`.vibe-flow.yaml → statuses.ready_to_merge`), else stay `in_review`. On request-changes: back to `in_progress`.
- Resolve all status names through `.vibe-flow.yaml → statuses.*`, never hardcode.
