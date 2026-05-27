---
name: pre-commit-guard
description: Use before any git commit or PR. Runs format/lint/typecheck/tests, checks for secrets/large files/debug statements, validates commit message. Triggers готов к commit, проверь перед commit, можно ли пушить, ready to merge.
allowed-tools: [Bash, Read]
model: sonnet
---

# Pre-Commit Guard

## Sequence (fail fast — stop on first error)

### 1. Stage check
```bash
git status -s
git diff --cached --stat
```

### 2. Secret scan
```bash
git diff --cached | grep -iE '(api[_-]?key|secret|password|token|bearer)\s*[=:]\s*["'"'"'][^"'"'"']{8,}'
```
If gitleaks installed:
```bash
gitleaks detect --staged --no-banner
```

### 3. Large file check
```bash
git diff --cached --name-only | xargs -I{} sh -c '[ -f "{}" ] && [ $(stat -c%s "{}") -gt 1048576 ] && echo "WARN: {} > 1MB"'
```

### 4. Format
```bash
ruff format --check .
```

### 5. Lint
```bash
ruff check $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
```

### 6. Type check
```bash
mypy $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
```

### 7. Tests
```bash
pytest -x --ff --tb=short --timeout=60
```

### 8. Forbidden patterns
```bash
git diff --cached -U0 | grep -E '^\+.*(print\(|breakpoint\(|console\.log|debugger;)'
```

### 9. Commit message format
- `<type>(<scope>): <subject>` (max 50 chars)
- type ∈ {feat, fix, refactor, docs, test, chore, perf, build, ci}
- imperative mood, no period

## Output
Single status: ✓ all passed / ⚠ N warnings / ✗ M errors

## Hard rules
- NEVER auto-commit. Only verify and report.
- Run from project root only
- Stop on first ✗
