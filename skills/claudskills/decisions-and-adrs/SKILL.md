---
name: decisions-and-adrs
description: "Use this skill whenever you create, write, modify, or statue an entry under `.decisions/` or `.adrs/`, or when you need to know the difference between a tactical DECISION and a strategic ADR, the two-zone frontmatter format of DECISION-NNN-*.md (zone author + zone review with `revisit`/`reviewed_by`/`reviewed_at`/`outcome` fields), the R2 strict rules under which green is allowed to author a tactical DECISION (scope=tactical, revisit=true at creation, necessary to unblock current task, DECISION-NNN referenced in code or commit message), or the R6 three-level defence around the `Authored-By:` commit trailer (pre-commit format, CI git-blame ↔ trailer cross-check, reviewer pass DoD sanity check). Also covers the architect's three statuing outcomes (confirm / reformulate / supersede) for tactical DECISIONS surfaced in RETRO.md `decisions_to_statue:` from the previous sprint, and the strategic ADR format. Loaded only by `architect` (writes strategic, statues tactical, both ADRs and DECISIONS), `green` (writes tactical DECISIONS under R2), and `sprint-planner` (lists pending tactical DECISIONS in `decisions_to_statue:` for next sprint's Wave 1 task). Other agents (PM, red, e2e-tester, reviewer, bug-detective) can read DECISION / ADR files without this skill — they just need the `## Relevant decisions` section of FEATURE.md to know which apply to a feature."
---

# Decisions and ADRs

The decision log mechanism for the agile-team-v2 workflow. Two distinct stores — `.decisions/` for tactical/strategic decisions with a review lifecycle, `.adrs/` for strategic Architecture Decision Records — plus the `Authored-By:` commit trailer that audits write authority.

This skill is loaded only by the three agents that **write** to these stores: architect, green, sprint-planner. Other agents read DECISION/ADR files freely (they're public artifacts), but they don't need the format details, the R2 strict rules, or the statuing protocol.

---

## The two stores

### `.adrs/` — strategic, multi-feature, project-direction

Architecture Decision Records. Format unchanged from v1. Strategic only — multi-feature impact, invariant changes, contracts that other features will depend on. The architect writes ADRs.

```markdown
# ADR <NNN> — <short title>

Date: <YYYY-MM-DD>
Scope: strategic
Author: architect
Decided: [autonomously | with human input]
Revisit: [true | false]

## Context
## Decision
## Consequences
## Related
- Features: <links>
- Prior ADRs: <links or None>
- Superseded ADRs: <links or None>
```

`Revisit: true` indicates an autonomous decision under uncertainty — picked up at retro for human review.

Tactical decisions go to `.decisions/`, **not** `.adrs/`. Do not mix.

### `.decisions/` — tactical or strategic, with two-zone frontmatter and review lifecycle

The decision log distinct from strategic ADRs. The architect writes strategic DECISIONS directly. Green may write **tactical** DECISIONS during implementation under R2 strict rules (below). The architect **statues** every unstatued tactical DECISION at the start of the next sprint via a Wave 1 task placed by the sprint-planner.

`.decisions/INDEX.md`:

```markdown
| ID            | Scope     | Status     | Title                            | Date       | Author    |
|---------------|-----------|------------|----------------------------------|------------|-----------|
| DECISION-042  | strategic | ACTIVE     | session storage backend          | 2026-04-15 | architect |
| DECISION-051  | tactical  | ACTIVE     | session-id format choice         | 2026-04-27 | green     |
```

`.decisions/DECISION-NNN-<slug>.md` — **two-zone frontmatter**:

```yaml
---
# Zone author — writeable at creation only
id: DECISION-051
date: 2026-04-27
scope: tactical          # tactical | strategic
status: ACTIVE           # ACTIVE | SUPERSEDED
author: green            # architect | green
affects: [internal/auth/session.go]

# Zone review — writeable by architect only, post-creation
review:
  revisit: true          # green sets true at creation; architect may flip false
  reviewed_by: null      # null at creation; "architect" after statuing
  reviewed_at: null
  outcome: null          # null | confirmed | reformulated | superseded
---

# <Title>

## Question
## Decision
## Rationale

## Reformulated by architect
(empty initially; filled at statue time if reformulating)
```

Every commit that creates or modifies anything under `.decisions/` carries the `Authored-By:` trailer (R6).

---

## R2 — Tactical DECISIONS by green

Green may write a tactical DECISION when **all four** hold:

1. `scope: tactical` (never `strategic` — reserved for the architect).
2. `review.revisit: true` at creation (never `false` initially).
3. The decision is **necessary to unblock the current task** — not opportunistic. If green could finish the task without writing the DECISION, the DECISION should not be written. The architect picks up recurring patterns at retro time.
4. The DECISION-NNN is referenced in the code (a `// see DECISION-NNN` comment) or in the commit message body.

Strategic DECISIONS are forbidden for green — they require the architect's authority. If green encounters what feels like a strategic decision in flight, the right move is a dispute (escalation type E in the dispute protocol) so the architect can decide and write the strategic DECISION.

The sprint-planner surfaces each unstatued tactical DECISION in `RETRO.md decisions_to_statue:` at retro processing. The next sprint's plan starts with a Wave 1 task block for the architect to statue every entry. CI rejects a sprint that closes with `review.revisit: true` and `review.reviewed_by: null` on a DECISION older than one sprint window (`check.sh` enforces).

---

## The architect's three statuing outcomes

For each unstatued tactical DECISION, the architect chooses exactly one outcome:

### Confirm

The decision is sound as written.

- `review.outcome: confirmed`
- `review.reviewed_by: architect`
- `review.reviewed_at: <YYYY-MM-DD>`
- `review.revisit: false`
- Body untouched.

### Reformulate

The fundamental decision is right, but the phrasing was incomplete or misleading.

- Same review fields as confirm with `outcome: reformulated`.
- Rewrite `## Decision` and/or `## Rationale` to phrase it correctly.
- Keep the same `id` and `date`.
- Fill `## Reformulated by architect` explaining what was wrong and how it was fixed — this section is the audit trail.

### Supersede

The decision is wrong.

- On the original DECISION:
  - `status: SUPERSEDED`
  - `review.outcome: superseded`
  - `review.reviewed_by: architect`
  - `review.reviewed_at: <YYYY-MM-DD>`
- Create a new `DECISION-MMM-<slug>.md` that explicitly supersedes this one (mention the superseded id in `## Rationale`).
- Update `.decisions/INDEX.md` to reflect both: the original moves to `SUPERSEDED`, the new one is `ACTIVE`.

### Escalation: tactical → strategic

If the decision's scope turned out larger than green originally judged (it affects multiple features or modifies an invariant assumed elsewhere), the architect may **promote** `scope: tactical` → `scope: strategic` during statuing. Note this in `## Reformulated by architect`. Optionally migrate the entry into `.adrs/` if it's genuinely a strategic ADR — in that case write a new ADR-NNN that consumes the DECISION's content, set the original DECISION's `status: SUPERSEDED` with `outcome: superseded`, and reference the new ADR.

---

## R6 — `Authored-By:` trailer and three-level defence

The `Authored-By:` commit trailer audits write authority on `.decisions/` and on the `mechanical:` flag in FEATURE.md frontmatter.

### When the trailer is mandatory

Every commit that:

- Creates, modifies, or deletes any file under `.decisions/`.
- Modifies the `mechanical:` field in any FEATURE.md frontmatter (architect-only field per R1).
- Modifies the `review.reviewed_by` field in any DECISION.

…**must** carry `Authored-By: <agent-id>` in the commit message body.

Values:

- `architect` — for the architect's writes (strategic DECISIONS, statuing tactical DECISIONS, modifying `mechanical:`).
- `green` — for green's tactical DECISIONS only.

### Three-level defence

1. **Pre-commit hook** — verifies YAML zone format on `.decisions/` files. Blocks creation without `revisit: true`. Blocks zone-review modification without all four fields (`revisit`, `reviewed_by`, `reviewed_at`, `outcome`). Blocks zone-author modification post-creation.
2. **CI bloquante (`check.sh --mode ci`)** — `git blame` on `review.reviewed_by` modifications must correspond to a commit with `Authored-By: architect`. Mismatch → CI block. Same for `mechanical:` ↔ `Authored-By: architect`.
3. **Reviewer pass DoD** — sanity check final: iterates over commits in the sprint window touching `.decisions/`, verifies trailer ↔ zone modification consistency. Mismatch → blocking finding.

This is **declarative**, not cryptographic. A buggy agent could write a false trailer. Mitigations: (a) agents follow their skill instructions, (b) `git blame` cross-checks the trailer against the commit identity, (c) the reviewer's pass DoD catches divergences before the sprint closes.

The cost of a forged trailer is high (blocking finding at pass DoD, sprint cannot close). The cost of honesty is zero (just write the right trailer). Incentive is correctly aligned.

Never bypass with `--no-verify`.

---

## Commit examples

### Architect creating a strategic DECISION

```
architect: DECISION-042 session storage backend choice

Feature: auth-login
Task: auth-login-decision-042
Authored-By: architect
```

### Architect statuing a tactical DECISION (confirm)

```
architect: confirm DECISION-051

Feature: auth-login
Task: auth-login-decision-review
Authored-By: architect
```

### Architect reformulating a tactical DECISION

```
architect: reformulate DECISION-051 — clarify session-id format

Feature: auth-login
Task: auth-login-decision-review
Authored-By: architect
```

### Architect superseding a tactical DECISION

```
architect: supersede DECISION-051 with DECISION-067

Feature: auth-login
Task: auth-login-decision-review
Authored-By: architect
```

### Green writing a tactical DECISION during implementation

```
green: implement Authenticate + DECISION-051 (session-id format)

Feature: auth-login
Task: auth-login-T001-green
Authored-By: green
```

### Architect modifying mechanical: in FEATURE.md (during scaffolding)

```
architect: scaffold auth-login

Feature: auth-login
Task: auth-login-scaffold
Authored-By: architect
```

The `mechanical:` field is set as part of the scaffolding commit; the trailer audits the authority.

---

## Anti-patterns

- **Writing a strategic DECISION as green.** Forbidden. Raise a dispute (escalation type E) and let the architect handle it.
- **Writing `revisit: false` at creation as green.** Forbidden. Tactical DECISIONS must be reviewed; `revisit: true` is mandatory at first write.
- **Writing a tactical DECISION opportunistically.** If you can finish the task without the DECISION, don't write one. The architect picks up recurring patterns at retro.
- **Editing an existing DECISION or ADR in place when superseding.** Always write a new entry that supersedes; never overwrite. The audit trail requires the original to remain readable.
- **Skipping the `Authored-By:` trailer with `--no-verify`.** CI catches it.
- **Modifying zone author after creation.** Author fields are immutable. If the metadata is wrong (e.g., wrong `affects:` list), supersede with a corrected DECISION.
- **Mixing tactical and strategic in `.adrs/`.** `.adrs/` is strategic only. Tactical goes to `.decisions/`.
- **Letting tactical DECISIONS pile up unstatued across sprints.** CI rejects a sprint that closes with unstatued tactical DECISIONS older than one sprint window.

---

## Quick reference table

| What                                          | Who writes                       | Trailer                  | Where                |
|-----------------------------------------------|----------------------------------|--------------------------|----------------------|
| Strategic ADR                                 | architect                        | Authored-By: architect (only on .decisions/ + mechanical: changes — ADRs alone don't require it) | `.adrs/NNN-*.md` |
| Strategic DECISION                            | architect                        | Authored-By: architect   | `.decisions/DECISION-NNN-*.md` |
| Tactical DECISION (R2)                        | green                            | Authored-By: green       | `.decisions/DECISION-NNN-*.md` |
| Statuing a tactical DECISION (confirm/reformulate/supersede) | architect | Authored-By: architect   | edits zone review of `.decisions/DECISION-NNN-*.md`; new DECISION on supersede |
| Modifying `mechanical:` flag in FEATURE.md   | architect                        | Authored-By: architect   | `.features/<slug>/FEATURE.md` frontmatter |
