---
name: drk-postgres
description: "PostgreSQL 16 & Drizzle ORM Best Practices für DRK-Digitalisierungstools. Verwende diesen Skill bei Variante-B-Apps (Server + Datenbank) für Schema-Design, Migrations, Security (RLS), Query-Optimierung und Docker-Konfiguration."
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
argument-hint: "[thema] z.B. schema, drizzle, security, rls, migration, docker"
---

# DRK PostgreSQL & Drizzle Best Practices

PostgreSQL 16 Best Practices für DRK-Digitalisierungstools.
Stack: Next.js 16 + Drizzle ORM + PostgreSQL 16 (Docker) + Hetzner.

## Aufgabe

Lies die zum Thema passenden Referenz-Dateien aus `skills/drk-postgres-skill/references/` und wende die Best Practices auf das aktuelle Projekt an.

Wenn `$ARGUMENTS` angegeben ist, fokussiere auf das genannte Thema. Ohne Argumente: Gib eine Übersicht der verfügbaren Themen.

## Referenz-Dateien

Die `skills/drk-postgres-skill/references/`-Dateien enthalten konkrete SQL- und Drizzle-Patterns.
Jede Datei ist nach dem Schema `kategorie-thema.md` benannt.

### Kategorien (nach Priorität)

| Kategorie | Dateien | Thema |
|-----------|---------|-------|
| **schema** | `schema-primary-keys.md`, `schema-data-types.md`, `schema-naming.md`, `schema-foreign-key-indexes.md` | Tabellen, Datentypen, PKs, FKs |
| **drizzle** | `drizzle-schema-patterns.md`, `drizzle-migrations.md` | Drizzle-ORM-Patterns, Schema, Migrations |
| **security** | `security-rls-tenant.md`, `security-privileges.md` | RLS, Least Privilege, Tenant-Isolation |
| **query** | `query-missing-indexes.md` | Indexes, Query-Optimierung |
| **data** | `data-n-plus-one.md`, `data-upsert.md` | N+1, Upserts, Batch-Inserts |
| **lock** | `lock-short-transactions.md` | Transaktionen kurz halten |
| **monitor** | `monitor-explain-analyze.md` | EXPLAIN ANALYZE, pg_stat_statements |
| **docker** | `docker-postgres-config.md` | PostgreSQL-Konfiguration im Docker-Kontext |

### Thema-Zuordnung

Wenn der Nutzer eines dieser Themen nennt, lies die zugehörigen Dateien:

- **schema**, **tabellen**, **datentypen**, **primary key**, **pk** → `schema-*.md`
- **drizzle**, **orm**, **migration** → `drizzle-*.md`
- **security**, **rls**, **tenant**, **privilege**, **rechte** → `security-*.md`
- **index**, **query**, **performance** → `query-missing-indexes.md`
- **n+1**, **upsert**, **batch** → `data-*.md`
- **transaktion**, **lock**, **deadlock** → `lock-short-transactions.md`
- **explain**, **monitor**, **stats** → `monitor-explain-analyze.md`
- **docker**, **config**, **hetzner**, **backup** → `docker-postgres-config.md`
- **alles**, **übersicht**, **setup** → Alle Dateien lesen

## Schnellregeln

- **Immer `bigint generated always as identity`** für Primary Keys (nicht `serial`)
- **Immer `timestamptz`** statt `timestamp`
- **Immer `text`** statt `varchar(n)` (außer bei echtem Constraint-Bedarf)
- **Immer Foreign Keys indexieren** — PostgreSQL macht das nicht automatisch
- **Immer `snake_case`** für Tabellen und Spalten
- **Immer `tenant_id` + RLS** für Multi-Tenant-Tabellen
- **Nie `SELECT *`** in Produktion
- **Nie API-Calls innerhalb von Transaktionen**

## Scope

Dieser Skill gilt für alle DRK-Apps mit Variante B (Server + Datenbank).
Siehe `INFRASTRUCTURE.md` für den DSGVO-Goldstandard.
