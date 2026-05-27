---
name: search-console
description: >
  Query Google Search Console Search Analytics via the webmasters API. Use when the
  user asks about search queries, clicks, impressions, CTR, ranking positions, top
  pages, or month-over-month traffic on their site. Handles OAuth scope + quota
  project automatically, supports multiple sites via config, and can join page URLs
  with WordPress post titles for readability.
compatibility: claude-code-only
---

# Search Console

Google Search Console Search Analytics を手早く引くためのラッパー群。`gcloud auth application-default` の ADC を利用し、クォータプロジェクトとサイトURLの指定を自動化する。

## 前提

- `gcloud` CLI インストール済み、`gcloud auth application-default login` で webmasters.readonly スコープを承認済み
  - 未承認なら: `gcloud auth application-default login --scopes="https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform"`
- `jq` と `python3` が PATH にある
- gcloud が PATH にない場合は `GCLOUD_BIN` 環境変数で実体パスを指定(例: `~/google-cloud-sdk/bin/gcloud`)

## 設定

優先順位: **環境変数 > `~/.claude/skills/search-console/config.json` > gcloud デフォルト**

### 設定ファイル形式

`~/.claude/skills/search-console/config.json`:
```json
{
  "default_site": "welovefactorio",
  "sites": {
    "mysite": {
      "url": "https://example.com",
      "quota_project": "your-gcp-project-id",
      "wp_ssh": "user@host",
      "wp_path": "/var/www/example.com/public_html",
      "wp_bin_path": "/home/user/bin"
    }
  }
}
```

サイトごとのフィールド:
- `url` — Search Console 登録のサイトURL(必須、末尾スラッシュ等まで完全一致)
- `quota_project` — Google Cloud プロジェクトID(必須)
- `wp_ssh` — WP-CLI 用 SSH ホスト(任意。`sc-join-titles.sh` を使うなら必要)
- `wp_path` — リモート上の WordPress インストールパス(任意。`sc-join-titles.sh` で必要)
- `wp_bin_path` — リモート上の `wp` コマンドが置かれているディレクトリ(任意。リモートPATHに `wp` が無い場合に指定)

### 環境変数による上書き

- `SC_SITE_URL` — サイトURL
- `SC_QUOTA_PROJECT` — クォータプロジェクトID
- `SC_WP_SSH` — WP-CLI 用 SSH ホスト
- `SC_WP_PATH` — リモート WordPress インストールパス
- `SC_WP_BIN_PATH` — リモート上の `wp` コマンドのディレクトリ
- `SC_SITE` — 設定ファイル内のサイトキー
- `GCLOUD_BIN` — gcloud バイナリのパス

## コマンド

スクリプトは `scripts/` 配下。直接実行する。

### sc-query

検索クエリ/ページ別集計を取得。

```bash
~/.claude/skills/search-console/scripts/sc-query.sh [options]
```

オプション:
- `--dim DIM` — 次元: `query` | `page` | `country` | `device` | `date`(既定: `query`)
- `--start DATE` — 開始日 YYYY-MM-DD(既定: 33日前)
- `--end DATE` — 終了日 YYYY-MM-DD(既定: 3日前。GSC のデータ反映に約 2-3 日かかるため)
- `--limit N` — 行数上限(既定: 25)
- `--site KEY` — 設定ファイル内のサイトキー
- `--format table|json|csv` — 出力形式(既定: `table`)
- `--raw` — API生レスポンスをそのまま出力

例:
```bash
# 直近30日のクエリ上位
sc-query.sh

# ページ別、直近60日、CSV
sc-query.sh --dim page --start 2026-02-20 --end 2026-04-20 --format csv

# JSON(他スクリプトへのパイプ用)
sc-query.sh --dim page --format json --limit 50
```

### sc-compare

前月比(=期間Aと期間Bの比較)。

```bash
~/.claude/skills/search-console/scripts/sc-compare.sh [options]
```

オプション:
- `--dim DIM` — `query` | `page` | `total`(既定: `total`)
- `--current-start / --current-end` — 現期間(既定: 33日前〜3日前)
- `--previous-start / --previous-end` — 比較期間(既定: 現期間の直前同じ日数)
- `--limit N` — 表示行数(既定: 15)
- `--site KEY`

例:
```bash
# サイト全体の前月比
sc-compare.sh

# ページ別 前月比 Top 20
sc-compare.sh --dim page --limit 20
```

### sc-join-titles

ページ URL の一覧を stdin で受け取り、WP 投稿タイトルを joined したテーブルを出力する。`wp_ssh` が設定されている必要あり。

```bash
sc-query.sh --dim page --format json | sc-join-titles.sh
```

URL から投稿IDを抽出し(`/archives/<ID>` or `/archives/<cpt>/<ID>`)、`wp post get <ID> --field=title` でタイトルを取得する。

## ワークフロー

ユーザーが Search Console について聞いてきたときの流れ:

1. **初回**: 設定ファイルの存在を確認。なければ `config.json` を作成する提案をする
2. **認証確認**: `gcloud auth application-default print-access-token` で成功するか確認
3. **スコープ/クォータ不足エラー**が出たら、必要な手順を案内
   - スコープ不足 → `gcloud auth application-default login --scopes=...` を提示
   - クォータプロジェクト欠落 → 設定ファイルか env で指定するよう案内
4. **意図に応じてコマンド選択**:
   - 「どんなクエリで来てる?」→ `sc-query.sh --dim query`
   - 「どのページが見られてる?」→ `sc-query.sh --dim page` + `sc-join-titles.sh`
   - 「前月比は?」→ `sc-compare.sh`
5. **結果をテーブル形式で要約**し、所感(伸びている/落ちている/改善余地)を一言添える

## トラブルシューティング

### `Insufficient Permission` / `ACCESS_TOKEN_SCOPE_INSUFFICIENT`
ADC が webmasters.readonly スコープで承認されていない。`gcloud auth application-default login --scopes="https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform"` を実行。

### `requires a quota project, which is not set by default`
クォータプロジェクトが未設定。以下のいずれかで解決:
- `gcloud auth application-default set-quota-project <PROJECT_ID>`(永続)
- `SC_QUOTA_PROJECT` 環境変数で指定
- `config.json` の `quota_project` に書く

### `SERVICE_DISABLED`
そのプロジェクトで Search Console API が無効。`gcloud services enable searchcoreconsole.googleapis.com --project=<PROJECT_ID>`(※ 正確な API 名は `searchconsole.googleapis.com`)

### データが0件
- サイトURLが正確に Search Console 登録値と一致しているか(末尾スラッシュ、http/https、www有無)
- 期間が GSC のデータ反映ラグ(約2-3日)より新しすぎないか

## 配布

このスキルはプラグイン形式にパッケージ化して個人リポジトリで公開可能。`~/.claude/skills/search-console/` ディレクトリ丸ごとを、プラグインリポジトリの `skills/search-console/` に配置すればよい。
