---
name: openshift-app
description: >-
  Package applications for OpenShift deployment: container images (UBI, arbitrary
  UID, multi-stage builds), packaging formats (Helm, Kustomize, Operators, OLM v1),
  CI/CD (Tekton, ArgoCD, Shipwright, Conforma), security (SCC, PSA, supply chain,
  image signing, secrets), operations (Routes, probes, scaling, monitoring, storage),
  disconnected/air-gapped patterns, and critical gotchas. Covers OCP 4.14-4.21.
  NOT for cluster installation or infrastructure management.
---

# OpenShift Application Packaging

Package, build, secure, and deploy applications on OpenShift Container Platform
4.14-4.21. Covers container images, deployment manifests, CI/CD pipelines, security
hardening, operational patterns, and disconnected environments.

## Quick Decision Guide

| Task | Go to |
|------|-------|
| Build a container image for OpenShift | [Container Images](#container-image-essentials) below |
| Choose Helm vs Kustomize vs Operator | [Packaging Decision Matrix](#packaging-decision-matrix) below |
| Fix SCC / permission errors | `references/security.md` S Restricted-v2 |
| Set up CI/CD pipeline | `references/cicd-gitops.md` |
| Harden supply chain (sign, attest, scan) | `references/security.md` S Supply Chain |
| Configure Routes, probes, scaling | `references/operations.md` |
| Deploy in air-gapped / disconnected env | `references/disconnected.md` |
| Migrate from DeploymentConfig | `references/gotchas.md` S DeploymentConfig |
| Understand OCP version breaking changes | `references/gotchas.md` S Version Timeline |

## Critical Gotchas (Read First)

### 1. Arbitrary UID -- The #1 "Works on K8s, Fails on OpenShift" Issue

OpenShift assigns a **random UID** from a namespace-specific range but always
sets **GID 0** (root group). Hardcoded `USER 1000` in Dockerfiles will fail
under `restricted-v2` SCC.

```dockerfile
# OpenShift-compatible Dockerfile pattern
FROM registry.access.redhat.com/ubi9/ubi-minimal:latest

COPY --chown=1001:0 app /app
RUN chmod -R g=u /app && \
    chgrp -R 0 /app

# Use 1001 as conventional non-root UID
# OpenShift ignores this and assigns its own UID, but vanilla K8s respects it
USER 1001
EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

Key rules:
- **Files**: `chgrp -R 0 && chmod -R g=u` (mirror owner perms to root group)
- **Ports**: must be > 1023 (no privileged ports under restricted SCC)
- **USER**: set to 1001 for portability, but leave `runAsUser` empty in pod spec
- **ENTRYPOINT**: always use exec form `["binary"]` (not shell form) for signal propagation
- **`/etc/passwd`**: if app needs username lookup, make it group-writable and use entrypoint to append dynamic entry
- **`/tmp`**: mount emptyDir if using `readOnlyRootFilesystem: true`

### 2. restricted-v2 SCC (Default Since OCP 4.11)

All authenticated users get `restricted-v2`. It is stricter than vanilla K8s PSS restricted:

| Field | restricted-v2 | K8s PSS restricted |
|-------|--------------|-------------------|
| Capabilities | Drop ALL | Drop some |
| allowPrivilegeEscalation | false (enforced) | false |
| seccompProfile | RuntimeDefault required | RuntimeDefault required |
| runAsUser | MustRunAsRange (namespace range) | MustRunAsNonRoot |
| Volume types | configMap, downwardAPI, emptyDir, PVC, projected, secret | Same + ephemeral |

Minimum compliant pod securityContext:
```yaml
securityContext:
  runAsNonRoot: true
  # Do NOT set runAsUser -- let OpenShift assign from namespace range
  seccompProfile:
    type: RuntimeDefault
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

PSA runs **in parallel** with SCCs. A pod must pass both. OpenShift auto-labels
namespaces with PSA levels matching the most privileged SCC available.

### 3. Helm 4 Is NOT Usable with ArgoCD on OpenShift (2026)

- Helm 4.0.0 released November 2025 with Server-Side Apply as default
- **OpenShift 4.19-4.21 still ships Helm 3** (web terminal bundles v3.17.1)
- **ArgoCD (through v3.3 / GitOps 1.20) only supports Helm 3**
- Helm 3 EOL: bug fixes July 2026, security fixes November 2026
- **Recommendation**: use Helm 3 now, plan Helm 4 migration after ArgoCD adds support

### 4. DeploymentConfig Is Deprecated (OCP 4.14)

Use `Deployment` for all new work. For ImageStream triggers on Deployments:
```yaml
metadata:
  annotations:
    image.openshift.io/triggers: >-
      [{"from":{"kind":"ImageStreamTag","name":"myapp:latest"},
        "fieldPath":"spec.template.spec.containers[?(@.name==\"myapp\")].image"}]
```
Also set `lookupPolicy.local: true` on the ImageStream.

### 5. OpenShift SDN Removed in OCP 4.17

Must migrate to OVN-Kubernetes before upgrading. Key impacts:
- OVN reserves `100.64.0.0/16` and `100.88.0.0/16` (check for conflicts)
- MTU decreases by 50 bytes (OVN overlay overhead)
- Migration requires 2 node reboots (~double upgrade time)
- Egress policies that couldn't be enforced before now CAN be -- audit existing NetworkPolicies

### 6. cgroup v1 Removed in OCP 4.19

All nodes must run cgroup v2 before upgrading. cgroup v2 was the default for
new installs since 4.14, deprecated in 4.16.

### 7. Logging 6.0 Removes EFK Stack Entirely

Elasticsearch, Fluentd, and Kibana are gone. Replaced by LokiStack + Vector +
console UI plugin. Migration is NOT in-place -- deploy Loki/Vector in parallel,
run both stacks during retention window, then retire Elasticsearch.

## Container Image Essentials

### UBI Base Image Selection

| Variant | Size (~compressed) | Package Manager | Use Case |
|---------|-------------------|----------------|----------|
| `ubi9/ubi` | ~80 MB | dnf/yum | Builder stages, development |
| `ubi9/ubi-minimal` | ~36 MB | microdnf | Light runtime, need to install packages |
| `ubi9/ubi-micro` | ~12 MB | None | Production runtime (multi-stage required) |
| `ubi9/ubi-init` | ~80 MB | dnf/yum | systemd services (StopSignal: SIGRTMIN+3) |

**Recommendation**: UBI Micro for production runtime via multi-stage build.
UBI Minimal as builder stage. UBI Micro is preferred over `scratch` because
compliance scanners classify `scratch` images as unrecognizable.

UBI is freely redistributable without a Red Hat subscription.

### Multi-Stage Build Pattern

```dockerfile
# Stage 1: Build
FROM registry.access.redhat.com/ubi9/ubi-minimal:latest AS builder
RUN microdnf install -y --setopt=tsflags=nodocs --setopt=install_weak_deps=0 \
    golang && microdnf clean all
COPY . /src
WORKDIR /src
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/server

# Stage 2: Runtime
FROM registry.access.redhat.com/ubi9/ubi-micro:latest
COPY --from=builder --chown=1001:0 /app/server /app/server
RUN chmod g=u /app/server
USER 1001
EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

### Red Hat Container Certification Requirements

If certifying for the Red Hat Ecosystem Catalog:
- **Base image**: must use UBI or RHEL base
- **Required labels**: `name`, `vendor`, `version`, `release`, `summary`, `description`
- **Required directory**: `/licenses` with software terms
- **Layers**: max 40 (recommended 5-20)
- **Security**: no critical/important CVEs in Red Hat components (`dnf update-minimal --security --sec-severity=Important --sec-severity=Critical`)
- **Non-root**: recommended (required for restricted-v2 SCC)
- **Preflight checks**: RunAsNonRoot, BasedOnUBI, HasLicense, HasRequiredLabel, LayerCountAcceptable, HasNoProhibitedPackages, etc.
- **Recertification**: every 12 months or when critical CVE > 3 months old

See `references/container-images.md` for full details.

## Packaging Decision Matrix

| Format | When to Use | Limitations |
|--------|------------|-------------|
| **Helm** | Distribute to other teams/customers; values-driven config; OperatorHub Helm operators | Helm 3 only on OCP today; chart-verifier for certification |
| **Kustomize** | Same-team env overlays (dev/staging/prod); GitOps prerequisite | No templating logic; `oc apply -k` does NOT support `--enable-helm` |
| **Helm + Kustomize** | Dominant hybrid: Helm for packaging, Kustomize for env patches | Requires `--enable-helm` flag (only works in `kustomize build` or ArgoCD) |
| **Operator (Go)** | Stateful apps needing Day-2 ops (backup/restore/scaling); L3-L5 maturity | Complex to develop; Operator SDK CLI deprecated in OCP 4.16 (upstream continues) |
| **Operator (Helm)** | Simple operators for OperatorHub distribution | Limited to L1-L2 capability maturity |
| **OLM v1 ClusterExtension** | Install operators on OCP 4.18+ | Requires user-provided ServiceAccount + RBAC; AllNamespaces only |
| **OpenShift Templates** | Legacy only (NOT recommended for new work) | Not portable to vanilla K8s; Template Service Broker removed in 4.4 |

### Helm on OpenShift -- Key Patterns

Detect OpenShift at template time:
```yaml
{{- define "mychart.isOpenshift" -}}
{{- if .Capabilities.APIVersions.Has "security.openshift.io/v1" -}}true{{- end -}}
{{- end -}}
```

Conditional Route vs Ingress:
```yaml
{{- if .Capabilities.APIVersions.Has "route.openshift.io/v1" }}
apiVersion: route.openshift.io/v1
kind: Route
{{- else }}
apiVersion: networking.k8s.io/v1
kind: Ingress
{{- end }}
```

SCC-compatible values (let OpenShift assign UIDs):
```yaml
securityContext:
  runAsUser: null    # Do NOT hardcode
  fsGroup: null      # Do NOT hardcode
  runAsNonRoot: true
```

See `references/packaging-formats.md` for OLM v1, Kustomize patterns, and
certified chart requirements.

## Additional References

| Reference | Contents |
|-----------|----------|
| `references/container-images.md` | UBI variants, multi-stage builds, arbitrary UID, certification, Podman, ImageStreams |
| `references/packaging-formats.md` | Helm on OCP, OLM v1 RBAC, Kustomize overlays, certified operators/charts |
| `references/security.md` | SCC/PSA, supply chain (Sigstore/RHTAS/Conforma), secrets (ESO/Vault), FIPS, compliance, NetworkPolicy |
| `references/cicd-gitops.md` | Tekton Pipelines, Chains, Pipelines-as-Code, ArgoCD Agent, Shipwright, image promotion |
| `references/operations.md` | Routes/TLS, probes, HPA/KEDA/VPA, monitoring, logging, storage, sidecars, serverless, multi-arch |
| `references/gotchas.md` | Version timeline (4.14-4.21), DeploymentConfig migration, SDN removal, networking changes |
| `references/disconnected.md` | oc-mirror v2, registry mirroring, OCI GitOps, Tekton bundles, OSUS upgrades, air-gap patterns |
