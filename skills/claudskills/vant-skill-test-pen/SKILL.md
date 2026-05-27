---
name: test-pen
description: Penetration testing - find security vulnerabilities. Test for SQL injection, XSS, auth bypass, etc. Use when security auditing or before deployments.
license: MIT
metadata:
  author: vant
  version: "1.0"
---

# Test Pen

> Penetration testing.

## When To Use

- Security audit
- Pre-deploy
- Compliance

## Common Vulnerabilities

| Type | Test | Impact |
|------|------|--------|
| SQL Injection | ' OR '1'='1 | Data leak |
| XSS | <script> | Cookie theft |
| CSRF | Token steal | Account |
| IDOR | user/1 → user/2 | Access |

## Tools

| Tool | Use |
|------|-----|
| OWASP ZAP | Web app scan |
| Burp Suite | Proxy testing |
| SQLMap | SQL injection |
| Nmap | Port scanning |

---

## Output

```
## Pen Test

| Finding | Severity | CVSS |
|--------|----------|------|
| SQL Injection | Critical | 9.8 |
| XSS | High | 7.2 |
| Info | Low | 3.0 |
```

**Role**: Pen Tester  
**Input**: Target  
**Output**: Vulnerabilities