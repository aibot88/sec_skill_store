---
name: sales-proton-mail
description: "Proton Mail platform help — privacy-first encrypted email with end-to-end encryption, zero-access architecture, Hide-my-Email aliases, Proton Mail Bridge for IMAP/SMTP, bundled Calendar/Drive/VPN/Pass (Free 1GB / Mail Plus ~$4/mo / Unlimited ~$10/mo, Swiss-based, 100M+ users). Use when setting up Proton Mail and migrating from Gmail or Outlook with Easy Switch, Proton Mail Bridge not connecting to Thunderbird or Apple Mail or Outlook, encrypted search not finding old emails you know exist, storage filling up on the free plan and wondering whether to upgrade, comparing Proton Mail to Tuta or Fastmail or Hey for privacy email, using Hide-my-Email aliases to reduce spam, wondering if Proton Mail works with third-party apps or automation tools, or evaluating Proton Mail for a small business with custom domains. Do NOT use for AI email drafting or inbox triage (use /sales-superhuman or /sales-shortwave). Do NOT use for team shared inbox with ticketing (use /sales-hiver or /sales-missive)."
argument-hint: "[describe what you need help with in Proton Mail]"
license: MIT
version: 1.0.0
tags: [sales, email-client, privacy, encryption, platform]
github: "https://github.com/ProtonMail"
---

# Proton Mail Platform Help

Helps with everything related to using Proton Mail — the privacy-first encrypted email service with end-to-end encryption, zero-access architecture, and bundled productivity suite (Calendar, Drive, VPN, Pass). Swiss-based, 100M+ users.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Proton Mail?**
   - A) Evaluating Proton Mail — is it right for me?
   - B) Migrating from Gmail/Outlook/another provider
   - C) Setting up Proton Mail Bridge for desktop clients
   - D) Comparing Proton Mail to alternatives (Tuta, Fastmail, Hey)
   - E) Managing storage, aliases, or custom domains
   - F) Troubleshooting search, Bridge, or sync issues
   - G) Evaluating Proton Mail for business/team use
   - H) Something else — describe it

2. **Which plan are you on (or considering)?**
   - A) Free (1 GB, 1 address, 150 msg/day limit)
   - B) Mail Plus (~$4/mo — 15 GB, 10 addresses, 1 custom domain)
   - C) Unlimited (~$10/mo — 500 GB, 15 addresses, 3 custom domains, VPN/Drive/Pass)
   - D) Business plan
   - E) Not sure yet

**If the user's request already provides most of this context, skip directly to the relevant step.**

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| AI email drafting or triage | `/sales-superhuman {question}` or `/sales-shortwave {question}` |
| Team shared inbox with ticketing | `/sales-helpdesk-selection {question}` |
| Inbox cleanup / unsubscribe | `/sales-clean-email {question}` |
| Server-side email filtering | `/sales-sanebox {question}` |
| Meeting scheduling | `/sales-meeting-scheduler {question}` |

When routing to another skill, provide the exact command.

If the question is about Proton Mail itself, continue to Step 3.

## Step 3 — Proton Mail platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, Bridge setup, migration, comparison context.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Evaluating Proton Mail**: Match their priorities. If they need AI, automation, or API access, Proton is not the right fit. If they want maximum privacy and encryption, it excels.
- **Migration**: Use Easy Switch for Gmail/Outlook. Warn about re-training contacts to use new address.
- **Bridge issues**: Check ports 1143/1025, firewall, antivirus. New Outlook is incompatible.
- **Storage**: Free tier fills fast. Upgrade to Mail Plus for 15 GB or use Drive for attachments.

If you discover a gotcha or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about pricing and plan features that may change.*

- **No public API.** No official REST API, no webhooks, no Zapier, no Make. Community libraries exist (Go, Python, Node.js) but are unofficial and may break. If you need automation, Proton is the wrong tool.
- **Search is limited by encryption.** End-to-end encryption means the server cannot index message bodies. Search works on metadata and locally cached content. Finding old emails is significantly harder than Gmail.
- **Bridge required for desktop clients.** IMAP/SMTP only works through Proton Mail Bridge (Mail Plus+ required). Bridge uses ports 1143/1025 and can conflict with firewalls. New Outlook is incompatible.
- **Free tier is very limited.** 1 GB storage, 1 address, 150 messages/day, no custom domains. Fills up fast with attachments.
- **No AI features.** Unlike Superhuman or Shortwave, Proton has no AI drafting, categorization, or smart inbox. Lumo AI is nascent.
- **Leaving is costly.** Your @proton.me/@protonmail.com address dies when you stop paying. Set up forwarding before canceling.
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Related skills

- `/sales-fastmail` — Fastmail independent email with full JMAP API, custom domains, Masked Email ($5/mo). Install:
  `npx skills add sales-skills/sales --skill sales-fastmail -a claude-code`
- `/sales-hey` — Hey privacy-first email service (Screener, Imbox/Feed/Paper Trail, no AI, $99/yr). Install:
  `npx skills add sales-skills/sales --skill sales-hey -a claude-code`
- `/sales-em-client` — eM Client desktop email client (PGP encryption, calendar/tasks, works with Proton Bridge). Install:
  `npx skills add sales-skills/sales --skill sales-em-client -a claude-code`
- `/sales-superhuman` — Superhuman email client (keyboard-driven speed, AI Write, MCP server, $25-40/mo). Install:
  `npx skills add sales-skills/sales --skill sales-superhuman -a claude-code`
- `/sales-shortwave` — Shortwave AI-native Gmail client (AI filters, Ghostwriter, MCP consumer). Install:
  `npx skills add sales-skills/sales --skill sales-shortwave -a claude-code`
- `/sales-spark-mail` — Spark Mail cross-platform AI email client (works with Proton via IMAP). Install:
  `npx skills add sales-skills/sales --skill sales-spark-mail -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (works with Proton Mail). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-clean-email` — Clean Email inbox cleanup (works with any IMAP provider including Proton). Install:
  `npx skills add sales-skills/sales --skill sales-clean-email -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Migrate from Gmail to Proton Mail
**User says**: "I want to move all my email from Gmail to Proton Mail. How do I do this?"
**Skill does**:
1. Reads platform guide for migration section
2. Explains Easy Switch: connects to Gmail via OAuth and imports emails, contacts, calendars
3. Notes: import is a one-time copy — new Gmail emails after import won't sync
4. Warns: recipients still have your old Gmail address. Set up Gmail forwarding to Proton during transition
5. Recommends Mail Plus ($4/mo) minimum for 15 GB storage — Free tier's 1 GB won't fit most Gmail exports
**Result**: Clear migration plan with storage warning

### Example 2: Bridge not connecting to Thunderbird
**User says**: "Proton Mail Bridge keeps timing out when I try to connect it to Thunderbird"
**Skill does**:
1. Reads platform guide Bridge troubleshooting section
2. Checks: is Bridge running? Are ports 1143 (IMAP) and 1025 (SMTP) free?
3. Suggests: increase Thunderbird timeout (Edit → Preferences → Config Editor → `mailnews.tcptimeout`)
4. Notes: firewalls and antivirus can block Bridge. Whitelist the Bridge process
5. If still failing: reset Bridge via Help → Clear cache, re-enter credentials
**Result**: Systematic troubleshooting for Bridge-Thunderbird connection

### Example 3: Should I use Proton or Fastmail?
**User says**: "I'm a solopreneur choosing between Proton Mail and Fastmail for my business email. I need a custom domain and I use Claude Code."
**Skill does**:
1. Compares: Proton offers E2E encryption, zero-access architecture; Fastmail offers JMAP API, speed, and IMAP without Bridge
2. Notes: Proton has no API — nothing to connect to Claude Code. Fastmail has a full JMAP API that could integrate
3. Compares pricing: Proton Mail Plus $4/mo vs Fastmail Standard ~$5/mo — similar for custom domain
4. Key difference: if automation and API access matter, Fastmail wins. If privacy is the top priority, Proton wins.
5. Notes both lack AI features — for AI email, consider Superhuman or Shortwave instead
**Result**: Decision framework based on API needs vs privacy priority

## Troubleshooting

### Search not finding emails
**Symptom**: You search for an email you know exists but Proton returns nothing
**Cause**: End-to-end encryption prevents server-side full-text search. Proton searches metadata (sender, subject, date) and locally cached message bodies. If the message isn't cached locally, body content won't match.
**Solution**: 1) Search by sender address or subject line instead of body text. 2) Use the web app (more content cached) rather than Bridge clients. 3) On paid plans, enable "Search message content" in Settings which builds a local encrypted index. 4) If migrated recently, wait for indexing to complete.

### Bridge connection errors
**Symptom**: Desktop email client shows "connection failed" or "login error" with Proton Mail Bridge
**Cause**: Port conflicts, firewall blocking, antivirus interference, or expired Bridge credentials.
**Solution**: 1) Verify Bridge is running and shows "Connected" status. 2) Check ports 1143/1025 are free (`lsof -i :1143`). 3) Whitelist Bridge in firewall and antivirus. 4) Re-enter the Bridge-generated password in your email client (not your Proton account password). 5) If using new Outlook for Windows, it's incompatible — use classic Outlook or Thunderbird.

### Storage full on free plan
**Symptom**: Can't receive new emails, "mailbox full" errors
**Cause**: Free plan only has 1 GB shared across Mail, Calendar, and Drive. Attachments fill this quickly.
**Solution**: 1) Delete large emails with attachments (sort by size in web app). 2) Empty trash and spam folders. 3) Upgrade to Mail Plus ($4/mo) for 15 GB. 4) Move attachments to Proton Drive on paid plans. 5) Use Hide-my-Email aliases to reduce spam volume.
