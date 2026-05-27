---
name: pev-bootstrap-playwright
description: pev-harness を使うプロジェクトに Playwright を導入する自動 bootstrap skill。 npm install / browser binary / playwright.config.ts template / seed test template / `npx playwright init-agents --loop=claude` (Playwright agents 自動生成) の 5 step を 1 操作で完了する。 pev-e2e-verify skill の Preflight が「未setup」と判定した時に自動的に提案される。
---

# pev-bootstrap-playwright

`pev-e2e-verify` skill を使えるようにする **one-time setup** skill。 新規プロジェクトに Playwright + Playwright agents を導入する 5 step を 1 操作で完了する。

## When to Use

起動すべき場面:

- `pev-e2e-verify` skill の Preflight が「Playwright 未setup」を検知した時 (auto-propose)
- ユーザーが `/pev-init-e2e` を明示的に呼んだ時
- 新規プロジェクトに pev-harness の E2E verification 機能を有効化したい時

起動すべきでない場面:

- Playwright が既に install + agents 初期化済の場合 (Preflight が detect)
- Playwright を使わない方針のプロジェクト (config に明示)

## Bootstrap Steps

### Step 1: 依存性 install

```bash
# プロジェクトルートで実行
npm install -D @playwright/test http-server
```

`@playwright/test` は test runner + assertion library。 `http-server` は webServer config 用 (Vite / Next.js を使うプロジェクトでは不要)。

### Step 2: Browser binary install

```bash
npx playwright install --with-deps chromium
```

Chromium のみで十分 (Firefox / WebKit は必要に応じて追加)。 `--with-deps` は CI/Linux で必要な system deps も install。

### Step 3: `playwright.config.ts` template 作成

プロジェクトに `playwright.config.ts` がない場合、 以下の template を書く:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests-e2e',
  outputDir: './artifacts/e2e/test-results',
  reporter: [
    ['list'],
    ['html', { outputFolder: './artifacts/e2e/playwright-report', open: 'never' }],
    ['json', { outputFile: './artifacts/e2e/results.json' }],
  ],
  webServer: {
    command: 'npm run preview', // プロジェクトの dev server コマンド
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

ユーザーに `webServer.command` と `baseURL` を質問返しする (プロジェクトの dev server に依存):

- Vite: `npm run dev` → `http://localhost:5173`
- Next.js: `npm run dev` → `http://localhost:3000`
- 静的 HTML: `npx http-server public -p 8080` → `http://localhost:8080`

### Step 4: Seed test template 作成

`tests-e2e/seed.spec.ts` を作成:

```ts
import { test, expect } from '@playwright/test';

// Seed test — Playwright agents (planner/generator) の前提として必須。
// 環境初期化 + 生成 test の参考例として機能する。
// このテストは plain homepage 確認のみ、 アプリの "smoke test" として最低限の動作確認。

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/.+/); // タイトルが空でないこと
});
```

プロジェクトの特性に応じて template を微調整 (e.g., login flow 必須なら seed test に含める)。

### DRY pattern (v1.6+、 dog food finding)

dog food (v1.4+v1.5、 multiply 機能) で、 各 test の `page.on('console', ...)` 等の boilerplate (5-6 行) が repeat される問題が判明。 Playwright Generator agent は seed.spec.ts を mirror するので、 **seed に DRY pattern を仕込む** と generated tests も DRY になる。

推奨 seed test pattern (sample-project の seed.spec.ts 参照):

```ts
import { test, expect, type Page, type ConsoleMessage } from '@playwright/test';

// Fixture: console error を全 test で監視
const consoleErrors: string[] = [];

test.beforeEach(async ({ page }) => {
  consoleErrors.length = 0;
  page.on('console', (msg: ConsoleMessage) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (err: Error) => {
    consoleErrors.push(`pageerror: ${err.message}`);
  });
});

// Helper: 共通 navigation
async function goHome(page: Page) {
  await page.goto('/');
  await expect(page.locator('h1')).toBeVisible();
}

test('homepage loads', async ({ page }) => {
  await goHome(page);
  // ...
});
```

Playwright Generator が新規 spec を書くとき、 `goHome(page)` のような既存 helper を **再利用** することが期待される。 重複 boilerplate を避ける。

### Step 5: Playwright agents 初期化

```bash
npx playwright init-agents --loop=claude
```

これで以下が **自動生成** される (1.59.1 で確認):

```text
.claude/agents/
├── playwright-test-planner.md     # 探索 + test plan 生成
├── playwright-test-generator.md   # plan → executable test
└── playwright-test-healer.md      # 失敗 test の自動修復
.mcp.json                          # playwright-test MCP server 設定
specs/README.md                    # test plan 置き場
```

**重要**: 各 agent の `tools:` field には `mcp__playwright-test__*` (browser 操作 + test 生成専用 tool) が listed されている。 Playwright が独自に spawn する `playwright-test` MCP server (`npx playwright run-test-mcp-server`) によって動く。 これは一般 `playwright` MCP とは別物、 test workflow 専用。

(注意: 公式 docs では `.github/` と記載されているが、 実装では `.claude/agents/` に出力される。 1.59.1 で確認済)

### Step 6 (option): `.gitignore` 更新

```gitignore
# Playwright artifacts
artifacts/e2e/
playwright-report/
test-results/
```

`artifacts/e2e/` は実行ごとに変わる中間生成物なので gitignore。 ただし `tests-e2e/` のテストコードと `specs/` の test plan はコミット対象。

## 実行手順 (Bash でまとめて)

```bash
# pev-bootstrap-playwright skill 起動時、 agent が以下を順次実行:

# Step 1
npm install -D @playwright/test http-server

# Step 2
npx playwright install --with-deps chromium

# Step 3: playwright.config.ts (template) を Write — webServer は user に確認
# Step 4: tests-e2e/seed.spec.ts を Write
# Step 5
npx playwright init-agents --loop=claude

# Step 6: .gitignore に追記
```

## sample-project での example

`examples/sample-project/` には v1.4 で playwright が install済の状態でコミットされている。 dog food fixture として、 pev-bootstrap-playwright skill を 1 度だけ実行した結果を repository に commit してある。

そのため、 sample-project では skill 起動は不要 (既に setup 済)。 他のプロジェクトでは初回 setup 時にこの skill を起動する。

## Preflight check との連動

`pev-e2e-verify` skill の Preflight が以下を確認:

| Check | Bootstrap step |
|---|---|
| `node_modules/@playwright/test/` 存在 | Step 1 |
| `npx playwright --version` 動作 | Step 1 + 2 |
| `playwright.config.ts` 存在 | Step 3 |
| `tests-e2e/seed.spec.ts` 存在 | Step 4 |
| `.claude/agents/playwright-test-{planner,generator,healer}.md` | Step 5 |
| `.mcp.json` の playwright-test MCP 設定 | Step 5 |

不足項目があれば該当 Step のみ実行可能 (incremental setup)。

## Failure handling

| Failure | 対処 |
|---|---|
| npm install 失敗 (network) | retry 3 回 + warning |
| Browser install 失敗 (disk space / permission) | hard fail + manual instruction 提示 |
| `init-agents` 失敗 (claude option not found) | Playwright version 確認 (v1.56+ 必須) |
| ユーザーが `webServer.command` を知らない | Vite / Next.js / 静的 HTML の 3 候補から選択 |

## Limitations

- **VS Code v1.105+ が前提** (Playwright agents 公式が要求)
- **OS dependent**: macOS / Linux 主、 Windows は Playwright 自体は動くが pev-harness の dog food は未確認
- **`npx playwright install` は CI 環境で別途実行が必要** (ローカル install を CI に持っていけない)

## Related

- [`pev-e2e-verify`](../pev-e2e-verify/SKILL.md) — bootstrap 完了後の test 実行
- `commands/pev-init-e2e.md` — explicit invocation
- Playwright agents 公式: <https://playwright.dev/docs/test-agents>
