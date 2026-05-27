---
name: gemini-code-review
description: Gemini CLI の Code Review 拡張で、作業後レビューを安全に実行するための最小手順と再発防止ルールを案内します。
---

# Gemini CLI によるコードレビュー

作業完了後に、**Gemini CLI** と [Code Review 拡張](https://github.com/gemini-cli-extensions/code-review)（`/code-review`, `/pr-code-review`）でレビューしたいときに使います。

## エージェントの役割と限界

- 対話型の Gemini CLI は基本的にユーザー環境で動作します。エージェントは手順案内と結果整理を担当します。
- レビュー結果を本プロジェクトで要約・共有する際は `.gemini/styleguide.md`（日本語・ですます調・簡潔な根拠）に従います。

## 前提

- セットアップは `README.md` の「Gemini CLI と Code Review 拡張」に従って完了済みであること。
- 実行ディレクトリはリポジトリルートを推奨。

## ブランチの変更: `/code-review`

1. 対象ブランチと `git status` を確認する。
2. Gemini CLI を起動し、必要なら「`.gemini/styleguide.md` に従って日本語で」と先に伝える。
3. `/code-review` を実行する。

## プルリクエスト: `/pr-code-review`

1. Gemini CLI 側で GitHub MCP を有効化する。
2. `/pr-code-review <PR_URL>` を実行する（または拡張ドキュメント準拠の環境変数方式）。
3. 認証やトークンスコープはローカル設定依存であることを前提にする。

## 再発防止ルール（最重要）

1. `gemini -p` でバッククォートを使わない  
   - NG: ``gemini -p "`.gemini/styleguide.md` に従って..."``  
   - シェル展開を避けるため、シングルクォートで囲むか、バッククォートを使わないようにします。
2. PR レビューはまず `--approval-mode yolo` を試す  
   - 拡張内部のツール実行が止まりにくい。
3. Private PR で `.diff` が 404 の場合はローカル取得へ切り替える  
   - 例: `git fetch origin pull/<n>/head:<tmp-branch>`
4. 失敗シグナルが出たら即フォールバックする  
   - 例: `Unauthorized tool call`, `Tool not found`, PR本文取得で停止。  
   - 対応: プロセス停止 -> `--approval-mode yolo` で再実行 -> だめなら対話モード `/pr-code-review`。
5. 実行後は結果を最低限まとめて返す  
   - `Findings`（重大度順）/ `Open questions` / 提案アクション（採用 or 見送り）。

## 利用のきっかけ

作業完了後に Gemini CLI でレビューしたいと言われたときに使います。
