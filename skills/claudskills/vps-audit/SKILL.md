---
name: vps-audit
description: Deep audit of a remote VPS running Docker, Coolify, and Traefik. Use when the user wants to check what containers are running, inspect Coolify services, review Traefik routes, check disk/memory, review firewall rules, or get an eagle-eye view of their production server. Triggers on phrases like "audit the vps", "what's running on the server", "check production", "how's the vps doing", "what containers are up", or "check coolify".
compatibility: Designed for Claude Code on WSL. Requires an SSH alias named "vps" in ~/.ssh/config pointing to a server running Docker, Coolify, and Traefik. See scripts/collect-vps.sh to customize the SSH target.
allowed-tools: Bash Read
---

# VPS Audit

All data collection runs in parallel via `scripts/collect-vps.sh` — SSH queries fire simultaneously. Your job is to synthesize the structured output. Do not re-run SSH commands yourself.

**Setup:** Add a `vps` alias to `~/.ssh/config` pointing to your server, or edit `scripts/collect-vps.sh` to change the SSH target.

## Step 1 — Collect

```bash
~/.claude/commands/vps-audit/scripts/collect-vps.sh
```

## Step 2 — Synthesize

Container names in the output have Coolify UUID suffixes stripped already.

---

### System Identity
From SYSTEM: hostname, OS, kernel, uptime, load average.
From RECENT_LOGINS: flag any unfamiliar login sources.

### Hardware / Resources
From RESOURCES: CPU model/cores, RAM total/used/available, disk used/total on `/`, swap pressure.

### Docker Containers
From CONTAINERS and CONTAINER_STATS. Group containers by project (infer from container name prefixes).

For each container: status (healthy / unhealthy / up N days), CPU%, memory, exposed ports.

Flag any container that is: unhealthy, exited/stopped, >10% CPU sustained, >500MB memory.

### Traefik Routing Table
From TRAEFIK_ROUTES — present as a table:

| Domain | Upstream | TLS |
|--------|----------|-----|

### Docker Storage
From DOCKER_STORAGE: images / containers / volumes / build cache totals.
From VOLUMES dangling section: list any orphaned volumes explicitly.

### Systemd Services (non-Docker)
From SYSTEMD_SERVICES: note status of key services — tailscaled, fail2ban, docker, containerd, cron, sshd. Flag any that are absent or failing.

### Network & Firewall
From LISTEN_PORTS and FIREWALL, categorize by bind address:
- **Public** (0.0.0.0): which ports and what serves them
- **Private/VPN** (Tailscale or private IP): which ports
- **Loopback** (127.0.0.1): internal-only

### Tailscale
From TAILSCALE: server Tailscale IP, which devices are online.

### Users & SSH
From FS_DIRS passwd lines: users with shell access.
Flag any unfamiliar login source in RECENT_LOGINS.

### Flags / Concerns
- Unhealthy or stopped containers
- Dangling volumes (list them)
- Swap usage >50%
- Disk >80% used
- Public port that should be VPN-only
- Unfamiliar logins
- fail2ban or tailscaled not running

Keep the report dense. Flag anything that needs action.
