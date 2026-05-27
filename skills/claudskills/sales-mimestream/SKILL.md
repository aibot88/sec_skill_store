---
name: sales-mimestream
description: "Mimestream platform help — native macOS email client built exclusively for Gmail using the Gmail API, with tracking prevention, email templates, Markdown compose, multi-account unified inbox, snooze, and deep macOS integration ($50/yr, no free tier). Use when setting up Mimestream for multiple Gmail accounts, Mimestream not showing labels or categories correctly, wondering if Mimestream is worth it over Gmail web or Apple Mail, comparing Mimestream to Superhuman or Airmail or Spark Mail for Mac, Mimestream notifications not working or delayed, Mimestream templates or Markdown formatting issues, frustrated by no Mimestream iOS app and stuck on Gmail mobile, or evaluating Mimestream privacy and tracking prevention. Do NOT use for AI email triage or AI-drafted replies (Mimestream has no AI features — use /sales-superhuman or /sales-fyxer). Do NOT use for team shared inbox or collaboration (use /sales-missive or /sales-hiver)."
argument-hint: "[describe what you need help with in Mimestream]"
license: MIT
version: 1.0.0
tags: [sales, email-client, productivity, platform]
---

# Mimestream Platform Help

Helps with Mimestream — a native macOS email client built exclusively for Gmail by a former Apple Mail engineer (7+ years at Apple). Uses the Gmail API directly (not IMAP), providing native label support, Gmail search, categories, aliases, and tracking prevention. Mac-only, Gmail-only, no AI features, no public API.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Mimestream?**
   - A) Set up Mimestream or configure accounts
   - B) Fix labels, categories, or search issues
   - C) Configure notifications, snooze, or templates
   - D) Compare Mimestream to other Mac email clients
   - E) Evaluate privacy / tracking prevention features
   - F) Something else — describe it

2. **How many Gmail accounts?**
   - A) One personal Gmail
   - B) One Google Workspace
   - C) Multiple (personal + work)

3. **What are you currently using?**
   - A) Gmail web
   - B) Apple Mail
   - C) Another email client (name it)
   - D) New to desktop email clients

**Skip-ahead rule**: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| AI email triage, auto-drafts, or AI writing | "Mimestream has no AI features — run: `/sales-superhuman {question}` or `/sales-fyxer {question}`" |
| Team shared inbox or collaboration | "Run: `/sales-missive {question}` or `/sales-hiver {question}`" |
| Server-side email filtering without switching clients | "Run: `/sales-sanebox {question}`" |
| Inbox cleanup or mass unsubscribe | "Run: `/sales-clean-email {question}`" |
| Meeting scheduling | "Run: `/sales-meeting-scheduler {question}`" |

For Mimestream-specific questions, continue to Step 3.

## Step 3 — Mimestream platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, Gmail API details, privacy model, keyboard shortcuts, and multi-account setup.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

- **For multi-account setup**: Add accounts via Settings. Each gets its own color, notification schedule, and signature. Use Unified Inbox to see all accounts together, or switch between individual inboxes.
- **For label/category issues**: Mimestream mirrors Gmail labels and categories via the API. If something is wrong in Mimestream, check Gmail web first — the issue may be server-side. Server-side Gmail filters can be managed directly from Mimestream.
- **For notification delays**: Try switching between Private Push (Cloud Pub/Sub, slight delay) and IMAP IDLE (direct, more immediate but uses more battery). Private Push doesn't share credentials with Mimestream servers.
- **For "is it worth it" questions**: The value proposition is speed + native macOS feel + tracking prevention + no intermediary servers. If you primarily use keyboard shortcuts, labels, and Gmail search, Mimestream surfaces these better than Apple Mail or Gmail web. If you need AI, cross-platform, or Outlook — look elsewhere.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about feature limitations that may change with updates.*

- **Gmail-only.** Mimestream only works with Gmail and Google Workspace. No Outlook, iCloud, Yahoo, or IMAP support. Microsoft 365 and IMAP are on the roadmap but no ETA.
- **Mac-only — no iOS app.** There is no iPhone or iPad app. iOS app is in development (TestFlight beta expected). This means you need a separate email app for mobile.
- **No AI features at all.** No AI triage, no AI writing, no AI summarization. If you want AI, use Superhuman ($30/mo), Shortwave ($7+/mo), or pair Mimestream with SaneBox ($7/mo) for server-side filtering.
- **No public API or automation.** No REST API, no webhooks, no Zapier, no Make, no MCP server. Cannot be programmatically controlled beyond macOS Accessibility API.
- **No free tier.** 14-day trial only. After that, $4.99/mo or $49.99/yr. Not available on the Mac App Store.
- **Subscription only.** No lifetime or one-time purchase option. Recurring payment required.
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Related skills

- `/sales-superhuman` — Superhuman fastest AI email client (keyboard workflow, Split Inbox, MCP server, $25-40/mo). Install:
  `npx skills add sales-skills/sales --skill sales-superhuman -a claude-code`
- `/sales-airmail` — Airmail Apple-exclusive email client (customizable actions, AppleScript automation, Free/$49yr). Install:
  `npx skills add sales-skills/sales --skill sales-airmail -a claude-code`
- `/sales-spark-mail` — Spark Mail cross-platform AI email client (Smart Inbox, Gatekeeper, Free/$5/$7/mo). Install:
  `npx skills add sales-skills/sales --skill sales-spark-mail -a claude-code`
- `/sales-bluemail` — BlueMail cross-platform email client (free unified inbox, GemAI, clustering, Free/$5/$12/mo). Install:
  `npx skills add sales-skills/sales --skill sales-bluemail -a claude-code`
- `/sales-em-client` — eM Client desktop email client (cross-platform, PGP encryption, calendar/tasks, Free/~€30yr). Install:
  `npx skills add sales-skills/sales --skill sales-em-client -a claude-code`
- `/sales-shortwave` — Shortwave AI-native Gmail client (AI filters, Ghostwriter, MCP consumer, $24-100/mo). Install:
  `npx skills add sales-skills/sales --skill sales-shortwave -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (smart folders, any provider, $7/mo). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Is Mimestream worth it over Gmail web?
**User says**: "I spend all day in Gmail on my Mac. Is Mimestream worth $50/year?"
**Skill does**:
1. Reads platform guide for feature comparison
2. Explains value: native macOS speed, keyboard shortcuts, multi-account unified inbox, tracking prevention, offline access, system notifications, dark mode reformatting
3. Notes what Gmail web does better: free, cross-device, extensions ecosystem, AI features (Gemini)
4. Notes Mimestream has no AI, no mobile app, no free tier
5. Recommends trying the 14-day trial to see if the speed difference justifies the cost
**Result**: Clear cost-benefit analysis for daily Gmail users

### Example 2: Comparing Mimestream to Superhuman for a Mac user
**User says**: "Should I get Mimestream or Superhuman for my Mac? I use Gmail."
**Skill does**:
1. Reads platform guide for comparison context
2. Compares: Mimestream $50/yr vs Superhuman $300+/yr — 6x price difference
3. Mimestream: native macOS app, faster native feel, tracking prevention, no AI
4. Superhuman: AI Write, Split Inbox, read receipts, MCP server for Claude Code, cross-platform (iOS, Android)
5. Recommends Mimestream if you want pure speed + privacy at low cost; Superhuman if AI features and mobile access justify the premium
**Result**: Clear positioning on the price-to-feature spectrum

### Example 3: Setting up multiple Gmail accounts with unified inbox
**User says**: "I have 3 Gmail accounts — personal, work Google Workspace, and a side project. How do I set them all up in Mimestream?"
**Skill does**:
1. Reads platform guide for multi-account setup
2. Walks through adding each account via OAuth (Settings → Accounts → Add Account)
3. Explains per-account customization: colors, notification schedules, signatures, aliases
4. Shows how to use Unified Inbox for all-in-one view vs switching between accounts
5. Notes Focus Filters can temporarily suppress non-work accounts during work hours
**Result**: Multi-account configured with per-account customization

## Troubleshooting

### Mimestream not showing Gmail categories or labels
**Symptom**: Inbox categories (Primary, Social, Promotions, Updates) or custom labels not appearing in Mimestream
**Cause**: Gmail categories must be enabled in Gmail settings (not Mimestream). Custom labels sync automatically but nested labels may need parent label visibility toggled.
**Solution**: 1) In Gmail web, go to Settings → Inbox → set Inbox type to "Default" and enable categories. 2) In Mimestream, check sidebar label visibility settings. 3) Force sync by quitting and reopening Mimestream. 4) For nested labels, ensure parent label is set to "Show" in Mimestream's label settings.

### Notifications delayed or not appearing
**Symptom**: New emails arrive in Mimestream but system notifications are late or missing
**Cause**: Mimestream offers two push methods — IMAP IDLE (direct, more immediate) and Private Push (Cloud Pub/Sub, slight delay). macOS notification settings may also block alerts.
**Solution**: 1) In Mimestream Settings → Notifications, check which method is active. Try switching between IMAP IDLE and Private Push. 2) Check macOS System Settings → Notifications → Mimestream — ensure "Allow Notifications" is on and alert style is set to Banners or Alerts. 3) Per-account notification schedules may be muting alerts outside work hours — check Settings → Accounts → Notification Schedule. 4) Focus Mode on macOS may be filtering Mimestream notifications.

### Mimestream feels slow or uses high CPU
**Symptom**: Mimestream becomes sluggish, beach balls, or uses significant CPU — especially with multiple accounts
**Cause**: Initial sync of large Gmail mailboxes downloads message metadata to local SQLite database. Multiple large accounts compound this.
**Solution**: 1) Wait for initial sync to complete — this is a one-time process that can take hours for large mailboxes (50K+ messages). 2) After sync, performance should improve dramatically. 3) If persistent, check Activity Monitor for runaway processes. 4) Try removing and re-adding the problematic account. 5) Ensure macOS and Mimestream are both updated to latest versions.
