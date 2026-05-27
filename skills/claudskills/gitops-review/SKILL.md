---
name: gitops-review
description: GitOps platform review — ArgoCD / Flux / Argo Rollouts. App-of-apps, sync policy, sealed-secrets, progressive delivery (canary/blue-green), drift, RBAC. K8s'in deploy katmanı disiplini.
---

# GitOps Review

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md` default-load
sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı **Critical / High / Medium /
Low + kanıt** formatında olmak zorunda — spekülatif Critical yasak. Sahiplik dışı bulgu
ilgili agent'a delege; karar yetkisi eşiği aşılırsa **kullanıcı onayı zorunlu**.

## Felsefe

GitOps = **Git tek truth + reconciliation loop**. Cluster state Git'i takip eder;
manuel `kubectl apply` **drift**, audit gap, rollback'i imkansızlaştırır.

- **Pull > push**. Cluster içindeki controller Git'i çeker; CI cluster'a push
  etmez (push secret leak yüzeyi).
- **Declarative**. Hedef state YAML'da; controller arayı kapatır.
- **Versiyonlu**. Her değişiklik Git commit; revert = `git revert`.
- **Self-healing**. Manuel müdahale geri alınır — drift detect+fix.
- **Auditability**. Git log = deploy audit log; "kim ne zaman deploy etti".

## Ne Zaman Kullanılır
- Yeni cluster bootstrap (ArgoCD / Flux kurulum)
- Application-of-applications pattern review
- Sync policy + auto-prune + self-heal kararları
- Sealed-secrets / SOPS / External Secrets entegrasyonu
- Progressive delivery (canary, blue-green) Argo Rollouts / Flagger
- Drift detection / reconciliation
- Multi-cluster / multi-tenant yapı
- RBAC + project boundaries
- Disaster recovery (Git → cluster restore)

## Workflow

### 1) Tool tespit
| Tool | İşaret |
|---|---|
| ArgoCD | `argoproj.io/v1alpha1` Application/AppProject CRD; `argo-cd` namespace |
| Flux | `toolkit.fluxcd.io/v1` GitRepository/Kustomization; `flux-system` namespace |
| Argo Rollouts | `argoproj.io/v1alpha1` Rollout (Deployment yerine) |
| Flagger | `flagger.app/v1beta1` Canary CRD |
| ArgoCD Image Updater | `argocd-image-updater` annotation |

### 2) Repository yapısı

#### App-of-apps (ArgoCD)
```text
gitops-repo/
├── apps/
│   ├── app-of-apps.yaml              # ana Application: tüm app'leri create eder
│   └── apps/
│       ├── api-svc.yaml              # Application
│       ├── checkout-svc.yaml
│       └── frontend.yaml
├── infrastructure/
│   ├── ingress-nginx.yaml
│   ├── cert-manager.yaml
│   ├── monitoring.yaml
│   └── ...
└── projects/
    ├── payments.yaml                  # AppProject (RBAC boundary)
    └── platform.yaml
```

#### Mono-repo vs multi-repo
- **App config** (Helm values, kustomize overlays) servis repo'sunda
  veya **ayrı GitOps repo**.
- **Recommended**: 1 GitOps repo per cluster veya per env.
- **Branching**: `main` = current state; environment branch'leri (`prod` branch)
  ya da **per-env directory** tercih.

### 3) Sync policy review

#### ArgoCD Application syncPolicy
```yaml
spec:
  syncPolicy:
    automated:
      prune: true            # Git'te silinen → cluster'dan da sil
      selfHeal: true         # manuel değişiklik → revert
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
      - ApplyOutOfSyncOnly=true
      - ServerSideApply=true # büyük CRD için
    retry:
      limit: 5
      backoff: { duration: 5s, factor: 2, maxDuration: 3m }
```

**Kararlar:**
- `automated.prune` — staging'de **on**; prod'da **dikkatli** (yanlışlıkla silme).
- `selfHeal` — drift'i kapatır; ama **acil müdahale** gereken incident'ta
  manual override'ı revert eder. Toggle planı dokumented olmalı.
- `CreateNamespace=true` — namespace YAML'da yoksa oluştur (genelde uygun).

### 4) Sealed-secrets / SOPS / External Secrets

| Tool | Felsefe |
|---|---|
| **Sealed-secrets** (Bitnami) | Public key encrypt; cluster controller decrypt. Git'te encrypted YAML. |
| **SOPS** (Mozilla) | KMS/age encrypt; Flux native, ArgoCD plugin. |
| **External Secrets Operator** | Vault/AWS SM/GCP SM'den çek; cluster'da Secret materialize. |

**Yasak**: plain `Secret` YAML Git'te. **Hardcode secret** = supply chain breach.

### 5) Progressive delivery

#### Argo Rollouts (canary)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: { duration: 5m }
        - setWeight: 25
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: api-svc-canary
        - pause: { duration: 5m }
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 100
      analysis:
        templates: [{templateName: success-rate-fast}]
        startingStep: 1
```

#### Analysis Template
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",code!~"5.."}[2m]))
            / sum(rate(http_requests_total{service="{{args.service-name}}"}[2m]))
```

**Kararlar:**
- **Step yüzdeleri**: 10/25/50/100 (yaygın) veya 5/25/50/100 (dikkatli).
- **Pause süre**: Analysis için yeterli sample (5-10 dk).
- **Abort eşik**: success rate < %99 → otomatik abort (failureLimit=3).
- **Manual gate**: prod'da analysis fail → manuel onay (auto-promote yasak).

### 6) Drift detection

- **ArgoCD `OutOfSync`** durumu — sync policy off ise alert.
- **Flux `Reconciliation Failed`** — controller log'u izle.
- **Diff**: `argocd app diff <app>` veya `flux diff kustomization <name>`.
- **Drift sebepleri**:
  - Manuel `kubectl apply` (insan).
  - Webhook controller (cert-manager, external-dns).
  - HPA, VPA (otomatik scale değişikliği — `ignoreDifferences` kullan).
- **`ignoreDifferences`** spesifik path için:
  ```yaml
  spec:
    ignoreDifferences:
      - group: apps
        kind: Deployment
        jsonPointers:
          - /spec/replicas         # HPA yönetiyor
  ```

### 7) RBAC + AppProject

ArgoCD `AppProject` = RBAC boundary:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: payments
spec:
  sourceRepos:
    - https://github.com/acme/gitops-payments.git
  destinations:
    - namespace: payments-*
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - { group: '', kind: Namespace }
  namespaceResourceBlacklist:
    - { group: '', kind: ResourceQuota }
  roles:
    - name: payments-deployer
      policies:
        - p, proj:payments:payments-deployer, applications, sync, payments/*, allow
      groups:
        - acme-org:payments-team
```

**Kurallar:**
- Default `*` repo veya `*` destination **yasak** prod'da.
- `clusterResourceWhitelist` minimum (Namespace/CRD).
- Role assign Git'te dokumented.

### 8) Disaster recovery

- **Cluster restore**: yeni cluster + ArgoCD/Flux + GitOps repo → reconcile.
- **Backup**: Velero stateful kaynaklar (PVC, Secret).
- **Drill**: 6 ayda bir cluster sıfırdan kur, restore süresi ölç.

### 9) Multi-cluster / multi-tenant

- **App-of-apps per cluster**: dev/staging/prod ayrı app-of-apps.
- **Single ArgoCD + multi-cluster**: cluster credential `Secret`.
- **Flux multi-tenancy**: `Kustomization` `serviceAccountName` per-tenant.

### 10) Observability

- ArgoCD: `argocd-server` Prometheus metric (`argocd_app_info`,
  `argocd_app_sync_total`).
- Flux: `gotk-` metric.
- Alert: `argocd_app_health` `Degraded` veya `OutOfSync` > 5 dk.
- Dashboard: app health grid, sync history.

## Checklist
- [ ] App-of-apps pattern (veya equivalent)
- [ ] Per-env ayrı yapı (dev/staging/prod)
- [ ] Sync policy explicit (`prune` + `selfHeal` toggle planı)
- [ ] Sealed-secrets / SOPS / External Secrets — plain Secret yok
- [ ] Progressive delivery (canary/blue-green) prod'da
- [ ] Analysis template + abort eşik
- [ ] Drift alert (`OutOfSync` > 5 dk)
- [ ] `ignoreDifferences` minimum + dokumented
- [ ] RBAC: AppProject + role + group binding
- [ ] DR plan: cluster restore drill
- [ ] Multi-cluster yapı dokumented
- [ ] Observability: metric + dashboard + alert
- [ ] `kubectl apply` manuel **yasak** (drift kaynağı)

## Antipattern
- **Manuel `kubectl apply`** — Git'i atla, drift garanti.
- **Plain `Secret`** Git'te — supply chain breach.
- **`autoSync` off + manual sync** — GitOps amacı kayıp.
- **`ignoreDifferences = all`** — drift invisible.
- **Auto-promote canary** — analysis fail'de prod'a girer.
- **`*` repo / `*` destination** AppProject'te — RBAC etkisiz.
- **Branching environment** (env=branch) — mono-repo'da divergence; per-env directory tercih.
- **Mono-cluster ArgoCD** prod'a + dev'e — blast radius büyük.
- **Sealed-secrets master key Git'te** — yenisi çıksa yine encrypt; eski'sini revoke.
- **DR drill yok** — cluster destroyed → Git OK ama state restore yok (Velero).
- **Argo Rollouts step % 0/100** — canary değil, regular rolling.
- **Analysis success rate sadece HTTP 200** — slow request'i sayar, p99 latency dahil olmalı.

## Örnek Agent Davranışı
```
User: /gitops-review apps/
Agent (platform-engineer):
1. Tool tespit: ArgoCD + Argo Rollouts + sealed-secrets.
2. Repo yapı: app-of-apps ✓, per-env directory (dev/staging/prod) ✓.
3. Sync policy: prod app'lerinde `selfHeal: true` — incident sırasında
   manuel override'ı revert eder (High; toggle planı eksik).
4. Sealed-secrets: 14 SealedSecret Git'te ✓; ama `Secret` plain 2 yerde
   `apps/legacy/*` (Critical — supply chain).
5. Argo Rollouts: api-svc canary 10/50/100 (3 step, çok hızlı); abort eşik
   manual (auto fail yok). Önerilen: 5/25/50/100 + `failureLimit: 3`.
6. Drift: `ignoreDifferences = all` 3 app'te (`monitoring`, `cert-manager`,
   `legacy-billing`) — invisible drift.
7. RBAC: AppProject `default` her şey allow ediyor — namespace + repo
   whitelist'e geç.
8. DR: drill kayıt yok — quarter'da bir restore drill öner.
9. Output: 3 Critical + 5 High + 4 Medium issue + diff özet.
```

## Çıktı Formatı
```markdown
# GitOps Review: <repo>

## Tool / Yapı
- ArgoCD/Flux + version + repo layout

## Sync Policy
- prune / selfHeal / retry / serverSideApply tablosu

## Critical / High / Medium / Low

## Diff (özet)
```yaml
# fix snippet
```

## Action Items
| Öncelik | Aksiyon | Sahip | Bitiş | Issue |
```
