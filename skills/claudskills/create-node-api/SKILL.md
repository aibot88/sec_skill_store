---
name: create-node-api
description: Scaffold a production-ready Node.js API — choose Express TypeScript or NestJS, then select database, auth, and extras.
---

# Create Node API

You are a Node.js API scaffolding assistant. Your job is to create a production-ready Node.js API and guide the user through selecting integrations.

## Reference Files Location

- Express: `~/.claude/project-scaffolding/reference/node/express-api.md`
- NestJS:  `~/.claude/project-scaffolding/reference/node/nestjs-api.md`

---

## Step 0 — Detect Environment

**Before asking anything**, check whether you are inside a Turborepo monorepo:

1. Look for `turbo.json` in the current directory or up to 3 parent directories
2. Also check for `package.json` with a `"workspaces"` field and an `apps/` directory

**If a monorepo is detected:**

Read the root `package.json` to get the monorepo name. List any existing apps in `apps/`.

Then ask:

> "You're inside the `<monorepo-name>` monorepo.
> Where do you want to create this API?
> A) Add as a new app in this monorepo (creates in `apps/<name>`)
> B) Create as a standalone API (creates in the current directory)"

**If no monorepo is detected:** Skip and proceed to Step 1.

**Store as `CONTEXT: monorepo | standalone`** — affects Steps 2, 7, and the final commit.

---

## Step 1 — Framework

Ask:

> "Which Node.js framework do you want?
> A) Express (TypeScript) — lightweight, full control, minimal opinions
> B) NestJS (TypeScript) — opinionated, decorators, Angular-like DI, great for large teams"

---

## Step 2 — Project Name

Ask:

> "What should the project be named? (kebab-case, e.g. `my-api`)"

---

## Step 3 — Database

Ask:

> "Which database setup do you need?
> A) PostgreSQL + Prisma (recommended — great DX, migrations, type safety)
> B) PostgreSQL + Drizzle (lighter — better for serverless/edge)
> C) MongoDB + Mongoose (document database)
> D) No database (pure API / proxy)"

---

## Step 4 — Auth

Ask:

> "Do you need authentication?
> A) JWT auth (access + refresh tokens, argon2 hashing)
> B) API key auth (simple header-based)
> C) No auth"

---

## Step 5 — Extras

Ask (user can select multiple, or none):

> "Which extras do you want? (comma-separated, e.g. `1,3` or `none`)
> 1) BullMQ job queues (Redis-backed background jobs)
> 2) Swagger / OpenAPI docs
> 3) File uploads (multer)
> 4) WebSockets
> 5) None"

---

## Step 6 — Read Reference File

Based on the framework chosen in Step 1, read the relevant reference file now:

- **Express** → `~/.claude/project-scaffolding/reference/node/express-api.md`
- **NestJS**  → `~/.claude/project-scaffolding/reference/node/nestjs-api.md`

Follow it exactly to scaffold the project.

---

## Step 7 — Scaffold the Project

### If CONTEXT = monorepo:

Navigate to `apps/` at the monorepo root first:
```bash
cd <monorepo-root>/apps
```
Create the project there. After creation, run `yarn install` from the **monorepo root** (not inside the app). Use the monorepo root's existing git repo — **do NOT run `git init`**.

### If CONTEXT = standalone:

Create in the current directory. Run `git init` as part of the final commit step.

---

### If Express (follow express-api.md):

1. Create project directory and `cd` into it
2. Initialize `package.json` (yarn)
3. Install core dependencies
4. Create `tsconfig.json`, `tsup.config.ts`
5. Create `src/config/env.ts` — Zod env validation (fails fast at startup)
6. Create `src/config/logger.ts` — Pino logger
7. Create `src/middleware/` — error handler, request logger
8. Create `src/modules/health/` — health + readiness endpoints
9. Create `src/app.ts` + `src/server.ts` — app/server split (no port in app.ts)
10. Add database, auth, extras based on selections
11. Create `Dockerfile` (multi-stage), `docker-compose.yml` (full stack), `docker-compose.dev.yml` (databases only), `.dockerignore`, `.env.example`, `.gitignore`
12. Run `yarn install` then `yarn build` to verify compilation
13. **If standalone:** `git init && git add . && git commit -m "chore: init express api"`
    **If monorepo:** `cd <monorepo-root> && git add apps/<name> && git commit -m "feat: add <name> express api to monorepo"`

### If NestJS (follow nestjs-api.md):

1. Run `nest new <project-name> --strict --package-manager=npm`
2. Install selected integrations (config, validation, JWT, Swagger, etc.)
3. Set up `src/config/` — Zod env validation via `ConfigModule.forRoot({ validate })`
4. Set up `src/common/` — global filter, interceptor, guard, pipes
5. Update `src/main.ts` — Helmet, CORS, `ValidationPipe`, `enableShutdownHooks`, Swagger
6. Create `src/modules/health/` with `@nestjs/terminus`
7. Add database module based on selection
8. Add auth module if selected
9. Add extras (BullMQ, file uploads, WebSockets) based on selections
10. Create `Dockerfile` (multi-stage, non-root user), `docker-compose.yml` (full stack), `docker-compose.dev.yml` (databases only), `.dockerignore`, `.env.example`
11. Run `npm run build` to verify compilation
12. **If standalone:** `git add . && git commit -m "chore: init nestjs api"`
    **If monorepo:** `cd <monorepo-root> && git add apps/<name> && git commit -m "feat: add <name> nestjs api to monorepo"`

---

## Step 8 — Final Summary

### Express summary:

```
✓ Project: <name>/

Structure:
  src/
    config/       — env validation (Zod), logger (Pino)
    middleware/   — error handler, auth, request logging
    modules/      — feature modules (health[, auth, ...])
    app.ts        — Express setup (testable, no port binding)
    server.ts     — port binding + graceful shutdown

Commands:
  yarn dev        — start with hot reload (tsx watch)
  yarn build      — compile to dist/ (tsup)
  yarn start      — run compiled dist/server.js
  yarn test       — run tests (Vitest)

[If Docker compose]:
  npm run docker:dev    — start databases only (for local dev)
  npm run docker:up     — start full stack in Docker (API + databases)
  npm run docker:down   — stop all containers
  npm run docker:logs   — tail API logs

Health endpoints:
  GET /healthz    — liveness
  GET /readyz     — readiness (checks DB + Redis)

Working endpoints after scaffold:
  POST /api/v1/auth/register  — create account
  POST /api/v1/auth/login     — get JWT token
  GET  /api/v1/auth/me        — current user (protected)
  GET  /api/v1/users          — list users (protected)
  GET  /api/v1/users/:id      — get user (protected)
  PATCH /api/v1/users/:id     — update user (protected)
  DELETE /api/v1/users/:id    — delete user (protected)

Quick test:
  docker compose up -d && npx prisma migrate dev --name init && yarn dev

Add a new module:
  src/modules/<feature>/controller.ts|service.ts|routes.ts|schema.ts
  Register in src/app.ts
```

### NestJS summary:

```
✓ Project: <name>/

Structure:
  src/
    config/       — env validation (Zod via ConfigModule), app config
    common/       — filters, interceptors, guards, decorators
    modules/      — feature modules (health[, auth, ...])
    app.module.ts — root module
    main.ts       — bootstrap with global middleware + Swagger

Commands:
  npm run start:dev   — start with hot reload
  npm run build       — compile
  npm run start:prod  — run compiled code
  npm run test        — unit tests (Jest)
  npm run test:e2e    — end-to-end tests

[If Swagger enabled]:
  http://localhost:3000/api/docs — interactive API docs

[If Docker compose]:
  npm run docker:dev    — start databases only (for local dev)
  npm run docker:up     — start full stack in Docker (API + databases)
  npm run docker:down   — stop all containers
  npm run docker:logs   — tail API logs

Working endpoints after scaffold:
  POST /api/v1/auth/register  — create account
  POST /api/v1/auth/login     — get JWT token
  GET  /api/v1/auth/me        — current user (protected)
  GET  /api/v1/users          — list users (protected)
  PATCH /api/v1/users/:id     — update user (protected)
  DELETE /api/v1/users/:id    — delete user (protected)
  GET  /api/v1/health         — health + DB check

Swagger UI: http://localhost:3000/api/docs

Quick test:
  docker compose up -d && npx prisma migrate dev --name init && npm run start:dev

Add a new module:
  nest generate module modules/<feature>
  nest generate controller modules/<feature>
  nest generate service modules/<feature>
  Register in app.module.ts imports
```

---

## Step 9 — Offer to Start the Server

After printing the summary, ask:

> "Want me to start the dev server now?
> A) Yes — start it now (runs in the background, output will appear here)
> B) No — I'll run it myself
>
> Note: If you chose a database, make sure to run `yarn docker:dev` (or `npm run docker:dev`) and `npx prisma migrate dev --name init` first."

**If A — start it now:**

Run the correct dev command **in the background** using the Bash tool with `run_in_background: true`:

- Express: `cd <project-dir> && yarn dev`
- NestJS: `cd <project-dir> && npm run start:dev`

After launching, tell the user:

> "Dev server started in the background.
> API running at: http://localhost:3000
> [If Swagger] Swagger docs: http://localhost:3000/api/docs
> Output will appear here when the server is ready.
>
> If you have a database selected, make sure Docker is running first:
>   yarn docker:dev   (starts DB containers)
>   npx prisma migrate dev --name init"

**If B — user runs it themselves:**

Show the exact commands:

> "Run these in your terminal:
> ```
> cd <project-name>
> yarn docker:dev                        # start database (Docker)
> npx prisma migrate dev --name init     # run migrations (if Prisma)
> yarn dev                               # Express
> # or
> npm run start:dev                      # NestJS
> ```"

---

## Step 10 — Generate CLAUDE.md

After the dev server question is resolved, **always** generate `CLAUDE.md` without asking.

Follow the complete `generate-claude-md` skill from Step 1 through Step 6:
- Framework is already known (Express or NestJS)
- Stack profile is already known from this flow — skip re-detection
- Write `CLAUDE.md` to the project root, commit it

Tell the user after generating:

> "Generated `CLAUDE.md` — Claude will read this automatically at the start of every future session in this project. No need to explain the stack again."

---

## Rules

### Express rules:
- Always split `app.ts` (Express config) from `server.ts` (port + graceful shutdown)
- Use `tsx watch` for dev, `tsup` for production build — NOT `ts-node`
- Validate env with Zod in `src/config/env.ts` — fail fast at startup
- Use Pino for logging, NOT console.log or Winston
- Feature/module-based structure — one folder per domain in `src/modules/`
- Use argon2 for password hashing, NOT bcrypt
- Express v5 propagates async errors automatically

### NestJS rules:
- NestJS v11 requires Node.js >= 20
- Always use `APP_GUARD`, `APP_FILTER`, `APP_INTERCEPTOR`, `APP_PIPE` tokens for DI-aware global registration — not `useGlobalX()` in `main.ts` when you need injection
- Use `ValidationPipe` globally with `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true`
- Use `nestjs-pino` for logging, not the built-in Logger (in production)
- Use `@nestjs/config` + Zod validate function for env validation
- TypeORM is legacy — prefer Prisma or Drizzle for new projects
- Use `@nestjs/bullmq` (NOT `@nestjs/bull` — Bull v3 is deprecated)
- Call `app.enableShutdownHooks()` before `app.listen()` for Kubernetes-safe graceful shutdown
- Enable Swagger CLI plugin in `nest-cli.json` to eliminate `@ApiProperty` boilerplate
- Use argon2 for password hashing, NOT bcrypt
