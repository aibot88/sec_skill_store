---
name: principle-security
description: Security design principles — trust boundaries and input validation, authentication vs authorization, secrets handling, secure defaults and defense in depth, lightweight threat modeling, cryptography hygiene, attack-surface minimization. Auto-load when designing auth, discussing authn or authz, handling secrets, defining trust boundaries, validating untrusted input, considering SSRF or CSRF, choosing session or JWT mechanics, configuring TLS, picking an encryption primitive, or weighing least-privilege trade-offs.
---

# Security

Security bugs are design bugs. They are cheapest to fix before the first line of code is written. This skill teaches the principles that prevent security bugs at design time; the `security-auditor` subagent audits the resulting diff against vulnerability categories, secret patterns, and language foot-guns post-implementation.

## Trust Boundaries

Name every boundary where data crosses trust levels. Validate at the boundary, not inside it.
- Name the boundary explicitly: user-to-service, service-to-service, internal-to-DB, public-to-admin.
- Validate at the boundary once — do not scatter input checks throughout internal code.
- Allowlist what is known-good; denylist silently grows as attackers find gaps.
- Structural validity (is it an integer?) is not semantic validity (is it *your* integer?).
- Re-validate whenever data crosses a boundary again — even "internal" calls.

## Authentication is Not Authorization

AuthN proves identity. AuthZ enforces policy. Confusing them produces exploitable gaps.
- Authentication answers "who are you?"; authorization answers "can you do this to that?".
- Enforce authorization on the resource, not the route — routes change; resources don't.
- Default-deny: if no explicit grant exists, the answer is no.
- Guard against confused deputy: a service acting on behalf of a user must not exceed that user's privileges.
- Token revocation and session invalidation are Day-1 design concerns, not afterthoughts.

## Secrets Belong in Secret Stores

A secret in source is a secret that belongs to everyone who ever had read access.
- Never store secrets in source, env files committed to git, URLs, or log output.
- Prefer a secret store (Vault, AWS Secrets Manager, GCP Secret Manager) over env vars for sensitive values.
- Design secret rotation from Day 1 — rotation that requires a deployment is already too slow.
- Scrub sensitive values at every logging boundary; structured logging makes this tractable.
- `.env.example` contains placeholder values only — never real tokens, passwords, or keys.

## Secure Defaults & Defense in Depth

A system should be secure without any extra configuration.
- Fail closed: if a security check cannot complete, deny access — never assume permission.
- Complete mediation: verify every access, every time — no auth caching that skips the check.
- Layer controls — network, service, data — so that one breach does not mean full compromise.
- Use conservative framework defaults; never disable security features for "dev convenience" that ships.
- Defense in depth: assume the outer layer will be breached; inner layers must hold independently.

## Cryptography: Use, Don't Build

The algorithm is the easy part; key management and misuse-resistance are where production systems fail.
- Pick a construction, not an algorithm: use `nacl/box`, `AES-GCM`, `Argon2id` — not raw AES.
- Key management is where cryptography fails in production: rotation, storage, access, derivation.
- Red flags: nonce reuse, `==` for MAC comparison, a custom HMAC scheme, PRNG instead of CSPRNG.
- Symmetric comparison of secrets must use constant-time comparison to prevent timing attacks.
- Pin one cipher suite for new services; do not negotiate downward.

## Least Privilege & Smallest Surface

Every capability that exists is a capability that can be abused.
- Issue the smallest token: tightest scope, narrowest audience, shortest viable lifetime.
- Expose the smallest API: every endpoint is an attack surface; delete what is not needed.
- Grant the smallest privilege: DB read-only for read paths; row-level isolation where possible.
- Prefer short-lived credentials with fast expiry over long-lived tokens with revocation lists.
- Audit what is reachable from the network vs what the config intends to expose.

## When Pre-Write Security Thinking is Overkill

- Local-only scripts with no network access and no secrets.
- Throwaway prototypes that will never leave a developer's machine.
- Internal tooling behind fully trusted, non-internet-routable networks.
- Single-file analysis scripts that read immutable data and produce no output artifacts.
- Gated PoC code behind a feature flag with no user-facing surface.

## Red Flags

| Flag | Problem |
|------|---------|
| Custom authentication scheme | Hand-rolled auth misses decades of hardened library work |
| Denylist input filter | New bypass vectors emerge; allowlist is the only durable approach |
| Permission check at the route/controller layer | Moves as routes change; resource-level enforcement is the invariant |
| Real value in `.env.example` | Anyone who clones the repo has the credential |
| JWT with no revocation strategy | Compromised token is valid until expiry with no recourse |
| Long-lived all-scope access tokens | Maximum blast radius on compromise; scope to the operation |
| Verbose error responses to untrusted callers | Leaks internals; production errors should be opaque reference IDs |
| Encryption scheme chosen by algorithm name only | Algorithm ≠ construction; misuse is the rule, not the exception |
