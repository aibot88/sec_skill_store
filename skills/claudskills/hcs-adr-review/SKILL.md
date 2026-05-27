---
name: hcs-adr-review
description: Review an Architecture Decision Record (ADR) in this repo for boundary discipline, charter compliance, and decision-ledger consistency.
allowed-tools: Read, Grep, Glob
---

# Skill: Review an ADR

Use when a PR adds or amends a file under `docs/host-capability-substrate/adr/`, or when a human asks "review ADR N".

## Inputs

- Path to the ADR being reviewed (e.g., `docs/host-capability-substrate/adr/0005-process-model-launchd.md`)
- The PR branch or commit range containing the change

## Procedure

1. Read the implementation charter (`docs/host-capability-substrate/implementation-charter.md`). Check current version.
2. Read the ADR under review.
3. Read `DECISIONS.md`. Check whether the ADR's decision is already in the Accepted ledger, Pending, or Reversed.
4. Read neighboring ADRs in `docs/host-capability-substrate/adr/` for any that depend on or conflict with this one.
5. Check the ADR's "Options Considered" section contains at least two real alternatives with explicit pros/cons.
6. Check the "Consequences" section lists both accepts and rejects, and notes any future-amendment paths.
7. Check the "References" section cites at least the charter, the research plan, and any applicable external docs (MCP spec, Claude Code docs, Codex docs, etc.).
8. Confirm the ADR's status is appropriate (`proposed`, `accepted`, `superseded`) and that the date is ISO-8601.

## Checks

- Does the decision respect the four-ring architecture?
- Does the decision respect the 15 charter invariants?
- Does the decision stay inside the substrate's owns list (not domain-server territory)?
- Is the decision narrow enough to be implementable in one PR, or does it imply multiple PRs?
- Does the ADR cite the charter version it was written against?
- If the ADR changes a previously-accepted decision, is there a corresponding entry in `DECISIONS.md` Reversed?

## Output format

Return:

1. **Blocking issues** (must fix before ADR accepted): missing options, missing consequences, charter invariant conflict, stale charter version citation.
2. **Non-blocking concerns**: clarity, wording, scope ambiguity.
3. **Suggested follow-ups**: additional ADRs the decision implies, regression traps to add, policy updates needed in system-config.
4. **Charter compliance statement**: explicit confirmation.

## Escalation

If the ADR involves schema/ontology, request `hcs-ontology-reviewer`.
If it involves policy, request `hcs-policy-reviewer`.
If it involves security-sensitive changes, request `hcs-security-reviewer`.

## Reference

- Charter: `docs/host-capability-substrate/implementation-charter.md`
- Decision ledger: `DECISIONS.md`
- ADR template: `docs/host-capability-substrate/adr/0000-template.md`
