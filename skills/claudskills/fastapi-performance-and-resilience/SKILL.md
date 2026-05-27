---
name: fastapi-performance-and-resilience
description: Use when hardening a scaffolded FastAPI service for load and failure after performance budgets and SLO targets are approved or deferred. Adds async-path discipline, the worker model, pool sizing, caching, breakers/bulkheads, retry budgets, and a CI load-test gate. Not for the shell, auth, observability, or tasks.
---

# FastAPI Performance and Resilience

## When to use

Invoke when a scaffolded FastAPI service must hold an SLO under load: blocking calls are stalling the event loop, downstream failures cascade, the connection pool is mis-sized, there is no caching posture or backpressure under burst, retries amplify outages, or there is no load-test gate proving the service meets its latency/throughput budget before release.

Do not use for: the service shell, settings, or error tiers (use `fastapi-service-scaffold`), auth or OWASP review (use `fastapi-auth-and-security-review`), OpenTelemetry/metrics/SLO definition (use `fastapi-observability-readiness`), or broker/task/event integration (use `fastapi-async-and-task-integration`).

## Inputs

Required:

- A service with the `fastapi-service-scaffold` baseline (settings, logging, ASGI-lifespan shutdown, health probes present).
- Approved `architecture/performance` budgets and `architecture/reliability` SLO targets (latency/throughput objective, error budget) — or explicit confirmation they are intentionally deferred.

Optional:

- The observability layer from `fastapi-observability-readiness` (for event-loop and resilience metrics) if already present.
- Known blocking/CPU-bound operations and downstream dependencies with their own SLAs.
- Expected peak traffic shape (RPS, burst factor, payload sizes) for the load test.

## Operating rules

- Never invent the budget or SLO. Latency/throughput targets, the error budget, and acceptable degradation belong to `architecture/performance` and `architecture/reliability`. If silent on a number this skill needs, pause and raise an ADR candidate rather than guessing a threshold.
- Extend the scaffold; do not duplicate it. Pool sizes, breaker thresholds, and timeout settings read from the validated settings seam, log through the scaffold logger, and tie shutdown to the scaffold ASGI-lifespan. Resilience metrics reuse the observability seam — do not wire a second telemetry stack.
- The event loop is sacred: no synchronous blocking or CPU-bound work in an `async def` path. Blocking I/O uses an async driver or `run_in_threadpool`/`anyio.to_thread`; CPU work goes to a process pool. Event-loop lag is measured, not assumed.
- The worker model is explicit and matches the workload: Gunicorn + `UvicornWorker` with a worker count derived from cores per `architecture/performance` — not a single Uvicorn process pretending to use all cores, and not threads where processes are required.
- Every external call is bounded and isolated: an explicit timeout, a circuit breaker, and a bulkhead (bounded concurrent calls) so one slow dependency cannot consume the whole pool. No unbounded `await` on a network call.
- Connection pools are sized, not defaulted: DB and HTTP client pool sizes derive from the worker model and the downstream limits, documented against `architecture/performance`. An unbounded or default pool under load is an outage.
- Retries have a budget: capped attempts, exponential backoff with jitter, and a global retry-budget cap so retries cannot amplify a downstream outage into a self-inflicted DDoS. No retry on non-idempotent operations without an idempotency key.
- Caching posture is deliberate: what is cached, the TTL, the invalidation trigger, and the stampede protection are explicit — never an unbounded process-local dict.
- Backpressure is enforced, not hoped for: bounded concurrency with a shed-load path (429/503 with `Retry-After`) when saturated, and `/readyz` reflecting saturation — degrade deliberately rather than collapse.
- Resilience is verified, not asserted: a load-test gate runs the expected traffic shape and a dependency-failure scenario, and passes only if the measured result meets the `architecture/reliability` SLO. A service without a passing load-test gate is not done.
- A change that does not pass `mypy`, `ruff`, tests, the boot smoke check, and the load-test gate is not done. Fix and re-run.

## Output contract

The performance and resilience layer MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — event-loop lag, breaker state, pool saturation, shed count, and retry rate are observable via the scaffold/observability seam.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — the worker model and pool sizes are settings-driven and environment-agnostic; resource limits documented.

Upstream contract: `architecture/performance` is the source of truth for latency/throughput budgets and pool sizing; `architecture/reliability` is the source of truth for SLO targets, the error budget, and acceptable degradation. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/fastapi-performance-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/fastapi-performance-quality-rubric.md` before declaring the work complete.
- Use `assets/fastapi-performance-and-resilience.template.md` as the worker, breaker, caching, and load-test reference.

## Process

1. Gather context: load `architecture/performance` (latency/throughput budgets, pool sizing, payload limits) and `architecture/reliability` (SLO, error budget, acceptable degradation). Confirm the scaffold baseline. If a needed number is missing, raise an ADR candidate before proceeding — do not pick a threshold.
2. Extend settings: add the worker count, per-dependency timeouts, breaker thresholds, bulkhead concurrency limits, pool sizes, retry budget, cache TTLs, and backpressure limits to the scaffold `Settings` model and `.env.example` (placeholders only).
3. Enforce async-path discipline: identify synchronous blocking or CPU-bound operations in `async def` paths; move blocking I/O to async drivers or `run_in_threadpool`/`anyio.to_thread`, CPU work to a process pool. Add an event-loop-lag probe wired into `/readyz` and the metrics seam.
4. Apply the worker model: Gunicorn + `UvicornWorker` with a worker count from settings (per `architecture/performance`); graceful shutdown propagates to all workers via the scaffold ASGI-lifespan.
5. Bound and isolate downstream calls: wrap each external dependency in an explicit timeout, a circuit breaker (open/half-open/closed with documented thresholds), and a bulkhead (bounded concurrent calls). A tripped breaker returns a defined degraded response, not a hang.
6. Size connection pools and set caching posture: DB/HTTP client pool sizes derived from the worker model and downstream limits; a deliberate caching layer with explicit TTL, invalidation, and stampede protection. Document both against `architecture/performance`.
7. Budget retries: capped attempts with exponential backoff + jitter and a global retry-budget limiter; no retry on non-idempotent calls without an idempotency key. Document the worst-case amplification factor and confirm it stays within the dependency's headroom.
8. Enforce backpressure and build the load-test gate: bounded concurrency with a 429/503 + `Retry-After` shed path and `/readyz` reflecting saturation; a load-test script (k6/Locust) running the expected traffic shape plus a dependency-failure scenario, asserting measured p99/throughput against the `architecture/reliability` SLO and failing the build if missed. Wire it into CI as a gate.
9. Build verification (mandatory): run `mypy`, `ruff check`, tests, and the boot smoke check; then run the load-test gate and confirm it passes against the SLO and that breakers/backpressure behave under the failure scenario. Fix and re-run on failure. Validate against the Output contract; document any unresolved gap in the service README.

## Outputs

Required:

- Async-path discipline: blocking/CPU work off the event loop; an event-loop-lag probe in `/readyz` and the metrics seam.
- A settings-driven worker model (Gunicorn + UvicornWorker) with shutdown propagated to all workers.
- Per-dependency timeout + circuit breaker + bulkhead with a defined degraded response.
- Sized connection pools and a deliberate caching posture (TTL, invalidation, stampede protection).
- A retry budget (capped attempts, backoff+jitter, global cap; idempotency-gated) with a documented amplification factor.
- Enforced backpressure with a shed-load path and saturation reflected in `/readyz`.
- A CI load-test gate asserting measured performance against the `architecture/reliability` SLO.

Output rules:

- No invented threshold — every budget/SLO number traces to `architecture/performance`/`architecture/reliability` or an open ADR candidate.
- The scaffold settings, logging, lifespan, and observability seam are extended, not duplicated.
- No synchronous blocking call on an `async def` path; no unbounded `await` on a network call; no retry on a non-idempotent call without an idempotency key.
- The service sheds load deliberately under saturation rather than collapsing.

## Quality checks

- [ ] `mypy`, `ruff check`, tests, and the boot smoke check all pass (or a skip is documented with reason).
- [ ] Every budget/SLO number traces to `architecture/performance`/`architecture/reliability` (no invented threshold).
- [ ] No synchronous blocking or CPU-bound work runs on an `async def` path; blocking I/O is async or threadpooled, CPU work is in a process pool.
- [ ] An event-loop-lag probe feeds `/readyz` and the metrics seam.
- [ ] The worker model (Gunicorn + UvicornWorker, worker count) is settings-driven and shutdown propagates to all workers.
- [ ] Every external call has an explicit timeout, a circuit breaker, and a bulkhead; a tripped breaker returns a defined degraded response, not a hang.
- [ ] Connection pool sizes are derived and documented; no default/unbounded pool under load.
- [ ] Caching posture is explicit (TTL, invalidation trigger, stampede protection) — no unbounded process-local cache.
- [ ] Retries are capped with backoff+jitter and a global budget; non-idempotent calls are not retried without an idempotency key; the amplification factor is documented.
- [ ] Backpressure sheds load with 429/503 + `Retry-After` under saturation, and `/readyz` reflects saturation.
- [ ] The CI load-test gate runs the expected traffic shape plus a dependency-failure scenario and fails the build if the SLO is missed (verified passing).
- [ ] Event-loop lag, breaker state, pool saturation, shed count, and retry rate are observable via the scaffold/observability seam.
- [ ] The service README documents the worker model, pool sizes, caching posture, resilience thresholds, and the load-test gate.

## References

- Upstream: [`architecture/performance`](../../../../architecture/performance/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Baseline this extends: `fastapi-service-scaffold`. Related: `fastapi-auth-and-security-review`, `fastapi-observability-readiness`, `fastapi-async-and-task-integration`.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md).
