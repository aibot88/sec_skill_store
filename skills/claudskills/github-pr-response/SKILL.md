---
name: github-pr-response
description: Respond to PR review comments from humans or AI reviewers. Fetches open review threads, triages each comment, implements fixes, posts a reply citing the commit, and optionally resolves threads. Use when a PR has received review feedback that needs actioning — trigger on "respond to PR comments", "address review feedback", "fix PR comments", "reply to review", or when review threads are open on a PR you authored.
categories: [github]
agents: [pi, hermes, claude, copilot]
version: 1.0.0
author: GitHub Copilot
license: MIT
metadata:
  source: custom
  scope: global
  hermes:
    tags: [GitHub, Pull-Requests, Code-Review, Feedback, Automation]
    related_skills: [github-pr-workflow, github-code-review, github-auth]
---

# GitHub PR Response Workflow

Triage → implement → reply → re-request review.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Inside the repo that owns the PR
- On the feature branch for the PR

---

## Step 1 — Fetch All Open Review Threads

**First, read the full comment text verbatim** using `run_in_terminal` (not a subagent — subagents summarise output and lose comment bodies):

```bash
gh pr view <PR> --comments | cat
```

This gives you the complete comment text for every review comment and general PR comment. Read this output yourself before acting.

Then fetch thread metadata (IDs needed for replies) via GraphQL — again using `run_in_terminal` directly so output is not summarised:

> ⚠️ Never delegate the "fetch PR comments" step to `execution_subagent`. Subagent summarisation silently discards comment bodies, causing you to implement the wrong fix.

Use GraphQL to get thread IDs, comment body, file path, and line number in one call.

```bash
OWNER=<owner>
REPO=<repo>
PR=<number>

gh api graphql -f query='
{
  repository(owner: "'$OWNER'", name: "'$REPO'") {
    pullRequest(number: '$PR') {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 3) {
            nodes {
              databaseId
              body
              path
              line
              author { login }
            }
          }
        }
      }
    }
  }
}'
```

Filter to unresolved threads only (`isResolved: false`). Collect:
- `databaseId` of the **first** comment in each thread (needed to post a reply)
- `body` — the reviewer's comment
- `path` + `line` — location in the code

---

## Step 2 — Triage Each Thread

For each unresolved thread, classify:

| Category | Action |
|----------|--------|
| Bug / correctness | Fix the code, add or update a test |
| Style / naming | Rename or restructure as suggested |
| Documentation | Update comment, docstring, or README section |
| Question / clarification | Reply with explanation; no code change needed |
| Disagree | Reply with reasoning; ask the user before ignoring |

Group by file so related changes are made together.

---

## Step 3 — Implement Fixes

Work through each thread in file order. For each code change:

1. Read the file before editing.
2. Make the minimal fix that addresses the comment.
3. Run tests:
   ```bash
   go test ./...        # Go
   pytest tests/ -q     # Python
   npm test             # Node
   ```
4. Stage and commit using a message that references the fix:
   ```bash
   git add <changed files>
   git commit -m "fix: <what was changed> (addresses review feedback)"
   ```

Note the **short commit SHA** after each commit — you'll cite it in the reply.

---

## Step 4 — Post a Reply to Each Thread

Reply using the REST API against the **first comment's `databaseId`**:

```bash
gh api repos/<owner>/<repo>/pulls/<PR>/comments/<databaseId>/replies \
  -f body="Fixed in <short-sha>. <one-sentence description of what changed and why.>"
```

**Good reply format:**
> Fixed in `a1b2c3d`. Moved token write after the collision check so a failed add never overwrites an existing credential.

**For question threads (no code change):**
> No code change needed — `TokenForRepo` is the single source of truth; `httpToken` and `resolveToken` were removed in this PR.

---

## Step 5 — Optionally Resolve Threads

Resolve threads where the fix is complete and unambiguous:

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: { threadId: "<PRRT_...id>" }) {
    thread { isResolved }
  }
}'
```

Do **not** resolve threads where:
- The reviewer may want to verify the fix themselves
- There is ongoing discussion
- You disagreed and are awaiting the user's decision

---

## Step 6 — Re-request Review

Once all threads have a reply:

```bash
# Get the reviewer's login first
gh pr view <PR> --json reviewRequests

# Re-request review
gh api repos/<owner>/<repo>/pulls/<PR>/requested_reviewers \
  -X POST -f "reviewers[]=<login>"
```

Or via `gh`:
```bash
gh pr edit <PR> --add-reviewer <login>
```

---

## Quick-Reference Cheatsheet

```bash
# List open threads (summary)
gh api graphql -f query='{ repository(owner:"O", name:"R") { pullRequest(number:N) {
  reviewThreads(first:50) { nodes { isResolved
    comments(first:1) { nodes { databaseId body path } } } } } } }'

# Reply to a thread
gh api repos/O/R/pulls/N/comments/<databaseId>/replies -f body="..."

# Resolve a thread
gh api graphql -f query='mutation { resolveReviewThread(input:{threadId:"PRRT_..."}) {
  thread { isResolved } } }'

# Re-request review
gh pr edit N --add-reviewer <login>
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using the thread `id` (GraphQL `PRRT_...`) for the reply endpoint | Use `databaseId` (integer) of the first comment instead |
| Posting a reply with no commit reference | Always cite the short SHA so reviewers can verify |
| Resolving threads before the reviewer sees the fix | Only resolve if the fix is mechanical and obvious |
| Batching all fixes into one commit | One logical commit per fix makes replies traceable |
| Forgetting to push before re-requesting review | `git push` first |

---

## Mandatory Done Checklist

Run this after every PR response session. Do **not** mark the task complete until every box is ticked.

```
[ ] Every unresolved thread has a reply citing a commit SHA
[ ] All fix commits have been pushed (git push)
[ ] Threads with mechanical, unambiguous fixes are resolved
[ ] Review re-requested from every reviewer who left feedback
    gh pr edit <PR> --add-reviewer <login>
```

The last step (re-request review) is the most commonly skipped. Reviewers are **not** notified when you reply to a thread — re-requesting review is the only reliable notification.
