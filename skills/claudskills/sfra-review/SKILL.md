---
name: sfra-review
description: SFRA (Storefront Reference Architecture) code review skill using Swarm pattern. Analyzes controllers, models, ISML, services, jobs for best practices, security, and performance. Triggers on "SFRA review", "SFCC code review", "cartridge review"
version: 1.1.0
triggers:
  - "SFRA review"
  - "SFCC code review"
  - "cartridge review"
  - "SFRA レビュー"
  - "コードレビュー"
---

# SFRA Best Practices Review スキル

SFCC/SFRA コードベースのベストプラクティスレビューを実行する。**Swarm パターン**（並列エージェント実行）で網羅的な分析を行い、P0/P1/P2 の重大度付きレビューレポートを生成。

## 概要

| 項目 | 内容 |
|------|------|
| **対象** | SFRA Storefront + Jobs（app_storefront_base + overlay cartridges） |
| **除外** | Headless/SCAPI/PWA Kit の実装レビュー（別スキルで対応）。SCAPI 移行**準備度**チェックは含む |
| **出力形式** | Markdown レビューレポート（P0/P1/P2 重大度付き） |
| **中間成果物** | `docs/review/.work/` に保存 |
| **最終成果物** | `docs/review/sfra-review.md` |

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator (SKILL.md)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 0: Scope Detection                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Cartridge 構成検出（app_storefront_base, plugin_, int_）  ││
│  │ - Sites/Locales 検出                                        ││
│  │ - 対象ファイル数/LOC 算出                                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                           │                                     │
│  Phase 1: Indexer (sequential)                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Controllers/Routes マップ、ISML 一覧、Services 定義、        ││
│  │ Hooks/Jobs 一覧、Model 一覧を "地図" として生成              ││
│  └─────────────────────────────────────────────────────────────┘│
│                           │                                     │
│  Phase 2: Explorer Swarm (並列 - 7 agents)                      │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│  │controller│ model   │  isml   │ client  │ service │cartridge│  jobs   │
│  │ (sonnet) │ (opus)  │(sonnet) │(sonnet) │ (opus)  │(sonnet) │(sonnet) │
│  └────┬─────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘
│       └──────────┴─────────┼─────────┴─────────┴─────────┴─────────┘│
│                            ▼                                     │
│                     Aggregator (opus)                            │
│                     Two-step Reduce                              │
│                            │                                     │
│  Phase 3: Reviewer Swarm (並列 - 4 agents)                       │
│  ┌─────────┬─────────┬─────────┬─────────┐                      │
│  │perform. │security │ best-   │ anti-   │                      │
│  │ (haiku) │ (opus)  │practice │ pattern │                      │
│  │         │         │ (haiku) │ (haiku) │                      │
│  └────┬────┴────┬────┴────┬────┴────┬────┘                      │
│       └─────────┴─────────┼─────────┘                           │
│                           ▼                                      │
│                    Aggregator (opus)                             │
│                    統合レビュー + Gate 判定                      │
│                           │                                      │
│  Phase 4: Reporter (sonnet)                                      │
│                           ▼                                      │
│                    sfra-review.md                                │
└─────────────────────────────────────────────────────────────────┘
```

## ワークフロー

### Phase 0: スコープ検出

**目的**: レビュー対象の Cartridge 構成と規模を把握

**手順**:
1. プロジェクトルートで cartridge 構成を検出
2. `cartridge` ディレクトリ配下の構造を分析
3. 対象ファイル数と LOC を算出

**検出項目**:
```yaml
scope:
  cartridges:
    - name: "app_storefront_base"
      type: "base"
      path: "cartridges/app_storefront_base"
    - name: "app_custom_mystore"
      type: "overlay"
      path: "cartridges/app_custom_mystore"
    - name: "int_payment"
      type: "integration"
      path: "cartridges/int_payment"
  stats:
    total_files: 450
    total_loc: 25000
    controllers: 35
    models: 28
    templates: 120
    jobs: 8
```

**出力**: `docs/review/.work/00_scope.json`

**Done 条件**: cartridge 構成が検出され、stats が算出されている

---

### Phase 1: Indexer（コードベース地図作成）

**目的**: レビュー対象のコードベース全体像を "地図" として可視化

**入力**: Phase 0 の scope 情報

**手順**:
1. Task ツールで `sfra-indexer` エージェントを起動（model: sonnet）
2. Controllers/Routes のマッピング
3. Models/Decorators の一覧化
4. ISML テンプレートの依存関係
5. Services/Hooks の定義収集
6. Jobs の一覧化

**出力**: `docs/review/.work/01_index.md`

**出力形式**:
```markdown
# SFRA Codebase Index

## Controllers (35 files)
| Controller | Routes | Middleware | Cartridge |
|------------|--------|------------|-----------|
| Account.js | Login, Register, ... | auth, csrf | app_custom |

## Models (28 files)
| Model | Decorators | Used By |
|-------|------------|---------|
| ProductModel.js | base, full | PDP, PLP |

## ISML Templates (120 files)
| Template | Includes | Remote Includes |
|----------|----------|-----------------|
| pdpMain.isml | productCard, reviews | recommendations |

## Services (12 definitions)
| Service ID | Type | Timeout | Retry |
|------------|------|---------|-------|
| payment.authorize | HTTP | 30s | 3 |

## Jobs (8 definitions)
| Job ID | Steps | Schedule |
|--------|-------|----------|
| ProductSync | 3 | Daily 2AM |
```

**Done 条件**: 全カテゴリの index が生成されている

---

### Phase 2: Explorer Swarm（コード分析）

**目的**: 各レイヤーを専門エージェントが並列で分析

**入力**: Phase 1 の index 情報

**手順**:
1. **並列実行**: 7 つの Explorer エージェントを Task ツールで同時起動

```
┌─────────────────────────────────────────────────────────────────┐
│ 並列実行（単一メッセージで複数 Task tool 呼び出し）             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Task(sfra-explorer-controller, model: sonnet)  ──┐              │
│ Task(sfra-explorer-model, model: opus)         ──┼─→ 並列      │
│ Task(sfra-explorer-isml, model: sonnet)        ──┤              │
│ Task(sfra-explorer-client, model: sonnet)      ──┤              │
│ Task(sfra-explorer-service, model: opus)       ──┤              │
│ Task(sfra-explorer-cartridge, model: sonnet)   ──┤              │
│ Task(sfra-explorer-jobs, model: sonnet)        ──┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

2. 各エージェントは担当範囲のみを分析し、ハンドオフ封筒形式で出力
3. **Aggregator 呼び出し**: Two-step Reduce で統合
   - Step 1: JSON 正規化（各エージェントの findings をマージ）
   - Step 2: Adjudication Pass（矛盾解消、重複排除）

**Explorer エージェント一覧**:

| Agent | Model | 担当範囲 |
|-------|-------|----------|
| explorer-controller | sonnet | Controllers, Routes, Middleware |
| explorer-model | opus | Models, Decorators, Transactions |
| explorer-isml | sonnet | Templates, Resource Bundles |
| explorer-client | sonnet | Client-side JS, CSS |
| explorer-service | opus | Services, External Integrations |
| explorer-cartridge | sonnet | Architecture, Layering |
| explorer-jobs | sonnet | Jobs, Batch Processing |

**出力**:
- `docs/review/.work/02_explorer/*.md`（各エージェントの生出力）
- `docs/review/.work/03_explorer_unified.md`（統合済み分析）

**Done 条件**:
- 7 エージェントすべてが status: ok で完了
- explorer_unified.md が生成されている

---

### Phase 3: Reviewer Swarm（品質レビュー）

**目的**: Cross-cutting concerns を専門エージェントが並列でレビュー

**入力**: Phase 2 の統合分析結果

**手順**:
1. **並列実行**: 4 つの Reviewer エージェントを Task ツールで同時起動

```
┌─────────────────────────────────────────────────────────────────┐
│ 並列実行（単一メッセージで複数 Task tool 呼び出し）             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Task(sfra-reviewer-performance, model: haiku)  ──┐              │
│ Task(sfra-reviewer-security, model: opus)      ──┼─→ 並列      │
│ Task(sfra-reviewer-bestpractice, model: haiku) ──┤              │
│ Task(sfra-reviewer-antipattern, model: haiku)  ──┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

2. 各 Reviewer は P0/P1/P2 の重大度付きで指摘事項を出力
3. **Aggregator 呼び出し**: 指摘の統合と Gate 判定

**Reviewer エージェント一覧**:

| Agent | Model | 担当範囲 |
|-------|-------|----------|
| reviewer-performance | haiku | Caching, require scope, API calls |
| reviewer-security | opus | XSS, CSRF, Input validation, PII |
| reviewer-bestpractice | haiku | SFRA guidelines, patterns |
| reviewer-antipattern | haiku | Known anti-patterns detection |

**出力**:
- `docs/review/.work/04_reviewer/*.md`（各エージェントの生出力）
- `docs/review/.work/05_review_unified.md`（統合済みレビュー）

**Done 条件**:
- 4 エージェントすべてが status: ok で完了
- Gate 判定が実行されている

---

### Phase 4: Reporter（レポート生成）

**目的**: 最終レビューレポートを生成

**入力**: Phase 3 の統合レビュー結果

**手順**:
1. Task ツールで `sfra-reporter` エージェントを起動（model: sonnet）
2. テンプレートに基づいてレポート生成
3. Executive Summary 作成
4. カテゴリ別 Findings 整理
5. Recommendations 作成

**出力**: `docs/review/sfra-review.md`

**Done 条件**: レポートが生成され、P0/P1/P2 のサマリーが含まれている

---

## Gate 判定ロジック

### P0 (Blocker) - 1 つで FAIL

| Category | Trigger |
|----------|---------|
| Security | XSS 脆弱性、PII ログ出力、CSRF 未対策 |
| Transaction | Transaction 境界外の書き込み |
| Architecture | app_storefront_base 直接編集 |
| Performance | グローバル require が 10 箇所以上 |

### P1 (Major) - 2 つ以上で FAIL

| Category | Trigger |
|----------|---------|
| Controller | server.append() での ViewData 変更 |
| ISML | isscript 内 business logic 5 箇所以上 |
| Service | タイムアウト/リトライ未設定 |
| Cartridge | Naming collision 検出 |
| Jobs | 冪等性未保証、Transaction 境界違反 |

### P2 (Minor) - 要対応リスト

| Category | Trigger |
|----------|---------|
| Performance | キャッシュ未活用 |
| Code Quality | Magic numbers |
| Best Practice | 軽微なガイドライン違反 |

### Gate 判定結果

```yaml
gate_decision:
  p0_count: 0
  p1_count: 3
  p2_count: 12
  result: "PASS"  # P0=0 かつ P1<2 なら PASS
  overall_status: "REVIEW_NEEDED"  # P1>0 または P2>5 なら要レビュー
```

---

## エージェント呼び出しパターン

### Phase 2 Explorer Swarm 呼び出し例

```markdown
7 つの Explorer エージェントを並列で起動する。
単一のメッセージ内で複数の Task tool を呼び出す。

Task(
  description: "Analyze SFRA controllers",
  prompt: "Index ファイル (.work/01_index.md) を読み、
           Controllers/Routes/Middleware を分析して
           ベストプラクティス違反を検出せよ。
           出力: .work/02_explorer/controller.md",
  subagent_type: "sfra-explorer-controller",
  model: "sonnet"
)

Task(
  description: "Analyze SFRA models",
  prompt: "Index ファイル (.work/01_index.md) を読み、
           Models/Decorators/Transactions を分析して
           ベストプラクティス違反を検出せよ。
           出力: .work/02_explorer/model.md",
  subagent_type: "sfra-explorer-model",
  model: "opus"
)

// ... 残り 5 エージェント同様
```

### Aggregator 呼び出し例

```markdown
全 Explorer の出力が揃ったら Aggregator を呼び出す。

Task(
  description: "Aggregate explorer findings",
  prompt: ".work/02_explorer/ 配下の全ファイルを読み、
           Two-step Reduce で統合せよ。
           Step 1: findings のマージ
           Step 2: 矛盾解消・重複排除
           出力: .work/03_explorer_unified.md",
  subagent_type: "sfra-aggregator",
  model: "opus"
)
```

---

## ツール使用ルール

### 各 Phase で使用可能なツール

| Phase | 許可ツール | 備考 |
|-------|-----------|------|
| Phase 0 | Glob, Bash (read-only) | ファイル検出のみ |
| Phase 1 | Read, Glob, Grep | Index 作成 |
| Phase 2 | Read, Glob, Grep | 分析のみ |
| Phase 3 | Read | レビューのみ |
| Phase 4 | Read, Write | レポート生成 |

### 書き込み制限

- **書き込み可能**: `docs/review/` および `docs/review/.work/` のみ
- **読み取り専用**: その他すべてのディレクトリ

---

## Orchestrate コマンド

自動実行モードでは、以下のフローで全 Phase を順次実行する:

### 自動実行フロー

```
/sfra-review → Phase 0 → Phase 1 → Phase 2 (7 agents) → Aggregator
            → Phase 3 (4 agents) → Aggregator + Gate → Phase 4 → Report
```

### Done 判定

各 Phase の完了条件をチェックし、次の Phase に自動遷移:

| Phase | Done 条件 |
|-------|----------|
| 0 | `00_scope.json` が生成済み |
| 1 | `01_index.md` が生成済み |
| 2 | 7 Explorer が status: ok、`03_explorer_unified.md` 生成済み |
| 3 | 4 Reviewer が status: ok、Gate 判定完了 |
| 4 | `sfra-review.md` が生成済み |

### エラーリカバリー

- Explorer 一部失敗: 成功分のみで Aggregator 実行（警告付き）
- Reviewer 失敗: Phase 3 からリトライ
- Aggregator 失敗: 対応する Phase からリトライ

---

## エラーハンドリング

| 状況 | 対応 |
|------|------|
| Cartridge 未検出 | status: blocked、ユーザーにパス確認を求める |
| Explorer 一部失敗 | 警告を出力し、成功したものだけで続行 |
| 全 Explorer 失敗 | status: blocked、原因を報告 |
| Aggregator 失敗 | Phase 2 からリトライ |
| Reporter 失敗 | Phase 4 からリトライ |

---

## 出力ディレクトリ構造

```
docs/review/
├── .work/                          # 中間成果物（.gitignore 推奨）
│   ├── 00_scope.json              # Phase 0: スコープ
│   ├── 01_index.md                # Phase 1: Index
│   ├── 02_explorer/               # Phase 2: Explorer 生出力
│   │   ├── controller.md
│   │   ├── model.md
│   │   ├── isml.md
│   │   ├── client.md
│   │   ├── service.md
│   │   ├── cartridge.md
│   │   └── jobs.md
│   ├── 03_explorer_unified.md     # Phase 2: 統合分析
│   ├── 04_reviewer/               # Phase 3: Reviewer 生出力
│   │   ├── performance.md
│   │   ├── security.md
│   │   ├── bestpractice.md
│   │   └── antipattern.md
│   └── 05_review_unified.md       # Phase 3: 統合レビュー
└── sfra-review.md                 # 最終レポート
```
