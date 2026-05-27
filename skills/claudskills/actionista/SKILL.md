---
description: >-
  Creates, debugs, and optimizes GitHub Actions workflow YAML files. Recommends
  current action versions with SHA pinning from a daily-updated index of 120+
  actions. Configures matrix builds, dependency caching, reusable workflows, OIDC
  authentication, secrets management, and runner selection. Reviews existing workflows for
  outdated actions, security issues, and performance problems. Use when the user
  asks about GitHub Actions, workflows, CI/CD, .github/workflows, any action by name
  (actions/checkout, setup-node, setup-python, etc.), or workflow optimization.
license: MIT
metadata:
  repository: https://github.com/claylo/actionista
  version: 1.0.1
name: actionista
---

# GitHub Actions Expertise

Comprehensive knowledge for creating, reviewing, and optimizing GitHub Actions workflows with current action versions and best practices.

## Environment

!`command -v actionlint 2>/dev/null && echo "actionlint: installed" || echo "actionlint: not installed"`
!`command -v act 2>/dev/null && echo "act: installed" || echo "act: not installed"`

If either tool is missing, suggest the user install them:
- `brew install actionlint` — workflow linter that catches syntax errors, type mismatches, and expression problems offline
- `brew install act` — runs workflows locally in Docker without pushing

## Quick Reference

### Action Versions

Consult `actions-index.json` in this skill directory for current versions of 120+ popular actions. The index is updated daily and organized by category.

**Always verify versions** before recommending — use the index or fetch from GitHub releases if needed.

### Core Patterns

| Pattern | When to Use | Reference |
|---------|-------------|-----------|
| Matrix builds | Test across versions/platforms | `references/patterns-matrix-builds.md` |
| Caching | Speed up dependency installation | `references/patterns-caching.md` |
| Artifacts | Share files between jobs | `references/patterns-artifacts.md` |
| Reusable workflows | Share workflows across repos | `references/patterns-reusable-workflows.md` |
| Concurrency | Prevent duplicate runs | `references/patterns-concurrency.md` |
| Environments | Deployment gates/approvals | `references/patterns-environments.md` |
| Composite actions | Create custom actions | `references/patterns-composite-actions.md` |

### Security Essentials

| Topic | Key Points | Reference |
|-------|------------|-----------|
| Secrets | Never hardcode, use OIDC when possible | `references/security-secrets.md` |
| Permissions | Principle of least privilege | `references/security-hardening.md` |
| Supply chain | Pin actions, review dependencies | `references/security-supply-chain.md` |

## Workflow Essentials

Every workflow should include these often-missed fields:

```yaml
permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
```

Full JSON Schema for workflow validation: `references/github-action.schema.json`

## Essential Workflow Patterns

### Dependency Caching

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

For custom caching, see `references/patterns-caching.md`.

### Matrix Strategy

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node: [18, 20, 22]
    exclude:
      - os: windows-latest
        node: 18
    include:
      - os: ubuntu-latest
        node: 20
        coverage: true
```

### Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    needs: build
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps: [...]
```

For conditional execution patterns (`if:`, `always()`, `failure()`), trigger event configuration, and expression syntax, see `references/triggers.md` and `references/expressions.md`.

## Security Best Practices

### Minimal Permissions

```yaml
permissions:
  contents: read

jobs:
  build:
    permissions:
      contents: read

  deploy:
    permissions:
      contents: read
      id-token: write
      packages: write
```

### Pin Action Versions

```yaml
# Good: Pin to full SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1

# Acceptable: Pin to major version
- uses: actions/checkout@v6

# Bad: Unpinned or floating
- uses: actions/checkout@main
- uses: actions/checkout
```

### OIDC for Cloud Authentication

Prefer OIDC over long-lived credentials. See `references/security-secrets.md` for setup guides for AWS, GCP, and Azure.

When reviewing workflows, generate an ASCII flowchart showing job dependencies.

## Validating Workflows

Before pushing workflow changes, verify correctness:

1. **Lint with actionlint** — catches syntax errors, type mismatches, and expression problems that YAML parsers miss:
   ```bash
   actionlint .github/workflows/*.yml
   ```

2. **Test locally with `act`** — runs workflows in Docker without pushing:
   ```bash
   act push --job build
   act pull_request -e event.json
   ```

3. **Check workflow run logs** — after pushing, verify in the Actions tab:
   - Confirm expected jobs triggered
   - Check for deprecation warnings in logs
   - Verify caching is hitting (`cache hit: true`)

4. **Validate secrets access** — workflows fail silently when secrets are missing. Verify required secrets exist in repo/org settings before relying on them.

## Workflow Analysis Checklist

When reviewing workflows, check:

### Versions
- [ ] All actions use current major versions (consult `actions-index.json`)
- [ ] Consider pinning to SHA for security-critical workflows
- [ ] No deprecated action versions

### Performance
- [ ] Dependencies are cached appropriately
- [ ] Parallel jobs where dependencies allow
- [ ] `timeout-minutes` set to prevent runaway jobs
- [ ] `fail-fast: false` if matrix jobs are independent

### Security
- [ ] Minimal `permissions` declared
- [ ] No secrets in logs (`add-mask` for dynamic secrets)
- [ ] OIDC preferred over long-lived credentials
- [ ] Third-party actions reviewed for security

### Reliability
- [ ] `concurrency` configured to prevent duplicate runs
- [ ] Conditional execution (`if:`) used appropriately
- [ ] `continue-on-error` only where truly needed
- [ ] Retry logic for flaky external calls

### Maintainability
- [ ] Descriptive job and step names
- [ ] Reusable workflows for shared logic
- [ ] Environment variables for repeated values
- [ ] Comments for complex logic

## Additional Resources

All reference files are in `references/`:

| File | Topic |
|------|-------|
| `workflow-syntax.md` | Complete workflow YAML reference |
| `expressions.md` | Expression syntax, contexts, functions |
| `triggers.md` | All event triggers with examples |
| `runners.md` | Runner selection, self-hosted setup |
| `permissions.md` | GITHUB_TOKEN scopes, OIDC setup |
| `troubleshooting.md` | Common errors and solutions |
| `patterns-matrix-builds.md` | Matrix strategies, include/exclude |
| `patterns-caching.md` | Cache action, custom keys, restore strategies |
| `patterns-artifacts.md` | Upload/download, retention, cross-job sharing |
| `patterns-reusable-workflows.md` | workflow_call, inputs, secrets |
| `patterns-concurrency.md` | Groups, cancel-in-progress |
| `patterns-environments.md` | Deployment environments, protection rules |
| `patterns-composite-actions.md` | Creating custom actions |
| `security-secrets.md` | Management, rotation, OIDC setup |
| `security-hardening.md` | Permissions, pinning, CodeQL |
| `security-supply-chain.md` | Dependency review, Dependabot |

Working templates in `examples/`: `ci-node.yaml`, `ci-rust.yaml`, `deploy-aws.yaml`, `release-please.yaml`

- **`actions-index.json`** — Current versions of 120+ popular actions (updated daily)
- **`tracked-actions.yaml`** — List of tracked actions by category
