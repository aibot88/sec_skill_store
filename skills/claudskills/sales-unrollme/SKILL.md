---
name: sales-unrollme
description: "Unroll.me platform help — free newsletter unsubscribe and daily digest tool that consolidates subscriptions into one Rollup email, supports Gmail/Outlook/Yahoo/AOL/iCloud, owned by NielsenIQ. Use when overwhelmed by newsletter and promotional email subscriptions, want to unsubscribe from dozens of mailing lists at once, Rollup digest not arriving or missing newsletters, comparing Unroll.me to Clean Email or SaneBox or Mailstrom for inbox cleanup, worried about Unroll.me privacy and whether it sells your email data, trying to use Unroll.me in Europe or the EU, or deciding if Unroll.me is safe to use given the FTC settlement. Do NOT use for AI email reply drafting or inbox triage (use /sales-fyxer or /sales-superhuman). Do NOT use for bulk cleanup of thousands of old emails (use /sales-clean-email)."
argument-hint: "[describe what you need help with in Unroll.me]"
license: MIT
version: 1.0.0
tags: [sales, email-management, inbox-cleanup, unsubscribe, platform]
github: "https://github.com/Unroll-Me"
---

# Unroll.me Platform Help

Helps with Unroll.me — a free newsletter unsubscribe and digest tool. Scans your inbox for subscriptions, lets you unsubscribe in one click or consolidate newsletters into a daily Rollup digest. Free because NielsenIQ monetizes anonymized purchase data from your emails.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What are you trying to do with Unroll.me?**
   - A) Unsubscribe from a bunch of newsletters
   - B) Set up or fix the Rollup daily digest
   - C) Evaluate whether Unroll.me is safe to use (privacy concerns)
   - D) Compare Unroll.me to alternatives
   - E) Something else — describe it

2. **Which email provider(s)?**
   - A) Gmail
   - B) Outlook / Microsoft 365
   - C) Yahoo / AOL
   - D) Apple iCloud
   - E) Multiple

**If the user's request already provides most of this context, skip directly to the relevant step.**

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Bulk cleanup of thousands of old emails | `/sales-clean-email {question}` |
| Automated inbox rules and ongoing email management | `/sales-clean-email {question}` |
| AI-powered email filtering with smart folders | `/sales-sanebox {question}` |
| AI email reply drafting in your voice | `/sales-fyxer {question}` or `/sales-superhuman {question}` |
| Open-source email assistant with API/CLI | `/sales-inbox-zero {question}` |
| Action item extraction from emails | `/sales-unboxd {question}` |
| Meeting note-taking or call recording | `/sales-note-taker {question}` |

For Unroll.me-specific questions, continue to Step 3.

## Step 3 — Unroll.me platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, privacy details, Rollup configuration, comparison data, and migration paths.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

- For **mass unsubscribe**: Connect your account, review the subscription list, tap Unsubscribe on each unwanted sender. Check back in 7 days — some senders have grace periods.
- For **Rollup issues**: Verify newsletters are set to "Add to Rollup" (not "Unsubscribe" or "Keep"). Check spam/junk folder for the Rollup email. Delivery time is set in Rollup settings.
- For **privacy evaluation**: Be direct — Unroll.me scans full email content and sells anonymized purchase data to NielsenIQ. If that's unacceptable, recommend Clean Email ($29.99/yr, headers only) or Leave Me Alone (pay-per-use, no data selling).
- For **EU users**: Unroll.me is not available in the EU since 2018. Recommend Clean Email, SaneBox, or Leave Me Alone as alternatives.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about privacy practices and availability that may change.*

- **Your email content funds the product.** Unroll.me scans full email bodies (not just headers) and NielsenIQ sells anonymized purchase/transaction data. This is not hidden — it's the business model.
- **FTC settlement (2019).** The FTC found Unroll.me's original privacy disclosures deceptive. Transparency improved post-settlement but the data practices continue.
- **Not available in the EU.** Unroll.me deleted all EU user accounts in 2018 because it couldn't comply with GDPR. EU users should use Clean Email, SaneBox, or Leave Me Alone.
- **No API, no webhooks, no Zapier/Make.** Unroll.me is a closed consumer tool with zero developer integration surface.
- **Limited to unsubscribe + digest.** Cannot bulk delete, archive, or sort old emails. Cannot block senders who ignore unsubscribe requests. For bulk cleanup, use Clean Email.
- **No opt-out from data scanning.** You cannot use the free service while opting out of inbox scanning. You can opt out of the "Measurement Panel" but baseline scanning continues.
- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Related skills

- `/sales-clean-email` — Clean Email inbox cleanup (bulk actions, Auto Clean rules, True Unsubscriber, headers-only privacy, $29.99/yr). Install:
  `npx skills add sales-skills/sales --skill sales-clean-email -a claude-code`
- `/sales-sanebox` — SaneBox server-side email filtering (smart folders, any email provider, metadata-only, $7-36/mo). Install:
  `npx skills add sales-skills/sales --skill sales-sanebox -a claude-code`
- `/sales-inbox-zero` — Inbox Zero open-source AI email assistant (auto-labeling, rules API/CLI, self-hostable, $18/mo or free). Install:
  `npx skills add sales-skills/sales --skill sales-inbox-zero -a claude-code`
- `/sales-fyxer` — Fyxer AI email assistant (inbox organization, AI drafting, meeting notes). Install:
  `npx skills add sales-skills/sales --skill sales-fyxer -a claude-code`
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install:
  `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Mass newsletter unsubscribe
**User says**: "I get 50+ newsletters a day and want to nuke most of them. Can Unroll.me help?"
**Skill does**:
1. Reads platform guide for unsubscribe workflow
2. Explains Unroll.me scans inbox and lists all detected subscriptions
3. User taps Unsubscribe on each unwanted sender — Unroll.me sends the cancellation request
4. Warns about 48h-7d grace period for some senders
5. Mentions the privacy tradeoff: Unroll.me is free but scans full email content for NielsenIQ
6. If privacy is a concern, suggests Clean Email ($29.99/yr) as a privacy-respecting alternative
**Result**: Clear unsubscribe workflow with honest privacy disclosure

### Example 2: Privacy evaluation (developer question)
**User says**: "Is Unroll.me safe to use? I heard they sell your data. What exactly do they access?"
**Skill does**:
1. Reads platform guide privacy section
2. Explains: Unroll.me scans full email content (bodies, not just headers), extracts purchase receipts and transaction data, sells anonymized market research to NielsenIQ clients
3. Cites the 2017 NYT expose (sold Lyft receipts to Uber) and 2019 FTC settlement
4. Notes EU accounts were deleted in 2018 due to GDPR non-compliance
5. Compares privacy approaches: Clean Email (headers only), SaneBox (metadata only), InboxPurge (client-side, nothing leaves browser)
**Result**: Honest, detailed privacy assessment with safer alternatives

### Example 3: Rollup digest not working
**User says**: "My Rollup email stopped arriving. I set it up weeks ago and it was working fine."
**Skill does**:
1. Reads platform guide for Rollup troubleshooting
2. Checks: Is the Rollup email going to spam/junk? Check those folders.
3. Verifies newsletters are still set to "Add to Rollup" in Unroll.me dashboard
4. Suggests disconnecting and reconnecting the email account
5. Notes: if the email provider changed OAuth permissions or app passwords, Unroll.me may have lost access
**Result**: Systematic diagnosis of Rollup delivery failure

## Troubleshooting

### Unsubscribe not working for specific senders
**Symptom**: Used Unroll.me to unsubscribe but emails keep arriving from the same sender
**Cause**: Many mailing lists have a 48-hour to 7-day grace period. Some senders ignore unsubscribe requests entirely. Some use multiple sending addresses.
**Solution**: Wait 7 days. If emails persist, the sender is non-compliant — Unroll.me cannot force compliance. Unlike Clean Email, Unroll.me has no Block/filter fallback. Workaround: create a filter in your email client (Gmail filters, Outlook rules) to auto-delete from that sender. For a tool with built-in blocking, switch to Clean Email.

### Rollup digest email not arriving
**Symptom**: Set up Rollup but never receive the daily digest email, or it stopped arriving
**Cause**: Rollup email may be landing in spam/junk. Email provider may have revoked Unroll.me's access. No newsletters are currently set to "Add to Rollup."
**Solution**: Check spam/junk folders. Verify at least one subscription is set to Rollup in the dashboard. Try disconnecting and reconnecting your email account. Check that Unroll.me still has OAuth access in your email provider's connected apps settings.

### Cannot sign up or connect email (EU user)
**Symptom**: Trying to create an Unroll.me account or connect an email but getting blocked or redirected
**Cause**: Unroll.me is unavailable in the EU since May 2018 — all EU accounts were deleted because the service cannot comply with GDPR.
**Solution**: Unroll.me will not work for EU-based users. Use Clean Email (GDPR-compliant, works globally, $29.99/yr), SaneBox (any provider, $7/mo), or Leave Me Alone (privacy-focused, pay-per-use) instead.
