---
name: crewai-task-and-tool-design
description: Use when an approved ai-architecture.md defines CrewAI tasks or callable tools. Produces task decomposition, tool schemas, an auth-enforcing execution adapter, idempotency, audit logging, and failure tests. Not for crew topology, retrieval design, or provider SDK work.
---

# CrewAI Task and Tool Design

## When to use

Invoke when `ai-architecture.md` approves a task surface and/or a tool surface
that a CrewAI agent may invoke, and CrewAI is the chosen framework.

Do not use to design the crew topology, role/process control flow, or
termination authority (that is the `crewai-agent-workflow` concern), to design
the retrieval topology, or to do provider SDK work (that belongs to the provider
skills).

## Inputs

Required:

- Approved `ai-architecture.md`.
- The approved task surface: task boundaries, each task's input/output
  contract, and which agent owns it.
- The approved tool surface: each tool's name, purpose, input schema,
  side-effect class, and per-tool authorization model.
- Idempotency policy and the idempotency-key source per side-effecting tool.
- Audit-logging requirements and retention rules.
- Target application language and framework; provider/model contract.

Optional:

- Existing tool implementations and the retrieval surface a research task wraps.
- Concurrency/ordering policy when a task fans out multiple tool calls.
- OpenTelemetry / tracing target.
- Sample successful and failed task and tool-call traces.

## Reference workflow

This skill is grounded in a concrete reference so it does not degrade into
generic framework advice: **Research-and-synthesize**. Three roles —
**Researcher** (retrieves source material for a question from the
architecture-defined retrieval surface), **Critic/verifier** (checks the draft's
claims against retrieved sources and gates completion), **Writer** (produces the
final answer with inline citations). Input: a question. Output: a cited
synthesized answer. The crew topology and the Critic's termination authority are
owned by `crewai-agent-workflow`; **this skill owns the CrewAI task
decomposition and the tool registry and execution adapter the Researcher (and
any tool-using agent) depends on** — the retrieve-sources tool the Researcher's
task calls, the task boundaries that carve the work into Researcher/Writer/Critic
units, the authorization-enforcing execution adapter, idempotency for
side-effecting tools, and audit logging. The realization is CrewAI-specific; the
workflow contract and the eval triplet below (grounding score, citation
correctness, answer correctness, computed over the fixed eval set and gated at
the architecture's thresholds) are framework-invariant.

## Operating rules

- Implement only the approved task and tool surface from `ai-architecture.md`.
  Do not invent a task, split or merge a task boundary, add a "helper" tool,
  widen an argument type, rename a tool, or relax a required field. A missing
  task boundary, tool, side-effect class, authorization model, idempotency
  policy, or audit-retention rule is an ADR candidate, not an implementation
  choice.
- Task decomposition maps to the approved scope. Each CrewAI `Task` has an
  explicit input/output contract and the agent that owns it; tasks are not
  invented beyond the architecture and not silently chained into autonomy the
  design never granted.
- Tool schemas are a contract surface. Each tool's input schema is exactly the
  approved schema; versioning and breaking-change policy apply as for any
  external API.
- Authorization is enforced in the execution adapter, never delegated to the
  model. The model proposes a tool call; the adapter resolves the principal from
  request context (not from model output) and verifies the principal is
  permitted to run that tool with those arguments before any side effect. A
  model-proposed call is untrusted input.
- Side-effecting tools are idempotent. Every mutating tool execution carries an
  idempotency key derived from a stable request property per the architecture's
  policy; a replayed or retried tool call does not double-apply. Read-only tools
  may skip this; each tool's side-effect class is classified explicitly, never
  guessed.
- Tools are registered as a closed set, only on the agents and tasks the
  architecture permits. In the reference the Researcher's task has the
  retrieve-sources tool; the Writer and Critic tasks receive no tools they were
  not granted.
- Tool fan-out is a decision. If a task is permitted to issue multiple tool
  calls, the adapter executes each with its own authorization and idempotency
  under explicit ordering or bounded concurrency; unbounded fan-out of
  side-effecting calls is an incident.
- Every tool execution is audited: tool name, resolved principal, authorization
  outcome, idempotency key, result class (success / denied / failed), and
  correlation id — never raw secrets, raw tool payloads, or unredacted PII.
- The eval triplet is wired, not described: grounding score, citation
  correctness, and answer correctness are computed against the fixed eval set
  and gated at the architecture's thresholds; the tool/task layer this skill
  owns is exercised by that harness.
- Provider-neutral: the model/provider is an `ai-architecture.md` input injected
  at deploy time; no provider SDK specifics are hardcoded here (those belong to
  the provider skills).

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — each tool schema and each task input/output contract is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — authorization enforced in the adapter before side effects, principal resolved from request context, credentials injected at deploy time, no secrets or PII in tool arguments, results, logs, or audit records without redaction.
- [observability-standards](../../../../../standards/observability-standards/README.md) — per-execution audit records and metrics (tool-call counts, authorization outcomes, idempotency hits, tool/task failures) with a correlation id propagated through the task and tool path.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model, prompt, tool, and task configuration injected at deploy time, never hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — task, tool, metric, and audit-field names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the task
boundaries, tool surface, each tool's authorization model and side-effect class,
idempotency policy, audit retention, fan-out policy, and eval plan;
`architecture/security` for tool authorization, side-effect classification,
idempotency, and audit rules. If any is silent, this skill pauses and raises an
ADR candidate rather than inventing the decision.

## Progressive references

- Read `references/crewai-task-and-tool-design-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/crewai-task-and-tool-design-quality-rubric.md` before declaring the task/tool layer complete.
- Use `assets/crewai-task-and-tool-design.template.md` as the task-decomposition, tool-schema, adapter, audit, and test-matrix reference.

## Process

1. Load `ai-architecture.md` and identify the approved task boundaries, the
   owning agent per task, the tool surface, each tool's side-effect class and
   authorization model, the idempotency policy, audit retention, and the eval
   plan.
2. Verify the task boundaries, per-tool authorization, side-effect class,
   idempotency-key source, fan-out policy, and audit retention are all present;
   if any is missing, raise an ADR candidate before writing code.
3. Decompose the work into CrewAI `Task`s matching the approved boundaries; for
   the reference, a retrieve task (Researcher), a synthesis task (Writer), and a
   verification task (Critic), each with an explicit input/output contract and
   owning agent.
4. Define each tool with its approved name, description, and input schema
   verbatim from the contract; classify each tool's side-effect class.
5. Register only the approved tools, only on the agents/tasks the architecture
   permits (the retrieve-sources tool on the Researcher's task only).
6. Implement the execution adapter: principal resolved from request context →
   authorization check → argument validation against the schema →
   idempotency-keyed execution for side-effecting tools → structured result.
7. Implement the fan-out policy: explicit ordering or bounded concurrency with
   per-call authorization and idempotency when a task issues multiple tool
   calls.
8. Add audit logging for every tool execution (tool name, principal, authz
   outcome, idempotency key, result class, correlation id) with redaction.
9. Wire the tool/task layer into the eval harness so the eval triplet
   (grounding, citation correctness, answer correctness) is computed over the
   fixed eval set and gated at thresholds.
10. Add tests for a valid tool call, an unauthorized call denied before side
    effect, a tool execution failure surfaced to its task, idempotent replay,
    fan-out ordering/bound, and an eval-gate failure.
11. Document unresolved architecture gaps as ADR candidates instead of silently
    filling them in.

## Outputs

- CrewAI `Task` decomposition realizing the approved task boundaries, each with
  an explicit input/output contract and owning agent.
- Tool definitions (name, description, input schema, side-effect class) derived
  verbatim from the contract.
- Tool execution adapter with principal resolution, authorization, argument
  validation, idempotency, and structured result shaping.
- Closed tool registry wired only to the agents/tasks the architecture permits.
- Fan-out ordering/concurrency control when a task issues multiple tool calls.
- Audit-logging integration for every tool execution.
- Eval-triplet wiring exercising the tool/task layer over the fixed eval set
  with gating thresholds.
- Tests for valid call, unauthorized call, tool failure, idempotent replay,
  fan-out bound, and eval-gate failure.

Output rules:

- Task boundaries map 1:1 to the approved scope; no task is invented, split, or
  merged.
- Authorization is enforced in the adapter before any side effect; a
  model-proposed call is never trusted.
- Every mutating tool execution carries an idempotency key; replay does not
  double-apply.
- Only approved tools are registered, only on permitted agents/tasks.
- No provider SDK specifics or credentials are hardcoded.

## Quality checks

- [ ] Task boundaries map 1:1 to the approved scope in `ai-architecture.md`; none invented, split, or merged.
- [ ] Each task has an explicit input/output contract and a single owning agent.
- [ ] Each tool's input schema matches the approved schema; no tool added, widened, renamed, or repurposed.
- [ ] Authorization is enforced in the execution adapter before any side effect, with the principal resolved from request context.
- [ ] Each tool's side-effect class is classified; every mutating tool carries an idempotency key and replay is proven not to double-apply.
- [ ] Only approved tools are registered, only on the agents/tasks the architecture permits.
- [ ] Tool fan-out is bounded with per-call authorization and idempotency, or explicitly disallowed.
- [ ] Audit records and telemetry exclude unredacted secrets, raw tool payloads, and PII.
- [ ] The eval triplet (grounding, citation correctness, answer correctness) is wired to the fixed eval set and gated at thresholds, exercising the tool/task layer.
- [ ] Tests cover valid call, unauthorized call, tool failure, idempotent replay, fan-out bound, and eval-gate failure.
- [ ] Any missing task boundary, tool, authorization, side-effect class, idempotency, audit-retention, or eval decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — task boundaries, tool surface, fan-out policy, eval plan.
- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md) — tool authorization model, side-effect classification, idempotency policy, audit and credential rules.
- Cross-framework siblings: [`autogen-tool-orchestration`](../../autogen/autogen-tool-orchestration/SKILL.md) (same archetype, AutoGen mechanics), [`crewai-agent-workflow`](../crewai-agent-workflow/SKILL.md) (consumes this skill's tasks/tools for the crew topology and termination). Sibling crewai skills are listed in the [crewai stack README](../README.md).
- Related implementation skills: [`anthropic-tool-use-runtime`](../../anthropic/anthropic-tool-use-runtime/SKILL.md) (provider tool mechanics this adapter wraps).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
