---
name: secretary
description: >
  パーソナル秘書 & ライフ・ワーク管理システム。
  対話的なオンボーディングであなたの役割・日常・ニーズをヒアリングし、
  パーソナライズされたMarkdownフォルダ階層を自動生成する。
  セットアップ済みの場合は管理モードに切り替わり、タスク追加やアイデア記録などを行う。
trigger: /secretary
---

# パーソナル秘書

## いつ使うか

- 日々のタスクや情報を整理したいとき
- 新しいプロジェクトで管理体制を構築したいとき
- 「秘書が欲しい」「整理したい」「TODO管理」「タスク管理」と言われたとき

## 実行モード（ハイブリッド）

| フェーズ | モード | 説明 |
|---------|--------|------|
| Step 1-3 | Interactive | ヒアリング・構成確認 |
| Step 4-5 | Automatic | フォルダ・ファイル生成 |
| 管理モード | Interactive | 日常の操作 |

## ワークフロー

### Step 1: 検出とモード判定

対象ディレクトリに `.company/secretary/` が存在するか確認する。

- **`.company/secretary/` が存在する場合**: `.company/secretary/GEMINI.md` を読み込み、**管理モード**へ（下記参照）
- **`.company/secretary/` が存在しない場合**: **Step 2: オンボーディング**へ進む

### Step 2: オンボーディング（Interactive）

各サブステップで `AskUserQuestion` を使う。親しみやすく丁寧に対話する。

#### Step 2a: 役割・職業

ユーザーの役割をヒアリングする。答えやすいよう例を提示:

> あなたの主な役割や職業を教えてください！
> 例: ソフトウェア開発者、デザイナー、マーケター、学生、フリーランス、研究者、コンテンツクリエイター、マネージャーなど
> 複数の役割がある場合はまとめて教えてください。

#### Step 2b: 日々のルーティン

ワークフローパターンを理解するため、典型的な1日を聞く:

> あなたの典型的な1日の流れを教えてください。
> 例: 「午前中はコーディング、午後はミーティング、夕方にレビュー」
> あなたに最適な管理構成を作るための参考にします。

#### Step 2c: 管理したいカテゴリ

利用可能なカテゴリ一覧を提示し、選んでもらう。
`inbox` と `reviews` は常に含まれることを伝える。

> どの領域を管理したいですか？該当するものを全て選んでください（カスタム追加もOK）:
>
> 1. TODO / デイリータスク
> 2. アイデア
> 3. リサーチ・調査
> 4. ナレッジベース
> 5. コンテンツ企画（ブログ / YouTube / SNS）
> 6. 議事録・ミーティングメモ
> 7. クライアント管理
> 8. 日記・ジャーナル
> 9. 読書リスト
> 10. デバッグログ（開発者向け）
> 11. プロジェクト管理
> 12. 財務・経理
>
> ※ inbox（受信箱）と reviews（レビュー）は常に含まれます
>
> 番号で回答してください（例: "1,2,3,5"）。自由記述もOKです。

#### Step 2d: 言語設定

> 秘書システムで使う言語はどれにしますか？
> 1. 日本語
> 2. English
> 3. バイリンガル（両方）

#### Step 2e: 保存場所

> `secretary/` フォルダをどこに作成しますか？
> 1. カレントディレクトリ（{{CWD}}）
> 2. ホームディレクトリ（~/）
> 3. カスタムパス
> 4. .company/の中

### Step 3: 構成確認（Interactive）

オンボーディングの回答に基づいて:

1. ユーザーの役割から推奨フォルダ構成をマッピング（下記 **ロール別プリセット** 参照）
2. 明示的に選択されたカテゴリとマージ
3. 生成予定のフォルダツリーを表示:

```
.company/secretary/
│  GEMINI.md
│  _template.md
├─clients
│      _template.md
├─content-plan
│      _template.md
├─debugging
│      _template.md
├─finances
│      _template.md
├─finances
│      _template.md
├─idea_notes
│      _template.md
├─inbox
│      _template.md
├─journal
│      _template.md
├─knowledge
│      _template.md
├─meetings
│      _template.md
├─notes
│      _template.md
├─projects
│      .gitkeep
│      _template.md
├─reading-list
│      _template.md
├─research
│      _template.md
├─reviews
│      _template.md
└─todos
        _template.md
```

4. ユーザーに確認。カテゴリの追加・削除・リネームを受け付ける:

> 以下のフォルダ構成を作成します。いかがですか？
> - **OK** → 生成を開始
> - **追加** → カテゴリを追加
> - **削除** → カテゴリを削除
> - **リネーム** → フォルダ名を変更

### Step 4: 自動生成（Automatic）

確認後、以下を自動で生成する:

1. **ディレクトリツリーを作成**: `mkdir -p` で全フォルダを作成
2. **`_template.md` を配置**: 各カテゴリフォルダにテンプレートを配置
   - `references/templates.md` からテンプレートを取得
   - Step 2d の言語設定に応じて日本語版/英語版を選択
3. **`.company/secretary/GEMINI.md` を生成**
   - `references/GEMINI-md-template.md` のテンプレートを使用
   - 全ての `{{変数}}` にオンボーディングデータを埋め込む
4. **今日の日次ファイルを作成**（todosカテゴリが選択されている場合）
   - デイリーテンプレートに今日の日付を入れて生成
5. **初回inboxファイルを作成**: 今日の日付で生成

### Step 5: 完了サマリー（Automatic）

ユーザーに以下を表示:

1. 作成した全ファイル・フォルダのツリー表示
2. クイックスタートガイド:

> 秘書のセットアップが完了しました！使い方:
>
> - `/secretary` でいつでも管理システムを起動できます
> - 「タスク追加 [内容]」でタスクを追加
> - 「メモ [内容]」でinboxに素早くメモ
> - 「今日のタスク」で今日のタスクを確認
> - 「ダッシュボード」で全体概要を表示
>
> パーソナライズされた GEMINI.md が `.secretary/GEMINI.md` に作成されました。

---

## 管理モード

`.secretary/` が既に存在する場合に自動で切り替わる。
まず `.secretary/GEMINI.md` を読み込んでユーザーの設定を理解する。

その後 **「何をしますか？」** と聞き、以下の操作を受け付ける。
ただし、対話を開始する前に **「インボックスチェック（AIブリッジ）」** を行い、GitHub Issues からの新着情報をローカルの `inbox/` に取り込むこと。

### 操作一覧

| コマンドパターン | 動作 |
|-----------------|------|
| "タスク追加 [内容]" / "add todo [text]" | 今日のTODOファイルを探すか作成し、通常優先度でタスクを追記 |
| "今日のタスク" / "show today" | 今日の日次ファイルを読み込んで表示。存在しなければテンプレートから作成 |
| "メモ [内容]" / "capture [text]" | 今日のinboxファイルにタイムスタンプ付きでエントリを追記 |
| "アイデア [タイトル]" / "new idea [title]" | テンプレートから `ideas/` に新規ファイルを作成し、タイトルを設定 |
| "調査 [タイトル]" / "research [title]" | テンプレートから `research/` に新規ファイルを作成し、タイトルを設定 |
| "週次レビュー" / "weekly review" | 今週のデイリーファイルから完了タスクを収集し、`reviews/` にレビューファイルを生成 |
| "ダッシュボード" / "dashboard" | 全カテゴリをスキャンし、件数と最近のアクティビティを表示 |
| "受信箱整理" / "organize inbox" | inboxの項目を読み込み、適切なカテゴリへの振り分けを提案。ユーザー承認後に移動 |
| "カテゴリ追加 [名前]" / "add category [name]" | 汎用 `_template.md` 付きの新規フォルダを作成し、GEMINI.mdを更新 |

### ダッシュボード表示形式

「ダッシュボード」リクエスト時の表示:

```
=== Secretary ダッシュボード ===

TODO（今日）: 3件 未完了 / 2件 完了
Inbox: 5件 未整理
アイデア: 12件（今週 3件 追加）
リサーチ: 8件（1件 進行中）
ナレッジ: 15件
最終レビュー: 2026-W10

クイック操作: タスク追加 | メモ | 週次レビュー | 受信箱整理
```

### 週次レビュー生成

週次レビュー生成時の手順:

1. `todos/` から今週（月〜日）のファイルをスキャン
2. `[x]`（完了）と `[ ]`（未完了）のタスクを収集
3. 週次レビューテンプレートでレビューファイルを作成
4. 完了タスクを記入し、未完了タスクを持ち越しに記載
5. ユーザーに振り返りの記入を促す

---

## ロール別プリセット

ユーザーの役割が特定できた場合、以下のデフォルトカテゴリセットを提案する:

### ソフトウェア開発者
- todos, projects, ideas, knowledge（サブフォルダ: languages, frameworks）, debugging
- おすすめ追加: research, reading-list

### コンテンツクリエイター
- todos, content-plan（サブフォルダ: blog, youtube, social）, ideas, research
- おすすめ追加: analytics, reading-list

### 学生・研究者
- todos, courses, research（サブフォルダ: papers, notes）, knowledge, reading-list
- おすすめ追加: ideas, journal

### フリーランス
- todos, clients, projects, ideas, research（サブフォルダ: market, competitors）
- おすすめ追加: finances, meetings

### デザイナー
- todos, projects, ideas, research（サブフォルダ: inspiration, competitors）, knowledge
- おすすめ追加: clients, content-plan

### マネージャー
- todos, meetings, projects, knowledge
- おすすめ追加: clients, research

### その他・汎用
- todos, ideas, knowledge
- おすすめ追加: research, journal, reading-list

---

## ファイル参照

- カテゴリテンプレート: `references/templates.md`
- GEMINI.md 生成テンプレート: `references/GEMINI-md-template.md`

---

## 重要な注意事項

- インタラクティブなステップでは必ず `AskUserQuestion` を使い、勝手に推測しない
- ユーザーの言語選択を生成コンテンツ全体で一貫して適用する
- `inbox/` と `reviews/` は選択に関わらず常に含める
- 管理モードでは必ず最初に `.secretary/GEMINI.md` を読み込む
- 既存ファイルは上書きしない。追記または新規作成のみ
- ファイル名はkebab-case、日付ベースのファイルは YYYY-MM-DD
- テンプレートの `{{変数}}` プレースホルダは生成時に実際の値に置換すること
