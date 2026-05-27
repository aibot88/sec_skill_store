---
name: syntherklaas
description: Generate synthetic data from scratch through an interactive dialog — ask the user table-by-table about columns, types, foreign keys, and constraints; render the data model as ASCII UML; ask for volume + distributions; then generate consistent fake data with Faker (locale-aware) + NL-locked providers for BSN/IBAN/postcode. Outputs CSV (loose files), XLSX (loose or multi-sheet), or SQLite. Schema can be saved to YAML for re-invoke (`/syntherklaas <yaml-path>` skips the dialog, runs deterministic generation). Use when the user wants test data, demo data, fake data with FK relations, or mentions "synthetic data", "fake data", "test data", "demo dataset", "BSN-safe test data", or "anonimiseer me een schema".
---

# syntherklaas

Interactive synthetic data generator. Two invocation paths:

1. **Full dialog** (`/syntherklaas`) — build the data model from scratch.
2. **Re-invoke** (`/syntherklaas <yaml-path>`) — load a previously-saved schema, confirm, run.

Pipeline: dialog → schema-YAML → Faker + numpy (deterministic seed) → topo-ordered DataFrames → writer (CSV-loose / XLSX-loose / XLSX-multi / SQLite).

## Dispatch

When the user invokes the skill, branch on the argument:

- **Argument is a `.yaml` or `.yml` file that exists** → go to **Re-invoke path** below.
- **No argument, or other text** → go to **Full dialog path** below.

---

## Re-invoke path

1. Load the YAML via `bash "${CLAUDE_SKILL_DIR}/scripts/run.sh" --schema <path> --preview` to validate it and obtain a JSON preview (the script returns exit code 2 on a malformed YAML).
2. Render a confirmation summary in chat — list the tables, locale, seed, output target (from the YAML's `output` block if present), and a 10-row preview per table.
3. Ask: **"OK om te genereren? (ok / annuleer)"**.
4. On `ok`:
   - If the YAML already has an `output` block, run `bash ${CLAUDE_SKILL_DIR}/scripts/run.sh --schema <path>` (it picks up format+path from the YAML).
   - Otherwise ask the user for format + path, then run `bash ${CLAUDE_SKILL_DIR}/scripts/run.sh --schema <path> --output <out> --format <fmt>`.
5. On `annuleer` — stop.

---

## Full dialog path

Greet the user briefly, then proceed through the phases below. The user may say "stop" at any point to abort.

### Phase 0 — Locale

Ask: **"Faker-locale? (default: `nl_NL` — accepteert bv. `en_US`, `de_DE`, `fr_FR`, ...)"**

Note: NL-locked providers (`nl.bsn`, `nl.iban`, `nl.postcode`, `nl.phone`, `nl.tussenvoegsel`) always emit NL-formatted values regardless of session locale. Mention this if the user picks non-NL and the schema later includes any `nl.*` provider.

### Phase 1 — Schema discovery (loop per table)

For each table:

1. Ask: **"Tabelnaam?"**
2. Ask: **"Hoe wil je de kolommen van `<tabel>` definiëren?"** with three options:
   - **Paste voorbeeld-data** — plak een paar regels CSV-achtig of freeform; ik leid kolommen + types af.
   - **Samen definiëren** — we lopen kolom-voor-kolom door (naam + voorbeeld), tot je `klaar` zegt.
   - **Doe een voorstel** — ik stel zelf kolommen voor op basis van de tabelnaam.
3. Branch:
   - **Paste**: user pastes CSV-like rows or freeform examples. Extract column names + 1-5 sample values per column.
   - **Guided**: loop "kolomnaam? voorbeeld(en)? volgende of klaar?" until the user signals done.
   - **Voorstel**: propose 5-10 plausible columns directly from the table name — each met een naam, type, gekozen provider en 1-2 voorbeelden — en spring meteen door naar de confirm-tabel (step 5; provider-inferentie heb je al in het voorstel gedaan). Als de tabelnaam te dun is om iets zinnigs te verzinnen (bv. `data`, `items`, `records`, `tabel1`, `temp`, eenletterige namen): vraag **eerst** "Waar is `<tabel>` voor?" en bouw het voorstel op basis van dat antwoord. Bij concrete namen (`klanten`, `orders`, `email_campagnes`, `facturen`, `producten`, `medewerkers`, ...) niet eerst vragen — stel direct voor en laat de user in step 6 corrigeren.
4. Based on column names + sample values, **infer a provider per column** from this table:

   | Provider name             | When to pick |
   |---------------------------|--------------|
   | `sequential` + `primary_key: true` | always for an `id` column |
   | `faker.name`              | column looks like a person name |
   | `faker.email`             | column looks like an email |
   | `faker.phone_number`      | non-NL phone, or generic phone |
   | `faker.address`           | generic address |
   | `faker.company`           | company name |
   | `faker.text`              | free-form text / notes |
   | `nl.bsn`                  | NL BSN |
   | `nl.iban`                 | NL IBAN |
   | `nl.postcode`             | NL postal code (`1234 AB`) |
   | `nl.phone`                | NL mobile (06-XXXXXXXX) |
   | `nl.tussenvoegsel`        | NL surname infix |
   | `numeric_range`           | integer/float with bounds (age, price, count, ...) |
   | `categorical`             | small fixed set of values (status, type, ...) |
   | `datetime_range`          | timestamp or date in a window |
   | `fk`                      | `<table>_id` columns or otherwise clearly referencing another table |

5. Render a confirm table:
   ```
   | col       | provider          | constraint     | voorbeeld     |
   | id        | sequential        | PK             | 1, 2, 3, ...  |
   | naam      | faker.name        | NOT NULL       | (Faker name)  |
   | bsn       | nl.bsn            | UNIQUE         | 123456782     |
   | leeftijd  | numeric_range int | min 18, max 80 | 42            |
   | status    | categorical       | choices=[...]  | active        |
   ```
6. **Conditional values** — detect cases where a column should only be populated when another column has a specific value (klassiek voorbeeld: `url` alleen gevuld bij `event_type=click`; `cancelled_at` alleen bij `status=cancelled`). Use the `when`-clause on the dependent column:
   ```yaml
   - name: url
     provider: faker.url
     when:
       column: event_type
       equals: click          # scalar of lijst, bv. [click, custom_click]
       # else_value: <value>  # optioneel; default null
   ```
   Rules: `when.column` moet **eerder** in dezelfde tabel staan (validator dwingt dat af) en mag niet op `sequential` / `fk` / PK kolommen. Stel `when` proactief voor wanneer de naam-combinatie het suggereert; render in de confirm-tabel met constraint `when event_type=click`.
7. Ask: **"Klopt? (ok / wijzig kolom <naam>)"**. On wijzig: update the column and re-render, loop until ok.
8. Ask: **"Foreign keys naar andere tabellen? (bv. `user_id → users.id` of `geen`)"**. Add as `fk`-provider columns.
9. Ask: **"Nog een tabel of klaar?"**. Loop until `klaar`.

### Phase 2 — ASCII UML

Topo-sort the tables and render boxes with columns + relations with cardinality. Style:

```
┌─────────────────────────┐         ┌──────────────────────────┐
│ users                   │ 1     * │ events                   │
├─────────────────────────┤─────────┤──────────────────────────┤
│ id (PK)         INT     │         │ id (PK)          INT     │
│ naam            STR     │         │ user_id (FK)     INT ────┤
│ bsn (UQ)        STR     │         │ kind             STR     │
│ leeftijd        INT     │         │ occurred_at      DATETIME│
└─────────────────────────┘         └──────────────────────────┘
```

Use `1..*` notation on the edges. Ask: **"Klopt het model? (ok / wijzig <tabel>)"**.

### Phase 3 — Volume + distributies

**Before asking the first volume question**, send een korte intro-message (geen AskUserQuestion) die uitlegt wát we nu gaan vastleggen en wat de keuzes betekenen. Voorbeeld-strekking (parafraseer, niet letterlijk kopiëren):

> We bepalen nu hoeveel rijen elke tabel krijgt. Per tabel kies je een verdeling:
> - **Vast** — exact dit aantal rijen (bv. `1000`). Geen variatie.
> - **Poisson λ=N** — N als gemiddelde, met natuurlijke variatie rond dat getal. Past bij "ongeveer N events per gebruiker" of "ongeveer N orders per dag".
> - **Normal μ±σ** — klokvormig rond μ met spreiding σ. Past bij "rond de 500, meeste tussen 400 en 600".
> - **Uniform min-max** — elk getal in `[min, max]` even waarschijnlijk. Brede gelijke spreiding.
> Voor child-tabellen geldt dit per parent-rij (`per_parent`); voor root-tabellen geldt het als totaal.

Pas de exact gepresenteerde opties in elke AskUserQuestion aan de tabel-context aan (bv. concrete λ/μ/min-max-suggesties op basis van wat de user eerder zei).

For each table in topological order, ask via AskUserQuestion:

- **Root** (no FK): **"Hoeveel rijen voor `<tabel>`?"** — bied 4 keuzes: een redelijke vaste waarde, een poisson, een normal, en een uniform. Concrete getallen invullen.
- **Child** (has FK with `per_parent` semantics): **"Hoeveel `<tabel>` per `<parent>`?"** — zelfde 4 opties, schaling per parent. Als user expliciet een totaal noemt, accepteer dat en val terug op `count` semantics.

For each `datetime_range` column: ask **"tijdsperiode? (bv. `2024-01-01..2024-12-31`; `uniform` of `normal`)"**.

For each `numeric_range` column: ask **"range? (bv. `18-80 uniform` of `35±12 normal`)"**.

For each `categorical` column: ask **"gewichten? (`uniform` of bv. `60/30/10` voor 3 choices)"**.

Translate user shorthand into the schema-YAML format (see `examples/demo-schema.yaml`).

### Phase 4 — Build YAML + preview

1. Write the schema to `/tmp/syntherklaas-<sessid>/schema.yaml` (mkdir-p first; use a fresh UUID or timestamp suffix).
2. Run: `bash "${CLAUDE_SKILL_DIR}/scripts/run.sh" --schema /tmp/.../schema.yaml --preview`
3. Parse the JSON preview and render Markdown tables (max 10 rows per table) in chat.

### Phase 5 — Output

1. Ask: **"Tevreden? (`ok` / `regenerate` met andere seed / `wijzig` schema)"**.
   - `regenerate`: edit the YAML to add a new `seed: <random_int>`, re-run preview.
   - `wijzig`: drop back to the relevant phase (1/2/3) to edit.
2. Ask: **"Output-formaat?"**
   1. `csv-loose` — losse CSV-bestanden (in een directory)
   2. `xlsx-loose` — losse XLSX-bestanden (in een directory)
   3. `xlsx-multi` — één multi-sheet XLSX
   4. `sqlite` — SQLite database (`.db` / `.sqlite`)
   5. `postgres` — één `.sql`-dump met PostgreSQL-dialect CREATE + INSERT
   6. `mssql` — één `.sql`-dump met Microsoft SQL Server dialect
3. Ask: **"Output-pad?"** (file for `xlsx-multi` / `sqlite` / `postgres` / `mssql`, directory for `csv-loose` / `xlsx-loose`).
4. Update the schema-YAML to include the chosen `output: {format, path}` block.
5. Run: `bash "${CLAUDE_SKILL_DIR}/scripts/run.sh" --schema /tmp/.../schema.yaml --output <path> --format <fmt>`
6. Report file paths + per-table row counts (the CLI prints these on stdout).

### Phase 6 — Save schema

Ask: **"Wil je dit schema opslaan voor herbruik? (geef een pad, of zeg `nee`)"**.

On a path: `cp /tmp/syntherklaas-<sessid>/schema.yaml <user-path>` and confirm with:
> "Volgende keer kun je het reproduceren met: `/syntherklaas <user-path>` — dan toon ik alleen een confirmatie en draai dezelfde generatie."

## Exit codes

- `0` — success
- `2` — schema/output/format problem (malformed YAML, unknown provider, FK to unknown column, output path conflict, Excel limit exceeded, ...)
- `3` — cyclic FK detected
- `4` — missing dependencies (`uv` not on PATH)

## Reference

- Pipeline modules in `scripts/`: `providers.py` (Faker + NL extras + numpy distributies), `schema.py` (YAML validator), `generate.py` (orchestrator + CLI), `writers.py` (dispatch), `sqlite_writer.py`, `xlsx_writer.py`, `fk_resolver.py` (topo-sort).
- Tests: `scripts/tests/` (run via `uv run pytest`).
- Worked example: `examples/demo-schema.yaml` (3-table klanten/orders/orderlines + distributies) + `examples/transcript.md` (session walkthrough).
