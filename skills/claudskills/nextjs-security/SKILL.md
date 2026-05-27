---
name: nextjs-security
description: >
  This skill should be used when working on security aspects of a Next.js application or when
  the user asks about Next.js security best practices. Trigger when: implementing authentication
  or session management; writing Server Actions or API Route Handlers; configuring security
  headers (CSP, HSTS, X-Frame-Options); preventing CSRF or XSS; managing environment variables
  or secrets; using the "server-only" package; creating a Data Access Layer; implementing rate
  limiting; configuring middleware for security; using React Taint APIs; auditing Next.js
  security; protecting against IDOR; implementing httpOnly cookies; sanitizing user input;
  using Zod for validation; or reviewing code for OWASP vulnerabilities in Next.js applications.
---

# Next.js Security: Hardening Standards

Apply these security standards to every Next.js application. Security is a multi-layered concern spanning the client, server, and network boundaries. Every Server Action and Route Handler is a public endpoint — treat all input as hostile.

## Core Principle

> **Defense in Depth**: Never rely on a single security boundary. Middleware can be bypassed (CVE-2025-29927). Client-side checks can be spoofed. Every layer must independently verify authentication, authorization, and input validity.

---

## 1. The 5-Layer Server Action Security Checklist

Every Server Action and Route Handler **must** implement all five layers:

### Layer 1: Authentication
Verify the user is logged in. Use `cookies()` to read session tokens set as `httpOnly`, `Secure`, `SameSite=Lax` (or `Strict`) cookies. **Never** store tokens in `localStorage`.

### Layer 2: Input Validation
Never trust client input. Validate and parse with **Zod** or **Valibot** using `safeParse()`. Reject invalid input before any database operation.

### Layer 3: Authorization
Verify the authenticated user has permission to access or mutate the specific resource. Prevents Insecure Direct Object Reference (IDOR) attacks.

### Layer 4: Rate Limiting
Protect against brute-force and DDoS using tools like `@upstash/ratelimit`. Apply per-user and per-IP limits.

### Layer 5: Safe Error Handling
Catch errors gracefully. Return generic messages to the client. **Never** expose backend stack traces, database errors, or internal paths.

```typescript
'use server';
import { z } from 'zod';
import { verifyAuth } from '@/lib/auth';

const schema = z.object({
  amount: z.number().positive().max(10000),
  userId: z.string().uuid(),
});

export async function createTransaction(data: unknown) {
  const session = await verifyAuth();                    // 1. Auth
  if (!session) throw new Error('Unauthorized');

  const parsed = schema.safeParse(data);                 // 2. Validate
  if (!parsed.success) throw new Error('Invalid input');

  if (session.user.id !== parsed.data.userId)            // 3. Authorize
    throw new Error('Forbidden');

  // 4. Rate limit (await rateLimit(session.user.id))

  try {
    // Database operation
    return { success: true };
  } catch (error) {
    console.error('Server error:', error);               // 5. Safe errors
    throw new Error('An internal error occurred');
  }
}
```

---

## 2. Authentication & Session Management

- **Prefer passkeys (WebAuthn/FIDO2)** over passwords. Enforce MFA for high-risk actions.
- **Use `httpOnly` cookies** for session tokens — `Secure`, `SameSite=Lax` (or `Strict`). Never `localStorage`.
- **Rotate session IDs** on privilege escalation. Set reasonable expiration times.
- **Validate `returnTo` parameters** — ensure they are relative paths to prevent open redirect attacks.

---

## 3. Server Components & Data Access Security

### The `server-only` Package
Mark any module containing database queries, API keys, or sensitive logic with `import 'server-only'`. The build fails immediately if accidentally imported into a Client Component.

### Data Access Layer (DAL)
Centralize all database queries in a dedicated server-only DAL that:
1. Verifies authorization on every call
2. Returns minimal, safe DTOs (never raw database records)
3. Wraps functions with `React.cache()` for deduplication
4. Restricts `process.env` access to this layer only

### React Taint APIs
Use `taintObjectReference` or `taintUniqueValue` to mark sensitive data. Next.js throws an error if tainted data crosses the Server→Client boundary. Check current API status in Next.js docs — these APIs may still be experimental in some versions.

---

## 4. CSRF Prevention

- **Server Actions** automatically compare `Origin` vs. `Host` headers and abort on mismatch.
- If behind a reverse proxy with different frontend/backend domains, configure `serverActions.allowedOrigins` in `next.config.ts`.
- For Route Handlers using cookies, enforce `SameSite=Lax/Strict` and consider third-party CSRF tokens (`@edge-csrf/nextjs`).

---

## 5. XSS Prevention

- React auto-escapes strings by default — the main risk is bypassing this.
- **Avoid `dangerouslySetInnerHTML`**. If required (e.g., markdown), sanitize with `DOMPurify` or `isomorphic-dompurify` first.
- **Validate redirect URLs** — only allow relative paths in `returnTo` parameters.

---

## 6. Security Headers

Apply these headers via `next.config.ts` `headers()` or middleware/proxy:

| Header | Value | Purpose |
|--------|-------|---------|
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'nonce-...' 'strict-dynamic'` | Prevents unauthorized script execution |
| `X-Frame-Options` | `DENY` | Prevents clickjacking |
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-sniffing |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` | Enforces HTTPS |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Controls referrer leakage |

---

## 7. Environment Variables

- **`NEXT_PUBLIC_` prefix** exposes variables to the browser bundle. **Never** use for database URLs, JWT secrets, or private API keys.
- Exclude `.env` and `.env.local` from version control. Use secret managers for production (AWS Secrets Manager, Vault, Vercel Env Vars).
- Restrict `process.env` access to the DAL to prevent accidental frontend leakage.
- When self-hosting across multiple instances, synchronize `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` to prevent cross-instance request failures.

---

## 8. Middleware Security Warning

**Critical:** Do **not** treat middleware (or `proxy.ts` in Next.js 16) as the sole security boundary. CVE-2025-29927 demonstrated that attackers could spoof headers to bypass middleware authorization entirely.

**Always re-verify auth** inside:
- Route Handlers
- Server Actions
- Data Access Layer functions

Middleware is appropriate for edge-level routing, header injection, and redirects — not for complete access control.

---

## 9. CI/CD Security Integration

- **SCA scanning:** Dependabot or Socket for dependency vulnerabilities.
- **SAST scanning:** Static analysis for code-level security issues.
- **Secret scanning:** TruffleHog or similar to catch leaked credentials.
- Block merges until all security checks pass.

---

## Additional Resources

### Reference Files

For the complete pre-deployment security audit checklist with code examples:
- **`references/security-checklist.md`** — Full security audit checklist with configuration patterns, header examples, and common vulnerability patterns

### Related Skills

- **`nextjs-best-practices`** — Architecture, data fetching, performance
- **`nextjs-testing`** — Testing auth flows, API routes, security scenarios
- **`nextjs-troubleshooting`** — Debugging auth issues, middleware problems
