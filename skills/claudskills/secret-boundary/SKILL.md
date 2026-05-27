---
name: secret-boundary
description: AI実行環境のシークレット境界設定。settings.json permissions.denyルールを生成し、シークレットへの事故的アクセスを防止する。
allowed-tools: Bash, Read, Write, Edit
argument-hint: "[baseline|audit] [options]"
---

# secret-boundary

AI実行環境のシークレット境界を設定する。

> **重要: このスキルが提供するのは「事故防止のガードレール」です。**
>
> `permissions.deny`はAIエージェントの事故的なシークレット読み取りを防ぎますが、
> 強制的なセキュリティ境界ではありません（ユーザー自身が変更可能なため）。
> 強制力が必要な場合はmanaged settingsとsandboxを併用してください。
>
> **このスキルでは守れないもの:**
> - 悪意ある攻撃者による意図的な回避（`cat .env`、`python -c "open('.env').read()"`等）
> - 環境変数に展開済みのシークレット（`op run`等で注入されたもの）
> - sandbox外のファイルシステムアクセス

## モード

### baseline（メインモード）

プロジェクト構造を分析し、適切なセキュリティ設定を生成する。

#### Step 1: プロジェクト走査

プロジェクト構造を確認し、シークレットが存在しうる場所を特定する:

```bash
# リポジトリ内のシークレット候補ファイルを検出
# 値は一切読まず、パスのみ列挙する
find . -maxdepth 3 \( \
  -name ".env" -o -name ".env.*" -o -name "*.env" \
  -o -name "*.pem" -o -name "*.p12" -o -name "*.pfx" -o -name "*.key" \
  -o -name "credentials.json" -o -name "service-account*.json" \
  -o -name ".npmrc" -o -name ".netrc" -o -name ".pypirc" \
  -o -name "secrets.yml" -o -name "secrets.yaml" \
\) -not -path "./.git/*" -not -path "./node_modules/*" 2>/dev/null | sort
```

#### Step 2: 既存設定の確認

```bash
# 現在のpermissions.deny設定のみを抽出（全文表示はしない）
for f in .claude/settings.json .claude/settings.local.json; do
  if [ -f "$f" ]; then
    echo "=== $f: permissions.deny ==="
    python3 - "$f" <<'PYEOF'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    deny = d.get('permissions', {}).get('deny', [])
    if deny:
        for r in deny: print(f'  - {r}')
    else:
        print('  (deny rules not set)')
except Exception as e:
    print(f'  (parse error: {e})')
PYEOF
  fi
done
```

#### Step 3: denyルール生成

Step 1の結果をもとに、`permissions.deny`ルールを生成する。

**基本ルール（ほぼ全プロジェクトに適用可能）:**

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/secrets/**)",
      "Read(**/*.pem)",
      "Read(**/*.p12)",
      "Read(**/*.pfx)",
      "Read(**/*.key)",
      "Read(**/credentials.json)",
      "Read(**/service-account*.json)",
      "Edit(./.env)",
      "Edit(./.env.*)",
      "Edit(**/.env)",
      "Edit(**/.env.*)",
      "Edit(**/secrets/**)",
      "Edit(**/*.pem)",
      "Edit(**/*.p12)",
      "Edit(**/*.pfx)",
      "Edit(**/*.key)",
      "Edit(**/credentials.json)",
      "Edit(**/service-account*.json)",
      "Write(./.env)",
      "Write(./.env.*)",
      "Write(**/.env)",
      "Write(**/.env.*)",
      "Write(**/secrets/**)",
      "Write(**/*.pem)",
      "Write(**/*.p12)",
      "Write(**/*.pfx)",
      "Write(**/*.key)",
      "Write(**/credentials.json)",
      "Write(**/service-account*.json)",
      "Bash(env:*)",
      "Bash(printenv:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

**プロジェクト固有ルール（検出結果に応じて追加）:**

検出されたファイルパターンに合わせてRead/Edit/Writeのdenyルールを追加する。例:
- `.npmrc`が存在 → `"Read(.npmrc)"`, `"Edit(.npmrc)"`, `"Write(.npmrc)"`
- `config/secrets.yml`が存在 → `"Read(config/secrets.yml)"`, `"Edit(config/secrets.yml)"`, `"Write(config/secrets.yml)"`

#### Step 4: 設定の適用

**既存のsettings.jsonがある場合は上書きしない。** 差分を提示し、ユーザーにマージ方針を確認する。

```
=== 推奨追加ルール ===
現在のdeny: [既存ルール一覧]
追加推奨:   [新規ルール一覧]

マージ方法:
1. 追加ルールのみ追記（既存ルールは維持）
2. 推奨ルール全体で置換
3. 個別に選択

どの方法で適用しますか？
```

ユーザーの確認後、`.claude/settings.json`または`.claude/settings.local.json`を更新する。

#### Step 5: 検証

生成した設定の検証手順を提示する:

```
=== 検証手順 ===

1. 防御されるケース（以下はdenyされるはず）:
   - Read(.env) → ブロック
   - Bash(printenv) → ブロック

2. 防御されないケース（以下は通過する。これは仕様）:
   - Bash(cat .env) → 通過（Bashの引数マッチの限界）
   - Bash(python3 -c "print(open('.env').read())") → 通過
   - op runで展開された環境変数の読み取り → 通過

3. より強い保護が必要な場合:
   - managed settingsを使用（ユーザーが変更不可）
   - sandbox modeを有効化
   - PreToolUse hooksで追加パターンを検出（hooks設定は手動で行う必要あり）
```

#### Step 6: 改善推奨（レポート後半）

検出結果をもとに改善推奨を提示する:

- **平文.envが存在**: `/op-env migrate`でop://参照に移行を推奨
- **広権限の資格情報**: Service Account化、最小権限化を推奨
- **長命トークン**: 短命トークン（STS/OIDC/OAuth）への移行を推奨
- **本番キーの存在**: AI実行環境からの即時除去を強く推奨

#### Step 7: 高保証が必要な場合（レポート末尾）

ガードレール以上の保護が必要な場合の案内:

- **Capability Broker**: MCPサーバーとして限定操作のみ公開し、AIにシークレットを渡さない設計。設計原則: 最小権限、監査ログ、human-in-the-loop承認
- **短命トークン発行**: STS AssumeRole、OIDC federation、OAuth client credentials flowで1〜15分のトークンを発行
- **環境隔離**: 別ユーザー/コンテナ/VMでAIを実行し、シークレットストアへのアクセスを物理的に分離

### audit（補助モード）

リポジトリ内（およびオプションでホーム配下）のシークレット候補を走査し、現在の保護状況を報告する。

**AIに秘密値を見せない。** スキャンはローカルscriptで実行し、パスと種別のみ返す。

#### 使い方

```bash
# リポジトリのみ走査（デフォルト）
bash meta-plugin/skills/secret-boundary/scripts/secret-scan.sh

# ホーム配下も走査（opt-in）
bash meta-plugin/skills/secret-boundary/scripts/secret-scan.sh --include-home
```

#### 出力形式

```
path,type,modified,permissions,deny_rule_exists
./.env,env-file,2025-12-01,644,no
./config/secrets.yml,config-secret,2025-11-15,644,no
```

能力分類（prod到達性、課金影響、書込可否等）はscriptでは判定しない。
必要に応じてユーザーに対話で確認し、`secret-boundary.local.yaml`に記録する。

#### secret-boundary.local.yaml

能力分類の補助台帳。**必ず.gitignoreに追加すること**（メタデータ自体が機微情報のため）。

```yaml
# secret-boundary.local.yaml
# このファイルは.gitignoreに追加すること
secrets:
  - path: .env
    type: env-file
    prod_reachable: false
    billing_impact: true
    writable: true
    ttl: permanent
    revocable: true
    notes: "OpenAI API key (dev), Supabase anon key"
```

## 関連スキル

- `/op-env`: 平文.envの保管衛生改善。secret-boundaryのremediate推奨からリンク
- `/security-observation`: コード内のセキュリティ脆弱性検出。対象が異なり補完関係
- `/claude-md-optimizer`: .claude/settings.json の最適化。secret-boundaryが生成した設定との整合性確認

## 参考資料

- Claude Code Settings: https://docs.anthropic.com/en/docs/claude-code/settings
- Claude Code Hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
- Claude Code Security: https://docs.anthropic.com/en/docs/claude-code/security
