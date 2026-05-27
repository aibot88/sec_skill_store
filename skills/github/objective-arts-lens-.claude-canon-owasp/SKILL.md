---
name: owasp
description: OWASP Top 10 and security vulnerability patterns
---

# /owasp — OWASP Security Standards

Apply OWASP (Open Web Application Security Project) guidelines: the industry standard for web application security.

## OWASP Top 10 (2021)

### A01: Broken Access Control
```csharp
// BAD: No authorization check
[HttpGet("/api/users/{id}")]
public User GetUser(int id) => _db.Users.Find(id);

// GOOD: Verify ownership
[HttpGet("/api/users/{id}")]
[Authorize]
public User GetUser(int id) {
    var user = _db.Users.Find(id);
    if (user.Id != CurrentUserId && !IsAdmin)
        throw new ForbiddenException();
    return user;
}
```

### A02: Cryptographic Failures
- Use TLS 1.2+ for all traffic
- Hash passwords with bcrypt/Argon2 (never MD5/SHA1)
- Encrypt sensitive data at rest (AES-256)
- Never hardcode secrets

### A03: Injection
```javascript
// BAD: SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: Parameterized query
const query = 'SELECT * FROM users WHERE id = @id';
await db.query(query, { id: userId });
```

### A04: Insecure Design
- Threat model before coding
- Use secure design patterns
- Limit resource consumption
- Separate tenants properly

### A05: Security Misconfiguration
- Remove default credentials
- Disable directory listing
- Remove unused features/frameworks
- Keep dependencies updated
- Review cloud permissions

### A06: Vulnerable Components
```bash
# Check for vulnerabilities
npm audit
dotnet list package --vulnerable
```

### A07: Authentication Failures
- Multi-factor authentication
- Rate limit login attempts
- Secure password recovery
- Session timeout
- Secure session tokens

### A08: Software and Data Integrity Failures
- Verify signatures on updates
- Use integrity checks (SRI for CDN)
- Secure CI/CD pipelines
- Validate deserialized data

### A09: Security Logging & Monitoring Failures
```csharp
// Log security events
_logger.LogWarning("Failed login attempt for {User} from {IP}",
    username, Request.RemoteIp);
_logger.LogCritical("Privilege escalation attempt by {User}",
    CurrentUser.Id);
```

### A10: Server-Side Request Forgery (SSRF)
```csharp
// BAD: User controls URL
var response = await _http.GetAsync(userProvidedUrl);

// GOOD: Allowlist domains
if (!_allowedDomains.Contains(new Uri(url).Host))
    throw new SecurityException("Domain not allowed");
```

## Security Checklist

### Input Validation
- [ ] All input validated server-side
- [ ] Whitelist validation preferred
- [ ] Parameterized queries for database
- [ ] Output encoding for HTML/JS/URL

### Authentication
- [ ] Strong password policy enforced
- [ ] Passwords hashed with bcrypt/Argon2
- [ ] MFA available/required
- [ ] Account lockout after failures
- [ ] Secure session management

### Authorization
- [ ] Default deny policy
- [ ] Role-based access control
- [ ] Verify ownership on resources
- [ ] Audit trail for sensitive actions

### Data Protection
- [ ] TLS for all traffic
- [ ] Sensitive data encrypted at rest
- [ ] No secrets in code/config
- [ ] PII minimization

### Error Handling
- [ ] Generic error messages to users
- [ ] Detailed errors only in logs
- [ ] No stack traces exposed

## When to Invoke /owasp

- Implementing authentication/authorization
- Processing user input
- Handling sensitive data
- Before security code review
- Designing new API endpoints
- Evaluating third-party dependencies
