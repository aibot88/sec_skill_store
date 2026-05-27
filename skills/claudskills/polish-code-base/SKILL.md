---
name: polish-code-base
description: |
  Use this skill to walk through an existing code base and
  fix surface-level problems that are obvious on a careful
  read: typos, grammar mistakes in comments and strings,
  inconsistent naming or formatting, dead imports, stale
  references, broken links, mismatched casing, and small
  contradictions between neighboring files. Stay on the
  visible layer — do not refactor logic, do not run unit
  tests, and do not chase deep design issues. Apply each
  fix directly when it is obvious, and report borderline
  cases for the author to decide.
---

Walk the repository top-down: README, configuration files,
  then source directories in the order a newcomer would read
  them, so the polish covers the parts a reader sees first.

Read each file end-to-end before editing it; a typo in line
  three may be repeated in line forty, and a single pass
  catches both.

Fix obvious typos in comments, docstrings, log messages,
  error messages, commit-ready user-facing strings, and
  identifiers that are clearly misspelled (`recieve` →
  `receive`, `seperator` → `separator`).

Fix grammar mistakes in English prose embedded in code:
  subject-verb agreement, article use, tense consistency,
  and punctuation, without changing the author's voice.

Normalize trivial inconsistencies that have a single
  obvious answer: trailing whitespace, mixed line endings,
  tabs versus spaces inside one file, missing final
  newline, and inconsistent quote style inside one file.

Flag naming inconsistencies where the same concept appears
  under two spellings in the same module (`userId` and
  `user_id`, `Cancelled` and `Canceled`); fix only when the
  dominant spelling is unambiguous, otherwise report.

Remove dead imports, unused variables the linter has
  already flagged in comments, commented-out code older
  than the surrounding file, and `TODO` notes that
  reference resolved tickets or removed code.

Fix broken Markdown: unbalanced backticks, unclosed code
  fences, dead reference-style link definitions, headings
  that skip levels (H2 → H4), and link text that no longer
  matches the destination.

Fix broken links in README and docs when the target has a
  clear modern equivalent (`http://` → `https://` on a host
  that requires it, moved canonical URLs); leave genuinely
  dead links flagged for the author.

Align error and log messages with the project's existing
  convention when one is visible: no trailing period, single
  sentence, lowercase or sentence case as the rest of the
  file uses.

Fix obvious contradictions between a file and its immediate
  neighbors: a function renamed in the source but still
  referenced by its old name in a sibling comment, a
  constant changed in one place and stale in another, a
  CHANGELOG entry that disagrees with the version in the
  manifest.

Apply the fix in place when the correct answer is obvious
  and reversible; group related fixes per file in a single
  edit so the diff stays readable.

Report — do not silently change — anything that requires a
  judgment call: ambiguous renames, stylistic preferences
  the project has not committed to, two equally common
  spellings, or a comment that may be intentionally archaic.

Do not refactor logic, extract functions, rename public
  APIs, reorder methods, or restructure modules; the job
  is polish, not redesign.

Do not run unit tests, integration tests, or the full
  build; this skill targets the visible layer and trusts
  that a separate build pass will catch behavioral
  regressions.

Do not touch generated files, vendored dependencies,
  lock files, minified assets, fixture data captured from
  real systems, or any file marked `do not edit`.

Do not "improve" prose that is already correct; leave
  voice, tone, and word choice alone unless a rule above
  applies.

Do not batch-fix with `sed`, `awk`, or global
  search-and-replace across the whole repo; walk file by
  file so each change is read in context before it is
  saved.

When the same issue appears in many files (a misspelled
  word, a stale URL, a deprecated header), fix every
  occurrence in the same pass and list the affected files
  in the report, so the author sees the scope at a glance.

End with a short report: the files touched, the kinds of
  fixes applied, and a separate list of borderline cases
  left for the author to decide.
