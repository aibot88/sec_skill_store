---
name: adr-compliance
description: Use when deeply validating an ADR's format, approval chain, linkage to standards, or deciding the correct ADR status
version: 1.0.0
owner: platform-governance
tier: full
source: .enterprise/governance/agent-skills/adr-compliance/SKILL.md
quick: .enterprise/governance/agent-skills/adr-compliance/SKILL-QUICK.md
portable: true
license: Apache-2.0
---

# ADR Compliance

## When to use
Use this skill when:
- creating a new ADR
- reviewing a submitted ADR for approval
- validating that a change requiring an ADR has one
- checking that an ADR correctly references affected standards
- generating an ADR draft on behalf of a human author

---

## 1. When an ADR is Required

An ADR MUST be created for:

- AD-01: Architectural changes (new patterns, new boundaries, structural refactoring)
- AD-02: Technology or framework additions (new dependency, new platform, new language)
- AD-03: Breaking changes to APIs, events, or data contracts
- AD-04: Security posture changes (auth method, encryption change, new exposure)
- AD-05: Deviation from any active standard or policy
- AD-06: Data migration or schema evolution affecting production data
- AD-07: Performance-impacting changes (new caching strategy, query changes on hot paths)
- AD-08: Governance or standards modifications

If uncertain whether an ADR is needed: create one. The cost is low; the cost of undocumented decisions is high.

---

## 2. ADR File Naming & Location

- AD-09: ADRs MUST be stored under `.specs/decisions/`.
- AD-10: File name MUST follow: `ADR-XXXX-<kebab-case-title>.md`
  - Example: `ADR-0012-adopt-event-sourcing-for-audit-trail.md`
- AD-11: XXXX is a zero-padded sequential number.
- AD-12: Numbers MUST NOT be reused, even if an ADR is deprecated or superseded.

---

## 3. Required Sections & Content

Every ADR MUST contain all of the following sections:

### 3.1 Header
```
# ADR-XXXX — [Short Title]
**Status:** Draft | Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date:** YYYY-MM-DD
**Authors:** [name(s)]
**Approved by:** [name(s)] (required before Accepted status)
```

### 3.2 Context
- AD-13: Describe the situation, problem, or requirement that necessitates a decision.
- AD-14: Reference the relevant standards, constraints, or business drivers.
- AD-15: Context MUST be factual — not the decision itself.

### 3.3 Decision
- AD-16: State the decision clearly and unambiguously.
- AD-17: Use active voice: "We will adopt...", "The system will use...", "This service MUST...".
- AD-18: The decision MUST be actionable — agents and engineers must be able to implement from it.

### 3.4 Alternatives Considered
- AD-19: At least one alternative MUST be documented.
- AD-20: Each alternative MUST include: description, pros, cons, and reason it was not chosen.
- AD-21: "Do nothing" is always a valid alternative and MUST be evaluated.

### 3.5 Consequences
- AD-22: List positive consequences (benefits, improvements).
- AD-23: List negative consequences (trade-offs, risks, debt introduced).
- AD-24: Mitigation plan for identified risks MUST be included.
- AD-25: Impact on existing components, services, or standards MUST be described.

### 3.6 Affected Standards
- AD-26: List every spec, standard, or policy this ADR modifies, deviates from, or supersedes.
- AD-27: Include the specific section or rule ID that is affected.
- AD-28: If this ADR introduces a new exception, state the exception scope and expiry date.

---

## 4. Status Lifecycle

```
Draft → Proposed → Accepted
                  ↘ Deprecated
                  ↘ Superseded by ADR-XXXX
```

- AD-29: `Draft` — work in progress, not yet reviewable.
- AD-30: `Proposed` — ready for review; must not be implemented until `Accepted`.
- AD-31: `Accepted` — approved by authorized owner; implementation may proceed.
- AD-32: `Deprecated` — decision is no longer in effect; superseding context must be explained.
- AD-33: `Superseded` — replaced by a newer ADR; reference to successor MUST be included.
- AD-34: Implementation MUST NOT begin until status is `Accepted`.

---

## 5. Approval Requirements

- AD-35: ADRs affecting architecture require approval from: Platform Architecture Owner or Staff Engineer.
- AD-36: ADRs affecting security posture require approval from: Security Owner.
- AD-37: ADRs affecting governance or standards require approval from: Engineering Leadership.
- AD-38: ADRs for local service deviations (no cross-team impact) require approval from: Tech Lead of the affected team.
- AD-39: Self-approval is forbidden — the author MUST NOT be the sole approver.

---

## 6. ADR Immutability Rules

- AD-40: Accepted ADRs MUST NOT be edited to change the decision retroactively.
- AD-41: If a decision changes, a new ADR MUST be created with `Supersedes: ADR-XXXX`.
- AD-42: Corrections to typos or formatting are allowed without creating a new ADR.
- AD-43: Context updates that do not change the decision are allowed with a changelog note in the ADR.

---

## 7. ADR Draft Template

When generating an ADR draft, use this structure:

```markdown
# ADR-XXXX — [Short Title]
**Status:** Draft
**Date:** YYYY-MM-DD
**Authors:** [name]
**Approved by:** —

---

## Context
[Describe the problem or situation requiring a decision.]

## Decision
[State clearly what has been decided.]

## Alternatives Considered

### Option A — [Name]
- **Description:** ...
- **Pros:** ...
- **Cons:** ...
- **Rejected because:** ...

### Option B — Do Nothing
- **Description:** Maintain current approach.
- **Pros:** No disruption.
- **Cons:** [Why this is insufficient.]
- **Rejected because:** ...

## Consequences

### Positive
- ...

### Negative / Trade-offs
- ...

### Risks & Mitigations
- **Risk:** ...  **Mitigation:** ...

## Affected Standards
- [Standard name] — [Section/rule affected]
```

---

## Examples

✅ Good: ADR-0007 with all sections, alternatives, explicit risks, approved by Platform Architect.
✅ Good: ADR that supersedes ADR-0003 and clearly explains why the old decision is no longer valid.

❌ Bad: ADR with only Context and Decision sections — missing Alternatives and Consequences.
❌ Bad: ADR in `Accepted` status with no approver listed.
❌ Bad: Implementation proceeding while ADR is still in `Draft` status.


## Quick Mode

For low-context activation, load `.enterprise/governance/agent-skills/adr-compliance/SKILL-QUICK.md` or `QUICK.md` first. Load this full skill for deep analysis, violation fixing, or formal review gates.

