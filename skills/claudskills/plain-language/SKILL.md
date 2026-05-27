---
name: plain-language
description: >-
  Use when asked to review project text for plain language compliance.
  Produces structured findings with rewrites. Triggers: plain language
  review, readability check, copy audit, make this clearer.
allowed-tools: Read Write Bash(scripts/scan-plaintext-files.sh:*) TaskCreate TaskGet TaskUpdate TaskOutput TaskList
---

# Plain Language Review

Review text files against the U.S. federal government Plain Language Guidelines (~30 rules across 6 categories) and produce a structured report of findings with concrete rewrites.

**Important: This skill produces a report. Do not modify any reviewed files.**

---

## Review Workflow

1. **Select files** — Use the user's specified files. If the user has not specified files or a project directory, ask them before proceeding — do not default to the current working directory. If none specified, run `scripts/scan-plaintext-files.sh <project-directory>` to discover all `.md`, `.mdx`, `.markdown`, `.txt`, `.rtf`, `.rst`, `.adoc`, `.org`, and `.wiki` files. The `<project-directory>` argument is **required** — it must be the root of the user's project (the repository being reviewed), NOT the skill's own directory.
2. **Load rules** — Read `references/rules-quick-ref.md` for the full rule checklist.
3. **Review files in parallel** — Spawn parallel sub-agents (via the Task tool — see Model & Effort Guidance for tier selection) to review files concurrently. Batch files into groups of 3–5 per sub-agent. Each sub-agent receives: the list of files to review, the rules from `references/rules-quick-ref.md`, and instructions to apply all rules, verify each rewrite resolves the flagged violation without introducing new ones, and produce findings in the Output Format below. Run up to 5 sub-agents concurrently. Once all complete, collect their findings. If a sub-agent fails, log the error and continue — do not block the rest of the review.
4. **Collect and deduplicate findings** — Gather findings from all sub-agents. Remove exact duplicates if file batches overlapped. For each finding, verify the rewrite resolves the flagged rule violation and does not introduce new violations.
5. **Classify severity** — Use `references/severity-rubric.md` to assign high/medium/low.
6. **Assemble report** — Write findings to `.agents/plain-language/plain-language-findings-YYYYMMDD.md` (create the directory if it doesn't exist; use today's date). Group findings by file, then by severity (high first). End with the summary block.

---

## Model & Effort Guidance

| Task | Model tier | Rationale |
|------|-----------|-----------|
| File discovery (script) | None — run `scripts/scan-plaintext-files.sh` | Deterministic shell script; no model needed. |
| File-review sub-agents | Fast cheap model (e.g. Claude Haiku 4.5, Gemini Flash 2.5) | Rule application is structured pattern matching against a fixed checklist. |
| Orchestration, rewrite verification, severity classification | Capable reasoning model (e.g. Claude Sonnet 4.5, Gemini 2.5 Pro) | Judgment tasks: deduplication, severity calls, cross-finding coherence. |

---

## Output Format

Use this exact structure for each finding:

```
## [file path]

### Finding [N] — [Rule name] (severity: [high|medium|low])
- **Line [N]:** "[original text]"
- **Guideline:** [One-sentence explanation of the rule violated]
- **Suggested:** "[concrete rewrite]"
```

**Example:**

```
## docs/getting-started.md

### Finding 1 — Use simple words (severity: medium)
- **Line 14:** "In order to utilize the configuration module..."
- **Guideline:** Replace complex words with simple alternatives — "utilize" → "use", "in order to" → "to"
- **Suggested:** "To use the configuration module..."

### Finding 2 — Use active voice (severity: high)
- **Line 23:** "The database will be initialized by the setup script."
- **Guideline:** Make the actor the subject of the sentence
- **Suggested:** "The setup script initializes the database."
```

If a file has no findings, omit it from the report entirely — do not include a "no issues found" entry. The summary's "Files reviewed" count should still include it.

End the report with a summary:

```
## Summary
- **Files reviewed:** [N]
- **Total findings:** [N] ([N] high, [N] medium, [N] low)
- **Top issues:** [List the 2-3 most frequent rule violations]
```

---

## When to Load Reference Files

Load references on demand to conserve context:

| File | When to load |
|------|-------------|
| `references/rules-quick-ref.md` | Always — load at start of every review |
| `references/word-substitutions.md` | When reviewing word choice in any finding |
| `references/active-voice-guide.md` | When you detect passive voice patterns (forms of "to be" + past participle) |
| `references/before-and-after-examples.md` | When a rewrite requires restructuring (sentence split, list conversion, undoing a hidden verb, or reorder) rather than a simple word swap |
| `references/severity-rubric.md` | When classifying findings — consult definitions and examples |

---

## Scope Rules

- **Review:** prose in `.md`, `.mdx`, `.markdown`, `.txt`, `.rtf`, `.rst`, `.adoc`, `.org`, `.wiki` files; UI strings; error messages
- **Skip:** code inside fences/backticks, variable names, import statements, configuration values, URLs, file paths
- **Preserve technical terms** — flag jargon only when a simpler alternative exists without losing precision
- **Do not modify reviewed files** — produce recommendations only
- Plain-language review checks how text reads, not whether its claims about the code are accurate. For docs/code drift detection (does this README command still exist?), see `tidy-project`'s Phase 1 docs drift reviewer.

---

## Gotchas

- Do not review files inside this skill's own directory — always use the user's project root, not the skill directory.
- Do not flag technical terms that have no simpler equivalent — precision beats plainness.
- Do not review text inside code fences, backticks, or inline code spans — only prose.
- A file with zero findings is still counted in "Files reviewed" — do not omit it from the summary count.
