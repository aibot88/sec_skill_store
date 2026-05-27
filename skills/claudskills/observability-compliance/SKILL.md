---
name: observability-compliance
description: Use when performing a deep observability audit or remediating missing structured logging, metrics, traces, or alerting rules
version: 1.0.0
owner: platform-governance
tier: full
source: .enterprise/governance/agent-skills/observability-compliance/SKILL.md
quick: .enterprise/governance/agent-skills/observability-compliance/SKILL-QUICK.md
portable: true
license: Apache-2.0
---

# Observability Compliance

## When to use
Use this skill when:
- reviewing a PR that adds new service operations, endpoints, or background jobs
- generating instrumentation code for new features
- auditing a service's observability coverage
- validating that log statements, metrics, and traces are correctly implemented

---

## 1. Structured Logging

- OC-01: ALL log statements MUST use **structured logging** (key/value pairs) — never concatenated strings.
- OC-02: Every backend log entry MUST include: `service`, `environment`, `correlationId`.
- OC-03: `traceId` and `spanId` MUST be included when distributed tracing context is available.
- OC-04: `eventName` or `operation` MUST be included to identify the log's business context.
- OC-05: Secrets, tokens, API keys, passwords, and PII MUST NEVER appear in log statements.
- OC-06: Payloads MUST be redacted by default — only safe, non-sensitive fields are logged.
- OC-07: Log levels MUST be used correctly:
  - `Debug` — high-volume, local diagnostics only; disabled in production by default
  - `Info` — business lifecycle milestones (order placed, payment confirmed)
  - `Warning` — recoverable anomalies (retry attempted, fallback activated)
  - `Error` — failed operations requiring attention
  - `Critical` — immediate action required (data corruption risk, auth outage)
- OC-08: Errors MUST be logged at `Error` or `Critical` — never swallowed silently.

---

## 2. Correlation & Trace Context

- OC-09: `correlationId` MUST be propagated from every inbound request/message to ALL outbound calls (HTTP, broker, background jobs).
- OC-10: `causationId` MUST be included on all domain and integration events (references the command or event that caused it).
- OC-11: HTTP services MUST accept an incoming correlation header (`X-Correlation-Id` or equivalent), generate one if missing, and return it in the response.
- OC-12: Message consumers MUST extract and propagate correlation context from the message envelope.
- OC-13: Background jobs MUST generate or inherit a correlation context at start.

---

## 3. Metrics

### 3.1 Required per HTTP endpoint
- OC-14: Request rate (requests/second, by endpoint and method)
- OC-15: Error rate (4xx and 5xx, by endpoint)
- OC-16: Latency distribution (p50, p95, p99, by endpoint)

### 3.2 Required per use case (Command/Query)
- OC-17: Commands executed (count, by command type)
- OC-18: Command failure rate (count, by command type and error category)
- OC-19: Queries executed (count, by query type)
- OC-20: Handler duration (p50/p95/p99, by handler)

### 3.3 Required per messaging operation
- OC-21: Events published (count, by event type)
- OC-22: Events consumed (count, by event type and consumer)
- OC-23: Consumer processing failures (count, by event type)
- OC-24: Outbox pending count
- OC-25: DLQ message count (by queue)
- OC-26: Consumer lag (time between event occurrence and processing)

### 3.4 Required per external dependency call
- OC-27: Dependency error rate (by dependency name)
- OC-28: Dependency latency (p95/p99, by dependency)
- OC-29: Circuit breaker state (CLOSED/OPEN/HALF-OPEN, by dependency)

---

## 4. Distributed Tracing

- OC-30: Spans MUST be created for:
  - inbound HTTP requests and gRPC calls
  - outbound HTTP and gRPC calls
  - database queries (at minimum for slow query threshold)
  - message broker publish and consume operations
  - significant background job phases
- OC-31: Span attributes MUST include:
  - use case or operation name
  - aggregate id (when safe — not PII)
  - event type (for broker operations)
  - outcome (success/failure)
- OC-32: Span names MUST be descriptive: `order.place`, `payment.charge`, `outbox.publish` — not generic `HTTP POST`.
- OC-33: Trace context MUST be propagated via W3C `traceparent` header or OpenTelemetry conventions.

---

## 5. Alerting Baseline

New services MUST configure baseline alerts:

- OC-34: p95 latency exceeds SLA threshold for > 5 minutes
- OC-35: Error rate exceeds threshold (default 1%) for > 2 minutes
- OC-36: DLQ count above threshold (default > 0) for > 5 minutes
- OC-37: Outbox backlog above threshold for > 5 minutes
- OC-38: Circuit breaker OPEN for > 60 seconds
- OC-39: Authentication error spike (> 10x normal rate)

---

## 6. Client Observability (Flutter / React Native)

- OC-40: Crashes MUST be captured and reported to crash reporting service.
- OC-41: Network failures MUST be captured (timeout, connection error, 5xx responses).
- OC-42: Slow screens/frames MUST be captured (render time > 500ms).
- OC-43: `correlationId` MUST be propagated in all outbound API calls when provided by backend.
- OC-44: User-sensitive data MUST NOT be captured in crash reports or performance traces.

---

## Examples

✅ Good:
```csharp
_logger.LogInformation(
    "Order placed successfully. OrderId={OrderId} CustomerId={CustomerId} CorrelationId={CorrelationId}",
    order.Id, order.CustomerId, correlationId);
```

❌ Bad:
```csharp
_logger.LogInformation($"Order placed: {order.Id} for user {user.Email} token={accessToken}");
// String concat + PII (email) + secret (token)
```

✅ Good: New endpoint registers counter, histogram, and propagates correlationId.
❌ Bad: New background job runs silently with no metrics and no correlation context.


## Quick Mode

For low-context activation, load `.enterprise/governance/agent-skills/observability-compliance/SKILL-QUICK.md` or `QUICK.md` first. Load this full skill for deep analysis, violation fixing, or formal review gates.

