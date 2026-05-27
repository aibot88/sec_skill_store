---
name: postgres-replication-and-ha-readiness
description: Use when designing, reviewing, or hardening PostgreSQL replication and high-availability posture against stated reliability targets. Produces streaming and logical replication topology, synchronous vs asynchronous trade-off decisions, replica lag monitoring and thresholds, automated failover behavior (Patroni, repmgr, or managed Multi-AZ), read-replica routing strategy, split-brain prevention, and multi-region posture. Do not use for schema design, query optimization, backup and restore procedures, or access-control hardening; use postgres-schema-and-migration, postgres-indexing-and-query-optimization, postgres-backup-and-operational-readiness, or postgres-security-and-data-access-hardening instead.
---

# Postgres Replication and HA Readiness

## When to use

Invoke when a PostgreSQL deployment has a stated availability or RPO/RTO target, when designing the replication topology for a new service, when validating an existing topology before a reliability review or scale event, or when remediating failover, split-brain, or replica-lag problems.

Do not use for: schema modeling or migrations (use `postgres-schema-and-migration`), query/index performance (use `postgres-indexing-and-query-optimization`), backup/PITR/restore drills (use `postgres-backup-and-operational-readiness`), or role/grant/TLS hardening (use `postgres-security-and-data-access-hardening`).

## Inputs

Required:

- The reliability targets in scope: availability SLO, RPO, RTO, and the failure domains that must be survived. Sourced from `reliability-architecture.md` where it exists.
- The replica topology decision and consistency posture from `data-architecture.md` (single-primary, read replicas, multi-region, sync vs async expectation).
- The deployment substrate: self-managed (Patroni/repmgr), managed (RDS/Aurora/Cloud SQL Multi-AZ), or Kubernetes operator.

Optional:

- Current replication setup: physical vs logical, slots, `synchronous_standby_names`, replica count and placement.
- Write and read throughput, and the read/write split the routing layer must serve.
- Current replica lag measurements and failover history.
- Network topology across AZs/regions and latency budget for synchronous commit.
- Connection-pooling and routing layer in use (PgBouncer, Pgpool, application-side).

## Operating rules

- Replication serves availability and read scaling. It is not a backup. State this explicitly and hand off durability/PITR to `postgres-backup-and-operational-readiness`.
- Every topology decision is justified against a failure domain from `reliability-architecture.md`: instance loss, AZ loss, region loss, or storage loss. A replica that does not survive a named failure domain is theater.
- Synchronous vs asynchronous is an RPO decision with a latency cost. Synchronous commit gives RPO≈0 at a write-latency tax; async gives bounded data loss. State the RPO each choice yields and the latency it costs. Quorum/`ANY` synchronous standbys are the default over a single sync standby.
- Failover must be automated and tested, or it does not count toward RTO. A manual runbook is not an RTO. Name the orchestrator (Patroni, repmgr, managed) and the measured failover time.
- Split-brain prevention is mandatory: fencing/STONITH, a consensus layer (etcd/Consul for Patroni), or the managed provider's guarantee. A topology without an explicit split-brain answer is rejected.
- Replica lag has a defined threshold tied to the read-consistency contract. State the lag budget, the monitoring signal, and the action when breached (route reads to primary, alert, depool replica).
- Read-replica routing makes staleness explicit. Reads requiring read-your-writes go to the primary or use synchronous replicas; eventually-consistent reads may use async replicas with a stated staleness budget.
- Logical replication is for selective/heterogeneous/zero-downtime-upgrade flows, not general HA. If proposed, name why physical streaming is insufficient and account for its limitations (no DDL, sequence, or large-object replication by default).
- Replication slots prevent WAL loss but can fill the primary's disk if a replica is down. Every slot has a monitoring signal and a `max_slot_wal_keep_size` posture.
- Do not co-locate all replicas in the primary's failure domain. AZ/region placement must match the failure domains the SLO requires.
- If the topology cannot meet the stated RPO/RTO within the substrate's constraints, pause and raise an ADR candidate against `reliability` rather than asserting a target the design cannot hold.

## Output contract

The replication and HA design MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — replication lag, slot WAL retention, replica health, and failover events are named observable signals with thresholds, not manual checks.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — failover and topology changes are automated, repeatable, and do not require a not-yet-run manual step to hold the SLO.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — replication slots, standby names, and routing roles follow project naming rules.

Upstream contract: `reliability-architecture.md` is the source of truth for the availability SLO, RPO, RTO, and the failure domains to survive. `data-architecture.md` is the source of truth for the replica topology decision and consistency posture. If the RPO/RTO is unstated or unachievable on the chosen substrate, pause and raise an ADR candidate against `reliability` — do not invent or silently weaken the target.

## Process

1. Establish targets and failure domains. Extract availability SLO, RPO, RTO, and the failure domains to survive from `reliability-architecture.md`. Extract the topology and consistency posture from `data-architecture.md`. If RPO/RTO is missing, pause and escalate.
2. Inventory the current (or proposed) topology: primary, standbys, replication type (physical streaming / logical), slots, `synchronous_commit` and `synchronous_standby_names` settings, replica placement across AZs/regions, and the routing layer.
3. Decide synchronous vs asynchronous per the RPO. If RPO≈0 is required, design quorum synchronous standbys (`ANY n (...)`), state the measured commit-latency cost, and confirm it fits the `performance` write budget (hand off the budget check if unknown).
4. Design the standby topology to match failure domains: number of replicas, AZ/region placement, cascading vs direct, and which replicas are failover candidates vs read-only. Every replica maps to a failure domain it lets the system survive.
5. Choose and specify the failover orchestrator: Patroni (+ etcd/Consul DCS), repmgr, a Kubernetes operator (CloudNativePG/Zalando), or managed Multi-AZ. Define the leader-election mechanism, health checks, and the expected automated failover time. Confirm it meets RTO.
6. Specify split-brain prevention concretely: DCS quorum and fencing for Patroni, watchdog/STONITH where applicable, or the managed provider's documented guarantee. State the behavior under network partition.
7. Define replica-lag posture: the lag budget tied to the read-consistency contract, the monitoring signal (`pg_stat_replication`, `pg_wal_lsn_diff`, replay lag), the alert threshold, and the automatic action on breach (depool, route to primary).
8. Define read-replica routing: which read classes are read-your-writes (→ primary or sync replica) vs eventually-consistent (→ async replica with stated staleness budget), and where routing is enforced (PgBouncer/Pgpool/app). Define behavior during failover (read-only window, reconnection).
9. Define replication-slot posture: slots per standby, `max_slot_wal_keep_size`, the disk-fill monitoring signal, and the cleanup action when a standby is permanently lost.
10. If logical replication is in scope, justify it against physical streaming, enumerate its limitations for this use (DDL/sequence/large-object handling, conflict handling), and define the publication/subscription topology and monitoring.
11. Define multi-region posture if required: sync vs async across regions (latency makes cross-region sync usually infeasible — state the RPO consequence), promotion strategy, and DNS/endpoint failover.
12. Produce the readiness assessment: topology diagram/narrative, the failure-domain coverage matrix (domain → survives? → how), the RPO/RTO the design delivers vs the target, monitoring signals with thresholds, and the failover test plan. Where the design cannot meet the target, state the gap and the ADR candidate.

## Outputs

Required:

- `replication-ha-readiness.md`: topology (narrative or diagram), failure-domain coverage matrix, sync/async decision with RPO and latency cost, failover orchestrator and measured/expected RTO, split-brain prevention mechanism, replica-lag budget and thresholds, read-routing rules, and slot posture.
- Monitoring signal list: replication lag, slot WAL retention, replica health, failover events — each with a threshold and an action.
- Failover test plan: what is exercised (planned switchover, primary kill, AZ loss), expected behavior, and pass criteria.

Conditional, when applicable:

- Logical replication publication/subscription design with limitation analysis.
- Multi-region promotion and endpoint-failover plan.
- ADR candidate(s) where the substrate cannot meet the stated RPO/RTO, or for sync-commit latency trade-offs.

Output rules:

- Every replica and topology element maps to a named failure domain it lets the system survive.
- The RPO/RTO the design delivers is stated explicitly and compared against the target.
- Failover is automated and has a test plan; a manual runbook is not counted as RTO.
- Backup/PITR is explicitly out of scope and handed off to `postgres-backup-and-operational-readiness`.

## Quality checks

- [ ] Availability SLO, RPO, and RTO are sourced from `reliability-architecture.md` (or an ADR candidate is raised for the gap).
- [ ] Every standby maps to a named failure domain it lets the system survive.
- [ ] Sync vs async is decided per the RPO, with the delivered RPO and the write-latency cost both stated.
- [ ] The failover orchestrator is named, with an expected/measured automated failover time compared against RTO.
- [ ] Split-brain prevention is explicit and states behavior under network partition.
- [ ] Replica-lag budget is tied to the read-consistency contract, with a monitoring signal, threshold, and breach action.
- [ ] Read routing distinguishes read-your-writes from eventually-consistent reads with a stated staleness budget.
- [ ] Replication slots have a WAL-retention bound and a disk-fill monitoring signal.
- [ ] Logical replication, if used, is justified against physical streaming with limitations enumerated.
- [ ] The design states the RPO/RTO it actually delivers vs the target, and raises an ADR candidate for any gap.
- [ ] Backup and restore are explicitly deferred to `postgres-backup-and-operational-readiness`.

## References

- Upstream: [`architecture/reliability`](../../../../architecture/reliability/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md).
- Related implementation skills: [`postgres-backup-and-operational-readiness`](../postgres-backup-and-operational-readiness/SKILL.md) (paired durability/restore concern), [`postgres-indexing-and-query-optimization`](../postgres-indexing-and-query-optimization/SKILL.md) (read-replica query posture), [`postgres-schema-and-migration`](../postgres-schema-and-migration/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`modular-monolith`](../../../../../architecture-patterns/modular-monolith/README.md), [`cqrs`](../../../../../architecture-patterns/cqrs/README.md) (read-model replica routing).
