---
name: scitex-security
description: GitHub security-alert utilities. `check_github_alerts(repo=...)` returns the open Dependabot/CodeQL alerts as a structured list. Drop-in replacement for `gh api repos/{owner}/{repo}/dependabot/alerts` shell-outs in monitoring dashboards.
primary_interface: python
interfaces:
  python: 2
  cli: 1
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-security/src/scitex_security/_skills/scitex-security/SKILL.md
tags: [scitex-security, scitex-package]
---

> **Interfaces:** Python ⭐⭐ · CLI ⭐ · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-security

GitHub security-alert utilities. `check_github_alerts(repo=...)` returns the open Dependabot/CodeQL alerts as a structured list. Drop-in replacement for `gh api repos/{owner}/{repo}/dependabot/alerts` shell-outs in monitoring dashboards.

See README.md and the package's public `__init__.py` for the full
function list. This skill leaf exists so agents discover the package
exists and roughly what shape it has — refer to the source for
signatures.

<!-- EOF -->
