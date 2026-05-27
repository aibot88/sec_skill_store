---
name: linkedin-feed-engage
description: Auto-comment on LinkedIn posts authored by your ICP — scroll the feed, identify posts from target prospects, and post relevant value-adding comments to build visibility before outreach. Use when the user says "auto-comment", "engage on feed", "comment on prospects' posts", "warm up before outreach", "build LinkedIn visibility", "feed engagement", or "comment automation".
---

# Auto-comment on ICP Feed

The premise: commenting thoughtfully on a prospect's post before sending an invite raises accept rate by 30-50%. They've seen your name and read something useful from you. This skill scrolls your LinkedIn feed, identifies posts authored by ICP-matching profiles, and posts a value-adding comment on each.

## Required prerequisites — check before you start

1. **`linkupapi` MCP connected.** Verify with `linkupapi_list_accounts`.
   - If the list is **empty**, tell the user they have two options to connect a LinkedIn account, then stop and wait:
     - **Hosted UI** — open https://app.linkupapi.com/account-connection (fastest, handles checkpoints in-browser).
     - **MCP login** — run `linkupapi_login` directly (platform=linkedin, with email+password OR a `login_token`). On `checkpoint_required` → run `linkupapi_checkpoint`.
2. **Pick the sending account** before Stage 1. After confirming at least one `status = connected` account exists, present the connected accounts via `AskUserQuestion` (single-select). Each option label is the account display name; description shows email + country. The chosen `account_id` is the one whose feed will be scrolled and that will post the comments.
3. The user must already know their ICP — this skill is NOT a discovery tool, it filters an existing feed against a known ICP.

## Daily LinkedIn safety caps (MANDATORY — enforced)

- **100 profile gets / day** — used for borderline ICP-match verification
- **15 searches / day** — generally not consumed by this skill (feed ≠ search)
- **Comment volume**: LinkedIn soft-caps around 30-50 comments/day. This skill **defaults to 15 comments / day max** to stay safely below.

**Before Stage 1**, run `linkupapi_get_logs` for last 24h on the chosen account, count today's `linkedin_profiles/get` and `linkedin_content/comment` (or whichever action posts a comment — confirm via tool schema). Compute remaining budget per category. Never override.

## Stage 0 — ICP + comment style

`AskUserQuestion`:

1. **ICP** — same shape as `linkedin-outreach` Stage 0. Offer to reuse `./icp/*.json` if present.
2. **Topic filter** — optional keywords the post body must contain (e.g. "outbound", "hiring", "AI sales"). Empty = no topic constraint, just author match.
3. **Comment style**:
   - **Auto-generate (recommended)** — agent reads each post + writes a 2-3 sentence value-adding comment in real time
   - **Templates with variables** — user provides 3-5 templates with `{post_topic}` / `{author_first_name}` placeholders, agent picks one per post
   - **Manual approval (HITL)** — agent drafts each, user approves/edits/skips before posting
4. **Volume cap** — max comments today (hard ceiling = 15)
5. **Time window** — only posts authored in the last X hours (default 48h; older posts have low engagement ROI)

Echo the brief with budget math + the daily cap remaining, wait for "yes".

## Stage 1 — Pull the feed

Tool: `linkedin_content`. Load schema with `ToolSearch query="select:mcp__linkupapi__linkedin_content"`. Likely action: `get_feed` or `get_user_feed`.

```json
{"account_id": "...", "action": "get_feed", "params": {"limit": 100}}
```

Pull 50-100 recent posts. Each result should include `post_url`, `author_profile_url`, `author_name`, `author_headline`, `post_text` (or excerpt), `posted_at`, `engagement_count`.

Drop immediately:
- Posts older than the time window
- Reposts where the user authored neither the original nor the repost commentary
- Promoted/sponsored posts (they're ads, not organic)
- Posts the user has already commented on (check `viewer_has_commented` if available)

## Stage 2 — Pre-filter on visible author signal

For each post, score the AUTHOR against ICP using only visible fields (`author_headline`, `author_name`):
- ✅ Headline matches ICP roles/industry → KEEP
- ❌ Clear mismatch → DROP
- ⚠️ Ambiguous → keep for Stage 3 enrichment IF budget permits

Then apply the topic filter on `post_text`:
- KEEP if post_text contains any topic keyword (case-insensitive substring or semantic match)
- If user provided no topic filter, skip this check

No tool calls at this stage — pure LLM judgment.

## Stage 3 — Enrich borderline authors (budget-aware)

For ⚠️ ambiguous authors only, run `linkedin_profiles get` to verify current role.

**Cap this stage at 1/3 of today's remaining profile budget.** Never exhaust the 100/day on Stage 3 — leave room for the user's other workflows (`linkedin-outreach`, `linkedin-enrich`).

Drop authors whose enriched current role doesn't match the ICP.

## Stage 4 — Generate comments

For each kept post, generate a comment per the chosen style.

**Auto-generated comment principles**:
- 2-3 sentences max (≤300 chars ideal)
- Add value — don't just agree. Worst possible comment: "Great post!"
- Reference a specific point from `post_text` (proves you read it, not just scrolled)
- End with an open question or insight, not a CTA / pitch
- No emojis unless the post itself uses them
- No links (LinkedIn ranks comments with links lower)
- No name-drop of the user's company unless directly relevant

Example shape:
> "The point about {specific_thing_from_post} resonates — we've seen the same pattern with {related_observation}. Curious whether {open_question}?"

If user picked **HITL**, surface each draft with `post_excerpt + author + comment_draft` and wait for approve / edit / skip per post. Don't batch the approvals.

## Stage 5 — Post comments (paced, cap-aware)

Use `linkedin_content` action that posts a comment (`comment` / `post_comment` — confirm via schema).

```json
{"account_id": "...", "action": "comment", "params": {"post_url": "...", "comment_text": "..."}}
```

**Pacing rules** (non-negotiable):
- Sleep **30-60 seconds** between comments. Comment cadence is the most-watched anti-bot signal — 15 comments in 5 minutes will get flagged.
- Vary the sleep duration randomly within that range.
- Stop immediately if today's 15-comment cap is reached.
- Stop immediately if any call returns a rate-limit error or 429.

If the run starts producing errors mid-batch, stop and surface to the user — don't retry blindly.

## Stage 6 — Persist & report (mandatory)

Write `./campaigns/{YYYY-MM-DD}-feed-engage.md`:
1. ICP definition + topic filter
2. Feed scan stats: posts pulled / matched author / matched topic / commented
3. Comment style used
4. Per-comment table: `# | post_url | author | author_company | comment_posted | timestamp`
5. Daily caps remaining
6. Skipped posts and why (already commented / topic mismatch / borderline dropped for budget)

Concise on-screen summary.

## Pre-handoff to outreach

When `linkedin-outreach` runs later this week and the prospect list overlaps with authors commented on this week, **the outreach skill should reference the comment in the invite note** — accept rate jumps significantly. The campaign log here is the source of truth for that cross-reference. Make sure `author_profile_url` is captured in the log so the outreach skill can match.

## Common pitfalls

- **Comment cadence too fast**: 15 in an hour = flag. Default 30-60s + random jitter.
- **Generic praise comments**: "Great post!" / "Love this!" — kill credibility AND get demoted in feed ranking. Always reference something specific.
- **Templated phrasing**: LinkedIn fingerprints repeated phrases across an account. Vary every comment, don't reuse opener words.
- **Controversial content**: skip posts about politics, layoffs, personal news unless the user explicitly opts in.
- **Old posts**: comments on posts >72h old get low visibility. Filter to last 48h by default.
- **Author replies expected**: when the author replies to your comment, the user should engage back manually within 24h (no automation here — too risky).

## Tool quick reference

| Tool | Action | Daily cap |
|---|---|---|
| `linkedin_content` | `get_feed` | — |
| `linkedin_profiles` | `get` | **100/day shared** |
| `linkedin_content` | `comment` / `post_comment` | **15/day (this skill)** |
| `linkupapi_get_logs` | — | run at Stage 0 |
