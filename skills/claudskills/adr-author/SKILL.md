---
name: adr-author
description: Architecture Decision Records — context, decision, consequences, supersession trail.
team: docs
input: Decision
output: ADR
---

# adr-author

## ADR shape

```markdown
# ADR-NNN: <decision title>

**Status:** proposed | accepted | superseded by ADR-MMM
**Date:** YYYY-MM-DD
**Deciders:** <names>

## Context
<one-paragraph background, with links>

## Decision
<the chosen path, in a single sentence>

## Alternatives considered
- Option A — pros, cons
- Option B — pros, cons

## Consequences
- Positive: <what gets easier>
- Negative: <what gets harder / what we give up>
- Neutral: <noteworthy non-consequences>

## Compliance / verification
<how we'll know we're following this>
```

## Operating principles

1. **One decision per ADR.** Bundling causes loss of granularity.
2. **Status is current.** Superseded ADRs link forward; new ADRs link back.
3. **Alternatives must be plausible.** Strawmen waste reviewer time.
4. **Consequences include the negative.** "We trade flexibility for simplicity" beats only-positives.
5. **Numbered + immutable.** Edit only for typos; new ADR for new decisions.
6. **Compliance is checkable,** not aspirational. Where does the linter run?

## Hand-off contract

`decision-doc-writer` produces broader decision docs; ADRs are the architecture-shaped subset. `docs-architect` integrates ADR index into docs site.
