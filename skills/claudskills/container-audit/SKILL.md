---
name: container-audit
description: Audit Dockerfiles and docker-compose files for base image, user privileges, secret leaks, layer efficiency, signal handling, healthchecks, and compose safety. One sub-agent per Dockerfile. Static, live (Trivy/Grype), and apply modes.
argument-hint: [dockerfile-path-or-glob]
allowed-tools: Read Grep Glob Write Edit Bash(bash:*) Agent
effort: high
paths: "**/Dockerfile*"
---

# Container Audit

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/container-audit/`.
> Run `mkdir -p .anthril/audits/container-audit` before the first `Write` call.
> Primary artefact: `.anthril/audits/container-audit/<artefact>`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## When to use

Run this skill when the user mentions:
- Dockerfile review, container security, image hardening
- CIS Docker Benchmark
- docker-compose audit
- Image size optimisation
- Secret leaks in container builds

Covers eight categories: base image choice (distroless/alpine, digest pinning), user privileges (non-root, dropped capabilities, read-only filesystem), secret leaks (no ARG/ENV secrets, BuildKit `--mount=type=secret`), layer efficiency (multi-stage, `COPY --from`, cache ordering), signal handling (tini, STOPSIGNAL, exec-form CMD), healthchecks, `.dockerignore` coverage, and docker-compose safety (no `privileged: true`, no host network, resource limits).

## Before You Start

1. **Determine operating mode.** `--live` enables `docker inspect`, `docker history`, and Trivy/Grype scans. `--apply` enables per-finding Dockerfile patching. `--runtime` is not applicable for this skill (there is no safe runtime test for a Dockerfile without a target environment).
2. **Find all Dockerfiles and compose files.** Run `scripts/list-dockerfiles.sh`.
3. **Sub-agent budget.** One `Agent(subagent_type=Explore)` per Dockerfile. Warn above 10 files.
4. **Load `.container-ignore`** for suppression rules.

## User Context

$ARGUMENTS

Container inventory: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/container-audit/scripts/list-dockerfiles.sh"`

Live mode availability: !`which docker 2>/dev/null || echo "docker:unavailable"` · !`which trivy 2>/dev/null || echo "trivy:unavailable"`

---

## Audit Phases

### Phase 1: Discovery & Mode Selection

1. Parse inventory output. Separate Dockerfiles, docker-compose files, `.dockerignore` files.
2. Confirm scope and mode with the user.
3. In `--live` mode, verify Docker daemon reachable; fall back to static if not.

### Phase 2: Per-Dockerfile Snapshot

For each Dockerfile, extract:

- FROM chain (stage names, base images, tags, digests)
- USER directives
- HEALTHCHECK
- ENTRYPOINT / CMD (exec form vs shell form)
- EXPOSE / ENV / ARG
- COPY patterns (source paths, `--from` references, `--chown`)
- RUN commands (shell-parsed)
- BuildKit-specific syntax (`--mount=type=secret`, `--mount=type=cache`)

In `--live` mode, additionally:
- Run `docker history <image>` for size-per-layer breakdown.
- Run `trivy image <image> --severity HIGH,CRITICAL --quiet` (or `grype`, `snyk container`) for CVE surface.
- Run `docker inspect <image>` for final USER, Entrypoint, and exposed ports.

### Phase 3: Parallel Sub-Agent Audit

Spawn one `Agent(subagent_type=Explore)` per Dockerfile (single assistant message). Each walks categories A–H from `reference.md` §1:

- **A. Base image** — distroless/alpine/scratch where possible, pinned by digest, from a trusted registry
- **B. User & privileges** — explicit non-root USER before ENTRYPOINT, dropped capabilities, read-only FS hint
- **C. Secrets & leaks** — no secrets in ARG/ENV, no copied `.env` files, no hardcoded tokens, BuildKit secrets for build-time
- **D. Layer efficiency** — multi-stage build, `COPY --from=` for artefact, RUN combined with cleanup, layer cache-friendly order
- **E. Signals & shutdown** — tini/dumb-init for PID 1, STOPSIGNAL, exec-form CMD (JSON array, not shell)
- **F. Healthcheck** — HEALTHCHECK present, interval sensible, command meaningful (not just `curl localhost`)
- **G. `.dockerignore`** — excludes `.git`, `node_modules`, `tests/`, `.env*`, OS junk
- **H. docker-compose** — no `privileged: true`, no `network_mode: host`, named volumes, resource limits, no `user: root`

### Phase 4: Merge & Risk Register

Merge sub-agent output. Dedupe via `.container-ignore`. Assign `CT-001…` IDs in severity-then-category order.

### Phase 5: Remediation Drafting

For every CRITICAL/HIGH/MEDIUM finding, append a commented `RUN`/`USER`/`HEALTHCHECK` block to `dockerfile-suggested.patch` with the target file:line, evidence, and suggested fix.

### Phase 6: Apply Mode (opt-in)

When `--apply`, iterate findings interactively with `[a]pply / [s]kip / [A]ll / [q]uit`. Edit Dockerfiles via `Edit`. Destructive changes (removing a `FROM`, `ENTRYPOINT`) need `DESTROY` confirmation.

### Phase 7: Reporting

Write `container-audit.md` + `container-audit.json` + `dockerfile-suggested.patch` (and `image-scan.json` in `--live` mode with Trivy output).

---

## Scoring

Category weights: A=15, B=20, C=20, D=10, E=5, F=10, G=10, H=10 (sum 100). See `reference.md` §3.

| Total | Verdict |
|---|---|
| 90–100 | PASS |
| 70–89 | PASS WITH WARNINGS |
| 50–69 | CONDITIONAL |
| <50 | FAIL |

---

## Important Principles

- **Secrets at build time use BuildKit, not ARG.** `ARG TOKEN=` is baked into the image history.
- **`USER` must be set before the final CMD.** Root at runtime is the default — flag every Dockerfile that doesn't explicitly switch.
- **Multi-stage is the norm.** Any Dockerfile that doesn't use multi-stage and ships a build toolchain is MEDIUM or HIGH depending on image size.
- **Tag pins move.** `FROM node:20-alpine` will drift. `FROM node:20.11.1-alpine3.19@sha256:<digest>` is pinned.
- **`latest` in production is a finding.** Always CRITICAL for production-tagged images.
- **docker-compose `privileged: true` is always CRITICAL** unless a suppression explains why (e.g., a CI runner).
- **Australian English. DD/MM/YYYY. Markdown-first.**

---

## Edge Cases

1. **No Dockerfile present.** Report "no containers found" and exit cleanly.
2. **Dockerfile is generated by a framework (`next/standalone`, `nixpacks`).** Flag as "generated; framework-managed"; skip apply suggestions but audit the final output.
3. **Multi-arch builds (buildx).** Audit each stage independently; flag if arch-specific base images differ in patch level.
4. **Windows-based images.** Base-image checks differ — skip alpine/distroless suggestions, check `servercore` vs `nanoserver`.
5. **`distroless` images without a shell.** Healthcheck must use the image's exec format, not `CMD-SHELL`.
6. **docker-compose with override files.** Parse base + all overrides; findings target the file where the issue originates.
7. **Compose uses `secrets:` top-level.** Good — don't flag. Flag when secrets are inlined in env instead.
