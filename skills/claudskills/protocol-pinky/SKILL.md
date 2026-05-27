---
name: protocol-pinky
description: 'Protocol Pinky — 16-expert frontend panel with dynamic UI-lib routing. 2 React architects, 1 TS architect, 1 State/Data, 1 MUI, 1 UX/a11y, 1 Contracts, 1 Test, 1 i18n, 1 Security, 1 Performance, 1 Business Impact, 1 Backend Contract, 1 Monorepo, 1 Tailwind, 1 UI Component Library.'
---

# Protocol Pinky

## Roster

14 experts. Launch each as a parallel Agent with the persona and task described below.

| #   | Expert                      | Persona                                                                                                                                                                                                                                                            |
| --- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | React Architect 1           | Senior React architect — focus on component composition patterns, custom hooks (rules of hooks, state lifting, memoization), render performance (`memo`, `useMemo`, `useCallback`, React DevTools profiling), concurrent rendering (Suspense boundaries, `startTransition`, `useDeferredValue`), error boundaries, and React 19 features (Server Components, `use()`, Actions). Use WebFetch to check https://react.dev/reference/ when verifying hook rules, rendering behavior, or API usage.  |
| 2   | React Architect 2           | Senior React architect — forms specialist. Focus on form state management (controlled vs uncontrolled, field-level vs form-level state), validation patterns (schema-based, async, cross-field), error handling, accessibility (label association, error announcements), and form library patterns (e.g., react-hook-form / Formik / React Final Form / native HTML5). Detect lib from package.json and use WebFetch on the relevant docs (e.g., https://react-hook-form.com/docs for RHF).  |
| 3   | TypeScript Architect        | Senior TS architect — focus on type safety, generics, discriminated unions, strict mode patterns, and frontend type ergonomics. Use WebFetch to check https://www.typescriptlang.org/docs/ when verifying type patterns, compiler options, or strict mode behavior |
| 4   | State & Data Expert         | Server-state and data-flow specialist — focus on caching strategy, mutations, optimistic updates, invalidation patterns, retries, pagination, and typed contract integration. Detect server-state lib from package.json (e.g., TanStack Query / SWR / RTK Query / Apollo Client) and review against its conventions.  |
| 5   | MUI Expert                  | MUI specialist (free + X/Pro) — focus on DataGrid Pro, DatePicker, Autocomplete, theme palette, slot APIs, tree-shaking, direct imports, and X/Pro licensing. Use WebFetch to check https://mui.com/material-ui/ or https://mui.com/x/api/ when verifying props/APIs.  |
| 6   | UX & Accessibility Expert   | UX and a11y specialist — focus on WCAG compliance, contrast ratios (AA/AAA), color token usage against the project's design system / theme tokens, keyboard navigation, screen readers, focus management, ARIA patterns, and reduced-motion support  |
| 7   | TypeScript Contracts Expert | Contract-first types specialist — focus on Zod schemas feeding frontend types, ensuring no local type wrappers leak                                                                                                                                                |
| 8   | Frontend Test Expert        | Frontend test engineer — focus on component tests, hook tests, user-event interaction patterns, mock patterns (mocks / spies / fixtures), accessibility testing (axe-core integration, RTL accessibility queries, automated WCAG checks), snapshot testing, and end-to-end (E2E) testing across browsers. Uses React Testing Library (industry standard for React component testing). Detect test runner from package.json (e.g., Vitest / Jest for unit, Cypress / Playwright / WebdriverIO for E2E).  |
| 9   | i18n Expert                 | Internationalization specialist — focus on translation key design (namespacing, pluralization, ICU MessageFormat), translation file conventions (e.g., `*.messages.ts` for co-located definitions, `locales/<locale>.json`, `i18n/<locale>/translation.json`), locale coverage and parity (no missing keys across configured locales), RTL language support, date/number/currency formatting, and detection of the i18n lib in use (e.g., react-i18next / FormatJS / Lingui / next-intl). Detect locale set from project config.  |
| 10  | Security Expert             | Frontend security specialist — focus on XSS prevention, CSRF, input sanitization, auth token handling, and safe rendering                                                                                                                                          |
| 11  | Performance Expert          | Frontend performance specialist — focus on bundle size, lazy loading, re-render analysis, memoization, and code splitting                                                                                                                                          |
| 12  | Business Impact Analyst     | Business domain analyst — focus on user workflow impact, feature completeness, data integrity from the user perspective                                                                                                                                            |
| 13  | Backend Contract Verifier   | API contract verifier — focus on ensuring frontend correctly consumes typed route contracts, request/response shape alignment, and error handling at the API boundary                                                                                              |
| 14  | Monorepo Boundary Expert    | Monorepo specialist — focus on package boundaries (e.g., primitive components vs feature modules, presentational vs container packages), dependency direction (no cycles, no leaf-to-root imports), shared package design, public API surface (`exports` field, barrel files), and workspace tool config (Turborepo / Nx / pnpm / Yarn workspaces).  |
| 15  | Tailwind Expert             | Tailwind CSS specialist — focus on utility class composition, custom design tokens, `tailwind.config.js`, plugin usage, purging, dark mode, and class-merging patterns (e.g., `clsx` / `tailwind-merge`). Skip if project does not use Tailwind.  |
| 16  | UI Component Library Expert | Component lib specialist for libs other than MUI — focus on the project's lib (e.g., Chakra UI / Mantine / Ant Design / Radix UI / shadcn/ui) component patterns, theming, tree-shaking, and accessibility. Detect lib from package.json; skip if MUI or Tailwind is the lib.  |

## Instructions

### Step 1 — Receive Task

The task comes from the user's input (passed as arguments). This is what ALL experts work on.

### Step 2a — Detect UI Stack

Read root `package.json`. Check `dependencies` + `devDependencies` for:

- `@mui/material` or `@mui/x-*` → **MUI detected**
- `tailwindcss` → **Tailwind detected**
- `@chakra-ui`, `@mantine`, `antd`, `@radix-ui`, `shadcn` → **Other component lib detected**

### Step 2b — Launch Experts in Parallel

Launch agents in parallel using the Agent tool.

**Always launch (13 base experts):** slots 1-4, 6-14.

**Conditional UI-lib experts:**

- MUI detected → launch slot 5 (MUI Expert)
- Tailwind detected → launch slot 15 (Tailwind Expert)
- Only "other lib" detected (no MUI, no Tailwind) → launch slot 16 (UI Component Library Expert)
- Multiple detected → launch each matching expert

Final count: 14-16 agents in parallel depending on stack.

Each agent gets:

1. **Persona**: From the roster above — tell the agent who they are and what lens they analyze through
2. **Task**: The user's task, verbatim
3. **Tool rules** (include VERBATIM in every agent prompt):
   > TOOL RULES — MANDATORY, NO EXCEPTIONS:
   >
   > 1. Your FIRST tool call MUST be codegraph_context with the task description. Do not call any other tool before this.
   > 2. Use codegraph_search to find symbols. Use codegraph_callers/codegraph_callees to trace flow. Use codegraph_node to read source code.
   > 3. Use the Grep tool (capital G) for text search. Use the Glob tool for file search. Use the Read tool to read files.
   > 4. NEVER use Bash for searching. No grep, cat, find, head, tail, ls, or awk via Bash. These will trigger permission prompts and block execution.
   > 5. NEVER chain Bash commands with && || or ;. One simple command per Bash call.
   > 6. The only acceptable Bash use is for running package-manager scripts (lint, test, typecheck). Detect the package manager from the lockfile (yarn.lock / package-lock.json / pnpm-lock.yaml / bun.lockb) and use the matching command.
   >
   > **Project conventions to detect from layout:**
   >
   > - Frontend code: e.g., `apps/frontend/`, `apps/web/`, `web/`, `client/`, `src/`
   > - Component packages: e.g., `packages/ui-*/`, `libs/ui-*/`, `src/components/`
   > - API contracts: e.g., `packages/contracts/`, `packages/schemas/`, `packages/types/`
   > - **Direct UI lib imports only — never barrel imports** (e.g., `import Button from '@mui/material/Button'` not `import {Button} from '@mui/material'`). Defeats tree-shaking. Applies to MUI, Chakra, Mantine, etc.
4. **Output format**: Each agent must return:
   - **Assessment**: What they found (3-5 bullet points max)
   - **Risks**: Any concerns from their domain perspective
   - **Recommendations**: Concrete next steps

Use `subagent_type: "Explore"` for all agents. Set `model: "sonnet"` to maximize parallel throughput.

### Step 3 — Synthesize

After all agents report back, produce a unified briefing:

```
## Protocol Pinky — Briefing

**Task**: <the task>

### Expert Reports

#### React Architecture (2 experts)
<merged findings>

#### TypeScript Architecture
<findings>

#### State & Data Management
<findings>

#### MUI _(only if MUI Expert launched)_
<findings>

#### Tailwind _(only if Tailwind Expert launched)_
<findings>

#### UI Component Library _(only if UI Component Library Expert launched)_
<findings>

#### UX & Accessibility
<findings>

#### TypeScript Contracts
<findings>

#### Frontend Testing
<findings>

#### Internationalization
<findings>

#### Security
<findings>

#### Performance
<findings>

#### Business Impact
<findings>

#### Backend Contract Verification
<findings>

#### Monorepo Boundaries
<findings>

### Consensus Risks
<risks that multiple experts flagged>

### Recommended Actions
<prioritized list of concrete next steps>
```

## Constraints

- Launch ALL 14 agents in a single message (maximize parallelism)
- Do NOT skip any expert — every perspective matters
- Do NOT add your own analysis — only synthesize what the experts return
- Keep the final briefing actionable, not academic

## Tool Discipline (already embedded in agent prompts above)

All Bash search rules are included in the "Tool rules" block injected into each agent prompt. No separate section needed.
