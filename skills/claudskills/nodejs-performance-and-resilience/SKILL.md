---
name: nodejs-performance-and-resilience
description: Use when hardening a scaffolded Node.js service for load and failure — enforcing event-loop discipline, clustering or worker threads for CPU work, backpressure and bounded concurrency, circuit breakers and bulkheads on downstream calls, timeout and retry budgets, and a load-test gate measured against the reliability SLO — after the service scaffold exists and performance budgets and SLO targets are approved or intentionally deferred. Do not use for the service shell or config, auth or security review, observability vendor wiring, or queue and event integration; use the other Node.js archetype skills instead.
---

# Node.js Performance and Resilience

## When to use

Invoke when a scaffolded Node.js service must hold an SLO under load: blocking work is starving the event loop, downstream failures cascade, there is no backpressure under burst, retries amplify outages, or there is no load-test gate proving the service meets its latency/throughput budget before release.

Do not use for: the service shell, config, or error tiers (use `nodejs-service-scaffold`), auth or OWASP review (use `nodejs-auth-and-security-review`), OpenTelemetry/metrics/SLO definition (use `nodejs-observability-readiness`), or broker/queue/event integration (use `nodejs-queue-and-event-integration`).

## Inputs

Required:

- A service with the `nodejs-service-scaffold` baseline (config, logging, graceful shutdown, health probes present).
- Approved `architecture/performance` budgets and `architecture/reliability` SLO targets (latency/throughput objective, error budget) — or explicit confirmation they are intentionally deferred.

Optional:

- The observability layer from `nodejs-observability-readiness` (for event-loop and resilience metrics) if already present.
- Known CPU-bound operations and downstream dependencies with their own SLAs.
- Expected peak traffic shape (RPS, burst factor, payload sizes) for the load test.

## Operating rules

- Never invent the budget or SLO. Latency/throughput targets, the error budget, and acceptable degradation belong to `architecture/performance` and `architecture/reliability`. If silent on a number this skill needs, pause and raise an ADR candidate rather than guessing a threshold.
- Extend the scaffold; do not duplicate it. Concurrency limits, breakers, and timeout config read from the validated config seam, log through the scaffold logger, and tie shutdown to the scaffold hook. Resilience metrics reuse the observability seam — do not wire a second telemetry stack.
- The event loop is sacred: no synchronous CPU-bound or blocking work on the main loop. CPU work goes to worker threads or a separate process; blocking I/O is replaced with async. Event-loop lag is measured, not assumed.
- Scale model is explicit and matches the workload: clustering (process-per-core) or worker threads per `architecture/performance` — not both by accident, and not a single process pretending to use all cores.
- Every external call is bounded and isolated: an explicit timeout, a circuit breaker, and a bulkhead (bounded concurrent calls) so one slow dependency cannot consume the whole pool. No unbounded `await` on a network call.
- Retries have a budget: capped attempts, exponential backoff with jitter, and a global retry-budget cap so retries cannot amplify a downstream outage into a self-inflicted DDoS. No retry on non-idempotent operations without an idempotency key.
- Backpressure is enforced, not hoped for: bounded queues/concurrency with a shed-load path (429/503 with `Retry-After`) when saturated — degrade deliberately rather than collapse.
- Resilience is verified, not asserted: a load-test gate runs the expected traffic shape and a dependency-failure scenario, and passes only if the measured result meets the `architecture/reliability` SLO. A service without a passing load-test gate is not done.
- A change that does not pass typecheck, lint, tests, the boot smoke check, and the load-test gate is not done. Fix and re-run.

## Output contract

The performance and resilience layer MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — event-loop lag, breaker state, pool saturation, shed count, and retry rate are observable via the scaffold/observability seam.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — the scale model (cluster/worker count) is config-driven and environment-agnostic; resource limits documented.

Upstream contract: `architecture/performance` is the source of truth for latency/throughput budgets; `architecture/reliability` is the source of truth for SLO targets, the error budget, and acceptable degradation. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/nodejs-performance-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/nodejs-performance-quality-rubric.md` before declaring the work complete.
- Use `assets/nodejs-performance-and-resilience.template.md` as the clustering, breaker, backpressure, and load-test reference.

## Process

1. Gather context: load `architecture/performance` (latency/throughput budgets, payload limits) and `architecture/reliability` (SLO, error budget, acceptable degradation). Confirm the scaffold baseline. If a needed number is missing, raise an ADR candidate before proceeding — do not pick a threshold.
2. Extend config: add the scale model and worker/cluster count, per-dependency timeouts, breaker thresholds, bulkhead concurrency limits, retry budget, and backpressure limits to the scaffold zod config schema and `.env.example` (placeholders only).
3. Enforce event-loop discipline: identify CPU-bound or blocking operations; move them to worker threads (`node:worker_threads`) or a separate process; replace blocking I/O with async. Add an event-loop-lag probe wired into `/readyz` and the metrics seam.
4. Apply the scale model: clustering (primary forks workers per core, shares the listen socket) or a worker-thread pool, per `architecture/performance`. The worker count is config-driven; graceful shutdown propagates to all workers via the scaffold hook.
5. Bound and isolate downstream calls: wrap each external dependency in an explicit timeout, a circuit breaker (open/half-open/closed with documented thresholds), and a bulkhead (bounded concurrent calls). A tripped breaker returns a defined degraded response, not a hang.
6. Budget retries: capped attempts with exponential backoff + jitter and a global retry-budget limiter; no retry on non-idempotent calls without an idempotency key. Document the worst-case amplification factor and confirm it stays within the dependency's headroom.
7. Enforce backpressure: bounded request concurrency / queue depth with a deliberate shed-load path (429/503 + `Retry-After`) when saturated; ensure `/readyz` reflects saturation so the load balancer diverts traffic.
8. Build the load-test gate: a script (k6/autocannon/Artillery) running the expected traffic shape plus a dependency-failure scenario; it asserts the measured p99/throughput against the `architecture/reliability` SLO and fails the build if the SLO is missed. Wire it into CI as a gate.
9. Build verification (mandatory): run `tsc --noEmit`, lint, tests, and the boot smoke check; then run the load-test gate and confirm it passes against the SLO and that breakers/backpressure behave under the failure scenario. Fix and re-run on failure. Validate against the Output contract; document any unresolved gap in the service README.

## Outputs

Required:

- Event-loop discipline: CPU/blocking work off the main loop; an event-loop-lag probe in `/readyz` and the metrics seam.
- A config-driven scale model (clustering or worker threads) with shutdown propagated to all workers.
- Per-dependency timeout + circuit breaker + bulkhead with a defined degraded response.
- A retry budget (capped attempts, backoff+jitter, global cap; idempotency-gated) with a documented amplification factor.
- Enforced backpressure with a deliberate shed-load path and saturation reflected in `/readyz`.
- A CI load-test gate asserting measured performance against the `architecture/reliability` SLO.

Output rules:

- No invented threshold — every budget/SLO number traces to `architecture/performance`/`architecture/reliability` or an open ADR candidate.
- The scaffold config, logging, shutdown, and observability seam are extended, not duplicated.
- No unbounded `await` on a network call; no retry on a non-idempotent call without an idempotency key.
- The service sheds load deliberately under saturation rather than collapsing.

## Quality checks

- [ ] `tsc --noEmit`, lint, tests, and the boot smoke check all pass (or a skip is documented with reason).
- [ ] Every budget/SLO number traces to `architecture/performance`/`architecture/reliability` (no invented threshold).
- [ ] No synchronous CPU-bound or blocking work runs on the main event loop; CPU work is on worker threads or a separate process.
- [ ] An event-loop-lag probe feeds `/readyz` and the metrics seam.
- [ ] The scale model (cluster/worker count) is config-driven and shutdown propagates to all workers.
- [ ] Every external call has an explicit timeout, a circuit breaker, and a bulkhead; a tripped breaker returns a defined degraded response, not a hang.
- [ ] Retries are capped with backoff+jitter and a global budget; non-idempotent calls are not retried without an idempotency key; the amplification factor is documented.
- [ ] Backpressure sheds load with 429/503 + `Retry-After` under saturation, and `/readyz` reflects saturation.
- [ ] The CI load-test gate runs the expected traffic shape plus a dependency-failure scenario and fails the build if the SLO is missed (verified passing).
- [ ] Event-loop lag, breaker state, pool saturation, shed count, and retry rate are observable via the scaffold/observability seam.
- [ ] The service README documents the scale model, resilience thresholds, and the load-test gate.

## References

- Upstream: [`architecture/performance`](../../../../architecture/performance/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Baseline this extends: `nodejs-service-scaffold`. Related: `nodejs-auth-and-security-review`, `nodejs-observability-readiness`, `nodejs-queue-and-event-integration`.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md).
