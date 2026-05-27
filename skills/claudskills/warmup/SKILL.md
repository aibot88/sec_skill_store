---
name: warmup
description: >
  The Warmup. A daily intelligence brief for the first coffee.
  CISO mode delivers a structured cybersecurity digest — active threat actors
  mapped to MITRE ATT&CK, emerging CVEs with exploitation status, research
  from CrowdStrike, Palo Alto Unit 42, Elastic Security Labs, and others,
  plus vendor M&A and regulatory movement.
  Product Leader mode delivers a product intelligence brief for GMs, PMs, and
  anyone steering a product — company signal, competitor moves, AI in product,
  funding and M&A, platform risk, regulatory pressure, analyst sentiment, and
  a vertical-specific section that adapts to what they build and who they build for.
  Custom mode lets any user describe their morning interests — stocks, industry
  news, competitor moves, policy, social signal — and maps them to a curated
  source suite.
  Output: a live Iron Log-branded HTML artifact, transparent about every
  source used, pulled on demand with your first coffee.
  Trigger phrases: "warmup", "run warmup", "run the warmup", "start my warmup",
  "give me my warmup", "warmup setup", "set up the warmup",
  "configure the warmup", "warmup config", "add source to warmup",
  "remove source from warmup", "show my warmup sources".
license: MIT
author: H. Michael Nichols
version: 0.3.16
part_of: The Loadout
---

# The Warmup

## Why "The Warmup"

In the gym, a warmup is not optional. You do not walk under the bar cold.
A warmup primes your nervous system, surfaces what is tight, and tells you
whether today's session needs to be adjusted before the work begins. It is
the ten minutes that makes the next ninety honest.

The Warmup does the same thing for your workday. Before you open your inbox,
before you take the first meeting, before you have the conversation that shapes
the next quarter — you know what moved. You know who is active. You know what
the field looks like this morning.

You do not go under the bar cold.

The name comes from *Mission Built*, where the principle is: prepare like the
result matters, because it does.

---

## When to use this skill

Activate this skill when the user asks you to do any of the following:

- Run their warmup
- Get today's warmup
- Set up the warmup for the first time
- Reconfigure their sources
- Add or remove a source from their brief
- See what sources are in use

**Trigger phrases include:** *"warmup"*, *"run warmup"*, *"run the warmup"*,
*"start my warmup"*, *"give me my warmup"*, *"what's in the brief today"*,
*"warmup setup"*, *"set up the warmup"*, *"configure the warmup"*,
*"warmup config"*, *"add [source] to my warmup"*, *"remove [source] from warmup"*,
*"show my warmup sources"*, *"exclude [source] from warmup"*.

---

## Philosophy

**Signal over noise. Every source labeled. Every claim attributed.**

The Warmup has a point of view: authoritative sources first, flagged sources
clearly marked, nothing buried in volume. A brief that forces you to sort
through noise is not a brief — it is a second inbox.

Four principles:

**1. Tier before topic.** Every item in the brief carries its source's trust
tier visually. A Tier 1 government advisory and a Tier 3 community post are
not the same weight of evidence. The brief treats them differently because
they are different. The user always knows what they are reading.

**2. Absence is information.** If a source returns nothing today, that is
reported. If a source is unavailable, that is reported. A blank section is
never padded. Silence from a source that usually speaks is itself a signal.

**3. The source panel is not optional.** Every run of the brief ends with a
full disclosure of every source that was consulted — active, quiet, or
excluded. The user must always be able to audit what their brief was built on.
This is the contract.

**4. Recommendations, not mandates.** When the skill recommends sources,
it explains why. When it flags a source as lower tier, it says so and says why.
The user decides what goes in their brief. The skill's job is to make sure
those decisions are informed.

---

## Modes

Three modes. Each is triggered by a natural phrase.

| Mode | When | What this skill does |
|---|---|---|
| **SETUP** | First time, or reconfiguring from scratch | Establish the user's profile, build their source suite, save to `WARMUP.md`, run a test brief |
| **RUN** | Any time the user wants their brief | Read `WARMUP.md`, fetch live intelligence from each active source, synthesize sections, render the Iron Log artifact |
| **CONFIGURE** | Modifying sources without full re-setup | Show active sources, apply changes (add / remove / exclude), update `WARMUP.md` |

**Brief types available at SETUP:**

| Brief type | Who it's for | Core focus |
|---|---|---|
| **CISO** | Security executives | Threat actors, CVEs, research, vendor market, regulatory |
| **Product Leader** | GMs, PMs, anyone steering a product | Company signal, competitors, AI in product, funding, platform risk, vertical-specific |
| **Custom** | Anyone | User-defined interests, fully flexible source suite |

If no `WARMUP.md` exists in the project root and the user asks to RUN, prompt
for SETUP first: *"No Warmup config found. Run 'warmup setup' to build your
source suite — it takes about two minutes."*

---

## SETUP Mode

**Trigger:** "warmup setup", "set up the warmup", "configure the warmup for the
first time"

### Step 1 — Choose a starting mode

Ask the user: *"Three brief types to choose from — which fits you best?
  · CISO — cybersecurity executive brief
  · Product Leader — GM / PM intelligence brief
  · Custom — describe your own interests and I'll build a source suite around them"*

- **CISO** is the flagship configuration. Pre-loaded with an authoritative
  source suite curated for security executives. Provide your company name
  and sector, region, and peer vendors are looked up automatically — one
  confirmation and you're done.
- **Product Leader** is built for GMs, PMs, and anyone steering a product.
  Provide your company name and competitors, vertical, region, and model
  are researched automatically. Confirm what's right, answer two quick
  follow-ups, and the brief is ready.
- **Custom** builds a source suite from scratch around the user's described
  interests. Takes a few more questions.
- The user can toggle between modes at any time via CONFIGURE.

### Step 1b — Get the user's name

Once the mode is chosen, ask: *"What's your name? I'll use it in your brief header."*
Examples: *"Mike"*, *"Sarah"*, *"Alex"* — or they can skip with anything like *"doesn't matter"* or *"just leave it blank"*.
Stored only in the local WARMUP.md, never sent anywhere. Save as `name:` in the profile. If skipped, leave blank.

### Step 2a — If CISO mode

**Lead with company name. Auto-fill everything derivable. Ask only what can't be looked up.**

Ask: *"What's your company name? I'll look up your sector, region, and typical peer vendors automatically. Or say 'skip' and I'll ask instead."*

**If the user provides a company name:**

Call the **WebSearch tool** with query: `"[Company]" company overview industry sector headquarters cybersecurity`

From the results, determine:
- **Sector** — map to one of the Sector Sources table values below (Healthcare, Financial Services, Energy / Utilities, Technology, Government, Manufacturing / OT, Retail, Critical Infrastructure, or the user's own phrasing if it doesn't map cleanly)
- **Region** — infer from HQ location. Map to: United States, European Union, APAC, Latin America, or Global if multinational
- **Peer vendors** — based on the company's sector and known competitive landscape, suggest 3–5 security vendors they likely watch (e.g., a healthcare org watches CrowdStrike, Palo Alto, Microsoft Sentinel; a fintech watches Wiz, SentinelOne, Lacework)

Present all findings in a single confirmation message:

*"Here's what I found for [Company]:
  · Sector: [X]
  · Region: [Y]
  · Peer vendors to track: [A, B, C]
Does that look right? Edit anything or say 'looks good' to continue."*

Accept natural-language edits. Update any field the user corrects. Save company, sector, and region to WARMUP.md.

**Then ask these two follow-up questions — do not skip them:**

**Follow-up 1 — People to follow:**
*"Anyone in the security world you want to follow closely — executives, CISOs, researchers, threat intel voices? I can suggest a few based on [Company]'s space."*
Suggest 2–3 relevant names based on sector and company (e.g., known CISOs at peer companies, prominent threat researchers, security journalists). Present as: *"People like [A], [B], [C] are worth following if you're in [sector]. Anyone to add, or skip this?"*
Save confirmed names to `track_people:` in WARMUP.md. If skipped, leave blank.

**Follow-up 2 — Personal interests:**
*"Last one — anything you want at the end of your brief that's not work? Sports, markets, a hobby, a team?"*
Save to `special_interests:` in WARMUP.md. If skipped, omit the section. Accept any answer — "skip", "nothing", or an actual interest. Do not pressure.

**If the user skips the company name:**

Ask these four questions one at a time:

1. *"What industry or sector is your organization in?"*
   Examples: *"Healthcare"*, *"Financial Services"*, *"Energy / Utilities"*, *"Technology"*, *"Government"*, *"Manufacturing / OT"*, *"Retail"*, *"Critical Infrastructure"*
   Accept open-form. Map to the Sector Sources table below.

2. *"What region are you primarily operating in?"*
   Examples: *"United States"*, *"European Union"*, *"APAC"*, *"Latin America"*, *"Global"*

3. *"Any specific vendors or competitors you want to track?"*
   Examples: *"Palo Alto, CrowdStrike, Wiz"*, *"Microsoft Sentinel, Splunk, SentinelOne"*, *"skip"*

4. *"Anything you want to stay current on outside of work? Totally optional."*

Build the source suite from the CISO Source Suite tables below.
Add sector-specific sources from the Sector Sources table.

### Step 2b — If Product Leader mode

**Lead with company name. Auto-fill sector, region, and competitors. Ask only what can't be looked up.**

Ask: *"What's your company name — and what product or area are you responsible for? I'll look up your sector, region, and top competitors automatically. Or describe it yourself and I'll go from there."*

Examples: *"Acme Corp, security platform"*, *"Blue Yonder, supply chain"*, *"skip — I'll describe it"*

**If the user provides a company name:**

Call the **WebSearch tool** with query: `"[Company]" product overview market competitors B2B B2C industry`

From the results, determine:
- **Product focus** — what the company primarily builds and sells
- **B2B / B2C / platform** — infer from business model. Map to: `b2b` / `b2c` / `platform` / `marketplace` / `hybrid`. If ambiguous, note it and ask.
- **Vertical / customer industry** — who the company sells to. Map to the vertical source options below (Security, Fintech, Healthcare, Enterprise SaaS, Developer tools, E-commerce, Logistics, etc.)
- **Region** — infer from HQ location
- **Top competitors** — identify 3–5 direct competitors from search results

Present all findings in a single confirmation message:

*"Here's what I found for [Company]:
  · Product: [what they build]
  · Model: [B2B / B2C / platform]
  · Vertical: [customer industry]
  · Region: [Y]
  · Top competitors: [A, B, C, D]
Does that look right? Edit anything or say 'looks good' to continue."*

Accept natural-language edits. If B2B/B2C is still unclear after the search, ask: *"One quick one — are you selling to businesses, consumers, or is it a platform other developers build on?"*

If the user's vertical doesn't map cleanly, ask: *"What does a bad week look like for your business — what external event would most disrupt your roadmap?"* Use the answer to infer the right vertical section.

**Then ask these three follow-up questions — do not skip them:**

**Follow-up 1 — AI vendors:**
*"Which AI vendors or tools matter most to your roadmap? I'd default to OpenAI, Anthropic, Google DeepMind, and Meta AI — plus any tools your team uses (Copilot, Cursor, Mistral). Anything to add or drop?"*
Save confirmed list to `ai_vendors:` in WARMUP.md. If skipped, use the default set.

**Follow-up 2 — People to follow:**
*"Anyone you want to track closely — executives, investors, analysts, journalists, or researchers? I can suggest a few based on [Company]'s space."*
Suggest 2–3 relevant names based on vertical and company (e.g., for a security platform: relevant VCs, CISOs at peer companies, prominent analysts). Present: *"People like [A], [B], [C] are worth following if you're in [vertical]. Anyone to add, or skip this?"*
Save confirmed names to `track_people:` in WARMUP.md. If skipped, leave blank.

**Follow-up 3 — Personal interests:**
*"Last one — anything you want at the end of your brief that's not work? Sports, markets, a hobby, a team?"*
Save to `special_interests:` in WARMUP.md. If skipped, omit the section. Do not pressure.

**If the user skips the company name:**

Ask these five questions one at a time:

1. *"What are you building and who are you building it for?"*
   Accept open-form. Infer product focus, B2B/B2C, and vertical from the answer.

2. *"What industry or vertical is your customer in — or, if B2C, who is your user?"*
   Map to the vertical source options below.

3. *"Who are your top three to five direct competitors?"*
   Generate a suggested list based on what they've described. Present: *"Based on what you've told me, I'd start with: [A, B, C]. Does that look right?"*

4. *"Which AI vendors or tools matter most to your roadmap?"*
   Suggest the standard default set and let them edit.

5. *"Any execs or analysts to track personally? Any non-work interests?"*

### Step 2c — If Custom mode

Ask: *"Describe what you want in your warmup. Be specific — topics,
companies, industries, markets, regions, anything that matters to how you start
your day."*

From the described interests, map each to one or more recommended sources
using the Custom Mode Source-Building Rules below.

For each mapped source, state:
- What you are recommending and why
- Its trust tier
- A flag if it is Tier 3 or lower: *"[Source] is Tier 3 (Community/Unverified).
  Items from it will be labeled in the brief. Worth including?"*

Recommend any sources the user likely wants but did not mention.

### Step 3 — Present the source list for review

Show the full proposed source suite before saving. Format:

```
Tier 1 — Authoritative
  ● CISA Alerts & Advisories
  ● CISA Known Exploited Vulnerabilities (KEV)
  ● NVD / CVE Database
  ...

Tier 2 — Research
  ◉ CrowdStrike Intelligence Blog
  ◉ Palo Alto Unit 42
  ...

Tier 3 — News
  ○ Krebs on Security
  ...

Excluded from this run: (none)

Special Interests  (if provided)
  ○ [Interest 1] — list the 1–3 sources that will cover it
    e.g. "Formula 1 → motorsport.com, ESPN F1, AP Sports"
    e.g. "SEC football → ESPN, 247Sports, AP Sports"
    e.g. "Bourbon releases → Whisky Advocate, BourbonBlog.com"
    e.g. "Markets → Reuters Markets, Yahoo Finance"
  ○ [Interest 2] — same format
```

If special interests were provided, always list them here. The user deserves to see what sources their brief will pull from — this section is not optional when interests exist.

Ask: *"Any sources to add or remove before I save this?"*

### Step 4 — Ask about the lookback window

Before saving, ask: *"Last thing — how far back should I look for your first
brief? The default is 1 day, but since this is your first run I'd recommend
7 days to get up to speed, or 30 days for a full month of context. What works
for you?"*

Accept any natural phrasing: *"7 days"*, *"go back two weeks"*, *"just today"*,
*"one month"*. Save the answer as `window_override` in WARMUP.md if the user
wants a persistent window, or use it only for this run if they say so.
If the user says *"default"* or *"1 day"*, use adaptive lookback (no override).
Remind them: *"You can always override this at run time — just say 'warmup,
go back 2 weeks' and I'll use that window for that run only."*

**Also ask about search depth:**

*"One more setting — search depth. By default I cap each search batch to 5 results and 200 words per article. This keeps the brief fast and token-efficient (typically 40–60K tokens for the fetch phase). If you have more token budget, 'deep' mode doubles both — 10 results per batch, 400 words per article — for broader coverage at roughly 2× the fetch cost. Standard is what I'd recommend for daily use. Which do you prefer?"*

Save as `search_depth: standard` or `search_depth: deep` in WARMUP.md. If the user skips or has no preference, default to `standard`.

### Step 5 — Save WARMUP.md

Save the config file at the project root using the WARMUP.md Config Format
defined below.

### Step 6 — Run a test brief

Immediately run a RUN cycle. If any sources return nothing, report:
*"[Source] returned no signal in the test run. It may be temporarily
unavailable or the search found nothing recent. I've kept it in your config —
it will be checked each run."*

Do not remove sources from config due to a single empty result.

---

## RUN Mode

**Trigger:** "warmup", "run warmup", "run the warmup", "start my warmup",
"give me my warmup", "what's in the brief today"

**Override trigger:** The user can specify a custom lookback at run time:
*"run the warmup one month back"*, *"run warmup since April 15"*,
*"give me the last two weeks"*, *"warmup — go back 30 days"*.
If a lookback phrase is detected, use that window instead of the computed
window and note it in the chat summary line.

### Step 1 — Read config and compute lookback window

Use the **Read file tool** (not bash) to read `WARMUP.md` from the user's project root. If you do not know the project root path, call `list_artifacts` first — the `html_path` from the `"the-warmup"` artifact reveals the workspace folder, and `WARMUP.md` lives in that same folder. If no artifact exists and no WARMUP.md is found, stop and prompt for SETUP.

Note: mode (CISO or Custom), user profile, active source list, excluded
sources, `last_run` date, `window_override` if set.

**Compute the lookback window:**

```
today         = current date (YYYY-MM-DD)
last_run_date = parsed from WARMUP.md `last_run` field (YYYY-MM-DD)
gap_days      = (today - last_run_date) in calendar days

# Override checks — apply first, skip the rest if matched
if user stated a lookback phrase in this run (e.g. "go back 30 days", "since April 15"):
  window = user-specified value   # note in summary line, skip remaining logic
elif window_override is set in WARMUP.md:
  window = window_override
elif last_run is missing or empty:
  window = 30   # first run — bootstrap with a month of context
elif gap_days == 1 AND daily_mode: true in WARMUP.md:
  window = 2    # daily fast-path: skip re-fetching a full 7-day window
elif gap_days <= 7:
  window = 7    # standard — always covers at least a week
else:
  window = min(gap_days, 30)   # catch-up run, capped at 30 days

# Weekend bridge (run after computing window above)
region = WARMUP.md `region` field (default: Sat+Sun weekend; IL/Israel: Fri+Sat)
if today == first working day after regional weekend AND gap_days <= 2:
  window = max(window, gap_days + 2)   # cover full weekend
  note in summary: "Lookback extended to cover weekend"
if gap_days > 7 AND interval spans a user-declared holiday (Notes: "holiday: YYYY-MM-DD"):
  note in summary: "Catch-up run — verify holiday coverage manually if needed"

# Search date parameter
search_after_date = today - (window + 1) days  # +1 catches late-yesterday and early-today
```

Note the computed window in the summary line. **Hard date filter:** every item in the brief MUST have a publication date within the lookback window — no exceptions. If a source has no in-window items, mark it `"status": "quiet"`.

### Step 2 — Fetch phase

Before starting any searches, output this line in chat:
*"🔍 Gathering intelligence from [N] sources · [M] search batches · lookback [X] days — this takes a few minutes."*

**Run all batches concurrently.** Do not wait for one batch to complete before starting the next — they are independent. Fire all batches in a single parallel pass, then synthesize after all return.

For each active source, search for recent content using WebSearch.

Search using compound batch queries — not one query per source. This cuts fetch volume from ~38 calls to ~10 without losing coverage. Run batches concurrently where possible; they do not depend on each other.

**Batch query table (CISO mode):**

| Batch | Sources covered | Query pattern |
|---|---|---|
| Gov pulse | CISA + NSA + FBI + FTC | `(site:cisa.gov OR site:nsa.gov OR site:ic3.gov OR site:ftc.gov) advisory alert after:YYYY-MM-DD` |
| Research | MSTIC + CrowdStrike + Elastic + Wiz + Unit 42 | `(site:microsoft.com/security OR site:crowdstrike.com/blog OR site:elastic.co/security-labs OR site:wiz.io/blog OR site:unit42.paloaltonetworks.com) [sector] threat after:YYYY-MM-DD` |
| CVE sweep | NVD + CISA KEV | `(site:nvd.nist.gov OR site:cisa.gov/known-exploited-vulnerabilities) CVE critical after:YYYY-MM-DD` |
| News | BleepingComputer + SecurityWeek + Krebs + THN + Dark Reading | `(site:bleepingcomputer.com OR site:securityweek.com OR site:krebsonsecurity.com OR site:thehackernews.com OR site:darkreading.com) [sector] after:YYYY-MM-DD` |
| Market | Reuters + Bloomberg + sector vendors | `[company OR sector] acquisition OR breach OR regulatory site:reuters.com OR site:bloomberg.com after:YYYY-MM-DD` |
| Social | X + r/netsec + LinkedIn | `[sector] security debate OR disclosure site:reddit.com/r/netsec after:YYYY-MM-DD` |
| Interests | One per special interest | Targeted query per interest (e.g., `Ironman 70.3 results 2026`) |

Replace `YYYY-MM-DD` with the computed lookback start date. Adapt queries to the user's sector and profile (e.g., a Healthcare CISO adds `site:hhs.gov hc3` to the gov batch). Run Gov, Research, CVE, News, Market, and Interests batches **all concurrently** — fire all batches in a single parallel pass, then synthesize after all return. Do not wait for one batch before starting the next.

**WebSearch result budget:** Check `search_depth` from WARMUP.md:
- `standard` (default): top 5 results per batch · 200 words per article
- `deep`: top 10 results per batch · 400 words per article

Standard is recommended for daily use — keeps fetch-phase cost at 40–60K tokens. Deep roughly doubles that for broader coverage. If `search_depth` is not set or unrecognized, use standard.

**Record for each found item:** source name, trust tier, URL, headline, 2–3 sentence summary, relevant tags (CVE ID, MITRE TTP ID, vendor name, M&A flag, regulatory flag, community flag).

**skipScan fast-path:** If `skip_scan: true` is set in `WARMUP.md`, skip the URL safety check entirely. Set `config.skipScan: true`, `safety.domains: []`, and `safety.totalUrls: 0` in WARMUP_DATA. Do not call URLScan.io. Do not perform Step A allowlist checks. Proceed directly to synthesis. A friendly disclaimer will render in the artifact in place of the Link Safety panel.

**URL safety check — run before adding any item to the brief:**

For every URL returned by search, check it against the trusted-domain allowlist
and URLScan.io before including it in the report.

```
Step A — Allowlist check (instant, no API call):
  If the URL's registered domain matches the allowlist below → VERIFIED SAFE.
  This covers all known-good sources across CISO and Product Leader modes.

  CISO allowlist domains:
    cisa.gov, nsa.gov, ic3.gov, fbi.gov, ftc.gov, nvd.nist.gov, attack.mitre.org,
    crowdstrike.com, unit42.paloaltonetworks.com, elastic.co, cloud.google.com,
    microsoft.com, blog.talosintelligence.com, secureworks.com, recordedfuture.com,
    wiz.io, krebsonsecurity.com, thehackernews.com, darkreading.com,
    securityweek.com, bleepingcomputer.com, arstechnica.com, scmagazine.com,
    crn.com, techcrunch.com, cybersecurityventures.com,
    hhs.gov, h-isac.org, fsisac.com, occ.gov, eisac.com, cio.gov,
    pcisecuritystandards.org, dragos.com, claroty.com, nozominetworks.com

  Product Leader allowlist domains:
    sec.gov, crunchbase.com, a16z.com, sequoiacap.com, cbinsights.com,
    gartner.com, forrester.com, producthunt.com,
    techcrunch.com, theverge.com, wired.com, fastcompany.com,
    reuters.com, bloomberg.com, lennysnewsletter.com, reforge.com,
    news.ycombinator.com, linkedin.com, g2.com, capterra.com, trustpilot.com,
    openai.com, anthropic.com, deepmind.google, ai.meta.com, research.facebook.com,
    mistral.ai, huggingface.co, arxiv.org,
    github.blog, github.com, stackoverflow.com, changelog.com,
    paymentsdive.com, pymnts.com, consumerfinance.gov,
    rockhealth.com, himss.org, cms.gov, fda.gov,
    socialmediatoday.com, saastr.com, chartmogul.com,
    digitalcommerce360.com, freightwaves.com, supplychaindive.com,
    nfx.com, bvp.com

  User-configured sources (from WARMUP.md `competitors:` and `ai_vendors:` fields):
    Extract the registered domain from each configured URL. These are user-chosen
    sources that passed their initial review at SETUP. Treat as allowlisted.
    Example: if competitors includes "https://www.splunk.com", splunk.com is allowlisted.

Step B — URLScan.io check (for domains not on the allowlist):
  Query: https://urlscan.io/search/#domain:<domain>
  If result exists AND verdict is explicitly clean → VERIFIED SAFE.
  All other outcomes → NOT VERIFIED: treat as flagged and exclude.

"All other outcomes" means: suspicious verdict, malicious verdict, no result
found, API timeout, API error, rate limit, ambiguous verdict, or any condition
where a clean result cannot be positively confirmed. There is no partial credit.
A URL is either verified safe or it does not appear in the report.
```

**If a URL is not verified safe (flagged, failed scan, or unknown):**
- Do not include the URL anywhere in the report. No hyperlink, no bare URL.
- Record it in a `flagged_urls` list: `{url, domain, verdict, source_name}`.
  For scan failures, set `verdict` to `"scan unavailable"`.
- The article's content may still appear in the brief as plain text without
  a link, attributed to the source name only, if the content is relevant
  (e.g., *"CrowdStrike reported X — link omitted, domain not verified"*).
- The `flagged_urls` list feeds into the safety WARMUP_DATA block and is
  surfaced in the scan badge and the Link Safety section at the bottom of
  the artifact. The scan badge text updates to: *"N links scanned · M not verified"*.
- If any URLs were excluded, add a brief note in the chat summary line:
  *"⚠ [M] URL(s) excluded — not verified safe (flagged or scan unavailable)."*
- The Link Safety section in the artifact must only list domains that passed
  verification. It must never show a domain that failed or was not checked.

After all batches complete, output in chat:
*"🔒 Running link safety verification on [N] URLs..."*

**Safety check is a Step 2 action — not a render-time assumption.** The `safety.domains` array in WARMUP_DATA must be built from the checks actually performed during this fetch phase. Do not copy verdicts from a previous run, do not assume all sources are clean, and do not fill in the array during synthesis or render. Every domain that appears in `safety.domains` must have been checked in Step 2 of this run. Verdict values: `"ALLOWLISTED"` (Step A match, no external call), `"CLEAN"` (Step B URLScan.io explicitly clean). Anything else is flagged and excluded.

**If a batch returns nothing:** mark those sources "no signal today." Do not invent content. A quiet source is reported honestly.

**Source prioritization:** Tier 1 and Tier 2 sources are fetched first and given the most depth. Tier 3 and Tier 4 are supplemental. If you run out of capacity, deprioritize Tier 3 and Tier 4 before cutting Tier 1 or 2.

### Step 3 — Synthesize phase

Output in chat before starting synthesis:
*"⚡ Synthesizing [N] items across [M] sections..."*

**DATE FILTER — MANDATORY GATE. No item enters WARMUP_DATA without passing this check.**

```
lookback_start = today - lookback_days

BEFORE WRITING EACH ITEM — run this check:
  1. Parse item.date as YYYY-MM-DD
  2. Is item.date ≥ lookback_start? → INCLUDE
  3. Is item.date < lookback_start? → DISCARD immediately. Do not include it "because it's relevant."

Real violations that MUST be caught (window = 7 days, today = 2026-05-16):
  lookback_start = 2026-05-09
  item.date = 2026-05-08  → 8 days old  → REJECT  ← one day over. Still REJECT.
  item.date = 2026-05-06  → 10 days old → REJECT  ← "only two weeks ago" is still REJECT.
  item.date = 2026-05-09  → 7 days old  → ACCEPT  (exactly at boundary = OK)
  item.date = 2026-05-10  → 6 days old  → ACCEPT
```

**No date = discard.** If a result has no parseable publication date, discard it. Do not guess or assume.

**"Relevant but old" = still discard.** An article can be highly relevant and still violate the date filter. Relevance does not override the date gate.

If after filtering a source has zero in-window items, mark it `"status": "quiet"` in `sources[]` and exclude it from `safety.domains`.

This gate runs **before** you organize items into sections. Do not route stale items into sections intending to remove them later — discard at first sight, before any further processing.

Organize fetched items into sections using the Section Structure below
(CISO mode) or the user's defined interest categories (Custom mode).

**Curation rule:** quality over quantity. If 25+ items come back from searches,
select the 12–18 most signal-dense. Prefer Tier 1 and Tier 2 findings.
Within a section, order by relevance to the user's profile, not by source tier.

### Step 3b — Special Interests (optional)

If `special_interests` is set in `WARMUP.md`, the Interests batch was already fetched concurrently in Step 2. Do not run a second fetch here.

Render the results from the Step 2 Interests batch as a **Special Interests** section in the artifact, positioned after AI Intelligence (or Industry Intel if the AI section is not present) and before Social Signal. Use general news and sports/topic sources — label all items with `○` (Tier 3 / Community/News).

Tag format: use `[NBA]`, `[SEC FOOTBALL]`, `[F1]`, etc. — whatever matches
the interest. Keep summaries conversational — this is the coffee reading, not
an intelligence item. Two to four sentences is enough.

If `special_interests` is not set or is empty, omit the section entirely.
Do not add a placeholder or ask about it during RUN.

### Step 4 — Render phase

**ABSOLUTE RULE — NO EXCEPTIONS:**
The brief HTML is ALWAYS built from the engine returned by the `warmup_get_template` **MCP tool** (invoked in Step 1b) or from the existing artifact file. **Never write HTML from scratch. Never read warmup-template.html from disk. Never use training-data memory of what the brief looks like.** The CSS, layout, typography, and PDF builder exist only in the tool response — reproducing them from memory will produce the wrong design and break PDF export.

If you reach this step without having invoked the `warmup_get_template` MCP tool (first run or engine update) or confirmed the existing artifact file is readable (version match), stop and invoke the `warmup_get_template` MCP tool now (tool call — not a file read) before continuing.

**Rule: only `WARMUP_DATA` changes between reports.** The engine (CSS, JS, PDF builder, renderer) is fixed in `warmup-template.html` and touched only when the version marker changes. Always deliver via `update_artifact` / `create_artifact` — never a `computer://` file link. The **Save PDF** button inside the artifact is the user's only download path.

**Inject and render (Step 1b already determined the base HTML):**

By the time you reach this step, Step 1b has already:
- Called `list_artifacts` and determined first run vs. daily run.
- For **daily runs with a version match:** the file exists at `html_path`.
- For **first runs or engine version mismatches:** `warmup_get_template` was already called and the engine shell is in context.

**Do not call `list_artifacts` or `warmup_get_template` again here.**

**Path A — Version match (daily run, no engine update):**  
Replace only the `<script id="warmup-data">` block in the existing HTML. Do NOT read the full file — the engine is 131KB and reading it wastes ~30K tokens. Use Grep to locate the exact line, read only that block, then Edit it in place.

1. **Grep** for `<script id="warmup-data">` in `html_path` to find the line number.
2. Use the **Read tool** with `offset` and `limit` set to read only the `<script id="warmup-data">` … `</script>` block (~10–20 lines). This gives you the exact current text to match.
3. Use the **Edit tool** to replace the entire block (from `<script id="warmup-data">` through its closing `</script>`) with exactly:
   ```
   <script id="warmup-data">
   window.WARMUP_DATA = <FULL JSON of the new WARMUP_DATA dict>;
   </script>
   ```
   Touch no other part of the HTML. The Edit tool does a targeted string replacement — the rest of the 131KB engine is never read or re-emitted.
4. Call `update_artifact` with `id: "the-warmup"` and the same `html_path`.

> **Do not use bash for this step.** Bash runs in a Linux sandbox where macOS file paths are remapped and will not resolve. Use the Grep, Read, and Edit file tools only — they accept the real macOS path from `html_path` directly.

**Path B — First run or engine update:**  

The MCP server injects WARMUP_DATA server-side. You do NOT write the template then edit a placeholder — the placeholder is gone after injection. Call the tool with your data, get back filled HTML, write it once.

1. **Call `warmup_get_template({ warmup_data: JSON.stringify(WARMUP_DATA) })`.** The server injects `WARMUP_DATA` into the engine shell before returning. The response is complete, filled HTML — no editing needed.

2. **Write the filled HTML to disk.** Use the Write tool to write the response to `warmup-artifact.html` in the **user's selected/workspace folder** (e.g. `~/Documents/Claude/Projects/`). Do NOT write to the outputs or temp directory; that path is cleared between sessions. Do not modify the HTML before writing — write it exactly as received.

3. **Register the artifact.** Call `create_artifact` (first run) or `update_artifact` (engine update) with `id: "the-warmup"` and `html_path` pointing to the written file.

Never call `create_artifact` when the artifact already exists — it will fail. Never call `update_artifact` when the artifact does not exist yet.

> **Do not use bash for Path B.** Bash runs in a Linux sandbox where macOS file paths are remapped and will not resolve. Use the Write file tool only.

**Path C — Edit in place (user requests a correction to the existing brief):**  
Triggered when the user asks to change something in the current report — fix a headline, correct a date, add or remove an item, rewrite a body — without running new searches. No searches. No template fetch. Extract, modify, patch.

Step 1: Use the Read tool to read the full HTML from `html_path`.

Step 2: Locate the `<script id="warmup-data">` … `</script>` block. Extract the JSON object inside it. Apply the user's requested change to the relevant field(s) in `WARMUP_DATA`. Touch nothing else.

Step 3: Replace the entire `<script id="warmup-data">` block with the modified version and use the Write tool to write the complete HTML back to `html_path`. Call `update_artifact` with `id: "the-warmup"` and the same `html_path`.

> **Do not use bash for Path C.** Same reason as Path A — bash runs in a Linux sandbox where macOS paths do not resolve. Use the Read and Write file tools only.

**Token cost summary:**

| Path | Trigger | Token cost |
|---|---|---|
| A — Data patch | Daily run, engine match | ~1–2KB targeted Grep+Read (avoids reading the full 131KB engine) |
| B — Full engine | First run or version mismatch | ~131KB filled HTML from MCP tool (one-time; no file read needed) |
| C — Edit in place | User correction to existing brief | ~1–2KB targeted Grep+Read (same Grep+targeted-Read approach as Path A) |

**When an engine bug is fixed:**
1. Apply the fix to `warmup/warmup-template.html` — this is the canonical source.
2. Apply the same fix to the active `warmup-artifact.html`.
3. Call `update_artifact` to push the fix into the live artifact.
4. The fix propagates to all future reports automatically because new reports start from the template.

**`WARMUP_DATA` schema (v0.3.0 — Morning Edition):**

> **Config field accuracy rule:** `mode`, `sector`, `company`, and `region` MUST be copied verbatim from `WARMUP.md`. Do not infer, generalize, abbreviate, or replace. If the user said "Security", sector = "Security". If the user said "Global", region = "Global". These values appear as pills the user sees on every run.

```json
{
  "config": {
    // Required
    "name": "Mike",
    "mode": "CISO",
    "company": "Elastic",
    "sector": "Cybersecurity",
    "reportDate": "Thursday, 15 May 2026",   // REQUIRED — full display string for the masthead date (e.g. "Friday, 15 May 2026").
                                               // Format: "{Weekday}, {DD} {Month} {YYYY}". Use today's date in the user's timezone.
                                               // Without this field the masthead date falls back to template placeholder text.
    "updated": "15 May 2026",                // Footer display string
    "lastRun": "2026-05-14",                 // ISO date — drives issue number
    "dateRange": "May 8 – May 15, 2026",     // Lookback window display string
    "sourcesActive": 12,
    "sourcesQuiet": 4,
    "showQuote": true,   // REQUIRED — must be true (JSON boolean). Omitting or setting false hides the daily quote.
    "scanTime": "HH:MM TZ", // REQUIRED — set to current generation time in 24-hr user-timezone format (e.g. "06:14 ET").
                              // Use timezone from WARMUP.md; default to UTC and write "HH:MM UTC" if not set.
                              // THE single timestamp source — populates masthead, signal bar, safety panel, PDF.
                              // Without this, Generated cell shows "—" and scan timestamp is blank.
    "timezone": "ET",   // REQUIRED — copy verbatim from WARMUP.md `timezone` field (e.g. "ET", "PT", "UTC").
                        // CRITICAL: this is the USER'S local timezone — NOT the company's headquarters timezone.
                        // Read it from WARMUP.md. Do not infer from the company location. Write "UTC" if not set.
                        // Without this field the time display in the masthead is missing timezone context.
    // Optional fields — include even if blank (write "" not omit)
    "region": "Global",
    "vendors": "CrowdStrike, Palo Alto",  // Copy verbatim from WARMUP.md vendors field. Write "" if blank — do not omit.
    "interests": "",
    "totalLinks": 18,  // Count of verified-safe clickable URLs in the rendered brief. Must equal safety.totalUrls.
    "skipScan": false,  // Optional — set true if skip_scan: true in WARMUP.md. Hides scan badge, skips safety panel, shows friendly disclaimer instead.
    "searchDepth": "standard"  // "standard" | "deep" — copy from WARMUP.md search_depth. Drives depth indicator in sources panel and configure modal.
  },
  "sections": [
    {
      "id": "threat",
      "label": "Threat Landscape",
      "sub": "Active campaigns and fresh exploitation. What your stack should be watching for today.",
      // sub: ALWAYS populated — the section's standing editorial deck, one sentence.
      //      This renders visibly in the brief as italic text under the section heading.
      //      NEVER put lookback computation text, agent instructions, or meta-commentary here.
      //      WRONG: "1-day lookback (first run). Say 'warmup, go back 7 days' for context."
      //      RIGHT: "Active campaigns and fresh exploitation. What your stack should be watching for today."
      //      Write it as editorial voice — a standing description of what this section covers.
      // note: null unless there is a today-only run caveat (e.g. "Source X was down"). Never repeat sub here.
      "note": null,
      "items": [
        {
          // items[0] is the EDITORIAL LEAD — rendered full-width with a large
          // headline and an oxblood drop-cap on the first letter of body.
          // Choose it deliberately: most important item in the section.
          "dot": "d1", "src": "CISA",
          "tags": [{"cls": "t-alert", "text": "KEV ADDED"}, {"cls": "t-mitre", "text": "T1190"}],
          "url": "https://...",
          "hl": "Article headline.",
          "deck": "Federal agencies have until June 4 to patch.",
          // deck: LEAD ITEMS ONLY. One short italic sentence — the 'so what?'.
          // Omit entirely on non-lead items (items[1..N]).
          "body": "2–3 sentence summary in plain prose.",
          "date": "YYYY-MM-DD"
        },
        {
          // items[1..N] render in a two-column grid. No deck field. Date-sorted.
          "dot": "d2", "src": "Source Name",
          "tags": [],
          "url": "https://...",
          "hl": "Article headline",
          "body": "2–3 sentence summary.",
          "date": "YYYY-MM-DD"
        }
      ]
    }
  ],
  "sources": [
    // status: "active" | "quiet" | "excluded" — exact strings only, no other values permitted.
    // ct: "N items" for active sources (e.g. "2 items"), "—" for quiet sources, "excluded" for excluded sources.
    {"nm": "CISA Alerts & Advisories", "dom": "cisa.gov", "dot": "d1", "ct": "2 items", "status": "active"},
    {"nm": "NSA Advisories", "dom": "nsa.gov", "dot": "d1", "ct": "—", "status": "quiet"}
  ],
  "safety": {
    // domains: REQUIRED — one entry per active source. Populated from Step 2 checks — never fabricated.
    // Empty array = safety panel does not render. This field must not be omitted or left empty.
    // verdict values (exact strings):
    //   "ALLOWLISTED"   — domain matched the Step A allowlist (no external call made)
    //   "CLEAN"         — domain passed URLScan.io Step B check (explicitly clean verdict)
    // Flagged domains do NOT appear here — they go in flagged_urls and are excluded from the brief.
    // INTEGRITY RULE: domains.length MUST equal the number of active sources exactly.
    "domains": [{"domain": "cisa.gov", "verdict": "ALLOWLISTED"}],
    "totalUrls": 12,   // REQUIRED — count of verified-safe clickable URLs in the rendered brief. Must equal config.totalLinks.
    "flagged": 0,
    "scannedAt": ""   // Empty string — renderer uses scanTime. Fill only to override.
  },
  // dates: REQUIRED — one entry per item using the item's hl string (or a unique prefix) as the key.
  // Used by the template to render per-item publication dates. Empty object = no dates rendered.
  "dates": {"Article headline prefix": "YYYY-MM-DD"}
}
```

**Editorial lead rules:**
- `items[0]` is the lead for every section. It renders full-width with a large Oswald headline and an oxblood drop-cap on the first letter of `body`.
- Always use `deck` on lead items — one italic sentence that adds the "so what?" framing.
- The lead is never re-sorted. Choose it deliberately — most important item in the section.
- Items 1..N render in a two-column grid, date-sorted descending. No `deck` field on these.

**`scanTime` is the single timestamp source.** Write it once as `"HH:MM TZ"` (24-hour, user's timezone, e.g. `"06:14 ET"`). The renderer uses it in the masthead, the Generated cell in the signal bar, the link-safety scanned-at line, and the PDF masthead. Do not write separate timestamp values anywhere else.

**On engine bugs:**
1. Apply the fix to `warmup/warmup-template.html` — this is the canonical source.
2. Apply the same fix to the active `warmup-artifact.html`.
3. Call `update_artifact` to push the fix into the live artifact.
4. The fix propagates to all future reports automatically because new reports start from the template.

**Never build the artifact HTML from scratch.** Always start from the engine shell returned by `warmup_get_template`. Building from scratch risks re-introducing fixed bugs and diverging from the canonical engine.

### Step 5 — Summary line

After rendering, output a single summary line in the chat:
*"[N] items across [N] sections · [N] sources active · [N] sources quiet today · Lookback: [N] days"*

If this was a catch-up run, append the reason:
*"… · Lookback: 12 days (catch-up from [last_run_date])"*

Nothing else in chat. The brief is the artifact. Do not duplicate its content
in the chat response.

### Step 5b — Source emergence check (periodic)

**When to run:** After any successful RUN where `(today - updated) >= 30 days`.
The `updated` field in WARMUP.md records when the source list was last configured.
If it has been 30+ days since the user last touched their source config, scan
for new sources that have emerged since then.

**How to run:**

During the fetch phase, note any domains that appeared in search results but are
**not** in the user's active or excluded source list. After synthesis, evaluate
each against the Source Trust Framework. Surface only sources that meet at least
one of these bars:
- Tier 1 or Tier 2 by the framework criteria
- A Tier 3 source with demonstrated sector relevance (it appeared in multiple
  fetched items, not just once) and strong editorial reputation
- A sector-specific source that didn't exist or wasn't notable 30 days ago
  (new research arm, new government advisory feed, etc.)

**Cap at 3 recommendations per run.** Do not recommend sources already in the
config (active or excluded). Do not recommend a source the user has previously
excluded — they made that call deliberately.

**Output format** — append after the summary line in chat, separated by a blank line:

```
💡 New source worth adding:
  [Source Name] · Tier N · domain.com
  [One sentence: what it covers and why it's relevant to the user's sector/profile.]
  Say "add [source name] to warmup" to include it.
```

If more than one recommendation: list them as a short block under a single
`💡 New sources worth adding:` header.

If nothing new qualifies: output nothing. Do not add a "no new sources found"
line — silence is the correct signal.

**Frequency note:** 30 days is the default check interval because a month is
roughly how long it takes for a new source to establish a track record worth
recommending. If the user wants tighter checks (e.g., weekly), they can add
`source_check_days: 7` to the Notes section of WARMUP.md and this step will
use that value instead.

### Step 6 — Update last_run in WARMUP.md

After a successful render, update the `last_run` field in `WARMUP.md` to
today's date in `YYYY-MM-DD` format. This is the record the next run uses
to compute its lookback window.

Do not update `last_run` if the run failed, produced no items, or produced fewer than 3 items total across all sections — treat these as degraded runs and preserve the window so the next run has a wider lookback to recover missing content.

---

## CONFIGURE Mode

**Trigger:** "warmup config", "update my warmup", "add source to warmup",
"remove source from warmup", "show my warmup sources",
"exclude [source] from warmup", "what sources is the warmup using"

### Show sources

Display the current source list in a compact table:

```
Source              | Tier | Domain                    | Status
--------------------|------|---------------------------|--------
CISA Alerts         |  1   | cisa.gov                  | Active
CISA KEV            |  1   | cisa.gov                  | Active
CrowdStrike Blog    |  2   | crowdstrike.com/blog       | Active
...
Krebs on Security   |  3   | krebsonsecurity.com       | Excluded
```

### Add a source

1. Assign a trust tier using the Source Trust Framework.
2. If Tier 3 or lower, flag it explicitly.
3. Add to `WARMUP.md` under the appropriate tier.
4. Confirm: *"Added [source] as Tier [N]. It will appear in your next brief."*

### Remove or exclude a source

Move from active list to Excluded Sources in `WARMUP.md`. The source remains
in the config but is skipped at runtime and shown in the Source Transparency
Panel as excluded.

### Recommend additional sources

If the user asks for recommendations: suggest 3–5 sources relevant to their
profile that they do not already have. For CISO mode, look for gaps in
sector-specific coverage or missing Tier 2 research firms.

### Switch mode

If the user wants to switch between CISO, Product Leader, and Custom modes,
run the appropriate branch of SETUP Step 2 and rebuild the source suite.
Carry over any manually-added sources the user wants to keep.

### Ask about lookback after any configuration change

After any meaningful config change (new sector, new sources, switched mode,
changed company), ask: *"How far back should the next brief look? Default is
1 day — or tell me a different window for this run."* This catches the case
where a config change means the user wants a fresh sweep to see how the new
sources perform. Do not ask after minor changes (typo fixes, timezone updates).

---

## CISO Source Suite

The default source suite for CISO mode. Load all of these unless the user
explicitly excludes one.

### Tier 1 — Government & Authoritative

These are primary sources of truth. Treat their content as high-confidence.
Never remove from the brief without user confirmation.

| Source | Search target | What it contributes |
|---|---|---|
| CISA Alerts & Advisories | site:cisa.gov advisories | Active exploits, critical advisories, joint alerts with NSA/FBI |
| CISA Known Exploited Vulnerabilities (KEV) | site:cisa.gov known-exploited-vulnerabilities | CVEs with confirmed in-the-wild exploitation |
| NVD / CVE Database | site:nvd.nist.gov OR "CVE-2026" new vulnerability | New and updated CVE records, CVSS scores |
| MITRE ATT&CK | site:attack.mitre.org | TTP context for attributed campaigns; use for tagging items from other sources |
| FBI Cyber Division | site:ic3.gov OR site:fbi.gov/investigate/cyber | Public PSAs, threat actor attributions, financial fraud patterns |
| NSA Cybersecurity Advisories | site:nsa.gov cybersecurity advisory | Nation-state TTP guidance, hardening recommendations |

### Tier 2 — Premier Research Firms

High-quality, vetted research with named analysts and editorial review.
Include all by default.

| Source | Search target | What it contributes |
|---|---|---|
| CrowdStrike Intelligence Blog | site:crowdstrike.com/blog | Adversary tracking (BEAR/SPIDER/KITTEN taxonomy), campaign analysis |
| Palo Alto Unit 42 | site:unit42.paloaltonetworks.com | Threat research, malware reverse engineering, IR findings |
| Elastic Security Labs | site:elastic.co/security-labs | Behavioral detection research, open-source SIEM rules |
| Google Mandiant | "mandiant" threat intelligence blog | APT group tracking, IR case studies, zero-day attribution |
| Microsoft Threat Intelligence (MSTIC) | site:microsoft.com/security/blog | Windows/Azure/cloud threat actor TTPs, nation-state activity |
| Cisco Talos | site:blog.talosintelligence.com | Threat telemetry, malware family analysis, email threat data |
| Secureworks CTU | site:secureworks.com/blog | GOLD/IRON/BRONZE group tracking, ransomware intelligence |
| Recorded Future | site:recordedfuture.com/blog | Dark web intelligence, global threat signals, public research |

### Tier 3 — Reputable Security News

Reliable reporting with editorial standards. Label items [NEWS].
Include all by default.

| Source | Search target | What it contributes |
|---|---|---|
| Krebs on Security | site:krebsonsecurity.com | Investigative security reporting, breach coverage |
| The Hacker News | site:thehackernews.com | Breaking security news, vulnerability coverage |
| Dark Reading | site:darkreading.com | CISO-relevant analysis, industry reporting |
| SecurityWeek | site:securityweek.com | Vendor news, vulnerability roundups |
| BleepingComputer | site:bleepingcomputer.com | Ransomware tracking, active exploit news |
| Ars Technica Security | site:arstechnica.com/security | Technical security reporting, long-form analysis |

### Tier 4 — Vendor & Market Intelligence

For tracking M&A, funding, product launches, regulatory moves. Label items
[VENDOR] or [REGULATORY]. Read with commercial interest context.

| Source | Search target | What it contributes |
|---|---|---|
| CRN | site:crn.com security | Channel news, vendor M&A, partner moves |
| SC Magazine | site:scmagazine.com | Security product news, market coverage |
| TechCrunch Security | site:techcrunch.com/category/security | Startup funding, cybersecurity acquisitions |
| Cybersecurity Ventures | site:cybersecurityventures.com | Market reports, spending forecasts |

---

---

## Product Leader Source Suite

Default source suite for Product Leader mode. Core sources load for all users; vertical-specific sources added at SETUP.

### Tier 1 — Primary Sources

| Source | Search target | What it contributes |
|---|---|---|
| SEC EDGAR | `site:sec.gov [company] OR [competitor]` | Public filings, 8-K events, earnings, exec changes |
| Crunchbase News | `site:crunchbase.com [sector] funding OR acquisition` | Funding rounds, M&A, investor signals |
| Company newsroom | `site:[company].com/news OR /press` | Official announcements, product launches, leadership moves |
| Competitor newsrooms | `site:[competitor].com/news OR /press` | Official competitor announcements |

### Tier 2 — Research & Premium Coverage

| Source | Search target | What it contributes |
|---|---|---|
| a16z | `site:a16z.com [sector] OR [vertical]` | Market theses, sector deep-dives, portfolio signals |
| Sequoia Capital | `site:sequoiacap.com [sector]` | Market memos, economic outlook, founder research |
| The Information | `site:theinformation.com [company] OR [sector]` | Investigative tech journalism (search for public excerpts) |
| Stratechery | `site:stratechery.com [company] OR [sector]` | Strategic analysis of tech business models |
| Benedict Evans | `site:ben-evans.com [sector] OR [topic]` | Consumer tech and market structure analysis |
| CB Insights | `site:cbinsights.com [sector] intelligence` | Market maps, funding data, industry reports |
| Gartner | `site:gartner.com [sector] magic quadrant OR report` | Analyst positioning, market category definitions |
| Forrester | `site:forrester.com [sector] wave OR report` | Enterprise buyer-focused analyst coverage |
| Product Hunt | `site:producthunt.com [category]` | New product launches, early competitor signal |

### Tier 3 — News & Community

Label items [NEWS] or [COMMUNITY].

| Source | Search target | What it contributes |
|---|---|---|
| TechCrunch | `site:techcrunch.com [company] OR [sector]` | Funding news, product launches, startup coverage |
| The Verge | `site:theverge.com [company] OR [product category]` | Consumer tech, platform policy, product reviews |
| Wired | `site:wired.com [company] OR [sector]` | Long-form technology and business reporting |
| Fast Company | `site:fastcompany.com [company] OR innovation` | Innovation, design, product culture |
| Reuters / Bloomberg | `site:reuters.com OR site:bloomberg.com [company] OR [sector]` | Breaking M&A (Tier 1); market color (Tier 3) |
| Lenny's Newsletter | `site:lennysnewsletter.com [topic]` | Practitioner PM and growth content |
| Reforge Blog | `site:reforge.com/blog [topic]` | Product growth and retention frameworks |
| Hacker News | `site:news.ycombinator.com [company] OR [product]` | Developer community signal; earliest mention of product issues |
| LinkedIn | `[person] OR [company] site:linkedin.com` | Exec commentary, people moves, product announcements |

### Tier 4 — Vendor & Analyst Marketing

| Source | Search target | What it contributes |
|---|---|---|
| G2 | `site:g2.com [company] OR [competitor] reviews` | Customer review signal, competitive grids |
| Capterra | `site:capterra.com [company] OR [competitor]` | B2B buyer reviews, alternative discovery |
| Trustpilot | `site:trustpilot.com [company] OR [competitor]` | Consumer review signal |
| Vendor blogs | `site:[vendor].com/blog [product area]` | AI vendor product updates, API changes |

### AI Vendor Sources (always included for Product Leader)

| Source | Search target | What it contributes |
|---|---|---|
| OpenAI Blog | `site:openai.com/blog` | Model releases, API changes, pricing |
| Anthropic | `site:anthropic.com/news OR /research` | Model releases, safety research, API updates |
| Google DeepMind | `site:deepmind.google OR site:blog.google/technology/ai` | Research, Gemini updates, infrastructure |
| Meta AI | `site:ai.meta.com/blog OR site:research.facebook.com` | Open-source models (Llama), research |
| Mistral AI | `site:mistral.ai/news` | European frontier model moves, open-weight releases |
| Hugging Face | `site:huggingface.co/blog` | Open-source model ecosystem, tooling |
| arXiv cs.AI | `site:arxiv.org cs.AI [topic]` | Pre-print research; leading indicator of capability direction |

Additional AI vendor sources from `ai_vendors:` in WARMUP.md appended at runtime.

### Vertical-Specific Sources (Product Leader)

| Vertical | Add These Sources |
|---|---|
| **Security product** | Full CISO Tier 1–2 suite (CISA, NVD, CrowdStrike, Unit 42, MSTIC, Elastic Security Labs, etc.) |
| **Fintech / payments** | OCC (`site:occ.gov`), CFPB (`site:consumerfinance.gov`), FS-ISAC, Payments Dive, PYMNTS |
| **Healthcare / digital health** | FDA Digital Health, CMS (`site:cms.gov`), Rock Health, HIMSS |
| **Consumer social / creator** | Social Media Today, Creator Economy Report, platform dev blogs (Meta, TikTok, YouTube, Snap) |
| **Enterprise SaaS** | Bessemer State of Cloud, SaaStr, ChartMogul blog, Lighter Capital |
| **Developer tools / platform** | GitHub Blog, Stack Overflow Developer Survey, npm trends, CNCF reports, Changelog |
| **E-commerce / retail** | Digital Commerce 360, Shopify Engineering Blog, NRF research, Morning Brew Retail |
| **Logistics / supply chain** | FreightWaves, Supply Chain Dive, Flexport blog |
| **Marketplace** | a16z marketplace posts, NFX (`site:nfx.com`), a16z marketplace essays |

## Sector-Specific Sources

Append these when the user's sector matches. Add to the appropriate tier in
the source suite.

| Sector | Add These Sources |
|---|---|
| Healthcare | HHS HC3 (`site:hhs.gov hc3`), Health-ISAC news (`site:h-isac.org`), AHA cybersecurity alerts |
| Financial Services | FS-ISAC public blog (`site:fsisac.com`), OCC alerts (`site:occ.gov`), FFIEC guidance |
| Energy / Utilities | E-ISAC (`site:eisac.com`), CISA ICS-CERT (`site:cisa.gov ics-cert`), NERC CIP updates |
| Government / Public Sector | FedRAMP news, FISMA updates, DoD CMMC bulletins (`site:dodcio.defense.gov`) |
| Technology | GitHub Security Advisories (`site:github.com/advisories`), Wiz Research (`site:wiz.io/blog`), Snyk Vulnerability DB |
| Retail / Consumer | PCI Security Council (`site:pcisecuritystandards.org`), NRF security news |
| Manufacturing / OT | Dragos OT Intel (`site:dragos.com/blog`), Claroty Research (`site:claroty.com/team82`), Nozomi Research |
| Critical Infrastructure | Extends Energy + Government sources; add ICS-CERT advisories explicitly |

---

## CISO Report — Section Structure

Organize the brief into these five sections, in this order.
Each section has a defined scope. Stay within it.

### Section 1 — THREAT LANDSCAPE

**What belongs here:** Named threat actors currently active; their targeted
sectors; their primary TTPs.

- Use CrowdStrike naming convention for threat groups where possible
  (SCATTERED SPIDER, COZY BEAR, VOLT TYPHOON, etc.). Note aliases when
  relevant (e.g., "APT29 / COZY BEAR").
- Tag each item with the actor name, 1–2 MITRE ATT&CK technique IDs
  (e.g., T1566.001 — Spearphishing Attachment), and source.
- If the user provided a sector, lead with actors known to target that
  sector. If no sector-specific activity exists this week, say so briefly
  rather than forcing items that do not fit.
- If the user provided a company name, note explicitly if the company
  or its sector has appeared in attribution reporting.

**Scope boundary:** Attribution and TTPs only. Do not put CVEs here —
those go in Emerging Threats. Do not put vendor news here — that goes
in Industry Intel.

### Section 2 — EMERGING THREATS

**What belongs here:** New vulnerabilities and attack techniques entering
circulation in the last 7 days.

- CISA KEV additions: any CVE added to the Known Exploited Vulnerabilities
  catalog this week.
- High/critical CVEs with active exploitation evidence or public POC.
- Zero-day disclosures. New malware families or significant variants.
- Each CVE entry: CVE ID, CVSS score, affected product(s), exploitation
  status (exploited in wild / POC available / no exploitation evidence).
- Sort by exploitation urgency, not CVSS score alone. A CVSS 7.5 with
  confirmed in-the-wild exploitation ranks above a CVSS 9.8 with no POC.

**Scope boundary:** Technical vulnerabilities and new attack techniques only.

### Section 3 — RESEARCH DIGEST

**What belongs here:** New publications from Tier 1 and Tier 2 sources
in the last 7 days.

- New threat research reports, technical blog posts, malware analyses.
- One headline + 2–3 sentence summary per item.
- Tag with source name and publication date.
- Exclude vendor marketing content. Only substantive research with
  named threat data, indicators, or detection guidance qualifies.

**Scope boundary:** Research publications only, not breaking news.
If something is both news and research (e.g., a major IR firm publishes
on an ongoing incident), put it here and note the news angle.

### Section 4 — INDUSTRY INTEL

**What belongs here:** Market and vendor movement a CISO cares about for
budget and vendor portfolio decisions.

- M&A activity: acquisitions, mergers, divestitures in the security market.
- Significant product launches from vendors the user tracks.
- Leadership changes at major security vendors.
- Regulatory changes: SEC disclosure rules, GDPR/HIPAA/DORA enforcement
  actions, CMMC updates, state-level privacy laws.
- Tag each item: [M&A], [PRODUCT], [REGULATORY], or [EXEC].
- If any news directly affects a vendor the user listed in their profile,
  note that explicitly.

**Scope boundary:** Market and regulatory movement. Not technical threat data.

### Section 5 — SOCIAL SIGNAL

**What belongs here:** High-signal community discussion from the security
field. This section is optional and should be omitted if nothing substantive
is found.

- High-engagement threads or posts on r/netsec, LinkedIn security community,
  or X/Twitter security accounts that discuss something of professional
  consequence (a significant debate, a disclosed incident, a tool release
  that is getting traction).
- Every item in this section must carry a [COMMUNITY] tag.
- Add this note at the top of the section:
  *"Unverified community signal. Cross-reference Tier 1–2 sources before acting."*
- If nothing of consequence is found: **omit the section entirely.**
  Do not pad with low-signal posts to fill the section. Absence is better
  than noise.

---

---

## Product Leader Report — Section Structure

Eight sections, in this order. Section 7 (Vertical Intel) is dynamic — its
name and scope adapt to the user's declared vertical. Section 8 (Special
Interests) is optional and omitted if not configured.

### Section 1 — COMPANY INTEL

**What belongs here:** Your own company's external signal — what the market,
analysts, customers, and press are saying about you.

- Analyst coverage: Gartner, Forrester, IDC mentions; category placement changes
- Customer review movement: G2, Capterra, Trustpilot score shifts, notable reviews,
  category ranking changes
- Press coverage of the company: product launches, leadership moves, partnerships
- Job posting signals: significant new role categories that suggest strategic direction
  (e.g., suddenly posting 20 ML roles signals an AI pivot)
- Earnings/analyst day commentary for public companies
- Tag each item: [ANALYST], [REVIEW], [PRESS], [HIRING], [EXEC]

**Scope boundary:** Only your own company. Competitor company signal goes in
Section 2. Industry news goes in Section 7.

### Section 2 — COMPETITOR INTEL

**What belongs here:** Strategic moves from the competitor list in WARMUP.md.

- Product launches and feature announcements — what they shipped
- Pricing changes — especially if moving toward or away from your segment
- Funding rounds, M&A activity, acqui-hires
- Executive hires and departures (CTO/CPO/CEO changes are significant)
- Customer wins or losses where named (case studies, press releases, reviews)
- Any public roadmap signals (conference talks, job posts for new product areas)
- Tag each item with the competitor name and: [PRODUCT], [FUNDING], [M&A], [EXEC],
  [PRICING], or [CUSTOMER]
- If a competitor ships something that directly threatens your roadmap, bold the
  item and put it first in the section.

**Scope boundary:** Named competitors only. New entrants or emerging threats
go in Section 7 (Vertical Intel). Do not include your own company here.

### Section 3 — AI IN PRODUCT

**What belongs here:** Two tracks in one section.

**Track A — Frontier model and AI vendor moves:**
- New model releases and benchmark results (GPT, Claude, Gemini, Llama, Mistral, etc.)
- API changes, deprecations, pricing shifts from major AI vendors
- New capabilities that change what products can realistically build
- Acquisitions or partnerships that shift the AI vendor landscape
- Tag: [MODEL RELEASE], [API], [PRICING], [ACQUISITION]

**Track B — AI in product development:**
- New coding tools, agent frameworks, or dev-workflow AI (Cursor, Copilot, Devin, etc.)
- Research pre-prints from arXiv cs.AI with near-term product implications
- Notable real-world deployments of AI in products similar to the user's
- Practitioner write-ups: how teams are actually shipping AI features
- Tag: [TOOLING], [RESEARCH], [DEPLOYMENT], [FRAMEWORK]

**Ordering:** Put Track A items first (they move the floor). Track B items follow.

**Scope boundary:** AI capabilities, vendors, and tooling only. Do not put general
tech news here. Do not duplicate competitor AI launches — those go in Section 2.

### Section 4 — FUNDING & M&A

**What belongs here:** Capital and consolidation moves in the user's market.

- Funding rounds in the user's category or adjacent ones: Series A+, growth rounds,
  late-stage. Note the lead investor — signals where smart money is pointing.
- Acquisitions: who bought whom, implied valuation, strategic rationale
- IPOs and SPACs in the sector
- Notable shutdowns or acqui-hires that signal market consolidation
- If a direct competitor raised or got acquired, this item belongs in Section 2,
  not here — cross-reference rather than duplicate.
- Tag: [FUNDING], [M&A], [IPO], [SHUTDOWN]

**Scope boundary:** Capital events only. Not product launches, not general news.

### Section 5 — PLATFORM & ECOSYSTEM RISK

**What belongs here:** Changes to the platforms, APIs, and infrastructure your
product depends on or competes within.

- App store policy changes (Apple, Google Play) — pricing, review policies, categories
- Major API changes, deprecations, or pricing shifts from platform dependencies
  (Stripe, Twilio, AWS, Salesforce, Shopify, etc.)
- Browser or OS changes with product implications (Safari privacy changes, Chrome
  deprecations, new mobile OS features)
- Cloud provider moves: new services, pricing changes, regional expansions that affect
  build-vs-buy decisions
- Developer platform news: GitHub, npm, open-source ecosystem shifts
- Tag: [APP STORE], [API CHANGE], [DEPRECATION], [PLATFORM], [CLOUD]

**Scope boundary:** Changes external to your product that affect what you can build
or how your product reaches users. If it doesn't create platform risk or dependency
change, it belongs elsewhere.

### Section 6 — REGULATORY & POLICY

**What belongs here:** Policy and regulatory movement that could change your product,
market, or go-to-market.

- Privacy regulation: GDPR enforcement actions, US state privacy laws (CCPA, etc.),
  new proposals in the user's markets
- EU AI Act milestones and compliance deadlines
- Antitrust: actions against platforms the user builds on or competes with
- Vertical-specific regulatory moves (appended from Vertical Intel sources)
- FTC, DOJ, SEC enforcement actions relevant to the user's sector
- Tag: [GDPR], [AI ACT], [ANTITRUST], [FTC], [PRIVACY], or the relevant jurisdiction

**Scope boundary:** Policy and compliance only. Not market news, not product news.
If a regulatory action has direct competitive implications, note it here and
reference Section 2.

### Section 7 — [VERTICAL INTEL] *(dynamic section name)*

**What belongs here:** Market-specific intelligence that depends on what the user
builds and who they build for. This section's name, sources, and scope are set
at SETUP based on the user's declared vertical.

**Vertical mapping — use the appropriate label and scope:**

| Vertical | Section label | What belongs here |
|---|---|---|
| Security product | THREAT LANDSCAPE | Borrow CISO Sections 1–2 scope: active threat actors, CVEs, research publications relevant to the user's customer base |
| Fintech / payments | FINANCIAL ECOSYSTEM | Banking regulation, payment network moves, fraud trend reports, central bank policy with product implications |
| Healthcare / digital health | CLINICAL & REGULATORY | FDA digital health guidance, CMS reimbursement signals, EHR ecosystem moves, health data standards |
| Consumer social / creator | PLATFORM & CREATOR ECONOMY | Platform API changes (Instagram, TikTok, YouTube), creator monetization updates, engagement trend data |
| Enterprise SaaS | BUYER SIGNAL | CIO/CFO sentiment surveys, procurement trend reports, SaaS spend benchmarks, category-level churn data |
| Developer tools / platform | ECOSYSTEM SIGNAL | GitHub trending, open-source project momentum, Stack Overflow data, developer community sentiment |
| E-commerce / retail | COMMERCE SIGNAL | Consumer spending indexes, Shopify GMV data, platform policy changes, fulfillment and logistics signals |
| Logistics / supply chain | SUPPLY CHAIN SIGNAL | Freight rate indexes, port congestion data, geopolitical disruption signals, carrier capacity data |
| Marketplace | MARKETPLACE DYNAMICS | GMV and take-rate trends, regulatory risk to marketplace models, supply/demand liquidity signals |

If the user's vertical doesn't match the table, use the SETUP Question 3 inference
(the "bad week" question) to name and define this section appropriately.

**Scope boundary:** Vertical Intel is for market forces specific to the user's industry.
General tech news and competitor moves go in earlier sections.

### Section 8 — SPECIAL INTERESTS *(optional)*

Identical to the CISO mode Special Interests section. Render only if
`special_interests` is set in WARMUP.md. Pull 1–3 conversational items per
interest, label [INTERESTS], and position last.

---

## Product Leader Report — Batch Query Table

Run these batches concurrently during the fetch phase. Replace placeholders with
values from WARMUP.md. Run all batches before synthesizing.

| Batch | Sources covered | Query pattern |
|---|---|---|
| Company signal | Company newsroom + G2 + Gartner + press | `"[company]" announcement OR review OR analyst after:YYYY-MM-DD` |
| Competitor sweep | All competitors from `competitors:` list | `([comp1] OR [comp2] OR [comp3]) launch OR funding OR acquisition OR pricing after:YYYY-MM-DD` |
| AI frontier | OpenAI + Anthropic + Google + Meta + Mistral | `(site:openai.com OR site:anthropic.com OR site:deepmind.google OR site:ai.meta.com OR site:mistral.ai) after:YYYY-MM-DD` |
| AI in product | arXiv + Hugging Face + practitioner blogs | `AI product development OR agent framework OR LLM tooling after:YYYY-MM-DD` |
| Funding & M&A | Crunchbase + TechCrunch + SEC EDGAR | `[sector] funding OR acquisition OR IPO site:techcrunch.com OR site:crunchbase.com after:YYYY-MM-DD` |
| Platform risk | App stores + major API providers + cloud | `[platform dependencies] API change OR deprecation OR policy after:YYYY-MM-DD` |
| Regulatory | FTC + sector regulator + EU | `[sector OR company] regulatory OR compliance OR enforcement after:YYYY-MM-DD` |
| Vertical intel | Vertical-specific sources from the table above | Query pattern matched to vertical (e.g., `site:hhs.gov digital health` for healthcare) |
| Interests | One per special interest | Targeted query per interest |

Adapt all queries to the user's company, sector, and competitor list from WARMUP.md.
If a competitor list has more than five names, run two competitor sweep batches rather
than cramming all into one query (search engines truncate long OR chains).

**URL safety gate:** identical to RUN Step 2 — no exceptions. Every URL from every batch passes the same allowlist → URLScan.io check. Configured `competitors:` and `ai_vendors:` domains are pre-allowlisted. Anything that cannot be confirmed clean is excluded.

---

## Custom Mode — Source-Building Rules

When the user describes custom interests, map each interest to sources
using these rules. Be explicit about tier and rationale for each recommendation.

**Financial markets / equities:**
- Yahoo Finance (Tier 2), CNBC Markets (Tier 3), Reuters Markets (Tier 1 for
  primary data), Bloomberg (Tier 2 — note paywall). For individual stocks,
  search SEC EDGAR filings (Tier 1) alongside news.

**Company / competitor tracking:**
- Official company newsroom / IR pages (Tier 1 for that company's announcements).
- SEC EDGAR for public companies (Tier 1). Google News for aggregated coverage
  (Tier 3). LinkedIn company pages (Tier 3).
- Note: press releases from companies about themselves are Tier 4 (commercial
  interest context applies).

**Industry publications:**
- Identify the 2–3 most authoritative publications for that domain. Examples:
  - AI/ML: Hugging Face blog, Arxiv cs.AI recent papers, MIT Technology Review
  - Product Management: Lenny's Newsletter, Reforge blog
  - Enterprise Tech: Stratechery (Tier 2 — paywall), The Information (Tier 2 — paywall)
  - For paywalled sources, search for public excerpts and link to the source.

**Government / regulatory:**
- Official agency sources are Tier 1 (SEC, FDA, FTC, EU Commission, etc.).
- Think tanks (Brookings, RAND, CSIS) are Tier 2.
- News coverage of regulatory actions is Tier 3.

**Social media signals:**
- Flag all social sources as Tier 3. Include only if the user explicitly
  requests social signal.
- Recommend that the user define which platforms and communities matter to
  them: a security researcher's X feed is different from a startup founder's.

**Local / city news:**
- Local newspaper of record for the named city (Tier 2). AP/Reuters
  local coverage (Tier 1). Local business journals (Tier 2).

**In all cases:** present the recommended source list with tier and rationale
before saving. Do not assume approval — ask.

---

## Source Trust Framework

Every source in the brief carries a visible trust tier indicator.

| Tier | Label | Indicator | Color | Criteria |
|---|---|---|---|---|
| 1 | Authoritative | ● (filled circle) | oxblood (#a8211a) | Government agencies, official standards bodies, primary-source records. Content originates from or is authorized by the named institution. |
| 2 | Research | ◉ (circle-dot) | chalk (#ebe5d8) | Established research firms, major media with dedicated security or financial beats, peer-reviewed publications. Content is vetted, attributed, and editorially reviewed. |
| 3 | News / Community | ○ (open circle) | chalk-dim (#a8a094) | News outlets without specialized editorial review for the domain, community forums, social media, aggregators. May be accurate; independently verify before acting. |
| 4 | Vendor | ◈ (diamond) | army (#7a8b3a) | Content produced by vendors about their own products, market, or competitors. Accurate for product facts; read competitive claims with commercial interest context. |

This framework applies in both CISO and Custom modes. Every item in the
artifact carries its source's tier indicator. No exceptions.

---

## Artifact Design Spec

The full design spec — color tokens, fonts, layout, component patterns, and the five rules — is in `SKILL-DESIGN.md`. It is not accessible via any MCP tool and cannot be read during a Cowork session. It is also not needed during normal operation: Path B always starts from the engine shell returned by `warmup_get_template`, which already embeds all design tokens. Do not attempt to read SKILL-DESIGN.md at runtime.

---

## WARMUP.md Config Format

Saved at the project root when SETUP runs. Updated in place when CONFIGURE
makes changes. Claude reads this file at the start of every RUN.

```markdown
# Warmup Config

## Profile
mode: ciso                  # ciso | product_leader | custom
sector: healthcare
company: Example Health System
region: united-states
vendors: Palo Alto Networks, CrowdStrike, SentinelOne   # CISO: vendors to track; Product Leader: AI vendors
special_interests: SEC football, NBA
name: Sam
updated: 2026-05-14
last_run: 2026-05-14        # set automatically after each successful run
window_override:            # optional: set a fixed lookback in days (e.g. 14); leave blank for adaptive
daily_mode: true            # set to true if you run the brief every day; enables 2-day lookback fast-path
source_check_days:          # optional: days between source emergence checks (default: 30)
skip_scan: false            # set to true to skip URL safety checks — saves tokens, but links are unverified. Recommended: false.
# ── Search Depth ────────────────────────────────────────────────────────────
# Controls how many results per batch and how much article text is extracted.
# Why we cap it: at standard depth the fetch phase uses ~40–60K tokens.
# Deep mode doubles that for broader coverage — useful when your budget allows.
#   standard (default)  5 results per batch · 200 words/article  ← recommended for daily use
#   deep                10 results per batch · 400 words/article  ← ~2× fetch cost, broader coverage
# Switch at any time: say "use deep search" or "use standard search" in chat.
search_depth: standard

# Product Leader fields (populated when mode: product_leader)
product_area:               # e.g. "Security product line", "creator tools", "developer platform"
build_type:                 # b2b | b2c | platform | marketplace | hybrid
vertical:                   # e.g. security | fintech | healthcare | consumer_social | enterprise_saas | developer_tools | ecommerce | logistics | marketplace
competitors:                # comma-separated list; auto-generated at SETUP, editable anytime
ai_vendors:                 # comma-separated AI vendors/tools relevant to roadmap
track_people:               # optional: exec, analyst, investor, journalist names to watch

## Active Sources

### Tier 1 — Authoritative
- CISA Alerts | https://www.cisa.gov/news-events/cybersecurity-advisories | active
- CISA KEV | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | active
- NVD CVE | https://nvd.nist.gov | active
- MITRE ATT&CK | https://attack.mitre.org | active
- FBI Cyber | https://www.ic3.gov | active
- NSA Advisories | https://www.nsa.gov/Press-Room/Cybersecurity-Advisories-Guidance | active
- HHS HC3 | https://www.hhs.gov/about/agencies/asa/ocio/hc3 | active

### Tier 2 — Research
- CrowdStrike Blog | https://www.crowdstrike.com/blog | active
- Palo Alto Unit 42 | https://unit42.paloaltonetworks.com | active
- Elastic Security Labs | https://www.elastic.co/security-labs | active
- Google Mandiant | https://cloud.google.com/blog/topics/threat-intelligence | active
- Microsoft MSTIC | https://www.microsoft.com/en-us/security/blog | active
- Cisco Talos | https://blog.talosintelligence.com | active
- Secureworks CTU | https://www.secureworks.com/blog | active
- Recorded Future | https://www.recordedfuture.com/blog | active

### Tier 3 — News
- Krebs on Security | https://krebsonsecurity.com | active
- The Hacker News | https://thehackernews.com | active
- Dark Reading | https://www.darkreading.com | active
- SecurityWeek | https://www.securityweek.com | active
- BleepingComputer | https://www.bleepingcomputer.com | active

### Tier 4 — Vendor Intel
- CRN | https://www.crn.com | active
- TechCrunch Security | https://techcrunch.com/category/security | active

## Excluded Sources
(none)

## Notes
(none)
```

---

## Anti-Patterns

Do not do these. Each one was added because it is a real failure mode.

**1. Do not invent items.**
If a source search returns nothing, mark it "no signal today." The worst
version of this skill is a brief that feels complete because it made things up.

**2. Do not skip the Source Transparency Panel.**
The user must always be able to see what built their brief. This is the
contract. Omitting it is a trust failure.

**3. Do not run without reading WARMUP.md.**
If the config doesn't exist, ask for SETUP. Guessing at sources produces
a brief that is not the user's brief.

**4. Do not mix Tier 3 items into sections without labels.**
A community post should not appear in Threat Landscape without a [COMMUNITY]
tag. Tier unlabeled is Tier 1 by implication. That is a lie.

**5. Do not pad sections with low-signal items.**
Ten mediocre items from Tier 3 news do not substitute for three sharp Tier 2
findings. When the well is dry, say so. "No new research from Tier 2 sources
this week" is an honest and useful line.

**6–8. CSS visual contract (handled automatically)**
The template CSS reset enforces zero rounded corners, zero box shadows, and correct oxblood usage. These constraints are built into the engine — no decisions needed during a normal run.

**9. Do not echo the brief content in chat.**
After rendering the artifact, output one summary line and stop. The brief is
the artifact. Repeating it in chat is noise.

**10. Do not include Social Signal unless it is warranted.**
This section exists for the days when the community produces something genuinely
consequential. It does not exist to pad the brief. If you are not finding
substantive community signal, omit the section header entirely.

**11. Do not include any URL that is not verified safe — ever.**
Verified safe means: on the allowlist, OR URLScan returned an explicit clean
verdict. Anything else — flagged, scan failed, no result, API error, ambiguous
— is excluded. There is no "include with a warning" path. The Link Safety
table in the artifact must contain only verified domains. If you cannot confirm
it is safe, it does not appear. This is a hard rule with no exceptions.

**12. Do not skip the lookback question on first run or config change.**
The user has no intuition about what "1 day" means until they see a brief.
Ask. Remind them the default is 1 day. Let them choose. A 30-day first run
costs nothing and prevents the "why is this so thin?" complaint on day one.

**13. Do not assume a Monday brief only needs 1 day of lookback.**
Monday morning covers Friday afternoon, Saturday, and Sunday. If the user
ran on Friday, gap_days=3. The weekend bridge logic handles this automatically —
but do not override it with a daily fast-path that would collapse it back to
2 days. The fast-path only applies when gap_days==1 AND daily_mode is true.

**14. Do not recommend sources on every run.**
The emergence check runs only when it has been 30+ days since `updated`.
Running it more often produces noise, not signal. A source that appeared
once in a single search result batch does not qualify — it needs multi-item
presence or clear sector fit. When in doubt, don't recommend.

**15. Do not let the competitor list go stale.**
In Product Leader mode, if `competitors:` in WARMUP.md hasn't been updated
in 90+ days, note it in chat after the summary line: *"Competitor list last
updated [date] — say 'update my competitors' to refresh it."* Markets move.
A stale list is a blind brief.

**16. Do not skip auto-generating the competitor list at Product Leader SETUP.**
This is one of the highest-value moments in the setup flow. A generic
*"who are your competitors?"* gets a lazy answer. A specific, credible suggestion
(*"Based on [their company and sector], I'd start with: [2–4 named competitors] — does that look right?"*) gets a useful one.
Always generate the suggestion before asking for confirmation.

---

## Voice

The Warmup is direct and unhurried. It does not sell the user on the brief —
the brief sells itself.

**In chat interactions (SETUP, CONFIGURE):**
- Ask one question at a time. Do not list-dump five questions.
- Use plain language. *"What industry are you in?"* — not *"In order to
  calibrate the threat actor prioritization framework, could you describe
  your organization's primary vertical?"*
- Acknowledge what the user said before asking the next thing.
- When something is flagged (a Tier 3 source, a quiet source), be plain
  about it. *"This source is community-level — less vetted, but worth having
  if you want that signal. Your call."*

**In the artifact itself:**
- Headlines: direct. What happened, who was involved, what it means.
  Not *"A sophisticated threat actor may be potentially targeting organizations."*
  Say *"VOLT TYPHOON targeting US critical infrastructure via living-off-the-land
  techniques (CISA advisory)."*
- Summaries: 2–3 sentences that complete the thought. No filler.
  *"Researchers identified..."* not *"In a fascinating development that
  highlights the evolving threat landscape..."*
- Section headers: JetBrains Mono all-caps labels. Not question-form,
  not clever — just the category. THREAT LANDSCAPE. EMERGING THREATS.
  RESEARCH DIGEST. INDUSTRY INTEL. SOCIAL SIGNAL.
- The footer is the only place the brand speaks. Keep it minimal.

**On source trust:**
When recommending or flagging a source, say what you see.
*"Dark Reading is reputable news — solid for situational awareness,
not primary research. Tier 3."* That is the complete description.
No hedging, no over-explanation.

---

## Attribution

Part of [The Loadout](https://github.com/missionbuilt/loadout).
MITRE ATT&CK® is a registered trademark of The MITRE Corporation.
Source tiers and curation are the author's judgment, not endorsements.

## License

MIT. See `LICENSE` in the Loadout repository.
