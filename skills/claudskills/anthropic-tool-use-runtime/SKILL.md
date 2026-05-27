---
name: anthropic-tool-use-runtime
description: Use when an approved ai-architecture.md defines an Anthropic Claude capability whose model calls tools or takes side-effecting actions. Produces tool schemas, an auth-enforcing execution adapter, idempotency, audit logging, and failure tests. Not for schema-only output, RAG, or agent design.
---

# Anthropic Tool Use Runtime

## When to use

Invoke when `ai-architecture.md` defines a capability whose model is allowed to
call tools (functions, side-effecting actions, external lookups) and the chosen
provider is Anthropic (Claude via the Messages API).

Do not use for free-form chat, schema-bound output without tool execution,
retrieval topology design, or agent control-flow and stop-condition design.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Capability name and model contract.
- Approved tool surface: each tool's name, purpose, input schema, side-effect class, and authorization model.
- Target application language and framework.

Optional:

- Idempotency policy and idempotency-key source per tool.
- Audit-logging requirements and retention rules.
- Parallel-tool-use allowance and `tool_choice` policy from the architecture.
- Whether any MCP connector tool is explicitly approved.
- Prompt-cache strategy for the tool-definition prefix.
- Latency, cost, and retry budgets.
- Sample successful and failed tool-call traces.

## Operating rules

- Preserve the tool surface from `ai-architecture.md`. Do not add, widen, rename, or repurpose a tool, and do not relax a tool's input schema. If a tool, side-effect class, or authorization model is missing, raise an ADR candidate instead of inventing it.
- Tool schemas are a contract surface. Each `input_schema` is exactly the approved schema; versioning and breaking-change policy apply as for any external API.
- Authorization is enforced in the execution adapter, never delegated to the model. The model proposes a tool call; the adapter verifies the caller is permitted to run that tool with those arguments before any side effect. A model-proposed call is untrusted input.
- Side-effecting tools are idempotent. Every mutating tool execution carries an idempotency key derived from a stable request property per the architecture's policy; a replayed `tool_use` does not double-apply.
- `tool_choice` is a deliberate decision, stated explicitly: `auto` (model decides), `any` (must call some tool), `{type: "tool", name}` (force one tool), or `none` (suppress tools). The choice traces to the contract, never left to default by omission.
- Parallel tool use is a decision. If the architecture allows the model to emit multiple `tool_use` blocks in one turn, the adapter executes them with explicit ordering/concurrency and authorization per call; if disallowed, parallel tool use is suppressed and asserted off.
- MCP connector tools are used only where `ai-architecture.md` explicitly approves a named connector. An MCP tool is a remote side-effecting surface: same authorization, idempotency, and audit rules apply, plus the connector's trust boundary is documented.
- Every tool execution is audited. The audit record captures tool name, authorization outcome, idempotency key, result class, and correlation id — never raw secrets or unredacted PII.
- Prompt caching is a decision, not an accident. `cache_control` is placed only on the stable tool-definition prefix (system prompt + tool definitions), never on per-request content (`tool_result`, user input, retrieved data); cache placement never changes tool semantics, and a cache miss is never a correctness failure.
- Extended thinking is handled, not ignored. If the capability uses extended thinking, thinking blocks are preserved or stripped per the architecture and the parser selects `tool_use` blocks while tolerating preceding `thinking` blocks; if unused, state N/A explicitly.
- No sensitive data in telemetry. Tool name, authorization outcome, latency, tokens, cache outcome, and result class are logged; tool arguments, results, secrets, and PII are redacted unless the architecture explicitly permits a field.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — each tool schema is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — authorization enforced before side effects; no secrets or PII in prompts, tool arguments, results, logs, or audit records without redaction; Anthropic API credentials injected at deploy time, never committed.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logs and metrics for latency, input/output tokens, cache-read/write tokens, tool-call counts, authorization outcomes, tool failures, and model/prompt version; trace propagation through the tool loop.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model id, prompt version, tool-cache strategy, and `tool_choice` policy are deploy-time configuration, not hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — capability, tool, metric, and audit-field names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the capability, tool surface, each tool's authorization model and side-effect class, idempotency policy, parallel-tool and `tool_choice` policy, any approved MCP connector, prompt-cache strategy, extended-thinking requirement, degradation behavior, and latency/cost budgets. If it is silent on any of these, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Progressive references

- Read `references/anthropic-tool-use-runtime-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/anthropic-tool-use-runtime-quality-rubric.md` before declaring the integration complete.
- Use `assets/anthropic-tool-use-runtime.template.md` as the request-shape, adapter, audit, telemetry, and test-matrix reference.

## Process

1. Load `ai-architecture.md` and identify the capability, the approved tool surface, each tool's side-effect class and authorization model, idempotency policy, and prompt-cache strategy.
2. Verify the architecture names the model tier, the `tool_choice` and parallel-tool policy, any approved MCP connector, the extended-thinking requirement, and degradation behavior.
3. Define each tool with its approved name, description, and `input_schema` verbatim from the contract; record the `tool_choice` decision and why.
4. Implement the Messages API request: system prompt, messages, tool definitions, the chosen `tool_choice`, and explicit decoding settings.
5. Place `cache_control` on the stable tool-definition prefix per the architecture's cache strategy; confirm no breakpoint sits on `tool_result` or per-request content.
6. Implement the execution adapter: authorization check → argument validation against `input_schema` → idempotency-keyed execution → structured `tool_result`.
7. Implement the tool loop: feed `tool_result` back, handle multiple/parallel `tool_use` blocks per the policy, and bound the loop with a max-iteration limit.
8. If extended thinking is required, reconcile thinking blocks with `tool_use` parsing per the architecture's retention rule; otherwise mark N/A.
9. Add audit logging for every tool execution and telemetry for model id, prompt version, latency, tokens, cache outcome, tool-call counts, authorization outcomes, and tool failures.
10. Add tests for a valid tool call, an unauthorized call, a tool execution failure, idempotent replay, retry/loop-bound exhaustion, and a cache-miss path.
11. Document unresolved architecture gaps as ADR candidates instead of silently filling them in.

## Outputs

- Anthropic Messages API integration for the tool-use capability, including the bounded tool loop.
- Tool definitions (name, description, `input_schema`) derived verbatim from the contract.
- Tool execution adapter with authorization, argument validation, idempotency, and structured `tool_result` shaping.
- Audit-logging integration for every tool execution.
- Prompt or message template files with tool-prefix cache-breakpoint placement noted.
- Tests for valid call, unauthorized call, tool failure, idempotent replay, loop-bound exhaustion, and cache miss.
- Telemetry notes for tokens, cache outcomes, latency, tool-call counts, authorization outcomes, and model version.

Output rules:

- The `tool_choice` and parallel-tool decisions are stated explicitly; never left implicit.
- Authorization is enforced in the adapter before any side effect; a model-proposed call is never trusted.
- Every mutating tool execution carries an idempotency key; replay does not double-apply.
- `cache_control` appears only on the tool-definition prefix; never on `tool_result` or per-request content.
- No Anthropic API key, MCP connector secret, or environment-specific endpoint committed to source.

## Quality checks

- [ ] The implementation consumes a named capability and tool surface from `ai-architecture.md`.
- [ ] Each tool's `input_schema` matches the approved schema; no tool added, widened, or repurposed.
- [ ] Authorization is enforced in the execution adapter before any side effect.
- [ ] Every mutating tool carries an idempotency key; replay is proven not to double-apply.
- [ ] `tool_choice` and parallel-tool-use policy are explicit and justified against the contract.
- [ ] MCP connector tools appear only where the architecture explicitly approves them, with the same authz/idempotency/audit rules.
- [ ] `cache_control` sits only on the tool-definition prefix and does not change tool semantics.
- [ ] Extended-thinking interaction with `tool_use` parsing is handled per the architecture (or explicitly N/A).
- [ ] Audit records and telemetry exclude unredacted secrets, tool arguments/results, and PII.
- [ ] Tests cover valid call, unauthorized call, tool failure, idempotent replay, loop-bound exhaustion, and a cache-miss path.
- [ ] Any missing tool, authorization, idempotency, cache, `tool_choice`, or degradation decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — capability, model contract, tool surface, `tool_choice`/parallel policy, cache strategy, degradation behavior, budgets.
- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md) — tool authorization model, side-effect classification, idempotency policy, audit and credential rules.
- Cross-provider counterpart: [`openai-tool-calling-runtime`](../../openai/openai-tool-calling-runtime/SKILL.md) — same archetype, OpenAI mechanics.
- Related implementation skills: [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (when tool use is embedded in agent control flow). Sibling anthropic skills are listed in the [anthropic stack README](../README.md).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
