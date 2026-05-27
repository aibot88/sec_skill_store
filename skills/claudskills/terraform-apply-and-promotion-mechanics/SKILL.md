---
name: terraform-apply-and-promotion-mechanics
description: Use when designing, reviewing, or hardening Terraform apply orchestration and environment promotion after the gate exists and infrastructure-platform and reliability have decided the environment ladder, approval model, and rollback expectations. Produces apply orchestration across the env ladder, manual-vs-auto-apply policy per environment, blast-radius-controlled apply discipline (targeted apply, refresh-only), a rollback procedure, a drift-remediation playbook, and runbook inputs for partial-apply failures and lock recovery. Do not use for repo/module layout, state/secret backend, pre-merge plan/policy gates, or module registry/supply chain; use the other terraform archetype skills instead.
---

# Terraform Apply and Promotion Mechanics

## When to use

Invoke when defining how Terraform changes are applied and promoted across environments, hardening the prod approval and rollback path, or producing runbook inputs for apply failures, drift, and lock recovery.

Do not use for: repo/module structure (use `terraform-module-and-repository-scaffold`), state backend/secret handling (use `terraform-state-and-secret-management`), pre-merge plan/policy gates (use `terraform-plan-gate-and-policy-as-code`), or module versioning/provenance (use `terraform-module-reuse-and-supply-chain`).

## Inputs

Required:

- An existing repo scaffold, configured state backend, and a blocking pre-merge gate (from the scaffold, state, and plan-gate skills).
- Approved `infrastructure-platform.md` decisions on the environment ladder (dev → staging → prod) and promotion model.
- Approved `architecture/reliability` decisions on rollback expectations, RTO for infra changes, and blast-radius tiers.

Optional:

- `architecture/operations` change-window and approval rules (consumed for prod approval gates).
- Existing CI/CD apply automation (apply is wired into it; CI identity/OIDC consumed, not configured here).
- Known incident history with apply failures, drift, or lock contention.
- Tier classification per environment/module.

## Operating rules

- Consume the ladder and rollback posture; do not invent them. The env promotion ladder comes from `infrastructure-platform.md`; rollback expectations and RTO come from `architecture/reliability`. If the approval model or rollback expectation is unstated, pause and raise an ADR candidate.
- Promotion is one direction along the ladder, same artifact/config. A change reaches prod only after succeeding in lower environments; prod is never applied from an unreviewed or divergent config. Skipping the ladder is an ADR-justified exception.
- Production apply is gated by explicit human approval. Auto-apply is acceptable for low-tier/non-prod; tier-0/prod requires a manual approval gate and change-window compliance. Auto-applying prod without approval is rejected.
- Apply uses the exact reviewed plan. Where the tooling supports it (saved plan file / Terraform Cloud run), apply the artifact the gate reviewed — not a fresh plan that could differ. State the mechanism.
- Blast radius is actively controlled. For high-tier changes, prefer narrowly-scoped applies, `-refresh-only` to reconcile drift separately from change, and avoid broad `-target` sprawl; document when `-target` is permitted and why it is a smell, not a default.
- Rollback is defined before apply, not improvised after. Every change states its rollback path: revert-commit-and-apply (default), or restore-prior-state-version where revert is unsafe (destroy/recreate, data resources). "Roll forward only" requires an ADR.
- "Terraform rollback" is not universal. Reverting config does not undo destroyed data or recreated immutable resources. The rollback procedure explicitly classifies which changes are safely revertible vs which need a forward-fix or state restore.
- Drift remediation is a defined playbook, not ad hoc. Consume drift signals from the plan-gate skill's scheduled detection; define who triages, the reconcile path (`refresh-only` + targeted apply vs config correction), and when drift is an incident.
- Partial-apply failure is expected and planned for. Provide runbook inputs: how to read partially-applied state, safe re-apply, lock recovery (`force-unlock` discipline with verification it is truly orphaned), and when to escalate.
- This skill owns apply orchestration, promotion, rollback, drift remediation, and apply-failure runbook inputs. It does not author the gate, configure the backend, or manage the registry — each is a named handoff. Runbook inputs are inputs (symptom → diagnostic → safe first action) handed to `architecture/operations` for operationalization.
- Apply runs with least privilege and short-lived credentials (OIDC, consumed). Long-lived apply credentials are an ADR-justified exception.

## Output contract

Apply and promotion mechanics MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — promotion ladder enforced, prod manual-approval gate, reviewed-plan applied, rollback artifact defined.
- [security-standards](../../../../../standards/security-standards/README.md) — apply uses least-privilege short-lived credentials; no secrets in apply logs; `force-unlock` is controlled.
- [observability-standards](../../../../../standards/observability-standards/README.md) — apply outcome, drift, and lock events are observable; drift remediation has an owner.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — environment, pipeline, and workspace naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives approval strictness, apply scoping, and rollback rigor.

Upstream contract: `infrastructure-platform.md` is the source of truth for the env ladder/promotion model; `architecture/reliability` is the source of truth for rollback expectations and RTO; `architecture/operations` for change windows/approvals. If a needed decision is unstated, pause and raise an ADR candidate. Scaffold/state/gate are inputs; the registry is a separate handoff.

## Process

1. Load `infrastructure-platform.md` (env ladder, promotion model), `architecture/reliability` (rollback, RTO, tiers), and `architecture/operations` (change windows, approvals). Confirm the scaffold, state backend, and gate exist. If the approval model or rollback expectation is missing, pause and raise an ADR candidate.
2. Inventory current apply automation (if any): how applies run per env, approval gates, rollback practice, drift handling, and lock-recovery practice. Record gaps against the reliability/operations requirements.
3. Define the promotion ladder mechanics: dev → staging → prod ordering, the gate each promotion must pass, the rule that prod uses only a config that succeeded lower, and how a change is tracked across environments.
4. Define manual-vs-auto-apply policy per environment/tier: auto-apply allowed for which low-tier envs; manual approval + change-window required for tier-0/prod. Wire the approval gate (CI environment protection / Terraform Cloud apply approval).
5. Ensure apply uses the reviewed plan: saved plan file or Terraform Cloud run artifact applied unchanged; document the mechanism and what happens if state moved since plan (re-plan + re-review).
6. Define blast-radius control: scoped applies for high-tier changes, `-refresh-only` to separate drift reconcile from change, an explicit policy on `-target` (permitted cases, why it is a smell), and any required staged/canary infra rollout.
7. Define the rollback procedure: classify changes as safely revertible (revert commit + apply) vs needing state restore or forward-fix (destroys, immutable recreates, data resources). Document the prior-state-version restore path and verification, mapped to the reliability RTO.
8. Define the drift-remediation playbook: consume scheduled drift signals from the plan-gate skill; triage owner, reconcile path (`refresh-only` + targeted apply vs config correction), and the threshold at which drift becomes an incident.
9. Produce apply-failure runbook inputs (symptom → first diagnostic → safe first action): partial apply (read tainted/partial state, safe re-apply), state lock stuck (`force-unlock` only after verifying the holder is orphaned), provider/auth failure, and post-failure escalation. Hand off to `architecture/operations` for operationalization.
10. Name handoffs: layout ← scaffold; backend/state ← state skill; drift detection + gate ← plan-gate skill; module provenance → `terraform-module-reuse-and-supply-chain`; runbook operationalization → `architecture/operations`.
11. Verify: rehearse a promotion (a change flows dev → staging → prod with the prod approval gate enforced), a rollback (revert + apply restores prior state for a revertible change; documented state-restore path for a non-revertible one), and a lock-recovery dry run. Document any rehearsal that cannot run in the environment as an explicit open risk.
12. Validate against [deployment-standards](../../../../../standards/deployment-standards/README.md), [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [naming-conventions](../../../../../standards/naming-conventions/README.md), and [architecture-schema](../../../../../standards/architecture-schema/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Promotion-ladder mechanics: env ordering, per-promotion gate, and same-config-up-the-ladder rule.
- Per-environment/tier manual-vs-auto-apply policy with the prod approval gate wired.
- Reviewed-plan-apply mechanism (saved plan / TFC run) with the stale-plan handling rule.
- Blast-radius control policy (scoped apply, `-refresh-only`, `-target` policy).
- Rollback procedure classifying revertible vs state-restore/forward-fix changes, mapped to RTO.
- Drift-remediation playbook (triage owner, reconcile path, incident threshold).
- Apply-failure runbook inputs (partial apply, lock recovery, auth failure) as symptom → diagnostic → safe first action.
- Handoff list.

Output rules:

- Prod is never auto-applied without approval; promotion is one-directional along the ladder.
- Apply uses the reviewed plan; a fresh divergent plan is not silently applied.
- Rollback is defined before apply; "roll forward only" requires an ADR.
- Runbook inputs are inputs, not full runbooks; gate/backend/registry are handoffs.

## Quality checks

- [ ] Env ladder/promotion model sourced from `infrastructure-platform.md`; rollback/RTO from `architecture/reliability`; approvals/windows from `architecture/operations` (or an ADR candidate is raised).
- [ ] Promotion is one-directional; prod uses only a config that succeeded in lower environments.
- [ ] Tier-0/prod apply requires a manual approval gate and change-window compliance; auto-apply is limited to permitted low-tier envs.
- [ ] Apply uses the exact reviewed plan; stale-plan-since-review triggers re-plan + re-review.
- [ ] Blast-radius control is defined (scoped apply, `-refresh-only`, explicit `-target` policy).
- [ ] Rollback procedure classifies revertible vs state-restore/forward-fix changes and maps to the reliability RTO.
- [ ] Drift-remediation playbook consumes the plan-gate drift signal and defines triage owner, reconcile path, and incident threshold.
- [ ] Apply-failure runbook inputs cover partial apply, lock recovery (verified-orphan `force-unlock`), and auth failure as symptom → diagnostic → safe first action.
- [ ] Apply uses least-privilege short-lived credentials; no secrets in apply logs.
- [ ] Promotion, rollback, and lock-recovery are rehearsed (or unrehearsed items logged as explicit open risks).
- [ ] Gate, backend, and registry are named handoffs, not implemented here.

## References

- Upstream: [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md), [`architecture/operations`](../../../../architecture/operations/SKILL.md) (runbook operationalization).
- Builds on: [`terraform-module-and-repository-scaffold`](../terraform-module-and-repository-scaffold/SKILL.md), [`terraform-state-and-secret-management`](../terraform-state-and-secret-management/SKILL.md), [`terraform-plan-gate-and-policy-as-code`](../terraform-plan-gate-and-policy-as-code/SKILL.md) (drift signal + reviewed plan).
- Related: [`terraform-module-reuse-and-supply-chain`](../terraform-module-reuse-and-supply-chain/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md).
