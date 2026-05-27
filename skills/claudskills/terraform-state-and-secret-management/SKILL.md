---
name: terraform-state-and-secret-management
description: Use when designing, reviewing, or hardening Terraform remote state and secret handling after the repo/module scaffold exists and security and infrastructure-platform have decided the state-isolation and secret posture. Produces remote state backend selection (S3+DynamoDB / GCS / Azure Storage / Terraform Cloud), state encryption at rest, state locking, workspace-vs-directory state isolation strategy, sensitive-output discipline, secret references to a secret manager instead of plaintext, and a no-committed-secrets posture. Do not use for repo/module layout, plan/policy gates, apply and promotion mechanics, or module registry/supply chain; use the other terraform archetype skills instead.
---

# Terraform State and Secret Management

## When to use

Invoke when configuring the remote state backend for a Terraform repository, restructuring state isolation across environments, or auditing/hardening state encryption, locking, and secret handling before the configuration manages real infrastructure.

Do not use for: repository/module structure (use `terraform-module-and-repository-scaffold`), pre-merge plan/policy gates (use `terraform-plan-gate-and-policy-as-code`), apply/promotion orchestration (use `terraform-apply-and-promotion-mechanics`), or module versioning/provenance (use `terraform-module-reuse-and-supply-chain`).

## Inputs

Required:

- An existing repo/module scaffold from `terraform-module-and-repository-scaffold` (provides the env-per-directory layout this skill backs with state).
- Approved `architecture/security` decisions on secret handling, state-at-rest encryption, and provider authentication posture.
- Approved `infrastructure-platform.md` decisions on environment isolation and the target cloud(s) (determines the backend choice).

Optional:

- Existing backend configuration and state files.
- The secret manager in use (AWS Secrets Manager / GCP Secret Manager / Azure Key Vault / Vault).
- Blast-radius tiers (drives how strictly state is isolated and access-controlled).
- Multi-cloud or multi-account constraints.
- Existing CI identity/OIDC setup (consumed; not configured here).

## Operating rules

- Consume the posture; do not invent it. State-isolation requirements and the secret posture come from `architecture/security` and `infrastructure-platform.md`. If the secret manager, encryption requirement, or isolation boundary is unstated, pause and raise an ADR candidate.
- Remote state is mandatory for any shared or production configuration. Local state for shared infra is a rejected design. The backend choice follows the target cloud and the platform decision, not preference.
- State is sensitive data. It is encrypted at rest, access-controlled to least privilege, never world-readable, and never committed to source. Treat the state bucket/store as a tier-0 asset.
- State is locked. Concurrent applies must be prevented (DynamoDB lock table for S3, native locking for GCS/Azure/Terraform Cloud). A backend without locking is rejected for shared use.
- State isolation matches the environment boundary from the scaffold. Each environment has its own state (separate backend key/prefix or workspace) so a non-prod apply can never mutate prod state. Env-per-directory with distinct state keys is the default; `terraform workspace` for environments is an ADR-justified exception.
- Secrets never live in plaintext in `.tf`, `.tfvars` committed to source, or unmarked outputs. Secret values are referenced from the secret manager (data source or injected variable); outputs carrying secrets are `sensitive = true`.
- Marking an output `sensitive = true` hides it from CLI output but it is still stored in plaintext in state — so state encryption and access control are the real control. State the boundary; do not present `sensitive` as encryption.
- Provider credentials use the OIDC/short-lived path defined by the CI identity setup (consumed, not configured here). Long-lived static keys in the backend or provider config are an ADR-justified exception only.
- This skill owns backend + state isolation + secret-reference discipline. It does not write policy-as-code, gate plans, orchestrate apply, or manage the module registry — each is a named handoff.
- A backend change is a state-migration event: any reconfiguration documents the `terraform init -migrate-state` (or `state mv`/pull-push) procedure and a rollback, and is treated as a tier-appropriate change.

## Output contract

State and secret handling MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — state encrypted at rest, least-privilege access to the state store, no plaintext secrets in code/state/outputs, OIDC/short-lived provider auth.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — per-environment isolated state; backend reproducible via IaC/config, not click-ops.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — backend bucket/key/prefix and lock-table naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives state access strictness and isolation granularity.

Upstream contract: `architecture/security` is the source of truth for secret handling, encryption, and provider auth; `infrastructure-platform.md` is the source of truth for environment isolation and target cloud. If a needed decision is unstated, pause and raise an ADR candidate. Repo layout, gates, apply, and registry are downstream/upstream handoffs, not implemented here.

## Process

1. Load `architecture/security` (secret posture, encryption, provider auth) and `infrastructure-platform.md` (env isolation, target cloud). Confirm the scaffold's env-per-directory layout exists. If a required decision is missing, pause and raise an ADR candidate.
2. Inventory current state handling (if any): backend type, encryption, locking, access policy, state isolation per env, and any plaintext secrets in code/`.tfvars`/outputs/state. Record each gap against a security requirement.
3. Select the remote backend per the target cloud and platform decision: S3 + DynamoDB lock, GCS, Azure Storage, or Terraform Cloud. Justify the choice against the architecture; reject local state for shared infra.
4. Configure state-at-rest encryption and access control: bucket/store encryption (KMS/CMK where the security posture requires), least-privilege access policy, block public access, versioning on the state store, and tier-0 treatment.
5. Configure state locking: DynamoDB lock table (S3) or native locking (GCS/Azure/Terraform Cloud), with a documented lock-recovery note (handoff to apply skill for the full runbook).
6. Define state isolation: per-environment backend key/prefix (or workspace, if ADR-justified) so environments cannot cross-mutate; map each `environments/<env>/` directory to its distinct state location.
7. Define secret-reference discipline: secret values pulled from the secret manager via data sources or injected variables; no secrets in committed `.tfvars`; `sensitive = true` on secret-bearing variables/outputs; document that `sensitive` is not encryption and state access control is the real boundary.
8. Confirm provider auth uses the OIDC/short-lived path from the CI identity setup; flag any long-lived static credential as an ADR-required exception.
9. Document the backend-migration procedure: `terraform init -migrate-state` (or `state mv`/pull-push) steps, verification, and rollback, treated per blast-radius tier.
10. State downstream/related handoffs: repo layout ← `terraform-module-and-repository-scaffold`; policy/secret-scanning gates → `terraform-plan-gate-and-policy-as-code`; lock-recovery/partial-apply runbook → `terraform-apply-and-promotion-mechanics`; module registry → `terraform-module-reuse-and-supply-chain`.
11. Verify: `terraform init` against the configured backend succeeds, a lock is acquired/released on a no-op plan, state is confirmed encrypted and access-restricted, and a secret scan of the tree finds no plaintext secrets. Document any check that cannot run in the environment.
12. Validate against [security-standards](../../../../../standards/security-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), [naming-conventions](../../../../../standards/naming-conventions/README.md), and [architecture-schema](../../../../../standards/architecture-schema/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Backend configuration per environment (S3+DynamoDB / GCS / Azure / Terraform Cloud) with distinct state per environment.
- State-at-rest encryption + least-privilege access policy + versioning + public-access block on the state store.
- State locking configuration with a lock-recovery note.
- Secret-reference pattern: secret-manager data sources/injected variables, `sensitive = true` discipline, and the explicit statement that `sensitive` ≠ encryption.
- Backend-migration procedure with rollback.
- Downstream/related handoff list.

Output rules:

- Functional backend/config, not placeholder.
- No local state for shared infra; no plaintext secrets in code, committed `.tfvars`, or unmarked outputs.
- State store treated as tier-0 (encrypted, access-controlled, versioned, non-public).
- Policy gates, apply orchestration, and registry are handoffs, not implemented here.

## Quality checks

- [ ] Secret posture, encryption, and provider auth are sourced from `architecture/security`; isolation and target cloud from `infrastructure-platform.md` (or an ADR candidate is raised).
- [ ] Remote backend is configured for all shared/production configs; no local state for shared infra.
- [ ] State is encrypted at rest with least-privilege access, versioning, and public access blocked.
- [ ] State locking is configured (DynamoDB or native) with a lock-recovery note.
- [ ] Each environment has isolated state; a non-prod apply cannot mutate prod state.
- [ ] No plaintext secrets in `.tf`, committed `.tfvars`, outputs, or anywhere in source; secrets are secret-manager references.
- [ ] Secret-bearing variables/outputs are `sensitive = true`, with an explicit note that this is not encryption and state access control is the real boundary.
- [ ] Provider auth uses OIDC/short-lived credentials; any long-lived key is an ADR-justified exception.
- [ ] A backend-migration procedure with rollback is documented.
- [ ] `terraform init` against the backend succeeds and locking is exercised (or the gap is documented).
- [ ] Repo layout, gates, apply, and registry are named handoffs, not implemented here.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md).
- Builds on: [`terraform-module-and-repository-scaffold`](../terraform-module-and-repository-scaffold/SKILL.md) (env-per-directory layout backed by state here).
- Related terraform archetype skills: [`terraform-plan-gate-and-policy-as-code`](../terraform-plan-gate-and-policy-as-code/SKILL.md) (secret-scanning/policy gates), [`terraform-apply-and-promotion-mechanics`](../terraform-apply-and-promotion-mechanics/SKILL.md) (lock-recovery/partial-apply runbook), [`terraform-module-reuse-and-supply-chain`](../terraform-module-reuse-and-supply-chain/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md).
