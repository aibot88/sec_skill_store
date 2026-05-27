---
name: ring:dev-frontend-performance
description: |
  Gate 6 of frontend development cycle — ensures Core Web Vitals compliance,
  Lighthouse performance score > 90, and bundle size within budget.
---

# Frontend Performance Testing (Gate 6)

## When to use
- Gate 6 (after E2E testing complete)
- Frontend development tasks requiring performance validation

## Skip when
- Not inside a frontend development cycle (ring:dev-cycle-frontend)
- Backend-only project with no UI components
- Task is documentation-only, configuration-only, or non-code
- Changes limited to test files, CI/CD, or non-rendered code

## Sequence
**Runs before:** ring:codereview
**Runs after:** ring:dev-frontend-e2e

## Related
**Complementary:** ring:dev-cycle-frontend, ring:qa-analyst-frontend


Performance is a feature. Budgets are enforced, not suggested.

**Block conditions:**
- LCP > 2.5s on any page = FAIL
- CLS > 0.1 on any page = FAIL
- INP > 200ms on any page = FAIL
- Lighthouse Performance < 90 = FAIL
- Bundle size increase > 10% without justification = FAIL

## Step 1: Validate Input

Required: `unit_id` (TASK id), `implementation_files`, `gate0_handoffs`.
Optional: `performance_baseline`, `gate5_handoff`.

## Step 2: Dispatch Frontend QA Analyst

```yaml
Task:
  subagent_type: "ring:qa-analyst-frontend"
  description: "Performance testing for {unit_id}"
  prompt: |
    ## Frontend Performance Gate

    unit_id: {unit_id}
    implementation_files: {implementation_files}

    Standards: Load via cached_standards or WebFetch:
    https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/frontend/testing-performance.md

    ## Required Checks

    ### 1. Core Web Vitals
    Measure on all changed pages (desktop + mobile):
    - LCP (Largest Contentful Paint): MUST be < 2.5s
    - CLS (Cumulative Layout Shift): MUST be < 0.1
    - INP (Interaction to Next Paint): MUST be < 200ms

    ### 2. Lighthouse Score
    ```bash
    npx lighthouse http://localhost:3000/{page} --output=json --quiet 2>/dev/null \
      | jq '.categories.performance.score * 100'
    ```
    Score MUST be > 90. Run on all affected pages.

    ### 3. Bundle Analysis
    ```bash
    npm run build 2>&1 | grep -E "Size|Gzipped|chunk"
    # Or: npx @next/bundle-analyzer
    ```
    Compare to baseline. Flag > 10% increase.

    ### 4. Client Component Audit
    ```bash
    grep -rn "'use client'" --include='*.tsx' --include='*.ts' src/ | wc -l
    ```
    Minimize 'use client' — prefer Server Components. Flag any new ones without justification.

    ### 5. Image Optimization
    ```bash
    grep -rn "<img " --include='*.tsx' src/ | grep -v "next/image"
    ```
    Zero bare `<img>` tags. All must use `next/image`.

    ## Performance Results Table (MANDATORY)
    | Page | LCP | CLS | INP | Lighthouse | Bundle Δ | Status |
    |------|-----|-----|-----|-----------|---------|--------|

    ## Output
    - Metrics table
    - Issues with severity
    - Optimization suggestions for any FAIL
```

## Step 3: Validate Results

```
if all pages pass all thresholds:
  → PASS → proceed to Gate 7

if any threshold exceeded:
  → Dispatch ring:frontend-engineer to optimize
  → Re-run performance test
  → iterations++

if iterations >= 3:
  → Escalate with full metrics report
```

## Output Format

```markdown
## Performance Testing Result
unit_id | result: PASS/FAIL | iterations

## Core Web Vitals
| Page | LCP | CLS | INP | Lighthouse | Status |

## Bundle Analysis
| Chunk | Before | After | Delta | Status |

## Issues
| Severity | Page | Metric | Value | Threshold |

## Handoff
gate6_result: PASS | ESCALATED
```
