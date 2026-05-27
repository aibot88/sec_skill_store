---
name: postgres-security-and-data-access-hardening
description: Use when designing, reviewing, or hardening PostgreSQL access control and data protection against the security architecture and data classification. Produces TLS and connection-security configuration, least-privilege role and grant model, row-level security policies for tenant isolation, column-level grants and encryption for PII, pgcrypto and at-rest/TDE posture, pgaudit configuration, credential and secret rotation posture, and network-exposure review. Do not use for schema design, query optimization, replication topology, or backup and restore; use postgres-schema-and-migration, postgres-indexing-and-query-optimization, postgres-replication-and-ha-readiness, or postgres-backup-and-operational-readiness instead.
---

# Postgres Security and Data Access Hardening

## When to use

Invoke when a PostgreSQL deployment must enforce a security architecture and data classification at the engine, when reviewing an existing database for access-control and data-protection gaps before go-live or a security review, or when remediating over-privileged roles, missing tenant isolation, unprotected PII, or weak connection security.

Do not use for: schema modeling or migrations (use `postgres-schema-and-migration`), query/index performance (use `postgres-indexing-and-query-optimization`), replication/HA topology (use `postgres-replication-and-ha-readiness`), or backup/restore/PITR (use `postgres-backup-and-operational-readiness`).

## Inputs

Required:

- The security architecture in scope: trust boundaries, threat model, authorization model, and tenant-isolation requirements, sourced from `security-architecture.md` where it exists.
- The data classification: which tables/columns are PII, confidential, or regulated, sourced from `security-architecture.md` / `data-architecture.md`.
- The deployment substrate: self-managed, managed (RDS/Aurora/Cloud SQL), or Kubernetes operator — this constrains TLS, audit, and TDE options.

Optional:

- Current role/grant inventory, `pg_hba.conf`, and `postgresql.conf` security settings.
- Existing RLS policies, column grants, and encryption usage.
- Application connection model (single app role, per-tenant role, connection pooler identity).
- Secret store and rotation mechanism in use.
- Compliance regime (GDPR/HIPAA/PCI/SOC2) and audit obligations.
- Network topology and current exposure (public IP, VPC, allowlists).

## Operating rules

- Enforce the architecture; do not invent the policy. The authorization model, tenant-isolation requirement, and data classification come from `security-architecture.md`. If a needed classification or isolation boundary is unstated, pause and raise an ADR candidate against `security` — do not guess.
- Least privilege is the default and is concrete. No role has `SUPERUSER`, broad `ALL PRIVILEGES`, or ownership it does not need. Application roles are not table owners. `PUBLIC` grants are revoked unless explicitly justified.
- Tenant isolation for tier-0/regulated multi-tenant data is enforced at the engine with Row-Level Security, not solely in application code. "The application filters by tenant_id" is not acceptable isolation for regulated data (per the data-layer decided constraints).
- PII protection uses the engine's capabilities: column-level `GRANT`/`REVOKE`, RLS, and encryption (`pgcrypto` for column-level, or substrate TDE for at-rest) per the classification. Application-only enforcement is rejected for tier-0 columns.
- Connection security is mandatory: TLS required (`sslmode=verify-full` expectation on clients, `ssl=on`, modern cipher/version floor), scram-sha-256 authentication, and `pg_hba.conf` that denies by default and never uses `trust` for non-local production access.
- Audit is scoped, not boil-the-ocean: `pgaudit` (or substrate-native audit) configured for the security-relevant event classes named by the threat model (DDL, role changes, privileged reads on regulated data), with log routing and tamper-evidence per `observability-standards`. Auditing everything is a performance and noise failure.
- Secrets and credentials have a rotation posture: no static long-lived superuser in app config, rotation owner and cadence stated, and the restore/bootstrap path does not embed an unrotated secret. Prefer IAM/short-lived auth where the substrate offers it.
- Network exposure is reviewed explicitly: no public database endpoint without a justified, allowlisted, TLS-enforced exception; the default is private connectivity within the platform trust zone (consumed from `infrastructure-platform`, not redesigned here).
- Every control names the threat or boundary it enforces from the threat model. Controls without a mapped threat are removed (no security theater); threats without a control are reported as gaps.
- Encryption choices state their threat model: `pgcrypto` protects against DB-file/backup exposure but puts keys in SQL/clients; TDE protects at-rest media loss but not a compromised superuser. Name what each does and does not defend.

## Output contract

The hardening design MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — authentication schemes, authorization scopes, secret handling, TLS, and PII tagging are enforced at the engine consistent with the standard.
- [architecture-schema § data ownership](../../../../../standards/architecture-schema/README.md) — grants respect single-component ownership; no cross-component write grants introduced.
- [observability-standards](../../../../../standards/observability-standards/README.md) — audit log routing, privileged-access signals, and auth-failure signals are named observable outputs with retention.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — roles, policies, and audit objects follow project naming rules.

Upstream contract: `security-architecture.md` is the source of truth for the threat model, authorization model, trust boundaries, and tenant-isolation requirement. `data-architecture.md` / `security-architecture.md` is the source of truth for data classification. `infrastructure-platform` owns the network trust zone (consumed, not redesigned). If classification or an isolation boundary the design needs is unstated, pause and raise an ADR candidate against `security`.

## Process

1. Establish the policy and classification. Extract the threat model, authorization model, trust boundaries, and tenant-isolation requirement from `security-architecture.md`; extract the data classification (PII/confidential/regulated tables and columns) from `security-architecture.md` / `data-architecture.md`. If anything required is unstated, pause and escalate.
2. Inventory the current security posture: roles and memberships, grants (including `PUBLIC` and ownership), `pg_hba.conf`, TLS/`postgresql.conf` security settings, existing RLS, column grants, encryption usage, audit configuration, and network exposure. Record each gap against a threat.
3. Design the role and grant model: a role hierarchy (login roles vs group roles), least-privilege grants per component, app roles that are not owners, revoked `PUBLIC`, and a privileged/break-glass role with audit. Map each grant to the authorization model.
4. Design tenant isolation: where the classification requires engine-enforced isolation, author RLS policies (`FORCE ROW LEVEL SECURITY`, per-tenant `USING`/`WITH CHECK` predicates, the session/role mechanism that carries tenant identity safely) and state the bypass risks (table owner, `BYPASSRLS`).
5. Design PII/column protection: column-level `REVOKE`/`GRANT` for restricted columns, view or masking strategy for analytic access, and column encryption posture — `pgcrypto` for application-tier-keyed columns vs substrate TDE for at-rest — each with its stated threat model and key-custody implication.
6. Design connection security: enforce TLS (server `ssl=on`, modern version/cipher floor, client `verify-full` expectation), scram-sha-256, and a default-deny `pg_hba.conf` with explicit per-source/per-db/per-role rules; eliminate `trust` and password (md5) auth for production.
7. Design the audit posture: configure `pgaudit` (or substrate-native) for the security-relevant event classes from the threat model (DDL, GRANT/role changes, privileged reads on regulated tables, failed auth), define log routing, retention, and tamper-evidence per `observability-standards`, and explicitly exclude high-volume low-value events.
8. Design the secret and credential rotation posture: rotation owner and cadence per credential class, elimination of static long-lived superuser in app config, preference for short-lived/IAM auth where the substrate supports it, and confirmation that the backup/restore bootstrap path (from the backup skill) does not depend on an unrotated embedded secret.
9. Review network exposure: confirm private connectivity within the platform trust zone, justify and allowlist any public exception with TLS enforced, and flag any endpoint reachable outside the intended boundary. Consume the trust-zone definition from `infrastructure-platform`; do not redesign it.
10. Produce the hardening assessment: a threat → control coverage matrix (threat/boundary → control → enforced where → residual risk), the role/grant model, RLS policies, column-protection plan, connection-security settings, audit configuration, rotation posture, and the network-exposure finding. Report threats with no control as gaps and controls with no threat as removable.
11. Verify. Apply the model against a representative database and test enforcement: a non-privileged role cannot read restricted columns, a cross-tenant query returns zero rows under RLS, non-TLS connections are refused, and audited events appear in the configured sink. Capture the test evidence. If a representative environment is unavailable, document each unverified control as an explicit open risk — do not declare hardened on untested policy.

## Outputs

Required:

- `security-hardening.md`: threat → control coverage matrix, role/grant model, tenant-isolation (RLS) design, PII/column-protection design, connection-security settings, audit configuration, secret-rotation posture, and network-exposure findings.
- Role and grant DDL (or a precise change list) implementing least privilege, marked as a migration handoff to `postgres-schema-and-migration` where it alters schema-owned objects.
- RLS policy DDL and column GRANT/REVOKE statements, with the carrying mechanism for tenant identity.
- Connection-security configuration: `pg_hba.conf` rules, TLS and auth settings.

Conditional, when applicable:

- Column-encryption design (`pgcrypto`/TDE) with key-custody and threat-model statement.
- `pgaudit` configuration with event-class scoping and retention.
- ADR candidate(s) for unstated classification/isolation, encryption key-custody trade-offs, or justified public-exposure exceptions.

Output rules:

- Every control maps to a threat or boundary from `security-architecture.md`; unmapped controls are removed; unmitigated threats are reported as gaps.
- Tier-0/regulated multi-tenant isolation is engine-enforced (RLS), never application-only.
- DDL that alters schema-owned objects is handed off to `postgres-schema-and-migration` as a migration, not silently applied.
- Network trust zone is consumed from `infrastructure-platform`, not redesigned.

## Quality checks

- [ ] Threat model, authorization model, tenant-isolation requirement, and data classification are sourced from `security-architecture.md`/`data-architecture.md` (or an ADR candidate is raised).
- [ ] No role has unjustified `SUPERUSER`/`ALL`/ownership; `PUBLIC` is revoked unless explicitly justified; app roles are not table owners.
- [ ] Tier-0/regulated multi-tenant data is isolated with `FORCE ROW LEVEL SECURITY`, with the tenant-identity carrying mechanism stated and bypass risks named.
- [ ] Restricted/PII columns are protected with column grants and/or encryption; application-only enforcement is not relied on for tier-0.
- [ ] TLS is enforced (server + client `verify-full` expectation), scram-sha-256 is used, and `pg_hba.conf` is default-deny with no production `trust`/md5.
- [ ] `pgaudit` (or native) covers the threat-model event classes with routing, retention, and tamper-evidence; high-volume low-value events are excluded.
- [ ] Secret/credential rotation has an owner and cadence; no static long-lived superuser in app config; restore bootstrap does not embed an unrotated secret.
- [ ] Network exposure is reviewed; any public endpoint is justified, allowlisted, and TLS-enforced; trust zone is consumed from `infrastructure-platform`.
- [ ] A threat → control coverage matrix exists; unmapped controls removed, unmitigated threats reported as gaps.
- [ ] Enforcement is tested (restricted-column denial, cross-tenant zero-rows, non-TLS refusal, audit-event presence) or each unverified control is logged as an explicit open risk.
- [ ] Schema-owned DDL changes are handed off to `postgres-schema-and-migration`, not silently applied.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md).
- Related implementation skills: [`postgres-schema-and-migration`](../postgres-schema-and-migration/SKILL.md) (owns DDL/migration mechanics this skill hands off), [`postgres-backup-and-operational-readiness`](../postgres-backup-and-operational-readiness/SKILL.md) (backup-secret custody overlap), [`postgres-replication-and-ha-readiness`](../postgres-replication-and-ha-readiness/SKILL.md) (replication-user privilege scope).
- Compatible patterns: [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md), [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`modular-monolith`](../../../../../architecture-patterns/modular-monolith/README.md).
