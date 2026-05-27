---
name: reopt-cli
description: Baseline guidance for the reopt CLI — authentication, login, global flags, security rules, and exit codes. Use before other reopt CLI skills or whenever a task involves `reopt login`, `reopt status`, brandapp credentials, or CI automation.
---

# reopt CLI

Baseline guidance for the `reopt` CLI. Load this before resource-specific `reopt` skills.

## When to Apply

Use this skill when:

- a task involves any `reopt` CLI command
- you need to confirm login state
- automation needs Brandapp OAuth credentials
- you are writing CI/CD steps around `reopt`

## Authentication

The CLI has two credential systems.

### User session

Use for interactive browsing and linking:

```bash
reopt login
reopt login --server https://app.reopt.ai
reopt status
reopt logout              # remove the local session token
reopt logout --all        # also wipe every brandapp credential under ~/.reopt/credentials.json
```

Session tokens live in `~/.reopt/auth.json`. When the local token is past
its hard expiry but Better Auth's session-extension window still applies,
the CLI silently refreshes the token on the next command (and on
`brandapp doctor`). No re-login is needed in that window — surface this
fact when scripting CI so users do not over-engineer retry logic.

### Brandapp OAuth credentials

Use for SDK calls and EAV sync:

```bash
export REOPT_CLIENT_ID=your_client_id
export REOPT_CLIENT_SECRET=your_client_secret
```

Or create them interactively:

```bash
reopt brandapp link
```

These credentials are written to `~/.reopt/credentials.json` and `.reopt.json` in the project root.

## Check Auth State

Run this before mutating operations:

```bash
reopt status
reopt status --ping       # also probe the server and report latency
```

If status shows `auth: not logged in`, run `reopt login` first.

## Other Top-Level Commands

| Command | Purpose |
| --- | --- |
| `reopt mcp` | Start a Model Context Protocol server over stdio. Used by IDE / agent integrations; bypasses commander entirely (fast path) and stays alive until stdin closes. |
| `reopt schema [resource]` | Inspect Brandapp resource schemas. Omit `[resource]` to list all available; pass a name to print one schema. Intended for tooling and agents. |
| `reopt completion <bash\|zsh\|fish>` | Print a shell completion script. The script walks the live commander tree (so new subcommands are picked up automatically) and includes aliases. |
| `reopt config list` (alias `ls`) | Show every preference stored in `~/.reopt/preferences.json`. |
| `reopt config get [key]` | Read one preference (or list all when `key` is omitted). |
| `reopt config set <key> <value>` | Persist a preference. Known keys: `server` (default API URL — overridden by `REOPT_CLI_SERVER` and `--server`), `format` (default output format), `interactive` (force prompt on/off, otherwise TTY-detected). |
| `reopt config unset <key>` (alias `rm`) | Remove a preference. |

`reopt config set format table` is the supported way to make a developer
machine default to the human-readable view without changing every command.

## Global Flags

These options are wired at the program level (`program.option(...)`), so
they apply to every subcommand:

| Flag | Default | Purpose |
| --- | --- | --- |
| `--format <type>` | `json` (or `config get format`) | Output format: `json` / `table` / `csv` / `yaml`. JSON is the agent-friendly default. |
| `--fields <fields>` | — | Restrict output to a comma-separated list of field names. |
| `--limit <n>` | — | Cap the number of results returned by list endpoints. |
| `--offset <n>` | — | Skip N results into a list endpoint. |
| `--page-all` | off | Iterate through every page; in JSON mode, output is NDJSON (one record per line). |
| `--page-limit <n>` | `10` | Maximum pages to fetch when `--page-all` is set. |
| `--page-delay <ms>` | `100` | Delay between page requests when `--page-all` is set. |
| `--timeout <ms>` | `30000` | Per-request HTTP timeout. |
| `--max-retries <n>` | `1` | Retry budget for idempotent (GET) requests. |
| `-q, --quiet` | off | Suppress non-essential output. |
| `-v, --verbose` | off | Verbose output (stack traces, debug info). |
| `--no-interactive` | off | Never prompt for missing arguments — fail with a validation error instead. Required for unattended scripts. |

Per-subcommand flags layered on top of the global set:

| Flag | Where | Purpose |
| --- | --- | --- |
| `--json` | several list commands | Legacy alias preserved for backward compatibility — prefer `--format json`. |
| `--dry-run` | EAV sync, brandapp link/unlink | Preview only — no mutation. |
| `--delete-orphans` | EAV sync/status | Include or apply removal of server-only attrs. |
| `-s, --schema <path>` | EAV commands | Custom EAV schema path (default `./eav.schema.ts`). |
| `-o, --out <path>` | EAV pull, eav plan, sync | Custom output path. |
| `-w, --watch` | EAV sync, `brandapp dev` | Watch file changes and re-run. |
| `--server <url>` | `login` | Override the auth server URL. |

## Security Rules

1. Never hardcode credentials.
2. Never print credential values.
3. Never commit files under `~/.reopt/`.
4. Inject secrets through a secret manager in CI.
5. Use `--dry-run` before any mutating EAV operation.
6. When invoking the CLI programmatically, pass arguments as arrays.

## Schema Discovery

```bash
reopt brandapp eav pull --out ./eav.schema.ts
reopt brandapp eav status --json
reopt brandapp eav status --delete-orphans --json
```

## Exit Codes

| Code | Meaning |
| --- | --- |
| `0` | Success |
| `1` | API or network error |
| `2` | Auth error |
| `3` | Validation error |
| `4` | Config error |
| `5` | Internal error |

