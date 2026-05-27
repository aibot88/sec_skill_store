---
name: nodejs-queue-and-event-integration
description: Use when adding asynchronous work or event integration to a scaffolded Node.js service — wiring BullMQ, KafkaJS, or SQS producers and consumers with explicit delivery semantics, a transactional outbox, idempotent consumers, retry with backoff, and dead-letter handling, plus integration tests against a real broker via Testcontainers — after the service scaffold exists and the broker and contracts are declared in backend-architecture. Do not use for the service shell or config, auth or security review, observability vendor wiring, or performance and resilience gating; use the other Node.js archetype skills instead.
---

# Node.js Queue and Event Integration

## When to use

Invoke when a scaffolded Node.js service must enqueue background work, publish domain events, or consume from a broker (BullMQ/Redis, Kafka, or SQS), and the integration needs correct delivery semantics, idempotency, retry/DLQ, and an outbox so a database commit and an event publish cannot diverge.

Do not use for: the service shell, config, or error tiers (use `nodejs-service-scaffold`), auth or OWASP review (use `nodejs-auth-and-security-review`), OpenTelemetry/metrics/SLO wiring (use `nodejs-observability-readiness`), or backpressure/circuit-breaker/load-test gating (use `nodejs-performance-and-resilience`).

## Inputs

Required:

- A service with the `nodejs-service-scaffold` baseline (DI container, validated config, logging, graceful shutdown present).
- `backend-architecture.md` declaring the broker, the event/message contracts, and the delivery-semantics and retry strategy — or explicit confirmation a needed decision is intentionally deferred.

Optional:

- Approved `architecture/reliability` for redelivery/DLQ expectations and the consumer SLO.
- The transactional data store (for the outbox table) if `backend-architecture.md` is silent.
- Ordering and partitioning requirements (Kafka key, FIFO group) per contract.

## Operating rules

- Never invent the broker, contract, or delivery semantics. Broker choice, message/event schemas, ordering, and at-least-once vs effectively-once belong to `backend-architecture.md`. If silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.
- Extend the scaffold; do not duplicate it. Producers/consumers register in the scaffold DI container, read connection config from the validated config seam, log through the scaffold logger, and close via the scaffold graceful-shutdown hook. Do not re-create any of these.
- Delivery is at-least-once unless the broker and contract guarantee otherwise: therefore every consumer is idempotent. Idempotency is explicit — a dedupe key (message id or business key) checked against a store, not "the handler is probably safe to re-run".
- A database write that must produce an event uses the transactional outbox: the domain change and the outbox row commit in one transaction; a relay publishes from the outbox. Never publish inside the request path before the transaction commits (dual-write hazard).
- Failure handling is explicit and bounded: a retry policy with backoff and a max attempt count, then a dead-letter destination. A message is never retried forever and never silently dropped.
- Consumers respect shutdown: on `SIGTERM` the consumer stops fetching, finishes in-flight messages within the scaffold shutdown timeout, and does not ack work it did not complete. Poison messages go to the DLQ, not an infinite redelivery loop.
- Producers do not block the request path on broker latency beyond a bounded timeout; a broker outage degrades to the outbox (for transactional events) or a clear, handled error — never an unbounded hang.
- An integration without a real-broker test is not done. Provide Testcontainers-backed tests proving: successful round trip, duplicate delivery handled idempotently, retry then DLQ on poison, and clean shutdown mid-consume.
- A change that does not pass typecheck, lint, the integration tests, and the boot smoke check is not done. Fix and re-run.

## Output contract

The queue/event integration MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — message/event payloads match the declared contract and are schema-validated on produce and consume; versioned, explicit envelope.
- [observability-standards](../../../../../standards/observability-standards/README.md) — produce/consume go through the scaffold logger with correlation; retry, DLQ, and lag are observable.

Upstream contract: `backend-architecture.md` is the source of truth for broker, contracts, ordering, and delivery semantics; `architecture/reliability` is the source of truth for redelivery/DLQ expectations and the consumer SLO. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/nodejs-queue-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/nodejs-queue-quality-rubric.md` before declaring the work complete.
- Use `assets/nodejs-queue-and-event-integration.template.md` as the producer, consumer, outbox, and test reference.

## Process

1. Gather context: load `backend-architecture.md` (broker, contracts, ordering, delivery semantics) and `architecture/reliability` (redelivery/DLQ, consumer SLO). Confirm the scaffold baseline and the transactional store. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Extend config: add broker connection settings, queue/topic names, consumer concurrency, retry attempts/backoff, and DLQ target to the scaffold zod config schema and `.env.example` (placeholders only).
3. Define the message envelope and schemas: a versioned envelope (`id`, `type`, `occurredAt`, `schemaVersion`, `payload`) with a zod schema per message type, validated on both produce and consume; reject unknown types.
4. Implement the producer: a typed publish API registered in the scaffold DI container, with a bounded send timeout. For events tied to a database write, write to an outbox table in the same transaction instead of publishing inline.
5. Implement the transactional outbox relay: a poller (or CDC hook) that reads unsent outbox rows, publishes them, marks them sent, and is itself idempotent and at-least-once safe.
6. Implement the consumer: registered in the DI container, idempotent via an explicit dedupe-key store, with a bounded retry+backoff policy and a max-attempt threshold that routes to the DLQ. Honor the scaffold graceful-shutdown hook (stop fetching, drain in-flight, no ack of incomplete work).
7. Make it observable: produce, consume, retry, DLQ, and consumer lag emit through the scaffold logger with correlation; expose the metrics seam hooks for `nodejs-observability-readiness` to instrument (do not wire the vendor here).
8. Write integration tests with Testcontainers: a real broker container; assert successful round trip, idempotent handling of a duplicate, retry-then-DLQ on a poison message, and clean shutdown mid-consume without losing or double-acking work.
9. Build verification (mandatory): run `tsc --noEmit`, lint, the integration test command, and the boot smoke check. Fix and re-run on failure. Validate against the Output contract standards; document any unresolved gap in the service README.

## Outputs

Required:

- Typed producer registered in the scaffold DI container with a bounded send timeout.
- Transactional outbox table + relay for events tied to a database write (no inline dual write).
- Idempotent consumer with an explicit dedupe-key store, bounded retry+backoff, and a DLQ route.
- Versioned message envelope with per-type zod schemas validated on produce and consume.
- Shutdown-aware consumer wired to the scaffold graceful-shutdown hook.
- Testcontainers integration tests: round trip, duplicate, retry→DLQ, shutdown mid-consume.

Output rules:

- The scaffold DI, config, logging, and shutdown are extended, not duplicated.
- No event is published inside the request path before its transaction commits (outbox required for transactional events).
- Every consumer is idempotent with an explicit dedupe mechanism — not assumed-safe.
- No message is retried unbounded or silently dropped; poison goes to the DLQ.

## Quality checks

- [ ] `tsc --noEmit`, lint, the integration tests, and the boot smoke check all pass (or a skip is documented with reason).
- [ ] Broker, contract, ordering, and delivery semantics trace to `backend-architecture.md` (no invented choice).
- [ ] The producer, consumer, and relay are registered in the scaffold DI container and use the scaffold config/logger/shutdown.
- [ ] Events tied to a DB write go through the transactional outbox; no inline publish-before-commit exists.
- [ ] The consumer is idempotent via an explicit dedupe-key store — a duplicate delivery is test-verified to have no double effect.
- [ ] Retry uses bounded backoff with a max-attempt count; exceeding it routes to the DLQ (test-verified).
- [ ] On `SIGTERM` the consumer stops fetching, drains in-flight within the scaffold timeout, and does not ack incomplete work (test-verified).
- [ ] Every message is envelope- and schema-validated on produce and consume; unknown types are rejected.
- [ ] Producer send is bounded by a timeout; a broker outage does not hang the request path.
- [ ] Produce/consume/retry/DLQ/lag are logged with correlation; metrics seam hooks are exposed for the observability skill.
- [ ] The service README documents the broker, contracts, retry/DLQ policy, and the outbox relay.

## References

- Upstream: [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Baseline this extends: `nodejs-service-scaffold`. Related: `nodejs-auth-and-security-review`, `nodejs-observability-readiness`, `nodejs-performance-and-resilience`.
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md).
