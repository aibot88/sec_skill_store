---
name: sql-server-best-practices
description: >
  SQL Server and Azure SQL best practices for developers and DBAs. Use this skill whenever the user
  asks about T-SQL, stored procedures, query performance, indexes, schema design, database security,
  or SQL Server / Azure SQL maintenance — even if they don't say "best practices." Triggers on
  requests like "write a stored proc," "this query is slow," "clustered vs nonclustered index,"
  "parameter sniffing," "WITH NOLOCK," "prevent SQL injection in MSSQL," "set up db permissions,"
  "index rebuilds or backups," or "review this migration script." Use for any T-SQL code review,
  DDL review, or schema design question where the database is SQL Server or Azure SQL.
  Skip for MySQL, PostgreSQL, SQLite, Oracle, or any non-MSSQL database — the guidance here
  (RCSI, sp_Blitz, T-SQL syntax, SQL Agent, NEWSEQUENTIALID, etc.) does not apply to other platforms
  and could actively mislead. Also skip for ORM-only questions (Entity Framework errors, LINQ,
  Django migrations) where no T-SQL or SQL Server configuration is involved.
license: Complete terms in LICENSE (MIT)
---

# SQL Server Best Practices

This skill covers both on-premises SQL Server (2016+) and Azure SQL Database / Managed Instance.
When differences exist between the two, they are called out in the relevant section.

## How to Use This Skill

Identify which domain(s) the user's request falls into, then read the corresponding reference file(s)
before responding. For requests that touch multiple domains (e.g., "review this stored proc and its
indexes"), read all relevant files.

| Domain | When to use | Reference file |
|--------|-------------|----------------|
| T-SQL & query patterns | Writing queries, stored procs, functions, CTEs, cursors, error handling | `references/query-patterns.md` |
| Indexing strategy | Index design, fragmentation, missing/duplicate indexes, query plan issues | `references/indexing.md` |
| Schema & data modeling | Table design, data types, naming conventions, constraints, relationships | `references/schema-design.md` |
| Security | Permissions, least privilege, dynamic SQL injection, encryption, auditing | `references/security.md` |
| Maintenance & monitoring | Health checks, index rebuild, statistics, backups, CHECKDB | `references/maintenance.md` |

## Quick Principles (always apply)

These apply regardless of domain — internalize them before reading any reference file:

1. **Correctness first.** A fast query that returns wrong results is worse than a slow correct one.
2. **Set-based over row-by-row.** SQL Server is optimized for set operations; cursors and loops are last resorts.
3. **Explicit over implicit.** Always specify schema (`dbo.TableName`), always use `SET NOCOUNT ON` in procs, always define column lists in `INSERT`.
4. **Test with realistic data volumes.** A query that looks fine on 1,000 rows can fall apart at 10 million.
5. **Don't guess — measure.** Use execution plans, `SET STATISTICS IO ON`, and `sp_BlitzCache` rather than intuiting performance.
6. **Least surprise.** Name things clearly. A reader unfamiliar with the system should be able to understand what a table, column, or proc does from its name alone.

## Always Flag — Regardless of What Was Asked

When reviewing any SQL, DDL, or migration code, always call out the following issues unprompted — even if the user only asked about something else:

- **`ON DELETE CASCADE`** — warn that it will silently delete child rows without confirmation or audit trail. Recommend removing it and handling deletes explicitly in a stored procedure instead.
- **`ON DELETE SET NULL`** — warn that it silently breaks FK relationships. Recommend explicit handling.
- **`NOLOCK` / `WITH (NOLOCK)`** — warn about dirty reads and phantom rows. Recommend enabling RCSI at the database level instead.
- **`EXEC(@sql)`** with string concatenation — flag as SQL injection risk. Recommend `sp_executesql` with parameters.

Keep the callout brief and constructive — one or two sentences, then move on to what the user actually asked.

## Pre-Flight Questions

Before writing any DDL or stored procedures, ask the questions below if the answers aren't already clear from context. Ask them together upfront — don't generate code first and ask after.

**For any stored procedure or T-SQL code:**

- **Naming convention** — ask once per conversation:
  > "What prefix do you use for stored procedures — `usp_` (common default), none, or something else?"
  > Note: avoid `sp_` — SQL Server searches the master database first for any proc starting with `sp_`, which causes unnecessary overhead and confusion with system procedures.

**For schema / table design or new database setup:**

- **Primary key type** — ask once per conversation:
  > "Do you prefer **INT IDENTITY** (auto-increment integers: 1, 2, 3…) or **GUID** (UNIQUEIDENTIFIER — globally unique, better for distributed systems)?"

- **Soft deletes** — ask when designing tables that represent entities users might "delete":
  > "Do you want soft deletes (an `IsDeleted BIT` flag + `DeletedAt DATETIME2` column so rows are hidden but not removed) or hard deletes (physically remove the row)?"

- **Audit trail** — ask for any new schema:
  > "Do you want standard audit columns on each table — `CreatedAt DATETIME2`, `UpdatedAt DATETIME2`, and optionally `CreatedBy` / `UpdatedBy`?"

If the user has already answered any of these earlier in the conversation, use that answer — don't ask again.

## Determining Which Reference(s) to Read

Ask yourself what the user is trying to accomplish:

- **"Write/fix/review a query or stored proc"** → `query-patterns.md`
- **"Why is this slow / add an index / review query plan"** → `indexing.md` + `maintenance.md` (sp_BlitzCache/sp_BlitzFirst live there) + possibly `query-patterns.md` for SARGability
- **"Design a table / choose a data type / naming question"** → `schema-design.md`
- **"Set up permissions / prevent SQL injection / audit access"** → `security.md`
- **"Set up maintenance jobs / check database health / configure backups"** → `maintenance.md`
- **"Review this migration or DDL script"** → `schema-design.md` + `security.md`
- **"General code review of SQL"** → read all five, prioritize issues by severity
