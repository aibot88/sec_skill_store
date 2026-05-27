---
name: lookup-docs
description: Fetch current documentation for libraries used in channelhub (Bun, grammy, MCP SDK, Playwright, bun:sqlite, etc.). Prefer Context7 when installed; fall back to WebFetch against the canonical doc site. Use when the user asks "how does X API work" or you're about to call an unfamiliar library method.
---

# Look up library documentation

## Why this exists

Channelhub leans on libraries that move faster than the model's training cut.
Today's debugging hit at least three "is this current?" moments:

- `bun:sqlite` API — added relatively recently, semantics drift
- `Bun.spawn` env / cwd inheritance — caught us out on the CI cwd bug
- `grammy` v1.x command registration — `bot.api.setMyCommands` shape
- MCP SDK request handlers (`CallToolRequestSchema`, notification handlers)

Pulling current docs catches version drift instantly.

## Preferred path: Context7

If the **Context7** plugin is available (auto-loaded MCP tools
`resolve-library-id`, `get-library-docs`), use it:

```
1. resolve-library-id with the library name → get a Context7 ID
2. get-library-docs with that ID + a topic → get current snippet
```

Install Context7 once, project-wide:

```bash
# As a Claude Code plugin (recommended):
/plugin install context7@anthropic-marketplace

# Or as a user-scope MCP server (works in any client):
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

After install, restart Claude Code in this repo and the tools surface
automatically.

## Fallback: WebFetch

If Context7 is not available, hit the canonical doc URL directly:

| Library | URL pattern |
|---|---|
| Bun runtime | `https://bun.sh/docs/<topic>` |
| `bun:sqlite` | `https://bun.sh/docs/api/sqlite` |
| `Bun.serve` | `https://bun.sh/docs/api/http` |
| `Bun.spawn` | `https://bun.sh/docs/api/spawn` |
| grammy | `https://grammy.dev/guide/<topic>` |
| MCP SDK | `https://github.com/modelcontextprotocol/typescript-sdk` (README) |
| Playwright | `https://playwright.dev/docs/<topic>` |
| tmux | `https://man.openbsd.org/tmux` |

Use WebFetch with a focused prompt — the smaller the question, the better
the synthesis.

## When NOT to look up

- Stable, ancient APIs (Node `fs`, `path`, `crypto`) — model knowledge is fine.
- Behavior already proven in this repo — read the source first
  (`grep` / `Read`) before fetching docs. Existing usage IS the docs.

## Reply to the user

When you used Context7 / WebFetch to settle a question, say so briefly
("Confirmed via Bun docs: …"). Don't paste raw docs unless it's directly
relevant. Cite the URL you fetched so the user can verify if they want.

## Note on supportability

Skills can call MCP tools when those tools are exposed to the current Claude
Code session. Context7 must be installed at the user / plugin level — this
skill cannot install it for you. If `resolve-library-id` errors with "tool
not found", drop to the WebFetch fallback in the same response.
