---
name: remix-scaffolders
description: Project-local Bun scaffolders shipped by THIS plugin (not the official `remix` CLI) for adding things incrementally to an existing project — `scripts/create-route.ts --name X --pattern //Y` (route + handler + router.map wiring, escaping Git Bash MSYS path mangling with `//`), `scripts/create-resource.ts --name X --param Yid [--only index,show,...]` (`resources()` block + 7-action controller mirror), `scripts/create-controller.ts --route admin.books` (stub for an existing RouteMap), `scripts/create-migration.ts --name add_X_table` (timestamped file under `db/migrations/`), `scripts/add-middleware.ts --name session|csrf|cors|cop|...` (inserts into `app/router.ts` in canonical stack order), `scripts/init-project.ts` (alternative to `remix new` for envs without the CLI). All idempotent, all refuse to overwrite (exit 2), all validate camelCase identifiers, all smoke-tested in `verify.ts`. Load whenever the user is adding a single route, resource, controller stub, migration, or middleware to an existing project, or asking how to scaffold a new entity. For framework-level commands (`remix new`/`doctor`/`routes`/`test`), see /remix:cli.
---

# Scaffolders

Project-local Bun scripts that scaffold incremental additions to an existing Remix v3 project. The official [cli](../cli/SKILL.md) does bootstrap + audit + inspect; these handle the day-to-day "add one route", "add one resource", "add one migration" operations.

Each script:
- Reads `app/routes.ts` and `app/router.ts` from the working directory
- Refuses to overwrite existing files (exit 2)
- Prints exactly what it changed
- Validates inputs (camelCase identifiers, escaped patterns, etc.)

## Available scaffolders

| Script | What it does |
|---|---|
| `init-project.ts`     | Alternative to `remix new` — scaffolds the whole project layout |
| `create-route.ts`     | Add a single route + handler + router.map() wiring |
| `create-resource.ts`  | Add a `resources(...)` block + 7-action controller |
| `create-controller.ts`| Stub a controller for an existing RouteMap entry |
| `create-migration.ts` | Drop a timestamped migration file under `db/migrations/` |
| `add-middleware.ts`   | Insert a built-in middleware in canonical position |

All live under `scripts/` in this plugin.

## Usage

```pwsh
# Bootstrap (alternative to `remix new`)
bun run scripts/init-project.ts --name my-app --app-name "My App"

# Incremental additions
bun run scripts/create-route.ts     --name about --pattern //about
bun run scripts/create-resource.ts  --name reviews --param reviewId
bun run scripts/create-resource.ts  --name books   --param bookId --only index,show
bun run scripts/create-controller.ts --route admin.books
bun run scripts/create-migration.ts --name add_reviews_table
bun run scripts/add-middleware.ts   --name session
bun run scripts/add-middleware.ts   --name csrf
bun run scripts/add-middleware.ts   --name cors
```

## When to use which

| Goal | Use |
|---|---|
| Brand new project | `remix new` ([cli](../cli/SKILL.md)) — official, canonical |
| Brand new project, no network / no CLI access | `init-project.ts` (this plugin) |
| One new route | `create-route.ts` |
| Full REST surface for a resource | `create-resource.ts` |
| Existing route in `routes.ts`, missing controller file | `create-controller.ts` |
| New migration | `create-migration.ts` |
| Add session, csrf, logger, etc. to router.ts | `add-middleware.ts` |
| Auto-fix small layout drift | `remix doctor --fix` ([cli](../cli/SKILL.md)) |

## Why these and not the CLI

`remix doctor --fix` is **repair-oriented** (rename mis-cased files, restore missing-but-defaultable fields, etc.). It doesn't *add* new entities.

These scaffolders are **add-oriented**:

- `create-route` knows how to update `routes.ts` AND wire `router.ts` AND stub the handler — three coordinated edits.
- `create-resource` generates the right 7-action mirror that `Controller<typeof routes.X>` expects.
- `add-middleware` sorts entries by canonical stack order (so `csrf()` lands between `session()` and `asyncContext()`, not at the bottom).
- `create-migration` produces the correct filename timestamp + `createMigration({up, down})` skeleton.

## Argument quoting on Git Bash (Windows)

Bun on Git Bash inherits the MSYS path-mangling quirk: a leading `/` in an argument gets expanded to a Windows path. Use `//` to escape:

```pwsh
bun run scripts/create-route.ts --name about --pattern //about
# Without the double slash, `/about` becomes `C:/Program Files/Git/about`
```

The scaffolder detects this and exits with a helpful error if it sees a Windows-path-looking pattern.

## Running under Node instead of Bun

```pwsh
node --experimental-strip-types scripts/init-project.ts --name my-app
```

Node ≥ 22.6.0 with the flag works. Node ≥ 23 has it on by default.

## Verification

Every scaffolder is smoke-tested by `bun run scripts/verify.ts` against the real Remix package. If a scaffolder regresses, the pre-commit hook blocks the commit. See [`scripts/README.md`](../../scripts/README.md) for the full harness.

## Further reading

- [`references/local-scaffolders.md`](./references/local-scaffolders.md) — full per-script reference (flags, edge cases, idempotency contract)
- See also: [cli](../cli/SKILL.md) (official CLI), [migrations](../migrations/SKILL.md), [middlewares](../middlewares/SKILL.md)
