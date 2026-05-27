---
name: define-technologies
description: Capture the technology choices for the project — languages, frameworks, data stores, auth, and key libraries. Stack-neutral; presents options with tradeoffs. Use when the project-builder agent is gathering technology information.
---

# Purpose

Settle the core stack before architecture and deployment so later choices line up. Stay stack-neutral: present options with tradeoffs, let the user decide.

# Questions to ask (in order)

1. Hard constraints: any language, framework, cloud, or tool the user is required to use — or forbidden from using?
2. Team familiarity: what does the user (or their team) already know well?
3. Primary runtime(s): where must the code run? (browser, server, mobile OS, desktop OS, edge, embedded)
4. Language(s) and framework(s) for each runtime. Let the user pick from the solution space.
5. Data storage needs: relational, document, key-value, search, blob, time-series, vector, graph, or none.
6. Authentication / authorization approach: none, in-app, or third-party identity provider.
7. Critical third-party services or APIs the project depends on.
8. AI / ML model dependency, if any (local, hosted, provider-specific).

Use `AskUserQuestion` for multi-choice items (storage type, auth approach).

# Solution space to present (stack-neutral, illustrative)

When the user is undecided, sketch 2–3 coherent options with tradeoffs rather than recommending one. These are examples of the *kinds* of options to offer, not a prescription:

- **Server-side languages**: TypeScript/Node, Python, Go, Rust, Java/Kotlin, C#, Ruby, Elixir, PHP.
- **Frontend**: React, Vue, Svelte, Solid, vanilla, server-rendered (Rails, Django, Phoenix, Laravel).
- **Mobile**: native (Swift / Kotlin), React Native, Flutter, Capacitor or PWA.
- **Desktop**: Electron, Tauri, native, web-only PWA.
- **Data**: PostgreSQL, MySQL, SQLite, MongoDB, Redis, DynamoDB, S3-compatible blob storage, vector DB (pgvector, Pinecone, Qdrant).
- **Auth**: roll your own (not advised for production), library (Passport, NextAuth, Devise, Spring Security), IdP (Auth0, Clerk, Keycloak, Cognito, Firebase Auth, WorkOS).

For each option the user expresses interest in, add a one-line tradeoff touching on ecosystem, performance profile, hiring pool, and operational complexity. Do not push a favorite.

# Required schema

- `constraints` (list)
- `runtimes` (list)
- `languages` (list, each mapped to a runtime)
- `frameworks` (list, each mapped to a runtime)
- `data_stores` (list of `{engine, purpose}`)
- `auth_strategy` (string)
- `external_services` (list)
- `ai_ml_dependency` (string or `"none"`)

# Output

Write to `PROJECT_BRIEF.md` under a `## Technologies` heading. Replace any prior `## Technologies` section when re-run.

# Frontmatter contribution

Update these YAML frontmatter fields (see `CLAUDE.md` for the full schema). Leave every other field untouched:

- `stack.languages` — list of language names
- `stack.frameworks` — list of framework names
- `stack.runtimes` — list of runtime targets (browser, server, mobile, desktop, edge, embedded)
- `stack.versions` — map of pinned versions (e.g., `{java: "21", gradle: "8.9", spring_boot: "3.3.2"}`). When a profile mandates "latest" for a tool, the agent must look up the current version via `WebFetch` and record it here.
- `stack.data_stores` — list of stores with purpose (e.g., `"postgres (primary)"`)
- `build.tool` — primary build tool (`gradle`, `maven`, `npm`, `pnpm`, `cargo`, `uv`, etc.)
- `build.commands` — map of common invocations (`test`, `lint`, `format`). Use the exact string the dev-team QA and developer should run (e.g., `./gradlew test`).
