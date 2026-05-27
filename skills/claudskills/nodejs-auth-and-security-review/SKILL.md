---
name: nodejs-auth-and-security-review
description: Use when adding authentication and authorization to a Node.js service, hardening its HTTP surface, or running an OWASP-style security review after the service scaffold exists and the auth provider decision is approved or intentionally deferred. Implements the authentication flow (Passport / JWT / OAuth2 / OIDC per architecture/security), the authorization model, secure HTTP headers (helmet), boundary input validation, CSRF and rate-limiting for auth endpoints, secret handling via the config seam, and a security test suite (authz matrix and negative cases). Do not use for the service shell, config, logging, or error tiers, observability vendor wiring, queue or event integration, or performance and resilience gating; use the other Node.js archetype skills instead.
---

# Node.js Auth and Security Review

## When to use

Invoke when adding login, token, or session handling to a Node.js service that has the scaffold baseline, wiring an OAuth2/OIDC provider or JWT verification, defining the authorization model, hardening the HTTP surface (headers, CSRF, rate limiting), or running an OWASP-style review before release.

Do not use for: the service shell, validated config, logging, or error tiers (use `nodejs-service-scaffold`), OpenTelemetry/metrics/SLO wiring (use `nodejs-observability-readiness`), queue or event integration (use `nodejs-queue-and-event-integration`), or performance and resilience gating (use `nodejs-performance-and-resilience`).

## Inputs

Required:

- A service with the `nodejs-service-scaffold` baseline (principal-provider seam, validated config, error tiers present).
- Approved `architecture/security` decisions on auth provider, session vs token strategy, and secret handling — or explicit confirmation they are intentionally deferred.

Optional:

- Approved `backend-architecture.md` for domain/route boundaries and the public/internal API split.
- Identity provider details (issuer, audience, JWKS URI) if OIDC/OAuth2.
- Authorization model (RBAC roles, ABAC attributes, or per-resource scopes) if `architecture/security` is silent.
- Compliance constraints (PII handling, audit-log requirements).

## Operating rules

- Never invent the auth provider or session strategy. Provider, session vs token model, token lifetime, and secret handling belong to `architecture/security`. If silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.
- Extend the scaffold seam; do not replace it. Token verification and principal population fill the `nodejs-service-scaffold` principal-provider shell — they do not re-implement config, logging, or error tiers.
- Authentication and authorization are distinct and both required: verifying identity (authentication) never implies permission (authorization). Every protected route resolves an explicit authorization decision; default-deny.
- Validate every input at the boundary with a schema (zod or equivalent); reject unknown fields. Never trust client-supplied identifiers for authorization (no IDOR — authorize against the authenticated principal, not a body/path id alone).
- Secrets flow through the validated config seam only — signing keys, client secrets, and JWKS URIs are config-validated at boot, never hardcoded, logged, or committed. Tokens, passwords, and `authorization` headers are redacted in logs.
- Secure HTTP headers are mandatory: helmet (or equivalent) with a deny-by-default Content-Security-Policy, HSTS, no `x-powered-by`. CSRF protection on cookie-session state-changing routes; rate limiting on authentication endpoints.
- Fail closed: an auth check that errors denies access. Never `catch` an authorization error into an allow.
- A security review without negative tests is not a review. Provide tests for unauthenticated access, wrong-role access, expired/tampered token, and IDOR — each asserting denial.
- A change that does not pass typecheck, lint, the security test suite, and the boot smoke check is not done. Fix and re-run.

## Output contract

The auth and hardening layer MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — no secrets in source/config/image; default-deny authorization; secure headers; input validated at the boundary; secrets via the config seam.
- [api-standards](../../../../../standards/api-standards/README.md) — consistent auth error shape and status codes (401 vs 403); documented public/protected route split.

Upstream contract: `architecture/security` is the source of truth for auth provider, session vs token strategy, token lifetime, and secret handling; `backend-architecture.md` is the source of truth for route/domain boundaries. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/nodejs-auth-playbook.md` when implementing any owned area or running the review.
- Read `references/nodejs-auth-quality-rubric.md` before declaring the work complete.
- Use `assets/nodejs-auth-and-security-review.template.md` as the middleware, guard, and test-matrix reference.

## Process

1. Gather context: load `architecture/security` (provider, session vs token, token lifetime, secret handling) and `backend-architecture.md` (route/domain boundaries, public vs protected split). Confirm the scaffold baseline exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Extend config: add the auth-related variables (issuer, audience, JWKS URI, client id/secret, signing key, session secret) to the scaffold's zod config schema and `.env.example` with placeholders — no real values.
3. Implement authentication: the verification strategy from `architecture/security` (Passport strategy, JWT/JWKS verification, or OAuth2/OIDC code flow) in `src/auth/`, populating the scaffold principal-provider seam with a typed `Principal`. Reject expired, malformed, or wrong-audience tokens.
4. Implement authorization: a default-deny guard (middleware/hook/Nest guard) resolving an explicit decision per route from the model in `architecture/security` (RBAC/ABAC/scopes). Authorize against the authenticated principal, never a client-supplied id alone.
5. Harden the HTTP surface: helmet (or equivalent) with a deny-by-default CSP and HSTS, remove `x-powered-by`, CSRF protection on cookie-session state-changing routes, and rate limiting on authentication endpoints. Wire these in the scaffold app factory after the request-context middleware.
6. Handle secrets: ensure every credential resolves through the validated config seam; add redaction for `authorization`, token, and password fields to the scaffold logger if not already present; document key/secret rotation in the service README.
7. Run the OWASP-style review: walk the playbook checklist (authn, authz/IDOR, injection, secrets, headers, rate limiting, error leakage, dependency audit via `npm audit`/equivalent). Record findings and resolutions in the service README security section.
8. Write security tests: a negative-case suite asserting denial for unauthenticated access, wrong-role/scope access, expired and tampered tokens, and IDOR; plus positive cases for each role. Include an authorization matrix table in the test file.
9. Build verification (mandatory): run `tsc --noEmit`, lint, the full test command (including the security suite), and the boot smoke check. Fix and re-run on failure. Then validate against the Output contract standards; revise until all pass or explicitly document any unresolved gap in the service README.

## Outputs

Required:

- Authentication implementation filling the scaffold principal-provider seam with a typed `Principal` (no shell logic left).
- Default-deny authorization guard with an explicit per-route decision and an authorization matrix.
- Hardened HTTP surface: helmet/CSP/HSTS, CSRF where applicable, rate-limited auth endpoints, no `x-powered-by`.
- Auth config added to the validated schema and `.env.example` (placeholders only); secret-rotation note in the README.
- OWASP-style review findings + resolutions recorded in the service README.
- Security test suite (negative + positive cases) with an authorization matrix.

Output rules:

- No secrets in source, committed config, `.env.example`, the image, or logs.
- Authentication never implies authorization; every protected route has an explicit default-deny decision.
- The scaffold's config, logging, and error tiers are extended, not duplicated.
- Auth checks fail closed — an error denies access.

## Quality checks

- [ ] `tsc --noEmit`, lint, the security test suite, and the boot smoke check all pass (or a skip is documented with reason).
- [ ] The principal-provider seam is filled with a typed `Principal`; no scaffold shell TODO remains for auth.
- [ ] Every protected route resolves an explicit default-deny authorization decision; unauthenticated and wrong-role access return 401/403 respectively (test-verified).
- [ ] Authorization uses the authenticated principal, not a client-supplied id alone (IDOR negative test passes).
- [ ] Expired and tampered tokens are rejected (test-verified).
- [ ] helmet/CSP/HSTS are set, `x-powered-by` is removed, CSRF protects cookie-session state-changing routes, auth endpoints are rate limited.
- [ ] All auth secrets resolve through the validated config seam; `authorization`/token/password fields are redacted in logs.
- [ ] No secrets appear in source, committed config, `.env.example`, or the image.
- [ ] `npm audit` (or equivalent) was run and findings are recorded with resolutions or an accepted-risk note.
- [ ] The service README records the OWASP-review findings and the secret-rotation procedure.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md).
- Baseline this extends: `nodejs-service-scaffold`. Related: `nodejs-observability-readiness`, `nodejs-queue-and-event-integration`, `nodejs-performance-and-resilience`.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`api-standards`](../../../../../standards/api-standards/README.md).
