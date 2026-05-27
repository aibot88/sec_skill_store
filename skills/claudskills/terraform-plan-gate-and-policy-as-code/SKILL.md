---
name: terraform-plan-gate-and-policy-as-code
description: Use when designing, reviewing, or hardening the pre-merge Terraform gate and policy-as-code after the repo scaffold and state backend exist and operations and security have decided gate strictness per blast-radius tier. Produces pre-merge checks (fmt, validate, plan diff posted to the PR), policy-as-code (OPA/Conftest, Checkov, tfsec, or Sentinel) with tier-scaled strictness, scheduled drift detection, required-reviewer rules per environment, and prohibited-resource/provider policy per environment. Do not use for repo/module layout, state/secret backend, apply and promotion orchestration, or module registry/supply chain; use the other terraform archetype skills instead.
---

# Terraform Plan Gate and Policy as Code

## When to use

Invoke when establishing the pre-merge CI gate for a Terraform repository, adding policy-as-code, wiring drift detection, or auditing/hardening gate strictness and reviewer rules before the configuration manages production infrastructure.

Do not use for: repo/module structure (use `terraform-module-and-repository-scaffold`), state backend/secret handling (use `terraform-state-and-secret-management`), apply/promotion orchestration (use `terraform-apply-and-promotion-mechanics`), or module versioning/provenance (use `terraform-module-reuse-and-supply-chain`).

## Inputs

Required:

- An existing repo/module scaffold and a configured remote state backend (from the scaffold and state skills).
- Approved `architecture/operations` decisions on gate posture: required reviewers, change windows, and per-tier promotion-gate expectations.
- Approved `architecture/security` decisions on policy requirements: encryption, public-exposure prohibitions, prohibited resources/providers, and the policy engine posture.

Optional:

- Blast-radius tier classification per environment/module (drives policy strictness).
- Existing CI system (GitHub Actions, GitLab CI, etc.) — the gate is wired into it; CI identity/OIDC is consumed, not configured here.
- Existing policy-as-code (Checkov/tfsec/OPA/Sentinel) baseline.
- Compliance regime mandating specific controls.

## Operating rules

- Consume the posture; do not invent it. Gate strictness, reviewer rules, and prohibited resources come from `architecture/operations` and `architecture/security`. If a tier's required strictness or a prohibition is unstated, pause and raise an ADR candidate.
- The gate is advisory until it blocks merge. `fmt`/`validate`/`plan`/policy must be required status checks on the protected branch, not optional CI that can be ignored. A non-blocking "gate" is a rejected design.
- The plan is reviewed by humans and machines. `terraform plan` output is posted to the PR (no secrets in the diff) for human review; policy-as-code evaluates the plan JSON for machine-enforced rules. Both are required.
- Policy strictness scales with blast radius. Higher-tier environments enforce stricter policy sets and more required reviewers; the tier→strictness mapping is explicit and traceable to `architecture-schema`. Uniform strictness that ignores tiers is rejected.
- Every policy maps to a security or operations rationale. No policy without a mapped requirement; no stated requirement (encryption, no public S3/SG, allowed regions, prohibited resource types) left unenforced. Report unmapped policies and unenforced requirements as gaps.
- Plan-time policy is not runtime security. Policy-as-code on the plan catches misconfig before apply; it does not replace in-cloud guardrails (SCPs) or runtime detection. State the boundary.
- Secret exposure in plan output is a defect: the gate must redact or avoid printing sensitive values in the PR-posted plan, and a secret scan runs in the gate (handing off the secret *storage* discipline to the state skill).
- Drift is detected on a schedule, not discovered during an incident. A scheduled `terraform plan -refresh-only` (or detect-drift) reports drift per environment with an owner and an action path; drift remediation *mechanics* are the apply skill (named handoff).
- This skill owns the pre-merge gate, policy-as-code, drift detection, and reviewer rules. It does not orchestrate apply, configure the backend, or manage the registry — each is a named handoff.
- The gate must run deterministically in CI without long-lived cloud credentials: plan uses the OIDC/short-lived identity from the CI setup (consumed), and policy evaluation runs on plan JSON without needing apply permissions.

## Output contract

The gate and policy-as-code MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — policy enforces encryption, no public exposure, prohibited resources/providers; no secrets in PR-posted plan; secret scan in the gate.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — gate is a required status check; per-tier reviewer and change-window rules enforced.
- [observability-standards](../../../../../standards/observability-standards/README.md) — drift detection runs on a schedule and reports per-environment drift as an observable signal with an owner.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — policy, check, and workflow naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives policy strictness and required-reviewer count.

Upstream contract: `architecture/operations` is the source of truth for reviewer rules, change windows, and gate posture; `architecture/security` is the source of truth for policy requirements and prohibitions. If a needed decision is unstated, pause and raise an ADR candidate. Scaffold/state are inputs; apply/promotion and registry are downstream handoffs.

## Process

1. Load `architecture/operations` (reviewer rules, change windows, gate posture) and `architecture/security` (policy requirements, prohibitions, engine posture). Confirm the scaffold and state backend exist. If a tier's strictness or a prohibition is unstated, pause and raise an ADR candidate.
2. Inventory current gating (if any): existing status checks, policy tooling, drift detection, branch protection, and reviewer rules. Record gaps against the operations/security requirements.
3. Define the pre-merge check pipeline: `terraform fmt -check`, `terraform init -backend=false` (or read-only init), `terraform validate`, and `terraform plan` with the JSON plan captured and a human-readable diff posted to the PR with secrets redacted.
4. Select and configure the policy engine(s) per the security posture: OPA/Conftest, Checkov, tfsec, or Sentinel. Author policies that evaluate the plan JSON for the stated requirements (encryption-required, no public S3/SG/buckets, allowed regions, prohibited resource types/providers, mandatory tags).
5. Define the tier→strictness mapping: per blast-radius tier, the policy set enforced and the required-reviewer count, traceable to `architecture-schema`. Higher tiers = stricter policy + more reviewers + tighter change windows.
6. Make the gate blocking: configure branch protection so `fmt`/`validate`/`plan`/policy are required status checks and the per-tier reviewer rules (from the scaffold's CODEOWNERS) are enforced before merge.
7. Add a secret scan to the gate and ensure the PR-posted plan redacts sensitive values; reference the state skill for secret-storage discipline.
8. Configure scheduled drift detection: a periodic `terraform plan -refresh-only` per environment that reports drift with an owner and an action path; hand off the remediation runbook to the apply skill.
9. State the boundary explicitly: plan-time policy is pre-apply misconfig prevention, not runtime security or in-cloud guardrails (SCPs are the cloud-platform skill's concern).
10. Name handoffs: layout ← scaffold; backend/secrets ← state skill; apply/promotion + drift remediation → `terraform-apply-and-promotion-mechanics`; module provenance/SCA → `terraform-module-reuse-and-supply-chain`.
11. Verify: run the full gate on a sample PR (a compliant change passes; a deliberately non-compliant change — e.g. public bucket, unencrypted volume, prohibited region — is blocked by policy), confirm the plan diff posts without secrets, and confirm branch protection rejects merge on failure. Document any check that cannot run.
12. Validate against [security-standards](../../../../../standards/security-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [naming-conventions](../../../../../standards/naming-conventions/README.md), and [architecture-schema](../../../../../standards/architecture-schema/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Pre-merge check pipeline: `fmt`, `validate`, `plan` (JSON + redacted PR diff), wired into CI as required status checks.
- Policy-as-code rule set (OPA/Conftest, Checkov, tfsec, or Sentinel) evaluating plan JSON, each policy mapped to a security/operations rationale.
- Tier→strictness mapping: policy set + required-reviewer count per blast-radius tier.
- Branch-protection and required-reviewer configuration enforcing the gate and CODEOWNERS.
- Secret scan in the gate + redaction of secrets in the PR-posted plan.
- Scheduled drift-detection workflow with per-environment drift reporting and owner.
- Handoff list (scaffold, state, apply, registry).

Output rules:

- The gate blocks merge; a non-blocking gate is not acceptable.
- Every policy maps to a stated requirement; unmapped policies removed, unenforced requirements reported as gaps.
- No secrets appear in the PR-posted plan.
- Apply orchestration, backend config, and registry are handoffs, not implemented here.

## Quality checks

- [ ] Gate posture/reviewer rules sourced from `architecture/operations`; policy requirements/prohibitions from `architecture/security` (or an ADR candidate is raised).
- [ ] `fmt`, `validate`, `plan`, and policy run as **required** status checks on the protected branch.
- [ ] `terraform plan` output is posted to the PR with sensitive values redacted.
- [ ] Policy-as-code evaluates plan JSON and enforces the stated requirements (encryption, no public exposure, allowed regions, prohibited resources/providers, mandatory tags).
- [ ] Policy strictness and required-reviewer count scale with blast-radius tier, traceable to `architecture-schema`.
- [ ] Every policy maps to a security/operations rationale; gaps (unmapped policy / unenforced requirement) are reported.
- [ ] A secret scan runs in the gate and the PR-posted plan contains no secrets.
- [ ] Scheduled drift detection runs per environment and reports drift with an owner and action path.
- [ ] The plan-time-policy vs runtime-security boundary is stated.
- [ ] The gate runs in CI without long-lived cloud credentials (OIDC/short-lived, consumed from the CI setup).
- [ ] Apply/promotion, backend, and registry are named handoffs, not implemented here.

## References

- Upstream: [`architecture/operations`](../../../../architecture/operations/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Builds on: [`terraform-module-and-repository-scaffold`](../terraform-module-and-repository-scaffold/SKILL.md) (CODEOWNERS/review rules), [`terraform-state-and-secret-management`](../terraform-state-and-secret-management/SKILL.md) (secret-storage discipline).
- Related terraform archetype skills: [`terraform-apply-and-promotion-mechanics`](../terraform-apply-and-promotion-mechanics/SKILL.md) (drift remediation + apply), [`terraform-module-reuse-and-supply-chain`](../terraform-module-reuse-and-supply-chain/SKILL.md) (module SCA/provenance).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`multi-tenant-saas`](../../../../../architecture-patterns/multi-tenant-saas/README.md).
