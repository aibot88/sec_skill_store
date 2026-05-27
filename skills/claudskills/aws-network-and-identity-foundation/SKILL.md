---
name: aws-network-and-identity-foundation
description: Use when designing, reviewing, or hardening the in-account AWS network and identity foundation after account topology exists and security and infrastructure-platform have decided trust zones and the identity model. Produces VPC topology (per-env, per-tier, multi-AZ subnets), inter-account connectivity (Transit Gateway / peering / PrivateLink), IAM Identity Center federation, IAM role-assumption patterns and permission boundaries, KMS CMK strategy, Secrets Manager with rotation, and Route 53 zone strategy. Do not use for org/account/SCP topology, workload compute selection, observability/cost wiring, or DR/multi-region; use the other aws archetype skills. Emits IaC-ready definitions, not Terraform module/state mechanics.
---

# AWS Network and Identity Foundation

## When to use

Invoke when standing up the in-account network and identity layer for an environment, restructuring VPC/connectivity, or auditing/hardening IAM, KMS, and secret handling before workloads land in the account.

Do not use for: AWS Organizations/OU/SCP topology (use `aws-account-and-organization-topology`); workload compute primitives, load balancing, autoscaling (use `aws-workload-runtime-and-deployment`); CloudWatch/cost instrumentation (use `aws-observability-and-cost-readiness`); multi-region/DR (use `aws-dr-and-multi-region-readiness`); IaC module/state/plan/apply mechanics (the `terraform` Family H skills own those — this skill emits IaC-ready definitions, not the modules).

## Inputs

Required:

- An account/OU layout from `aws-account-and-organization-topology` (the accounts this network and identity foundation is built inside).
- Approved `architecture/security` decisions on trust zones, the IAM/identity model, and encryption posture, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `infrastructure-platform.md` Network & Trust-Boundary and Identity & Access sections.
- The workload tier from `architecture-schema` (drives subnet isolation, CMK granularity, rotation cadence).
- The external IdP for IAM Identity Center federation (Okta / Entra ID / Google).
- Inter-account/inter-VPC connectivity needs (which accounts/services must reach which).
- CIDR plan or IPAM constraints; on-prem connectivity (DX / VPN) requirements.

## Operating rules

- Never generate tutorial-grade network/identity. Assume a multi-account org where the default is no connectivity and every grant and route is justified.
- Consume `architecture/security` and `infrastructure-platform.md`; do not invent decisions. Trust zones, the identity model, encryption posture, and connectivity intent are architectural decisions. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Stay in-account; the org/account boundary is upstream. This skill builds inside the accounts `aws-account-and-organization-topology` created; it does not create accounts, OUs, or SCPs. Name that boundary.
- The VPC is segmented by tier and never flat. Per-env VPCs with public / private-app / private-data subnet tiers across at least the multi-AZ count the reliability tier requires. A single flat subnet or a public data tier is rejected.
- Connectivity is explicit and least-route. Inter-account/inter-VPC reachability uses Transit Gateway or peering with scoped route tables; service-to-service uses PrivateLink where it avoids opening the network. No blanket VPC peering "to keep it simple".
- Human access is federated and short-lived. IAM Identity Center federated to the IdP with permission sets; no IAM users for humans, no long-lived access keys. Workload-to-AWS uses IAM roles (instance/IRSA/task roles), not embedded credentials.
- Every role is least-privilege under a permission boundary. Roles are scoped to the operational need; a permission boundary caps the maximum even if a policy is over-broad. Wildcard `Action`/`Resource` is an ADR-justified exception.
- Encryption is customer-managed where the posture requires it. KMS CMKs (per-env, and per-tenant where the tenancy model requires) with key policies scoped to the using roles; default AWS-managed keys only where `architecture/security` allows. Encryption in transit and at rest is the default, not opt-in.
- Secrets live in Secrets Manager with rotation. No secrets in env vars baked into launch templates/task defs, SSM plaintext, or AMIs. Rotation is configured at the cadence the security posture defines; the secret-consumption path is least-privilege.
- DNS is a designed zone strategy. Route 53 private hosted zones per env, split-horizon where required, delegation aligned to the account/env boundary — not ad-hoc records.
- This skill owns in-account network + identity + encryption + DNS foundation. Org topology, workload runtime, observability/cost, DR, and IaC mechanics are named handoffs, not implemented here.
- A foundation whose connectivity and least-privilege have not been validated (reachability matrix, IAM access-analyzer / policy review) is not done.

## Output contract

The network and identity foundation MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — least-privilege IAM under permission boundaries, no IAM users/long-lived keys for humans or workloads, customer-managed encryption where required, private connectivity over public exposure, secrets in Secrets Manager with rotation.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — the foundation is reproducible via IaC-ready definitions; no click-ops-only network or identity.
- [observability-standards](../../../../../standards/observability-standards/README.md) — VPC Flow Logs and CloudTrail data-event seam present (full observability/cost wiring deferred to `aws-observability-and-cost-readiness`).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — VPC, subnet, role, CMK alias, and hosted-zone naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives subnet isolation, CMK granularity, and rotation cadence.

Upstream contract: `architecture/security` is the source of truth for trust zones, the IAM model, and encryption posture; `infrastructure-platform.md` is the source of truth for network shape and connectivity intent. If a needed decision is missing, pause and raise an ADR candidate. Org topology, workload runtime, observability/cost, DR, and IaC mechanics are named handoffs.

## Progressive references

- Read `references/aws-network-identity-playbook.md` when designing any owned area or checking the anti-pattern list.
- Read `references/aws-network-identity-quality-rubric.md` before declaring the foundation complete.
- Use `assets/aws-network-identity.template.md` as the VPC / IAM / KMS / Secrets / Route 53 pattern reference.

## Process

1. Gather context: load `architecture/security` (trust zones, IAM model, encryption posture) and `infrastructure-platform.md` (network shape, connectivity intent). Resolve the workload tier from `architecture-schema`. Confirm the account/OU layout from `aws-account-and-organization-topology`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Design VPC topology: per-env VPCs, public / private-app / private-data subnet tiers across the reliability-required AZ count, CIDR/IPAM plan, NAT and egress posture, no public data tier.
3. Design inter-account/inter-VPC connectivity: Transit Gateway or peering with scoped route tables; PrivateLink for service-to-service where it avoids broad network opening; on-prem DX/VPN if required.
4. Configure human identity: IAM Identity Center federated to the IdP, permission sets per role mapped to the account/OU layout; no IAM users for humans.
5. Design workload identity: IAM roles (instance / IRSA / task) with least-privilege policies, each under a permission boundary; no embedded credentials.
6. Design the KMS CMK strategy: per-env (and per-tenant where required) CMKs, key policies scoped to using roles, in-transit and at-rest encryption defaults.
7. Configure Secrets Manager: secret hierarchy, rotation at the security-defined cadence, least-privilege consumption path; reject any plaintext-secret pattern.
8. Design the Route 53 zone strategy: private hosted zones per env, split-horizon where required, delegation aligned to the account/env boundary.
9. Validate: produce a reachability matrix (who can reach whom) and confirm it matches the trust zones; run an IAM policy/access review (Access Analyzer or equivalent) confirming no unintended access or excess privilege; document any check that cannot run.
10. Produce `network-identity-foundation.md` (VPC/subnet plan, connectivity matrix, IAM role/permission-boundary map, CMK strategy, secret/rotation policy, DNS strategy) plus the gap list with ADR candidates and the named handoff list. Validate against security-, deployment-, observability-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- VPC/subnet topology (per-env, tiered, multi-AZ) with CIDR/IPAM and egress posture.
- Inter-account/inter-VPC connectivity design (TGW/peering/PrivateLink) with scoped routes.
- IAM Identity Center federation + permission sets (no IAM users for humans).
- Workload IAM roles with least-privilege policies under permission boundaries.
- KMS CMK strategy with scoped key policies and encryption defaults.
- Secrets Manager hierarchy with rotation and least-privilege consumption.
- Route 53 zone strategy.
- `network-identity-foundation.md`, the gap list with ADR candidates, and the named handoff list.

Output rules:

- IaC-ready definitions/policy, not prose-only; not the Terraform module/state mechanics.
- No flat/public-data VPC; no IAM users or long-lived keys; no plaintext secrets.
- Every role is bounded and least-privilege; wildcards are ADR-justified exceptions.
- Org topology, workload runtime, observability/cost, DR, and IaC mechanics are named handoffs.

## Quality checks

- [ ] Trust zones, IAM model, and encryption posture are sourced from `architecture/security`; network shape from `infrastructure-platform.md` (or an ADR candidate is raised).
- [ ] The foundation is built inside the existing account/OU layout; no org/account/SCP design is done here.
- [ ] VPCs are per-env and tiered (public / private-app / private-data) across the reliability-required AZ count; no flat or public-data subnet.
- [ ] Inter-account/inter-VPC connectivity is explicit with scoped route tables; PrivateLink used where it avoids broad network opening; no blanket peering.
- [ ] Human access is IAM Identity Center federated with permission sets; no IAM users for humans, no long-lived keys.
- [ ] Workload identity uses IAM roles under permission boundaries; least-privilege; wildcards are ADR-justified.
- [ ] KMS CMKs are per-env (per-tenant where required) with key policies scoped to using roles; encryption in transit and at rest is default.
- [ ] Secrets are in Secrets Manager with rotation at the security-defined cadence; no plaintext-secret patterns.
- [ ] Route 53 is a designed zone strategy aligned to the account/env boundary.
- [ ] A reachability matrix matches the trust zones and an IAM access review shows no excess privilege, or the gap is documented.
- [ ] Org topology, workload runtime, observability/cost, DR, and IaC mechanics are named handoffs, not designed here.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md).
- Builds on: [`aws-account-and-organization-topology`](../aws-account-and-organization-topology/SKILL.md) (the accounts/OUs this foundation is built inside).
- Related aws archetype skills (downstream): [`aws-workload-runtime-and-deployment`](../aws-workload-runtime-and-deployment/SKILL.md), [`aws-observability-and-cost-readiness`](../aws-observability-and-cost-readiness/SKILL.md), [`aws-dr-and-multi-region-readiness`](../aws-dr-and-multi-region-readiness/SKILL.md).
- IaC mechanics handoff: the `terraform` Family H skills own module/state/plan/apply for these definitions.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
