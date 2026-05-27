---
name: philips-hue
description: "Philips Hue スマートライトの制御スキル。Hue BridgeのローカルCLIP API v2を使用して照明のON/OFF、明るさ調整、色変更、シーン制御を行う。「Hueの電気をつけて」「リビングを暖色にして」「全部の照明を消して」「ライトの一覧」などの依頼時に使用。"
---

# Philips Hue 制御スキル

## 環境変数

`.env` に以下を設定:
- `HUE_BRIDGE_IP` - Hue BridgeのローカルIP
- `HUE_API_KEY` - Hue APIキー

## APIキーの取得方法

1. Hue Bridge と同じLANに接続
2. `scripts/hue_control.py discover` でBridge IPを発見
3. Hue Bridge の物理ボタンを押す
4. `scripts/hue_control.py register` でAPIキーを取得
5. `.env` に記録

## 使い方

```bash
# Bridge発見
python3 scripts/hue_control.py discover

# APIキー登録
python3 scripts/hue_control.py register

# デバイス一覧
python3 scripts/hue_control.py list

# ライトON/OFF
python3 scripts/hue_control.py on <light_id>
python3 scripts/hue_control.py off <light_id>

# 明るさ設定 (0-100)
python3 scripts/hue_control.py brightness <light_id> 80

# 色設定 (色温度 153-500 mirek)
python3 scripts/hue_control.py color_temp <light_id> 300

# 全ライトOFF
python3 scripts/hue_control.py all_off
```

## API リファレンス

ローカル CLIP API v2 エンドポイント: `https://<bridge_ip>/clip/v2/resource/`

主要リソース:
- `light` - 個別ライト
- `room` - 部屋
- `scene` - シーン
- `grouped_light` - グループライト

認証ヘッダー: `hue-application-key: <api_key>`

SSL証明書はBridge自己署名のため `verify=False` で接続する。
