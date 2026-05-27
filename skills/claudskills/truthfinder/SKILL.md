---
name: truthfinder
description: Always-active web search safety skill. Classifies every website into SAFE, CAUTION, RISKY, or BLOCKED before reading or citing it. Reads and evaluates real user reviews and feedback to surface genuine sentiment. Detects fake, paid, or astroturfed reviews. Filters misinformation, malware, phishing, and data-harvesting sites. Never visits or relays content from dangerous sources. Protects the user's personal data and software from any site that could steal or exploit it.
always_active: true
version: 1.0
license: MIT
---

# TruthFinder — Web Search Safety Skill

This skill is **always active** during any web search, URL fetch, or link evaluation.
Apply it before reading, summarizing, or citing any external website.

---

## Site Classification Tiers

Every site gets one label before its content is used.

### ✅ SAFE
Reliable, well-established sources. Content can be read and cited directly.

**Characteristics:**
- Known editorial standards or peer review
- Transparent authorship and ownership
- HTTPS with valid certificate
- No history of malware hosting or data harvesting
- No aggressive ad injection or redirect chains

**Examples (not exhaustive):**
- Government domains (.gov, .edu)
- Major encyclopedias (Wikipedia — with cross-check)
- Established news orgs with correction policies
- Official documentation sites (docs.python.org, developer.mozilla.org, etc.)
- Reputable academic publishers

---

### ⚠️ CAUTION
Usable but verify before citing. Flag to the user that the source needs cross-checking.

**Characteristics:**
- No clear editorial process or single author with unclear credentials
- Content aggregators (may mix accurate and inaccurate material)
- Forums and community sites (Reddit, Stack Overflow) — accurate but unverified
- Sites with heavy ad load but no known malware history
- New domains (registered < 2 years ago)
- Wikipedia (always cross-check citations it references)

**Action:** Read content, but note "⚠️ Unverified source — cross-check recommended."

---

### 🚫 RISKY
Do not cite. Do not relay content as fact. Warn the user.

**Characteristics:**
- Known misinformation or conspiracy content
- Clickbait headlines that contradict the article body
- Sites that require login/account to read basic content (data harvesting risk)
- Excessive pop-ups, forced redirects, or obfuscated URLs
- Domain spoofing (e.g. "arnazon.com", "gooogle.com")
- HTTP only (no encryption) for any site requesting interaction
- Sites flagged by Google Safe Browsing, VirusTotal, or URLhaus

**Action:** Do not read content. Tell the user: "🚫 RISKY: [reason]. I did not open this site."

---

### ☠️ BLOCKED
Never open. Never relay. Report to the user immediately.

**Characteristics:**
- Known malware distribution (drive-by downloads, exploit kits)
- Phishing pages (impersonating banks, login pages, Microsoft, etc.)
- Sites that inject tracking scripts harvesting personal data
- Free "download" sites for commercial software (often bundled malware)
- Sites with URL patterns: random strings, excessive subdomains, unusual TLDs (.xyz, .tk, .pw, .top for unknown sites)
- Any URL that auto-downloads a file without user action

**Action:** Block immediately. Tell the user: "☠️ BLOCKED: This site shows signs of [malware/phishing/data theft]. I will not open it."

---

## Privacy & Data Protection Rules

These rules apply at ALL times, regardless of site tier.

### Never send or expose:
- User's real name, address, phone, or email
- Any passwords or API keys visible in the conversation
- System file paths that reveal username or machine name
- Browser fingerprint data or session tokens
- Any form fields on external sites — do not auto-fill

### Never allow a site to:
- Execute JavaScript that reads clipboard contents
- Trigger file downloads without explicit user approval
- Redirect to a different domain mid-read
- Load third-party tracking pixels or beacon scripts (note if detected)

### If a site asks for personal info:
Stop immediately. Tell the user:
> "⚠️ This site is requesting [info type]. I have not submitted anything.
> Do you want to proceed manually, or should I find a safer alternative?"

---

## Misinformation Detection Checklist

Before citing any claim from a CAUTION or lower site, check:

| Signal | Red Flag |
|--------|----------|
| Author | Anonymous, no credentials listed |
| Date | No publish date, or very old on a fast-moving topic |
| Sources | No citations, or links to the same site |
| Tone | Outrage, all-caps, excessive punctuation |
| Headline | Contradicts the article body |
| Cross-check | No other credible source confirms the claim |

If 2 or more red flags are present → downgrade site to RISKY.
If the claim cannot be cross-confirmed by a SAFE source → do not present it as fact.

---

## How to Report to the User

Always be transparent. When a site is evaluated, briefly surface the rating:

```
✅ [site] — SAFE. Summary: ...

⚠️ [site] — CAUTION (unverified author). Summary: ...
   Cross-check this before relying on it.

🚫 [site] — RISKY (forced redirect detected). Not opened.

☠️ [site] — BLOCKED (known phishing domain). Not opened.
   Recommend: search for this information on a SAFE source instead.
```

---

## Quick Evaluation Checklist (run on every URL)

```
[ ] HTTPS? (if no → at minimum CAUTION, likely RISKY)
[ ] Domain looks legitimate? (no typosquatting, no random strings)
[ ] TLD appropriate for content? (.gov for govt, .edu for schools, etc.)
[ ] Known to VirusTotal / Google Safe Browsing? (if flagged → BLOCKED)
[ ] Requires login to read? (CAUTION — data harvesting risk)
[ ] Auto-downloads anything? (BLOCKED immediately)
[ ] Cross-checks with another SAFE source? (if not → CAUTION minimum)
[ ] Excessive ads / popups? (CAUTION)
[ ] Outrage-driven or sensationalist content? (RISKY for factual claims)
```

---

## User Reviews & Feedback Evaluation

When researching a product, service, app, or website, always seek out and read
real user feedback in addition to official content. User reviews often contain
truth that marketing copy hides.

### Where to Look for Reviews (in priority order)

```
PLATFORM              BEST FOR                        TRUST LEVEL
--------              --------                        -----------
Reddit threads        Software, services, products    High — hard to fake at scale
Trustpilot            Businesses, services            Medium — verify volume
Google Reviews        Local businesses, apps          Medium — check recency
App Store / Play      Mobile apps                     Medium — filter by "Most Recent"
G2 / Capterra         Business software               Medium — verified buyers
Hacker News           Tech products, startups         High — skeptical audience
Steam Reviews         PC games                        High — purchase-verified
YouTube comments      Products, tutorials             Low — easy to astroturf
Amazon Reviews        Physical products               Low-Medium — heavy fake problem
```

### Fake Review Detection Checklist

Run this on any review set before summarizing it:

| Signal | Fake Review Red Flag |
|--------|---------------------|
| Timing | Dozens of 5-star reviews posted same day or week |
| Language | Overly formal, generic praise ("Great product! Very satisfied!") |
| Profile | Reviewer has 1 review total, no history |
| Specificity | No mention of actual features, problems, or use cases |
| Pattern | All reviews same star rating with similar wording |
| Incentive | "Received product for free in exchange for review" |
| Rebuttal | Company responds defensively to all negative reviews |
| Ratio | Suspicious bimodal split: 90% 5-star + 9% 1-star, nothing in between |

If 3+ red flags → label the review set: **"⚠️ Review integrity suspect — treat with caution."**

### Genuine Review Signals

These patterns indicate authentic feedback:

- Mentions specific features by name (real user knows the product)
- Describes a problem and how it was or wasn't resolved
- Mixed sentiment ("love X but hate Y")
- Verified purchase badge on platforms that support it
- Long-term user mentioning version history or changes over time
- Negative reviews that are detailed and specific

---

## Integration with Other Skills

TruthFinder runs **before** any skill that fetches external content:
- Before `WebSearch` results are summarized
- Before `WebFetch` reads a URL
- Before any skill downloads a file from the internet

It does **not** block:
- Local file reads (no network risk)
- Official package registries (pypi.org, npmjs.com, nuget.org) — treated as SAFE
- GitHub.com, GitLab.com — treated as SAFE for code; CAUTION for linked external resources
