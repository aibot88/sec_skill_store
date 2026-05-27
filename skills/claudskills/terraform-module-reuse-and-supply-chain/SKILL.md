---
name: terraform-module-reuse-and-supply-chain
description: Use when designing, reviewing, or hardening Terraform module reuse and dependency supply chain after the repo scaffold exists and security and operations have decided versioning and provenance requirements. Produces a versioned module registry strategy (private TFC registry or Git tags), semantic versioning of modules, provider and module dependency pinning in consumers, provenance review for community modules, an SBOM-equivalent for the module dependency tree, and a deprecation policy for breaking changes. Do not use for repo/module layout, state/secret backend, plan/policy gates, or apply and promotion mechanics; use the other terraform archetype skills instead.
---

# Terraform Module Reuse and Supply Chain

## When to use

Invoke when establishing how Terraform modules are versioned, published, consumed, and trusted; when introducing a module registry; or when auditing/hardening provider and module dependency provenance before reuse scales across teams.

Do not use for: repo/module structure (use `terraform-module-and-repository-scaffold`), state backend/secret handling (use `terraform-state-and-secret-management`), pre-merge plan/policy gates (use `terraform-plan-gate-and-policy-as-code`), or apply/promotion orchestration (use `terraform-apply-and-promotion-mechanics`).

## Inputs

Required:

- An existing repo/module scaffold (from `terraform-module-and-repository-scaffold`) defining module boundaries and structure.
- Approved `architecture/security` decisions on dependency provenance, allowed sources, and supply-chain requirements.
- Approved `architecture/operations` decisions on versioning, deprecation, and change-communication expectations.

Optional:

- Existing module registry (Terraform Cloud private registry, internal Git, public Registry usage).
- Current provider/module pinning state in consumers and lockfiles.
- Inventory of community/third-party modules in use.
- Compliance regime mandating provenance/SBOM.

## Operating rules

- Consume the posture; do not invent it. Provenance/allowed-source rules come from `architecture/security`; versioning/deprecation expectations come from `architecture/operations`. If a source-trust rule or the versioning scheme is unstated, pause and raise an ADR candidate.
- Reusable modules are versioned artifacts, not branch references. Modules are consumed at an immutable version (registry version or Git tag/commit SHA), never a moving `main`/branch. Floating module sources are rejected.
- Modules follow semantic versioning. `MAJOR.MINOR.PATCH` with a documented contract: breaking input/output/behavior changes are MAJOR. Version bumps that misrepresent the change are a defect.
- Consumers pin everything. Module versions and provider versions are pinned in consumers; the dependency lockfile (`.terraform.lock.hcl`) is committed and reviewed. Unpinned or lockfile-absent consumers are rejected.
- Provenance is required for external code. Community/public modules and providers are reviewed and pinned to a verified version/SHA; prefer mirrored/vendored or registry-proxied sources where the security posture requires. "Trusted because popular" is not provenance.
- The dependency tree is enumerable. Produce an SBOM-equivalent: the full module + provider dependency graph with sources and pinned versions, regenerable and reviewable. An opaque transitive tree is rejected for tier-0 infra.
- Breaking changes have a deprecation path. A MAJOR release documents what broke, the migration, and a deprecation window; consumers are notified per the operations change-communication expectation. Silent breaking releases are rejected.
- Supply-chain integrity is preventive, not reactive. Pinning, provenance, and SBOM are required outputs here; this complements (does not replace) the plan-gate skill's policy scanning and the state skill's secret discipline — name the boundary.
- This skill owns module versioning, registry strategy, consumer pinning, provenance, SBOM-equivalent, and deprecation policy. It does not author module structure, configure state, gate plans, or orchestrate apply — each is a named handoff.

## Output contract

Module reuse and supply chain MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — pinned versions/SHAs, provenance review for external modules/providers, SBOM-equivalent for the dependency tree, committed lockfile.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — modules consumed at immutable versions; reproducible builds from pinned dependencies.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — module name, version tag, and registry-namespace conventions.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives provenance strictness and allowed sources.

Upstream contract: `architecture/security` is the source of truth for provenance/allowed-source rules and supply-chain requirements; `architecture/operations` is the source of truth for versioning/deprecation/change-communication. If a needed decision is unstated, pause and raise an ADR candidate. Scaffold/state/gate/apply are inputs or sibling handoffs, not implemented here.

## Process

1. Load `architecture/security` (provenance, allowed sources, supply-chain requirements) and `architecture/operations` (versioning, deprecation, change communication). Confirm the scaffold's module boundaries exist. If a source-trust rule or versioning scheme is missing, pause and raise an ADR candidate.
2. Inventory current reuse posture: how modules are sourced (branch vs tag vs registry), provider/module pinning, lockfile presence, community modules in use, and any deprecation practice. Record gaps against the security/operations requirements.
3. Define the registry strategy: private Terraform Cloud registry, internal Git with semver tags, or registry proxy/mirror — chosen per the security posture and team scale. Reject branch-reference consumption.
4. Define module semantic versioning: the `MAJOR.MINOR.PATCH` contract, what constitutes a breaking change (input/output removal or type change, behavior change, provider-constraint widening), and the tagging/release process.
5. Define consumer pinning rules: exact/constrained module versions, pinned `required_providers`, and a committed, reviewed `.terraform.lock.hcl` (including multi-platform hashes where teams differ). State the upgrade workflow.
6. Define provenance for external dependencies: review and pin community modules/providers to verified versions/SHAs; specify mirroring/vendoring or registry-proxy where the security posture requires; document the trust criteria.
7. Produce the SBOM-equivalent: the enumerable module + provider dependency graph with sources and pinned versions, the command/process to regenerate it, and the review cadence.
8. Define the deprecation policy: how a MAJOR/breaking release is documented (changelog, migration notes), the deprecation window, and how consumers are notified per the operations change-communication expectation.
9. State the supply-chain boundary: pinning/provenance/SBOM here complement the plan-gate skill's policy/SCA scanning and the state skill's secret discipline; name what each owns.
10. Name handoffs: module structure ← `terraform-module-and-repository-scaffold`; state ← state skill; policy/SCA scan ← `terraform-plan-gate-and-policy-as-code`; apply/promotion ← `terraform-apply-and-promotion-mechanics`.
11. Verify: confirm a consumer resolves modules/providers only at pinned immutable versions, the lockfile is committed and consistent, the SBOM-equivalent regenerates and matches the lockfile, and a sample community module has a recorded provenance review. Document any check that cannot run.
12. Validate against [security-standards](../../../../../standards/security-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), [naming-conventions](../../../../../standards/naming-conventions/README.md), and [architecture-schema](../../../../../standards/architecture-schema/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Module registry strategy (private TFC registry / internal Git semver tags / proxy) with the no-branch-reference rule.
- Semantic-versioning contract for modules (breaking-change definition + release/tagging process).
- Consumer pinning rules: pinned module + provider versions and a committed, reviewed `.terraform.lock.hcl`.
- Provenance procedure for community/external modules and providers (trust criteria + pinning/mirroring).
- SBOM-equivalent of the module + provider dependency tree with a regeneration process and review cadence.
- Deprecation policy for breaking changes (documentation, window, consumer notification).
- Handoff list.

Output rules:

- Modules are consumed at immutable versions; floating branch references are not acceptable.
- Lockfile is committed and reviewed; providers and modules are pinned in consumers.
- External dependencies have recorded provenance; "popular = trusted" is not provenance.
- Policy scanning, state, structure, and apply are handoffs, not implemented here.

## Quality checks

- [ ] Provenance/allowed-source rules sourced from `architecture/security`; versioning/deprecation from `architecture/operations` (or an ADR candidate is raised).
- [ ] A registry strategy is defined; modules are consumed at immutable versions (registry version or tag/SHA), never a branch.
- [ ] Module semantic-versioning contract defines what constitutes a breaking (MAJOR) change.
- [ ] Consumers pin module and provider versions; `.terraform.lock.hcl` is committed and reviewed.
- [ ] Community/external modules and providers have a recorded provenance review and are pinned to verified versions/SHAs.
- [ ] An SBOM-equivalent of the module + provider dependency tree exists, regenerates, and matches the lockfile.
- [ ] A deprecation policy documents breaking changes, the window, and consumer notification per operations.
- [ ] Provenance strictness and allowed sources scale with blast-radius tier (`architecture-schema`).
- [ ] The supply-chain boundary vs the plan-gate SCA scan and state secret discipline is stated.
- [ ] Module structure, state, gate, and apply are named handoffs, not implemented here.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/operations`](../../../../architecture/operations/SKILL.md).
- Builds on: [`terraform-module-and-repository-scaffold`](../terraform-module-and-repository-scaffold/SKILL.md) (module boundaries/structure).
- Related terraform archetype skills: [`terraform-plan-gate-and-policy-as-code`](../terraform-plan-gate-and-policy-as-code/SKILL.md) (policy/SCA scan boundary), [`terraform-state-and-secret-management`](../terraform-state-and-secret-management/SKILL.md), [`terraform-apply-and-promotion-mechanics`](../terraform-apply-and-promotion-mechanics/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md).
