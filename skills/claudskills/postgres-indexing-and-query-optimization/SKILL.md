---
name: postgres-indexing-and-query-optimization
description: Use when reviewing or remediating PostgreSQL query and index performance against a stated performance budget. Produces an index audit (B-tree, hash, GIN, GiST, BRIN, partial, expression, covering), EXPLAIN (ANALYZE, BUFFERS)-driven query review, pg_stat_statements hot-query identification, partitioning validation (range/list/hash), N+1 and join-order remediation, and autovacuum and bloat posture. Do not use for initial schema design, new-table modeling, migration authoring, replication topology, or backup strategy; use postgres-schema-and-migration, postgres-replication-and-ha-readiness, or postgres-backup-and-operational-readiness instead.
---

# Postgres Indexing and Query Optimization

## When to use

Invoke when a PostgreSQL workload has a stated or suspected performance problem, when validating that an existing schema meets `performance` budgets before a scale event, when auditing indexes for redundancy or bloat, or when remediating slow queries, N+1 access, or bad join orders.

Do not use for: greenfield schema modeling or new-table design (use `postgres-schema-and-migration`), migration authoring, replication or HA topology (use `postgres-replication-and-ha-readiness`), backup/restore (use `postgres-backup-and-operational-readiness`), or access-control hardening (use `postgres-security-and-data-access-hardening`).

## Inputs

Required:

- Connection to the target database or a representative copy with production-like data distribution and volume.
- The performance budget in scope: per-query latency targets, throughput expectations, or the specific slow path. Sourced from `performance-architecture.md` where it exists.
- The access patterns the database serves, from `data-architecture.md` or `backend-architecture.md`.

Optional:

- `pg_stat_statements` output or permission to enable it.
- Existing index inventory and DDL.
- Known slow queries, application traces, or APM data.
- Table size, growth rate, and write/read ratio per hot table.
- Partitioning strategy already in place.
- Autovacuum settings and current bloat estimates.

## Operating rules

- Measure before changing. Every recommendation is backed by `EXPLAIN (ANALYZE, BUFFERS)` on production-like data, not by intuition or row counts alone.
- Tie every change to a budget. An optimization with no stated latency or throughput target to satisfy is not in scope — escalate to `performance` for the budget.
- Every proposed index names the query pattern it serves, expected selectivity, the scan type it replaces, and its write-amplification and storage cost. Reject indexes that cannot name a query.
- Find and remove redundant, unused, and duplicate indexes before adding new ones. An unused index is a write tax with no benefit.
- Prefer query and schema-access fixes over index sprawl. An N+1, a missing join predicate, or a non-sargable expression is fixed at the query, not papered over with an index.
- Index creation on a live table uses `CREATE INDEX CONCURRENTLY` and is treated as a migration: it needs the same lock analysis and `migration-plan.md` discipline as `postgres-schema-and-migration`. Hand off the migration mechanics to that skill.
- Validate partitioning against actual pruning. A partition scheme that does not enable partition pruning for the dominant queries is a liability, not a win.
- Autovacuum and bloat are performance concerns. A correct index on a bloated table still underperforms; include vacuum/bloat posture in the review.
- Do not change `random_page_cost`, `work_mem`, or planner settings globally to fix one query without an ADR — prefer per-query or per-role scoping.
- If a fix requires a schema change (new column, denormalization, materialized view), pause and raise it as a handoff to `postgres-schema-and-migration` with the measured justification; do not author the migration here.

## Output contract

Findings and recommendations MUST conform to:

- [naming-conventions](../../../../../standards/naming-conventions/README.md) — index names are explicit and snake_case; no anonymous or ORM-default names introduced.
- [observability-standards](../../../../../standards/observability-standards/README.md) — query latency, slow-query, and bloat signals are named as observable metrics, not one-off manual checks.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — any index DDL is `CONCURRENTLY`, backwards-compatible, and gated as a migration handoff.

Upstream contract: `performance-architecture.md` is the source of truth for latency and throughput budgets. `data-architecture.md` and `backend-architecture.md` are the source of truth for which access patterns are legitimate. If no budget exists for the path under review, pause and raise an ADR candidate against `performance` rather than optimizing to an invented target.

## Process

1. Establish the budget and the workload. Confirm the per-query latency or throughput target from `performance-architecture.md`. Confirm the legitimate access patterns from `data-architecture.md` / `backend-architecture.md`. If either is missing, pause and escalate.
2. Enable and read `pg_stat_statements`. Rank queries by total time, mean time, and call count. Identify the hot set: the queries that consume the budget.
3. Inventory existing indexes. Detect duplicates, overlapping prefixes, unused indexes (`pg_stat_user_indexes` with low/zero scans), and invalid indexes. Mark candidates for removal.
4. For each hot query, capture `EXPLAIN (ANALYZE, BUFFERS)` on production-like data. Identify the cost driver: seq scan on a large table, bad row estimate, nested-loop blowup, sort spill to disk, bitmap heap recheck, or repeated execution (N+1).
5. Classify each finding: missing index, wrong index type, non-sargable predicate, stale statistics, bad join order, missing partition pruning, N+1 from the application, or bloat-induced degradation.
6. For index findings, choose the right index type deliberately: B-tree (equality/range/sort), hash (equality only), GIN (composite/array/jsonb/full-text), GiST (geometric/range/nearest-neighbor), BRIN (large append-only naturally-ordered tables), partial (skewed predicates), expression (computed predicates), or covering (`INCLUDE`) for index-only scans. Justify the choice against the query.
7. For query findings, propose the rewrite: make predicates sargable, fix join order or add the missing join predicate, replace `OFFSET` pagination with keyset pagination, batch N+1 access, or introduce a materialized view (flagging the schema-change handoff).
8. For partitioning findings, validate that the dominant queries carry the partition key and achieve pruning; recommend range/list/hash adjustments or partition-wise join enablement. Validate constraint-exclusion vs runtime pruning behavior.
9. For statistics and planner findings, recommend `ANALYZE`, increased `default_statistics_target` on skewed columns, extended statistics (`CREATE STATISTICS`) for correlated columns, or per-query/per-role planner scoping — never undocumented global GUC changes.
10. For bloat and autovacuum findings, quantify table and index bloat, recommend autovacuum tuning (scale factor, cost limit) per hot table, and flag tables needing `REINDEX CONCURRENTLY` or `pg_repack`.
11. Produce the optimization report: ranked findings, the measured before-state (`EXPLAIN` output and `pg_stat_statements` numbers), the recommended change, the expected after-state, the budget it satisfies, and the cost (write amplification, storage, lock).
12. Verify. Apply recommendations against the production-like copy, re-capture `EXPLAIN (ANALYZE, BUFFERS)` and `pg_stat_statements` deltas, and confirm each change moves the metric toward its budget. Hand off any required index DDL or schema change to `postgres-schema-and-migration` as a migration with lock analysis.

## Outputs

Required:

- `query-optimization-report.md`: ranked findings, each with measured before-state, classification, recommended change, expected after-state, the budget it satisfies, and the cost.
- Index change list: indexes to add (with type, definition, and query justification) and indexes to drop (with evidence of redundancy or non-use), all marked as migration handoffs.

Conditional, when applicable:

- Query rewrites with side-by-side `EXPLAIN (ANALYZE, BUFFERS)` before/after.
- Partitioning validation note with pruning evidence.
- Autovacuum and bloat remediation plan per hot table.
- ADR candidate(s) for global planner setting changes or materialized-view introduction.

Output rules:

- Every recommendation cites measured evidence; no recommendation rests on row counts or intuition alone.
- Every added index names a query; every dropped index names its non-use evidence.
- Index DDL and schema changes are handed off to `postgres-schema-and-migration`, not authored here.
- The report states the budget each change is in service of.

## Quality checks

- [ ] Every finding is backed by `EXPLAIN (ANALYZE, BUFFERS)` on production-like data.
- [ ] Every recommendation names the `performance` budget it is in service of.
- [ ] Every proposed index names its query pattern, type rationale, selectivity, and write/storage cost.
- [ ] Redundant, duplicate, and unused indexes are identified with `pg_stat_user_indexes` evidence before any index is added.
- [ ] N+1, non-sargable predicates, and bad join orders are remediated at the query, not masked with indexes.
- [ ] Partitioning recommendations include pruning evidence for the dominant queries.
- [ ] Autovacuum/bloat posture is assessed for every hot table in scope.
- [ ] Any index DDL or schema change is handed off to `postgres-schema-and-migration` as a `CONCURRENTLY` migration with lock analysis — not authored in this skill.
- [ ] Global planner/GUC changes, if recommended, have an ADR candidate and are scoped per-query or per-role where possible.
- [ ] Post-change verification re-captures `EXPLAIN` and `pg_stat_statements` and shows movement toward budget.

## References

- Upstream: [`architecture/performance`](../../../../architecture/performance/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md).
- Related implementation skills: [`postgres-schema-and-migration`](../postgres-schema-and-migration/SKILL.md) (owns the index/schema DDL and migration mechanics this skill hands off).
- Compatible patterns: [`modular-monolith`](../../../../../architecture-patterns/modular-monolith/README.md), [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`cqrs`](../../../../../architecture-patterns/cqrs/README.md) (read-model query tuning).
