---
name: scitex-sh
description: Safe subprocess wrapper — `execute(['cmd', 'arg'])` is a list-only API (no shell injection), with sensible defaults for capture, timeout, and error reporting. Drop-in replacement for `subprocess.run([...], check=True, capture_output=True, text=True)` boilerplate.
primary_interface: python
interfaces:
  python: 2
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-sh/src/scitex_sh/_skills/scitex-sh/SKILL.md
tags: [scitex-sh, scitex-package]
---

> **Interfaces:** Python ⭐⭐ · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-sh

Safe subprocess wrapper — `execute(['cmd', 'arg'])` is a list-only API (no shell injection), with sensible defaults for capture, timeout, and error reporting. Drop-in replacement for `subprocess.run([...], check=True, capture_output=True, text=True)` boilerplate.

See README.md and the package's public `__init__.py` for the full
function list. This skill leaf exists so agents discover the package
exists and roughly what shape it has — refer to the source for
signatures.
