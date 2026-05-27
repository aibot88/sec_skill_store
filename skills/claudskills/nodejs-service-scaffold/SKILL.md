---
name: nodejs-service-scaffold
description: Use when creating, modernizing, or production-hardening a Node.js backend service after backend architecture is approved or intentionally deferred. Produces a framework-aware (Express, Fastify, or NestJS) TypeScript service shell with fail-fast validated configuration, a structured pino logging seam, liveness and readiness probes, layered error handling (uncaughtException, unhandledRejection, framework error handler, graceful shutdown), an AsyncLocalStorage request context, a DI container shell downstream archetypes extend, and a non-root multi-stage container image without baked secrets. Do not use for auth flow implementation, observability vendor wiring, queue or event integration, or performance and resilience gating; use the other Node.js archetype skills instead.
---

# Node.js Service Scaffold

## When to use

Invoke when starting a new Node.js backend service, standardizing an existing service baseline, modernizing a service that lacks validated config, structured logging, health probes, or layered error handling, or preparing a Node.js service for container deployment.

Do not use for: auth, session, or OWASP review work (use `nodejs-auth-and-security-review`), observability vendor wiring — OpenTelemetry, prom-client, SLO/alerts (use `nodejs-observability-readiness`), queue, broker, or event integration (use `nodejs-queue-and-event-integration`), or performance and resilience gating — backpressure, circuit breakers, load-test gates (use `nodejs-performance-and-resilience`).

## Inputs

Required:

- Service name and the business capability it serves.
- Approved `backend-architecture.md`, or explicit confirmation that backend architecture is intentionally deferred.

Optional:

- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Framework choice if `backend-architecture.md` is silent (Fastify default for new services; Express for ecosystem-constrained services; NestJS if a module/DI framework is mandated).
- DI container preference if silent (the framework's built-in for NestJS; `awilix` default otherwise).
- Data layer named by architecture (Prisma / Drizzle / TypeORM) — registered as a seam only, not implemented here.
- Target Node.js LTS (20+ default), package manager, and monorepo vs single-service repo placement.

## Operating rules

- Never generate tutorial-grade scaffolding. Assume multiple environments, structured logging, container deployment, graceful shutdown, and operational ownership.
- Consume `backend-architecture.md`; do not invent decisions. Framework, domain boundaries, data layer, and contracts belong to `backend-architecture.md`; auth provider and secret handling belong to `architecture/security`. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.
- Owns the DI and principal-provider baseline only — the shell, not the flow. Token verification, session, and protected-route logic belong to `nodejs-auth-and-security-review`. Scaffold the seam; do not implement the flow.
- Secure by default: configuration is validated at boot and fails fast; no secrets in source, committed config, the image, or `.env`; the container runs as a non-root user from a digest-pinned base image.
- Configuration is validated, not read ad hoc: a single typed, frozen config object built from a schema (zod or equivalent) at startup. Missing or malformed required variables abort boot with a clear message — never a runtime `undefined`.
- Error handling is layered in a specific order: `process.on('uncaughtException')` and `process.on('unhandledRejection')` (log fatal, flush, exit non-zero) → the framework error handler (Express error middleware / Fastify `setErrorHandler` / Nest exception filter; structured body, no stack or internals in non-dev) → graceful shutdown on `SIGTERM`/`SIGINT` (stop accepting, drain in-flight, close server and registered resources within a bounded timeout, then exit). All four are required.
- Observability is a seam, not an implementation: a structured pino logger bound to an AsyncLocalStorage request context (request id correlated) is mandatory in the baseline; OpenTelemetry, metrics, and alerting are explicitly deferred to `nodejs-observability-readiness` behind a no-op tracer/metrics interface.
- Health probes are mandatory: a liveness endpoint (process is up) and a readiness endpoint (registered dependency checks pass) are separate and wired before any feature route.
- A scaffold that does not build is not done. Run typecheck, lint, the test run, and a boot smoke check before declaring completion; fix and re-run on failure.
- Confirm the target directory before writing files. Recommend `services/<service-name>/` in a monorepo or repo root for a single-service repo. Refuse to write into a plugin or skill repository without explicit user override.

## Output contract

The generated service shell MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — env-agnostic image; runtime config injected, not baked; one artifact per environment; non-root container.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logging with request-id correlation and an environment tag; tracer/metrics seam present.
- [security-standards](../../../../../standards/security-standards/README.md) — no secrets in source, committed config, or image; config fails fast on missing required secrets.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — service, module, and file naming.

Upstream contract: `backend-architecture.md` is the source of truth for framework, domain boundaries, data layer, and contracts; `architecture/security` is the source of truth for auth provider, session model, and secret handling. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/nodejs-scaffold-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/nodejs-scaffold-quality-rubric.md` before declaring the scaffold complete.
- Use `assets/nodejs-service-scaffold.template.md` as the directory-layout, config, and entry-point reference.

## Process

1. Gather context: service name, business capability, **target directory**, target Node LTS, package manager, and the auth provider decision from `architecture/security`. Load `backend-architecture.md` and extract framework, domain boundaries, data layer, and contracts. If a needed decision is missing, raise an ADR candidate before proceeding. Confirm the target directory is not a plugin or skill repository.
2. Generate the project layout: `package.json` (deps pinned exactly — no `^` or `~`, `engines.node` set), `tsconfig.json` (`strict: true`), `eslint`/lint config, `.gitignore`, and the directory structure (feature/domain layout per `backend-architecture.md`). Reference `assets/nodejs-service-scaffold.template.md` for the canonical layout.
3. Generate validated configuration: a schema (zod or equivalent) in `src/config/index.ts` parsing `process.env` at boot, producing a single frozen typed config object; abort with a clear message on any missing or malformed required variable. Create `.env.example` documenting every variable with placeholder values only.
4. Generate the structured logging and request-context seam: a pino logger in `src/observability/logger.ts`; an AsyncLocalStorage request context in `src/observability/context.ts`; framework middleware/hook that assigns or propagates a request id and binds a child logger. Add a no-op tracer/metrics interface in `src/observability/telemetry.ts` with explicit TODO comments naming `nodejs-observability-readiness` as the owner.
5. Generate the layered error handling: process-level `uncaughtException` and `unhandledRejection` handlers (log fatal, flush logs, exit non-zero) in `src/server/process-handlers.ts`; the framework error handler (Express error middleware / Fastify `setErrorHandler` / Nest exception filter) returning a structured body with no stack or internals in non-dev; graceful shutdown on `SIGTERM`/`SIGINT` in `src/server/shutdown.ts` that stops accepting connections, drains in-flight requests, closes the server and registered resource hooks within a bounded timeout, then exits.
6. Generate health probes: a liveness endpoint (`/healthz`) returning 200 when the process is up, and a readiness endpoint (`/readyz`) iterating registered dependency-check hooks and returning 503 until all pass. Wire both before any feature route.
7. Generate the DI and principal-provider baseline: the container from `backend-architecture.md` (Nest built-in, or `awilix`/`tsyringe`) in `src/container/index.ts`. Register the principal/auth-context provider as a typed shell. Add explicit TODO comments naming `nodejs-auth-and-security-review` as the owner of token verification, session, and protected-route logic, and the data-layer client as a seam owned by the data implementation.
8. Generate container packaging: a multi-stage `Dockerfile` (build stage, slim runtime stage) running as a non-root user from a digest-pinned base image, a `.dockerignore`, and a documented `HEALTHCHECK` hitting `/healthz`. No secrets baked; runtime config arrives via environment.
9. Generate local-run documentation in the service README: how to run each environment, every required environment variable (mirrored from `.env.example`), the runtime-config contract, and the explicit table of seams downstream archetypes fill (auth, observability vendor, queue/event, performance gates, data layer).
10. Build verification (mandatory): run `tsc --noEmit`, the lint command, the test command (`vitest`/`jest`), and a boot smoke check (start the server, assert `GET /healthz` returns 200, shut down cleanly). Fix and re-run on failure. Then validate against the standards in the Output contract; revise until all pass or explicitly document any unresolved gap in the README.

## Outputs

Required:

- TypeScript service source tree with `package.json` (pinned deps, `engines.node`), `tsconfig.json` (`strict`), and lint config.
- Validated, frozen typed configuration with fail-fast boot and `.env.example`.
- Structured pino logger + AsyncLocalStorage request context + request-id correlation; no-op tracer/metrics seam.
- Layered error handling: process handlers, framework error handler, graceful shutdown (all wired).
- Separate liveness (`/healthz`) and readiness (`/readyz`) probes.
- DI container with a typed principal-provider shell (auth flow explicitly deferred).
- Multi-stage non-root `Dockerfile` from a digest-pinned base, `.dockerignore`, documented `HEALTHCHECK`.
- Service README listing all seams downstream archetypes fill.

Output rules:

- Generated files are functional and the service boots, not placeholder-heavy.
- No secrets in source, committed config, `.env.example`, or the image.
- The principal provider is a seam, not a flow — token verification, session, and route guards are explicitly deferred to `nodejs-auth-and-security-review`.
- The same image runs in every environment; configuration arrives at runtime via environment variables.

## Quality checks

- [ ] `tsc --noEmit` reports zero errors and the lint command passes.
- [ ] The test command runs and the boot smoke check (`GET /healthz` → 200, clean shutdown) passes, or a skip is documented with reason.
- [ ] `package.json` pins every dependency (no `^`/`~`) and sets `engines.node`.
- [ ] Configuration is schema-validated at boot and aborts on a missing required variable — verified by removing one required var and observing a clear non-zero exit.
- [ ] No secrets appear in source, committed config, `.env.example`, or the built image.
- [ ] All four error layers are wired: `uncaughtException`, `unhandledRejection`, framework error handler, graceful shutdown on `SIGTERM`/`SIGINT`.
- [ ] The framework error handler returns no stack trace or internal details in non-dev environments.
- [ ] `/healthz` and `/readyz` are separate; `/readyz` returns 503 until registered dependency checks pass.
- [ ] The pino logger binds a request id from AsyncLocalStorage; the tracer/metrics seam is a no-op with a TODO naming `nodejs-observability-readiness`.
- [ ] The DI principal provider is a typed shell tied to an `architecture/security` decision; token/session logic is explicitly deferred with TODO comments.
- [ ] The `Dockerfile` is multi-stage, runs as non-root, uses a digest-pinned base, and bakes no secrets.
- [ ] The service README lists all seams downstream archetypes are expected to fill.

## References

- Upstream: [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Related Node.js archetype skills (extend this baseline): `nodejs-auth-and-security-review`, `nodejs-observability-readiness`, `nodejs-queue-and-event-integration`, `nodejs-performance-and-resilience`.
- Standards: [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
