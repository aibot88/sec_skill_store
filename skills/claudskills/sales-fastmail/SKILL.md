---
name: sales-fastmail
description: "Fastmail platform help — independent privacy-respecting email with full JMAP API, custom domains, Masked Email aliases, calendar/contacts/files, OAuth 2.0, IMAP/SMTP/CardDAV/CalDAV/WebDAV, CORS-enabled, community MCP server (Individual ~$5/mo / Business Standard ~$5/user/mo, 20+ years independent, no ads). Use when setting up Fastmail with a custom domain for your business, JMAP API calls failing or session auth not working, building automations against the Fastmail JMAP API with Python or JavaScript, Masked Email aliases not creating or hitting rate limits, comparing Fastmail to Proton Mail or Gmail or Hey for solopreneur email, migrating from Gmail or Outlook to Fastmail, Fastmail calendar not syncing with Google Calendar, connecting the Fastmail MCP server to Claude Desktop, choosing between Fastmail Individual and Business plans, or wondering why Fastmail has no native Zapier or Make integration. Do NOT use for AI email drafting or smart inbox triage (use /sales-superhuman or /sales-shortwave). Do NOT use for team shared inbox with ticketing (use /sales-hiver or /sales-missive). Do NOT use for end-to-end encrypted email (use /sales-proton-mail)."
argument-hint: "[describe what you need help with in Fastmail]"
license: MIT
version: 1.0.0
tags: [sales, email-provider, api, jmap, privacy, platform]
github: "https://github.com/fastmail"
---

# Fastmail Platform Help

Helps with everything related to using Fastmail — the independent, privacy-respecting email service with a full JMAP API, custom domains, Masked Email aliases, and integrated calendar/contacts/files. 20+ years independent, no ads, standards-first.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Fastmail?**
   - A) Evaluating Fastmail — is it right for me?
   - B) Migrating from Gmail/Outlook/another provider
   - C) Building with the JMAP API (read, send, search, masked email)
   - D) Comparing Fastmail to alternatives (Proton Mail, Hey, Gmail)
   - E) Setting up custom domains, aliases, or Masked Email
   - F) Troubleshooting sync, calendar, or search issues
   - G) Connecting the MCP server to Claude Desktop
   - H) Something else — describe it

2. **Which plan are you on (or considering)?**
   - A) Individual (~$5/mo — 60 GB, custom domains, Masked Email)
   - B) Duo (~$8/mo — 2 people, shared calendars)
   - C) Family (~$11/mo — 6 people, 360 GB)
   - D) Business Basic (~$3/user/mo — 6 GB, shared email)
   - E) Business Standard (~$5/user/mo — 60 GB, custom domains)
   - F) Business Professional (~$9/user/mo — 150 GB, retention archive)
   - G) Not sure yet

**If the user's request already provides most of this context, skip directly to the relevant step.**

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| AI email drafting or triage | `/sales-superhuman {question}` or `/sales-shortwave {question}` |
| End-to-end encrypted email | `/sales-proton-mail {question}` |
| Team shared inbox with ticketing | `/sales-helpdesk-selection {question}` |
| Inbox cleanup / unsubscribe | `/sales-clean-email {question}` |
| Server-side email filtering | `/sales-sanebox {question}` |
| Meeting scheduling | `/sales-meeting-scheduler {question}` |

When routing to another skill, provide the exact command.

If the question is about Fastmail itself, continue to Step 3.

## Step 3 — Fastmail platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, JMAP API quick-start, migration, MCP server setup.

**Read `references/fastmail-api-reference.md`** for detailed API documentation — authentication, endpoints, OAuth flow, Masked Email methods.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Evaluating Fastmail**: Match their priorities. If they need E2E encryption, Proton is better. If they need API access and speed, Fastmail excels. If they need AI, neither — suggest Superhuman or Shortwave.
- **Migration**: Use the built-in import tool for Gmail/Outlook. Warn about re-training contacts to use new address.
- **JMAP API**: Start with API token auth (simplest). Use OAuth 2.0 with PKCE for production apps. Session endpoint returns all account info.
- **Masked Email**: Rate limits apply on creation. Use for signups, newsletters, vendor forms. Integrates natively with 1Password and Bitwarden.
- **MCP server**: Community-built (jmhron/FastMailMCP). Requires API token. 7 tools for mailbox management, email search, reading, and sending.

If you discover a gotcha or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about pricing and plan features that may change.*

- **No native Zapier/Make integration.** Unlike many SaaS tools, Fastmail has no official Zapier or Make connector. Automate via JMAP API directly, IMAP polling, or webhook workarounds.
- **Calendar JMAP not yet available.** Calendar is CalDAV-only. JMAP calendar support is planned but not shipped yet. Contacts work via both JMAP and CardDAV.
- **Price increases.** Fastmail raised prices ~40% in late 2025. Current EUR pricing may differ from older USD references you find online.
- **Android app reported as weak.** The web app and iOS are well-regarded; Android has received complaints about UX quality.
- **No AI features.** Unlike Superhuman or Shortwave, Fastmail has no AI drafting, categorization, or smart inbox. It's a traditional email client with excellent API access.
- **MCP server is community-built.** The FastMailMCP server is not official. It works well but may lag behind API changes.
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Related skills

- `/sales-proton-mail` — Proton Mail privacy-first encrypted email (E2E encryption, zero-access, no API). Install:
  `npx skills add sales-skills/sales --skill sales-proton-mail -a claude-code`
- `/sales-hey` — Hey opinionated email service (Screener, Imbox/Feed/Paper Trail, $99/yr). Install:
  `npx skills add sales-skills/sales --skill sales-hey -a claude-code`
- `/sales-superhuman` — Superhuman fastest AI email client (Split Inbox, AI Write, MCP server, $25-40/mo). Install:
  `npx skills add sales-skills/sales --skill sales-superhuman -a claude-code`
- `/sales-shortwave` — Shortwave AI-native Gmail client (AI filters, Ghostwriter, MCP consumer, $24-100/mo). Install:
  `npx skills add sales-skills/sales --skill sales-shortwave -a claude-code`
- `/sales-em-client` — eM Client desktop email client (PGP, calendar/tasks, works with Fastmail via IMAP). Install:
  `npx skills add sales-skills/sales --skill sales-em-client -a claude-code`
- `/sales-spark-mail` — Spark Mail cross-platform AI email client (works with Fastmail via IMAP). Install:
  `npx skills add sales-skills/sales --skill sales-spark-mail -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (works with Fastmail). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-clean-email` — Clean Email inbox cleanup (works with any IMAP provider including Fastmail). Install:
  `npx skills add sales-skills/sales --skill sales-clean-email -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Query emails via JMAP API
**User says**: "How do I search for emails from a specific sender using the Fastmail JMAP API?"
**Skill does**:
1. Reads API reference for JMAP authentication and Email/query method
2. Shows: get API token from Settings → Privacy & Security → Manage API tokens
3. Provides working cURL example: POST to apiUrl with Email/query + filter by `from` field
4. Explains result references: chain Email/query → Email/get to fetch full message properties
5. Notes: use `properties` parameter to limit returned fields for performance
**Result**: Working API example with auth and query chain

### Example 2: Should I use Fastmail or Proton Mail?
**User says**: "I'm a solopreneur choosing between Fastmail and Proton Mail. I need custom domain email and might want to automate things."
**Skill does**:
1. Compares: Fastmail has full JMAP API, OAuth 2.0, MCP server; Proton has no API at all
2. Notes: Proton offers E2E encryption; Fastmail uses TLS + AES at rest (strong but not E2E)
3. Pricing: comparable — Fastmail Individual ~$5/mo vs Proton Mail Plus ~$4/mo for custom domain
4. Key decision: if automation/API matters, Fastmail wins decisively. If E2E encryption is top priority, Proton wins.
5. Neither has AI features — for AI email, suggest Superhuman or Shortwave
**Result**: Clear decision framework based on API needs vs encryption priority

### Example 3: Set up Masked Email with 1Password
**User says**: "How do I use Fastmail's Masked Email feature with 1Password to generate unique email addresses for each service?"
**Skill does**:
1. Reads platform guide for Masked Email section
2. Explains: in 1Password, when creating a new login, click the email field → "Generate Masked Email"
3. Notes: requires Fastmail Individual+ plan and 1Password connected via Settings → Privacy & Security
4. Warns about rate limits on Masked Email creation via API
5. Tip: use `forDomain` to track which service each alias belongs to
**Result**: Step-by-step 1Password integration with rate limit awareness

## Troubleshooting

### JMAP API returns 401 Unauthorized
**Symptom**: API calls fail with 401 even though you have a token
**Cause**: Token may be expired, revoked, or missing the required scope. API tokens and app passwords are different — API tokens work with JMAP, app passwords work with IMAP/SMTP.
**Solution**: 1) Verify you're using an API token (not app password) for JMAP. 2) Check token has required scopes (at minimum `urn:ietf:params:jmap:core`). 3) Use `Authorization: Bearer {token}` header. 4) If using OAuth, check if access token expired and refresh via `/oauth/refresh`.

### Calendar not syncing with Google Calendar
**Symptom**: Events added in Fastmail don't appear in Google Calendar or vice versa
**Cause**: Fastmail calendar uses CalDAV, not a direct Google sync. Two-way sync requires subscribing to each other's calendar URLs.
**Solution**: 1) In Fastmail, go to Calendars → Subscribe → paste your Google Calendar ICS URL. 2) In Google Calendar, go to Other calendars → From URL → paste your Fastmail CalDAV URL. 3) Note: this is read-only subscription sync, not true two-way sync. For full sync, use a bridge like CalDAV-to-Google tools.

### Masked Email creation fails with rate limit error
**Symptom**: MaskedEmail/set returns `rateLimit` SetError
**Cause**: Fastmail rate-limits Masked Email creation to prevent abuse. Creating many aliases in quick succession triggers this.
**Solution**: 1) Wait and retry — rate limits reset after a cooling period. 2) Batch creations with delays between them. 3) If building an integration, implement exponential backoff on `rateLimit` errors.
