---
name: op-signin
description: Sign in to the 1Password CLI. Idempotent — does nothing if already authed. Reports current account.
argument-hint: "[--account <shorthand>]"
allowed-tools: Bash(op signin:*), Bash(op whoami:*), Bash(op account list:*)
---

# /op-signin

Sign the user in to 1Password CLI and confirm success.

## Steps

1. Check if already signed in:
   ```bash
   op whoami
   ```
   If it succeeds, the user is authed. Report the account info from the output and stop.

2. If `op whoami` fails with "no signed-in accounts", run:
   ```bash
   op signin $ARGUMENTS
   ```
   `op signin` is idempotent and uses the desktop app integration — it will trigger biometric (Touch ID / Windows Hello / system auth). If the desktop app integration isn't enabled, the command will print instructions; do not retry, instead relay the instructions to the user.

3. After signin, run `op whoami` again to confirm and report the account.

4. If the user passed `--account <shorthand>` in `$ARGUMENTS`, that account is selected. Otherwise the most-recently-used account is used (per `OP_ACCOUNT` env var if set).

## If `OP_SERVICE_ACCOUNT_TOKEN` is set

Don't run `op signin` — service-account auth is automatic. Just run `op whoami` and report the service account identity.

## On failure

- "1Password app is not running" → tell the user to start the 1Password desktop app and re-run.
- "1Password CLI integration is not turned on" → tell the user to enable **Settings > Developer > Integrate with 1Password CLI** in the 1Password app, then re-run.
- "no biometric unlock" → tell the user to enable Touch ID / Windows Hello in **Settings > Security**.

Don't try to install or configure 1Password automatically — these are one-time interactive setup steps.
