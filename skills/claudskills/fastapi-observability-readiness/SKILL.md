---
name: fastapi-observability-readiness
description: Use when making a scaffolded FastAPI service production-observable after reliability SLO targets are approved or deferred. Replaces the telemetry seam with OpenTelemetry, prometheus-client RED metrics, trace-correlated structlog, and SLO/burn-rate alerts. Not for the shell, auth, tasks, or performance.
---

# FastAPI Observability Readiness

## When to use

Invoke when a scaffolded FastAPI service needs production observability: distributed tracing, RED (Rate/Errors/Duration) metrics, logs correlated to traces, and SLI/SLO definitions with burn-rate alerting before release or before an on-call rotation takes it.

Do not use for: the service shell, settings, logging client, or error tiers (use `fastapi-service-scaffold`), auth or OWASP review (use `fastapi-auth-and-security-review`), task or event integration (use `fastapi-async-and-task-integration`), or pool-sizing/circuit-breaker/load-test gating (use `fastapi-performance-and-resilience`).

## Inputs

Required:

- A service with the `fastapi-service-scaffold` baseline (no-op telemetry seam, structlog logger, request context present).
- Approved `architecture/reliability` SLO targets (latency/availability objectives, error budget) — or explicit confirmation they are intentionally deferred.

Optional:

- Approved `backend-architecture.md` for the service's critical user journeys (which endpoints define the SLI).
- Telemetry backend (OTLP collector endpoint, Prometheus scrape vs push, vendor) if `architecture/reliability` or operations is silent.
- Existing alerting/runbook location (operations) to link from the SLO definitions.

## Operating rules

- Never invent SLO targets. Latency/availability objectives and the error budget belong to `architecture/reliability`. If silent, pause and raise an ADR candidate rather than guessing a number.
- Replace the scaffold seam; do not duplicate it. OpenTelemetry, metrics, and the real tracer fill the `fastapi-service-scaffold` no-op telemetry interface and bind to the existing `contextvars` request context — they do not re-create the logger or error tiers.
- The three signals are correlated, not parallel: every log line within a request carries the active trace id and span id; every metric and trace shares the same request/resource attributes. Uncorrelated signals are three dashboards no one can join during an incident.
- Metrics follow the RED method for request-driven work: a request Rate counter, an Errors counter (by class), and a Duration histogram with explicit, documented buckets — never auto-ranged buckets that make latency SLIs unreadable.
- Instrument the boundary, not the internals: auto-instrument ASGI/HTTP/DB client libraries via OpenTelemetry; add manual spans only for business-meaningful operations. Cardinality is bounded — no unbounded label values (user id, raw path, request id) on metrics.
- SLIs are defined as queries, not prose: each SLI is a concrete metric expression; each SLO pairs it with the target from `architecture/reliability` and an error-budget window.
- Alerts are multi-burn-rate, not single-threshold: a fast-burn (page) and a slow-burn (ticket) rule per SLO, expressed against the error budget — not a static "p99 > X" that pages on every blip.
- Telemetry export is settings-driven and degrades safely: the OTLP endpoint and sampling come from the validated settings seam; a collector outage degrades to dropped spans, never a crashed or blocked request path.
- A change that does not pass `mypy`, `ruff`, tests, and the boot smoke check — with traces, metrics, and correlated logs observed locally — is not done. Fix and re-run.

## Output contract

The observability layer MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — three correlated signals; RED metrics with documented buckets; SLIs as queries; multi-burn-rate alerts tied to an error budget; bounded metric cardinality; export settings-driven and fail-safe.

Upstream contract: `architecture/reliability` is the source of truth for SLO targets and the error budget; `backend-architecture.md` is the source of truth for the critical journeys an SLI must cover. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/fastapi-observability-playbook.md` when implementing any owned area or defining SLOs.
- Read `references/fastapi-observability-quality-rubric.md` before declaring the work complete.
- Use `assets/fastapi-observability-readiness.template.md` as the OTel SDK, metrics, and SLO/alert reference.

## Process

1. Gather context: load `architecture/reliability` (SLO targets, error budget, windows) and `backend-architecture.md` (critical user journeys). Confirm the scaffold telemetry seam exists. If SLO targets are missing, raise an ADR candidate before proceeding — do not pick numbers.
2. Extend settings: add the OTLP endpoint, sampling ratio, metrics exposure mode (scrape/push), and service/resource attributes to the scaffold `Settings` model and `.env.example` (placeholders only).
3. Replace the tracer seam: initialize the OpenTelemetry Python SDK in `app/observability/tracing.py` with resource attributes, OTLP exporter, and the FastAPI/ASGI + DB/client auto-instrumentations. Wire it during ASGI-lifespan startup so the app is instrumented.
4. Add RED metrics: a prometheus-client registry in `app/observability/metrics.py` exposing a request-rate counter, an error counter by class, and a duration histogram with explicit documented buckets; a `/metrics` ASGI endpoint or push exporter per settings. Bound all label sets.
5. Correlate logs: extend the scaffold structlog config so every line within a request emits the active `trace_id` and `span_id` (read from the OTel context bound to the existing `contextvars` request context). Do not fork the logger.
6. Define SLIs and SLOs: in `docs/observability/slo.md` (or the operations-linked location), write each SLI as a concrete metric query and pair it with the target and error-budget window from `architecture/reliability`.
7. Define alerts: a fast-burn (page) and slow-burn (ticket) multi-burn-rate rule per SLO, expressed against the error budget, in the alerting format the operations/runbook location expects. Link each alert to its runbook.
8. Build verification (mandatory): run `mypy`, `ruff check`, tests, and the boot smoke check; then start the service locally and confirm a request produces a trace, increments the RED metrics, and logs lines carrying the matching `trace_id`. Fix and re-run on failure. Validate against the Output contract; document any unresolved gap in the service README.

## Outputs

Required:

- OpenTelemetry SDK initialized with resource attributes, OTLP export, and auto-instrumentation (filling the scaffold tracer seam).
- RED metrics (rate counter, error counter by class, duration histogram with documented buckets) exposed via `/metrics` or push; bounded cardinality.
- Logs correlated to traces (`trace_id`/`span_id` on every in-request line) via the existing structlog config and request context.
- `docs/observability/slo.md`: each SLI as a metric query, each SLO with target + error-budget window from `architecture/reliability`.
- Multi-burn-rate alert rules (fast-burn page + slow-burn ticket) per SLO, each linked to a runbook.

Output rules:

- The scaffold structlog config, request context, and error tiers are extended, not duplicated.
- No SLO number is invented — every target traces to `architecture/reliability` or an open ADR candidate.
- Metric label cardinality is bounded; no user id / raw path / request id as a metric label.
- Telemetry export is settings-driven; a collector outage never blocks or crashes the request path.

## Quality checks

- [ ] `mypy`, `ruff check`, tests, and the boot smoke check all pass (or a skip is documented with reason).
- [ ] The scaffold no-op telemetry seam is replaced; no telemetry TODO remains.
- [ ] A local request produces a trace, increments the RED metrics, and emits logs carrying the matching `trace_id` (verified).
- [ ] The duration histogram uses explicit, documented buckets (not auto-ranged).
- [ ] No metric carries an unbounded label (user id, raw path, request id).
- [ ] Every SLI in `slo.md` is a concrete metric query; every SLO cites a target and error-budget window from `architecture/reliability`.
- [ ] Each SLO has a fast-burn (page) and slow-burn (ticket) alert rule expressed against the error budget.
- [ ] Each alert links to a runbook location.
- [ ] OTLP endpoint and sampling resolve through the validated settings seam; a collector outage degrades to dropped spans, not a failed request (verified by pointing at a dead endpoint).
- [ ] The service README references `docs/observability/slo.md` and the alerting location.

## References

- Upstream: [`architecture/reliability`](../../../../architecture/reliability/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md).
- Baseline this extends: `fastapi-service-scaffold`. Related: `fastapi-auth-and-security-review`, `fastapi-async-and-task-integration`, `fastapi-performance-and-resilience`.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md).
