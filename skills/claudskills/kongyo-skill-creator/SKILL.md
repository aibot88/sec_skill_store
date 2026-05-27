---
name: kongyo-skill-creator
description: "Use when authoring a new skill, refactoring an explanation-heavy skill into an executable runbook, standardizing skill structure, reviewing skill practicality, or preparing skill validation before deployment."
---

# Kongyo Skill Creator

`kongyo` 系 skill の強みは「知識の説明」ではなく「その場で動ける運用メモ」にある。最初の 1 画面で何をすればいいかが分かり、分岐基準と失敗時の戻り方が見え、必要なら `references/` と `assets/` に深掘りできる形へ整える。新規作成や大きな変更では、skill もコードと同じく「失敗例で検証してから直す」対象として扱う。

## いつ使うか

- 新規 skill を作るが、実行手順・判断基準・落とし穴まで含めたいとき
- 既存 skill が説明中心で、現場でそのまま使えないとき
- 複数の skill を同じ書き味に寄せたいとき
- `description` の trigger、section 順序、テンプレ資産の切り出し方を見直したいとき
- 新規 skill や重要 skill を、subagent シナリオで検証してから出したいとき

使わない場面:
- 一回限りのメモ
- API 仕様を保管するだけの資料
- 既に短く完結していて、分岐も再利用資産もない skill

## クイックスタート

1. 入力の形を確認する。実ファイル、貼り付け本文、箇条書きメモのどれでもよい。
2. `## モードを決める` の表で `new / refactor / standardize / review` を 1 つ選ぶ。
3. `## 必要入力` の不足を埋める。不明な値は推測で固定せず、placeholder と確認事項に回す。
4. `## 出力契約` と `## 出力テンプレート` に沿って、`SKILL.md` 草案またはレビュー結果を出す。
5. 新規作成、大幅変更、discipline-enforcing skill なら `## 検証サイクル` で失敗シナリオと再評価を設計する。
6. 最後に `references/review-checklist.md` の Quality Gate で自己採点する。

## 必要入力

| 入力 | 必須 | 不足時の扱い |
|---|---|---|
| 対象 source | 必須 | skill 化する本文、既存 `SKILL.md`、またはメモの提示を依頼する |
| 作業モード | 推奨 | `## モードを決める` で推定し、成果物に推定理由を書く |
| 想定利用者 / 完了条件 | 推奨 | `誰が何を終えるための skill か` を仮置きし、確認事項に残す |
| 前提環境 / toolchain | 任意 | 不明なら汎用 placeholder にし、固有コマンドを断定しない |
| 既存の `references/` / `assets/` | 任意 | 無ければ候補だけ示し、実ファイル作成は求められた場合だけ行う |
| 検証要否 | 任意 | 新規、大幅変更、規律を守らせる skill は検証対象として扱う |

## モードを決める

| 状況 | モード | 返すもの |
|---|---|---|
| 新しい skill を作る材料だけがある | `new` | kongyo-style の `SKILL.md` 草案 |
| 既存 skill が説明中心で実行しにくい | `refactor` | 書き換え後の `SKILL.md` 草案と主な変更点 |
| 複数 skill の書き味を揃えたい | `standardize` | 共通構成、差分方針、代表テンプレ |
| 既存 skill が実用可能か見たい | `review` | checklist 採点、合否、最小修正案 |
| skill の効き方を確かめたい | `validate` | pressure/application scenario、期待失敗、再評価計画 |
| source が短すぎて skill 化の価値が薄い | `no-op / ask` | 提案不要の理由、または不足情報の質問 |

## 最初に読むもの

- `references/kongyo-skill-patterns.md`
  `kongyo` 系 skill を 3 archetype に分類している。まずこれで寄せる型を決める。
- `references/review-checklist.md`
  仕上げ前の品質ゲート。trigger 明確性、初速、分岐、コピペ性、事故防止を採点する。
- `references/skill-tdd-and-discovery.md`
  新規作成、大幅変更、description 見直し、subagent 検証が必要なときだけ読む。

## 出力契約

最低でも次を満たす。

| 項目 | 必須条件 |
|---|---|
| Frontmatter | `name` は kebab-case、`description` だけで trigger が判断できる |
| First screen | 先頭 1 画面で「いつ使うか」「最短成功パス」「必要入力」が読める |
| Decision support | 分岐が 2 つ以上あるなら table または `if ... then ...` を置く |
| Reuse | コマンド、プロンプト、設定例、テンプレのいずれかを 1 つ以上置く |
| Failure handling | 3 件以上の落とし穴、または troubleshooting を置く |
| Disclosure | 長い詳細は `references/`、コピーして使う雛形は `assets/` に逃がす |
| Discovery | `description` は trigger-only。workflow 要約を書かない |
| Validation | 新規・大幅変更なら検証シナリオまたは検証結果を残す |

必要に応じて次も追加する。

- `references/`: variant ごとの詳細、長い API/CLI 補足、評価軸、比較表
- `assets/`: 雛形ファイル、最小プロジェクト、設定例、画像・アイコン
- `scripts/`: 同じコードを何度も書くか、手動では壊しやすい処理があるとき

## Archetype を決める

primary archetype を 1 つ決めてから書く。hybrid は許容するが、初速を支配するのは 1 つに絞る。

| Archetype | 向いている skill | 最初に必要なもの | 典型的な追加資産 |
|---|---|---|---|
| Operations | 個人/チーム運用、日常手順、環境管理 | 前提環境、layout/table、日常フロー | command cheat sheet、troubleshooting |
| Practice | CLI / library / FFI / framework の実践ガイド | quickstart、原則、実例、decision table | `references/` の詳細 docs、`assets/` の starter |
| Meta | skill 作成、分類、提案、ふりかえり | 分類基準、出力契約、提案テンプレ | archetype 別 template、review checklist |

具体例は `references/kongyo-skill-patterns.md` を読む。

## Workflow

1. **ソースを監査する**
   次を抜き出す。
   - 誰が何を終えるための skill か
   - 最短成功パスは何か
   - どこで判断が分岐するか
   - 何を間違えると痛いか
   - 何を `assets/` や `references/` に切り出せるか
   - 不明な固有値を placeholder にするか、確認事項に回すか
   - どんな状況で agent が失敗・合理化しそうか

2. **primary archetype を決める**
   `Operations / Practice / Meta` のどれが中心かを先に決める。全部入りにしない。

3. **`SKILL.md` / `references/` / `assets/` の境界を切る**
   - `SKILL.md`: すぐ動くための手順、判断、注意点だけ残す
   - `references/`: variant 詳細、長い比較表、評価軸、公式情報の要約
   - `assets/`: そのままコピーしたい雛形や最小構成
   - `scripts/`: deterministic にしたい処理だけ

4. **frontmatter を先に確定する**
   `description` は trigger-only にする。
   `Use when <task>, <symptom>, or <decision point>.`

   悪い例: `XX を設定し、A を確認し、B を修正する runbook`
   良い例: `Use when 新規導入、既存設定の修正、または failure 原因調査を行うとき。`

5. **先頭 1 画面を作る**
   以下を優先順に置く。
   - `## いつ使うか`
   - `使わない場面`
   - quickstart か minimal workflow
   - 必要入力 / 前提環境

   抽象的な背景説明はこの後ろに回す。

6. **分岐と判断基準を書く**
   branch が 2 つ以上あるなら、table か `if ... then ...` を必ず入れる。
   判断が暗黙だと skill は trigger しても実行で詰まる。

7. **コピペ資産を置く**
   次のどれかを必ず 1 つ以上用意する。
   - コマンド列
   - dispatch prompt
   - 設定ファイル全文
   - 雛形 SKILL
   - 変更提案フォーマット

   placeholder を使うなら、何に置換するかも 1 行で明記する。
   資産の中に fenced code block を含めるなら、外側は 4 backticks 以上にして Markdown が壊れないようにする。

8. **落とし穴と戻り方を書く**
   `気をつける` だけで終わらせない。
   `誤り -> 実害 -> 回避策` か `症状 -> 原因 -> 打ち手` で書く。

9. **仕上げを検査する**
   `references/review-checklist.md` で採点する。

## 検証サイクル

新規 skill、大幅変更、discipline-enforcing skill は、読むだけのレビューで出さない。subagent が使えるなら、最低 1 本は「実際に使う」シナリオで検証する。

| 対象 | 検証方法 | 見るもの |
|---|---|---|
| 規律を守らせる skill | pressure scenario | agent が抜け道や合理化をしないか |
| 実践 guide / runbook | application scenario | 手順、入力、分岐、failure handling が使えるか |
| reference skill | retrieval scenario | 必要情報にたどり着けるか、穴がないか |
| review だけ | static checklist | 0 点軸、template 崩れ、description trap |

検証で失敗したら、失敗内容をそのまま潰す最小修正だけを入れる。詳細な scenario 設計、合理化表、RED-GREEN-REFACTOR の進め方は `references/skill-tdd-and-discovery.md` を読む。

## 不足情報の扱い

- 命名規則、承認者、CLI、DBMS、framework などの固有値が無いときは、`<PLACEHOLDER>` にして置換ルールを書く
- 一般化してよい値は一般化する。例: DBMS 不明なら PostgreSQL 固有構文を避け、`EXPLAIN` など共通概念に寄せる
- `references/` や `assets/` は、ユーザーがファイル作成を求めていない場合は「切り出し候補」として示す

## 出力テンプレート

### `new` / `refactor`

```md
---
name: <skill-name>
description: "Use when <task>, <symptom>, or <decision point>."
---

# <Skill Title>

## いつ使うか

- <trigger 1>
- <trigger 2>

使わない場面:
- <out of scope>

## クイックスタート / 最短成功パス

1. <first action>
2. <decision or verification>
3. <final output or handoff>

## 必要入力 / 前提環境

| 入力 | 必須 | 不足時の扱い |
|---|---|---|
| <input> | 必須 | <ask / placeholder / skip> |

## Decision Table

| 状況 | 次の操作 |
|---|---|
| <condition> | <action> |

## コピペ資産

<command / prompt / checklist / file template>

## Failure Handling

| 症状 | 原因 | 打ち手 |
|---|---|---|
| <symptom> | <cause> | <action> |

## 検証計画

- Scenario: <agent がこの skill を実際に使う現実的な状況>
- Expected failure without skill: <baseline で起きそうな失敗>
- Pass condition: <成果物が満たす条件>
```

### `review`

````md
## 現状評価

<合格 / 要修正 / 提案不要>。<理由 1-2 文>

## Checklist 採点

| 軸 | 点 | 理由 |
|---|---:|---|
| Trigger clarity | <0-2> | <reason> |
| First-screen success path | <0-2> | <reason> |
| Inputs / prerequisites | <0-2> | <reason> |
| Decision support | <0-2> | <reason> |
| Copy-paste assets | <0-2> | <reason> |
| Failure handling | <0-2> | <reason> |
| Progressive disclosure | <0-2> | <reason> |
| Fidelity | <0-2> | <reason> |
| Validation readiness | <0-2> | <reason> |

## 最小修正案

| 変更箇所 | 修正内容 |
|---|---|
| `description` | <trigger-only に直し、workflow 要約を消す> |
| body | <first-screen / decision / template / failure handling の不足を埋める> |
| validation | <必要なら scenario と pass condition を追加する> |

## 改善パッチ案

```md
<貼り付け可能な差分または置換案>
```
````

## 記述ルール

- 理屈より先に操作を書く
- 見出しは `読む順 = 作業順` に寄せる
- 断定できることは断定する
- `description` は起動条件だけを書く。手順や workflow を要約しない
- 一般論より固有名詞、コマンド、ファイル名、しきい値を優先する
- テンプレート内に三連バッククォートを含める場合、外側 fence は四連バッククォート以上にする
- 例は少なくてよい。使える 1 例を、複数の薄い例より優先する
- section が長くなったら要約だけ `SKILL.md` に残し、詳細は `references/` に逃がす
- 複数 variant があるなら対称的な section を並べるより、decision table で入口を一本化する
- 関連 skill は「次に何を読むべきか」が自然なものだけ残す

## Quality Gate

`references/review-checklist.md` の合格条件を満たすまで出さない。

- 合計 14/18 以上
- `Trigger clarity`, `First-screen success path`, `Decision support`, `Failure handling` の 4 軸で 0 点を出さない
- `references/` や `assets/` を追加した場合は、`SKILL.md` から直接たどれる状態にする
- 新規、大幅変更、規律を守らせる skill では検証シナリオか検証結果を示す

## Red Flags

- `description` が「ガイド」「ベストプラクティス」だけで終わっている
- `description` が手順や workflow を要約していて、本文を読まずに動けてしまう
- quickstart が理屈の後ろに埋もれている
- branch があるのに decision table がない
- テンプレが抽象的で、コピペしても動かない
- テンプレ内テンプレの code fence が同じ backtick 数で、Markdown として閉じ位置が崩れる
- 「明らかに分かるから検証不要」として、使うシナリオを走らせていない
- `references/` に逃がしたのに `SKILL.md` から読みに行く条件が書かれていない
- 落とし穴が `注意する` `確認する` で終わる
- archetype を混ぜすぎて、最初の見出し順が作業順になっていない
