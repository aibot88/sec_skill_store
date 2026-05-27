---
name: infrastructure-platform
description: Use when an approved system design exists and the team needs production-grade platform and infrastructure architecture before IaC implementation. Produces cloud and account topology, environment model, runtime substrate selection, network and trust-boundary architecture, identity and secrets strategy, deployment and release substrate, IaC ownership boundaries, CI/CD posture, operational platform services, cost strategy, disaster posture, and implementation handoff guidance. Do not use for Terraform authoring, Kubernetes manifests, CI/CD YAML, application runtime tuning, incident response, or service runbooks; use the relevant implementations/infrastructure/<vendor> skill instead.
---

# Infrastructure Platform

## When to use

Invoke after `system-design` has approved a design and before `implementations/infrastructure/*` skills generate Terraform, Kubernetes manifests, Helm charts, container images, or CI/CD pipelines.

Do not use for application-level configuration, in-cluster service tuning, runbook or oncall workflow design (use `operations`), incident response (use `reliability`), or vendor-specific resource code (use the relevant implementation skill).

## Inputs

Required:

- Approved `system-design.md` and the relevant ADRs.
- The platform scope in question: greenfield platform, new environment, new tenant or region, or platform evolution.
- Workload inventory: services, jobs, datastores, and external integrations the platform must host.

Optional:

- PRD or system-design sections covering scale, residency, compliance regime, and SLOs.
- Existing platform state: cloud accounts, networks, clusters, IaC repos, and golden paths.
- Vendor, region, or hosting constraints.
- Cost envelope and FinOps expectations.
- Team operating model: who owns platform, who owns services, what is paved-road vs free-for-all.

## Operating rules

- Separate platform concerns from application concerns. The platform exposes contracts (deployability, networking, identity, secrets, telemetry, runtime guarantees); applications consume them. Reject ad hoc app-team ownership of foundational primitives and platform logic leaking into services.
- Runtime substrate follows workload shape, not vendor enthusiasm. Choose against workload behavior, scaling, operational maturity, compliance, and deployment frequency. Reject Kubernetes-by-default and serverless-by-trend; every substrate has operational cost, scaling tradeoffs, and failure modes.
- Environment topology is explicit. Every environment names its purpose, isolation boundary, data posture, parity expectations, promotion flow, and ownership. Reject ad hoc staging and environment sprawl without lifecycle governance.
- Network architecture starts with trust boundaries. Every workload sits in a named trust zone with explicit ingress, egress, and connectivity assumptions. Reject flat networks, unrestricted east-west traffic, and implicit trust.
- Identity is the new perimeter. Define workload identity, human access, service-to-service authentication, and secrets lifecycle. Reject static credentials, shared admin accounts, and long-lived machine secrets; prefer federated/workload identity, short-lived credentials, and centralized policy.
- Deployment is architecture, not scripting. Each workload class names its rollout mechanism, rollback behavior, blast-radius expectations, and deployment gating signals. Reject one deployment strategy for all workloads.
- Infrastructure ownership boundaries are explicit. IaC defines platform-owned vs service-owned modules, policy-enforced boundaries, and state ownership. Reject giant monolithic Terraform repos and unrestricted infrastructure mutation.
- Complexity is opt-in. Multi-region, multi-account, multi-cluster, and multi-tenant architecture each require a measurable business driver, operational ownership, and an ADR. Reject speculative geo-distribution and future-proofing through uncontrolled complexity.
- Cost is a first-class architectural constraint. Decisions consider idle cost, autoscaling behavior, storage growth, network egress, reserved capacity, and operational staffing. Reject "optimize later" cost posture.
- Challenge weak platform assumptions directly and operationally: unnecessary Kubernetes, flat networks, shared credentials, CI/CD trust gaps, operational over-complexity.
- When a platform decision changes a regulatory, residency, or trust boundary, raise an ADR candidate against `system-design`.

## Output contract

`platform-architecture.md` MUST conform to [standards/architecture-schema](../../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, and linkage back to `system-design.md` and its ADRs.

Security, observability, and operational content additionally conforms to [security-standards](../../../standards/security-standards/README.md), [observability-standards](../../../standards/observability-standards/README.md), and [deployment-standards](../../../standards/deployment-standards/README.md). Skill structure conforms to [documentation-standards](../../../standards/documentation-standards/README.md).

Use `assets/platform-architecture.template.md` as the scaffold; it implements the schema. No vendor-specific Terraform, manifests, or pipeline YAML appear in the architecture unless they materially change architecture behavior.

## Progressive references

- Read `references/platform-architecture-playbook.md` when inventorying workloads, choosing cloud/account topology, environment model, runtime substrate, network and trust-boundary architecture, identity and secrets strategy, packaging, deployment and IaC strategy, CI/CD posture, cross-cutting platform services, cost/FinOps posture, or disaster posture, and to check the anti-pattern list.
- Read `references/platform-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/platform-architecture.template.md` for `platform-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 2, 4, 5, 9, 14). Step 15 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. Inventory every workload that needs a runtime home (APIs, background jobs, scheduled workloads, queues, streaming, databases, edge services, third-party integrations) with runtime expectations, scaling shape, criticality, and deployment frequency.
- [ ] Step 2: Choose cloud and account topology: provider(s), account/project structure, organizational boundaries, region strategy. Justify against blast radius, billing isolation, compliance, ownership, and residency. Draft an ADR candidate for multi-account/multi-cloud decisions. See `references/platform-architecture-playbook.md`.
- [ ] Step 3: Define environment architecture: environment list, lifecycle, promotion flow, parity expectations; per environment isolation level, production parity, data posture, and deployment gating. Reject shared mutable staging.
- [ ] Step 4: Choose the runtime substrate per workload class (Kubernetes, serverless, managed app platform, VM, edge, batch). Justify against scaling, deployment frequency, startup latency, operational maturity, and observability. Draft an ADR candidate for the substrate decision.
- [ ] Step 5: Define network and trust-boundary architecture: VPC/VNet layout, subnet segmentation, ingress model, egress controls, DNS topology, private connectivity, east-west posture. Every component names its trust zone, ingress/egress policy, and internet exposure. Draft an ADR candidate for trust-boundary decisions.
- [ ] Step 6: Define identity and access architecture: workload identity, human access model, service authentication, audit posture, admin boundaries, break-glass, and privileged-session handling. Reject static cloud credentials and shared operational identities.
- [ ] Step 7: Define secrets and configuration strategy: secrets store, issuance path, rotation cadence, injection mechanism, and config-vs-secret boundary. Reject secrets in Git or images and manual rotation.
- [ ] Step 8: Define packaging and artifact strategy: base-image strategy, artifact provenance, image signing, vulnerability scanning, registry topology, SBOM, and immutable-artifact expectations. Reject mutable production artifacts and unscanned images.
- [ ] Step 9: Define deployment and release architecture: deployment substrate (GitOps/push), release strategy per workload class (rolling, blue-green, canary, progressive), gating signals, rollback, and blast-radius controls. Draft an ADR candidate for the deployment-mechanism decision. Reject direct production mutation.
- [ ] Step 10: Define IaC strategy: tool selection, repo layout, module boundaries (platform-owned vs service-owned), policy-as-code posture, state management, drift detection, module versioning, and approval workflow. Reject unbounded state and no-ownership repos.
- [ ] Step 11: Define CI/CD platform architecture: build trust model, artifact promotion path, environment promotion flow, secrets handling in CI, policy gates, provenance, supply-chain integrity, ephemeral runners, and deployment authorization. Reject CI with unrestricted production credentials.
- [ ] Step 12: Define cross-cutting platform services: observability backend, metrics/logging/tracing pipelines, certificate management, service-mesh posture, feature-flag infrastructure, with ownership boundaries and tenant isolation. Detailed instrumentation belongs to `operations`.
- [ ] Step 13: Define cost and FinOps posture: tagging standards, budget ownership, autoscaling defaults, reserved-capacity posture, off-hours policies, egress-risk areas, storage growth, cost-allocation visibility, and budget-breach response.
- [ ] Step 14: Define disaster and resilience posture: backup substrate, region-failover topology, DR posture, RTO/RPO assumptions, active-passive vs active-active, restore testing, and regional isolation behavior. Draft an ADR candidate for region-topology/DR decisions. Reject backups without restore drills.
- [ ] Step 15: Generate `platform-architecture.md` from `assets/platform-architecture.template.md`. Consolidate ADR candidates (numbering, status, alternatives, downsides). Validate against [standards/architecture-schema](../../../standards/architecture-schema/README.md) and `references/platform-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `platform-architecture.md` at `docs/architecture/<product-slug>/platform-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../../standards/architecture-schema/README.md).

Optional, when applicable:

- Account topology, network/trust-zone, or deployment topology diagrams.
- Workload-to-substrate mapping table; IaC ownership matrix; cost allocation model.
- ADR drafts for substrate, region topology, IaC tool, or deployment mechanism decisions.

Output rules:

- Keep the architecture decision-oriented and operationally grounded, not vendor-decorative.
- Document tradeoffs and the rejected alternative, not only the chosen path.
- Name workloads and zones by role and trust posture, not by vendor product.
- Treat cost, disaster posture, and operational ownership as part of the design, not later implementation detail.

## Quality checks

- [ ] `references/platform-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `platform-architecture.md` validates against [standards/architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every workload class names its runtime substrate and the justification.
- [ ] Environment list states isolation level, data posture, and parity rules.
- [ ] Every component sits in a named trust zone with stated ingress and egress rules.
- [ ] Workload identity, human access, and service-to-service auth are each explicitly defined.
- [ ] Secrets model names the store, issuance path, rotation cadence, and injection mechanism.
- [ ] Image strategy covers base images, signing, scanning, and registry topology.
- [ ] Each workload class names its release mechanism and rollback path.
- [ ] IaC strategy names the module boundary between platform and service ownership.
- [ ] Multi-region, multi-account, or multi-tenant complexity, if present, is justified by a stated driver and has an ADR.
- [ ] Cost posture states tagging, autoscaling defaults, and a budget-breach action; disaster posture states RTO/RPO.
- [ ] No vendor-specific Terraform, manifests, or pipeline YAML appear unless they materially change architecture behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/infrastructure/aws`, `implementations/infrastructure/gcp`, `implementations/infrastructure/azure`, `implementations/infrastructure/kubernetes`, `implementations/infrastructure/terraform`, `implementations/infrastructure/github-actions`.
- Related architecture skills: [`operations`](../operations/SKILL.md), [`reliability`](../reliability/SKILL.md), [`security`](../security/SKILL.md), [`performance`](../performance/SKILL.md).
