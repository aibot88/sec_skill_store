---
name: agent-security
description: Run agent-adapted STRIDE + access-control analysis on an agent system. Produces a ranked risk list with agentic mitigations (scope / split / filter / gate / review).
---

# Agent Security — audit skill

Generic skill shipped with the training. Walks two lenses against any
agent system pointed at it:

1. **Access-control analysis** — what external systems the agent can
   reach, and whether each reach is necessary.
2. **Agent-STRIDE** — the six STRIDE categories adapted to agent
   systems (not classical software systems).

## Invocation

Ask Claude to "apply the agent-security skill to [target system]."
Output lands at `module-4/security-report.md`.

## Access-control pass

For each external touch-point the target system has, answer:

- What does the agent reach? (connector, file write beyond working dir,
  sub-agent dispatch, tool use)
- Why does it reach? (what the system actually does with it)
- Could the system work without it? (if yes → unused access, flag)

List unused access as a cluster of access-control findings. Each gets a
severity rating (high / medium / low) based on what the access could
enable if the agent misbehaves.

## Agent-STRIDE

Six categories, each adapted. See `stride.md` for full definitions.
Short form:

- **Spoofing** — an agent impersonates a human author; a memory file
  pretends to be from a source that doesn't exist.
- **Tampering** — an agent modifies memory / rules / sources in ways
  that sneak into future sessions; output drift through silent edits.
- **Repudiation** — the agent writes without attribution; no audit of
  which agent produced what at what time.
- **Information disclosure** — the agent reveals content it was told
  to hold (personal notes, Confidential data, restricted sources).
- **Denial of service** — agent loops, subagent sprawl, runaway memory
  growth that locks out the human operator.
- **Elevation of privilege** — an agent invokes another agent that has
  wider scope than the first should carry; transitive trust violations.

For each category, name the top 1-2 specific risks in the target
system — not generic category descriptions.

## Mitigations (five shapes)

Each risk gets one suggested mitigation:

- **Scope** — narrow what the agent reads / writes / invokes.
- **Split** — separate the agent into two with distinct permission
  profiles.
- **Filter** — add a rule the agent must apply before writing (e.g.,
  "redact PII before saving").
- **Gate** — add a human-approval step (e.g., "show me the diff before
  applying").
- **Review** — add a second agent that checks the first's output.

Match mitigation shape to risk shape. Not all shapes fit all risks.

## Output shape

`module-4/security-report.md`:

```
## Access-control findings
<list, ranked by severity>

## Agent-STRIDE findings
<six sub-sections, each with 1-2 named risks>

## Ranked mitigations
<three-tier: high / medium / low, each with one mitigation shape>
```

See `access-analysis.md` and `stride.md` for the full walk.
See `mitigations.md` for worked examples of each shape.
