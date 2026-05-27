---
name: iac-terraform-audit
description: Audit Terraform, OpenTofu, Terragrunt, and Pulumi modules for state, provider pinning, security (Checkov/tfsec), module hygiene, environment separation, drift, and cost. One sub-agent per module. Static, live, and apply modes.
argument-hint: [module-path-or-glob]
allowed-tools: Read Grep Glob Write Edit Bash(bash:*) Agent
effort: high
paths: "**/*.tf"
---

# IaC Terraform Audit

ultrathink

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/iac-terraform-audit/`.
> Run `mkdir -p .anthril/audits/iac-terraform-audit` before the first `Write` call.
> Primary artefact: `.anthril/audits/iac-terraform-audit/<artefact>`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## When to use

Run this skill when the user mentions:
- Terraform review, IaC audit, infrastructure security
- Checkov, tfsec, OpenTofu review, Pulumi audit
- Pre-migration infra cleanup
- State file concerns, provider pinning, module design

Covers eight categories: state and backend configuration (remote state, encryption, locking, workspace separation), provider pinning (`required_providers` with version constraints, `required_version`), security (Checkov/tfsec taxonomy — public S3 ACLs, unencrypted RDS, open security groups, wildcard IAM, plaintext secrets in tfvars), module hygiene (variable validation, descriptions, types, outputs, sensitive flag), environment separation, drift risk, cost hotspots, and CI testing coverage.

## Before You Start

1. **Determine operating mode.** `--live` runs `terraform plan` against each module (refresh-only, no apply). `--apply` writes HCL patches. `--runtime` is not applicable (Terraform has no safe runtime test).
2. **Enumerate modules.** Run `scripts/list-modules.sh` — groups `.tf` files by directory.
3. **Sub-agent budget.** One agent per module. Warn above 10.
4. **Load `.iac-ignore`** for suppressions (pattern: `<module_path>:<finding_id>` or `<module_path>:*`).
5. **Live-mode requirements.** `terraform init` must succeed per module — warn the user if state backends require credentials and fall back to static audit for modules that can't initialise.

## User Context

$ARGUMENTS

Module inventory: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/iac-terraform-audit/scripts/list-modules.sh"`

Tools: !`which terraform tofu 2>/dev/null | head -1 || echo "terraform:unavailable"` · !`which checkov tfsec 2>/dev/null | head -1 || echo "checkov:unavailable"`

---

## Audit Phases

### Phase 1: Discovery & Mode Selection

1. Parse module inventory. Identify Terraform / OpenTofu / Terragrunt / Pulumi.
2. Confirm scope; warn if >10 modules.
3. Verify live-mode tools. Fall back per-module if `terraform init` fails.

### Phase 2: Per-Module Snapshot

For each module, parse HCL (via `hcl2json` if available, else structural grep):

- Providers (`required_providers`, version constraints, source)
- Required Terraform version (`required_version`)
- Backend config (type, encryption, locking)
- Resources (by provider+type, name)
- Variables (with type, default, description, sensitive, validation)
- Outputs (with sensitive, description)
- Locals
- Data sources
- Module calls (local / registry / Git, with version)
- Lifecycle blocks

In `--live` mode, additionally run `terraform plan -refresh-only` and capture the summary (additions / changes / destructions predicted).

### Phase 3: Cross-Module Topology

1. Build a module-dependency graph (who calls whom via `module.<name>` blocks, who reads whose state via `terraform_remote_state`).
2. Detect shared backends (multiple modules writing to the same state key — usually a bug).
3. Emit Mermaid graph for the report.

### Phase 4: Parallel Sub-Agent Audit

Spawn one `Agent(subagent_type=Explore)` per module in a single assistant message. Each walks categories A–H in `reference.md` §1:

- **A. State & Backend** — remote backend, encryption at rest, state locking (DynamoDB / GCS / etc.), workspace separation, state file not in git
- **B. Provider pinning** — `required_providers` with `~>` or exact, `required_version` set, source pinned to a hash registry URL
- **C. Security (Checkov/tfsec)** — open SGs, public S3 ACLs, unencrypted RDS, IAM `*`, KMS missing, plaintext secrets, EBS/EFS encryption
- **D. Module hygiene** — variables with `type` and `description`, `validation` blocks for bounded inputs, `sensitive = true` on secrets, outputs documented
- **E. Environment separation** — workspace or directory per env, no cross-env refs, prod state isolated
- **F. Drift risk** — `lifecycle.ignore_changes` abuse (should be targeted), `null_resource` for imperative work, `create_before_destroy` on resources that require it
- **G. Cost hotspots** — oversized default instance types, unbounded autoscaling max, NAT Gateways when cheaper egress suffices, attached-but-unused EIPs
- **H. Testing & CI** — `terraform fmt` / `validate` / `tflint` integration in CI, `terraform-docs` generation, pre-commit hooks

Sub-agents MUST NOT run `terraform apply` / `terraform destroy` / state-mutating commands. Read-only plans only.

### Phase 5: Cross-Module Analysis

- Duplicate resource patterns across modules → module extraction candidates
- Cyclic dependencies via `terraform_remote_state`
- Provider version drift (module A uses AWS ~>5, module B uses ~>4)
- Missing `required_version` consistency

### Phase 6: Merge & Risk Register

Consolidate findings. Dedupe via `.iac-ignore`. Apply severity adjustments:
- Findings on production modules (determined via workspace name or directory convention) keep severity
- Findings on non-prod modules downgrade one tier
- Checkov/tfsec findings (if live tools available) cross-validated with sub-agent output

Assign `IAC-001…` IDs.

### Phase 7: Remediation Drafting

Emit commented HCL blocks to `iac-suggested.tf`. Rules:

- **Every FK-like resource relationship** uses `depends_on = []` explicit when needed
- **Every state change to sensitive resources** is commented with `# MANUAL REVIEW — STATE RISK`
- **Provider pinning suggestions** include both the current pin and the recommended
- **Module extraction suggestions** emit a minimal new module skeleton in a sub-block of the suggestion file

### Phase 8: Apply Mode (opt-in)

When `--apply`, iterate findings with `[a]pply / [s]kip / [A]ll / [q]uit`. Any HCL change that would affect state (adding `lifecycle { prevent_destroy = true }`, changing a backend key) requires `DESTROY` confirmation.

### Phase 9: Reporting

Write `iac-terraform-audit.md` + `iac-terraform-audit.json` + `iac-suggested.tf` (+ `terraform-plan.txt` in live mode).

---

## Scoring

Weights: A=20, B=10, C=30, D=10, E=10, F=10, G=5, H=5 (sum 100). See `reference.md` §3.

| Total | Verdict |
|---|---|
| 90+ | PASS |
| 70–89 | PASS WITH WARNINGS |
| 50–69 | CONDITIONAL |
| <50 | FAIL |

---

## Important Principles

- **State is the crown jewel.** Remote, encrypted, locked, and never in git.
- **`~>` is a minor-version pin.** `~>5.0` allows 5.x; `~>5.0.0` allows 5.0.x. Know which you want.
- **Security findings that are true on paper may be false in context.** A public S3 ACL on a static-site bucket is intentional. Flag but let the user suppress.
- **`lifecycle.ignore_changes = all` is almost always wrong.** Target specific attributes.
- **`null_resource` + `local-exec` is imperative.** Flag every occurrence.
- **Cost findings are suggestions, never failures.** Use INFO severity.
- **Australian English. DD/MM/YYYY. Markdown-first.**

---

## Edge Cases

1. **Terragrunt.** Parse `terragrunt.hcl` blocks (`include`, `dependency`, `generate`). Findings on generated files go to the `terragrunt.hcl` that generated them.
2. **Pulumi.** Parse `index.ts` / `__main__.py`. Map to the same A–H taxonomy.
3. **CDK (TypeScript/Python).** Skip — not in scope. Emit one finding: "CDK module detected; not covered by this skill."
4. **Remote module (`source = "git::..."` or `source = "terraform-aws-modules/..."`).** Audit the caller's reference and the version; do not recurse into the remote.
5. **`terraform init` fails in live mode.** Record as a module-level limitation; continue static audit.
6. **State encrypted with SSE-KMS but key is unmanaged.** Flag MEDIUM — "encrypted but key lifecycle unclear".
7. **Mono-repo with many modules.** Cluster by top-level directory; one sub-agent per cluster if counts are high.
8. **A module has only data sources, no resources.** Audit the providers and backend; skip C/F.
