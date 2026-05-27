---
name: sbom-generate
description: 'Generate CycloneDX 1.7 and/or SPDX 2.3 SBOMs for the repo, optionally cosign-signed, optionally cross-validated against syft output. Use when producing an SBOM for compliance, attaching to a release artefact, integrating with an SBOM registry, or satisfying a customer attestation request.'
argument-hint: "[--format cyclonedx|spdx|both] [--sign] [--output PATH]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "sbom"
  - "cyclonedx"
  - "spdx"
  - "generate sbom"
chain:
  - compliance-report
  - vex-publish
outputBudget: short
cooldown: per-session
---

# Vulnetix SBOM Generate Skill

## Use when

- Producing an SBOM for SOC 2 / supply-chain compliance.
- Attaching an SBOM to a release artefact (GitHub release, container registry).
- Submitting to an SBOM registry (e.g. NTIA, in-house).
- Cosign signing for keyless OIDC supply-chain attestation.
- Cross-validating Vulnetix output against syft for component-count drift.

## Don't use for

- Just the license list — use `/vulnetix:license-check`.
- Full compliance bundle (SBOM + VEX + SARIF) — use `/vulnetix:compliance-report`.
- Container-image SBOM — use `/vulnetix:container-scan` with syft composition.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Use `binaries.cosign` to gate signing. If user asks for `--sign` without cosign, surface install hint and skip signing.

## Step 2: Generate

```bash
OUT="${OUTPUT_DIR:-.vulnetix/sboms/$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "$OUT"

if [[ "$FORMAT" == "cyclonedx" ]] || [[ "$FORMAT" == "both" ]]; then
    vulnetix scan -o json-cyclonedx > "$OUT/sbom.cdx.json"
fi

if [[ "$FORMAT" == "spdx" ]] || [[ "$FORMAT" == "both" ]]; then
    vulnetix license -o json-spdx > "$OUT/sbom.spdx.json"
fi
```

## Step 3: Optional sign

```bash
[[ "$SIGN" == "true" ]] && cosign sign-blob --yes "$OUT/sbom.cdx.json" --bundle "$OUT/sbom.cdx.json.sig.bundle"
```

## Step 4: Compose with detected SBOM tools (conditional)

If `binaries.syft: true`, also produce a syft SBOM for cross-validation:

```bash
syft "$(pwd)" -o cyclonedx-json > "$OUT/sbom.syft.cdx.json"
```

Surface the diff (component count delta) so the user can spot gaps.

## Step 5: Render

```
SBOM(s) generated:
- CycloneDX: <path>  (<N components>, <M deps>)
- SPDX: <path>
- Signature: <path|none>
- Cross-validated with: syft (delta: +3 components)
```

Suggest `/vulnetix:compliance-report` for a full compliance bundle, or `/vulnetix:vex-publish` to attach VEX.

## Edge cases & gotchas

- `vulnetix scan -o json-cyclonedx` produces CycloneDX 1.7; `vulnetix license -o json-spdx` produces SPDX 2.3. The flags are not interchangeable.
- Cosign signing requires keyless OIDC identity (Fulcio) or `--key file:cosign.key`. CI runners typically have OIDC; dev laptops may not.
- Cross-validation with syft requires `binaries.syft: true`. The delta = Vulnetix components - syft components; non-zero delta usually means private packages.
- CycloneDX 1.7 supports VEX-in-SBOM; pass `--include-vex` to embed the VEX block (otherwise it is a separate file).
- Output directory `.vulnetix/sboms/<ISO8601>/` is created on every invocation; never overwrites.
- For repos with no manifest files, the SBOM contains only the application metadata (no components). Check `components.length` before publishing.
