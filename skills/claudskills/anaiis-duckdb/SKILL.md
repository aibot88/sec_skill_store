---
name: anaiis-duckdb
description: Ad hoc SQL analytics on local parquet, CSV, Excel, JSON, Avro, or SQLite files — auto-triggers on data analysis requests
---

# DuckDB Analytics

Run ad hoc SQL analytics on local and remote structured data files using the DuckDB CLI.

## When to use this skill

- Analyzing, querying, or exploring local parquet, CSV, Excel, JSON, Avro, or SQLite files
- Inspecting schema, row counts, or column distributions
- Joining, aggregating, or filtering across multiple files or formats
- Data exported from BigQuery or other systems for local analysis
- Any structured data query where Python would require loading the file into memory

## Tool selection rules

| Task | Tool |
|---|---|
| SQL aggregations, joins, filters, window functions | DuckDB CLI |
| Reading parquet, CSV, JSON, Avro, Excel, SQLite natively | DuckDB CLI |
| Glob patterns across multiple files | DuckDB CLI |
| Remote file access (S3, GCS, HTTP) | DuckDB CLI with httpfs |
| Writing results to parquet or CSV | DuckDB CLI |
| Plotting (matplotlib, plotly, seaborn) | Python |
| ML pipelines, sklearn, feature engineering | Python |
| Complex control flow or custom transforms | Python |

**Never** load a multi-GB file into pandas with `pd.read_parquet()` or `pd.read_csv()`. DuckDB reads all supported formats natively with streaming/out-of-core execution.

Before using the `duckdb` Python package, check if it is installed:

```bash
pip list | grep duckdb
```

If not installed, default to the CLI rather than installing without asking.

## Performance context

DuckDB is the default engine regardless of file size. For single-file CSV/parquet under ~50MB, Python's `csv` module is marginally faster (3x on a 1.7MB file), but that difference is noise compared to LLM round-trip latency. Use DuckDB for SQL ergonomics, multi-format support, and out-of-core execution on large files.

Use Python only for plotting, ML pipelines, or tasks that genuinely need control flow.

## Standard workflow

### 1. Check file size

```bash
ls -lh path/to/file
```

- Under ~100MB: safe to preview with `SELECT * LIMIT 10`
- Over 100MB: use column projections, filters, and aggregations; avoid `SELECT *` without `LIMIT`
- Multiple files: use glob patterns (see below)

### 2. Introspect schema before querying

Parquet:
```bash
duckdb -c "DESCRIBE SELECT * FROM 'path/to/file.parquet';"
duckdb -c "SELECT COUNT(*) FROM 'path/to/file.parquet';"
```

CSV (auto-detect schema):
```bash
duckdb -c "DESCRIBE SELECT * FROM read_csv_auto('path/to/file.csv');"
duckdb -c "SELECT * FROM read_csv_auto('path/to/file.csv') LIMIT 5;"
```

JSON:
```bash
duckdb -c "DESCRIBE SELECT * FROM read_json_auto('path/to/file.json');"
duckdb -c "SELECT * FROM read_json_auto('path/to/file.json') LIMIT 5;"
```

Excel:
```bash
duckdb -c "INSTALL spatial; LOAD spatial;"
duckdb -c "SELECT * FROM st_read('path/to/file.xlsx') LIMIT 5;"
```

Avro:
```bash
duckdb -c "SELECT * FROM 'path/to/file.avro' LIMIT 5;"
```

SQLite (attach and query):
```bash
duckdb -c "ATTACH 'path/to/file.db' AS src (TYPE SQLITE); SHOW TABLES;"
duckdb -c "ATTACH 'path/to/file.db' AS src (TYPE SQLITE); SELECT * FROM src.table_name LIMIT 5;"
```

### 3. Query patterns

**Prefer heredoc multi-statement blocks** over multiple sequential `-c` calls. Each `-c` invocation is a subprocess round-trip; batching into a single heredoc runs all statements in one pass and minimizes latency.

One-shot query:
```bash
duckdb -c "SELECT col, COUNT(*) FROM 'file.parquet' GROUP BY col ORDER BY 2 DESC LIMIT 20;"
```

JSON output for piping to jq:
```bash
duckdb -json -c "SELECT col, COUNT(*) FROM 'file.parquet' GROUP BY col;" | jq '.[]'
```

Multiple files via glob:
```bash
duckdb -c "SELECT * FROM 'data/*.parquet' LIMIT 10;"
duckdb -c "SELECT COUNT(*) FROM 'exports/2024-*.parquet';"
```

Multi-statement heredoc (preferred for 2+ queries -- single subprocess, no round-trips):
```bash
duckdb <<'SQL'
CREATE TABLE t AS SELECT * FROM 'file.parquet';
SELECT column_name, column_type FROM information_schema.columns WHERE table_name = 't';
SELECT COUNT(*), AVG(value_col) FROM t WHERE condition;
SQL
```

Cross-format join:
```bash
duckdb <<'SQL'
CREATE TABLE a AS SELECT * FROM 'file.parquet';
CREATE TABLE b AS SELECT * FROM read_csv_auto('file.csv');
SELECT a.id, a.col1, b.col2 FROM a JOIN b ON a.id = b.id LIMIT 20;
SQL
```

### 4. Export results

```bash
duckdb -c "COPY (SELECT col, COUNT(*) FROM 'file.parquet' GROUP BY col) TO 'output.csv' (HEADER, DELIMITER ',');"
duckdb -c "COPY (SELECT * FROM 'file.parquet' WHERE condition) TO 'filtered.parquet' (FORMAT PARQUET);"
```

## Guardrails

- Do not create persistent `.duckdb` database files unless the user explicitly asks. Use in-memory mode (no db path argument).
- Do not install Python packages (`duckdb`, `pandas`, `pyarrow`) without asking.
- Do not use `SELECT *` without `LIMIT` on files over 100MB.
- Prefer heredoc batching over multiple `-c` calls whenever 2 or more queries target the same data.
- Query discipline (purpose classification, column selection, re-query prevention): follow `rules/duckdb.md`.

## Output format

- Small result sets (under 20 rows): render as a markdown table.
- Large result sets: show the query used and a prose summary of findings.
- Schema introspection: show as a table with column name, type, and nullable.
