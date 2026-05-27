---
name: spring-security-auth-review
description: Use when reviewing or hardening authentication and authorization in a Spring Boot service that uses Spring Security, JWT, OAuth2, sessions, refresh tokens, or service-to-service auth. Produces an actionable auth review, findings by severity, trust-boundary analysis, secure Spring Security configuration guidance, and remediation priorities. Do not use for general application security review, non-Spring services, or domain authorization policy design outside the framework layer. Pairs with spring-boot-service-scaffold (actuator and security baseline), backend-architecture (trust boundaries, authorization touchpoints, CSRF/CORS posture, and rate-limit behavior), spring-boot-observability-readiness (auth event logging and redaction), and quality-engineering (security test coverage).
---

# Spring Security Auth Review

## When to use

Invoke before shipping any Spring Boot service that handles authenticated requests, or whenever Spring Security, JWT/OAuth2, sessions, refresh tokens, CORS, CSRF, actuator exposure, or service-to-service auth changes materially.

Do not use for general application security review, non-Spring services, frontend-only auth UX, cryptographic protocol design, or domain authorization policy design above the framework layer.

## Inputs

Required:

- Spring Boot service source tree.
- Spring Security configuration, including `SecurityFilterChain` or `SecurityWebFilterChain`.
- Auth model: JWT, OAuth2 resource server, session, BFF, refresh token, or service-to-service.

Optional:

- OpenAPI spec or endpoint list.
- System design or trust boundary map.
- Token issuer/JWKS details.
- Role/scope model.
- CORS and CSRF requirements.
- Deployment profile configuration.
- Existing security tests.

## Operating rules

- Review service-level auth even if an API gateway exists. Gateway-only authorization is not enough.
- Treat authentication and authorization separately. Authenticated does not mean authorized.
- Fail closed. Reject broad `permitAll`, wildcard CORS with credentials, unpinned JWT algorithms, missing audience validation, and hardcoded secrets.
- Match the Spring stack and version. Servlet and reactive security have different configuration and propagation risks.
- Never log raw tokens, credentials, authorization headers, credential cookies, or full JWT claims.
- Findings must be actionable, evidence-backed, severity-classified, and confidence-marked (Confirmed / Probable / Suspected).
- Detect Spring Security version before reviewing. If the service uses `WebSecurityConfigurerAdapter` or `authorizeRequests` (Security 5.x), record a Blocker finding ("obsolete API; upgrade to Spring Security 6 lambda DSL required before further hardening") and adapt the rest of the review to the actual API surface in use — do not write Security 6 recommendations against a Security 5 codebase.
- Halt the review if the service has no `SecurityFilterChain`/`SecurityWebFilterChain` bean and no JWT/OAuth2 dependency. An auth review is not a substitute for missing auth — recommend running `spring-boot-service-scaffold` first to produce a baseline.
- Always scan committed configuration for secrets (`application*.yml`, `bootstrap*.yml`, `.env*`, `src/main/resources/**`). Found secrets are Blocker severity regardless of presumed harmlessness.

## Output contract

The review measures the service against [security-standards](../../../../../standards/security-standards/README.md). That standard is authoritative for:

- AuthN: OAuth2/OIDC default, short-lived service tokens, MFA for production access.
- AuthZ: RBAC at the gateway, ABAC at the service that owns the resource, 401 vs 403 distinction.
- Secrets: zero secrets in source control (Blocker), managed store, rotation cadences.
- Data protection: TLS 1.3, at-rest encryption, no PII/tokens in logs.
- Vulnerability management: SCA, SAST, container scan, CVE SLOs.

Findings reference the specific clause in `security-standards` they violate. Auth event logging and redaction also conform to [observability-standards](../../../../../standards/observability-standards/README.md). CSRF / CORS / `RATE_LIMITED` posture is consistent with [api-standards](../../../../../standards/api-standards/README.md).

## Progressive references

- Read `references/trust-boundaries-and-filter-chain.md` when mapping actors, trust boundaries, `SecurityFilterChain`/`SecurityWebFilterChain`, request matchers, actuator exposure, and filter ordering.
- Read `references/jwt-oauth-token-lifecycle.md` when reviewing JWT/OAuth2 validation, audience checks, algorithms, JWKS caching, refresh tokens, sessions, token storage, secrets, and key rotation.
- Read `references/authorization-browser-and-exposure.md` when reviewing endpoint authorization, method security, tenant isolation, service-to-service auth, CSRF, CORS, cookies, and information leakage.
- Read `references/observability-testing-and-reporting.md` when reviewing audit logging, metrics, security tests, severity classification, and required review artifacts.
- Read `references/auth-review-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/auth-review.template.md` for `auth-review.md`.
- Use `assets/security-config.template.java` when emitting or recommending `SecurityConfig.java`.

## Process

Progress:

- [ ] Step 1: **Pre-flight gate.** Confirm the service has at least one `SecurityFilterChain`/`SecurityWebFilterChain` bean and a JWT/OAuth2/session dependency on the classpath. If neither exists, halt and recommend `spring-boot-service-scaffold`. Then map trust boundaries: actors, clients, tokens, issuers, gateways, services, protected resources, tenant boundaries, and machine-to-machine paths. Create a minimal map if none exists.
- [ ] Step 2: Identify Spring Boot and Spring Security versions and the stack (servlet vs reactive). If `WebSecurityConfigurerAdapter` or `authorizeRequests` is in use, record a Blocker finding and adapt the rest of the review to that API surface. Otherwise review filter chains, matchers, authorization rules, exception handling, filter ordering, method-security enablement, and actuator exposure against the Security 6 lambda DSL.
- [ ] Step 3: Review JWT/OAuth2 validation: algorithm pinning, issuer, audience, expiry, not-before, clock skew, JWKS cache behavior, and key-fetch failure mode.
- [ ] Step 4: Review authorization enforcement: endpoint scopes/roles, method-level checks, ownership checks, tenant scoping, confused deputy risk, and gateway-only assumptions.
- [ ] Step 5: Review refresh token, session, token storage, secret, and key management strategy.
- [ ] Step 6: Review CSRF, CORS, cookie settings, browser flows, and environment-specific exposure rules.
- [ ] Step 7: Review error handling and information leakage: 401/403 behavior, login failures, token validation messages, stack traces, and token logging.
- [ ] Step 8: Review observability and auditability: auth logs, metrics, JWKS failures, refresh anomalies, and sensitive-data redaction.
- [ ] Step 9: Review security testing: unauthenticated, malformed/expired/wrong-audience token, insufficient scope, CSRF, CORS, actuator, refresh replay, and key rotation tests.
- [ ] Step 10: **Secrets scan (mandatory).** Run `grep -rE 'password|secret|token|api[_-]?key' src/main/resources/ **/application*.yml .env*` (or `ripgrep` equivalent). Recommend `trufflehog` or `gitleaks` against git history. Any committed secret is a Blocker finding with file:line evidence.
- [ ] Step 11: **Static analysis (mandatory).** Run a CVE scan (`mvn org.owasp:dependency-check-maven:check` or `snyk test`) and a config-pattern scan (`semgrep --config p/spring-security --config p/jwt` against the source tree). Merge findings into the review with confidence Confirmed. If neither tool is available, record a Medium finding noting the skipped scan.
- [ ] Step 12: Generate `auth-review.md` and, when useful, `SecurityConfig.java` or patch guidance. Validate against [standards/security-standards](../../../../../standards/security-standards/README.md) (each finding cites the specific clause it violates) AND against `references/auth-review-quality-rubric.md`. Revise until both pass or explicitly document any unresolved gap.

## Outputs

- `auth-review.md` with verdict, trust boundary map, findings table, severity, evidence, remediation, and prioritized fixes.
- Optional `SecurityConfig.java` or `.kt` hardening example when the user needs generated config.

Optional outputs when appropriate:

- Threat model notes.
- Token lifecycle diagram.
- RBAC or scope matrix.
- JWKS caching guidance.
- Refresh token schema recommendations.
- Key rotation runbook.

Output rules:

- Lead with blockers and high-risk findings.
- Include code/config evidence for every finding.
- Prefer precise remediation over generic advice.
- Do not expose secrets, raw tokens, or sensitive claims in review output.
- Clearly separate verified findings from assumptions and open questions.

## Quality checks

- [ ] `references/auth-review-quality-rubric.md` was loaded before finalizing.
- [ ] `auth-review.md` follows `assets/auth-review.template.md`.
- [ ] Every finding has severity, component, evidence, impact, and remediation.
- [ ] Spring Security version and Servlet vs reactive stack are identified.
- [ ] The configuration could realistically survive production exposure.

## References

- `references/trust-boundaries-and-filter-chain.md`
- `references/jwt-oauth-token-lifecycle.md`
- `references/authorization-browser-and-exposure.md`
- `references/observability-testing-and-reporting.md`
- `references/auth-review-quality-rubric.md`
- `assets/auth-review.template.md`
- `assets/security-config.template.java`
