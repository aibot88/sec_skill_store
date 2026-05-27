---
name: util-preparek8senv
model: claude-sonnet-4-6
effort: medium
description: >
  Prepare Kubernetes environment infrastructure by generating K8s manifests for all 3rd party
  supporting applications for a single target environment defined in CLAUDE.md. Creates/updates
  ENVIRONMENT.md with per-environment configs and credentials, then generates persistent
  StatefulSet-based K8s manifests for each 3rd party application (databases, message queues,
  caches, SSO, API gateways, etc.) directly in the `environment/` folder. Since the
  `environment/` folder is gitignored, each machine maintains its own independent copy.
  Ensures all services are remotely accessible using tools from DEVTOOL.md.
  Trigger on keywords: "prepare k8s environment", "prepare kubernetes", "setup k8s infra",
  "generate k8s manifests for 3rd party", "prepare environment", "setup infrastructure",
  "prepare k8s", "init k8s environment", "scaffold k8s environment".
  Accepts an optional environment argument to select which Kubernetes environment to generate for.
---

# Util Prepare K8s Environment

Prepare Kubernetes infrastructure by generating K8s manifests for all 3rd party supporting
applications for a **single target environment**. Manifests are generated directly in the
`environment/` folder (no per-environment subfolders). Since the `environment/` folder is
gitignored, each machine maintains its own independent copy of the manifests.

## Input Resolution

This skill accepts an optional `<environment>` argument:

```
/util-preparek8senv [environment]
```

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<environment>` | No | `home_server` | Target environment name — must match a Kubernetes environment in CLAUDE.md |

If omitted:
- If CLAUDE.md defines exactly **one** Kubernetes environment → auto-select it.
- If CLAUDE.md defines **multiple** Kubernetes environments → list them and ask the user to specify.

The environment name is matched **case-insensitively** against the environment headings in CLAUDE.md, accepting snake_case, kebab-case, or title-case input (e.g., `home_server`, `home-server`, `Home Server` all match `## Home Server`).

All other configuration is read from the project root:

| File | Purpose | Required |
|------|---------|----------|
| `CLAUDE.md` | Project detail, environments, 3rd party applications, rules | Yes |
| `ENVIRONMENT.md` | Per-environment configs and credentials for 3rd party apps | Created if missing |
| `DEVTOOL.md` | Local development tools (CLI paths for kubectl, mysql, mongosh, etc.) | Yes |

## Workflow

### 1. Parse CLAUDE.md

Read CLAUDE.md from the project root and extract:

- **Project Code**: From `# Project Detail` → Project Code (e.g., `URP`). Used as K8s namespace (lowercase: `urp`).
- **Environment list**: Each `## <Environment Name>` heading under `# Environment` is an environment. Extract:
  - Environment name (e.g., "Localhost", "Home Server")
  - Snake_case identifier for folder name (e.g., `localhost`, `home_server`)
  - Domain name (e.g., `localhost`, `home.server`) — from the `- Domain:` field
  - Deployment Type (e.g., `Manual`, `Kubernetes`) — from the `- Deployment Type:` field
  - Operating system, Kubernetes distribution/version (for Kubernetes environments)
  - SSH configuration (IP, port) — for remote environments
  - Kube config reference — if mentioned
- **3rd Party Application list**: Each `## <Application Name>` heading under `# Supporting 3rd Party Applications`. Extract:
  - Application name (e.g., "Hub Cache", "Hub Core Database")
  - Technology and version (e.g., "Redis version 7.2.1", "MongoDB version 7.0.6")
  - Databases/database names if applicable
  - Dependencies (`- Depends on:` list)
- **Credential rules**: From `# Rules` section — standard username/password format for new accounts.

**Stop conditions:**
- If `# Environment` section is missing or has no environments → stop with error
- If `# Supporting 3rd Party Applications` section is missing or has no entries → stop with error
- If `DEVTOOL.md` does not exist → stop with error
- If no environment has `Deployment Type: Kubernetes` → stop with error: "No Kubernetes environments found in CLAUDE.md. This skill only generates manifests for environments with Deployment Type: Kubernetes."

### 1b. Target Environment Selection

After parsing all environments, identify Kubernetes environments and select the target:

1. Filter environments to those with `Deployment Type: Kubernetes`.
2. If the user provided an `<environment>` argument, match it against the Kubernetes environments (case-insensitively, accepting snake_case, kebab-case, or title-case).
   - If matched → use it as the target environment.
   - If not matched → list available Kubernetes environments and stop.
3. If no argument was provided:
   - If exactly **one** Kubernetes environment exists → auto-select it.
   - If **multiple** exist → list them and ask the user to specify.

The selected environment is the **target environment** used for Step 2 (ENVIRONMENT.md sync) and Step 3 (K8s manifest generation). Only this one environment is processed.

### 2. Sync ENVIRONMENT.md

#### 2a. ENVIRONMENT.md Does Not Exist

Create a new `ENVIRONMENT.md` at the project root using the template structure below.

#### 2b. ENVIRONMENT.md Already Exists

Treat as **append-only**:
1. Parse the existing ENVIRONMENT.md to identify which environment sections (`# <Environment Name>`) and which service subsections (`## <Service Name>`) exist.
2. Compare against CLAUDE.md:
   - **Missing environment section**: Append the entire environment section with all 3rd party app subsections.
   - **Missing service subsection** under an existing environment: Append the missing service subsection at the end of that environment section.
   - **Missing config keys** under an existing service: Append the missing key lines with `TODO` placeholder values.
   - **Existing config keys**: Do **nothing** — leave existing values as-is, even if they differ from defaults.
3. **Never remove, modify, or reorder** existing sections, headings, or values.

#### 2c. ENVIRONMENT.md Template

```markdown
# Context
- This document contains environment-specific variables and credentials for all 3rd party
  supporting applications used in this project.
- Organized by environment as defined in CLAUDE.md.
- **This file must NOT be committed to version control.**

---

# {{Environment Name}}
{{For localhost:}}
- Kube Config: `{{path to kube config or TODO}}`
{{For remote environments:}}
- SSH Credentials:
  - Username: `{{username or TODO}}`
  - Password: `{{password or TODO}}`
- Kube Config: `{{path to kube config or TODO}}`

## {{3rd Party Application Name}}
- {{Technology}} version {{version}}
{{Technology-specific fields — see Section 2d}}

---
```

#### 2d. Technology-Specific Config Fields

For each 3rd party application, include config fields based on its technology type.
Use credential rules from CLAUDE.md `# Rules` section for default username/password values.
Use `TODO` for any value not yet known.

| Technology | Config Fields |
|-----------|---------------|
| MongoDB | Host, Port, Username, Password, Databases (list) |
| MySQL | Host, Port, Username, Password, Databases (list) |
| Redis | Host, Port, Password, Database Index |
| RabbitMQ | Host, AMQP Port, Admin Port, Username, Password, Vhost |
| Keycloak | Host, HTTP Port, Admin Username, Admin Password, Realm, Client IDs |
| Meilisearch | Host, Port, Master Key |
| Kong | Proxy Host, Proxy Port, Admin Host, Admin Port |
| Mailcatcher | SMTP Host, SMTP Port, HTTP Port |

#### 2e. Custom Docker Image Override

Any service in ENVIRONMENT.md may optionally specify a custom Docker image using the `Docker Image`
field:

- **`Docker Image`**: A Docker image reference (registry, name, and tag).
  Format: `- Docker Image: <image-reference>`
  Example: `- Docker Image: gilacode/hub_single_sign_on:26.5.4`
  The image will be used as-is in the K8s manifest with `imagePullPolicy: IfNotPresent`.

When the `Docker Image` field is not present, the skill falls back to the **official Docker Hub
image** with the exact version from CLAUDE.md (default behavior).

This field is **per-environment** in ENVIRONMENT.md — one environment may use a custom image
while another uses the official image. The skill reads the target environment's section.

**Default values:**
- Host: use the **Domain** from the environment's `- Domain:` field in CLAUDE.md (e.g., `localhost`, `home.server`). If no Domain is specified, fall back to `localhost` for localhost environments or the SSH IP for remote environments. If neither is available, use `TODO`.
- Ports: technology defaults (MongoDB: `27017`, MySQL: `3306`, Redis: `6379`, RabbitMQ AMQP: `5672`, RabbitMQ Admin: `15672`, Keycloak: `8180`, Meilisearch: `7700`, Kong Proxy: `8000`, Kong Admin: `8001`, Mailcatcher SMTP: `1025`, Mailcatcher HTTP: `1080`)
- Username/Password: from CLAUDE.md rules section (default: `bestrnd` / `B3st1n3t@2025`), or technology defaults (e.g., RabbitMQ: `guest`/`guest`, MongoDB: no auth)

### 3. Generate K8s Manifests

#### 3a. Ensure Folder Structure

1. Check if `environment/` folder exists at the project root. If not, create it.

Resulting structure (all manifests directly in `environment/`):
```
environment/
  namespace.yaml
  smtp_server.yaml
  hub_cache_pvc.yaml
  hub_cache.yaml
  hub_core_database_pvc.yaml
  hub_core_database.yaml
  ...
```

#### 3b. Generate Namespace Manifest

Create `environment/namespace.yaml`:
- Namespace name: project code in lowercase (e.g., `urp`)
- Identical regardless of environment

#### 3c. Generate PVC Manifests (Separate Files)

For each 3rd party application that requires data persistence (databases, message queues, caches),
generate a **separate** PVC file: `environment/<service_snake_case>_pvc.yaml`.

**Why separate files:** If the PVC is bundled inside the service manifest, running
`kubectl delete -f <service>.yaml` followed by `kubectl apply -f <service>.yaml` would delete
and recreate the PVC, destroying all persisted data. Keeping the PVC in its own file ensures
that `kubectl delete -f <service>.yaml` only removes the StatefulSet, ConfigMap, Secret, and
Services — the PVC (and its data) remains untouched.

The PVC file contains only the PersistentVolumeClaim resource:

```yaml
# ==============================================================================
# {{Application Name}} ({{Technology}}) — PersistentVolumeClaim
# ==============================================================================
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{service-name}}-pvc
  namespace: {{namespace}}
  labels:
    app: {{service-name}}
    project: {{project-code}}
    environment: {{environment}}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: {{size — see Section 3d for defaults per technology}}
```

#### 3d-svc. Generate Per-Service Manifests

For each 3rd party application, generate `environment/<service_snake_case>.yaml` containing a multi-document YAML (separated by `---`) with:

1. **ConfigMap** — non-sensitive configuration (hostnames, ports, database names, vhosts)
2. **Secret** — sensitive configuration (passwords, admin credentials), base64-encoded. Read actual values from ENVIRONMENT.md for the matching environment.
3. **StatefulSet** (NOT Deployment) — ensures persistent identity, stable network IDs, and ordered scaling:
   - **Image resolution** (checked in ENVIRONMENT.md for the target environment — see Section 2e):
     1. If `Docker Image` is specified → use the exact image reference as-is. Set `imagePullPolicy: IfNotPresent`. Do NOT include `args` or `command` — the custom image's `ENTRYPOINT`/`CMD` handles startup.
     2. Otherwise → use the official Docker Hub image with the exact version from CLAUDE.md (e.g., `mongo:7.0.6`, `mysql:8.4`). Include `args`/`command` as needed by the technology.
   - `volumeMounts` referencing the PVC (defined in the separate `_pvc.yaml` file) for data persistence
   - `env` or `envFrom` referencing ConfigMap and Secret
   - Resource requests/limits (sensible defaults per technology)
   - Readiness and liveness probes (technology-appropriate)
   - `serviceName` matching the headless Service name
4. **Service** — two services per StatefulSet:
   - **Headless Service** (`clusterIP: None`) — for StatefulSet stable DNS
   - **NodePort Service** — for remote access from developer machines and CLI tools.
     Use a deterministic NodePort assignment strategy to avoid conflicts:
     - Base port = `30000 + (index * 10)` where index is the service's position in alphabetical order
     - Map each technology's primary port to the NodePort
5. **Init containers** (if the service depends on another service):
   - E.g., Keycloak depends on Hub Support Database — add an init container that waits for MySQL to be ready before starting Keycloak

**Important:** The service manifest must NOT contain the PersistentVolumeClaim. It only references the PVC by `claimName` in the StatefulSet's `volumes` section.

#### 3d. Technology-Specific Manifest Details

**MongoDB:**
- Image: `mongo:{version}`
- PVC: 5Gi default
- Ports: 27017
- Env: `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD` (from Secret, or skip if no auth)
- Init script: create databases listed in CLAUDE.md via ConfigMap-mounted init script
- Probe: `mongosh --eval "db.adminCommand('ping')"`

**MySQL:**
- Image: `mysql:{version}`
- PVC: 5Gi default
- Ports: 3306
- Env: `MYSQL_ROOT_PASSWORD` (from Secret)
- Init script: create databases listed in CLAUDE.md via ConfigMap-mounted `/docker-entrypoint-initdb.d/` script
- Probe: `mysqladmin ping -h localhost`

**Redis:**
- Image: `redis:{version}`
- PVC: 1Gi default
- Ports: 6379
- Env: `REDIS_PASSWORD` (from Secret, optional — skip if no auth)
- Probe: `redis-cli ping`

**RabbitMQ:**
- Image: `rabbitmq:{version}-management` (include management plugin for admin UI)
- PVC: 2Gi default
- Ports: 5672 (AMQP), 15672 (Management UI)
- Env: `RABBITMQ_DEFAULT_USER`, `RABBITMQ_DEFAULT_PASS`, `RABBITMQ_DEFAULT_VHOST` (from Secret/ConfigMap)
- Probe: `rabbitmq-diagnostics -q ping`

**Keycloak:**
- Image resolution: check ENVIRONMENT.md for `Docker Image` first (see Section 2e).
  - If custom image (e.g., `gilacode/hub_single_sign_on:26.5.4`): use the specified image name; do NOT add `args: ["start-dev"]` (custom image handles startup). Use HTTP Port from ENVIRONMENT.md (typically `8180` for custom builds) for containerPort, probes, and services. Add `KC_HTTP_PORT` to ConfigMap.
  - If no custom image: `quay.io/keycloak/keycloak:{version}` with `args: ["start-dev"]`. Default port `8080`.
- PVC: none (stateless — state is in the database)
- Env: `KC_DB`, `KC_DB_URL`, `KC_DB_USERNAME`, `KC_DB_PASSWORD`, `KC_HEALTH_ENABLED`, `KC_HTTP_ENABLED`, `KC_HOSTNAME_STRICT`, `KC_HTTP_PORT`, `KEYCLOAK_ADMIN`, `KEYCLOAK_ADMIN_PASSWORD` (from Secret/ConfigMap)
- Init container: wait for MySQL (Hub Support Database) to be ready
- Probe: HTTP GET `/health/ready` on the configured HTTP port

**Kong API Gateway:**
- Image: `kong:{version}`
- PVC: none (stateless — DB-less mode or state in database)
- Ports: 8000 (Proxy), 8001 (Admin API)
- Env: `KONG_DATABASE=off`, `KONG_PROXY_LISTEN=0.0.0.0:8000`, `KONG_ADMIN_LISTEN=0.0.0.0:8001`
- Probe: HTTP GET `/status` on admin port

**Mailcatcher (SMTP):**
- Image: `schickling/mailcatcher:{version}` or `sj26/mailcatcher:latest` (if specific version unavailable)
- PVC: none (ephemeral — mail is not persisted)
- Ports: 1025 (SMTP), 1080 (HTTP UI)
- Probe: TCP check on port 1025

**Meilisearch:**
- Image: `getmeili/meilisearch:v{version}`
- PVC: 2Gi default
- Ports: 7700
- Env: `MEILI_MASTER_KEY` (from Secret)
- Probe: HTTP GET `/health`

#### 3e. Create or Update Logic

For each service, there are up to two files to manage in `environment/`:
- `<service_snake_case>_pvc.yaml` — PVC file (only for services that require persistence)
- `<service_snake_case>.yaml` — service manifest (ConfigMap, Secret, StatefulSet, Services)

For each file:

1. **If the file does not exist** (CREATE mode): Generate and write the manifest.
2. **If it already exists** (UPDATE mode):
   - Read the existing manifest
   - Compare against current CLAUDE.md/ENVIRONMENT.md values for the target environment:
     - Version changed → update image tag
     - New databases added → update init scripts
     - Credentials changed in ENVIRONMENT.md → update Secret values
     - New dependencies → add init containers
     - Storage size changed → update PVC (in `_pvc.yaml` only)
   - Preserve any resources marked with `# CUSTOM:` comments
   - Update only the parts that changed
   - Log what was changed

#### 3f. Remote Accessibility

All NodePort Services must be accessible from the developer's machine using the CLI tools
specified in DEVTOOL.md. Include a comment block at the top of each service manifest with
connection instructions:

```yaml
# Service: {{Application Name}} ({{Technology}} {{version}})
# Environment: {{Environment Name}}
#
# Connect from local machine:
#   {{CLI tool from DEVTOOL.md}} {{connection command using NodePort}}
#
# Example:
#   mysql -h {{host}} -P {{nodeport}} -u {{username}} -p{{password}}
#   mongosh mongodb://{{host}}:{{nodeport}}/{{database}}
#   rdcli -h {{host}} -p {{nodeport}}
#   rabbitmqadmin -H {{host}} -P {{nodeport}} list queues
---
```

Use the **Domain** from the target environment's `- Domain:` field in CLAUDE.md as host with NodePort (e.g., `localhost`, `home.server`). If no Domain is specified, fall back to `localhost` for localhost environments or the SSH IP for remote environments.

### 4. Output Summary

Print a summary of all actions taken:

```
## K8s Environment Preparation Summary

### Target Environment
| Environment | Deployment Type | Output Folder |
|-------------|----------------|---------------|
| Home Server | Kubernetes | environment/ |

### ENVIRONMENT.md
| Action | Details |
|--------|---------|
| Created/Updated | Synced Home Server environment, 11 services |

### K8s Manifests Generated
| Service | File | Status |
|---------|------|--------|
| SMTP Server | environment/smtp_server.yaml | Created |
| Hub Cache (PVC) | environment/hub_cache_pvc.yaml | Created |
| Hub Cache | environment/hub_cache.yaml | Created |
| Hub Core Database (PVC) | environment/hub_core_database_pvc.yaml | Created |
| Hub Core Database | environment/hub_core_database.yaml | Created |
| ... | ... | ... |

### NodePort Assignments
| Service | Primary Port | NodePort |
|---------|-------------|----------|
| HC Adapter Message Queue | 5672 | 30000 |
| HC Database | 3306 | 30010 |
| Hub Cache | 6379 | 30020 |
| Hub Core Database | 27017 | 30030 |
| Hub Single Sign On | 8180 (custom) / 8080 (official) | 30040 |
| Hub Support Database | 3306 | 30050 |
| SC API Gateway | 8000 | 30060 |
| SC Adapter Message Queue | 5672 | 30070 |
| SC Database | 3306 | 30080 |
| SMTP Server | 1025 | 30090 |
```

## Important Rules

- **NEVER remove, modify, or delete existing values** in ENVIRONMENT.md. Only add missing sections, services, and config keys.
- **StatefulSet over Deployment** — all 3rd party services use StatefulSet to ensure persistent identity, stable network IDs, and data persistence across pod restarts.
- **PersistentVolumeClaim in separate files** — PVCs MUST be generated in their own `<service>_pvc.yaml` files, never bundled inside the service manifest. This prevents accidental data loss when recreating services with `kubectl delete -f` / `kubectl apply -f`. The service manifest references the PVC by `claimName` only.
- **PersistentVolumeClaim** is mandatory for any service that stores data (databases, message queues, caches). Ephemeral services (Mailcatcher, Kong DB-less) are exempt.
- **NodePort for remote access** — every service must have a NodePort Service so developers can connect using local CLI tools from DEVTOOL.md.
- **Deterministic NodePort assignment** — use alphabetical ordering of service names to assign NodePorts starting from 30000 with interval of 10. This ensures consistent ports across environments and avoids conflicts.
- **Init containers for dependencies** — if a 3rd party app depends on another (e.g., Keycloak → MySQL), add an init container that waits for the dependency to be ready.
- **Image resolution precedence** — for each service, check ENVIRONMENT.md for the target environment's `Docker Image` field first (see Section 2e). If present, use the exact image reference with `imagePullPolicy: IfNotPresent` and do not add `args`/`command`. If absent, fall back to the official Docker Hub image with the exact version from CLAUDE.md (never use `latest`).
- **Namespace isolation** — all manifests use the project namespace (project code lowercase). The namespace manifest is generated once.
- **Credential rules from CLAUDE.md** — when generating default credentials for new services, follow the `# Rules` section in CLAUDE.md for standard username/password format.
- **Idempotent execution** — safe to re-run. Existing manifests are updated only where values changed. Manual customizations marked with `# CUSTOM:` are preserved.
- **ENVIRONMENT.md is the credential source** — K8s Secret values come from ENVIRONMENT.md, not hardcoded. If a value is `TODO` in ENVIRONMENT.md, use `TODO` (base64-encoded) in the Secret and log a warning.
- This skill only generates manifests for **3rd party supporting applications** — NOT for custom applications (those are handled by `depgen-k8s`).
