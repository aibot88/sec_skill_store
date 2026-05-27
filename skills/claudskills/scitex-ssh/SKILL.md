---
description: Persistent, auto-reconnecting SSH reverse tunnels for NAT traversal — installs an `autossh` systemd unit on the local host so a bastion/relay server can SSH back in even through firewalls and dynamic IPs. Python API — `setup(port, bastion_server=, secret_key_path=)`, `remove(port)`, `status(port=None)`, `get_version()`. Defaults read from env vars `SCITEX_SSH_BASTION_SERVER` and `SCITEX_SSH_SECRET_KEY_PATH`. 3 MCP tools — `tunnel_setup`, `tunnel_remove`, `tunnel_status`. Bundled bash scripts (`setup-autossh-service.sh` / `remove-autossh-service.sh`) install/remove `autossh-tunnel-<port>.service` via systemctl. Drop-in replacement for hand-writing `autossh -M 0 -NR port:localhost:22 user@host` commands, crafting `/etc/systemd/system/autossh-tunnel-*.service` unit files by hand, `sshuttle`, and manual `ssh -R` plus `tmux` reconnect loops. Use whenever the user asks to "set up a reverse SSH tunnel", "keep SSH alive through NAT", "access a lab machine from outside", "tunnel through a bastion", "autossh systemd service", "check tunnel status", "remove a tunnel", "expose this machine via a jump host", or mentions bastion server, NAT traversal, autossh, reverse SSH, HPC login node.
allowed-tools: mcp__scitex__tunnel_*
primary_interface: cli
interfaces:
  python: 1
  cli: 3
  mcp: 2
  skills: 2
  hook: 0
  http: 0
---

# SSH Tunnels with scitex-ssh

> **Interfaces:** Python ⭐ · CLI ⭐⭐⭐ (primary) · MCP ⭐⭐ · Skills ⭐⭐ · Hook — · HTTP —

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-ssh
import scitex_ssh

# Umbrella — pip install scitex
import scitex.tunnel
```

`pip install scitex-ssh` alone does NOT expose the `scitex` namespace;
`import scitex.tunnel` raises `ModuleNotFoundError`. To use the
`scitex.tunnel` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core
- [01_quick-start.md](01_quick-start.md) — Quick start
- [02_python-api.md](02_python-api.md) — Python API

### Workflows
- [10_cli-commands.md](10_cli-commands.md) — CLI commands
- [11_mcp-tools-for-ai-agents.md](11_mcp-tools-for-ai-agents.md) — MCP tools for AI agents

### Standards
- [20_environment-variables.md](20_environment-variables.md) — Environment variables
