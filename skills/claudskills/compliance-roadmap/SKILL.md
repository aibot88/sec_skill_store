---
description: Build a phased compliance roadmap with milestones, dependencies, and resource needs
---

# Compliance Roadmap

Build a phased compliance roadmap for "$ARGUMENTS" with concrete milestones, inter-certification dependencies, resource estimates, and target dates.

## Prerequisites

None — this is a Phase 0 (Scope) skill.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for regulation inventory, priorities, and control framework

2. **Phase 1 — Quick wins and highest-priority regulations:**
   - Select Tier 1 regulations and quick wins from the priority analysis
   - Define specific milestones with target completion dates
   - Identify controls to implement first (highest leverage points)
   - Estimate effort: internal hours, external consultant days, tool costs

3. **Phase 2 — Comprehensive coverage:**
   - Select Tier 2 regulations building on Phase 1 foundations
   - Map dependencies — which Phase 1 controls are prerequisites?
   - Define milestones with target dates accounting for Phase 1 completion
   - Estimate incremental effort (many controls already in place)

4. **Phase 3 — Advanced and sector-specific:**
   - Select Tier 3 and sector-specific regulations
   - Map dependencies on Phase 1 and Phase 2 controls
   - Define milestones with target dates
   - Estimate effort for remaining gap controls

5. **Dependency mapping:**
   - Document inter-certification dependencies (e.g., ISO 27001 before CSA STAR Level 2, SOC 2 before enterprise sales)
   - Identify critical path — which certifications gate others?
   - Flag parallel tracks that can proceed independently

6. **Resource planning:**
   - Estimate total resources: internal FTEs, external consultants, audit costs, tooling
   - Create budget breakdown by phase
   - Identify hiring or training needs
   - Recommend GRC tooling (if applicable)

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/00-scope.md` (append to existing) with sections:
   - **Roadmap Overview** — visual timeline of all three phases
   - **Phase 1 Plan** — regulations, milestones, dates, resources
   - **Phase 2 Plan** — regulations, milestones, dates, resources
   - **Phase 3 Plan** — regulations, milestones, dates, resources
   - **Dependency Graph** — inter-certification dependencies and critical path
   - **Resource Summary** — total budget, FTE needs, external support

## Output

The compliance roadmap appended to `.metapowers/compliance/$ARGUMENTS/00-scope.md`. Present a summary to the user highlighting:
- Phase 1 target regulations and timeline
- Critical path dependencies
- Total estimated resource needs
- Recommended next step: begin Phase 1 assessments (e.g., `/compliance:soc2 $ARGUMENTS` or `/compliance:iso27001 $ARGUMENTS`)
