---
name: compliance-report
description: 'Build a compliance bundle — CycloneDX SBOM, SPDX license report, SARIF findings, OpenVEX/CycloneDX VEX, optional cosign signatures, manifest.json with SHA-256 sums, Markdown index. Use when assembling an audit bundle, SOC 2 attestation, supply-chain compliance package, or evidence for a customer security questionnaire.'
argument-hint: "[--sign] [--output-dir .vulnetix/compliance/]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "compliance"
  - "audit report"
  - "attestation"
  - "sbom bundle"
chain:
  - sbom-generate
  - vex-publish
outputBudget: medium
cooldown: per-session
---

# Vulnetix Compliance Report Skill

## Use when

- Assembling an audit bundle for SOC 2, ISO 27001, or FedRAMP.
- Supply-chain compliance: producing CycloneDX SBOM + VEX + SARIF in one delivery.
- Evidence for a customer security questionnaire that asks for SBOM + signed attestations.
- Pre-release: assembling the security artefacts that ship alongside the release.
- Quarterly compliance review: regenerating the full bundle for archive.

## Don't use for

- Just generating an SBOM — use `/vulnetix:sbom-generate`.
- Per-CVE VEX statements — use `/vulnetix:vex-publish` (this skill composes it).
- Single-scanner output — use the individual `/vulnetix:sast-scan`, `/vulnetix:secret-scan`, etc.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Produces a bundle suitable for audit / attestation submission.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Use `binaries.cosign` to gate the `--sign` step.

## Step 2: Generate artifacts in parallel

```bash
OUT="${OUTPUT_DIR:-.vulnetix/compliance/$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "$OUT"

vulnetix scan -o json-cyclonedx > "$OUT/sbom.cdx.json" &
vulnetix license -o json-spdx > "$OUT/licenses.spdx.json" &
vulnetix scan --evaluate-sast -o json-sarif > "$OUT/findings.sarif" &
wait
```

## Step 3: Generate VEX (uses local memory.yaml)

```bash
vulnetix triage --provider vulnetix --vex-format cyclonedx -o json > "$OUT/vex.cdx.json"
```

## Step 4: Sign (conditional)

If `--sign` and `binaries.cosign: true`:

```bash
cosign sign-blob --yes "$OUT/sbom.cdx.json" --bundle "$OUT/sbom.cdx.json.sig.bundle"
cosign sign-blob --yes "$OUT/findings.sarif" --bundle "$OUT/findings.sarif.sig.bundle"
```

If cosign absent and user requested `--sign`, surface install hint and continue without signatures.

## Step 5: Manifest

Write `$OUT/manifest.json` listing all artifacts with sha256 sums. Render Markdown index `$OUT/README.md`.

## Step 6: Render report

```
Compliance bundle: <path>
- SBOM (CycloneDX): <path/size/component count>
- Licenses (SPDX): <path/license count/conflict count>
- Findings (SARIF): <path/critical/high/medium count>
- VEX (CycloneDX): <path/statement count>
- Signed: <yes|no>  (cosign: <available|missing>)
```

Suggest next: `/vulnetix:vex-publish --upload` for VEX submission, or supply the path to your audit pipeline.

## Edge cases & gotchas

- Four parallel CLI calls (`scan -o json-cyclonedx`, `license -o json-spdx`, `scan --evaluate-sast -o json-sarif`, `triage --vex-format cyclonedx`). Stagger if rate-limited.
- Cosign signing requires keyless OIDC identity (Fulcio); local devs without an OIDC identity must use `--key file:cosign.key`.
- Output directory is `.vulnetix/compliance/<ISO8601>/`; multiple invocations create siblings, never overwrite.
- Optional `--upload` sends VEX to Vulnetix; SBOM/SARIF/SPDX stay local unless `--upload-all` is passed.
- Manifest.json SHA-256 sums are computed AFTER signing — re-verify with `sha256sum -c manifest.json` before archive.
- For repos with no manifest files, `scan -o json-cyclonedx` produces a near-empty SBOM. Check `components` count before publishing.
