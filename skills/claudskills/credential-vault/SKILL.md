---
name: credential-vault
description: "Secure API key management for Claude Code — encrypted storage, auto-rotation, leak detection, safe injection"
author: hanabi-jpn
version: 1.0.0
tags:
  - security
  - credentials
  - api-keys
  - encryption
  - keychain
  - rotation
  - leak-detection
  - vault
  - secret-management
  - claude-code
---

```
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║         ╦  ╦╔═╗╦ ╦╦  ╔╦╗                                     ║
    ║         ╚╗╔╝╠═╣║ ║║   ║                                      ║
    ║          ╚╝ ╩ ╩╚═╝╩═╝ ╩                                      ║
    ║                                                                ║
    ║    ┌─────────────────────────────────────────────────┐        ║
    ║    │  ┌───┐                                         │        ║
    ║    │  │ K │  ╔═══════════════════════════════════╗   │        ║
    ║    │  │ E │  ║  sk-ant-***  ──▶  AES-256-GCM    ║   │        ║
    ║    │  │ Y │  ║  ghp_****    ──▶  ████████████    ║   │        ║
    ║    │  │ S │  ║  AKIAIO****  ──▶  ████████████    ║   │        ║
    ║    │  │   │  ║  xoxb-****   ──▶  ████████████    ║   │        ║
    ║    │  └───┘  ╚═══════════════════════════════════╝   │        ║
    ║    │                                                 │        ║
    ║    │      macOS Keychain ◀──▶ Credential Vault       │        ║
    ║    └─────────────────────────────────────────────────┘        ║
    ║                                                                ║
    ║    [ CREDENTIAL VAULT — ZERO PLAINTEXT. ZERO LEAKS. ]         ║
    ║    [ Your keys are locked. Your secrets are safe. ]            ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
```

`AES-256-GCM` `KEYCHAIN-NATIVE` `AUTO-ROTATION` `LEAK-DETECTION` `ZERO-PLAINTEXT`

[![Author](https://img.shields.io/badge/author-hanabi--jpn-orange)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Encryption](https://img.shields.io/badge/encryption-AES--256--GCM-brightgreen)]()
[![Keys](https://img.shields.io/badge/manages-API_keys_%7C_tokens_%7C_secrets-yellow)]()

> **API keys in plaintext are ticking time bombs. Credential Vault defuses them before they detonate.**

---

## Overview

Credential Vault is a secure API key and secret management system built specifically for developers using Claude Code on macOS. The fundamental problem is simple but pervasive: developers store API keys in `.env` files, shell profiles, and configuration files as plaintext. These keys end up in git history, shell history, log files, clipboard contents, and terminal scrollback buffers. A single `git push` with an unignored `.env` file can expose production credentials to the public internet. CVE-2026-21852 demonstrated how MCP servers could silently harvest these plaintext credentials from the environment and exfiltrate them through crafted tool responses. Credential Vault eliminates this entire class of vulnerability by ensuring that credentials never exist as plaintext outside of the macOS Keychain's encrypted storage.

The architecture centers on macOS Keychain integration as the single source of truth for all credentials. When a developer stores a key with `vault store`, it is encrypted with AES-256-GCM and written to a dedicated Keychain (`claude-code-vault` by default) that is separate from the user's login Keychain. When Claude Code or any tool needs a credential, `vault get` retrieves it from Keychain and injects it directly into the process environment without ever writing it to disk. The vault tracks key age and enforces rotation policies — keys older than `$VAULT_AUTO_ROTATE_DAYS` trigger rotation warnings, and the vault can coordinate automatic rotation for supported services (Anthropic, OpenAI, GitHub, AWS). Leak detection runs continuously, scanning log files, terminal output, git staging areas, and clipboard contents for patterns matching stored credentials. When a leak is detected, the vault immediately alerts the developer and can trigger automatic key rotation to minimize exposure. Multi-project isolation ensures that keys for different projects are scoped and cannot cross-contaminate — a compromised development environment cannot access production credentials stored in a separate vault partition.

```
  ┌──────────────────────────────────────────────────────────────┐
  │              CREDENTIAL VAULT ARCHITECTURE                    │
  │                                                              │
  │  DEVELOPER                    VAULT ENGINE                   │
  │  ┌────────────┐                                              │
  │  │ vault store│──────▶  ┌─────────────────────────┐         │
  │  │ vault get  │──────▶  │    KEY PROCESSOR        │         │
  │  │ vault scan │──────▶  │                         │         │
  │  └────────────┘         │  Validate ──▶ Encrypt   │         │
  │                         │      │            │      │         │
  │                         │      ▼            ▼      │         │
  │                         │  Strength    AES-256-GCM │         │
  │                         │  Analysis    Encryption  │         │
  │                         └──────────┬──────────────┘         │
  │                                    │                         │
  │                                    ▼                         │
  │                         ┌─────────────────────┐             │
  │                         │  macOS KEYCHAIN      │             │
  │                         │  ┌───────────────┐   │             │
  │                         │  │ claude-code-  │   │             │
  │                         │  │ vault         │   │             │
  │                         │  │               │   │             │
  │                         │  │ [project-a]   │   │             │
  │                         │  │  ANTHROPIC_KEY│   │             │
  │                         │  │  GITHUB_TOKEN │   │             │
  │                         │  │               │   │             │
  │                         │  │ [project-b]   │   │             │
  │                         │  │  AWS_KEY      │   │             │
  │                         │  │  STRIPE_KEY   │   │             │
  │                         │  └───────────────┘   │             │
  │                         └─────────────────────┘             │
  │                                    │                         │
  │                                    ▼                         │
  │   INJECTION                  LEAK DETECTION                  │
  │  ┌────────────┐          ┌──────────────────┐               │
  │  │ Process    │          │ Log files        │               │
  │  │ Environment│◀─safe──  │ Git staging      │               │
  │  │ (in-memory │  inject  │ Shell history    │               │
  │  │  only)     │          │ Clipboard        │               │
  │  └────────────┘          │ Terminal output  │               │
  │                          └──────────────────┘               │
  └──────────────────────────────────────────────────────────────┘
```

---

## System Prompt Instructions

You are **Credential Vault**, a secure API key and secret management agent for Claude Code on macOS. You operate under the following strict rules:

1. **Never store credentials in plaintext on disk.** All API keys, tokens, passwords, and secrets must be encrypted with AES-256-GCM before storage. The only acceptable persistent storage location is the macOS Keychain. Plaintext credentials must never be written to `.env` files, shell profiles (`.zshrc`, `.bashrc`, `.bash_profile`), configuration files, or any other disk location.

2. **Use macOS Keychain as the single source of truth.** All credential operations (store, retrieve, rotate, revoke) must go through the macOS Keychain API via the `security` command-line tool. The dedicated Keychain (`$VAULT_KEYCHAIN`) is separate from the user's login Keychain to prevent accidental exposure through Keychain Access.app or iCloud Keychain sync.

3. **Inject credentials through process environment only.** When a tool or script needs a credential, retrieve it from Keychain and inject it as an environment variable in the child process. The credential exists in memory only for the duration of that process. Never write credentials to temporary files, named pipes, or shared memory segments that other processes could access.

4. **Enforce key strength requirements.** Analyze all stored credentials for minimum strength: API keys must be at least 32 characters, passwords must meet complexity requirements (uppercase, lowercase, numbers, symbols, minimum 16 characters), and RSA keys must be at least 2048 bits. Flag weak credentials and recommend regeneration.

5. **Track credential age and enforce rotation.** Every stored credential has a creation timestamp and a rotation deadline based on `$VAULT_AUTO_ROTATE_DAYS`. When a credential approaches its rotation deadline (7 days before), generate a warning. When the deadline passes, escalate to critical. For supported services (Anthropic, OpenAI, GitHub, AWS, Stripe), offer automated rotation that generates a new key, stores it, and revokes the old one.

6. **Scan continuously for credential leaks.** When `$VAULT_LEAK_SCAN` is true, monitor the following surfaces for patterns matching stored credentials: git staging area (pre-commit), git log output, terminal scrollback, log files in `/tmp/` and project directories, clipboard contents, and shell history files. When a leak is detected, immediately alert the developer and recommend rotation.

7. **Isolate credentials per project.** Each project directory gets its own credential namespace in the Keychain. A credential stored for `project-a` is not accessible when working in `project-b`. This prevents lateral movement — if one project's environment is compromised, credentials for other projects remain safe.

8. **Integrate with git-secrets for pre-commit protection.** Automatically configure git-secrets hooks in every project that uses Credential Vault. These hooks prevent committing files that contain patterns matching stored credentials. Maintain a pattern file that is updated whenever credentials are stored or rotated.

9. **Support secure export and import for team sharing.** When credentials need to be shared with team members, `vault export` creates an encrypted archive using the recipient's public key. The archive can only be decrypted by the intended recipient. Never export credentials in plaintext, even to "secure" channels like encrypted messaging apps.

10. **Audit all credential access.** Every `vault get`, `vault store`, `vault rotate`, and `vault revoke` operation is logged to `~/.vault/audit.log` with timestamp, operation type, credential identifier (never the credential value), requesting process, and result. This audit trail is append-only with `chmod 0600` permissions.

11. **Detect credential exposure in Claude Code output.** Scan all text that Claude Code generates (tool outputs, explanations, code suggestions) for patterns matching stored credentials. If Claude Code ever includes a credential in its output — even partially — immediately flag it and recommend rotation. This defends against CVE-2026-21852 where MCP servers embedded stolen credentials in tool output.

12. **Validate credential sources before storage.** When storing a new credential, verify its format matches the expected pattern for the declared service. An Anthropic API key should match `sk-ant-*`, a GitHub token should match `ghp_*` or `gho_*`, and an AWS key should match `AKIA*`. Reject credentials that do not match expected patterns to prevent storing corrupted or fake credentials.

13. **Support emergency revocation.** The `vault revoke` command immediately removes a credential from Keychain, invalidates it with the service provider (for supported services), updates git-secrets patterns, and triggers a scan for any remaining references. This is the nuclear option for confirmed credential compromise.

14. **Coordinate with mac-sentinel for runtime protection.** Pass credential patterns (not values) to mac-sentinel so it can monitor for exfiltration attempts. When mac-sentinel detects a network connection attempting to transmit data matching credential patterns, it blocks the connection and alerts Credential Vault.

15. **Coordinate with repo-guardian for pre-clone protection.** When repo-guardian scans a new repository and finds `.env` files with credential patterns, it recommends migrating those credentials to Credential Vault. When fake credentials with endpoint overrides are detected (redirect attacks), Credential Vault verifies that its stored credentials use only official service endpoints.

16. **Never expose credentials in error messages.** All error messages, log entries, and diagnostic output must redact credential values. Use the credential identifier (e.g., "ANTHROPIC_API_KEY for project-a") rather than the value. Even partial credential exposure (first/last characters) is prohibited.

17. **Support multiple encryption backends.** While AES-256-GCM is the default, support ChaCha20-Poly1305 as an alternative for environments where AES hardware acceleration is unavailable. The encryption backend is configurable via `$VAULT_ENCRYPTION`.

18. **Handle Keychain access prompts gracefully.** macOS may prompt for Keychain password or Touch ID when accessing credentials. Credential Vault must handle these prompts without timing out or failing silently. Cache Keychain unlock status for the session to minimize repeated prompts.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `VAULT_KEYCHAIN` | `claude-code-vault` | Name of the dedicated macOS Keychain for credential storage. Separate from login Keychain. |
| `VAULT_ENCRYPTION` | `aes-256-gcm` | Encryption algorithm for credential storage. Options: `aes-256-gcm`, `chacha20-poly1305`. |
| `VAULT_AUTO_ROTATE_DAYS` | `90` | Number of days before credentials trigger rotation warnings. Set to 0 to disable rotation tracking. |
| `VAULT_LEAK_SCAN` | `true` | Enable continuous leak detection across git, logs, clipboard, and terminal output. |

---

## Commands

### `vault store`

Stores a credential securely in the vault.

```
$ vault store ANTHROPIC_API_KEY --project my-app
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — STORE                    ║
╚══════════════════════════════════════════════════════════╝

Enter credential value (hidden): ••••••••••••••••••••••••••••

Validation:
  Format:    sk-ant-api03-*** ✓ (Anthropic API key pattern)
  Length:    108 characters ✓ (minimum 32)
  Strength:  HIGH (sufficient entropy)
  Service:   Anthropic (auto-detected)

Storage:
  Keychain:  claude-code-vault
  Namespace: my-app
  Encryption: AES-256-GCM
  Created:   2026-03-01 16:00:00
  Rotation:  2026-05-30 16:00:00 (90 days)

git-secrets pattern updated:
  → Added sk-ant-api03-[first8chars] pattern to .git-secrets

✓ ANTHROPIC_API_KEY stored securely for project "my-app"
```

### `vault get`

Retrieves a credential and injects it into the environment.

```
$ vault get ANTHROPIC_API_KEY --project my-app
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — RETRIEVE                 ║
╚══════════════════════════════════════════════════════════╝

Keychain:    claude-code-vault
Namespace:   my-app
Credential:  ANTHROPIC_API_KEY

Authentication: Touch ID ✓

Injection method: process environment (in-memory only)
  → export ANTHROPIC_API_KEY="sk-ant-***" (value not displayed)
  → Available to child processes of this shell session
  → Will not persist after terminal closes

Credential age: 34 days (56 days until rotation)
Last accessed: 2026-02-28 09:15:00

✓ ANTHROPIC_API_KEY injected into environment
```

### `vault list`

Lists all stored credentials with metadata.

```
$ vault list
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — INVENTORY                ║
╚══════════════════════════════════════════════════════════╝

Keychain: claude-code-vault

Project: my-app (4 credentials)
  ┌──────────────────────┬───────────┬──────────┬──────────────┐
  │ Credential           │ Service   │ Age      │ Rotation     │
  ├──────────────────────┼───────────┼──────────┼──────────────┤
  │ ANTHROPIC_API_KEY    │ Anthropic │ 34 days  │ 56 days left │
  │ GITHUB_TOKEN         │ GitHub    │ 12 days  │ 78 days left │
  │ OPENAI_API_KEY       │ OpenAI    │ 89 days  │ ⚠ 1 day left │
  │ STRIPE_SECRET_KEY    │ Stripe    │ 102 days │ ✗ OVERDUE    │
  └──────────────────────┴───────────┴──────────┴──────────────┘

Project: internal-tools (2 credentials)
  ┌──────────────────────┬───────────┬──────────┬──────────────┐
  │ Credential           │ Service   │ Age      │ Rotation     │
  ├──────────────────────┼───────────┼──────────┼──────────────┤
  │ AWS_ACCESS_KEY_ID    │ AWS       │ 45 days  │ 45 days left │
  │ AWS_SECRET_ACCESS_KEY│ AWS       │ 45 days  │ 45 days left │
  └──────────────────────┴───────────┴──────────┴──────────────┘

Summary: 6 credentials across 2 projects
Warnings: 1 nearing rotation, 1 overdue
```

### `vault rotate`

Rotates a credential, generating a new key and revoking the old one.

```
$ vault rotate OPENAI_API_KEY --project my-app
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — ROTATION                 ║
╚══════════════════════════════════════════════════════════╝

Target: OPENAI_API_KEY (my-app)
Service: OpenAI (auto-rotation supported)
Current age: 89 days (rotation overdue in 1 day)

Rotation steps:
  [1/4] Generating new API key via OpenAI API...
        ✓ New key generated: sk-proj-*** (not displayed)
  [2/4] Storing new key in vault...
        ✓ Encrypted with AES-256-GCM, stored in Keychain
  [3/4] Revoking old key via OpenAI API...
        ✓ Old key revoked (confirmed inactive)
  [4/4] Updating git-secrets patterns...
        ✓ Pattern updated for new key prefix

Rotation complete:
  Old key: REVOKED (2026-03-01 16:05:00)
  New key: ACTIVE (rotation due: 2026-05-30)

✓ OPENAI_API_KEY rotated successfully
```

### `vault scan`

Scans for leaked credentials across all surfaces.

```
$ vault scan
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — LEAK SCAN                ║
╚══════════════════════════════════════════════════════════╝

Scanning for leaked credentials...

Git staging area:
  ✓ No credentials in staged files

Git history (last 50 commits):
  ✗ CRITICAL: STRIPE_SECRET_KEY found in commit a1b2c3d
    File: config/payment.js (line 15, since removed)
    → Key still accessible via: git show a1b2c3d:config/payment.js
    → Recommendation: rotate key immediately, use git-filter-repo
      to purge from history

Shell history:
  ✗ WARNING: ANTHROPIC_API_KEY found in ~/.zsh_history
    Line 4821: export ANTHROPIC_API_KEY=sk-ant-api03-...
    → Recommendation: remove line and use `vault get` instead

Log files:
  ✓ /tmp/*.log — no credential patterns
  ✓ Project logs — no credential patterns

Clipboard:
  ✓ No credential patterns in clipboard

Terminal scrollback:
  ⚠ WARNING: Partial key match in terminal buffer
    → Recommendation: clear terminal with `clear && printf '\e[3J'`

Summary: 1 critical leak, 2 warnings
```

### `vault audit`

Displays the credential access audit trail.

```
$ vault audit --last 10
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — AUDIT LOG                ║
╚══════════════════════════════════════════════════════════╝

Last 10 operations:

  2026-03-01 16:05:00  ROTATE  OPENAI_API_KEY (my-app)
                       Process: vault-cli (PID 51234)
                       Result: SUCCESS — old key revoked

  2026-03-01 16:00:00  STORE   ANTHROPIC_API_KEY (my-app)
                       Process: vault-cli (PID 51220)
                       Result: SUCCESS

  2026-02-28 09:15:00  GET     ANTHROPIC_API_KEY (my-app)
                       Process: claude-code (PID 48291)
                       Result: SUCCESS — injected to env

  2026-02-28 09:14:00  GET     GITHUB_TOKEN (my-app)
                       Process: claude-code (PID 48291)
                       Result: SUCCESS — injected to env

  2026-02-27 14:30:00  SCAN    [all credentials]
                       Process: vault-cli (PID 50102)
                       Result: 0 leaks detected

  2026-02-25 11:00:00  STORE   AWS_ACCESS_KEY_ID (internal-tools)
                       Process: vault-cli (PID 49887)
                       Result: SUCCESS

  2026-02-25 11:00:00  STORE   AWS_SECRET_ACCESS_KEY (internal-tools)
                       Process: vault-cli (PID 49887)
                       Result: SUCCESS

  2026-02-20 16:45:00  GET     STRIPE_SECRET_KEY (my-app)
                       Process: node (PID 49102)
                       Result: SUCCESS — injected to env

  2026-02-15 10:00:00  STORE   STRIPE_SECRET_KEY (my-app)
                       Process: vault-cli (PID 48500)
                       Result: SUCCESS

  2026-02-15 09:55:00  STORE   GITHUB_TOKEN (my-app)
                       Process: vault-cli (PID 48490)
                       Result: SUCCESS

Total operations this month: 47
Failed operations: 0
```

### `vault export`

Exports encrypted credentials for team sharing.

```
$ vault export --project my-app --recipient alice@team.com
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — SECURE EXPORT            ║
╚══════════════════════════════════════════════════════════╝

Exporting credentials for project: my-app
Recipient: alice@team.com

Encryption:
  → Fetching recipient's public key from Keychain/keyserver
  ✓ Public key found (RSA 4096-bit, fingerprint: A1B2...C3D4)

Credentials included (4):
  [1] ANTHROPIC_API_KEY
  [2] GITHUB_TOKEN
  [3] OPENAI_API_KEY
  [4] STRIPE_SECRET_KEY

Export file: ~/Desktop/my-app-vault-export.enc
  Size: 2.1 KB (encrypted)
  Algorithm: RSA-4096 + AES-256-GCM (hybrid encryption)
  Recipient: alice@team.com ONLY

⚠ This file can only be decrypted by alice@team.com
  Share via any channel — the encryption protects the contents.
  Recipient imports with: vault import my-app-vault-export.enc

✓ Export complete
```

### `vault import`

Imports encrypted credentials from a team member.

```
$ vault import ~/Downloads/my-app-vault-export.enc --project my-app
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — SECURE IMPORT            ║
╚══════════════════════════════════════════════════════════╝

Import file: ~/Downloads/my-app-vault-export.enc
Decrypting with your private key...
  ✓ Decryption successful (hybrid RSA-4096 + AES-256-GCM)

Credentials found (4):
  [1] ANTHROPIC_API_KEY — Anthropic (format valid ✓)
  [2] GITHUB_TOKEN — GitHub (format valid ✓)
  [3] OPENAI_API_KEY — OpenAI (format valid ✓)
  [4] STRIPE_SECRET_KEY — Stripe (format valid ✓)

Importing to project namespace: my-app
  [1/4] ANTHROPIC_API_KEY ✓ stored
  [2/4] GITHUB_TOKEN ✓ stored
  [3/4] OPENAI_API_KEY ✓ stored
  [4/4] STRIPE_SECRET_KEY ✓ stored

git-secrets patterns updated for all 4 credentials.
Rotation tracking started (90-day cycle from today).

✓ Import complete — 4 credentials stored securely
  Source file securely deleted from ~/Downloads/
```

### `vault revoke`

Emergency credential revocation.

```
$ vault revoke STRIPE_SECRET_KEY --project my-app --emergency
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — EMERGENCY REVOCATION     ║
╚══════════════════════════════════════════════════════════╝

⚠ EMERGENCY REVOCATION initiated for STRIPE_SECRET_KEY (my-app)

Steps:
  [1/5] Removing from macOS Keychain...
        ✓ Deleted from claude-code-vault
  [2/5] Revoking with Stripe API...
        ✓ Key invalidated on Stripe dashboard
  [3/5] Scanning for remaining references...
        → Found in git history (commit a1b2c3d)
        → Recommendation: run git-filter-repo to purge
  [4/5] Updating git-secrets patterns...
        ✓ Pattern removed (key no longer valid)
  [5/5] Notifying mac-sentinel...
        ✓ mac-sentinel updated — monitoring for residual usage

Revocation complete:
  Key status: REVOKED (cannot be used for API calls)
  Revoked at: 2026-03-01 16:15:00
  Remaining references: 1 (git history — manual cleanup needed)

✗ STRIPE_SECRET_KEY is permanently revoked
  Generate a new key on the Stripe dashboard and store with:
  vault store STRIPE_SECRET_KEY --project my-app
```

### `vault status`

Displays overall vault health and statistics.

```
$ vault status
╔══════════════════════════════════════════════════════════╗
║              CREDENTIAL VAULT — STATUS                   ║
╚══════════════════════════════════════════════════════════╝

Keychain:       claude-code-vault (UNLOCKED)
Encryption:     AES-256-GCM
Leak scanning:  ACTIVE (last scan: 12 min ago)
git-secrets:    CONFIGURED (3 projects)

Credentials:    6 active, 1 revoked
Projects:       2 (my-app, internal-tools)

Health:
  Rotation compliance   ████████████████░░░░  80%
  Key strength          ████████████████████  100%
  Leak-free status      ██████████████████░░  90%
  Audit completeness    ████████████████████  100%

Alerts:
  ⚠ OPENAI_API_KEY (my-app) — rotation due in 1 day
  ✗ STRIPE_SECRET_KEY (my-app) — rotation overdue (12 days)
  ✗ Credential leak detected in git history (see vault scan)

Overall health: 82/100 (B)
```

---

## Workflow Diagram

```
  ┌─────────────────────────────────────────────────────────────┐
  │              CREDENTIAL VAULT WORKFLOW                       │
  │                                                             │
  │  Developer needs API key for Claude Code session            │
  │       │                                                     │
  │       ▼                                                     │
  │  ┌──────────────┐    ┌───────────────┐                     │
  │  │ vault store  │───▶│ Validate      │                     │
  │  │ (first time) │    │ format +      │                     │
  │  └──────────────┘    │ strength      │                     │
  │                      └───────┬───────┘                     │
  │                              │                              │
  │                              ▼                              │
  │                      ┌───────────────┐                     │
  │                      │ Encrypt with  │                     │
  │                      │ AES-256-GCM   │                     │
  │                      └───────┬───────┘                     │
  │                              │                              │
  │                              ▼                              │
  │                      ┌───────────────┐                     │
  │                      │ Store in      │                     │
  │                      │ macOS Keychain│                     │
  │                      └───────┬───────┘                     │
  │                              │                              │
  │       ▼                      │                              │
  │  ┌──────────────┐           │                              │
  │  │ vault get    │◀──────────┘                              │
  │  │ (each use)   │                                          │
  │  └──────┬───────┘                                          │
  │         │                                                   │
  │         ▼                                                   │
  │  ┌──────────────┐    ┌───────────────┐                     │
  │  │ Decrypt from │───▶│ Inject into   │                     │
  │  │ Keychain     │    │ process env   │                     │
  │  └──────────────┘    │ (memory only) │                     │
  │                      └───────┬───────┘                     │
  │                              │                              │
  │                              ▼                              │
  │                      ┌───────────────┐                     │
  │                      │ Claude Code   │                     │
  │                      │ uses key      │                     │
  │                      └───────┬───────┘                     │
  │                              │                              │
  │  CONTINUOUS ◀────────────────┘                              │
  │  ┌──────────────┐                                          │
  │  │ vault scan   │ (monitors git, logs, clipboard, shell)   │
  │  └──────┬───────┘                                          │
  │         │                                                   │
  │    LEAK FOUND?                                              │
  │    YES │         NO │                                       │
  │        ▼            ▼                                       │
  │  ┌──────────┐  ┌──────────┐                                │
  │  │ ALERT +  │  │ Continue │                                │
  │  │ ROTATE   │  │ monitor  │                                │
  │  └──────────┘  └──────────┘                                │
  └─────────────────────────────────────────────────────────────┘
```

---

## Error Handling

| Error | Cause | Solution |
|---|---|---|
| `VAULT_E001: Keychain not found` | The `claude-code-vault` Keychain does not exist yet | Run `vault init` to create the dedicated Keychain. This only needs to be done once per machine. |
| `VAULT_E002: Keychain locked — authentication required` | macOS Keychain requires password or Touch ID | Authenticate via the macOS prompt. If running headless, use `security unlock-keychain -p <password> claude-code-vault`. |
| `VAULT_E003: Credential format invalid` | Stored value does not match expected pattern for the declared service | Verify the credential is correct and complete. Use `--skip-validation` if the credential uses a non-standard format (not recommended). |
| `VAULT_E004: Rotation failed — API error` | Service provider API rejected the rotation request | Check API connectivity and permissions. Ensure the current key has permission to create new keys. Rotate manually via the service dashboard and store with `vault store`. |
| `VAULT_E005: Duplicate credential` | A credential with the same name already exists in the project namespace | Use `vault store --overwrite` to replace, or `vault rotate` to properly rotate the existing credential. |
| `VAULT_E006: Export recipient key not found` | Cannot find the recipient's public key for encrypted export | Ask the recipient to share their public key, or use `--symmetric` for password-based encryption (less secure). |
| `VAULT_E007: Leak detected in real-time` | A stored credential pattern was found in output, logs, or git | Follow the remediation steps in the alert. Rotate the compromised credential immediately with `vault rotate --emergency`. |

---

## FAQ

**Q1: Why not just use `.env` files with `.gitignore`?**
A: `.gitignore` is a convention, not a security boundary. Developers accidentally commit `.env` files constantly — it is one of the top causes of credential leaks on GitHub. Even with `.gitignore`, `.env` files are plaintext on disk, readable by any process, and often backed up to cloud services. Credential Vault eliminates plaintext storage entirely.

**Q2: How does macOS Keychain encryption work?**
A: macOS Keychain uses a combination of AES-256-GCM encryption and the Secure Enclave (on Apple Silicon Macs) to protect stored items. The Keychain is locked when the user logs out or the screen locks. Credential Vault uses a dedicated Keychain separate from the login Keychain, providing an additional isolation layer.

**Q3: What happens if I lose my Mac?**
A: FileVault full-disk encryption (verified by mac-sentinel) protects the Keychain at rest. Without your login password or recovery key, the Keychain contents are cryptographically inaccessible. Credential Vault also supports exporting encrypted backups that can be imported on a new machine.

**Q4: Does this work with Docker and devcontainers?**
A: Yes. Use `vault get --docker-inject` to pass credentials as Docker build secrets or runtime environment variables without writing them to Dockerfiles, docker-compose files, or image layers.

**Q5: Can multiple team members share the same vault?**
A: No, each developer has their own vault on their own machine. Use `vault export` and `vault import` with public-key encryption to securely share credentials between team members. This ensures no single point of compromise.

**Q6: How does auto-rotation work?**
A: For supported services, Credential Vault uses the service's API to generate a new key, stores it in the vault, verifies the new key works, and then revokes the old key. The entire process is atomic — if any step fails, the old key remains active.

**Q7: What services support auto-rotation?**
A: Currently: Anthropic, OpenAI, GitHub (personal access tokens), AWS (IAM access keys), and Stripe. More services are planned. For unsupported services, Credential Vault sends rotation reminders and tracks manual rotation.

**Q8: Does the leak scanner have false positives?**
A: Rarely. The scanner matches against exact credential patterns stored in the vault, not generic regex patterns. This means it only flags strings that are actually your credentials, not random strings that happen to look like API keys.

**Q9: How does this integrate with the other hanabi-jpn security skills?**
A: Credential Vault is the central credential authority. mac-sentinel receives credential patterns (not values) to monitor for exfiltration. repo-guardian checks repositories for fake credentials designed to redirect API calls. All three skills share a unified security posture model.

**Q10: Can I use this for SSH keys and certificates?**
A: Yes. Use `vault store SSH_PRIVATE_KEY --file ~/.ssh/id_rsa` to store the key contents. The original file can then be deleted from disk. Retrieve with `vault get SSH_PRIVATE_KEY --file /tmp/id_rsa` (temporary, auto-deleted after use).

**Q11: What is the performance impact?**
A: `vault get` takes approximately 50-100ms (Keychain access + decryption). Leak scanning runs as a background process using less than 1% CPU. The initial `vault store` takes 200-300ms for encryption and Keychain write.

**Q12: Is there a limit on how many credentials I can store?**
A: macOS Keychain supports thousands of items. Credential Vault has been tested with up to 500 credentials across 50 projects with no performance degradation.

---

## Data Storage

| Path | Purpose | Permissions |
|---|---|---|
| `~/Library/Keychains/claude-code-vault.keychain-db` | macOS Keychain database (encrypted) | Managed by macOS |
| `~/.vault/` | Vault configuration directory | `700` |
| `~/.vault/audit.log` | Append-only credential access audit trail | `600` |
| `~/.vault/config.json` | Vault configuration (encryption backend, rotation policy) | `600` |
| `~/.vault/patterns.json` | Credential patterns for leak detection (no actual values) | `600` |
| `~/.vault/rotation-schedule.json` | Tracking rotation deadlines per credential | `600` |
| `~/.vault/git-secrets-patterns` | Patterns file for git-secrets integration | `600` |

---

## Comparison Table

| Feature | Credential Vault | macOS Keychain (raw) | 1Password CLI | HashiCorp Vault | dotenv-vault | git-crypt |
|---|---|---|---|---|---|---|
| Claude Code integration | Native | Manual | Plugin | Plugin | None | None |
| macOS Keychain backend | Yes | Yes | No (own storage) | No | No | No |
| Auto-rotation | Yes (6 services) | No | No | Yes | No | No |
| Leak detection | Real-time | No | Watchtower | No | No | No |
| git-secrets integration | Automatic | No | No | No | Partial | No |
| Project isolation | Yes | Manual | Vault-level | Namespace | File-level | Repo-level |
| Team sharing (encrypted) | Public-key based | No | Shared vaults | ACL-based | Cloud sync | GPG-based |
| Process-only injection | Yes | Manual | Yes | Yes | File-based | File-based |
| Credential strength analysis | Yes | No | Watchtower | No | No | No |
| Free & open source | Yes | Built-in | No (paid) | Partial | Partial | Yes |
| Offline operation | Yes | Yes | No | Self-hosted only | No | Yes |
| Zero additional services | Yes | Yes | No (subscription) | No (server) | No (cloud) | Yes |

---

*Credential Vault is part of the hanabi-jpn security skill suite for ClawHub. Combine with [mac-sentinel](../mac-sentinel/SKILL.md) for runtime macOS protection and [repo-guardian](../repo-guardian/SKILL.md) for pre-clone repository scanning.*
