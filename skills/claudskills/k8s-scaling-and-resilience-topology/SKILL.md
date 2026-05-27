---
name: k8s-scaling-and-resilience-topology
description: Use when sizing and hardening the scaling and resilience posture of a Kubernetes workload after reliability and performance have decided SLOs, replica floors, and disruption budgets. Produces tuned HPA / VPA / KEDA selection and parameters, tier-correct PodDisruptionBudget sizing, pod anti-affinity and topology-spread constraints, multi-zone placement, graceful-shutdown wiring (terminationGracePeriodSeconds + preStop), and surge/maxUnavailable budgets per workload tier. This tunes the baseline HPA/PDB the manifest archetype created. Do not use for base manifest authoring, network/identity policy, observability pipeline wiring, image hardening, or cluster/node provisioning and the cluster-autoscaler/Karpenter node layer; use the other Family G archetype skills (node provisioning is out of family).
---

# Kubernetes Scaling and Resilience Topology

## When to use

Invoke when sizing autoscaling for a workload, hardening its survivability against node drains and zone loss, or auditing an inherited workload whose HPA/PDB/affinity is unsafe. This skill *tunes and hardens* the baseline HPA/PDB that `k8s-workload-packaging-and-manifest` created.

Do not use for: base Deployment/Service/HPA/PDB authoring (use `k8s-workload-packaging-and-manifest`); NetworkPolicy/RBAC (use `k8s-network-and-identity-policy`); the metrics pipeline that feeds autoscaling (use `k8s-observability-and-operations-readiness`); image hardening (use `k8s-supply-chain-and-image-hardening`); cluster/node provisioning and the cluster-autoscaler/Karpenter *node* layer (out of Family G — owned by the cloud platform stack and Terraform; this skill owns *pod*-level scaling only).

## Inputs

Required:

- A workload manifest set from `k8s-workload-packaging-and-manifest` (the baseline HPA/PDB this skill tunes).
- Approved `architecture/reliability` decisions on SLOs, replica floors, and disruption budgets per tier, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/performance` decisions on resource targets and latency budgets.
- The workload tier from `architecture-schema` (drives PDB strictness and replica floor).
- The scaling signal: CPU/memory vs custom/event metrics (drives HPA vs KEDA).
- Cluster zone topology (number of zones, whether the scheduler is zone-aware).
- The metrics source name (consumed; the pipeline is the observability archetype's ownership).

## Operating rules

- Never generate tutorial-grade scaling. Assume real traffic spikes, routine node drains, and a zone outage — the workload must survive all three.
- Consume `architecture/reliability` and `architecture/performance`; do not invent decisions. SLOs, replica floors, disruption budgets, and resource targets are architectural decisions. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- The autoscaler matches the scaling signal. CPU/memory-bound → HPA on resource metrics; event/queue-driven → KEDA on the event source; right-sizing requests → VPA (in `recommendation` mode unless an ADR approves auto). Choosing HPA for a queue worker is a defect.
- HPA and VPA do not both manage the same dimension. VPA `auto` updating CPU/memory while HPA scales on CPU is a known conflict — VPA stays in `recommendation` mode, or scopes to non-HPA dimensions, unless an ADR resolves it.
- PDB sizing is tier-correct and never blocks all disruption. `minAvailable`/`maxUnavailable` is sized so a voluntary disruption can still proceed; `maxUnavailable: 0` (or `minAvailable: 100%`) deadlocks node drains and is rejected.
- Replicas have a floor and spread. The replica floor comes from the reliability tier; multi-replica workloads carry pod anti-affinity and a topology-spread constraint so replicas do not co-locate on one node or one zone.
- Multi-zone is the default for tier-0/1. Topology spread across zones (`topologyKey: topology.kubernetes.io/zone`) with `whenUnsatisfiable` set per tier — `DoNotSchedule` for strict tiers, `ScheduleAnyway` where availability beats balance.
- Graceful shutdown is wired, not assumed. `terminationGracePeriodSeconds` covers in-flight work; a `preStop` hook (or readiness flip + drain) lets the workload deregister before SIGTERM. A workload that drops connections on rollout is not done.
- Surge and unavailable budgets respect the tier and the cluster. `maxUnavailable: 0` for availability-critical *rollouts* (distinct from PDB); surge bounded where node capacity is constrained.
- This skill owns pod-level scaling and resilience topology. Base manifests, network/identity, the metrics pipeline, image hardening, and the node-autoscaler layer are named handoffs, not implemented here.
- A scaling/resilience posture not tested against a simulated node drain (PDB honored, no outage) and a scale event is not done.

## Output contract

The generated scaling and resilience posture MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — rollout surge/unavailable budgets per tier; graceful shutdown so rollouts drop no traffic; rollback unaffected by scaling config.
- [observability-standards](../../../../../standards/observability-standards/README.md) — the autoscaler's metric source is named and observable (pipeline wiring deferred to the observability archetype).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — HPA/PDB/constraint object names `kebab-case`, suffixed by kind when ambiguous.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives PDB strictness, replica floor, and zone-spread enforcement.

Upstream contract: `architecture/reliability` is the source of truth for SLOs, replica floors, and disruption budgets; `architecture/performance` is the source of truth for resource and latency targets. If a needed decision is missing, pause and raise an ADR candidate. Base manifests, network/identity, metrics pipeline, image hardening, and node autoscaling are named handoffs.

## Progressive references

- Read `references/k8s-scaling-resilience-playbook.md` when tuning any owned object or checking the anti-pattern list.
- Read `references/k8s-scaling-resilience-quality-rubric.md` before declaring the posture complete.
- Use `assets/k8s-scaling-resilience.template.md` as the HPA/KEDA/VPA/PDB/affinity pattern reference.

## Process

1. Gather context: load `architecture/reliability` (SLOs, replica floors, disruption budgets per tier) and `architecture/performance` (resource/latency targets). Resolve the workload tier from `architecture-schema`. Confirm the baseline HPA/PDB from the manifest archetype exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Select the autoscaler from the scaling signal: HPA (resource/custom metric), KEDA (event/queue), VPA (`recommendation` for right-sizing). Justify the choice against the workload's scaling shape; resolve any HPA/VPA dimension conflict.
3. Tune HPA/KEDA parameters: min from the reliability replica floor, max from the performance/capacity envelope, target metric and stabilization windows so it neither flaps nor lags the SLO.
4. Size the PDB per tier so voluntary disruptions can still proceed (never a drain-deadlocking budget), consistent with the replica floor.
5. Author pod anti-affinity and a topology-spread constraint so replicas do not co-locate on a node; for tier-0/1, spread across zones with `whenUnsatisfiable` per tier.
6. Wire graceful shutdown: `terminationGracePeriodSeconds` covering in-flight work and a `preStop` hook (or readiness-flip drain) so the workload deregisters before SIGTERM.
7. Set rollout surge/`maxUnavailable` per tier (distinct from the PDB), bounded by cluster capacity.
8. Verify: a simulated node drain (`kubectl drain` or cordon+delete) shows the PDB honored and no SLO breach; a scale event shows the autoscaler reacts within the stabilization window; document any check that cannot run in the environment.
9. Emit the tuned objects under `k8s/` plus `scaling-resilience.md` (autoscaler rationale, PDB math, zone-spread posture, shutdown budget) and the named handoff list. Validate against deployment-, observability-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Selected and tuned autoscaler (HPA / KEDA / VPA-recommendation) with min/max and stabilization rationale.
- Tier-correct PDB sizing that never deadlocks a node drain.
- Pod anti-affinity + topology-spread constraint (zone-spread for tier-0/1).
- Graceful-shutdown wiring (`terminationGracePeriodSeconds` + `preStop`/drain).
- Rollout surge/`maxUnavailable` per tier.
- `scaling-resilience.md` (autoscaler rationale, PDB math, zone posture, shutdown budget) and the named handoff list.

Output rules:

- Functional, schema-valid objects — not placeholder.
- No HPA/VPA managing the same dimension without an ADR; no drain-deadlocking PDB.
- Multi-replica workloads always carry anti-affinity + spread; tier-0/1 spreads across zones.
- Base manifests, network/identity, metrics pipeline, image hardening, and node autoscaling are handoffs, not implemented here.

## Quality checks

- [ ] The autoscaler matches the scaling signal (HPA resource/custom, KEDA event, VPA recommendation); the choice is justified.
- [ ] HPA and VPA do not both manage the same dimension (or an ADR resolves it; VPA defaults to `recommendation`).
- [ ] HPA/KEDA min comes from the reliability replica floor; max from the performance/capacity envelope; stabilization tuned to the SLO.
- [ ] The PDB is tier-correct and a voluntary node drain can still proceed (no `maxUnavailable: 0` / `minAvailable: 100%` deadlock).
- [ ] Multi-replica workloads carry pod anti-affinity and a topology-spread constraint; tier-0/1 spread across zones with tier-correct `whenUnsatisfiable`.
- [ ] Graceful shutdown is wired: `terminationGracePeriodSeconds` covers in-flight work and a `preStop`/readiness-drain deregisters before SIGTERM.
- [ ] Rollout surge/`maxUnavailable` matches the tier and is bounded by cluster capacity.
- [ ] A simulated node drain honors the PDB with no SLO breach, and a scale event reacts within the stabilization window, or the gap is documented.
- [ ] `scaling-resilience.md` documents autoscaler rationale, PDB math, zone posture, and shutdown budget; base manifest/network/metrics/hardening/node-autoscaler are named handoffs.

## References

- Upstream: [`architecture/reliability`](../../../../architecture/reliability/SKILL.md), [`architecture/performance`](../../../../architecture/performance/SKILL.md).
- Builds on: [`k8s-workload-packaging-and-manifest`](../k8s-workload-packaging-and-manifest/SKILL.md) (baseline HPA/PDB this skill tunes).
- Holistic review pass: [`k8s-deploy-manifest-review`](../k8s-deploy-manifest-review/SKILL.md) (omnibus).
- Related Family G archetype skills: `k8s-network-and-identity-policy`, `k8s-observability-and-operations-readiness` (owns the metrics pipeline that feeds autoscaling), `k8s-supply-chain-and-image-hardening`.
- Standards: [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
