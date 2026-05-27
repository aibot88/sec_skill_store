---
name: sales-airmail
description: "Airmail platform help — Apple-exclusive email client with customizable swipe actions, multi-step Custom Actions, Smart Inbox, Send Later, snooze, AppleScript automation, Siri Shortcuts, Objective-C plugin framework, S/MIME and GPG encryption, Privacy Mode with local-only processing (Free 1 account / Pro ~$9/mo or ~$49/yr via App Store). Use when setting up Airmail across Mac iPhone iPad and Apple Watch, custom swipe actions or multi-step Custom Actions not working as expected, comparing Airmail to Spark Mail or Superhuman or Apple Mail, Airmail crashing or sync broken between Mac and iPhone, wondering if Airmail Pro subscription is worth upgrading from free, automating Airmail with AppleScript or Siri Shortcuts, or Airmail plugin development with the Objective-C framework. Do NOT use for cross-platform email clients on Windows or Android (use /sales-bluemail or /sales-em-client). Do NOT use for team shared inbox with ticketing (use /sales-hiver or /sales-missive)."
argument-hint: "[describe what you need help with in Airmail]"
license: MIT
version: 1.0.0
tags: [sales, email-client, productivity, platform]
github: "https://github.com/Airmail"
---

# Airmail Platform Help

Helps with Airmail — an Apple-exclusive email client for Mac, iPhone, iPad, Apple Watch, and Apple Vision Pro. Known for deep customization (swipe actions, Custom Actions, keyboard shortcuts), Smart Inbox filtering, Send Later scheduling, snooze, S/MIME/GPG encryption, and Privacy Mode (local processing, tracking pixel blocking). Supports Gmail, Exchange, Outlook, iCloud, IMAP, POP3. Apple Design Award winner. No public REST API — automation via AppleScript (Mac), Siri Shortcuts (iOS), URL schemes, and an Objective-C plugin framework.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Airmail?**
   - A) Set up Airmail and configure Smart Inbox / Custom Actions
   - B) Fix crashes, sync issues, or performance problems
   - C) Compare Airmail to other email clients
   - D) Automate Airmail with AppleScript, Siri Shortcuts, or plugins
   - E) Evaluate Airmail Pro vs free tier
   - F) Something else — describe it

2. **Which device(s)?**
   - A) Mac
   - B) iPhone / iPad
   - C) Apple Watch
   - D) Multiple Apple devices

3. **Which plan?**
   - A) Free — 1 account, basic features
   - B) Pro (~$9/mo or ~$49/yr) — multiple accounts, Send Later, Snooze, Custom Actions, push notifications
   - C) Not sure / evaluating

**Skip-ahead rule**: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Cross-platform email (need Windows/Android) | `/sales-bluemail {question}` or `/sales-em-client {question}` |
| Team shared inbox with ticketing | `/sales-hiver {question}` or `/sales-missive {question}` |
| Server-side email filtering without switching clients | `/sales-sanebox {question}` |
| AI-powered email triage/drafting | `/sales-superhuman {question}` or `/sales-fyxer {question}` |
| Connecting tools via Zapier/Make/API | Note: Airmail has no REST API or iPaaS integration |

For Airmail-specific questions, continue to Step 3.

## Step 3 — Airmail platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, customization options, automation surface (AppleScript, Siri Shortcuts, plugins), encryption setup, and integration details.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

- For **Custom Actions setup**: Create multi-step actions in Settings → Custom Actions. Chain operations: e.g., "Label as Client + Forward to assistant + Archive." Assign to swipe gestures for one-tap execution.
- For **sync issues**: Sign out and re-add the account. Ensure iCloud sync is enabled for settings. Check that push notifications are on (Pro only). Force close and reopen the app.
- For **AppleScript automation**: Use Airmail's AppleScript dictionary on Mac. Common actions: send email, move messages, search inbox. Combine with Automator or Shortcuts app for scheduled workflows.
- For **plugin development**: Clone the AirmailPlugIn-Framework from GitHub. Plugins are Objective-C bundles inheriting from AMPlugin. Copy built bundles to `~/Library/Containers/it.bloop.airmail/Data/Library/Application Support/Airmail/General/Plugins`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features and stability that may be outdated.*

- **Push notifications require Pro.** Free users who previously had push from the one-time purchase era lost it when Airmail switched to subscriptions. This is the most complained-about change.
- **Apple ecosystem only.** No Windows, no Android, no Linux. If you need cross-platform, use BlueMail, eM Client, or Spark Mail instead.
- **Stability issues persist.** Users report crashes (up to 20/day in severe cases), flag sync broken between Mac and iOS, and search returning wrong results. Updates sometimes break things.
- **Development pace is slow.** Users report few new features in years. Support response times are inconsistent.
- **Plugin framework is Objective-C only.** The AirmailPlugIn-Framework on GitHub is stale — last significant updates were years ago. Not viable for modern Swift development.
- **No REST API, no webhooks, no Zapier/Make.** Automation is limited to AppleScript (Mac), Siri Shortcuts (iOS), and URL schemes.
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Related skills

- `/sales-superhuman` — Superhuman email client (fastest keyboard workflow, MCP server, AI triage, $25-40/mo). Install:
  `npx skills add sales-skills/sales --skill sales-superhuman -a claude-code`
- `/sales-spark-mail` — Spark Mail cross-platform AI email client (Smart Inbox, Gatekeeper, team collaboration, Free/$5/$6.99). Install:
  `npx skills add sales-skills/sales --skill sales-spark-mail -a claude-code`
- `/sales-bluemail` — BlueMail cross-platform email client (free unified inbox, GemAI AI writing, clustering, Free/$5/$12). Install:
  `npx skills add sales-skills/sales --skill sales-bluemail -a claude-code`
- `/sales-em-client` — eM Client desktop email client (cross-platform, PGP encryption, calendar/tasks, Free/~€30yr/~€40). Install:
  `npx skills add sales-skills/sales --skill sales-em-client -a claude-code`
- `/sales-mimestream` — Mimestream native macOS Gmail client (Gmail API-powered, tracking prevention, no AI, $50/yr). Install:
  `npx skills add sales-skills/sales --skill sales-mimestream -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (smart folders, any provider, $7/mo). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-clean-email` — Clean Email inbox cleanup (bulk actions, Auto Clean, True Unsubscriber). Install:
  `npx skills add sales-skills/sales --skill sales-clean-email -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Setting up Custom Actions for a sales workflow
**User says**: "I want a one-swipe action in Airmail that labels an email as 'Lead', forwards it to my CRM intake address, and archives the original."
**Skill does**: Reads platform guide. Walks through: 1) Go to Settings → Custom Actions → Add Action. 2) Chain three steps: Apply Label "Lead" → Forward to crm-intake@company.com → Archive. 3) Assign to a swipe gesture (e.g., long swipe left). 4) Test with a dummy email. Notes this requires Pro for custom actions. Warns that forwards are plain — no API webhook, so CRM must accept email intake.

### Example 2: Automating Airmail with AppleScript on Mac
**User says**: "How do I use AppleScript to send a daily summary email from Airmail?"
**Skill does**: Reads platform guide automation section. Explains: 1) Open Script Editor, use Airmail's AppleScript dictionary (`tell application "Airmail 5"`). 2) Construct the message with `make new outgoing message`. 3) Set recipient, subject, body. 4) Use `send` command. 5) Schedule via macOS Shortcuts app or launchd plist for daily execution. Notes AppleScript is Mac-only and requires Airmail to be running.

### Example 3: Comparing Airmail to Spark Mail
**User says**: "I'm on Mac and iPhone. Should I use Airmail or Spark Mail? Both seem similar."
**Skill does**: Reads platform guide. Compares: Both support Mac/iOS with Smart Inbox. Airmail is Apple-exclusive with deeper customization (Custom Actions, AppleScript, plugins) and Privacy Mode (local processing). Spark is cross-platform (adds Windows/Android), has team collaboration (shared drafts, comments), and AI writing features. Airmail Pro costs ~$49/yr; Spark Premium is ~$60/yr. Key tradeoff: Airmail for privacy and customization power users; Spark for cross-platform and team features. Notes Airmail's stability has been criticized more than Spark's.

## Troubleshooting

### Airmail crashes frequently or freezes
**Symptom**: App crashes multiple times a day, freezes when opening emails, or becomes unresponsive after switching accounts
**Cause**: Known stability issues — especially with multiple accounts, large mailboxes, or after updates. VPN and firewall software can also trigger crashes.
**Solution**: 1) Update to the latest version from the App Store. 2) Remove and re-add email accounts one at a time to isolate the problem account. 3) Disable VPN temporarily to test. 4) On Mac, delete Airmail's cache: quit the app, delete `~/Library/Containers/it.bloop.airmail/Data/Library/Caches`. 5) Try Safe Mode (hold Shift while launching on Mac) to diagnose plugin conflicts.

### Flag/read sync broken between Mac and iPhone
**Symptom**: Flags set on Mac don't appear on iPhone, or read status doesn't sync across devices
**Cause**: iCloud sync for Airmail settings can desync. IMAP flag sync depends on the mail server handling flags correctly.
**Solution**: 1) Ensure iCloud sync is enabled in Airmail settings on both devices. 2) Force sync by pulling down on inbox (iOS) or refreshing (Mac). 3) Check that both devices use the same Airmail account (not separate local configs). 4) For IMAP accounts, verify the server supports IMAP flags — some budget hosts don't. 5) Sign out of Airmail on all devices, wait 5 minutes, sign back in.

### Lost features after subscription switch
**Symptom**: Push notifications, custom actions, or multi-account support stopped working after Airmail switched from one-time purchase to subscription
**Cause**: Airmail moved to a subscription model — features previously included in the one-time purchase now require Pro subscription.
**Solution**: 1) Check if you're on the free tier (Settings → Subscription). 2) If you previously purchased Airmail, the subscription is the only way to restore Pro features — the one-time purchase is no longer honored for new features. 3) Evaluate if Pro (~$49/yr) is worth it vs switching to Spark Mail (free tier is more generous) or Apple Mail (free, built-in).
