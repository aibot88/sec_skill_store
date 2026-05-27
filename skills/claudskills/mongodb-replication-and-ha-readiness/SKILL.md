---
name: mongodb-replication-and-ha-readiness
description: Use when designing or hardening MongoDB replica-set topology and high-availability posture after the data model exists and reliability and data-architecture have set the availability and consistency targets. Produces replica-set member topology and election behavior, read-preference routing, write-concern selection that the topology can actually honor, arbiter posture, oplog-window sizing for failover, change-stream availability, and multi-region replica placement. Do not use for document modeling or shard-key choice, query tuning, backup/PITR, security/auth, or host/cluster provisioning; use the other Family B archetype skills (provisioning is infrastructure).
---

# MongoDB Replication and HA Readiness

## When to use

Invoke when standing up a replica set for production, restructuring members/elections, validating that the declared write/read concerns are actually survivable, sizing the oplog for failover, or placing replicas across regions.

Do not use for: document modeling, validators, or shard-key choice (use `mongodb-data-model-and-migration`); query/index tuning (use `mongodb-indexing-and-query-optimization`); backup, oplog-based PITR, restore drills (use `mongodb-backup-and-operational-readiness`); auth/RBAC/TLS/audit and internal-auth credentials (use `mongodb-security-and-data-access-hardening`); host, VM, or cluster provisioning (infrastructure layer — this skill designs the MongoDB topology, not the machines).

## Inputs

Required:

- An existing data model from `mongodb-data-model-and-migration` (the per-operation read/write concern declarations this topology must be able to honor).
- Approved `architecture/reliability` availability targets and RPO/RTO per data tier, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `data-architecture.md` consistency posture and replica/region intent.
- The workload tier from `architecture-schema` (drives member count, region spread, arbiter prohibition).
- Read/write mix and latency sensitivity per operation class.
- Region/AZ topology available and inter-region latency.
- Change-stream consumers (resumability requirements) and their lag tolerance.

## Operating rules

- Never design a topology the declared concerns cannot survive. If the model declares `w: "majority"`, the member topology must keep a writable majority through the planned failure (one node, one AZ, one region per the tier). A topology that cannot honor the declared concern is rejected.
- Consume `architecture/reliability` and `data-architecture.md`; do not invent decisions. Availability targets, RPO/RTO, and consistency posture are upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Design the topology; do not redesign the model. Per-operation read/write concern is declared by `mongodb-data-model-and-migration`. This skill ensures the replica set can *honor* it; a concern that is wrong for the durability requirement is a finding handed back, not changed here.
- Odd voting-member count; elections must always resolve. An even voting count or a partition-prone layout that can deadlock an election is rejected. Member priorities reflect intended primary placement.
- Arbiters are a last resort, not a default. An arbiter contributes a vote but no data — with `w: "majority"` it can force acknowledged-but-not-durable writes on a member loss. Arbiters are prohibited for tier-0 and used elsewhere only with an explicit ADR.
- Read preference is explicit and consistency-aware. `primary` for read-after-write; `secondaryPreferred`/`nearest` only where staleness is acceptable and stated. Every secondary-read path names its staleness tolerance; `maxStalenessSeconds` is set where used.
- Write concern is sized to durability, not latency convenience. State-mutating writes default to `w: "majority"` (and `j: true` where the loss of the last write is unacceptable). A relaxed concern names the data it applies to and the accepted loss window.
- The oplog window must exceed the worst recovery interval. Size the oplog so a lagging or recovering secondary (and the failover/maintenance window) fits inside it; an oplog that rolls over before a secondary catches up forces a full resync. State the measured window vs the requirement.
- Multi-region placement matches the tier and the RTO. Tier-0 cross-region posture (and whether a region can be lost without data loss given the write concern) is explicit, including the latency cost of `w: "majority"` across regions.
- Change-stream availability is designed, not assumed. If consumers depend on change streams, resumability (resume tokens), the oplog window backing them, and behavior across failover are specified.
- This skill owns replica-set topology + HA posture. Modeling, query tuning, backup/PITR, security/auth, and host provisioning are named handoffs; internal-auth (keyfile/x.509) is required and named to `mongodb-security-and-data-access-hardening`.
- A topology whose failover has not been rehearsed (stepdown/kill the primary; confirm election, concern still honored, no data loss) is not done.

## Output contract

The replication and HA design MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — replication lag, election/stepdown events, oplog window, and member health are exposed signals.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — the topology is reproducible from configuration, not click-ops; member changes are rolling.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives member count, region spread, and arbiter prohibition.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — replica-set and member naming.
- [security-standards](../../../../../standards/security-standards/README.md) — internal auth (keyfile/x.509) and TLS between members are required; the mechanism is named to `mongodb-security-and-data-access-hardening`.

Upstream contract: `architecture/reliability` is the source of truth for availability targets and RPO/RTO; `data-architecture.md` is the source of truth for consistency posture. Per-operation read/write concern is declared by `mongodb-data-model-and-migration`. If a needed decision is missing, pause and raise an ADR candidate.

## Progressive references

- Read `references/mongodb-replication-playbook.md` when designing any owned area or checking the anti-pattern list.
- Read `references/mongodb-replication-quality-rubric.md` before declaring the topology complete.
- Use `assets/mongodb-replication.template.md` as the topology / read-preference / write-concern / oplog pattern reference.

## Process

1. Gather context: load `architecture/reliability` (availability, RPO/RTO) and `data-architecture.md` (consistency, region intent). Pull the per-operation read/write concern declarations from `mongodb-data-model-and-migration`. Resolve the tier from `architecture-schema`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Design member topology: odd voting count, data-bearing members across the AZ/region spread the tier requires, member priorities reflecting intended primary placement, hidden/delayed members if the reliability posture calls for them.
3. Validate concern survivability: confirm the declared `w`/`readConcern` is still honored through the planned failure (one node / one AZ / one region per tier). Where it is not, raise a finding to `mongodb-data-model-and-migration` or an ADR candidate.
4. Set arbiter posture: prohibit for tier-0; elsewhere only with an explicit ADR documenting the durability trade-off under `w: "majority"`.
5. Define read-preference routing per operation class: `primary` for read-after-write, `secondaryPreferred`/`nearest` only with a stated staleness tolerance and `maxStalenessSeconds`.
6. Confirm write-concern posture matches durability: `w: "majority"` (+ `j: true` where required) for state mutations; any relaxed concern names the data and the accepted loss window.
7. Size the oplog: compute the worst recovery/lag/maintenance interval and set the oplog window to exceed it; state measured-vs-required.
8. Design multi-region placement (if in scope): member roles per region, the latency cost of cross-region majority, and whether a region loss is survivable without data loss given the write concern.
9. Specify change-stream availability: resume-token handling, the oplog window backing streams, and failover behavior for consumers.
10. Rehearse failover: step down or kill the primary; confirm a timely election, the declared concerns still honored, no acknowledged-write loss; capture timings vs the RTO. Document any check that cannot run.
11. Produce `replication-ha.md` (member/priority/region map, concern-survivability matrix, read-preference table, oplog sizing, change-stream posture, rehearsed-failover results) plus the named handoff list. Validate against observability-, deployment-, security-standards, architecture-schema, and naming-conventions. Revise until all pass or the gap is documented.

## Outputs

Required:

- Replica-set member topology (counts, priorities, AZ/region placement, hidden/delayed if used).
- Concern-survivability matrix: declared `w`/`readConcern` vs the planned failure.
- Read-preference routing table with staleness tolerances and `maxStalenessSeconds`.
- Write-concern posture per operation class with accepted-loss windows for any relaxed concern.
- Oplog sizing (measured worst recovery interval vs configured window).
- Multi-region placement and change-stream availability design (where in scope).
- Rehearsed-failover results vs RTO.
- `replication-ha.md` and the named handoff list.

Output rules:

- Reproducible topology configuration — not prose-only, not click-ops.
- Odd voting count; no tier-0 arbiter; no topology that cannot honor the declared concern.
- Every secondary-read path states its staleness tolerance.
- Modeling, query tuning, backup/PITR, security/auth, and host provisioning are named handoffs.

## Quality checks

- [ ] Availability targets and RPO/RTO are sourced from `architecture/reliability`; consistency posture from `data-architecture.md` (or an ADR candidate is raised).
- [ ] The declared per-operation read/write concerns come from `mongodb-data-model-and-migration`; this skill does not redefine them.
- [ ] Voting-member count is odd and elections always resolve; member priorities reflect intended primary placement.
- [ ] No arbiter for tier-0; any arbiter elsewhere has an ADR documenting the `w:"majority"` durability trade-off.
- [ ] The declared write/read concern is honored through the planned failure (node/AZ/region per tier); a gap is a finding or ADR candidate.
- [ ] Every secondary-read path names a staleness tolerance and sets `maxStalenessSeconds`.
- [ ] State-mutating writes use `w: "majority"` (+ `j: true` where required); relaxed concerns name the data and accepted loss window.
- [ ] The oplog window exceeds the worst recovery/lag/maintenance interval (measured vs required stated).
- [ ] Multi-region placement (if in scope) states the cross-region majority latency cost and region-loss survivability.
- [ ] Change-stream resumability and failover behavior are specified where consumers exist.
- [ ] Failover was rehearsed (primary stepdown/kill) with election timing, concern still honored, and no acknowledged-write loss, or the gap is documented.

## References

- Upstream: [`architecture/reliability`](../../../../architecture/reliability/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md).
- Builds on: [`mongodb-data-model-and-migration`](../mongodb-data-model-and-migration/SKILL.md) (declares the per-operation read/write concerns this topology must honor).
- Related Family B archetype skills: `mongodb-indexing-and-query-optimization`, `mongodb-backup-and-operational-readiness` (oplog-based PITR/restore), `mongodb-security-and-data-access-hardening` (internal auth + TLS between members).
- Downstream: backend implementation skills own read-preference wiring in ODM/repository code.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`security-standards`](../../../../../standards/security-standards/README.md).
