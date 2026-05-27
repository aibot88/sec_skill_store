---
name: iac-scan
description: 'Terraform / OpenTofu / Nix / k8s manifest misconfiguration detection — open security groups, missing encryption, public S3/GCS, IAM wildcards, plaintext secrets, missing tags. Use when reviewing an IaC PR, gating `terraform apply` / `tofu apply`, auditing existing state for drift, or building a compliance report for cloud configuration.'
argument-hint: "[--paths file1 file2]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "iac scan"
  - "terraform scan"
  - "tofu scan"
  - "kubernetes manifest"
chain:
  - verify-fix
outputBudget: short
cooldown: per-session
---

# Vulnetix IaC Scan Skill

## Use when

- Pre-apply: scan `*.tf` / `*.tofu` for misconfigurations.
- PR review: catch open security groups, plaintext secrets, IAM wildcards.
- Audit existing infra against compliance baselines (CIS, NIST).
- Detect drift between repo IaC and deployed state.
- Pre-merge: gate on critical findings (e.g. publicly-readable S3).

## Don't use for

- Source-code SAST — use `/vulnetix:sast-scan`.
- Dockerfile / container analysis — use `/vulnetix:container-scan`.
- Cloud runtime monitoring — Pix is static-only; use a CSPM for runtime.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Confirm `derived.has_iac: true` or `--paths` provided. Otherwise abort.

## Step 2: Run scan

```bash
vulnetix iac --paths "$PATHS" -o json > .vulnetix/iac.${TIMESTAMP}.json
```

Captures: open security groups, missing encryption, public S3/GCS, IAM wildcards, unpinned providers, secrets in plaintext, missing tags, unencrypted state backends.

## Step 3: Render

| Severity | File:Line | Resource | Issue | Recommendation |

Group by file. For each high-severity issue, include a 2-3 line code example of the fix.

## Step 4: Risk overlay

If `binaries.terraform: true` (or `tofu`), suggest:

```bash
terraform plan -no-color | head -200    # for context on what would change
```

Don't run `terraform apply` from the skill.

## Memory update

`.vulnetix/iac/<timestamp>.summary.yaml` with finding counts.

## Edge cases & gotchas

- Requires `derived.has_iac: true` OR explicit `--paths`. CWD without `*.tf` files = empty result.
- Detection is static — it cannot evaluate runtime variable interpolation. `var.environment == "prod"` conditional logic is reported as both branches.
- `terraform plan` integration is suggestive only — the skill does NOT run `terraform plan` automatically (state access concerns).
- Provider-specific rules (AWS / GCP / Azure) are detected via resource type prefixes; modules wrapping resources may obscure the type.
- Pre-existing infra not present in IaC (`terraform import` candidates) is not detected.
- k8s manifest support is limited to top-level YAML in `*.yaml` files with kind: matching common workload types.
