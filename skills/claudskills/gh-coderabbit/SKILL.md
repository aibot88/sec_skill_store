---
name: gh:coderabbit
description: "Python向け統合コードレビュー。Quality/Security/Performance/Architecture/Anti-Fallback + CodeRabbitパターンを全検出"
---

# /gh:coderabbit - 統合コードレビュー

Python限定の包括的コードレビューコマンド。
sc:analyzeの4ドメイン分析とCodeRabbitパターン検出を統合し、Phase構造で明確な実行フローを提供。

## Triggers

- PR作成前の事前レビュー
- コード品質の包括的評価
- リファクタリング対象の洗い出し
- セキュリティ/パフォーマンス問題の事前検出

## Usage

```
/gh:coderabbit [target] [--depth quick|deep]
```

- `target`: 対象パス（省略時はプロジェクト全体）
- `--depth quick`: Phase 1 (Lint) のみ実行
- `--depth deep`: 全Phase実行（デフォルト）

## Phase Structure

### Phase 0: Setup（逐次実行）

1. **LEARNINGS.md読み込み**: 既知パターンとチェックリスト取得
2. **対象ファイル探索**: `Glob: **/*.py` で Python ファイル発見

```yaml
Tools:
  - Read: LEARNINGS.md
  - Glob: **/*.py (対象パス内)
```

### Phase 1: Lint + Dead Code（並列実行）

Ruff + Vulture による自動検出を実行。

```yaml
Tools（並列実行 - ruff系とvulture系は独立）:
  並列グループA:
    - Bash: ruff check --output-format=json [target]
    - Bash: ruff format --check [target]
  並列グループB:
    - Bash: vulture [target] --min-confidence 80  # Dead Code検出
```

**Vulture検出対象**:

| 種類 | 説明 | 信頼度 |
|------|------|--------|
| 未使用関数 | 呼び出されていない関数定義 | 60-100 |
| 未使用クラス | インスタンス化されていないクラス | 60-100 |
| 未使用メソッド | 呼び出されていないメソッド | 60-100 |
| 未使用変数 | 代入後使用されていない変数 | 60-100 |
| 未使用インポート | ruff F401 と重複、クロスチェック | 100 |
| 到達不能コード | return/raise 後のコード | 100 |

**注意**: `--min-confidence 80` で誤検出を抑制。フレームワーク用コールバック等は whitelist で除外。

**Ruff自動検出ルール**:

| ルール | 説明 | 頻度 |
|--------|------|------|
| FBT001, FBT002 | Boolean位置引数 | 高 |
| ANN202, ANN204 | 戻り値型アノテーション欠落 | 高 |
| PIE790 | 不要な `pass` 文 | 高 |
| RUF022 | `__all__` ソート順 | 中 |
| RUF043 | 正規表現にraw文字列未使用 | 中 |
| G004 | f-string使用のログ文 | 中 |
| TRY401 | 冗長な例外ログ | 中 |

### Phase 2: Pattern Scan（並列実行）

全ドメインのパターンを並列Grepで検索。

```yaml
並列実行グループ:
  # Quality ドメイン
  - Grep: "def \\w+\\([^)]*\\):" (型ヒント欠落候補)
  - Grep: '"""' 欠落（docstring検出）
  
  # Security ドメイン
  - Grep: "eval\\(|exec\\(|subprocess\\.call" (コードインジェクション)
  - Grep: "password|secret|token.*=.*['\"]" (ハードコード認証情報)
  - Grep: "pickle\\.load|yaml\\.load(?!.*Loader)" (安全でないデシリアライズ)
  
  # Performance ドメイン
  - Grep: "for.*in.*for.*in" (ネストループ - O(n²)候補)
  - Grep: "\\+= .*\\[|\\]\\.append" (ループ内リスト操作)
  - Grep: "time\\.sleep" (同期的待機)
  
  # Architecture ドメイン
  - Grep: "from.*import.*\\*" (ワイルドカードインポート)
  - Grep: "global\\s+\\w+" (グローバル変数使用)
  
  # CodeRabbit パターン
  - Grep: "/ (count|total|len\\([^)]+\\)|original_\\w+)" (ゼロ除算リスク)
  - Grep: "MIN_CELLS\\s*=\\s*\\d+" (Off-by-one候補)
  - Grep: "\\[\\d+\\]" (固定インデックスアクセス)
  - Grep: "def __init__\\([^)]*\\):" (-> None欠落候補)

  # Anti-Fallback ドメイン
  - Grep: "except\\s+\\w*(?:Exception|Error).*:\\s*(?:return|pass)" (catch-all + デフォルト返却/握りつぶし)
  - Grep: "except\\s*:\\s*(?:pass|return|continue)" (bare except + 握りつぶし)
  - Grep: "getattr\\(.*,.*,.*\\)" (getattr 3引数 - サイレントフォールバック候補)
  - Grep: "\\.get\\(.*,\\s*(?:None|False|0|\\[\\]|\\{\\}|''|\"\")" (dict.get + デフォルト値 - 必須設定値候補)
  - Grep: "or\\s+(?:default_|fallback_|FALLBACK)" (明示的フォールバック変数)
  - Grep: "except.*(?:Exception|Error).*:\\s*logger\\.(?:warning|debug)" (例外ダウングレード候補)
```

### Phase 3: Evaluate（逐次実行）

検出結果を評価・分類。

```yaml
評価基準:
  Critical: 実行時エラー、セキュリティ脆弱性、エラー完全消失(except:pass)
  High: データ破損リスク、パフォーマンス問題、catch-all+デフォルト返却(根本原因隠蔽)
  Medium: 保守性問題、型安全性、getattr/dict.getフォールバック(意図確認要)
  Low: スタイル、ドキュメント、明示的フォールバック変数(命名問題)
  
アクション:
  1. 重要度分類（Critical > High > Medium > Low）
  2. LEARNINGS.md との照合（既知パターンか？）
  3. カテゴリ別グルーピング
  4. 新規パターン候補の抽出
```

### Phase 4: Report（逐次実行）

構造化された結果を出力。

## 出力フォーマット

```markdown
## /gh:coderabbit レビュー結果: [target]

### 概要
- 対象ファイル: X件
- Ruff検出: Y件
- Vulture検出: V件（Dead Code）
- パターン検出: Z件
- Anti-Fallback検出: F件
- 重要度: Critical X / High Y / Medium Z / Low W

### Critical Issues
| ファイル | 行 | カテゴリ | 説明 |
|---------|---|----------|------|

### High Priority
| ファイル | 行 | カテゴリ | 説明 |
|---------|---|----------|------|

### Medium Priority
（省略可能）

### LEARNINGS.md 照合
- 既知パターン一致: X件
- 新規パターン候補: Y件（LEARNINGS.md更新推奨）

### 推奨アクション
1. [最優先修正項目]
2. [次の修正項目]
```

## 検出パターン詳細

### Quality ドメイン

| パターン | 検出方法 | 説明 |
|---------|---------|------|
| 型ヒント欠落 | Grep: 関数定義 | ANN系ルール対象 |
| docstring欠落 | Grep: クラス/関数直後 | D100-D417系対象 |
| 複雑度超過 | Ruff: C901 | 認知的複雑度 |

### Security ドメイン

| パターン | 検出方法 | 説明 |
|---------|---------|------|
| コードインジェクション | Grep: eval/exec/subprocess | S102, S307 |
| ハードコード認証情報 | Grep: password/secret/token | S105, S106 |
| 安全でないデシリアライズ | Grep: pickle.load/yaml.load | S301, S506 |
| SQL インジェクション | Grep: f-string + execute | S608 |

### Performance ドメイン

| パターン | 検出方法 | 説明 |
|---------|---------|------|
| O(n²)候補 | Grep: ネストループ | 大規模データで問題 |
| リスト連結ループ | Grep: += [] パターン | リスト内包推奨 |
| 同期的待機 | Grep: time.sleep | asyncio.sleep推奨 |

### Architecture ドメイン

| パターン | 検出方法 | 説明 |
|---------|---------|------|
| ワイルドカードインポート | Grep: from X import * | 名前空間汚染 |
| グローバル変数 | Grep: global keyword | 依存関係不明確 |
| 循環インポート候補 | Read: 相互参照分析 | 構造問題 |

### Dead Code ドメイン（Vulture）

| パターン | 検出方法 | 重要度 |
|---------|---------|--------|
| 未使用関数 | Vulture: unused function | High |
| 未使用クラス | Vulture: unused class | High |
| 未使用メソッド | Vulture: unused method | Medium |
| 未使用変数 | Vulture: unused variable | Low |
| 到達不能コード | Vulture: unreachable code | High |
| 未使用プロパティ | Vulture: unused property | Medium |
| 未使用属性 | Vulture: unused attribute | Low |

**Whitelist推奨ケース**:
- フレームワークコールバック（pytest fixtures, Django signals等）
- `__all__` でエクスポートされる公開API
- 動的呼び出し（`getattr`、リフレクション）

### CodeRabbit パターン

| パターン | 検出方法 | 説明 |
|---------|---------|------|
| ゼロ除算リスク | Grep: `/ count\|total\|len()` | ガード必須 |
| Off-by-one | Grep: MIN_CELLS定義 + max index確認 | MIN_CELLS = max_index + 1 |
| インデックス範囲 | Grep: 固定インデックス | 境界チェック必須 |
| `__init__` 戻り値型 | Grep: def __init__ without -> None | ANN204 |
| `Path` vs `str \| Path` | Grep: `: Path[^|]` | API一貫性 |

### Anti-Fallback ドメイン

| パターン | 検出方法 | 重要度 | 説明 |
|---------|---------|--------|------|
| エラー握りつぶし | Grep: `except.*: pass` | Critical | エラー情報の完全消失 |
| bare except | Grep: `except:` (型指定なし) | Critical | 全例外を無差別キャッチ |
| catch-all + デフォルト返却 | Grep: `except Exception.*: return None` | High | 根本原因の隠蔽 |
| 例外ダウングレード | Grep: `except.*Error.*: logger.warning` | High | errorレベルで記録すべき |
| getattr フォールバック | Grep: `getattr(obj, attr, default)` | Medium | 属性欠落を隠蔽する可能性 |
| dict.get デフォルト値 | Grep: `.get(key, None\|False\|0)` | Medium | 必須設定値なら`dict[key]`を使用 |
| 明示的フォールバック変数 | Grep: `or default_\|fallback_` | Low | 命名で意図は明確だが要確認 |

**許容ケース**（誤検知として除外）:

- オプション設定値の `dict.get(key, default)` — 明示的にオプショナルと判断できる場合
- UI/表示系の `getattr` — 表示崩れ防止のgraceful degradation
- テストコード内のフォールバック — テストヘルパーでの使用
- `logging.getLogger` 等のライブラリ標準パターン

### テスト品質

| パターン | 検出対象 | 説明 |
|---------|---------|------|
| NaNエッジケース | tests/内のnp.nan/NaN | 欠損値テスト |
| 空データケース | tests/内のempty/len==0 | 空入力テスト |
| 境界値テスト | tests/内の0, -1, MAX | 境界条件テスト |

## Tool Coordination

| Phase | Tools | 並列/逐次 |
|-------|-------|----------|
| 0 | Read, Glob | 逐次 |
| 1 | Bash (ruff, vulture) | **並列** |
| 2 | Grep ×16-21 | **並列** |
| 3 | 内部処理 | 逐次 |
| 4 | 出力生成 | 逐次 |

## Examples

### プロジェクト全体のレビュー

```
/gh:coderabbit
# Phase 0-4 全実行
# 全ドメイン + CodeRabbitパターン検出
```

### 特定ディレクトリのレビュー

```
/gh:coderabbit src/data
# src/data ディレクトリのみ対象
```

### クイックチェック（Lintのみ）

```
/gh:coderabbit --depth quick
# Phase 0-1 のみ（Ruff検出）
# 手動パターン検出はスキップ
```

## Boundaries

**Will:**

- `ruff check` を実行してRuffルール違反を検出
- `vulture` を実行してデッドコード（未使用関数/クラス/変数）を検出
- 6ドメイン（Quality/Security/Performance/Architecture/Dead Code/Anti-Fallback）のパターン検出
- CodeRabbitが指摘するパターンを手動で検出
- LEARNINGS.md との照合と新規パターン提案
- 重要度に基づいた優先度付け

**Will Not:**

- コードの自動修正（提案のみ）
- 実行時テスト（静的解析のみ）
- Python以外の言語サポート
- 外部サービス連携（CodeRabbit APIは使用しない）

## LEARNINGS.md 連携

1. **事前読み込み**: Phase 0 で LEARNINGS.md を読み込み
2. **パターン照合**: Phase 3 で既知パターンとの一致を報告
3. **新規提案**: 頻出する未登録パターンを LEARNINGS.md 更新候補として提案
