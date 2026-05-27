---
name: terraform-module-and-repository-scaffold
description: Use when creating, restructuring, or reviewing the Terraform repository and module layout after infrastructure-platform has decided the environment ladder, module boundaries, and blast-radius tiers. Produces the repo structure (root + modules/ + environments/<env>/), provider and required_version constraints, module input/output and documentation conventions, an examples/ directory for consumers, and code-owner and review rules tied to environment and blast-radius tier. Do not use for state backend or secret handling, plan/policy gates, apply and promotion orchestration, or module-registry supply chain; use the other terraform archetype skills instead.
---

# Terraform Module and Repository Scaffold

## When to use

Invoke when starting a new Terraform repository, standardizing an existing one's layout, splitting a monolithic configuration into modules, or auditing module/repo structure and review rules before scaling the team or environments.

Do not use for: remote state and secret handling (use `terraform-state-and-secret-management`), pre-merge plan/policy gates (use `terraform-plan-gate-and-policy-as-code`), apply/promotion mechanics (use `terraform-apply-and-promotion-mechanics`), or module registry/versioning/supply chain (use `terraform-module-reuse-and-supply-chain`).

## Inputs

Required:

- Approved `infrastructure-platform.md` declaring the environment ladder, module boundaries, blast-radius tiers, and target cloud(s).
- Approved `architecture/operations` decisions on review/ownership posture and promotion-gate expectations (consumed for code-owner rules; gate mechanics are downstream).

Optional:

- Existing Terraform code or repository.
- Team topology (who owns which modules/environments).
- Cloud provider(s) and required provider set.
- Monorepo vs multi-repo preference.
- Naming conventions already in force.

## Operating rules

- Consume the boundaries; do not invent them. Module boundaries, the environment ladder, and blast-radius tiers come from `infrastructure-platform.md`. If a boundary or the ladder is unstated, pause and raise an ADR candidate rather than guessing the decomposition.
- Modules encapsulate a boundary, not a resource. A module wraps a meaningful unit from the architecture (a network, a service runtime, a data store), exposes typed inputs and outputs, and hides internal resources. One-resource passthrough modules are rejected.
- Environment composition is explicit and isolated. `environments/<env>/` directories compose modules; environments do not share state files or reach into each other. The env-per-directory layout is the default; `terraform workspace` for envs is an ADR-justified exception (state-strategy specifics are the state skill's concern, but the directory layout is decided here).
- Pin everything that affects the plan: `required_version` for Terraform/OpenTofu and `required_providers` with version constraints in every root and module. Unpinned providers are rejected.
- Every module is documented and exemplified: a `README.md` (purpose, inputs, outputs, example) and an `examples/` directory that `terraform validate`s. An undocumented module is incomplete.
- Inputs and outputs follow conventions: typed variables with descriptions and (where safe) defaults, validation blocks for constrained inputs, outputs named for consumers, and no implicit reliance on provider defaults that the architecture cares about.
- Review and ownership scale with blast radius. CODEOWNERS maps modules and environments to owners; higher-tier environments/modules require stricter reviewer rules. The mapping is defined here; gate enforcement is the plan-gate skill.
- This skill defines structure and conventions only. It does not configure the state backend, write policy-as-code, orchestrate apply, or set up the module registry — each is a named handoff.
- Scaffolding must `terraform init` and `terraform validate` cleanly (and `fmt`), with a no-op `plan` against the examples where feasible, before it is done.

## Output contract

The repository and module scaffold MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — environment ladder reflected in the directory structure; environments are reproducible and isolated.
- [security-standards](../../../../../standards/security-standards/README.md) — no secrets or backend credentials in scaffolded files; `.tfvars` with secrets are not committed (enforced structurally; mechanics are the state skill).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — module, resource, variable, and directory naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — blast-radius/tier classification drives CODEOWNERS strictness and environment separation.

Upstream contract: `infrastructure-platform.md` is the source of truth for module boundaries, the environment ladder, and blast-radius tiers; `architecture/operations` is the source of truth for ownership/review posture. If a needed decision is unstated, pause and raise an ADR candidate. State, gates, apply, and registry are explicit downstream handoffs.

## Process

1. Load `infrastructure-platform.md` (module boundaries, env ladder, blast-radius tiers, target clouds) and `architecture/operations` (review/ownership posture). If a boundary or the ladder is missing, pause and raise an ADR candidate.
2. Inventory existing code (if any): current layout, module granularity, version pinning, documentation, and ownership. Record gaps against the architecture boundaries.
3. Design the repository layout: `modules/<module>/`, `environments/<env>/` per the ladder, shared `examples/`, and supporting directories. State monorepo vs multi-repo and justify if it diverges from the architecture.
4. Decompose into modules along the architecture boundaries: one module per meaningful boundary, each with `main.tf`/`variables.tf`/`outputs.tf`/`versions.tf`/`README.md`. Reject single-resource passthrough modules and god-modules.
5. Define version discipline: `required_version` and `required_providers` with constraints in every root and module; a documented upgrade policy. (Lockfile/registry handling is the supply-chain skill — note the handoff.)
6. Define input/output conventions: typed variables with `description`, `validation` blocks for constrained inputs, safe defaults, consumer-oriented outputs, and an explicit rule against leaking provider defaults the architecture depends on.
7. Author per-module `README.md` and an `examples/` directory that `terraform validate`s for each module, so consumers have a working reference.
8. Define CODEOWNERS and review rules: map modules and environments to owners; stricter required-review for higher blast-radius tiers (definition only — enforcement is the plan-gate skill).
9. State downstream handoffs explicitly: backend/state/secrets → `terraform-state-and-secret-management`; pre-merge gates/policy → `terraform-plan-gate-and-policy-as-code`; apply/promotion → `terraform-apply-and-promotion-mechanics`; registry/versioning/provenance → `terraform-module-reuse-and-supply-chain`.
10. Verify: `terraform fmt -check`, `terraform init` (backend not configured here — use `-backend=false`), and `terraform validate` on every module and example clean. Document any skipped check rather than declaring success silently.
11. Validate against [deployment-standards](../../../../../standards/deployment-standards/README.md), [security-standards](../../../../../standards/security-standards/README.md), [naming-conventions](../../../../../standards/naming-conventions/README.md), and [architecture-schema](../../../../../standards/architecture-schema/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Repository layout: `modules/`, `environments/<env>/` per the ladder, `examples/`, and supporting structure.
- One Terraform module per architecture boundary, each with `main`/`variables`/`outputs`/`versions`/`README`.
- `required_version` + pinned `required_providers` in every root and module.
- Input/output conventions applied (typed, described, validated, consumer-named).
- `examples/` per module that `terraform validate`s.
- `CODEOWNERS` and review-rule definitions tiered by blast radius.
- Explicit downstream-handoff list.

Output rules:

- Functional scaffold, not placeholder `.tf` stubs.
- No single-resource passthrough modules or god-modules.
- No secrets, backend credentials, or committed secret `.tfvars`.
- Structure and conventions only; state/gates/apply/registry are handoffs, not implemented here.

## Quality checks

- [ ] Module boundaries and the environment ladder are sourced from `infrastructure-platform.md` (or an ADR candidate is raised).
- [ ] Repository uses `modules/` + `environments/<env>/` per the ladder; environments are isolated (no shared state directory, no cross-reach).
- [ ] Every module wraps an architecture boundary with typed inputs/outputs; no single-resource passthrough or god-modules.
- [ ] Every root and module pins `required_version` and `required_providers`.
- [ ] Every module has a `README.md` and an `examples/` entry that `terraform validate`s.
- [ ] Variables are typed and described, with `validation` blocks for constrained inputs; outputs are consumer-named.
- [ ] `CODEOWNERS` maps modules/environments to owners with stricter rules for higher blast-radius tiers.
- [ ] `terraform fmt -check`, `init -backend=false`, and `validate` pass for every module and example (or the gap is documented).
- [ ] State, gates, apply, and registry are named downstream handoffs, not implemented here.

## References

- Upstream: [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md), [`architecture/operations`](../../../../architecture/operations/SKILL.md).
- Related terraform archetype skills (downstream): [`terraform-state-and-secret-management`](../terraform-state-and-secret-management/SKILL.md), [`terraform-plan-gate-and-policy-as-code`](../terraform-plan-gate-and-policy-as-code/SKILL.md), [`terraform-apply-and-promotion-mechanics`](../terraform-apply-and-promotion-mechanics/SKILL.md), [`terraform-module-reuse-and-supply-chain`](../terraform-module-reuse-and-supply-chain/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`modular-monolith`](../../../../../architecture-patterns/modular-monolith/README.md), [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md).
