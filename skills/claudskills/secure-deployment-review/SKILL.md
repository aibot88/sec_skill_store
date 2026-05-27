---
name: secure-deployment-review
description: Container, K8s, CI/CD ve runtime security review.
---

# Secure Deployment Review

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md` default-load
sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı **Critical / High / Medium /
Low + kanıt** formatında olmak zorunda — spekülatif Critical yasak. Sahiplik dışı bulgu
ilgili agent'a delege; karar yetkisi eşiği aşılırsa **kullanıcı onayı zorunlu**.

## Ne Zaman Kullanılır
- Yeni servis prod'a alınıyor
- Quarterly audit
- Security incident sonrası hardening
- Compliance prep (SOC2/ISO/PCI)

## Workflow
1. **Image**
   - Trivy/Grype scan; critical/high CVE listele
   - Pinned base, non-root, distroless tercih
   - SBOM üret (syft) ve sakla
2. **K8s**
   - kubesec/polaris/kube-score
   - PodSecurity admission `restricted`
   - NetworkPolicy default-deny + explicit allow
   - RBAC least privilege
   - ServiceAccount workload-spesifik
3. **Secret**
   - ESO / Vault / SOPS
   - Rotate prosedürü
   - Repo'da hardcoded (gitleaks)
4. **CI/CD**
   - Pipeline secret SCOPE'lu
   - Artifact imzalama (cosign)
   - Provenance (SLSA L2+)
   - Branch protection
5. **Runtime**
   - Falco/Tetragon kuralları
   - Pod logs PII redact
   - egress allowlist

## Checklist
- [ ] Image CVE scan CI'da gating
- [ ] Pinned base + signed
- [ ] Non-root, readonly fs
- [ ] NetworkPolicy default-deny
- [ ] PodSecurity restricted
- [ ] Secret manager (no hardcoded)
- [ ] RBAC minimal
- [ ] Pipeline OIDC (no static cloud cred)
- [ ] Artifact signed + provenance
- [ ] Audit log enable

## Antipattern
- `latest` tag prod
- Root user container
- `privileged: true` justify yok
- `hostNetwork`, `hostPID` justify yok
- ClusterRole `*` üzerine `*`
- CI'da static AWS_ACCESS_KEY env
- Secret base64'e tutup "şifreli" diye geçmek
- Telemetry'ye stack trace + PII
- Public S3 bucket / public Postgres

## Örnek Agent Davranışı
```
User: /security-audit deploy
Agent:
1. trivy image api:1.42 -> 2 critical, 5 high
2. kubesec deploy.yaml -> runAsNonRoot eksik, capabilities drop yok
3. NetworkPolicy yok namespace production
4. RBAC: api-sa ClusterRole get pods (gereksiz, namespaced'e indir)
5. Rapor (severity sıralı) + fix önerileri
```

## Çıktı Formatı
```markdown
# Secure Deploy Review: <scope>

## Critical/High/Medium/Low
## Fix önerileri (kanıt + komut/diff)
## Compliance mapping (CWE/OWASP/CIS)
```
