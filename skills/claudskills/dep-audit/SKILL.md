---
description: Audit npm dependencies across all package.json files — reports outdated, security issues, and unused packages
argument-hint: [--fix] — pass --fix to auto-update safe (patch/minor) upgrades
---

# Dependency Audit

Request: $ARGUMENTS

## Context

- Root package.json: !`cat /Users/danilo/www/vida/package.json | node -p "const p=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); JSON.stringify({...p.dependencies,...p.devDependencies}, null, 2)"`
- Frontend deps: !`node -p "const p=require('/Users/danilo/www/vida/frontend/package.json'); JSON.stringify({...p.dependencies,...p.devDependencies}, null, 2)"`
- Backend deps: !`node -p "const p=require('/Users/danilo/www/vida/backend/package.json'); JSON.stringify({...p.dependencies,...p.devDependencies}, null, 2)"`

## Your task

### Step 1 — Check for outdated packages

```bash
cd /Users/danilo/www/vida && npm outdated --json 2>/dev/null
cd /Users/danilo/www/vida/frontend && npm outdated --json 2>/dev/null
cd /Users/danilo/www/vida/backend && npm outdated --json 2>/dev/null
```

### Step 2 — Security audit

```bash
cd /Users/danilo/www/vida && npm audit --json 2>/dev/null
cd /Users/danilo/www/vida/frontend && npm audit --json 2>/dev/null
cd /Users/danilo/www/vida/backend && npm audit --json 2>/dev/null
```

### Step 3 — Report

Produce a table grouped by severity:

**Security vulnerabilities:**
| Package | Severity | Vulnerability | Fix available |
|---------|----------|--------------|---------------|
| some-pkg | high | CVE-2024-XXXX | upgrade to 2.1.0 |

**Outdated packages:**
| Package | Location | Current | Wanted | Latest | Type |
|---------|----------|---------|--------|--------|------|
| react | frontend | 18.2.0 | 18.2.0 | 19.1.0 | major |
| vite | frontend | 5.0.0 | 5.4.2 | 6.3.5 | minor→patch |

Categorize each update as:
- `patch` — safe to update immediately
- `minor` — review changelog, likely safe
- `major` — breaking changes, requires careful upgrade

### Step 4 — Auto-fix (if --fix passed)

If $ARGUMENTS contains `--fix`, apply safe patch and minor updates:
```bash
cd /Users/danilo/www/vida/frontend && npm update
cd /Users/danilo/www/vida/backend && npm update
```

Then re-run `npm run check && npm run test` for both to verify nothing broke.

### Step 5 — Summary

```
Security: X critical, X high, X moderate, X low
Outdated: X packages across 3 workspaces
  X patch updates (safe to apply now)
  X minor updates (review changelog)
  X major updates (require planning)
```

For critical/high vulnerabilities, open a GitHub issue using `mcp__github__issue_write` with label `infra`.
