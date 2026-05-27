---
name: code-panel-review
description: |
  Run a multi-agent "panel review" of the user's local code changes before they open a PR.
  Orchestrates five specialized reviewer agents (Security, Performance, Resilience, Bugs,
  Compliance) via the GitHub Copilot SDK, collects their JSON findings, and synthesizes a
  consolidated, deduplicated, severity-ranked report. Use when the user wants a pre-PR review of their own uncommitted or
  unpushed changes. Trigger phrases include: "run the panel on this", "panel review my changes",
  "review my changes before I push", "pre-PR review", "run a code panel review".
  Do NOT use for: reviewing already-merged code, reviewing someone else's PR, quick single-file
  questions, or style/lint-only requests.
---

# Code Panel Review

Orchestrate five specialized reviewer agents against the user's local changes and synthesize
their findings into a single severity-ranked report.

## Prerequisites (one-time)

- User must have authenticated the GitHub Copilot CLI: `copilot auth login`.
  The SDK reads OAuth credentials from the OS keychain (or `COPILOT_GITHUB_TOKEN` /
  `GH_TOKEN` / `GITHUB_TOKEN` if set).
- A GitHub Copilot subscription is required (this skill does NOT use BYOK in v1).
- Node.js 24+ available on PATH.

If the toolkit reports an auth error, tell the user to run `copilot auth login` and retry.

## Procedure

### Phase 1 — Resolve the review scope

Run these checks in parallel:

```bash
# committed-but-unpushed commits (the default scope)
git log --oneline @{upstream}..HEAD 2>/dev/null || git log --oneline ^origin/HEAD HEAD 2>/dev/null
# staged changes
git diff --cached --name-only
# unstaged (working tree) changes
git diff --name-only
# untracked files not covered by .gitignore
git ls-files --others --exclude-standard
```

**Before asking the user anything, filter every bucket through the default excludes**
(see Phase 2 for the full default-exclude list, including `**/.gitignore` and
`**/yarn.lock`). Files that would be excluded by default must not appear in the counts
or lists shown to the user — otherwise you're asking them to decide on files that will
never reach an agent. The only exception: if the user's invocation phrase explicitly
names a default-excluded file (e.g. "review my gitignore changes"), drop that exclude
for this run and *do* count it.

Interpret the filtered results:

1. **Nothing in any of the four buckets after filtering** → respond:
   > Nothing to review — no committed-unpushed, staged, unstaged, or untracked changes found
   > (after applying default excludes).

   Stop. Do not invoke the toolkit.

2. **Staged and/or unstaged changes exist (post-filter)** → ask the user:
   > You have uncommitted changes: **X** staged, **Y** unstaged. Include them in the review? (y/n)

3. **Untracked files exist (post-filter)** → ask the user (list up to 10, elide the rest):
   > You have **N** untracked files to potentially review:
   > - path/one.kt
   > - path/two.kt
   > - ...
   >
   > Include them in the review? (y/n)

Ask each applicable question once; wait for the answer before moving on. If the user declines
everything and there are no committed-unpushed changes either, treat it as "nothing to review".

### Phase 2 — Invoke the toolkit

Before running the toolkit, verify Node is 24+:

```bash
node --version
```

If the major version is below 24, stop and tell the user:
> This skill requires Node 24+. Detected `<version>`. Please upgrade Node (e.g. via `nvm install 24 && nvm use 24`) and re-run.

Build the toolkit arg list from the resolved scope, then run it **in the background**
and poll progress at a fixed cadence. The toolkit can take several minutes because it
spawns 5 Copilot agents in parallel; a silent blocking run is a poor UX, but streaming
every event via the `Monitor` tool creates too many per-event notifications.

```bash
node .claude/skills/code-panel-review/toolkit/dist/index.mjs \
  --repo "$(pwd)" \
  --include-committed-unpushed \
  [--include-staged] \
  [--include-unstaged] \
  [--include-untracked] \
  [--exclude <glob> ...] \
  --allowed-hosts-file .claude/skills/code-panel-review/allowed-hosts.txt \
  2>&1
```

Include each `--include-*` flag only for buckets the user opted into. The `2>&1`
redirect is important — it merges stderr (progress lines) with stdout so a single
`BashOutput` read catches both.

**Always pass `--allowed-hosts-file`** pointing to `allowed-hosts.txt` in this skill
directory. Reviewers are allowed web access for API/doc lookups, but every URL they
fetch is checked against this allowlist at runtime; hostnames not in the file are
denied. Without this flag, no URLs are approved (reviewers lose web access entirely).
If the user needs to allow an additional host for a specific run, add `--allowed-host
<hostname>` (repeatable) alongside the file.

**Run pattern (20s polling):**

1. Invoke Bash with `run_in_background: true`. Record the `shell_id` returned. Tell
   the user the panel is running and that you'll check in every 20 seconds.

2. Enter a polling loop. Each iteration:
   - Run `sleep 20` via Bash (foreground, short). This gives the agents time to make
     progress between reports.
   - Call `BashOutput` with the `shell_id`. It returns the incremental output since
     the last read.
   - Parse the incremental output. You'll see lines like:
     - `[panel 2026-04-18T…] security: starting (model=claude-opus-4.6)`
     - `[panel 2026-04-18T…] security: → view(src/foo/Bar.kt)`
     - `[panel 2026-04-18T…] security: turn complete`
     - `[panel 2026-04-18T…] security: finished in 37938ms`
     - `[panel 2026-04-18T…] security: failed: <reason>`
     - `PANEL_OUTPUT_DIR=/var/folders/.../panel-review-XYZ` (stdout, signals completion)
   - Produce a single concise summary line for the user covering this 20s window
     (e.g. "security and bugs still reading files; resilience finished in 58s").
     Don't paste raw event lines — summarize per reviewer.

3. Exit the loop when:
   - `PANEL_OUTPUT_DIR=…` appears (the happy path), **or**
   - All five reviewers have emitted either `finished in …ms` or `failed: …`, **or**
   - `BashOutput` reports the shell has exited.

4. Capture the `PANEL_OUTPUT_DIR` path from the output for Phase 3.

If the user asks "what's happening?" between polls, do an immediate `BashOutput` read
and summarize — no need to wait for the next 20s tick.

**Use `--exclude` to drop noise files before inviting the agents.** Every file in the
manifest costs agent context and may dilute findings. Before invoking the toolkit, scan
the resolved file list and add `--exclude` flags for paths with no human-authored review
value. The agents will not infer this — you must pre-filter.

**Always apply these default excludes on every run** (pass them on every invocation,
regardless of what's in the manifest — it's fine if they match nothing):

```
--exclude "**/.gitignore" --exclude "**/yarn.lock"
```

Only drop a default exclude if the user explicitly asks to review one of those files
(e.g. "review my gitignore changes").

**Also consider excluding** (apply when the resolved file list actually contains matches,
and announce them before running):
- **Other lockfiles:** `**/package-lock.json`, `**/pnpm-lock.yaml`, `**/Gemfile.lock`,
  `**/poetry.lock`, `**/Cargo.lock`, `**/go.sum`, `**/composer.lock`, `**/*.lockb`
- **Build / bundler output:** `dist/**`, `build/**`, `out/**`, `.next/**`, `target/**`,
  `**/*.min.js`, `**/*.bundle.js`, `**/*.map`
- **Vendored / generated:** `vendor/**`, `**/generated/**`, `**/*.generated.*`
- **Binaries / media:** `**/*.{png,jpg,jpeg,gif,svg,ico,webp,pdf,zip,tar,gz}`

Pattern syntax (Node's `path.matchesGlob`): `*` = any chars except `/`, `**` = any chars
including `/`, `?` = one char. A pattern without `/` is also matched against the basename,
so `yarn.lock` alone catches `yarn.lock` anywhere in the tree.

Call out the exclusions you're applying in one line before running the toolkit, so the
user can object:
> Excluding from review: yarn.lock, dist/**, **/*.min.js. Proceeding.

If the resolved file list contains only files that would be excluded, tell the user and
stop — there's nothing meaningful to review.

The toolkit:
- Builds a manifest of `{path, changed_lines}` entries (no file content — agents read files
  themselves via the SDK's read-only filesystem tool).
- Loads `.code-panel-review.yaml` from the repo root if present, otherwise uses defaults
  (Security=claude-opus-4.6, Performance=gpt-5.4, Resilience=claude-opus-4.6, Bugs=gpt-5.4,
  Compliance=gpt-5.4; all enabled).
- Resolves each reviewer's requested model against the SDK's `listModels()` via fuzzy match.
- Spawns enabled reviewers in parallel, validates each response against the finding schema
  (retries once on schema failure), and writes one JSON file per reviewer.

On success, the toolkit prints a single line to stdout:

```
PANEL_OUTPUT_DIR=/tmp/panel-review-<ISO-timestamp>
```

### Phase 3 — Read the per-reviewer outputs

For each reviewer that was enabled, Read the file at
`<PANEL_OUTPUT_DIR>/<reviewer>.json` (one of: `security.json`, `performance.json`,
`resilience.json`, `bugs.json`, `compliance.json`).

If a `<reviewer>.error.json` exists instead, that reviewer failed schema validation twice —
note the failure in the Panel summary section of the final report but do not fail the whole run.

### Phase 4 — Synthesize

Follow `prompts/SYNTHESIZER.md` in this skill directory to cluster, dedupe, rank, and present
the final report. Output is markdown in the chat, grouped by severity tier (see the synthesizer
prompt for the exact layout).

## Configuration (optional)

The user may place a `.code-panel-review.yaml` at the repo root to override defaults. See
`.code-panel-review.yaml.example` in this skill directory for the schema. Unspecified fields
fall back to defaults; unknown keys produce a warning (not an error) so the format is
forward-compatible.

## Non-goals (v1)

- Auto-applying fixes — this skill reports only.
- Reviewing remote branches or someone else's PR.
- CI integration.
- A fifth "architecture" reviewer or running the same lens across multiple models.
- Full-repo review when no changes exist.
- Caching or incremental review — each invocation is a fresh run.
