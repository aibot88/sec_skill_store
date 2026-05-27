# security.skill.md
## Software Supply Chain & Security Standards

---

## 1. Core Principle

Security is not a scan step—it is a property of the system.

Every artifact we produce must be:

- **Traceable** → tied to source, commit, and pipeline
- **Verifiable** → cryptographically signed
- **Inspectable** → includes SBOM + scan results
- **Reproducible** → built deterministically in CI
- **Minimal** → ships only what runs — no source, no dev deps, no scripts

If we cannot prove where it came from, how it was built, and what it contains, we do not ship it.

---

## 2. SLSA Level 3 Target (Operationalized)

### 2.1 Build Environment

- All builds occur in CI only (Azure Pipelines / GitHub Actions)
- No local builds for release artifacts
- Ephemeral runners only — no persistent build agents
- Build steps defined entirely in code (YAML) — no manual portal config
- Build environment must be isolated — no network access during compilation

### 2.2 Source Integrity

- All code must originate from version control (Git)
- Protected branches (`main`, `release/*`)
- PR review required — no direct commits to production branches
- Signed commits preferred (`git config commit.gpgsign true`)
- Branch protection: require status checks, dismiss stale approvals

### 2.3 Dependency Integrity

- Lockfiles required (`package-lock.json`) — committed to repo
- No floating versions (`^`, `~`) in production dependencies
- `npm ci` only in CI — never `npm install`
- Run `npm audit --audit-level=high` as a build gate
- Pin base Docker images by digest, not tag:
  ```dockerfile
  # WRONG
  FROM node:20-alpine
  # RIGHT
  FROM node:20-alpine@sha256:<digest>
  ```

---

## 3. Container Hardening

### 3.1 Multi-Stage Build (Mandatory)

```dockerfile
# Stage 1: Build
FROM node:20-alpine@sha256:<digest> AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY tsconfig.json ./
COPY src/ ./src/
RUN npx tsc

# Stage 2: Runtime (minimal)
FROM node:20-alpine@sha256:<digest> AS runtime
WORKDIR /app
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -s /bin/sh -D appuser
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER appuser
EXPOSE 3000
CMD ["node", "dist/jobs/server.js"]
```

**What does NOT ship in the container:**
- `src/` (TypeScript source)
- `scripts/` (one-off migration tools)
- `context/` (analysis docs, exports, handoffs)
- `directives/` (Cartographer directives)
- `standing-orders/`
- `skills/`
- `tsconfig.json`
- `.env` (injected at runtime)
- `devDependencies`

### 3.2 .dockerignore (Mandatory)

```
.git
.env
node_modules
src/
scripts/
context/
directives/
standing-orders/
skills/
*.md
*.log
```

### 3.3 Runtime Security

- Non-root user (see Dockerfile above)
- Read-only filesystem where possible (`readOnlyRootFilesystem: true`)
- No shell in final image if feasible (`FROM distroless`)
- Drop all capabilities: `--cap-drop=ALL`
- No `privileged` mode — ever

---

## 4. Required Security Artifacts (Per Build)

### 4.1 SBOM (Software Bill of Materials)

- Format: CycloneDX JSON
- Tooling: `syft`
- Generate from the **final container image**, not source:

```bash
syft <image>:<tag> -o cyclonedx-json > sbom.cdx.json
```

- Also generate from source for license analysis:

```bash
syft . -o cyclonedx-json > sbom-source.cdx.json
```

### 4.2 Vulnerability Scans

**Container image scan (Trivy):**
```bash
trivy image --format sarif --output trivy-image.sarif <image>:<tag>
trivy image --severity CRITICAL,HIGH --exit-code 1 <image>:<tag>
```

**Filesystem / dependency scan (Snyk):**
```bash
snyk test --sarif-file-output=snyk.sarif
snyk container test <image>:<tag> --sarif-file-output=snyk-container.sarif
```

**Both must pass.** Trivy catches OS-level CVEs. Snyk catches npm dependency
vulnerabilities and has better reachability analysis.

**Build gate:** Fail the pipeline on any CRITICAL severity finding.
HIGH severity findings must be triaged within 7 days.

### 4.3 License Compliance

```bash
syft . -o cyclonedx-json | grype --only-fixed
```

Flag any dependency with:
- GPL-3.0 (copyleft risk in proprietary deployment)
- AGPL (network copyleft)
- No license declared

DoD environments may require explicit license review. Generate a license
report and include it alongside the SBOM.

### 4.4 Build Provenance

Must include:
- Git commit SHA
- Branch name
- Pipeline run ID
- Build timestamp (UTC)
- All dependency input hashes (from lockfile)
- Builder identity (CI service principal)

For GitHub Actions, use the SLSA provenance generator:
```yaml
- uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v2.0.0
```

### 4.5 Artifact Signing

Keyless signing via Sigstore (preferred for CI):
```bash
cosign sign --yes <image>@<digest>
```

Or with a managed key:
```bash
cosign sign --key cosign.key <image>@<digest>
```

**Sign the digest, not the tag.** Tags are mutable. Digests are not.

### 4.6 Attestation

Attach SBOM and provenance as in-toto attestations:
```bash
cosign attest --predicate sbom.cdx.json --type cyclonedx <image>@<digest>
cosign attest --predicate provenance.json --type slsaprovenance <image>@<digest>
```

---

## 5. Secrets Management

- No secrets in source code — ever
- No secrets in Docker images — ever
- No `.env` files committed — `.env.example` with placeholder values only
- Runtime secrets injected via:
  - Azure Container Apps: environment variables or managed identity
  - Local dev: `.env` file (gitignored)
- MSAL auth tokens: use managed identity in production, client credentials locally
- Rotate secrets on a defined schedule

---

## 6. CI Pipeline Requirements

```yaml
steps:
  - checkout
  - npm ci
  - npm run lint
  - npm run type-check        # tsc --noEmit
  - npm run test
  - npm run build              # tsc → dist/
  - docker build
  - trivy image scan           # SARIF output, fail on CRITICAL
  - snyk test                  # SARIF output, fail on CRITICAL
  - syft sbom generation       # CycloneDX JSON
  - license check              # flag copyleft
  - cosign sign                # sign image by digest
  - cosign attest              # attach SBOM + provenance
  - deploy (if all gates pass)
```

**Every step must pass. No skipping. No `continue-on-error: true` for
security steps.**

---

## 7. Azure Container Apps Deployment Gates

Only deploy if ALL of the following are true:
- SBOM exists and is attached to the image
- Trivy scan completed with zero CRITICAL findings
- Snyk scan completed with zero CRITICAL findings
- Build provenance generated and attached
- Image signed with cosign
- All attestations verifiable

Store SBOM, SARIF, and provenance:
- Attached to the container image (via cosign attest)
- Archived in the CI pipeline artifacts
- Optionally pushed to a dedicated security SharePoint library for audit

---

## 8. Dependency Update Policy

- Run `npm audit` weekly (automated via Dependabot or Snyk monitor)
- CRITICAL: patch within 24 hours
- HIGH: patch within 7 days
- MEDIUM: patch within 30 days
- LOW: patch at next release cycle
- Review Dependabot PRs weekly — do not let them accumulate

---

## 9. Anti-Patterns (Strictly Avoid)

- Local builds for release artifacts
- Unsigned images pushed to any registry
- Missing or stale SBOM
- Ignored CRITICAL vulnerabilities
- `npm install` in CI (use `npm ci`)
- Floating dependency versions in production
- Secrets in Dockerfiles, source, or CI logs
- Running containers as root
- Unpinned base images (`FROM node:latest`)
- `continue-on-error` on security scan steps
- Shipping source code, dev dependencies, or scripts in the container

---

## 10. Incident Response

If a CVE is discovered in a deployed image:
1. Assess: is it reachable in our code path?
2. If reachable + CRITICAL: hotfix within 24 hours
3. Rebuild image with patched dependency
4. Re-scan, re-sign, re-attest
5. Redeploy
6. Document in incident log with CVE ID, affected image digest, and resolution

---

## 11. Definition of Done (Security)

A release is only shippable when:

- [ ] Built in CI (not locally)
- [ ] SBOM generated (CycloneDX)
- [ ] Trivy scan passed (zero CRITICAL)
- [ ] Snyk scan passed (zero CRITICAL)
- [ ] License review passed (no copyleft violations)
- [ ] Build provenance generated
- [ ] Image signed (cosign)
- [ ] Attestations attached (SBOM + provenance)
- [ ] No secrets in image
- [ ] Running as non-root user
- [ ] Base image pinned by digest

---

## 12. Guiding Principle

> We ship verifiable artifacts. If we can't prove it's clean, it doesn't deploy.
