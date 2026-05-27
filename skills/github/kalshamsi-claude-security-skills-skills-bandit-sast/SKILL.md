---
name: bandit-sast
description: "Use when scanning Python code for security vulnerabilities, running Bandit, performing Python SAST, auditing Python security bugs, or reviewing Python source for injection, weak crypto, or insecure deserialization."
---

# Bandit SAST

This skill performs static application security testing (SAST) for Python projects using Bandit, identifying common security anti-patterns such as use of dangerous functions, hardcoded credentials, insecure cryptography, and injection risks, then mapping findings to CWE and OWASP Top 10:2021 standards.

## When to Use

- When the user asks to "scan Python code for security issues" or "run Bandit"
- When the user mentions "Python SAST" or "security scan Python"
- When reviewing Python code for vulnerabilities before deployment
- When a pull request contains changes to `.py` files and a security check is requested
- When the user asks to find insecure patterns like `eval`, `exec`, `pickle`, or hardcoded passwords in Python

## When NOT to Use

- When scanning non-Python code (JavaScript, Go, Java, etc.) — you **MUST** decline and recommend `semgrep-rule-creator` or the language-specific tool instead
- When the user is asking about Python code style, formatting, or linting — you **MUST** decline and recommend `pylint` or `flake8`
- When the user wants runtime or dynamic analysis of a running application — you **MUST** decline and recommend DAST tools like `dast-nuclei`
- When the user wants to generate security test code — you **MUST** decline and recommend `security-test-generator`
- When the user wants a CI/CD security pipeline — you **MUST** decline and recommend `devsecops-pipeline`
- When the `security-review` skill already covers the request at a general level and no Python-specific SAST depth is needed

## Prerequisites

### Tool Installed (Preferred)

```bash
# Detection
which bandit || python -m bandit --version

# Installation (if not found)
pip install bandit
```

Minimum version: Bandit 1.7+. No API key required.

### Tool Not Installed (Fallback)

> **Note:** This is a limited review. Install Bandit for comprehensive scanning with full test coverage.

When Bandit is not available, perform these top-10 manual Python security checks:

1. **eval() / exec() usage** — Search for `eval(` and `exec(` calls, especially with user-controlled input
2. **subprocess with shell=True** — Search for `subprocess.call(`, `subprocess.Popen(`, `subprocess.run(` with `shell=True` and string interpolation
3. **Hardcoded passwords** — Search for variables named `password`, `passwd`, `secret`, `api_key` assigned to string literals
4. **pickle deserialization** — Search for `pickle.loads(`, `pickle.load(`, `cPickle.load(` on untrusted data
5. **Weak hashing** — Search for `hashlib.md5(`, `hashlib.sha1(` used for password hashing or security-sensitive operations
6. **assert in production** — Search for `assert` statements used for input validation (stripped in optimized mode)
7. **Wildcard imports** — Search for `from module import *` which can mask injected names
8. **try-except-pass** — Search for bare `except:` or `except Exception:` followed by `pass`, which silences security errors
9. **Insecure temp files** — Search for `tempfile.mktemp(` (use `tempfile.mkstemp()` or `NamedTemporaryFile` instead)
10. **yaml.load() without SafeLoader** — Search for `yaml.load(` without `Loader=yaml.SafeLoader` or `yaml.safe_load(`

## Workflow

> **MANDATORY FIRST ACTION — Verify the tool before reporting its output.**
>
> Your first Bash call must be `command -v bandit || bandit --version`. Branch on the result:
>
> - **Bandit is available** — proceed with the installed-tool workflow (step 3a below). The report may use `## Bandit SAST Scan Results`, cite B-series test IDs (B101, B602, etc.), and reference the Bandit version, because real Bandit output backs all of it.
> - **Bandit is not available** — proceed with the fallback workflow (step 3b below). The report must:
>   - Use header `## Python Security Review (Manual Fallback)`.
>   - Open with: `> Note: This is a limited review. Install Bandit for comprehensive scanning.`
>   - Cite CWE + OWASP only. B-series test IDs are Bandit's internal taxonomy — using them without running Bandit misattributes the findings to a tool that did not produce them.
>   - Not claim a scanner, version, or file count that the turn history doesn't show.
>
> The contract is simple: **every artifact in the report must trace back to something the skill actually did in this turn.** If you did not run `bandit`, don't present Bandit results. The user is relying on the report matching what was actually scanned.

1. **Detect Python project** — Confirm Python files exist by checking for `*.py` files, `requirements.txt`, `setup.py`, `pyproject.toml`, or `Pipfile`.
2. **Check for Bandit** — Run `which bandit || python -m bandit --version` to determine if Bandit is installed.
3. **If Bandit is installed:**
   a. Run `bandit -r . -f json -q` to scan all Python files recursively with JSON output.
   b. Parse the JSON output — each result contains `test_id`, `test_name`, `issue_severity`, `issue_confidence`, `issue_text`, `filename`, and `line_number`.
   c. Map each `test_id` to its CWE using the Reference Tables below.
   d. Map each CWE to its OWASP Top 10:2021 category.
4. **If Bandit is NOT installed:**
   a. Offer to install via `pip install bandit`.
   b. If the user declines, run the 10 manual fallback checks listed in Prerequisites.
   c. Include the disclaimer: "This is a limited review. Install Bandit for comprehensive scanning."
5. **Compile findings** — Deduplicate results and sort by severity: Critical > High > Medium > Low.
6. **Generate report** — Present findings using the Findings Format below.
7. **Summarize** — State total findings, breakdown by severity, and top 3 remediation priorities.

## Findings Format

> **MANDATORY FORMAT:** You **MUST** include Severity, CWE, and OWASP Top 10:2021 mapping on **every** finding. Use the exact table format shown below — do not use freeform text.

Each finding should include:

| Field | Description |
|-------|-------------|
| Severity | Critical / High / Medium / Low |
| CWE | CWE-XXX identifier |
| OWASP | A01-A10 category (OWASP Top 10:2021) |
| Location | file:line |
| Issue | Description of the vulnerability |
| Remediation | How to fix it |

### Example Finding

| Field | Value |
|-------|-------|
| Severity | High |
| CWE | CWE-78 |
| OWASP | A03:2021 - Injection |
| Location | app/utils.py:27 |
| Issue | `subprocess.call()` with `shell=True` and f-string user input enables OS command injection |
| Remediation | Use `subprocess.run()` with a list of arguments and `shell=False` (default) |

## Reference Tables

### Bandit Test ID to CWE Mapping

| Bandit Test ID | Test Name | CWE | OWASP | Default Severity |
|----------------|-----------|-----|-------|------------------|
| B101 | assert_used | CWE-703 | A07:2021 - Security Misconfiguration | Low |
| B102 | exec_used | CWE-78 | A03:2021 - Injection | Medium |
| B301 | pickle | CWE-502 | A08:2021 - Software and Data Integrity Failures | Medium |
| B303 | md5 / sha1 | CWE-328 | A02:2021 - Cryptographic Failures | Medium |
| B306 | mktemp_q | CWE-377 | A01:2021 - Broken Access Control | Medium |
| B307 | eval | CWE-78 | A03:2021 - Injection | Medium |
| B501 | request_with_no_cert_validation | CWE-295 | A07:2021 - Security Misconfiguration | High |
| B602 | subprocess_popen_with_shell_equals_true | CWE-78 | A03:2021 - Injection | High |
| B603 | subprocess_without_shell_equals_true | CWE-78 | A03:2021 - Injection | Low |
| B608 | hardcoded_sql_expressions | CWE-89 | A03:2021 - Injection | Medium |
| B105 | hardcoded_password_string | CWE-259 | A07:2021 - Security Misconfiguration | Low |
| B106 | hardcoded_password_funcarg | CWE-259 | A07:2021 - Security Misconfiguration | Low |
| B403 | import_pickle | CWE-502 | A08:2021 - Software and Data Integrity Failures | Low |
| B506 | yaml_load | CWE-502 | A08:2021 - Software and Data Integrity Failures | Medium |

### OWASP Top 10:2021 Quick Reference

| Category | Description | Common CWEs |
|----------|-------------|-------------|
| A01:2021 | Broken Access Control | CWE-377 |
| A02:2021 | Cryptographic Failures | CWE-328 |
| A03:2021 | Injection | CWE-78, CWE-89 |
| A07:2021 | Security Misconfiguration | CWE-259, CWE-295, CWE-703 |
| A08:2021 | Software and Data Integrity Failures | CWE-502 |

## Example Usage

### With Bandit Installed

**User prompt:**
> "Run a Bandit scan on this Python project"

**Expected output (abbreviated):**

```text
## Bandit SAST Scan Results

Scanned 14 files in src/

### Findings (4 total: 0 Critical, 2 High, 1 Medium, 1 Low)

| # | Severity | CWE | OWASP | Location | Issue |
|---|----------|-----|-------|----------|-------|
| 1 | High | CWE-78 | A03 | src/deploy.py:31 | subprocess.Popen() with shell=True and user input (B602) |
| 2 | High | CWE-78 | A03 | src/utils.py:12 | eval() called with user-supplied string (B307) |
| 3 | Medium | CWE-502 | A08 | src/cache.py:45 | pickle.loads() on data from network socket (B301) |
| 4 | Low | CWE-703 | A07 | src/config.py:8 | assert used for input validation (B101) |

### Recommendations
1. Replace subprocess shell calls with list-based arguments (Finding #1)
2. Replace eval() with ast.literal_eval() or a safe parser (Finding #2)
3. Use json.loads() instead of pickle for untrusted data (Finding #3)
```

### Without Bandit (Fallback Mode)

**User prompt:**
> "Check this Python code for security issues"

**Expected output (abbreviated):**

```text
## Python Security Review (Manual Fallback)

> Note: This is a limited review. Install Bandit for comprehensive scanning.

Scanned 8 .py files

### Findings (2 total: 0 Critical, 1 High, 1 Medium)

| # | Severity | CWE | OWASP | Location | Issue |
|---|----------|-----|-------|----------|-------|
| 1 | High | CWE-78 | A03 | scripts/run.py:19 | subprocess.call() with shell=True and string formatting |
| 2 | Medium | CWE-259 | A07 | config/settings.py:5 | Hardcoded password: DB_PASSWORD = "admin123" |

### Recommendations
1. Use subprocess.run() with a list of arguments instead of shell=True (Finding #1)
2. Move credentials to environment variables or a secrets manager (Finding #2)
```
