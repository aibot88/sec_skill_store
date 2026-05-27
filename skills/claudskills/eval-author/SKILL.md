---
name: eval-author
description: Author behavior evals for a change in five categories — Functional, Security, Performance, Accessibility, Drift — pinned to threshold floors per risk level (AXIS-26 §8.2, §8.3).
version: 0.0.1
---

# Eval Author

Every requirement in `delta.md` MUST trace to at least one eval. Eval depth scales with risk (§6.3, §8.2).

## Categories (§8.3)

| Category | Asks | Typical form |
|---|---|---|
| **Functional** | Does the system do what the spec says? | YAML cases, BDD `.feature`, pytest, jest |
| **Security** | Does the system avoid CWE-mapped weaknesses? | Targeted exploit attempts, fuzz inputs |
| **Performance** | p95 latency, throughput, resource budgets | Load script + assertion |
| **Accessibility** | WCAG 2.2 AA criteria for user-facing surfaces | axe-core, manual checklist |
| **Drift** | Does runtime still match spec? | Schema diffs, telemetry fingerprints |

## Threshold floors (§8.2 — implementations MAY raise, MUST NOT lower)

| Risk | Behavior pass rate | Latency p95 | Constitutional |
|---|---|---|---|
| low | ≥95% | — | 0 MUST violations |
| moderate | ≥98% | within 10% of baseline | 0 MUST; SHOULD requires ADR |
| high | ≥99.5% | within 5% of baseline | 0 violations; full CWE Top 25 clear; threat model signed; canary stable |

## Process

1. For each requirement in `delta.md`, propose at least one eval. For high-risk security or PII requirements, propose Functional + Security.
2. Layout under `.axis/changes/<id>/evals/<category>/<slug>.<ext>`.
3. Author cases in the runner's native syntax (Braintrust, Promptfoo, pytest, jest, .feature).
4. For LLM-judged evals: write the rubric and a κ-validation plan against human ratings (§8.3).
5. Set the suite-level threshold = max(risk-level floor, project override in `.axis/evals/config.yaml`).
6. Configure re-run policy per §8.3: N ≥ 3 RECOMMENDED at risk high; median pass rate decides.

## Anti-patterns

- **Eval theater**: thresholds set so nothing fails. Counter: κ-validation, quarterly eval-of-evals (§8.3, §D.5).
- One mega-eval covering all five categories — separate them so the report is informative.
- Hand-coded "pass: true" without an executable assertion.
- Latency assertions that don't reference a baseline.

## References

- AXIS-26 §8 Verification Model.
- §D.5 Anti-Patterns.
