---
name: coolify-security
description: >
  This skill should be used when securing Coolify deployments, managing secrets and environment
  variables, configuring Docker Build Secrets, setting up RBAC team roles, isolating containers
  on the network, configuring resource limits (CPU/memory), hardening firewall rules (UFW),
  managing terminal access, or auditing Coolify security. Trigger when: "Coolify security",
  "Coolify secrets", "Coolify environment variables security", "Docker Build Secrets Coolify",
  "Coolify RBAC", "Coolify team roles", "Coolify network isolation", "Coolify firewall",
  "UFW Docker Coolify", "Coolify resource limits", "Coolify terminal access",
  "secure Coolify", "harden Coolify", "Coolify permissions", "Coolify audit log",
  "Coolify SSO", "Coolify OAuth".
---

# Coolify Security

Covers secrets management, RBAC, network isolation, resource limits, and access control for Coolify v4 self-hosted.

> **Self-Hosted Responsibility**: Coolify self-hosted means YOU own server security. Coolify manages application-layer orchestration, not OS-level hardening.

## Secrets Management

### Three Types of Secrets in Coolify

| Type | Scope | Visibility | Use For |
|------|-------|------------|---------|
| **Runtime Env Vars** | Running container | Visible via `docker inspect` | Database URLs, API keys, feature flags |
| **Build-time Env Vars** | Build process | Visible in build logs + image layers | npm tokens, build-time API keys |
| **Docker Build Secrets** | Build process only | NOT in image layers or logs | Private registry tokens, signing keys |

### Decision Tree: Where to Put a Secret

```
START: When is this secret needed?
│
├─ Only at runtime (app needs it while running)?
│  └─► Runtime Environment Variable
│      Set "Build Variable" = OFF in Coolify
│
├─ Only at build time (npm install, Docker build)?
│  ├─ Is it acceptable if this value appears in image layers?
│  │  ├─ Yes → Build-time Environment Variable
│  │  └─ No  → Docker Build Secret
│  │          (requires Dockerfile with --mount=type=secret)
│  │
│  └─ None of the above → Docker Build Secret (safest)
│
├─ Needed at both build AND runtime?
│  └─► Two separate entries: one build-time, one runtime
│      Do NOT use build-time alone (baked into image)
│
└─ Shared across multiple apps?
   └─► Shared Environment Variable (project-level or team-level)
       Coolify supports shared variables that multiple resources reference
```

### Docker Build Secrets Pattern

For secrets that must not appear in image layers:

**In Coolify**: Enable "Use Docker Build Secrets" checkbox on the environment variable. Coolify automatically:
1. Passes each build variable via `--secret id=KEY,env=KEY` instead of `--build-arg`
2. Prepends `# syntax=docker/dockerfile:1` to the Dockerfile if missing
3. Auto-injects `--mount=type=secret` into every `RUN` instruction (no manual Dockerfile changes needed)
4. Generates `COOLIFY_BUILD_SECRETS_HASH` to maintain build cache integrity

**No Dockerfile modification required** — Coolify handles the BuildKit secret injection automatically. Coolify uses BuildKit by default, so this works without additional server configuration.

**Manual Dockerfile approach** (if you prefer explicit control):
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
COPY . .
RUN npm run build
```

### Shared Variables (project, environment, team, server scopes)

> **New in beta.471 (April 2026):** Coolify expanded shared variables to four scopes with explicit interpolation syntax. Earlier versions only supported project-level shared variables.

**Four scopes available:**

| Scope | Where | Interpolation syntax | Use case |
|---|---|---|---|
| **Server** | Server settings | `{{server.VAR}}` | Variables specific to one host (e.g., `BACKUP_S3_BUCKET` per server) |
| **Team** | Team settings | `{{team.VAR}}` | Org-wide values (e.g., `MONITORING_API_KEY`) |
| **Project** | Project → Shared Variables | `{{project.VAR}}` | Project-wide config (e.g., `STRIPE_PUBLISHABLE_KEY` shared across services) |
| **Environment** | Project → Environment | `{{environment.VAR}}` | Per-environment overrides (`{{environment.DATABASE_URL}}` differs between staging and production) |

**Reference example:**
```
DATABASE_URL={{environment.DATABASE_URL}}
STRIPE_KEY={{project.STRIPE_PUBLISHABLE_KEY}}
SLACK_WEBHOOK={{team.SLACK_DEPLOY_WEBHOOK}}
```

**Rotation:** Update the shared variable and redeploy affected applications. There is no automatic propagation — redeployment is required. Plan rotation around your deployment cadence.

**Older Coolify versions:** Only project-level shared variables exist; the team/environment/server scopes are unavailable. Verify `coolify_version` MCP tool returns ≥ beta.471 before relying on them.

## RBAC (Role-Based Access Control)

### Team Roles

| Role | Capabilities | Limitations |
|------|-------------|-------------|
| **Owner** | Full access: create/delete all resources, manage team members, access all settings, view/edit all secrets, terminal access, manage servers and billing | None |
| **Admin** | Manage apps/databases/projects, delete member-created resources, modify terminal access settings | Cannot delete owner-created resources, cannot manage users or servers |
| **Member** | View and collaborate on assigned projects, see redacted secrets, delete own deployments | Cannot manage team members, cannot modify server settings, limited secret visibility |

### Permission Scope

Coolify v4 RBAC operates at the **team** level:
- Each team has its own servers, projects, and resources
- Users can belong to multiple teams with different roles
- Resources (servers, apps, databases) belong to a team
- No per-app or per-server granular permissions within a team
- API tokens are team-scoped with permission levels: `read-only`, `read:sensitive`, `*` (full CRUD), or `deploy` (trigger deploy only)

### Known RBAC Limitations

- No per-resource permissions (e.g., "admin can deploy app A but not app B") — planned for v4 stable or v5
- No custom roles (only Owner/Admin/Member)
- No SAML/LDAP/OIDC natively — only OAuth via GitHub, GitLab, Google, Azure, Bitbucket
- No audit log for who changed what (environment variables, settings) — Issue #2525
- Terminal access is all-or-nothing per server (cannot selectively disable for Members while keeping it for Admins)
- All env vars in Docker Compose projects are injected into ALL containers — Issue #7655 (deferred to v5)

**Workaround for per-app isolation**: Create separate teams for each project or security boundary. Each team has its own resources and RBAC.

## Network Isolation

### The `coolify` Docker Network

All Coolify-managed containers join the `coolify` Docker network (bridge mode):

- **All containers on the same server CAN reach each other** by container name
- Traefik routes external HTTP/HTTPS traffic to containers
- Non-HTTP ports are not exposed externally by default

### Isolating Apps from Each Other

To prevent two apps on the same server from communicating:

1. **Separate Docker networks** — Coolify does not natively support per-app networks. Workaround: use Docker Compose with custom networks.
2. **Separate servers** — The only guaranteed isolation is running on different servers.
3. **Application-level firewall** — Use iptables rules inside the container (complex, fragile).

**Reality**: Coolify's networking model assumes trust within a server. For true multi-tenant isolation, use separate servers or a container orchestrator with network policies (Kubernetes).

### Exposing Ports

| Method | Access | Use For |
|--------|--------|---------|
| **Traefik routing (default)** | HTTP/HTTPS only, via domain | Web applications |
| **Port mapping** | Any TCP/UDP port on host | Databases, custom protocols |
| **No exposure** | Internal only (coolify network) | Background workers, internal services |

**Security rule**: Only expose ports that must be accessible externally. Default to internal-only.

## UFW and Docker — The Known Conflict

### The Problem

Docker modifies `iptables` directly, bypassing UFW rules. This means:
- UFW `deny` rules do NOT block Docker-published ports
- A database exposed on port 5432 is accessible to the internet even if UFW blocks 5432

### The Fix

```bash
# Option 1: Disable Docker's iptables manipulation (affects ALL containers)
# /etc/docker/daemon.json
{
  "iptables": false
}
# Then restart Docker: systemctl restart docker
# WARNING: This breaks inter-container networking; requires manual iptables rules

# Option 2 (Recommended): Use ufw-docker utility
# https://github.com/chaifeng/ufw-docker
wget -O /usr/local/bin/ufw-docker https://github.com/chaifeng/ufw-docker/raw/master/ufw-docker
chmod +x /usr/local/bin/ufw-docker
ufw-docker install

# Allow specific access
ufw-docker allow <CONTAINER_NAME> 5432/tcp
ufw-docker allow <CONTAINER_NAME> 5432/tcp from 203.0.113.50
```

### Best Practice

- Bind database ports to `127.0.0.1` only: `127.0.0.1:5432:5432` (not `0.0.0.0:5432:5432`)
- Use SSH tunnels for remote database access instead of exposing ports
- Install `ufw-docker` to make UFW rules apply to Docker containers

## Resource Limits

### Setting Limits

In application or database settings:

| Setting | Purpose | Default |
|---------|---------|---------|
| **Memory Limit** | Maximum memory the container can use | Unlimited (dangerous) |
| **Memory Reservation** | Soft limit / guaranteed minimum | Not set |
| **CPU Limit** | Maximum CPU cores (e.g., `1.5`) | Unlimited |
| **CPU Reservation** | Guaranteed CPU minimum | Not set |

### OOM Behavior

When a container hits its memory limit:
1. Docker's OOM killer terminates the container process
2. Coolify's restart policy (`unless-stopped`) restarts the container
3. If the container OOMs repeatedly, it enters a restart loop
4. Check with: `docker inspect <CONTAINER> | grep -i oom`

### Build Process Limits

Build processes do NOT have separate resource limits in Coolify. A runaway build can consume all server resources. Mitigation:
- Use a separate build server (see coolify-infrastructure)
- Set `NODE_OPTIONS=--max-old-space-size=2048` for Node.js builds
- Monitor server resources during builds

## Terminal Access and Auditing

### Terminal Access

Coolify provides a **web terminal** in the UI for running commands inside containers:
- Admin and Developer roles can access the terminal
- Viewer role cannot access the terminal
- Terminal sessions are not logged or audited

### Locking Down Terminal Access

- Assign the **Viewer** role to team members who should not have shell access
- Create separate teams with appropriate roles for different access levels
- There is no way to allow deployment but deny terminal access within the same role

### Audit Logging

**Current state**: Coolify v4 has limited audit logging:
- Deployment history is logged (who triggered, when, status)
- Environment variable changes are NOT audited
- Terminal sessions are NOT logged
- API access is NOT logged per-request

**Workaround**: Enable server-level auditd for SSH and Docker command logging.

## Anti-Patterns

| Anti-Pattern | Consequence |
|-------------|-------------|
| Storing secrets as build-time env vars when only needed at runtime | Secrets baked into Docker image layers, extractable via `docker history` |
| Using the same API token for all CI/CD pipelines | Compromising one pipeline compromises everything |
| Not setting memory limits on any container | One runaway process can OOM-kill the entire server |
| Relying on UFW alone to protect Docker-published ports | UFW rules are bypassed by Docker's iptables manipulation |
| Giving Developer role to users who should be Viewers | Developers can access terminal, modify env vars, trigger deployments |
| Running containers as root without `USER` directive | Container escape gives root on host if Docker is not hardened |
| Using `--privileged` flag on any container | Full host access; defeats all container isolation |
| Exposing database ports to 0.0.0.0 | Database accessible from any IP; bots will find it |
| Not rotating API tokens or database credentials | Long-lived credentials increase blast radius of compromise |
| Sharing one team for all projects | No isolation between projects; one compromised member affects everything |

## Related Skills

- **coolify-deploy** — Build secrets configuration, environment variable setup
- **coolify-databases** — Database credential management, SSL configuration
- **coolify-infrastructure** — Server-level security, SSH configuration
- **coolify-troubleshoot** — Diagnosing OOM kills, network issues

## Additional Resources

### Reference Files

- **`references/hardening-checklist.md`** — Step-by-step server and Coolify hardening guide
- **`references/ufw-docker-guide.md`** — Complete UFW + Docker configuration with ufw-docker utility
