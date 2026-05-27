---
name: ascent-data-health
description: >-
  Validates SQLite-WAL database configuration and migration discipline
  for <<PROJECT_TITLE>>. Checks WAL mode, foreign-key enforcement,
  migration tracking, and migration file ordering — the silent-failure
  prevention layer for the data tier.
version: <<PROJECT_VERSION>>
allowed-tools:
  - Read
  - Grep
  - Glob
---

# ascent-data-health

Validates the data tier configuration that ADR-004 (SQLite-WAL as default database) commits to. SQLite misconfigurations are silent — foreign keys are off by default, WAL mode must be explicitly enabled, and migration ordering errors cause schema drift without error messages. This skill catches those silent failures before they become production data corruption.

For the structural §7 check that [ascent-self-audit](../ascent-self-audit/SKILL.md) includes, see that skill's Step 8. This skill provides deeper data-tier analysis beyond what the umbrella check covers.

## When this skill engages

- After schema changes or new migrations are added
- When onboarding to verify the data tier is correctly configured
- As a periodic health check alongside `ascent-self-audit`
- When debugging data integrity issues (missing foreign-key violations, duplicate rows)

## Inputs

- **`backend/storage/db.js`** — database initialization and pragma configuration (required)
- **`backend/storage/migrations/*.sql`** — migration files (required for ordering check)

## Outputs

- **Per-check report** — each of the 4 checks marked PASS or FAIL with specific detail
- **Summary line** — "data-health: N/4 checks passing"

## Operational logic

The skill executes these steps in order. Step numbers are local to this skill.

### Step 1 — WAL mode enabled

**Condition:** `backend/storage/db.js` contains a pragma statement setting journal_mode to WAL.

**Action on PASS:** Report "WAL mode — PASS. journal_mode = WAL is set."

**Action on FAIL:** Report "WAL mode — FAIL. backend/storage/db.js does not set `pragma('journal_mode = WAL')`. Without WAL mode, concurrent reads block during writes. See ADR-004."

### Step 2 — Foreign keys enforced

**Condition:** `backend/storage/db.js` contains a pragma statement enabling foreign keys.

**Action on PASS:** Report "Foreign keys — PASS. foreign_keys = ON is set."

**Action on FAIL:** Report "Foreign keys — FAIL. backend/storage/db.js does not set `pragma('foreign_keys = ON')`. SQLite ignores foreign-key constraints by default — data integrity is not enforced without this pragma."

### Step 3 — Migration tracking present

**Condition:** `backend/storage/db.js` contains the `_migrations` table creation pattern (CREATE TABLE IF NOT EXISTS _migrations) and a migration-runner loop that reads `.sql` files from the migrations directory.

**Action on PASS:** Report "Migration tracking — PASS. _migrations table and runner present."

**Action on FAIL:** Report "Migration tracking — FAIL. No migration-tracking pattern found in db.js. Schema changes applied outside the migration runner cause drift between environments."

### Step 4 — Migration file ordering

**Condition:** All `.sql` files in `backend/storage/migrations/` follow the zero-padded numeric prefix pattern (`NNN_description.sql`, e.g., `001_initial.sql`, `002_add_users.sql`). Files must be lexicographically sortable to apply in the correct order.

**Action on PASS:** Report "Migration ordering — PASS. N migration files, all correctly prefixed."

**Action on FAIL:** Report each non-conforming filename. Example: "Migration ordering — FAIL. `2_users.sql` is not zero-padded — should be `002_users.sql`. Non-padded prefixes sort incorrectly past 9 migrations."

**Fallback:** If `backend/storage/migrations/` doesn't exist or is empty, report "Migration ordering — PASS (0 migration files — directory not yet populated)."

## Examples

### Example 1 — Healthy scaffold

**Input state:** Freshly scaffolded project with default `db.js` and `001_initial.sql`.

**Skill output:**
```
ascent-data-health: 4/4 checks passing
  WAL mode             PASS (journal_mode = WAL)
  Foreign keys         PASS (foreign_keys = ON)
  Migration tracking   PASS (_migrations table + runner)
  Migration ordering   PASS (1 migration file, correctly prefixed)
```

### Example 2 — Missing foreign-key pragma

**Input state:** Developer removed the `foreign_keys = ON` pragma to "fix" a constraint error.

**Skill output:**
```
ascent-data-health: 3/4 checks passing (1 failure)
  WAL mode             PASS
  Foreign keys         FAIL
    → backend/storage/db.js does not set pragma('foreign_keys = ON')
    → SQLite ignores FK constraints by default — data integrity is not enforced
  Migration tracking   PASS
  Migration ordering   PASS
```

## Anti-patterns

### Anti-pattern 1 — Bypassing the migration runner

Applying schema changes with raw SQL statements in application code instead of migration files. **Why it's tempting:** "it's just one column." **What to do instead:** every schema change gets a numbered `.sql` file in `backend/storage/migrations/`. The migration runner tracks what's applied; raw SQL doesn't.
