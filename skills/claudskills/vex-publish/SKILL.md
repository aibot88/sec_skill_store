---
name: vex-publish
description: 'Generate OpenVEX / CycloneDX VEX attestations from `.vulnetix/memory.yaml` triage decisions, optionally sign with cosign, optionally upload to Vulnetix and post to a GitHub PR. Use when documenting triage decisions for supply-chain consumers, attaching VEX to a CycloneDX SBOM, or satisfying customer attestation requests.'
argument-hint: "[--format openvex|cyclonedx] [--upload]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "vex"
  - "publish vex"
  - "openvex"
  - "attestation"
chain:
  - compliance-report
outputBudget: short
cooldown: per-session
---

# Vulnetix VEX Publication Skill

## Use when

- Triage cycle is complete and you need to publish VEX statements for supply-chain consumers.
- A customer requested OpenVEX attestations for a specific delivery.
- Attaching VEX to a CycloneDX SBOM in a compliance bundle.
- Posting VEX status as a PR comment so reviewers see the security disposition.
- Auditing the decision history — VEX is the durable record of what was decided when.

## Don't use for

- Making the triage decisions — use `/vulnetix:vuln`, `/vulnetix:exploits`, `/vulnetix:fix` first; this skill publishes existing decisions.
- Generating the SBOM itself — use `/vulnetix:sbom-generate`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Turns the decisions captured in `.vulnetix/memory.yaml` into a signed/uploadable VEX document.

## Step 1: Load memory

Read `.vulnetix/memory.yaml`. Collect every entry with a non-default `decision.choice` (i.e. anything that isn't `investigating`).

## Step 2: Map decisions → VEX status

Mapping (Vulnetix CLI uses the same):
- `not-affected` / `risk-avoided` → `not_affected`
- `fix-applied` → `fixed`
- `risk-accepted` / `deferred` / `mitigated` → `affected` (with mitigations)
- `investigating` → `under_investigation`

## Step 3: Generate VEX

```bash
vulnetix triage --provider vulnetix --vex-format ${FORMAT:-openvex} -o json > .vulnetix/vex/${TIMESTAMP}.vex.json
```

Default format `openvex`. If user passes `--format cyclonedx`, the CLI emits CycloneDX VEX.

## Step 4: Upload (conditional)

If user passed `--upload`:

```bash
vulnetix upload --file .vulnetix/vex/${TIMESTAMP}.vex.json
```

Otherwise, skip and report the local file path.

## Step 5: GitHub PR comment (conditional)

If `binaries.gh: true` and we're inside a PR (env `GITHUB_REF` or `gh pr view --json number`):

```bash
gh pr comment "$PR_NUMBER" --body-file .vulnetix/vex/${TIMESTAMP}.vex.summary.md
```

Where the summary file is a short Markdown rendering of the VEX (auto-generated from the JSON).

## Step 6: Render report

```
VEX statements: N
- not_affected: N
- fixed: N
- affected (with mitigations): N
- under_investigation: N
File: .vulnetix/vex/<timestamp>.vex.json
Uploaded: <yes|no>
PR comment: <yes|no>
```

## Edge cases & gotchas

- VEX status maps from `decision.choice` via a closed dict — `not-affected/risk-avoided` → `not_affected`, `fix-applied` → `fixed`, `risk-accepted/deferred/mitigated` → `affected (with mitigation)`, `investigating` → `under_investigation`. Custom decision strings break the mapping.
- `--format openvex` (default) and `--format cyclonedx` produce different schemas; consumers downstream typically prefer one or the other.
- `--upload` sends to the Vulnetix triage endpoint — requires authenticated CLI; community-tier may rate-limit.
- PR comment posting needs `binaries.gh: true` AND the current directory inside a PR-context git repo (CI envs typically have GITHUB_REF set).
- Signing with cosign uses keyless OIDC by default; the user must have a valid OIDC identity (CI runners typically do, dev laptops may not).
- Memory schema requires `decision.choice` populated for every entry to be published — entries with `status: under_investigation` are filtered out unless `--include-investigating` is passed.
