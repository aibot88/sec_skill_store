# Skill: Insight Engineering (Guidelines)

## Critical Thread-Start Guardrail (Mandatory)
- Before writing or editing code in each thread, run this checklist and keep it active through completion:
- Deduplicate near-identical logic early (request parsing, fetch wrappers, mapping, formatter helpers).
- Extract non-obvious numeric literals into named constants/config (especially limits, weights, thresholds, pace factors).
- Use stable list keys (prefer IDs; otherwise deterministic prefix + index fallback) and avoid brittle concatenations.
- Avoid raw one-off design tokens in components (colors, spacing, radii); prefer shared theme tokens/config where practical.
- If any item above is violated in touched code, fix it in the same thread before shipping.

## Rules
- Critical: always avoid magic numbers in touched code. Any limit, TTL, retry count, weight, threshold, interval, or heuristic must use a named constant or config entry.
- PR freshness is mandatory: if there is a gap since the last implementation cycle and the previous PR may have been merged, create a new `codex/*` branch and open a new PR. Do not continue on an old PR by default.
- Always share the active PR link after each commit/update.
- After every commit, include the PR link in the status update to the user.
- After pushing a coding branch, immediately create the GitHub PR when tooling/auth is available. Then inspect Gemini feedback directly through the available GitHub tooling/API path, patch every valid finding, rerun the relevant tests/checks, and merge once the PR is clean. Only fall back to sharing a PR-creation URL when direct PR creation/review access is blocked.
- No magic numbers for thresholds/heuristics. Use named constants/config objects (e.g., `INSIGHT_THRESHOLDS`) so they’re readable, reviewable, and easy to tune later.
- No hardcoded tunables (thresholds, time windows, scoring cutoffs). Use named constants/config and keep them centralized.
- Build as future SaaS by default: every feature/function must be tenant-aware and work for any client shop/account, not only a single brand/store.
- Do not hardcode client-specific store names, domains, SKUs, or assumptions into core logic unless explicitly requested and isolated behind config/feature flags.
- Optimize for maintainability and readability: favor clear abstractions, predictable data flow, minimal surprise, and code that can be safely modified by future engineers.
- Keep changes review-friendly: avoid large monolithic code drops; split into focused modules/functions with clear responsibilities.
- Keep account evolution flexible: support future account/shop onboarding, account-specific rules, and schema changes through configuration and scoped extension points.
- Apply secure engineering defaults for external attacker resistance: validate/sanitize untrusted inputs, enforce authN/authZ and tenant boundaries, avoid exposing sensitive data, apply least-privilege access, and add abuse controls (rate limits, safe error handling, audit-friendly logs).

## Required pre-PR checks
- Multi-tenant completeness check: after any tenant/account refactor, verify there are no hardcoded store identifiers left in write/read/query/log paths.
- Schema reality check: before using any table, confirm it exists in `server/db/database.js`; if provider data may be absent, implement fallback behavior.
- Migration observability check: do not use silent catch blocks for data backfills; log warnings with operation context.

## Security Engineering Baseline (Mandatory)
- Treat every external input as untrusted: HTTP body/query/headers, webhooks, pixel events, LLM responses, file uploads, third-party API responses, and DB-loaded JSON.
- Enforce deny-by-default boundaries: allowlist protocols, hosts, paths, MIME types, and enum values. Reject unknowns with safe errors.
- Never rely on client-side checks for security decisions. Server must revalidate all critical data.

### Network and SSRF controls
- For any server-side URL fetch/navigation (`fetch`, SDK HTTP, Puppeteer), enforce:
- `https` by default; `http` should be an explicit, justified exception.
- explicit host allowlist (per tenant when needed)
- no private/local/loopback/link-local ranges unless explicitly enabled by secure config
- fixed origin checks after URL resolution to prevent host-escape via redirects or `//host` paths
- Keep redirects restricted (`redirect: manual` where possible) and cap timeout/retry budgets.
- Do not pass user-provided absolute URLs directly into browser automation or backend fetches.

### Browser automation controls
- Prefer sandboxed browser launch by default.
- Do not use `--no-sandbox`/`--disable-setuid-sandbox` unless explicitly enabled by audited env flag and documented risk acceptance.
- Run automation with least privilege and strict scope (short timeouts, limited pages, bounded concurrency).
- Capture only non-sensitive evidence; avoid storing full HTML/cookies/session tokens.

### AuthN/AuthZ and tenant isolation
- Every read/write query must be tenant-scoped (`store/account/client`) and must not return cross-tenant data.
- Never trust tenant identifiers from UI alone; verify against authenticated context where available.
- For privileged actions, require explicit authorization checks and auditable logs.

### Input validation and output safety
- Validate schema/types/ranges before processing.
- Normalize and truncate untrusted strings before persistence/logging/rendering.
- Avoid dynamic SQL string interpolation; use parameterized statements only.
- Sanitize user-facing rendered data to prevent injection/XSS.

### Secrets and sensitive data
- Never commit secrets, tokens, cookies, raw credentials, or webhook signatures.
- Redact secrets in logs/errors/debug payloads (`[REDACTED]` pattern).
- Store minimum required data only; avoid unnecessary PII retention.

### Data integrity and resilience
- Do not silently swallow migration/backfill failures.
- Log operation context on best-effort failure paths.
- Use idempotency keys or dedupe guards for repeatable ingest/webhook flows.
- Add bounded fallbacks, not unbounded retries.

### AI/LLM-specific safeguards
- Treat model output as untrusted.
- Validate structured output against schema before use.
- Do not let model output directly trigger privileged operations without rule-based checks.
- Strip secrets and tenant-sensitive data from prompts unless strictly required.

### Dependency and supply-chain hygiene
- Prefer maintained official packages and pin major versions deliberately.
- Review new dependencies for security implications before adoption.
- Keep runtime flags and env defaults secure-first.

### Security review checklist for each feature
- Threat model written in 3 lines: attacker input, target asset, abuse path.
- New external calls audited for SSRF/private-network access.
- Auth/tenant boundaries verified on all new queries/routes.
- Logs/errors verified for secret leakage.
- Failure modes tested (timeout, malformed payload, unavailable upstream).

### Forbidden patterns
- No default hardcoded secrets.
- No `eval`-style dynamic execution from untrusted data (e.g., `eval()`, `new Function()`, `setTimeout(<string>)`, `setInterval(<string>)).
- No broad CORS or permissive wildcard auth in production paths.
- No security-sensitive behavior hidden behind undocumented env toggles.
