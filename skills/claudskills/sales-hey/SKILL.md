---
name: sales-hey
description: "Hey platform help — opinionated privacy-first email service by 37signals with Screener sender approval, Imbox/Feed/Paper Trail organization, spy pixel blocking, and no AI by design ($99/yr personal, $12/user/mo domains). Use when setting up Hey for the first time and wondering if the workflow fits, frustrated that you can't import old emails into Hey, Hey search isn't finding emails you know exist, trying to decide between Hey and Superhuman or Shortwave or Fastmail, wondering if $999/yr for custom domain is worth it vs Hey for Domains at $12/user/mo, or comparing Hey's anti-AI philosophy to AI-powered alternatives. Do NOT use for AI email drafting (use /sales-superhuman or /sales-shortwave). Do NOT use for email deliverability for outbound (use /sales-deliverability)."
argument-hint: "[describe what you need help with in Hey]"
license: MIT
version: 1.0.0
tags: [sales, email-client, privacy, platform]
---

# Hey Platform Help

Helps with everything related to using Hey — the opinionated, privacy-first email service by 37signals that reimagines email with Screener, Imbox/Feed/Paper Trail, and deliberate anti-AI philosophy.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Hey?**
   - A) Evaluating Hey — is the workflow right for me?
   - B) Setting up Hey for the first time (personal or business)
   - C) Configuring Screener, Feed, or Paper Trail
   - D) Comparing Hey to alternatives (Superhuman, Shortwave, Fastmail, Proton Mail)
   - E) Dealing with migration — importing old emails or leaving Hey
   - F) Troubleshooting search, editor, or sync issues
   - G) Something else — describe it

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| AI email drafting or triage | `/sales-superhuman compare AI email clients` or `/sales-shortwave` |
| Email deliverability (outbound) | `/sales-deliverability {question}` |
| Meeting scheduling | `/sales-meeting-scheduler {question}` |
| Inbox cleanup / unsubscribe | `/sales-clean-email {question}` |
| Server-side email filtering | `/sales-sanebox {question}` |

When routing to another skill, provide the exact command.

If the question is about Hey itself (setup, workflow, comparison, troubleshooting), continue to Step 3.

## Step 3 — Hey platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, workflow details, migration guidance.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Evaluating Hey**: Match their workflow to Hey's philosophy. If they need AI, automation, or API access, Hey is not the right fit. If they want radical spam elimination and privacy, it excels.
- **Migration in**: Acknowledge the no-import limitation honestly. Suggest forwarding strategy.
- **Migration out**: Note that data export is available if they cancel.
- **Comparison**: Always compare on philosophy (Hey) vs speed (Superhuman) vs AI (Shortwave) vs independence (Fastmail).

If you discover a gotcha or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about pricing and features that may be outdated.*

- **No email import.** You cannot import existing emails when switching to Hey. Your old email stays in the old system. This is the #1 driver of churn.
- **@hey.com address required for personal plan.** You can't use a custom domain on the $99/yr plan — that requires HEY for Domains at $12/user/mo.
- **No public API, no webhooks, no Zapier/Make.** Hey is deliberately isolated. If you need automation, it's the wrong tool.
- **No AI features — by design.** Hey takes a "HI not AI" stance. No AI drafting, no AI triage, no smart categorization beyond the static Imbox/Feed/Paper Trail buckets.
- **Search is basic.** No advanced operators, no date-range filtering like Gmail. Finding old emails can be frustrating.
- **Leaving is hard.** Your @hey.com address dies when you cancel. Set up forwarding before letting the subscription lapse.

## Related skills

- `/sales-proton-mail` — Proton Mail privacy-first encrypted email (E2E encryption, zero-access, Bridge for IMAP, Free/$4/$10/mo). Install:
  `npx skills add sales-skills/sales --skill sales-proton-mail -a claude-code`
- `/sales-superhuman` — Superhuman email client (keyboard-driven speed, AI Write, MCP server, $25-40/mo). Install:
  `npx skills add sales-skills/sales --skill sales-superhuman -a claude-code`
- `/sales-shortwave` — Shortwave AI-native Gmail client (AI filters, Ghostwriter, MCP consumer, $7-24/mo). Install:
  `npx skills add sales-skills/sales --skill sales-shortwave -a claude-code`
- `/sales-spark-mail` — Spark Mail cross-platform AI email client (Smart Inbox, Gatekeeper, team collaboration, free tier). Install:
  `npx skills add sales-skills/sales --skill sales-spark-mail -a claude-code`
- `/sales-mimestream` — Mimestream native macOS Gmail client (Gmail API-powered, tracking prevention, no AI, $50/yr). Install:
  `npx skills add sales-skills/sales --skill sales-mimestream -a claude-code`
- `/sales-fastmail` — Fastmail independent email with full JMAP API, custom domains, Masked Email ($5/mo). Install:
  `npx skills add sales-skills/sales --skill sales-fastmail -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (smart folders, any email provider, $7/mo). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-clean-email` — Clean Email inbox cleanup (bulk actions, Auto Clean rules, Unsubscriber, $29.99/yr). Install:
  `npx skills add sales-skills/sales --skill sales-clean-email -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Evaluating Hey vs Superhuman
**User says**: "I get 150 emails a day and spend too much time in my inbox. Should I use Hey or Superhuman?"
**Skill does**:
1. Reads platform guide for comparison context
2. Explains the core philosophy difference: Hey reduces email stress via rigid organization (Screener eliminates unwanted senders, Feed corrals newsletters); Superhuman reduces stress via speed (process everything in sub-100ms, keyboard shortcuts, AI drafts)
3. Notes Hey has no AI, no automation, no API; Superhuman has AI Write, MCP server, CRM integrations
4. Compares pricing: Hey $99/yr vs Superhuman $300-480/yr
5. Recommends: if you want fewer emails reaching you at all, Hey. If you want to blast through all emails faster with AI help, Superhuman.
**Result**: Clear decision framework based on philosophy vs speed tradeoff

### Example 2: Setting up Hey for a small team
**User says**: "I want to move my 3-person startup to Hey. How does HEY for Domains work?"
**Skill does**:
1. Reads platform guide pricing section
2. Explains: HEY for Domains is $12/user/month, lets you use your custom domain (e.g., team@yourstartup.com)
3. Notes: each team member gets full Hey features (Screener, Feed, Paper Trail)
4. Warns: no shared inbox, no team collaboration features, no API for integrations — each account is fully independent
5. If they need shared inbox or collaboration, routes to `/sales-helpdesk-selection`
**Result**: User understands Hey for Domains setup and limitations for team use

### Example 3: Can I automate anything with Hey?
**User says**: "I want to auto-forward certain emails from Hey to my CRM. Is there an API or Zapier integration?"
**Skill does**:
1. Explains clearly: No. Hey has no public API, no webhooks, no Zapier/Make integration. It's deliberately isolated.
2. Notes the only workaround is setting up forwarding rules within Hey to send copies to another email that IS connected to your CRM
3. Suggests: if automation is critical, Hey may not be the right fit. Alternatives with API/automation: Superhuman (MCP server), Shortwave (MCP consumer), Fastmail (JMAP API), or Gmail itself
4. Routes to `/sales-superhuman` or `/sales-shortwave` if they want AI + automation
**Result**: Honest answer with workaround and alternative suggestions

## Troubleshooting

### Can't find old emails in search
**Symptom**: You know an email exists but search returns nothing
**Cause**: Hey's search is basic — no advanced operators, no date filtering, no Boolean logic. It searches subject and body text but may not index attachments or handle partial matches well.
**Solution**: 1) Try different keywords — use exact phrases the sender would have used. 2) Check Paper Trail and Feed separately — search may only search the current section. 3) Check The Screener — the email may be from an unapproved sender still waiting in screening. 4) If the email predates your Hey account, it wasn't imported (Hey doesn't import).

### Editor cursor jumping or deleting content
**Symptom**: When composing a reply, the cursor jumps to unexpected positions or previous thread content gets deleted
**Cause**: Known bug in Hey's rich text editor, particularly when editing quoted text in replies
**Solution**: 1) Compose in a separate text editor and paste into Hey. 2) Avoid editing within quoted reply blocks. 3) Use "Reply in a new window" if available. 4) Report to hey@37signals.com with browser/OS details.

### Screener filling up with legitimate senders
**Symptom**: Important emails stuck in The Screener because you haven't approved the sender yet
**Cause**: Every new sender must be manually approved. If you receive emails from many unique senders (e.g., sales, customer support), the Screener queue grows quickly.
**Solution**: 1) Check The Screener daily — make it part of your morning routine. 2) Approve entire domains (e.g., approve all @company.com senders at once if available). 3) If the Screener model doesn't fit your workflow (too many unique senders), Hey may not be ideal — consider Spark Mail's Gatekeeper or SaneBox's filtering which are less binary.
