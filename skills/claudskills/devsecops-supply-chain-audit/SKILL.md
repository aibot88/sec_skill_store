---
name: devsecops-supply-chain-audit
description: Audit software supply chain across every ecosystem (npm, pip, Go, Ruby, Cargo, Maven, Docker, Terraform) — pinning, vulnerabilities, secrets, SBOM, signing, branch protection, CODEOWNERS. One sub-agent per ecosystem. Three modes.
argument-hint: [repo-path]
allowed-tools: Read Grep Glob Write Edit Bash(bash:*) Agent
effort: high
---

# DevSecOps Supply Chain Audit

ultrathink

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/devsecops-supply-chain-audit/`.
> Run `mkdir -p .anthril/audits/devsecops-supply-chain-audit` before the first `Write` call.
> Primary artefact: `.anthril/audits/devsecops-supply-chain-audit/<artefact>`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## When to use

Run this skill when the user mentions:
- Supply-chain audit, DevSecOps
- SLSA, SBOM, Dependabot, Renovate
- Dependency security, secrets scanning, SCA
- Branch protection review

Detects every ecosystem in the repo (npm, pnpm, yarn, pip, Poetry, Go modules, Cargo, Bundler, Maven, Gradle, Composer, Docker images, Terraform providers) and spawns one sub-agent per ecosystem. Covers dependency pinning (lockfile committed, exact-vs-range, integrity hashes), vulnerability surface (`npm audit`, `pip-audit`, `govulncheck`, `bundler-audit`, `trivy`, `grype`), secret scanning (gitleaks-style patterns against HEAD and history), SBOM generation (Syft, CycloneDX), provenance and signing (SLSA level, cosign, sigstore, `npm --provenance`), branch protection, CODEOWNERS coverage, and Dependabot/Renovate configuration.

## Before You Start

1. **Determine operating mode.** `--live` runs vulnerability scanners available on the system (`npm audit`, `pip-audit`, `govulncheck`, `bundler-audit`, `trivy`). `--apply` can open PRs pinning dependencies, adding `dependabot.yml`, or hardening branch protection via `gh api`.
2. **Detect ecosystems.** Run `scripts/detect-ecosystems.sh`. One sub-agent per ecosystem detected.
3. **Load `.secops-ignore`** for suppression (e.g., accepting a vulnerability in a dev dependency).
4. **Sub-agent budget.** One agent per ecosystem. 2–6 sub-agents typical.

## User Context

$ARGUMENTS

Ecosystems detected: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/devsecops-supply-chain-audit/scripts/detect-ecosystems.sh"`

Live scanners: !`which npm pip-audit govulncheck trivy 2>/dev/null | head -4 || echo "none available"`

---

## Audit Phases

### Phase 1: Discovery & Mode Selection

1. Parse ecosystem output. Set up one sub-agent per ecosystem.
2. Check for repo-wide signals (Dependabot config, CODEOWNERS, branch-protection docs, signing config).
3. Confirm mode with user.

### Phase 2: Repo-wide Signal Snapshot

Collect:

- `.github/dependabot.yml` presence and ecosystem coverage
- `renovate.json` / `.renovaterc` presence
- `.github/CODEOWNERS` presence and coverage
- Branch protection (via `gh api repos/:owner/:repo/branches/main/protection` in live mode)
- Commit signing (`git log --show-signature -1` in live mode)
- SLSA level clues (`--provenance` in publish workflows, signed releases, reproducible builds)
- `SECURITY.md` presence
- `.gitleaks.toml` / secret scan config

### Phase 3: Parallel Sub-Agent Audit (one per ecosystem)

Spawn sub-agents simultaneously. Each receives:
- Ecosystem identifier (npm / pip / go / ruby / cargo / maven / docker / terraform)
- Pre-detected manifest files and lockfiles
- The audit taxonomy and severity rubric from `reference.md`
- The operating mode
- Scanner output from live mode (if available)

Each sub-agent walks categories A–H:

- **A. Dependency pinning** — lockfile present and committed? exact vs range? integrity hashes where supported (npm `integrity`, pip `hash`, cargo `checksum`, go `go.sum`)
- **B. Vulnerability surface** — count CRITICAL/HIGH/MEDIUM/LOW from scanner. Known-actively-exploited CVEs called out.
- **C. Secret patterns** — gitleaks/trufflehog-style patterns (AWS keys, private key headers, high-entropy strings) across tracked files. Live mode extends to `git log -p` (history).
- **D. SBOM & provenance** — SBOM generation configured? SLSA level (L0–L4)? `npm publish --provenance` for npm packages?
- **E. Image signing** — cosign config? sigstore? `cosign verify` works live?
- **F. Branch protection (repo-wide)** — required reviews, required status checks, signed commits, linear history, restrict deletions
- **G. CODEOWNERS** — covers sensitive paths (`.github/`, `infra/`, `auth/`, `payments/`)
- **H. Automation** — Dependabot / Renovate grouping sensible, security-only fast-lane for critical vulns

### Phase 4: Merge & SLSA Self-Assessment

1. Merge sub-agent findings. Apply `.secops-ignore`.
2. Compute SLSA level per `reference.md` §3:
   - L0: no provenance
   - L1: provenance generated
   - L2: hosted build with authenticated publish
   - L3: hardened, tamper-evident build service
   - L4: two-party review + reproducible builds
3. Assign `SEC-001…` IDs.

### Phase 5: Remediation Drafting

Per finding, emit actionable remediation:
- Dependency pinning fixes → commented diff for `package.json` / `requirements.txt` / `go.mod`
- Vulnerability surface → `npm audit fix` / `pip install -U` commands (but commented — user runs)
- Secret leaks (current files) → listed with `file:line` and a rotation instruction
- Secret leaks (history) → `git filter-repo` command block (requires explicit user action)
- Branch protection gaps → `gh api` PATCH commands (commented)

Output files: `devsecops-supply-chain-audit.md`, `devsecops-supply-chain-audit.json`, `slsa-self-assessment.md`, and `sbom.json` if generated in live mode.

### Phase 6: Apply Mode (opt-in)

Interactive. Per finding:
- **Safe**: lockfile regeneration, `.github/dependabot.yml` creation, `SECURITY.md` stub, CODEOWNERS addition.
- **Require confirmation**: branch-protection API calls, opening PRs.
- **Never auto-applied**: history rewrites (`git filter-repo`), secret rotation, publishing changes.

### Phase 7: Reporting

Render report from `templates/output-template.md`.

---

## Scoring

Weights: A=15, B=25, C=20, D=10, E=5, F=15, G=5, H=5 (sum 100). See `reference.md` §4.

| Total | Verdict |
|---|---|
| 90+ | PASS |
| 70–89 | PASS WITH WARNINGS |
| 50–69 | CONDITIONAL |
| <50 | FAIL |

---

## Important Principles

- **Known-exploited CVEs are always CRITICAL.** Check against CISA's Known Exploited Vulnerabilities (KEV) catalogue.
- **A leaked secret in the current HEAD is CRITICAL even if the secret was later "removed".** It's in history. Surface + rotate.
- **SLSA L1 is achievable in a weekend.** SLSA L3 requires infrastructure. Set expectations.
- **Dependabot on its own isn't enough.** Many teams enable it and ignore the PRs. Flag if the last 10 Dependabot PRs are unmerged.
- **Dev dependencies matter.** A compromised dev-dep can exfiltrate secrets during `npm install`.
- **Signed commits are a weak signal alone** — combine with branch-protection-required and required-reviews.
- **Australian English. DD/MM/YYYY. Markdown-first.**

---

## Edge Cases

1. **Monorepo.** Sub-agents may need to walk multiple package.jsons / requirements.txts inside one ecosystem. Aggregate findings per ecosystem.
2. **Private registry.** If lockfile references a private registry, live-mode scanners may fail with auth errors — record as limitation and continue static.
3. **Archived repo.** Downgrade findings by one tier; note archival state.
4. **First-party code vulnerabilities.** Out of scope — refer to `software-development` plugin.
5. **Secrets found in history but rotated.** Document but do not suppress — history rewrite is still recommended.
6. **No lockfile (pure `package.json`).** CRITICAL for JS/TS, HIGH for Python (requirements.txt without `==`).
7. **Go modules with `replace` directives pointing at forks.** Audit the fork's provenance.
