---
name: watchdog
description: >
  Scan repos for health issues: stale PRs, failing CI, old issues, TODO refs,
  lockfile problems, and security advisories.
  TRIGGER when: user asks about repo health, "check my repos", "stale PRs",
  "CI status", security advisories, or invokes "/watchdog".
  DO NOT TRIGGER when: user is working on watchdog agent code itself.
metadata:
  author: DROOdotFOO
  version: "1.0.0"
  tags: watchdog, health, monitoring, CI, security
---

# Watchdog

Continuous repo health monitor. Runs 6 checks: stale PRs, CI status, issue age,
TODO-closed-refs, lockfile audit, and security advisories.

## What You Get

- Health report: pass/warn/fail for 6 checks per repo
- Markdown report file or terminal output
- Alerts in `~/.local/share/watchdog/alerts.jsonl` for cross-agent consumption

## CLI Usage

```bash
# One-shot scan
watchdog scan owner/repo

# Scan with local path for extra checks (TODO refs, lockfile)
watchdog scan owner/repo --path /path/to/repo

# Save markdown report
watchdog report owner/repo --output health.md

# Continuous watch mode
watchdog watch owner/repo --interval 60
```

## MCP Server

```bash
watchdog serve
```

### Configure MCP

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "watchdog": {
      "command": "watchdog",
      "args": ["serve"]
    }
  }
}
```

### MCP Tools

| Tool | Description |
|------|-------------|
| `watchdog_scan` | Scan repos for health issues (GitHub API checks) |
| `watchdog_scan_local` | Scan with local path for TODO refs and lockfile audit |

## Install

```bash
cd agents/watchdog
pip install -e .
```

Requires `gh` CLI (authenticated) for GitHub API checks.
