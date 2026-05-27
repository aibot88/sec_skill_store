---
name: query-writeback
description: "Answer cross-source questions about an open-llm-wiki vault and optionally write reusable synthesis back into concept pages. Use when the user asks a wiki question that requires comparing, connecting, or tracing multiple source/concept pages. By default answer first and propose writeback; modify files only when the user explicitly asks for writeback, pre-authorizes wiki growth, or approves the proposed changes."
license: MIT
metadata:
  version: "0.3.0"
  reviewed-for: "Claude Code Skills quality"
---

# Query Writeback

Use the wiki to answer synthesis questions, then preserve high-value synthesis
only when file changes are authorized.

## Runtime Tools

Use deterministic scripts when available:

- `wiki_search.py` to find relevant source and concept pages
- `wiki_writeback.py` to produce a reviewable diff before changing files
- `wiki_lint.py` after approved writeback

Example:

```bash
python scripts/wiki_search.py "<vault>" "<query>" --limit 8
python scripts/wiki_writeback.py "<vault>" --target concepts/<page>.md --query "<query>" --body-file <draft.md>
```

## Trigger Boundary

Use this skill for questions that require cross-source synthesis:

- relationships between concepts
- comparisons across papers
- timelines or evolution paths
- recurring questions that would benefit from a reusable concept note

Do not use it for simple factual lookup, casual chat, non-wiki topics, or
questions where a single source page already gives the answer.

## File-Safety Boundary

- Read from the resolved wiki vault only.
- Answering is read-only by default.
- Writeback requires explicit user approval unless the current instruction has
  already authorized automatic wiki growth.
- Before writing, show the target files and a short summary of the proposed
  additions.
- Never rewrite a whole concept page when a targeted insertion is enough.
- Never update `sources/` or QA reports from this skill. Use `wiki-ingest` for
  source changes.
- Always append a `log.md` entry for approved writeback.

## Workflow

### 1. Resolve Scope

Read `SCHEMA.md`, `index.md`, and relevant concept/source pages. Identify:

- concepts involved
- source pages cited
- relationships being tested
- gaps or missing evidence

### 2. Assess Coverage

Use this decision table:

| Verdict | Condition | Action |
| --- | --- | --- |
| `FULL` | wiki has enough cited material | answer from wiki |
| `PARTIAL` | related pages exist but evidence is incomplete | answer with caveats and list gaps |
| `NONE` | wiki lacks relevant material | say what is missing and suggest ingest |

Do not trigger ingestion automatically. If new sources are needed, propose a
separate `wiki-ingest` run.

### 3. Answer

Answer in normal prose and cite wiki pages with `[[LLM-NNNN]]` or
`[[concept-name]]`. Label inference when a relationship is not explicitly stated
by a source.

### 4. Decide Whether Writeback Is Valuable

Propose writeback when at least one is true:

- the answer cites three or more source pages
- the answer contains a comparison table or timeline
- the answer connects two concepts not currently linked
- the question is likely to recur
- the answer identifies a durable gap or contradiction marker

Single-source details and speculative answers usually should not be written
back.

### 5. Self-Check Before Writeback

Check every relational claim:

- explicit in source: write as fact with citation
- implied but not stated: label as inference
- guessed from chronology or similarity: do not write as a claim

Every paragraph added to a concept page needs at least one citation. Do not
write unsupported synthesis.

### 6. Execute Approved Writeback

When writeback is approved:

1. Prefer updating an existing concept page.
2. Create a new concept page only when no existing concept fits.
3. Add frontmatter for new concept pages using `templates/concept-template.md`.
4. Add bidirectional links when useful.
5. Update `index.md` if a new concept page is created.
6. Append to `log.md`:
   `[YYYY-MM-DD HH:MM] query-writeback | concepts/<page>.md | agent | query: "<original question>"`

Mark writeback-derived sections with:

`query-derived: YYYY-MM-DD`

If `wiki_writeback.py` is available, use it to produce the diff first. Apply
only after approval or pre-authorization.

## Completion Criteria

Finish with:

- direct answer to the user's question
- citations used
- whether writeback was skipped, proposed, or completed
- changed files if writeback happened
- lint result after writeback when runtime tools are available
- remaining gaps that require future ingest
