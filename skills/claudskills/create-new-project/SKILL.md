---
name: create-new-project
description: "Scaffold a complete production-ready project with a single command. Asks key questions (project name, SaaS?, modules), then creates the full stack: .NET API (Vertical Slice + Clean Arch), Docker Compose, PostgreSQL, RabbitMQ, Redis, Elasticsearch, logging pipeline, email pipeline, auth, and optionally Flutter/React apps."
argument-hint: "[project-name]"
---

# /create-new-project Skill

## Purpose

Creates a complete, production-ready project skeleton from scratch. In 5 minutes, you get the same mature infrastructure that would take weeks to build manually. Every project follows the same architecture (Vertical Slice + Clean Architecture + Mediator) and includes battle-tested patterns for logging, email, auth, caching, and more.

## Flow

### Phase 1 — Gather Information

Ask the user the following questions using AskUserQuestion. Each question should have clear options. If a project name is provided as an argument, skip question 1.

#### Question 1: Project Name
```
What is the project name?
```
Free text. Must be PascalCase (e.g., ExampleApp, MarketPlace, ShopHub).
Derive abbreviation for Docker container prefix (e.g., ExampleApp → ea, MarketPlace → mp).

#### Question 2: Applications
```
Which applications does this project need?
```
Options (multiSelect: true):
- Flutter mobile app (iOS + Android)
- React web app (admin panel / dashboard)
- React public website (SSR with Next.js)

At least one must be selected.

#### Question 3: SaaS
```
Is this a SaaS project (multi-tenant)?
```
Options:
- No — single tenant, simple User entity only
- Yes — User + Profile + Tenant model

#### Question 3a (if SaaS = Yes): Tenant Entity Name
```
What is the tenant entity name?
```
Options:
- Dealer
- Company
- Organization
- Seller
- Other (custom name)

#### Question 3b (if SaaS = Yes): Multi-Profile
```
Can a user belong to multiple tenants?
```
Options:
- Yes — user can have profiles in different tenants (e.g., customer at multiple dealers)
- No — one user, one tenant

#### Question 3c (if SaaS = Yes): Embed Auth
```
Do tenants need to embed your app (iframe/SDK auto-login)?
```
Options:
- Yes — embed auth flow (tenant-scoped auto-login, auto-create user/profile)
- No — standard login only

#### Question 4: Additional Modules
```
Which additional modules should be included?
```
Options (multiSelect: true):
- File Storage (MinIO/S3)
- Audit Trail (change history tracking)
- Soft Delete (default: included, ask only to confirm)
- Spatial/GIS support (maps, location, polygons — switches DB to PostGIS and seeds the extension)
- Claude Design integration (visual prototyping via `/design-screen` skill — requires Claude Pro/Max/Team/Enterprise subscription)

Note: Logging pipeline, email pipeline, Redis, RabbitMQ, JWT auth, health checks are ALWAYS included — they're core infrastructure, not optional.

#### Question 5: Port Offset
```
Do you have other projects running on this machine?
```
Options:
- No — use default ports (3000, 5432, 6379, etc.)
- Yes — apply port offset (+10000) to avoid conflicts

#### Question 6: Team (if no team installed)
Check if `.claude/.team-installs.json` exists. If not, ask:

```
Which team should be installed for this project?
```

**Auto-detection:** Check `~/.claude/repos/agentteamland/` for directories containing `team.json` with agents. List them as options.

If no cached teams found, ask for a git repo URL:
```
Enter the team repo URL (e.g., https://github.com/agentteamland/software-project-team.git)
```

If `--team <url>` was passed as argument, use that directly without asking.

**Install the team:** Run `/team install <url>` which clones to `~/.claude/repos/agentteamland/` and symlinks agents/skills/rules into the project's `.claude/`.

### Phase 2 — Create Project Structure

Based on answers, create the complete project. Use the software-project-team agents' knowledge as reference.

#### 2.1 Root Files

Create in the specified project directory:

```
{ProjectName}/
├── {ProjectName}.sln                    ← Solution file at root
├── docker-compose.yml                   ← All services
├── .env                                 ← Environment config (gitignored)
├── .env.example                         ← Template (committed)
├── .gitignore                           ← .NET + Docker + IDE
├── .dockerignore                        ← Docker build exclusions
├── CLAUDE.md                            ← Project summary (filled with tech stack info)
└── README.md                            ← Project description
```

#### 2.2 .NET Projects (Always Created)

```
src/
├── {ProjectName}.Domain/                ← Pure C#, BaseEntity, IAuditableEntity, IAggregateRoot, ISoftDeletable
├── {ProjectName}.Application/           ← Mediator, FluentValidation, Behaviors, Interfaces, Exceptions
├── {ProjectName}.Infrastructure/        ← EF Core, JWT, BCrypt, Redis, RMQ, Email sender
├── {ProjectName}.Logging/               ← Shared: RmqLogSink, LogChannelQueue, LogPublisherHostedService
├── {ProjectName}.Api/                   ← Composition root, Minimal API endpoints, Dockerfile.dev
├── {ProjectName}.Socket/                ← SignalR bridge, IApiClient, Dockerfile.dev
├── {ProjectName}.Worker/                ← BackgroundService + Cronos, Dockerfile.dev
├── {ProjectName}.LogIngest/             ← Log consumer (RMQ → Elasticsearch), Dockerfile.dev
└── {ProjectName}.MailSender/            ← Email consumer (RMQ → SMTP), Dockerfile.dev
```

**Key patterns to include:**
- martinothamar/Mediator (source generator, NOT MediatR)
- Pipeline behaviors: Logging → UnhandledException → Validation → Performance → Idempotency → Caching
- IApplicationDbContext interface in Application
- ApplicationDbContext in Infrastructure with AuditableEntityInterceptor
- JWT auth (HS256, 15min access, 30day refresh in Redis)
- X-Internal-Token for system-to-system (Worker→API, API→Socket)
- RMQ connection + topology (logs.fanout, emails.fanout)
- Health endpoints (/api/health/ping)
- Global exception handler (NotFoundException→404, ValidationException→422, ForbiddenException→403)
- Swagger with Bearer token support
- Auto-migrate in Development
- seed.sql file with admin test user

**Cold-build csproj requirements (mandatory — verified failure modes):**

These four package/framework references are **required for cold build to succeed**. Their omission is the most common cause of verify-system stalling on a fresh scaffold. See [api-agent/children/known-issues.md](../../agents/api-agent/children/known-issues.md) for the discovery context, [api-agent/children/architecture-layers.md](../../agents/api-agent/children/architecture-layers.md) for the canonical csproj package sets.

1. **`Infrastructure.csproj`** — must include `<FrameworkReference Include="Microsoft.AspNetCore.App" />` because `Auth/CurrentUser.cs` uses `IHttpContextAccessor` (from `Microsoft.AspNetCore.Http`).
2. **`Api.csproj`** — must include `Microsoft.EntityFrameworkCore.Design` package (with `PrivateAssets`). EF Core's tooling requires it on the **startup project** running `dotnet ef`, not just on `Infrastructure`.
3. **`Worker.csproj`, `LogIngest.csproj`, `MailSender.csproj`** — each must include `<PackageReference Include="Microsoft.Extensions.Hosting" Version="9.*" />`. .NET 9's `Microsoft.NET.Sdk.Worker` SDK does NOT transitively expose the `Host` static class; cold build fails with `CS0103: 'Host' does not exist`.
4. **Initial EF migration** — generate it as the **last step of Phase 2** (subsection 2.8 below) before `docker compose up -d`.

**If SaaS = Yes, additionally include:**
- User entity (email, passwordHash, firstName, lastName)
- Profile entity (userId, tenantId, role, isActive)
- Tenant entity (name, code, status) with configured tenant name
- ITenantEntity interface + global query filter + TenantInterceptor
- ITenantContext (from JWT claims)
- Embed auth endpoint (if selected)
- Auth endpoints: login, register, refresh, select-profile, logout

**If SaaS = No:**
- User entity only (simple, no Profile/Tenant)
- Auth endpoints: login, register, refresh, logout

**If Soft Delete = Yes (default):**
- ISoftDeletable interface (IsDeleted, DeletedAt, DeletedBy)
- Global query filter for soft delete
- SaveChanges interceptor to convert Delete → Modified

**If Audit Trail = Yes (default):**
- AuditLog entity
- Change tracking in SaveChanges (entity, field, old value, new value, who, when)

**If File Storage = Yes:**
- IStorageService in Application
- S3StorageService in Infrastructure
- MinIO service in Docker Compose

#### 2.3 Docker Compose Services

**Always included (core infrastructure):**
- db — healthcheck, persistent volume. Image depends on Q4 Spatial/GIS answer:
  - **No** (default): `postgres:17-alpine`
  - **Yes**: `imresamu/postgis:17-3.5-alpine` — multiarch (Apple Silicon compatible). Official `postgis/postgis` image does not publish an ARM64 manifest as of 2026; `imresamu/postgis` is maintained by PostGIS maintainer Imre Samu and is the recommended drop-in. When using this image, the first migration must run `CREATE EXTENSION IF NOT EXISTS postgis;` (see database-agent migration-management). Note: PostGIS image is ~5× larger than vanilla postgres — don't pull it for projects that don't need spatial.
- rabbitmq (rabbitmq:3-management-alpine) — healthcheck
- redis (redis:7-alpine) — healthcheck
- elasticsearch (elasticsearch:8.15.0) — single-node, security disabled, JVM 512m
- kibana (kibana:8.15.0) — connected to elasticsearch
- mailpit (axllent/mailpit) — dev SMTP + Web UI
- db-ui (adminer) — DB management
- redis-ui (rediscommander/redis-commander)
- api — .NET SDK, dotnet watch, depends on db+rabbitmq+redis healthy
- socket — .NET SDK, dotnet watch
- worker — .NET SDK, dotnet watch
- log-ingest — .NET SDK, dotnet watch, depends on rabbitmq+elasticsearch healthy
- mail-sender — .NET SDK, dotnet watch, depends on rabbitmq+redis healthy

**If File Storage = Yes:**
- minio (minio/minio) — S3-compatible, console UI

**If Flutter = Yes:**
- (Flutter runs natively, not in Docker — note in README)

**If React = Yes:**
- app (node, vite dev server or next dev)

**Dev Dockerfile pattern for all .NET services:**
- SDK:9.0 image
- Copy all .csproj files for restore (layer cache)
- dotnet restore
- ENTRYPOINT dotnet watch run
- Source mounted as volume (not copied)
- Shadow volumes for bin/obj
- Per-service NuGet cache volume

#### 2.4 Flutter App (if selected)

Create Flutter project with the framework's standard structure:
```
flutter/
├── lib/
│   ├── main.dart
│   ├── app/ (MaterialApp, router, theme)
│   ├── core/ (responsive, providers, extensions, constants)
│   ├── data/ (models, repositories, sources/mock + remote)
│   ├── features/ (feature-first screens)
│   └── l10n/ (ARB files — only if i18n is wired, see cleanup below)
├── pubspec.yaml (riverpod, go_router, dio, i18n packages)
└── analysis_options.yaml
```

**Scaffolding order (do NOT deviate):**

1. Scaffold our custom files first (`lib/main.dart`, `lib/app/`, `lib/core/`, `lib/data/`, `lib/features/`, `pubspec.yaml`, `analysis_options.yaml`). At this point there is NO `ios/` or `android/` platform folder — that's fine.
2. Generate the missing platform folders by running:
   ```bash
   flutter create . --org com.{project-lowercase} --project-name {project-snake-case} --platforms=ios,android
   ```
   **NEVER pass `--overwrite`.** Without `--overwrite`, Flutter preserves every existing file (pubspec, main.dart, analysis_options.yaml, README.md, test/widget_test.dart) and only generates the missing platform folders. With `--overwrite`, Flutter silently replaces the custom entry files with template "counter demo" stubs and the non-obvious damage is easy to miss — `lib/app/`, `lib/core/`, `lib/data/`, `lib/features/` survive (they're not in the template), so the project looks fine at a glance while `main.dart`, `pubspec.yaml`, and `analysis_options.yaml` have been nuked.

**Post-scaffold cleanup (mandatory):**

- **Delete `test/widget_test.dart`.** It's the default Flutter stub testing the counter app that our `main.dart` replaces. Leaving it breaks `flutter test` (the counter widget it imports no longer exists). Real widget tests go under `test/features/{feature}/presentation/screens/` per the screen blueprint.
- **Do not create `l10n.yaml` unless i18n is fully wired.** An orphan `l10n.yaml` (no ARB files, `MaterialApp` without `AppLocalizations.localizationsDelegates`) emits warnings and confuses later sessions. Either (a) fully seed i18n during scaffolding — add `flutter_localizations` to pubspec, create minimal `lib/l10n/app_en.arb` + `app_tr.arb` with `app_name`, wire `MaterialApp`, and write `l10n.yaml` without `synthetic-package` (that option was deprecated in Flutter 3.24) — or (b) skip `l10n.yaml` entirely and let `flutter-agent` add it when the first localized string appears.

#### 2.5 React App (if selected)

Create React + TypeScript + Vite project (or Next.js if SSR selected):
```
app/
├── src/
│   ├── main.tsx
│   ├── components/ui/ (shared components)
│   ├── features/ (feature-first pages)
│   ├── hooks/ (custom hooks)
│   ├── lib/ (api client, auth, utils)
│   ├── stores/ (Zustand stores)
│   └── locales/ (i18n JSON files)
├── package.json
├── tsconfig.json
├── vite.config.ts (or next.config.ts)
└── tailwind.config.ts
```

#### 2.6 Project-Level .claude Configuration

```
.claude/
├── settings.json                        ← PreToolUse hook for coding rules injection
├── hooks/
│   └── inject-coding-rules.sh           ← Auto-inject app-specific rules on edit
├── rules/
│   └── coding-common.md                 ← Cross-cutting project rules (starts empty)
├── docs/
│   ├── coding-standards/
│   │   ├── api.md                       ← API-specific rules (starts empty)
│   │   ├── flutter.md                   ← (if Flutter selected)
│   │   └── react.md                     ← (if React selected)
│   ├── coding-rules-system.md
│   └── documentation-workflow.md
├── brain-storms/                        ← Empty, ready for brainstorms
├── backlog.md                           ← Empty, ready for deferred items
├── wiki/                                ← Project knowledge base (living)
│   └── index.md                         ← Auto-maintained table of contents
├── agent-memory/                        ← Per-agent learning history
├── journal/                             ← Inter-agent communication
└── design/                              ← (only if Q4 Claude Design = Yes) — empty, ready for /design-screen
```

**If Claude Design = Yes** (Q4): create `.claude/design/` directory; ensure CLAUDE.md mentions the `/design-screen` workflow; pre-write a stub `.atl/wiki/design-workflow.md` pointing at the canonical doc.

#### 2.7 Code Intelligence (.mcp.json)

Create `.mcp.json` at project root for codebase-memory-mcp integration:

```json
{
  "mcpServers": {
    "codebase-memory": {
      "command": "codebase-memory",
      "args": ["--project-root", "."]
    }
  }
}
```

This provides knowledge graph indexing of the entire codebase — function relationships, call chains, dependency mapping. Agents can query "who calls this?" and get precise answers instead of scanning files.

#### 2.8 Initial EF Migration (mandatory)

After all .NET projects, Docker compose, and supporting files are in place but BEFORE Phase 3's `docker compose up -d`, scaffold the initial EF migration. This requires the four cold-build csproj requirements from § 2.2 (Infrastructure framework reference + Api EF Design package + Worker hosting) to already be in place — the migration scaffold itself uses EF design-time tools.

```bash
docker compose run --rm api dotnet ef migrations add InitialCreate \
  --project ../{ProjectName}.Infrastructure \
  --startup-project .
```

This creates `Infrastructure/Persistence/Migrations/{timestamp}_InitialCreate.{cs,Designer.cs}` + `ApplicationDbContextModelSnapshot.cs`. EF auto-migrate picks them up on first API startup.

Without this step, the API starts but the database stays empty — verify-system Level 3 fails on auth/login because the `Users` table doesn't exist. The four cold-build requirements (csproj refs + initial migration) are interdependent: skipping any of them blocks verify-system.

If `dotnet-ef` is not on the api container's tool set, the run command fails with "Could not execute because the specified command or file was not found." Install it inside the container first (`docker compose run --rm api dotnet tool install --global dotnet-ef`) or — preferably — bake the install into `Dockerfile.dev` so subsequent fresh builds already have it.

### Phase 3 — Build and Start

1. **Build .NET solution** inside Docker:
   ```bash
   docker compose run --rm api dotnet build /src/{ProjectName}.sln
   ```

2. **Start all services:**
   ```bash
   docker compose up -d
   ```

3. **Wait 30-60 seconds** for services to stabilize (boot, migrate, connect).

4. **Index codebase for code intelligence** (if codebase-memory installed):
   ```bash
   codebase-memory index --path .
   ```

### Phase 4 — System Verification (MANDATORY skill invocation)

**This is a HARD requirement.** You MUST call the `Skill` tool with `verify-system` here. Do NOT run the verification commands manually as a separate flow — the Skill tool call is what makes this step auditable for the user. The user explicitly relies on seeing the skill's invocation as proof that verification ran.

```
Skill(skill="verify-system")
```

The skill returns markdown instructions for a 4-level end-to-end check:
- Level 1: All containers running
- Level 2: All ports accessible
- Level 3: All applications healthy (meaningful responses)
- Level 4: All pipelines working (logging, email, auth, socket, worker, redis, storage)

After invoking the skill:
1. Execute every check the skill describes (the skill is a script — you are the runtime).
2. Collect results level-by-level.
3. **Show the user the final verification report block** (the boxed `╔══...══╗` summary the skill defines) before moving on.

**The project is NOT ready until the report shows ALL PASS.** If any test fails:
- Diagnose the root cause (don't paper over it)
- Fix it
- Re-invoke the skill
- Show the new report

Do not proceed to Phase 5 until verification is green and the user has seen the report.

### Phase 5 — Git Initialize

```bash
cd {project-directory}
git init   # only if not already a git repo
git add -A
git commit -m "feat: initial project setup with full infrastructure"
```

If the directory was already a git repo (e.g. user pre-cloned an empty remote), skip `git init` and just commit on top of the existing history.

## Important Rules

1. **Everything runs in Docker.** The skill NEVER installs SDKs locally (except noting Flutter needs local install).
2. **martinothamar/Mediator, NOT MediatR.** Source generator based.
3. **Minimal API, NO Controllers.** Every project uses endpoint groups.
4. **LogIngest logs to console ONLY.** Prevents infinite RMQ loop.
5. **Consumers declare their own topology.** Don't assume API created it first.
6. **seed.sql for development data.** Idempotent INSERTs, fixed UUIDs.
7. **Port offset if multi-project.** All ports configurable via .env.
8. **CLAUDE.md is filled with actual project info** — tech stack, port list, development commands.

## What Is NOT Included (by design)

- Domain entities (project-specific — added during development)
- Business logic (added via API Agent as features are built)
- Production deployment (CI/CD templates are in Infra Agent's knowledge)
- Flutter/React screens (added via Flutter/React Agent as features are built)

The skill creates the **skeleton** — the team of agents fills it with life.

## Accumulated Learnings

(Auto-rebuilt by /save-learnings from `learnings/*.md` frontmatter. Do not edit by hand. Initially empty — entries appear as the skill encounters reusable edge cases.)
