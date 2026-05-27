---
name: sales-spark-mail
description: "Spark Mail platform help — cross-platform AI email client by Readdle with Smart Inbox categorization, Gatekeeper sender screening, AI writing and summarization, email translation, team collaboration (shared drafts, internal comments, delegation), calendar integration, works with Gmail/Outlook/iCloud/Exchange/Yahoo/IMAP on Mac/Windows/iOS/Android (Free, Premium $5/mo, Teams $6.99/user/mo). Use when setting up Spark Mail Smart Inbox or Gatekeeper for email triage, Spark AI writing or summarization not working well, Spark sync issues or crashes across devices, comparing Spark to Superhuman or Shortwave or Apple Mail, choosing between Spark free vs Premium vs Teams plans, or worried about Spark Mail privacy and server-side processing. Do NOT use for comparing AI email assistants broadly (use /sales-do). Do NOT use for team shared inbox with ticketing (use /sales-missive or /sales-hiver)."
argument-hint: "[describe what you need help with in Spark Mail]"
license: MIT
version: 1.0.0
tags: [sales, email-client, ai-email, productivity, platform]
---

# Spark Mail Platform Help

Helps with Spark Mail — a cross-platform AI email client by Readdle (est. 2007). Smart Inbox auto-categorizes email, Gatekeeper screens unwanted senders, and AI features handle writing, summarization, and translation. Team features include shared drafts, internal comments, and email delegation. Works with Gmail, Outlook, iCloud, Exchange, Yahoo, and any IMAP provider across Mac, Windows, iOS, Android, and Apple Watch. 19.5M+ downloads, Apple Editors' Choice.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Spark Mail?**
   - A) Set up Spark Mail and configure Smart Inbox / Gatekeeper
   - B) Fix sync, performance, or crash issues
   - C) Use AI features (writing, summarization, translation)
   - D) Set up team collaboration (shared drafts, comments, delegation)
   - E) Compare Spark to other email clients
   - F) Something else — describe it

2. **Which platform(s)?**
   - A) Mac / iPhone / iPad
   - B) Windows / Android
   - C) Cross-platform (multiple devices)

3. **Which plan are you on (or considering)?**
   - A) Free — core features, Smart Inbox, Gatekeeper
   - B) Premium Individual ($59.99/yr / ~$5/mo) — AI features, advanced customization
   - C) Premium Teams ($6.99/user/mo) — collaboration, shared drafts, delegation
   - D) Not sure / evaluating

**Skip-ahead rule**: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Comparing AI email clients broadly | `/sales-do {question}` |
| Team shared inbox with ticketing/SLAs | `/sales-missive {question}` or `/sales-hiver {question}` |
| Server-side email filtering without switching clients | `/sales-sanebox {question}` |
| Connecting tools via Zapier/Make/API | Note: Spark Mail has no public API or iPaaS integration |

For Spark-specific questions, continue to Step 3.

## Step 3 — Spark Mail platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, Smart Inbox setup, AI features, team collaboration, and privacy details.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

- For **Smart Inbox setup**: Enable it in Settings → Smart Inbox. It auto-sorts into Personal, Notifications, and Newsletters. Pin important contacts so their emails always surface first. Use Gatekeeper to block or screen unknown senders.
- For **sync issues**: Force-sync by pulling down on inbox. Check that background app refresh is enabled on mobile. If persistent, sign out and re-add the account. Spark 3 introduced some stability regressions — ensure you're on the latest version.
- For **AI features**: AI writing and summarization require Premium. They work best for short emails — for complex replies, use AI as a starting draft and edit. AI is less sophisticated than Superhuman or Shortwave's offerings.
- For **plan selection**: Free is genuinely useful (Smart Inbox + Gatekeeper alone are worth it). Premium ($5/mo) for AI writing/summarization. Teams ($6.99/user/mo) only if you need shared drafts and delegation.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features and privacy that may be outdated.*

- **Server-side processing.** Spark stores your email credentials on Readdle's servers to power features like Smart Inbox and push notifications. This is a privacy tradeoff — your emails pass through their servers. They claim GDPR/CCPA compliance and no data selling, but security-conscious users should be aware.
- **AI is lighter than competitors.** Spark's AI writing and summarization are functional but less contextually deep than Superhuman or Shortwave. Think of it as enhanced Smart Compose, not a full AI assistant.
- **No public API.** No REST API, webhooks, Zapier, Make, or any programmatic interface. Cannot be automated.
- **Spark 3 stability.** The Spark 3 rewrite introduced performance regressions — slowness, crashes, and sync inconsistencies. Most issues have been fixed in updates, but some users still report problems.
- **Free tier is generous.** Unlike Superhuman ($30/mo) or Shortwave ($7+/mo), Spark's core features (Smart Inbox, Gatekeeper, multi-account) are free forever.
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Related skills

- `/sales-superhuman` — Superhuman email client (fastest keyboard workflow, MCP server, AI triage, $30/mo). Install:
  `npx skills add sales-skills/sales --skill sales-superhuman -a claude-code`
- `/sales-shortwave` — Shortwave AI-native Gmail client (AI filters, Ghostwriter, MCP consumer, $7-14/mo). Install:
  `npx skills add sales-skills/sales --skill sales-shortwave -a claude-code`
- `/sales-newmail` — NewMail AI email assistant (voice-trained drafting, task extraction, daily briefings, $15-30/mo). Install:
  `npx skills add sales-skills/sales --skill sales-newmail -a claude-code`
- `/sales-fyxer` — Fyxer AI email assistant (inbox organization, AI drafting, meeting notes). Install:
  `npx skills add sales-skills/sales --skill sales-fyxer -a claude-code`
- `/sales-missive` — Missive collaborative team inbox (internal threads, co-drafting, API). Install:
  `npx skills add sales-skills/sales --skill sales-missive -a claude-code`
- `/sales-hey` — Hey privacy-first email service by 37signals (Screener, Imbox/Feed/Paper Trail, no AI, $99/yr). Install:
  `npx skills add sales-skills/sales --skill sales-hey -a claude-code`
- `/sales-mimestream` — Mimestream native macOS Gmail client (Gmail API-powered, tracking prevention, no AI, $50/yr). Install:
  `npx skills add sales-skills/sales --skill sales-mimestream -a claude-code`
- `/sales-bluemail` — BlueMail cross-platform email client (free unified inbox, GemAI AI writing, clustering, Later Board, Free/$5/$12/Enterprise). Install:
  `npx skills add sales-skills/sales --skill sales-bluemail -a claude-code`
- `/sales-em-client` — eM Client desktop email client (cross-platform, PGP encryption, calendar/tasks, Free/€30yr/€40 one-time). Install:
  `npx skills add sales-skills/sales --skill sales-em-client -a claude-code`
- `/sales-airmail` — Airmail Apple-exclusive email client (customizable actions, AppleScript automation, Privacy Mode, Free/$49yr). Install:
  `npx skills add sales-skills/sales --skill sales-airmail -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (smart folders, any provider, $7/mo). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Configuring Smart Inbox for a busy founder
**User says**: "I get 200+ emails a day and most are newsletters and notifications. How do I set up Spark to surface only the important stuff?"
**Skill does**: Reads platform guide. Walks through: 1) Enable Smart Inbox to auto-sort into Personal/Notifications/Newsletters. 2) Pin your top 10 contacts so they always appear first. 3) Enable Gatekeeper to screen unknown senders. 4) Use "Mute Thread" for recurring threads you want auto-archived. 5) Set Smart Notifications to only alert for pinned contacts. Notes this all works on the free plan.

### Example 2: Evaluating Spark vs Superhuman for a sales team
**User says**: "We're a 5-person sales team on Gmail. Spark Teams at $7/user sounds way cheaper than Superhuman at $30/user. What are we giving up?"
**Skill does**: Reads platform guide for feature comparison. Explains: Spark Teams gives you shared drafts, internal comments, and delegation at $6.99/user/mo. You lose Superhuman's sub-100ms speed, keyboard-driven workflow, Split Inbox, read receipts, and deeper AI (auto-triage, AI-generated follow-up suggestions). If your team prioritizes cost and doesn't need power-user keyboard shortcuts, Spark is excellent value. If speed and individual productivity are paramount, Superhuman justifies the premium. Recommends trying Spark's free tier first.

### Example 3: Privacy concerns about server-side processing
**User says**: "I heard Spark stores my email password on their servers. Is that true? Should I be worried?"
**Skill does**: Reads platform guide privacy section. Explains that yes, Spark stores credentials server-side to power Smart Inbox, push notifications, and cross-device sync. Notes they use Google Cloud with encryption, are GDPR/CCPA compliant, don't sell data, and don't train AI models on your emails. Compares: Apple Mail is fully local, Superhuman also processes server-side, SaneBox also processes server-side. If privacy is the top priority, recommends Canary Mail (end-to-end encryption) or Apple Mail (fully local processing).

## Troubleshooting

### Spark is slow or crashes frequently
**Symptom**: App freezes when opening, searching takes seconds, or the app crashes mid-use — especially on Mac or iOS
**Cause**: Spark 3 (major rewrite) introduced performance regressions. Large mailboxes with 10K+ emails strain the sync engine.
**Solution**: 1) Update to the latest version — most stability issues have been patched. 2) Remove and re-add email accounts to force a fresh sync. 3) On Mac, quit and reopen Spark if it freezes. 4) Reduce the number of connected accounts if running 5+. 5) If persistent, report via Spark's in-app feedback — Readdle actively patches issues.

### Emails not syncing across devices
**Symptom**: Read/archive/delete actions on one device don't appear on another, or new emails arrive on one device but not another
**Cause**: Background app refresh may be disabled, or the server-side sync hit a conflict.
**Solution**: 1) Pull down on inbox to force-sync. 2) Ensure background app refresh is enabled (iOS: Settings → Spark → Background App Refresh). 3) Check that all devices are signed into the same Spark account. 4) Sign out and re-add the email account if sync remains broken.

### Smart Inbox not categorizing correctly
**Symptom**: Important emails end up in Newsletters/Notifications, or spam-like emails appear in Personal
**Cause**: Smart Inbox uses Readdle's ML categorization which isn't perfect. New contacts may be miscategorized until the system learns.
**Solution**: 1) Pin important contacts — pinned senders always appear in Priority. 2) Move miscategorized emails to the correct category — this trains the system. 3) Use Gatekeeper to block persistent junk senders. 4) Check that the sender isn't using a generic domain that confuses categorization.
