---
name: lloydbriantech-ascent
description: >-
  ASCENT engineering framework. Use to scaffold new projects, enhance existing
  ASCENT projects, migrate non-ASCENT projects to ASCENT standards, or answer
  questions about ASCENT's conventions, principles, or nine engineering roles
  (delivery-lead, architect, ui-ux-designer, developer, data-engineer,
  ai-engineer, tester, devops, cybersecurity).
version: 0.3.0
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# lloydbriantech-ascent

The parent skill of the ASCENT engineering framework. It scaffolds new projects, enhances existing ASCENT projects, and migrates non-ASCENT projects to ASCENT standards. One skill routes user intent across nine engineering roles at runtime — see [ADR-001](../../docs/framework/DECISIONS/ADR-001-single-parent-skill.md) for why one skill instead of nine.

## When this skill engages

This skill should engage when any of the following hold:

- The user asks to scaffold or create a new project with ASCENT
- The user is in an ASCENT project (a `.ascent-meta.json` is present) and asks about conventions, principles, ADRs, or framework operations
- The user invokes a specific role explicitly (e.g. "as the architect role, draft an ADR for X")
- The user asks to bring an existing non-ASCENT project up to ASCENT standards (migrate mode)
- The user asks "what role handles X?" or otherwise references framework discipline

For requests that don't match these patterns, this skill should not engage.

## Operating modes

ASCENT defines four modes per [ADR-003](../../docs/framework/DECISIONS/ADR-003-ascent-meta-marker.md). The skill detects the active mode at the start of every invocation by examining the target directory.

| Mode | Engaged when | Behavior |
|---|---|---|
| `scaffold` | No `.ascent-meta.json` present | Greenfield creation — interview + full project tree |
| `enhance` | `.ascent-meta.json` present with a real slug | Additive surgical changes only (per [ADR-002](../../docs/framework/DECISIONS/ADR-002-modify-not-overwrite.md)) |
| `migrate` | User passes `--migrate` flag | Bring an existing non-ASCENT project up to ASCENT standards |
| `bootstrap` | Slug is `ascent-starter` and meta is a placeholder | Slug substitution after `gh repo create --template` |

The canonical mode-detection schema is in ADR-003. The phase-protocol contract that governs how modes interact with phase gates is in [references/PHASE-PROTOCOL.md](references/PHASE-PROTOCOL.md).

## The nine roles

The skill routes intent across nine non-overlapping roles. Each owns a slice of the project lifecycle.

| Role | Owns |
|---|---|
| delivery-lead | Phase plans, requirements decomposition, risk register, dependencies, gate criteria, status synthesis |
| architect | Skeleton, ADRs, container topology, framework docs, Make framework, observability contract |
| ui-ux-designer | Design system, theming, page layouts, visual specs, interaction patterns, accessibility-as-design |
| developer | Backend implementation, frontend implementation, agent task modules, integration patterns |
| data-engineer | Schema design, indexing, query optimization, migration safety, data quality |
| ai-engineer | Prompt engineering, eval harnesses, model abstraction, agentic patterns, safety guardrails |
| tester | All test disciplines, quality gates, NFR catalog, traceability, validation |
| devops | Infra, CI/CD, AWS, distribution, observability collection, release engineering |
| cybersecurity | Security baseline, threat modeling, secrets, hardening, compliance |

Per-role detail lives in `references/role-<name>.md` modules.

## Reference modules

The skill loads reference modules on demand based on the engaged role(s) and the task at hand. The full module set:

**Roles (9):**

- [references/role-delivery-lead.md](references/role-delivery-lead.md)
- [references/role-architect.md](references/role-architect.md)
- [references/role-ui-ux-designer.md](references/role-ui-ux-designer.md)
- [references/role-developer.md](references/role-developer.md)
- [references/role-data-engineer.md](references/role-data-engineer.md)
- [references/role-ai-engineer.md](references/role-ai-engineer.md)
- [references/role-tester.md](references/role-tester.md)
- [references/role-devops.md](references/role-devops.md)
- [references/role-cybersecurity.md](references/role-cybersecurity.md)

**Protocols and conventions (6):**

- [references/ASCENT-INVARIANTS.md](references/ASCENT-INVARIANTS.md)
- [references/MAKE-NAMING.md](references/MAKE-NAMING.md)
- [references/SLUG-CONVENTIONS.md](references/SLUG-CONVENTIONS.md)
- [references/PHASE-PROTOCOL.md](references/PHASE-PROTOCOL.md)
- [references/ENV-DISCIPLINE.md](references/ENV-DISCIPLINE.md)
- [references/ADR-TEMPLATE.md](references/ADR-TEMPLATE.md)

**Practices and style (6):**

- [references/feature-lifecycle.md](references/feature-lifecycle.md)
- [references/observability-contract.md](references/observability-contract.md)
- [references/writing-style.md](references/writing-style.md)
- [references/doc-architecture.md](references/doc-architecture.md)
- [references/audience-mapping.md](references/audience-mapping.md)
- [references/external-services-integration.md](references/external-services-integration.md)

Once each module exists, the inline-code references above are converted to markdown links via surgical edits in the corresponding chunk's PR.

## Routing logic

Per ADR-001, the skill routes user intent through three stages. Each is deterministic — given the same input directory and prompt, the same role(s) and modules load.

### Stage 1 — Mode detection

The skill examines `.ascent-meta.json` per ADR-003. The Operating modes table above maps the file's state to the active mode (scaffold, enhance, migrate, bootstrap). Mode determines *what kind* of work; Stage 2 determines *who owns* it.

### Stage 2 — Role inference

Three signals govern which role(s) engage:

**A. Explicit invocation.** The user names a role: "as the architect role, ..." or "the developer should handle this." That role engages; no inference needed.

**B. Implicit inference from intent shape.** The user describes a task; the skill matches the task shape against the roles' "When this role engages" tables. The pattern table below is representative, not exhaustive.

| Intent shape | Engaged role(s) | Lifecycle stage |
|---|---|---|
| "scaffold / create a new project" | architect (primary), delivery-lead | Greenfield |
| "add a new endpoint / feature / capability" | delivery-lead, architect, developer, tester (+ specialists per area) | Full lifecycle |
| "write an ADR" | architect | n/a |
| "set up / update phase plan" | delivery-lead | n/a |
| "investigate slow / broken X" | developer (primary), specialists per investigation outcome, tester (regression) | 3–4 |
| "audit / check compliance" | delivery-lead (status), cybersecurity (security baseline) | n/a |
| "rotate secrets / handle credentials" | cybersecurity, devops | n/a |
| "deploy / release" | devops, tester (gate) | 5–6 |
| "improve accessibility / UX" | ui-ux-designer, developer | 2–3 |
| "optimize query / migration" | data-engineer, developer | 2–3 |
| "fix a bug" | developer (primary), tester (regression) | 3–4 |
| "what role handles X?" | answer with the role; load that role's module | n/a (meta-query) |

**C. Multi-role expansion.** When the intent matches `feature-lifecycle.md`'s Stage 2 specialist triggers (schema change, AI change, UI surface change, infra change, auth/secrets/egress change), the corresponding specialist roles engage *alongside* the primary lifecycle roles.

**The minimum-sufficient principle.** Engage the smallest set of roles that fully covers the task. A typo fix is not a "feature" — it's a developer touch. Bigger isn't better; over-engagement produces theater, not work. When the intent is ambiguous, **ask a clarifying question** rather than expand to every potentially-relevant role. Example 13 below shows this in practice.

### Stage 3 — Reference-module loading

The skill loads modules lazily, on consultation:

**Always loaded** (skill-level, every invocation):

- `ASCENT-INVARIANTS.md` — the 14 invariants every operation respects

**Per-mode loaded**:

- scaffold / migrate: `SLUG-CONVENTIONS.md`, `MAKE-NAMING.md`, `PHASE-PROTOCOL.md`, `ENV-DISCIPLINE.md`
- enhance: only what the engaged role(s) need
- bootstrap: `SLUG-CONVENTIONS.md`

**Per-role loaded**:

- Each engaged role's `role-*.md` module
- Any practice or protocol module the role's Cross-references section names
- Any module the role's header cites (if not already loaded)

Modules are consulted, not pre-emptively pulled. Claude's context budget is finite; loading discipline matters.

### Worked walk-through

User prompt: *"Add a Stripe payment endpoint to my ASCENT project."*

**Stage 1 — Mode detection.** `.ascent-meta.json` is present with a real slug → mode is **enhance**.

**Stage 2 — Role inference.**

- "endpoint" matches the "add a new endpoint" intent → delivery-lead, architect, developer, tester engage
- "Stripe" matches the external-service-integration trigger from `feature-lifecycle.md` → devops engages at Stage 5 (production secret config)
- "payment" elevates cybersecurity engagement (PCI implications, not just secret handling)

Five roles engage at Stage 2 design: delivery-lead, architect, developer, tester, cybersecurity. devops engages at Stage 5.

**Stage 3 — Reference-module loading.**

- Always loaded: `ASCENT-INVARIANTS.md`
- Per-mode (enhance): only what the engaged roles need
- Per-role: `role-delivery-lead.md`, `role-architect.md`, `role-developer.md`, `role-tester.md`, `role-cybersecurity.md`
- Cross-referenced from role-developer.md: `external-services-integration.md`, `observability-contract.md`
- Cross-referenced from role-cybersecurity.md: `ENV-DISCIPLINE.md`

Nine reference modules consulted across the engagement.

The skill is now ready to design and implement the Stripe integration, with each engaged role's discipline applied at the right stage.

## Examples

Thirteen representative prompts demonstrating the routing logic in action. Each shows the detected mode, the engaged role(s), and brief reasoning. The set spans the routing surface: greenfield, enhance, migrate, bootstrap; explicit and implicit invocation; single-role and multi-role; meta-query; and ambiguity-handling.

### Example 1 — Greenfield scaffold

> "Scaffold a new ASCENT project called lawn-care-app."

**Mode:** scaffold · **Roles:** architect, delivery-lead

No `.ascent-meta.json` present → scaffold. The greenfield routing pattern engages architect (skeleton, ADRs, Make framework, container topology) and delivery-lead (initial PHASE-PLAN). Other roles wait until features land.

### Example 2 — Authenticated endpoint

> "Add a JWT-based authentication endpoint to my API."

**Mode:** enhance · **Roles:** delivery-lead, architect, developer, tester, cybersecurity

A new endpoint = feature lifecycle. "Authentication" triggers cybersecurity engagement at Stage 2 design and Stage 4 validation per `feature-lifecycle.md`'s auth/secrets/egress trigger.

### Example 3 — Standalone ADR

> "Write an ADR for our choice of Postgres over MySQL."

**Mode:** enhance · **Roles:** architect

Explicit invocation: "ADR" maps to architect, the role that owns ADRs. No other role engages — this is a standalone decision-recording task, not a feature implementation.

### Example 4 — Phase planning

> "Set up the phase plan for our next sprint."

**Mode:** enhance · **Roles:** delivery-lead

Explicit invocation by intent: phase planning is delivery-lead's owned territory per `PHASE-PROTOCOL.md`. No specialists needed unless the prompt elaborates with concrete features.

### Example 5 — Investigation

> "Our login response is slow — investigate."

**Mode:** enhance · **Roles:** developer (primary), then data-engineer or devops (conditional), tester (regression)

Investigation starts with developer. Specialists pair in based on what surfaces: slow query → data-engineer; network or infra latency → devops. The tester engages after the fix to ensure regression protection. Engagement expands as the investigation narrows.

### Example 6 — External service integration

> "We need to add Stripe payment integration."

**Mode:** enhance · **Roles:** delivery-lead, architect, developer, tester, cybersecurity, devops

The full routing surface — six roles. External service triggers `external-services-integration.md`'s pattern (wrapper, retry, observability); "payment" elevates cybersecurity for PCI implications; devops handles production secret config and Stage 5 deploy. The architect engages cybersecurity *at Stage 2 design*, not at Stage 4 retrofit.

### Example 7 — AI eval regression

> "Our AI eval scores dropped after the prompt change — diagnose."

**Mode:** enhance · **Roles:** ai-engineer (primary), tester

Prompt and eval changes are ai-engineer's specialty per `role-ai-engineer.md`. The tester pairs in for eval-discipline rigor (acceptance-criteria-to-eval traceability). The developer engages only if the regression traces to wrapper or orchestration code rather than the prompt itself.

### Example 8 — Migrate non-ASCENT project

> "Migrate this existing Node project to ASCENT."

**Mode:** migrate · **Roles:** architect, delivery-lead

Migration is a sequence of additive enhancements that bring an existing project up to ASCENT standards. The architect designs the migration plan as a phased sequence; delivery-lead schedules it. Implementing roles engage feature-by-feature once the plan exists.

### Example 9 — Accessibility improvement

> "Make the dashboard accessible to screen readers."

**Mode:** enhance · **Roles:** ui-ux-designer, developer

Accessibility lives at design time per `role-ui-ux-designer.md`'s accessibility-as-design rule, not at Stage 4 retrofit. The UI/UX designer produces the spec (keyboard navigation, screen-reader semantics, focus management); the developer implements it. The tester verifies acceptance after.

### Example 10 — Credential rotation

> "Rotate our Anthropic API key."

**Mode:** enhance · **Roles:** cybersecurity, devops

Secret rotation cadence is cybersecurity's discipline; the rotation operation runs through devops (who operates the secret store and deploy pipeline). The developer does not engage — application code reads the secret from environment, which is already rotation-ready.

### Example 11 — Bootstrap from starter

> "Bootstrap this project after cloning the starter."

**Mode:** bootstrap · **Roles:** architect

Slug is `ascent-starter` and `.ascent-meta.json` is the template placeholder → bootstrap. The architect arbitrates the slug substitution and offers the interview if the user wants customization beyond defaults.

### Example 12 — Meta-query

> "What role handles container topology?"

**Mode:** any (meta-query) · **Roles:** architect (the answer)

A "what role handles X?" query is a routing question, not a work request. The skill answers with the role name (architect) and loads that role's module so a follow-up question can be answered with role-grounded detail.

### Example 13 — Ambiguous intent

> "Make our API faster."

**Mode:** enhance · **Roles:** *(clarification required before routing)*

"Faster" is ambiguous: latency reduction (developer + data-engineer), throughput increase (devops), or both. Multi-role expansion is the wrong default — it produces theater across five roles when one or two are actually needed. The skill asks: *"Faster meaning lower latency, higher throughput, or both? And on which routes?"* Routing resumes once the answer narrows the scope. The minimum-sufficient principle from Stage 2 governs: ambiguity resolves through clarification, not through expansion.

## When this skill does not engage

For prompts unrelated to ASCENT, the skill stays out and the user's general Claude conversation continues. Three patterns where the skill should not engage:

- **Generic programming questions** — "Write a Python function to sort a list."
- **Non-ASCENT framework questions** — "How do I configure webpack?"
- **General knowledge** — "Explain the CAP theorem."

The trigger surface is the framework, its conventions, its nine roles, and the projects it scaffolds. Outside that, the skill defers.
