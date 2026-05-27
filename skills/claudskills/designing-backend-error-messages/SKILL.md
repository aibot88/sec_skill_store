---
name: designing-backend-error-messages
description: Designs backend API error contracts with a REST-default approach using RFC 9457 Problem Details, stable machine-readable codes, retry semantics, validation error payloads, observability, and security-safe messaging. Reviews existing error handling against a binary rubric and proposes concrete fixes. Produces optional artifacts such as errors.yaml entries, Problem Details examples, OpenAPI fragments, and runbook templates. Use when creating or revising backend error responses, auditing API error quality, mapping status/code behavior, or documenting error handling for REST, gRPC, GraphQL, and async services.
category: System Architecture
---

# Designing Backend Error Messages

Author backend error-message contracts with a REST-first workflow. Switch transport guidance only when the task explicitly targets gRPC, GraphQL, or async/event systems.

## Workflow

1. **Establish scope and transport**
   - Identify API style: REST (default), gRPC, GraphQL, or async/event.
   - Identify whether the task is design-from-scratch or refactor/review.

2. **Define the canonical error shape first**
   - For REST, use `application/problem+json`.
   - Include these baseline fields:
     - `type`, `title`, `status`, `code`, `detail`, `trace_id`
   - Add extensions only when needed:
     - `errors[]` (validation), `is_transient`, `retry_after_ms`, `help_url`, domain metadata.

3. **Define status-code policy and error-code taxonomy**
   - Map each failure mode to the most specific status code.
   - Assign a stable namespaced machine code per failure mode (for example `validation.email.invalid_format`).
   - Keep code names stable; never rename published codes.

4. **Write user-facing message copy**
   - Keep `title` stable per error type.
   - Make `detail` occurrence-specific and actionable.
   - State the next action clearly: fix request, retry (with timing), or contact support with `trace_id`.

5. **Handle validation and retry semantics explicitly**
   - Return all field errors in one response.
   - Use JSON Pointer paths in `errors[].pointer`.
   - Set retry semantics with `is_transient`; include `Retry-After` / equivalent hints when applicable.
   - For non-idempotent operations, require idempotency keys before recommending retries.

6. **Enforce observability and security guarantees**
   - Ensure `trace_id` is propagated, logged, and returned.
   - Log forensic detail internally; never expose stack traces, SQL, infra internals, secrets, or PII on the wire.
   - Use a registry-backed serializer so unregistered errors degrade to a safe generic internal error response.

7. **Produce outputs requested by the user (optional artifacts)**
   - Optional: error contract examples, `errors.yaml` entries, OpenAPI snippets, transport-specific examples, runbook stubs, review findings.
   - If not specified, propose these artifacts but do not force them.

8. **Run a final quality gate before returning**
   - Verify structure, retry signaling, validation coverage, security hygiene, observability linkage, and documentation completeness.

## Defaults

- Default transport: **REST + RFC 9457 Problem Details**.
- Default retry signal: explicit boolean `is_transient`, with `Retry-After` when known.
- Default field path format: **JSON Pointer**.
- Default machine-code style: lowercase namespaced identifiers with dots.
- Default support pivot: include `trace_id` in every error response.

## Output template (use when authoring)

```markdown
## Error contract
- Shape: [Problem Details / gRPC Status / GraphQL errors+extensions / async envelope]
- Required fields: [...]
- Retry fields: [...]
- Validation fields: [...]

## Error catalog additions
- [code] → [status] → [transient/permanent] → [trigger] → [remediation]

## Examples
- [At least one concrete response body per major failure mode]

## Notes
- Observability: [trace/log/metric linkage]
- Security: [leak-prevention checks passed]
```

## Examples

**Example 1 — Author REST errors for a new endpoint**

- **Input:** "Design error handling for `POST /v1/charges` with validation failures, rate limits, and upstream payment outages."
- **Output:**
  - Problem Details contract with required fields (`type`, `title`, `status`, `code`, `detail`, `trace_id`)
  - Status/code mapping (for example `422 validation.failed`, `429 rate_limit.per_user_exceeded`, `503 billing.processor_unavailable`)
  - Concrete sample payloads for 422, 429, and 503
  - Optional `errors.yaml` entries and OpenAPI response references

**Example 2 — Review and fix an existing response**

- **Input:** "Review this error payload: `{ \"status\":500, \"message\":\"NullPointerException at billing.go:142\" }` and propose a safe replacement."
- **Output:**
  - Findings: incorrect status, leaked internal details, missing machine code, missing traceability, no remediation guidance
  - Corrected payload using safe public detail, stable `code`, and `trace_id`
  - Recommended internal log fields to preserve forensic debugging without leakage

**Example 3 — Non-REST transport request**

- **Input:** "Define gRPC errors for `CreateInvoice` including invalid argument, concurrency abort, and temporary upstream outage."
- **Output:**
  - Canonical gRPC status mapping (`INVALID_ARGUMENT`, `ABORTED`, `UNAVAILABLE`)
  - Structured details plan (for example `ErrorInfo`, `BadRequest`, `RetryInfo`)
  - Retry guidance aligned to idempotency and transient classification

## Edge cases

- **gRPC**: Use canonical gRPC status codes; include structured details (for example `ErrorInfo`, `BadRequest`, `RetryInfo`) when relevant.
- **GraphQL**: Return domain details in `errors[].extensions` and maintain stable `extensions.code` semantics.
- **Async/event-driven**: Keep stable error envelopes on dead-letter or failure events and preserve correlation identifiers across hops.
- **Conditional conflicts**: Distinguish plain conflicts from precondition/header failures.

## Progressive disclosure references

Load only the file needed for the task.

- **Foundations and status mapping**: [references/01-foundations-and-status-codes.md](references/01-foundations-and-status-codes.md)
- **Stable codes, message writing, validation, retry taxonomy**: [references/02-codes-messages-validation-and-retryability.md](references/02-codes-messages-validation-and-retryability.md)
- **Idempotency, observability, security controls**: [references/03-idempotency-observability-and-security.md](references/03-idempotency-observability-and-security.md)
- **Transport-specific implementation + anti-patterns**: [references/04-transport-guidance-and-anti-patterns.md](references/04-transport-guidance-and-anti-patterns.md)
- **Registry-driven documentation and OpenAPI integration**: [references/05-documenting-errors-registry-and-openapi.md](references/05-documenting-errors-registry-and-openapi.md)
- **AI-consumable docs, runbook template, review rubric, starter catalog, sources**: [references/06-ai-agent-docs-runbooks-rubric-catalog-and-sources.md](references/06-ai-agent-docs-runbooks-rubric-catalog-and-sources.md)
