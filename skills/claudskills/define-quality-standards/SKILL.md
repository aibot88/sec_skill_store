---
name: define-quality-standards
description: Capture the quality and standards baseline — linting, formatting, testing strategy, security, accessibility, performance budgets, documentation, and observability. Use when the project-builder agent is gathering quality/standards information.
---

# Purpose

Decide what "good" means for this project up-front so the scaffold can include the right guardrails from day one.

# Questions to ask (in order)

1. Code style: existing style guide (company, open-source convention) or pick language defaults?
2. Linting and formatting tools per language.
3. Testing strategy: which levels apply (unit, integration, end-to-end) and rough coverage expectation.
4. Test frameworks per language.
5. Security baseline: dependency scanning, secrets management, SAST, auth testing, and whether to include a threat-modeling commitment (ask explicitly whether a threat model document should be part of the scaffold).
6. Accessibility target (for any UI): none, WCAG AA, or WCAG AAA.
7. Performance budgets: any hard numbers (page load, API p95 latency, memory ceiling, bundle size)?
8. Documentation expectations: README only, README plus ADRs, or full docs site.
9. Observability baseline: logs only, logs + metrics, or logs + metrics + tracing.
10. Profile opt-ins: which `profile-*` skills in the session workspace should this project follow? List skill names by exact name (e.g., `profile-java-database-access`). Leave empty if none apply. If the user is unsure, glob `<SESSION_DIR>/.claude/skills/profile-*/SKILL.md` and show the names plus their description lines so the user can pick.

Use `AskUserQuestion` where multiple choice fits.

# Solution space to present

- **Test pyramid shapes**: heavy unit / balanced / heavy integration or E2E. Tradeoff: feedback speed vs. realism.
- **Security tooling**: language-native audit tools (`npm audit`, `pip-audit`, `cargo audit`), Dependabot or Renovate, Snyk, Semgrep, Trivy (containers), explicit threat-model document.
- **Observability**: OpenTelemetry + self-hosted (Prometheus/Grafana/Jaeger), hosted (Datadog, Honeycomb, New Relic, Grafana Cloud), print-to-stdout + log aggregator.
- **ADR practice**: none / lightweight markdown ADRs / formal architecture docs.

# Required schema

- `style_guide` (string)
- `linters_formatters` (list per language)
- `testing` (`{levels, coverage_target, frameworks}`)
- `security` (list)
- `accessibility_target` (string)
- `performance_budgets` (list)
- `documentation` (string)
- `observability` (string)
- `profiles` (list of profile skill names — possibly empty)

# Output

Write **two** top-level sections to `PROJECT_BRIEF.md`, in this order:

1. `## Quality & Standards` — captures the answers to questions 1–9 above. Replace any prior `## Quality & Standards` section when re-run.
2. `## Profiles` — one profile skill name per line, exactly as they appear in `.claude/skills/`. Write `None` on a single line if the list is empty. Replace any prior `## Profiles` section when re-run.

The `## Profiles` section is a separate top-level heading (not a subsection) because every role agent reads it independently during the `develop` workflow.

# Frontmatter contribution

Update these YAML frontmatter fields (see `CLAUDE.md` for the full schema). Leave every other field untouched:

- `test.framework` — the primary test framework (e.g., `junit`, `spock`, `pytest`, `vitest`, `jest`, `go test`)
- `test.levels` — list of levels the project commits to (e.g., `[unit, integration]`, `[unit, integration, e2e]`)
- `test.coverage_target` — the stated target (e.g., `80%`, `none`)
- `profiles` — list of profile skill names, exactly as they appear in `.claude/skills/`. Must be identical to the names written in the `## Profiles` prose section; keep them in sync.
