---
name: wiki-review
description: >
  Arbitrates proposed wiki additions accumulated under
  `briefs/wiki-proposals/`. Walks each proposal with the human, asks
  merge / rewrite / discard / defer. Uses `.claude/.wiki-review-active`
  sentinel to authorise wiki/ writes during the session — the
  `block_wiki_write.py` PreToolUse hook detects the sentinel and allows
  the write. The single legitimate path through the wiki gate.
  Use when the user says "wiki review", "merge proposals", "review wiki
  proposals", or "/wiki-review".
---

# Wiki review — merge proposals into the wiki

The `wiki/` directory is the project's source of truth and is **gate-locked**
by the `block_wiki_write.py` PreToolUse hook. This skill is the single
legitimate path that bypasses the gate.

## Prerequisites

- A `wiki/` directory exists at the project root (the hook only fires
  on writes targeting `wiki/**`).
- One or more proposal files under `briefs/wiki-proposals/*.md` with
  frontmatter declaring `target:` (the wiki path they should land at).

If no proposals exist, exit with a one-line message: *"No proposals in
`briefs/wiki-proposals/`. Nothing to review."*

## Workflow

### Step 1 — Inventory

List `briefs/wiki-proposals/*.md`. Skip:
- `README.md`
- Files starting with `EXAMPLE-`
- Subdirectories (e.g. `archive/`)

Report the count to the human: *"N proposals to review."*

### Step 2 — Walk each proposal

For each proposal, in chronological order (filename starts with date):

1. **Read the proposal**. Extract `target:` from frontmatter (the wiki
   path it should land at) and the body.
2. **Show a one-paragraph summary** to the human (target path + 2-3
   sentence gist of the proposal).
3. **Ask**: *merge as-is* / *rewrite* / *discard* / *defer* ?
4. Branch on the answer (Step 3, 4, 5, or 6).

### Step 3 — Merge as-is

1. **Create the sentinel**: `touch .claude/.wiki-review-active` (an
   empty file is enough — the hook checks existence, not content).
2. **Write the proposal body** to the target wiki path declared in
   the frontmatter. Create parent directories if needed.
3. **Delete the proposal file** from `briefs/wiki-proposals/`.
4. **Remove the sentinel**: `rm .claude/.wiki-review-active`.

If the write fails or the user interrupts mid-merge: still remove the
sentinel before exiting. A leftover sentinel disables the gate for the
next session.

### Step 4 — Rewrite

Ask the human for the changes (which sections, what tone, what to cut).
Apply them to the proposal body in memory. Then proceed with Step 3
(merge the rewritten version, delete the original proposal).

### Step 5 — Discard

Delete the proposal file. Do not write to `wiki/`. Move on.

### Step 6 — Defer

Leave the proposal in place. Move on to the next.

### Step 7 — End of run

After the last proposal:

1. **Verify** `.claude/.wiki-review-active` does not exist. Remove it
   if it does — its presence outside an active run is a bug that
   silently disables the wiki gate.
2. **Report** to the human: *"N merged, M rewritten, K discarded, L
   deferred."*

## Why this gate exists

Direct writes to `wiki/**` are blocked by `block_wiki_write.py`. The
wiki is the project's long-term memory: every entry must be reviewed
by a human before it lands. Agents that learn something new propose
via `briefs/wiki-proposals/YYYY-MM-DD-<slug>.md`; the human merges
during `/wiki-review`.

## Gotchas

- **Never leave the sentinel in place** outside an active run. If the
  skill exits mid-flight (crash, ctrl-c), the sentinel persists and
  disables the gate until manually removed.
- **One sentinel for the whole session, not per proposal**. Create it
  before the first merge, remove it after the last. Avoids touch/rm
  churn on N proposals.
- **Frontmatter `target:` is required**. If a proposal lacks it, ask
  the human where it should land before writing — don't guess.
- **Discard is irreversible** in this skill. The proposal file is
  deleted with no archive. If you want history, use defer instead.

**STOP.** Your deliverables: zero or more wiki entries created, plus
the proposal files cleaned up.
