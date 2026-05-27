---
name: k8s-workload-packaging-and-manifest
description: Use when authoring or hardening the Kubernetes workload manifest set for a service after infrastructure-platform and backend-architecture have decided the runtime substrate, workload class, and release strategy. Produces Deployment / StatefulSet / DaemonSet / Job / CronJob, Service, Ingress, a baseline HPA and PDB, ConfigMap/Secret-referenced configuration injection, distinct startup/readiness/liveness probes, mandatory resource requests and limits, and tier-correct rolling-update parameters — plus container packaging via the language sub-skills. This is the archetype-scoped authoring successor to the k8s-deploy-manifest-review omnibus. Do not use for NetworkPolicy/RBAC depth, autoscaling/PDB sizing and resilience topology, observability wiring, image hardening and admission control, or cluster provisioning; use the other Family G archetype skills (cluster provisioning is out of family).
---

# Kubernetes Workload Packaging and Manifest

## When to use

Invoke when shipping a workload to Kubernetes for the first time, materially changing a workload's manifest set, or hardening inherited manifests for production-readiness authoring. This skill owns the *authoring* of the manifest slice; the `k8s-deploy-manifest-review` omnibus remains the holistic cross-archetype review pass.

Do not use for: NetworkPolicy / ServiceAccount / RBAC depth (use `k8s-network-and-identity-policy`); HPA/VPA/KEDA tuning, PDB sizing, anti-affinity, topology spread, graceful shutdown (use `k8s-scaling-and-resilience-topology`); metrics/log/trace wiring and ServiceMonitor (use `k8s-observability-and-operations-readiness`); image hardening, signing, SBOM, admission control (use `k8s-supply-chain-and-image-hardening`); cluster provisioning, node pools, control-plane topology (out of Family G — owned by the cloud platform stack and Terraform).

## Inputs

Required:

- A container image reference (registry + tag, digest-pinnable) or the source to package via a language sub-skill.
- Approved `infrastructure-platform.md`, or explicit confirmation it is intentionally deferred.

Optional:

- Approved `backend-architecture.md` for workload class, resource expectations, and operational contracts.
- The workload's tier from `architecture-schema` (drives replica and PDB defaults).
- Release strategy from `infrastructure-platform.md` Deployment & Release Architecture (rolling / blue-green / canary / progressive).
- Configuration and secret keys the workload consumes (names only; values are never authored here).
- Stateful requirements (persistent volumes, ordered identity) if the workload is not stateless.

## Operating rules

- Never generate tutorial-grade manifests. Assume production: probes that actually gate traffic, both resource requests and limits, a digest-pinned image, and a declared rollback.
- Consume `infrastructure-platform.md` and `backend-architecture.md`; do not invent decisions. Runtime substrate, workload class, release strategy, and resource expectations come from upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Select the workload kind from the class, not by habit. Stateless API → Deployment; ordered/identity-bound → StatefulSet; node-local agent → DaemonSet; run-to-completion → Job; scheduled → CronJob. Justify the choice against the workload class.
- Every container has `resources.requests` AND `resources.limits`. A container without both is rejected — it breaks scheduling fairness and node stability.
- The three probes are distinct and purposeful. `startupProbe` covers slow init, `readinessProbe` gates traffic, `livenessProbe` restarts a hung process. Reusing one endpoint for all three, or omitting readiness, is rejected.
- The image is referenced by digest where the registry supports it; `imagePullPolicy` is explicit. A floating `:latest` tag is rejected for any promotable environment.
- Configuration is injected, never baked. Config via ConfigMap, secrets via Secret reference (the *reference* only — secret values and the secret backend are owned upstream/by the security archetype). No environment-branched manifests.
- Author a tier-correct baseline HPA and PDB so the workload is not born unsafe, but defer sizing and resilience topology to `k8s-scaling-and-resilience-topology`. Set a safe default; mark the tuning handoff explicitly.
- Set the pod-template security-context baseline (non-root, drop ALL, no privilege escalation, read-only root FS) as a floor; deep image hardening, signing, and admission control are the supply-chain archetype's ownership — name the handoff.
- Rolling-update parameters match the tier. `maxUnavailable: 0` for tier-0/1 availability-critical workloads; tighter surge for capacity-constrained clusters. The release *strategy* (blue-green/canary) is consumed from upstream, not invented.
- This skill owns the manifest set + packaging entrypoint. NetworkPolicy/RBAC depth, autoscaling tuning, observability wiring, and image hardening are named handoffs, not implemented here.
- A manifest set that does not `kubectl apply --dry-run=server` cleanly and pass a schema/policy lint is not done.

## Output contract

The generated manifest set MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — rolling update default; tier-0 requires canary or blue-green per upstream; readiness/liveness probes mandatory; rollback artifact declared; env-agnostic (no env-branched manifests, no baked config).
- [security-standards](../../../../../standards/security-standards/README.md) — security-context baseline (`runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop ALL capabilities), non-default ServiceAccount referenced (RBAC depth deferred), no secret values in manifests.
- [observability-standards](../../../../../standards/observability-standards/README.md) — logs to stdout; Prometheus scrape annotation or ServiceMonitor seam present (full wiring deferred to the observability archetype).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — resource names `kebab-case`, suffixed by kind when ambiguous; labels follow the recommended `app.kubernetes.io/*` set.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives replica and PDB defaults.

Upstream contract: `infrastructure-platform.md` is the source of truth for runtime substrate, release strategy, and packaging strategy; `backend-architecture.md` is the source of truth for workload class and resource expectations. If a needed decision is missing, pause and raise an ADR candidate. NetworkPolicy/RBAC, autoscaling tuning, observability wiring, and image hardening are named handoffs.

## Progressive references

- Read `references/k8s-workload-manifest-playbook.md` when authoring any owned resource or checking the anti-pattern list.
- Read `references/k8s-workload-manifest-quality-rubric.md` before declaring the manifest set complete.
- Use `assets/k8s-workload-manifest.template.md` as the manifest-set and label/probe-pattern reference.

## Process

1. Gather context: load `infrastructure-platform.md` (Workload Inventory, Runtime Substrate Selection, Deployment & Release Architecture, Packaging & Artifact Strategy) and `backend-architecture.md` (workload class, resource expectations, operational contracts). Resolve the workload tier from `architecture-schema`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Package the container: invoke the matching language sub-skill (`dockerfile-and-jvm-tuning` for JVM; the planned non-JVM siblings for Python/Node/Go/.NET/static). Obtain a digest-pinnable image reference.
3. Select the workload kind from the class and author the controller (Deployment / StatefulSet / DaemonSet / Job / CronJob) with replicas from the tier default, the security-context baseline, and explicit `imagePullPolicy`.
4. Set resource requests and limits on every container, derived from the upstream resource expectation — never blank, never guessed silently.
5. Author the three distinct probes: `startupProbe` (slow init budget), `readinessProbe` (traffic gate), `livenessProbe` (hang restart). Endpoints and thresholds differ by purpose.
6. Author `Service` (ClusterIP unless upstream declares external) and `Ingress` where the workload is externally reached, referencing the upstream traffic shape.
7. Wire configuration injection: ConfigMap for config, Secret *references* for secrets (names only). No values, no env-branched manifests.
8. Author the tier-correct baseline `HorizontalPodAutoscaler` and `PodDisruptionBudget` (PDB required when replicas > 1) as safe defaults, with an explicit handoff comment to `k8s-scaling-and-resilience-topology` for sizing.
9. Set rolling-update parameters per tier (`maxUnavailable: 0` for availability-critical); honor the upstream release strategy (blue-green/canary handed off to the delivery mechanics, not invented here).
10. Verify: `kubectl apply --dry-run=server` (or `kubeconform`/`kubectl --dry-run=client` where no cluster) passes; a schema/policy lint passes; document any check that cannot run in the environment.
11. Emit the manifest set under `k8s/` plus `deploy.md` (rollout + rollback) and the explicit handoff list. Validate against deployment-, security-, observability-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Workload controller manifest (Deployment / StatefulSet / DaemonSet / Job / CronJob) matching the workload class.
- `Service` and, where externally reached, `Ingress`.
- Baseline `HorizontalPodAutoscaler` and `PodDisruptionBudget` (PDB when replicas > 1) with the sizing handoff marked.
- Distinct `startupProbe`, `readinessProbe`, `livenessProbe`.
- Resource `requests` and `limits` on every container.
- ConfigMap / Secret-reference configuration injection (references only).
- Security-context baseline on the pod template.
- `deploy.md` (rollout strategy + rollback) and the named handoff list.

Output rules:

- Functional, schema-valid manifests — not placeholder.
- Both `requests` and `limits` on every container; no floating `:latest` for promotable envs.
- No secret values, no env-branched manifests, no baked config.
- Autoscaling sizing, NetworkPolicy/RBAC depth, observability wiring, and image hardening are handoffs, not implemented here.

## Quality checks

- [ ] Workload kind matches the workload class from `backend-architecture.md` / `infrastructure-platform.md`.
- [ ] Every container has both `resources.requests` and `resources.limits`.
- [ ] `startupProbe`, `readinessProbe`, and `livenessProbe` are present and distinct.
- [ ] Image is digest-pinnable and `imagePullPolicy` is explicit; no floating `:latest` for promotable environments.
- [ ] Configuration is injected via ConfigMap/Secret references; no secret values or env-branched manifests.
- [ ] A baseline HPA exists and a PDB exists for any workload with replicas > 1, with the sizing handoff to `k8s-scaling-and-resilience-topology` marked.
- [ ] Security-context baseline set (`runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop ALL), non-default ServiceAccount referenced.
- [ ] Rolling-update parameters match the tier; the upstream release strategy is honored, not invented.
- [ ] `kubectl apply --dry-run=server` (or offline schema lint) passes, or the gap is documented.
- [ ] `deploy.md` declares rollout and rollback; NetworkPolicy/RBAC, scaling, observability, and image hardening are named handoffs.

## References

- Upstream: [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md).
- Packaging sub-skills: [`dockerfile-and-jvm-tuning`](../dockerfile-and-jvm-tuning/SKILL.md) (JVM; non-JVM siblings planned).
- Holistic review pass: [`k8s-deploy-manifest-review`](../k8s-deploy-manifest-review/SKILL.md) (omnibus; this skill owns the authoring slice).
- Related Family G archetype skills: `k8s-network-and-identity-policy`, `k8s-scaling-and-resilience-topology`, `k8s-observability-and-operations-readiness`, `k8s-supply-chain-and-image-hardening`.
- Standards: [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
