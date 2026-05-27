---
name: dev-standards
description: i-Willink 共通開発標準。スタック非依存の汎用層（TypeScript strict / Conventional Commits / OWASP / テスト方針 / コミット粒度）。各 agent が起動時に preload する。プロジェクト固有の規約は `project-standards` skill 側に書く。
---

# i-Willink Dev Standards (stack-agnostic)

このスキルは i-Willink 全プロジェクトに共通する開発標準。**スタック特化のルールは含まない** — それは各プロジェクトの `project-standards` skill が担う。

---

## 1. コード品質

### 言語横断
- **意図が読める命名**: 短さより明瞭さ。`d` ではなく `dueDateUtc`
- **コメントは「WHY」が非自明な時のみ**: 制約・不変条件・回避策・読み手が驚く挙動。WHAT を書かない（コード自体が説明する）
- **早期 return で nest を浅く**: ガード節で例外条件を最初に処理
- **YAGNI**: 仮想の将来要件のための抽象化禁止。3 行類似は重複ではなく「まだ重複じゃない」

### TypeScript（採用プロジェクトのみ適用）
- `strict: true` 必須。`any` 禁止、`unknown` を使い narrowing する
- `noUncheckedIndexedAccess: true` 推奨
- 型の export は `type` キーワード明示

### Flutter / Dart（採用プロジェクトのみ）
- `analysis_options.yaml` の `strict-casts` / `strict-inference` / `strict-raw-types` を有効化
- null safety を抜けない（`!` の使用は局所化して justify コメント）

### PHP / WordPress（採用プロジェクトのみ）
- PHPCS WordPress-Extra 準拠
- `wp_unslash()` / `sanitize_*()` / `esc_*()` は **境界**で必ず実施

---

## 2. テスト方針

- **境界では検証、内部では信頼**: 外部入力・API・DB 境界を厚く、純粋関数の internals は薄く
- **happy path だけでは不十分**: edge case と failure path を必ず 1 本ずつ
- **モックは外部境界のみ**: 内部関数のモックは設計が壊れているサイン
- **テストの命名**: `test_<対象>_<条件>_<期待結果>` 形式（言語慣習に従って adapt）
- **新規コード**: カバレッジ 80% 以上目安（hard rule ではない・behavior coverage を優先）

---

## 3. セキュリティ

### OWASP Top 10 を常に意識
- **Injection**: prepared statements / parameterized queries 必須
- **Broken Access Control**: 認可は API 層で必ず（フロントだけはダメ）
- **Cryptographic Failures**: 自前 crypto 禁止、ライブラリ標準を使う
- **SSRF / XSS / CSRF**: フレームワークの保護機構を無効化しない

### 秘密情報
- `.env` をコミットしない（`.env.example` のみ管理）
- API キー・トークンをコードに hardcode 禁止
- ログに secrets を出さない（マスキング必須）

---

## 4. コミット規約

**Conventional Commits 必須**:

```
<type>(<scope>): <subject>

[body — WHY を書く]

[footer]
```

### type
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみ
- `refactor`: 振る舞いを変えない構造変更
- `test`: テストのみ
- `chore`: ビルド・依存・設定
- `perf`: パフォーマンス改善
- `style`: フォーマットのみ

### コミット粒度
- **1 commit = 1 論理変更**。レビューしやすさ最優先
- 大きな変更は分割（feat 1 件で 800 行超えたら分割を検討）
- WIP commit を main に混ぜない（feature branch 上では OK・squash で消す）

---

## 5. PR 運用

- **小さく、レビューしやすく**: 500 行超は分割を真剣に検討
- **PR description で WHY を語る**: WHAT は diff で読める
- **Self-review してから request review**: 自分で 1 周読む
- **CI green で初めて merge 可能**

---

## 6. AI 開発（Claude Code / Codex 使用時）

- **Generator-Verifier 分離**: 実装はメイン agent（Claude Code は main Claude、Codex は main Codex）、レビューは Verifier role（dev-reviewer 相当）
- **Telephone game 回避**: 順序的同一作業を subagent 連鎖に分割しない
- **Early victory 警戒**: テスト 1-2 本で「成功」を信じない（dev-tester プロトコルに従う）
- **同一ファイル並列編集禁止**: subagent 並列起動時は read-only に限定
- **Codex subagent は明示許可時のみ**: Codex ではユーザーが subagent / delegation / parallel agent work を明示した場合だけ起動する
- **project knowledge は共有**: Codex でも `.claude/skills/project-standards/SKILL.md` と `.claude/agent-memory/dev-reviewer/MEMORY.md` を読む（Codex 専用 copy は作らない）

---

## 7. このスキルの境界

含む: 全プロジェクト共通の最低ライン
含まない: スタック特化規約・プロジェクト固有のドメイン知識・チーム慣習

→ プロジェクト固有のものは `.claude/skills/project-standards/SKILL.md` に書く（雛形は kit の `examples/project-standards-template/` 参照）。このパスは Claude Code と Codex で共有する。
