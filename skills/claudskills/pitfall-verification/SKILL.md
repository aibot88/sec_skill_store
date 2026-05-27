---
name: pitfall-verification
description: Use after completing any PRD, spec, plan, or code implementation — verifies that artifact-specific pitfalls (security, idempotency, integration contracts, edge cases, LLM output) do not apply before declaring work done. Two rounds max.
---

# Pitfall verification

Use this skill after finishing any PRD, spec, plan, or code artifact — before declaring the work done. It is NOT a generic review. It is a targeted check that *typical pitfalls for this type of artifact, in this domain, do not apply here*.

Invoke with: `/superpowers-gstack:pitfall-verification`

## When to invoke

Automatically after completing:

- A PRD, spec, or design document
- An implementation plan
- A code change (feature, refactor, bug fix)
- Output from `writing-specs`, `writing-plans`, `executing-plans`, `verification-before-completion`, or any GStack planning/review skill

Run **twice max**. Two rounds catch almost everything; a third round has sharply diminishing returns.

## Sequence

1. **Self-check first** (~30 seconds): placeholders, scope drift, internal consistency, ambiguity. This is the standard sanity pass. Fix anything obvious.
2. **Pitfall verification** (this skill): targeted check for the pitfalls below, adapted to the artifact type and domain.

Do not skip step 1 — self-check and pitfall verification are different lenses.

## Pitfall lists per artifact type

These are **starting points, not exhaustive checklists**. Always ask: *what typically goes wrong with this kind of artifact, in this specific domain?* Infer additional pitfalls from the actual code/spec under review.

### PRD

- Unclear user story or missing success metric
- Hidden stakeholder assumptions (who signs off? who blocks?)
- Unspecified non-functional requirements (perf, privacy, accessibility, i18n)
- Conflicting requirements across sections
- Missing failure modes (what if X is unavailable? what if load spikes?)
- Over-specification of solution vs under-specification of problem

### Spec / plan

- Ambiguous contracts — input/output types, error shapes, null semantics
- Uspecified edge cases (empty, max-size, concurrent, partial failure)
- Missing error states / recovery paths
- Hidden assumptions about call order, transactions, idempotency
- Signature drift: spec references functions/fields that do not exist in the code
- Assumed external API behavior that has not been verified

### Code

- **Security**: prompt injection, input sanitation, credential leakage, SSRF, path traversal, auth bypass
- **Idempotency**: side effects on retry, hidden state, ordering dependencies
- **Integration contracts**: field names, types, and signatures that actually match the code they call into (cross-check — do not assume)
- **Edge cases**: empty input, oversized input, Unicode, currencies, time zones, DST, negative numbers, leap years
- **LLM output**: markdown-wrapped JSON, unexpected JSON structure, hallucinated fields, schema drift
- **Concurrency**: race conditions, deadlocks, shared mutable state
- **Resource lifecycle**: leaked handles, unclosed connections, memory growth under load

## How to run the check

For each pitfall on the relevant list:

1. **State the pitfall** — one sentence.
2. **Locate the risk surface** — which function, field, section, or claim could be affected?
3. **Verify**, do not assume. Read the actual code/spec. Cross-check field names against the implementation. Test the edge case mentally with real values.
4. **Report**: *Not applicable* (with reason) / *Applicable and handled* (point to where) / *Applicable and not handled* (propose fix).

If a pitfall is not applicable to this domain, say so explicitly — do not silently skip it. Stating "N/A because this code never touches dates" is itself a verification signal.

## Domain inference

The lists above are *generic-LLM-common*. Real pitfalls are often domain-specific. Before the round, spend 15 seconds asking:

- What kind of system is this? (auth? payments? ETL? LLM pipeline? UI? infra?)
- What categories of bugs hit this kind of system most often?
- What did *past* bugs in this codebase/team look like? (check git log, CHANGELOG, incident notes if accessible)

Add those inferred pitfalls to the round before running.

## Output format

End the round with a compact verdict:

```
Pitfall verification (round N/2):
- [pitfall] → N/A | handled at file:line | NOT HANDLED — proposed fix
- ...

Verdict: CLEAN | ISSUES FOUND (see above)
```

If round 1 surfaces issues, fix them, then run round 2 on the patched artifact. If round 2 is clean, declare done. If round 2 still finds issues, surface them to the user — do not silently run round 3.

## Why two rounds

One round catches the obvious pitfalls. Round 2, run on the patched artifact, catches pitfalls that the fixes from round 1 introduced or exposed. Beyond that, returns drop fast and reviewer fatigue introduces noise.

## What this skill is NOT

- Not a security audit (narrower, adversarial, deeper)
- Not a code review of style or readability
- Not a test suite (does not execute code)
- Not a replacement for `verification-before-completion` (which checks *claims vs reality* for already-finished work — pitfall verification is upstream of that)

Use it as the *last check before handing off* — after implementation, before the user sees "done".
