---
name: misardefender
description: "Manage and interact with MisarDefender — the local macOS security daemon. Use when: checking security daemon status, viewing security events, starting/stopping defender, scanning for threats, checking file integrity, reviewing network activity logs. Triggers: 'defender', 'misardefender', 'security daemon', 'check threats', 'file integrity', 'security events', 'defender status'."
user-invocable: true
argument-hint: "[start|stop|status|scan|logs|dashboard]"
---

# MisarDefender

MisarDefender is a local macOS security daemon that monitors file integrity, network activity, processes, credentials, USB devices, and app signatures. Alerts via macOS Notification Center.

**Source**: `scripts/misardefender/defender.py`
**Stack**: Python 3.9+ · SQLite (`defender.db`) · launchd · localhost:9876 dashboard

## Architecture — 6 Security Layers

| Layer | Monitors |
|-------|----------|
| 1 — File Integrity | SHA-256 hashes of critical paths (SSH, Keychain, LaunchAgents) |
| 2 — Network | Outbound connections, suspicious domains |
| 3 — Process | Running processes against whitelist, suspicious patterns |
| 4 — Credential | Keychain access, credential exposure |
| 5 — USB | Device attach/detach events |
| 6 — App Integrity | Code signature validation |

## Commands

```bash
python3 scripts/misardefender/defender.py start      # Start daemon (launchd)
python3 scripts/misardefender/defender.py stop       # Stop daemon
python3 scripts/misardefender/defender.py status     # Check daemon status
python3 scripts/misardefender/defender.py scan       # One-shot manual scan
open http://localhost:9876                           # Open dashboard
```

## Usage

```
/misar-dev:misardefender                   # Show status + recent events
/misar-dev:misardefender start             # Start the daemon
/misar-dev:misardefender stop              # Stop the daemon
/misar-dev:misardefender status            # Daemon status
/misar-dev:misardefender scan              # Run a manual scan
/misar-dev:misardefender logs              # Show recent security events
/misar-dev:misardefender dashboard         # Open localhost:9876
```

## Instructions

When invoked:

1. **Parse the argument** (start / stop / status / scan / logs / dashboard)
2. For `status`: run `python3 scripts/misardefender/defender.py status` and summarize
3. For `logs`: query `defender.db` events table — show last 20 events ordered by timestamp
4. For `start` / `stop` / `scan`: run the corresponding command and report result
5. For `dashboard`: open `http://localhost:9876` via Bash
6. No arg: show status + last 5 critical/high events

## Security Notes

- `defender.db` and `defender.log` are runtime files — never commit them
- Daemon runs as local user (not root) — some monitors may have limited visibility
- Touch ID authentication is handled by a companion Swift binary
- All SQLite writes are local-only; no network exfiltration
