---
name: mongodb-indexing-and-query-optimization
description: Use when auditing or optimizing MongoDB query and aggregation performance for an existing data model after data-architecture and the data model exist and performance has set the query SLOs. Produces an explain("executionStats")-driven query review, an index audit (compound/multikey/text/geo/TTL/partial/wildcard), aggregation-pipeline cost review, projection and collation posture, shard-key effectiveness analysis, and profiler-driven hot-collection identification with a remediation plan. Do not use for document modeling, validator or shard-key choice, replication topology, backup, security hardening, or ODM/repository query code; use the other Family B archetype skills (modeling/shard-key is data-model-and-migration; ODM code is the backend skill).
---

# MongoDB Indexing and Query Optimization

## When to use

Invoke when MongoDB queries or aggregation pipelines miss their SLO, when reviewing an inherited index set for waste or gaps, when a collection has gone hot, or when validating shard-key effectiveness against real query routing.

Do not use for: document modeling, `$jsonSchema` validators, or shard-key *choice* (use `mongodb-data-model-and-migration`); replica read-preference topology (use `mongodb-replication-and-ha-readiness`); backup/restore (use `mongodb-backup-and-operational-readiness`); auth/RBAC/encryption (use `mongodb-security-and-data-access-hardening`); ODM/repository query code (the backend implementation skill owns that — this skill tunes the engine, not application code).

## Inputs

Required:

- An existing MongoDB data model and index set from `mongodb-data-model-and-migration` (the collections, validators, and declared access patterns this skill audits against).
- Approved `performance` query SLOs (latency/throughput targets per query class), or explicit confirmation they are intentionally deferred.

Optional:

- Approved `data-architecture.md` consistency and sharding posture (shard-key effectiveness is judged against it).
- The slow-query / profiler output, or access to a prod-like dataset to capture it.
- Top query and aggregation shapes by frequency and by latency.
- Collection sizes, document-size distribution, working-set vs RAM, write rates.
- Read-preference in use (affects whether secondary index coverage matters).

## Operating rules

- Never optimize without evidence. `explain("executionStats")` (or `allPlansExecution`) on a representative dataset is the unit of evidence; an index change with no before/after explain is rejected.
- Consume `performance` and `data-architecture.md`; do not invent decisions. The query SLOs, consistency posture, and sharding decision are upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Tune the engine; do not redesign the model. Document shape, validators, and the shard-key *choice* are `mongodb-data-model-and-migration`'s ownership. This skill audits and optimizes against the existing model; a needed model change is raised as a finding and handed back, not made here.
- Every index earns its keep. Each index maps to a named query/aggregation pattern with a cardinality expectation and a write-impact note. Unused, redundant (prefix-of-another), and "just in case" indexes are flagged for removal — index bloat is a write tax and a RAM tax.
- Compound index order follows ESR. Equality, then Sort, then Range. A compound index violating ESR for its target query is a defect unless explicitly justified.
- A query that does a `COLLSCAN` on a non-trivial collection is a finding. The fix is an index, a query rewrite, or a documented acceptance with rationale and size bound — never silent.
- Covered queries where it matters. For hot read paths, prefer a covering index + projection so the query is served from the index; flag fetched-but-unused fields.
- Aggregation pipelines are cost-reviewed stage by stage. `$match` and `$project` pushed early; `$lookup` cardinality bounded; `$sort` backed by an index or bounded by `$limit`; `$unwind` explosion noted. A blocking sort or an unbounded `$lookup` on a hot path is a finding.
- Collation and projection are explicit on text/locale-sensitive paths. A query whose collation differs from its index's collation silently does not use the index — call it out.
- Shard-key effectiveness is judged on routing, not theory. Using the profiler / explain, quantify how many queries are single-shard vs scatter-gather; a hot or scatter-prone shard key is reported as a finding to `mongodb-data-model-and-migration` (resharding is its ownership).
- Hot collections are found via the profiler, not guesswork. Enable the profiler at an appropriate threshold (or read the slow-query log), rank by total time and by frequency, and remediate the top contributors.
- This skill owns query/index/pipeline optimization. Modeling, replication, backup, security, and ODM code are named handoffs.
- An optimization without a captured before/after `explain` (and, for hot paths, a profiler delta) is not done.

## Output contract

The optimization MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — slow-query/profiler signals and query-latency metrics exposed; the profiler posture is reproducible, not ad-hoc.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — named indexes describing their purpose; no anonymous index keys.
- [security-standards](../../../../../standards/security-standards/README.md) — profiler/explain captures and exported query samples carry no PII or secrets.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — index builds on live collections use a rollout-safe path (rolling/background) and are reproducible from source.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — indexes stay within the owning component's collections; no cross-component index coupling.

Upstream contract: `performance` is the source of truth for query SLOs; `data-architecture.md` is the source of truth for consistency and sharding posture. Document modeling, validators, and shard-key choice belong to `mongodb-data-model-and-migration`. If a needed decision is missing, pause and raise an ADR candidate.

## Progressive references

- Read `references/mongodb-indexing-playbook.md` when auditing any owned area or checking the anti-pattern list.
- Read `references/mongodb-indexing-quality-rubric.md` before declaring the optimization complete.
- Use `assets/mongodb-indexing.template.md` as the explain/index-audit/pipeline-review pattern reference.

## Process

1. Gather context: load `performance` (query SLOs) and `data-architecture.md` (consistency, sharding). Pull the existing model, validators, and declared access patterns from `mongodb-data-model-and-migration`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Enable evidence collection: turn on the database profiler at an appropriate `slowms` (or read the slow-query log) on a representative dataset; capture the top query and aggregation shapes by total time and by frequency.
3. Audit the index set: list every index, map each to a named query pattern, and flag unused, redundant (prefix), and unjustified indexes for removal with the write/RAM cost stated.
4. Review hot queries via `explain("executionStats")`: identify `COLLSCAN`, large `totalDocsExamined : nReturned` ratios, in-memory sorts, and non-covered hot reads; propose an index, rewrite, or documented acceptance per finding.
5. Verify compound-index ESR order against each target query; flag and correct violations.
6. Cost-review aggregation pipelines stage by stage: early `$match`/`$project`, index-backed or bounded `$sort`, bounded `$lookup`, noted `$unwind` explosion; rewrite or index the blocking stages.
7. Check collation/projection alignment on text/locale-sensitive paths; flag index-collation mismatches that silently disable the index.
8. Analyze shard-key effectiveness (if sharded): quantify single-shard vs scatter-gather query share; report a hot or scatter-prone key as a finding to `mongodb-data-model-and-migration`.
9. Validate: re-run `explain("executionStats")` for each changed query and capture the before/after; for hot paths, capture the profiler delta; confirm SLOs are met or document the residual gap.
10. Produce `query-optimization.md` (profiler findings ranked, index-audit table with keep/drop/add + rationale, per-query before/after explain, pipeline rewrites, shard-key finding if any) plus the named handoff list. Validate against observability-, naming-, security-, deployment-standards and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Profiler/slow-query findings ranked by total time and frequency.
- Index-audit table: every index → query pattern, keep/drop/add decision, write/RAM-cost note.
- Per-hot-query `explain("executionStats")` before/after with the chosen remediation.
- Aggregation-pipeline cost review with rewrites for blocking stages.
- Collation/projection alignment findings.
- Shard-key effectiveness analysis (if sharded) handed back to modeling where the key is wrong.
- `query-optimization.md` and the named handoff list.

Output rules:

- Functional, reproducible index/pipeline definitions — not prose-only.
- No index change without a before/after `explain`; no PII/secrets in captured samples.
- No model/validator/shard-key redesign here — those are findings handed to `mongodb-data-model-and-migration`.
- Live index builds use a rollout-safe path; modeling, replication, backup, security, and ODM code are named handoffs.

## Quality checks

- [ ] Query SLOs are sourced from `performance`; consistency/sharding posture from `data-architecture.md` (or an ADR candidate is raised).
- [ ] Every index maps to a named query/aggregation pattern; unused, redundant, and "just in case" indexes are flagged with their write/RAM cost.
- [ ] Every compound index target follows ESR (equality, sort, range) or has a documented exception.
- [ ] Every `COLLSCAN` on a non-trivial collection is a finding with an index, rewrite, or documented bounded acceptance.
- [ ] Hot read paths are covered (index + projection) or the gap is justified.
- [ ] Aggregation pipelines are stage-cost-reviewed; blocking sorts and unbounded `$lookup`/`$unwind` on hot paths are remediated.
- [ ] Collation/projection mismatches that silently disable an index are called out.
- [ ] Shard-key effectiveness is quantified (single-shard vs scatter-gather); a wrong key is a finding handed to `mongodb-data-model-and-migration`.
- [ ] Every changed query has a captured before/after `explain("executionStats")`; hot paths have a profiler delta.
- [ ] Modeling, replication, backup, security, and ODM code are named handoffs, not done here.

## References

- Upstream: [`architecture/performance`](../../../../architecture/performance/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md).
- Builds on: [`mongodb-data-model-and-migration`](../mongodb-data-model-and-migration/SKILL.md) (model, validators, declared access patterns; owns modeling and shard-key choice).
- Related Family B archetype skills: `mongodb-replication-and-ha-readiness`, `mongodb-backup-and-operational-readiness`, `mongodb-security-and-data-access-hardening`.
- Downstream: backend implementation skills own ODM/repository query code; this skill tunes the engine.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
