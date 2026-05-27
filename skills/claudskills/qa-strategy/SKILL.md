---
name: qa-strategy
description: "[QA Process · ISO 25010 + ISTQB CTFL v4.0] Test Strategy document creation — defines scope, risk appetite, test approach, coverage goals, and tool selection for the project. Run before qa-plan."
---

# Helix — QA Strategy

> 📚 **Knowledge References** (loaded automatically):
> `qa-strategy-patterns.md` — ISTQB test strategy templates, risk appetite frameworks, coverage models

A Test Strategy is the highest-level QA document — it answers *why* and *how* testing will be done across the project lifecycle.

## Step 1: Gather Context

Ask the user:
```
1. What type of project? (web app / API / mobile / backend service / other)
2. What quality risks concern you most? (data loss / security / performance / accessibility / UX)
3. What's the release cadence? (continuous / sprint-based / major releases)
4. Any compliance requirements? (GDPR, HIPAA, PCI-DSS, WCAG 2.1)
5. Team structure — dedicated QA engineers, devs doing QA, or both?
```

## Step 2: Define Strategy Dimensions

Cover all 6 dimensions:

| Dimension | Content |
|-----------|---------|
| **Scope** | What is in/out of scope for testing |
| **Risk Appetite** | Which risk categories are critical vs acceptable |
| **Test Approach** | Shift-left, risk-based, exploratory, automated-first |
| **Coverage Goals** | % targets per tier (unit ≥90%, integration ≥70%, E2E critical paths) |
| **Tool Selection** | Free-first tools per test type |
| **Exit Criteria** | What "done" looks like for each tier |

## Step 3: Risk Appetite Matrix

```
| Risk Category      | Likelihood | Impact | Priority |
|--------------------|------------|--------|----------|
| Data loss/corruption | ?        | High   | ?        |
| Security breach    | ?          | High   | ?        |
| Performance SLO    | ?          | Medium | ?        |
| Accessibility      | ?          | Medium | ?        |
| Visual regression  | ?          | Low    | ?        |
```

Fill with user's input. High × High = must test every release.

## Step 4: Coverage Model

Map test types to project risk areas:

```
Critical paths     → E2E (every release)
Business logic     → Unit ≥ 90% coverage
API contracts      → Contract tests (every service change)
Auth / Security    → Security audit (every release)
Performance SLOs   → Load test (pre-release)
```

## Step 5: Output

Save to `docs/qa/qa-strategy.md`:

```markdown
# Test Strategy — [Project Name]
**Version:** 1.0 | **Date:** YYYY-MM-DD | **Author:** QA

## Scope
## Risk Appetite
## Test Approach
## Coverage Goals
## Tool Selection
## Exit Criteria per Tier
## Compliance Requirements
```

Commit to repo.

## Done

Present strategy doc path + summary table of coverage goals.
Suggest next step: `/helix qa-plan`

## Self-Evaluation Loop

```
1. Output ครบตาม scope ไหม?
2. Risk appetite สอดคล้องกับ project type ไหม?
3. Exit criteria ชัดเจน วัดได้จริงไหม?
4. มี side effect ที่ไม่ตั้งใจไหม?
```
