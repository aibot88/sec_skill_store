---
name: x-publisher
description: Draft, validate, split into threads, open X/Twitter composer links, and use the dry-run-first MCP workflow for live X posting when local credentials are explicitly configured. Use when Codex needs to prepare social launch copy, repo/project announcements, X posts, tweet threads, or shareable publishing drafts where the user should manually review before posting.
---

# X Publisher

## Overview

Prepare X posts safely from local drafts. V1 creates validated composer links; v2 adds a dry-run-first MCP server in the source repo for curated posting and account-management workflows. Live posting is opt-in only and still requires exact confirmation.

## Workflow

1. Draft concise post text in the user's voice and keep the strongest point first.
2. Run `scripts/x_publish.py validate` before sharing any post or thread.
3. Use `scripts/x_publish.py intent` for a single post composer link.
4. Use `scripts/x_publish.py thread` for long Markdown/text drafts.
5. Tell the user that the browser composer is the final review step and they must click Post manually unless they explicitly ask for the v2 live MCP workflow and local credentials are configured.

## Commands

Run commands from this skill folder:

```bash
python scripts/x_publish.py draft --text "Shipped x-publisher v1: local drafts, validation, threading, and X composer links."
python scripts/x_publish.py validate --text "Shipped x-publisher v1" --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py intent --text "Shipped x-publisher v1" --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py thread --file post.md
```

Add `--open` to `intent` only after the generated URL looks correct.

## Guardrails

- Do not post directly from the v1 CLI. If asked for direct posting, use the v2 MCP guidance in `references/mcp-usage.md`, require exact confirmation for mutating tools, and keep live credentials in environment variables only.
- Do not request or store X API keys in prompts or committed files.
- Treat local character counts as a conservative approximation. For direct API posting, re-check current X docs and use the official `twitter-text` guidance.
- Prefer shortening the draft before splitting into a thread unless the user explicitly wants a thread.
- Treat the source repo as authoritative. Sync the installed skill from the source repo with `python tools/install_local.py`.

## References

- `references/posting-workflow.md`: Practical draft, validation, and composer-link workflow.
- `references/mcp-usage.md`: How to list and run the v2 MCP server.
- `references/x-api-mcp-v2.md`: Notes for the full X API MCP/plugin direction.
