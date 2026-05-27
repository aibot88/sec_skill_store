---
name: gc-vault
description: gc-vault でラップされた GCP プロジェクトに対して gcloud / gcloud storage / bq / terraform 等のコマンドを実行する際に使用する。直接の gcloud auth login やローカル credentials に頼らず、1Password に保管された bootstrap SA キーから短命の借用トークンを発行してコマンドを実行する。
---

# gc-vault: 安全な GCP 認証ラッパー

Claude Code の Bash ツールから実行する場合は **「Claude Code から実行する手順（必読）」** に従うこと。サンドボックス解除と 1Password の認証の二段階防御で運用する。

## いつ使うか

ユーザーが以下のような操作を求めたとき、本スキルを適用する：

- `gcloud` / `gcloud storage` / `bq` の実行（`gsutil` は `gc-vault` の認証経路では動作しない、後述）
- Terraform `google` provider を使う `terraform plan` / `apply`
- GCP の Client Libraries を使うスクリプト（Ruby / Python / Go 等）の起動
- `cloud-sql-proxy` 等の補助ツール起動

## Claude Code から実行する手順（必読）

### プロファイルの確認

利用可能なプロファイル名はユーザーが `~/.config/gc-vault/config.toml` で定義している。プロファイル名を agent 側で把握していない場合は、以下の読み取りコマンドで確認する（サンドボックス内で動作する）。

```bash
gc-vault list
```

### プロファイルの選び方

ユーザーの要求文に明示的な profile 名が含まれていない限り、**agent は推測で profile を決めない**。`gc-vault list` で利用可能な一覧を取得し、ユーザーに選択を促す。ユーザーの言葉遣い（「dev」「production」等）から推測することはしない（誤って本番に対して操作するリスクを避けるため）。

選択を促す具体的な方法は profile の件数で分岐する:

- **2 件以上の場合**: `AskUserQuestion` ツールで選択肢を提示するか、平文で一覧を出して選んでもらう
- **1 件のみの場合**: `AskUserQuestion` は最低 2 選択肢を要求するため使えない。平文で「このプロファイル `<profile>` で実行してよいですか？」と確認し、肯定応答を得てから進める。読み取り系コマンド（`gcloud ... list` / `describe` 等）なら、確認文中に実行予定のコマンドも併記するとやり取りが減る

### 手順

`Bash` ツール呼び出しに **`dangerouslyDisableSandbox: true`** を指定して `gc-vault exec <profile> -- <command>` を実行する。

```
Bash ツール呼び出し:
  command: gc-vault exec <profile> -- gcloud sql instances list
  dangerouslyDisableSandbox: true
```

実行時に発生するユーザー操作:

1. **Bash 承認プロンプト**（Claude Code 側）— サンドボックス解除を伴う実行をユーザーが承認
2. **1Password の認証プロンプト**（1Password アプリ）— bootstrap SA キーへのアクセスを生体認証で承認

この 2 段階により、agent が意図しない `gc-vault exec` を呼ぼうとしても、ユーザーが少なくともどちらかで止められる。

### 1Password の認証が毎回要求される理由

通常、`op` CLI は「ターミナルセッション」単位で 1 回 1Password の認証を要求し、セッション内（10 分間 / 操作のたびに延長）は再認証なしで動作する（[公式仕様](https://developer.1password.com/docs/cli/app-integration-security/)）。しかし Claude Code の Bash ツールは各呼び出しごとに独立したプロセスを spawn するため、1Password 側からは **毎回別セッション** として扱われ、結果的にすべての `gc-vault exec` で 1Password の認証が要求される。

これは 1Password / Claude Code どちらの明示的な設定でもなく、両者のプロセスモデルの相互作用から生じる挙動。1Password 設定で実現するものではない。

将来 Claude Code がプロセスを再利用するようになる、あるいは 1Password がセッション判定ロジックを変更する等で「毎回 1Password の認証」が省略される可能性がある。Bash 承認プロンプトを通過した後に 1Password の認証プロンプトが出ない場合は、防御層が 1 段に減っているため、ユーザーに警告して挙動の変化を共有すること。

### 1Password の認証が頻繁で煩わしい場合

連続して多数の GCP 操作が必要な場面では、毎回の Bash 承認 + 1Password の認証が運用上重くなる。その場合は、ユーザーに **「別ターミナルで `gc-vault shell <profile>` を起動し、そこから `claude` を立ち上げる」** 運用（README「代替運用」を参照）への切り替えを提案する。この運用なら起動時の 1Password の認証は 1 回で済み、Claude Code 内では `gcloud` を直接実行できる（credentials がセッション中露出するトレードオフあり）。

切り替えの目安: 同じセッションで 3 件以上の `gc-vault exec` が見込まれる場合、または既に何度か実行してユーザーから「面倒」「重い」等の反応があった場合。

### コマンドを組み立てる際のルール

- `--project` フラグは付けない（`gc-vault` が `CLOUDSDK_CORE_PROJECT` を自動セットする）
- 1 回の `gc-vault exec` で複数の処理を `&&` 等で連結しない（複合コマンドにすると Bash 承認の粒度が粗くなり、ユーザーが意図を読み取りにくくなるため）
- 連続して多数のコマンドが必要な場合でも、**1 コマンド = 1 `gc-vault exec`** を保つ
- `gsutil` は使わず `gcloud storage` を使う（`gsutil` は `CLOUDSDK_AUTH_ACCESS_TOKEN` も `GOOGLE_APPLICATION_CREDENTIALS` も認証ソースとして直接読まないため、`gc-vault exec` 経由では 401 Anonymous caller になる。`gcloud storage ls` / `cp` / `rsync` 等が代替）

### NG

- サンドボックス有効のまま `gc-vault exec` を呼ぶ（`op` がデスクトップアプリに到達できず失敗する）
- `gcloud sql instances list` のように `gc-vault` を経由しない呼び出し（クレデンシャルがないため失敗、または個人アカウントを誤用する）
- `~/.claude/settings.json` の `sandbox.network.allowUnixSockets` への追加を提案する（実機検証で複数ソケット + 追加の IPC 経路の許可が必要と判明、設定がフラジャイル。`gc-vault` リポジトリの README「採用しないアプローチ」参照）

## いつ使わないか

- **kubectl (GKE)**: `gke-gcloud-auth-plugin` が独自フローのため非対応
- **firebase CLI**: 独自認証

## 提案するコマンドの作り方

ユーザーから「<profile> の Cloud SQL インスタンスを確認したい」などの要望があったら：

OK: `gc-vault exec <profile> -- gcloud sql instances list`（`dangerouslyDisableSandbox: true` 付き）

NG: `gcloud sql instances list --project=<project>`（クレデンシャルがないため失敗）

その他の例:

```bash
gc-vault exec <profile> -- gcloud projects describe "$CLOUDSDK_CORE_PROJECT"
gc-vault exec <profile> -- gcloud run services list
gc-vault exec <profile> -- gcloud storage ls gs://my-bucket/
gc-vault exec <profile> -- bq ls
gc-vault exec <profile> -- terraform plan
gc-vault exec <profile> -- bin/rails console
```

## 環境変数

`gc-vault` がセットする環境変数：

- `CLOUDSDK_AUTH_ACCESS_TOKEN`: gcloud 系 CLI 用の短命トークン
- `CLOUDSDK_CORE_PROJECT`: profile の `project` 値
- `GOOGLE_APPLICATION_CREDENTIALS`: SDK / Terraform 用の `impersonated_service_account` 形式 ADC JSON のパス
- `GCP_VAULT_ACTIVE_PROFILE`: 現在のプロファイル名（プロンプト表示等）

## 注意事項

- アクセストークンは 30 〜 60 分で失効。長時間プロセス（cloud-sql-proxy 等）は SDK 側の自動更新（ADC 経由）に依存
- 1Password デスクトップアプリが起動・unlock されている必要がある（`gc-vault` が内部で `op` CLI を呼び出すため）
- `gcloud auth login` での個人アカウント認証は **使わない方針**。既存の credentials は `gcloud auth revoke --all` + `gcloud auth application-default revoke` で削除可能
- Claude Code のサンドボックスは `op` CLI が 1Password デスクトップアプリと通信する経路（複数の Unix ソケット等）を遮断する。そのため `gc-vault exec` の呼び出しには `dangerouslyDisableSandbox: true` が必須
- 1Password の認証が毎回要求される挙動が将来変化した場合（プロンプトが省略される等）、防御層が一段減るためユーザーに伝える
- ツール本体: https://github.com/zenn-dev/gc-vault
