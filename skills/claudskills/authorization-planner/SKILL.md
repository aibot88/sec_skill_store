---
name: Authorization Planner
description: Use when a user wants to plan, scope, or get started with adding authorization
  to their application - guides brainstorming to produce a phased implementation plan
  that incorporates the right skills and commands in sequence
---

# Authorization Planner

This plugin adds a first pass at SpiceDB fine-grained authorization to an application
being built or modified. The goal is getting authorization structurally correct --
right permissions, right places, right operations. It is not a production hardening
or debugging tool.

## Ideal Workflow

### Once, early -- before or alongside data model design

Run `/spicedb-dev:plan`. This scopes the work, produces `authorization-plan.md`,
and writes an authorization snippet to `CLAUDE.md` so permissions are considered
automatically in every future session without needing to invoke any command. This is
the most important setup step.

Then `/spicedb-dev:design-model` -- scans for existing model files and extracts
entity names. Produces `permission-model.md`.

Then `/spicedb-dev:generate-schema` -- converts the model to `schema.zed`.
Schema-validator runs automatically.

Deploy the schema externally: `zed schema write schema.zed`.

### Continuously, alongside every feature

Every feature needs both operations -- this is the most common implementation mistake:

1. **Relationship writes** (`/spicedb-dev:implement-spicedb-relationships`) --
   run when writing handlers that create resources, grant membership, or delete resources.
   SpiceDB returns NO_PERMISSION for everything until relationships are written. Writes
   must come before checks.

2. **Permission checks** (`/spicedb-dev:implement-spicedb-checks`) -- run when
   writing any handler that reads, modifies, or deletes a resource on behalf of a user.
   For list endpoints, use LookupResources -- not CheckPermission in a loop.

Use `/spicedb-dev:implement-spicedb` when unsure which is needed -- it
communicates the paired requirement and routes to the right command.

### Periodically

`/spicedb-dev:audit-coverage` produces a coverage matrix: every permission in
the schema vs. whether a corresponding check exists in code. Routes each gap to the
correct implement command.

### Once, when stable

`/spicedb-dev:test-permissions` generates test fixtures and integration tests
from the schema.

## Routing by Situation

- New project, no existing auth → `/spicedb-dev:plan`
- Have a data model, need permission design → `/spicedb-dev:design-model`
- Have a permission model, need a schema → `/spicedb-dev:generate-schema`
- Have a schema, need implementation → `/spicedb-dev:implement-spicedb`
- Inherited codebase, need coverage picture → `/spicedb-dev:audit-coverage`
- Unsure which SpiceDB pattern fits → `spicedb-schema-design` skill
- Questions about client code or consistency → `spicedb-best-practices` skill

## Scoping Tips

**Greenfield**: Start with the simplest model that works. Three resources with basic
RBAC beats ten resources with speculative complexity. Add caveats and custom roles
only when a concrete scenario requires them.

**Existing app**: The `checkpoint-identifier` agent can map current authorization
boundaries before designing the SpiceDB model. Run it early to reveal scope that
isn't obvious from the data model alone.

**Multi-tenant SaaS**: Finalize tenant isolation before designing resource-level
permissions. The tenant boundary is the most consequential design decision -- getting
it wrong affects every other resource.

**Migration**: Do not skip Phase 1. Read existing auth code first to understand the
current permission surface. See the Migration Track in `/spicedb-dev:plan`.
