---
name: review-cicd
description: CI/CD and deployment reliability audit. Use when pipeline configs, Dockerfiles, K8s manifests, Skaffold config, or GitHub Actions workflows change. Checks build integrity, environment parity, secret hygiene, and rollback safety.
---

# Review CI/CD — Deployment & Pipeline Reliability Audit

## Purpose

Evaluate the reliability, security, and consistency of the CI/CD pipeline and deployment
infrastructure. Use when pipeline configs change, builds feel fragile, deployments fail
unexpectedly, or during periodic infrastructure health checks.

This skill expects (auto-detects from repo layout):

- **CI workflows** — e.g., `.github/workflows/*.yml` (GitHub Actions), `.gitlab-ci.yml` (GitLab), `.circleci/config.yml` (CircleCI), `.azure-pipelines.yml` (Azure), `cloudbuild.yaml` (GCP), `buildspec.yml` (AWS)
- **Dockerfiles** — anywhere in repo (root, `docker/`, `deploy/`, per-service dirs)
- **Kubernetes manifests** — common locations (`k8s/`, `manifests/`, `deploy/k8s/`, `infra/k8s/`)
- **Monorepo build tool** — Turborepo / Nx / pnpm workspaces / Yarn workspaces (detected from root config)

## Expert Panel

You are a review board composed of:

- **CI/CD Pipeline Engineer** — GitHub Actions, build triggers, test gating, caching strategy
- **Container Security Specialist** — Dockerfile best practices, image scanning, layer optimization, secret leakage
- **Kubernetes Platform Engineer** — Manifests, health checks, resource limits, networking, rollbacks
- **Release Engineer** — Versioning, deployment ordering, rollback strategy, environment promotion
- **Monorepo Build Specialist** — Turborepo cache, workspace-aware builds, build order correctness
- **Secret Management Specialist** — No hardcoded secrets, env var hygiene, external secret operators

Each expert must speak separately. No repetition between experts.

## Instructions

### Step 0 — Scope Detection

Detect the base branch (auto: `develop` for GitFlow, `main`/`master` for trunk-based, `release` if used as integration branch):

```bash
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
[ -z "$BASE" ] && for b in develop main master release; do
  git show-ref --verify --quiet "refs/heads/$b" && BASE="$b" && break
done
[ -z "$BASE" ] && BASE=$(git rev-parse --abbrev-ref HEAD)
echo "base=$BASE"
```

Run: `git diff $BASE...HEAD --name-only`

Focus on changes in:

- CI workflows — `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, `.azure-pipelines.yml`, `cloudbuild.yaml`, `buildspec.yml`
- Dockerfiles — `Dockerfile*` anywhere in repo
- Kubernetes manifests — common dirs (`k8s/`, `manifests/`, `deploy/k8s/`, `infra/k8s/`)
- Monorepo build config — `turbo.json`, `nx.json`, `pnpm-workspace.yaml`, `package.json` workspaces
- Version tracking — e.g., `version.info`, `VERSION`, package versions

If no CI/CD files changed, run a baseline audit of the current pipeline and deployment config.

Use `git` commands only — do NOT use `gh` CLI or GitHub API.

### Phase 1 — GitHub Actions Pipeline Integrity

**Step 1a — Audit workflows:**

Read `.github/workflows/`. Apply checks below. Non-pipeline workflows (CodeQL, stale, labeler, etc.) won't trigger pipeline-specific findings — that's expected.

Check:

| Check              | What to verify                                                                                                       |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| Trigger rules      | Which branches trigger CI? Are PRs covered?                                                                          |
| Job dependencies   | Do deploy/version-bump/release jobs depend on prior test/lint/sanity jobs?                                           |
| Step ordering      | Is the sequence: install → audit (security scan) → format → lint → build → test → deploy?                            |
| Runtime version    | Does it match the project's pin file (`.nvmrc`, `.python-version`, `.tool-versions`, etc.)?                          |
| Fail-fast behavior | Does a lint failure block the build? Does a test failure block merge?                                                |
| Cache strategy     | Is the package manager + build tool cache (npm/yarn/pnpm/pip/cargo/go; Turbo/Nx/Bazel) restored AND saved correctly? |

**Step 1b — Test gating:**

For workflows read in 1a, verify:

- A test job exists and runs before deploy/publish/release steps.
- Test job failure blocks downstream jobs (no `continue-on-error: true`; deploy job has `needs: [test]`).
- Workflow triggers on PRs to the protected branch (`on: pull_request`).

Check for branch-protection-as-code:

- `.github/settings.yml` (Probot Settings) — `branches.protection.required_status_checks`
- `.github/rulesets/*` — GitHub native rulesets
- IaC files (`*.tf`, Pulumi) — `github_branch_protection` resources
- `CODEOWNERS` — review enforcement

If none found, flag: actual protection lives in repo settings UI — not auditable from repo. Recommend human verify.

**Step 1c — Cross-workflow conflicts:**

With all workflows already read in 1a, verify no conflicts:

- Two workflows pushing the same image tag or registry path (race condition).
- Two workflows deploying to the same environment without coordination.
- Scheduled workflows (`on: schedule`) overlapping with push/PR workflows on shared resources.
- Missing `concurrency` groups on long-running deploy jobs — runs can stack.
- Broad permissions (`permissions: write-all`) overlapping with least-privilege workflows — escalation surface.

**Step 1d — Secret references:**

```bash
grep -rn "secrets\.\|GITHUB_TOKEN\|GH_TOKEN" .github/workflows/
```

For matches found, verify:

- No secrets used in step `run` commands without `env` indirection (bad: `run: echo ${{ secrets.X }}` — secret expands into shell history/logs; good: `env: TOKEN: ${{ secrets.X }}` + `run: echo $TOKEN` — secret stays in env, masked by Actions).
- Secret names are consistent (not mixing `GITHUB_TOKEN` and `GH_TOKEN` without reason).
- No secrets passed to steps that don't need them.
- Third-party actions pinned by SHA (`uses: owner/action@<commit-sha>`), not by tag (`@v1`) — tags are mutable, SHA is not.

### Phase 2 — Dockerfile Security & Efficiency

**Step 2a — Inventory all Dockerfiles:**

```bash
find . -type f \( -name 'Dockerfile' -o -name 'Dockerfile.*' -o -name '*.Dockerfile' -o -name '*.dockerfile' -o -name 'Containerfile' \) -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null
```

Read each Dockerfile. For every Dockerfile, check:

| Check              | What to verify                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------------- |
| Base image pinning | Is the base image pinned to a specific version (not `:latest`)?                                     |
| Multi-stage builds | Does it use multi-stage to minimize final image size?                                               |
| Non-root user      | Does the final stage run as non-root?                                                               |
| COPY ordering      | Are dependency manifests (`package.json`/`yarn.lock`, `pyproject.toml`/`requirements.txt`, `go.mod`/`go.sum`, `Cargo.toml`/`Cargo.lock`, `Gemfile`/`Gemfile.lock`) copied before source for layer caching? |
| Secret leakage     | Are build args containing secrets (e.g., `GITHUB_TOKEN`) only used in build stages, never in final?                                                                                                      |
| .dockerignore      | Does a `.dockerignore` exist? Does it exclude language-specific build artifacts (`node_modules`, `.venv`, `target/`, `vendor/`, `dist/`, `build/`) and secrets (`.env`, `.git`)?                          |

**Step 2b — Check for hardcoded secrets:**

```bash
grep -rn "password\|secret\|token\|credential\|api.key" . \
  --include="Dockerfile" --include="Dockerfile.*" --include="*.Dockerfile" --include="*.dockerfile" --include="Containerfile" \
  --exclude-dir=node_modules --exclude-dir=.git

grep -rn "ARG.*TOKEN\|ARG.*SECRET\|ARG.*PASSWORD" . \
  --include="Dockerfile" --include="Dockerfile.*" --include="*.Dockerfile" --include="*.dockerfile" --include="Containerfile" \
  --exclude-dir=node_modules --exclude-dir=.git
```

Flag any token or secret that persists into the final image layer.

**Step 2c — Check Dockerfile-to-service alignment:**

```bash
# List Dockerfiles
find . -type f \( -name 'Dockerfile' -o -name 'Dockerfile.*' -o -name '*.Dockerfile' -o -name '*.dockerfile' -o -name 'Containerfile' \) -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null

# List Dockerfiles referenced in build configs
grep -hE "dockerfile:|file:" docker-compose*.yml cloudbuild.yaml buildspec.yml skaffold.yaml 2>/dev/null
```

Verify every Dockerfile is referenced in at least one build config, and every build config references existing Dockerfiles. Flag orphans either way.

### Phase 3 — Kubernetes Manifest Integrity

**Step 3a — Inventory the manifest structure:**

```bash
# Detect Kustomize roots (each kustomization.yaml = a root)
find . -name kustomization.yaml -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null

# Detect Helm charts (each Chart.yaml = chart root)
find . -name Chart.yaml -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null

# Fallback: K8s-shaped YAMLs anywhere (raw manifests, no Kustomize/Helm)
grep -rln "^apiVersion:" . --include="*.yaml" --include="*.yml" --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null
```

If all three return empty, no K8s in repo — skip Phase 3.

**Step 3b — Check Deployment manifests:**

For each Deployment manifest in the repo (identified by `kind: Deployment`), verify:

| Check           | What to verify                                                                            |
| --------------- | ----------------------------------------------------------------------------------------- |
| Health checks   | Does the deployment have `livenessProbe` and `readinessProbe`?                            |
| Resource limits | Are `resources.requests` and `resources.limits` set?                                      |
| Image reference | Does it use the correct image name (matching the image referenced in build configs — see Phase 4)? |
| Replicas        | Is `replicas` set appropriately?                                                          |
| Env vars        | Are env vars sourced from ConfigMaps/Secrets, not hardcoded?                              |
| Port alignment  | Do container ports match service ports?                                                   |

```bash
grep -rln "^kind: Deployment" . --include="*.yaml" --include="*.yml" --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null | while read file; do
  echo "=== $file ==="
  grep -c "livenessProbe\|readinessProbe" "$file"
  grep -c "resources:" "$file"
  grep "image:" "$file"
done
```

**Step 3c — Environment parity check:**

```bash
# Kustomize: discover overlay envs (any name)
find . -type d -path '*/overlays/*' -mindepth 1 -not -path '*/node_modules/*' 2>/dev/null | sort

# Helm: per-env values files
find . -type f \( -name 'values-*.yaml' -o -name 'values.*.yaml' \) -not -path '*/node_modules/*' 2>/dev/null | sort
```

Verify:

- Every environment has the same set of patches (or document why one is missing).
- Config patches don't introduce environment-specific logic that should be in the base.
- Secret store patches reference the correct external secret operator.

**Step 3d — Kustomization integrity:**

```bash
find . -name kustomization.yaml -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | while read kfile; do
  echo "=== $kfile ==="
  cat "$kfile"
done
```

For each `kustomization.yaml`, verify every file listed under `resources:`, `bases:`, `components:`, `patches:`, `patchesStrategicMerge:` exists relative to the file's directory. Flag dangling references.

### Phase 4 — Build Chain Integrity

**Step 4a — Inventory build configs:**

```bash
# Find build orchestration / image build configs (whichever the project uses)
ls -la docker-compose*.yml 2>/dev/null
find . \( -name 'cloudbuild.yaml' -o -name 'buildspec.yml' -o -name 'skaffold.yaml' -o -name 'Dockerfile*' \) -not -path '*/node_modules/*' 2>/dev/null | head -20
```

For each build config found, check:

| Check                | What to verify                                              |
| -------------------- | ----------------------------------------------------------- |
| All services present | Does the config cover all deployable services?              |
| Dockerfile paths     | Does each artifact point to the correct Dockerfile?         |
| Build args           | Are build args (tokens, versions) passed correctly?         |
| Tag policy           | Is the image tag policy consistent and reproducible?        |
| Deploy profiles      | Are per-environment profiles present and correctly scoped?  |

**Step 4b — Verify build-config to K8s alignment (if K8s used):**

```bash
# Images defined in build configs
grep -hE "image:|imageName:" docker-compose*.yml cloudbuild.yaml buildspec.yml skaffold.yaml 2>/dev/null | grep -v "#"

# Images referenced in K8s deployments (common manifest dirs)
find k8s/ manifests/ deploy/k8s/ infra/k8s/ -name '*.yaml' 2>/dev/null | xargs grep -hE "image:" 2>/dev/null
```

Every build-config image name must match a K8s deployment image reference.

### Phase 5 — Secret Hygiene

**Step 5a — Find all secret references across the pipeline:**

```bash
# GitHub Actions secrets
grep -rn "secrets\." .github/workflows/ --include="*.yml" --include="*.yaml"

# K8s external secrets (scan all YAML in repo)
grep -rn "SecretStore\|ExternalSecret\|secretRef\|secretKeyRef" . --include="*.yaml" --include="*.yml" --exclude-dir=node_modules --exclude-dir=.git

# Environment variable files
find . -name ".env.example" -not -path "*/node_modules/*" 2>/dev/null
```

**Step 5b — Check for secret leakage patterns:**

```bash
# Hardcoded values in K8s manifests
grep -rn "password:\|secret:\|token:" . --include="*.yaml" --include="*.yml" --exclude-dir=node_modules --exclude-dir=.git | grep -v "secretKeyRef\|SecretStore\|ExternalSecret\|secretRef"

# Secrets in Dockerfiles that might persist in layers
grep -rn "ENV.*SECRET\|ENV.*TOKEN\|ENV.*PASSWORD" . \
  --include="Dockerfile" --include="Dockerfile.*" --include="*.Dockerfile" --include="*.dockerfile" --include="Containerfile" \
  --exclude-dir=node_modules --exclude-dir=.git
```

Flag any secret that is:

- Hardcoded in a manifest or Dockerfile
- Passed as a build arg that persists in the final image
- Not sourced from an external secret operator

### Phase 6 — Rollback & Production Readiness

Assess:

| Dimension              | What to verify                                                                |
| ---------------------- | ----------------------------------------------------------------------------- |
| Rollback strategy      | Can a bad deployment be rolled back with `kubectl rollout undo`?              |
| Migration safety       | Are DB migrations (if any) backward-compatible?                               |
| Version tracking       | Is the version file (`VERSION`, `version.info`, `package.json`, `pyproject.toml`, `Cargo.toml`, etc.) or git tag updated atomically with the build? |
| Deployment ordering    | Can services be deployed independently, or must they deploy together?         |
| Backward compatibility | Can the new version coexist with the old version during rolling update?       |
| Observability          | Are health endpoints (`/health`, `/health/ready`, `/health/live`) configured? |

```bash
# Check health endpoints in service code (any language)
grep -rn "/health" . --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.rb" --include="*.java" --include="*.cs" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist --exclude-dir=build | head -20

# Check if readiness/liveness probes use the health endpoints
grep -rA5 "readinessProbe\|livenessProbe" . --include="*.yaml" --include="*.yml" --exclude-dir=node_modules --exclude-dir=.git
```

### Phase 7 — Consolidated Pipeline Map

Produce:

**Violation Summary:**

| Violation | Severity                               | File   | Details        |
| --------- | -------------------------------------- | ------ | -------------- |
| _type_    | 🔴 HIGH / 🟡 MEDIUM / 🔵 LOW / ℹ️ INFO | _path_ | _what and why_ |

### Phase 8 — Improvements

If any violations are found, provide two strategies:

**Minimal Safe Fix** (short term, low disruption):

- Specific config corrections
- Missing health checks to add
- Secret references to fix
- Manifest patches to align

**Structural Redesign** (if pipeline is systemically fragile):

- Pipeline restructuring
- Deployment strategy changes
- Secret management migration
- Monitoring and alerting additions

Prioritize by: **Blast radius x Likelihood of failure x Recovery time**

### Phase 9 — Pipeline Safety Score (MANDATORY)

The pipeline safety score is MANDATORY — without a numeric score, pipeline health stays subjective and there's no way to track whether infrastructure changes are improving or degrading deployment reliability over time. Report all scores. Every dimension gets a number, even if it's a 10.

Score the pipeline 1-10 for each dimension:

| Dimension              | Score (1-10) | Justification                                         |
| ---------------------- | ------------ | ----------------------------------------------------- |
| CI test gating         |              | Are tests required to pass before merge/deploy?       |
| Dockerfile security    |              | Base pinning, non-root, no secret leakage             |
| K8s manifest integrity |              | Health checks, resource limits, port alignment        |
| Environment parity     |              | Are environments (overlays, values files) consistent?    |
| Secret hygiene         |              | No hardcoded secrets, external secret operators used     |
| Rollback safety        |              | Can a bad deploy be reverted quickly and safely?         |
| Build chain alignment  |              | Build configs ↔ Dockerfiles ↔ K8s image references match |

**Scoring action table:**

| Score | Action                                                 |
| ----- | ------------------------------------------------------ |
| 9-10  | Report — reliable, no action needed                    |
| 7-8   | Report — acceptable, minor hardening optional          |
| 4-6   | Report — flag for review, fixes recommended            |
| 1-3   | Report — critical risk, immediate remediation required |

Calculate an overall average score.

**Verdict rules:**

- **PASS** — average ≥ 7
- **FLAG** — average 4–6
- **REDESIGN** — average < 4

## Contract

Append this JSON block to every audit output — it is the verifiable contract:

```json
{
  "agent": "review-cicd",
  "branch": "<branch>",
  "date": "<today>",
  "verdict": "PASS|FLAG|REDESIGN",
  "dimensions": {
    "ciTestGating": 0,
    "dockerfileSecurity": 0,
    "k8sManifestIntegrity": 0,
    "environmentParity": 0,
    "secretHygiene": 0,
    "rollbackSafety": 0,
    "buildChainAlignment": 0
  },
  "averageScore": 0,
  "findings": ["specific issues"],
  "improvements": ["specific recommendations"]
}
```

## Output Constraints

- No vague "improve the pipeline" advice.
- Every finding must reference a specific file, line, or configuration.
- Separate confirmed violations from assumptions from unknowns.
- If insufficient information to conclude, state: "Insufficient information to conclude".
- This audit measures deployment reliability — not code quality or test coverage.
- Never recommend disabling or bypassing CI checks.

## Optional: Self-Correction (Manual)

After reviewing the output, you may paste the findings into a new prompt:

> "Here are the findings from my CI/CD audit. Which of these might be incorrect
> due to missing context? What additional data would increase confidence?"

IMPORTANT: This step must be human-initiated — never auto-dismiss findings.
The human decides what to act on.
