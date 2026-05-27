---
name: qa-plan
description: "[QA Process · ISTQB CTFL v4.0] Test Plan creation — objectives, schedule, resources, entry/exit criteria, and risk mitigation. Run after qa-strategy, before test execution."
---

# Helix — QA Plan

> 📚 **Knowledge References** (loaded automatically):
> `qa-plan-patterns.md` — ISTQB test plan structure (IEEE 829), entry/exit criteria templates, resource planning

A Test Plan translates the Test Strategy into a concrete, time-bound execution plan for a specific release or sprint.

## Step 1: Load Strategy

Check if `docs/qa/qa-strategy.md` exists. If yes, load it. If no, ask user to run `/helix qa-strategy` first or provide key details inline.

## Step 2: Gather Release Context

```
1. What release / sprint is this plan for?
2. What features / changes are in scope?
3. Target release date?
4. Available testing resources (people / environments)?
5. Known risks or dependencies?
```

## Step 3: Build Test Plan

### Entry Criteria
Conditions that must be met before testing starts:
- Code complete and deployed to test environment
- Unit tests passing (≥ coverage targets)
- No P0/P1 open defects from previous release
- Test data seeded and verified

### Exit Criteria
Conditions that define "testing done":
- All Tier 1 functional tests passing
- Tier 2 non-functional tests passing
- P0/P1 defects resolved, P2 accepted or deferred
- Test report approved by stakeholders

### Test Schedule

| Phase | Start | End | Responsible |
|-------|-------|-----|-------------|
| Tier 1 — Functional | | | |
| Tier 2 — Non-Functional Quality | | | |
| Exploratory Testing | | | |
| Defect Fix + Retest | | | |
| Sign-off | | | |

### Risk & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Environment instability | Medium | High | Backup env ready |
| Late code freeze | Medium | High | Buffer days in schedule |
| Test data gaps | Low | Medium | qa-data skill |

## Step 4: Output

Save to `docs/qa/qa-plan-YYYY-MM-DD.md`:

```markdown
# Test Plan — [Release Name]
**Version:** 1.0 | **Date:** YYYY-MM-DD

## Scope
## Entry Criteria
## Exit Criteria
## Test Schedule
## Resources
## Risk & Mitigation
## Sign-off
```

Commit to repo.

## Done

Present plan path + schedule table.
Suggest next step: `/helix qa-risk`

## Self-Evaluation Loop

```
1. Entry/exit criteria วัดได้จริงไหม?
2. Schedule realistic ไหม?
3. Risk มี mitigation ครบไหม?
4. สอดคล้องกับ qa-strategy ไหม?
```
