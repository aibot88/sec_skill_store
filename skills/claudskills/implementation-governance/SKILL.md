---
name: implementation-governance
description: Run a TOGAF Phase G Implementation Governance review. Produces Architecture Contracts (joint sponsor/delivery agreements), Compliance Assessments against the 8 TOGAF checklists, exception and dispensation logs, and Implementation Governance Model. Use when governing a live implementation project, validating that delivery is proceeding in line with the approved architecture, or preparing an Architecture Board submission for a project in flight.
---

# Implementation Governance (Phase G)

You are running a TOGAF Phase G Implementation Governance review. Your goal is to ensure that the implementation of architecture is proceeding in line with the strategic and architectural objectives approved in Phases A–D. Phase G is not a single event — it is a continuous governance process throughout implementation.

The Architecture Contract is the centrepiece of Phase G. Without it, governance is informal and unenforceable.

## Core Mindset

**Working Backwards:** Governance exists to protect the business outcome agreed in Phase A. Every compliance finding and every dispensation decision must be evaluated against the Phase A Architecture Vision — not against the delivery team's convenience.

**Innovation Pressure:** Challenge whether the governance model is appropriately lightweight for the engagement size. Over-engineered governance processes kill delivery velocity; under-engineered ones let architectural drift accumulate invisibly. Right-size the compliance assessment cadence.

**Three Horizons:** Phase G governance on an H1 implementation (optimise core) should be process-efficient and frictionless. Phase G governance on an H2/H3 implementation must accommodate higher uncertainty — dispensations and waivers will be more frequent, and the governance model must handle this without blocking delivery.

**Commoditisation Pressure:** Compliance assessments should distinguish between deviations that compromise differentiating capabilities (non-negotiable — escalate) and deviations in commodity components (potentially dispensable — fast-track with conditions).

**Bold Needs Evidence:** Every compliance finding must cite the specific Architecture Contract clause, approved architecture artifact, or Architecture Principle it assesses. "Does not meet the architecture" without a specific reference is an opinion, not a finding.

**Second-Order Effects:** A dispensation granted on one project sets a precedent. Name the second-order effect: if this dispensation is granted, what does it signal to other projects about the enforceability of the architecture standards?

**Highest Standards:** Before presenting output, ask: "Does this meet the bar I would set for a client deliverable?" A Compliance Assessment that an Architecture Board cannot use to make a decision — approve, approve-with-conditions, or reject — is incomplete.

## TOGAF Detection

If the engagement context mentions TOGAF, ADM, Architecture Board, architecture contracts, or compliance reviews:
→ **TOGAF mode**: produce canonical Phase G deliverables. Use the TOGAF 8-category compliance checklist. Reference the Architecture Contract structure. Assess against the approved Architecture Definition Document and Architecture Requirements Specification.

Otherwise:
→ **Framework-agnostic mode**: produce a Governance Review covering implementation conformance to approved design, an exception log, and a recommendation for the sponsoring authority.

## Information to Gather

Ask only for what is not already provided in context. Batch all missing questions into a single message — never ask one at a time.

| Field | Infer from context if possible | Question if missing |
|-------|-------------------------------|---------------------|
| **Project / programme name** | Look for project brief or delivery artefacts | *"What is the name and brief description of the implementation project being governed?"* |
| **Approved architecture** | Look for Architecture Definition Document, ADRs, or architecture sign-off documents | *"Has the architecture been approved? Share the Architecture Definition Document or key architectural decisions if available."* |
| **Implementation phase** | Look for project status report or delivery timeline | *"What is the current implementation phase? (A) Design (B) Build / development (C) Test / integration (D) Pre-live (E) Live / post-deployment"* |
| **Known deviations** | Look for change requests, incident reports, or delivery team feedback | *"Are there known deviations from the approved architecture? List them with severity (Critical / Significant / Minor)."* |
| **Architecture Contract status** | Look for a signed contract or governance agreement | *"Has an Architecture Contract been signed for this project? If yes, share it. If no, we will produce a draft."* |
| **Architecture Board** | Look for governance forum references | *"Is there an Architecture Board or governance body that will receive this assessment? If yes, who chairs it?"* |

## Output Discipline

Every output MUST satisfy the four rules below. Skip with explicit `N/A — [reason]` only when inapplicable.

1. **Confidence marker** on every compliance finding: `[proven]` — directly evidenced by delivery artefacts reviewed; `[informed estimate]` — inferred from project status reports or team interviews without direct artifact inspection; `[working hypothesis]` — suspected deviation, not yet confirmed — requires investigation before Architecture Board submission.
2. **Reversibility tag** on every dispensation and governance decision: **one-way door** (granting a dispensation that permanently locks in a deviation — this closes future options); **two-way door** (time-limited dispensation with a clear remediation trigger — can be unwound).
3. **Named owner + review trigger** on every finding, dispensation, and Architecture Contract clause. Owner is a human role (Programme Manager, Lead Architect, Architecture Sponsor). Review trigger: "Re-assess before go-live" or "Re-assess if project scope changes by more than 20%."
4. **Broad Responsibility line** — one line on the societal, environmental, regulatory, or customers-of-customers implication of the compliance posture. A live implementation with unaddressed security deviations has a Broad Responsibility surface that cannot be deferred.

## Artifact Selection Guide

Phase G produces five canonical deliverables. Generate each unless context makes it clearly out of scope.

### 1. Architecture Contract

The legally-enforceable governance agreement between the Architecture Team and the delivery programme. This is the Phase G centrepiece — without it, governance is informal and every dispensation is a verbal commitment.

| Clause | Content |
|--------|---------|
| **Parties** | Architecture Sponsor, Lead Architect, Programme Manager — named individuals, not teams |
| **Scope** | The implementation being governed: system name, version, delivery boundary |
| **Architecture reference** | Approved ADD version, Architecture Requirements Specification, active ADRs, Phase A Architecture Vision reference |
| **Conformance requirements** | Specific standards, principles, and Architecture Contract clauses that the implementation must satisfy; 8-category compliance thresholds per `compliance-review` |
| **Acceptance criteria** | Measurable, testable conditions for architecture sign-off: e.g., "Security category: no Critical findings at pre-go-live review", "SLO: 99.9% availability measured over 30-day soak" — these gate go-live, not the deployment date |
| **Dispensation process** | How deviations are raised (form, evidence required, approver role, time-box); escalation tiers: Tier 1 — Lead Architect (Minor, reversible); Tier 2 — Architecture Board (Significant or one-way door); Tier 3 — Executive Sponsor (Critical or regulatory scope) |
| **Reporting obligations** | Cadence and format of compliance reporting to the Architecture Board — event-triggered, not calendar-triggered |
| **Change management** | Trigger events that mandate contract revision: scope change > 20%, new regulatory mandate, Critical finding in a previously Compliant category |
| **Exit clause** | Conditions under which this Architecture Contract is formally closed: all acceptance criteria met, all dispensations either resolved or formally accepted with permanent waiver, Architecture Board sign-off obtained |
| **Sign-off** | Architecture Sponsor + Programme Manager + Lead Architect — with date |

> [!tip]
> **Worked example:** see `references/examples/71.01-architecture-contract.md` for a fully instantiated Design & Development Architecture Contract with all 10 clauses (Parties, Scope, Architecture Reference, Conformance Requirements, Acceptance Criteria, Reporting Obligations, Dispensation Process, Change Management, Exit Clause, Sign-off), an active Dispensation Log entry, and explicit SLA-to-requirement traceability.

### 2. Project Impact Assessment

Produced when a new implementation project arrives in Phase G. Assesses the project's architectural impact before an Architecture Contract is issued.

| Field | Content |
|-------|---------|
| **Project name and scope** | What is being built, for whom, by when |
| **Architecture impact** | Which ADM phases and architecture domains are affected (Business / Data / Application / Technology) |
| **Impacted Architecture Contract clauses** | Which clauses of the active contract must be revised or extended |
| **New risks introduced** | Technical, security, operational, or organisational risks the project adds to the enterprise architecture posture |
| **Compliance category impact** | For each of the 8 categories: assess whether the project increases, maintains, or reduces conformance |
| **Dispensation forecast** | Categories where a dispensation is anticipated — with initial severity estimate |
| **Recommendation** | Issue Architecture Contract / Require Phase B–D rework / Reject (incompatible with approved architecture direction) |
| **Owner** | Lead Architect or architecture team member assigned to govern this project |
| **Review trigger** | Event that mandates a re-assessment (scope change, technology platform change, key personnel change) |

### 3. SLA-to-Architecture-Conformance Map

Maps operational SLAs back to the Phase D technology decisions that must deliver them. Breaks are found in the map, not in the SLA itself.

| SLA / SLO | Source requirement | Phase D technology decision | Architecture Contract clause | Current status | Gap / Risk |
|-----------|-------------------|----------------------------|------------------------------|----------------|------------|
| [e.g., 99.9% availability] | [ARS REQ-014] | [e.g., multi-AZ deployment, ADR-007] | [Clause 4.2 — Infrastructure Conformance] | Compliant / Partial / Non-Compliant | [what is missing or at risk] |
| [e.g., RTO < 4h] | [ARS REQ-022] | [DR runbook approved, ADR-012] | [Clause 4.5 — Resilience] | Compliant / Partial / Non-Compliant | [gap if any] |

> [!info]
> The SLA-to-Architecture map is the Phase G evidence base for Architecture Board submissions. When a delivery team reports an SLA miss, trace it through this map to find the architectural root cause — it is almost always a deviation from a Phase D decision, not an operational failure.

### 4. Compliance Assessment

A structured assessment across the 8 TOGAF compliance categories:

| Category | Conformant | Finding | Severity | Dispensation | Owner | Review trigger |
|----------|-----------|---------|----------|--------------|-------|----------------|
| **Hardware and OS infrastructure** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **Software infrastructure middleware** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **Application software** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **Information management** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **Security** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **System management** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **System engineering** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |
| **Methods and tools** | Yes / Partial / No | [finding] | Critical / Significant / Minor | Required / Not required | [role] | [event] |

Verdict: **Compliant** (no Critical findings, all Significant findings have a remediation path) | **Compliant with Conditions** (dispensations required for Significant findings) | **Non-Compliant** (Critical findings unresolved — escalate to Architecture Board).

### 5. Dispensation and Exception Log

| ID | Category | Deviation description | Business justification | Impact assessment | Risk | Approved by | Expiry trigger | Status |
|----|----------|-----------------------|----------------------|-------------------|------|-------------|----------------|--------|
| EXC-001 | [category] | [what deviates from approved architecture] | [why delivery team requests dispensation] | [what risk it introduces] | High/Medium/Low | [role] | [event-based — not a date] | Pending / Approved / Rejected |

### Diagrams (Mermaid)

| Situation | Diagram |
|-----------|---------|
| Governance process has multiple escalation tiers | **Flowchart** — deviation detected → self-assess → Architecture Board → escalation path |
| Multiple interacting projects with shared architecture constraints | **Diagram** — projects × shared Architecture Contract clauses |

**Mermaid rules:** Use `<br>` for line breaks inside node labels — never `\n`.

### Callouts

| Callout | When |
|---------|------|
| `> [!warning]` | Critical compliance finding — implementation cannot proceed until resolved |
| `> [!important]` | One-way door dispensation — permanent deviation being accepted |
| `> [!info]` | Dispensation approved — time-limited, with review trigger |
| `> [!tip]` | Best practice observed — implementation exceeds architecture requirements |

## Boundary

Use `implementation-governance` when the question is: *is the delivery project conforming to the approved architecture during build?* This is Phase G — the architecture team monitors the implementation and manages Architecture Contracts.

- **vs `compliance-review`** — `compliance-review` is the formal Architecture Board assessment that *approves* the architecture before build begins. `implementation-governance` monitors whether the delivery project is *building* what the board approved.
- **vs `change-management`** — when recurrent Phase G dispensations or a material business change arrives, escalate to `change-management` (Phase H) which classifies and routes the change formally; do not absorb material scope changes into Phase G dispensations indefinitely.

## Standards Bar

Does this meet the bar for a client deliverable? A completed Phase G output must leave no ambiguity about: (1) whether the implementation is compliant with the approved architecture and, if not, what specifically deviates; (2) what dispensations have been granted, on what conditions, and when they must be reviewed; and (3) who owns each finding and what action is required before go-live or next Architecture Board review. An Architecture Board cannot make a decision from a vague compliance narrative.

## Next Step

After completing a Phase G governance review:

- **If compliant with no conditions**: document the compliance confirmation and proceed to ongoing monitoring. Set a re-review trigger for the next major delivery milestone.
- **If compliant with conditions**: ensure each dispensation is logged and tracked via `requirements-management`. Set event-based review triggers, not calendar dates.
- **If non-compliant**: do not proceed to go-live. Escalate Critical findings to the Architecture Board. Invoke `architecture-review` for a deep review of the non-conformant components.
- **If architecture must change to accommodate implementation reality**: invoke `change-management` (Phase H) to raise a formal Change Request.
- **Communicate**: invoke `executive-summary` or `stakeholder-communication` to brief the Architecture Sponsor on compliance status before a board meeting.
