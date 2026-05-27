---
name: replication-patterns
description: "Use when designing how a database keeps multiple copies of its data in agreement across nodes for availability, read scaling, and disaster recovery: the three foundational topologies (single-leader / primary-replica, multi-leader / multi-primary, leaderless / quorum), synchronous vs asynchronous replication and the replication-lag trade-off, log shipping vs statement replication vs trigger-based replication, the read-after-write consistency problem and its mitigations (sticky session, read-from-leader, monotonic reads), the failover model and split-brain risk, and the relationship to the CAP/PACELC choices the topology realizes. Do NOT use for horizontal partitioning across nodes (use sharding-strategy), the CAP theoretical frame itself (use cap-theorem-tradeoffs), single-node transactional guarantees (use acid-fundamentals), or query tuning (use query-optimization)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"engineering\",\"domain\":\"engineering/data\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-16\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-16\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"replication\\\\\\\",\\\\\\\"primary replica\\\\\\\",\\\\\\\"multi-leader\\\\\\\",\\\\\\\"leaderless\\\\\\\",\\\\\\\"quorum\\\\\\\",\\\\\\\"synchronous replication\\\\\\\",\\\\\\\"asynchronous replication\\\\\\\",\\\\\\\"replication lag\\\\\\\",\\\\\\\"read-after-write\\\\\\\",\\\\\\\"failover\\\\\\\",\\\\\\\"split brain\\\\\\\",\\\\\\\"log shipping\\\\\\\",\\\\\\\"WAL streaming\\\\\\\"]\",\"triggers\":\"[\\\\\\\"single-leader vs multi-leader\\\\\\\",\\\\\\\"synchronous vs async replication\\\\\\\",\\\\\\\"what happens on failover\\\\\\\",\\\\\\\"split brain\\\\\\\",\\\\\\\"read-after-write consistency\\\\\\\"]\",\"examples\":\"[\\\\\\\"design replication topology for a service with one region writing and three regions reading\\\\\\\",\\\\\\\"decide between synchronous and asynchronous replication given a target RPO\\\\\\\",\\\\\\\"diagnose stale reads after a write — likely replication lag without read-after-write handling\\\\\\\",\\\\\\\"explain the split-brain risk in multi-leader replication\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"horizontally partition data across nodes (use sharding-strategy)\\\\\\\",\\\\\\\"reason about the CAP theorem abstractly (use cap-theorem-tradeoffs)\\\\\\\",\\\\\\\"explain ACID properties (use acid-fundamentals)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"cap-theorem-tradeoffs\\\\\\\",\\\\\\\"acid-fundamentals\\\\\\\",\\\\\\\"sharding-strategy\\\\\\\",\\\\\\\"transaction-isolation\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"cap-theorem-tradeoffs\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"cap-theorem-tradeoffs owns the theoretical frame for the consistency-availability trade-off; this skill owns the operational topologies and protocols that realize a chosen position on that trade-off. The two compose: CAP names the choice; replication-patterns is one of the realizations.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"sharding-strategy\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"sharding-strategy owns horizontal partitioning of data across nodes (different nodes hold different data); this skill owns replication of the same data across nodes (multiple nodes hold the same data). The two often combine in production systems but answer different questions.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"acid-fundamentals\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"acid-fundamentals owns the single-system transactional model; this skill owns the multi-node replication patterns that distributed systems use to scale, replicate, and survive failure. Replication often relaxes some ACID properties (most notably durability and isolation in async modes).\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"cap-theorem-tradeoffs\\\\\\\",\\\\\\\"sharding-strategy\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"Replication is to a database what mirror copies of a master photograph are to a museum's record — single-leader async is the photographer keeping the negative and printing copies as requested; single-leader sync is the conservator requiring two darkroom signatures before any print leaves the building; multi-leader is multiple authorized photographers in different cities each accepting submissions and reconciling at intervals; leaderless quorum is asking three of five archivists to vote on whether this print matches the master, accepting their verdict. Failover is replacing the negative-keeper when they retire; split brain is what happens when the agency forgets to revoke the old keeper's keys.\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"Replication is the discipline of keeping multiple copies of the same data on multiple nodes so that the system can serve reads from any copy, survive the failure of any node, or both. The three foundational topologies are single-leader (primary-replica; one node accepts writes, others receive a stream of changes), multi-leader (multi-primary; multiple nodes accept writes and reconcile), and leaderless (quorum; clients write to a quorum of nodes directly). Each topology has its own consistency, availability, conflict-handling, and operational properties; choosing among them is choosing the system's CAP/PACELC position and accepting the operational complexity that comes with it. Synchronous vs asynchronous replication is an orthogonal choice within each topology, trading durability/consistency against latency. The discipline is matching the topology and the synchrony choice to the workload's actual requirements for read scaling, write availability, recovery point objective (RPO), and recovery time objective (RTO).\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/replication-patterns/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/replication-patterns/SKILL.md
---

# Replication Patterns

## Coverage

The catalog of replication topologies and the operational discipline that makes them work in production. Covers the three foundational topologies (single-leader / primary-replica, multi-leader / multi-primary, leaderless / quorum), the synchrony spectrum (sync, semi-sync, async, quorum-sync), the mechanism choices (statement-based, row-based, trigger-based, logical, physical), the read-after-write consistency problem and its mitigations (sticky session, read-from-leader, monotonic reads, version tokens), the failover model and quorum-based split-brain prevention, the conflict-resolution choices in multi-leader and leaderless systems (LWW, CRDTs, vector clocks, application merge), and the relationship to the CAP/PACELC choices the topology realizes.

## Philosophy

Replication is the discipline that gives a database fault tolerance, read scaling, and disaster recovery — at the cost of consistency-handling, conflict resolution, and operational complexity.

The default starting point is single-leader with asynchronous replication: simple, well-understood, sufficient for most read-mostly workloads. The departures from this default — multi-leader, leaderless, synchronous, geographic — each address a specific requirement (multi-region writes, strong consistency under partition, RPO=0) and add proportional complexity.

The most common production failures are not in the replication topology itself but in the application's handling of its consequences: stale reads producing user-visible bugs, split brain producing silent data divergence, failover producing unrehearsed surprises. The discipline is treating replication as an architecture the application is co-designed with, not a database feature that handles itself.

## Topology Selection

| Topology | Best for | Trade-offs |
|---|---|---|
| Single-leader, async | Read-heavy workloads with tolerance for stale reads | Replication lag; possible data loss on leader failure |
| Single-leader, sync | Workloads requiring RPO=0 | Write latency; replica failure can block writes |
| Multi-leader | Multi-region writes; active-active disaster recovery | Conflict resolution complexity |
| Leaderless (quorum) | High availability with tunable consistency | Read latency = slowest of R; quorum-sizing decisions |
| Synchronous via Raft/Paxos (Spanner, CockroachDB) | Strong consistency at scale | High write latency for distant replicas |

The starting point for most workloads is single-leader async; depart from this default only when the workload requires it.

## Synchronous vs Asynchronous Trade-off

| Property | Synchronous | Asynchronous |
|---|---|---|
| Write latency | Higher (waits for replica) | Lower (acks immediately) |
| RPO (data loss on failure) | Zero | Up to lag window |
| Read consistency from replicas | Strong | Eventual |
| Replica failure impact | Can block writes | None |
| Use case | High-stakes financial transactions, strong-RPO systems | Most production read-replicas |

Semi-sync (wait for one replica with timeout-to-async fallback) is the middle ground; production-default for many systems.

## Read-After-Write Mitigations

| Mitigation | How it works | Cost |
|---|---|---|
| Read-from-leader for a window after write | Client routes back to leader for N seconds | Loses read scaling for write-heavy users |
| Sticky session | Client always reads from same replica | Replica failure invalidates session |
| Monotonic reads | Client tracks last-seen version; replica must be ≥ that fresh | Requires version-token plumbing |
| Wait-for-replica | Client waits until replica catches up | Adds latency to the read |
| Accept stale reads | Application tolerates staleness | Only viable when stale data is OK |

Every read-mostly workload with async replicas must choose one. Defaulting to "read from any replica" produces stale-data bugs.

## Failover and Split-Brain Prevention

| Mechanism | Split-brain risk | Used by |
|---|---|---|
| Manual operator failover | None (if procedure is correct) | Small / legacy systems |
| Heuristic auto-failover (no quorum) | High under partition | Older Postgres tools (without proper consensus) |
| Quorum-based promotion (Raft / Paxos) | Eliminated by majority requirement | Modern HA tools (Patroni, etcd, CockroachDB internal) |
| STONITH fencing | Old leader killed; cannot continue writing | Pacemaker / Corosync HA |

A system that must not split-brain uses quorum-based promotion. The cost is requiring an odd number of voting nodes ≥ 3.

## Verification

After applying this skill, verify:
- [ ] The replication topology is intentional and documented: single-leader / multi-leader / leaderless; sync / async / semi-sync; physical / logical / trigger-based.
- [ ] Read-after-write consistency is handled explicitly. Sticky session, read-from-leader, monotonic reads, version tokens, or accept-stale is a named choice.
- [ ] Replication lag is monitored. Lag thresholds trigger alerts before users notice.
- [ ] Failover procedure is documented, tested, and rehearsed. Untested failover is failover that fails first time.
- [ ] Split-brain prevention uses quorum-based promotion for any system requiring it. Heuristic failover is recognized as risky.
- [ ] Backups exist separately from replication. Replica state and backup state are distinguished.
- [ ] For multi-leader: the conflict resolution mechanism (LWW / CRDT / vector clocks / app merge) is defined and tested with concurrent-write scenarios.
- [ ] For leaderless: W and R values are chosen for the workload's consistency-vs-latency target; W+R>N if strong consistency is required.
- [ ] Cross-region replication latency is measured and accepted as part of the design budget.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Horizontally partitioning data across nodes | `sharding-strategy` | sharding partitions data; replication copies it |
| Reasoning about the CAP/PACELC theoretical frame | `cap-theorem-tradeoffs` | CAP names the trade-off; this skill realizes it |
| Single-node transactional guarantees | `acid-fundamentals` | ACID is the single-system frame |
| Choosing isolation levels | `transaction-isolation` | transaction-isolation owns concurrency; this owns multi-node |
| Indexing | `indexing-strategy` | indexing is within-node retrieval |
| Tuning a slow query | `query-optimization` | query-optimization is per-query |

## Key Sources

- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 5 (Replication) — modern comprehensive treatment of all three topologies with practical detail.
- Lamport, L. (1998). ["The Part-Time Parliament"](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf). *ACM TOCS*, 16(2). The Paxos consensus algorithm; foundation of synchronous replication with split-brain prevention.
- Ongaro, D., & Ousterhout, J. (2014). ["In Search of an Understandable Consensus Algorithm (Raft)"](https://raft.github.io/raft.pdf). *USENIX ATC 2014*. The Raft consensus algorithm; basis of etcd, CockroachDB, many modern HA systems.
- DeCandia, G., Hastorun, D., Jampani, M., et al. (2007). ["Dynamo: Amazon's Highly Available Key-Value Store"](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf). *SOSP 2007*. The foundational paper on leaderless (Dynamo-style) replication; basis of Cassandra, Riak, DynamoDB.
- PostgreSQL Global Development Group. ["PostgreSQL Documentation — Replication"](https://www.postgresql.org/docs/current/runtime-config-replication.html) and ["Logical Replication"](https://www.postgresql.org/docs/current/logical-replication.html). Reference for Postgres physical streaming and logical replication.
- MySQL Reference Manual. ["Replication"](https://dev.mysql.com/doc/refman/8.0/en/replication.html). MySQL replication including binlog formats, semi-sync, and group replication.
- MongoDB Manual. ["Replication"](https://www.mongodb.com/docs/manual/replication/). MongoDB replica sets, automatic failover, and oplog-based replication.
- Vogels, W. (2009). ["Eventually Consistent"](https://queue.acm.org/detail.cfm?id=1466448). *ACM Queue*. Practitioner essay on eventual consistency in replicated systems.
- Shapiro, M., Preguiça, N., Baquero, C., & Zawirski, M. (2011). ["A Comprehensive Study of Convergent and Commutative Replicated Data Types"](https://hal.inria.fr/inria-00555588). CRDT foundational paper; basis for multi-leader conflict resolution without data loss.
- Brewer, E. (2012). ["CAP Twelve Years Later"](https://ieeexplore.ieee.org/document/6133253). *IEEE Computer*. Brewer's retrospective on CAP, useful for understanding the consistency-availability trade-offs replication realizes.
