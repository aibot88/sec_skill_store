---
name: backend-security
description: Backend development with security-first approach. Use when building APIs, handling data, implementing authentication, or addressing security vulnerabilities.
---

# Backend Development with Security Focus

Secure backend development prevents vulnerabilities while maintaining functionality. Every endpoint, database query, and user input is a potential attack vector.

## Core Security Principles

**Golden rule**: Never trust client input. Always validate, sanitize, and verify.

1. **Defense in Depth** - Multiple layers of security controls
2. **Principle of Least Privilege** - Grant minimum necessary permissions
3. **Fail Securely** - Fail to a secure state when errors occur
4. **Assume Breach** - Design assuming attackers are already inside
5. **Security by Design** - Build security from the start, not as afterthought

## API Security

**Key Principles**:
- Use UUIDs instead of sequential IDs to prevent enumeration
- Implement rate limiting on all endpoints
- Apply authentication middleware before business logic
- Validate all input formats (UUID, email, etc.)
- Use parameterized queries to prevent SQL injection
- Return only necessary fields (don't expose passwords, internal data)
- Version your APIs (`/api/v1/`, `/api/v2/`)
- Limit request payload sizes (JSON: 10kb, files: 5MB max)
- Whitelist allowed file types for uploads
- Always verify authorization (user owns resource or has permissions)

## Authentication & Authorization

**JWT Best Practices**:
- Use strong secrets (64+ characters, generate with `crypto.randomBytes(64).toString('hex')`)
- Short-lived access tokens (15 min) + long-lived refresh tokens (7 days)
- Store minimal payload (user ID only, no sensitive data)
- Validate token type (access vs refresh) and expiration
- Use separate secrets for access and refresh tokens
- Support secret rotation for zero-downtime updates

**Password Security**:
- Enforce strong passwords (12+ chars, uppercase, lowercase, number, special char)
- Hash with bcrypt (salt rounds: 12+)
- Never store plaintext passwords
- Implement account lockout (5 failed attempts = 15 min lock)
- Use generic error messages (don't reveal if email exists)
- Consider MFA for sensitive operations

**Role-Based Access Control (RBAC)**:
- Define roles (Admin, User, Guest) and permissions separately
- Map roles to permissions explicitly
- Check authentication first, then authorization
- Create reusable middleware for permission checks
- Use enums for type safety
- Always verify resource ownership (IDOR prevention)

## Input Validation & Sanitization

**Schema Validation** (use Zod, Joi, or similar):
- Define schemas for all API inputs (body, params, query)
- Validate types, formats, lengths, patterns
- Use `.trim()`, `.toLowerCase()`, `.optional()`, `.default()` as needed
- Return detailed validation errors (field + message)
- Create reusable validation middleware

**SQL Injection Prevention**:
- ALWAYS use parameterized queries (`$1`, `$2` placeholders)
- NEVER concatenate strings in SQL queries
- Use ORMs (Prisma, TypeORM) when possible for built-in protection
- Escape special characters if parameterization isn't possible

**XSS Prevention**:
- Sanitize HTML input with DOMPurify or similar
- Whitelist allowed tags and attributes
- Escape output when rendering user content
- Use Content Security Policy headers
- Prefer storing plain text; sanitize only when HTML is necessary

**Path Traversal Prevention**:
- Validate filenames with regex (alphanumeric, dash, underscore, dot only)
- Use `path.resolve()` and check resolved path starts with allowed directory
- Never trust user-provided paths directly
- Whitelist allowed file extensions
- Check file existence before serving

## Database Security

**Connection Security**:
- Use SSL/TLS in production (rejectUnauthorized: true)
- Store credentials in environment variables
- Configure connection pool limits (max: 20, timeout: 2000ms)
- Handle connection errors gracefully
- Use separate read-only users for reporting queries

**Query Security**:
- Always use parameterized queries (prevents SQL injection)
- Wrap multi-step operations in transactions
- Use ROLLBACK on errors
- Log query errors (but not sensitive data)
- Release connections after use

**Data Encryption at Rest**:
- Encrypt sensitive fields (credit cards, SSN, PII)
- Use AES-256-GCM for encryption
- Store IV and auth tag with encrypted data
- Use strong encryption keys (32 bytes, in hex)
- Never store encryption keys in code - use environment variables

## Error Handling

**Secure Error Responses**:
- Never expose stack traces or internal details in production
- Log full error details server-side (path, method, user, stack)
- Return generic messages to clients ("Internal server error")
- Use custom error classes with isOperational flag
- Differentiate between operational errors (404, 400) and programmer errors (500)
- Include detailed errors only in development mode
- Use centralized error handling middleware

## Security Headers & CORS

**Essential Security Headers** (use helmet.js):
- `X-Frame-Options: DENY` - Prevent clickjacking
- `X-Content-Type-Options: nosniff` - Prevent MIME sniffing
- `X-XSS-Protection: 1; mode=block` - Enable XSS filter
- `Strict-Transport-Security` - Force HTTPS (max-age=31536000; includeSubDomains)
- `Content-Security-Policy` - Define allowed content sources
- `Referrer-Policy: strict-origin-when-cross-origin` - Control referrer info
- `Permissions-Policy` - Disable unused browser features

**CORS Configuration**:
- Never use `origin: '*'` in production
- Whitelist specific origins in environment variables
- Allow localhost only in development
- Enable credentials for cookie-based auth
- Cache preflight requests (maxAge: 86400)
- Specify allowedHeaders (Content-Type, Authorization)
- Set exposedHeaders for pagination (X-Total-Count)

## Secrets Management

**Environment Variables**:
- Never hardcode secrets in source code
- Use `.env` files (add to `.gitignore`)
- Validate all environment variables on startup using Zod
- Enforce minimum lengths for secrets (64+ characters)
- Validate formats (email, URL, specific prefixes like `sk_`)
- Exit process if required secrets are missing
- Use cloud secret managers in production (AWS Secrets Manager, Vault)

**Secrets Rotation**:
- Support multiple active secrets for zero-downtime rotation
- Try current secret first, fallback to previous
- Set expiration dates for old secrets
- Rotate secrets quarterly or after suspected compromise

## Rate Limiting & DoS Prevention

**Rate Limiting Strategy**:
- Use Redis store for distributed rate limiting
- General API: 100 requests per 15 minutes
- Auth endpoints: 5 attempts per hour (skip successful requests)
- Key by user ID if authenticated, otherwise IP
- Progressive limits (authenticated users get higher limits)
- Return 429 status with clear error message

**Request Throttling**:
- Slow down after threshold (50 requests) before blocking
- Add incremental delays (500ms per extra request)
- Set maximum delay (20 seconds)
- Prevents aggressive blocking while discouraging abuse

## Logging & Monitoring

**Structured Logging** (use Winston or Pino):
- Use JSON format with timestamps
- Log levels: error, warn, info, debug
- Include context: method, URL, status, duration, userId, IP
- Separate error.log and combined.log files
- Console logging in development only
- Never log sensitive data (passwords, tokens, credit cards)
- Sanitize objects before logging (redact sensitive fields)

**Security Event Monitoring**:
- Track critical events (failed logins, invalid tokens, permission denials)
- Log IP, user agent, path, timestamp for all security events
- Alert on SQL injection attempts, XSS attempts
- Integrate with monitoring services (Sentry, DataDog, New Relic)
- Set up alerts for suspicious patterns (multiple failed logins, rate limit exceeded)
- Review logs regularly for anomalies

## Common Vulnerabilities (OWASP Top 10)

**SQL Injection**:
- Always use parameterized queries (`$1`, `$2`) - NEVER string concatenation
- Use ORMs (Prisma, TypeORM) for built-in protection

**Cross-Site Scripting (XSS)**:
- Sanitize HTML input (DOMPurify)
- Escape output when rendering
- Use Content Security Policy headers

**Cross-Site Request Forgery (CSRF)**:
- Use CSRF tokens for cookie-based auth (csurf package)
- Set httpOnly, secure, sameSite: 'strict' on cookies
- For JWT APIs, validate origin and use proper CORS

**Insecure Deserialization**:
- NEVER use eval() or Function() with user input
- Use JSON.parse + schema validation only
- Avoid vm.runInNewContext and similar

**XML External Entities (XXE)**:
- Disable external entity resolution in XML parsers
- Use JSON instead of XML when possible

**Insecure Direct Object References (IDOR)**:
- Always verify resource ownership before returning data
- Check `resource.userId === req.user.uuid` or admin status
- Use UUIDs instead of sequential IDs

## Testing Security

**Unit Tests**:
- Test password validation (reject weak, accept strong)
- Test password hashing (bcrypt format, verify correct/incorrect)
- Test authorization (401 without token, 403 without permissions)
- Test input validation (reject malicious patterns)

**Integration Tests**:
- Test SQL injection attempts (should return 400, not all data)
- Test rate limiting (10+ requests should trigger 429)
- Test IDOR (users can't access others' resources)
- Test CSRF protection on state-changing endpoints

**Automated Security Scanning**:
- `npm audit` - Check dependencies for vulnerabilities
- `npx snyk test` - Continuous vulnerability monitoring
- `eslint-plugin-security` - Static analysis for security issues
- `gitleaks detect` - Check for hardcoded secrets in code
- Run scans in CI/CD pipeline

## Implementation Guidelines

**IMPORTANT**: Do NOT create summary markdown files, documentation files, or README files unless explicitly requested by the user.

## Best Practices

1. **Never Trust User Input** - Validate, sanitize, and escape all input regardless of source
2. **Use Parameterized Queries** - Always use prepared statements for database queries
3. **Implement Proper Authentication** - Use industry-standard methods (JWT, OAuth) with secure configuration
4. **Apply Principle of Least Privilege** - Grant minimum necessary permissions to users and services
5. **Encrypt Sensitive Data** - Use encryption at rest and in transit (TLS/SSL)
6. **Keep Dependencies Updated** - Regularly update packages and scan for vulnerabilities
7. **Implement Rate Limiting** - Prevent abuse and DoS attacks on all endpoints
8. **Log Security Events** - Monitor and alert on suspicious activities
9. **Handle Errors Securely** - Never expose stack traces or internal details to clients
10. **Use Security Headers** - Implement helmet.js and configure CSP, HSTS, etc.
11. **Validate Environment Config** - Ensure all required secrets are present on startup
12. **Implement Request Timeouts** - Prevent resource exhaustion from slow requests
13. **Use HTTPS Everywhere** - Never transmit sensitive data over unencrypted connections
14. **Implement CSRF Protection** - For cookie-based auth, use CSRF tokens
15. **Regular Security Audits** - Conduct code reviews and penetration testing
16. **Have an Incident Response Plan** - Prepare for security breaches before they happen
17. **Minimize Attack Surface** - Disable unnecessary features and endpoints
18. **Use Security Linters** - Integrate security scanning in CI/CD pipeline
19. **Implement Proper Session Management** - Use secure, httpOnly cookies with appropriate expiration
20. **Document Security Decisions** - Maintain a threat model and security architecture docs

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Express.js Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [API Security Best Practices](https://github.com/shieldfy/API-Security-Checklist)
