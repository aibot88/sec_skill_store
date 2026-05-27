---
name: monocloud-quickstart
description: Use this skill FIRST whenever a user asks to add MonoCloud (authentication or management) to a project but hasn't said which framework. It detects the project type by reading `package.json`, `*.csproj`, `requirements.txt`, etc., then routes to the correct framework-specific MonoCloud skill (`monocloud-auth-nextjs`, `monocloud-auth-express`, `monocloud-auth-fastify`, `monocloud-management-js`, `monocloud-management-dotnet`). Also use when the user says "set up MonoCloud", "add MonoCloud login", "integrate MonoCloud", "use the MonoCloud SDK", or "manage users programmatically with MonoCloud" without naming a stack.
license: MIT
---

# MonoCloud Quickstart Router

This skill detects the project's stack and points you at the correct MonoCloud skill. **Do not try to write integration code from this skill** — load the framework-specific skill and follow its `SKILL.md`.

## Step 1 — Detect the framework

Run the bundled detector. It scans the working directory (or a path you pass) and prints the recommended skill plus its reasoning:

```bash
node scripts/detect.js              # current dir
node scripts/detect.js /path/to/app
```

The detector handles these signals:

| Signal in project | Skill to use |
|---|---|
| `"next"` in `package.json` dependencies | `monocloud-auth-nextjs` |
| `"@monocloud/auth-nextjs"` already installed | `monocloud-auth-nextjs` |
| `"@monocloud/management"` already installed | `monocloud-management-js` |
| `"fastify"` in `package.json` (no `next`) | `monocloud-auth-fastify` |
| `"express"` in `package.json` (no `next`/`fastify`) | `monocloud-auth-express` |
| `*.csproj` referencing `MonoCloud.Management` | `monocloud-management-dotnet` |
| Any `*.csproj` (no MonoCloud yet, .NET project) | `monocloud-management-dotnet` (management) — for auth on .NET, MonoCloud doesn't yet ship a dedicated agent skill; use the docs link in the project. |

If two skills could apply (e.g. an Express API in a Next.js monorepo), prefer the more specific match in the **app or package you're editing**, not the workspace root.

## Step 2 — Confirm with the user (only if ambiguous)

If detection is ambiguous (e.g. multiple `package.json` files in a monorepo, or both `"express"` and `"@monocloud/management"` declared), ask the user which app they want to wire up before proceeding.

## Step 3 — Load the framework skill

Once you know which skill to use, **stop reading this file** and switch to that skill's `SKILL.md`. The framework skill owns:

- Installation command
- Environment variables (these differ per SDK — see "Env-var families" below)
- File layout (middleware/proxy location, DI registration, etc.)
- Code patterns
- Troubleshooting

## Env-var families (for quick reference)

MonoCloud uses **prefix-namespaced** env vars per SDK. Don't mix them.

| Prefix | SDK |
|---|---|
| `MONOCLOUD_AUTH_*` | `@monocloud/auth-nextjs` (frontend / Next.js session auth) |
| `MONOCLOUD_BACKEND_*` | `@monocloud/backend-node/{express,fastify}` (API token validation) |
| `MC_MANAGEMENT_*` | `@monocloud/management` (JS Management API SDK) |
| `MonoCloud:Management:*` (config keys, not env) | `MonoCloud.Management` (.NET Management API SDK) |

## Skills catalog

- [`monocloud-auth-nextjs`](../monocloud-auth-nextjs/SKILL.md) — Sign-in/sign-up, sessions, route protection, components, hooks for Next.js (App + Pages Router).
- [`monocloud-auth-express`](../monocloud-auth-express/SKILL.md) — JWT / introspection token validation, scope + group enforcement for Express APIs.
- [`monocloud-auth-fastify`](../monocloud-auth-fastify/SKILL.md) — Same engine as above, with a Fastify `onRequest` hook.
- [`monocloud-management-js`](../monocloud-management-js/SKILL.md) — `@monocloud/management` — programmatic admin: users, clients, groups, resources, keys, logs, options, branding, trust stores.
- [`monocloud-management-dotnet`](../monocloud-management-dotnet/SKILL.md) — `MonoCloud.Management` NuGet — same surface in .NET with DI registration.

## Don't guess — verify after wiring

After the framework skill has been applied, run that skill's diagnostic:

```bash
node skills/<skill-folder>/scripts/verify.js
```

For example: `node skills/monocloud-auth-nextjs/scripts/verify.js`. The diagnostic checks env vars and that the SDK appears in `package.json`.

## Deeper reference

- [`references/concepts.md`](references/concepts.md) — tenant URL, OIDC vs Management APIs, public vs confidential clients.
