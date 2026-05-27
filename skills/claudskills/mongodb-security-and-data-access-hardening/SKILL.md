---
name: mongodb-security-and-data-access-hardening
description: Use when hardening MongoDB authentication, authorization, encryption, and audit after the data model and PII classification exist and security and data-architecture have set the auth model and PII posture. Produces the authentication mechanism (SCRAM / x.509 / LDAP / Kerberos), least-privilege RBAC roles (built-in vs custom), field-level redaction posture, client-side field-level encryption for PII, TLS for client and intra-cluster traffic, IP allowlists, and audit-log configuration. Do not use for document modeling, query tuning, replica topology, backup procedure, or KMS/secret-store provisioning; use the other Family B archetype skills (KMS provisioning is infrastructure).
---

# MongoDB Security and Data Access Hardening

## When to use

Invoke when establishing the security posture for a production MongoDB deployment, enforcing PII protection at the engine, restructuring roles and grants, adding client-side field-level encryption, or auditing an inherited deployment for auth/RBAC/encryption/audit gaps.

Do not use for: document modeling or migrations (use `mongodb-data-model-and-migration`); query/index tuning (use `mongodb-indexing-and-query-optimization`); replica-set topology (use `mongodb-replication-and-ha-readiness`); backup/restore procedure (use `mongodb-backup-and-operational-readiness` — this skill owns the backup-artifact key/access *model* it consumes); KMS / secret-store provisioning (infrastructure layer — this skill wires CSFLE to the KMS, it does not stand the KMS up).

## Inputs

Required:

- An existing data model with PII-tagged fields from `mongodb-data-model-and-migration` and the collection PII classification from `data-architecture.md`.
- Approved `architecture/security` decisions on the authentication model, encryption posture, and PII classification, or explicit confirmation they are intentionally deferred.

Optional:

- The workload/data tier from `architecture-schema` (drives whether engine-enforced PII protection is mandatory).
- The identity provider for LDAP/Kerberos/x.509 federation.
- The KMS/key provider available for CSFLE and at-rest encryption (consumed, not provisioned here).
- Compliance regime (GDPR/HIPAA/PCI) driving redaction and audit scope.
- The replica-set internal-auth requirement named by `mongodb-replication-and-ha-readiness`.

## Operating rules

- PII is enforced at the engine, not in the application — for tier-0 data this is non-negotiable. Where MongoDB supports field-level redaction, CSFLE, or role-scoped views, the protection is engine-enforced. "The application filters it" is rejected for tier-0 PII (a locked data-tier constraint).
- Consume `architecture/security` and `data-architecture.md`; do not invent decisions. The auth model, encryption posture, and PII classification are upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Harden the engine; do not reclassify the data. Which fields/collections are PII is owned by `data-architecture.md` / `mongodb-data-model-and-migration`. This skill *enforces* the classification; a mis- or unclassified field is a finding handed back, not classified here.
- Authentication is always on; the mechanism matches the identity model. SCRAM at minimum; x.509/LDAP/Kerberos where the identity model requires. An auth-disabled deployment, or an internet-reachable deployment without auth, is rejected outright.
- Authorization is least-privilege and role-based. Built-in roles only where they fit exactly; custom roles scoped to the minimal actions and resources otherwise. No application connecting as a cluster-admin or `root`-equivalent; one role per access pattern, not one superuser shared.
- The internal-auth requirement from replication is honored. Replica-set members authenticate via keyfile or x.509 and member traffic is TLS — this skill specifies the mechanism that `mongodb-replication-and-ha-readiness` named as required.
- Encryption in transit is mandatory. TLS for client connections and intra-cluster traffic; plaintext listeners are rejected. Certificate provenance and rotation are stated.
- CSFLE protects the PII the classification marks. Client-side field-level encryption (or queryable encryption where the access pattern needs it) for fields the classification marks sensitive, keyed via the provisioned KMS. The KMS itself is an infrastructure handoff; the field→key mapping and the encrypted-field schema are owned here.
- Network exposure is minimized. Bind to private interfaces, IP allowlists/security-group posture stated, no `0.0.0.0` bind on an internet-reachable host. Network reachability that the trust zones do not justify is a finding.
- Audit logging captures the security-relevant events. Authentication failures, role/grant changes, privileged operations, and access to PII collections are audited to a tamper-resistant destination, with no PII or secret values written into the audit stream itself.
- This skill owns auth + RBAC + encryption + redaction + audit. Modeling, query tuning, topology, backup procedure, and KMS/secret-store provisioning are named handoffs; it provides the backup-artifact key/access model that `mongodb-backup-and-operational-readiness` consumes.
- A posture whose access controls have not been negative-tested (an unauthorized principal is actually denied; a PII field is actually unreadable without the key) is not done.

## Output contract

The security and data-access hardening MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — auth always on, least-privilege RBAC, TLS in transit, engine-enforced PII protection, no secrets in audit/logs, key custody via the provisioned KMS.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — PII classification ownership: this skill enforces, it does not reclassify; each collection's access is scoped to its owning component.
- [observability-standards](../../../../../standards/observability-standards/README.md) — auth-failure, grant-change, and PII-access audit signals exposed to a tamper-resistant destination.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — roles, TLS config, and audit config reproducible from configuration, not click-ops.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — role and audit-filter naming.

Upstream contract: `architecture/security` is the source of truth for the auth model and encryption posture; `data-architecture.md` is the source of truth for PII classification. If a needed decision is missing, pause and raise an ADR candidate.

## Progressive references

- Read `references/mongodb-security-playbook.md` when hardening any owned area or checking the anti-pattern list.
- Read `references/mongodb-security-quality-rubric.md` before declaring the posture complete.
- Use `assets/mongodb-security.template.md` as the auth / RBAC / TLS / CSFLE / audit pattern reference.

## Process

1. Gather context: load `architecture/security` (auth model, encryption posture) and `data-architecture.md` (PII classification). Pull the PII-tagged fields/collections from `mongodb-data-model-and-migration` and the internal-auth requirement from `mongodb-replication-and-ha-readiness`. Resolve the tier from `architecture-schema`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Set the authentication mechanism: SCRAM baseline; x.509/LDAP/Kerberos per the identity model; confirm auth is enabled and no unauthenticated reachable path exists.
3. Design RBAC: one role per access pattern, least-privilege actions/resources, built-in roles only where they fit exactly, custom roles otherwise; no shared superuser; application principals scoped to their collections.
4. Specify internal auth: keyfile or x.509 for replica-set members plus member TLS, satisfying the requirement named by `mongodb-replication-and-ha-readiness`.
5. Configure TLS: client and intra-cluster TLS, certificate provenance and rotation, plaintext listeners disabled.
6. Design CSFLE: map each classification-marked PII field to its encryption key and the queryable/standard encryption mode the access pattern needs; reference the provisioned KMS (provisioning is an infrastructure handoff).
7. Set field-level redaction / role-scoped views for PII that must be visible to some roles and not others.
8. Minimize network exposure: private bind, IP allowlist/security-group posture, no unjustified reachability.
9. Configure audit logging: auth failures, role/grant changes, privileged ops, PII-collection access to a tamper-resistant destination; verify no PII/secret values are written to the audit stream.
10. Provide the backup-artifact key/access model consumed by `mongodb-backup-and-operational-readiness`.
11. Negative-test: confirm an unauthorized principal is denied, an over-broad grant is absent, and a CSFLE-protected field is unreadable without the key; capture results. Document any check that cannot run.
12. Produce `security-hardening.md` (auth mechanism, role/grant matrix, TLS posture, CSFLE field→key map, redaction/view posture, network exposure, audit configuration, negative-test results, backup-artifact key model) plus the named handoff list. Validate against security-, architecture-schema, observability-, deployment-standards, and naming-conventions. Revise until all pass or the gap is documented.

## Outputs

Required:

- Authentication mechanism with auth confirmed enabled and no unauthenticated reachable path.
- Least-privilege RBAC role/grant matrix (one role per access pattern; no shared superuser).
- Internal-auth specification (keyfile/x.509 + member TLS) satisfying the replication requirement.
- TLS posture (client + intra-cluster, cert provenance/rotation, no plaintext listener).
- CSFLE field→key map and encryption mode for classification-marked PII.
- Field-level redaction / role-scoped view posture.
- Network-exposure posture (private bind, allowlist).
- Audit-log configuration (events, destination, no-PII-in-audit verification).
- Backup-artifact key/access model for `mongodb-backup-and-operational-readiness`.
- Negative-test results and `security-hardening.md` plus the named handoff list.

Output rules:

- Reproducible auth/TLS/role/audit configuration — not click-ops, not prose-only.
- Auth always on; no internet-reachable unauthenticated path; tier-0 PII engine-enforced.
- The data classification is enforced, not authored here; KMS/secret-store provisioning is a named handoff.

## Quality checks

- [ ] Auth model and encryption posture are sourced from `architecture/security`; PII classification from `data-architecture.md` (or an ADR candidate is raised).
- [ ] PII classification is consumed from `mongodb-data-model-and-migration` / `data-architecture.md`; a mis/unclassified field is a finding handed back, not classified here.
- [ ] Authentication is enabled; the mechanism matches the identity model; no unauthenticated reachable path exists.
- [ ] RBAC is least-privilege: one role per access pattern, no shared superuser, application principals scoped to their collections.
- [ ] Replica-set internal auth (keyfile/x.509) and member TLS satisfy the requirement named by `mongodb-replication-and-ha-readiness`.
- [ ] TLS is enforced for client and intra-cluster traffic; no plaintext listener; cert provenance/rotation stated.
- [ ] Every classification-marked PII field has a CSFLE key mapping and an encryption mode appropriate to its access pattern.
- [ ] Role-scoped redaction/views exist where PII must be visible to some roles and not others.
- [ ] Network exposure is minimized (private bind, IP allowlist); unjustified reachability is a finding.
- [ ] Audit logging covers auth failures, grant changes, privileged ops, and PII-collection access to a tamper-resistant destination, with no PII/secrets in the audit stream.
- [ ] Access controls were negative-tested (unauthorized denied; PII unreadable without the key), or the gap is documented.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md).
- Builds on: [`mongodb-data-model-and-migration`](../mongodb-data-model-and-migration/SKILL.md) (PII-tagged fields), [`mongodb-replication-and-ha-readiness`](../mongodb-replication-and-ha-readiness/SKILL.md) (names the internal-auth requirement satisfied here).
- Consumed by: [`mongodb-backup-and-operational-readiness`](../mongodb-backup-and-operational-readiness/SKILL.md) (backup-artifact key/access model).
- Related: `mongodb-indexing-and-query-optimization`. KMS/secret-store provisioning is the infrastructure layer's ownership.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
