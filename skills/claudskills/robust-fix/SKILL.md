---
name: robust-fix
description: robust-review の S-Critical/S-High Finding を定型修正パターン（unwrap除去、injection対策、未チェックインデックス等）で自動修正し、各修正後に検証ゲート（build/type/test）で安全を確認する。USE WHEN robust-review 直後、Tier 2 Finding の一括処理、リリース前の堅牢性ホットフィックス。SKIP 設計判断を伴う修正は Tier 1 エスカレーション、仕様乖離の修正は spec-fix、汎用バグは fix-with-verify を使うこと。
argument-hint: "[file-path or 'all'] [--dry-run]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-opus-4-7
---

# 堅牢性 Finding 自動修正

`/robust-review` で検出された S-Critical / S-High の Finding を自動修正し、検証ゲートで修正の安全性を確認する。

---

## 使い方

```
/robust-fix              # 直前の robust-review Finding を修正
/robust-fix all          # robust-review all を実行してから修正
/robust-fix src/api.rs   # 指定ファイルの robust-review → 修正
/robust-fix --dry-run    # 修正計画のみ出力（実行しない）
```

---

## 実行フロー

### Step 1: Finding の取得

Finding の取得元（優先順）:
1. 会話中に直前の `/robust-review` 出力がある → そこから Finding を抽出
2. 引数にファイルパスまたは `all` が指定 → `/robust-review` 相当のチェックを先に実行
3. どちらもない → `git diff --name-only HEAD` の変更ファイルに対してチェック実行

### Step 2: 修正対象の選別

| 深刻度 | 対応 |
|--------|------|
| S-Critical | **必ず修正** |
| S-High | **必ず修正** |
| S-Medium | 修正しない（報告のみ） |
| S-Low | 修正しない（報告のみ） |

修正パターンの判定:

| Finding カテゴリ | 定型修正パターン | 修正内容 |
|-----------------|-----------------|---------|
| SQL インジェクション | `format!()` / テンプレートリテラル → バインド | `.bind()` / パラメータ化 |
| XSS | 未サニタイズ出力 | サニタイズ関数の適用 |
| unwrap() / expect() | パニック源 | `?` 演算子 / `match` / `.unwrap_or()` |
| 未チェックインデックス | `arr[i]` | `.get(i)` / 境界チェック |
| 0 除算 | `a / b` | 事前チェック + エラーハンドリング |
| todo!() / unimplemented!() | 未実装マーカー | 仕様書に基づく実装 or エラー返却 |
| ハードコード機密情報 | リテラル値 | 環境変数 / 設定ファイル参照 |
| as キャスト | 暗黙の切り捨て | `try_into()` / `checked_*` |

定型パターンに該当しない S-Critical/S-High:
- 修正を試みるが、**自信度が低い場合はスキップして報告に含める**
- 「修正に設計判断が必要」と判断した場合は Tier 1 エスカレーション候補として報告

### Step 3: 修正の実行

`--dry-run` 指定時はここで停止し、修正計画を出力する。

1. Finding ごとに修正を実行（Edit ツール使用）
2. 修正単位: **1 Finding = 1 修正**（複数 Finding をまとめない）
3. 各修正後に **検証ゲートを実行**:

### Step 4: 検証ゲート

修正ごとに以下を順次実行（1つでも失敗したら修正をリバートする判断へ）:

| ゲート | 検出方法 | コマンド |
|--------|---------|---------|
| ビルド | Cargo.toml / package.json / go.mod 等 | `cargo check` / `npm run build` / `go build ./...` |
| 型チェック | 同上 | `cargo clippy` / `npx tsc --noEmit` / `go vet` |
| テスト | 同上 | `cargo test` / `npm test` / `go test ./...` |

CLAUDE.md に `## Commands` セクションがある場合はそのコマンドを優先使用する。

### Step 5: 失敗時のリバート判断

検証ゲート失敗時:
1. エラー内容を解析
2. **修正起因のエラー** → 修正を元に戻す（`git checkout -- {file}`）→ 次の Finding へ
3. **既存のエラー**（修正前から存在） → 修正は維持 → 既存エラーとして報告
4. 同一 Finding の修正が **3回連続失敗** → スキップして報告に含める

---

## 出力形式

```
╔══════════════════════════════════════╗
║  堅牢性修正レポート                   ║
╚══════════════════════════════════════╝

■ サマリー
  修正成功:    {n} 件
  スキップ:    {n} 件（定型パターン外 or 修正失敗）
  S-Medium 以下: {n} 件（対象外 — 報告のみ）

═══ 修正済み ═══

[1] SEC-1 | S-Critical | SQL インジェクション
  ファイル: <path/to/handler>:<N>
  修正: format!() → .bind() に変更
  検証: build:pass type:pass test:pass

[2] ROB-3 | S-Critical | unwrap() パニック源
  ファイル: <path/to/file>:<N>
  修正: unwrap() → ? 演算子に変換
  検証: build:pass type:pass test:pass

═══ スキップ（要手動対応） ═══

[S-1] ROB-5 | S-High | 同時書き込み対策
  ファイル: <path/to/repository>:<N>
  理由: トランザクション分離レベルの設計判断が必要
  推奨: エスカレーション（Tier 1）

═══ 報告のみ（S-Medium 以下） ═══

[I-1] ROB-8 | S-Medium | 空リスト未処理
  ファイル: <path/to/file>:<N>
[I-2] SEC-4 | S-Low | .env の .gitignore 確認
```

---

## パイプライン統合

impl-orchestrator の Stage 5 から呼ばれる場合:
- Finding リストがオーケストレーターから直接渡される（Step 1 をスキップ）
- 修正後の検証ゲート結果がオーケストレーターの `gate_results` に反映される
- スキップされた Finding はエスカレーション分類に回される

スタンドアロン実行時:
- 自分で `/robust-review` 相当のチェックを実行してから修正
