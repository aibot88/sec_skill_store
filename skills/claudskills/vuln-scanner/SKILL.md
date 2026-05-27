---
name: vuln-scanner
description: 脆弱性スキャンスキル。CVE/依存関係脆弱性を検出し、npm audit/pip-audit/trivy等の結果を解析。セキュリティリスクの優先順位付けと修正提案を提供。
---

# Vuln Scanner

依存関係の脆弱性をスキャン・分析するスキル。CVEデータベースと照合し、セキュリティリスクを特定する。

## Node.js (npm audit)

### 基本実行

```bash
# 脆弱性スキャン
npm audit

# JSON形式で出力
npm audit --json

# 深度指定
npm audit --audit-level=moderate

# 自動修正
npm audit fix

# 破壊的変更を含む修正
npm audit fix --force
```

### 出力の解析

```bash
# 脆弱性の数
npm audit --json | jq '.metadata.vulnerabilities'

# 深刻度別
npm audit --json | jq '.advisories | to_entries | group_by(.value.severity) | map({severity: .[0].value.severity, count: length})'

# 修正可能な脆弱性
npm audit --json | jq '.advisories | to_entries[] | select(.value.findings[0].paths != null) | .value.title'
```

### レポート例

```
# npm audit
found 3 vulnerabilities (1 low, 1 moderate, 1 critical)
- critical: Prototype Pollution in lodash
- moderate: ReDoS in debug
- low: Denial of Service in qs
```

## Python (pip-audit)

### インストール・実行

```bash
# インストール
pip install pip-audit

# 基本スキャン
pip-audit

# requirements.txtから
pip-audit -r requirements.txt

# JSON出力
pip-audit --format=json

# 脆弱性のみ表示
pip-audit --only-vuln
```

### Safety

```bash
# インストール
pip install safety

# スキャン
safety check

# requirements.txtから
safety check -r requirements.txt

# JSON出力
safety check --json
```

## コンテナ/インフラ (Trivy)

### インストール

```bash
# macOS
brew install trivy

# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
```

### 使用方法

```bash
# イメージスキャン
trivy image node:18

# ファイルシステムスキャン
trivy fs .

# 設定ファイルスキャン
trivy config .

# JSON出力
trivy image --format json --output results.json node:18

# 深刻度フィルタ
trivy image --severity HIGH,CRITICAL node:18
```

## Snyk

### インストール・実行

```bash
# インストール
npm install -g snyk

# 認証
snyk auth

# スキャン
snyk test

# JSON出力
snyk test --json

# 修正提案
snyk fix

# 継続的モニタリング
snyk monitor
```

## 脆弱性の分類

### CVSSスコア

| スコア | 深刻度 | 対応優先度 |
|--------|--------|-----------|
| 9.0-10.0 | Critical | 即時対応 |
| 7.0-8.9 | High | 24時間以内 |
| 4.0-6.9 | Medium | 1週間以内 |
| 0.1-3.9 | Low | 次回リリース |

### よくある脆弱性タイプ

| タイプ | CVE例 | 対応 |
|--------|-------|------|
| Prototype Pollution | CVE-2020-8203 | lodashアップデート |
| ReDoS | CVE-2017-16137 | 正規表現見直し |
| Path Traversal | CVE-2017-16119 | パス検証追加 |
| XSS | CVE-2020-28503 | サニタイゼーション |

## 修正優先順位付け

```bash
#!/bin/bash
echo "=== Vulnerability Summary ==="
npm audit --json > audit.json

critical=$(jq '.metadata.vulnerabilities.critical' audit.json)
high=$(jq '.metadata.vulnerabilities.high' audit.json)
moderate=$(jq '.metadata.vulnerabilities.moderate' audit.json)
low=$(jq '.metadata.vulnerabilities.low' audit.json)

echo "Critical: $critical"
echo "High: $high"
echo "Moderate: $moderate"
echo "Low: $low"

if [ "$critical" -gt 0 ] || [ "$high" -gt 0 ]; then
  echo "ACTION REQUIRED: Critical or High vulnerabilities found"
  exit 1
fi
```

## 修正手順

### 1. 影響範囲確認

```bash
# 影響を受けるパッケージの使用箇所
rg "lodash" package.json
rg "from 'lodash'" src/
```

### 2. 安全なアップデート

```bash
# パッチバージョン
npm update lodash

# メジャーバージョン（破壊的変更の可能性）
npm install lodash@latest
```

### 3. テスト実行

```bash
npm test
npm run build
```

### 4. 依存関係のロック

```bash
npm shrinkwrap
# または
npm ci
```

## CI統合

```yaml
# GitHub Actions
- name: Run npm audit
  run: npm audit --audit-level=high

- name: Run Trivy
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    severity: 'HIGH,CRITICAL'
```

## 例外処理

### 一時的な例外

```json
// .nsprc
{
  "exceptions": [
    "CVE-2020-12345"
  ]
}
```

### npm audit除外

```bash
# .npmrc
audit=false

# または特定の Advisory を除外
npm audit --omit=dev
```

## 定期的なスキャン

```bash
# cronジョブ例（毎日実行）
0 9 * * * cd /path/to/project && npm audit --audit-level=moderate > /var/log/audit.log
```
