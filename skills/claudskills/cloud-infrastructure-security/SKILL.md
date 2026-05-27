---
name: cloud-infrastructure-security
description: |
  雲端基礎設施安全檢查清單與最佳實踐。
  Use when: 部署到雲端平台、配置 IAM、設定 CI/CD pipeline、實作 IaC、配置監控或管理 secrets。
  Triggers: "cloud security", "IAM policy", "CI/CD security", "Terraform security", "Cloudflare WAF", "雲端安全", "基礎設施安全".
---

# Cloud & Infrastructure Security Skill | 雲端基礎設施安全

確保雲端基礎設施、CI/CD pipeline 與部署配置遵循安全最佳實踐並符合業界標準。

## 適用情境

- 部署應用程式到雲端平台（AWS, Vercel, Railway, Cloudflare）
- 配置 IAM 角色與權限
- 設定 CI/CD pipeline
- 實作基礎設施即程式碼（Terraform, CloudFormation）
- 配置日誌與監控
- 管理雲端環境中的 secrets
- 設定 CDN 與邊緣安全
- 實作災難復原與備份策略

---

## 雲端安全檢查清單

### 1. IAM 與存取控制

#### 最小權限原則

```yaml
# ✅ 正確：最小權限
iam_role:
  permissions:
    - s3:GetObject  # 只有讀取權限
    - s3:ListBucket
  resources:
    - arn:aws:s3:::my-bucket/*  # 特定 bucket

# ❌ 錯誤：過度寬鬆的權限
iam_role:
  permissions:
    - s3:*  # 所有 S3 動作
  resources:
    - "*"  # 所有資源
```

#### 驗證步驟

- [ ] 生產環境不使用 root 帳號
- [ ] 所有特權帳號啟用 MFA
- [ ] 服務帳號使用角色，非長期憑證
- [ ] IAM policy 遵循最小權限
- [ ] 定期進行存取審查
- [ ] 未使用的憑證已輪替或移除

---

### 2. Secrets 管理

#### 雲端 Secrets Manager

```typescript
// ✅ 正確：使用雲端 secrets manager
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManager({ region: 'us-east-1' });
const secret = await client.getSecretValue({ SecretId: 'prod/api-key' });
const apiKey = JSON.parse(secret.SecretString).key;

// ❌ 錯誤：硬編碼或僅在環境變數
const apiKey = process.env.API_KEY; // 不輪替，不審計
```

#### 驗證步驟

- [ ] 所有 secrets 存放在雲端 secrets manager
- [ ] 資料庫憑證啟用自動輪替
- [ ] API keys 至少每季輪替
- [ ] 程式碼、日誌或錯誤訊息中沒有 secrets
- [ ] 啟用 secret 存取審計日誌

---

### 3. 網路安全

#### VPC 與防火牆配置

```terraform
# ✅ 正確：限制的安全群組
resource "aws_security_group" "app" {
  name = "app-sg"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # 僅內部 VPC
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # 僅 HTTPS 出站
  }
}

# ❌ 錯誤：對網際網路開放
resource "aws_security_group" "bad" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # 所有 port，所有 IP！
  }
}
```

#### 驗證步驟

- [ ] 資料庫非公開存取
- [ ] SSH/RDP port 限制為 VPN/bastion
- [ ] 安全群組遵循最小權限
- [ ] 配置 Network ACLs
- [ ] 啟用 VPC flow logs

---

### 4. 日誌與監控

#### CloudWatch/Logging 配置

```typescript
// ✅ 正確：完整的日誌
const logSecurityEvent = async (event: SecurityEvent) => {
  await cloudwatch.putLogEvents({
    logGroupName: '/aws/security/events',
    logStreamName: 'authentication',
    logEvents: [{
      timestamp: Date.now(),
      message: JSON.stringify({
        type: event.type,
        userId: event.userId,
        ip: event.ip,
        result: event.result,
        // 永不記錄敏感資料
      })
    }]
  });
};
```

#### 驗證步驟

- [ ] 所有服務啟用 CloudWatch/logging
- [ ] 記錄失敗的驗證嘗試
- [ ] 審計管理員動作
- [ ] 配置日誌保留期（合規要求 90+ 天）
- [ ] 配置可疑活動警報
- [ ] 日誌集中且防篡改

---

### 5. CI/CD Pipeline 安全

#### 安全的 Pipeline 配置

```yaml
# ✅ 正確：安全的 GitHub Actions workflow
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read  # 最小權限

    steps:
      - uses: actions/checkout@v4

      # 掃描 secrets
      - name: Secret scanning
        uses: trufflesecurity/trufflehog@main

      # 依賴審計
      - name: Audit dependencies
        run: npm audit --audit-level=high

      # 使用 OIDC，非長期 token
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: us-east-1
```

#### 驗證步驟

- [ ] 使用 OIDC 取代長期憑證
- [ ] Pipeline 中進行 secrets 掃描
- [ ] 依賴漏洞掃描
- [ ] Container image 掃描（如適用）
- [ ] 強制分支保護規則
- [ ] 合併前需要程式碼審查
- [ ] 強制簽署提交

---

### 6. Cloudflare & CDN 安全

#### Cloudflare 安全配置

```typescript
// ✅ 正確：帶安全標頭的 Cloudflare Workers
export default {
  async fetch(request: Request): Promise<Response> {
    const response = await fetch(request);

    const headers = new Headers(response.headers);
    headers.set('X-Frame-Options', 'DENY');
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    headers.set('Permissions-Policy', 'geolocation=(), microphone=()');

    return new Response(response.body, {
      status: response.status,
      headers
    });
  }
};
```

#### 驗證步驟

- [ ] WAF 啟用 OWASP 規則
- [ ] 配置速率限制
- [ ] 啟動 Bot 防護
- [ ] 啟用 DDoS 防護
- [ ] 配置安全標頭
- [ ] 啟用 SSL/TLS strict 模式

---

### 7. 備份與災難復原

#### 自動備份

```terraform
# ✅ 正確：自動 RDS 備份
resource "aws_db_instance" "main" {
  allocated_storage     = 20
  engine               = "postgres"

  backup_retention_period = 30  # 30 天保留
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql"]

  deletion_protection = true  # 防止意外刪除
}
```

#### 驗證步驟

- [ ] 配置自動每日備份
- [ ] 備份保留符合合規要求
- [ ] 啟用時間點復原
- [ ] 每季進行備份測試
- [ ] 災難復原計畫已文件化
- [ ] RPO 和 RTO 已定義並測試

---

## 部署前雲端安全檢查清單

任何生產雲端部署前：

- [ ] **IAM**：不使用 root 帳號、啟用 MFA、最小權限 policy
- [ ] **Secrets**：所有 secrets 在雲端 secrets manager 並輪替
- [ ] **網路**：安全群組受限、無公開資料庫
- [ ] **日誌**：CloudWatch/logging 啟用並設定保留
- [ ] **監控**：配置異常警報
- [ ] **CI/CD**：OIDC 認證、secrets 掃描、依賴審計
- [ ] **CDN/WAF**：Cloudflare WAF 啟用 OWASP 規則
- [ ] **加密**：靜態和傳輸中資料已加密
- [ ] **備份**：自動備份並測試過復原
- [ ] **合規**：符合 GDPR/HIPAA 要求（如適用）
- [ ] **文件**：基礎設施已文件化、runbooks 已建立
- [ ] **事件回應**：安全事件計畫已就位

---

## 常見雲端安全配置錯誤

### S3 Bucket 曝露

```bash
# ❌ 錯誤：公開 bucket
aws s3api put-bucket-acl --bucket my-bucket --acl public-read

# ✅ 正確：私有 bucket 並指定存取
aws s3api put-bucket-acl --bucket my-bucket --acl private
aws s3api put-bucket-policy --bucket my-bucket --policy file://policy.json
```

### RDS 公開存取

```terraform
# ❌ 錯誤
resource "aws_db_instance" "bad" {
  publicly_accessible = true  # 永遠不要這樣做！
}

# ✅ 正確
resource "aws_db_instance" "good" {
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.db.id]
}
```

---

## 參考資源

- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [Cloudflare Security Documentation](https://developers.cloudflare.com/security/)
- [OWASP Cloud Security](https://owasp.org/www-project-cloud-security/)
- [Terraform Security Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/)

**記住**：雲端配置錯誤是資料外洩的主要原因。單一曝露的 S3 bucket 或過度寬鬆的 IAM policy 可能危及整個基礎設施。永遠遵循最小權限原則與縱深防禦。
