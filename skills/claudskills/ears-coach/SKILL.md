---
name: ears-coach
description: Coach for EARS-formatted requirements. Activate when authoring or reviewing /specs/<cap>/spec.md, .axis/changes/<id>/delta.md, or any requirement statement.
version: 0.0.1
---

# EARS Coach

EARS — Easy Approach to Requirements Syntax (Mavin et al., 2009) — is the requirement style required at AXIS-26 Standard conformance and above (§S2).

## Templates

| Pattern | Template |
|---|---|
| Ubiquitous | `The <system> SHALL <action>.` |
| Event-Driven | `WHEN <trigger>, the <system> SHALL <action>.` |
| State-Driven | `WHILE <state>, the <system> SHALL <action>.` |
| Unwanted-Behavior | `IF <trigger>, THEN the <system> SHALL <action>.` |
| Optional | `WHERE <feature flag>, the <system> SHALL <action>.` |

## Authoring rules

1. One requirement per line. Active voice. The `<system>` is the subject.
2. Each requirement must be testable as a single eval (Functional, Security, Performance, Accessibility, or Drift; §8.3).
3. Pin a stable ID on every ADDED requirement. MODIFIED and REMOVED markers MUST cite the ID (§6.6).

## Anti-patterns to flag

- **Compound requirements** ("…and…"). Split into separate clauses.
- **Implementation language** in a requirement ("uses Redis", "calls Stripe API"). Move to `design.md`.
- **Subjective predicates** ("fast", "secure", "user-friendly"). Replace with measurable thresholds.
- **Future tense** ("will eventually"). EARS uses SHALL.
- **More than three preconditions** stacked in one clause. Split.
- **Missing trigger or state** for Event-Driven or State-Driven clauses.
- **Optional without a feature-flag binding** that exists in the codebase.

## Process

1. Inspect each requirement candidate.
2. Classify it into one of the five EARS patterns (or refuse if it's not a requirement at all — design or scope copy belongs elsewhere).
3. Rewrite to fit the template; keep the requirement's intent.
4. Suggest the eval category (§8.3) the requirement maps to.
5. If the requirement modifies an existing ID, ensure `### MODIFIED Requirement <ID>` precedes it (§6.6).

## References

- AXIS-26 §6.6 Capability Specs and Deltas.
- AXIS-26 §S2 EARS form requirement.
- Mavin, A. et al. *Easy Approach to Requirements Syntax.* IEEE RE, 2009.
