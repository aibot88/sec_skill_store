---
name: ascent-env-audit
description: >-
  Verifies that <<PROJECT_TITLE>> follows ENV-DISCIPLINE: .env is
  gitignored and dockerignored, .env.example has empty defaults only
  (no REPLACE_ME), every environment variable read in code appears in
  .env.example, and no secrets are committed or baked into images.
  Can run standalone or as a component of ascent-self-audit's umbrella.
version: <<PROJECT_VERSION>>
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# ascent-env-audit

Validates <<PROJECT_TITLE>>'s environment variable discipline against the ENV-DISCIPLINE contract. Catches the deployment-incident-in-waiting: committed secrets, fake placeholders that get accidentally deployed, and env vars that code reads but `.env.example` doesn't declare. Runs standalone or as a component of [ascent-self-audit](../ascent-self-audit/SKILL.md)'s umbrella audit.

## When this skill engages

- Before a commit that touches `.env.example`, Dockerfile, or docker-compose files
- As a component of ascent-self-audit's comprehensive check (delegated invocation)
- After adding a new environment variable to the code
- When a security review flags secret-handling concerns
- During onboarding to verify the developer's `.env` setup
- When CI reports an unexpected environment-variable error in staging/production

## Inputs

- **Project root directory** — reads `.env.example`, `.gitignore`, `.dockerignore`, Dockerfiles, and source code
- **Source directories** (optional) — defaults to `backend/` and `frontend/`; override for projects with different structure
- **Invocation mode** — standalone (full output with guidance) or component (structured PASS/FAIL for umbrella aggregation)

## Outputs

- **ENV-DISCIPLINE report** — each rule checked with PASS or FAIL status
- **Per-violation detail** — the specific violation, the file and line if applicable, and the fix action
- **Summary line** — "N/M env checks passing"
- **Exit code** — 0 if all checks pass, 1 if any check fails

## Operational logic

The skill executes these checks in order. Each check produces PASS or FAIL. Step numbers are local to this skill.

### Step 1 — Verify .env.example exists

**Condition:** `.env.example` file exists at the project root.

**Action on PASS:** Proceed to Step 2.

**Action on FAIL:** Report "FAIL: .env.example not found — create it with empty defaults for every env var the project reads." Exit with summary.

**Fallback:** Check if the file exists under a different name (`.env.sample`, `.env.template`) and suggest renaming to `.env.example`.

### Step 2 — Verify .env is gitignored

**Condition:** `.gitignore` contains a line that matches `.env` (excluding `.env.example` via negation pattern `!.env.example`).

**Action on PASS:** Report ".env listed in .gitignore — PASS."

**Action on FAIL:** Report "FAIL: .env is not gitignored — add `.env` to .gitignore. This is the single most important ENV-DISCIPLINE rule."

### Step 3 — Verify .env is dockerignored

**Condition:** `.dockerignore` contains a line that matches `.env`.

**Action on PASS:** Report ".env listed in .dockerignore — PASS."

**Action on FAIL:** Report "FAIL: .env is not dockerignored — production images must not contain .env files. Add `.env` to .dockerignore."

### Step 4 — Verify .env.example has empty defaults only

**Condition:** Every line in `.env.example` that assigns a variable uses an empty value (`VAR_NAME=` with nothing after the `=`). Lines starting with `#` are comments and are permitted. No line matches the REPLACE_ME detection regex: `(REPLACE_ME|<your-[a-z-]+>|YOUR_[A-Z_]+_HERE|<paste-.*>)`.

**Action on PASS:** Report ".env.example has empty defaults only — PASS."

**Action on FAIL:** For each non-empty value, report the line. Example: "FAIL: .env.example line 3: `<<ENV_PREFIX>>_PORT=3000` — remove the default value. Empty defaults (`<<ENV_PREFIX>>_PORT=`) are the schema; the code owns defaults."

**Inline example:** `.env.example` with `<<ENV_PREFIX>>_DB_URL=postgresql://REPLACE_ME` → FAIL: line matches REPLACE_ME pattern. Fix: change to `<<ENV_PREFIX>>_DB_URL=`.

### Step 5 — Verify every code-read appears in .env.example

**Condition:** For every `process.env['...']` or `process.env[...]` or `process.env.VAR_NAME` reference in source files (backend/ and frontend/), the variable name appears as a key in `.env.example`.

**Action on PASS:** Report "All code-read env vars present in .env.example — PASS."

**Action on FAIL:** For each missing variable, report the source file, line, and the variable name. Example: "FAIL: backend/server.js:12 reads `<<ENV_PREFIX>>_SECRET_KEY` but it's missing from .env.example — add `<<ENV_PREFIX>>_SECRET_KEY=` to .env.example."

**Fallback:** Skip env vars that are standard Node.js vars (`NODE_ENV`, `PORT`, `HOME`, `PATH`) unless they use the project's env prefix.

### Step 6 — Verify no Dockerfile copies .env

**Condition:** No Dockerfile in the project contains `COPY .env` or `COPY .env.*` (excluding `.env.example`). The production image must not contain secrets.

**Action on PASS:** Report "No Dockerfile copies .env files — PASS."

**Action on FAIL:** Report the Dockerfile and line. Example: "FAIL: backend/Dockerfile:15 contains `COPY .env .` — production images must not contain .env. Secrets come from the environment at runtime."

### Step 7 — Verify no committed .env in git history

**Condition:** `git ls-files .env` returns no results (the file is not tracked). Additionally, `git log --all --diff-filter=A -- .env` returns no results (the file was never committed, even if later removed).

**Action on PASS:** Report "No .env file in git history — PASS."

**Action on FAIL:** Report "FAIL: .env was committed to git history. Even if removed, the secrets it contained are in the repository's history. Rotate all credentials that were in the file."

**Fallback:** If git is not available (not a git repository), skip this check and report "SKIP: not a git repository — cannot verify git history."

### Step 8 — Aggregate and report

Collect all PASS/FAIL results from Steps 1-7. Report summary: "7/7 env checks passing" or "5/7 env checks passing (2 violations found)."

In component mode: return structured result `{skill: "ascent-env-audit", passed: N, total: M, violations: [...]}`.

In standalone mode: print the full report with guidance for each violation.

## Examples

### Example 1 — Clean env discipline (all checks pass)

**Input state:** Project with `.env.example` containing empty defaults, `.gitignore` and `.dockerignore` both list `.env`, no Dockerfiles copy `.env`, all code-read vars present in `.env.example`.

**Skill output:**
```
ascent-env-audit: 7/7 checks passing
  PASS: .env.example exists
  PASS: .env listed in .gitignore
  PASS: .env listed in .dockerignore
  PASS: .env.example has empty defaults only
  PASS: All code-read env vars present in .env.example
  PASS: No Dockerfile copies .env files
  PASS: No .env file in git history
```

### Example 2 — REPLACE_ME placeholder detected

**Input state:** `.env.example` line 5: `<<ENV_PREFIX>>_API_KEY=sk-REPLACE_ME`

**Skill output:**
```
ascent-env-audit: 6/7 checks passing (1 violation)
  ...
  FAIL: .env.example has empty defaults only
    → line 5: <<ENV_PREFIX>>_API_KEY=sk-REPLACE_ME
    → Fix: change to <<ENV_PREFIX>>_API_KEY= (empty default). The code owns the default; .env.example is the schema.
  ...
```

### Example 3 — Code reads undeclared variable

**Input state:** `backend/server.js` line 42 reads `process.env['<<ENV_PREFIX>>_REDIS_URL']` but `.env.example` doesn't list `<<ENV_PREFIX>>_REDIS_URL`.

**Skill output:**
```
ascent-env-audit: 6/7 checks passing (1 violation)
  ...
  FAIL: All code-read env vars present in .env.example
    → backend/server.js:42 reads <<ENV_PREFIX>>_REDIS_URL but it's missing from .env.example
    → Fix: add <<ENV_PREFIX>>_REDIS_URL= to .env.example
  ...
```

### Example 4 — Missing .env.example (edge case)

**Input state:** No `.env.example` file exists.

**Skill output:**
```
ascent-env-audit: 0/7 checks passing (1 critical violation)
  FAIL: .env.example not found
    → Create .env.example with empty defaults for every env var the project reads.
  (remaining checks skipped — .env.example must exist first)
```

## Anti-patterns

### Anti-pattern 1 — Helpful default values in .env.example

Setting `<<ENV_PREFIX>>_PORT=3000` or `<<ENV_PREFIX>>_LOG_LEVEL=info` in `.env.example`. **Why it's tempting:** it looks like good documentation. **What to do instead:** empty defaults (`<<ENV_PREFIX>>_PORT=`). The code owns the default value; `.env.example` is the schema, not the configuration. Non-empty values get cargo-culted into production deployments.

### Anti-pattern 2 — .env.example as config template

Treating `.env.example` as a template to copy and fill in. **Why it's tempting:** "just copy and change the values." **What to do instead:** `.env.example` is the schema (what variables exist). `.env` is the configuration (what values they have). The developer creates `.env` and fills in values; they don't "copy and modify" `.env.example`.

### Anti-pattern 3 — Multiple .env files per environment

Creating `.env.staging`, `.env.production`, `.env.test` and committing them. **Why it's tempting:** per-environment config in the repo feels organized. **What to do instead:** one `.env.example` (schema). Per-environment values come from the environment at runtime (AWS Secrets Manager, Kubernetes secrets). Committed per-environment files contain secrets.

### Anti-pattern 4 — Adding vars to code without updating .env.example

A developer adds `process.env['<<ENV_PREFIX>>_NEW_VAR']` but forgets to add the line to `.env.example`. **Why it's tempting:** the code works on the developer's machine (they set the var locally). **What to do instead:** run `ascent-env-audit` per-commit. Step 5 catches this automatically.

### Anti-pattern 5 — Ignoring the git-history check

Dismissing "FAIL: .env was committed to git history" as a historical artifact. **Why it's tempting:** "we removed it, so it's fine." **What to do instead:** the secrets are in the history. Anyone who clones the repo can see them. Rotate every credential that was in the file. Then consider `git filter-branch` or BFG to remove the file from history.
