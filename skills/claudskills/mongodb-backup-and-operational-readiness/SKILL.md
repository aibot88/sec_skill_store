---
name: mongodb-backup-and-operational-readiness
description: Use when designing or hardening MongoDB backup, point-in-time recovery, and operational readiness after the replica topology exists and reliability and operations have set RPO/RTO and runbook expectations. Produces a backup strategy (mongodump / filesystem snapshot / Cloud Manager / Atlas continuous), oplog-based PITR, a documented and rehearsed restore drill with measured RPO/RTO, oplog-window and replication-lag observability, and runbook inputs for primary loss, oplog rollover, and chunk-balancer issues. Do not use for document modeling, query tuning, replica topology, security/auth, backup-artifact encryption key model, or storage provisioning; use the other Family B archetype skills.
---

# MongoDB Backup and Operational Readiness

## When to use

Invoke when establishing a MongoDB backup strategy, adding point-in-time recovery, validating that a restore actually meets RPO/RTO, wiring oplog-window observability, or producing operational runbook inputs for a production deployment.

Do not use for: document modeling or migrations (use `mongodb-data-model-and-migration`); query/index tuning (use `mongodb-indexing-and-query-optimization`); replica-set topology and failover behavior (use `mongodb-replication-and-ha-readiness`); auth/RBAC/TLS/CSFLE and the backup-artifact encryption key model (use `mongodb-security-and-data-access-hardening`); storage/volume/bucket provisioning (infrastructure layer — this skill designs the backup procedure, not the storage substrate).

## Inputs

Required:

- An existing replica-set topology from `mongodb-replication-and-ha-readiness` (snapshot consistency, the source member for backups, and the oplog window all depend on it).
- Approved `architecture/reliability` RPO/RTO per data tier, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/operations` decisions on backup ownership, drill cadence, and the runbook hook.
- The workload tier from `architecture-schema` (drives backup frequency, retention, PITR requirement).
- Deployment model: self-hosted, Cloud Manager/Ops Manager, or Atlas (drives the backup mechanism).
- Data volume, change rate, and the maintenance/backup window.
- Compliance-driven retention or legal-hold requirements.

## Operating rules

- Backup and restore are paired — a backup with no rehearsed restore is not done. This is a locked data-tier constraint. The deliverable is a *restore that has been performed*, not a backup job that succeeds.
- Consume `architecture/reliability` and `architecture/operations`; do not invent decisions. RPO/RTO, backup ownership, and drill cadence are upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Build on the topology; do not redesign it. The replica set, the backup-source member, and the oplog window are `mongodb-replication-and-ha-readiness`'s ownership. This skill consumes them; a topology change the backup needs is a finding handed back, not made here.
- The backup mechanism matches the deployment and the RPO. `mongodump` for small datasets and logical portability; filesystem/volume snapshot for large datasets and fast restore; Cloud Manager/Ops Manager or Atlas continuous backup where the platform provides it. A mechanism whose achievable RPO exceeds the target is rejected.
- A consistent backup respects the replica set. Snapshots are taken from a consistent point (a hidden/secondary member, or a journaled snapshot), never a naive copy of a live primary's files. State how consistency is guaranteed.
- PITR requires an oplog chain that covers the recovery window. Oplog-based PITR is only real if the oplog/backup oplog slice spans from the base backup to the target time. State the maximum recoverable point and the gap, if any, to the RPO.
- RPO and RTO are measured in a drill, not asserted. Execute a restore: measure the actual data-loss window (RPO) and time-to-restore (RTO) against the targets. A gap is reported with an ADR candidate, never hidden.
- Restore drills are scheduled, not one-off. The drill cadence from `architecture/operations` is encoded; a restore proven once and never again decays into an assumption.
- Backups are encrypted and access-controlled — the key/access model is named to security. This skill requires encrypted, least-privilege-access backup artifacts and names the key and access model to `mongodb-security-and-data-access-hardening`; an unencrypted backup of production data is rejected.
- Observability covers the things that silently break recovery. Oplog window, replication lag, backup job success/failure, last-successful-backup age, and (sharded) balancer state are exposed signals with thresholds.
- Runbook inputs are concrete. For primary loss, oplog rollover, and chunk-balancer issues: the signal that fires, the confirming command, the first recovery step, and the escalation — structured for the operations runbook, not prose.
- This skill owns backup + PITR + restore drill + operational readiness. Modeling, query tuning, topology, security key model, and storage provisioning are named handoffs.
- A backup posture without an executed restore drill and measured RPO/RTO is not done.

## Output contract

The backup and operational-readiness design MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — oplog window, replication lag, backup success/age, and balancer-state signals exposed with thresholds.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — backup and restore procedures are reproducible from configuration, not click-ops.
- [security-standards](../../../../../standards/security-standards/README.md) — backups encrypted and access-controlled; no PII/secret leakage in backup tooling logs; the key/access model is named to `mongodb-security-and-data-access-hardening`.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives backup frequency, retention, and the PITR requirement.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — backup-set, snapshot, and vault naming.

Upstream contract: `architecture/reliability` is the source of truth for RPO/RTO; `architecture/operations` is the source of truth for backup ownership and drill cadence. The replica topology and oplog window belong to `mongodb-replication-and-ha-readiness`. If a needed decision is missing, pause and raise an ADR candidate.

## Progressive references

- Read `references/mongodb-backup-playbook.md` when designing any owned area or checking the anti-pattern list.
- Read `references/mongodb-backup-quality-rubric.md` before declaring the backup posture complete.
- Use `assets/mongodb-backup.template.md` as the backup/PITR/restore-drill/runbook pattern reference.

## Process

1. Gather context: load `architecture/reliability` (RPO/RTO) and `architecture/operations` (backup ownership, drill cadence, runbook hook). Pull the replica topology, backup-source member, and oplog window from `mongodb-replication-and-ha-readiness`. Resolve the tier from `architecture-schema`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Select the backup mechanism from the deployment model and the RPO: `mongodump`, filesystem/volume snapshot, Cloud Manager/Ops Manager, or Atlas continuous; justify against achievable RPO and restore speed.
3. Define consistency: which member backups are taken from and how a consistent point is guaranteed (secondary/hidden member, journaled snapshot); never a naive live-primary file copy.
4. Design PITR: the base backup + oplog slice chain covering the recovery window; state the maximum recoverable point and any gap to the RPO.
5. Set frequency and retention from the tier: full/incremental cadence, retention period, legal-hold/compliance handling.
6. Encrypt and access-control the artifacts: require encryption at rest and least-privilege access; name the key and access model to `mongodb-security-and-data-access-hardening`.
7. Wire observability: oplog window, replication lag, backup job success/failure, last-successful-backup age, and (sharded) balancer state, each with a threshold and an alert destination.
8. Author runbook inputs: primary loss, oplog rollover, chunk-balancer issues — signal → confirming command → first recovery step → escalation.
9. Execute the restore drill: restore to a target time, measure actual RPO (data-loss window) and RTO (time-to-restore) against targets, exercise PITR to a chosen point; record results and any gap. Encode the recurring drill cadence.
10. Produce `backup-operational-readiness.md` (mechanism + rationale, consistency method, PITR chain and max recoverable point, frequency/retention, observability thresholds, runbook inputs, drill results vs RPO/RTO) plus the named handoff list. Validate against observability-, deployment-, security-standards, architecture-schema, and naming-conventions. Revise until all pass or the gap is documented.

## Outputs

Required:

- Backup mechanism selection with rationale against the RPO and restore speed.
- Consistency method (backup-source member + consistent-point guarantee).
- PITR design: base + oplog chain, maximum recoverable point, gap-to-RPO if any.
- Frequency and retention per tier, with compliance/legal-hold handling.
- Encryption + least-privilege access requirement (key/access model named to security).
- Observability signals with thresholds (oplog window, lag, backup age, balancer state).
- Concrete runbook inputs for primary loss, oplog rollover, chunk-balancer issues.
- An executed restore drill recording measured RPO/RTO vs targets, plus the recurring drill cadence.
- `backup-operational-readiness.md` and the named handoff list.

Output rules:

- Reproducible backup/restore procedures — not click-ops, not prose-only.
- No backup posture without an executed, measured restore; no unencrypted production backup.
- The replica topology is consumed, not redesigned; storage provisioning and the encryption key model are named handoffs.

## Quality checks

- [ ] RPO/RTO are sourced from `architecture/reliability`; backup ownership and drill cadence from `architecture/operations` (or an ADR candidate is raised).
- [ ] The replica topology, backup-source member, and oplog window are consumed from `mongodb-replication-and-ha-readiness` — not redesigned here.
- [ ] The backup mechanism matches the deployment model and its achievable RPO is within target.
- [ ] Backup consistency is guaranteed (secondary/hidden member or journaled snapshot); no naive live-primary file copy.
- [ ] PITR has an oplog chain covering the recovery window; the maximum recoverable point and any RPO gap are stated.
- [ ] Frequency and retention match the tier; compliance/legal-hold handling is defined.
- [ ] Backups are encrypted and access-controlled; the key/access model is named to `mongodb-security-and-data-access-hardening`.
- [ ] Oplog window, replication lag, backup success/age, and balancer-state signals are exposed with thresholds.
- [ ] Concrete runbook inputs exist for primary loss, oplog rollover, and chunk-balancer issues.
- [ ] A restore drill was executed with measured RPO/RTO vs targets; PITR to a chosen point was exercised; the recurring drill cadence is encoded — or the gap is documented.

## References

- Upstream: [`architecture/operations`](../../../../architecture/operations/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Builds on: [`mongodb-replication-and-ha-readiness`](../mongodb-replication-and-ha-readiness/SKILL.md) (topology, backup-source member, oplog window).
- Related Family B archetype skills: `mongodb-data-model-and-migration`, `mongodb-indexing-and-query-optimization`, `mongodb-security-and-data-access-hardening` (backup-artifact encryption key/access model).
- Storage provisioning is the infrastructure layer's ownership.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
