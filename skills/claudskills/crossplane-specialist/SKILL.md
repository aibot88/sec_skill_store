---
id: crossplane-specialist
name: crossplane-specialist
type: skill
version: 1.0.0
domain: [infra]
platform: [crossplane, kubernetes]
task: [debugging, review]
maturity: validated
description: >
  Deep-dive Crossplane platform review: XRD design, Composition correctness,
  provider config audit, managed resource health, and GitOps integration.
  Use for structured investigations of stuck Claims, composition pipeline bugs,
  and credential injection patterns. Triggers on: "Crossplane audit", "XRD review",
  "Composition debug", "stuck Claim", "managed resource stuck", "provider config
  review", "Crossplane GitOps".
argument-hint: "<XRD name, Claim name, or problem description>"
tools: Read, Grep, Glob, Bash
effort: max
model: opus
---

# Crossplane Specialist

Structured investigation for Crossplane-based infrastructure platforms. Five phases:
gather context, diagnose, design, recommend, verify.

## Arguments

- `$0` — XRD name, Claim name, or problem description. Required.

---

## Phase 1: Context Gathering

1. List installed providers and packages:
   ```bash
   kubectl get providers
   kubectl get configurations
   kubectl get functions
   ```
2. List XRDs and their ready status:
   ```bash
   kubectl get xrd
   ```
3. List Claims and Composites:
   ```bash
   kubectl get composite --all-namespaces
   kubectl get claim --all-namespaces
   ```
4. Glob for Crossplane manifests in the working directory:
   ```bash
   find . -name "*.yaml" | xargs grep -l "apiVersion: apiextensions.crossplane.io" | sort
   ```

---

## Phase 2: Diagnosis

**Stuck Claim / Composite trace:**

```bash
kubectl describe claim <name> -n <namespace>
kubectl describe composite <name>
kubectl get managed --all-namespaces | grep -v "True"
kubectl describe <managed-resource-kind> <name>
```

**Provider health:**

```bash
kubectl describe provider <name>
kubectl get providerconfig
kubectl describe providerconfig <name>
```

**Composition pipeline:**

```bash
kubectl get composition <name> -o yaml
kubectl get function --all-namespaces
```

---

## Phase 3: Design / Root-Cause Analysis

Map symptoms to causes:

| Symptom                     | Common Causes                                         | Check                                          |
| --------------------------- | ----------------------------------------------------- | ---------------------------------------------- |
| Claim stuck `Waiting`       | Composite not ready, no matching Composition          | `kubectl describe composite` → events          |
| Managed resource `NotFound` | Wrong external-name annotation, ID mismatch           | Provider docs for external-name format         |
| Provider `Unhealthy`        | Bad credentials, missing `ProviderConfig`             | `kubectl describe provider` events             |
| Composition patch fails     | Wrong `fromFieldPath`, type mismatch                  | `kubectl get composite -o yaml` patched fields |
| Function pipeline error     | Function pod crash, malformed `FunctionIO`            | `kubectl logs -n crossplane-system` function   |
| Deletion stuck (finalizer)  | Managed resource `Delete` policy, cloud resource busy | Check deletion policy + cloud console          |

Cite `kind:name` or `file:line` for every finding.

---

## Phase 4: Recommendations

Output findings in priority order:

```
[CRITICAL] <title>
Resource: <kind:name or file:line>
Issue: <one sentence>
Evidence: <kubectl output or config snippet>
Fix: <specific change, with YAML diff if applicable>
Trade-off: <alternative and its downside, if meaningful>
```

Order: CRITICAL → WARNING → INFO.

---

## Phase 5: Verification

After fixes are applied:

1. `kubectl get composite <name>` — `READY: True`, `SYNCED: True`.
2. `kubectl get managed` — all managed resources show `READY: True`.
3. `kubectl describe claim <name>` — no error events.
4. `kubectl apply --dry-run=server -f composition.yaml` — no schema errors.
5. If deletion policy changed: confirm behavior by deleting a test Claim in a non-prod environment.

---

## Reference Docs

| File                    | When to use                                               |
| ----------------------- | --------------------------------------------------------- |
| `xrd-design.md`         | XRD schema design, versioning, validation rules           |
| `compositions.md`       | Composition patch-and-transform, pipeline mode, Functions |
| `provider-configs.md`   | Credential injection, `ProviderConfig` patterns           |
| `managed-resources.md`  | External-name, deletion policy, resource lifecycle        |
| `gitops-integration.md` | Argo CD / Flux health checks, package management          |
