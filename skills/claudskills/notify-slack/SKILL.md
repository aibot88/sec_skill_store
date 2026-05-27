---
name: notify-slack
description: Slack chat.postMessage を叩く共通シェル関数。~/.config/patrol/secrets.sh の SLACK_BOT_TOKEN / SLACK_CHANNEL_ID を読んで投稿する。メンション付き通知はユーザーの U08RPS2BLUD を文字列に含める。
---

# notify-slack

プロジェクト横断で使える Slack 通知関数の canonical 版。

## 由来

`agent-playbook/scripts/patrol-config.sh` の `notify_slack` を抽出・正規化したもの。今後、agent-playbook 側もここを参照する方向に寄せる。

## 使い方（プロジェクトからの取得）

```bash
bash ~/mgmt-team/platform-standards/scripts/ps-fetch.sh \
  catalog/skills/notify-slack \
  --dest .claude/skills/notify-slack
```

取得後、シェルスクリプトから:

```bash
source .claude/skills/notify-slack/notify.sh
notify_slack "<@U08RPS2BLUD> 作業開始" "$SLACK_CHANNEL_ID"
```

## 前提

- `~/.config/patrol/secrets.sh` に `SLACK_BOT_TOKEN` を定義
- 投稿先チャンネル ID は呼び出し時の第 2 引数、または環境変数 `SLACK_CHANNEL_ID`
- メンション運用はグローバル指示に従い `<@U08RPS2BLUD>` を本文に含める

## 非機能

- BOT_TOKEN が無ければ**静かに終了**（return 0）。CI や secrets 未設定の端末で落ちない
- curl 失敗時も `|| true` で握りつぶす。通知は副次的処理のため本体を止めない
- POST body は python3 で JSON シリアライズして改行・特殊文字を安全に扱う
