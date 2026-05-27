---
name: openai-tool-calling-runtime
description: Use when implementing OpenAI tool or function calling from an approved ai-architecture.md tool surface. Produces tool schemas, provider SDK wiring, execution adapters, authorization checks, idempotency rules, audit logging, tool failure handling, and tests for allowed, denied, failed, and retried tool calls. Do not use for AI architecture, generic chat, RAG, structured extraction without tools, or agent framework orchestration.
---

# OpenAI Tool Calling Runtime

## When to use

Invoke when `ai-architecture.md` defines a tool surface and OpenAI is the chosen
provider for tool-calling behavior.

Do not use when the tool surface has not been approved, when actions have
unresolved side effects, or when the user is asking for framework-level agent
orchestration.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Tool names, schemas, side-effect classes, and authorization scopes.
- Target application language and framework.
- Audit and logging requirements.

Optional:

- Existing service interfaces for tool execution.
- Idempotency keys or correlation-id strategy.
- Rate limits and retry budgets.
- Human-in-the-loop requirements.

## Operating rules

- Implement only tools approved in `ai-architecture.md`. An unlisted tool is a defect, not an enhancement.
- Every tool has a side-effect class, authorization scope, and idempotency rule defined before code is written. Any missing → refuse and raise an ADR candidate.
- Authorization and input validation precede side effects, always. The model proposing a call is never sufficient justification to execute it.
- Side-effecting tools are idempotent or guarded by an idempotency key or correlation id supplied by the caller, not the model.
- Tool failures are explicit states. Timeout, denied-authorization, malformed-arguments, and downstream-failure each have defined handling and a defined model-visible result.
- Audit before mutate. Tool name, actor, correlation id, redacted arguments, outcome, and side-effect class are recorded before the side effect commits.
- No secret or PII leakage through tool arguments, results, or logs.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — tool schemas are a contract surface; argument shape and versioning policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — authorization enforced before side effects, audit trail, no credential or PII leakage, provider and downstream credentials injected at deploy time.
- [observability-standards](../../../../../standards/observability-standards/README.md) — audit logs, per-tool metrics, and trace propagation across the tool-call boundary.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — tool endpoints and credentials are deploy-time configuration, never baked into prompts or code.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — tool names and audit field names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the tool surface, schemas, side-effect classes, authorization scopes, and idempotency rules; `architecture/security` is the source of truth for the authorization model. If either is silent, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Load `ai-architecture.md` and identify each approved tool, schema, side-effect class, and authorization scope.
2. Refuse to implement tools with undefined side effects, missing auth scope, or missing idempotency behavior.
3. Generate provider-specific tool schema definitions.
4. Implement a tool execution adapter that validates input before invoking application code.
5. Enforce authorization, idempotency, rate limits, and audit logging before side effects.
6. Handle tool failure, timeout, denied authorization, and model retry behavior explicitly.
7. Add tests for allowed tool calls, denied tool calls, malformed arguments, tool failure, and retry exhaustion.
8. Emit operational notes covering audit trails, side effects, and safe rollback.

## Outputs

- OpenAI tool schema definitions.
- Tool execution adapter.
- Authorization and idempotency checks.
- Audit logging hooks.
- Tests for success, denial, malformed input, failure, and retry paths.
- Operational notes for tool side effects.

## Quality checks

- [ ] Every implemented tool appears in `ai-architecture.md`.
- [ ] Every tool has a schema, side-effect class, idempotency rule, and authorization scope.
- [ ] Tool input is validated before any side effect occurs.
- [ ] Tests cover allowed, denied, malformed, failed, and retried tool calls.
- [ ] Audit logs identify tool name, actor, correlation id, outcome, and side-effect class.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — tool surface, schemas, side-effect classes, idempotency rules.
- Related architecture: [`architecture/security`](../../../../architecture/security/SKILL.md) — authorization model and trust boundaries for tool execution.
- Related implementation skills: [`openai-structured-output-runtime`](../openai-structured-output-runtime/SKILL.md) (tool arguments are structured output), [`openai-evals-and-observability`](../openai-evals-and-observability/SKILL.md) (tool-failure and denial regression gates), [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (agent tool registry builds on this provider mechanic).
- Compatible patterns: [`event-driven`](../../../../../architecture-patterns/event-driven/README.md) (tool side effects as domain events).
