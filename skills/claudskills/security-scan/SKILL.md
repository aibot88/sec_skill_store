---
name: security-scan
description: >
  Scan the codebase for security vulnerabilities based on the OWASP Top 10.
  Use when the user asks to audit security, find vulnerabilities, check for
  security issues, or says "security scan", "audit this", "find security bugs".
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(find *), Bash(git *)
---

## Context

- Repository: !`git rev-parse --show-toplevel 2>/dev/null || pwd`
- Languages detected: !`find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rb" -o -name "*.java" \) | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10`
- Target: $ARGUMENTS

## Task

Perform a security audit of the codebase (or the path specified in $ARGUMENTS) covering the OWASP Top 10:

1. **A01 - Broken Access Control**: Look for missing authorization checks, IDOR patterns, direct object references, insecure direct database access without ownership checks.

2. **A02 - Cryptographic Failures**: Find hardcoded secrets, API keys, passwords in source code. Check for use of weak algorithms (MD5, SHA1 for passwords, ECB mode). Look for unencrypted sensitive data in logs or responses.

3. **A03 - Injection**: Search for SQL queries built with string concatenation, unsanitized shell commands, template injection, LDAP injection, and XSS sinks.

4. **A04 - Insecure Design**: Identify missing rate limiting on auth endpoints, no CSRF protection on state-changing forms, missing input length limits.

5. **A05 - Security Misconfiguration**: Check for debug mode enabled, verbose error messages exposing internals, permissive CORS headers, default credentials in config files.

6. **A06 - Vulnerable Components**: Note any obviously outdated dependency versions or known-vulnerable packages in `package.json`, `requirements.txt`, `go.mod`, or `Gemfile`.

7. **A07 - Authentication Failures**: Look for weak session management, missing account lockout, insecure password reset flows, JWT with weak or no signature verification.

8. **A08 - Software Integrity Failures**: Check for use of untrusted CDN resources without integrity hashes, insecure deserialization of user-supplied data.

9. **A09 - Logging Failures**: Verify that authentication events are logged, that logs do not contain passwords or tokens, and that errors are logged without exposing stack traces to users.

10. **A10 - SSRF**: Find URL parameters or user-controlled values passed to HTTP clients, file readers, or DNS lookups without validation.

For each finding, read the surrounding code to confirm it is a real issue, not a false positive.

## Output Format

### Executive Summary
Total findings by severity. One-paragraph risk assessment.

### Findings

For each vulnerability:
- **ID**: VULN-001, VULN-002, ...
- **Category**: OWASP category (e.g., A03 - Injection)
- **Severity**: Critical / High / Medium / Low / Informational
- **File**: `path/to/file.py:42`
- **Description**: what the vulnerability is
- **Evidence**: the specific code snippet or pattern found
- **Remediation**: concrete steps to fix it

### No Issues Found
List categories where no issues were detected (to show coverage).

### Out of Scope
Note any areas not checked (e.g., third-party libraries, infrastructure config not present in the repo).
