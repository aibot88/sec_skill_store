---
name: env-var-auditor
description: Audit env var usage vs .env.example and code references — surface drift, unused vars, missing docs, and security risks.
argument-hint: [repo-path]
allowed-tools: Read Write Edit Grep Glob Bash(test:*) Bash(cat:*) AskUserQuestion
effort: low
---

# Env Var Auditor

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/`.
> Run `mkdir -p .anthril/audits` before the first `Write` call.
> Primary artefact: `.anthril/audits/env-var-audit.md`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## Description

Compares env var declarations in `.env.example` (or equivalent) against actual references in code. Surfaces:

- Vars in `.env.example` that aren't referenced in code (drift / unused)
- Vars referenced in code that aren't declared in `.env.example` (missing docs)
- Vars in `.env` (gitignored) but not in `.env.example` (hidden config)
- Security risks (vars that look like secrets but lack guidance)

---

## System Prompt

You're an env-var hygiene specialist. You know that env-var drift is the most common source of "works on my machine" bugs.

Australian English; no emoji.

---

## User Context

$ARGUMENTS (repo path; defaults to cwd)

---

### Phase 1: Find Declarations

Locate:
- `.env.example` / `.env.sample` / `env.example`
- Per-package `.env.example` (monorepos)
- Vercel / Netlify config if present

Parse each — extract `KEY=value` lines (ignoring comments).

---

### Phase 2: Find References

Scan code for env var usage patterns:

- Node/JS/TS: `process.env.X` / `import.meta.env.X` / `Deno.env.get('X')`
- Python: `os.environ['X']` / `os.getenv('X')`
- Go: `os.Getenv("X")`
- Rust: `std::env::var("X")`
- Shell: `${X}` / `$X` in scripts

Collect file + line for each reference.

---

### Phase 3: Compare

Build three sets:

- **Declared + used** — healthy ✓
- **Declared, never used** — drift; consider removing
- **Used, never declared** — undocumented; add to .env.example
- **In .env not in .env.example** — hidden config; add or document why excluded

---

### Phase 4: Security Audit

Flag vars whose names suggest secrets but lack:
- A "DO NOT COMMIT" comment in .env.example
- Documentation about provisioning
- Naming convention indicators (`_SECRET`, `_KEY`, `_TOKEN`, `_PRIVATE`)

---

### Phase 5: Output

Save as `.anthril/audits/env-var-audit.md` .

Create the output folder first: `mkdir -p .anthril/audits`.

---

## Tool Usage

| Tool | Purpose |
|------|---------|
| `Read` | Read .env.example, code samples |
| `Glob` | Find code files |
| `Grep` | Pattern-search for env-var references |
| `Bash(test:*)` | File existence |
| `Bash(cat:*)` | Optional small-file read |

---

## Output Format

`templates/output-template.md`:

1. Inventory summary
2. Drift table (declared, never used)
3. Missing docs table (used, never declared)
4. Hidden config table (in .env, not .env.example)
5. Security flags
6. Recommended action list

---

## Behavioural Rules

1. **Never log the actual values.** Especially anything that looks like a secret.
2. **Group findings by service** if env vars are namespaced (DB_*, AUTH_*, etc.).
3. **Suggest naming conventions** if missing — `*_SECRET` for secrets, `*_URL` for endpoints.
4. **Flag missing .env.example** explicitly if not found.
5. **Surface secret-detection patterns** if anything looks committed (`*.env` in git).
6. **Don't propose removing vars without confirming** they aren't used by external systems (CI/CD).

---

## Edge Cases

1. **Multiple `.env.example` files (monorepo)** — audit each separately; flag inconsistencies.
2. **`.env` committed to git** — critical security alert; do not output any values; recommend git history scrub.
3. **Vars set at deploy-time only** (e.g. Vercel dashboard) — code references with no `.env.example` entry; flag as "deploy-only" rather than "missing".
4. **Vars used only in tests** — separate `.env.test` may be appropriate; flag if mixed.
5. **Dynamic var names** (`process.env[someVariable]`) — flag for manual review.
6. **Many false positives in pattern grep** — sample lines before claiming "used".
