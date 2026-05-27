---
name: claude-vault
description: Use this skill whenever the user mentions API keys, passwords, tokens, credentials, secrets, .env files, OAuth tokens, or any sensitive value that needs to end up in code, config, or a command. The skill stores secrets in a vault that the model never reads — you reference them by name and let the claude-vault CLI inject the actual values.
version: 0.1.0
---

# claude-vault — secret handling without seeing plaintext

## The rule

**You must never read, paste, save, echo, or pass plaintext secret values.** All secret operations go through the `claude-vault` CLI. The CLI reads values from a vault that you do not have access to and writes them where they need to go. Your job is to:

1. Recognize when a workflow involves a secret.
2. Generate code/config that references the secret **by name only** (env var or `{{vault:NAME}}` placeholder).
3. Tell the user (or directly run) the right `claude-vault` command to fill in the actual value.

A PreToolUse hook will block obvious leak paths (reading vault files, `op read`, `printenv`, etc.) and a PostToolUse hook will redact known secret patterns from any output you do see. If a hook blocks a tool call, treat it as **the rule working** and propose an alternative — do not look for ways around it.

## When this skill activates

Trigger on any of these signals:

- The user names a credential type: "API key", "password", "token", "secret", "credential", "OAuth", "bearer", "private key".
- The user wants to write or modify `.env`, `.env.local`, `secrets.json`, `config.local.*`, `credentials.*`, or anything they describe as "the file with my keys".
- You're about to write code that reads from `os.environ`, `process.env`, `ENV[...]`, or similar — and the env var holds something sensitive.
- You see `Authorization: Bearer ...`, `OPENAI_API_KEY=...`, `password=...`, or similar patterns in user-supplied content.

## Quick check before any secret work

Run `claude-vault list` first to see what's already in the vault. Names only — no values. This tells you whether a secret already exists or needs to be created.

```bash
claude-vault list
```

If `claude-vault init` hasn't been run yet, run it once. It picks the backend (file / Keychain / 1Password) and creates `~/.claude-vault/`.

## The four standard workflows

### 1. Storing a new secret

User says: "I want to add my OpenAI API key" / "Save this token" / "Set up my AWS credentials".

Run:
```bash
claude-vault set OPENAI_API_KEY
```

The CLI will prompt the user **directly in their terminal** with hidden input. You will not see the value. Do not ask the user to paste the value into chat — that defeats the whole point. If they paste it anyway, treat it as compromised: tell them to rotate it.

Naming convention: `UPPER_SNAKE_CASE`, matches the env var name the value will eventually live under (e.g., `OPENAI_API_KEY`, `STRIPE_SECRET_KEY`, `GITHUB_TOKEN`).

### 2. Using a secret in code

User says: "Add OpenAI integration" / "Use my Stripe key here".

Generate code that reads from an env var — never hardcode:

```python
import os
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

For env files, write the **placeholder** form:

```
# .env
OPENAI_API_KEY={{vault:OPENAI_API_KEY}}
```

Then either run inject yourself or tell the user to:

```bash
claude-vault inject .env
```

This replaces every `{{vault:NAME}}` in the file with the real value. The CLI does the substitution; you only see "injected OPENAI_API_KEY".

### 3. Running a one-off command that needs a secret

User says: "Test this against the live API" / "Run this script with my key".

Don't put the secret in the command line. Use:

```bash
claude-vault use OPENAI_API_KEY=OPENAI_API_KEY -- python script.py
```

`NAME=ENVVAR` says "take the secret named NAME and expose it as env var ENVVAR to the child process". Use the same name on both sides if there's no reason to differ.

### 4. Rotating or removing

```bash
claude-vault set OPENAI_API_KEY    # overwrites with a new value
claude-vault rm OLD_TOKEN
```

After rotation, re-run `claude-vault inject` on any committed-template files.

## Forbidden actions

Do not do any of these — the hooks will block most of them, but you must also not propose them:

- `cat`/`head`/`less`/`tail`/`xxd` of `~/.claude-vault/secrets/*` or any file under the vault home.
- `security find-generic-password ... -w` (Keychain read).
- `op read`, `op item get` (1Password read).
- `printenv`, bare `env`, `echo $SECRET_VAR` — these can dump injected values to your tool output.
- Pasting a secret value into a Bash command, Edit, Write, or any text response.
- Asking the user to paste a secret into chat.
- Saving secret values to memory (the auto-memory system).

## When a hook blocks you

You'll see a message like `claude-vault: vault read attempt blocked. Use 'claude-vault inject' or 'claude-vault use' instead.` Don't retry the same call. Switch to the right workflow: if you wanted to read a value, you almost certainly wanted `inject` or `use` instead. Tell the user what you tried, why the hook blocked it, and the correct command.

## When the user does something risky

If the user pastes a plaintext secret into chat, says "just hardcode it for now", or asks you to read the vault — push back briefly:

> That value is now in our chat history. Rotate it, then re-add via `claude-vault set <NAME>`.

For "hardcode for now": offer the inject workflow, which is just as fast and doesn't leak the value into git.

## Backends

The user's chosen backend (file, Keychain, 1Password) is shown by `claude-vault backend`. You don't need to care which one — the CLI abstracts it. The only difference you might see: with 1Password, `set` may open a browser for auth; with Keychain, the user may get a Touch ID prompt.

## Summary

- Never see plaintext. Reference by name.
- `set` (user enters), `list` (names only), `inject` (placeholder → file), `use` (env → child process), `rm` (delete).
- Hooks enforce. Treat blocks as confirmation, not obstacles.
