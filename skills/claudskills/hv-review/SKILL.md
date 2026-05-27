---
name: hv-review
description: Staff-engineer review of a feature branch before merge or PR — reads commits, diff, referenced item IDs, and matching KNOWLEDGE.md topics; dispatches an Opus reviewer that checks intent match, convention compliance, and quality. Returns PASS / CONCERNS / FAIL. Use on "review this", "check before I ship", "look over the branch", or implicitly from /hv-ship.
user-invocable: true
---

**Print the banner below (including the code fences) to the user verbatim before any other action. Skip if dispatched as a subagent.**

```
════════════════════════════════════════════════════════════════════════
  🔍  hv-review  ·  staff-engineer review of a branch
  triggers: "review this", "check before ship"  ·  pairs: hv-ship
════════════════════════════════════════════════════════════════════════
```

# hv-review — Pre-Merge Review

## Configuration

Read `.hv/config.json`:

- `models.orchestrator` — model for the reviewer (default `opus`)

## When to Use

- Before merging or opening a PR — typically invoked from `/hv-ship`
- *"Review this branch"*, *"Second-opinion this"*, *"Look over what I've got"*
- After manual commits to a branch you want validated before integrating

## When NOT to Use

- Code is still in flight → finish implementing via `/hv-work`
- You want to change code based on the review → `/hv-refactor` or a fresh `/hv-work` run
- Nothing committed yet → there's nothing to review

## Step 1 — Preflight

```bash
.hv/bin/hv-preflight
```

See `docs/reference/preflight.md` for exit-code handling.

## Step 2 — Scope the Review

```bash
.hv/bin/hv-review-scope <branch>
```

If the user didn't name a branch, default to the current one. `hv-review-scope` emits JSON with:

- `branch`, `base`, `commitCount`
- `commits` — array of `{hash, subject}`
- `touchedFiles` — paths changed vs base
- `referencedIds` — `[B##]`/`[F##]`/`[T##]` found in commit messages
- `intents` — matched TODO entries for each referenced ID

If `commitCount` is 0, stop and tell the user.

## Step 3 — Consult KNOWLEDGE & DECISIONS

Read the `hv-knowledge` block in `CLAUDE.md` to see available topics. Pick topics that plausibly touch the changed areas based on `touchedFiles` and commit subjects — infer liberally (e.g., a file under `Networking/` → the `Networking` topic). Then query both stores for those topics:

```bash
.hv/bin/hv-knowledge-query "Topic A" "Topic B"
.hv/bin/hv-decisions-query "Topic A" "Topic B"
```

Carry KNOWLEDGE bullets into the reviewer brief. Pass DECISIONS entries under a `**Hard boundaries:**` section — the reviewer must **FAIL** if the diff violates any boundary, even if the change looks otherwise good.

## Step 4 — Capture the Diff

The reviewer needs concrete diff content, not just file names. For each touched file (up to ~8 — more than that, ask the user which to focus on):

```bash
git diff <base>...<branch> -- <file>
```

**Issue all the per-file `git diff` calls in parallel** — they're independent and serial calls add up fast on bigger branches. Keep a per-file diff map in memory for the reviewer brief.

## Step 5 — Dispatch the Reviewer

Dispatch a single review agent using the **orchestrator** model. Brief template:

```
Review the feature branch `<branch>` against base `<base>` before merge.

**Commits:**
<hash> <subject>
<hash> <subject>
...

**Items being resolved:**
- [B07] Timer badge shows stale duration — "<full intent line from TODO>"
- [F03] Quick-switch projects — "<full intent line from TODO>"

**Relevant project conventions (from KNOWLEDGE.md):**
- <bullet 1>
- <bullet 2>

**Hard boundaries (from DECISIONS.md):**
<entries from hv-decisions-query, if any — full rule + forbids/permits>

**Diff by file:**
<file>
```diff
<diff content>
```
...

**Evaluate on three axes. For each, return PASS / CONCERN / FAIL with evidence.**

1. **Intent match** — does the diff deliver what the TODO entries promise? Anything missing, anything scope-creeping?
2. **Convention compliance** — does the diff respect the bullets from KNOWLEDGE.md? Any regressions on captured gotchas?
3. **Obvious quality** — dead code, error swallowing, untested new branches, security smells, API contract breaks, performance cliffs. Not a full code review; focus on things the user would regret after merge.
- **Decision violations.** Compare the diff against the `**Hard boundaries:**` block above. Any forbidden pattern present in the diff = FAIL.

Return verdict as three labeled sections. Be specific: file:line for every concern. Rank concerns by severity.

**Final verdict** (on the last line, all caps): PASS | CONCERNS | FAIL
- PASS — no concerns worth surfacing
- CONCERNS — works, but surfaces should be flagged before merge
- FAIL — merge would regress behavior, break intent, or violate a project convention
```

## Step 6 — Relay the Verdict

Present the reviewer's output **verbatim** (or nearly so — trim only restatements). Don't summarize away the evidence; specifics are the point.

Structure:

```
Review: `hv/foo` → main (3 commits, 5 files)

### 1. Intent match — PASS
<evidence>

### 2. Convention compliance — CONCERN
- src/Foo.swift:42 — uses raw URLSession; KNOWLEDGE says all network calls go through NetworkClient
- ...

### 3. Obvious quality — PASS
<evidence>

Verdict: CONCERNS
```

## Step 7 — Route Based on Verdict

The verdict is the entire product — return it and stop. Never ask a follow-up; the caller (the user, or `/hv-ship` when invoked) owns what happens next.

- **PASS** — tell the user *"Ready to ship. Run `/hv-ship`."*
- **CONCERNS** — print the concerns inline (already done in Step 6) and suggest the next move: *"Address via `/hv-work` and rerun `/hv-review`, or accept and ship via `/hv-ship`."* When invoked from `/hv-ship`, return the verdict; the parent owns the question (see `/hv-ship` Step 3).
- **FAIL** — tell the user the merge would regress. Suggest fixing via `/hv-work` or `/hv-debug`. Don't route to `/hv-ship`.

## Rules

- **Read-only.** Never edit, commit, or stage. The verdict is the entire product.
- **Evidence over opinion.** Every concern must cite file:line or commit hash.
- **Scope is bounded.** Only the diff against the base is reviewed — don't wander into unchanged code.
- **Call it honestly.** If conventions were violated but the user has a good reason, the reviewer still reports CONCERN — the user decides what to do.
- **Don't re-run on a passed branch.** If the same scope was just reviewed in the session and came back PASS, skip Step 5 and report the cached verdict.
