---
name: iac-review
description: Terraform / Pulumi / CloudFormation review — state management, module contract, plan output, drift detection, security scan (tfsec/checkov/OPA), cost diff (Infracost). Plan ≠ apply disiplini.
---

# IaC Review

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md` default-load
sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı **Critical / High / Medium /
Low + kanıt** formatında olmak zorunda — spekülatif Critical yasak. Sahiplik dışı bulgu
ilgili agent'a delege; karar yetkisi eşiği aşılırsa **kullanıcı onayı zorunlu**.

## Ne Zaman Kullanılır
- IaC PR review (yeni resource / değişiklik)
- Yeni module yazımı
- State migration planı
- Drift detection alarm
- Security scan bulgu inceleme (tfsec/checkov)
- Multi-env refactor
- Cost engineering

## Workflow

### 1) Tool tespit
| Tool | İşaret |
|---|---|
| Terraform | `*.tf`, `terraform.tfstate*`, `.terraform.lock.hcl` |
| Pulumi | `Pulumi.yaml`, `Pulumi.<stack>.yaml` |
| CloudFormation | `*.yaml`/`*.json` `AWSTemplateFormatVersion` |
| Ansible | `playbook.yml`, `inventory/`, `roles/` |
| AWS CDK | `cdk.json`, `bin/`, `lib/*.ts` |

### 2) State management review
- **Remote backend** mu? Local state **fail**.
- **Locking** (DynamoDB / GCS object lock).
- **Encryption at rest** (KMS / SSE-S3).
- **Versioning** açık (state geri alma için).
- **Per-env ayrı state** (dev/staging/prod karışmıyor).
- **Workspace vs directory** — directory tercih (clarity).

### 3) Module contract review
- `variables.tf` input + `outputs.tf` output explicit.
- `versions.tf` Terraform + provider versiyonu pin.
- `variable` validation block (tip + range + regex).
- `default` değer verilirken comment.
- Module source `?ref=v1.2.0` semver pin (mutable ref yasak).

### 4) Plan output review
PR description'da `terraform plan` zorunlu:
```text
Plan: 3 to add, 1 to change, 0 to destroy.
```

- **`to destroy > 0`** → highlight + 2-person review.
- **`prevent_destroy = false` ihlali** → block.
- **Sensitive resource** (DB, KMS, prod K8s) → ek onay.
- **Provider/region değişimi** → state migration ayrı PR.

### 5) Resource hijyeni
- **Naming**: `<env>-<service>-<purpose>` convention.
- **Tag/label** zorunlu: Environment, Service, ManagedBy, Owner, CostCenter.
- **Lifecycle**:
  - `prevent_destroy = true` DB/KMS/VPC.
  - `create_before_destroy = true` zero-downtime.
  - `ignore_changes` minimum (drift kaynağı).
- **`for_each` > `count`** (stable address).
- **Provider alias** multi-region explicit.

### 6) Secret review
- **State'te plaintext**: `random_password`, `local_file` → state encryption şart.
- **`*.tfvars` Git'te**: `terraform.tfvars` `.gitignore`'da olmalı; sample
  `terraform.tfvars.example` OK.
- **`TF_VAR_*`** ENV preferred runtime için.
- **Vault provider** secret reference; plaintext yok.
- **CI'da OIDC federation** (AWS / GCP); long-lived access key yok.

### 7) Security scan
| Tool | Kapsam |
|---|---|
| **tfsec** | TF-specific, hızlı, CIS/HIPAA/PCI rule set |
| **checkov** | Multi-IaC, geniş policy (1k+ check) |
| **kics** | Multi-IaC, KICS query language |
| **OPA + Conftest** | Custom policy (organization-specific) |
| **Sentinel** | TF Cloud paid, policy-as-code |

Severity threshold:
- **Critical** → block PR (örn. public S3 bucket, security group `0.0.0.0/0` to all ports).
- **High** → review + plan eklenir.
- **Medium** → ticket, follow-up.

### 8) Drift detection
- **`terraform plan` cron** (haftalık) — drift varsa alert.
- **AWS Config / GCP Asset Inventory** — gerçek state karşılaştırma.
- **Drift sebepleri**:
  - Console click (insan).
  - Auto-scaling / managed service değişimi (beklenen).
  - 3rd party tool (Crossplane, Operator).
- **Reconcile**: state'e adapte (`terraform import` / `state mv`) veya
  config'e ekle (`ignore_changes` precise).

### 9) Cost diff (Infracost)
- PR comment: `Δ cost / month`.
- `> $100/ay` artış → review + justification.
- Idle resource detection (gauge unused).

### 10) Module test
- **terratest** (Go) — apply + assert + destroy.
- **`terraform test`** (1.6+) — declarative.
- **Kitchen-terraform** (Ruby).
- Ayrı test AWS account / GCP project — prod'a bulaşma yok.

## Checklist
- [ ] Remote backend + locking + encryption + versioning
- [ ] Per-env ayrı state
- [ ] Module contract (variables/outputs/versions)
- [ ] Module source semver pin (`?ref=v1.2.0`)
- [ ] Plan output PR'a yapışık
- [ ] `to destroy` highlight + onay
- [ ] Tag/label zorunlu
- [ ] `prevent_destroy` kritik resource'larda
- [ ] Secret state encryption + tfvars Git dışı
- [ ] tfsec/checkov clean (Critical=0)
- [ ] OPA/Conftest custom policy (varsa)
- [ ] Cost diff (Infracost) PR'a yapışık
- [ ] Drift detection cron aktif
- [ ] Module test (terratest / terraform test)

## Antipattern
- **Local state**.
- **`master`/`main` ref** module source.
- **`-auto-approve`** rutin.
- **State manuel `rm`/`mv`** review'sız.
- **Cross-env tek state**.
- **`*.tfvars` secret** Git'te.
- **`count = enabled ? 1 : 0`** boolean toggle.
- **`provisioner "local-exec"`** rutin.
- **`null_resource + local-exec`** state-driven olmayan.
- **`ignore_changes = all`**.
- **`-target`** apply rutin.
- **Console click** prod'da.
- **Module versiyon `latest`** prod'da.
- **Plan output review yok**.

## Örnek Agent Davranışı
```
User: /iac-review terraform/envs/prod/
Agent (iac-engineer):
1. Tool tespit: Terraform 1.6.4, AWS provider 5.x.
2. State: S3 backend + DynamoDB lock ✓; encryption KMS ✓; versioning ✓.
3. Module contract: 3 modül; `vpc` `master` ref kullanıyor (Critical, mutable).
4. Plan output:
   - Plan: 7 to add, 2 to change, 1 to destroy.
   - destroy: aws_db_instance.legacy → `prevent_destroy = false` (Critical).
5. Tag eksik: 4 resource'ta `CostCenter` yok (Medium).
6. Secret: `terraform.tfvars` `.gitignore`'da var ✓; `TF_VAR_DB_PASSWORD` CI ENV.
7. Security: tfsec 3 finding (1 High public S3 ACL, 2 Medium SG egress).
8. Cost: Infracost +$340/ay → RDS instance class büyütüldü.
9. Output:
   - Critical: vpc module ref pin + DB prevent_destroy + S3 ACL
   - High: SG egress
   - Medium: tag eksik 4 resource
   - 8 issue açıldı (sahip + tarih).
```

## Çıktı Formatı
```markdown
# IaC Review: <path>

## State / Backend
- Remote, locking, encryption, versioning, per-env

## Module Contract
- variables / outputs / versions / source pin

## Plan Output
```text
Plan: ... to add, ... to change, ... to destroy
```

## Critical / High / Medium / Low

## Security Scan
- tfsec / checkov / OPA özet

## Cost Diff (Infracost)
- Δ $/ay

## Action Items
| Öncelik | Aksiyon | Sahip | Bitiş | Issue |
```
