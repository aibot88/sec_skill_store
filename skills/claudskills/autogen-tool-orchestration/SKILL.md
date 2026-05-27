---
name: autogen-tool-orchestration
description: Use when an approved ai-architecture.md defines a tool surface and AutoGen is the chosen framework. Produces tool schemas, an authorization-enforcing execution adapter, idempotency, audit logging, and tool-failure tests. Not for agent topology, retrieval design, or provider SDK work.
---

# AutoGen Tool Orchestration

## When to use

Invoke when `ai-architecture.md` approves a tool surface that AutoGen agents
call (functions, side-effecting actions, external lookups) and AutoGen
(AgentChat / Core) is the chosen framework.

Do not use to design the multi-agent topology or termination authority (that is
`autogen-multi-agent-workflow`), to design the retrieval surface or tool
surface itself (an upstream architecture decision), or to implement
provider/model SDK specifics (those belong to the provider skills).

## Inputs

Required:

- Approved `ai-architecture.md`.
- The approved tool surface: each tool's name, purpose, input schema, and
  side-effect class.
- Per-tool authorization model and the principal source.
- Idempotency policy and the idempotency-key source for each side-effecting
  tool.
- Audit-logging requirements and retention rules.
- Eval plan: the fixed evaluation set and the pass thresholds.
- Target application language and framework; provider/model contract.

Optional:

- Existing tool implementations and the retrieval surface backing the
  Researcher's retrieval tool.
- Retry, latency, and cost budgets per tool.
- OpenTelemetry / tracing target.
- Sample successful and failed tool-execution traces.

## Reference workflow

This skill is grounded in a concrete reference so it does not degrade into
generic framework advice: **Research-and-synthesize**. Three roles —
**Researcher** (retrieves source material for a question from the
architecture-defined retrieval surface), **Critic/verifier** (checks the
draft's claims against retrieved sources, gates completion), **Writer**
(produces the final answer with inline citations). Input: a question. Output: a
cited synthesized answer. This skill owns the **tool/function registration and
execution adapter** the Researcher (and any tool-using agent) depends on: tool
schemas, an authorization-enforcing execution adapter, idempotency for
side-effecting tools, audit logging, and tool-failure tests. The realization is
AutoGen-specific; the tool contract and the eval triplet below are
framework-invariant.

## Operating rules

- Preserve the tool surface from `ai-architecture.md`. Do not add, widen,
  rename, or repurpose a tool, and do not relax a tool's input schema. A
  missing tool, side-effect class, authorization model, idempotency policy, or
  audit retention rule → pause and raise an ADR candidate; do not invent it.
- Tool schemas are a contract surface. Each registered tool's input schema is
  exactly the approved schema; versioning and breaking-change policy apply as
  for any external API.
- Authorization is enforced in the execution adapter, never delegated to the
  model. The model proposes a tool call; the adapter resolves the principal
  from request context (not from model output) and verifies the principal is
  permitted to run that tool with those arguments before any side effect. A
  model-proposed tool call is untrusted input.
- Only approved tools are registered, and each tool only on the agents the
  topology permits. The tool set is a closed set from the architecture's tool
  surface; the Researcher holds the retrieval tool, the Writer and Critic do
  not get tools they were not granted.
- Side-effecting tools are idempotent. Every mutating tool execution carries an
  idempotency key derived from a stable request property per the architecture's
  policy; a replayed or retried tool call does not double-apply. Read-only
  tools may skip this only when their side-effect class is explicitly read-only.
- Every tool execution is audited. The audit record captures tool name,
  resolved principal, authorization outcome, idempotency key, result class
  (success / denied / failed), and correlation id — never raw secrets or
  unredacted PII.
- Tool failure is a handled path, not an exception swallowed as success. A
  denied or failed call returns a structured error result to the agent loop;
  the Critic's grounding gate never passes on a failed retrieval.
- The eval triplet is wired, not described: grounding score, citation
  correctness, and answer correctness are computed against the fixed eval set
  and gated at the architecture's thresholds, exercising the registered
  retrieval tool end to end.
- Provider-neutral: the model/provider is an `ai-architecture.md` input
  injected at deploy time; no provider SDK specifics are hardcoded here (those
  belong to the provider skills).

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — each tool schema is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — authorization enforced in the adapter before any side effect; no secrets or PII in tool arguments, results, logs, or audit records without redaction; credentials injected at deploy time, never committed.
- [observability-standards](../../../../../standards/observability-standards/README.md) — per-execution audit record and metrics for tool-call counts, authorization outcomes, idempotency outcomes, tool failures, and latency, with a correlation id.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model, tool config, and authorization policy injected at deploy time, never hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — tool, principal, metric, and audit-field names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the tool
surface, each tool's side-effect class and authorization model, the idempotency
policy and key source, audit retention, and the eval plan; `architecture/security`
for the authorization model, side-effect classification, idempotency policy,
and audit/credential rules. If any is silent on a material decision, this skill
pauses and raises an ADR candidate rather than inventing it.

## Progressive references

- Read `references/autogen-tool-orchestration-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/autogen-tool-orchestration-quality-rubric.md` before declaring the integration complete.
- Use `assets/autogen-tool-orchestration.template.md` as the schema, adapter, idempotency, audit, and test-matrix reference.

## Process

1. Load `ai-architecture.md` and identify the approved tool surface, each
   tool's input schema and side-effect class, the per-tool authorization model
   and principal source, the idempotency policy and key source, audit
   retention, and the eval plan.
2. Verify each tool's side-effect class, authorization model, idempotency
   policy, and audit retention are all present; if any is missing, raise an ADR
   candidate before writing code.
3. Define each tool with its approved name, description, and input schema
   verbatim from the contract; classify its side-effect class explicitly.
4. Register each tool only on the agents the topology permits (the Researcher's
   retrieval tool on the Researcher only); keep the tool set a closed set.
5. Implement the execution adapter: resolve principal from request context →
   authorization check → argument validation against the input schema →
   idempotency-keyed execution → structured result.
6. Implement idempotency for every side-effecting tool: derive the key from the
   stable property per policy; a replay returns the prior result, never a
   second side effect.
7. Add audit logging for every tool execution (tool name, principal, authz
   outcome, idempotency key, result class, correlation id) with redaction.
8. Wire tool failure into the agent loop as a structured error result; ensure
   the Critic's grounding gate cannot pass on a failed retrieval.
9. Add tracing/metrics for tool-call counts, authorization outcomes,
   idempotency outcomes, tool failures, and latency with a correlation id.
10. Wire the eval triplet (grounding, citation correctness, answer
    correctness) against the fixed eval set, exercising the registered
    retrieval tool, and gate at the architecture's thresholds.
11. Add tests for a valid tool call, an unauthorized call denied at execution,
    a tool execution failure, idempotent replay (no double-apply), an
    out-of-surface/ungranted tool call denial, and an eval-gate failure.
12. Document unresolved architecture gaps as ADR candidates instead of silently
    filling them in.

## Outputs

- AutoGen tool registry wired to the approved tools on permitted agents only.
- Tool definitions (name, description, input schema) derived verbatim from the
  contract, with explicit side-effect classification.
- Execution adapter with principal resolution, authorization, argument
  validation, idempotency, and structured result shaping.
- Idempotency layer keyed per the architecture's policy for side-effecting
  tools.
- Audit-logging integration for every tool execution.
- Tool-failure handling wired into the agent loop.
- Tracing/metrics for tool-call counts, authorization, idempotency, failures,
  and latency.
- Eval-triplet harness exercising the registered retrieval tool, gated at
  thresholds.
- Tests for valid call, unauthorized call, tool failure, idempotent replay,
  out-of-surface/ungranted denial, and eval-gate failure.

Output rules:

- Authorization is enforced in the adapter before any side effect; a
  model-proposed call is never trusted.
- Each tool's input schema matches the approved schema 1:1; no tool added,
  widened, or repurposed.
- Every mutating tool execution carries an idempotency key; replay does not
  double-apply.
- Only approved tools are registered, only on permitted agents.
- The eval triplet is computed and gated against the registered retrieval
  tool, not merely described.
- No provider SDK specifics or credentials are hardcoded.

## Quality checks

- [ ] The implementation consumes a named tool surface from `ai-architecture.md`.
- [ ] Each tool's input schema matches the approved schema; no tool added, widened, renamed, or repurposed.
- [ ] Authorization is enforced in the execution adapter, with the principal resolved from request context, before any side effect.
- [ ] Every side-effecting tool carries an idempotency key; replay is proven not to double-apply.
- [ ] Only approved tools are registered, only on the agents the topology permits (Researcher holds retrieval).
- [ ] Each tool's side-effect class is explicitly classified, not guessed.
- [ ] Every tool execution is audited (tool, principal, authz outcome, idempotency key, result class, correlation id) with no raw secrets or unredacted PII.
- [ ] Tool failure returns a structured error into the agent loop; the Critic's grounding gate cannot pass on a failed retrieval.
- [ ] The eval triplet (grounding, citation correctness, answer correctness) is wired through the registered retrieval tool and gated at thresholds.
- [ ] Tests cover valid call, unauthorized denial, tool failure, idempotent replay, out-of-surface/ungranted denial, and eval-gate failure.
- [ ] Any missing tool, side-effect class, authorization, idempotency, audit, or eval decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — tool surface, capability contract, eval plan.
- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md) — per-tool authorization model, side-effect classification, idempotency policy, audit and credential rules.
- Cross-framework siblings: [`crewai-task-and-tool-design`](../../crewai/crewai-task-and-tool-design/SKILL.md) (same archetype, CrewAI mechanics), [`anthropic-tool-use-runtime`](../../anthropic/anthropic-tool-use-runtime/SKILL.md) (provider tool mechanics this wraps). Sibling autogen skills are listed in the [autogen stack README](../README.md).
- Related implementation skills: [`autogen-multi-agent-workflow`](../autogen-multi-agent-workflow/SKILL.md) (the topology that consumes this skill's tools).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
