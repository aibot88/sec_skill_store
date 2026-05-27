---
name: op-shell-plugins
description: Use this skill when the user wants to authenticate third-party CLIs (gh, aws, stripe, doctl, hcloud, etc.) using 1Password instead of plaintext config files or environment variables — anything involving `op plugin init`, `op plugin run`, `op plugin list`, `op plugin inspect`, `op plugin clear`, `~/.op/plugins.sh`, biometric auth for CLIs, or replacing tokens in `~/.aws/credentials` / `~/.config/gh` / etc.
version: 1.0.0
---

# Shell plugins — third-party CLI auth via 1Password

`op plugin` lets the 1Password CLI provision credentials for a third-party CLI on demand, with biometric approval, instead of leaving long-lived tokens on disk.

Supported plugins (partial list — check `op plugin list` for current set): `gh`, `aws`, `stripe`, `doctl`, `hcloud`, `cargo`, `circleci`, `databricks`, `fly`, `heroku`, `linode-cli`, `mongodb-atlas`, `npm`, `okta`, `openai`, `pip`, `sentry-cli`, `tugboat`, `vercel`.

Requires desktop app integration with biometric unlock enabled (no service-account use case for shell plugins — they're for interactive humans).

## The flow

1. Once per CLI: `op plugin init <name>` — interactive prompt creates an item in 1Password (or selects an existing one) and saves a config mapping.
2. Once per shell rc: `source ~/.op/plugins.sh` (so `gh`, `aws`, etc. become aliases to `op plugin run`).
3. Whenever you run the third-party CLI, biometric prompt → 1Password injects the credential as an env var → command runs.

## Initial setup

```bash
op plugin init gh         # GitHub CLI
op plugin init aws        # AWS CLI
op plugin init stripe     # Stripe CLI
```

For each, `op` asks:
- **Which credential to use** — pick existing item or create one.
- **Default scope:**
  - **Use as global default** — `gh` always uses this credential.
  - **Use as default in this directory** — only when CWD is under this directory (per-project).
  - **Prompt me each time** — no default; ask in each terminal session.

Add to your shell rc (`~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`):
```bash
source ~/.op/plugins.sh
```

This file aliases `gh`, `aws`, etc. to `op plugin run gh`, `op plugin run aws`. Open a new shell or `source` the file.

## Daily use

After setup, just use the CLI normally:
```bash
gh repo list
aws s3 ls
stripe customers list
```

Each invocation triggers a biometric prompt (or, after first prompt in a session, reuses the unlocked credential). The third-party CLI sees the credential via its expected env var (e.g., `GITHUB_TOKEN`, `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, `STRIPE_API_KEY`).

## Without `plugins.sh`

If you don't want the auto-aliasing:
```bash
op plugin run -- gh repo list
op plugin run -- aws s3 ls
```

Useful in scripts where you'd rather be explicit, or when troubleshooting.

## Inspecting and clearing config

```bash
op plugin list                    # all available plugins (whether configured or not)
op plugin inspect                 # interactive view of your configurations
op plugin inspect gh              # specific plugin

op plugin clear gh                # remove session/dir/global default in precedence order
op plugin clear gh --all          # remove all (session + dir + global)
```

## Per-project credentials

A common pattern: one team uses `gh` for personal repos and a bot account for CI mirroring. Configure per-directory:

```bash
cd ~/work/teamA-repo
op plugin init gh                 # choose item, set "default in this directory"

cd ~/personal/repo
op plugin init gh                 # choose other item, "default in this directory"
```

In each directory, `gh` uses the right token automatically.

## Replacing existing credential files

After `op plugin init aws`, you can safely delete `~/.aws/credentials` (the file). Same for `~/.config/gh/hosts.yml`'s token, `~/.stripe-cli/config.toml`'s API key, etc. The 1Password version is now the source of truth.

## When NOT to use shell plugins

- **Headless / CI environments.** Shell plugins require biometric auth → desktop app. Use service accounts and `op read`/`op run` instead.
- **Long-running scripts/services.** They'd biometric-prompt on every invocation. Use `op run --env-file` to load credentials once at startup.
- **Plugins that don't exist for your CLI.** Check `op plugin list`. If your CLI isn't there, fall back to setting the env var with `op run`:
  ```bash
  op run -- /path/to/some-cli some-command
  ```
  with a `.env` mapping `SOME_CLI_TOKEN=op://...`.

## Gotchas

1. **`source ~/.op/plugins.sh` must be in your shell rc** for the aliases to work. New terminals won't have them otherwise.
2. **Biometric prompt latency.** Each call has a small UX cost. For a long pipeline of `aws` calls, prefer `op run -- script.sh` so you authenticate once.
3. **The aliases are shell aliases, not symlinks.** They don't work from `make`, `npm scripts`, or anything that bypasses your interactive shell unless that subshell also sources the file. Workaround: `op plugin run -- ...` explicitly, or set the env var with `op run`.
4. **Per-directory defaults are matched by CWD prefix.** Symlinks and `cd -` can confuse the lookup; use `op plugin inspect` to verify which credential is active.
