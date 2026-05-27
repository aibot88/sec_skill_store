---
name: k8s-supply-chain-and-image-hardening
description: Use when hardening the container image and enforcing supply-chain integrity for a Kubernetes workload after security and operations have decided the image-trust, scanning, and provenance posture. Produces minimal non-root read-only-root-FS images with dropped capabilities, image signing (cosign), SBOM generation (Syft), vulnerability scanning (Trivy/Grype) as a required gate, and admission-control policy (Kyverno/Gatekeeper) enforcing signed-image, non-root, and digest-pinned requirements at the cluster. This is the archetype-scoped successor to the security-context slice of the omnibus. Do not use for base manifest authoring, network/identity policy, autoscaler tuning, observability wiring, the CI pipeline that runs the gate, or cluster provisioning; use the other Family G archetype skills (pipeline wiring is the CI stack; cluster provisioning is out of family).
---

# Kubernetes Supply Chain and Image Hardening

## When to use

Invoke when hardening a workload's container image, establishing the signing/SBOM/scan gate, or authoring the admission policy that enforces image trust at the cluster — or when auditing an inherited workload running unsigned, root, or unscanned images. This skill owns the *hardening and enforcement*; the security-context floor was set by the manifest archetype.

Do not use for: base manifest authoring (use `k8s-workload-packaging-and-manifest`); NetworkPolicy/RBAC and the PSS namespace floor (use `k8s-network-and-identity-policy`); autoscaler tuning (use `k8s-scaling-and-resilience-topology`); metrics/log/trace wiring (use `k8s-observability-and-operations-readiness`); the CI pipeline that executes the scan/sign steps (owned by the `github-actions` stack — this skill defines the gate and the admission policy, not the workflow); cluster provisioning and control-plane setup (out of Family G — owned by the cloud platform stack and Terraform).

## Inputs

Required:

- A container image or build from the language packaging sub-skill, and the workload manifest set from `k8s-workload-packaging-and-manifest` (the security-context floor this skill hardens and the image this skill signs/scans).
- Approved `architecture/security` decisions on image-trust, scanning severity gate, and provenance posture, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/operations` decisions on the registry, signing-key custody, and attestation storage.
- The workload tier from `architecture-schema` (drives scan-severity gate strictness and signing requirement).
- The signing infrastructure (cosign keyless/OIDC vs key-pair) and the SBOM format (SPDX / CycloneDX).
- The admission engine in use (Kyverno / Gatekeeper) — consumed; PSS namespace floor is the network archetype's.
- The CI system (consumed: this skill defines the gate; the pipeline wiring is the CI stack's ownership).

## Operating rules

- Never generate tutorial-grade hardening. Assume the image will be attacked: a root container, a writable root FS, a critical CVE, or an unsigned image must all be impossible to deploy.
- Consume `architecture/security` and `architecture/operations`; do not invent decisions. Image-trust requirements, the scan severity gate, signing-key custody, and provenance posture are decisions made upstream. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- The image is minimal, non-root, read-only-root-FS, and capability-stripped. Distroless/scratch/minimal base, a non-root UID, `readOnlyRootFilesystem`, and `drop: [ALL]` are hard requirements — this skill hardens the floor the manifest archetype set; it does not merely restate it.
- Every promoted image is signed. cosign signature (keyless/OIDC preferred per the upstream key-custody decision); an unsigned image cannot be promoted. Signing is on the digest, not a mutable tag.
- An SBOM is generated and attached. Syft (or the upstream-named tool) produces an SBOM in the named format, attached/attested to the image digest so the dependency set is auditable post-deploy.
- Vulnerability scanning is a required gate, not a report. Trivy/Grype runs and fails the promotion at the upstream-defined severity threshold (tier-correct). A scan whose findings do not block promotion is decoration.
- Admission control enforces trust at the cluster, not just in CI. A Kyverno/Gatekeeper policy rejects unsigned images, root containers, mutable-tag images, and missing-digest references at admission — so a bypassed pipeline still cannot deploy an untrusted image. CI gates and admission are defense-in-depth, not either/or.
- The admission policy extends the PSS floor; it does not replace it. The `pod-security.kubernetes.io/enforce` namespace label is the network archetype's; this skill adds the signed-image / digest-pinned / provenance policies PSS does not cover. Name the boundary.
- Provenance is attestable. Where the upstream posture requires it, a build provenance attestation (SLSA-style) is produced and verified by the admission policy — not just a signature that proves who signed, but a record of how it was built.
- This skill owns image hardening + supply-chain enforcement + the admission policy. Base manifests, network/identity, scaling, observability, and the CI pipeline wiring are named handoffs, not implemented here.
- A workload whose admission policy has not been tested with a deliberately bad image (unsigned, root, mutable tag) that is correctly rejected is not done.

## Output contract

The generated hardening and enforcement MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — minimal non-root read-only-root-FS image, dropped capabilities, signed images, SBOM, scan-as-gate, admission enforcement of image trust.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — image signed and scanned before promotion; the gate blocks promotion; enforcement reproducible as policy manifests.
- [observability-standards](../../../../../standards/observability-standards/README.md) — admission rejections and scan-gate failures are observable (collection wiring handed off to the observability archetype).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — policy and attestation object names `kebab-case`, suffixed by kind when ambiguous.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives scan-severity gate strictness and the signing/provenance requirement.

Upstream contract: `architecture/security` is the source of truth for image-trust, scan gate, and provenance posture; `architecture/operations` is the source of truth for registry, key custody, and attestation storage. If a needed decision is missing, pause and raise an ADR candidate. Base manifests, network/identity, scaling, observability, and CI pipeline wiring are named handoffs.

## Progressive references

- Read `references/k8s-supply-chain-playbook.md` when hardening any owned area or checking the anti-pattern list.
- Read `references/k8s-supply-chain-quality-rubric.md` before declaring hardening complete.
- Use `assets/k8s-supply-chain.template.md` as the image / signing / SBOM / scan / admission pattern reference.

## Process

1. Gather context: load `architecture/security` (image-trust, scan severity gate, provenance) and `architecture/operations` (registry, key custody, attestation storage). Resolve the workload tier from `architecture-schema`. Confirm the image/build and the manifest security-context floor exist. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Harden the image: minimal base (distroless/scratch/minimal), explicit non-root UID, `readOnlyRootFilesystem`, `drop: [ALL]` capabilities, no shell/package-manager in the runtime layer where avoidable; reconcile with the manifest archetype's floor (harden, do not just restate).
3. Configure signing: cosign signing on the image digest using the upstream key-custody path (keyless/OIDC preferred); verification configuration for the admission policy.
4. Generate the SBOM: Syft (or upstream-named) in the named format (SPDX/CycloneDX), attached/attested to the digest.
5. Configure the vulnerability-scan gate: Trivy/Grype at the tier-correct severity threshold from `architecture/security`, defined to fail promotion (the gate definition — the pipeline that runs it is the CI stack's handoff).
6. Author the admission policy: Kyverno/Gatekeeper rules rejecting unsigned images, root containers, mutable-tag/non-digest references, and (where required) missing provenance — extending, not replacing, the PSS namespace floor.
7. Configure provenance where required: a build attestation (SLSA-style) produced and verified by the admission policy.
8. Verify: deploy a deliberately bad image (unsigned, then root, then mutable-tag) and confirm the admission policy rejects each; confirm a known-CVE image fails the scan gate; document any check that cannot run in the environment.
9. Emit the hardening + policy under `k8s/security/` plus `supply-chain.md` (image posture, signing/SBOM/scan gate, admission policy matrix, provenance) and the named handoff list. Validate against security-, deployment-, observability-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Hardened image spec: minimal base, non-root UID, read-only root FS, dropped capabilities.
- cosign signing configuration on the digest + verification config.
- SBOM in the named format, attached/attested to the digest.
- Vulnerability-scan gate definition at the tier-correct severity (fails promotion).
- Admission policy (Kyverno/Gatekeeper) rejecting unsigned/root/mutable-tag/missing-provenance images.
- Build-provenance attestation where the upstream posture requires it.
- `supply-chain.md` (image posture, gate, admission matrix, provenance) and the named handoff list.

Output rules:

- Functional, enforceable policy and image spec — not placeholder.
- An unsigned, root, or unscanned image cannot be promoted or admitted.
- The admission policy extends the PSS floor; it does not duplicate or replace the network archetype's namespace label.
- Base manifests, network/identity, scaling, observability, and CI pipeline wiring are handoffs, not implemented here.

## Quality checks

- [ ] The image uses a minimal base, a non-root UID, `readOnlyRootFilesystem`, and `drop: [ALL]` — hardened beyond the manifest archetype's floor.
- [ ] Every promoted image is cosign-signed on the digest via the upstream key-custody path; unsigned images cannot be promoted.
- [ ] An SBOM is generated in the named format and attached/attested to the image digest.
- [ ] A vulnerability scan runs at the tier-correct severity threshold and fails promotion on breach (gate, not report).
- [ ] An admission policy rejects unsigned images, root containers, and mutable-tag/non-digest references at the cluster.
- [ ] The admission policy extends the PSS namespace floor (owned by `k8s-network-and-identity-policy`) — it does not duplicate or replace it.
- [ ] Build provenance is produced and admission-verified where the upstream posture requires it.
- [ ] A deliberately bad image (unsigned / root / mutable-tag) is correctly rejected by admission, and a known-CVE image fails the scan gate, or the gap is documented.
- [ ] `supply-chain.md` documents image posture, the gate, the admission matrix, and provenance; base manifest/network/scaling/observability/CI-pipeline are named handoffs.

## References

- Upstream: [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/operations`](../../../../architecture/operations/SKILL.md).
- Builds on: [`k8s-workload-packaging-and-manifest`](../k8s-workload-packaging-and-manifest/SKILL.md) (security-context floor hardened here), [`dockerfile-and-jvm-tuning`](../dockerfile-and-jvm-tuning/SKILL.md) (image this skill signs/scans).
- Boundary: [`k8s-network-and-identity-policy`](../k8s-network-and-identity-policy/SKILL.md) owns the PSS namespace floor; this skill owns the extended admission policy.
- Holistic review pass: [`k8s-deploy-manifest-review`](../k8s-deploy-manifest-review/SKILL.md) (omnibus).
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
