| name | description |
|------|-------------|
| daily-news | 日々情報収集 |

# トレンドネタ収集

はてなブックマークIT人気エントリーとHacker Newsの人気記事を収集し、
ideas/daily/YYYYMMDD-trend.md に保存する。

## 実行手順

### 0. ユーザープロファイル読み込み

CLAUDE.md を読み込み、以下の興味領域を理解する：
- AI(開発、セキュリティ、ローカルAI、ツール、それらの応用)
- Webセキュリティ/ハッキング（OWASP、脆弱性、サプライチェーン攻撃）
- Java / Spring Boot / バックエンド開発全般

### 1. トレンド情報の収集

以下のサイトから最新のトレンド情報を取得：

**日本市場（はてブIT）**
- https://b.hatena.ne.jp/hotentry/it
- https://b.hatena.ne.jp/hotentry/it/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0
- https://b.hatena.ne.jp/hotentry/it/AI%E3%83%BB%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92
- 各エントリーのタイトル、元記事URL、ブックマーク数を必ず取得
- はてブのエントリーページURLではなく、リンク先の元記事URLを抽出

**グローバル（Hacker News）**
- https://news.ycombinator.com/
- 各記事のタイトル、HNコメントページURL、ポイント数を取得
- タイトルは日本語に翻訳して出力

**Reddit（10サブレッド）**
- WebFetchツールはreddit.comをブロックするため、Bashツールでcurlを使用
- 各サブレッドから /hot.json?t=day&limit=10 で上位10件を取得
- old.reddit.com を使用
- User-Agent ヘッダーを設定: "User-Agent: neta-trend-collector/1.0"
- タイトルは日本語に翻訳して出力

取得例:
curl -s -H "User-Agent: neta-trend-collector/1.0" \
  "https://old.reddit.com/r/programming/hot.json?t=day&limit=10" | \
  jq -r '.data.children[] | "\(.data.title)|\(.data.ups)|\(.data.num_comments)|https://www.reddit.com\(.data.permalink)"'

対象サブレッド:

AI系:
- r/OpenAI
- r/LocalLLaMA
- r/ClaudeCode

セキュリティ系：
- r/netsec
- r/cybersecurity

コア技術系:
- r/java
- r/programming

個人開発系:
- r/indiehackers
- r/selfhosted

### 2. 分析

収集した情報を以下の観点で分析：

**興味領域マッチング（最優先）**
- 各記事を興味領域と照合し、関連度を評価
- 高関連度の記事を注目トピックの最上位に配置

**興味度の定義**:
- ★★★: 興味領域に直接関連（AI、キーボード、個人開発、Spring Boot等）
- ★★: 間接的に関連（技術トレンド全般、エンジニアリング文化）
- ★: 一般的なIT/技術ニュース

はてブIT

- 日本のエンジニアに刺さりやすい話題
- 議論を呼びそうなトピック
- 技術トレンド（AI、開発手法、ツール等）

Hacker News
- グローバルで話題の技術トレンド
- スタートアップ・プロダクト関連
- セキュリティ関連（脆弱性、攻撃手法、インシデント）
- 議論を呼んでいるトピック（ポイント数が高い）

Reddit（13サブレッド）
- セキュリティ系：最新の脅威、実践的な攻撃・防御手法
- AI系：OpenAI、ローカルLLM、Claude Code関連
- OSS/個人開発系：OSSプロジェクト、個人開発、Web開発
- 投票数（ups）とコメント数でコミュニティの反応を評価
- 議論が活発なトピック（コメント数が多い）を優先

### 3. 出力

まず「情報収集完了。」というメッセージを返してから、
結果を ideas/daily/YYYYMMDD-trend.md に保存。
フォーマット要約の箇所は元記事ＵＲＬの記事の本文を、フォーマットに記載された形にして記載。

フォーマット:

# トレンドネタ: YYYY-MM-DD

## はてブIT（日本市場）

### 注目トピック

| タイトル | ブクマ数 | 興味度 | カテゴリ | 要約 |
|---------|---------|--------|---------|------|
| [タイトル](元記事URL) | XXX users | ★★★/★★/★ | AI/開発等 | 150文字以内の要約 |

### 全エントリー

1. [タイトル](元記事URL) (XXX users) - 概要

## Hacker News（グローバル）

### 注目トピック

| タイトル | ポイント | 興味度 | カテゴリ | 要約 |
|---------|---------|--------|---------|------|
| [タイトル](HNコメントURL) | XXXpt | ★★★/★★/★ | AI等 | 日本語で150文字以内の要約 |

### 全エントリー

1. [タイトル](HNコメントURL) (XXXpt) - 概要

## Reddit（10サブレッド）

### 注目トピック

| タイトル | 投票数 | コメント数 | 興味度 | サブレッド | 要約 |
|---------|--------|-----------|--------|-----------|------|
| [タイトル](RedditURL) | XXX ups | XXX | ★★★/★★/★ | r/xxx | 参照時までの各ユーザのやり取りを200文字以内の要約 |

### カテゴリ別エントリー

#### AI系
1. [タイトル](RedditURL) (XXX ups, XXX comments) - r/xxx - 概要

#### コア技術系
1. [タイトル](RedditURL) (XXX ups, XXX comments) - r/xxx - 概要

#### 個人開発系
1. [タイトル](RedditURL) (XXX ups, XXX comments) - r/xxx - 概要

### 4. Git自動コミット＆プッシュ

ファイル保存後、以下を実行:
- git add ideas/daily/
- git commit -m "daily: YYYYMMDD trend collected"
- git push origin main

## 注意事項
- すべての記事にURLリンクを必ず含める
- はてブは元記事URLを取得（はてブページURLではなく）
- HNはコメントページURL（item?id=形式）を使用
- HN/Redditのタイトルは日本語に翻訳
- YYYYMMDDは実行日の日付を使用
- 要約の文字制限は目安であり、絶対に守らなくて良い
