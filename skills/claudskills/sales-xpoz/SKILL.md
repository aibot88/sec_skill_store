---
name: sales-xpoz
description: "Xpoz platform help — social data API and MCP server for AI agents, searching Twitter/X, Instagram, TikTok, Reddit via natural language queries, 1.5B+ indexed posts, OAuth 2.1, TypeScript/Python SDKs, CSV exports. Use when Xpoz MCP server isn't connecting or authenticating, search results are returning irrelevant posts and you need better queries, CSV exports are timing out or returning incomplete data, you want to build a brand monitoring pipeline using the Xpoz SDK, you're hitting the 100K free tier limit and need to understand upgrade options, or you need to compare Xpoz vs Octolens vs Brand24 for developer-first social listening. Do NOT use for social listening strategy across tools (use /sales-social-listening) or choosing between social listening platforms (use /sales-social-listening)."
argument-hint: "[describe what you need help with in Xpoz — e.g., 'MCP server not connecting' or 'how to search Reddit posts by keyword']"
license: MIT
version: 1.0.0
tags: [sales, social-listening, social-data-api, mcp, platform]
github: "https://github.com/XPOZpublic"
---

# Xpoz Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What do you need help with?**
   - A) MCP server setup or connection issues
   - B) Search queries returning bad results
   - C) SDK integration (TypeScript or Python)
   - D) CSV exports and async operations
   - E) Understanding pricing/limits
   - F) Building a monitoring pipeline
   - G) Something else — describe it

2. **Which access method are you using?**
   - A) MCP server (Claude Desktop, Cursor, Windsurf, Claude Code)
   - B) TypeScript SDK (`@xpoz/xpoz`)
   - C) Python SDK (`xpoz`)
   - D) Haven't started yet

3. **Which plan are you on?**
   - A) Free (100K results/mo)
   - B) Pro ($20/mo, 1M results)
   - C) Max ($200/mo, 10M results)
   - D) Not sure

**If the user's request already provides most of this context, skip directly to Step 2.**

## Step 2 — Route or answer directly

- Social listening strategy or tool comparison → `/sales-social-listening [question]`
- Brand monitoring setup methodology → `/sales-social-listening [question]`
- Octolens-specific questions → `/sales-octolens [question]`
- Brand24 questions → `/sales-brand24 [question]`
- Influencer discovery → `/sales-influencer-marketing`

Otherwise, answer directly from the platform reference below.

## Step 3 — Xpoz platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, MCP tools inventory, SDK usage, data model, integration recipes, code examples.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Based on the user's specific situation:

1. **MCP setup** — verify config JSON, check OAuth flow, test with simple query
2. **Query optimization** — use platform-specific tools, add date filters, limit results
3. **Pipeline building** — choose SDK vs MCP, handle pagination, implement caching
4. **Exports** — use async operations with status polling for large datasets
5. **Cost management** — monitor result counts, use caching to reduce API calls

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

- **TikTok tools are "coming soon."** Don't build pipelines relying on TikTok data from Xpoz yet — it's listed but not fully available.
- **No webhooks or push notifications.** Xpoz is pull-only (MCP queries or SDK calls). You must poll for new data — there's no way to get notified when new mentions appear.
- **Free tier is generous but has no tracked items.** The 100K results/month free tier gives 1 tracked item — you can search but can't set up persistent monitoring across multiple brands/keywords without upgrading.
- **OAuth requires Google account.** MCP authentication uses Google OAuth 2.1 — there's no API key option for MCP connections. SDKs use API keys obtained from xpoz.ai/get-token.
- **No Boolean search.** Unlike Awario or Brand24, you can't construct complex Boolean queries. Natural language and keyword filters are the query method.
- **Results are from indexed data, not real-time.** The 1.5B+ post database is continuously updated but there may be a lag between when content is posted and when it appears in Xpoz results. Use `forceLatest: true` for freshest data.
- **CSV exports are async.** Large exports (up to 500K rows) run as background operations — you must poll `checkOperationStatus` until complete.

## Related skills

- `/sales-social-listening` — Social listening strategy — tool comparison, monitoring setup, sentiment analysis, crisis detection, competitive intelligence
- `/sales-octolens` — Octolens platform help — developer-first social listening on GitHub, HN, Reddit, X, LinkedIn with MCP server and webhooks
- `/sales-brand24` — Brand24 platform help — social listening with MCP server, Storm Alerts, Share of Voice
- `/sales-awario` — Awario platform help — budget social listening with Boolean search and Awario Leads
- `/sales-mention` — Mention platform help — real-time media monitoring, REST API
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Set up MCP server in Claude Code
**User says**: "How do I connect Xpoz to Claude Code so I can search Twitter mentions?"
**Skill does**:
1. Provides the MCP config JSON with streamable-http transport
2. Explains OAuth flow — first query triggers Google login
3. Shows example natural language query for Twitter mentions
4. Lists available Twitter tools (searchTwitterUsers, getTwitterPostsByKeywords, etc.)
**Result**: Working MCP connection with first successful query

### Example 2: Build a brand monitoring script with Python SDK
**User says**: "I want to check Reddit every hour for mentions of my product and send them to Slack"
**Skill does**:
1. Shows Python SDK installation and API key setup
2. Provides code for Reddit post search with keyword filtering
3. Explains pagination and caching to stay within result limits
4. Adds Slack webhook integration for notifications
**Result**: Working Python script for Reddit monitoring pipeline

### Example 3: Optimize search queries for relevance
**User says**: "My Xpoz searches return too many irrelevant tweets — how do I filter better?"
**Skill does**:
1. Explains available filtering: date ranges, engagement thresholds, language
2. Shows how to use specific tools (getTwitterPostsByKeywords vs getTwitterPostsByAuthor)
3. Recommends using field selection to reduce noise
4. Suggests caching strategy to avoid re-fetching known results
**Result**: Refined query strategy returning relevant results

## Troubleshooting

### MCP server won't connect
**Symptom**: Claude Desktop or Cursor shows "connection failed" for Xpoz MCP
**Cause**: Usually incorrect config format, network issues, or OAuth not completed
**Solution**: Verify config uses `"type": "streamable-http"` and URL is exactly `https://mcp.xpoz.ai/mcp`. On first connection, complete the Google OAuth popup. Check that your firewall/VPN allows outbound HTTPS to mcp.xpoz.ai.

### Search returns zero results for known content
**Symptom**: You know a tweet/post exists but Xpoz returns nothing
**Cause**: Content may not yet be indexed, or query is too narrow
**Solution**: Try `forceLatest: true` to bypass cache. Broaden keyword terms. Check that the platform is supported (TikTok is limited). Xpoz indexes 1.5B+ posts but not every post — very recent or low-engagement content may have indexing delays.

### CSV export never completes
**Symptom**: `checkOperationStatus` keeps returning "processing" indefinitely
**Cause**: Export is too large or the operation timed out silently
**Solution**: Reduce the result set (add date filters, narrow keywords). Exports support up to 500K rows — if your query matches more, add constraints. Try `cancelOperation` and re-submit with tighter filters. Check your plan's result limit hasn't been exhausted for the month.
