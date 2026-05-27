---
name: principle-code-review
description: Code review heuristics — four-axis review lens (correctness, security, design integrity, test coverage); confidence-based filtering (no finding without a concrete failure scenario); review comment tone (observation over accusation); nitpick filtering; what counts as a real finding vs linter noise. Auto-load when writing or framing a review comment, deciding whether a PR finding is worth surfacing, reviewing a diff for correctness, or filtering review nitpicks.
---

# Code Review

Principles for high-signal code review. For tool-specific mechanics (diff-size routing, suggestion-block format, GitHub workflow), see the `reviewer` agent.

## Four-Axis Review Lens

Every review covers four axes:

- **Correctness** — off-by-ones, null paths, concurrency races, lost errors, unhandled edge cases.
- **Security** — injection, auth/authz gaps, secrets in code, unsafe deserialization, SSRF, missing input validation at trust boundaries.
- **Design integrity** — SOLID violations, leaky abstractions, tight coupling, circular deps, domain logic bleeding into infrastructure.
  *For complexity / duplication / length, prefer Quality-stage output over subjective comments — see `workflow-development`.*
- **Tests** — missing coverage on new branches, brittle tests, tests that mirror implementation rather than behavior.

## What's Not a Finding

Do not surface these:

- Formatting, import order, quote style — owned by the linter, not the reviewer.
- Stylistic preferences with no behavioral impact.
- Speculative "could be" comments without a concrete failure mode.

These erode review signal. If your only comment is a style preference, stay silent.

## Confidence-Based Filtering

Before surfacing a finding, apply this filter:

1. **Name the failure scenario.** What breaks, under what inputs, in what deployment context? If you cannot articulate it, the finding is speculative — drop it.
2. **One strong comment over five weak ones.** Ten medium-confidence findings force the author to triage; two high-confidence findings close the loop.
3. **Missing tests are a finding, not an afterthought.** Untested new branches are incomplete work.

Confidence floor by severity:

| Severity | Minimum confidence | Action if below floor |
|---|---|---|
| Critical | 0.9 | Must name an exploit or data-loss path |
| High | 0.75 | Must name a realistic failure scenario |
| Medium | 0.5 | Can surface; mark as "likely" |
| Low / Nit | Any | Drop unless the fix is a one-liner |

## Tone

Review the code, not the author.

- **Observation language:** "This path returns nil without checking the error" — not "You forgot to check the error."
- **Acknowledge good work briefly.** Silence is not approval; a short note reduces defensive reading.
- **Frame as options for Medium/Low.** "One option: …" not "You should …".
- **Reserve mandates for Critical/High.** Direct language is appropriate when the stakes are real.

## Red Flags

| Pattern | What it signals |
|---|---|
| Finding with no named failure scenario | Speculation — refine or drop |
| Five+ findings, none above Medium | Signal-to-noise failure — prioritize |
| Only linter-owned comments (style, formatting) | Scope creep — let the linter own these |
| Zero positive observations in a long review | Adversarial culture risk |
| Nitpick marked Critical | Severity inflation — recalibrate |

## When Code Review Hurts

- **Throwaway prototypes** — review cost exceeds value if you're about to discard the code.
- **Hotfix rollbacks** — reverting to a known-good state introduces no new logic to review.
- **Trivially covered one-liners** — if the tests already encode the contract, a comment adds ceremony without safety.
