---
name: prod-check
description: Use when the user explicitly selects the prod-check skill or wants a pre-production code review scoped to recent commits, checking impact, contracts, auth, stability, and regressions.
---

# prod-check

Read `AGENTS.md`, then read `.agent-teamflow` from the repo root, then follow the workflow below. Treat the user's remaining request text as `$ARGUMENTS`.

---

Pre-production high-stakes code review scoped to today's work (or an explicit range). Analyzes the diff for impact on existing dependencies, contract breakage (API/DB/types), missing env vars, auth/security gaps, error handling, and regression coverage.

Use when asked to "prod check", "production review", "is this safe to ship", or before merging to staging or main.

Run this workflow in an isolated worker if the current agent runtime supports one; otherwise run it in the main session. Keep diff and grep output concise. Report only the final findings table (or `READY FOR PROD`) to the user.

## Core principle: impact over implementation

Do not just check if the new code works. Check if the new code **breaks existing, untouched parts of the system**. The goal is to catch failure modes that automated tests and the author missed.

## Setup — scope the diff to your work, not the full base-branch backlog

The typical branching model is `main ← staging ← <integration-branch> ← feature`. Diffing against any base branch sweeps in every contributor's accumulated work, drowning the signal. Instead, scope the review to commits you actually authored.

Read `.agent-teamflow` to get `branches.main` and `branches.staging`.

1. **Refresh refs:**
   ```bash
   git fetch origin
   ```

2. **Determine commit scope from `$ARGUMENTS`:**

   - **No argument (default)** — today's commits by the current git user:
     ```bash
     AUTHOR=$(git config user.email)
     SINCE=$(date '+%Y-%m-%d 00:00:00 %z')   # local midnight
     git log --author="$AUTHOR" --since="$SINCE" --all --pretty=format:'%H %ad %s' --date=iso
     ```
     If empty, tell the user "no commits authored by you since midnight" and stop.

   - **`since <expr>`** — pass through to `git log --since="$expr"` (e.g. `since yesterday`, `since "3 hours ago"`).

   - **`mr <N>` / `pr <N>`** — fetch the MR/PR's commits:
     ```bash
     # GitLab
     glab mr view <N> --output json | jq -r '.commits[].sha'
     # GitHub
     gh pr view <N> --json commits | jq -r '.commits[].oid'
     ```

   - **`<SHA1>..<SHA2>`** — explicit commit range.

3. **Print the scope** so the user can confirm:
   ```
   Scope: <N> commits authored by <email> since <when>
     <sha1> <subject>
     <sha2> <subject>
   ```

4. **Capture the diff for ONLY those commits:**
   ```bash
   FIRST_SHA=<oldest-in-scope>
   LAST_SHA=<newest-in-scope>
   git diff --stat ${FIRST_SHA}^..${LAST_SHA}
   git diff ${FIRST_SHA}^..${LAST_SHA}
   ```
   For non-contiguous commits, generate per-commit and concatenate.

5. Read the full diff content before scoring.

6. **Cross-reference touched files against the full repo for callers/importers** — when checking impact, `grep` the entire repo for usages. The scope limits *what you review*, not *where you look for callers*.

## Checklist

1. **Impact & Side Effects** — For every modified function, component, exported type, or hook, grep the repo for importers/callers. Flag any change to inputs, outputs, or types that breaks those call sites.

2. **Contract Integrity** — API response shapes, DB schemas (migrations), procedure signatures, shared types/interfaces. Verify the contract with consumers still holds.

3. **Environment & Infrastructure** — New env vars referenced in code but missing from deploy config. Migrations that lock large tables, drop columns still read by old code, or change indexes on hot paths.

4. **Security & Auth** — New endpoints/mutations have correct auth guards. No exposed secrets, tokens, or PII in logs. SQL/prompt injection surface checked. Rate limits intact.

5. **Stability & Error Handling** — New async logic has `try/catch` or `.catch`. User-facing failures show an error state, not a blank screen. No swallowed errors. Transactions still atomic.

6. **Testing & Regressions** — New logic has test coverage. Bug fixes have a regression test. Existing tests still mapped to new code paths.

## Output format

Start with a Summary Table:

| Severity | File:Line | Risk | Why it matters | Suggested fix |
|---|---|---|---|---|
| Critical | ... | ... | ... | ... |

**Severity ladder:**
- `Critical` — will break production or existing users on deploy
- `Warning` — likely issue under realistic conditions, deserves a fix or explicit acceptance
- `Advice` — nice-to-have polish, safe to defer

After the table, expand each row with the relevant code snippet and reasoning.

If no risks remain after a deep impact analysis, output exactly:

**READY FOR PROD**
