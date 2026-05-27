---
name: op-secrets-injection
description: Use this skill when the user is loading 1Password secrets into a running process or config file — anything involving `op run`, `op inject`, `op read`, `.env` files containing `op://...` references, secret-reference template syntax, the `{{ op://... }}` placeholder format, populating YAML/JSON/TOML config from a template, or wiring 1Password into Docker/Kubernetes/CI/CD. Also use when the user asks how to keep secrets out of `.env`, source control, or shell history.
version: 1.0.0
---

# Loading secrets at runtime: `op read`, `op inject`, `op run`

Three commands solve three different problems. Pick by destination, not by habit.

| Destination | Use |
|---|---|
| Single secret value, transient (one shell command) | `op read` |
| Config file on disk (or stdin/stdout pipeline) with placeholders | `op inject` |
| Process that expects env vars (most apps, dev servers, scripts) | `op run` |

## `op read` — single secret to stdout

```
op read [flags] <secret-reference>
```

| Flag | Purpose |
|---|---|
| `-o, --out-file <path>` | Write to file instead of stdout. |
| `--file-mode <octal>` | Output file mode (default `0600`). |
| `-n, --no-newline` | Suppress trailing newline. |
| `-f, --force` | Overwrite existing file without prompt. |

### Reference query parameters

Append `?attribute=...` or `?ssh-format=...` to extract derived values:

```bash
op read "op://prod/2fa/otp-field?attribute=otp"            # current 6-digit code
op read "op://prod/login/password?attribute=type"          # field type metadata
op read "op://prod/ssh-key/private key?ssh-format=openssh" # OpenSSH-formatted key
```

### Inline in commands

This is fine when the secret is needed once and won't end up in `ps` output for long:

```bash
docker login -u "$(op read op://prod/docker/user)" -p "$(op read op://prod/docker/pass)"
psql "$(op read op://prod/db/connection_string)"
```

For long-running commands, prefer `op run` — exposing secrets via `$(...)` puts them in the parent shell's argv briefly.

## `op inject` — render a templated file

```
op inject [flags]
```

| Flag | Purpose |
|---|---|
| `-i, --in-file <path>` | Template input. If omitted, reads stdin. |
| `-o, --out-file <path>` | Output destination. If omitted, writes stdout. |
| `--file-mode <octal>` | Output file mode (default `0600`). |
| `-f, --force` | Overwrite existing output. |

### Template syntax

Two reference forms are accepted in templates:

```
unenclosed:   op://vault/item/field
enclosed:     {{ op://vault/item/field }}
```

Use **enclosed** in nearly every case — they're robust around adjacent text:

```yaml
database_url: postgres://{{ op://prod/db/user }}:{{ op://prod/db/pass }}@{{ op://prod/db/host }}/{{ op://prod/db/name }}
```

Unenclosed references end at the first character outside `[A-Za-z0-9_.?\-]`, which makes adjacent characters dangerous.

### Environment-variable interpolation in templates

Templates can also expand env vars, with default-value support:

```
${VAR}            ${VAR:-default}
$VAR              op://${ENV:-dev}/db/password
```

Combined: a single template handles dev/staging/prod by exporting `ENV` differently before each `op inject`.

### Streaming when you don't need the file on disk

```bash
op inject -i nginx.conf.tpl | docker run -i --rm nginx nginx -c /dev/stdin -t
op inject -i app.yaml.tpl | kubectl apply -f -
```

This avoids the "delete the resolved file when done" rule entirely.

### When you must write the file

Always treat output as plaintext-secret material:

```bash
op inject -i config.yml.tpl -o config.yml
trap 'shred -u config.yml 2>/dev/null || rm -f config.yml' EXIT
# ... start app that reads config.yml ...
```

Add the resolved filename to `.gitignore`.

## `op run` — exec a command with secrets in env

```
op run [flags] -- <command> [args...]
```

| Flag | Purpose |
|---|---|
| `--env-file <path>` | Load env vars from a dotenv file. Repeatable; later files win on conflict. |
| `--no-masking` | Don't redact secrets in the subprocess's stdout/stderr. |

### The dotenv pattern (recommended for app dev)

`.env` contains references, not values. Commit it. The plaintext secrets never touch disk:

```bash
# .env — safe to commit
DATABASE_URL=op://prod/db/connection_string
STRIPE_SECRET_KEY=op://prod/stripe/api-key
JWT_SIGNING_KEY=op://prod/auth/jwt-key
SENTRY_DSN=op://prod/sentry/dsn
```

```bash
op run --env-file=.env -- npm run dev
op run --env-file=.env -- python manage.py runserver
op run --env-file=.env -- ./bin/server
```

### Multi-environment with one template

`.env` references a variable substituted at run time:

```bash
# .env
DATABASE_URL=op://${APP_ENV}/db/connection_string
API_KEY=op://${APP_ENV}/api/key
```

```bash
APP_ENV=staging op run --env-file=.env -- ./bin/server
APP_ENV=prod    op run --env-file=.env -- ./bin/server
```

### Chained references (env var → secret reference)

Set the env var to a reference, then use a subshell so `$VAR` expands *inside* the subprocess (after `op run` has substituted):

```bash
DB_PASS=op://prod/db/password op run -- sh -c 'echo "$DB_PASS" | psql ...'
```

The wrong way (broken):
```bash
DB_PASS=op://prod/db/password op run -- echo "$DB_PASS"
# parent shell expands $DB_PASS to the literal "op://..." string before op run sees it
```

### Masking

By default, secrets passed via env are redacted from the child process's stdout/stderr. Helpful for screenshare/CI logs. Disable with `--no-masking` (or `OP_RUN_NO_MASKING=true`) only for debugging.

### Multiple env files

```bash
op run --env-file=.env.shared --env-file=.env.local -- ./bin/server
```

Later files override earlier files for the same key.

## CI / production patterns

### GitHub Actions

```yaml
- uses: 1password/load-secrets-action@v2
  with:
    export-env: true
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
    DATABASE_URL: op://prod/db/connection_string
    STRIPE_KEY: op://prod/stripe/api-key
- run: ./bin/migrate && ./bin/start
```

If you don't want the Action, raw `op` works:
```yaml
- run: |
    curl -sSf https://downloads.1password.com/linux/keys/1password.asc | sudo gpg --dearmor -o /usr/share/keyrings/1password-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" | sudo tee /etc/apt/sources.list.d/1password.sources
    sudo apt update && sudo apt install -y 1password-cli
    op run --env-file=.env -- ./bin/migrate
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
```

### Docker (build vs run)

**Don't bake secrets into images.** Inject at run time:

```bash
docker run --rm \
  -e OP_SERVICE_ACCOUNT_TOKEN \
  -v "$PWD/.env:/app/.env:ro" \
  -v "$(which op):/usr/local/bin/op:ro" \
  myapp:latest \
  op run --env-file=/app/.env -- /app/bin/start
```

Better: use the official `1password/op` image multi-stage to bake `op` into your runtime image, then run as above.

### Kubernetes

Use the [1Password Operator](https://developer.1password.com/docs/k8s/) or render `Secret` manifests with `op inject` at deploy time:

```bash
op inject -i secret.yaml.tpl | kubectl apply -f -
```

## Anti-patterns to flag

- A `.env` file with plaintext values committed to a repo. Replace values with `op://...` references and run via `op run --env-file`.
- `op read $REF >> ~/.bashrc`. Bakes the value into the dotfile. Use `op run` or read on demand.
- A script that does `export PASS=$(op read ...)` then runs many subcommands. Acceptable for ad-hoc use; for anything checked in, prefer `op run --env-file=.env -- script.sh`.
- Calling `op read` in a hot loop. Each call hits the local agent / 1Password.com. Read once into a variable, or run the inner work under `op run`.
- Using `--no-masking` in production. It's a debug flag.
