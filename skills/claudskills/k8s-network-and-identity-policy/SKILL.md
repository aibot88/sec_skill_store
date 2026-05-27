---
name: k8s-network-and-identity-policy
description: Use when authoring or hardening the Kubernetes network and workload-identity policy for a service after security and infrastructure-platform have decided the trust zones, identity model, and east-west posture. Produces default-deny NetworkPolicy (namespace-scoped, label-selected), least-privilege ServiceAccount + Role/ClusterRole bindings, Ingress / Gateway API exposure posture, mTLS or service-mesh wiring where adopted, image-pull secret and registry-auth handling, and Pod Security Standards namespace enforcement. Do not use for workload manifest authoring, autoscaling and resilience topology, observability wiring, image hardening / signing / admission-controller policy, or cluster provisioning; use the other Family G archetype skills (cluster provisioning is out of family).
---

# Kubernetes Network and Identity Policy

## When to use

Invoke when establishing the network and identity posture for a workload or namespace, restructuring east-west segmentation, or auditing/hardening NetworkPolicy, RBAC, ingress exposure, and Pod Security Standards before a workload reaches a shared cluster.

Do not use for: Deployment/Service/HPA manifest authoring (use `k8s-workload-packaging-and-manifest`); autoscaling, PDB sizing, anti-affinity (use `k8s-scaling-and-resilience-topology`); metrics/log/trace wiring (use `k8s-observability-and-operations-readiness`); image hardening, signing, SBOM, and the admission-controller policy engine itself (use `k8s-supply-chain-and-image-hardening`); cluster provisioning, CNI installation, control-plane topology (out of Family G — owned by the cloud platform stack and Terraform).

## Inputs

Required:

- A workload manifest set from `k8s-workload-packaging-and-manifest` (the ServiceAccount reference and Service this skill backs with policy).
- Approved `architecture/security` decisions on trust zones, identity model, and east-west posture, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `infrastructure-platform.md` Network & Trust-Boundary and Identity & Access sections.
- The workload tier from `architecture-schema` (drives isolation and RBAC strictness).
- Service-mesh adoption (Istio / Linkerd / none) and whether mTLS is mesh-provided or native.
- The CNI in use (Calico / Cilium) — consumed for NetworkPolicy capability, not installed here.
- The peer set: which namespaces/services this workload may legitimately reach and be reached by.

## Operating rules

- Never generate tutorial-grade policy. Assume a shared multi-tenant cluster where the default is hostile and every allowed flow is justified.
- Consume `architecture/security` and `infrastructure-platform.md`; do not invent decisions. Trust zones, identity model, mesh adoption, and east-west posture are architectural decisions. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- NetworkPolicy is default-deny. Every namespace carrying a workload has a default-deny ingress (and egress where the posture requires) policy; allows are explicit, label-selected, and minimal. A namespace with no policy is rejected.
- Allowed flows are justified, not convenient. Each ingress/egress allow names the peer and the reason. `podSelector: {}` allow-all, or `0.0.0.0/0` egress without justification, is rejected.
- Identity is least privilege. A dedicated ServiceAccount per workload (never `default`), bound to the narrowest Role/ClusterRole that the workload's operational contract requires. Wildcard verbs/resources (`*`) are an ADR-justified exception only.
- ClusterRole is the exception, Role is the default. Cluster-scoped permission requires a named reason; namespace-scoped Role is the baseline.
- Registry auth uses the short-lived path where the platform supports it. Image-pull secrets reference the registry-auth mechanism from the platform decision; long-lived static registry credentials committed or broadly mounted are an ADR-justified exception.
- mTLS posture is explicit. Where a mesh is adopted, declare whether mTLS is `STRICT` and how it is enforced; where no mesh, state whether native TLS or an alternative covers east-west — do not leave it implied.
- Pod Security Standards are enforced at the namespace, not assumed. Set the `pod-security.kubernetes.io/enforce` level (`restricted` baseline) and audit/warn levels; the *admission policy engine* (Kyverno/Gatekeeper) that extends PSS is the supply-chain archetype's ownership — name the handoff.
- Ingress/Gateway exposure is minimal and typed. Only externally reached workloads get an Ingress/Gateway; TLS, host, and path posture come from the platform traffic shape, not invented.
- This skill owns network + identity policy. Workload manifests, autoscaling, observability, and image hardening/admission are named handoffs, not implemented here.
- A policy set that does not pass a connectivity test (allowed peer reaches, denied peer is blocked) and an RBAC review is not done.

## Output contract

The generated network and identity policy MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — default-deny NetworkPolicy, least-privilege RBAC, non-default ServiceAccount, no broadly-mounted long-lived registry credentials, explicit mTLS posture.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — NetworkPolicy present by default; policy reproducible via manifests, not click-ops.
- [observability-standards](../../../../../standards/observability-standards/README.md) — policy-deny and authz-failure events are observable (audit/log seam present; full wiring deferred to the observability archetype).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — policy, ServiceAccount, Role/Binding names `kebab-case`, suffixed by kind when ambiguous.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives isolation granularity and RBAC strictness.

Upstream contract: `architecture/security` is the source of truth for trust zones, identity model, mesh/mTLS, and east-west posture; `infrastructure-platform.md` is the source of truth for network boundaries and registry-auth mechanism. If a needed decision is missing, pause and raise an ADR candidate. Workload manifests, autoscaling, observability, and admission-policy engine are named handoffs.

## Progressive references

- Read `references/k8s-network-identity-playbook.md` when authoring any owned policy or checking the anti-pattern list.
- Read `references/k8s-network-identity-quality-rubric.md` before declaring the policy set complete.
- Use `assets/k8s-network-identity.template.md` as the NetworkPolicy / RBAC / PSS pattern reference.

## Process

1. Gather context: load `architecture/security` (trust zones, identity model, mesh/mTLS, east-west posture) and `infrastructure-platform.md` (network boundaries, registry-auth). Resolve the workload tier from `architecture-schema`. Confirm the workload manifest set (ServiceAccount reference, Service) exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Author the namespace default-deny: a NetworkPolicy selecting all pods denying ingress (and egress where the posture requires) as the baseline every allow is carved from.
3. Author explicit allow policies: label-selected ingress from named peers, label-selected egress to named peers plus DNS; each allow annotated with the peer and reason. No allow-all.
4. Author the dedicated ServiceAccount and the least-privilege Role (or ClusterRole only with a named reason) and binding, scoped to exactly the verbs/resources the operational contract requires.
5. Configure registry auth: image-pull secret referencing the platform registry-auth mechanism via the short-lived path; flag any long-lived static credential as an ADR-required exception.
6. Set the mTLS / mesh posture: where a mesh is adopted, declare `STRICT` mTLS and the enforcement object; where no mesh, state the east-west encryption decision explicitly.
7. Enforce Pod Security Standards at the namespace: `pod-security.kubernetes.io/enforce: restricted` (baseline) plus audit/warn; mark the admission-policy-engine extension as a handoff to `k8s-supply-chain-and-image-hardening`.
8. Set Ingress/Gateway exposure only where externally reached, with TLS/host/path from the platform traffic shape; default to no external exposure.
9. Verify: a connectivity test shows an allowed peer reaches the workload and a denied peer is blocked; an RBAC review (`kubectl auth can-i --list` as the SA) shows no excess permission; document any check that cannot run in the environment.
10. Emit the policy set under `k8s/` plus `network-identity.md` (the allowed-flow matrix, RBAC rationale, mTLS posture) and the named handoff list. Validate against security-, deployment-, observability-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Namespace default-deny NetworkPolicy (ingress, and egress where required).
- Explicit label-selected allow policies, each annotated with peer and reason.
- Dedicated ServiceAccount + least-privilege Role/ClusterRole + binding.
- Image-pull secret referencing the short-lived registry-auth path.
- Explicit mTLS / east-west encryption posture.
- Pod Security Standards namespace enforcement (with the admission-engine handoff marked).
- Ingress/Gateway exposure only where externally reached.
- `network-identity.md` (allowed-flow matrix, RBAC rationale, mTLS posture) and the named handoff list.

Output rules:

- Functional, schema-valid policy — not placeholder.
- Default-deny is present; no allow-all NetworkPolicy or wildcard RBAC without an ADR.
- No broadly-mounted long-lived registry credentials.
- Workload manifests, autoscaling, observability, and the admission-policy engine are handoffs, not implemented here.

## Quality checks

- [ ] Every workload-carrying namespace has a default-deny NetworkPolicy (ingress, and egress where the posture requires).
- [ ] Every allow is label-selected, minimal, and annotated with the peer and reason; no `podSelector: {}` allow-all or unjustified `0.0.0.0/0` egress.
- [ ] A dedicated ServiceAccount is used (never `default`); the bound Role is least-privilege; ClusterRole and wildcard verbs/resources have a named ADR reason.
- [ ] Registry auth uses the short-lived path; any long-lived static credential is an ADR-justified exception and is not broadly mounted.
- [ ] The mTLS / east-west encryption posture is stated explicitly (mesh `STRICT` + enforcement object, or the no-mesh decision).
- [ ] Pod Security Standards are enforced at the namespace (`restricted` baseline + audit/warn); the admission-policy-engine extension is handed to `k8s-supply-chain-and-image-hardening`.
- [ ] Ingress/Gateway exists only where the workload is externally reached, with TLS/host/path from the platform traffic shape.
- [ ] A connectivity test confirms allowed peers reach and denied peers are blocked, or the gap is documented.
- [ ] An RBAC review confirms no excess permission for the ServiceAccount.
- [ ] `network-identity.md` documents the allowed-flow matrix, RBAC rationale, and mTLS posture; workload/scaling/observability/admission are named handoffs.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md).
- Builds on: [`k8s-workload-packaging-and-manifest`](../k8s-workload-packaging-and-manifest/SKILL.md) (ServiceAccount reference and Service this skill backs with policy).
- Holistic review pass: [`k8s-deploy-manifest-review`](../k8s-deploy-manifest-review/SKILL.md) (omnibus).
- Related Family G archetype skills: `k8s-scaling-and-resilience-topology`, `k8s-observability-and-operations-readiness`, `k8s-supply-chain-and-image-hardening` (owns the admission-policy engine).
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
