---
name: vue-review
description: Vue 3 SFCをベストプラクティスに照らして一括レビューする。「Vueコンポーネントをレビューして」「SFCをチェックして」「型安全性を確認して」「TailwindのUIを検査して」「Biomeルールへの準拠を確認して」と依頼された時に使用する。
metadata:
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Vue 3 コンポーネントレビュースキル

このスキルは Vue 3 SFC（Single File Component）を以下の観点から一括レビューする：

- Vue 3 / Composition API のベストプラクティス
- TypeScript の型安全性
- Tailwind CSS の使用パターン
- Biome のlinting・formatting ルール
- アクセシビリティ

## 動作方法

1. `$ARGUMENTS` で指定されたファイルまたはパターンを読み込む
2. ファイルが未指定の場合はどのファイルをレビューするかユーザーに確認する
3. 以下の全チェック項目に照らして確認する
4. 問題は後述の出力例と同じ形式で一括出力する

## チェック項目

### Vue 3 / Composition API

**必須パターン**
- `<script setup lang="ts">` を使用しているか（Options API は使用しない）
- `defineProps<T>()` で Props を型付けしているか（`withDefaults` を必要に応じて使用）
- `defineEmits<T>()` で Emits を型付けしているか
- `ref` / `reactive` / `computed` を適切に使い分けているか
- `watchEffect` より `watch` を優先し、依存を明示しているか
- `onMounted` などのライフサイクルフックは `<script setup>` 内に記述されているか

**アンチパターン（警告）**
- `any` 型の使用
- `reactive()` でプリミティブをラップしている
- テンプレート内の inline arrow function（パフォーマンス劣化）
- `v-for` に `key` が未設定、または index を key に使用
- `v-if` と `v-for` を同一要素に併用

### TypeScript 型安全性

**必須**
- Props は `interface` または `type` で明示的に型定義されているか
- `ref<T>()` のジェネリクスを省略していないか（推論できない場合）
- API レスポンスの型は `shared/api` の OpenAPI 定義から引用しているか
- `null` / `undefined` の可能性がある値を non-null assertion（`!`）で握り潰していないか

**推奨**
- `readonly` で変更不要な Props を保護しているか
- `as const` を enum 代替として使用しているか

### Tailwind CSS

**必須**
- インラインスタイル（`style=""`）ではなく Tailwind クラスを使用しているか
- 独自の CSS は `<style>` ブロックに閉じ込め、グローバルスタイルを汚染していないか
- レスポンシブ対応が必要な箇所に breakpoint prefix（`sm:` `md:` `lg:`）を使用しているか

**推奨**
- 繰り返し使う長いクラス列は `@apply` や子コンポーネントへの切り出しを検討しているか
- `text-` / `bg-` などはプロジェクトの色パレット変数（`tailwind.config` 準拠）を使用しているか
- ダークモード対応が必要な箇所に `dark:` prefix を使用しているか

### Biome（Linting / Formatting）

**Linting チェック**
- 未使用の import がないか（`noUnusedImports`）
- 未使用の変数がないか（`noUnusedVariables`）
- `console.log` が本番コードに残っていないか（`noConsole`）
- 条件式に代入が含まれていないか（`noAssignInExpressions`）
- `==` ではなく `===` を使用しているか（`noDoubleEquals`）

**Formatting チェック**
- インデントは 2 スペース（tab は不使用）
- セミコロンの有無はプロジェクトの `biome.json` 設定に従う
- import 文は自動整列されているか

### アクセシビリティ

- インタラクティブ要素（`button`, `input` 等）に `aria-label` または可視テキストがあるか
- 画像に `alt` 属性が設定されているか
- フォームの `<label>` と `<input>` が関連付けられているか（`for` / `id`）

## 出力形式

```
## レビュー結果: <ファイルパス>

### 重大（修正必須）
- file:line: 説明

### 警告（修正推奨）
- file:line: 説明

### 情報（参考）
- file:line: 説明

### 合格
- チェック項目: OK
```

問題が 0 件の場合は「全チェック合格」と出力する。

## 詳細リファレンス

より詳細なルールは以下を参照する：

- [references/vue3-patterns.md](references/vue3-patterns.md) — Vue 3 Composition API パターン集
- [references/typescript-patterns.md](references/typescript-patterns.md) — TypeScript 型安全パターン
- [references/biome-rules.md](references/biome-rules.md) — Biome 設定と主要ルール
