---
name: passive
description: パッシブスキルシステムの設計リファレンス。パッシブのデータモデル・発動条件(always/attack/none)・スロットシステム・生成パイプライン・ランタイム実行フローを網羅する。パッシブの新規追加、発動条件の変更、弓パッシブの調整、装備スロットの操作などで参照すること。passive, パッシブ, スロット, slot, 弓スキル, bow skill, 装備効果, attack, always, none などのキーワードで使う。
---

# パッシブスキルシステム

パッシブは装備や持ち替えで自動発動するスキル。プレイヤーに最大3つのスロットがあり、それぞれに1つのパッシブを装備できる。

## 関連スキル

- **magic-casting**: 詠唱パイプライン。パッシブ「設定書」使用時の装備処理もこれを通る
- **active**: アクティブシステム。詠唱パイプラインを共有
- **ohmydat**: プレイヤー個別ストレージ。パッシブ装備状態の保存先
- **maf-export**: Go ジェネレータのエクスポートパイプライン全体

---

## 1. データモデル（Generator側）

### Passive 構造体

**ファイル:** `maf-command-generator/app/domain/model/passive/types.go`

```go
type Passive struct {
    ID               string     // スラッグID
    Name             string     // 表示名（最大80文字）
    Role             string     // 役割説明（最大200文字）
    Condition        string     // 発動条件: "always" | "attack" | "none"
    Slots            []int      // 装備可能スロット（1〜3, ユニーク, 最低1つ）
    Description      string     // 効果説明（最大400文字）
    Script           []string   // 発動時コマンド（1行以上）
    Bow              *BowConfig // bow専用設定（任意）
    GenerateGrimoire *bool      // true: 設定書を生成しルートテーブルから参照可能 / false: 設定書未生成・ルートテーブル参照不可（必須）
}

type BowConfig struct {
    LifeSub *int // 矢の寿命短縮量（0〜1200 tick）
}
```

### generate_grimoire フィールド

- 必須フィールド。省略するとバリデーションエラー
- `false` にすることで「設定書では入手できないが、特定アイテムに付与できるパッシブ」を定義できる

### 発動条件（Condition）の意味

| Condition | 発動タイミング | 処理ファイル |
|-----------|-------------|------------|
| `always` | 毎tick（装備中ずっと） | `passive/tick` → `run_effect` |
| `attack` | 近接攻撃でダメージを与えた時 | `advancement/melee_hit` → `passive/on_melee_hit` → `passive/tick` |
| `none` | 自動発動なし（手動呼び出し専用） | `function maf:generated/passive/effect/{id}` を他システムから実行 |

---

## 2. 生成パイプライン

**ファイル:** `maf-command-generator/app/domain/export/passive.go`

```
savedata/passive.json
    ↓ PassiveEntity.Load()
model/passive/Passive[]
    ↓ export.BuildPassiveArtifacts()
    ├── []PassiveEffectFunction   { ID, Body }
    ├── []PassiveBowFunction      { ID, Body }
    └── []PassiveActiveFunction { PassiveID, Slot, FunctionID, GiveBody, ApplyBody, Book }
    ↓ WritePassiveArtifacts()
generated/passive/
    ├── effect/{id}.mcfunction        — 効果スクリプト
    ├── bow/{id}.mcfunction           — 弓パッシブ専用スクリプト
    ├── give/{id}_slot{N}.mcfunction  — 設定書 give コマンド
    ├── apply/{id}_slot{N}.mcfunction — スロット書き込み処理
    └── spell/{id}_slot{N}.mcfunction — 設定書使用時の casting ロード
```

### 生成される成果物（各パッシブにつき複数ファイル）

1. **effect/{id}.mcfunction** — 効果スクリプト
   - `always`/`attack`/`none`: `Script[]` をそのまま結合
2. **bow/{id}.mcfunction** — `bow` 条件のパッシブ専用。矢着弾時に実行される本体スクリプト
3. **give/{id}_slot{N}.mcfunction** — パッシブ設定書（本）の give コマンド
4. **apply/{id}_slot{N}.mcfunction** — `oh_my_dat` にパッシブID/conditionを書き込む処理
5. **spell/{id}_slot{N}.mcfunction** — `oh_my_dat:...maf.magic.casting` に `kind:"passive"` の詠唱データを書き込む処理

---

## 3. 弓パッシブの特殊生成

**ファイル:** `passive.go` の `buildBowEffectBody()`

`bow` 条件のパッシブは `effect/{id}.mcfunction` が自動生成される:

```mcfunction
execute unless score @s mafBowUsed matches 1.. run return 0
execute store result storage maf:tmp bow_player_id int 1 run scoreboard players get @s mafPlayerID
execute as @e[type=arrow,...] run function maf:passive/tag_passive_arrow {passive_id:"...",life:N}
```

- `mafBowUsed`: 弓を使った回数（バニラスコアボード）。1以上なら弓を使った
- `life`: 矢の生存tick。`1200 - LifeSub` で計算。LifeSub 未設定時は `1200 - 1200 = 0` になり即消滅
- 矢にタグ `maf_passive_arrow` を付与し、パッシブ情報を矢アイテムの custom_data に書き込む

---

## 4. ランタイム実行フロー（Datapack側）

### 4a. always パッシブ（毎tick）

```
maf:magic/tick
  → maf:passive/tick          (全プレイヤー毎tick)
    → slot1/2/3 にIDがあれば → maf:passive/run_effect with {id}
      → $function maf:generated/passive/effect/$(id)  (マクロ)
    → メインハンド装備にパッシブがあれば → run_mainhand_effect
      → oh_my_dat にID/slot/conditionをコピー → run_effect
```

### 4b. bow パッシブ（弓使用→矢着弾）

**発射フェーズ（passive/tick 内）:**
```
effect/{id}.mcfunction (自動生成)
  → mafBowUsed >= 1 を確認
  → 近くの矢にタグ付け + パッシブ情報を embed
  → tag_passive_arrow.mcfunction で矢に maf_passive_arrow タグ + custom_data 書き込み
```

**着弾フェーズ（advancement トリガー）:**
```
advancement/arrow_hit.json → maf:passive/on_arrow_hit
  1. maf_passive_arrow タグ付き矢を探す
  2. 矢の custom_data からパッシブ情報を maf:tmp に退避
  3. HurtTime:10s のエンティティ（ダメージを受けた対象）に対して実行:
     → run_bow_effect with maf:tmp → $function maf:generated/passive/bow/$(passiveId)
  4. 矢を kill、一時データ削除
```

### 4c. パッシブ設定書の使用（装備処理）

パッシブ設定書も `minecraft:book` アイテムで、`maf.passive.{id,slot,condition}` を持つ。  
使用すると `magic/use_active` が `generated/passive/spell/{id}_slot{slot}` を呼んで casting を作り、通常の詠唱パイプラインを通る:

```
cast/exec → run_passive_apply with {id, slot}
  → $function maf:generated/passive/apply/$(id)_slot$(slot)
    → oh_my_dat の maf.passive.slot{N}.id に passiveID を書き込み
    → "[slotN]に[パッシブ名]を設定しました" メッセージ
```

- 詠唱時間: 固定 200 tick（10秒）
- MP消費: 固定 10 MP
- クールダウン: 0

---

## 5. oh_my_dat ストレージ構造

### パッシブ装備状態

```
oh_my_dat: _[-4]...[-4].maf.passive
├── slot1.id: "regeneration"     ← スロット1に装備中のパッシブID
├── slot2.id: "test_bow_passive" ← スロット2
├── slot3.id: (なし)             ← 空きスロット
└── mainhand                     ← 一時領域（毎tick書き込み→削除）
    ├── id: "..."
    ├── slot: N
    └── condition: "..."
```

- `slot1`〜`slot3` は永続。設定書使用時に書き込まれる
- `mainhand` は一時的。`run_mainhand_effect` が毎tick作成→使用→削除する

### アイテム側のパッシブ情報

```snbt
minecraft:custom_data={
  maf:{
    passiveId: "regeneration",
    passiveSlot: 1,
    passiveCondition: "always",
    passive: {id:"regeneration", slot:1, condition:"always"}
  }
}
```

`cost/cast/cooltime/title/description` はアイテムへ埋め込まず、`generated/passive/spell/{id}_slot{N}.mcfunction` から実行時に `maf.magic.casting` へロードする。

---

## 6. パッシブ追加手順

1. `savedata/passive.json` にエントリ追加
2. `Condition` を設定（`always`/`attack`/`none`）
3. `Slots` を設定（例: `[1, 2]` → スロット1か2に装備可能）
4. `Script` に効果コマンドを記述
5. `generate_grimoire` を設定（`true`: 設定書を生成する / `false`: 設定書不要）
6. `none` は tick 自動発動しないため、必要に応じて他functionから `maf:generated/passive/effect/{id}` を呼び出す
7. `make run/export` で生成
8. `generate_grimoire: true` なら `/function maf:generated/passive/give/{id}_slot{N}` でテスト
