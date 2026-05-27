---
name: perch
description: Server intelligence layer for RunCloud-managed Linux servers. Use when the user mentions Perch, /perch_*, RunCloud, nginx-rc, server intelligence, server diagnosis, WordPress site auditing, plugin vulnerability scanning, or any time they want to investigate, monitor, or heal a server they own.
when_to_use: User says "perch", "/perch_X", "runcloud", "nginx-rc", "audit my site", "site is white-screening", "what's wrong with the server", or any server-debugging request on a host they manage.
when_not_to_use: Tasks that target servers Perch is not connected to. Pure local development. Anything that requires modifying public/shared infrastructure without explicit confirmation.
---

# Perch — Server Intelligence Skill

Perch is a self-hosted intelligence layer that watches, diagnoses, and (within strict bounds) heals Linux servers managed by RunCloud — or any plain Ubuntu/Debian/AlmaLinux box. It runs as an MCP server, an HTTP API, and a Telegram bot. The brain (SQLite) accumulates per-server, per-webapp knowledge over time.

This skill teaches Claude how to use Perch correctly and safely.

## Identity

- **What it is**: Server intelligence layer. Reads everything, learns over time, talks to you in plain English.
- **What it isn't**: SaaS, monitoring dashboard, or runtime dependency. No vendor lock-in. Free forever.
- **How it talks**: Telegram, Slack, Claude Code MCP, HTTP API, CLI — same intelligence, multiple surfaces.
- **Where data lives**: `~/.perch/brain.db` (SQLite, on the user's server) and `~/.perch/vault.json` (AES-256-GCM encrypted credentials). Nothing leaves the box unless the user explicitly configures a webhook.

## Architecture

```
You (Claude Code / Telegram / Slack / HTTP)
        ↓
PERCH CORE
  ├── brain.ts          SQLite KB (servers, webapps, problems, plugins, knowledge, actions_log)
  ├── gateway.ts        Friendly alert formatter (multi-channel)
  ├── ssh-enhanced.ts   SSH with TOFU host verification + WP-CLI helper
  ├── vault.ts          AES-256-GCM credential vault
  └── redact.ts         Centralized privacy redactor (16 patterns)
        ↓
MODULES
  ├── wordpress/        db, plugins, security, backup, images, perf, errors
  ├── api/server.ts     HTTP wrapper for external integration
  └── monitor.sh        14-rule cron automation engine
```

## /perch_* MCP Tool Catalog

### Server (RunCloud API)
- `list_servers`, `get_server`, `get_server_stats`, `get_server_health`
- `control_service`, `clean_server_disk`, `get_server_logs`
- `update_ssh_settings`, `update_server_autoupdate`
- 130+ more — see `src/index.ts`

### Server (SSH)
- `ssh_run_command` — arbitrary SSH (validate inputs)
- `ssh_server_status`, `ssh_smart_fix`, `ssh_restart_service`
- `ssh_kill_orphans`, `ssh_disk_cleanup`, `ssh_check_ports`
- `ssh_wp_cli`, `ssh_artisan`, `ssh_tail_log`

### WordPress
- `perch_wp_db_audit` — autoload, transients, orphans, fragmentation
- `perch_wp_db_clean` — drop expired transients/sessions (idempotent)
- `perch_wp_plugins` — list + Wordfence Intelligence vulnerability scan
- `perch_wp_plugin_update`, `perch_wp_plugin_deactivate` (logs to undo)
- `perch_wp_security` — 12-check hardening audit
- `perch_wp_backup` — backup health
- `perch_wp_images_scan`, `perch_wp_images_optimize`
- `perch_wp_perf` — performance snapshot
- `perch_wp_errors` — diagnose PHP fatals + white screens

### Vault
- `perch_vault_put`, `perch_vault_get`, `perch_vault_list`, `perch_vault_delete`

### Brain & Intelligence
- `perch_brain` — KB summary
- `perch_webapp_history` — per-webapp problem history
- `perch_brain_search` — FTS5 search across all problems
- `perch_actions_log` — recent destructive actions
- `perch_undo` — reverse the last destructive action
- `perch_multi_server_dashboard` — one-shot all-server status
- `perch_self_update` — pull latest, rebuild, restart

## RunCloud Gotchas (CRITICAL — get these right)

| Wrong | Right (RunCloud) |
|---|---|
| `nginx` | `nginx-rc` |
| `nginx.service` | `nginx-rc.service` |
| `/etc/nginx/` | `/etc/nginx-rc/` |
| `php8.x-fpm` | `php8x-fpm-rc` |
| `/etc/nginx/conf.d/` (overwritten) | `/etc/nginx-rc/extra.d/` (custom-safe) |
| `/var/log/nginx/error.log` | `/var/log/nginx-rc/error.log` |
| `/var/www/` | `/home/{appuser}/webapps/{appname}/` |
| `www-data` | each webapp's own system user |

**Never** edit `/etc/nginx-rc/conf.d/` — RunCloud regenerates these and your changes vanish. Use `/etc/nginx-rc/extra.d/` for custom blocks.

PHP-FPM logs: `/home/{user}/logs/php_error.log` per webapp.

## Safety Policy (READ THIS BEFORE EVERY DESTRUCTIVE TOOL CALL)

### Auto-allowed (no confirm needed)
- Restart crashed `nginx-rc`, `php*-fpm-rc`, MySQL/MariaDB
- Kill orphan processes (PPID=1)
- Truncate (not delete) log files >50MB
- SSL renewal when <7 days remain
- Clear expired WordPress transients (WP-CLI built-in safe op)
- Clear `/tmp` PHP sessions older than 24h

### Confirm-required (always ask first)
- Plugin deactivation (`perch_wp_plugin_deactivate`)
- Plugin updates
- WP core update
- Database table changes (OPTIMIZE/REPAIR)
- File deletions
- Nginx config edits beyond reload
- Service stops without restart
- Reboot

### Never auto, ever
- Backup restoration
- DELETE/UPDATE on user data tables
- `rm` outside `/tmp`
- User account changes
- Hetzner-level shutdown / rebuild

## Master Key Handling

`PERCH_MASTER_KEY` (env var) is the only thing protecting the credential vault. Rules:

- **Never** echo the key in MCP responses, logs, or alerts.
- **Never** save the key to brain.db or any file Perch creates (it lives only in `~/.perch/.env` mode 0600, sourced by systemd EnvironmentFile).
- If the user asks "what's my master key?" — refuse and direct them to their password manager / `~/.perch/.env`.
- Vault rotation requires the OLD key as input — see `npm run vault rotate -- --old-key=...`.

## Common Workflows

### "Why is mysite.com white-screening?"
1. `perch_wp_errors` with domain → returns root cause + suggested fix
2. If `fixableByPerch: true` and user confirms → `perch_wp_plugin_deactivate`
3. `perch_wp_errors` again to verify the fatal cleared
4. Tell user what was disabled and why

### "Audit all my WP sites"
1. `list_servers` → for each server, `list_webapps`
2. For each WP webapp: `perch_wp_db_audit`, `perch_wp_security`, `perch_wp_plugins`
3. Summarize per-site, surface critical issues first

### "Rotate my RunCloud API key"
1. `perch_vault_get` with `runcloud:apikey` (current value, redact in summary)
2. User generates new key in RunCloud panel
3. `perch_vault_put` with the new value
4. Verify with `ping` tool (returns pong if auth works)

### "Update Perch and tell me what changed"
1. `perch_self_update` with `dryRun: true` first (returns commit count + changelog)
2. Show user the changelog, ask to proceed
3. `perch_self_update` (real) if confirmed

### "What do you know about disk-full incidents?"
1. `perch_brain_search` with query "disk full"
2. Group by server / by month
3. If patterns emerge ("happens after weekly backup"), surface that

## Anti-Patterns (Claude must NEVER)

- ❌ Echo `PERCH_MASTER_KEY`, vault values, or wp-config DB_PASSWORD into chat output
- ❌ Modify `/etc/nginx-rc/conf.d/` files
- ❌ Run `perch_wp_plugin_deactivate` without explicit user confirmation
- ❌ Run any `*delete*` tool without dry-run first
- ❌ Hard-code RunCloud paths assuming Ubuntu nginx defaults — always use the RunCloud variants
- ❌ Tell the user "I'll just restart nginx" without first checking `nginx -t` config validity
- ❌ Stuff entire DB query results into chat — use `perch_brain_search` summaries
- ❌ Ignore the safety whitelist/blacklist — defer to docs/safety.md when uncertain

## When to Trigger This Skill

Auto-load when the user mentions any of:
- "perch", "/perch_X", "the perch tool"
- "runcloud", "nginx-rc", "RunCloud server"
- "site is down", "white screen", "500 error" (and they own the server)
- "audit my WordPress site", "check plugin vulnerabilities", "wp_options bloat"
- "ssh into [host I own]", "restart nginx-rc / php-fpm"
- "perch.adityaarsharma.com" or "github.com/adityaarsharma/perch"

## Source of Truth

The repo at `https://github.com/adityaarsharma/perch` is canonical. When this skill conflicts with the repo, the repo wins. Specifically read:

- `README.md` — vision + comparison + connectors
- `docs/install.md` — install paths
- `docs/automation.md` — 14 cron rules + thresholds
- `docs/safety.md` — auto/confirm/never policy (verbatim authority)
- `docs/master-key.md` — encryption key lifecycle
- `docs/runcloud.md` — RunCloud-specific operational reference
- `src/index.ts` — authoritative tool list (`tools` array)

## Installation

```bash
# Drop this skill where Claude Code looks for skills
mkdir -p ~/.claude/skills/perch
cp /path/to/perch/skills/perch/SKILL.md ~/.claude/skills/perch/SKILL.md
# Restart Claude Code
```

---

*Skill version 1.0 — generated April 2026 from the live Perch codebase.*
