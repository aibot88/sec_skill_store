---
name: aso-toolkit
description: >
  ASO frameworks for generating, auditing, and optimising App Store and Google
  Play marketing copy. Covers keyword research, metadata optimisation across
  every field, competitor analysis, and audit scoring. Run this whenever
  authoring or refining store text for any app — /store-spec consults it for
  every copy field. Inspired by Eronred's open-source aso-skills toolkit;
  optionally pairs with the Appeeky MCP for live App Store data.
---

# ASO Toolkit — Frameworks for store-text generation

This skill is the **content brain**. It tells you how to think about an ASO
text problem — what to research, what to write, how to score it. The
**field-level rules** (character limits, indexing weights, banned words)
live in the platform-specific skills:

- `ios-store-requirements` — App Store Connect specs and policy
- `android-store-requirements` — Google Play Console specs and policy

`/store-spec` orchestrates: it reads the spec, uses *this* skill for the
generation frameworks, and the platform skills for the field rules.

---

## When to use

- Authoring a new `spec.yaml` (`/store-spec`) — for the iOS + Android copy blocks
- Refining existing copy without re-rendering screenshots
- Auditing a competitor's listing or your own current store page
- Picking keywords before writing copy
- Localising copy for a new market
- Preparing PPO / store-listing-experiment variants

---

## Capabilities (sub-tasks)

This skill bundles four frameworks that work together. You can run them
individually or as a pipeline.

| Capability | Purpose | Output |
|------------|---------|--------|
| **Keyword research** | Find the terms users actually search | Tiered keyword list (primary / secondary / long-tail) |
| **Metadata optimisation** | Author every text field with hierarchy + variants | 3 variants per field with char-counted output |
| **Competitor analysis** | Steal what works; identify gaps | Keyword-gap table + positioning notes |
| **ASO audit** | Score an existing listing | 10-factor scorecard with prioritised fixes |

---

## 1. Keyword research framework

A keyword's value = `searchVolume × relevance ÷ difficulty`. Without live
data the agent estimates these qualitatively, then upgrades the estimate
when an Appeeky-style data source is connected.

**Tiering:**

| Tier | Description | Where it goes |
|------|-------------|---------------|
| **Primary** (1–2 terms) | Highest-intent + highest-relevance + reasonable competition. The terms a user would type if they wanted exactly this app. | iOS App Name, Play Title |
| **Secondary** (3–6 terms) | High relevance, often combined with the primary in compound queries ("mortgage calculator with chart"). | iOS Subtitle, Play Short Description |
| **Long-tail** (10+ terms) | Lower-volume specific phrases. Easier to rank for; convert better. | iOS Keyword Field, Play Full Description body |

**Process when no live data is available:**

1. Read `aso.positioning` + `app.category` + the app's actual core function.
2. Brainstorm 25–40 candidate terms across user-jobs ("how do I…"),
   product-categories ("mortgage calculator"), and outcomes
   ("save on car loan"). Write each as something a user would type.
3. Group into tiers using the heuristics:
   - Primary: 1–3 words, exactly matches the core job
   - Secondary: 2–4 words, modifies the core job (with a feature, audience, comparator)
   - Long-tail: 4+ words, specific intent or scenario
4. Write the tiered list into `spec.yaml` `aso.primary_keywords` /
   `aso.secondary_keywords`. Long-tail lives only in the description body.

**With Appeeky (or equivalent live data) connected:**

For each candidate, fetch search volume + difficulty + your app's current
rank. Sort by `volume × (1 − difficulty/10) × relevance`. Drop terms with
volume < 10 or difficulty > 8 unless they're brand-defensive (your own name).

**Banned words and phrases (verify against platform skills):**

- Google Play title/icon/dev-name banned: "free", "best", "top", "#1",
  "sale", "no ads", "ad free", "download now", "update". See
  `android-store-requirements` §9.
- Apple uses general "accurate metadata" enforcement rather than a fixed
  ban list. See `ios-store-requirements` §8.

---

## 2. Metadata optimisation framework

For every field, generate **3 variants** with explicit framing differences.
The user picks one or runs a PPO/Play experiment with multiple. Char counts
must be inline so the user sees fit at a glance.

### iOS App Store

#### App Name (30 chars)

Format: `{Brand} {Primary keyword phrase}`

Three framing axes:

1. **Brand-led** — `Coin: Mortgage Calculator`
2. **Function-led** — `Mortgage & Loan Calculator`
3. **Outcome-led** — `Loan Math: Mortgage & Cars`

Constraints (per `ios-store-requirements` §3): brand + ONE primary keyword;
highest-weight field; **never** repeat any word in Subtitle or Keyword Field.

#### Subtitle (30 chars)

Three angles, none repeating words from the Name:

1. **Secondary keywords combined** — `Home + auto loan affordability`
2. **Outcome-promise** — `See interest before you sign`
3. **Audience cue** — `For first-home buyers`

#### Keyword Field (100 chars, comma-separated, no spaces)

Pack with long-tail terms not yet in Name or Subtitle. Apple deduplicates,
so repeats waste your budget. Order doesn't matter.

```
home loan,car loan,refinance,interest rate,monthly payment,amortization,affordability,first time buyer
```

Always validate: total length ≤ 100, no word appearing in Name or Subtitle.

#### Description (4,000 chars, NOT indexed)

Pure conversion text. ~97% of visitors stop at the fold (~170 chars):

- **Line 1:** Plain-English what the app does and for whom
- **Line 2:** Top 2–3 differentiators or benefit bullets
- **Line 3:** Social proof signal *(only if real — see honesty rule below)*
- **Body:** feature bullets → use cases → trust signals → CTA

Three variants vary the **tone**: confident-helpful / playful-direct /
no-nonsense-functional.

#### Promotional Text (170 chars)

Updatable without resubmission. Use for time-sensitive messaging.

#### What's New (release notes, 4,000 chars, per locale)

Specific over generic. "Faster pie chart rendering and improved slider
sensitivity" beats "Performance improvements and bug fixes".

### Google Play

#### Title (30 chars)

Same shape as iOS App Name. Highest weight on Play.

#### Short Description (80 chars)

The single most important Play field you'll author. Indexed AND shown
directly in search results — must read as one compelling sentence AND
carry a keyword. Three variants vary on which **secondary keyword** is
woven in.

#### Full Description (4,000 chars)

NLP indexed end-to-end. Density target: top 2–3 keywords each at ~2–3% of
total chars, repeated naturally ~5× across the body. Structure:

```
Hook paragraph (with primary keyword)
→ Feature bullets (each starts with a benefit)
→ Use cases (with secondary keywords woven in)
→ Trust signals (factual only)
→ CTA
```

Plain text only. Line breaks + emoji bullets help scannability. Google's
NLP penalises stuffing — use keywords in meaningful sentences.

#### What's New / Recent Changes (500 chars per locale)

Specific. Not indexed for ranking — for users only.

### Universal honesty rule (recap)

Every claim in every field must be verifiable from explicit evidence in
the spec/config or user-provided context. Default to omission. See
`store-spec` SKILL.md "Honesty rule" for the full table; the canonical
anti-pattern is "No Ads" — never assume it; most free apps run ads.

---

## 3. Competitor analysis framework

Pick 3–5 direct competitors (same category, similar size). For each:

1. **Inventory their text fields** (Name, Subtitle, Title, Short Desc).
   What primary keyword do they own?
2. **Keyword gap** — terms they target that you don't, and vice versa.
3. **Positioning** — what's their one-line value prop? Is the market
   crowded around the same framing or is there an unclaimed angle?
4. **Creative teardown** — first three screenshots: what story arc, what
   keywords appear in captions?

Output a small table:

| Competitor | Primary kw | Secondary kw | Their angle | Gap I can fill |
|------------|------------|--------------|-------------|----------------|
| ...        | ...        | ...          | ...         | ...            |

When Appeeky / similar is connected, pull live keyword rankings to
quantify "they rank top-3 for X but you don't show up — go after X."

---

## 4. ASO audit scorecard

When auditing an existing listing, score each factor 0–10. Total / 100.

| Factor | What's good (8–10) | What's poor (0–3) |
|--------|--------------------|-------------------|
| 1. Name uses primary keyword | Brand + primary keyword fits in 30 | No keyword, just brand |
| 2. Subtitle uses secondary keywords | Different words from name; 2–3 secondaries | Repeats name words; vague |
| 3. Keyword field utilisation (iOS) | At/near 100 chars; no duplicates; long-tail | Half-empty; duplicates from name/subtitle |
| 4. Short Description (Play) keyword fit | Single compelling sentence with keyword | Generic tagline; no keyword |
| 5. Description fold | First 3 lines: what, who, why | Opens with app name or generic boilerplate |
| 6. Description body keyword density | ~2–3% top keywords, natural prose | 0% or stuffed |
| 7. Screenshot caption alignment | Captions reinforce primary keyword | Captions are decorative only |
| 8. First screenshot impact | Clear primary value prop, scannable in 1 sec | Cluttered or device-frame only |
| 9. Honesty | All claims verifiable; no fake social proof | Star ratings/counts not from real data |
| 10. Locales | Top 3 markets fully localised (text + screenshots) | English-only or auto-translated |

**Quick wins** = fix any factor scoring 0–3.
**High-impact changes** = move any 4–6 to 8+.
**Strategic** = big rewrites, only after experimenting.

---

## 5. Output templates (drop-in for spec.yaml)

When `/store-spec` calls this skill in copy-generation, the output should
flow directly into the spec.yaml fields. Use this YAML shape:

```yaml
aso:
  primary_keywords: [keyword one, keyword two]      # 1–2 terms
  secondary_keywords: [k3, k4, k5]                  # 3–6 terms
  positioning: "{one-sentence unique angle}"
  target_audience: "{from config or inferred}"

google_play:
  title: ""                  # 30
  short_description: ""      # 80
  full_description: |        # 4,000; ~2–3% density; 5× primary repetition
    ...
  recent_changes: ""         # 500; specific, not generic

app_store:
  name: ""                   # 30; brand + primary
  subtitle: ""               # 30; secondary; no name repeats
  description: |             # 4,000; first 3 lines = the fold
    ...
  keywords: ""               # 100; comma-separated, no spaces; no name/subtitle repeats
  promotional_text: ""       # 170; updatable
```

---

## 6. Live-data integration (optional)

This skill works standalone using the frameworks above and the agent's
ASO knowledge. For real-time App Store / Play data — keyword search
volumes, competitor metadata snapshots, ranking history, trending terms —
connect a data source via MCP:

**Appeeky MCP** (used by the source toolkit):

```jsonc
{
  "mcpServers": {
    "appeeky": {
      "url": "https://mcp.appeeky.com/mcp",
      "headers": { "Authorization": "Bearer apk_your_key_here" }
    }
  }
}
```

When connected, the toolkit can pull live keyword rankings, competitor
metadata, download estimates, trending terms, and featured-app lists. The
keyword research and competitor analysis frameworks above upgrade
seamlessly: qualitative estimates become quantitative.

**Eronred's open-source aso-skills toolkit** is a deeper companion if
you want the full 14-skill constellation (review-management, app-launch,
ua-campaign, monetization-strategy, retention-optimization, etc.):

- Repo: https://github.com/Eronred/aso-skills
- License: MIT
- Install: `npx skills add eronred/aso-skills`

This skill adapts its core ASO-text frameworks for the spec-generation
flow but stays focused — the broader marketing topics (UA, retention,
launch, monetisation) live in their toolkit.

---

## Cross-references

- `store-spec` — orchestrator; calls into this skill for copy generation
- `store-assets` — renders the output
- `ios-store-requirements` — App Store Connect field constraints
- `android-store-requirements` — Google Play field constraints

## Sources & further reading

- Eronred ASO Skills (MIT) — https://github.com/Eronred/aso-skills
- Appeeky API docs — https://docs.appeeky.com
- App Store search & ASO — see `ios-store-requirements`
- Google Play algorithm + NLP — see `android-store-requirements`
