---
name: scitex-audit
description: Unified repo security scanner for scientific Python projects — one call orchestrates `bandit` (Python AST security linter), `shellcheck` (shell-script linter), `pip-audit` (Python dependency CVE scanner), and GitHub Security Advisory alerts, merging their findings into a single JSON report. Public API (1 symbol) — `audit(path: str = ".", checks: Optional[list[str]] = None, output_file: Optional[str] = None) -> dict` (`checks` picks a subset of backends; with `None` runs all available; returns `{checker: [findings]}`; optionally writes JSON to `output_file`). CLI entry — `scitex audit [path] [--checks bandit,shellcheck,pip-audit,github] [--output report.json]` (via parent `scitex` CLI). No MCP tools. Drop-in replacement for manually running `bandit -r .` + `shellcheck **/*.sh` + `pip-audit` + `gh api /repos/.../vulnerability-alerts` and stitching together four output formats, or configuring each tool separately in CI. Use whenever the user asks to "audit this repo for security issues", "run bandit on this project", "check Python deps for CVEs with pip-audit", "lint shell scripts with shellcheck", "merge security scan results into one report", "pull GitHub security advisories", or mentions `scitex audit`, `scitex.audit`, unified security scan.
---

# scitex-audit

Single-entry security scanner. One `audit()` call dispatches across the
installed checker backends and merges their findings.

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-audit
import scitex_audit
scitex_audit.audit(...)

# Umbrella — pip install scitex
import scitex.audit
scitex.audit.audit(...)
```

`pip install scitex-audit` alone does NOT expose the `scitex` namespace;
`import scitex.audit` raises `ModuleNotFoundError`. To use the
`scitex.audit` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core

* [01_quick-start](01_quick-start.md) — Minimal usage, all checks / subset
* [02_python-api](02_python-api.md) — `audit()` signature and result schema
* [03_checkers](03_checkers.md) — The four checker backends

### Interface

* [10_cli-reference](10_cli-reference.md) — `scitex audit` subcommand (via parent CLI)
