---
name: aws-account-and-organization-topology
description: Use when designing, reviewing, or hardening the AWS Organizations and account topology for a system after infrastructure-platform and security have decided the org structure and environment ladder. Produces the AWS Organizations OU structure, landing-zone approach (Control Tower or custom), Service Control Policy guardrails, environment-isolated account layout, central billing and cost-allocation tagging, and baseline AWS Config/audit posture. Do not use for in-account VPC/IAM/KMS design, workload compute selection, observability wiring, or DR topology; use the other aws archetype skills (network-and-identity-foundation, workload-runtime-and-deployment, observability-and-cost-readiness, dr-and-multi-region-readiness) instead.
---

# AWS Account and Organization Topology

## When to use

Invoke when establishing a new AWS Organization, restructuring accounts/OUs, adding an environment to the account ladder, or auditing org-level guardrails before workloads land.

Do not use for: in-account network/identity foundation — VPC, IAM roles, KMS, Secrets Manager (use `aws-network-and-identity-foundation`), workload compute primitives (use `aws-workload-runtime-and-deployment`), observability/cost instrumentation (use `aws-observability-and-cost-readiness`), or DR/multi-region (use `aws-dr-and-multi-region-readiness`).

## Inputs

Required:

- Approved `infrastructure-platform.md` declaring the org topology intent and the environment ladder (which environments exist and how they isolate).
- Approved `architecture/security` decisions on the guardrail posture: required encryption, allowed regions, root-usage policy, and audit/logging centralization.

Optional:

- Existing AWS Organization state (accounts, OUs, SCPs, Control Tower status).
- Compliance regime (e.g. PCI/HIPAA/FedRAMP) driving isolation and audit requirements.
- Tenancy model (single-tenant vs multi-tenant) affecting account-per-tenant decisions.
- Cost-allocation and chargeback requirements.
- IaC tooling preference for org management (consumed by `terraform` skills, not implemented here).

## Operating rules

- Consume the topology; do not invent it. The OU structure intent, environment ladder, and isolation requirements come from `infrastructure-platform.md`; the guardrail posture comes from `architecture/security`. If either is silent on a needed decision (e.g. account-per-environment vs shared, allowed regions), pause and raise an ADR candidate.
- Accounts are the strongest AWS isolation and blast-radius boundary. Environment isolation (prod vs non-prod) is account-level, not tag-level or VPC-level. A shared prod/non-prod account is rejected absent an ADR.
- Mandatory foundational accounts: a management (org root, no workloads), a log-archive (immutable central logging), and an audit/security account. Workload accounts never hold org-management privileges.
- Prefer a landing zone (Control Tower or a documented custom equivalent) over hand-built org plumbing; justify a custom landing zone with an ADR if Control Tower is rejected.
- SCPs are guardrails, not IAM. They express organization-wide denies (deny disallowed regions, deny root actions, deny disabling CloudTrail/Config/GuardDuty, require encryption) and never substitute for in-account least-privilege (that is `aws-network-and-identity-foundation`).
- Guardrails are default-deny at the edges that matter: every SCP names the threat or policy it enforces from `architecture/security`. No guardrail without a mapped rationale; no required control left unguarded.
- Central, tamper-resistant audit is non-negotiable: org-wide CloudTrail to the log-archive account, AWS Config baseline rules, and GuardDuty enabled org-wide, with the log-archive account access-restricted.
- Cost allocation is structural: a mandatory tagging policy (`Environment`, `Workload`, `CostCenter`, `Owner`) enforced via tag policies, consolidated billing, and per-OU/account cost visibility. Tagging discipline defined here; spend monitoring/anomaly detection is `aws-observability-and-cost-readiness`.
- Stay at the org/account boundary. VPCs, IAM roles, KMS keys, and workloads are explicitly downstream — name the handoff, do not design them here.
- This skill emits IaC-ready definitions and policy documents; it does not own the IaC module mechanics or state (that is the `terraform` Family H skills).

## Output contract

The org and account topology MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — centralized immutable audit logging, encryption-required guardrails, no org-management privilege in workload accounts, restricted log-archive access.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — environment isolation is account-level and reproducible via IaC; no click-ops-only org structure.
- [observability-standards](../../../../../standards/observability-standards/README.md) — org-wide CloudTrail/Config/GuardDuty enabled and routed to the log-archive account.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — account, OU, and tag-key naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — workload tier classification drives account isolation strictness and guardrail severity.

Upstream contract: `infrastructure-platform.md` is the source of truth for the OU structure and environment ladder; `architecture/security` is the source of truth for guardrail posture, allowed regions, and audit centralization. If a needed decision is unstated, pause and raise an ADR candidate. VPC/IAM/KMS/Secrets and all workload concerns are downstream handoffs, not designed here.

## Process

1. Load `infrastructure-platform.md` (org intent, environment ladder, isolation requirements) and `architecture/security` (guardrail posture, allowed regions, audit centralization, compliance regime). If a required decision is missing, pause and raise an ADR candidate.
2. Inventory current state (if any): existing accounts, OUs, SCPs, Control Tower status, CloudTrail/Config/GuardDuty coverage, and tagging. Record every gap against a security/platform requirement.
3. Design the OU structure: foundational OUs (Security, Infrastructure/Shared, Workloads) and workload OUs aligned to the environment ladder and tier classification. Place the mandatory management, log-archive, and audit accounts.
4. Choose the landing-zone approach: AWS Control Tower (default) or a documented custom landing zone (with an ADR justifying the rejection of Control Tower). State the enrollment/account-vending mechanism.
5. Define the account layout: account-per-environment (and per-tenant where the tenancy model requires), naming, ownership, and the rule that workload accounts hold no org-management privilege.
6. Design SCP guardrails: per guardrail, the deny/condition and the `architecture/security` rationale it enforces — deny disallowed regions, deny root usage, deny disabling CloudTrail/Config/GuardDuty, require encryption (e.g. S3/EBS), restrict leaving the org. Map each SCP to OU scope.
7. Design centralized audit: org-wide CloudTrail to the log-archive account (immutable, MFA-delete/Object-Lock as applicable), AWS Config baseline conformance pack, GuardDuty org-wide, and access restriction on the log-archive account.
8. Define the tagging and cost-allocation policy: mandatory tag keys (`Environment`, `Workload`, `CostCenter`, `Owner`), AWS tag policies enforcing them, consolidated billing, and cost-allocation activation. Note the handoff of spend monitoring to `aws-observability-and-cost-readiness`.
9. Produce the topology assessment: OU/account diagram or narrative, the SCP guardrail → rationale matrix, the audit posture, the tagging policy, and an explicit gap list with ADR candidates for any unstated/unmet requirement.
10. State downstream handoffs explicitly: VPC/identity foundation → `aws-network-and-identity-foundation`; workload runtime → `aws-workload-runtime-and-deployment`; spend/observability → `aws-observability-and-cost-readiness`; DR → `aws-dr-and-multi-region-readiness`; IaC module/state mechanics → the `terraform` Family H skills.
11. Validate against [security-standards](../../../../../standards/security-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [naming-conventions](../../../../../standards/naming-conventions/README.md), and [architecture-schema](../../../../../standards/architecture-schema/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- `account-organization-topology.md`: OU structure, account layout (incl. mandatory management/log-archive/audit accounts), landing-zone approach, and the environment-ladder mapping.
- SCP guardrail set with, per policy, its scope and the `architecture/security` rationale it enforces.
- Centralized audit design: org CloudTrail, Config baseline, GuardDuty, log-archive access restriction.
- Tagging and cost-allocation policy (mandatory keys + tag-policy enforcement + consolidated billing).
- Gap list with ADR candidates and the explicit downstream-handoff list.

Output rules:

- IaC-ready definitions/policy documents, not prose-only; not the IaC module/state mechanics (that is `terraform`).
- Environment isolation is account-level; no tag-only "isolation".
- Every SCP maps to a named security/platform rationale; unmapped guardrails are removed, unguarded required controls are reported as gaps.
- No VPC/IAM/KMS/workload design; those are named handoffs.

## Quality checks

- [ ] OU structure and environment ladder are sourced from `infrastructure-platform.md`; guardrail posture from `architecture/security` (or an ADR candidate is raised).
- [ ] Mandatory management, log-archive, and audit accounts exist; workload accounts hold no org-management privilege.
- [ ] Environment isolation (prod vs non-prod) is account-level, not tag- or VPC-level.
- [ ] A landing-zone approach is chosen; a custom landing zone (if used) has an ADR justifying rejection of Control Tower.
- [ ] Every SCP names the `architecture/security` rationale it enforces and its OU scope.
- [ ] Org-wide CloudTrail routes to an access-restricted, immutable log-archive account; Config baseline and GuardDuty are org-wide.
- [ ] A mandatory tagging policy (`Environment`, `Workload`, `CostCenter`, `Owner`) is enforced via tag policies with consolidated billing.
- [ ] Tier classification (architecture-schema) is reflected in account isolation strictness and guardrail severity.
- [ ] Downstream handoffs (network/identity, workload runtime, observability/cost, DR, IaC mechanics) are named, not designed here.
- [ ] Outputs are IaC-ready definitions/policies, not prose-only.

## References

- Upstream: [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Related aws archetype skills (downstream): [`aws-network-and-identity-foundation`](../aws-network-and-identity-foundation/SKILL.md), [`aws-workload-runtime-and-deployment`](../aws-workload-runtime-and-deployment/SKILL.md), [`aws-observability-and-cost-readiness`](../aws-observability-and-cost-readiness/SKILL.md), [`aws-dr-and-multi-region-readiness`](../aws-dr-and-multi-region-readiness/SKILL.md).
- IaC mechanics handoff: the `terraform` Family H skills own module/state/plan/apply for these definitions.
- Compatible patterns: [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md) (account-per-tenant decisions), [`microservices`](../../../../../architecture-patterns/microservices/README.md).
