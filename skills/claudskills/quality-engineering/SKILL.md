---
name: quality-engineering
description: Use when an approved system design exists and a system or service needs a production-grade testing strategy before merge approval, release, or production promotion. Produces a risk-based testing strategy with acceptance criteria from PRD success metrics, a contract and integration test plan that avoids mocking the system under test, CI/CD quality gates, and implementation handoff notes. Do not use for isolated unit-test authoring, one-off test debugging, framework-specific test syntax, load-test implementation, or penetration testing.
---

# Quality Engineering

## When to use

Invoke after `system-design` (and any relevant backend/frontend/data architecture and published contracts) is approved, and before the first production-bound feature merges or a service is promoted through CI. Use this skill to decide what must be tested, at which layer, with which production-like dependencies, and which gates block merge and release. The trigger is an approaching merge/release/promotion decision for a system whose architecture and contracts already exist.

Do not use for authoring isolated unit tests, debugging an individual failing test, framework-specific test syntax or runner configuration, load-test implementation, penetration testing, or exploratory QA execution. Those belong to downstream `implementations/*` test work.

## Inputs

Required:

- Approved `system-design.md` and the architecture documents it spawned (backend/frontend/data, as present).
- Approved PRD with success metrics.
- Published service contract: `openapi.yaml`, event/webhook contracts, or equivalent.
- Persistence schema or migration plan, when the system has a data layer.

Optional:

- Existing test structure, CI constraints, runtime budgets, and known flaky areas.
- SLOs, latency/throughput targets, and operational risk surfaces.
- Security and compliance requirements; tenancy model.
- Implementation ecosystem preference (for harness handoff notes only).

## Operating rules

- Product outcomes drive testing. Every major suite must justify which risk it reduces and which user-visible or system behavior it validates. Reject coverage-driven testing with no risk mapping.
- Test the contract, not the implementation. Validate externally visible behavior — APIs, events, workflows, state transitions, persistence guarantees. Reject tests coupled to internal structure.
- Production realism beats mock-heavy isolation. Use real databases, queues, caches, and middleware in disposable containers. Mock only systems outside the service boundary or failures unsafe to reproduce. Reject mocking repositories, persistence adapters, or the system under test.
- Every externally visible behavior needs both success and failure validation, including edge conditions. Reject success-only plans.
- Acceptance criteria derive from PRD success metrics and SLOs, never invented independently. Reject "works properly".
- Quality is layered: each layer reduces a distinct risk class. Reject duplicated behavioral scope across layers without justification.
- Determinism is mandatory: deterministic setup, teardown, isolated state, reproducible execution. Do not rely on transactional rollback across asynchronous boundaries.
- CI/CD gates are architecture. Every suite declares trigger, runtime budget, flake policy, and release impact. Reject undefined merge or release criteria.
- Observability is testable behavior. Validate logs, metrics, traces, alerts, correlation IDs, and redaction. Reject systems observable only during failure investigation.
- Challenge weak testing assumptions directly and operationally. Ask for confirmation with a recommended default when a decision changes the gate contract: "I recommend X because Y. Confirm or redirect."
- Preserve the architecture. Do not redefine bounded contexts, components, data flow, or contracts; consume them. If a quality concern reveals an architecture gap, raise it as an ADR candidate or open decision.

## Output contract

`testing-strategy.md` MUST conform to [standards/quality-artifacts](../../../standards/quality-artifacts/README.md), which is authoritative for its file layout, frontmatter, required and conditional sections, ADR linkage, versioning, and linkage rules.

It additionally conforms to: [prd-schema](../../../standards/prd-schema/README.md) (acceptance criteria trace to success metrics), [api-standards](../../../standards/api-standards/README.md) (contract tests assert the error envelope, status conventions, and idempotency mechanism), [security-standards](../../../standards/security-standards/README.md) (401/403/insufficient-scope/cross-tenant coverage), [observability-standards](../../../standards/observability-standards/README.md) (structured signals, redaction), and [deployment-standards](../../../standards/deployment-standards/README.md) (gates align with the promotion flow). Skill structure conforms to [documentation-standards](../../../standards/documentation-standards/README.md).

Use `assets/testing-strategy.template.md`; it implements the schema. Do not invent endpoints, states, scopes, or success metrics — consume the approved upstream documents.

## Progressive references

- Read `references/testing-strategy-quality-rubric.md` before finalizing and use it as the validation checklist.
- Read `references/testing-strategy-playbook.md` when classifying risk by layer, deriving acceptance criteria, designing the contract/integration matrices, defining test data and determinism, planning authorization/observability/resilience/migration/performance validation, defining CI gates, or checking the anti-pattern list.
- Use `assets/testing-strategy.template.md` for the artifact.

## Process

Progress:

- [ ] Step 1: Load the approved `system-design.md`, the architecture documents it spawned, the published contracts, the persistence/migration plan, and the PRD success metrics. Identify critical workflows, externally visible behavior, and operational risk surfaces. Refuse to invent endpoints, states, scopes, or metrics.
- [ ] Step 2: Map each PRD success metric to a measurable acceptance criterion (observable behavior, threshold, pass/fail) or a documented non-testable rationale.
- [ ] Step 3: Classify risks by category and severity, and map each to exactly one owning test layer. Reject using E2E to compensate for missing integration or contract coverage.
- [ ] Step 4: Define test layers — scope, ownership, runtime budget, confidence target per layer. Reject overlapping behavioral scope without justification.
- [ ] Step 5: Build the contract test matrix: per API/event/webhook define happy-path, negative, error-envelope, auth posture, idempotency, and compatibility/versioning behavior.
- [ ] Step 6: Define the integration test plan: production-like dependencies in disposable containers, topology, isolation, state reset, startup ordering, and the explicit mock boundary (only outside the service).
- [ ] Step 7: Define test data and state management: fixtures, seed, deterministic cleanup, transaction boundaries, and eventual-consistency handling.
- [ ] Step 8: Define authorization and security validation (401, 403, insufficient scope, cross-tenant) and observability validation (logs, metrics, traces, alerts, correlation IDs, redaction).
- [ ] Step 9: When applicable, define migration/persistence validation, resilience/failure validation, and performance/scalability validation with measurable thresholds; otherwise record the omission rationale.
- [ ] Step 10: Define CI/CD quality gates: per suite trigger, runtime budget, flake policy, blocking vs advisory, merge-gating vs release-gating, and artifact retention, aligned to the promotion flow.
- [ ] Step 11: Draft an ADR inline for each non-obvious testing/tooling decision (pyramid balance, contract tooling, harness substrate, flake-quarantine policy) under `adrs/NNNN-<slug>.md`, and reference each from the ADR Index.
- [ ] Step 12: Generate `testing-strategy.md` from `assets/testing-strategy.template.md` with explicit implementation handoffs. Validate against [standards/quality-artifacts](../../../standards/quality-artifacts/README.md) and `references/testing-strategy-quality-rubric.md`; revise until both pass or note the unresolved gap explicitly.

## Outputs

Required:

- `testing-strategy.md` at `docs/quality/<product-or-service-slug>/`, with frontmatter and sections per [standards/quality-artifacts](../../../standards/quality-artifacts/README.md).

Optional, when applicable:

- `matrices/acceptance-criteria.md`, `matrices/contract-test-matrix.md`, `matrices/workflow-coverage.md`.
- Integration topology diagram, CI gate matrix, resilience test catalog, observability validation checklist.
- ADR drafts for testing/tooling strategy.

Output rules:

- Every suite must map to a named risk it reduces and a behavior it validates.
- Every externally visible behavior must define happy-path, negative, and edge-condition validation.
- Every non-idempotent operation must validate retry and idempotency using the contract's mechanism.
- No mock may replace a component inside the system boundary.
- Acceptance criteria must be measurable or carry a documented non-testable rationale.
- Do not redefine bounded contexts, components, data flow, or contracts; consume them.

## Quality checks

- [ ] `references/testing-strategy-quality-rubric.md` was loaded before finalizing.
- [ ] `testing-strategy.md` validates against [standards/quality-artifacts](../../../standards/quality-artifacts/README.md): frontmatter complete; required sections present; conditional omissions justified under `## Omitted sections`.
- [ ] Every PRD success metric maps to a measurable acceptance criterion or a documented non-testable rationale.
- [ ] Every externally visible workflow has happy-path and failure-path validation; every API contract asserts the [api-standards](../../../standards/api-standards/README.md) error envelope.
- [ ] Non-idempotent operations validate retry and idempotency via the contract's mechanism.
- [ ] Auth validation covers 401, 403, and cross-tenant denial where applicable, per [security-standards](../../../standards/security-standards/README.md).
- [ ] No mock replaces a component inside the system boundary; integration tests use production-like dependencies.
- [ ] Test setup and cleanup are deterministic and reproducible.
- [ ] Observability behavior is validated and secret redaction is asserted.
- [ ] CI/CD gates declare merge and release requirements and align with [deployment-standards](../../../standards/deployment-standards/README.md).
- [ ] Migration, resilience, and performance validation are present where applicable or explicitly omitted with rationale.

## References

- Output schema: [`standards/quality-artifacts`](../../../standards/quality-artifacts/README.md).
- `assets/testing-strategy.template.md`
- `references/testing-strategy-playbook.md`
- `references/testing-strategy-quality-rubric.md`
- Upstream architecture: [`system-design`](../system-design/SKILL.md), [`backend-architecture`](../backend-architecture/SKILL.md).
- Downstream consumers: each [implementations/*](../../implementations/) skill wires this strategy into its own runner and fixtures.
