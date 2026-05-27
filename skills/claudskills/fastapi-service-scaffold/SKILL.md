---
name: fastapi-service-scaffold
description: Use when scaffolding or production-hardening a FastAPI service shell after backend architecture is approved or deferred. Produces the settings/logging/health/error-handling/lifespan/DI/container baseline the other FastAPI skills extend. Not for auth, observability, tasks, or performance.
---

# FastAPI Service Scaffold

## When to use

Invoke when starting a new FastAPI service, standardizing an existing service baseline, modernizing a service that lacks validated settings, structured logging, health probes, or layered error handling, or preparing a FastAPI service for container deployment.

Do not use for: auth, session, or OWASP review work (use `fastapi-auth-and-security-review`), observability vendor wiring — OpenTelemetry, prometheus-client, SLO/alerts (use `fastapi-observability-readiness`), Celery/RQ/arq or Kafka task and event integration (use `fastapi-async-and-task-integration`), or performance and resilience gating — pool sizing, circuit breakers, load-test gates (use `fastapi-performance-and-resilience`).

## Inputs

Required:

- Service name and the business capability it serves.
- Approved `backend-architecture.md`, or explicit confirmation that backend architecture is intentionally deferred.

Optional:

- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Data layer named by architecture (SQLAlchemy 2.x + Alembic default) — registered as a seam only, not implemented here.
- ASGI server choice if silent (Uvicorn standalone for dev; Gunicorn + `uvicorn.workers.UvicornWorker` for prod).
- Target Python version (3.11+ default), dependency manager (uv default), and monorepo vs single-service repo placement.

## Operating rules

- Never generate tutorial-grade scaffolding. Assume multiple environments, structured logging, container deployment, ASGI-lifespan shutdown, and operational ownership.
- Consume `backend-architecture.md`; do not invent decisions. Domain boundaries, data layer, and contracts belong to `backend-architecture.md`; auth provider and secret handling belong to `architecture/security`. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.
- Owns the DI and principal-provider baseline only — the shell, not the flow. Token verification, session, and protected-route logic belong to `fastapi-auth-and-security-review`. Scaffold the seam (a typed `Depends`); do not implement the flow.
- Secure by default: settings are validated at boot and fail fast; no secrets in source, committed config, the image, or `.env`; the container runs as a non-root user from a digest-pinned base image.
- Settings are validated, not read ad hoc: a single typed Pydantic `Settings` (`BaseSettings`) instance built at startup. Missing or malformed required variables abort boot with a clear message — never a runtime `None`.
- Error handling is layered in a specific order: `sys.excepthook` and the asyncio loop exception handler (log fatal, flush, exit non-zero for unhandled) → FastAPI/Starlette exception handlers (structured body, no traceback or internals in non-dev) → ASGI-lifespan graceful shutdown (stop accepting, drain in-flight, close registered resources within a bounded timeout) wired to uvicorn signal handling. All four are required.
- Observability is a seam, not an implementation: a structlog structured logger bound to a `contextvars` request context (request id correlated) is mandatory in the baseline; OpenTelemetry, metrics, and alerting are explicitly deferred to `fastapi-observability-readiness` behind a no-op tracer/metrics interface.
- Health probes are mandatory: a liveness endpoint (process is up) and a readiness endpoint (registered dependency checks pass) are separate and wired before any feature route.
- A scaffold that does not run is not done. Run typecheck, lint, the test run, and a boot smoke check before declaring completion; fix and re-run on failure.
- Confirm the target directory before writing files. Recommend `services/<service-name>/` in a monorepo or repo root for a single-service repo. Refuse to write into a plugin or skill repository without explicit user override.

## Output contract

The generated service shell MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — env-agnostic image; runtime config injected, not baked; one artifact per environment; non-root container.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logging with request-id correlation and an environment tag; tracer/metrics seam present.
- [security-standards](../../../../../standards/security-standards/README.md) — no secrets in source, committed config, or image; settings fail fast on missing required secrets.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — service, module, and file naming.

Upstream contract: `backend-architecture.md` is the source of truth for domain boundaries, data layer, and contracts; `architecture/security` is the source of truth for auth provider, session model, and secret handling. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/fastapi-scaffold-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/fastapi-scaffold-quality-rubric.md` before declaring the scaffold complete.
- Use `assets/fastapi-service-scaffold.template.md` as the directory-layout, settings, and lifespan reference.

## Process

1. Gather context: service name, business capability, **target directory**, target Python version, dependency manager, and the auth provider decision from `architecture/security`. Load `backend-architecture.md` and extract domain boundaries, data layer, and contracts. If a needed decision is missing, raise an ADR candidate before proceeding. Confirm the target directory is not a plugin or skill repository.
2. Generate the project layout: `pyproject.toml` (deps pinned exactly with a hashed lockfile — no unbounded specifiers, `requires-python` set), `mypy`/`ruff` config, `.gitignore`, and the package structure (domain layout per `backend-architecture.md`). Reference `assets/fastapi-service-scaffold.template.md` for the canonical layout.
3. Generate validated settings: a Pydantic `Settings(BaseSettings)` in `app/config.py` parsing the environment at import, instantiated once; abort with a clear message on any missing or malformed required variable. Create `.env.example` documenting every variable with placeholder values only.
4. Generate the structured logging and request-context seam: a structlog logger in `app/observability/logging.py`; a `contextvars` request context in `app/observability/context.py`; ASGI middleware that assigns or propagates a request id and binds a bound logger. Add a no-op tracer/metrics interface in `app/observability/telemetry.py` with explicit TODO comments naming `fastapi-observability-readiness` as the owner.
5. Generate the layered error handling: `sys.excepthook` and `loop.set_exception_handler` (log fatal, flush, exit non-zero) in `app/server/process_handlers.py`; FastAPI/Starlette exception handlers returning a structured body with no traceback or internals in non-dev; an ASGI-lifespan (`lifespan` context manager) that on shutdown stops accepting, drains in-flight, and closes registered resource hooks within a bounded timeout.
6. Generate health probes: a liveness endpoint (`/healthz`) returning 200 when the process is up, and a readiness endpoint (`/readyz`) iterating registered dependency-check callables and returning 503 until all pass. Wire both before any feature router.
7. Generate the DI and principal-provider baseline: FastAPI `Depends` providers in `app/container.py`. Register the principal/auth-context provider as a typed dependency shell. Add explicit TODO comments naming `fastapi-auth-and-security-review` as the owner of token verification, session, and protected-route logic, and the data-layer client (SQLAlchemy session) as a seam owned by the data implementation.
8. Generate container packaging: a multi-stage `Dockerfile` (build stage, slim runtime stage) running as a non-root user from a digest-pinned base image, a `.dockerignore`, and a documented `HEALTHCHECK` hitting `/healthz`. No secrets baked; runtime config arrives via environment.
9. Generate local-run documentation in the service README: how to run each environment, every required environment variable (mirrored from `.env.example`), the runtime-config contract, and the explicit table of seams downstream archetypes fill (auth, observability vendor, task/event, performance gates, data layer).
10. Build verification (mandatory): run `mypy`, `ruff check`, the test command (`pytest`), and a boot smoke check (start the app, assert `httpx` `GET /healthz` returns 200, shut down cleanly via lifespan). Fix and re-run on failure. Then validate against the standards in the Output contract; revise until all pass or explicitly document any unresolved gap in the README.

## Outputs

Required:

- Python/FastAPI service package with `pyproject.toml` (pinned deps + hashed lockfile, `requires-python`) and `mypy`/`ruff` config.
- Validated Pydantic `Settings` with fail-fast boot and `.env.example`.
- structlog logger + `contextvars` request context + request-id correlation; no-op tracer/metrics seam.
- Layered error handling: process/asyncio handlers, FastAPI/Starlette exception handlers, ASGI-lifespan graceful shutdown (all wired).
- Separate liveness (`/healthz`) and readiness (`/readyz`) probes.
- `Depends` DI providers with a typed principal-provider shell (auth flow explicitly deferred).
- Multi-stage non-root `Dockerfile` from a digest-pinned base, `.dockerignore`, documented `HEALTHCHECK`.
- Service README listing all seams downstream archetypes fill.

Output rules:

- Generated files are functional and the app boots, not placeholder-heavy.
- No secrets in source, committed config, `.env.example`, or the image.
- The principal provider is a seam, not a flow — token verification, session, and route guards are explicitly deferred to `fastapi-auth-and-security-review`.
- The same image runs in every environment; configuration arrives at runtime via environment variables.

## Quality checks

- [ ] `mypy` and `ruff check` report zero errors.
- [ ] The test command runs and the boot smoke check (`GET /healthz` → 200, clean lifespan shutdown) passes, or a skip is documented with reason.
- [ ] `pyproject.toml` pins every dependency with a hashed lockfile and sets `requires-python`.
- [ ] Settings are validated at boot and abort on a missing required variable — verified by removing one required var and observing a clear non-zero exit.
- [ ] No secrets appear in source, committed config, `.env.example`, or the built image.
- [ ] All four error layers are wired: `sys.excepthook`, asyncio loop handler, FastAPI/Starlette exception handlers, ASGI-lifespan graceful shutdown.
- [ ] Exception handlers return no traceback or internal details in non-dev environments.
- [ ] `/healthz` and `/readyz` are separate; `/readyz` returns 503 until registered dependency checks pass.
- [ ] The structlog logger binds a request id from the `contextvars` context; the tracer/metrics seam is a no-op with a TODO naming `fastapi-observability-readiness`.
- [ ] The `Depends` principal provider is a typed shell tied to an `architecture/security` decision; token/session logic is explicitly deferred with TODO comments.
- [ ] The `Dockerfile` is multi-stage, runs as non-root, uses a digest-pinned base, and bakes no secrets.
- [ ] The service README lists all seams downstream archetypes are expected to fill.

## References

- Upstream: [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Related FastAPI archetype skills (extend this baseline): `fastapi-auth-and-security-review`, `fastapi-observability-readiness`, `fastapi-async-and-task-integration`, `fastapi-performance-and-resilience`.
- Standards: [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
