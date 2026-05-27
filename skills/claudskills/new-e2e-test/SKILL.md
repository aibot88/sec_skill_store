---
name: new-e2e-test
description: Scaffold a Playwright E2E test in one of the apps that has a Playwright config, matching the existing test fixtures and auth patterns
disable-model-invocation: true
---

# /new-e2e-test — add a Playwright E2E spec

Scaffolds a new `*.spec.ts` under `apps/<app>/e2e/` matching the house pattern.

## Apps with Playwright configured

- `apps/hospitality` (auth-gated via `authPage` fixture)
- `apps/gen`
- `apps/marketing`
- `apps/rialto-web`

## Gather context

Ask (or infer from user's task):

1. **Which app?** One of the four above.
2. **What flow?** One sentence — becomes the test description and file name suffix.
3. **Auth required?** Default yes for hospitality; no for marketing/rialto-web/gen public pages. Auth uses the Resource Owner Password Grant pattern (programmatic Auth0 login via env vars) — never manual browser login.
4. **Route to exercise.** Full path relative to the app's base URL.

## Template — authenticated hospitality test

```typescript
import { test, expect } from "./fixtures.js";

test.describe("<flow name>", () => {
  test("<specific assertion>", async ({ authPage }) => {
    await authPage.goto("/<route>");

    // Assertion 1 — page shell loads
    await expect(authPage.getByTestId("dashboard-layout")).toBeVisible();

    // Assertion 2 — feature-specific
    // Use getByRole, getByLabel, getByTestId — never CSS selectors
    await expect(authPage.getByRole("heading", { name: "<expected>" })).toBeVisible();

    // Interaction (if any)
    await authPage.getByRole("button", { name: "<action>" }).click();

    // Post-interaction assertion
    await expect(authPage.getByText("<expected state>")).toBeVisible();
  });
});
```

## Template — unauthenticated / marketing / public

```typescript
import { test, expect } from "@playwright/test";

test.describe("<page or flow>", () => {
  test("<assertion>", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });
});
```

## Rules

- **Use `fixtures.js` import for hospitality auth tests.** Bare `@playwright/test` bypasses the Auth0 login fixture.
- **Prefer role-based locators (`getByRole`, `getByLabel`) over CSS selectors.** If an element isn't role-queryable, add `data-testid` to the component rather than a CSS class lookup — it survives refactors.
- **Auth tests rely on `E2E_AUTH*` env vars.** Document the test plan but the test runner skips auth tests if the vars aren't set (see `fixtures.ts` for the skip logic).
- **Never use `page.waitForTimeout()`** — wait for concrete signals (visible text, network response, URL change) instead. Fixed waits cause flake.
- **One assertion per `test()` block when practical.** If a single flow has 5 steps, consider 5 tests named `"step 1: …", "step 2: …"` — the CI output is far more useful when a flake happens.

## After scaffolding

Run the test locally to confirm it passes (or at least runs):

```bash
cd apps/<app>
pnpm test:e2e          # full suite
pnpm test:e2e <file>   # one file
```

Auth-gated tests need `E2E_AUTH*` env vars set (see the app's `.env.example`). Without them, the test skips rather than fails.

## After the first green run

- Add the spec path to `docs/E2E-TEST-PLAN.md` if the app maintains one (hospitality does)
- For visual tests (Rialto), use `apps/rialto-web/playwright.config.ts` — it runs screenshot comparisons not behavioral checks
