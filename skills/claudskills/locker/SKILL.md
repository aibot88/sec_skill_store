---
name: locker
description: >
  Deterministic secret storage for guppi skills. Use when you need to store,
  retrieve, or manage API tokens and secrets across guppi skills.
allowed-tools: "Bash(guppi-locker:*)"
version: "0.1.2"
author: "Sam Dengler"
license: "MIT"
---

# Locker — Secret storage for guppi skills

Provides a single, deterministic interface for storing and retrieving secrets. Secrets are encrypted locally using a master key stored in the OS keychain. Skills call `guppi-locker get SERVICE KEY` to retrieve secrets.

## Setup

```bash
guppi-locker init
```

## Commands

### `guppi-locker get SERVICE KEY`

Retrieve a secret. Prints the value to stdout.

```bash
token=$(guppi-locker get courier handoffs)
```

### `guppi-locker set SERVICE KEY [--value VALUE] [--force]`

Store a secret. Prompts interactively if `--value` is omitted.

```bash
guppi-locker set courier handoffs --value "token-value"
guppi-locker set courier handoffs               # prompts for value
guppi-locker set courier handoffs --force        # overwrite without confirmation
```

**Options:**
- `--value` — secret value (prompts if omitted)
- `--force` — overwrite existing secret without confirmation

### `guppi-locker delete SERVICE KEY`

Remove a secret.

### `guppi-locker list [SERVICE]`

List secrets (never prints values).

```bash
guppi-locker list              # all secrets
guppi-locker list courier      # secrets for courier only
```

### `guppi-locker init`

First-time setup. Generates a master encryption key, stores it in the OS keychain, and creates the encrypted secrets file.

## Skill Management

```bash
guppi-locker skill install   # Register with guppi-cli
guppi-locker skill show      # Display SKILL.md contents
```
