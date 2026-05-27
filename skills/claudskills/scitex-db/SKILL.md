---
name: scitex-db
description: Relational-DB wrapper for scientific Python — `SQLite3` and `PostgreSQL` classes composed from a dozen shared mixins (connection, transaction, query, schema, index, row/batch ops, import/export, backup, blob, maintenance) with first-class numpy `ndarray` BLOB storage, health checks, duplicate removal, and schema inspection. Public API (5 symbols) — `SQLite3(db_path, ...)` (unified SQLite client with `.execute(sql, params)`, pandas `.to_df(table)`, `.save_array(name, arr)` / `.load_array(name)` for compressed-ndarray BLOBs, `.check_health()`, `.inspect()`, context-manager transactions), `PostgreSQL(dsn, ...)` (same surface for Postgres), `delete_duplicates(conn, table, columns=None)` (dedupe rows by column subset), `delete_sqlite3_duplicates(db_path, ...)` (SQLite-specific convenience), `inspect(db)` (dump schema + row counts + index summary). CLI — `scitex-db inspect <db>`, `scitex-db health <db>`. No MCP tools. Drop-in replacement for hand-rolled `sqlite3.connect(...)` wrappers, `psycopg2` boilerplate, storing ndarrays via `pickle.dumps` → `BLOB` (no compression, no typed load), SQLAlchemy Core when you don't need an ORM, and bespoke "find and delete duplicate rows" SQL snippets. Use whenever the user asks to "store numpy arrays in SQLite", "persist experiment results to Postgres", "dedupe rows in a table", "check this SQLite DB is healthy / not corrupt", "inspect the schema of a DB", "save/load compressed ndarrays as BLOBs", or mentions `scitex.db`, `SQLite3` class, numpy BLOB storage.
---

# scitex-db

Two database classes (`SQLite3`, `PostgreSQL`) composed from a dozen
shared mixins, plus standalone maintenance helpers.

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-db
import scitex_db
scitex_db.SQLite3(...)

# Umbrella — pip install scitex
import scitex.db
scitex.db.SQLite3(...)
```

`pip install scitex-db` alone does NOT expose the `scitex` namespace;
`import scitex.db` raises `ModuleNotFoundError`. To use the
`scitex.db` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core

* [01_quick-start](01_quick-start.md) — SQLite3 + PostgreSQL minimal examples
* [02_python-api](02_python-api.md) — Public symbols
* [03_mixins](03_mixins.md) — The mixin architecture (capability groups)
* [04_numpy-blob](04_numpy-blob.md) — Storing ndarrays with compression
* [05_maintenance](05_maintenance.md) — `check_health`, `delete_duplicates`, `inspect`

### Interface

* [10_cli-reference](10_cli-reference.md) — `scitex-db inspect` / `health`
