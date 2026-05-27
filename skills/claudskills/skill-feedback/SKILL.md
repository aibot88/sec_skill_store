---
name: skill-feedback
description: Local-first self-assessment for Claude Code skills. After you use any skill (your own or someone else's), call `skill-feedback log <skill> --rating N --outcome ... [--friction "..."]` to append one entry to `.agent-plus/skill-feedback/<skill>.jsonl`. The skill author can then run `skill-feedback report` for an aggregate, or `skill-feedback submit <skill>` to bundle entries into a GitHub issue body for the skill's source repo. No telemetry leaves the machine unless the user explicitly runs `submit`.
when_to_use: Trigger immediately AFTER using any other agent-plus skill (or any third-party skill the user installed) — log a one-line self-assessment so the skill's author has signal. Also trigger on phrases like "show feedback for X", "rate this skill", "report skill usage", "what's the feedback on the hermes skill", "submit the feedback to the upstream repo", "where are the skill logs stored".
allowed-tools: Bash(skill-feedback:*) Bash(python3 *skill-feedback*:*)
---

# skill-feedback

Append-only self-assessment log for Claude Code skills. The agent rates its own use of a skill; the rating lands in `.agent-plus/skill-feedback/<skill>.jsonl` next to the project, never on a network. Skill authors run `report` to aggregate, or `submit` to bundle into a GitHub issue body for the skill's source repo.

The binary lives at `${CLAUDE_SKILL_DIR}/../../bin/skill-feedback`; the plugin auto-adds `bin/` to PATH, so call it as `skill-feedback`.

## When to reach for this

**The default trigger is implicit:** every time you finish using a skill — yours or another agent-plus plugin's — emit one log entry before stopping. Treat it like a `CHANGELOG` line, not a separate task. One call, one line, done.

```bash
# Successful use of hermes-remote, no friction
skill-feedback log hermes-remote --rating 5 --outcome success

# Partial: the skill mostly fit, but you had to fall back to raw curl for one bit
skill-feedback log hermes-remote --rating 3 --outcome partial \
  --friction "no streaming chat support; fell back to curl + SSE"

# Failure: the skill didn't fit the request at all
skill-feedback log github-remote --rating 1 --outcome failure \
  --friction "user wanted to merge a PR; pr merge isn't wrapped"
```

Also trigger on explicit user requests:

- "show me feedback on the hermes skill" → `skill-feedback show hermes-remote --since 7d`
- "report on all skill usage" → `skill-feedback report --since 30d --pretty`
- "submit the feedback to the upstream repo" → `skill-feedback submit hermes-remote --no-dry-run`

## What to put in the fields

| Field | Required | Guidance |
| :--- | :--- | :--- |
| `<skill>` | yes | The exact `name:` value from the skill's SKILL.md (e.g. `hermes-remote`). |
| `--rating 1..5` | yes | 5 = skill fit perfectly, 1 = skill was actively a wrong fit. Be honest — over-positive ratings waste the author's time. |
| `--outcome success\|partial\|failure` | yes | Was the user's actual request resolved using this skill? |
| `--friction "..."` | optional | One short label, e.g. `"no streaming"`, `"missing --json on list"`, `"wrong default timeout"`. Aggregates by exact match — keep it short and reusable across sessions. |
| `--note "..."` | optional | Up to 1000 chars of free text. Capped + regex-scrubbed for token patterns before write. |

**Don't over-share.** No transcripts, no user prompts, no arguments containing PII or secrets. If in doubt, leave `--note` off and rely on `--friction` alone.

## Headline commands

```bash
skill-feedback log <skill> --rating 1-5 --outcome success|partial|failure \
                  [--friction "<short label>"] [--note "<longer text>"] \
                  [--tool-version <ver>]

skill-feedback show <skill> [--since 7d] [--limit 50]
skill-feedback report [--skill <name>] [--since 30d] [--pretty]
skill-feedback submit <skill> [--since 30d] [--repo owner/name] [--no-dry-run]
skill-feedback path [--skill <name>]
```

All commands emit JSON to stdout. Use `--pretty` for indentation. Every payload carries a top-level `tool: {name, version}` field for self-diagnosis (pattern #6 in the agent-plus README).

## Storage

JSONL, one entry per line, append-only:

```jsonc
{"ts":"2026-04-26T21:30:00Z","skill":"hermes-remote","rating":5,
 "outcome":"success","session_id":"...","tool_version":"0.4.1","schema":1}
```

Storage root is resolved in this order (highest first):

1. `SKILL_FEEDBACK_DIR` env var (absolute path)
2. `<git-toplevel>/.agent-plus/skill-feedback/` if cwd is in a git repo
3. `<cwd>/.agent-plus/skill-feedback/` if a project-local `.agent-plus/` exists
4. `~/.agent-plus/skill-feedback/` (last-resort fallback)

Run `skill-feedback path` to print the resolved root, or `skill-feedback path --skill X` for the per-skill jsonl path.

## Submit flow (opt-in)

`submit` bundles recent entries into a markdown body and (with `--no-dry-run`) opens a GitHub issue against the skill's source repo. Repo URL is read from the skill's `plugin.json#repository` field, or you can pass `--repo owner/name` explicitly.

- **Default is `--dry-run`.** It prints the title + body so the user can review before anything leaves the machine.
- **`--no-dry-run`** requires either `gh` on PATH (uses `gh issue create`) or falls back to writing the body to `<root>/<skill>.submit.md` for manual paste. No raw GitHub API calls — auth is borrowed from `gh`.
- **Free-text fields are regex-scrubbed before write**, but the regex only catches token shapes — not PII, customer names, internal hostnames, or contextual leaks. **You (the agent) are the final gate** before anything reaches a public tracker; see "Privacy review before submit" below. The user owns the decision to publish.

## Privacy review before submit

Regex scrubbing (in `log`) is the floor, not the ceiling. It catches `ghp_…`, `AKIA…`, `sk-ant-…`, etc., but it cannot recognise PII or context-sensitive content. **Before running `submit --no-dry-run`, you (the agent already executing this skill in the user's Claude Code session) must do a privacy review pass on the assembled body.** No extra API call, no SDK — your existing context is what does the work.

Workflow:

1. **Always run `submit --dry-run` first** (it's the default). Read the `body` field in the resulting JSON. The result also exposes `agent_review_required: true` plus an `agent_review_checklist` array as a built-in reminder.
2. **Scan `body` against this checklist** for content the regex cannot pattern-match:
   - PII: real names, email addresses, phone numbers, physical addresses
   - Customer / employer / client / project names that aren't public
   - Internal hostnames, private URLs, file paths revealing identity (e.g. `/Users/<name>/work/<client>/...`)
   - Ticket IDs, repo names, or Slack channel names that aren't public
   - Error messages or stack traces that quote internal data
   - Anything you wouldn't paste into a public issue on an open-source repo
3. **If anything in step 2 is present:** ABORT. Do not run `--no-dry-run`. Tell the user exactly what you found and let them decide:
   - Edit `<root>/<skill>.jsonl` by hand and retry
   - Use `--since` to scope a window that excludes the sensitive entries
   - Skip the submit
4. **Only run `--no-dry-run`** after step 2 returns clean.

This is documentation, not enforcement — there is no flag to require the review and no flag to bypass it. You're trusted to do this correctly because you have the user's context and the regex doesn't.

## Privacy + safety contract

- **Local-first.** No network call on `log`, `show`, `report`, or `path`. Only `submit --no-dry-run` can reach a network, and only via `gh`.
- **Length-cap + secret-scrub.** Free-text inputs are capped at 1000 chars and regex-stripped of GitHub PATs (`ghp_…`, `github_pat_…`, `gho_/ghu_/ghs_/ghr_…`), AWS access keys (`AKIA…`), Anthropic (`sk-ant-…`), Langfuse (`pk-lf-…` / `sk-lf-…`), Stripe (`sk_live_/sk_test_/rk_/pk_…`), generic OpenAI-style `sk-…`, Supabase (`sbp_…`), Sentry (`sntrys_…`), Google API keys (`AIza…`), Slack (`xoxb-/xoxa-/xoxp-/xoxr-/xoxs-…`), Discord bot tokens, JWTs (`eyJ…`), `Bearer …`, and `Authorization: …` patterns before write. Not exhaustive — don't paste secret-shaped strings into `--note` to begin with.
- **No transcript ingestion.** The CLI never reads `~/.claude/projects/...` or any session log. Only what the agent passes on the command line is stored.
- **Skill name is whitelisted.** `[A-Za-z0-9._-]+` only — prevents path traversal and keeps the JSONL filename predictable.

## Design rules (agent-plus patterns)

1. **Aggregate server-side.** `report` does the math locally — outcomes histogram, rating average, top friction strings — agent gets one blob, not 200 raw entries.
2. **Stay in your lane.** No dashboard, no SaaS, no SDK. JSONL on disk; `gh` for the optional issue write. If `gh` isn't there, write the body to disk and tell the user where.
3. **`--json` is the default.** No human-prose output paths; pipe into `jq`.
4. **Strip values the agent shouldn't see.** Same secret-pattern set as `github-remote`'s `_scrub_text()`.
5. **Self-diagnosing output.** Every payload has `tool: {name, version}` from the manifest.

## When NOT to use this — fall back to the underlying CLI

- **You want to view or edit a single entry.** `skill-feedback` is append-only by design. Use `cat`, `jq`, or open the `.jsonl` file in an editor.
- **You want to delete entries.** Not exposed by the CLI. Edit the `.jsonl` directly, or `rm` the file. (No PII should be in there in the first place — see scrub rules above.)
- **You want richer analytics.** Pipe `report --pretty` (or raw `.jsonl`) into `jq` / DuckDB / a notebook. The CLI deliberately ships only the aggregations agents need at the terminal.
- **You want to file a bug, not a feedback report.** Open an issue manually. `submit` is for batched feedback, not single-issue triage.

## What it doesn't do

Deliberately out of scope for v1:

- No retroactive transcript scraping. The agent has to log explicitly.
- No edit / delete commands — the file is plain `.jsonl`, edit it yourself if needed.
- No SaaS upload. `submit` only opens a GitHub issue (and only with `--no-dry-run`).
- No automatic re-submission or de-duplication; once an issue is filed, those entries are not marked "submitted" — the user can purge or rotate `.agent-plus/skill-feedback/<skill>.jsonl` themselves.

## Example: log → report → submit cycle

```bash
# 1. After each skill use the agent logs one line
skill-feedback log linear-remote --rating 4 --outcome success \
  --friction "no --from-csv on bulk create"

# 2. The skill author runs report a week later
skill-feedback report --skill linear-remote --since 7d --pretty

# 3. If the signal is strong, bundle and file an issue upstream
skill-feedback submit linear-remote --since 30d                    # dry-run preview
skill-feedback submit linear-remote --since 30d --no-dry-run       # actually file
```
