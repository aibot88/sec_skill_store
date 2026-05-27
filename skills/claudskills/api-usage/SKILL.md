---
name: api-usage
description: REST API for creating AI-powered video ads programmatically. Bearer token auth via API key, OAuth client_credentials, or OAuth Authorization Code (Connect flow).
version: 1.1.0
---

# Prizmad REST API

Prizmad provides a REST API for creating AI-powered video ads programmatically. The MCP server at `/api/mcp` is a thin agent-friendly wrapper on top of these endpoints — anything the MCP layer does, you can do with a curl loop.

## Authentication

Three interchangeable ways to obtain a Bearer token. See [`/.well-known/agent-skills/oauth/SKILL.md`](https://prizmad.com/.well-known/agent-skills/oauth/SKILL.md) for the full OAuth spec.

### Option 1: API key (simplest)

```http
Authorization: Bearer przmad_sk_live_...
```

Manage keys at <https://prizmad.com/api-keys>.

### Option 2: OAuth 2.0 client_credentials (server-to-server)

```bash
curl -X POST https://prizmad.com/oauth/token \
  -d grant_type=client_credentials \
  -d client_id=my-app \
  -d client_secret=przmad_sk_live_...
```

Returns `access_token` (HS256 JWT, 1 h, audience `https://prizmad.com/api`).

### Option 3: OAuth 2.1 Authorization Code + PKCE + DCR (Connect flow)

The "Add custom connector" path used by Claude Desktop / Claude.ai / ChatGPT / Cursor. RS256 JWT bound to the MCP audience, refresh-rotated. Discovery: `/.well-known/oauth-authorization-server`.

## Discovery

- **OpenAPI**: `https://prizmad.com/openapi.json`
- **Interactive docs (Scalar)**: `https://prizmad.com/api/docs`
- **API catalog (RFC 9727)**: `https://prizmad.com/.well-known/api-catalog`
- **Health**: `https://prizmad.com/api/health`

## Endpoints

### Public (no auth)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/templates` | List all video templates with features and token costs |
| GET | `/api/v1/avatars` | List built-in avatar presets with recommended voices |

### Authenticated

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/videos` | List the caller's recent video projects (paginated; `?limit`, `?status`). Returns projectUrl / shareUrl / downloadUrl per row. |
| POST | `/api/v1/videos` | Create a new video render. Returns `videoId` + estimated time + poll cadence. **Requires Pro plan.** |
| GET | `/api/v1/videos/{id}` | Status by id — progress %, steps, projectUrl, shareUrl, downloadUrl, errorMessage. Auto-mints a share token on completion. |
| GET | `/api/v1/videos/{id}/download` | Authenticated mp4 stream proxied through prizmad.com. |
| POST | `/api/v1/videos/batch` | Launch up to 20 renders in parallel; pre-checks total token cost. |
| POST | `/api/v1/upload` | Multipart upload for one or more product / avatar images. |
| POST | `/api/v1/upload-from-url` | JSON upload (image URL or base64 blob) — agent-friendly. Returns a prizmad.com-hosted URL. |

## Output URLs

Every video status response carries three URL kinds, in priority order:

| Field | Goes to |
|---|---|
| `projectUrl` | Owner-only dashboard `/projects/<id>` (full remix / edit / asset / download) — primary link to give the signed-in user. |
| `shareUrl` | Public `/share/<token>` page — only for forwarding outside the account. |
| `downloadUrl` | Authenticated `/api/v1/videos/<id>/download` mp4 proxy. |

The raw Vercel Blob URL is **never** part of the public response; downloads always flow through `prizmad.com`.

## Plan + token rules

- API generation requires a **Pro plan** (`POST /api/v1/videos` returns 403 with an upgrade URL otherwise).
- Tokens come from the user's monthly plan first, then any top-up balance.
- Insufficient balance returns 402 with `required`, `balance`, and `topUpUrl`.

## Rate limits

- 10 requests per minute per API key on most endpoints.
- 30 requests per minute on the MCP endpoint.
- Token consumption per `create_video` is template-specific — see the `cost` field in `/api/v1/templates`.
