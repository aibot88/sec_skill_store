---
name: semgrep-sast
description: Semgrep SAST scanning for static analysis, vulnerability detection, and code quality enforcement. Integrates with the Semgrep MCP plugin for automated scanning.
---

# Semgrep SAST Scanning

## When to Use This Skill

- Running static analysis security testing (SAST) on source code
- Scanning for vulnerabilities, anti-patterns, and code quality issues
- Enforcing coding standards via custom Semgrep rules
- Supply chain security scanning for dependency vulnerabilities
- Pre-commit/pre-merge quality gates
- Integrating SAST into CI/CD pipelines

## Target Agents

- `cyber-sentinel` - Primary user for security vulnerability scanning
- `code-reviewer` - SAST pass during code reviews
- `qa-engineer` - Quality gate enforcement with automated scanning
- `automated-test-scripter` - Integrating SAST into test pipelines
- `devops-engineer` - CI/CD pipeline SAST integration

## Prerequisites

- Semgrep installed: `pip install semgrep` or `pipx install semgrep`
- Semgrep token configured: `semgrep login` (saves to `~/.semgrep/settings.yml`)
- Semgrep MCP plugin enabled in Claude Code

## Semgrep MCP Plugin Tools

The Semgrep plugin provides these MCP tools for automated scanning:

| Tool | Purpose |
|------|---------|
| `semgrep_scan` | Run Semgrep scan with default rules |
| `semgrep_findings` | Retrieve findings from a previous scan |
| `semgrep_scan_supply_chain` | Scan dependencies for known vulnerabilities |
| `semgrep_scan_with_custom_rule` | Scan with a user-defined Semgrep rule |
| `semgrep_rule_schema` | Get the schema for writing custom rules |
| `get_supported_languages` | List languages Semgrep can scan |
| `get_abstract_syntax_tree` | Get AST for a file (useful for rule development) |

## Scanning Workflows

### 1. Quick Security Scan

Run a default Semgrep scan on the current project:

```bash
# Via CLI
semgrep scan --config auto .

# Via MCP plugin (preferred in Claude Code)
# Use the semgrep_scan tool
```

### 2. Supply Chain / Dependency Scan

Check for known vulnerabilities in dependencies:

```bash
# Via CLI
semgrep ci --supply-chain

# Via MCP plugin
# Use the semgrep_scan_supply_chain tool
```

### 3. Custom Rule Scan

Write and apply custom rules for project-specific patterns:

```yaml
# Example: Detect hardcoded API keys
rules:
  - id: hardcoded-api-key
    patterns:
      - pattern: $KEY = "..."
      - metavariable-regex:
          metavariable: $KEY
          regex: (api_key|apikey|api_secret|secret_key|auth_token)
    message: "Hardcoded API key detected in $KEY"
    languages: [python, javascript, typescript]
    severity: ERROR
```

### 4. Language-Specific Scans

```bash
# Python security
semgrep scan --config p/python .

# JavaScript/TypeScript security
semgrep scan --config p/javascript .

# OWASP Top 10
semgrep scan --config p/owasp-top-ten .

# Secrets detection
semgrep scan --config p/secrets .
```

## Severity Interpretation

| Semgrep Severity | NoE Mapping | Action |
|-----------------|-------------|--------|
| ERROR | Critical | Must fix before merge |
| WARNING | Major | Should fix before merge |
| INFO | Minor | Fix when convenient |

## Integration with Quality Gates

### Pre-Merge Quality Gate

```bash
# Step 1: Lint (language-specific)
ruff check . || eslint . || rubocop

# Step 2: Semgrep SAST scan
semgrep scan --config auto --error .

# Step 3: Semgrep supply chain
semgrep ci --supply-chain

# Step 4: Tests
pytest || npm test || go test ./...

# Step 5: Dependency audit
pip-audit || npm audit || bundle audit
```

### CI/CD Integration (GitHub Actions)

```yaml
- name: Semgrep SAST Scan
  uses: semgrep/semgrep-action@v1
  with:
    config: >-
      p/default
      p/owasp-top-ten
      p/secrets
  env:
    SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
```

## Writing Custom Rules

Use the `semgrep_rule_schema` MCP tool to get the full schema, then write rules:

```yaml
rules:
  - id: rule-id
    pattern: <semgrep-pattern>
    message: "Description of issue"
    languages: [python]
    severity: WARNING
    metadata:
      category: security
      owasp: "A03:2021 - Injection"
```

### Common Pattern Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `pattern` | Exact match | `pattern: eval(...)` |
| `pattern-not` | Exclude match | `pattern-not: eval("literal")` |
| `pattern-either` | OR matching | Multiple patterns |
| `pattern-inside` | Context match | Inside a function/class |
| `metavariable-regex` | Regex on captures | Variable name patterns |

## Scan Output Interpretation

When reviewing Semgrep findings:

1. **Triage by severity** - ERROR findings first
2. **Check for false positives** - Review context around the finding
3. **Group related findings** - Same rule across multiple files indicates systemic issue
4. **Map to OWASP** - Use metadata.owasp field for compliance tracking
5. **Track over time** - Compare scan results across commits

## Project-Level Configuration

Create `.semgrep.yml` in project root for persistent configuration:

```yaml
# .semgrep.yml
rules:
  - p/default
  - p/owasp-top-ten
  - p/secrets

exclude:
  - tests/
  - node_modules/
  - vendor/
  - "*.min.js"

severity:
  - ERROR
  - WARNING
```

## Additional Resources

- [Semgrep Registry](https://semgrep.dev/explore) - Browse community rules
- [Semgrep Playground](https://semgrep.dev/playground) - Test rules online
- [Custom Rule Tutorial](https://semgrep.dev/docs/writing-rules/overview) - Write your own rules
