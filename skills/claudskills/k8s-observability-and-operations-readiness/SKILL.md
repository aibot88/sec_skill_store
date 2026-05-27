---
name: k8s-observability-and-operations-readiness
description: Use when wiring metrics, logs, traces, and operational readiness for a Kubernetes workload or namespace after operations and reliability have decided the observability substrate, SLOs, and runbook hooks. Produces ServiceMonitor/PodMonitor scrape wiring, kube-state-metrics and cAdvisor signal coverage, log-shipping configuration (Fluent Bit / Vector / Loki / cloud-native), OpenTelemetry collector wiring for traces, SLO alert rules, audit-log collection, and runbook inputs for pod-eviction storms, ImagePullBackOff sprees, and node-pressure incidents. Do not use for base manifest authoring, network/identity policy, autoscaler tuning, image hardening, or the observability backend/substrate decision and cluster provisioning; use the other Family G archetype skills (substrate selection is upstream; cluster provisioning is out of family).
---

# Kubernetes Observability and Operations Readiness

## When to use

Invoke when making a Kubernetes workload or namespace observable and operable for production — scrape wiring, log shipping, tracing, SLO alerts, and runbook inputs — or when auditing an inherited workload that is a black box in incidents.

Do not use for: base manifest authoring (use `k8s-workload-packaging-and-manifest`); NetworkPolicy/RBAC (use `k8s-network-and-identity-policy`); autoscaler tuning that *consumes* these metrics (use `k8s-scaling-and-resilience-topology`); image hardening and admission (use `k8s-supply-chain-and-image-hardening`); choosing the observability backend/substrate (decided upstream in `infrastructure-platform.md` / `architecture/operations`); cluster provisioning and control-plane audit *enablement* (out of Family G — owned by the cloud platform stack and Terraform; this skill wires workload/namespace-level collection).

## Inputs

Required:

- A workload manifest set from `k8s-workload-packaging-and-manifest` (the Service/pod this skill makes observable; it exposes a metrics port and stdout logs).
- Approved `architecture/operations` decisions on the observability substrate, alerting destinations, and runbook hooks, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/reliability` SLOs and error-budget policy (drive alert thresholds).
- The workload tier from `architecture-schema` (drives alert severity, retention, sampling).
- The observability stack in use (Prometheus/Grafana/Loki/Tempo or cloud-native) — consumed, not chosen here.
- The trace propagation format (W3C tracecontext / B3) and sampling target.
- Known operational failure modes for this workload (informs runbook inputs).

## Operating rules

- Never generate vanity telemetry. A metric nobody alerts on, a log nobody can query, and a trace with no propagation are not observability — they are cost.
- Consume `architecture/operations` and `architecture/reliability`; do not invent decisions. The observability substrate, alert destinations, SLOs, and runbook hooks are decisions made upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- The observability backend is consumed, not chosen. ServiceMonitor/log-shipper/collector targets the substrate named upstream. Selecting Prometheus-vs-Datadog here is out of scope — a missing substrate is an ADR candidate, not a default.
- Every workload exposes the three signals. Metrics via a scraped endpoint (ServiceMonitor/PodMonitor, not just bare annotations where the stack supports CRDs), logs to stdout shipped structured, traces emitted with context propagation. A workload missing one signal is not operations-ready.
- Alerts are tied to SLOs and are actionable. Each alert rule maps to an SLO or a known failure mode, has a severity from the tier, and names the runbook. A threshold with no runbook and no SLO is rejected.
- Signal coverage includes the platform, not just the app. kube-state-metrics (object state), cAdvisor (container resource), and node-pressure signals are wired so eviction storms and node pressure are visible — not only app latency.
- Logs are structured and PII-safe by default. Shipped logs are structured (JSON), correlate to traces (trace/span IDs), and do not carry secrets or PII; redaction is in the pipeline, not assumed downstream.
- Audit-log collection is scoped to what this layer owns. Workload/namespace-relevant audit events (RBAC denials, policy-deny from the network archetype, admission rejections) are collected; *enabling* the API-server audit policy is a control-plane concern handed off, not done here.
- Runbook inputs are concrete, not prose. For pod-eviction storms, ImagePullBackOff sprees, and node-pressure incidents: the signal that fires, the query to confirm, the first diagnostic step, and the escalation — structured for the operations runbook, not a paragraph.
- This skill owns observability + operations readiness wiring. Base manifests, network/identity, autoscaler tuning, image hardening, and the substrate decision are named handoffs, not implemented here.
- A workload whose alerts have not been test-fired and whose runbook inputs have not been dry-run is not operations-ready.

## Output contract

The generated observability and operations wiring MUST conform to:

- [observability-standards](../../../../../standards/observability-standards/README.md) — metrics scraped via ServiceMonitor/PodMonitor, structured stdout logs shipped, traces with context propagation, SLO-tied alerts, trace/log correlation.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — observability wiring shipped as reproducible manifests, not click-ops dashboards; env-agnostic.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — ServiceMonitor/alert/dashboard object names `kebab-case`, suffixed by kind when ambiguous.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives alert severity, retention, and sampling rate.

Upstream contract: `architecture/operations` is the source of truth for the observability substrate, alert destinations, and runbook hooks; `architecture/reliability` is the source of truth for SLOs and error budgets. If a needed decision is missing, pause and raise an ADR candidate. Base manifests, network/identity, autoscaler tuning, image hardening, and substrate selection are named handoffs.

## Progressive references

- Read `references/k8s-observability-operations-playbook.md` when wiring any owned signal or checking the anti-pattern list.
- Read `references/k8s-observability-operations-quality-rubric.md` before declaring the workload operations-ready.
- Use `assets/k8s-observability-operations.template.md` as the ServiceMonitor/log/trace/alert/runbook pattern reference.

## Process

1. Gather context: load `architecture/operations` (substrate, alert destinations, runbook hooks) and `architecture/reliability` (SLOs, error budgets). Resolve the workload tier from `architecture-schema`. Confirm the workload exposes a metrics port and stdout logs. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Wire metrics: a ServiceMonitor/PodMonitor (or the substrate's equivalent) scraping the workload endpoint; confirm kube-state-metrics and cAdvisor coverage so object state and container resource are visible.
3. Wire log shipping: the upstream-named shipper (Fluent Bit / Vector / cloud-native) collecting stdout, parsing to structured JSON, injecting trace/span IDs, redacting PII/secrets in-pipeline, to the named log backend.
4. Wire tracing: the OpenTelemetry collector (or substrate equivalent), context propagation format, and the tier-correct sampling rate; confirm trace↔log correlation IDs line up.
5. Author SLO alert rules: each tied to an SLO or a known failure mode, severity from the tier, destination from the upstream alert config, and a named runbook — no orphan thresholds.
6. Wire platform-signal coverage: node-pressure, eviction, and ImagePullBackOff signals so cluster-level incidents are visible, not only app metrics.
7. Scope audit-log collection: collect workload/namespace RBAC-denial, network-policy-deny, and admission-rejection events; hand off API-server audit-policy enablement to the control-plane owner.
8. Produce runbook inputs: for pod-eviction storms, ImagePullBackOff sprees, and node-pressure — the firing signal, the confirming query, the first diagnostic step, the escalation — structured for the operations runbook.
9. Verify: test-fire each alert (synthetic breach) and confirm it routes to the destination; dry-run each runbook input against the live signals; document any check that cannot run in the environment.
10. Emit the wiring under `k8s/observability/` plus `operations-readiness.md` (signal inventory, alert→SLO→runbook map, sampling/retention) and the named handoff list. Validate against observability-, deployment-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- ServiceMonitor/PodMonitor scrape wiring with kube-state-metrics and cAdvisor coverage.
- Log-shipping configuration (structured, trace-correlated, PII/secret-redacted) to the named backend.
- OpenTelemetry collector wiring with context propagation and tier-correct sampling.
- SLO alert rules, each tied to an SLO/failure mode, severity, destination, and a named runbook.
- Platform-signal coverage (node-pressure, eviction, ImagePullBackOff).
- Scoped audit-log collection (with control-plane audit-policy handoff marked).
- Concrete runbook inputs for the three named incident classes.
- `operations-readiness.md` (signal inventory, alert→SLO→runbook map, sampling/retention) and the named handoff list.

Output rules:

- Functional, reproducible wiring as manifests — not click-ops, not placeholder.
- No orphan alerts (every alert maps to SLO/failure mode + runbook); no PII/secrets in shipped logs.
- The substrate is consumed, not chosen; substrate selection is an upstream handoff.
- Base manifests, network/identity, autoscaler tuning, and image hardening are handoffs, not implemented here.

## Quality checks

- [ ] The workload exposes all three signals: scraped metrics, structured stdout logs, propagated traces.
- [ ] Metrics are wired via ServiceMonitor/PodMonitor (or substrate equivalent); kube-state-metrics and cAdvisor coverage is present.
- [ ] Shipped logs are structured, carry trace/span correlation IDs, and are PII/secret-redacted in-pipeline.
- [ ] Traces use the upstream propagation format with tier-correct sampling; trace↔log IDs correlate.
- [ ] Every alert rule maps to an SLO or known failure mode, has tier-correct severity, a destination, and a named runbook — no orphans.
- [ ] Node-pressure, eviction, and ImagePullBackOff signals are covered (platform, not only app).
- [ ] Audit-log collection is scoped to workload/namespace events; API-server audit-policy enablement is handed off.
- [ ] Concrete runbook inputs exist for pod-eviction storms, ImagePullBackOff sprees, and node-pressure (signal → query → first step → escalation).
- [ ] Each alert was test-fired to its destination and each runbook input dry-run, or the gap is documented.
- [ ] The observability substrate is the one named upstream (or an ADR candidate is raised); base manifest/network/autoscaler/hardening are named handoffs.

## References

- Upstream: [`architecture/operations`](../../../../architecture/operations/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Builds on: [`k8s-workload-packaging-and-manifest`](../k8s-workload-packaging-and-manifest/SKILL.md) (exposes the metrics port and stdout logs this skill wires).
- Holistic review pass: [`k8s-deploy-manifest-review`](../k8s-deploy-manifest-review/SKILL.md) (omnibus).
- Related Family G archetype skills: `k8s-network-and-identity-policy` (produces policy-deny audit events collected here), `k8s-scaling-and-resilience-topology` (consumes the metrics wired here), `k8s-supply-chain-and-image-hardening`.
- Standards: [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
