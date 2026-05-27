---
name: sales-parsestream
description: "ParseStream platform help — multi-platform keyword monitoring across Reddit, X, LinkedIn, Quora, and Hacker News with AI reply drafts and auto-reply via Reddit OAuth. Use when ParseStream alerts are returning too much noise and you need to narrow keywords or subreddits, AI-generated replies sound robotic and don't match your brand voice, auto-reply timing feels unnatural and you're worried about Reddit spam detection, you're not getting email notifications for keywords you know are being discussed, you want to monitor multiple platforms but only see results from one, you need to restrict monitoring to specific subreddits or exclude communities, or you're comparing ParseStream vs KeyMentions vs RedShip vs Syften for multi-platform monitoring. Do NOT use for social listening strategy across tools (use /sales-social-listening) or choosing between monitoring platforms (use /sales-social-listening)."
argument-hint: "[describe what you need help with in ParseStream — e.g., 'auto-replies are getting flagged as spam']"
license: MIT
version: 1.0.0
tags: [sales, social-listening, reddit, platform]
---

# ParseStream Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What do you need help with?**
   - A) Setting up keyword monitoring (keywords, platforms, subreddit filters)
   - B) Reducing noise / improving relevance of alerts
   - C) AI reply quality and customization
   - D) Auto-reply configuration and account safety
   - E) Email notification issues
   - F) Something else — describe it

2. **Which platforms are you monitoring?**
   - A) Reddit only
   - B) Reddit + X/Twitter
   - C) Reddit + LinkedIn + Quora
   - D) All five (Reddit, X, LinkedIn, Quora, HN)

3. **What's your goal?**
   - A) Lead generation (find people asking for recommendations)
   - B) Brand monitoring (track mentions of my product)
   - C) Competitor monitoring (watch competitor discussions)
   - D) Content engagement (reply to relevant conversations)

**If the user's request already provides context, skip to Step 2.**

## Step 2 — Route or answer directly

- Multi-platform monitoring strategy or tool comparison → `/sales-social-listening [question]`
- Reddit monitoring with AI relevance scoring (0-100) → `/sales-redship [question]`
- Reddit monitoring with auto-publish comments → `/sales-keymentions [question]`
- Reddit + Quora with forced manual posting → `/sales-threadradar [question]`
- Reddit monitoring across 15+ community platforms → `/sales-syften [question]`
- Audience intelligence and pain point research → `/sales-reddinbox [question]`

Otherwise, answer directly from the platform reference below.

## Step 3 — ParseStream platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, monitoring setup, reply customization, and account safety guidance.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Based on the user's situation:

1. **Noise reduction** — narrow keywords with subreddit inclusion/exclusion, adjust AI filtering settings
2. **Reply quality** — customize brand context, select appropriate response style, adjust length
3. **Account safety** — understand timing delays, queue limits, recognize ban signals early
4. **Platform coverage** — configure per-platform monitoring, prioritize high-intent platforms
5. **Notification tuning** — set up filters to only alert on high-relevance mentions

If you discover a gotcha not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research — review these, especially items about pricing and capabilities that may change.*

- **Pricing is not publicly disclosed.** Third-party sources report ~$29-79/mo across Lite/Pro/Growth/Enterprise tiers, but ParseStream doesn't publish prices on their site. Expect to see pricing only after signup or during trial.
- **No Slack integration.** Email-only alerts. If your team lives in Slack, this is a dealbreaker — consider Syften or RedShip instead.
- **No API, webhooks, or Zapier.** Entirely UI-driven. You cannot pipe ParseStream data into a CRM, dashboard, or automation workflow. If programmatic access matters, use RedShip ($19/mo, REST API + webhooks on all plans) or Syften (REST API + webhooks).
- **Auto-reply carries Reddit ban risk.** Smart timing delays reduce but don't eliminate risk. Reddit actively detects automated engagement. Use manual review mode for high-value accounts.
- **Very new product (launched mid-2025).** No reviews on G2, Capterra, or Product Hunt. Limited track record. Evaluate carefully during trial.
- **No multi-project support.** You can't separate monitoring for different products or brands into distinct workspaces.
- **No AI relevance scoring.** Unlike RedShip (0-100 scoring), ParseStream uses binary AI filtering (relevant/not) without granular prioritization.

## Related skills

- `/sales-social-listening` — Social listening strategy — tool comparison, monitoring setup, competitive intel, crisis detection
- `/sales-redship` — RedShip platform help — AI-scored Reddit monitoring with SEO post discovery, REST API + webhooks, $19/mo
- `/sales-keymentions` — KeyMentions platform help — Reddit keyword monitoring with AI comment generation and auto-publish
- `/sales-syften` — Syften platform help — 15+ community platforms with sub-minute Reddit alerts, Boolean search, API + webhooks
- `/sales-threadradar` — ThreadRadar platform help — Reddit + Quora with AI-drafted replies, forced manual posting (safer)
- `/sales-replyguy` — ReplyGuy platform help — AI reply generation across Twitter, Reddit, LinkedIn
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Auto-replies getting flagged
**User says**: "My Reddit account keeps getting warned after using ParseStream auto-reply. How do I avoid getting banned?"
**Skill does**:
1. Reads platform guide for auto-reply safety settings
2. Recommends switching to manual review mode for the warned account
3. Advises reducing reply frequency, varying response styles, and ensuring replies add genuine value
4. Suggests creating a new Reddit account specifically for engagement (separate from main brand account)
**Result**: Clear safety strategy to reduce ban risk while maintaining engagement

### Example 2: Too much noise in alerts
**User says**: "I'm getting hundreds of irrelevant emails from ParseStream. Most mentions have nothing to do with my product."
**Skill does**:
1. Reviews current keyword setup and suggests narrower, more specific keywords
2. Recommends using subreddit exclusion filters to block high-noise communities
3. Suggests adding brand context to help AI filtering distinguish relevant from irrelevant mentions
4. Notes that without AI relevance scoring, binary filtering means some noise is inevitable
**Result**: Refined monitoring setup that reduces alert volume to actionable mentions

### Example 3: Comparing ParseStream to alternatives with API access
**User says**: "I need to pipe monitoring data into my CRM. Can ParseStream do this?"
**Skill does**:
1. Confirms ParseStream has no API, webhooks, or iPaaS support — entirely UI-driven
2. Recommends alternatives with programmatic access: RedShip ($19/mo, REST API + webhooks on all plans), Syften (REST API Standard+, webhooks PRO), or Octolens ($119/mo, REST + webhooks + MCP server)
3. Routes to `/sales-social-listening` for a full comparison of tools with developer-friendly integrations
**Result**: Clear answer that ParseStream can't do this, with actionable alternatives

## Troubleshooting

### Auto-reply account getting rate-limited or banned
**Symptom**: Reddit account receives warnings, shadowban, or suspension after using ParseStream auto-reply
**Cause**: Automated replies detected by Reddit's anti-spam systems despite timing delays
**Solution**: Switch to manual review mode immediately. Reduce reply volume (aim for 3-5 genuine replies per day max). Ensure every reply adds unique value — don't use templates. Vary reply length and style. Consider using a dedicated engagement account separate from your main brand account. Wait 2-4 weeks before re-enabling any automated features on a warned account.

### Missing mentions from specific platforms
**Symptom**: You know discussions are happening on X or LinkedIn but ParseStream isn't alerting you
**Cause**: Platform coverage varies — Reddit typically has best coverage; LinkedIn and Quora may have gaps
**Solution**: Verify the platform is enabled in your monitoring settings. Try broader keywords for underperforming platforms. Note that LinkedIn monitoring is limited to public posts only (not private groups). If a specific platform consistently misses mentions, consider supplementing with a platform-specific tool.

### AI replies sound generic and promotional
**Symptom**: Suggested replies read like ads and would clearly get downvoted on Reddit
**Cause**: Default AI settings without brand context customization produce generic responses
**Solution**: Update brand context with specific product details, value props, and tone guidelines. Select the "value-first" or "founder story" response style instead of direct pitch. Reduce reply length. Add instructions to never mention product in the first sentence. Always review and heavily edit AI suggestions before posting — treat them as rough drafts, not final copy.
