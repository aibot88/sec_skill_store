---
name: postgres-backup-and-operational-readiness
description: Use when designing, reviewing, or hardening PostgreSQL backup, point-in-time recovery, and day-2 operational readiness against stated RPO/RTO targets. Produces backup strategy (pg_basebackup or pgBackRest with WAL archiving for PITR), rehearsed restore drills with measured RPO/RTO, retention and cost posture, observability for replication lag, storage health, bloat, transaction-ID wraparound, and connection saturation, plus runbook inputs for failover, vacuum-freeze emergencies, and connection exhaustion. Do not use for replication topology design, schema or migration work, query optimization, or access-control hardening; use postgres-replication-and-ha-readiness, postgres-schema-and-migration, postgres-indexing-and-query-optimization, or postgres-security-and-data-access-hardening instead.
---

# Postgres Backup and Operational Readiness

## When to use

Invoke when a PostgreSQL deployment needs a verified backup and recovery posture, when validating restore capability against an RPO/RTO before go-live or a reliability review, when defining day-2 operational observability and runbook inputs, or when remediating a backup, retention, or operational-readiness gap.

Do not use for: replication/HA topology and failover (use `postgres-replication-and-ha-readiness`), schema or migration work (use `postgres-schema-and-migration`), query/index performance (use `postgres-indexing-and-query-optimization`), or role/grant/TLS hardening (use `postgres-security-and-data-access-hardening`).

## Inputs

Required:

- The RPO and RTO targets in scope, sourced from `reliability-architecture.md` where it exists.
- The operational ownership and on-call model, and the alerting/runbook conventions from `operations` (the `operations` architecture artifact or the project's operational standards).
- The deployment substrate: self-managed, managed (RDS/Aurora/Cloud SQL), or Kubernetes operator — this constrains the available backup mechanisms.

Optional:

- Current backup configuration: tooling, schedule, WAL archiving target, last successful restore date.
- Database size, growth rate, write volume (drives WAL volume and backup window).
- Storage substrate and object-store target for backups (S3/GCS/Azure Blob) and its retention/lifecycle policy.
- Current observability stack and existing alerts.
- Compliance/retention obligations (regulatory minimum retention, legal hold).
- Known operational incidents (wraparound scares, connection exhaustion, bloat events).

## Operating rules

- A backup without a rehearsed, timed restore is not a backup. Every backup strategy includes a restore drill that produces a measured RTO and a verified RPO. Unrehearsed backups are reported as a critical gap.
- RPO drives WAL archiving; RTO drives backup type and restore path. Logical dumps (`pg_dump`) are not a PITR strategy — PITR requires a physical base backup plus continuous WAL archiving.
- Prefer `pgBackRest` (or the managed provider's native continuous backup) over hand-rolled `pg_basebackup` + archive scripts for any production system; justify any hand-rolled approach with an ADR.
- Backups are tested for both corruption and recoverability: checksum/verification on the backup, and a periodic full restore-and-validate into an isolated environment.
- Retention is a policy with a cost. State the retention window, the PITR window it enables, the storage cost posture, and the lifecycle/expiry mechanism. Retention shorter than the compliance obligation is a rejected design.
- Backups are encrypted at rest and in transit, and the restore path does not depend on a secret stored only in the system being recovered. Cross-account/cross-region copy posture is stated for disaster scenarios.
- Transaction-ID wraparound and multixact wraparound are existential risks: the design includes wraparound-age monitoring with a threshold well before the freeze emergency, and a documented emergency-vacuum runbook input.
- Connection saturation is an operational failure mode: the design states the connection-limit posture, the pooling layer, the saturation signal, and the runbook input. It does not redesign the pooling layer (that is `data-architecture`/`backend-architecture`); it makes the failure observable and actionable.
- Observability is mandatory and specific: replication lag, WAL archive success/lag, backup success/duration/size, restore-drill recency, storage headroom, bloat, wraparound age, and connection saturation each have a signal, a threshold, and an owner.
- Runbook inputs are produced here, not full runbooks: this skill states the alert-worthy symptom, the first diagnostic, and the safe first action, and hands the operationalized runbook to `operations`.
- If the substrate cannot meet the stated RPO/RTO (e.g., backup window exceeds RTO, WAL archive lag exceeds RPO), pause and raise an ADR candidate against `reliability`/`operations` rather than asserting an unverified target.

## Output contract

The backup and operational-readiness design MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — backup success, WAL archive lag, restore-drill recency, storage health, bloat, wraparound age, and connection saturation are named observable signals with thresholds.
- [security-standards](../../../../../standards/security-standards/README.md) — backups encrypted at rest and in transit; backup credentials and restore keys are not stored solely inside the recoverable system; no secrets in backup scripts.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — backup and restore are automated and repeatable; the restore procedure does not depend on a not-yet-run manual setup step.

Upstream contract: `reliability-architecture.md` is the source of truth for RPO and RTO. The `operations` artifact/standards are the source of truth for alerting conventions, on-call ownership, and runbook format. If RPO/RTO is unstated or unachievable on the substrate, pause and raise an ADR candidate — do not invent or silently weaken the target. Replication topology and failover behavior are inputs from `postgres-replication-and-ha-readiness`, not decisions made here.

## Process

1. Establish targets and substrate. Extract RPO/RTO from `reliability-architecture.md`; extract alerting/on-call/runbook conventions from `operations`. Confirm the substrate (self-managed / managed / operator) and the backup mechanisms it allows. If RPO/RTO is missing, pause and escalate.
2. Inventory current posture: backup tool, schedule, WAL archiving destination and success rate, last verified restore, retention window, encryption, and cross-region copy. Record gaps explicitly.
3. Design the backup strategy: physical base-backup tool (`pgBackRest` default; managed-native; hand-rolled `pg_basebackup` only with ADR), full/differential/incremental cadence, backup window vs write volume, and the object-store target.
4. Design WAL archiving for PITR: archive method (`archive_command`/`archive_library` or tool-managed), archive destination, archive-lag budget derived from RPO, and the recovery target capability (time/LSN/named restore point).
5. Compute and state the delivered RPO and RTO: RPO from WAL archive cadence + archive lag; RTO from base-restore time + WAL replay time at the stated write volume. Compare against target; raise an ADR candidate for any gap.
6. Define the restore drill: scope (full PITR into an isolated environment), frequency, automation, the validation step (data sanity + application smoke), and the measured-RTO capture. A design without a scheduled, automated drill is incomplete.
7. Define retention and cost posture: retention window, the PITR window it enables, lifecycle/expiry mechanism on the object store, compliance-minimum check, and the storage-cost statement.
8. Define backup security: encryption at rest and in transit, key custody (not solely inside the recoverable system), access control on the backup store, and cross-account/cross-region copy for disaster isolation.
9. Define day-2 observability signals with thresholds and owners: backup success/duration/size, WAL archive success/lag, restore-drill recency, replication lag (consumed from the replication skill's contract), storage headroom, table/index bloat, transaction-ID and multixact wraparound age, and connection saturation.
10. Produce runbook inputs (not full runbooks) for the high-severity operational failure modes: primary loss / restore-from-backup, WAL archive failure, backup failure, approaching wraparound (emergency vacuum), severe bloat, storage exhaustion, and connection exhaustion. Each input states the alert symptom, first diagnostic query/command, and the safe first action; hand off to `operations` for operationalization.
11. Produce the readiness assessment: the delivered RPO/RTO vs target with evidence from the drill, the signal/threshold/owner table, the runbook-input set, and an explicit gap list with ADR candidates.
12. Verify. Execute (or require execution of) at least one full restore drill into an isolated environment, capture the measured RTO and verified RPO, and confirm the monitoring signals fire as designed. If a real drill cannot be run in this environment, document the unverified state explicitly as a critical open risk — do not declare readiness on an unrehearsed backup.

## Outputs

Required:

- `backup-operational-readiness.md`: backup strategy, WAL archiving/PITR design, delivered RPO/RTO vs target, retention and cost posture, backup security posture, and the readiness gap list.
- Observability signal table: signal, source, threshold, action, owner — covering backup, WAL archive, restore-drill recency, storage, bloat, wraparound, and connection saturation.
- Restore drill plan: scope, frequency, automation, validation steps, and measured-RTO capture method.
- Runbook inputs for the high-severity failure modes (symptom → first diagnostic → safe first action), formatted for `operations` to operationalize.

Conditional, when applicable:

- ADR candidate(s) where the substrate cannot meet RPO/RTO or where a hand-rolled backup approach is chosen.
- Cross-region/cross-account disaster-copy design.
- Compliance-retention reconciliation note.

Output rules:

- Every backup claim is paired with a rehearsed, timed restore; unrehearsed backups are reported as a critical gap, not a pass.
- The delivered RPO/RTO is stated with evidence and compared to the target.
- Runbook inputs are inputs (symptom/diagnostic/first action), not full operational runbooks.
- Replication/failover topology is consumed, not redesigned; pooling-layer architecture is consumed, not redesigned.

## Quality checks

- [ ] RPO/RTO are sourced from `reliability-architecture.md` (or an ADR candidate is raised for the gap).
- [ ] PITR is backed by a physical base backup plus continuous WAL archiving — `pg_dump` is not presented as PITR.
- [ ] The delivered RPO and RTO are computed, stated, and compared against the target with drill evidence.
- [ ] A scheduled, automated restore drill into an isolated environment is defined, with a measured-RTO capture step.
- [ ] Retention window is stated with the PITR window it enables, the expiry mechanism, and a compliance-minimum check.
- [ ] Backups are encrypted at rest and in transit, and restore does not depend on a secret stored only in the recoverable system.
- [ ] Transaction-ID/multixact wraparound age has a monitoring signal with a threshold ahead of the freeze emergency and a runbook input.
- [ ] Connection saturation has a signal, threshold, and runbook input (without redesigning the pooling layer).
- [ ] Every required observability signal has a threshold, an action, and an owner.
- [ ] Runbook inputs cover restore-from-backup, WAL archive failure, wraparound, bloat, storage exhaustion, and connection exhaustion, each as symptom → diagnostic → safe first action.
- [ ] Replication topology and failover are consumed from `postgres-replication-and-ha-readiness`, not redesigned here.

## References

- Upstream: [`architecture/operations`](../../../../architecture/operations/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Related implementation skills: [`postgres-replication-and-ha-readiness`](../postgres-replication-and-ha-readiness/SKILL.md) (paired availability concern; failover topology is an input here), [`postgres-indexing-and-query-optimization`](../postgres-indexing-and-query-optimization/SKILL.md) (bloat/vacuum overlap), [`postgres-schema-and-migration`](../postgres-schema-and-migration/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`modular-monolith`](../../../../../architecture-patterns/modular-monolith/README.md).
