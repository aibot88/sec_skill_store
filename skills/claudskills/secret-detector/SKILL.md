---
name: secret-detector
description: 機密情報検出スキル。APIキー、パスワード、トークン等の機密情報をコードから検出。git-secrets/truffleHog/gitleaks等のツールを統合。漏洩防止と早期発見に使用。
---

# Secret Detector

コードベースに含まれる機密情報を検出するスキル。APIキー、パスワード、シークレットトークン等の漏洩を防ぐ。

## 検出パターン

### よくある漏洩パターン

| 種類 | パターン例 |
|------|-----------|
| API Key | `sk-xxxx`, `AKIAxxxx`, `api_key = "xxx"` |
| AWS | `aws_access_key_id`, `aws_secret_access_key` |
| DB | `password = "xxx"`, `DB_PASSWORD` |
| JWT | `eyJ` で始まる長い文字列 |
| Private Key | `-----BEGIN RSA PRIVATE KEY-----` |

## gitleaks

### インストール

```bash
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
```

### 使用方法

```bash
# 現在のコードをスキャン
gitleaks detect --source . -v

# Git履歴も含めてスキャン
gitleaks detect --source . --log-opts="--all"

# JSON出力
gitleaks detect --source . --report-path findings.json --report-format=json

# 特定のコミット範囲
gitleaks detect --source . --log-opts="HEAD~10..HEAD"
```

### 設定ファイル (.gitleaks.toml)

```toml
title = "gitleaks config"

[[rules]]
id = "aws-access-key"
description = "AWS Access Key"
regex = '''AKIA[0-9A-Z]{16}'''
tags = ["aws", "key"]

[[rules]]
id = "github-token"
description = "GitHub Personal Access Token"
regex = '''ghp_[0-9a-zA-Z]{36}'''
tags = ["github", "token"]

[allowlist]
paths = [
  '''tests/.*''',
  '''\.env\.example''',
]
```

## truffleHog

### インストール

```bash
pip install trufflehog
```

### 使用方法

```bash
# Gitリポジトリをスキャン
trufflehog git https://github.com/user/repo

# ローカルディレクトリ
trufflehog filesystem .

# JSON出力
trufflehog filesystem . --json

# 除外パス
trufflehog filesystem . --exclude-paths="tests/,docs/"
```

## git-secrets

### セットアップ

```bash
# インストール
git clone https://github.com/awslabs/git-secrets
cd git-secrets
make install

# リポジトリに設定
cd /path/to/repo
git secrets --install
git secrets --register-aws
```

### パターン追加

```bash
# カスタムパターン
git secrets --add 'api_key\s*=\s*["\'][^"\']+["\']'
git secrets --add 'password\s*=\s*["\'][^"\']+["\']'

# 除外パターン
git secrets --add --allowed 'placeholder'
```

### スキャン実行

```bash
# 現在のファイルをスキャン
git secrets --scan

# ステージングされたファイル
git secrets --scan --staged

# 全履歴をスキャン
git secrets --scan-history
```

## detect-secrets (Python)

### インストール

```bash
pip install detect-secrets
```

### 使用方法

```bash
# ベースライン作成
detect-secrets scan > .secrets.baseline

# スキャン実行
detect-secrets scan --baseline .secrets.baseline .

# 監査（手動確認）
detect-secrets audit .secrets.baseline
```

## 正規表現パターン集

```bash
# grepで手動検出

# AWS Access Key
rg "AKIA[0-9A-Z]{16}" .

# AWS Secret Key
rg "(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+=]{40}['\"]" .

# GitHub Token
rg "ghp_[0-9a-zA-Z]{36}" .
rg "github_pat_[0-9a-zA-Z_]{82}" .

# Generic API Key
rg "(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"][0-9a-zA-Z_-]{20,}['\"]" .

# Password
rg "(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"][^'\"]+['\"]" .

# Private Key
rg "-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----" .

# JWT
rg "eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*" .
```

## 除外設定

### .gitleaks.toml

```toml
[allowlist]
paths = [
  '''\.env\.example''',
  '''tests/fixtures/.*''',
  '''docs/examples/.*''',
]

regexes = [
  "EXAMPLE_API_KEY",
  "your-api-key-here",
]
```

### .trufflehog.yaml

```yaml
skip_paths:
  - "tests/"
  - "docs/"
skip_detectors:
  - "PrivateKey"
```

## 検出時の対応

### 1. 即座の対応

```bash
# 漏洩したシークレットを無効化
# AWS: IAMコンソールでキーを削除/無効化
# GitHub: Settings > Developer settings > Personal access tokens で削除

# Git履歴からも削除（注意が必要）
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/file-with-secret' \
  --prune-empty --tag-name-filter cat -- --all
```

### 2. 安全な移行

```bash
# 環境変数を使用
# .env (gitignoreに追加)
API_KEY=real-api-key-here

# アプリケーションで読み込み
process.env.API_KEY
```

### 3. pre-commitフック

```bash
#!/bin/bash
# .git/hooks/pre-commit
git secrets --scan --staged
if [ $? -ne 0 ]; then
  echo "Secrets detected! Commit blocked."
  exit 1
fi
```

## CI統合

```yaml
- name: Check for secrets
  run: |
    gitleaks detect --source . --verbose --exit-code 1
```

## 定期スキャン

```bash
#!/bin/bash
# daily-secret-scan.sh
cd /path/to/project
gitleaks detect --source . --report-path /var/log/secrets-$(date +%Y%m%d).json
if [ $? -ne 0 ]; then
  # アラート送信
  curl -X POST $SLACK_WEBHOOK -d '{"text": "Secrets detected!"}'
fi
```
