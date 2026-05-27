---
name: run-spec-audit
description: >-
  Run a spec-vs-code audit on this codebase. Compare actual implementation in
  app/, lib/, lib/typeorm/, typeorm/, and tests against project
  specifications in docs/. Report only defects with exact file and line
  citations, classified as MISSING, DIVERGENT, UNDOCUMENTED, or PHANTOM. Use
  when asked to audit code against specs, find spec divergence, run a Council
  of Three audit, check doc-code consistency, verify lifecycle/transition/
  report/MCP behavior matches documentation, run spec compliance, code-vs-docs
  check, or audit lifecycle.
---

# Spec Audit

Act as the Tester. Compare actual code against project specifications
and report only defects with exact file and line citations.

## Tool Restrictions

This skill is **read-only**. Use only:

- `grep`, `glob`, `view` for searching and reading files.
- `bash` for read-only commands (e.g. `cat`, `head`, `wc`, `find`, `ls`,
  `git log`, `git show`, `git diff`).

Do **not** use `edit`, `create`, or any write/delete tools. Do not
modify any files during the audit.

## Pre-Flight Check

Before starting the audit:

1. Verify all context files listed below exist. Use `glob` or `ls`.
2. For any missing file, note it in the output header and skip
   references to it.
3. Create the output directory `tests/quality/spec_audits/` if it
   does not exist (this is the only permitted write).

## Scope Narrowing

If the user specifies a subsystem (e.g. "audit MCP only", "audit
lifecycle"), limit scrutiny to the relevant areas and context files.
Skip unrelated scrutiny areas and spec documents. State which areas
were included and which were skipped in the output header.

## Context Files To Read

Read these specification documents first:

1. `README.md`
2. `tests/quality/QUALITY.md`
3. `docs/lifecycle-workflow.md`
4. `docs/version-lifecycle-dates.md`
5. `docs/requirements-ui-behaviour.md`
6. `docs/reports.md`
7. `docs/admin-center.md`
8. `docs/mcp-server-user-guide.md`
9. `docs/mcp-server-contributor-guide.md`
10. `docs/database-schema.md`
11. `docs/arkitekturbeskrivning-kravhantering.md`
12. `AGENTS.md`
13. `docs/developer-mode-overlay.md`
14. `docs/reference-data-and-ai.md`
15. `docs/sql-server-developer-workflow.md`

Then read the actual code in `app/`, `lib/`, `lib/typeorm/entities/`,
`typeorm/`, and `tests/quality/functional.test.ts`.

Also read `./references/integration-contracts.md` (relative to the skill folder)
for the authoritative REST and MCP field schemas used by scrutiny areas 8–10.

## Requirement Confidence Tiers

Tag every finding with `[Req: tier — source]`. Weight by tier:

- **formal** — written by humans in `docs/` or `README.md`. Divergence
  is a real finding.
- **user-confirmed** — stated explicitly by the user in the current
  thread. Authoritative unless contradicted by stronger evidence.
- **inferred** — deduced from current behavior or defensive code.
  Report divergence as `NEEDS REVIEW`, not as a definitive defect.

## Rules

- ONLY list defects. Do not summarize what matches.
- For EVERY defect, cite exact file and line number(s).
- If you cannot cite a line number, do not include the finding.
- Before claiming something is missing, grep the codebase and **show
  the grep command and its result** proving absence.
- Before claiming something exists, read the actual function body and
  **quote both the spec line and the code line**.
- Classify each finding as `MISSING`, `DIVERGENT`, `UNDOCUMENTED`, or
  `PHANTOM`.
- For findings against inferred requirements, add `NEEDS REVIEW`.
- Locate functions by grepping for their name. Do not rely on
  hardcoded line numbers from previous audits or from this skill's
  scrutiny areas — line numbers shift as the code evolves.
- Treat each `tests/quality/QUALITY.md` fitness-to-purpose scenario
  as a mandatory audit checkpoint. For every scenario, verify the
  cited code location still matches the described behavior.
- Apply the coverage-theater-prevention list from QUALITY.md. If a
  test matches one of those anti-patterns, flag it as `PHANTOM`
  coverage in the findings.
- If a finding touches a Human Gate topic (business meaning of
  statuses, authorization policy, Swedish/English terminology, report
  column expectations), tag it `NEEDS HUMAN GATE` in addition to the
  classification.

## Defect Classifications

- **MISSING** — Spec requires it, code does not implement it.
- **DIVERGENT** — Spec and code both address it, but they disagree.
- **UNDOCUMENTED** — Code does it, the docs do not mention it.
- **PHANTOM** — The docs describe something materially different from
  what is actually implemented.

## Severity Levels

Assign a severity to each finding:

- **CRITICAL** — Security vulnerability or data-loss risk.
- **HIGH** — Wrong behavior visible to users or downstream systems.
- **MEDIUM** — Edge case, partial implementation, or inconsistency.
- **LOW** — Cosmetic, documentation gap, or naming mismatch.

Sort findings by severity (CRITICAL first, LOW last).

## Finding Cap

If more than 30 findings are discovered, report only the top 30 by
severity. At the end, note the total count and how many lower-severity
findings were omitted.

## Project-Specific Scrutiny Areas

See `references/scrutiny-areas.md` for the full list of
project-specific areas to examine.

## Output Format

```md
### path/to/file.ext
- **Line 123:** [MISSING / DIVERGENT / UNDOCUMENTED / PHANTOM]
  [Severity: HIGH] [Req: tier — source] Description.
  Spec says: ...
  Code does: ...
  Evidence: `grep -rn "functionName" lib/` → no matches
```

## Summary Table

End every audit with a summary table:

```md
## Summary

| # | File | Classification | Severity | One-line |
|---|------|---------------|----------|----------|
| 1 | lib/dal/requirements.ts | DIVERGENT | HIGH | ... |
| 2 | lib/mcp/server.ts | MISSING | MEDIUM | ... |
```

## Self-Audit Step

After completing the spec-vs-code audit, audit this skill itself
for relevance:

1. List all `docs/*.md` files in the repo. Flag any doc not in the
   context-files list that could be relevant to spec compliance.
2. List key code directories (`app/`, `lib/`, `lib/typeorm/`,
   `typeorm/`, `components/`). Flag new top-level modules or DAL files
   not covered by the scrutiny areas.
3. Check `references/scrutiny-areas.md` for stale file paths or
   function names that no longer exist.
4. Compare `tests/quality/QUALITY.md` scenario count and IDs against
   `references/scrutiny-areas.md` entries. Flag:
   - New QUALITY.md scenarios that have no matching scrutiny area.
   - Scrutiny areas that reference removed or renumbered scenarios.
   - Coverage-target subsystems in QUALITY.md that no longer match
     the actual project structure.
5. Report self-audit findings in a separate section:

```md
## Skill Self-Audit

| # | Issue | Suggestion |
|---|-------|------------|
| 1 | `docs/new-feature.md` exists but is not in context list | Add to context files |
| 2 | `lib/dal/new-module.ts` not covered by scrutiny areas | Add scrutiny area |
| 3 | Scrutiny area 5 references `deviations.ts:500-693` but function starts at line 520 | Update reference |
```

Do not auto-apply self-audit suggestions. Report them for the user
to approve.

## After The Audit

Save raw output to `tests/quality/spec_audits/YYYY-MM-DD-[model].md`.

## Companion Protocols

- **Runtime verification:**
  `npm run test:integration` — runs Playwright integration tests
  against the live app with seeded data. Use after a spec audit to
  verify findings at runtime. Also runs in CI.
- **Field contracts:**
  `./references/integration-contracts.md` — extracted field schemas
  from the integration protocol, used by scrutiny areas 8–10.

For Council of Three multi-model audits, see
`./references/council-of-three.md` (relative to the skill folder).
