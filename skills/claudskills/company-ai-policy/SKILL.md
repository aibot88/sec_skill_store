---
name: company-ai-policy
description: Audit an agent system against Kaleva Retail Group's AI and data-usage policies. Produces a row-per-rule compliance report with verdicts (compliant / violating / "I can't tell") and evidence from the target system's files.
---

# Company AI Policy — audit skill

Built by Antti for Kaleva Retail Group from their active policies at
the time of the M4 training. Not a generic bundle — it encodes Kaleva's
specific decisions about what's off-limits.

## How to use

Ask Claude to "apply the company-ai-policy skill to [target system]."
Claude will read every rule in `policies/`, walk the target system's
files, and produce a row-per-rule report at `module-4/policy-report.md`.

## Rule sources

- `policies/data-usage.md` — what data an agent may read, what it may
  write, where outputs may land.
- `policies/security.md` — authentication, secret handling, audit
  trails, transitive trust.
- `policies/ai-use.md` — enterprise-agreement rules, model-tier
  restrictions, human-in-the-loop thresholds.
- `policies/sector-rules.md` — retail-sector specific (GDPR for
  customer data, NIS2 adjacencies, PCI-DSS scope boundary).

## Report shape

For each rule across the four policy files, one row:

| Rule | One-line description | Verdict | Evidence |
|---|---|---|---|
| R-XXX | ... | compliant / violating / I can't tell | Quote from target system or `what evidence needed` |

## The "I can't tell" rule

"I can't tell" is a real verdict, not a hedge. Use it when the rule's
compliance cannot be decided from the target files alone. Always pair
with a `what evidence would resolve this` note. Do not upgrade to
"compliant" without evidence; do not downgrade to "violating" on a
hunch.

## Scope

Target is the full Kaleva-shaped agent system: `memory/`, `sources/`,
`agents/`, root `CLAUDE.md`, `module-N/` folders, any `skills/` folders.
Never read customer data stores, production databases, or the
classification-restricted material from Security's draft policy. If the
target references Restricted data, flag as a dependency not a source.
