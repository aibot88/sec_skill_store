---
name: op-service-accounts
description: Use this skill when the user is setting up 1Password for headless / CI / production environments — anything involving service accounts (`op service-account create`), service account tokens, `OP_SERVICE_ACCOUNT_TOKEN`, Connect servers (`op connect`), `OP_CONNECT_HOST`/`OP_CONNECT_TOKEN`, GitHub Actions integration, deploying with 1Password secrets, the events-api integration, or scoping 1Password access for automation.
version: 1.0.0
---

# Service accounts and Connect servers

Two ways to give automation access to 1Password without a human:

| | Service Accounts | Connect (self-hosted) |
|---|---|---|
| Where it runs | 1Password.com | Your infra (Docker/K8s) |
| Setup | One CLI command | Run a server, generate creds |
| Network egress to 1Password.com | Per-call | Once at server boot |
| Best for | CI/CD, scripts, small-to-medium | High-throughput, on-prem, regulated |
| Vault scope | Selected vaults, granular permissions | Selected vaults |
| Personal/Private/Employee vault | **No access** | **No access** |

For most cases, **service accounts**. Connect when you have throughput, latency, or compliance reasons to keep the secrets path inside your network.

## Service accounts

### Create

```bash
op service-account create <name> [flags]
```

| Flag | Purpose |
|---|---|
| `--vault <vault>:<perms>` | Repeatable. Permissions: `read_items`, `write_items`, `share_items`. `write_items` and `share_items` require `read_items`. Default if no perms: `read_items`. |
| `--expires-in <duration>` | Token TTL — e.g., `90d`, `24h`, `4w`. No expiry if omitted. |
| `--can-create-vaults` | Allow the SA to create new vaults. |
| `--raw` | Print only the token (for piping into a secret store). |

The token is shown **once**. Store it immediately; you can't retrieve it again.

```bash
op service-account create "ci-prod-deploy" \
  --vault Prod:read_items \
  --vault "CI Tokens":read_items,write_items \
  --expires-in 90d
```

```bash
TOKEN=$(op service-account create "ci-build" --vault Build:read_items --expires-in 30d --raw)
gh secret set OP_SERVICE_ACCOUNT_TOKEN --body "$TOKEN" --repo myorg/myrepo
unset TOKEN
```

### Use

```bash
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."
op vault list                # works without any signin
op read op://Prod/db/password
op run --env-file=.env -- ./bin/app
```

The token bypasses interactive auth entirely. `op signin` is not needed and `op whoami` will report the service account identity.

### Limitations and rules

- **Cannot access Personal, Private, or Employee vaults** — these are user-only.
- **Cannot manage users, groups, or vaults' membership** — administrative ops require an interactive admin.
- **Cannot enroll in shell plugins** (`op plugin init` requires desktop biometric).
- **Token rotation:** create a new SA + token, swap it in CI, then delete or expire the old one.
- **Rate limits:**
  ```bash
  op service-account ratelimit       # show current limit + usage
  ```

### List service accounts

```bash
op service-account list
```

(Then drill in via the desktop app for full audit history.)

## CI / production patterns

### GitHub Actions

Use the official action when possible:

```yaml
- uses: 1password/load-secrets-action@v2
  with:
    export-env: true
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
    DATABASE_URL: op://Prod/db/connection_string
    STRIPE_KEY: op://Prod/stripe/api-key
- run: ./bin/migrate && ./bin/start
```

Or install `op` and use `op run`:

```yaml
- uses: 1password/install-cli-action@v1
- run: op run --env-file=.env -- ./bin/migrate
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
```

### Other CI (CircleCI, GitLab, Jenkins, etc.)

```bash
# Install op
curl -sSf https://cache.agilebits.com/dist/1P/op2/pkg/v2.34.0/op_linux_amd64_v2.34.0.zip | \
  busybox unzip -o - -d /usr/local/bin op
chmod +x /usr/local/bin/op

# Use it
export OP_SERVICE_ACCOUNT_TOKEN="$OP_SERVICE_ACCOUNT_TOKEN"
op run --env-file=.env -- ./build.sh
```

(Pin to a known version. Always set `OP_SERVICE_ACCOUNT_TOKEN` from the CI's secret store, never inline.)

### Docker

```dockerfile
FROM 1password/op:2 AS op
FROM node:20-slim
COPY --from=op /usr/local/bin/op /usr/local/bin/op
COPY .env package.json ./
RUN npm ci
COPY . .
ENTRYPOINT ["op", "run", "--env-file=.env", "--"]
CMD ["node", "server.js"]
```

```bash
docker run --rm -e OP_SERVICE_ACCOUNT_TOKEN myapp
```

### Kubernetes — 1Password Operator

Install the operator, create `OnePasswordItem` CRDs that reference items, and the operator creates corresponding `Secret` resources. Cleaner than running `op` inside containers. See <https://developer.1password.com/docs/k8s/>.

Alternative without the operator: render manifests at deploy time:

```bash
op inject -i deploy.yaml.tpl | kubectl apply -f -
```

## Connect (self-hosted secrets API)

Run a Connect server in your infra, then `op` (and the SDKs) talk to it instead of 1Password.com.

### Provision

```bash
# Create the server config (downloads 1password-credentials.json)
op connect server create "us-east-1" --vaults Prod,Staging
# Issue a token for the server
op connect token create "us-east-1" "deploy-token" --vaults Prod
```

Two artifacts:
- `1password-credentials.json` — server's identity. Mount into the Connect container.
- The **token** (printed once) — what clients send.

### Run the server

```yaml
# docker-compose.yml
services:
  op-connect-api:
    image: 1password/connect-api:latest
    ports: ["8080:8080"]
    volumes:
      - ./1password-credentials.json:/home/opuser/.op/1password-credentials.json
      - data:/home/opuser/.op/data
  op-connect-sync:
    image: 1password/connect-sync:latest
    volumes:
      - ./1password-credentials.json:/home/opuser/.op/1password-credentials.json
      - data:/home/opuser/.op/data
volumes:
  data:
```

### Use Connect from `op`

```bash
export OP_CONNECT_HOST="http://op-connect.internal:8080"
export OP_CONNECT_TOKEN="eyJ..."
op vault list                            # talks to Connect, not 1Password.com
op read op://Prod/db/password
op run --env-file=.env -- ./bin/app
```

### Connect management

```bash
op connect server list
op connect server get "us-east-1"
op connect server edit "us-east-1" --name "us-east-1-prod"
op connect server delete "us-east-1"          # invalidates all its tokens

op connect token list
op connect token create "us-east-1" "deploy" --vaults Prod
op connect token edit   "us-east-1" "deploy" --name "deploy-2026"
op connect token delete "us-east-1" "deploy"

op connect vault grant  "us-east-1" --vault Staging
op connect vault revoke "us-east-1" --vault OldVault

op connect group grant  --group "DevOps"
op connect group revoke --group "DevOps"
```

### Token scoping

Token permissions inherit from the server's vault grants by default. Restrict per-token to read-only or write-only:

```bash
op connect token create "us-east-1" "read-only" --vaults Prod:r
op connect token create "us-east-1" "writer"    --vaults Audit:w
```

`r` = read items, `w` = write items, `r,w` = both.

## Events API

Audit/event integrations (sign-in attempts, item usages, audit events) use a separate token type:

```bash
op events-api create "Splunk-prod" \
  --features signinattempts,itemusages,auditevents \
  [--expires-in 1y]
```

The token is printed once. Configure your SIEM (Splunk, Elastic, Datadog, etc.) with the 1Password Events API integration using this token. Available features: `signinattempts`, `itemusages`, `auditevents`.

## Decision tree

- **Local dev (interactive)** → desktop app integration + `op signin`. No service account needed.
- **CI/CD pipelines** → service account. Cheapest, simplest.
- **Production app reading secrets at startup** → service account; if throughput >10/s sustained or you're in a regulated environment, Connect.
- **K8s production** → 1Password Operator (uses Connect under the hood).
- **SIEM ingestion** → events-api token.

## Gotchas

1. **`OP_SERVICE_ACCOUNT_TOKEN` and `op signin` shouldn't both be set.** The token wins, but it's confusing. Pick one mode per shell.
2. **SA tokens have no expiry by default.** Pass `--expires-in` and rotate. Treat them like long-lived API keys.
3. **Connect's `1password-credentials.json` is the server's identity** — losing it means re-creating the Connect server. Back it up to a secure store.
4. **Connect tokens are tied to a server.** Deleting `op connect server delete` invalidates every token issued for it.
5. **Events API tokens are read-only and feature-scoped.** They cannot read item contents or do anything except stream the configured event types.
6. **Service accounts can't run `op item template`** in some early CLI versions — if you hit `unauthorized`, check version and consider using a JSON file you produced once interactively as your template.
