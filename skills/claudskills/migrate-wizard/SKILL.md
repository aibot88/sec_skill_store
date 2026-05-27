---
name: migrate-wizard
description: Use when migrating an AI Studio project to production in one pass. Orchestrates all migration steps (analyze, export, repo setup, graduation, monitoring, security) with upfront configuration and automatic step detection. Trigger examples - "AI Studioから本番に移行して", "migrate to production", "ワンパスでマイグレーション", "production migration wizard"
---

# Migrate Wizard

AI Studio プロジェクトを本番環境にワンパスでマイグレーションするオーケストレーター。各スキルを順番に実行し、必要な設定は最初にまとめて聞く。

## Overview

このスキルは以下の6ステップを自動検出・一括実行する:

| Step | Skill | やること |
|:----:|-------|---------|
| 0 | analyze-and-document | プロジェクト分析 → CLAUDE.md 生成 |
| 1 | export-from-ai-studio | コード整形 + apiKey サニタイズ |
| 2 | repo-initializer-google | GitHub リポ整備 (.gitignore, README) |
| 3 | graduate-from-ai-studio **または** Vercelパス | デプロイ先に応じた構成 **ファイル生成** |
| 3.5 | cloud-run-deploy / vercel-deploy | **インフラ構築 + 初回デプロイ** (CLI 認証済みの場合) |
| 4 | monitoring-sentry-datadog | 監視・エラートラッキング |
| 5 | security-hardening-gcp | セキュリティ強化 (SA, Secret Manager, API Key 制限) |

**Step 3 の代替: Vercel デプロイパス** (デプロイ先=Vercel 選択時のみ)

| Sub-Step | Skill | やること |
|:--------:|-------|---------|
| 3a | vercel-nextjs-config | next.config.ts 修正 + vercel.json 生成 |
| 3b | vercel-link | Vercel プロジェクトにリンク |
| 3c | vercel-env | 環境変数設定 (GEMINI_API_KEY 等) |
| 3d | vercel-deploy | プレビュー → 本番デプロイ |
| 3e | vercel-firebase-auth-domain | Firebase Auth authorized domain に Vercel URL を追加 |

**ナレッジスキル** (直接実行ステップではなく、フロー実行時に参照される):

| Skill | 参照タイミング |
|-------|--------------|
| vercel-ai-studio-export | Step 1 (export-from-ai-studio) 実行時: AI Studio エクスポートの構造理解のため |
| vercel-gcp-project-identification | Step 3e (vercel-firebase-auth-domain) 実行時: 正しい GCP プロジェクトの特定のため |

## When to Use

- User says "本番に移行して", "migrate to production", "ワンパスでマイグレーション"
- AI Studio で作ったプロジェクトを初めて本番化する
- 複数のスキルを個別に呼ぶのが面倒なとき

**When NOT to use:**
- 特定のステップだけ実行したい → 個別スキルを直接使う
- 開発環境のセットアップだけ → `setup-dev-environment` を使う

---

## Phase 0: Prerequisites Check

**最初に実行環境を確認する。** 以下のツールの存在と認証状態をチェック:

| Tool | Check command | Required | Fallback |
|------|--------------|----------|----------|
| `git` | `git --version` | **必須** (なければ中止) | — |
| `gcloud` | `gcloud auth print-access-token 2>/dev/null` | 推奨 | リモート操作を手動コマンドとして Summary に集約 |
| `firebase` | `npx firebase-tools --version 2>/dev/null` | 推奨 | Firebase デプロイコマンドを Summary に集約 |
| `gh` | `gh auth status 2>/dev/null` | 推奨 | GitHub repo 作成を手動手順として案内 |
| `npm` or `pip` | `npm --version` / `pip --version` | 推奨 | SDK インストールコマンドを Summary に集約 |
| `docker` | `docker --version 2>/dev/null` | 任意 | Dockerfile 生成はするがローカル検証不可と案内 |
| `vercel` | `vercel --version 2>/dev/null` | **Vercel選択時のみ必須** | Vercel 操作コマンドを Summary に集約 |

**出力フォーマット:**
```
=== Environment Check ===

✓ git       installed
✓ gcloud    authenticated (project: my-project-123)
✓ firebase  installed (v13.x)
✓ gh        authenticated (user: TakuroFukamizu)
✓ npm       installed (v20.x)
△ docker    not found — Dockerfile is generated but cannot validate locally
✗ terraform not found — will ask about IaC choice

→ Proceeding. Missing tools affect remote operations only;
  manual commands will be listed in the summary.
```

**判定ルール:**
- `git` がない → **中止**。`git --version` が失敗したらエラーメッセージを出して終了。
- `gcloud` 認証済み → **フル自動化モード (Cloud Run)**: GCP プロジェクト設定、API 有効化、Cloud Run デプロイ、Secret Manager、IAM 設定をすべて自動実行。
- `gcloud` 未認証 → **ファイル生成モード (Cloud Run)**: IaC ファイルと CI/CD 設定を生成し、リモート操作は手動コマンドとして Phase 5 Summary に集約。
- その他のツールが不在 → 続行。影響を受けるステップは graceful degrade。

**Vercel パスは `vercel` と `gcloud` の組み合わせで 3 モード:**

| vercel CLI | gcloud CLI | モード名 | 動作 |
|:----------:|:----------:|---------|------|
| ✓ 認証済み | ✓ 認証済み | **FULL** | Step 3a-3e + Step 5 すべて自動実行 |
| ✓ 認証済み | ✗ 未認証 | **PARTIAL** | Step 3a-3d 自動実行。Step 3e (Firebase Auth domain) と Step 5 (API Key 制限, Budget) は手動コマンドを Summary に集約 |
| ✗ 未認証 | — | **FILE-GEN** | Step 3a のみ (ファイル生成)。Step 3b-3e は手動コマンドを Summary に集約 |

Phase 3 の Plan Presentation と Phase 5 の Summary はこのモードに応じて表示を切り替える。

**CLI 認証の推奨:**
未認証のツールがある場合、以下を表示:
```
⚠ 認証すると、インフラ構築からデプロイまで自動化できます。
  今すぐ認証しますか？

  gcloud: gcloud auth login [推奨]
  vercel: vercel login [Vercel 選択時に必要]

  (a) はい — 認証を実行
  (b) いいえ — ファイル生成のみで進める (デプロイは手動)
```

---

## Phase 1: Auto-Detect

プロジェクトのファイルと状態をスキャンし、各ステップの完了状況を判定する。

### 検出手順

以下を順番に実行:

1. **`firebase-applet-config.json` を読む** (存在すれば)
   - `projectId` を抽出 → `gen-lang-client-*` パターンなら AI Studio プロジェクトとして記録
   - `apiKey` フィールドの値を確認 → `AIzaSy` で始まるなら「未サニタイズ」
   - `firestoreDatabaseId`, `appId` も記録 (後続ステップで使用)

2. **`CLAUDE.md` の存在と内容を確認**
   - ファイルが存在し、`## Architecture` または `## Tech Stack` セクションを含む → Step 0 完了
   - 存在しない or 空 → Step 0 未完了

3. **apiKey サニタイズ状態を確認**
   - `firebase-applet-config.json` に `AIzaSy` で始まる apiKey がない → Step 1 完了 (の条件1)
   - **Gemini 実使用を検出** (export-from-ai-studio スキルの検出手順に従う):
     - ソースコードで Gemini SDK import または `GEMINI_API_KEY` 実使用を検索
     - **使用あり:** `.env.example` に `GEMINI_API_KEY` を含む → Step 1 完了 (の条件2)
     - **使用なし:** `.env.example` に `GEMINI_API_KEY` がない + Gemini 依存が `package.json` にない → Step 1 完了 (の条件2)
   - Gemini 使用の有無を `gemini_used: boolean` として記録し、後続ステップ (Step 3.5, Step 5) に渡す
   - 条件が満たされていない → Step 1 未完了

4. **リポジトリ状態を確認**
   - `.git` ディレクトリが存在する
   - `git remote -v` でリモートが設定されている
   - `.gitignore` に以下が含まれている: `.env`, `.env.local`, `service-account*.json`
   - `README.md` が存在しセットアップ手順を含む
   - **すべて満たす → Step 2 完了。一部欠ける → Step 2 部分完了 (不足分のみ実行)**

5. **卒業状態を確認** (Cloud Run パスの場合)
   - `Dockerfile` が存在する
   - `infra/terraform/` or `infra/pulumi/` or `infra/scripts/` のいずれかが存在する
   - `.github/workflows/deploy.yml` (または類似の CD workflow) が存在する
   - `firebase.json` が存在する
   - **すべて存在 → Step 3 完了。一部のみ → Step 3 部分完了 (不足分のみ生成)**
   - 存在する Dockerfile のベースイメージが検出した runtime と一致するか確認。不一致なら警告。

   **Vercel パスの場合の追加チェック:**
   - `.vercel/` ディレクトリが存在するか → `vercel link` 済みかどうか
   - `vercel.json` が存在するか
   - `next.config.ts` または `next.config.js` に `output: 'standalone'` が含まれていないことの確認 (Vercel では不要)

6. **監視状態を確認**
   - `package.json` の dependencies に `@sentry/node` or `sentry-sdk` or `dd-trace` が含まれる
   - サーバーエントリポイント (`server.ts`, `server.js`, `main.py`) に Sentry/Datadog 初期化コードがある
   - **両方あれば完了。dependencies のみ → 部分完了。なければ未完了。**

7. **セキュリティ状態を確認**
   - `gcloud` が認証済みの場合 — 以下の **4項目すべて** を確認:
     - `gcloud iam service-accounts list --project=PROJECT_ID` → デフォルト compute SA 以外の専用 SA が存在するか
     - `gcloud secrets list --project=PROJECT_ID` → Secret Manager にシークレットが格納されているか
     - `gcloud services api-keys list --project=PROJECT_ID` → API Key にリファラー制限が設定されているか
     - `gcloud billing budgets list --billing-account=BILLING_ACCOUNT` → Budget alert が存在するか
     - **4項目すべて OK → 完了。一部のみ → 部分完了 (不足項目のみ実行)。**
     - 注意: SA + Secret Manager が存在しても、API Key 制限や Budget alert がなければ Step 5 は部分実行が必要。
   - `gcloud` 未認証の場合:
     - `unconfirmed` (実行推奨) として扱う

8. **AI Studio 既存インフラの検出** (`gcloud` 認証済みの場合のみ)
   - `firebase-applet-config.json` の `projectId` を使って:
     - `gcloud run services list --project=PROJECT_ID` → 既存 Cloud Run サービス
     - `gcloud firestore databases list --project=PROJECT_ID` → 既存 Firestore DB
   - 検出結果を記録し、Phase 2 で表示

### 出力フォーマット

```
=== Migration Status ===

✓ Step 0  analyze-and-document      — CLAUDE.md detected
✗ Step 1  export-from-ai-studio     — apiKey not sanitized, .env.example missing
△ Step 2  repo-initializer-google   — .git exists / .gitignore missing .env entry
✗ Step 3  graduate-from-ai-studio   — Dockerfile missing, no IaC, no CI/CD
?  Step 4  monitoring-sentry-datadog — unconfirmed (recommend execution)
?  Step 5  security-hardening-gcp    — unconfirmed (recommend execution)

AI Studio infrastructure detected:
  Project: gen-lang-client-0a1b2c3d
  Cloud Run: ai-studio-app (asia-northeast1)
  Firestore: (default) database

→ Steps 1, 2 (partial), 3, 4, 5 will be executed
```

**記号凡例:**
- ✓ = 完了 (スキップ)
- △ = 部分完了 (不足分のみ実行)
- ✗ = 未完了 (フル実行)
- ? = 未確認 (実行推奨)

---

## Phase 2: Intake Questions

未完了ステップが必要とする入力を**1回のメッセージでまとめて質問**する。完了済みステップの質問は表示しない。

**重要: 質問の表示条件は「どのステップが未完了か」ではなく「後続ステップが必要とする入力があるか」で判定する。** 例えば Step 3 が完了済みでも Step 5 が未完了なら、Firebase プロジェクト情報 (Q1) は聞く必要がある (既存インフラの hardening に必要)。

### 質問一覧

```
=== Migration Configuration ===

以下の質問に回答してください:

--- デプロイ先 ---

Q0. デプロイ先を選択してください:
  (a) Cloud Run [GCP完結、コンテナベース]
  (b) Vercel [Next.js最適化、git-push-to-deploy]
  (c) Railway [コンテナ、長時間処理向け] ← 将来拡張予定 (現在は選択不可)

--- デプロイ・インフラ設定 ---

  ▼ デプロイ先 = Cloud Run の場合:

Q1. Firebase プロジェクト:
  (a) 新規作成 [推奨: 完全独立した本番環境]
  (b) AI Studio の既存プロジェクトを継続 (gen-lang-client-xxxxx)
  ← gen-lang-client-xxxxx で Cloud Run, Firestore が検出されました

Q2. IaC ツール:
  (a) Terraform [推奨: エコシステムが最も充実]
  (b) Pulumi (TypeScript) [プロジェクトと同じ言語]
  (c) gcloud + firebase CLI スクリプト [最もシンプル、追加ツール不要]

Q3. GCP リージョン: [asia-northeast1] ← Enter でデフォルト

Q3.5. GCP プロジェクト ID:              ← gcloud 認証済みの場合のみ
  現在のプロジェクト: my-project-123
  (a) このプロジェクトを使う
  (b) 別のプロジェクト ID を入力: ________
  (c) 新規プロジェクトを作成: ________

  ▼ デプロイ先 = Vercel の場合:

Q1-V. Firebase プロジェクト:
  (a) 新規作成 [推奨: 完全独立した本番環境]
  (b) AI Studio の既存プロジェクトを継続 (gen-lang-client-xxxxx)

Q2-V. Vercel project name: [プロジェクト名を入力]

Q3-V. Vercel scope (team名 or personal): [スコープ名を入力]

--- 監視 ---

Q4. 監視ツール:
  (a) Sentry [エラートラッキング]
  (b) Datadog [APM + メトリクス]
  (c) 両方
  (d) スキップ

--- セキュリティ ---

Q5. セキュリティ強化:
  (a) 実行する [推奨]
  (b) スキップ
```

### 表示条件

| 質問 | 表示条件 |
|------|---------|
| Q0 (デプロイ先) | 常に表示 |
| Q1 (Firebase project) / Q1-V | Step 3 未完了 OR Step 5 未完了/未確認 |
| Q2 (IaC tool) | Step 3 未完了 **AND** デプロイ先=Cloud Run |
| Q3 (GCP region) | Step 3 未完了 **AND** デプロイ先=Cloud Run |
| Q3.5 (GCP project ID) | `gcloud` 認証済み **AND** (Step 3 OR Step 3.5 OR Step 5 未完了) |
| Q2-V (Vercel project name) | Step 3 未完了 **AND** デプロイ先=Vercel |
| Q3-V (Vercel scope) | Step 3 未完了 **AND** デプロイ先=Vercel |
| Q4 (Monitoring) | Step 4 未完了/未確認 |
| Q5 (Security) | Step 5 未完了/未確認 |

**追加条件:**
- Q1/Q1-V で既存プロジェクト選択 AND `gcloud` 認証済み → 既存インフラの情報 (Cloud Run URL, Firestore DB) を自動取得
- Q2 で terraform/pulumi 選択 AND 未インストール → 「選択したツールのインストールが別途必要です」と注記
- Q0 で Vercel 選択 AND `vercel` CLI 未インストール → 「vercel CLI のインストールが必要です: `npm i -g vercel`」と注記
- Q4 = スキップ → Step 4 を丸ごとスキップ
- Q5 = スキップ → Step 5 を丸ごとスキップ

**Step 2 (repo-initializer-google) の入力について:**
- `.git` が存在しない場合のみ、プロジェクト名を追加で質問する
- `.git` が既にある場合は `.gitignore` / README の補完のみで、追加質問なし

---

## Phase 3: Plan Presentation

Phase 2 の回答を元に実行計画を表示。ユーザーの `y` で実行開始。

**Cloud Run パス (gcloud 認証済み = フル自動化):**

```
=== Migration Plan ===

Target: Cloud Run (asia-northeast1) / Terraform / Sentry
GCP Project: my-project-123
Firebase: New project
Automation: FULL (gcloud ✓ / firebase ✓)

Step 1  export-from-ai-studio
        → firebase-applet-config.json apiKey サニタイズ
        → Firebase init コード → 環境変数注入に変更
        → .env.example 生成

Step 2  repo-initializer-google (部分実行)
        → .gitignore: .env, service-account*.json 追加
        → README: セットアップ手順追記

Step 3  graduate-from-ai-studio [ファイル生成]
        → Dockerfile + .dockerignore (Node.js multi-stage)
        → infra/terraform/ (main.tf, variables.tf, outputs.tf, terraform.tfvars.example)
        → .github/workflows/deploy.yml (Workload Identity Federation)
        → firebase.json + .firebaserc + firestore.indexes.json
        → .env.example 更新

Step 3.5  cloud-run-deploy [GCP 自動構築 + デプロイ] ★
        → GCP API 有効化 (Cloud Run, Artifact Registry, Secret Manager)
        → Artifact Registry リポジトリ作成
        → Secret Manager にシークレット格納
        → 専用 SA 作成 + IAM 設定
        → Cloud Run に初回デプロイ
        → Firebase ルール・インデックスをデプロイ

Step 4  monitoring-sentry-datadog
        → npm install @sentry/node
        → Sentry 初期化コード挿入 (server.ts)
        → Gemini API メトリクス追加

Step 4.5  再デプロイ [自動実行] ★
        → gcloud run deploy (監視コードを本番に反映)

Step 5  security-hardening-gcp [自動実行] ★
        → Firebase API Key リファラー制限
        → Budget alert 設定
        → Cloud Audit Logs 確認

★ = gcloud で自動実行 (認証済み)
実行しますか？ (y/n)
```

**Cloud Run パス (gcloud 未認証 = ファイル生成モード):**
```
Automation: FILE GENERATION ONLY (gcloud ✗)
Step 3.5 は省略。Step 5 はコード改善のみ。
GCP 操作は手動コマンドとして Summary に記載。
```

**Vercel パス (vercel 認証済み = フル自動化):**

```
=== Migration Plan ===

Target: Vercel / Sentry
Vercel Project: my-app (scope: my-team)
Firebase: Existing project (gen-lang-client-xxxxx)
Automation: FULL (vercel ✓ / gcloud ✓)

Step 1  export-from-ai-studio
        → firebase-applet-config.json apiKey サニタイズ
        → Firebase init コード → 環境変数注入に変更
        → .env.example 生成

Step 2  repo-initializer-google (部分実行)
        → .gitignore: .env 追加
        → README: セットアップ手順追記

Step 3a  vercel-nextjs-config [ファイル生成]
        → next.config.ts: output: 'standalone' を除去 (存在する場合)
        → vercel.json 生成 (headers, rewrites 等)

Step 3b  vercel-link [自動実行] ★
        → vercel link --project my-app --scope my-team --yes

Step 3c  vercel-env [自動実行] ★
        → GEMINI_API_KEY, NEXT_PUBLIC_FIREBASE_* を Vercel 環境変数に設定
        → .env.local / .env の値を自動読み取り

Step 3d  vercel-deploy [自動実行] ★
        → vercel deploy (プレビュー) → 動作確認 → vercel deploy --prod (本番)

Step 3e  vercel-firebase-auth-domain [自動実行] ★
        → Firebase Auth authorized domains に Vercel URL を追加

Step 4  monitoring-sentry-datadog
        → npm install @sentry/nextjs
        → Sentry 初期化コード挿入
        → Gemini API メトリクス追加

Step 4.5  再デプロイ [自動実行] ★
        → vercel deploy --prod (監視コードを本番に反映)

Step 5  security-hardening-gcp [自動実行] ★
        → Secret Manager 移行 (gcloud 認証済みの場合)
        → Firebase API Key リファラー制限
        → Budget alert 設定

★ = CLI で自動実行 (認証済み)
実行しますか？ (y/n)
```

**Vercel パス (PARTIAL: vercel ✓ / gcloud ✗):**
```
Automation: PARTIAL (vercel ✓ / gcloud ✗)
Step 3a-3d は自動実行。
Step 3e (Firebase Auth domain) と Step 5 は gcloud 未認証のため手動コマンドを Summary に記載。
```

**Vercel パス (FILE-GEN: vercel ✗):**
```
Automation: FILE GENERATION ONLY (vercel ✗)
Step 3a のみ実行 (ファイル生成)。Step 3b-3e は手動コマンドとして Summary に記載。
```

**完了済みステップは表示しない。** スキップしたステップ (Q4/Q5 でスキップ選択) も表示しない。

---

## Phase 4: Sequential Execution

承認後、各ステップを順番に実行する。

### 実行プロトコル

各ステップについて以下を行う:

1. **スキルの SKILL.md を読み込む** — `skills/<skill-name>/SKILL.md` を Read で読む
2. **スキルの検出/分析フェーズを実行** — Phase 1 の結果をキャッシュとして活用
3. **スキルの質問/承認フェーズをスキップ** — Phase 2 で回答済みの設定をそのまま使用
4. **スキルの生成フェーズを実行** — SKILL.md の手順に従ってファイルを生成
5. **進捗を報告** — 生成したファイルをリスト表示

### 各ステップの実行詳細

**Step 0: analyze-and-document** (未完了の場合のみ)
- `skills/analyze-and-document/SKILL.md` を Read
- Phase 1 (自動スキャン) → Phase 3 (CLAUDE.md 生成) を実行
- Phase 2 (ユーザー確認) は最小限: 検出結果を表示し、重大な誤りがなければ自動で進める

**Step 1: export-from-ai-studio** (未完了の場合のみ)
- `skills/export-from-ai-studio/SKILL.md` を Read
- **`skills/vercel-ai-studio-export/SKILL.md` を Read** — AI Studio エクスポートの構造理解のためナレッジ参照
- `firebase-applet-config.json` の apiKey をプレースホルダーに置換
- Firebase 初期化コードを環境変数注入に変更
- **Gemini 実使用を検出** — プロジェクト全体 (`src/`, `server.ts`, `api/`, `lib/` 等。`node_modules/`, `*.config.*` 除く) で Gemini SDK import + `GEMINI_API_KEY` 実使用を検索。未使用なら:
  - `package.json` から Gemini SDK 依存を削除
  - `vite.config.ts` から `GEMINI_API_KEY` expose を削除
  - `.env.example` から `GEMINI_API_KEY` を除外
- `.env.example` を生成/更新 (Gemini 使用時のみ `GEMINI_API_KEY` を含む)
- 言語は `package.json` (Node.js) or `requirements.txt` (Python) から自動検出

**Step 2: repo-initializer-google** (未完了/部分完了の場合)
- `skills/repo-initializer-google/SKILL.md` を Read
- Phase 1 で検出した不足項目のみ実行:
  - `.gitignore` に不足エントリがあれば追加
  - README にセットアップ手順がなければ追記
  - `.git` がなく `gh` が使える場合: リポ作成 + 初回 push
  - `.git` があるが remote がない場合: remote 追加のみ

**Step 3: graduate-from-ai-studio** (未完了/部分完了の場合 / **デプロイ先=Cloud Run のみ**)
- `skills/graduate-from-ai-studio/SKILL.md` を Read
- Phase 2 の回答を渡す:
  - Firebase project strategy → Q1 の回答
  - IaC tool → Q2 の回答
  - GCP region → Q3 の回答
- SKILL.md の Phase 1 (分析) は wizard の Phase 1 結果を使用
- SKILL.md の Phase 2, 3 (質問, 承認) をスキップ
- SKILL.md の Phase 3.5 (apiKey サニタイズ) は Step 1 で実行済みならスキップ
- SKILL.md の Phase 4 (ファイル生成) を実行
- 部分完了の場合: 不足ファイルのみ生成

**Step 3.5: cloud-run-deploy — GCP インフラ構築 + 初回デプロイ** (デプロイ先=Cloud Run AND `gcloud` 認証済みの場合のみ)

> **このステップが Cloud Run パスの「手動作業」を自動化する核心。** Step 3 で生成したファイルを使い、`gcloud` コマンドで実際に GCP 上にインフラを構築しデプロイする。

- `skills/cloud-run-deploy/SKILL.md` を Read
- **前提:** Step 3 で Dockerfile, IaC ファイル, firebase.json が生成済み
- **GCP project ID:** Q3.5 の回答を使用

**重要: `gcloud config set project` は使用禁止。** `vercel-gcp-project-identification` スキルの規則に従い、すべてのコマンドで `--project=PROJECT_ID` を明示する。AI Studio の `gen-lang-client-*` プロジェクトとユーザーの作業用プロジェクトを取り違えるリスクを防ぐため。

実行手順:
1. Q1 = 新規の場合: `gcloud projects create PROJECT_ID` + `firebase projects:addfirebase PROJECT_ID`
2. API 有効化: `gcloud services enable run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com cloudbuild.googleapis.com iam.googleapis.com --project=PROJECT_ID`
3. Artifact Registry リポジトリ作成: `gcloud artifacts repositories create SERVICE --repository-format=docker --location=REGION --project=PROJECT_ID`
4. Secret Manager にシークレット格納 **(Gemini 使用時のみ):**
   - `gemini_used = true` の場合: `echo -n "VALUE" | gcloud secrets create gemini-api-key --data-file=- --project=PROJECT_ID` (`.env` / `.env.local` から値を読み取り、なければユーザーに確認)
   - `gemini_used = false` の場合: `gemini-api-key` シークレットの作成をスキップ
   - **FIREBASE_API_KEY 等、Gemini 以外のシークレットは常に作成する**
5. 専用 SA 作成: `gcloud iam service-accounts create SERVICE-sa --project=PROJECT_ID`
6. IAM 設定: `gcloud projects add-iam-policy-binding PROJECT_ID --member=serviceAccount:SERVICE-sa@PROJECT_ID.iam.gserviceaccount.com --role=roles/secretmanager.secretAccessor` (+ `roles/datastore.user`)
7. Cloud Run デプロイ:
   - `gemini_used = true`: `gcloud run deploy SERVICE --source . --region REGION --service-account SERVICE-sa@PROJECT_ID.iam.gserviceaccount.com --set-secrets="GEMINI_API_KEY=gemini-api-key:latest" --allow-unauthenticated --project=PROJECT_ID`
   - `gemini_used = false`: `gcloud run deploy SERVICE --source . --region REGION --service-account SERVICE-sa@PROJECT_ID.iam.gserviceaccount.com --allow-unauthenticated --project=PROJECT_ID` (--set-secrets に GEMINI_API_KEY を含めない)
8. Firebase デプロイ: `firebase deploy --only firestore:rules,firestore:indexes --project=PROJECT_ID` (`firebase` CLI がある場合)
9. デプロイ確認: `gcloud run services describe SERVICE --region REGION --project=PROJECT_ID --format='value(status.url)'` → `curl SERVICE_URL/health`

`gcloud` 未認証の場合: Step 3.5 は丸ごとスキップ。上記コマンドを Summary の手動作業リストに集約。

---

**Step 3 (Vercel パス): デプロイ先=Vercel の場合のみ実行** — graduate-from-ai-studio の代わりに以下の Sub-Step を順番に実行する:

**Step 3a: vercel-nextjs-config**
- `skills/vercel-nextjs-config/SKILL.md` を Read
- `next.config.ts` / `next.config.js` を確認:
  - `output: 'standalone'` が存在する場合は除去 (Vercel では不要)
  - Vercel 向け最適化設定を追加
- `vercel.json` を生成 (headers, rewrites, functions 設定等)
- SKILL.md の手順に従ってファイルを生成/更新

**Step 3b: vercel-link**
- `skills/vercel-link/SKILL.md` を Read
- Q2-V (Vercel project name) と Q3-V (Vercel scope) の回答を使用
- `vercel link --project <project-name> --scope <scope>` を実行
- `.vercel/` ディレクトリが既に存在する場合は再リンクの要否を確認

**Step 3c: vercel-env** (`vercel` 認証済みの場合は自動実行)
- `skills/vercel-env/SKILL.md` を Read
- Step 1 で確認した環境変数 (GEMINI_API_KEY, NEXT_PUBLIC_FIREBASE_* 等) を Vercel 環境変数に設定
- `.env.example` の内容を参照して必要な変数を特定
- **`vercel` 認証済みの場合:** `.env` / `.env.local` から値を自動読み取り、`vercel env add` で設定。値が見つからない変数はユーザーに確認。
- **`vercel` 未認証の場合:** 設定コマンドを Summary に集約

**Step 3d: vercel-deploy** (`vercel` 認証済みの場合は自動実行)
- `skills/vercel-deploy/SKILL.md` を Read
- **`vercel` 認証済みの場合:**
  1. `vercel deploy` でプレビューデプロイを実行
  2. プレビュー URL を取得・表示
  3. `vercel deploy --prod` で本番デプロイを実行
  4. 本番 URL を取得・記録 (Step 3e で使用)
- **`vercel` 未認証の場合:** デプロイコマンドを Summary に集約

**Step 3e: vercel-firebase-auth-domain**
- `skills/vercel-gcp-project-identification/SKILL.md` を Read — **ナレッジ参照**: Q1-V で選択した Firebase プロジェクトに対応する GCP プロジェクト ID を正確に特定するため
- `skills/vercel-firebase-auth-domain/SKILL.md` を Read
- Step 3d で取得した本番 URL (例: `my-app.vercel.app`) を Firebase Auth の authorized domains に追加
- `gcloud` 認証済みの場合: Firebase Console API または gcloud CLI で直接設定
- `gcloud` 未認証の場合: 手動設定コマンドを Summary に集約

**Step 4: monitoring-sentry-datadog** (未完了/未確認 AND スキップ未選択の場合)
- `skills/monitoring-sentry-datadog/SKILL.md` を Read
- Q4 の回答に基づいて Sentry / Datadog / 両方を設定
- SDK インストール (`npm install` or `pip install`)
- サーバーエントリポイントに初期化コード挿入
- `.env.example` に DSN/API key を追加
- **DSN/API key の値自体はユーザーが後で設定** → Summary の手動作業に含める

**Step 4.5: 再デプロイ** (Step 4 で監視コードを追加した場合 AND CLI 認証済みの場合)

> Step 3.5 / 3d でデプロイした後に Step 4 で Sentry/Datadog コードを追加しているため、本番に反映するには再デプロイが必要。

- **Cloud Run パス** (`gcloud` 認証済み): `gcloud run deploy SERVICE --source . --region REGION --project=PROJECT_ID` (SA + secrets 設定は既存を引き継ぐ)
- **Vercel パス** (`vercel` 認証済み): `vercel deploy --prod`
- **CLI 未認証の場合:** Summary の手動作業に「監視コード追加後の再デプロイ」として記載
- **Step 4 をスキップした場合:** Step 4.5 も丸ごとスキップ

---

**Step 5: security-hardening-gcp** (未完了/未確認 AND スキップ未選択の場合)
- `skills/security-hardening-gcp/SKILL.md` を Read
- `gcloud` 認証済みの場合 — 以下を**自動実行**:
  - **Cloud Run パス:** Step 3.5 で SA + Secret Manager 設定済みなので重複しない。Step 5 は以下に集中:
    - Firebase API Key リファラー制限
    - Budget alert 設定
    - Cloud Audit Logs 確認
  - **Vercel パス:** SA は不要。以下を実行:
    - Secret Manager 移行 (GEMINI_API_KEY 等を Secret Manager にバックアップ)
    - Firebase API Key リファラー制限 (Vercel ドメインを許可リストに含める)
    - Budget alert 設定
  - Q1 で既存プロジェクト選択 → 既存インフラに対して hardening
  - Q1 で新規プロジェクト選択 → 新規構成でセキュア設計
- `gcloud` 未認証の場合:
  - コード内のセキュリティ改善のみ実行
  - リモート操作コマンドを Summary に集約

### エラーハンドリング

**ファイル操作系 (続行可能):**
- **ファイル生成の失敗** → エラーを表示し、そのステップをスキップして次へ進む。Summary で未完了として報告。
- **既存ファイルとの衝突** → 上書き前に diff を表示し、マージするか確認する。**これが実行中対話の一つ。**
- **npm install / pip install の失敗** → 警告を出して続行。Summary に手動インストールコマンドを記載。

**CLI コマンド系 (副作用あり — 失敗分類に応じて対応):**

| 失敗したコマンド | 重大度 | 対応 |
|----------------|--------|------|
| `gcloud projects create` | **致命的** | Step 3.5 以降を丸ごと中止。Summary にエラーと手動復旧コマンドを記載。 |
| `gcloud services enable` | **致命的** | 後続の AR, SM, SA, deploy がすべて依存。Step 3.5 を中止。 |
| `gcloud secrets create` | 高 | Secret なしでデプロイ不可。Step 3.5 の deploy をスキップ。SA 作成は続行。 |
| `gcloud run deploy` | 高 | デプロイ失敗。Step 4.5 (再デプロイ) もスキップ。Summary に手動デプロイコマンドを記載。 |
| `firebase deploy` | 中 | Firestore rules/indexes が未適用。Cloud Run デプロイ自体は成功。Summary に手動コマンドを記載。 |
| `vercel link` | **致命的 (Vercel パス)** | Step 3c-3e がすべて依存。Step 3a の成果物は残す。Summary に手動コマンドを記載。 |
| `vercel env add` | 中 | デプロイは可能だが env 不足で動作しない可能性。警告して続行。 |
| `vercel deploy --prod` | 高 | 本番デプロイ失敗。Step 3e (Firebase Auth domain) もスキップ (URL が不明)。Summary に手動コマンドを記載。 |
| Firebase Auth domain PATCH | 中 | Google Sign-In が Vercel ドメインで動作しない。Summary に手動設定手順を記載。 |
| `gcloud services api-keys update` (Step 5) | 中 | API Key 制限なし。セキュリティリスクだが動作には影響なし。Summary に警告と手動コマンドを記載。 |
| `gcloud billing budgets create` (Step 5) | 低 | コスト管理なし。動作には影響なし。Summary に手動コマンドを記載。 |

**共通ルール:**
1. **致命的失敗:** 依存する後続ステップをすべてスキップ。ユーザーに即座に通知し、続行するか確認する。
2. **高/中の失敗:** エラーを表示し、依存しないステップは続行。失敗ステップを Summary に `⚠ FAILED` として記載し、手動復旧コマンドを提供。
3. **部分的に成功した状態:** Summary に「部分構築状態」セクションを追加し、何が完了して何が未完了かを明示。例: 「SA は作成済みだが Cloud Run デプロイは未完了」
4. **すべての失敗で:** 失敗コマンドの stderr を Summary に含め、原因の特定を支援する。

### 進捗表示フォーマット

**Cloud Run パス (フル自動化モード):**

```
[1/7] export-from-ai-studio ...
      ✓ firebase-applet-config.json apiKey → プレースホルダー化
      ✓ src/lib/firebase.ts → 環境変数注入に変更
      ✓ .env.example 生成

[2/7] repo-initializer-google (部分実行) ...
      ✓ .gitignore 更新 (.env, service-account*.json 追加)
      ✓ README.md セットアップ手順追記
      — GitHub repo 作成: スキップ (既存)

[3/7] graduate-from-ai-studio [ファイル生成] ...
      ✓ Dockerfile + .dockerignore
      ✓ infra/terraform/ (4 files)
      ✓ .github/workflows/deploy.yml
      ✓ firebase.json + .firebaserc + firestore.indexes.json
      ✓ .env.example 更新

[4/7] cloud-run-deploy [GCP 自動構築] ...
      ✓ GCP API 有効化 (run, artifactregistry, secretmanager, cloudbuild, iam)
      ✓ Artifact Registry リポジトリ作成
      ✓ Secret Manager: gemini-api-key 作成
      ✓ SA 作成: SERVICE-sa@PROJECT.iam.gserviceaccount.com
      ✓ Cloud Run デプロイ: https://SERVICE-xxxxx-an.a.run.app
      ✓ Firebase デプロイ: firestore rules + indexes

[5/8] monitoring-sentry-datadog ...
      ✓ npm install @sentry/node
      ✓ Sentry 初期化コード挿入 (server.ts)
      ✓ Gemini API メトリクス追加

[6/8] 再デプロイ (監視コード反映) ...
      ✓ gcloud run deploy SERVICE --project=PROJECT_ID ...
      ✓ 再デプロイ完了

[7/8] security-hardening-gcp [自動実行] ...
      ✓ Firebase API Key リファラー制限設定
      ✓ Budget alert 作成: $50/月
      ✓ Cloud Audit Logs 確認: 有効

[8/8] デプロイ確認 ...
      ✓ Health check: https://SERVICE-xxxxx-an.a.run.app/health → 200 OK
```

**Cloud Run パス (ファイル生成モード):**
```
Step 3.5 (cloud-run-deploy) はスキップ。
Step 5 はコード内改善のみ。GCP 操作は Summary に手動コマンドとして記載。
```

**Vercel パス (フル自動化モード):**

```
[1/8] export-from-ai-studio ...
      ✓ firebase-applet-config.json apiKey → プレースホルダー化
      ✓ src/lib/firebase.ts → 環境変数注入に変更
      ✓ .env.example 生成

[2/8] repo-initializer-google (部分実行) ...
      ✓ .gitignore 更新 (.env 追加)
      ✓ README.md セットアップ手順追記

[3a/8] vercel-nextjs-config [ファイル生成] ...
      ✓ next.config.ts: output: 'standalone' を除去
      ✓ vercel.json 生成

[3b/8] vercel-link [自動実行] ...
      ✓ vercel link --project my-app --scope my-team --yes
      ✓ .vercel/project.json 生成

[3c/8] vercel-env [自動実行] ...
      ✓ GEMINI_API_KEY: .env.local から読み取り → 設定完了
      ✓ NEXT_PUBLIC_FIREBASE_API_KEY: 設定完了
      ✓ NEXT_PUBLIC_FIREBASE_PROJECT_ID: 設定完了

[3d/8] vercel-deploy [自動実行] ...
      ✓ vercel deploy → https://my-app-xxxx.vercel.app (プレビュー)
      ✓ vercel deploy --prod → https://my-app.vercel.app (本番)

[3e/8] vercel-firebase-auth-domain [自動実行] ...
      ✓ GCP プロジェクト特定: gen-lang-client-0a1b2c3d
      ✓ Firebase Auth authorized domains に my-app.vercel.app を追加

[6/9] monitoring-sentry-datadog ...
      ✓ npm install @sentry/nextjs
      ✓ Sentry 初期化コード挿入
      ✓ Gemini API メトリクス追加

[7/9] 再デプロイ (監視コード反映) ...
      ✓ vercel deploy --prod
      ✓ https://my-app.vercel.app 更新完了

[8/9] security-hardening-gcp [自動実行] ...
      ✓ Firebase API Key リファラー制限 (my-app.vercel.app 追加)
      ✓ Budget alert 設定

[9/9] デプロイ確認 ...
      ✓ https://my-app.vercel.app → 200 OK
```

---

## Phase 5: Summary & Next Steps

全ステップ完了後、生成ファイル一覧と手動作業リストを表示する。

### 出力フォーマット

**Cloud Run パス (フル自動化モード):**

```
=== Migration Complete ===

デプロイ先: Cloud Run (asia-northeast1)
サービス URL: https://SERVICE-xxxxx-an.a.run.app
Health check: 200 OK

生成・変更したファイル:
  (Step 1-3 のファイルリスト)

GCP 構築済み:
  ✓ API 有効化, Artifact Registry, Secret Manager, SA + IAM
  ✓ Cloud Run デプロイ完了
  ✓ Firebase rules + indexes デプロイ完了
  ✓ API Key リファラー制限, Budget alert 設定済み

⚠ 残りの手動作業 (CI/CD 用):
  1. Workload Identity Federation 設定:
     https://github.com/google-github-actions/auth#workload-identity-federation

  2. GitHub Secrets 設定:
     gh secret set WIF_PROVIDER --body "..."
     gh secret set WIF_SERVICE_ACCOUNT --body "SERVICE-sa@PROJECT.iam.gserviceaccount.com"
     gh secret set GCP_PROJECT_ID --body "PROJECT"

  3. 監視の認証情報:
     gh secret set SENTRY_DSN --body "https://xxx@sentry.io/yyy"

  4. API Key ローテーション (推奨):
     apiKey が git history に残っている場合、Google Cloud Console で再発行

  5. CI/CD 初回テスト:
     git push origin main → GitHub Actions が自動デプロイ

=== Next: Development Environment ===
→ 「開発環境セットアップして」 or 「setup dev environment」
```

**Cloud Run パス (ファイル生成モード):**
```
gcloud 未認証のため、GCP 操作は手動コマンドとして記載:
  1. gcloud auth login
  2. gcloud services enable run.googleapis.com ... --project=PROJECT_ID
  3. gcloud artifacts repositories create SERVICE --project=PROJECT_ID ...
  4. gcloud secrets create gemini-api-key --project=PROJECT_ID ...
  5. gcloud iam service-accounts create SERVICE-sa --project=PROJECT_ID
  6. gcloud run deploy SERVICE --project=PROJECT_ID ...
  7. firebase deploy --only firestore --project=PROJECT_ID
  ※ 全コマンドで --project= を明示 (gcloud config set project は使わない)
  (+ WIF, GitHub Secrets, 監視, API Key ローテーション)
```

**Vercel パス (フル自動化モード):**

```
=== Migration Complete ===

デプロイ先: Vercel
本番 URL: https://my-app.vercel.app
プレビュー URL: https://my-app-xxxx.vercel.app

生成・変更したファイル:
  (Step 1-3e のファイルリスト)

Vercel 構築済み:
  ✓ プロジェクトリンク完了
  ✓ 環境変数設定完了 (5 件)
  ✓ 本番デプロイ完了
  ✓ Firebase Auth authorized domains 更新済み

GCP セキュリティ (gcloud 認証済みの場合):
  ✓ Firebase API Key リファラー制限 (my-app.vercel.app 追加)
  ✓ Budget alert 設定済み

⚠ 残りの手動作業:
  1. Sentry DSN の設定:
     vercel env add SENTRY_DSN

  2. 本番デプロイの確認:
     https://my-app.vercel.app が正常に動作しているか確認

  3. API Key ローテーション (推奨):
     apiKey が git history に残っている場合、Google Cloud Console で再発行

  4. カスタムドメイン設定 (任意):
     Vercel Dashboard → Project → Settings → Domains

  5. Git 連携 (任意):
     Vercel Dashboard で GitHub repo と連携 → push で自動デプロイ

=== Next: Development Environment ===
→ 「開発環境セットアップして」 or 「setup dev environment」
```

**Vercel パス (PARTIAL: vercel ✓ / gcloud ✗):**
```
Vercel 構築済み:
  ✓ プロジェクトリンク, 環境変数, デプロイ完了

⚠ gcloud 未認証のため、以下は手動:
  1. Firebase Auth authorized domain に Vercel URL を追加:
     gcloud auth login
     curl -X PATCH ... (vercel-firebase-auth-domain スキル参照)
  2. Firebase API Key リファラー制限:
     gcloud services api-keys update KEY_ID --project=PROJECT_ID ...
  3. Budget alert 設定:
     gcloud billing budgets create --billing-account=... --project=PROJECT_ID
  (+ Sentry DSN, API Key ローテーション)
```

**Vercel パス (FILE-GEN: vercel ✗):**
```
vercel 未認証のため、Vercel 操作は手動コマンドとして記載:
  1. npm i -g vercel && vercel login
  2. vercel link --project PROJECT --scope SCOPE --yes
  3. vercel env add GEMINI_API_KEY
  4. vercel deploy && vercel deploy --prod
  5. Firebase Auth authorized domains に Vercel URL を追加
  (+ 監視, API Key ローテーション)
```

### 手動作業リストの動的生成ルール

**Cloud Run パス:**

| 条件 | 手動作業に含める |
|------|----------------|
| `gcloud` 認証済み | WIF + GitHub Secrets + 監視認証情報 + apiKey ローテーション のみ |
| `gcloud` 未認証 | GCP 構築の全コマンド (API 有効化 → AR → SM → SA → Cloud Run → Firebase) |
| Q4 = Sentry | Sentry DSN の GitHub Secrets 設定 |
| Q4 = Datadog | Datadog API Key の GitHub Secrets 設定 |
| apiKey が git history に存在 | API Key ローテーション手順 |
| WIF 未設定 | WIF 設定ドキュメントへのリンク (常に含める) |

**Vercel パス:**

| 条件 | 手動作業に含める |
|------|----------------|
| `vercel` 認証済み | Sentry DSN 設定 + カスタムドメイン (任意) + apiKey ローテーション のみ |
| `vercel` 未認証 | Vercel 操作の全コマンド (login → link → env → deploy → Firebase Auth domain) |
| `gcloud` 未認証 | Firebase Auth authorized domain 手動設定 + Security hardening コマンド |
| Q4 = Sentry | `vercel env add SENTRY_DSN` |
| apiKey が git history に存在 | API Key ローテーション手順 |

---

## Common Mistakes

- **CLI 未認証のまま進む** → ファイル生成モードになり、インフラ構築・デプロイが全部手動になる。Phase 0 で `gcloud auth login` / `vercel login` を強く推奨。
- **Step 0 (CLAUDE.md) なしで進む** → Step 3 のフレームワーク検出精度が下がる。CLAUDE.md があると情報が補完される。
- **既存ファイルの衝突で「上書き」を安易に選ぶ** → 既にカスタマイズされた Dockerfile や workflow を壊す可能性。diff を確認すること。
- **WIF と GitHub Secrets を設定しない** → フル自動化モードでも CI/CD は WIF (Cloud Run) / Git 連携 (Vercel) がないと自動デプロイにならない。
- **apiKey ローテーションを忘れる** → git history に残った apiKey は取り消せない。Google Cloud Console で再発行が必要。
- **Secret の値確認を忘れる** → Step 3.5 / 3c で `.env` / `.env.local` から値を自動読み取りするが、ファイルがない場合は空の値が設定される。事前に値があることを確認。
- **Vercel で `output: 'standalone'` を残す** → Vercel では不要で、ビルドエラーの原因になる。Step 3a で自動除去するが、手動でも確認すること。
- **Step 4.5 の再デプロイ失敗を見逃す** → 監視コード追加後の再デプロイが失敗すると、本番に監視が反映されない。エラーが出たら Summary の手動作業を確認。
