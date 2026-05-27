---
name: meta-ads-cli-skill
description: Comprehensive operational guide for agents using Meta Ads CLI.
version: 1.0.0
tools:
  - meta-ads-cli
  - hcassar-meta-ads
---

# Meta Ads CLI Skill (`meta-ads-cli`)

This skill teaches an agent how to use Meta Ads CLI safely and effectively in an automated environment.

## 1) Tool identity

- Repository package name: `hcassar-meta-ads`
- Runtime CLI name (Commander): `meta-ads-cli`
- NPM bin currently configured as: `hcassar-meta-ads`
- Local dev entry: `npm run dev -- <command>`

Agent note: depending on install method, either `meta-ads-cli` (linked/source) or `hcassar-meta-ads` (npm bin mapping) may be the executable. Validate with `--help`.

## 2) Core capabilities

- Profile setup with app credentials
- OAuth auth and long-lived token acquisition
- Profile listing/switching
- Account listing/details
- Campaign listing/details (+ optional insights)
- Ad set listing by campaign
- JSON or table output

## 3) Preflight checks

Before operational commands:

1. Node >= 18
2. Setup completed (`setup`)
3. Auth completed (`auth`)
4. Correct ad account context selected

Quick checks:

```bash
meta-ads-cli --help
meta-ads-cli config
meta-ads-cli profiles --list
```

## 4) First-time setup workflow

### 4.1 Configure profile

```bash
meta-ads-cli setup
```

Prompts include:

- profile name
- app ID
- app secret
- optional ad account ID (`act_...`)

### 4.2 Authenticate

```bash
meta-ads-cli auth
```

or profile-specific:

```bash
meta-ads-cli auth --profile client-a
```

### 4.3 Verify

```bash
meta-ads-cli accounts
meta-ads-cli campaigns --limit 5
```

## 5) Command map for agents

Auth/config:

- `setup`
- `auth [-p <profile>]`
- `logout [-p <profile>]`
- `config [-p <profile>]`
- `profiles --list`
- `profiles --switch`

Accounts:

- `accounts [--json] [-p <profile>]`
- `account <account-id> [--json] [-p <profile>]`

Campaigns:

- `campaigns [-a <account-id>] [-l <limit>] [--json] [-p <profile>]`
- `campaign <campaign-id> [--insights] [--json] [-p <profile>]`
- `adsets <campaign-id> [-l <limit>] [--json] [-p <profile>]`

## 6) Recommended automation workflows

### 6.1 Account discovery

```bash
meta-ads-cli accounts --json
```

### 6.2 Campaign inventory

```bash
meta-ads-cli campaigns --account-id act_123456789 --limit 50 --json
```

### 6.3 Campaign deep dive with insights

```bash
meta-ads-cli campaign 120213377777777 --insights --json
```

### 6.4 Ad set breakdown

```bash
meta-ads-cli adsets 120213377777777 --limit 100 --json
```

## 7) Agent operating rules

1. Prefer `--json` for downstream parsing.
2. Always pin profile explicitly in multi-client jobs.
3. If account ID is absent in profile, pass `--account-id`.
4. Perform read-only validation before making context changes (`profiles --switch`).
5. Mask secrets in logs and outputs.

## 8) Output parsing strategy

Capture these fields in automation state:

- profile name
- account ID (`act_...`)
- campaign ID
- ad set ID
- status and metric fields (impressions, clicks, spend)

If table output is returned, prefer rerun with `--json` for stable parsing.

## 9) Error handling runbook

### Not authenticated

```bash
meta-ads-cli auth
```

### No profile found

```bash
meta-ads-cli setup
```

### Missing account ID

Pass it directly:

```bash
meta-ads-cli campaigns --account-id act_123456789
```

or set it in profile via setup.

### Token expired/invalid

Re-run auth for the target profile:

```bash
meta-ads-cli auth --profile <name>
```

### OAuth callback port conflict

Default callback uses localhost port 3000 in auth flow implementation. Free the port or adjust source config as needed.

## 10) Multi-profile operating pattern

1. `meta-ads-cli profiles --list`
2. `meta-ads-cli config --profile <name>`
3. `meta-ads-cli auth --profile <name>`
4. Run data command with `--profile <name>`

## 11) Security requirements for agents

- Never output app secret/token values.
- Never commit local config files.
- Keep ad account boundaries strict.
- Report permissions failures plainly instead of bypass attempts.

## 12) Quick command cheatsheet

```bash
meta-ads-cli setup
meta-ads-cli auth --profile default
meta-ads-cli profiles --list
meta-ads-cli accounts --json
meta-ads-cli campaigns --account-id act_123456789 --limit 20 --json
meta-ads-cli campaign 120213377777777 --insights --json
meta-ads-cli adsets 120213377777777 --limit 50 --json
meta-ads-cli logout --profile default
```
