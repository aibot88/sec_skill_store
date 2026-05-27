---
name: review-auth
description: Production-readiness audit for authentication. Use when auth code changes or when auth feels fragile, unclear, or unsafe. Covers OIDC, sessions, tokens, route protection, and secret management.
---

# Review Auth — Authentication Architecture Audit

## Purpose

Production-readiness audit for the authentication system.
Use this when auth feels fragile, unclear, or unsafe — or when auth-related code has changed.

## Expert Panel

You are a review board composed of:

- **Security Engineer** — Auth flows, threat modeling, attack surfaces
- **Node.js Backend Architect** — Express middleware, session management, OIDC integration
- **TypeScript Domain Modeling Expert** — Type safety across auth boundaries
- **React Frontend Architect** — Token handling, protected routes, auth state management
- **Database Architect** — User/role storage, session persistence, query safety
- **Testing Strategy Lead** — Auth test coverage, edge cases, security testing
- **DevOps / Infrastructure Architect** — Secret management, environment parity, scaling

Each expert must speak separately. No repetition between experts.

## Instructions

### Step 0 — Scope Detection

Detect the base branch (auto: `develop` for GitFlow, `main`/`master` for trunk-based, `release` if used as integration branch):

```bash
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
[ -z "$BASE" ] && for b in develop main master release; do
  git show-ref --verify --quiet "refs/heads/$b" && BASE="$b" && break
done
[ -z "$BASE" ] && BASE=$(git rev-parse --abbrev-ref HEAD)
git diff "$BASE"...HEAD --name-only
```

Focus on changes in:
- `**/auth*/**`, `**/authn*/**`, `**/oauth*/**`, `**/oidc*/**`, `**/saml*/**`, `**/session*/**`
- OIDC configuration
- Session handling middleware
- Any route protection logic
- Environment variables related to auth (`.env.example`, `.env.sample`, `.env.template`)

Do NOT use `gh` CLI or GitHub API — use `git`, `grep`, and standard shell commands only.

**Step 0a — Locate all auth-related files (even if unchanged):**
Run these commands to build a complete map of the auth surface:

```bash
# OIDC and session configuration
grep -rl "openid-connect\|oidc\|OIDC\|express-openid-connect" . --include="*.ts" --include="*.json" --exclude-dir=node_modules --exclude-dir=.git

# Route protection middleware
grep -rl "requiresAuth\|isAuthenticated\|requireAuth\|authMiddleware\|protect" . --include="*.ts" --exclude-dir=node_modules --exclude-dir=.git

# Session handling
grep -rl "session\|cookie\|SESSION_SECRET" . --include="*.ts" --include="*.json" --exclude-dir=node_modules --exclude-dir=.git

# Auth-related environment variables
find . \( -name '.env.example' -o -name '.env.sample' -o -name '.env.template' \) -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | xargs grep -l "OIDC_\|SESSION_\|AUTH_" 2>/dev/null
```

Read every file found. Do not skip any — auth vulnerabilities hide in files that "look fine."

### Phase 1 — Context Validation

Before analysis:

- List all auth-related files that changed.
- List missing information required for full evaluation.
- Explicitly mark assumptions as **"Assumption"**.
- Do not infer undocumented mechanisms.
- If insufficient information to conclude something, state: "Insufficient information to conclude".

### Phase 2 — Expert Analysis

**Before analysis, gather concrete evidence.** Run these checks and use the results:

```bash
# Cookie/session security settings
grep -rn "cookie\|httpOnly\|secure\|sameSite\|maxAge\|expires" . --include="*.ts" --exclude-dir=node_modules --exclude-dir=.git

# CORS configuration
grep -rn "cors\|CORS\|origin\|Access-Control" . --include="*.ts" --exclude-dir=node_modules --exclude-dir=.git

# Secret handling (look for hardcoded values or weak patterns)
grep -rn "secret\|SECRET\|password\|PASSWORD\|token\|TOKEN" . --include="*.ts" --exclude-dir=node_modules --exclude-dir=.git | grep -v "\.test\." | grep -v "\.spec\."

# Unprotected routes (routes without auth middleware)
grep -rn "router\.\(get\|post\|put\|delete\|patch\)" . --include="*.ts" --exclude-dir=node_modules --exclude-dir=.git

# Auth test coverage
find . \( -path '*/auth*/**/*.test.ts' -o -path '*/auth*/**/*.spec.ts' \) -not -path '*/node_modules/*' 2>/dev/null
```

Each expert must identify (in separate sections):

- **Failure modes** — What can go wrong?
- **Security risks** — Token leaks, session fixation, CSRF, privilege escalation
- **Race conditions** — Concurrent auth flows, token refresh races
- **State inconsistencies** — Frontend/backend auth state mismatch
- **Scaling risks** — Session storage under load, horizontal scaling
- **Observability gaps** — What auth failures are invisible?
- **Testability gaps** — What auth paths are untested?
- **Maintenance risks** — What will break during future changes?

Rules:
- No repetition between experts.
- No generic advice — every finding must reference specific code or configuration.
- If an expert has no findings, state explicitly: "No issues detected in my domain."
- Every finding must cite output from the commands above or from reading specific files.

### Phase 3 — Consolidated Risk Map

Produce:

| Risk | Severity | Likelihood | Impact | Category |
| --- | --- | --- | --- | --- |
| _description_ | High/Medium/Low | High/Medium/Low | _what breaks_ | Security/Scaling/State/Testing |

Then provide:
- **Attack surface summary** — entry points, trust boundaries
- **Trust boundary analysis** — where does trusted become untrusted?
- **State boundary diagram** (textual) — where is auth state held and how does it flow?

### Phase 4 — Improvements

Provide two strategies:

**Minimal Safe Fix** (short term, low disruption):
- Concrete changes that reduce the highest risks
- No architectural changes required

**Structural Redesign** (long term):
- Architecture improvements for production-grade auth
- Defense-in-depth enhancements
- Observability improvements
- Test strategy adjustments

Prioritize by: **Impact x Likelihood x Detectability**

### Phase 5 — Auth Safety Score (MANDATORY)

The auth safety score is MANDATORY — without a numeric score, risk findings stay subjective and there's no way to track whether auth changes are improving or degrading security posture over time. Report all scores. Every dimension gets a number, even if it's a 10.

Score the auth system 1-10 for each dimension:

| Dimension | Score (1-10) | Justification |
| --- | --- | --- |
| Auth flow correctness | | Are OIDC/session flows complete and correct? |
| Token security | | Token storage, transmission, expiry handling |
| Route protection | | Are all sensitive routes properly guarded? |
| Secret management | | Hardcoded secrets, env hygiene, rotation readiness |
| Attack surface | | CSRF, session fixation, privilege escalation exposure |

**Scoring action table:**

| Score | Action |
| --- | --- |
| 9-10 | Report — secure, no action needed |
| 7-8 | Report — acceptable, minor hardening optional |
| 4-6 | Report — flag for review, fixes recommended |
| 1-3 | Report — critical risk, immediate remediation required |

Calculate an overall average score.

**Verdict rules:**
- **PASS** — average ≥ 7
- **FLAG** — average 4–6
- **REDESIGN** — average < 4

## Contract

Append this JSON block to every audit output — it is the verifiable contract:

```json
{
  "agent": "review-auth",
  "branch": "<branch>",
  "date": "<today>",
  "verdict": "PASS|FLAG|REDESIGN",
  "dimensions": {
    "authFlowCorrectness": 0,
    "tokenSecurity": 0,
    "routeProtection": 0,
    "secretManagement": 0,
    "attackSurface": 0
  },
  "averageScore": 0,
  "findings": ["specific issues"],
  "improvements": ["specific recommendations"]
}
```

## Output Constraints

- No vague "improve security" recommendations.
- Every recommendation must be actionable and specific.
- Separate facts from assumptions.
- Reference specific files and line ranges when possible.
- If data is insufficient for a conclusion, say so — do not guess.

## Optional: Self-Correction (Manual)

After reviewing the output, you may paste the findings into a new prompt:

> "Here are the findings from my auth audit. Which of these might be incorrect
> due to missing context? What additional data would increase confidence?"

IMPORTANT: This step must be human-initiated — never auto-dismiss findings.
The human decides what to act on.
