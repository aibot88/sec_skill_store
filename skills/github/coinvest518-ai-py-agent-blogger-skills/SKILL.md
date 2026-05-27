# Buffer (MCP) Skill

Purpose: post to Buffer-connected social channels (Pinterest, YouTube, TikTok for FDWA right now) via Buffer's official MCP server.

## Transport

- Endpoint: `https://mcp.buffer.com/mcp`
- Auth: `Authorization: Bearer $BUFFER_API_KEY`
- Transport: streamable HTTP (`langchain-mcp-adapters`)

## Tools used

- `get_account` — bootstrap, returns org id
- `list_channels(organizationId)` — enumerate connected services
- `get_channel(channelId)` — needed for Pinterest to read `metadata.boards[].serviceId`
- `create_post(input)` — actual post. Mode defaults to `shareNow` (publishes immediately, NOT queued).
- `get_post(postId)` — verify actual publish status (`status=sent`, `error=null`)

## Pinterest requirements (the part that kept breaking)

Pinterest is the strictest channel. Every successful pin needs ALL of:
1. `assets.images[0].url` — public HTTPS image URL. No `image_url` = SKIP the channel (don't queue).
2. `assets.images[0].metadata.altText` — required by MCP schema, not optional.
3. `metadata.pinterest.boardServiceId` — `get_channel` → `metadata.boards[n].serviceId`. FDWA auto-picks the board whose name contains "crypto"; env override `BUFFER_PINTEREST_BOARD_SERVICE_ID`.
4. `metadata.pinterest.title` — plain text, **≤100 chars, NO emojis, NO URLs, NO hashtags**. Pinterest rejects pins with decorated titles (error: "Pinterest title cannot..."). `_pin_title()` strips these before sending.
5. `metadata.pinterest.url` — destination URL for pin click-through. FDWA uses `BUFFER_PINTEREST_SOURCE_URL` (default `https://futuristicwealth.gumroad.com/`).

If ImgBB fails and `image_url` is null → Pinterest is skipped with reason `no image (pinterest requires image)`. Do NOT attempt text-only posts to Pinterest.

## Scheduling modes

- `shareNow` — publish immediately. Use for the fire-and-forget `post_now()` path.
- `customScheduled` + `dueAt` (ISO 8601 with offset) — schedule future post. Used when state carries `buffer_scheduled_at`.
- `addToQueue` — NOT used. Goes into Buffer's slot queue; not what we want for agent runs.
- `shareNext` — also unused.

## Gotchas

- Buffer returning `success: true` from `create_post` does NOT mean the pin is live. Buffer may accept then fail at publish time if per-channel metadata is missing (e.g., Pinterest title/sourceUrl). ALWAYS verify via `get_post(postId)` → `status == "sent"`, `error == null` when debugging.
- Image `altText` omitted → MCP schema validation fails before Buffer even sees the request.
- Pinterest title character rule is strict. Keep it literal: no emojis, no hashtags, no markdown, ≤100 chars. `_pin_title()` handles this.

## Env vars

- `BUFFER_API_KEY` (required, sync:false)
- `BUFFER_MCP_URL` default `https://mcp.buffer.com/mcp`
- `BUFFER_DEFAULT_MODE` default `shareNow`
- `BUFFER_PINTEREST_SOURCE_URL` default `https://futuristicwealth.gumroad.com/`
- `BUFFER_PINTEREST_BOARD_SERVICE_ID` optional — pin to a specific board; else auto-picks "crypto" board
- `BUFFER_CHANNEL_IDS` optional csv to restrict targets

## Code

Implementation: `src/agent/agents/buffer_agent.py`. Public surface stable: `run(state)`, `post_now(...)`, `schedule_post(...)`, `list_channels()`. Clients (Telegram `/buffer_now`, Notion commands, graph node) don't change when MCP internals change.
