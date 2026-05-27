---
name: qa-risk
description: "[QA Process · ISO 31000 + ISTQB CTFL v4.0] Risk-based test prioritization — builds a risk matrix (likelihood × impact), ranks test areas by priority, and flags critical paths for performance testing."
---

# Helix — QA Risk-Based Prioritization

> 📚 **Knowledge References** (loaded automatically):
> `qa-risk-patterns.md` — ISO 31000 risk framework, ISTQB risk-based testing, likelihood/impact matrices

Risk-based testing ensures the highest-risk areas get the most test coverage. Fail fast on what matters most.

## Step 1: Identify Risk Areas

Scan the codebase and ask:
```
1. What are the most business-critical features?
2. What changed most in this release?
3. What broke in previous releases?
4. What has the lowest test coverage now?
5. Any third-party integrations or external dependencies?
```

## Step 2: Build Risk Matrix

Score each area: **Likelihood** (1–4) × **Impact** (1–4) = **Risk Score**

```
| Feature / Area        | Likelihood | Impact | Score | Priority |
|-----------------------|------------|--------|-------|----------|
| Payment processing    | 2          | 4      | 8     | 🔴 High  |
| User authentication   | 2          | 4      | 8     | 🔴 High  |
| Search / filtering    | 3          | 2      | 6     | 🟡 Med   |
| Admin dashboard       | 1          | 3      | 3     | 🟢 Low   |
```

**Priority mapping:**
- Score 8–16 → 🔴 High — test every release, include in Tier 3 performance if critical
- Score 4–7  → 🟡 Medium — test on change
- Score 1–3  → 🟢 Low — test on major releases only

## Step 3: Map to Test Tiers

For each High-priority area, assign mandatory test coverage:

```
| Area               | Unit | Integration | E2E | Security | Load Test |
|--------------------|------|-------------|-----|----------|-----------|
| Payment processing | ✅   | ✅          | ✅  | ✅       | ✅ flag   |
| Authentication     | ✅   | ✅          | ✅  | ✅       | —         |
```

**Flag for Tier 3 Performance:** Areas with Score ≥ 8 AND high concurrent usage → add to `/helix test-perf-load` scope.

## Step 4: Output

Save to `docs/qa/qa-risk-YYYY-MM-DD.md`:
- Risk matrix table
- Priority list (High → Medium → Low)
- Tier 3 performance flags
- Recommended test execution order

## Done

Present risk matrix + flag list.
If any Tier 3 flags exist, remind user: run `/helix test-perf-load` separately with flagged endpoints.
Suggest next step: proceed with test execution tiers or `/helix qa-explore`

## Self-Evaluation Loop

```
1. Risk matrix ครอบคลุม business-critical features ไหม?
2. Score calculation สม่ำเสมอไหม?
3. Tier 3 flags สมเหตุสมผลไหม?
4. มี area ที่ลืมไปไหม?
```
