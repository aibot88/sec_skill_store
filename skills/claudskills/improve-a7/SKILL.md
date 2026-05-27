---
name: improve-a7
description: Improve adoption criterion A7 (Proactive Quality Management) by configuring automated dependency updates, security scanning, and agent-driven tech debt PRs. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve A7 — Proactive Quality Management

## Current State

### Dependency update automation
!`ls .github/dependabot.yml 2>/dev/null && echo "(dependabot configured)" || echo "(no dependabot)"`
!`cat .github/dependabot.yml 2>/dev/null | head -20 || echo "(no dependabot config)"`
!`ls renovate.json .renovaterc .renovaterc.json 2>/dev/null && echo "(renovate configured)" || echo "(no renovate)"`

### Security scanning workflows
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -l "codeql\|snyk\|trivy\|audit\|security\|vulnerability" 2>/dev/null || echo "(no security workflows)"`
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -h "codeql\|snyk\|trivy\|npm audit\|pip-audit" 2>/dev/null | head -10 || echo "(no security scan steps)"`

### Tech debt / quality scheduled workflows
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -l "schedule" 2>/dev/null | xargs grep -l "lint\|debt\|refactor\|todo\|fixme\|quality" 2>/dev/null || echo "(no scheduled quality workflows)"`

### Evidence of bot/agent PRs for quality work
!`git log --since="90 days ago" --format="%s" 2>/dev/null | grep -i "bump\|update dep\|security\|vulnerability\|cve\|renovate\|dependabot" | head -10 || echo "(no automated quality PRs found)"`

### Package manager (to tailor dependency update config)
!`ls package.json pyproject.toml pom.xml go.mod Cargo.toml requirements.txt 2>/dev/null | head -5 || echo "(no package manifest)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No proactive quality management by agents; quality work is entirely human-initiated
- Level 1: Agents run quality checks (security scans, dependency audits) when explicitly asked by a developer
- Level 2: Agents automatically flag or report tech debt, security issues, and dependency updates, but do not open PRs to fix them
- Level 3: Agents proactively open PRs for tech debt reduction, dependency updates, security remediations, and standards enforcement without human initiation

**Assessment guide:**
- No automated quality tooling → Level 0
- Quality checks in CLAUDE.md or skills but only on request → Level 1
- Security scan workflows or scheduled reports that flag issues but no auto-PRs → Level 2
- Dependabot/Renovate active AND scheduled agent-driven PRs for tech debt → Level 3

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add quality check commands to CLAUDE.md so developers know to ask agents to run them:

```markdown
## Quality Checks

Run these checks before submitting a PR:

```bash
# Dependency audit (pick the relevant one):
npm audit                     # Node.js
pip-audit                     # Python (pip install pip-audit)
cargo audit                   # Rust (cargo install cargo-audit)
mvn dependency:analyze        # Java/Maven

# Static analysis:
npx eslint . --ext .js,.ts    # JavaScript/TypeScript
ruff check .                  # Python
golangci-lint run             # Go

# Dependency freshness:
npm outdated                  # Node.js
pip list --outdated           # Python
```

When asked to "do a quality check", run the relevant commands for this project and report findings.
```

**If current level is 1 → raise to 2:**
Create scheduled workflows that automatically scan and report findings (but do not auto-create fix PRs yet):

1. **Dependency audit report** — Create `.github/workflows/dependency-audit.yml`:
```yaml
name: Dependency Audit
on:
  schedule:
    - cron: '0 8 * * 1'  # Every Monday at 8am
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Run dependency audit
        id: audit
        continue-on-error: true
        run: |
          # Adjust for your package manager:
          if [ -f package.json ]; then
            npm ci --prefer-offline 2>/dev/null || npm install
            RESULT=$(npm audit --json 2>/dev/null || echo '{}')
            VULN_COUNT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('metadata',{}).get('vulnerabilities',{}).get('total', 0))" 2>/dev/null || echo "unknown")
          elif [ -f requirements.txt ]; then
            pip install pip-audit -q
            VULN_COUNT=$(pip-audit -r requirements.txt --format json 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "unknown")
          else
            VULN_COUNT="unknown (no supported package manager)"
          fi
          echo "vuln_count=$VULN_COUNT" >> $GITHUB_OUTPUT
          echo "Vulnerabilities found: $VULN_COUNT"

      - name: Create issue if vulnerabilities found
        if: steps.audit.outputs.vuln_count != '0'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create \
            --title "Weekly dependency audit: ${{ steps.audit.outputs.vuln_count }} vulnerability/vulnerabilities found" \
            --body "Automated dependency audit found issues.
          
          Run \`npm audit\` (or equivalent) locally for details.
          
          Add label \`agent-implement\` to trigger automated remediation." \
            --label "security,dependencies"
```

2. **Outdated dependencies report** — Create `.github/workflows/dependency-freshness.yml`:
```yaml
name: Dependency Freshness
on:
  schedule:
    - cron: '0 9 1 * *'  # First day of each month
  workflow_dispatch:

jobs:
  check-outdated:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4
      - name: Check outdated packages
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          if [ -f package.json ]; then
            npm install -q
            OUTDATED=$(npm outdated --parseable 2>/dev/null | wc -l || echo 0)
            if [ "$OUTDATED" -gt 0 ]; then
              gh issue create \
                --title "Monthly dependency check: $OUTDATED outdated packages" \
                --body "$(npm outdated 2>/dev/null || echo 'Run npm outdated for details')" \
                --label "dependencies"
            fi
          fi
```

**If current level is 2 → raise to 3:**
Enable automated PR creation for dependency updates and add an agent-driven tech debt workflow:

1. **Configure Dependabot** for automated dependency update PRs. Create `.github/dependabot.yml`:

Detect package manager from evidence above and use the appropriate config:

```yaml
version: 2
updates:
  # For Node.js projects:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "automated"
    commit-message:
      prefix: "chore"

  # For Python projects — replace npm block with:
  # - package-ecosystem: "pip"
  #   directory: "/"
  #   schedule:
  #     interval: "weekly"

  # For Docker images:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "automated"

  # For GitHub Actions:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "automated"
```

2. **Agent-driven tech debt PRs** — Create `.github/workflows/agent-tech-debt.yml`:
```yaml
name: Agent Tech Debt
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday morning
  workflow_dispatch:

jobs:
  tech-debt:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Find tech debt items
        id: debt
        run: |
          TODO_COUNT=$(grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | wc -l || echo 0)
          echo "todo_count=$TODO_COUNT" >> $GITHUB_OUTPUT
          echo "Tech debt items: $TODO_COUNT"

      - name: Implement one tech debt item
        if: steps.debt.outputs.todo_count != '0'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          ITEMS=$(grep -rn "TODO\|FIXME" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . 2>/dev/null | grep -v node_modules | head -5)
          echo "Tech debt items found:"
          echo "$ITEMS"
          # Configure agent invocation:
          # claude --print "Fix one of these TODO/FIXME items: $ITEMS. Create a PR."
          echo "Configure ANTHROPIC_API_KEY secret and agent invocation"
```

3. Update CLAUDE.md:
```markdown
## Proactive Quality Management

Automated quality management is configured:

- **Dependabot** (`.github/dependabot.yml`): Opens PRs weekly for outdated npm/pip/docker/actions dependencies
- **Dependency Audit** (weekly): Creates issues when vulnerabilities are found
- **Tech Debt** (weekly): Agent opens PRs to fix TODO/FIXME items

To label a dependency PR for automated merging: add `automerge` label and configure a branch protection rule.
To disable a specific update: edit `.github/dependabot.yml` or add `ignore` rules.
```

**If already at level 3:**
Report that A7 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level.
