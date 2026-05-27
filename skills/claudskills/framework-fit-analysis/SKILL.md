---
name: framework-fit-analysis
description: "Use when choosing, replacing, or justifying a framework, library, SDK, runtime, database, UI kit, or platform by fit: constraints, team skill, ecosystem maturity, migration cost, operability, performance, security, and exit cost. Do NOT use for routine dependency hygiene (use `dependency-architecture`), documenting an accepted decision (use `architecture-decision-records`), or framework-specific implementation work."
license: MIT
compatibility: "Portable technology-selection discipline for application frameworks, libraries, SDKs, platforms, runtimes, data stores, and agent tooling."
allowed-tools: Read Grep
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: capability
  category: engineering
  domain: architecture/technology-selection
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-11"
  drift_check: "{\"last_verified\":\"2026-05-11\"}"
  eval_artifacts: present
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"framework fit\",\"technology selection\",\"library choice\",\"SDK evaluation\",\"platform evaluation\",\"migration cost\",\"exit cost\",\"operability\",\"ecosystem maturity\",\"build vs buy\"]"
  examples: "[\"should we use Next.js server actions, route handlers, or a separate API service for this workflow?\",\"evaluate whether adding this charting library is worth it\",\"compare Supabase, Firebase, and custom Postgres for this project under real constraints\",\"we want to replace this framework - what fit analysis should happen before an ADR?\"]"
  anti_examples: "[\"audit installed packages for duplication and supply-chain risk\",\"write the ADR after we chose the framework\",\"implement this feature in the framework we already selected\",\"profile a slow page and optimize bottlenecks\"]"
  relations: "{\"boundary\":[{\"skill\":\"dependency-architecture\",\"reason\":\"dependency-architecture governs dependency graph shape and package boundaries; framework-fit-analysis evaluates a candidate technology decision\"},{\"skill\":\"architecture-decision-records\",\"reason\":\"architecture-decision-records records accepted decisions; framework-fit-analysis compares options before acceptance\"},{\"skill\":\"performance-engineering\",\"reason\":\"performance-engineering measures and optimizes actual behavior; framework-fit-analysis weighs expected performance among selection criteria\"},{\"skill\":\"refactor\",\"reason\":\"refactor changes existing code structure; framework-fit-analysis decides whether a larger technology shift is justified\"}],\"related\":[\"architecture-decision-records\",\"dependency-architecture\",\"performance-engineering\",\"owasp-security\"],\"verify_with\":[\"architecture-decision-records\",\"dependency-architecture\"]}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":180,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/framework-fit-analysis/SKILL.md
---

# Framework Fit Analysis

## Coverage

Evaluate technology fit before adoption, replacement, or standardization. Covers requirement fit, constraints, ecosystem maturity, maintenance health, team skill, integration cost, migration path, performance envelope, security posture, operational burden, lock-in, exit cost, and decision recording.

## Philosophy

Technology choice is context-dependent. "Best" without constraints is marketing. A good fit analysis makes tradeoffs explicit enough that a team can accept the costs knowingly.

Do not confuse popularity with fit. Do not let a narrow implementation preference choose a durable platform. The right output is a recommendation plus consequences, not a ranking table with fake precision.

## Method

1. State the job the technology must do.
2. List hard constraints: runtime, hosting, data, compliance, team, budget, timeline.
3. Define evaluation criteria and weights qualitatively: must-have, important, nice-to-have.
4. Compare credible options, including staying put.
5. Assess migration and exit costs.
6. Identify operational ownership and failure modes.
7. Recommend one path with accepted tradeoffs.
8. Hand off to `architecture-decision-records` if the decision is durable.

## Evals

This skill ships a comprehension-eval artifact at [`examples/evals/framework-fit-analysis.json`](https://github.com/jacob-balslev/skill-graph/blob/main/examples/evals/framework-fit-analysis.json). The checklist below is the authoring gate for technology-fit decisions; the eval file is the grader surface.

## Verification

- [ ] The recommendation is tied to explicit project constraints
- [ ] "Do nothing" or "keep current stack" was considered when real
- [ ] Migration and exit costs are named
- [ ] Operational ownership is named
- [ ] Performance and security claims are evidence-backed or marked uncertain
- [ ] The decision can be reversed only with known cost
- [ ] Follow-up ADR is proposed for durable choices

## Do NOT Use When

| Use instead | When |
|---|---|
| `dependency-architecture` | You need dependency graph hygiene, package boundaries, duplication control, or supply-chain guardrails. |
| `architecture-decision-records` | The choice is already made and needs a record. |
| `performance-engineering` | You need to measure and optimize actual runtime behavior. |
| A framework-specific skill | The framework is already chosen and the task is implementation. |
