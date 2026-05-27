---
name: profiles-and-credentials
description: Use when authoring or modifying any claude-team-toolkit skill that loads credentials, switches between accounts/orgs/environments, or needs confirmation for destructive operations. Reference for the shared profile + ctt_* helper pattern used by all credential-bearing skills.
user-invocable: false
---

# Profiles & Credentials — shared pattern reference

Reference skill describing the credential / profile / confirmation pattern used by all claude-team-toolkit skills (azure-devops, fastlane, firebase, heroku, k6, maestro, postgres, rspec, sentry, shopify, slack, trello, etc.). Implementation lives in [`lib/credentials.sh`](../../lib/credentials.sh) and [`lib/confirm.sh`](../../lib/confirm.sh).

## Overview

All credential-bearing skills share a uniform pattern:

- INI credentials at `~/.<service>/credentials` (mode 600)
- Multiple `[profile]` sections per file (e.g., `[default]`, `[work]`, `[prod]`)
- Resolution order: `--profile <name>` flag → `<SERVICE>_PROFILE` env → `~/.<service>/active_profile` → `[default]`
- Helper sourced from `lib/credentials.sh` populates `CTT_<KEY>` env vars
- Destructive ops gated by `ctt_confirm` from `lib/confirm.sh`
- Actions audit-logged to `~/.claude-team-toolkit/audit.log` (key NAMES only, never values)

## When to Use

- Authoring a NEW skill that needs per-account/per-org/per-env switching
- Modifying credential loading in an existing skill
- Adding destructive operations that need typed confirmation
- Debugging why a skill picks the wrong profile
- Reviewing security posture of a skill

## When NOT to Use

- One-off scripts not meant for reuse → just hardcode and move on
- Skills with no credentials (e.g., `react-native`, `rails-security`) → nothing to load
- Cross-cloud unified credential systems → use the cloud's native config (`~/.aws/credentials`, etc.) instead of reinventing

## Profile file shape

```ini
# ~/.<service>/credentials  (mode 600)
[default]
field_a = value
field_b = secret

[other-profile]
field_a = different
require_confirm = true        # gate every mutation in this profile
```

After `ctt_load_creds <service> [profile]`:
- `CTT_PROFILE=<resolved>` (e.g., `default`)
- `CTT_FIELD_A=<value>`, `CTT_FIELD_B=<secret>` (uppercased, hyphens → underscores)

## Helper API (from `lib/credentials.sh`)

| Function | Purpose |
|---|---|
| `ctt_load_creds <svc> [profile]` | Resolve + load profile into `CTT_*` env |
| `ctt_save_profile <svc> <profile> <k=v>...` | Atomic INI section write |
| `ctt_list_profiles <svc>` | List sections, mark active with `*` |
| `ctt_use_profile <svc> <profile>` | Set active profile pointer |
| `ctt_active_profile <svc>` | Print resolved active profile |
| `ctt_remove_profile <svc> <profile>` | Refuses to remove last profile |
| `ctt_mask <value>` | Returns `****<last4>` for safe logging |
| `ctt_validate_perms <file>` | Refuses non-600/400 mode (POSIX only) |
| `ctt_audit_log <svc> <action>` | Append timestamp + profile + action |

## Confirmation API (from `lib/confirm.sh`)

```bash
ctt_confirm "Delete app foo?" || return 1                # y/N prompt
ctt_confirm "Drop table users?" "DELETE" || return 1      # typed phrase
ctt_warn_destructive "Action description"                # noisy stderr banner
```

`CTT_NONINTERACTIVE=1` auto-denies all confirmations (CI safety).

## Common Mistakes

- Reading credentials directly with `awk` instead of `ctt_load_creds` → bypasses perm validation
- Logging full credential values instead of `ctt_mask` → secrets leak to terminal/CI logs
- Using `eval` to set vars from credentials → injection risk. Helper uses `printf -v` for safety.
- Audit log records values not just key names → audit log itself becomes a secret store
- Confirmation without typed phrase for irreversible ops → "y" is too easy a typo
- Service name with uppercase or special chars → helper validates `^[a-z0-9-]+$`

## Security defaults

- Credentials directory: `chmod 700`. File: `chmod 600`. Helper refuses to load otherwise (POSIX).
- Windows: best-effort (NTFS ACLs not enforced by helper) — document in skill's safety section.
- `CTT_NONINTERACTIVE=1` in CI → auto-deny destructive ops (no surprise mutations).
- Audit log at `~/.claude-team-toolkit/audit.log` (mode 600). Records: timestamp, service, profile, action.
- Never write credentials into git, chat output, or any file outside `~/.<service>/credentials`.
