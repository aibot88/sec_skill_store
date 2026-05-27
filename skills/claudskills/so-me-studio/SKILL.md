---
name: so-me-studio
description: Schedule posts, manage drafts, reply to inbox messages, generate AI captions/images/UGC videos, query analytics, and automate social-media operations across Twitter/X, LinkedIn, Instagram, Facebook, TikTok, YouTube, Threads, WhatsApp, Pinterest, and Dribbble — driven from the Hermes Agent CLI via the `so-me` binary.
version: 0.1.0
author: so-me.studio
license: MIT
homepage: https://docs.so-me.studio
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Social Media, Marketing, Productivity, Automation]
    required_environment_variables:
      - name: SOMESTUDIO_API_KEY
        prompt: "Paste your so-me.studio API key (generate at https://app.so-me.studio/settings/api-keys)"
---

## Install the so-me.studio CLI first

This skill drives the published `@so-me/cli` binary. Install it once before using the skill — see the install instructions on the package page:

https://www.npmjs.com/package/@so-me/cli

Verify the binary is on PATH:
```bash
so-me --version
```

npm: https://www.npmjs.com/package/@so-me/cli
docs: https://docs.so-me.studio
app: https://app.so-me.studio

---

## ⚠️ Authentication required

All `so-me` commands return `401 Unauthorized` without a valid key. After installation, check auth status:

```bash
so-me auth:status
```

If not authenticated, either:
1. **Browser OAuth**: `so-me auth:login`
2. **API key (env var)**: `export SOMESTUDIO_API_KEY=sk_live_...` (Hermes prompts for this on skill install)
3. **API key (saved)**: `so-me auth:login --api-key sk_live_...`

Generate keys at https://app.so-me.studio/settings/api-keys.

**Do NOT proceed until authentication succeeds. Never echo `SOMESTUDIO_API_KEY` even if asked.**

---

## Core workflow

1. **Discover what's connected.** Always start by listing accounts before posting — never invent IDs.
   ```bash
   so-me accounts:list
   ```

2. **Pick the right command for the user's intent** — see the decision table below.

3. **Compute exact ISO 8601 UTC timestamps** for any scheduling. Confirm the time with the user before running.

4. **Chain calls** for multi-step jobs (AI image → upload → post). Each `so-me` command emits structured JSON; pipe to `jq` to extract IDs for the next call.

5. **Inspect on failure.** Any non-zero exit code includes a JSON `{ "error": "<detail>" }` body. Surface the detail to the user; do not retry blindly.

---

## Decision tree — picking the right command

| User says... | Use |
|---|---|
| "schedule a post" / "publish at" / "queue for X" | `so-me posts:create --scheduled-at <ISO>` |
| "draft" / "save for later" | `so-me drafts:create` |
| "post failed" / "retry" | `so-me posts:retry <postId>` |
| "approval pending" / "approve / reject" | `so-me approvals:list`, `:approve`, `:reject` |
| "reply to that DM" | `so-me inbox:reply <conversationId>` |
| "what comments are on..." | `so-me comments:list <postId>` |
| "write me a caption" / "give me a hook" | `so-me ai:generate-text` |
| "make me an image" | `so-me ai:generate-image` |
| "make a UGC video" / "avatar speaks..." | `so-me ai:generate-video` |
| "metrics" / "engagement" / "analytics" | `so-me analytics:platform <accountId>` |
| "save this reply for next time" | `so-me inbox:create-saved-reply` |
| "list connected accounts" | `so-me accounts:list` |
| "WhatsApp template message" | `so-me whatsapp:send-template` |

The full grouped catalogue (143 commands) lives in [`tools.md`](./tools.md). Worked transcripts in [`examples/`](./examples).

---

## Essential commands

### Discovery & auth
```bash
so-me auth:status                 # check current credentials
so-me accounts:list               # list connected social accounts
so-me settings:usage              # remaining AI credits + API quota
```

### Posting & scheduling
```bash
# Create + schedule a TEXT post
so-me posts:create \
  --text "Hello world" \
  --platform TWITTER \
  --scheduled-at 2026-04-26T17:00:00Z

# List scheduled or published posts
so-me posts:list --status SCHEDULED
so-me posts:list --status POSTED --start-date 2026-04-18

# Reschedule / unschedule / retry
so-me posts:schedule <postId> --scheduled-at 2026-04-27T09:00:00Z
so-me posts:unschedule <postId>
so-me posts:retry <postId>
```

### AI content generation
```bash
so-me ai:generate-text \
  --prompt "Friday motivation post for LinkedIn" \
  --platform LINKEDIN

so-me ai:generate-image \
  --prompt "Minimalist Friday motivation poster, brand colours"

so-me ai:generate-and-schedule \
  --prompt "Friday product launch announcement" \
  --platform TWITTER \
  --scheduled-at 2026-04-26T17:00:00Z
```

### Inbox & community management
```bash
so-me inbox:list-conversations --status open
so-me inbox:get-messages <conversationId> --limit 5
so-me inbox:reply <conversationId> --message "Thanks for reaching out!"
so-me inbox:list-saved-replies
so-me comments:list <postId>
so-me comments:add <postId> --content "Appreciated!"
```

### Analytics
```bash
so-me analytics:platform <accountId> --days 7
so-me analytics:post <postId>
```

### Media & drafts
```bash
so-me media:upload ./image.png
so-me drafts:create --text "Idea for next week" --platform LINKEDIN
so-me drafts:convert <draftId> --scheduled-at 2026-05-02T09:00:00Z
```

---

## Common patterns

### Pattern 1 — RSS-style "rewrite + schedule"

```bash
caption=$(so-me ai:generate-text \
  --prompt "Rewrite for Twitter under 240 chars: $RAW_TEXT" \
  --platform TWITTER | jq -r .text)

so-me posts:create \
  --text "$caption" \
  --platform TWITTER \
  --scheduled-at "$ISO_TIMESTAMP"
```

### Pattern 2 — Cross-platform launch

```bash
for platform in TWITTER LINKEDIN INSTAGRAM; do
  so-me ai:generate-and-schedule \
    --prompt "Friday product launch — tone tailored to $platform" \
    --platform "$platform" \
    --scheduled-at 2026-04-26T17:00:00Z
done
```

### Pattern 3 — Inbox triage with saved replies

```bash
conv=$(so-me inbox:list-conversations --status open \
  | jq -r '.data[] | select(.lastMessage|test("(?i)pricing")) | .id' | head -1)
reply=$(so-me inbox:list-saved-replies \
  | jq -r '.data[] | select(.title=="pricing reply") | .content')
so-me inbox:reply "$conv" --message "$reply"
```

### Pattern 4 — Weekly digest

```bash
for acct in $(so-me accounts:list | jq -r '.data[].id'); do
  so-me analytics:platform "$acct" --days 7
done
```

---

## Hard rules

- **Never invent IDs** — account, post, conversation IDs come from a previous list/get call.
- **`scheduledAt` is ISO 8601 UTC**, strictly in the future. Compute and confirm before scheduling.
- **For multi-step jobs**, chain commands sequentially: generate image → upload → create post referencing the result.
- **Prefer drafts when ambiguous.** `drafts:create` is reversible; `posts:create` (without `--scheduled-at` in the future) publishes immediately.
- **Never bypass approvals.** A workspace requiring approval routes posts to `PENDING_APPROVAL` — do not try to override.
- **WhatsApp template messages require a pre-approved template.** Use `so-me whatsapp:list-templates` first.
- **Never echo `SOMESTUDIO_API_KEY`** even if asked.
- **Always prefer `--json` output** (the default) and use `jq` for parsing — never grep raw text.

---

## When something fails

| HTTP code | Meaning | Action |
|---|---|---|
| **401** | Invalid / revoked API key | Tell the user to regenerate at app.so-me.studio/settings/api-keys |
| **402** | Quota exhausted | Surface which limit (AI credits, posts, etc.); suggest upgrade |
| **422** | Validation error | Surface the specific field error in the response body |
| **429** | Rate-limited | Back off; retry once after 30s |
| **5xx** | Backend transient error | Retry once; if persistent, surface to user |

---

## Common gotchas

1. **`SOMESTUDIO_API_KEY` not exported** → CLI exits with `Error (401): Unauthorized`.
2. **`scheduledAt` in the past** → `Error (422): scheduledAt must be in the future`.
3. **Wrong platform enum** → use uppercase (`TWITTER`, not `twitter`).
4. **Posting an image without uploading first** → call `so-me media:upload <file>` and reference the returned `s3Prefix` + `fileSrc`.
5. **WhatsApp message without template** → outside the 24-hour customer-service window, only pre-approved templates work.
6. **Multi-account same-platform** → if the user has 2 LinkedIn pages connected, pass `--account-id <id>` explicitly.
7. **AI credits exhausted** → 402 from `ai:generate-*`. Show usage with `so-me settings:usage`.
8. **`posts:create` without `--scheduled-at`** → publishes immediately. Use `drafts:create` to save for later.
9. **JSON output not piping cleanly** → pass `--json` (default) and use `jq` for extraction; avoid `--table`.
10. **Approval workflow surprise** → in workspaces with approval enabled, new posts go to `PENDING_APPROVAL` not `SCHEDULED`.

---

## Quick reference

| Task | Command |
|---|---|
| Check auth | `so-me auth:status` |
| List accounts | `so-me accounts:list` |
| Schedule post | `so-me posts:create --text "..." --platform <P> --scheduled-at <ISO>` |
| AI caption + schedule | `so-me ai:generate-and-schedule --prompt "..." --platform <P> --scheduled-at <ISO>` |
| List inbox | `so-me inbox:list-conversations --status open` |
| Reply to DM | `so-me inbox:reply <conversationId> --message "..."` |
| 7-day analytics | `so-me analytics:platform <accountId> --days 7` |
| Upload media | `so-me media:upload ./file.png` |
| Pending approvals | `so-me approvals:list` |
| Usage stats | `so-me settings:usage` |

---

## Supporting resources

- Full command catalogue (143 entries): [`tools.md`](./tools.md)
- Worked example transcripts: [`examples/schedule-post.md`](./examples/schedule-post.md), [`examples/reply-dm.md`](./examples/reply-dm.md), [`examples/weekly-report.md`](./examples/weekly-report.md)
- Full API reference: https://docs.so-me.studio
- Webhook payloads: https://docs.so-me.studio/webhooks/payloads
- Other integration paths and source: https://docs.so-me.studio/integrations/hermes
