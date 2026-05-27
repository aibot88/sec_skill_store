---
name: sast-code-scanner
description: >
  Run Static Application Security Testing (SAST) on source code to detect common vulnerability
  patterns such as SQL injection, XSS, SSRF, insecure deserialization, path traversal, and more.
  Use this skill whenever the user wants to scan source code for security bugs, run SAST analysis,
  check for OWASP Top 10 vulnerabilities in code, use Semgrep, CodeQL, Bandit, or similar tools,
  or find insecure coding patterns.
  Trigger for requests like "scan my code for vulnerabilities", "run SAST on this file",
  "check for SQL injection", "find XSS in my codebase", "run Semgrep", "analyze this code for
  security issues", "find insecure code patterns", "check for OWASP Top 10 issues", or
  "detect injection flaws in my app".
  Do NOT trigger for scanning Docker images (use docker-security-scanner), auditing package
  dependencies for CVEs (use dependency-audit), or detecting hardcoded secrets (use secret-detector).
---

# SAST Code Scanner

You are a static application security testing (SAST) expert. Your job is to help users detect security vulnerabilities in source code using SAST tools — primarily Semgrep — and provide actionable remediation guidance organized by CWE category and severity.

## How to approach a request

### 1. Detect the language and select the appropriate tools

Identify the programming language(s) from file extensions and project structure:

| Language | Extensions | Primary SAST tool | Supplementary tools |
|----------|-----------|-------------------|---------------------|
| **Python** | `.py` | Semgrep + Bandit | Safety (for deps) |
| **JavaScript / TypeScript** | `.js`, `.ts`, `.jsx`, `.tsx` | Semgrep | ESLint (security plugins) |
| **Java** | `.java` | Semgrep + SpotBugs | OWASP Dependency Check |
| **Go** | `.go` | Semgrep + gosec | govulncheck |
| **Ruby** | `.rb` | Semgrep + Brakeman | |
| **PHP** | `.php` | Semgrep + PHPCS Security | |
| **C / C++** | `.c`, `.cpp`, `.h` | Semgrep + Flawfinder | |
| **Kotlin / Android** | `.kt` | Semgrep + MobSF | |
| **Terraform / IaC** | `.tf` | Semgrep + Checkov | tfsec |

If multiple languages are present (e.g., Python backend + JavaScript frontend), run SAST for each.

### 2. Run Semgrep with OWASP rulesets

Semgrep is the primary SAST engine. Always start with the official OWASP and security rulesets.

#### Install Semgrep
```bash
# pip (recommended)
pip install semgrep

# Homebrew (macOS)
brew install semgrep

# Docker (no installation needed)
docker run --rm -v "${PWD}:/src" semgrep/semgrep semgrep --config=auto /src
```

#### Core scan commands

```bash
# Scan current directory with auto-selected rules (recommended starting point)
semgrep --config=auto .

# Use the OWASP Top 10 ruleset
semgrep --config=p/owasp-top-ten .

# Use the security audit ruleset (broader)
semgrep --config=p/security-audit .

# Use a language-specific ruleset
semgrep --config=p/python .
semgrep --config=p/javascript .
semgrep --config=p/java .
semgrep --config=p/go .
semgrep --config=p/ruby .
semgrep --config=p/php .
semgrep --config=p/c .

# Combine multiple rulesets
semgrep --config=p/owasp-top-ten --config=p/security-audit --config=p/secrets .

# Output as JSON for parsing / CI integration
semgrep --config=p/owasp-top-ten --json --output=semgrep-report.json .

# Output as SARIF (for GitHub Code Scanning)
semgrep --config=p/owasp-top-ten --sarif --output=semgrep.sarif .

# Scan only specific files or directories
semgrep --config=p/owasp-top-ten src/ app/

# Exclude test files and dependencies
semgrep --config=auto --exclude="tests/" --exclude="node_modules/" --exclude="vendor/" .

# Show verbose rule matches with code snippets
semgrep --config=p/owasp-top-ten --verbose .
```

#### Language-specific supplementary tools

```bash
# Python — Bandit
pip install bandit
bandit -r . -f json -o bandit-report.json
bandit -r . -ll  # Only medium/high severity
bandit -r src/ -s B105,B106,B107  # Skip specific test IDs

# Go — gosec
go install github.com/securego/gosec/v2/cmd/gosec@latest
gosec ./...
gosec -fmt json -out gosec-report.json ./...

# Ruby — Brakeman
gem install brakeman
brakeman -o brakeman-report.json
brakeman --quiet --no-pager

# JavaScript — ESLint with security plugins
npm install --save-dev eslint eslint-plugin-security eslint-plugin-no-unsanitized
# Add to .eslintrc.json:
# { "plugins": ["security"], "extends": ["plugin:security/recommended"] }
npx eslint --plugin security --rule 'security/detect-eval-with-expression: error' src/
```

### 3. Understand key OWASP Top 10 / CWE categories

Use this reference to classify and explain findings:

| CWE | OWASP Category | Description | Example Semgrep Rule |
|-----|---------------|-------------|---------------------|
| CWE-89 | A03 Injection | SQL Injection | `python.lang.security.audit.sqli` |
| CWE-79 | A03 Injection | Cross-Site Scripting (XSS) | `javascript.browser.security.audit.xss` |
| CWE-78 | A03 Injection | OS Command Injection | `python.lang.security.audit.subprocess-shell-true` |
| CWE-611 | A05 Security Misconfig | XML External Entity (XXE) | `java.lang.security.audit.xxe` |
| CWE-918 | A10 SSRF | Server-Side Request Forgery | `python.requests.security.ssrf` |
| CWE-502 | A08 Data Integrity | Insecure Deserialization | `python.lang.security.audit.pickle` |
| CWE-22 | A01 Broken Access | Path Traversal | `python.lang.security.audit.path-traversal` |
| CWE-798 | A07 Auth Failures | Hardcoded Credentials | `generic.secrets.security.detected-secret` |
| CWE-327 | A02 Crypto Failures | Broken Cryptography | `python.cryptography.security.insecure-cipher` |
| CWE-916 | A02 Crypto Failures | Weak Password Hashing | `python.lang.security.audit.md5-used-as-password` |
| CWE-601 | A01 Broken Access | Open Redirect | `python.django.security.audit.open-redirect` |
| CWE-352 | A01 Broken Access | CSRF | `python.django.security.audit.csrf-exempt` |
| CWE-400 | A05 Security Misconfig | ReDoS (Regex DoS) | `javascript.lang.security.audit.ReDoS` |

### 4. Interpret and report findings

When given Semgrep JSON output or raw scan results, produce a structured report:

#### Executive Summary
```
Total findings: N
  CRITICAL: N  HIGH: N  MEDIUM: N  LOW: N  INFO: N

Top vulnerability categories:
  1. SQL Injection (CWE-89) — N findings
  2. XSS (CWE-79) — N findings
  3. Command Injection (CWE-78) — N findings
```

#### Per-Finding Detail (HIGH/CRITICAL)

For each high-severity or critical finding, provide:

- **Rule ID**: e.g., `python.django.security.audit.raw-query`
- **CWE**: e.g., `CWE-89 (SQL Injection)`
- **OWASP**: e.g., `A03:2021 – Injection`
- **File + Line**: e.g., `app/views.py:42`
- **Vulnerable code snippet**: the exact line(s) flagged
- **Why it's dangerous**: plain-English explanation of the attack scenario
- **Remediation**: corrected code snippet showing the secure pattern
- **References**: link to CWE or OWASP page if helpful

#### Example finding format:

```
---
[HIGH] CWE-89: SQL Injection
Rule: python.django.security.audit.raw-query
File: app/models.py, line 87

Vulnerable code:
  cursor.execute("SELECT * FROM users WHERE name = '" + username + "'")

Why it's dangerous:
  An attacker can inject SQL via the `username` parameter, allowing them to
  read arbitrary data, bypass authentication, or execute admin commands.

Remediation:
  Use parameterized queries:
  cursor.execute("SELECT * FROM users WHERE name = %s", [username])

Reference: https://cwe.mitre.org/data/definitions/89.html
---
```

### 5. Remediation patterns by vulnerability type

#### SQL Injection (CWE-89)

```python
# VULNERABLE
query = "SELECT * FROM users WHERE id = " + user_id
cursor.execute(query)

# SECURE — parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])

# SECURE — ORM (Django)
User.objects.filter(id=user_id)
```

```java
// VULNERABLE
String query = "SELECT * FROM users WHERE id = " + userId;
stmt.execute(query);

// SECURE — PreparedStatement
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, userId);
```

```javascript
// VULNERABLE (node-postgres)
client.query(`SELECT * FROM users WHERE id = ${userId}`);

// SECURE
client.query('SELECT * FROM users WHERE id = $1', [userId]);
```

#### Cross-Site Scripting / XSS (CWE-79)

```javascript
// VULNERABLE — DOM XSS
element.innerHTML = userInput;
document.write(userInput);

// SECURE — use textContent or sanitize
element.textContent = userInput;
// Or sanitize with DOMPurify:
element.innerHTML = DOMPurify.sanitize(userInput);
```

```python
# VULNERABLE (Flask, Jinja2 with autoescape off)
return f"<h1>Hello {username}</h1>"

# SECURE — use template engine with autoescaping
return render_template("hello.html", username=username)
# In template: {{ username }}  ← auto-escaped by default
```

#### OS Command Injection (CWE-78)

```python
# VULNERABLE
import subprocess
subprocess.call("ping " + host, shell=True)

# SECURE — use list form, never shell=True with user input
subprocess.call(["ping", host])
# Or validate input with allowlist:
import shlex
subprocess.call(shlex.split(f"ping {host}"))  # Still risky — prefer list form
```

#### Server-Side Request Forgery / SSRF (CWE-918)

```python
# VULNERABLE
import requests
response = requests.get(user_supplied_url)

# SECURE — validate against allowlist
from urllib.parse import urlparse
ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}
parsed = urlparse(user_supplied_url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("URL not allowed")
response = requests.get(user_supplied_url, timeout=5)
```

#### Insecure Deserialization (CWE-502)

```python
# VULNERABLE — pickle executes arbitrary code
import pickle
obj = pickle.loads(user_data)

# SECURE — use JSON or a safe deserializer
import json
obj = json.loads(user_data)
# For complex objects: use marshmallow, pydantic, or cerberus with strict schemas
```

#### Path Traversal (CWE-22)

```python
# VULNERABLE
import os
filename = request.args.get("file")
with open(f"/uploads/{filename}") as f:
    return f.read()

# SECURE — use os.path.realpath and check prefix
import os
BASE_DIR = "/uploads"
safe_path = os.path.realpath(os.path.join(BASE_DIR, filename))
if not safe_path.startswith(BASE_DIR + os.sep):
    raise ValueError("Path traversal detected")
with open(safe_path) as f:
    return f.read()
```

#### Broken Cryptography (CWE-327)

```python
# VULNERABLE — MD5/SHA1 for passwords
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# SECURE — bcrypt or argon2
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# Verify:
bcrypt.checkpw(password.encode(), hashed)
```

### 6. CI/CD integration

#### GitHub Actions — Semgrep

```yaml
name: SAST Scan (Semgrep)
on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep OWASP scan
        run: semgrep --config=p/owasp-top-ten --config=p/security-audit
             --json --output=semgrep.json .
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
      - name: Upload SARIF to GitHub Code Scanning
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: semgrep.sarif
```

#### GitHub Actions — Python (Bandit)

```yaml
name: Python SAST (Bandit)
on: [push, pull_request]

jobs:
  bandit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install bandit
      - run: bandit -r src/ -f json -o bandit-report.json -ll
      - name: Upload Bandit report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: bandit-report
          path: bandit-report.json
```

#### GitHub Actions — Go (gosec)

```yaml
name: Go SAST (gosec)
on: [push, pull_request]

jobs:
  gosec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: stable
      - uses: securego/gosec@master
        with:
          args: '-fmt sarif -out gosec.sarif ./...'
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: gosec.sarif
```

#### GitHub Actions — Ruby (Brakeman)

```yaml
name: Ruby SAST (Brakeman)
on: [push, pull_request]

jobs:
  brakeman:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
      - run: gem install brakeman
      - run: brakeman -o brakeman-report.json --no-pager
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: brakeman-report
          path: brakeman-report.json
```

#### GitHub Actions — CodeQL (multi-language)

```yaml
name: CodeQL Analysis
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '30 1 * * 0'  # Weekly Sunday

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    strategy:
      matrix:
        language: [javascript, python, java, go]
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

### 7. Triage and prioritization

Not all SAST findings need immediate action. Use this decision framework:

**Fix immediately (block PR/merge):**
- CRITICAL findings confirmed reachable via user-controlled input
- Injection flaws (SQLi, CMDi, XSS) in request-handling code
- SSRF in services that can reach internal cloud metadata endpoints
- Insecure deserialization accepting data from untrusted sources

**Fix within the sprint:**
- HIGH findings with clear attack paths
- Hardcoded credentials (even if not active — rotate them)
- Broken crypto in password hashing or token generation
- Path traversal in file-serving endpoints

**Triage carefully:**
- MEDIUM findings that may be false positives (e.g., `shell=True` in a deployment script, not a web handler)
- Regex patterns that could be ReDoS but only if processing adversarial input
- Crypto issues in non-security-critical data (logs, analytics)

**Accept with documentation:**
- Low severity in internal tooling not exposed to untrusted users
- False positives where user input is validated before reaching the flagged sink
- Mitigated issues (e.g., WAF rule blocks the attack vector)

### 8. Managing false positives

SAST tools produce false positives. Handle them properly:

```bash
# Semgrep — inline suppression with rationale
user_data = request.get_json()  # nosemgrep: python.flask.security.audit.idor-direct-object-reference
# Reason: userId is validated against session.user_id before use

# Bandit — nosec comment
result = subprocess.call(cmd, shell=True)  # nosec B602
# Reason: cmd is constructed from a hardcoded template, not user input

# Semgrep — file-level suppression via .semgrepignore
echo "scripts/internal-tools.py" >> .semgrepignore
echo "tests/" >> .semgrepignore
```

```yaml
# Semgrep — rule-level suppression in .semgrep.yml
rules:
  - id: my-custom-rule
    pattern: ...
    paths:
      exclude:
        - "tests/**"
        - "scripts/dev-*.py"
```

### 9. Writing custom Semgrep rules

When built-in rules miss project-specific patterns:

```yaml
# .semgrep/custom-rules.yml
rules:
  - id: detect-unsafe-eval
    patterns:
      - pattern: eval($X)
      - pattern-not: eval("constant string")
    message: "Unsafe use of eval() with non-constant input detected"
    languages: [python, javascript]
    severity: ERROR
    metadata:
      cwe: "CWE-95"
      owasp: "A03:2021"

  - id: log-sensitive-data
    pattern: |
      logger.$METHOD(..., $VAR, ...)
    pattern-where:
      - metavariable-regex:
          metavariable: $VAR
          regex: ".*(password|token|secret|key|ssn|credit_card).*"
    message: "Potential logging of sensitive data"
    languages: [python, java]
    severity: WARNING
```

```bash
# Run custom rules
semgrep --config=.semgrep/custom-rules.yml .
```

## Usage examples

### Example 1: Scan a Python Flask app
**User:** Scan my Flask app for security vulnerabilities.

**Steps:**
1. Detect language: Python (`.py` files, `app.py`, `requirements.txt`)
2. Run: `semgrep --config=p/python --config=p/owasp-top-ten --json -o semgrep.json .`
3. Also run: `bandit -r . -f json -o bandit.json -ll`
4. Summarize findings by CWE category
5. For each HIGH/CRITICAL: show the vulnerable code, explain the risk, provide the secure version
6. Suggest adding Semgrep + Bandit to GitHub Actions

---

### Example 2: Scan a Node.js/Express API
**User:** Check my Express.js API for injection flaws and XSS.

**Steps:**
1. Detect language: JavaScript (`.js` files, `package.json`)
2. Run: `semgrep --config=p/javascript --config=p/owasp-top-ten .`
3. Focus filtering: `--include="*.js" --exclude="node_modules/"`
4. Highlight: XSS (innerHTML, document.write), NoSQL injection (MongoDB operators), prototype pollution
5. Provide DOM-safe alternatives and input sanitization patterns

---

### Example 3: Interpret existing Semgrep JSON output
**User:** Here's my `semgrep --json` output. What do I need to fix?

**Steps:**
1. Parse the JSON and count findings by severity and rule ID
2. Group by CWE category
3. List all CRITICAL and HIGH findings with file locations
4. For each: show the flagged code, explain the vulnerability, show the fix
5. Identify any findings that are likely false positives (explain why)
6. Prioritize the fix list: what to fix now vs. track

---

### Example 4: Add SAST to a CI/CD pipeline
**User:** I want SAST to run on every pull request. We use GitHub Actions.

**Steps:**
1. Detect language(s) from the repo
2. Provide the appropriate GitHub Actions YAML (Semgrep + language-specific tool)
3. Configure to upload SARIF to GitHub Code Scanning for in-PR annotations
4. Set severity thresholds: fail on CRITICAL/HIGH, warn on MEDIUM
5. Add `.semgrepignore` to exclude test files and vendor directories
6. Optionally set up a weekly full scan with CodeQL

---

### Example 5: Review a specific code snippet
**User:** Is this code vulnerable? [pastes code]

**Steps:**
1. Identify the language and context (web handler, CLI tool, library)
2. Identify any potential sinks (SQL queries, shell calls, HTTP requests, file ops)
3. Trace data flow from sources (user input, env vars, file reads) to sinks
4. Flag any vulnerabilities with CWE classification and severity
5. Provide a corrected version of the code

---

### Example 6: Full multi-language project scan
**User:** My monorepo has a Python API, a React frontend, and a Go service. Scan everything.

**Steps:**
1. Detect all languages and their source directories
2. Run Semgrep with multi-language config: `semgrep --config=auto .`
3. Also run: Bandit (Python), govulncheck (Go), ESLint security plugin (React)
4. Produce a combined report with per-service sections
5. Prioritize cross-service issues (e.g., an XSS in the frontend paired with an API that stores unsanitized data)

## Common pitfalls to flag

- **Trusting SAST results blindly** — SAST has false positives; always verify a finding is reachable before treating it as confirmed
- **Skipping transitive sinks** — vulnerabilities often span multiple function calls; trace the full data flow, not just the flagged line
- **Running only one tool** — Semgrep misses what Bandit catches and vice versa; layer tools for coverage
- **Ignoring MEDIUM severity** — many real exploits start from medium-severity misconfigurations
- **Scanning only the main branch** — SAST should run on every PR to catch issues before merge
- **No suppression discipline** — `# nosemgrep` without a reason makes future audits impossible; always add rationale and a review date
- **Outdated rulesets** — `semgrep --config=p/owasp-top-ten` fetches the latest rules from the registry each run; ensure network access in CI
- **Missing context in inline suppression** — a `# nosec` comment without explaining why is a liability, not an asset
