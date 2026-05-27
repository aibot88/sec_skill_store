---
name: k8s-deploy-manifest-review
description: Use when authoring or reviewing Kubernetes manifests for a production
  workload. Produces or hardens Deployment, Service, HPA, PDB, NetworkPolicy, and
  ServiceAccount with correct probes, resource bounds, security context, and a
  safe rollout strategy.
---

# Kubernetes Deploy Manifest Review

## When to use

Invoke when shipping a workload to Kubernetes for the first time, when the workload's manifests are being changed materially, or when reviewing inherited manifests for production-readiness. Do not invoke for non-Kubernetes deployments.

## Inputs

- Container image reference (registry + tag/digest).
- Workload type (stateless service assumed; stateful workloads need extra design).
- Replica count, expected resource usage (CPU/memory), HPA targets.
- Network model: which namespaces and external services this workload may reach.

## Output contract

Generated or reviewed manifests MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — rolling update default; tier-0 services require canary or blue-green; readiness/liveness probes mandatory; rollback artifact declared.
- [security-standards](../../../../../standards/security-standards/README.md) — `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, drop ALL capabilities, NetworkPolicy by default, ServiceAccount scoping (not the default SA).
- [observability-standards](../../../../../standards/observability-standards/README.md) — Prometheus scrape annotations or a ServiceMonitor; logs to stdout.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — resource names `kebab-case`, suffixed by kind when ambiguous.
- Tier classification from [architecture-schema](../../../../../standards/architecture-schema/README.md) drives PDB requirements and replica defaults.

## Process

1. Author or review `Deployment`:
   - `replicas` set; `strategy: RollingUpdate` with `maxSurge: 1, maxUnavailable: 0`.
   - `imagePullPolicy: IfNotPresent`; image pinned by digest when possible.
   - `resources.requests` AND `resources.limits` set on every container.
   - `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities: { drop: [ALL] }`.
   - Probes: `startupProbe` (slow start), `readinessProbe` (gate traffic), `livenessProbe` (restart on hang). They must be distinct.
2. Author `Service` (ClusterIP unless explicitly external).
3. Author `HorizontalPodAutoscaler` with min/max replicas and target metrics.
4. Author `PodDisruptionBudget` when replicas > 1 (`minAvailable: 1` or `maxUnavailable: 1`).
5. Author `NetworkPolicy` with default-deny ingress; allow only required peers.
6. Author dedicated `ServiceAccount` (no use of `default`); bind only required RBAC.
7. If reviewing existing manifests, produce `findings.md` categorized Blocker / High / Medium / Low.
8. Emit the manifest set under `k8s/` plus a `deploy.md` summarizing the rollout strategy and rollback procedure.

## Outputs

- `k8s/deployment.yaml`, `service.yaml`, `hpa.yaml`, `pdb.yaml`, `networkpolicy.yaml`, `serviceaccount.yaml`.
- `deploy.md` (rollout + rollback).
- `findings.md` when reviewing existing manifests.

## Quality checks

- [ ] Every container has both `requests` and `limits` set.
- [ ] `startupProbe`, `readinessProbe`, and `livenessProbe` are distinct.
- [ ] `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, all capabilities dropped.
- [ ] `NetworkPolicy` denies by default and lists only required peers.
- [ ] `PodDisruptionBudget` exists for any workload with replicas > 1.
- [ ] No use of the `default` ServiceAccount.

## References

(None in v0.1.)
