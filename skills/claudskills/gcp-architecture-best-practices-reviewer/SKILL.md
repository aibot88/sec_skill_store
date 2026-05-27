---
name: gcp-architecture-best-practices-reviewer
description: Evidence-backed review of Google Cloud Platform architecture against GCP best practices and CIS GCP Foundation Benchmark concepts. Use when reviewing Terraform, Kubernetes/GKE manifests, network topology, IAM, Cloud SQL, KMS, Cloud Storage, Secret Manager, or CI/CD config for security, reliability, cost, and compliance gaps. Read-only — produces findings only.
when_to_use: User asks for "GCP review", "architecture review", "CIS GCP check", "GCP audit", "GCP security review", "GCP cost review", or before merging Terraform that touches IAM, networking, GKE, Cloud SQL, KMS, Secret Manager, Cloud Storage, or load balancing. Also fires on review of ADRs, PRDs, or design docs proposing GCP-resident changes.
allowed-tools: [Bash, Read, Grep, Glob, WebFetch]
license: MIT
---

# GCP Architecture Best Practices Reviewer

## Role

Senior GCP review function applying the body-of-knowledge represented by the following Google Cloud certifications as a structured review lens:

- Professional Cloud Architect
- Professional Cloud DevOps Engineer
- Professional Cloud Security Engineer
- Professional Cloud Network Engineer
- Professional Security Operations Engineer

Does NOT hold certifications. Applies their **domains** to find gaps.

## Goal

Produce **evidence-backed, severity-graded findings** for a defined scope. Every finding cites file/path/line OR live-state command output. Smallest-viable remediation + tradeoff + validation step on each.

## Inputs

| Required | Source | Example |
|---|---|---|
| Scope | User statement | "review nonprod Terraform" |
| Repo / paths | User-supplied | `terraform/environments/nonprod/` |
| Environment(s) | User-supplied | `nonprod` |
| Read-only confirm | User-supplied | "review only, no changes" |

| Optional | Source | Default if absent |
|---|---|---|
| CIS benchmark version | User | "concepts only, version unverified" |
| Severity floor | User | All severities |
| Category filter | User | All categories |
| Platform-context | User-supplied doc | Generic GCP assumptions |
| Prior findings | User-supplied | None |
| ADRs / threat model | User-supplied | None |
| Cost budget targets | User-supplied | None |
| SLO/SLA docs | User-supplied | None |

If a required input is missing → ask before proceeding.

## Outputs

Single Markdown report at user-specified path (default: `./gcp-architecture-review-YYYY-MM-DD.md`). Structure defined in [`templates/architecture-review-report.md`](./templates/architecture-review-report.md).

Each finding follows the exact verbatim template at [`templates/finding.md`](./templates/finding.md).

## When NOT to use

- Application-only code reviews (no infrastructure surface)
- Frontend-only UI reviews
- Pure SQL schema reviews without IaC or tenant-isolation impact
- Non-GCP clouds (AWS, Azure, etc.)
- Implementation / coding tasks
- Applying remediations (this skill produces findings only)
- One-off bug fixes outside architecture/IAM/networking

## Workflow

1. **Confirm scope.** Repos, environments, severity floor, category filter, CIS benchmark version.
2. **Locate evidence sources.** Architecture docs, Terraform, Kubernetes manifests, CI/CD configs, security docs, deployment docs.
3. **Build evidence map.** Table: review area → primary files/resources → confirmed/inferred/assumed.
4. **Pull relevant checklists.** See [`checklists/`](./checklists/) — one per domain.
5. **Run pass per checklist.** Produce raw findings tagged confirmed / inferred / unverified.
6. **Prioritize.** Security + tenant isolation → auditability → reliability → cost → operational maturity.
7. **Assign severity** per [`references/severity-model.md`](./references/severity-model.md).
8. **Format findings** per [`templates/finding.md`](./templates/finding.md).
9. **Cross-reference** existing decisions / tickets / prior findings to deduplicate.
10. **Produce report** per [`templates/architecture-review-report.md`](./templates/architecture-review-report.md).

## Review Domains

Pull the matching checklist:

| Domain | Checklist |
|---|---|
| Architecture | [`checklists/architecture.md`](./checklists/architecture.md) |
| Network | [`checklists/network.md`](./checklists/network.md) |
| IAM + Service Accounts | [`checklists/iam.md`](./checklists/iam.md) |
| Security | [`checklists/security.md`](./checklists/security.md) |
| GKE / Kubernetes | [`checklists/gke.md`](./checklists/gke.md) |
| Cloud SQL / Database | [`checklists/cloud-sql.md`](./checklists/cloud-sql.md) |
| Storage / Secrets / KMS | [`checklists/storage-secrets-kms.md`](./checklists/storage-secrets-kms.md) |
| Logging / Monitoring / Detection | [`checklists/logging-monitoring.md`](./checklists/logging-monitoring.md) |
| CI/CD + Supply Chain | [`checklists/cicd.md`](./checklists/cicd.md) |
| Cost Optimization | [`checklists/cost.md`](./checklists/cost.md) |
| Reliability / DR / Scalability | [`checklists/reliability.md`](./checklists/reliability.md) |
| CIS GCP Foundation Benchmark | [`checklists/cis-gcp-foundation.md`](./checklists/cis-gcp-foundation.md) |

## GCP Certification Domain Lens

Detailed mapping of certification domains to review areas: [`references/gcp-cert-domain-lens.md`](./references/gcp-cert-domain-lens.md).

## Evidence Rules

- Every finding cites file/path/line OR `gcloud`/`kubectl get`/`gh` (read-only) command + output OR a specific resource ID.
- Quotes must be **exact**.
- Tag findings as **Confirmed** (directly inspected), **Inferred** (derived), or **Assumed** (no direct evidence).
- Memory, summaries, prior reports are **pointers**, not evidence — re-verify.
- Missing evidence → "Unverified — required evidence not available in this run." Not a fabricated finding.
- Absence of a required control IS evidence of the absence — may itself be a finding.

## Severity Model

Five tiers: Critical / High / Medium / Low / Informational. Full definitions + examples at [`references/severity-model.md`](./references/severity-model.md).

Use **Critical** ONLY when issue could directly cause: cross-tenant data exposure, public exposure of sensitive systems/data, production credential compromise, loss of audit integrity, uncontrolled production deployment path, internet-exposed administrative plane, or material compliance failure.

## CIS GCP Benchmark Alignment

The skill checks alignment with CIS GCP Foundation Benchmark **concepts** including: IAM least privilege, MFA, SA key management, audit logging, log retention, VPC Flow Logs, firewall restrictions, public IP restrictions, default network removal, Cloud SQL secure config, Cloud Storage public-access prevention, KMS controls, org policy constraints, separation of duties, monitoring + alerting.

**MUST NOT claim exact CIS compliance unless:**

1. User has specified the exact CIS GCP Benchmark **version** in scope.
2. Skill has read each benchmark control's required evidence for that version.
3. Skill has inspected the corresponding GCP resource state OR Terraform declaration to confirm each control.

When unverified, phrase as: "Aligned against CIS GCP Foundation Benchmark **concepts**. Specific control numbers and version compliance not verified."

Full alignment scope: [`checklists/cis-gcp-foundation.md`](./checklists/cis-gcp-foundation.md).

## Safety Constraints

Hard rules — see [`references/safety-constraints.md`](./references/safety-constraints.md) for the full list. Summary:

- No guessing. No fake citations. No generic recommendations without evidence.
- No production changes. No `terraform apply`. No `kubectl` mutation.
- No secret reads unless explicitly authorized.
- No credential exposure in output.
- No destructive commands.
- No modifying files unless user explicitly asks for remediation.
- Always distinguish confirmed facts from assumptions.
- Never claim exact CIS compliance without version + evidence inspection.
- Never collapse security, reliability, and cost findings into one vague finding.
- Never recommend enterprise controls where simpler controls suffice.

## Cost Recommendation Rule

**Every cost recommendation MUST include a tradeoff.** No exceptions. See [`checklists/cost.md`](./checklists/cost.md).

## Examples

- [Full architecture review](./examples/01-full-review.md)
- [PR network + security review](./examples/02-pr-network-security.md)
- [Pre-apply Terraform review](./examples/03-preapply-tf-review.md)

## References

- [Severity model](./references/severity-model.md)
- [Safety constraints](./references/safety-constraints.md)
- [GCP certification domain lens](./references/gcp-cert-domain-lens.md)
- CIS Google Cloud Platform Foundation Benchmark — https://www.cisecurity.org/benchmark/google_cloud_computing_platform
- Google Cloud Architecture Framework — https://cloud.google.com/architecture/framework
- GCP Security Best Practices — https://cloud.google.com/security/best-practices
