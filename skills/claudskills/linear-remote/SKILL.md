---
name: linear-remote
description: Read-first wrapper around the Linear GraphQL API. Single-call issue context (comments + relations + state), name-resolved teams/projects/states/labels, `issues create --from-markdown` turns a design doc into a Linear issue without hand-stitching flags. Use whenever the user wants to read, triage, or write Linear issues — creating an issue from a markdown doc, fetching issue context (including comments and relations) without chaining 5+ MCP calls, listing project work by state, or moving an issue and waiting for webhook-driven transitions. Wraps a static personal API key, so it sidesteps the MCP OAuth browser-auth wall entirely.
when_to_use: Trigger on phrases like "add this to linear", "create a linear issue", "what's on LOA-229", "list linear issues", "move this to In Review", "linear project status", "what's blocking <issue>", "triage linear", "tag assignee in linear", "turn this doc into a linear issue".
allowed-tools: Bash(linear-remote:*) Bash(python3 *linear-remote*:*)
---

# linear-remote

Project-scoped CLI that wraps the Linear GraphQL API into a read-first, JSON-output tool. Stdlib-only Python 3 (no pip, no venv). Designed for agent-driven Linear work — one call returns the full issue + comments + relations + state picture, name-resolved, with a first-class `--from-markdown` path for the "turn this design doc into an issue" workflow.

Lives at `${CLAUDE_SKILL_DIR}/../../bin/linear-remote`; the plugin auto-adds `bin/` to PATH, so just run `linear-remote ...`.

## Prerequisites

- **`LINEAR_API_KEY`** set (project `.env` / `.env.local` or shell env). Get one at https://linear.app/settings/api. Personal API keys only — this plugin deliberately avoids the OAuth browser flow that the MCP requires.
- **Optional:** `LINEAR_TEAM_ID` — a team UUID or key (e.g. `LOA`) to omit `--team` on every call.

The CLI bails with a clear missing-config message if `LINEAR_API_KEY` is absent.

## When to reach for this

- User says **"add this to linear as an issue"** with a chunk of markdown → write the markdown to a file, then `issues create --from-markdown <path> --team <name>`. YAML frontmatter (`team:`, `project:`, `labels:`, `priority:`, `assignee:`) is respected. First H1 becomes the title, rest becomes the body.
- User asks **"what's LOA-229 about"** → run `issues get LOA-229 --include-comments --include-relations --pretty`. One call → title, body, state, assignee, labels, project, parent, comments, and blocking/blocked-by relations.
- User asks **"list my in-progress work on <project>"** → run `issues list --project <name> --state 'In Progress' --assignee <email>`.
- User wants a **project status snapshot** → run `projects overview '<name>' --pretty`. State-bucketed issues (backlog / todo / inProgress / inReview / done / canceled), milestones, recent activity, completion %.
- User says **"move LOA-229 to In Review"** → run `issues move LOA-229 'In Review'`. Add `--wait` when the transition is downstream of a GitHub PR merge (Linear's webhook auto-moves to "Done"). 60s default timeout, 3s poll, partial JSON on timeout.
- User wants to **comment on an issue** → run `comments add LOA-229 @./review-notes.md` (the `@path` form reads body from a file).

## Headline commands

```bash
linear-remote issues get <id-or-query> [--include-comments] [--include-relations]
linear-remote issues list [--project ...] [--state ...] [--assignee ...] [--team-filter ...] [--label ...] [--limit 25] [--cursor <c>]
linear-remote issues search <query> [--limit 25]

linear-remote issues create --title <t> --team <name> [--project <n>] [--body "..."|--body @file] [--labels a,b] [--priority 0-4] [--assignee <email>]
linear-remote issues create --from-markdown <path> [--team <name>]        # killer feature

linear-remote issues update <id> [--title ...] [--state ...] [--assignee ...] [--labels a,b] [--priority N] [--project ...]
linear-remote issues move <id> <state-name> [--wait] [--timeout 60]
linear-remote issues assign <id> <assignee>

linear-remote comments add <issue-id> <body>          # <body> accepts @path for file input
linear-remote comments list <issue-id>

linear-remote projects list [--team-filter <name>]
linear-remote projects overview <name> [--bucket-limit 25]

linear-remote teams list
linear-remote states <team-name>
linear-remote labels [--team-filter <name>]
linear-remote cycles <team-name>
```

All list/show commands emit JSON to stdout. Use `--pretty` for indentation.

Every payload carries a top-level `tool: {name, version}` field so you can self-diagnose version drift directly from the output. Run `linear-remote --version` to print the version without a command.

### jq recommendation

Pipe through `jq` to slice out the bits you need instead of paging the full JSON into context. Examples:

```bash
# Just the open-issue identifiers from a project overview
linear-remote projects overview 'Agent Plus' | jq -r '.issuesByState.inProgress[].identifier'

# Title + state for one issue, no comments tree
linear-remote issues get LOA-229 | jq '{id: .identifier, title, state: .state.name}'

# Drop the tool meta when piping an issue payload to another tool
linear-remote issues get LOA-229 | jq 'del(.tool)'
```

## Design rules (agent-plus patterns)

1. **Aggregate server-side.** `issues get --include-comments --include-relations` returns the whole context tree in one call. `projects overview` bundles project meta + milestones + state-bucketed issues + recent activity.
2. **Resolve by name.** Pass `--team LOA`, `--project 'Agent Plus'`, `--state 'In Progress'`, `--assignee alice@example.com`. The CLI resolves UUIDs internally, with `lru_cache` on enum lookups so `update + move` in one invocation doesn't re-query.
3. **Accept either ID format.** Every issue argument accepts the human key (`LOA-229`) or the UUID. Free-text falls through to search with ambiguity surfacing candidates.
4. **`--wait` on webhook-driven transitions.** `issues move --wait` polls `issue.state.name` every 3s until it matches the target, 60s default, override with `--timeout`. On timeout: non-zero exit with partial JSON. Instant mutations return immediately without polling.
5. **`--json` is the default.** No human-prose output paths.
6. **Zero API-key leakage.** Every API response walks through `_scrub()` before emission — masks `apiKey`, `token`, `secret`, `webhookSecret`, `password`, and similar. A canary-value test asserts a known secret substring never appears in any output.

## `--from-markdown` contract

- YAML frontmatter (optional): `team`, `project`, `labels` (list or inline), `assignee`, `priority` (0-4), `title` (overrides H1).
- First `# H1` → title. Everything after → description.
- `<!-- html comments -->` stripped (Linear renders them as visible text).
- `--team` flag overrides frontmatter; frontmatter overrides `LINEAR_TEAM_ID`.

## Pagination

List commands return `{nodes: [...], pageInfo: {hasNextPage, endCursor}}`. Pass `--cursor <endCursor>` for the next page. `--limit` default 25, max 100.

## Config precedence (highest first)

1. `--api-key` / `--team` CLI flags
2. `--env-file <path>`
3. `.env.local` / `.env` walked up from cwd (closest wins)
4. Shell env

Only `LINEAR_*` prefixed vars are picked up.

## Error message contract

Every error path emits problem + cause + fix + link:

- Missing key → "Set in project `.env` or `.env.local` (keys prefixed `LINEAR_`), or `~/.claude/settings.json`. Get one: https://linear.app/settings/api"
- 401 → "API key rejected. Check for whitespace/truncation. Rotate at https://linear.app/settings/api"
- 403 → "Key lacks access to this workspace or resource. Confirm you're a member and the key belongs to it."
- GraphQL field-level errors → the `path` and `message` surfaced verbatim so you can see which field failed.
- 429 → "Rate-limited by Linear. Retry after <N>s (Retry-After header). Linear's complexity budget is ~1500/hr."

## When NOT to use this — fall back to the Linear GraphQL API directly

**This wrapper's write surface is deliberately narrow** (issues CRUD + move/assign, comments add/list, projects list/overview, read-only teams/states/labels/cycles). For anything outside that surface, don't try to bend `linear-remote` flags to fit — drop straight to `curl https://api.linear.app/graphql -H "Authorization: $LINEAR_API_KEY"` with a hand-written GraphQL document. The API key is already in scope; the only thing the wrapper adds is name resolution and scrubbing, and neither helps you when the operation isn't wrapped at all.

Specific cases where you should hit GraphQL directly, not `linear-remote`:

- **Project milestone CRUD** (create / update / delete milestones, reorder, set target dates). `projects overview` reads milestones; there's no `milestones` subcommand for writes. Use `projectMilestoneCreate` / `projectMilestoneUpdate` / `projectMilestoneDelete` mutations.
- **Workflow state CRUD** (add a new state to a team, rename, change color, reorder, archive). `states <team>` is read-only. Use `workflowStateCreate` / `workflowStateUpdate` / `workflowStateArchive`.
- **Cycle management beyond listing** (create a cycle, shift dates, close/uncomplete). `cycles <team>` is read-only. Use `cycleCreate` / `cycleUpdate`.
- **Team / workspace admin** (create teams, change team settings, invite members, manage roles, org-level config). Not wrapped at all. Use `teamCreate` / `teamUpdate` / `teamMembershipCreate` and the org mutations.
- **Webhook management and integration config** (register/rotate webhooks, configure GitHub/Slack/Intercom integrations, OAuth app settings). Not wrapped. Use `webhookCreate` / `webhookUpdate` / `integrationRequest` and friends.
- **Documents, initiatives-beyond-read, roadmaps, custom views, custom fields** — none are wrapped. Use `documentCreate` / `initiativeCreate` / `initiativeUpdate` / `roadmap*` / `customView*` mutations directly, and consult Linear's schema introspection (`query { __schema { mutationType { fields { name } } } }`) if you're unsure of the field name.

**Don't get stuck in a loop.** If `linear-remote --help` doesn't show a subcommand for the write you need, or a command returns "unknown subcommand" / "unsupported operation", stop retrying with different flags — write the GraphQL query/mutation yourself and `curl` it. The wrapper exists to make *reading and common writes* faster; it's not trying to be a full GraphQL client, and padding it out with one-off mutations defeats the point.

## What it doesn't do

Deliberately out of scope for v1:

- Cycle / milestone CRUD (read-only).
- Initiative CRUD.
- Team / workspace management.
- Custom field mutations.
- Webhook configuration.
- Cross-issue relation mutations (`relate`). Relations surface in `issues get` read-only.
- OAuth. Personal API key only — avoids the browser-auth wall that the MCP hits.

Use the Linear UI, the MCP, or raw GraphQL for those. This plugin is read-first Linear work plus the common write surface (issue create/update/move, comments add).
