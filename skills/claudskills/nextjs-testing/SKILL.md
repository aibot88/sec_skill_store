---
name: nextjs-testing
description: >
  This skill should be used when writing or setting up tests for a Next.js application.
  Trigger when: configuring Vitest, Cypress, or Playwright for Next.js; writing unit tests
  for components or hooks; writing E2E tests; testing React Server Components; testing API
  routes or Route Handlers; testing Server Actions; setting up test infrastructure;
  choosing between testing tools; implementing data-testid attributes; testing authentication
  flows; mocking API responses with cy.intercept() or page.route();
  troubleshooting test failures; testing with production builds; or asking about Next.js
  testing best practices, patterns, or anti-patterns.
---

# Next.js Testing: Standards & Patterns

Next.js blurs the line between frontend and backend. Relying on unit tests alone is insufficient — E2E tests are essential for catching bugs at the client/server intersection.

## Core Principle

> **Test the boundary**: The most dangerous bugs in Next.js hide where Server Components meet Client Components, where cached data meets fresh data, and where middleware meets Route Handlers. Prioritize E2E tests that exercise these intersections.

---

## 1. Tool Selection

| Tool | Use For | Strengths |
|------|---------|-----------|
| **Vitest** | Unit/component tests — functions, hooks, simple Client Components | Fast, Jest-compatible, native ESM |
| **Cypress** | E2E — complex client-side state, time-travel debugging | `cy.intercept()`, `window` access, visual debugging |
| **Playwright** | E2E — speed, parallelization, cross-browser, multi-tab | Native parallel execution, heavily server-rendered apps |

### Decision Guide
- **Heavily interactive SPA-like pages** → Cypress (better debugging of client state)
- **Heavily server-rendered, multi-tab, or cross-browser** → Playwright (faster, parallel)
- **Both are excellent choices** — pick based on team preference

---

## 2. E2E Setup Patterns

### Always Test Against Production Builds

Next.js behaves differently in dev vs. production (caching, static generation, hydration). Always run E2E tests against `npm run build && npm run start`. This catches build-time errors, missing env vars, hydration mismatches, and caching issues invisible in dev mode.

### Automated Server Startup

Use `start-server-and-test` (Cypress) or the built-in `webServer` config (Playwright) to automatically start, wait for, and tear down the server. See `references/testing-setup-patterns.md` for complete configuration templates.

### Key Setup Rules

- Configure a global `baseUrl` (`http://localhost:3000`) — use relative paths in all tests.
- Never start the server using `cy.exec()` or `cy.task()` — causes port conflicts and strips log access.

---

## 3. Testing React Server Components

### E2E Over Component Tests for RSCs

Async Server Components are not fully supported by component testing tools. **Use E2E tests** (Cypress or Playwright) to validate RSC behavior.

### Test the Output, Not the Execution

E2E runners cannot access server-side code. Test the **rendered HTML DOM**, not how the component fetches data internally.

### Handle Suspense Naturally

For streaming RSCs wrapped in `<Suspense>`, rely on the test runner's automatic retry:
- Assert the loading skeleton appears
- Assert the final content replaces it

---

## 4. Testing API Routes & Route Handlers

### Direct HTTP Testing

Test endpoints directly with `cy.request()` or Playwright's `request` API. Faster and more isolated than clicking through UI.

### API Mocking for UI Tests

Use `cy.intercept()` (Cypress) or `page.route()` (Playwright) to mock API responses during UI tests. Enables testing edge cases (500 errors, empty states, slow responses) reliably.

---

## 5. Writing Resilient Tests

### Use `data-testid` Attributes

Never target elements by CSS classes, IDs, or tag names — they are brittle and tied to styling. Use dedicated test attributes:

```tsx
<button data-testid="submit-order">Place Order</button>
```

```typescript
// Cypress
cy.get('[data-testid="submit-order"]').click();

// Playwright
page.getByTestId('submit-order').click();
```

### Clean State Before Tests

Clean up state in `before` or `beforeEach`, not `afterEach`. If a test fails mid-execution, `afterEach` won't run, leaving dangling state that breaks subsequent tests. Every test must pass independently with `.only`.

### Anti-Pattern: Arbitrary Waits

Never use `cy.wait(5000)`. Instead:
- Alias API routes and wait for the network response
- Assert a specific DOM element has appeared
- Use Playwright's auto-waiting assertions

---

## 6. Authentication Testing

### Programmatic Login

Never type credentials via UI for every test. Use programmatic authentication:
- **Cypress:** `cy.session()` caches cookies and `localStorage` across tests.
- **Playwright:** `storageState` persists and reuses auth state across specs.

See `references/testing-setup-patterns.md` for complete auth setup templates for both frameworks.

### Anti-Pattern: Testing Third-Party OAuth via UI

Never navigate to Google, GitHub, or Auth0 login screens in tests. These providers detect automation and block with CAPTCHAs. Mock the OAuth callback or use a test provider instead.

---

## 7. CI/CD Integration

- Block merges until E2E tests pass on a **production build**.
- Run tests in parallel (Playwright natively; Cypress with `cypress-parallel` or Cypress Cloud).
- Use headless browsers in CI (`--headless` flag).
- Store test artifacts (screenshots, videos) on failure for debugging.

---

## Additional Resources

### Reference Files

For complete configuration examples and setup templates:
- **`references/testing-setup-patterns.md`** — Vitest, Cypress, and Playwright configuration templates for Next.js with working examples

### Related Skills

- **`nextjs-security`** — What to test for security (auth flows, CSRF, input validation)
- **`nextjs-troubleshooting`** — Debugging test failures, hydration mismatches
- **`nextjs-best-practices`** — Architecture patterns that affect testability
