---
name: premerge
description: "Run all review skills (self, SOLID, test coverage, security, docs), merge findings, apply auto-fixes, generate unified summary. Triggers: 'premerge', 'pre-merge', 'full review', 'review everything', 'pre-push', 'check all'."
---

# Pre-Merge Review Skill

Orchestrate all reviews before merging. Fix what's fixable. Report the rest.

## Autonomous Operation Philosophy

This skill operates as an **autonomous orchestrator** that:
1. Runs all sub-skills with minimal human intervention
2. Coordinates cross-skill collaboration automatically
3. Applies safe fixes without asking
4. Only prompts for decisions that truly require human judgment
5. Produces a complete, actionable report

**Goal**: Developer invokes `/premerge`, goes to get coffee, comes back to a clean codebase or a clear list of what needs manual attention.

## What This Does

1. **Interactive scope selection** - Choose commits or review entire working tree
2. Run all sub-skills in parallel with scope context
3. **Facilitate skill collaboration** - Skills share findings and coordinate fixes
4. Merge and deduplicate findings
5. Prioritize by severity × impact
6. **Apply all safe auto-fixes automatically**
7. **Run collaboration round** - Let skills respond to each other's findings
8. Verify/update documentation accuracy
9. Generate `summary.json` with complete audit trail
10. Present unified verdict with clear next steps

## Workflow

### Step 0: Interactive Scope Selection

Present user with review scope options:

```bash
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

# Get commit options
COMMITS=$(git log --oneline ${MAIN_BRANCH}..HEAD 2>/dev/null | head -20)
COMMIT_COUNT=$(echo "$COMMITS" | wc -l | tr -d ' ')

# Get changed files in working tree
CHANGED_FILES=$(git diff --name-only 2>/dev/null)
CHANGED_COUNT=$(echo "$CHANGED_FILES" | grep -v '^$' | wc -l | tr -d ' ')

# Get untracked files
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null)
UNTRACKED_COUNT=$(echo "$UNTRACKED" | grep -v '^$' | wc -l | tr -d ' ')
```

**Interactive Prompt** (use AskUserQuestion tool):

```
What scope should we review?

Options:
1. "Last commit" - Review HEAD only
2. "Last N commits" - Review recent commits (specify N)
3. "All commits since ${MAIN_BRANCH}" - Review all ${COMMIT_COUNT} commits on this branch
4. "Changed files in working tree" - Review ${CHANGED_COUNT} modified files (unstaged/staged)
5. "Entire repository" - Full codebase review (slowest, most thorough)

Recommended: Option 3 for feature branches, Option 5 for initial reviews
```

Based on selection, set scope variables:

```bash
# Option 1: Last commit
SCOPE="commit"
SCOPE_TARGET="HEAD"
FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

# Option 2: Last N commits
SCOPE="commits"
SCOPE_TARGET="HEAD~N..HEAD"
FILES=$(git diff-tree --no-commit-id --name-only -r HEAD~N..HEAD)

# Option 3: All commits since main
SCOPE="branch"
SCOPE_TARGET="${MAIN_BRANCH}..HEAD"
FILES=$(git diff --name-only ${MAIN_BRANCH}..HEAD)

# Option 4: Changed files
SCOPE="working-tree"
SCOPE_TARGET="working-tree"
FILES=$(git diff --name-only && git ls-files --others --exclude-standard)

# Option 5: Entire repository
SCOPE="full"
SCOPE_TARGET="all"
FILES=$(find . -type f -name "*.java" -o -name "*.md" -o -name "*.properties" -o -name "*.yaml" | grep -v target | grep -v node_modules)
```

Write scope to temp file for skills to consume:

```bash
mkdir -p .review-output

cat > .review-output/scope.json <<EOF
{
  "scope": "${SCOPE}",
  "target": "${SCOPE_TARGET}",
  "files": [$(echo "$FILES" | sed 's/.*/"&"/' | paste -sd,)],
  "fileCount": $(echo "$FILES" | wc -l),
  "branch": "${BRANCH}",
  "mainBranch": "${MAIN_BRANCH}",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
```

### Step 1: Context

Display selected scope:

```bash
SCOPE=$(jq -r '.scope' .review-output/scope.json)
TARGET=$(jq -r '.target' .review-output/scope.json)
FILE_COUNT=$(jq -r '.fileCount' .review-output/scope.json)
BRANCH=$(jq -r '.branch' .review-output/scope.json)

echo "=== Pre-Merge Review ==="
echo "Branch: $BRANCH"
echo "Scope: $SCOPE ($TARGET)"
echo "Files: $FILE_COUNT"
echo ""
```

### Step 2: Run Reviews (Parallel Phase)

Execute all review skills in parallel. Each reads `.review-output/scope.json`.

```bash
mkdir -p .review-output

# Pass scope to each skill via --scope-file flag or environment
export REVIEW_SCOPE_FILE=".review-output/scope.json"

# Run ALL skills in parallel using Task tool with multiple agents
# Each skill operates autonomously and writes its findings

# Skills invoked simultaneously:
#   self-review --scope-file scope.json
#   solid-review --scope-file scope.json
#   test-coverage --scope-file scope.json
#   security-review --scope-file scope.json
#   write-docs --scope-file scope.json
```

**Parallel Execution Strategy:**
- Launch all 5 skills as parallel Task agents
- Each skill operates independently on the scoped files
- Skills apply their own auto-fixes as they run
- Skills write collaboration requests for cross-skill issues

**Expected outputs (Phase 1):**
- `self-review.json` - commit hygiene, build, architecture, patterns
- `solid-review.json` - SOLID violations
- `test-coverage.json` - missing tests, quality
- `security-review.json` - vulnerabilities, OWASP checks, secrets
- `docs-review.json` - documentation accuracy, completeness
- `fixes-applied.json` - all auto-fixes applied by all skills

### Step 2.5: Skill Collaboration Round

After initial parallel run, process cross-skill collaboration requests.

```
┌─────────────────────────────────────────────────────────────────┐
│                    COLLABORATION FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐     flags security      ┌─────────────────┐  │
│  │ self-review  │ ──────────────────────► │ security-review │  │
│  └──────────────┘     concern             └─────────────────┘  │
│         │                                          │            │
│         │ flags missing docs                       │            │
│         ▼                                          │            │
│  ┌──────────────┐                                  │            │
│  │  write-docs  │ ◄────────────────────────────────┘            │
│  └──────────────┘     requests security docs                    │
│         │                                                       │
│         │ updates API docs                                      │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │ test-coverage│ ◄── security-review requests security tests  │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Collaboration Protocol:**

1. **Collect collaboration requests** from all skill outputs:
```python
collaboration_requests = []
for report in ['self-review.json', 'security-review.json', ...]:
    requests = json.load(report).get('collaborationNeeded', [])
    collaboration_requests.extend(requests)
```

2. **Group by target skill**:
```python
by_skill = defaultdict(list)
for req in collaboration_requests:
    by_skill[req['targetSkill']].append(req)
```

3. **Execute collaboration actions**:

| Source Skill | Target Skill | Action |
|--------------|--------------|--------|
| self-review → security-review | New auth code flagged | Deep security scan of specific files |
| self-review → write-docs | New API endpoint | Generate endpoint documentation |
| security-review → write-docs | Security requirements | Add security notes to docs |
| security-review → test-coverage | Vulnerable code | Prioritize security test coverage |
| security-review → self-review | Critical vulnerability | BLOCK_MERGE signal |
| solid-review → write-docs | Architecture change | Update architecture docs |
| test-coverage → write-docs | Test gaps | Document testing requirements |

4. **Apply collaboration fixes**:
```bash
# write-docs responds to requests by generating docs
# security-review does deep-dive on flagged files
# test-coverage updates priority list
# All append to fixes-applied.json
```

**Scope-Aware Behavior:**
- **commit/commits/branch scope**: Only analyze files changed in selected commits
- **working-tree scope**: Only analyze modified and untracked files
- **full scope**: Analyze entire codebase

### Step 2.5: Documentation Verification

Run `write-docs` to verify documentation accuracy:
- Checks if docs match actual implementation
- Detects outdated information
- Identifies missing documentation
- Optionally updates docs (with confirmation)

```bash
# Check documentation health
# - README.md current?
# - API docs match endpoints?
# - Architecture docs accurate?
# - Setup instructions work?
```

If docs are stale, offer to update them before continuing review.

### Step 3: Merge Findings

Collect all findings, deduplicate by file+rule:

```python
# Pseudocode
all_findings = []
seen = set()

for report in ['self-review.json', 'solid-review.json', 'test-coverage.json', 'security-review.json', 'docs-review.json']:
    data = json.load(report)
    for finding in data.get('findings', []):
        key = f"{finding['file']}:{finding.get('line','')}:{finding['rule']}"
        if key not in seen:
            all_findings.append(finding)
            seen.add(key)

# Sort by severity
severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
all_findings.sort(key=lambda f: severity_order.get(f['severity'], 99))
```

### Step 4: Autonomous Fix Application

**Philosophy**: If a fix is mechanical and doesn't change behavior, just do it. Don't ask.

#### Tier 1: Apply Automatically (No Confirmation)

These fixes are applied immediately without user interaction:

| Category | Issue | Fix |
|----------|-------|-----|
| **Code Style** | Missing `final` on `@Inject` | Add `final` modifier |
| **Code Style** | Missing `@Override` | Add annotation |
| **Code Style** | Import organization | Sort and remove unused |
| **Code Style** | Trailing whitespace | Remove |
| **Types** | Concrete collection types | `ArrayList` → `List` |
| **Types** | Raw generic types | Add type parameters |
| **Security** | `printStackTrace()` | Replace with logger |
| **Security** | Missing `@Valid` on DTOs | Add validation |
| **Docs** | Outdated endpoint paths | Update automatically |
| **Docs** | Stale config references | Correct from code |

#### Tier 2: Apply and Report (Inform User)

These fixes are applied, then reported for awareness:

| Category | Issue | Fix | Why Report |
|----------|-------|-----|------------|
| **Security** | Weak BCrypt cost | Upgrade to 12 | Performance impact |
| **Security** | Missing rate limit | Add sensible default | May need tuning |
| **Architecture** | Public → package-private | Reduce visibility | API change |
| **Testing** | Test file renamed | Update to match prod | Verify coverage |

#### Tier 3: Require Confirmation

Only ask for these significant decisions:

| Issue | Why Ask |
|-------|---------|
| Architecture boundary violation | May be intentional design |
| Missing tests for complex logic | Need to understand requirements |
| Security vulnerability with multiple fix options | Trade-offs to consider |
| Breaking API changes | External consumers affected |
| Removing deprecated code | May have hidden dependencies |

### Step 5: Coordinated Fix Execution

Fixes are applied in a coordinated manner across all skills:

```bash
# 1. Read all fixes from all skills
cat .review-output/*/fixes-to-apply.json | jq -s 'flatten'

# 2. Deduplicate (same file+line from multiple skills)
# Security-review has priority for security fixes
# self-review has priority for style fixes

# 3. Apply in order: security → architecture → style → docs
for fix in $(jq -r '.[] | @base64' fixes.json); do
  apply_fix "$fix"
  log_fix "$fix" >> .review-output/fixes-applied.json
done

# 4. Re-run build to verify fixes don't break anything
./build.sh build 2>&1 | tee /tmp/post-fix-build.log

# 5. If build fails, rollback last fix and report
if [[ $? -ne 0 ]]; then
  git checkout -- "$last_fixed_file"
  echo "Fix caused build failure, rolled back"
fi
```

**Fix Conflict Resolution:**

When multiple skills want to fix the same code:

| Conflict | Resolution |
|----------|------------|
| security vs style | Security wins |
| security vs docs | Security wins |
| architecture vs style | Architecture wins |
| self-review vs solid-review | More specific fix wins |

**Post-Fix Verification:**
- Re-run build after all fixes
- Run affected tests if available
- Verify no new issues introduced

### Step 6: Generate summary.json

```json
{
  "meta": {
    "commit": "abc1234",
    "branch": "feature/auth",
    "reviewedAt": "2026-01-31T12:00:00Z",
    "scope": "branch",
    "scopeTarget": "main..HEAD",
    "skillsRun": ["self-review", "solid-review", "test-coverage", "security-review", "write-docs"],
    "autonomousMode": true
  },
  "build": {
    "passed": true,
    "exitCode": 0,
    "fixedDuringReview": true,
    "buildFixesApplied": 2
  },
  "findings": {
    "total": 15,
    "beforeFixes": 28,
    "afterFixes": 15,
    "autoFixed": 13,
    "critical": 0,
    "high": 3,
    "medium": 8,
    "low": 4,
    "byCategory": {
      "architecture": 2,
      "solid": 5,
      "testing": 4,
      "documentation": 2,
      "patterns": 2,
      "security": 6
    }
  },
  "fixes": {
    "tier1Applied": 10,
    "tier2Applied": 3,
    "tier3Pending": 2,
    "total": 13,
    "bySkill": {
      "self-review": 5,
      "security-review": 4,
      "write-docs": 3,
      "solid-review": 1
    },
    "details": [
      {
        "file": "UserService.java",
        "line": 15,
        "fix": "Added final to @Inject field",
        "skill": "self-review",
        "tier": 1
      }
    ]
  },
  "collaboration": {
    "requestsSent": 5,
    "requestsProcessed": 5,
    "crossSkillFixes": 3,
    "details": [
      {
        "from": "self-review",
        "to": "write-docs",
        "reason": "New endpoint needs documentation",
        "status": "completed",
        "result": "Added API docs for POST /api/matches"
      },
      {
        "from": "security-review",
        "to": "self-review",
        "reason": "Critical: SQL injection in UserRepository",
        "status": "completed",
        "result": "BLOCK_MERGE signal sent"
      }
    ]
  },
  "coverage": {
    "testFilePercent": 85,
    "criticalMissing": ["PaymentService.java"],
    "securityTestsCoverage": 75
  },
  "documentation": {
    "accuracy": 95,
    "completeness": 90,
    "filesUpdated": ["api-reference.md", "architecture.md"],
    "staleFilesFixed": ["README.md"],
    "remainingGaps": []
  },
  "grades": {
    "overall": "B",
    "build": "A",
    "architecture": "A",
    "solid": "C",
    "testing": "B",
    "documentation": "A",
    "security": "B"
  },
  "topIssues": [
    {
      "priority": 1,
      "severity": "high",
      "category": "testing",
      "file": "PaymentService.java",
      "description": "Critical service missing tests",
      "action": "Add PaymentServiceTest.java",
      "autoFixable": false,
      "requiresHuman": true
    },
    {
      "priority": 2,
      "severity": "high",
      "category": "solid",
      "file": "UserService.java",
      "description": "SRP violation - 12 dependencies",
      "action": "Split into focused services",
      "autoFixable": false,
      "suggestedRefactoring": "Extract UserAuthService and UserProfileService"
    }
  ],
  "verdict": {
    "canPush": false,
    "blockers": ["1 critical service missing tests"],
    "warnings": ["SOLID violations in UserService"],
    "humanDecisionsNeeded": 2,
    "estimatedManualWork": "30 minutes"
  },
  "auditTrail": {
    "startTime": "2026-01-31T12:00:00Z",
    "endTime": "2026-01-31T12:03:45Z",
    "duration": "3m45s",
    "phases": [
      {"phase": "scope-selection", "duration": "5s"},
      {"phase": "parallel-review", "duration": "2m30s"},
      {"phase": "collaboration", "duration": "45s"},
      {"phase": "fix-application", "duration": "20s"},
      {"phase": "verification", "duration": "5s"}
    ]
  }
}
```

### Step 7: Present Summary

```markdown
## Full Review Summary

**Commit**: abc1234 (feature/auth)  
**Overall Grade**: B

### Build
✓ Passed

### Findings
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 3 |
| Medium | 8 |
| Low | 4 |

### Auto-Fixes Applied
✓ 3 fixes applied (missing final, @Override)

### By Category
| Category | Findings | Grade |
|----------|----------|-------|
| Architecture | 2 | A |
| SOLID | 5 | C |
| Testing | 4 | B |
| Documentation | 2 | B |
| Security | 6 | C |

### Top Issues to Address

1. **[HIGH/testing]** PaymentService.java missing tests
   → Add PaymentServiceTest.java

2. **[HIGH/solid]** UserService.java has 12 dependencies  
   → Split into UserAuthService + UserProfileService

3. **[HIGH/solid]** OrderProcessor uses instanceof chain
   → Refactor to strategy pattern

### Test Coverage
- File coverage: 85%
- Critical missing: PaymentService.java

### Documentation
- Accuracy: 90% (mostly correct)
- Completeness: 85% (minor gaps)
- Stale: README.md (mentions old endpoint)
- Missing: Control Plane service docs

### Verdict
⚠ **Address 1 blocker before push**
- PaymentService needs tests (critical business logic)

---
Report saved to `summary.json`
```

## Grading Logic

**Overall Grade** = weighted average:
- Build: 15% (pass/fail)
- Security: 25%
- Architecture: 15%
- SOLID: 15%
- Testing: 20%
- Documentation: 10%

**Can Push** criteria:
- Build passes
- No critical security findings
- No critical/high security vulnerabilities (injection, auth bypass)
- No hardcoded secrets in production code
- No high findings in architecture
- All critical services have tests
- Documentation is reasonably current (accuracy ≥80%)

## Arguments

- `--scope <commit|branch|working-tree|full>` - Pre-select scope (skip interactive prompt)
- `--commits <N>` - Review last N commits (implies --scope commits)
- `--since <ref>` - Review changes since ref (e.g., --since main)

**Examples:**
```bash
/premerge                    # Interactive scope selection
/premerge --scope full       # Full repo review
/premerge --commits 3        # Last 3 commits
/premerge --since main       # All changes since main
/premerge --scope working-tree  # Only modified files
```

## Integration with learn

After premerge review, if significant issues were found/fixed, suggest:

```
Want me to update CLAUDE.md with what we learned?
- Gotcha: PaymentService needs careful testing
- Pattern: UserService should be split
```

## Integration with write-docs

If documentation is stale or inaccurate (score <80%), prompt:

```
Documentation needs updates:
- README.md mentions deprecated endpoint
- Control Plane service not documented

Run write-docs to fix? [y/N]
```

If confirmed, run write-docs skill to update documentation before completing review.

## Scope Flow

```
┌─────────────────────┐
│  User invokes       │
│  /premerge          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Interactive        │
│  Scope Selection    │
│  (or --scope flag)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Write scope.json   │
│  with file list     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Run skills in parallel:            │
│  • self-review (reads scope.json)   │
│  • solid-review (reads scope.json)  │
│  • test-coverage (reads scope.json) │
│  • security-review (reads scope.json)│
│  • write-docs (reads scope.json)    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Merge findings     │
│  Apply fixes        │
│  Generate summary   │
└─────────────────────┘
```
