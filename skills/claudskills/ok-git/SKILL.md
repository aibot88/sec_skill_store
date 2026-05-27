---
name: ok-git
description: git config global を前提に、日常的な Git 操作（状況確認・ブランチ作成・安全コミット・同期）を bundled script で実行する。ユーザーが「コミットして」「ブランチ切って」「pushして」「差分見て」などを依頼したときに使う。作業リポジトリ直下の scripts/ は前提にせず、agent skills ディレクトリ内の ok-git/scripts/git_ops.sh を解決して使う。git config は変更せず既存設定を利用する。
compatibility: codex,copilot
---

# OK Git

## 目的

Git 日常作業を安全に高速化する。  
この skill は `git config` を変更せず、既存の global 設定を使って操作する。

## トリガー例

- 「この変更をコミットして push して」
- 「作業ブランチ切って進めて」
- 「今の状態と差分を見て」
- 「rebase pull して同期して」

## 絶対ルール

- `git config --global` / `--local` / `--system` を変更しない。
- `git commit --author` を使わない。
- コミットメッセージに `Co-Authored-By` を入れない。
- 破壊的操作（`reset --hard`、履歴改変 push など）はユーザー明示指示がない限り行わない。
- ブランチ名はリポジトリごとの既存慣習を優先する。`codex/` などの prefix を勝手に固定しない。

## Agent Execution Contract

- この skill の `scripts/git_ops.sh` は、作業リポジトリ直下ではなく skill bundle 内にある。
- `scripts/git_ops.sh` を現在の project から相対参照してはいけない。
- まず agent 側の skills ディレクトリから `ok-git/scripts/git_ops.sh` を解決し、その絶対パスを使って実行する。
- 候補パスは次の順に確認する:
  - `~/.codex/skills/ok-git/scripts/git_ops.sh`
  - `~/.copilot/skills/ok-git/scripts/git_ops.sh`
- helper script が見つからない場合は「skill 配置が壊れている」と報告して停止する。勝手に生の `git` / `gh` コマンド列へ置き換えない。
- helper script の実行時だけ script の絶対パスを使い、Git 操作の対象リポジトリは常にユーザーの現在の作業ディレクトリとする。

helper script の解決例:

```bash
for root in "$HOME/.codex/skills" "$HOME/.copilot/skills"; do
  if [ -x "$root/ok-git/scripts/git_ops.sh" ]; then
    OK_GIT_SCRIPT="$root/ok-git/scripts/git_ops.sh"
    break
  fi
done

if [ -z "${OK_GIT_SCRIPT:-}" ]; then
  echo "[ERROR] ok-git helper script was not found in agent skills directories" >&2
  exit 1
fi
```

## 標準フロー

### 1. 状態確認

```bash
"$OK_GIT_SCRIPT" inspect
```

以下を確認する:

- 現在ブランチ
- 変更状況（`git status -sb`）
- remote
- global / effective の `user.name`, `user.email`

### 2. ブランチ作成（必要時）

```bash
"$OK_GIT_SCRIPT" start-branch --name <branch-name> --base main
```

- ブランチ名を決める前に、既存のローカル/リモートブランチ名、直近のマージ済みブランチ、必要なら PR タイトルや issue 番号を見て、そのリポジトリの命名慣習に合わせる。
- 明示指示や既存慣習がない場合でも、エージェント都合の固定 prefix は付けない。
- 既存ブランチ名との衝突を検出して停止する。
- `--base` を省略すると現在ブランチから作成する。

### 3. 安全コミット

全変更をまとめてコミット:

```bash
"$OK_GIT_SCRIPT" commit --all --message "<日本語メッセージ>"
```

対象ファイルだけコミット:

```bash
"$OK_GIT_SCRIPT" commit --paths "path/a,path/b" --message "<日本語メッセージ>"
```

ルール:

- コミット時は global `user.name` / `user.email` を明示的に使用する。
- `Co-Authored-By` を含むメッセージは拒否する。

### 4. 同期（pull/push）

rebase pull:

```bash
"$OK_GIT_SCRIPT" sync
```

rebase pull + push:

```bash
"$OK_GIT_SCRIPT" sync --push
```

- `sync --push` は、既存 upstream があるブランチでは rebase pull の後に push する。
- 初回 push で upstream 未設定かつリモートブランチ未作成の場合は、helper が `git push -u` 相当へ自動フォールバックする。
- `sync` 単体は初回 push を自動で作らない。未設定ブランチで pull 先がない場合は停止する。

## 失敗時の対処

- コンフリクト時は自動解決しない。競合ファイルを提示してユーザー確認後に進める。
- global identity が未設定の場合は停止し、設定状況を報告する（設定変更は行わない）。
- helper script が見つからない場合は、skill インストール/同期不備として報告する。作業リポジトリ直下の `scripts/` を探し続けない。

## 実装補助

- 統合スクリプト: `ok-git/scripts/git_ops.sh`
