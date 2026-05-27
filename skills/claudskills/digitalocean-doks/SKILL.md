---
name: digitalocean-doks
description: DigitalOcean Kubernetes (DOKS) disipline — cluster provisioning (HA control plane, VPC, surge upgrade, maintenance window), node pool design (auto-scale, multi-pool, label/taint, dedicated vs shared CPU), networking (DO Load Balancer annotation, Cilium NetworkPolicy, proxy protocol), storage (DO Block Storage RWO, Spaces RWX), security (PAT scope, kubeconfig rotation, audit log), observability (DO Monitoring + Prometheus), cost (LB bandwidth, block storage, egress), backup (Velero + Spaces), CI/CD (doctl + DOCR), DR drill, K8s sürüm yönetimi.
---

# DigitalOcean Kubernetes (DOKS)

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md`
default-load sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı
**Critical / High / Medium / Low + kanıt** formatında olmak zorunda — spekülatif
Critical yasak. Sahiplik dışı bulgu ilgili agent'a delege; karar yetkisi eşiği
aşılırsa **kullanıcı onayı zorunlu**.

## Felsefe

- **HA control plane prod zorunlu** — $40/ay maliyeti, SLA temeli.
- **VPC önce yarat** — cluster sonra; cross-region migrate yok.
- **Auto-upgrade kapalı, maintenance window sabit** — sürprize kapalı.
- **Surge upgrade aç** — downtime'sız node rotation.
- **PDB doğru kurulmazsa Cluster-Autoscaler takılır** — eviction tuzağı.
- **DOCR + DOKS image pull secret managed** — manual token YASAK.
- **DO API rate limit gerçek** — CI exponential backoff.

## Ne Zaman Kullanılır

- Yeni DOKS cluster provisioning (greenfield)
- Mevcut DOKS audit (sürüm, node pool, security, cost)
- K8s sürüm upgrade plan (N-2 destekli, maintenance window)
- Node pool tasarımı (general / apps / gpu / spot ayırımı)
- DO Load Balancer + ingress-nginx entegrasyonu
- NetworkPolicy bootstrap (Cilium)
- DOCR image pull + private registry
- Multi-environment topology (prod/staging/dev VPC ayrımı)
- Velero + Spaces backup kurulum
- DR drill (RTO/RPO doğrulama)
- Cost optimization (over-provisioned PVC, LB bandwidth)
- AWS/GCP'den DOKS'a migrasyon

## Workflow

### 1) Discovery

```bash
doctl kubernetes cluster list
doctl kubernetes cluster get <id> --format Name,Version,HA,Region,VPCUUID,NodePools,Status
doctl kubernetes cluster node-pool list <cluster-id>
doctl compute load-balancer list
doctl databases list
kubectl get nodes -o wide
kubectl get pods -A | grep -E 'cilium|nginx|cert-manager|external-dns'
```

### 2) Cluster posture audit

- **HA control plane**: prod cluster `ha = true` mı?
- **Auto-upgrade**: kapalı + maintenance window tanımlı mı?
- **K8s sürüm**: N-2 destekli mi (DO release notes)?
- **VPC**: prod ayrı VPC mi? default VPC'de değil mi?
- **Surge upgrade**: aktif mi?
- **Maintenance window**: low-traffic UTC slot mu?

### 3) Node pool audit

- **Pool ayrımı**: default (general) + apps + ingress (taint) + gpu (varsa)?
- **Node size**: prod dedicated CPU (c-/m-/g-)? Shared (s-) prod'da yasak.
- **Auto-scale**: `min ≥ 2`, `max` capacity-plan'dan. PDB tutarlı mı?
- **Label/Taint**: workload izolasyonu (`role=apps`, `role=ingress`)?
- **Topology spread**: 3+ zone (region zone count'a bağlı)?

### 4) Networking

- **CNI**: Cilium aktif mi (yeni cluster default)?
- **NetworkPolicy**: prod namespace'lerde deny-default + allow-list yazılı mı?
- **DO Load Balancer annotation** doğru mu?

```yaml
# ingress-nginx svc örnek
service:
  annotations:
    service.beta.kubernetes.io/do-loadbalancer-protocol: "https"
    service.beta.kubernetes.io/do-loadbalancer-tls-passthrough: "false"
    service.beta.kubernetes.io/do-loadbalancer-certificate-id: "<uuid>"
    service.beta.kubernetes.io/do-loadbalancer-enable-proxy-protocol: "true"
    service.beta.kubernetes.io/do-loadbalancer-size-slug: "lb-small"
    service.beta.kubernetes.io/do-loadbalancer-redirect-http-to-https: "true"
```

- **Proxy protocol** ingress-nginx'te `use-proxy-protocol: "true"` set mi? (LB annotation + ingress config birlikte)
- **External-DNS**: DO provider, rate-limit batched mi?
- **cert-manager** Let's Encrypt staging + prod issuer ayrı mı?

### 5) Storage

- **PV provisioner**: `do-block-storage` default. RWX talebi varsa workload yanlış → Spaces (s3) veya managed DB.
- **PVC size**: over-provisioned mu? Resize policy var mı?
- **Snapshot**: scheduled mi (RPO doc'lu)?
- **Volume IOPS**: size'la lineer; DB workload için size up zorunlu.

### 6) Security

- **PAT scope** minimal mi? CI ayrı PAT mı?
- **kubeconfig** rotation ≤ 7 gün mü? Long-lived kubeconfig var mı?
- **VPC isolation** prod/staging/dev ayrı mı?
- **DOCR**: private mi? imagePullSecret managed (`doctl registry kubernetes-manifest`)?
- **Audit log** Spaces'e export var mı (SOC 2)?
- **Cluster admin** sayısı (≤ 3 öneri)?

### 7) Observability

- **DO Monitoring** node-level metric aktif mi?
- **Prometheus/Grafana** kuruldu mu? scrape conf?
- **Loki/Promtail** log aggregation?
- **kube-state-metrics + node-exporter** etiketli mi?
- **DOKS API rate limit** dashboard var mı?

### 8) Cost

```bash
doctl monitoring metrics droplet bandwidth --droplet-id <id>
doctl compute load-balancer get <id> --format SizeSlug,Status,Region
doctl compute volume list --format Name,SizeGigaBytes,Region,DropletIDs
```

- HA CP $40 → prod justified.
- Node hourly: cluster-autoscaler shrink doğru mu (min ≥ 2 kalır)?
- LB egress: 1TB free; sonra $0.01/GB → CDN ile düşür.
- Block storage: over-provisioned PVC?
- Cross-region egress: cost rapor.

### 9) Backup / DR

- **Velero + Spaces**: schedule (daily/weekly), retention (30g), namespace selector.
- **Restore drill**: quarterly, RTO/RPO doğrulanmış mı?
- **Managed DB backup**: DO managed Postgres PITR var, restore drill?

### 10) CI/CD

- **doctl-actions** kubeconfig çek (token rotation 7g).
- **DOCR push** + ImagePullSecret managed.
- **Rollout** `RollingUpdate maxSurge 25% maxUnavailable 0`.
- **PDB**: `minAvailable: 1` (replicas 2+).

### 11) Findings + Action Items

Critical / High / Medium / Low + kanıt + sahip + tarih + projected impact.

## Antipatterns

- **Single control plane prod** (SPOF + no SLA).
- **Auto-upgrade aç + maintenance window yok** (sürpriz CrashLoop).
- **Default VPC prod** (network isolation yok).
- **Shared CPU (s-*) prod** (CPU steal noise).
- **PDB yok + auto-scale aç** (eviction takılır).
- **NetworkPolicy yok** prod.
- **DOCR public** prod image.
- **kubeconfig long-lived** (rotation yok).
- **LB SSL Passthrough + ingress TLS** çift termine.
- **RWX talep eden workload** (DO Block Storage RWO; mimari değişmeli).
- **External-DNS rate-limit ignore** (DO API throttle).
- **`latest` tag** prod.
- **Cluster admin 10+ kişi**.
- **Velero yok** prod.
- **Maintenance window prime-time**.
- **DOKS audit log Spaces'e yok** (compliance fail).

## Delege

- `kubernetes-troubleshooting` skill — pod crash, eviction tuzağı.
- `infrastructure-implementer` — manifest + IaC değişikliği.
- `iac-engineer` — Terraform DO provider modülü.
- `observability-engineer` — Prometheus/Loki scrape.
- `security-reviewer` — PAT, audit log, VPC isolation.
- `finops-review` skill — bandwidth + LB + PVC cost.
- `deployment-strategist` — rollout + PDB + drain.

## Çıktı şablonu

```markdown
# DOKS Review: prod-cluster

## Current state
- Region: fra1, K8s 1.30.5, HA: yes
- VPC: vpc-prod-fra1 (özel)
- Node pools: default (3x c-4), apps (5x c-8), ingress (2x s-2)
- Auto-upgrade: off, maintenance Sun 03:00 UTC, surge: on
- LB: 1x lb-small ($12 + bandwidth)

## Findings
- **Critical**: ingress pool shared CPU (s-2) → CPU steal p99 spike
- **Critical**: NetworkPolicy yok prod namespace
- **High**: PDB yok 4 deployment → autoscaler eviction takılıyor
- **High**: kubeconfig 90-day token (rotation 7g önerilir)
- **Medium**: Velero yok
- **Medium**: DOKS audit log Spaces'e değil (SOC 2 fail)
- **Low**: 3 PVC over-provisioned (160GB used 28GB)

## Action items
| P0 | NetworkPolicy deny-default + allow | @platform | 2026-05-18 |
| P0 | ingress pool s-2 → c-4 | @platform | 2026-05-20 |
| P1 | PDB minAvailable 1 (4 deploy) | @platform | 2026-05-23 |
| P1 | kubeconfig rotation 7g + CI ayrı PAT | @security | 2026-05-23 |
| P2 | Velero + Spaces backup | @platform | 2026-06-06 |
| P2 | Audit log Spaces export | @security | 2026-06-13 |
| P3 | PVC resize 3 volume | @platform | 2026-06-20 |
```
