---
name: kuroco-api-content
metadata:
  author: Diverta inc.
  version: "1.1.0"
  lastUpdated: "2026-02-20"
description: Kuroco API設計・実装およびコンテンツ管理（CRUD操作）のベストプラクティス。使用キーワード：「Kuroco API」「エンドポイント設定」「API設計」「認証」「CORS」「APIセキュリティ」「ログインAPI」「トークン認証」「Cookie認証」「JWT」「StaticToken」「X-RCMS-API-ACCESS-TOKEN」「rcms-api」「g.kuroco.app」「流量制限」「レート制限」「キャッシュ」「credentials include」「fetch」「axios」「HTTPリクエスト」「401エラー」「403エラー」「429エラー」「認証エラー」「権限エラー」「APIレスポンス」「pageInfo」「ページネーション」「アクセストークン」「リフレッシュトークン」「grant_token」「コンテンツ定義」「記事管理」「Topics」「TopicsGroup」「カテゴリ」「WYSIWYG」「ファイルアップロード」「CSVインポート」「コンテンツAPI」「拡張項目」「ext_col」「topics_id」「subject」「contents」「ymd」「topics_flg」「フィルター」「filter」「order_by」「一覧取得」「詳細取得」「list」「details」「insert」「update」「delete」「bulk_upsert」「一括更新」「タグ」「tag」「予約投稿」「open_ymd」「close_ymd」「公開設定」「閲覧制限」「関連コンテンツ」「pageID」「cnt」。APIの設計、呼び出し、認証、エラー処理、コンテンツの作成・取得・更新・削除・フィルタリングに関する質問で使用。
---

# Kuroco API連携 & コンテンツ管理

Kuroco HeadlessCMSのAPI設計・実装およびコンテンツ管理に関するベストプラクティス。

**ドキュメント参照**: `/kuroco-docs` スキルを使用してKuroco公式ドキュメントを検索・参照できます。

## 目次

### Part 1: API連携パターン

- [エンドポイント設計](#エンドポイント設計)
- [セキュリティ設定](#セキュリティ設定)
- [キャッシュ戦略](#キャッシュ戦略)
- [流量制限](#流量制限)
- [API呼び出しパターン](#api呼び出しパターン)
- [エラーハンドリング](#エラーハンドリング)

### Part 2: コンテンツ管理パターン

- [コンテンツ構造](#コンテンツ構造)
- [拡張項目（カスタムフィールド）](#拡張項目カスタムフィールド)
- [Topics API オペレーション](#topics-api-オペレーション)
- [コンテンツCRUD操作](#コンテンツcrud操作)
- [フィルタークエリ](#フィルタークエリ) → 詳細は [references/filter-query.md](references/filter-query.md)
- [ファイル・CSV操作](#ファイルcsv操作) → 詳細は [references/file-operations.md](references/file-operations.md)
- [管理API（admin_api）によるコンテンツ操作](#管理apiadmin_apiによるコンテンツ操作)

---

# Part 1: API連携パターン

## エンドポイント設計

### 基本構造

KurocoのAPIパスは以下の形式：
```
https://{サイトキー}.g.kuroco.app/rcms-api/{api_id}/{endpoint_path}
```

例：
```
https://example.g.kuroco.app/rcms-api/1/news
https://example.g.kuroco.app/rcms-api/1/member/login
```

### エンドポイント設定の主要項目

| 項目 | 説明 | 例 |
|------|------|-----|
| パス | エンドポイントのURL | `news`, `member/list` |
| モデル | 操作対象 | Topics, Member, InquiryForm |
| オペレーション | 操作種別 | list, details, insert, update, delete |
| キャッシュ | レスポンスキャッシュ期間 | 86400（1日） |
| 流量制限 | リクエスト数制限 | 100回/分 |
| 認証必須 | ログイン必須かどうか | true/false |

### 主要カテゴリとモデル

**認証（Authentication）**
| オペレーション | 説明 | メソッド |
|--------------|------|---------|
| `login_challenge` | ログイン | POST |
| `token` | アクセストークン取得 | POST |
| `logout` | ログアウト | POST |
| `profile` | ログインユーザー情報取得 | GET |
| `reminder` | パスワードリマインダー | POST |

**コンテンツ（Topics）**
| オペレーション | 説明 | メソッド |
|--------------|------|---------|
| `list` | 一覧取得 | GET |
| `details` | 詳細取得 | GET |
| `insert` | 新規追加 | POST |
| `update` | 更新 | POST |
| `delete` | 削除 | POST |
| `bulk_upsert` | 一括更新 | POST |

**メンバー（Member）**
| オペレーション | 説明 | メソッド |
|--------------|------|---------|
| `list` | メンバー一覧 | GET |
| `details` | メンバー詳細 | GET |
| `insert` | メンバー登録 | POST |
| `update` | メンバー更新 | POST |

**フォーム（InquiryMessage/InquiryForm）**
| オペレーション | 説明 | メソッド |
|--------------|------|---------|
| `send` | フォーム送信 | POST |
| `list` | 回答一覧 | GET |
| `details` | 回答詳細 | GET |

## セキュリティ設定

> **詳細リファレンス**: セキュリティ設定の詳細は [references/security-settings.md](references/security-settings.md) を参照してください。
>
> **公式ドキュメント**: 詳細な公式情報は `../kuroco-docs/docs/management/api-security.md` 等を参照してください。

### 認証方式

管理画面: [API] → [セキュリティ] で4種類から選択。

| 認証方式 | 用途 | ヘッダー |
|---------|------|---------|
| なし | 開発・テスト用（本番非推奨） | 不要 |
| 静的アクセストークン | サーバー間通信、公開API | `X-RCMS-API-ACCESS-TOKEN: {固定トークン}` |
| 動的アクセストークン | ログイン必須サイト（JWT） | `X-RCMS-API-ACCESS-TOKEN: {動的トークン}` |
| Cookie | ログイン必須Webサイト | `credentials: 'include'`（フロントエンド側） |

#### 1. Cookie認証（Webアプリ推奨）

セッションベースの認証。`credentials: 'include'` が必須。

```javascript
// ログイン
const response = await fetch('https://example.g.kuroco.app/rcms-api/1/login', {
  method: 'POST',
  credentials: 'include',  // 必須
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})

// レスポンス例
// {
//   "grant_token": "xxxxx",
//   "status": 0,
//   "member_id": 123
// }
```

**注意点**:
- サードパーティCookie問題（Safari等でブロックされる）
- APIドメインとフロントエンドを**同一ドメイン（サブドメイン違い）**に設定が必要（ファーストパーティCookie化）
  - 例: `api.example.com` と `www.example.com`
- Cookie認証APIが複数ある場合、各API間で認証状態が**共有される**

#### 2. トークン認証（モバイルアプリ推奨）

JWTベースの認証。ヘッダーにトークンを付与。

```javascript
// トークン取得
const tokenResponse = await fetch('https://example.g.kuroco.app/rcms-api/1/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})

const { access_token, refresh_token } = await tokenResponse.json()

// レスポンス例
// {
//   "access_token": {
//     "value": "eyJhbGciOiJS...",
//     "expiresAt": "2024-01-01T12:00:00+09:00"
//   },
//   "refresh_token": {
//     "value": "xxxxxx",
//     "expiresAt": "2024-01-08T12:00:00+09:00"
//   }
// }

// API呼び出し時
const response = await fetch('https://example.g.kuroco.app/rcms-api/1/news', {
  headers: {
    'X-RCMS-API-ACCESS-TOKEN': access_token.value
  }
})
```

**前提条件**: ユーザー1人以上、`login_challenge` + `token` エンドポイント必須。トークン認証APIが複数ある場合、各API間で認証状態は**共有されない**。

#### 3. StaticToken認証（サーバー間通信）

固定トークンによるAPIアクセス制限。

```javascript
const response = await fetch('https://example.g.kuroco.app/rcms-api/1/internal-api', {
  headers: {
    'X-RCMS-API-ACCESS-TOKEN': 'your-static-token-here'
  }
})
```

**設定場所**: 管理画面 → API → セキュリティ → StaticToken

**注意**: 静的トークンはフロントエンドに組み込まれるとユーザーに見える。流出時のトークン更新を想定した運用が必要。

### IPアドレス制限

管理画面: [API] → [セキュリティ] → [IPアドレス制限]

指定されたIPアドレスからのアクセスのみ許可します。

| 指定形式 | 例 | 説明 |
|---------|-----|------|
| 個別IP | `192.0.2.1` | 単一IPアドレス |
| CIDR | `192.0.2.0/24` | サブネット単位 |
| 範囲指定 | `192.0.2.1-192.0.2.2` | ハイフンによるIP範囲 |

**IPアドレスグループ**: 定数機能で `IPSETS_*` を定義し、`[[IPSETS_*]]` で参照可能（`../kuroco-docs/docs/faq/is-it-possible-to-set-multiple-ip-addresses-at-once.mdx` 参照）。

### CORS設定

管理画面: [API] → [セキュリティ] → [CORS]

| 項目 | 対応ヘッダー | 説明 |
|------|------------|------|
| CORS_ALLOW_ORIGINS | Access-Control-Allow-Origin | 許可オリジン（**ワイルドカード`*`は非推奨**） |
| CORS_ALLOW_METHODS | Access-Control-Allow-Methods | 許可HTTPメソッド |
| CORS_ALLOW_HEADERS | Access-Control-Allow-Headers | 許可リクエストヘッダー |
| CORS_MAX_AGE | Access-Control-Max-Age | プリフライトキャッシュ秒数 |
| CORS_ALLOW_CREDENTIALS | Access-Control-Allow-Credentials | Cookie送信の許可 |

**CSRF対策**: CORS + `Content-Type: application/json` でモダンブラウザでのCSRF攻撃を防御。ワイルドカードを使うと防御効果がなくなるため、必ず特定ドメインを指定すること。

**変更反映の遅延**: CORS設定変更後は `CORS_MAX_AGE` 分だけブラウザにキャッシュされる。即時反映にはブラウザキャッシュクリアまたは `CORS_MAX_AGE` を `0` に設定。

### APIリクエスト制限

| 制限タイプ | 説明 |
|----------|------|
| None | 制限なし |
| GroupAuth | ログインユーザーの**グループ権限**をチェックし、合致した場合のみ許可 |
| MemberCustomSearchAuth | ログインユーザーが**カスタムメンバーフィルター**の条件に合致する場合のみ許可 |

### 閲覧制限の優先順序

コンテンツ返却時の制限は以下の順序で評価されます（上位優先）:

1. **API → IPアドレス制限**（API全体）
2. **エンドポイント → APIリクエスト制限**（エンドポイント単位）
3. **コンテンツ定義 → APIリクエスト制限**
4. **コンテンツカテゴリ → APIリクエスト制限**
5. **個別コンテンツ → APIリクエスト制限**

### 後処理によるレスポンス制限

管理画面: [API] → エンドポイント → [後処理]

APIレスポンスから不要なフィールドを除外し、公開情報を制御:

| 処理タイプ | 説明 |
|----------|------|
| 出力許可リスト | 指定フィールドのみ返す（ホワイトリスト）。例: `list.subject`, `pageInfo` |
| 出力変換リスト | フィールドの削除・名称変更・変換関数の適用 |
| カスタム処理 | Smartyテンプレートでの独自ロジック |

**パフォーマンスTip**: 出力許可リストは他の処理の前に配置するとSQLレベルで効果あり。

### プラットフォームセキュリティ

Kurocoプラットフォームが提供するインフラレベルのセキュリティ:

- **通信**: HTTPS完全暗号化、TLS証明書自動管理
- **防御**: WAF、CDN、DDoS対策（オプションでFastly DDoS Protection）
- **認証連携**: SAML/OAuth外部ログイン、クライアント証明書（オプション）
- **監査**: アクセスログ、アプリケーションログ
- **認定**: ISMS (ISO 27001)、ISMSクラウド (ISO 27017)、プライバシーマーク
- **診断**: 毎日のコンテナ脆弱性スキャン、VADDY連携自動診断

### 管理API（admin_api）による設定変更

APIのセキュリティ設定は管理画面だけでなく、**管理API経由**でも操作可能です。`/kuroco-admin-api` スキルを使用してCLI経由で管理APIを実行できます。

## キャッシュ戦略

### 推奨設定

| ユースケース | キャッシュ期間 | 設定値 |
|------------|--------------|-------|
| 静的コンテンツ（ニュース等） | 1日 | 86400 |
| 更新頻度低いコンテンツ | 1週間 | 604800 |
| リアルタイム性が必要 | キャッシュなし | 0 |
| 認証が必要なAPI | キャッシュなし | 0 |

**重要**: コンテンツ・メンバー等のデータ更新時、キャッシュは自動クリアされます。

### キャッシュヘッダー

レスポンスヘッダーで確認可能：
```
Cache-Control: max-age=86400
```

## 流量制限

### レスポンスヘッダー

```
x-rcms-ratelimit-limit: 100      # 制限数
x-rcms-ratelimit-remaining: 95   # 残りリクエスト数
x-rcms-ratelimit-reset: 60       # リセットまでの秒数
```

### 429エラー時の対応

```javascript
const response = await fetch(url)

if (response.status === 429) {
  const resetTime = response.headers.get('x-rcms-ratelimit-reset')
  throw new Error(`流量制限超過。${resetTime}秒後に再試行してください`)
}
```

## API呼び出しパターン

### 一覧取得（ページネーション付き）

```javascript
async function fetchNewsList(page = 1, perPage = 10) {
  const params = new URLSearchParams({
    pageID: page,
    cnt: perPage
  })

  const response = await fetch(
    `https://example.g.kuroco.app/rcms-api/1/news?${params}`,
    { credentials: 'include' }
  )

  const data = await response.json()

  // レスポンス構造
  // {
  //   "list": [...],
  //   "pageInfo": {
  //     "totalCnt": 100,
  //     "perPage": 10,
  //     "totalPageCnt": 10,
  //     "pageNo": 1
  //   }
  // }

  return data
}
```

### フィルター検索

```javascript
// filter パラメータで検索
const params = new URLSearchParams({
  filter: 'subject contains "重要"',
  order_by: 'ymd desc'
})

const response = await fetch(
  `https://example.g.kuroco.app/rcms-api/1/news?${params}`,
  { credentials: 'include' }
)
```

### 詳細取得

```javascript
async function fetchNewsDetail(topicsId) {
  const response = await fetch(
    `https://example.g.kuroco.app/rcms-api/1/newsdetail/${topicsId}`,
    { credentials: 'include' }
  )

  const data = await response.json()

  // レスポンス構造
  // {
  //   "details": {
  //     "topics_id": 1,
  //     "subject": "タイトル",
  //     "contents": "<p>本文</p>",
  //     ...
  //   }
  // }

  return data.details
}
```

### コンテンツ作成

```javascript
async function createNews(newsData) {
  const response = await fetch(
    'https://example.g.kuroco.app/rcms-api/1/news/insert',
    {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        subject: newsData.title,
        contents: newsData.body,
        ymd: newsData.date,
        topics_flg: 1  // 1: 公開, 0: 非公開
      })
    }
  )

  return response.json()
}
```

## エラーハンドリング

### 主要エラーコード

| コード | 説明 | 対応 |
|--------|------|------|
| 400 | リクエストエラー | リクエストパラメータを確認 |
| 401 | 認証エラー | ログイン状態・トークンを確認 |
| 403 | 権限エラー | APIの権限設定を確認 |
| 404 | リソース未存在 | パス・IDを確認 |
| 429 | 流量制限超過 | リトライまで待機 |
| 500 | サーバーエラー | Kurocoサポートに連絡 |

### エラーレスポンス例

```json
{
  "errors": [
    {
      "code": "authentication_error",
      "message": "ログインが必要です"
    }
  ]
}
```

### エラーハンドリング実装

```javascript
async function apiRequest(url, options = {}) {
  const response = await fetch(url, {
    credentials: 'include',
    ...options
  })

  if (!response.ok) {
    const errorData = await response.json()

    switch (response.status) {
      case 401:
        throw new Error('認証が必要です')
      case 403:
        throw new Error('アクセス権限がありません')
      case 429:
        throw new Error('リクエスト制限を超えました')
      default:
        throw new Error(errorData.errors?.[0]?.message || 'APIエラー')
    }
  }

  return response.json()
}
```

---

# Part 2: コンテンツ管理パターン

## コンテンツ構造

### 階層構造

```
コンテンツ定義（TopicsGroup）
├── カテゴリ（TopicsCategory）
│   └── コンテンツ（Topics）
└── 拡張項目（ext_col_01〜ext_col_XX）
```

### コンテンツ定義の設定

管理画面: [コンテンツ定義] → [新規作成]

| 項目 | 説明 |
|------|------|
| グループ名 | コンテンツ定義の名前 |
| 識別子 | ユニークなID（英数字） |
| 本文の入力方法 | WYSIWYG、マークダウン、HTML |
| 閲覧制限 | 全員/グループ制限/カスタム検索 |
| 編集制限 | 全員/グループ制限/カスタム検索 |
| 拡張項目 | カスタムフィールド（最大99個） |

## 拡張項目（カスタムフィールド）

| タイプ | 説明 | APIレスポンス例 |
|--------|------|----------------|
| テキスト | 1行テキスト | `"ext_col_01": "値"` |
| テキストエリア | 複数行テキスト | `"ext_col_02": "複数行\nテキスト"` |
| WYSIWYG | リッチテキスト | `"ext_col_03": "<p>HTML</p>"` |
| 数値 | 整数・小数 | `"ext_col_04": 100` |
| 日付 | 日付選択 | `"ext_col_05": "2024-01-01"` |
| 選択（単一） | ラジオボタン | `"ext_col_06": "選択肢1"` |
| 選択（複数） | チェックボックス | `"ext_col_07": ["選択肢1", "選択肢2"]` |
| ファイル/画像 | アップロード | `"ext_col_08": { "id": "xxx", "url": "https://...", "desc": "" }` |
| リンク | URLリンク | `"ext_col_10": { "url": "https://...", "title": "リンク名" }` |
| 関連コンテンツ | 他コンテンツ参照 | `"ext_col_11": { "topics_id": 123, "subject": "タイトル" }` |

## Topics API オペレーション

| オペレーション | 説明 | メソッド | パス例 |
|--------------|------|---------|-------|
| list | 一覧取得 | GET | `/news` |
| details | 詳細取得 | GET | `/newsdetail/{topics_id}` |
| insert | 新規追加 | POST | `/news/insert` |
| update | 更新 | POST | `/news/update/{topics_id}` |
| delete | 削除 | POST | `/news/delete/{topics_id}` |
| bulk_upsert | 一括更新 | POST | `/news/bulk` |

## コンテンツCRUD操作

### 一覧取得レスポンス

```json
{
  "list": [
    {
      "topics_id": 1,
      "subject": "タイトル",
      "contents": "本文（HTML）",
      "ymd": "2024-01-01",
      "topics_flg": 1,
      "category_id": 1,
      "ext_col_01": "拡張項目値",
      "tag": ["タグ1", "タグ2"]
    }
  ],
  "pageInfo": {
    "totalCnt": 100,
    "perPage": 10,
    "totalPageCnt": 10,
    "pageNo": 1
  }
}
```

### コンテンツ作成

```javascript
const response = await fetch('/rcms-api/1/news/insert', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    subject: 'タイトル',
    contents: '<p>本文</p>',
    ymd: '2024-01-01',
    topics_flg: 1,           // 1: 公開, 0: 非公開
    category_id: 1,
    open_ymd: '2024-12-01',  // 予約公開開始日
    close_ymd: '2024-12-31', // 公開終了日
    tag: ['タグ1', 'タグ2'],
    ext_col_01: 'カスタム値'
  })
})
```

### コンテンツ更新

```javascript
const response = await fetch(`/rcms-api/1/news/update/${topicsId}`, {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    subject: '更新タイトル',
    contents: '更新本文'
    // 更新したいフィールドのみ送信可能
  })
})
```

### コンテンツ削除

```javascript
await fetch(`/rcms-api/1/news/delete/${topicsId}`, {
  method: 'POST',
  credentials: 'include'
})
```

## フィルタークエリ

基本構文: `filter={field} {operator} {value}`

| 演算子 | 例 |
|--------|-----|
| `=`, `!=` | `filter=category_id = 1` |
| `>`, `>=`, `<`, `<=` | `filter=ymd >= '2024-01-01'` |
| `contains` | `filter=subject contains 'キーワード'` |
| `in`, `not_in` | `filter=category_id in [1, 2, 3]` |

複合条件: `filter=(category_id = 1 or category_id = 2) and topics_flg = 1`

ソート: `order_by=ymd desc`

**詳細な使い方**: [references/filter-query.md](references/filter-query.md) を参照

## ファイル・CSV操作

### ファイルアップロード

```javascript
// 1. ファイルアップロード
const formData = new FormData()
formData.append('file', file)
const result = await fetch('/rcms-api/1/files/upload', {
  method: 'POST',
  credentials: 'include',
  body: formData
})
const { file_id } = await result.json()

// 2. コンテンツに紐付け
await fetch('/rcms-api/1/news/insert', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    subject: 'タイトル',
    ext_col_02: { file_id, desc: '説明' }
  })
})
```

**詳細（一括更新、カテゴリ、タグ、閲覧制限）**: [references/file-operations.md](references/file-operations.md) を参照

## 管理API（admin_api）によるコンテンツ操作

`/kuroco-admin-api` スキルを使うと、管理画面と同等のコンテンツ操作をCLI経由で実行できます。フロントエンドAPI（rcms-api）との違いに注意してください。

### フロントエンドAPI vs 管理API

| 項目 | フロントエンドAPI（rcms-api） | 管理API（admin_api） |
|------|---------------------------|-------------------|
| 対象 | エンドユーザー | 管理者・運用者 |
| 認証 | StaticToken / DynamicToken / Cookie | 管理画面セッションCookie |
| エンドポイント | `/rcms-api/{api_id}/{path}` | `/direct/rcms_api/admin_api/` |
| 利用場面 | フロントエンド実装 | データ一括操作、構造確認、設定変更 |

### コンテンツ定義一覧の取得

```bash
# admin_api: コンテンツ定義（TopicsGroup）一覧（columnsで必要カラムのみ取得）
kuroco-admin exec topics/topics_group_list --columns topics_group_id,group_nm --json
```

### コンテンツ一覧の取得

```bash
# admin_api: 特定コンテンツ定義のコンテンツ一覧（columnsで必要カラムのみ取得）
kuroco-admin exec topics/topics_list --param "topics_group_id[]=1" --param cnt=10 --columns topics_id,subject,ymd --json
```

### コンテンツの作成

```bash
# admin_api: コンテンツ作成（※実行前にユーザー確認必須）
kuroco-admin exec topics/topics_edit --MODE INSERT --data '{"subject":"タイトル","contents":"本文","topics_group_id":1,"topics_flg":1}' --json
```

### 活用シーン

- **サイト構造の把握**: コンテンツ定義一覧・拡張項目の確認
- **データの一括確認・修正**: 管理画面GUIを経由せず効率的にデータ操作
- **スキーマ確認**: `kuroco-admin help topics/topics_edit --json` でフィールド定義を取得

> **注意**: insert/update/deleteは必ずユーザーに確認してから実行すること。詳細は `/kuroco-admin-api` スキル参照。

## ベストプラクティス

- **キャッシュ活用**: エンドポイント設定で `キャッシュ: 86400`（1日）を設定。更新時は自動クリア
- **ページネーション**: `pageID` と `cnt` パラメータで分割取得

---

## 関連スキル

- `/kuroco-frontend-integration` - Nuxt.js/Next.jsでのAPI呼び出しパターン、AI自動デプロイ
- `/kuroco-server-processing` - Smartyプラグイン・構文リファレンス、Webhook・バッチ処理
- `/kuroco-admin-api` - 管理API（admin_api）の操作

## 関連ドキュメント

### スキル内リファレンス
- [references/security-settings.md](references/security-settings.md) - セキュリティ設定の詳細リファレンス
- [references/filter-query.md](references/filter-query.md) - フィルタークエリ詳細
- [references/file-operations.md](references/file-operations.md) - ファイル・CSV操作詳細

### Kuroco公式ドキュメント
- `../kuroco-docs/docs/management/api-security.md` - APIセキュリティ設定（認証方式、IP制限）
- `../kuroco-docs/docs/management/api-list.md` - API一覧・CORS設定
- `../kuroco-docs/docs/management/api-postprocessing.md` - API後処理の設定
- `../kuroco-docs/docs/reference/endpoint-settings.md` - エンドポイント設定項目一覧
- `../kuroco-docs/docs/reference/post-processing.md` - 後処理の詳細リファレンス
- `../kuroco-docs/docs/tutorials/configure-endpoint.md` - エンドポイント設定方法
- `../kuroco-docs/docs/tutorials/login.md` - ログイン実装
- `../kuroco-docs/docs/tutorials/restricting-api-access-with-statictoken.md` - StaticToken認証
- `../kuroco-docs/docs/reference/api-cache.md` - APIキャッシュ
- `../kuroco-docs/docs/reference/filter-query.md` - フィルタークエリ
- `../kuroco-docs/docs/about/security.md` - プラットフォームセキュリティ概要
- `../kuroco-docs/docs/faq/in-what-order-are-viewing-restrictions-applied.mdx` - 閲覧制限の優先順序
- `../kuroco-docs/docs/faq/cors-and-content-type-prevent-csrf-attacks.mdx` - CSRF対策
- `../kuroco-docs/docs/faq/the-api-returns-403-forbidden-even-though-no-restrictions-are-applied.mdx` - 403エラーの解決
- `../kuroco-docs/docs/tutorials/adding-a-topics.md` - コンテンツ定義作成
- `../kuroco-docs/docs/tutorials/bulk-upload-in-csv.md` - CSVアップロード
- `../kuroco-docs/docs/management/content-structure-topics.md` - コンテンツ構造
