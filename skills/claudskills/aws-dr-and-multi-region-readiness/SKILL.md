---
name: aws-dr-and-multi-region-readiness
description: Use when designing and rehearsing AWS disaster-recovery and multi-region posture for a workload after the runtime and observability exist and reliability and operations have decided RPO/RTO targets and failover ownership. Produces multi-AZ baseline, tier-driven multi-region topology (active-passive / active-active), cross-region data replication (RDS replicas, S3 CRR, DynamoDB Global Tables), Route 53 health-check failover, AWS Backup posture, and a documented, rehearsed failover drill with measured RPO/RTO. Do not use for org/account topology, network/identity foundation, single-region workload runtime, observability/cost wiring, or Terraform module/state mechanics; use the other aws (or Family H) skills.
---

# AWS DR and Multi-Region Readiness

## When to use

Invoke when designing the disaster-recovery posture for a workload, extending it across regions, or establishing and rehearsing the failover drill with RPO/RTO validation — for a workload that already runs single-region with observability.

Do not use for: AWS Organizations/account topology (use `aws-account-and-organization-topology`); single-region VPC/IAM/KMS foundation (use `aws-network-and-identity-foundation`); single-region compute selection and deployment (use `aws-workload-runtime-and-deployment`); CloudWatch/cost instrumentation (use `aws-observability-and-cost-readiness`); IaC module/state/plan/apply mechanics (the `terraform` Family H skills).

## Inputs

Required:

- A deployed single-region runtime from `aws-workload-runtime-and-deployment` with observability from `aws-observability-and-cost-readiness` (the workload this DR posture protects and the signals failover keys off).
- Approved `architecture/reliability` RPO/RTO targets per workload tier, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/operations` decisions on failover ownership, drill cadence, and the runbook hook.
- The workload tier from `architecture-schema` (drives multi-AZ vs multi-region and active-passive vs active-active).
- Data-store inventory (RDS/Aurora, S3, DynamoDB, EBS) and their consistency requirements.
- Existing backup posture and any compliance-driven retention.
- The single-region network/identity foundation (extended cross-region, not redesigned).

## Operating rules

- Never generate a paper DR plan. A DR posture that has not been rehearsed with a measured RPO/RTO is aspirational, not readiness — this is a locked infrastructure-tier design constraint.
- Consume `architecture/reliability` and `architecture/operations`; do not invent decisions. RPO/RTO targets, failover ownership, and drill cadence are architectural decisions. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Extend the existing foundation and runtime; do not redesign them. The single-region VPC/identity (`aws-network-and-identity-foundation`) and runtime (`aws-workload-runtime-and-deployment`) are extended cross-region. This skill does not re-author the single-region design.
- Multi-AZ is the floor; multi-region is tier-driven. Multi-AZ is the baseline for tier-0/1. Multi-region (active-passive or active-active) is added only where the tier and RPO/RTO demand it — gold-plating a tier-2 workload to active-active is rejected as much as a single-region tier-0.
- Topology follows RPO/RTO, not preference. Backup-restore, pilot-light, warm-standby, or active-active is chosen to *meet the stated RTO/RPO* at acceptable cost. The chosen pattern names the RTO/RPO it satisfies and the cost trade-off.
- Data replication matches the store and the RPO. RDS/Aurora cross-region replicas, S3 Cross-Region Replication, DynamoDB Global Tables, EBS snapshot copy — each with a replication lag budget that satisfies the RPO. A replication path whose lag exceeds the RPO is rejected.
- Failover is health-driven and reversible. Route 53 health-check-based failover (or equivalent) with a defined trigger; the procedure includes fail-back, not just fail-over. A one-way failover with no rehearsed return path is incomplete.
- Backups are immutable, encrypted, and restore-tested. AWS Backup (or equivalent) with tier-driven retention, cross-region/cross-account copy, encryption via the foundation CMK strategy, and a restore that has actually been performed — an untested backup is an assumption.
- The drill is documented and rehearsed with measured numbers. A failover runbook plus an executed drill that records the achieved RPO and RTO against the targets. A gap between achieved and target is reported, not hidden.
- This skill owns DR + multi-region + backup + the rehearsed drill. Org topology, single-region foundation/runtime, observability/cost wiring, and IaC mechanics are named handoffs.
- A DR posture without an executed drill and measured RPO/RTO is not done.

## Output contract

The DR and multi-region posture MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — failover and traffic-shift mechanics reproducible via IaC-ready definitions; fail-back procedure defined.
- [observability-standards](../../../../../standards/observability-standards/README.md) — failover health checks and DR alarms wired (consuming the observability skill's substrate); drill results recorded.
- [security-standards](../../../../../standards/security-standards/README.md) — cross-region replicas and backups encrypted via the foundation CMK strategy; replica/backup access least-privilege.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — region, replica, backup-vault, and failover-record naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives multi-AZ vs multi-region and the active-passive vs active-active decision.

Upstream contract: `architecture/reliability` is the source of truth for RPO/RTO per tier; `architecture/operations` is the source of truth for failover ownership and drill cadence. If a needed decision is missing, pause and raise an ADR candidate. Org topology, single-region foundation/runtime, observability/cost, and IaC mechanics are named handoffs.

## Progressive references

- Read `references/aws-dr-multi-region-playbook.md` when designing any owned area or checking the anti-pattern list.
- Read `references/aws-dr-multi-region-quality-rubric.md` before declaring the DR posture complete.
- Use `assets/aws-dr-multi-region.template.md` as the replication / failover / backup / drill pattern reference.

## Process

1. Gather context: load `architecture/reliability` (RPO/RTO per tier) and `architecture/operations` (failover ownership, drill cadence, runbook hook). Resolve the workload tier from `architecture-schema`. Confirm the single-region runtime and observability exist. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Set the baseline: confirm or specify multi-AZ for tier-0/1 compute and data (extending the runtime, not redesigning it).
3. Decide the multi-region topology from the tier and RPO/RTO: backup-restore / pilot-light / warm-standby / active-active; state which RTO/RPO it satisfies and the cost trade-off.
4. Design data replication per store: RDS/Aurora cross-region replica, S3 CRR, DynamoDB Global Tables, EBS snapshot copy — each with a replication-lag budget that satisfies the RPO.
5. Design failover: Route 53 health-check-based failover with a defined trigger, the standby promotion procedure, and the fail-back path.
6. Design backups: AWS Backup with tier-driven retention, cross-region/cross-account copy, encryption via the foundation CMK strategy, immutability where compliance requires.
7. Wire DR observability: failover health checks and DR alarms via the observability skill's substrate; record where drill metrics are captured.
8. Author and execute the drill: a failover runbook, then a rehearsed drill that records achieved RPO and RTO against the targets; report any gap.
9. Validate: the executed drill meets (or the gap to) the RPO/RTO targets; a restore from backup has actually been performed; the fail-back path has been exercised; document any check that cannot run.
10. Produce `dr-multi-region-readiness.md` (baseline, topology + RTO/RPO rationale, replication budgets, failover + fail-back procedure, backup posture, drill results vs targets) plus the gap list with ADR candidates and the named handoff list. Validate against deployment-, observability-, security-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Multi-AZ baseline confirmation for tier-0/1.
- Multi-region topology with the RTO/RPO it satisfies and the cost trade-off.
- Per-store cross-region replication with a replication-lag budget meeting the RPO.
- Route 53 health-check failover with a defined trigger and a fail-back procedure.
- AWS Backup posture: tier retention, cross-region/cross-account copy, CMK encryption, immutability where required.
- DR observability wiring (failover health checks + DR alarms) via the observability substrate.
- An executed failover drill recording achieved RPO/RTO against targets.
- `dr-multi-region-readiness.md`, the gap list with ADR candidates, and the named handoff list.

Output rules:

- IaC-ready definitions, not prose-only; not the Terraform module/state mechanics.
- No paper plan — the drill is executed and RPO/RTO measured.
- Topology matches the tier and RPO/RTO; over- and under-provisioning are both rejected.
- Org topology, single-region foundation/runtime, observability/cost, and IaC mechanics are named handoffs.

## Quality checks

- [ ] RPO/RTO targets are sourced from `architecture/reliability`; failover ownership and drill cadence from `architecture/operations` (or an ADR candidate is raised).
- [ ] The single-region foundation and runtime are extended, not redesigned.
- [ ] Multi-AZ is confirmed for tier-0/1 compute and data.
- [ ] The multi-region topology matches the tier and names the RTO/RPO it satisfies and the cost trade-off (no gold-plating, no under-provisioning).
- [ ] Each data store has a cross-region replication path with a lag budget that satisfies the RPO.
- [ ] Route 53 health-check failover has a defined trigger and a documented fail-back path.
- [ ] AWS Backup has tier retention, cross-region/cross-account copy, foundation-CMK encryption, and immutability where compliance requires.
- [ ] Failover health checks and DR alarms are wired via the observability skill's substrate.
- [ ] A drill has been executed and the achieved RPO/RTO recorded against targets; a backup restore and the fail-back path were actually exercised, or the gap is documented.
- [ ] Org topology, single-region foundation/runtime, observability/cost, and IaC mechanics are named handoffs.

## References

- Upstream: [`architecture/reliability`](../../../../architecture/reliability/SKILL.md), [`architecture/operations`](../../../../architecture/operations/SKILL.md).
- Builds on: [`aws-workload-runtime-and-deployment`](../aws-workload-runtime-and-deployment/SKILL.md) (single-region runtime extended here), [`aws-network-and-identity-foundation`](../aws-network-and-identity-foundation/SKILL.md) (foundation extended cross-region), [`aws-observability-and-cost-readiness`](../aws-observability-and-cost-readiness/SKILL.md) (substrate for failover health/alarms).
- Related aws archetype skill: [`aws-account-and-organization-topology`](../aws-account-and-organization-topology/SKILL.md).
- IaC mechanics handoff: the `terraform` Family H skills own module/state/plan/apply.
- Standards: [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
