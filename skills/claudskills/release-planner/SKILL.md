---
name: release-planner
description: >
  Plan out the feature set for a release (MVP, v1, v2, or any milestone). Enumerates
  candidate features, prioritises them against capacity and deadline, publishes a
  Confluence roadmap page, and creates empty JIRA epic placeholders — one per
  feature — that downstream skills (feature-spec-author, backlog-manager) flesh out.
  Use when: scoping an MVP, planning the next release, rolling over deferred work
  into a new milestone, or any time you need a reviewable feature list before
  specs are written. Phase 0.5 of the ol-sdd-workflow orchestrator, sitting between
  steering (Phase 0) and feature specification (Phase 1).
---

# Release Planner

## Role

You turn product goals (from steering) into a prioritised feature list for a specific release or milestone. You do NOT design features — that's Phase 1. You produce the shortlist, with enough description that stakeholders can review and approve scope, and you publish that shortlist as:
- a Confluence roadmap page (narrative + table)
- one empty JIRA epic per in-scope feature

You are invoked by the `ol-sdd-workflow` orchestrator at Phase 0.5, or directly when release planning is needed.

## Inputs

- Approved steering docs: `documentation/steering/product.md`, `tech.md`, `structure.md`
- Release target — name (e.g., "MVP", "v1.0", "Q2-2026") and date
- Capacity — total engineer-days or hours across the release window
- Constraints — hard deadlines, must-have regulatory features, external dependencies
- Optional: existing backlog, prior release retrospectives, stakeholder requests

## Outputs

| Output | Where |
|--------|-------|
| Feature list | `documentation/releases/{release-name}/features.md` (prioritised table) |
| Release narrative | Same file, top section (the "why" of this release) |
| Confluence page | "Release Plan — {release-name}" under project parent page |
| JIRA epics | One empty epic per in-scope feature, labelled `release:{name}` |
| Epic map | `documentation/releases/{release-name}/epic-map.md` (feature name → JIRA key) |

## Workflow

### Step 1 — Load Context

Read:
- `documentation/steering/product.md` — vision, users, objectives, principles
- `documentation/steering/tech.md` — stack capability constraints
- `documentation/workflow-config.md` — JIRA project, Confluence space
- Existing `documentation/releases/` if any prior release exists — check for deferred features

If steering docs are absent, stop and route the user to `product-vision-steering` (Phase 0). Release planning without steering produces disconnected feature lists.

### Step 2 — Gather Release Context

Ask the user (skip questions you can answer from inputs):
- Release name and target date
- Capacity (team size × working days × utilisation)
- Release theme or one-line goal
- Any features already known to be in scope (regulatory, contractual, carry-over from prior release)
- Any features already known to be out of scope

### Step 3 — Enumerate Candidate Features

Produce a raw candidate list. Sources:
- Key features listed in `product.md`
- Stakeholder requests (if the user provides them)
- Carry-over from prior releases
- Gaps identified in steering analysis
- Follow-on features implied by features the user has named

For each candidate, draft:
- **Name** (kebab-case, e.g., `licence-data-extraction`)
- **One-line description** (what value it delivers to whom)
- **T-shirt size** (XS/S/M/L/XL — rough order-of-magnitude, not a commitment)
- **MoSCoW priority** (Must / Should / Could / Won't-this-release)
- **Upstream dependencies** (other features or external systems)
- **Downstream consumers** (features that unlock with this)
- **Rough rationale** (why this release, why this priority)

Do not produce detailed designs. Keep each feature to ~3–5 sentences total.

### Step 4 — Fit to Capacity

Convert T-shirt sizes to rough hours (XS=8, S=24, M=60, L=120, XL=240 — adjustable per-team). Sum the Musts. If Musts exceed capacity, surface the conflict — don't silently defer:

> "Your 240-hour release has 320 hours of Must features. We need to either extend the deadline, reduce scope, or reclassify some Musts as Shoulds. Which would you prefer?"

Propose:
- A **minimum viable scope** (Musts only, fits within 60% of capacity)
- A **target scope** (Musts + top Shoulds, ~85% of capacity)
- A **stretch scope** (adds Coulds if everything above lands early)

Leave 15% headroom by default — release planning that plans to 100% always slips.

### Step 5 — Present for Approval

Show the user:
- Release narrative (theme, why now, success criteria)
- Feature table with all columns
- Three scope tiers (minimum / target / stretch)
- Open questions or risks

**Gate: user approves the feature list and target scope before any epics are created.**

Iterate until approved. This phase is deliberately cheap — it's faster to rework a 10-row table than to unwind 15 JIRA epics.

### Step 6 — Publish

On approval:

1. **Write `documentation/releases/{release-name}/features.md`** containing:
   - Release narrative
   - Scope tiers
   - Feature table (priority order within tier)
   - Dependency diagram (Mermaid)
   - Open questions log

2. **Create the Confluence page** "Release Plan — {release-name}" under the project parent page. Structure:
   - H1: `{Release Name} — Release Plan`
   - H2: Goal and narrative
   - H2: Scope (three tiers)
   - H2: Feature table
   - H2: Dependencies (Mermaid)
   - H2: Timeline (if there's a rough phasing)
   - H2: Open questions
   - H2: Linked epics (populated after step 3)

3. **Create one JIRA epic per in-scope feature** (target scope by default; user can ask for minimum or stretch). For each:
   - Summary: `{Feature Name} — {one-line description}`
   - Description: the 3–5 sentence feature brief + link back to Confluence release page
   - Labels: `release:{release-name}`, `feature:{feature-name}`, `priority:{must|should|could}`
   - Status: To Do (unplanned — no stories or subtasks yet)
   - T-shirt size / rough estimate in a custom field if available
   - Parent: none (epics are top-level)
   
   Do NOT create stories or subtasks — those are `backlog-manager`'s responsibility when `feature-spec-author` has approved a full spec for the feature.

4. **Write `documentation/releases/{release-name}/epic-map.md`**:
   ```markdown
   # Epic Map — {release-name}
   
   | Feature | Priority | T-Size | JIRA Epic | Spec Status |
   |---------|----------|--------|-----------|-------------|
   | licence-data-extraction | Must | L | [TI-100](url) | not specced |
   | document-viewer | Must | M | [TI-101](url) | not specced |
   ```
   
   The `Spec Status` column is updated by `feature-spec-author` when it completes a spec for the feature.

5. **Update the Confluence release page** with the linked-epics section (table of JIRA epic keys and URLs).

6. Return to caller with:
   - Release page URL
   - Count of epics created
   - Epic map file path

---

## Re-planning and Roll-over

When invoked on an existing release:

- **Mid-release adjustment**: read current `features.md`, identify deltas (new features, deferred features, re-prioritised features), propose changes, get approval, update files and JIRA labels. Append a "Replan {date}" section — never rewrite history.
- **Post-release roll-over**: when a release closes with deferred features, invoke `release-planner` for the next release with "carry over from {prior release}" as input. It reads the prior release's unfinished epics and adds them as candidates (user can re-prioritise or drop).

Never delete JIRA epics — if a feature is cancelled, transition to "Won't Do" with rationale.

---

## What This Skill Does NOT Do

- Does not design features — that's `feature-spec-author` at Phase 1 (triggered per-feature once scope is approved)
- Does not produce requirements, design docs, or task breakdowns — those happen in Phase 1
- Does not create stories or subtasks — that's `backlog-manager` at Phase 2 (triggered once a feature has an approved spec)
- Does not plan sprints — that's `sprint-planner` at Phase 3
- Does not commit to exact effort estimates — T-shirt sizes only. Detailed estimation happens per-task in Phase 1 and is summed in Phase 2.
- Does not make architectural decisions — those live in `documentation/steering/tech.md` (Phase 0) or are deferred to individual feature designs (Phase 1)

---

## Handoff to Phase 1

When the user is ready to design a feature from this release:

```
User: "use feature-spec-author to spec out licence-data-extraction"
```

`feature-spec-author` reads `documentation/releases/{release-name}/epic-map.md`, finds the matching JIRA epic (`TI-100`), and links the full spec to that existing epic. It does not create a new epic. When tasks.md is approved, `backlog-manager` creates stories and subtasks as children of the pre-existing epic.

This handoff is the reason release-planner creates empty epics upfront: every downstream artifact (spec, stories, subtasks, sprint plans, impl logs) is traceable back to a release-scope decision made at Phase 0.5.

---

## References

- `prompts/coding/templates/release-plan-template.md` — features.md template
- `prompts/coding/templates/jira-epic-template.md` — epic fields (release-planner populates a skeleton version)
- Atlassian MCP: `createJiraIssue`, `createConfluencePage`, `updateConfluencePage`
- Upstream: `software-architect` high-level-design mode produces a similar "phased development plan" but as design documentation; `release-planner` extends this with JIRA publishing and release-centric prioritisation


---

## Feedback

If the user corrects this skill's output due to a misinterpretation or missing rule **in the skill itself** (not a one-off preference), invoke `skill-feedback` to capture structured feedback and optionally post a GitHub issue.

If `skill-feedback` is not installed, ask the user: *"This looks like a skill defect. Would you like to install the `skill-feedback` skill to report it?"* If the user declines, continue without feedback capture.
