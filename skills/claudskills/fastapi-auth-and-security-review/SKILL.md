---
name: fastapi-auth-and-security-review
description: Use when adding auth/authz, HTTP-surface hardening, or an OWASP review to a scaffolded FastAPI service after the auth provider decision is approved or deferred. Adds the authentication, default-deny authz, hardening, and security-test layer the scaffold defers. Not for observability, tasks, or performance.
---

# FastAPI Auth and Security Review

## When to use

Invoke when adding login, token, or API-key handling to a FastAPI service that has the scaffold baseline, wiring an OAuth2/OIDC provider or JWT verification, defining the authorization model, hardening the HTTP surface (headers, CSRF, rate limiting), or running an OWASP-style review before release.

Do not use for: the service shell, settings, logging, or error tiers (use `fastapi-service-scaffold`), OpenTelemetry/metrics/SLO wiring (use `fastapi-observability-readiness`), task or event integration (use `fastapi-async-and-task-integration`), or performance and resilience gating (use `fastapi-performance-and-resilience`).

## Inputs

Required:

- A service with the `fastapi-service-scaffold` baseline (principal `Depends` seam, validated settings, error tiers present).
- Approved `architecture/security` decisions on auth provider, session vs token strategy, and secret handling — or explicit confirmation they are intentionally deferred.

Optional:

- Approved `backend-architecture.md` for route/domain boundaries and the public/internal API split.
- Identity provider details (issuer, audience, JWKS URI) if OIDC/OAuth2.
- Authorization model (RBAC roles, ABAC attributes, or OAuth scopes) if `architecture/security` is silent.
- Compliance constraints (PII handling, audit-log requirements).

## Operating rules

- Never invent the auth provider or session strategy. Provider, session vs token model, token lifetime, and secret handling belong to `architecture/security`. If silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.
- Extend the scaffold seam; do not replace it. Token verification and principal population fill the `fastapi-service-scaffold` principal `Depends` shell — they do not re-implement settings, logging, or error tiers.
- Authentication and authorization are distinct and both required: verifying identity never implies permission. Every protected route resolves an explicit authorization decision; default-deny.
- Validate every input at the boundary with a Pydantic model; reject unknown fields (`model_config = ConfigDict(extra="forbid")`). Never trust client-supplied identifiers for authorization (no IDOR — authorize against the authenticated principal, not a path/body id alone).
- Secrets flow through the validated settings seam only — signing keys, client secrets, and JWKS URIs are settings-validated at boot, never hardcoded, logged, or committed. Tokens, passwords, and `authorization` headers are redacted in logs.
- Secure HTTP headers are mandatory: a security-headers middleware with a deny-by-default Content-Security-Policy, HSTS, and no server banner. CSRF protection on cookie-session state-changing routes; rate limiting on authentication endpoints.
- Fail closed: an auth check that errors denies access. Never catch an authorization error into an allow.
- A security review without negative tests is not a review. Provide tests for unauthenticated access, wrong-role access, expired/tampered token, and IDOR — each asserting denial.
- A change that does not pass `mypy`, `ruff`, the security test suite, and the boot smoke check is not done. Fix and re-run.

## Output contract

The auth and hardening layer MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — no secrets in source/settings/image; default-deny authorization; secure headers; input validated at the boundary; secrets via the settings seam.
- [api-standards](../../../../../standards/api-standards/README.md) — consistent auth error shape and status codes (401 vs 403); documented public/protected route split.

Upstream contract: `architecture/security` is the source of truth for auth provider, session vs token strategy, token lifetime, and secret handling; `backend-architecture.md` is the source of truth for route/domain boundaries. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/fastapi-auth-playbook.md` when implementing any owned area or running the review.
- Read `references/fastapi-auth-quality-rubric.md` before declaring the work complete.
- Use `assets/fastapi-auth-and-security-review.template.md` as the dependency, guard, and test-matrix reference.

## Process

1. Gather context: load `architecture/security` (provider, session vs token, token lifetime, secret handling) and `backend-architecture.md` (route/domain boundaries, public vs protected split). Confirm the scaffold baseline exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Extend settings: add the auth-related variables (issuer, audience, JWKS URI, client id/secret, signing key, session secret) to the scaffold `Settings` model and `.env.example` with placeholders — no real values.
3. Implement authentication: the verification strategy from `architecture/security` (OAuth2/OIDC code flow, JWT/JWKS verification, or API-key) in `app/auth/`, populating the scaffold principal `Depends` seam with a typed `Principal`. Reject expired, malformed, or wrong-audience tokens.
4. Implement authorization: a default-deny dependency (`Security`/`Depends` guard) resolving an explicit decision per route from the model in `architecture/security` (RBAC/ABAC/scopes). Authorize against the authenticated principal, never a client-supplied id alone.
5. Harden the HTTP surface: a security-headers middleware with a deny-by-default CSP and HSTS, no server banner, CSRF protection on cookie-session state-changing routes, and rate limiting on authentication endpoints. Wire these after the scaffold request-context middleware.
6. Handle secrets: ensure every credential resolves through the validated settings seam; add redaction for `authorization`, token, and password fields to the scaffold structlog processors if not already present; document key/secret rotation in the service README.
7. Run the OWASP-style review: walk the playbook checklist (authn, authz/IDOR, injection, secrets, headers, rate limiting, error leakage, dependency audit via `pip-audit`). Record findings and resolutions in the service README security section.
8. Write security tests: a negative-case suite asserting denial for unauthenticated access, wrong-role/scope access, expired and tampered tokens, and IDOR; plus positive cases for each role. Include an authorization matrix table in the test file.
9. Build verification (mandatory): run `mypy`, `ruff check`, the full test command (including the security suite), and the boot smoke check. Fix and re-run on failure. Then validate against the Output contract standards; revise until all pass or explicitly document any unresolved gap in the service README.

## Outputs

Required:

- Authentication implementation filling the scaffold principal `Depends` seam with a typed `Principal` (no shell logic left).
- Default-deny authorization dependency with an explicit per-route decision and an authorization matrix.
- Hardened HTTP surface: security headers/CSP/HSTS, CSRF where applicable, rate-limited auth endpoints, no server banner.
- Auth settings added to the validated model and `.env.example` (placeholders only); secret-rotation note in the README.
- OWASP-style review findings + resolutions recorded in the service README.
- Security test suite (negative + positive cases) with an authorization matrix.

Output rules:

- No secrets in source, committed config, `.env.example`, the image, or logs.
- Authentication never implies authorization; every protected route has an explicit default-deny decision.
- The scaffold's settings, logging, and error tiers are extended, not duplicated.
- Auth checks fail closed — an error denies access.

## Quality checks

- [ ] `mypy`, `ruff check`, the security test suite, and the boot smoke check all pass (or a skip is documented with reason).
- [ ] The principal `Depends` seam is filled with a typed `Principal`; no scaffold shell TODO remains for auth.
- [ ] Every protected route resolves an explicit default-deny authorization decision; unauthenticated and wrong-role access return 401/403 respectively (test-verified).
- [ ] Authorization uses the authenticated principal, not a client-supplied id alone (IDOR negative test passes).
- [ ] Expired and tampered tokens are rejected (test-verified).
- [ ] Security headers/CSP/HSTS are set, no server banner, CSRF protects cookie-session state-changing routes, auth endpoints are rate limited.
- [ ] All auth secrets resolve through the validated settings seam; `authorization`/token/password fields are redacted in logs.
- [ ] No secrets appear in source, committed config, `.env.example`, or the image.
- [ ] `pip-audit` (or equivalent) was run and findings are recorded with resolutions or an accepted-risk note.
- [ ] The service README records the OWASP-review findings and the secret-rotation procedure.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md).
- Baseline this extends: `fastapi-service-scaffold`. Related: `fastapi-observability-readiness`, `fastapi-async-and-task-integration`, `fastapi-performance-and-resilience`.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`api-standards`](../../../../../standards/api-standards/README.md).
