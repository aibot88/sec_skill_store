---
name: ultra-test
description: "Pre-delivery quality audit — Anti-Pattern + Coverage Gap + Wiring + E2E + Performance + Security. Writes .ultra/test-report.json; no state.db writes."
runtime: all
mcp_tools_required:
  - task.list
  - ask.question
cli_fallback: "task list"
---

# ultra-test — Phase 3.5

Project-level quality audit before `/ultra-deliver`. Auditors are orthogonal;
each writes a JSON gate result; the skill aggregates into `.ultra/test-report.json`.
This is **not** for running unit tests (that is `/ultra-dev`). This is the
pre-ship gate.

## Prerequisites

- `task.list` returns ≥1 task with `status=completed`
- Repo has test files (Step 0 pre-check)

## Workflow

### Step 0 — Pre-Execution

1. Detect project type from config (`package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` / …)
2. `task.list { status: "completed" }` → confirm ≥1 task delivered
3. Find test files (suffix `.test.*`, `.spec.*`, `test_*.py`, `*_test.go`)

Block with instructive error if any precheck fails.

### Step 1 — Anti-Pattern Detection

Detect fake / meaningless tests that waste CI time.

| Pattern | Example | Severity |
|---------|---------|----------|
| Tautology | `assert True`, `expect(true).toBe(true)` | CRITICAL |
| Empty test | function body is just `pass` / `{}` | CRITICAL |
| Core-logic mock | `jest.mock()` on domain/service/state files | CRITICAL |

Use Grep with language-appropriate regex; count matches per file.

**Gate**: any CRITICAL match → fail.

### Step 2 — Coverage Gap Analysis

Find exported functions / classes with **zero** test references.

1. Enumerate exports in `src/` (or language equivalent)
2. For each symbol, grep test files for its name
3. Bucket:
   - HIGH: core business logic untested
   - MEDIUM: utility untested
   - LOW: config/constant untested

**Output**: `.ultra/docs/test-coverage-gaps.md`
**Gate**: any HIGH → fail.

### Step 2.5 — Wiring Verification

Detect orphan code — files that exist and pass tests but are not reachable.

1. Enumerate exported symbols in source files
2. For each export, grep **non-test** source for imports
3. Report exports with 0 non-test imports as orphaned

Also check boundary wiring:
- Component → API (fetch/axios targets a real route)
- API → DB (handler imports a real client)
- Form → handler (onSubmit is not `() => {}`)
- State → render (state appears in JSX/template)

Stub detection (Level-2 substantive):
- Functions returning empty `[]` / `{}` without real work
- `console.log`-only bodies
- Handlers calling only `e.preventDefault()`
- Components returning only `<div>Placeholder</div>`

**Output**: append to `test-coverage-gaps.md` under `## Wiring Gaps`.
**Gate**: any HIGH orphan or stub → fail.

### Step 3 — E2E Testing (conditional)

**Trigger**: project has web UI or API endpoints.

1. Start dev server (detect `scripts.dev` / `scripts.start`)
2. Navigate key pages/endpoints
3. Verify elements render; check console errors
4. Exercise primary user flows

**Method per runtime**:
- Claude: `mcp__claude-in-chrome__*` or Playwright via Bash
- Others: Playwright via `npx playwright` (CLI portable)

**Gate**: critical pages fail / major errors → fail.

### Step 4 — Performance (conditional, frontend only)

Lighthouse on dev server. Core Web Vitals gates:
- LCP < 2.5s
- INP < 200ms
- CLS < 0.1

**Gate**: any metric above threshold → fail.

### Step 5 — Security Audit

Dependency vulnerability scan via project's native tool:
- `npm audit --json` / `pnpm audit --json` / `yarn audit --json`
- `cargo audit --json`
- `pip-audit --format=json`
- `govulncheck ./...`

**Severity**:
- Critical/High → fail
- Medium → warn
- Low → info

### Step 6 — Auto-Fix Loop

If any gate failed, loop (max 5 attempts):

1. Read `blocking_issues`
2. Fix what is fixable without user input:
   - Coverage Gap → write missing tests
   - Anti-Pattern → rewrite fake tests
   - E2E error → fix the code
   - Performance → code-level optimizations (lazy, splitting, memoization)
3. External blockers (upstream CVE, breaking dep bump) → break, report, ask user
4. If all gates pass → exit loop

If max reached → surface remaining issues; `passed=false`.

### Step 7 — Persist `.ultra/test-report.json`

```jsonc
{
  "timestamp": "<ISO8601>",
  "git_commit": "<HEAD>",
  "passed": true,
  "run_count": 1,
  "gates": {
    "anti_pattern":  { "passed": true, "critical": 0, "warning": 1 },
    "coverage_gaps": { "passed": true, "high": 0, "medium": 3, "low": 5 },
    "wiring":        { "passed": true, "orphans": 0, "stubs": 0 },
    "e2e":           { "passed": true, "skipped": false },
    "performance":   { "passed": true, "lcp": 1.8, "inp": 150, "cls": 0.05 },
    "security":      { "passed": true, "critical": 0, "high": 0, "medium": 2 }
  },
  "blocking_issues": []
}
```

Rules:
- File exists → increment `run_count`
- `passed = true` iff all gates `.passed === true`
- `blocking_issues` lists human-readable strings for any fail

### Step 8 — Report

Print a compact summary (emoji-free, ≤20 lines). Suggest `/ultra-deliver` only
when `passed=true`.

## Quality Gates — summary

| Gate | Requirement |
|------|-------------|
| Anti-Pattern | 0 critical |
| Coverage Gaps | 0 HIGH |
| Wiring | 0 HIGH orphan, 0 HIGH stub |
| E2E | all flows pass (if applicable) |
| Performance | all Core Web Vitals (if frontend) |
| Security | 0 critical/high |

## MCP → CLI fallback matrix

| Purpose | MCP tool | CLI fallback |
|---------|----------|--------------|
| Confirm ≥1 completed task | `task.list { status: "completed" }` | `ultra-tools task list --status completed` |
| Confirm risky auto-fix | `ask.question` | Claude: `AskUserQuestion`; CLI: `ultra-tools ask --question …` |

## What this skill DOES NOT do

- Does NOT run unit tests (that is `/ultra-dev`)
- Does NOT mutate state.db (auditing is read-only against state)
- Does NOT release or tag (that is `/ultra-deliver`)

## Integration

| | |
|---|---|
| **Input** | Source + test files, state.db (read-only) |
| **Output** | `.ultra/test-report.json`, `.ultra/docs/test-coverage-gaps.md` |
| **Next** | `/ultra-deliver` (only when `passed=true`) |
