---
name: qualification
description: Lead qualification using BANT 6-criteria gate (Problem, Budget, Authority, Timeline, Fit, Margin) at marketing-sales handoff. Qualified leads enter pipeline, unqualified go to nurture. If bottleneck is downstream, reduce upstream lead gen. Use when evaluating leads, managing marketing-sales handoff, or when pipeline quality is poor.
type: skill
---

# Lead Qualification

## When to Apply
- Evaluating new leads for pipeline entry
- Marketing-sales handoff decisions
- When pipeline quality is poor (low conversion rates)
- When downstream bottleneck exists (too many unqualified leads)
- Configuring qualification criteria during onboarding

## Core Framework

### BANT 6-Criteria Gate

Every lead must pass all 6 criteria before entering the pipeline at Step 2:

| Criteria | Question | Pass Condition |
|---|---|---|
| **Problem** | Does the prospect have a problem our product solves? | Specific, articulated pain point matching our solution |
| **Budget** | Is budget allocated or likely? | Budget exists or can be created within purchase timeline |
| **Authority** | Is the decision-maker engaged or accessible? | Direct contact with buyer, or champion with access to buyer |
| **Timeline** | Is there a reasonable purchase timeframe? | Active evaluation, not "maybe someday" |
| **Fit** | Does our product capability match their need? | Core use case alignment, not edge-case stretching |
| **Margin** | Can we achieve acceptable margin on this deal? | Deal economics above minimum threshold |

### Qualification Flow

```
Incoming lead
  |
  +-> Score against 6 criteria
  |
  +-> All 6 pass: QUALIFIED
  |     -> Enter pipeline Step 2
  |     -> Assign to appropriate sales Actions
  |
  +-> 1-2 fail: NURTURE
  |     -> Add to nurture sequence
  |     -> Re-evaluate in 30/60/90 days
  |     -> Do NOT add to pipeline
  |
  +-> 3+ fail: DISQUALIFY
        -> Remove from active tracking
        -> Log reason for future pattern analysis
```

### Downstream Bottleneck Rule

When the pipeline bottleneck is downstream (e.g., demo capacity at 90% utilization):

**Reduce upstream lead gen volume, don't increase it.**

```
Bottleneck: Demo capacity (30/month, 90% utilized)
Qualified leads waiting: 15 in queue

WRONG: "Generate more leads to increase pipeline"
RIGHT: "Reduce lead gen to match demo throughput.
        Generating more leads than demo can handle is waste."
```

This is TOC's subordination principle applied to the sales pipeline.

### Quality vs Quantity Tradeoffs

| Scenario | Recommendation |
|---|---|
| High volume, low qualification rate (<20%) | Tighten lead gen targeting. "39% qualification means 61% wasted effort." |
| Low volume, high qualification rate (>80%) | Expand lead gen. Quality is proven, need more volume. |
| High volume, high qualification rate | Scale carefully — check downstream capacity first. |
| Low volume, low qualification rate | Fix targeting AND qualification criteria. Both broken. |

### Qualification Criteria Calibration

Criteria should be reviewed quarterly:
- Too strict: pipeline starves (qualification rate >90%, pipeline-to-quota <2x)
- Too loose: pipeline polluted (qualification rate <20%, downstream conversion drops)
- Target: 30-50% qualification rate with healthy downstream conversion

## Decision Rules

1. **All 6 criteria must pass** — partial qualification goes to nurture, not pipeline
2. **Nurture is not rejection** — unqualified today may qualify later
3. **Downstream capacity limits upstream** — never flood a constrained pipeline
4. **Qualification rate is a health metric** — track it, calibrate criteria
5. **Log disqualification reasons** — patterns reveal targeting problems
6. **Quarterly criteria review** — criteria drift over time, recalibrate

## Anti-Patterns to Detect

| Anti-Pattern | Signal | Response |
|---|---|---|
| Pipeline pollution | Unqualified leads in pipeline | "These leads don't meet criteria. Move to nurture." |
| Upstream flooding | Lead gen outpacing downstream capacity | "Subordinate upstream volume to downstream throughput." |
| Over-strict criteria | >90% qualification, starving pipeline | "Criteria may be too strict. Consider relaxing [specific criterion]." |
| Missing criteria | Qualification without checking all 6 | "Budget and Authority not checked. These are common failure points." |
| Wishful qualification | "Budget probably exists" | "Unverified. Mark as hypothesis, verify before pipeline entry." |
| Ignoring nurture | Disqualified leads abandoned | "Nurture sequences convert 5-15% over 6 months. Don't abandon." |
