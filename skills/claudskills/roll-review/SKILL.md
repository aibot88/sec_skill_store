---
hidden: true
name: roll-.review
license: MIT
model: sonnet
allowed-tools: "Read, Bash(git:*)"
description: Self code review step in the TCR workflow. Runs after each micro-step is completed and before commit, checking code quality, security, and design issues.
---

# WK Self Code Review

**Quality gate for the TCR loop** - Self-review after each micro-step is completed and before commit.

## Position in WK Workflow

```
TCR Loop:
  Write Test → Run Test → ✅ Green → Self Review → Commit
                                          ↓
                                     Critical?
                                   Yes → Fix → Redo
                                    No → Proceed
```

## When Triggered

- **Auto-triggered**: After each TCR micro-step in `$roll-build` / `$roll-fix`
- **Manual trigger**: When the user wants to review current changes

## When Not to Use

- Docs-only changes (README, CHANGELOG) with no code diff
- Test pyramid / coverage standards check (use `$roll-.qa`)
- Post-deploy production sampling (use `$roll-sentinel`)

## Review Scope

```bash
# Default: review staged changes (recommended for TCR)
$roll-.review staged

# Review all uncommitted changes
$roll-.review unstaged

# Review specific files
$roll-.review files src/utils.ts
```

## Review Dimensions (6 Core Dimensions)

```
┌─────────────────────────────────────────────────────────┐
│  WK Quality Checklist                                   │
├─────────────────────────────────────────────────────────┤
│  ✅ Correctness     - Logic is correct, no bugs         │
│  ✅ Security        - No vulnerabilities, input valid.  │
│  ✅ Maintainability - Clear naming, sound structure     │
│  ✅ Performance     - No performance pitfalls           │
│  ✅ Testability     - Easy to test, edge cases covered  │
│  ✅ Scope           - Focused on current task, no       │
│                       unrelated changes                 │
└─────────────────────────────────────────────────────────┘
```

## Severity Levels and Decisions

| Level | Definition | Decision |
|-------|-----------|----------|
| 🔴 **Critical** | Bug, security vulnerability | **Must fix**, redo TCR |
| 🟡 **Warning** | Maintainability issue | **Recommend fix** or document |
| 🟢 **Suggestion** | Minor optimization | Optional, proceed with commit |
| ✅ **Pass** | No issues | Proceed with commit |

## Output Format

```markdown
## Self Review Report
**Scope**: staged (2 files, +45/-12 lines)

### 🔴 Critical (Must Fix)
| File | Line | Issue | Action |
|------|------|-------|--------|
| auth.ts | 23 | SQL injection | Use parameterized query |

### 🟡 Warnings
- utils.ts:45 - Magic number, consider: `const MAX_RETRY = 3`

### ✅ Passed
- Naming conventions
- Error handling
```

## TCR Integration

In each micro-step of `$roll-build`:

```markdown
**Micro-Step X: [Description]**

1. Write/Update Test
2. Run Test → ✅ Green
3. **$roll-.review staged**
   - 🔴 Critical? → Fix → Redo step
   - 🟡 Warning? → Quick fix or document
   - ✅ Pass? → Proceed
4. git commit -m "tcr: description"
```

## WK Principle Alignment

- **Agent-First**: Structured review checklist, executable by AI
- **Check Phase**: Local quality control
- **Micro-steps**: Small fast steps, each review < 100 lines
- **TCR**: Can only commit after passing self-check, ensuring repo quality
