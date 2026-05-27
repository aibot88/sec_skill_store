---
name: sales-konnectinsights
description: "Konnect Insights platform help — omnichannel CXM with social listening, social CRM, unified inbox (30+ channels), analytics, publishing, crisis management, Zapier integration, REST API. Use when Konnect Insights mentions are full of irrelevant noise and you need to tighten keyword queries, the unified inbox is overwhelming and you need to organize ticket routing, social listening dashboards don't show the metrics your stakeholders care about, Zapier triggers aren't firing for new mentions or tickets, API authentication isn't working with your account token and user token, or you need to connect Konnect Insights to your CRM (Salesforce, HubSpot, Zoho). Do NOT use for social listening strategy across tools (use /sales-social-listening) or choosing between social listening platforms (use /sales-social-listening)."
argument-hint: "[describe what you need help with in Konnect Insights — e.g., 'how do I set up crisis alerts' or 'Zapier trigger not firing']"
license: MIT
version: 1.0.0
tags: [sales, social-listening, cxm, platform]
---

# Konnect Insights Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What do you need help with?**
   - A) Setting up social listening (keywords, sources, alerts)
   - B) Configuring the unified inbox and ticket routing
   - C) Social analytics and dashboards
   - D) Social publishing and scheduling
   - E) Crisis detection and alerts
   - F) API or Zapier integration
   - G) CRM connection (Salesforce, HubSpot, Zoho)
   - H) Something else — describe it

2. **Which plan are you on?**
   - A) Getting Started ($29/user/mo)
   - B) Startup / Standard ($99+/mo)
   - C) Standard Plus or Custom/Enterprise
   - D) Trial
   - E) Not sure

**If the user's request already provides most of this context, skip directly to Step 2.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end.

## Step 2 — Route or answer directly

If the request maps to a broader strategy:
- Social listening strategy or tool comparison → `/sales-social-listening [question]`
- Social media publishing strategy → `/sales-social-media-management [question]`
- CRM selection or comparison → `/sales-crm-selection [question]`
- Help desk strategy → `/sales-helpdesk-selection [question]`

Otherwise, answer directly from the platform reference below.

## Step 3 — Konnect Insights platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, data model, integration recipes, code examples.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Based on the user's specific question:

1. **Listening setup** — design keyword strategy, configure sources, set up alert thresholds
2. **Inbox management** — set up ticket routing rules, priority tags, SLA timers
3. **Dashboard design** — build reports for stakeholders, configure widgets
4. **Integration** — connect to CRM, set up Zapier workflows, use API endpoints
5. **Crisis plan** — configure real-time alerts, design escalation workflow

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

- **Zapier requires the "All-in-one" plan.** If you're on Getting Started or Startup, Zapier integration won't work — you need to upgrade or use native integrations instead.
- **No TikTok monitoring.** Konnect Insights does not currently capture TikTok activity. If TikTok is important, supplement with another tool.
- **Advanced workflow setup takes time.** Configuring custom dashboards and automation rules for specific client reporting formats requires initial investment — start with pre-built templates.
- **Support response times can be slow.** Implementation requests and feedback may take longer than expected. Plan for self-service configuration where possible.
- **API docs are partially JS-rendered.** The developer portal at developer.konnectinsights.com may not show all endpoints without JavaScript. Use Zapier triggers as an alternative integration path.
- **Pricing is volume-based.** Costs scale with mention volume and social profiles — monitor usage to avoid surprise charges.

## Related skills

- `/sales-social-listening` — Social listening strategy — tool comparison, monitoring setup, Boolean queries, sentiment, crisis detection
- `/sales-social-media-management` — Social media management strategy — publishing, scheduling, engagement
- `/sales-helpdesk-selection` — Help desk comparison and selection
- `/sales-crm-selection` — CRM comparison and selection
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Set up competitive monitoring
**User says**: "I want to track my brand and two competitors across social channels in Konnect Insights"
**Skill does**:
1. Reads platform-guide.md for listening setup details
2. Designs keyword groups for brand + competitors (including name variations)
3. Configures topic clusters for each brand
4. Sets up a Share of Voice comparison dashboard
**Result**: Competitive monitoring ready with grouped topics and comparison dashboard

### Example 2: Connect Konnect Insights to Salesforce
**User says**: "How do I sync social mentions from Konnect Insights into Salesforce as cases?"
**Skill does**:
1. Reads platform-guide.md for integration patterns
2. Explains the native Salesforce AppExchange integration
3. Shows Zapier alternative: trigger on "Get Messages by Topic" → create Salesforce Case
4. Notes that Zapier requires All-in-one plan
**Result**: Two integration paths with code and configuration steps

### Example 3: Crisis alerts aren't working
**User says**: "I set up crisis detection but I'm not getting alerts when negative mentions spike"
**Skill does**:
1. Checks alert configuration — threshold settings, delivery channel (email/Slack)
2. Verifies keyword query includes crisis terms combined with brand
3. Checks if mention volume is high enough to trigger threshold alerts
4. Suggests testing with lower thresholds then adjusting up
**Result**: Alert configuration fixed with proper thresholds and delivery

## Troubleshooting

### Zapier triggers not firing
**Symptom**: Konnect Insights Zap is set up but no data flows
**Cause**: Wrong plan (need All-in-one), or incorrect Group ID / Topic ID in trigger config
**Solution**: Verify you're on the All-in-one plan. Check that Group ID and Topic ID fields match your actual Konnect Insights groups (find IDs in the platform's URL bar or via the "Get Groups" / "Get Topics" triggers). Test with a simple "Get Groups" trigger first to confirm authentication works.

### Dashboard metrics don't match expectations
**Symptom**: Numbers in analytics dashboards don't align with what you see in the inbox
**Cause**: Dashboard date range filters, source filters, or topic filters don't match inbox view
**Solution**: Reset all filters to the same date range and sources. Check if the dashboard aggregates across all topics while the inbox shows a single topic. Verify that sentiment tags haven't been manually overridden on specific tickets.

### Unified inbox is overwhelming
**Symptom**: Too many tickets across 30+ channels, team can't keep up
**Cause**: No routing rules, no priority system, all channels dumping into one queue
**Solution**: Set up cluster-based routing — assign topics to specific team members. Create priority rules (crisis keywords → P1, complaints → P2, general → P3). Use auto-assignment to distribute load. Start with fewer channels and expand as capacity allows.
