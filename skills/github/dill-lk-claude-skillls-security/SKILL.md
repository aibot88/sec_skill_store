# Skill: Security

Review code for vulnerabilities, apply secure coding practices, design authentication/authorisation systems, and harden infrastructure configurations.

---

## Overview

Claude can perform security reviews, identify OWASP Top 10 vulnerabilities, suggest remediation, design secure authentication flows, and audit configuration files. Use this skill as a first-pass security reviewer and secure design partner.

---

## Task Patterns

### 1. Security Code Review

**Prompt template:**
```
Perform a security review of the following [language] code.

Check for:
- Injection vulnerabilities (SQL, command, LDAP, XPath)
- Broken authentication or session management
- Sensitive data exposure
- Insecure direct object references
- Security misconfiguration
- XSS / CSRF vulnerabilities
- Insecure deserialisation
- Use of components with known vulnerabilities
- Insufficient logging and monitoring

For each finding:
1. Name and severity (Critical / High / Medium / Low)
2. Affected code location
3. Explanation of the risk
4. Remediation with corrected code

[language]
[paste code]
```

---

### 2. Fix a Specific Vulnerability

**Prompt template:**
```
The following [language] code is vulnerable to [vulnerability type, e.g., SQL injection / XSS / SSRF].

[language]
[paste vulnerable code]

Provide:
1. Explanation of exactly how this code is exploitable
2. A proof-of-concept attack string (for understanding only)
3. The corrected, hardened code
4. A test case that proves the vulnerability is fixed
```

---

### 3. Design an Authentication System

**Prompt template:**
```
Design a [JWT / session-based / OAuth2 / API key] authentication system for [application type].

Requirements:
- [requirement 1, e.g., stateless]
- [requirement 2, e.g., refresh token rotation]
- [requirement 3, e.g., multi-factor authentication]

Provide:
- Architecture overview
- Token structure and signing algorithm
- Token storage recommendation (where and why)
- Expiry and refresh strategy
- Logout and revocation approach
- Security hardening checklist
```

---

### 4. Design an Authorisation / RBAC System

**Prompt template:**
```
Design a [RBAC / ABAC / ReBAC] authorisation model for [application].

Roles and permissions:
- [role 1]: [permissions]
- [role 2]: [permissions]

Requirements:
- [e.g., hierarchical roles]
- [e.g., resource-level permissions]
- [e.g., audit trail for permission changes]

Show: data model, permission check logic, and API middleware integration.
```

---

### 5. Audit a Configuration File

**Prompt template:**
```
Audit the following [nginx / docker / kubernetes / terraform / AWS IAM] configuration for security issues.

Flag:
- Over-permissive access controls
- Missing encryption settings
- Exposed sensitive values
- Insecure defaults not overridden
- Missing rate limiting or DDoS protection

[paste configuration]
```

---

### 6. Input Validation and Sanitisation

**Prompt template:**
```
Add comprehensive input validation and sanitisation to the following [language] code.

Requirements:
- Validate all inputs at the boundary (before processing)
- Use allowlist validation, not blocklist
- Sanitise for the output context (HTML, SQL, shell, file path)
- Return descriptive validation errors without leaking internals

[language]
[paste code]
```

---

### 7. Secrets Management Audit

**Prompt template:**
```
Review the following codebase structure and configuration for secret management issues:

[paste file list, config snippets, or environment handling code]

Check for:
- Hardcoded credentials or API keys
- Secrets in environment variables without a vault
- Secrets committed to version control
- Logging of sensitive values
- Insecure secret rotation practices

Recommend a secrets management approach for this stack.
```

---

## Advanced Techniques

### Threat Model Generation

```
Generate a threat model for [application / feature] using the STRIDE framework.

System description:
- Components: [list]
- Data flows: [describe]
- Trust boundaries: [describe]
- External actors: [list]

For each STRIDE category (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), list threats and mitigations.
```

### Penetration Test Planning

```
Create a penetration testing checklist for [web app / API / mobile app / infrastructure].

Scope: [describe in/out of scope]
Environment: [staging / production-like]

Organise by:
1. Reconnaissance
2. Authentication and session testing
3. Authorisation and access control testing
4. Input validation testing
5. Business logic testing
6. Infrastructure and configuration review
```

### Dependency Vulnerability Scan Analysis

```
Analyse the following dependency vulnerability report and prioritise remediation:

[paste npm audit / pip-audit / Dependabot / Snyk report]

For each vulnerability:
1. Assess actual exploitability in our context
2. Recommend upgrade path or workaround
3. Flag any transitive dependencies requiring special handling
```

---

## OWASP Top 10 Quick Reference (2021)

| # | Category | Key Mitigation |
|---|---|---|
| A01 | Broken Access Control | Enforce on server; deny by default |
| A02 | Cryptographic Failures | TLS everywhere; encrypt sensitive data at rest |
| A03 | Injection | Parameterised queries; input validation |
| A04 | Insecure Design | Threat modelling; secure design patterns |
| A05 | Security Misconfiguration | Harden defaults; disable unused features |
| A06 | Vulnerable Components | Dependency scanning; keep packages updated |
| A07 | Auth Failures | MFA; secure session management |
| A08 | Software & Data Integrity | Verify signatures; secure CI/CD |
| A09 | Logging Failures | Log security events; alert on anomalies |
| A10 | SSRF | Allowlist outbound requests; network egress controls |

---

## Security Checklist

- [ ] All inputs validated and sanitised at trust boundaries
- [ ] No secrets hardcoded; secrets stored in vault or secret manager
- [ ] Authentication uses a well-tested library (no custom crypto)
- [ ] Authorisation checked server-side on every request
- [ ] All dependencies scanned for known CVEs
- [ ] Error messages reveal no internal details to external users
- [ ] All HTTP responses include security headers (CSP, HSTS, etc.)
- [ ] Sensitive data encrypted at rest and in transit
- [ ] Security events are logged and monitored
- [ ] OWASP Top 10 reviewed and addressed
