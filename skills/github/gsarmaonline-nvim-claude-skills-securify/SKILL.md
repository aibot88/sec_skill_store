---
name: securify
description: Scan a repository for security vulnerabilities across dependencies, code, secrets, and API surface
---

You are being invoked via the /securify skill. Your task is to perform a comprehensive security audit of the current repository, identify vulnerabilities, and produce an actionable report. You must also specifically assess API security posture.

## Overview

This skill covers:
1. Detect project type and languages
2. Scan dependencies for known CVEs
3. Audit code for OWASP Top 10 and common security anti-patterns
4. Check API endpoints for authentication, authorization, and input validation gaps
5. Detect hardcoded secrets and credentials
6. Review security-related configuration files
7. Generate a prioritized vulnerability report with remediation guidance

---

## Step 1 — Detect Project Type

Identify all languages and frameworks in use by checking for:

- `package.json` → Node.js / TypeScript
- `requirements.txt` / `pyproject.toml` / `Pipfile` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `pom.xml` / `build.gradle` → Java / Kotlin
- `Gemfile` → Ruby
- `*.csproj` → C# / .NET

Note all detected stacks — a repo may have multiple (e.g. a Node.js frontend + Python backend).

---

## Step 2 — Dependency Vulnerability Scan

Run the appropriate dependency scanner for each detected stack. Do NOT skip this step.

### Node.js
```bash
npm audit --json 2>/dev/null || yarn audit --json 2>/dev/null
```
Parse the output and list packages with severity: `critical`, `high`, `moderate`, `low`.

### Python
```bash
pip-audit --format=json 2>/dev/null || safety check --json 2>/dev/null
```
If neither is installed, fall back to:
```bash
pip list --format=json | python3 -c "import sys,json; pkgs=json.load(sys.stdin); print('\n'.join(f'{p[\"name\"]}=={p[\"version\"]}' for p in pkgs))"
```
and note that pip-audit/safety should be installed for full scanning.

### Go
```bash
govulncheck ./... 2>/dev/null
```
If not available:
```bash
go list -m all 2>/dev/null
```
and recommend installing `govulncheck`.

### Rust
```bash
cargo audit 2>/dev/null
```

### Ruby
```bash
bundle audit check --update 2>/dev/null
```

### Java
Check for known vulnerable versions of common dependencies in `pom.xml` or `build.gradle` (Log4Shell, Spring4Shell, etc.).

For each vulnerability found, record:
- Package name and version
- CVE ID (if available)
- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Description
- Fixed version (if available)

---

## Step 3 — Secret and Credential Detection

Search the entire repository (excluding `.git/`) for accidentally committed secrets.

### Patterns to search for (use Grep):

**API Keys and tokens:**
```
(api[_-]?key|apikey)\s*[:=]\s*['"]?[A-Za-z0-9\-_]{16,}
(secret[_-]?key|secret)\s*[:=]\s*['"]?[A-Za-z0-9\-_]{16,}
(access[_-]?token|auth[_-]?token)\s*[:=]\s*['"]?[A-Za-z0-9\-_\.]{16,}
Bearer\s+[A-Za-z0-9\-_\.]{20,}
```

**Cloud provider credentials:**
```
AKIA[0-9A-Z]{16}                          # AWS Access Key ID
(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}   # AWS Secret
AIza[0-9A-Za-z\-_]{35}                    # Google API Key
[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com  # Google OAuth
sk-[a-zA-Z0-9]{48}                        # OpenAI API Key
ghp_[a-zA-Z0-9]{36}                       # GitHub Personal Access Token
ghs_[a-zA-Z0-9]{36}                       # GitHub App Token
```

**Database connection strings:**
```
(mongodb|postgres|postgresql|mysql|redis):\/\/[^:]+:[^@]+@
DATABASE_URL\s*=\s*['"]?[^\s'"]+
```

**Private keys:**
```
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
```

**Passwords:**
```
password\s*[:=]\s*['"][^'"]{8,}['"]
passwd\s*[:=]\s*['"][^'"]{8,}['"]
```

For each match, record:
- File path and line number
- Type of secret detected
- Severity: CRITICAL (private keys, cloud credentials) / HIGH (API keys, tokens) / MEDIUM (passwords in config)

Check `.gitignore` to confirm `.env` files are excluded. If not, flag it.

---

## Step 4 — API Security Audit

Find all API route definitions using Grep. Then for each route, evaluate the security controls below.

### 4a. Locate API Routes

Search for route definitions matching the detected framework:

**Express/Fastify/Koa (Node.js):**
```
(app|router)\.(get|post|put|patch|delete|all)\s*\(
```

**FastAPI/Flask (Python):**
```
@(app|router)\.(get|post|put|patch|delete)\(
```

**Go (Gin/Echo/Chi/Fiber):**
```
\.(GET|POST|PUT|PATCH|DELETE|Any)\s*\(
```

**Rails:**
```
(get|post|put|patch|delete)\s+['"]\/
resources\s+:
```

### 4b. For Each Route, Check:

#### Authentication
- Does the route have an auth middleware/guard/decorator?
  - Express: `authMiddleware`, `authenticate`, `verifyToken`, `requireAuth`, `passport.authenticate`
  - FastAPI: `Depends(get_current_user)`, `Security(...)`
  - NestJS: `@UseGuards(AuthGuard)`, `@UseGuards(JwtAuthGuard)`
  - Go: middleware chain applied before handler
- Flag any route that handles sensitive data (user info, payments, admin) without authentication

#### Authorization
- After authentication, is there authorization (RBAC/ABAC)?
  - Look for: role checks, permission checks, `hasRole()`, `can()`, `@Roles()`, `@RequirePermission()`
- Flag routes that allow any authenticated user to access admin/privileged resources without role checks

#### Input Validation
- Is request body/query/path input validated?
  - Express: `express-validator`, `joi`, `zod`, `yup`
  - FastAPI: Pydantic models
  - Go: binding tags `binding:"required"`, `validate:"..."`
  - NestJS: `class-validator` DTOs
- Flag routes that read `req.body`, `request.json()`, or query params without validation

#### Rate Limiting
- Is there a rate limiter applied globally or per-route?
  - Express: `express-rate-limit`, `rate-limiter-flexible`
  - FastAPI: `slowapi`
  - Go: `tollbooth`, `golang.org/x/time/rate`
- Flag public auth endpoints (`/login`, `/register`, `/forgot-password`) without rate limiting

#### CORS
- Check CORS configuration:
  - Is `origin: '*'` used in production (over-permissive)?
  - Are credentials (`withCredentials`) allowed with wildcard origin?
  - Look for: `cors()`, `CORSMiddleware`, `Access-Control-Allow-Origin`

#### HTTPS / TLS
- Are there any HTTP redirects to HTTPS?
- Is HSTS configured?
- Look for: `helmet()`, security headers, `SECURE_SSL_REDIRECT`

#### SQL Injection
- Search for raw query string concatenation:
  ```
  query\s*[+]=?\s*.*req\.(body|params|query)
  execute\s*\(\s*f['"]\s*SELECT
  cursor\.execute\s*\(\s*['"].*%s.*%.*request
  db\.raw\s*\(.*\+
  ```
- Flag any parameterized query bypass patterns

#### Command Injection
- Search for dangerous subprocess calls with user input:
  ```
  exec\s*\(.*req\.(body|params|query)
  subprocess\.(run|call|Popen).*request
  os\.system\s*\(.*input
  child_process\.exec\s*\(.*req
  ```

#### Path Traversal
- Search for file system operations with user-controlled paths:
  ```
  fs\.(readFile|writeFile|readdir)\s*\(.*req\.(body|params|query)
  open\s*\(.*request\.(form|args|json)
  ```

#### XSS (for server-side rendering)
- Search for unescaped user input in templates:
  ```
  innerHTML\s*=\s*.*req
  dangerouslySetInnerHTML
  render_template_string\s*\(.*request
  ```

### 4c. Summarize API Security Findings

For each finding, note:
- Route: `POST /api/auth/login`
- Issue: Missing rate limiting
- Severity: HIGH
- File: `src/routes/auth.ts:42`
- Recommendation: Apply `express-rate-limit` with max 5 attempts per 15 minutes

---

## Step 5 — Security Configuration Review

Check for insecure security-related configuration:

### Environment Variables
- Is there a `.env.example` present? If not, flag it.
- Are any sensitive defaults set in `.env.example` (e.g., `SECRET_KEY=mysecretkey`)?

### Security Headers
- Is `helmet` (Node.js), `django-csp`, or equivalent used?
- Are the following headers set?
  - `Content-Security-Policy`
  - `X-Frame-Options`
  - `X-Content-Type-Options`
  - `Strict-Transport-Security`
  - `Referrer-Policy`

### Session Configuration
- Is session secret a hardcoded weak string?
- Are cookies set with `httpOnly: true`, `secure: true`, `sameSite: 'strict'`?

### JWT Configuration
- Are JWTs using `HS256` with a weak/hardcoded secret? (Should use RS256 or strong HS256 secret)
- Is token expiry set (missing `expiresIn` is a vulnerability)?
- Is `jwt.verify()` used (not just `jwt.decode()` which skips verification)?

### Docker / Container
- Is the app running as root in Docker? (Look for `USER` directive in Dockerfile)
- Are secrets passed as `ARG` or `ENV` in Dockerfile (leaked in image layers)?

### Dependencies
- Is `package-lock.json` / `yarn.lock` / `poetry.lock` committed? (Ensures reproducible, auditable builds)

---

## Step 6 — Generate Vulnerability Report

Create the file `docs/SECURITY_AUDIT.md` with the following structure:

```markdown
# Security Audit Report

**Generated:** <current date>
**Repository:** <repo name>
**Audited By:** /securify skill

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | X |
| 🟠 HIGH | X |
| 🟡 MEDIUM | X |
| 🔵 LOW | X |
| **Total** | **X** |

---

## 1. Dependency Vulnerabilities

### CRITICAL

#### [Package Name] vX.Y.Z — CVE-XXXX-XXXX
- **Description:** Brief description of the vulnerability
- **Fix:** Upgrade to vX.Y.Z
- **Command:** `npm update package-name` or `pip install --upgrade package-name`

### HIGH
...

### MEDIUM
...

---

## 2. Secrets & Credentials Found

### CRITICAL — Hardcoded Private Key
- **File:** `config/server.key:1`
- **Issue:** RSA private key committed to repository
- **Action:** Remove immediately, rotate the key, add to `.gitignore`

### HIGH — API Key Exposed
- **File:** `src/config.js:12`
- **Issue:** API key hardcoded in source file
- **Action:** Move to environment variable, invalidate and regenerate the key

---

## 3. API Security Issues

### Authentication Gaps

#### 🔴 CRITICAL — Admin Endpoint Without Authentication
- **Route:** `DELETE /api/admin/users/:id`
- **File:** `src/routes/admin.ts:78`
- **Issue:** No authentication middleware applied
- **Fix:** Add auth guard before handler

#### 🟠 HIGH — Missing Rate Limiting on Auth Endpoints
- **Routes:** `POST /api/auth/login`, `POST /api/auth/forgot-password`
- **Issue:** No rate limiting — vulnerable to brute force attacks
- **Fix:**
  ```javascript
  const loginLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });
  router.post('/auth/login', loginLimiter, loginHandler);
  ```

#### 🟡 MEDIUM — Overly Permissive CORS
- **File:** `src/app.ts:15`
- **Issue:** `origin: '*'` allows any domain to make requests
- **Fix:** Specify allowed origins explicitly:
  ```javascript
  cors({ origin: ['https://yourdomain.com'] })
  ```

### Input Validation Gaps

#### 🟠 HIGH — SQL Injection Risk
- **File:** `src/db/queries.ts:34`
- **Issue:** User input concatenated into raw SQL query
- **Fix:** Use parameterized queries:
  ```javascript
  // UNSAFE:
  db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
  // SAFE:
  db.query('SELECT * FROM users WHERE id = $1', [req.params.id])
  ```

### Authorization Issues

#### 🟠 HIGH — Missing Role Check on Admin Route
- **Route:** `GET /api/admin/stats`
- **File:** `src/routes/admin.ts:12`
- **Issue:** Route is authenticated but any user can access admin data
- **Fix:** Add role check middleware

---

## 4. Security Configuration Issues

### 🟡 MEDIUM — Security Headers Not Set
- **Issue:** No `helmet` or equivalent security headers middleware
- **Fix:**
  ```javascript
  import helmet from 'helmet';
  app.use(helmet());
  ```

### 🔵 LOW — Cookies Missing Security Flags
- **File:** `src/session.ts:8`
- **Issue:** Session cookies not set with `httpOnly` and `secure` flags
- **Fix:**
  ```javascript
  cookie: { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'strict' }
  ```

---

## 5. Recommended Next Steps

### Immediate Actions (CRITICAL)
1. [ ] Rotate any exposed secrets/API keys immediately
2. [ ] Add authentication to unprotected admin endpoints
3. [ ] Remove hardcoded credentials from source code

### Short-term (HIGH)
1. [ ] Add rate limiting to all authentication endpoints
2. [ ] Fix SQL injection vulnerabilities with parameterized queries
3. [ ] Upgrade vulnerable dependencies

### Medium-term (MEDIUM/LOW)
1. [ ] Add `helmet` for security headers
2. [ ] Restrict CORS to known origins
3. [ ] Configure secure cookie flags
4. [ ] Set up automated dependency scanning in CI

---

## 6. Automated Security Tools to Add

Based on this project's stack, consider adding these tools:

### Dependency Scanning (CI)
```yaml
# .github/workflows/security.yml
- name: Dependency audit
  run: npm audit --audit-level=high
```

### Static Analysis
- **Node.js:** `eslint-plugin-security`, `semgrep`
- **Python:** `bandit`, `semgrep`
- **Go:** `gosec`
- **Rust:** `cargo-audit`

### Secret Scanning
```yaml
- name: Secret scan
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: main
```

---

*This report was generated automatically by the /securify skill. Manual review is recommended for complex logic vulnerabilities.*
```

---

## Step 7 — Add Security CI Workflow

Create or update `.github/workflows/security.yml` with appropriate security scanning jobs:

```yaml
name: Security Scan

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6am

jobs:
  dependency-audit:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm audit --audit-level=high

  secret-scan:
    name: Secret Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: TruffleHog Secret Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --only-verified

  sast:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Semgrep SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/jwt
            p/sql-injection
```

Only create this file if `.github/workflows/` already exists or the user has a GitHub Actions setup. Otherwise, note it as a recommendation.

---

## Step 8 — Update CLAUDE.md

Add a security workflow section to `CLAUDE.md` (only if CLAUDE.md exists):

```markdown
### Security Auditing

- Use the `/securify` skill to scan for vulnerabilities before major releases or when adding new API endpoints
- Run `/securify` after adding new dependencies to check for known CVEs
- Never commit `.env` files or hardcoded secrets — use environment variables
- Ensure all API endpoints have authentication and rate limiting where appropriate
- Review `docs/SECURITY_AUDIT.md` for outstanding security issues
```

---

## Step 9 — Final Summary

After completing all steps, output a concise summary to the user:

```
Security Audit Complete
=======================

Repository: <name>
Stack detected: <e.g., Node.js (Express), Python (FastAPI)>

Findings:
  🔴 CRITICAL  X issues
  🟠 HIGH      X issues
  🟡 MEDIUM    X issues
  🔵 LOW       X issues

Top priorities:
  1. <Most critical finding with file:line>
  2. <Second most critical finding>
  3. <Third most critical finding>

Full report: docs/SECURITY_AUDIT.md

Recommended tools to install:
  - <tool> for <purpose>
```

---

## Important Notes

- **Do NOT modify any source code** — only report findings and suggest fixes
- **Do NOT expose or print full secret values** — truncate to first 4 and last 4 characters when referencing found secrets (e.g., `sk-ab...xy12`)
- Flag when `.env` is missing from `.gitignore`
- Prioritize API endpoint security findings since exposed APIs are the primary attack surface
- If no vulnerabilities are found in a category, explicitly state "No issues found" for clarity
- When tools like `pip-audit`, `govulncheck`, or `cargo audit` are not installed, note it in the report and include install instructions
