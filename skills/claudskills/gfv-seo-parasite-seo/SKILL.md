---
name: parasite-seo
description: When the user wants to choose or execute third-party platform SEO (high-authority sites for rankings or backlinks). Also use when the user mentions "parasite SEO," "parasitic SEO," "barnacle SEO," "hosted content," "third-party publishing," "Medium SEO," "Reddit SEO," "GitHub parasite SEO," "LinkedIn Pulse SEO," "high-authority platforms," "distributed authority," "borrow domain authority," or "rank without own website." For GitHub-specific playbooks, use github. For Medium.com posts, use medium-posts. For Grokipedia, use grokipedia-recommendations. For AI answer-engine visibility (not platform selection), use generative-engine-optimization.
  Use when: The executive requests execution of this domain.
  Skip when: The task is outside the scope of this module.
metadata:
  version: 1.1.0
---


> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure. Follow these conventions.

### GFV Infrastructure Integration

**Credentials** — Never use `.env` files. All secrets live in macOS Keychain:
```bash
security find-generic-password -s "<service>" -a "<account>" -w
```
Check `~/Documents/Code/gfv-brain/scripts/pil_config.py` for service mappings.

**Data Sources** — Before querying external APIs, check PIL first:
- `search_pil` / `smart_search` / `vector_search` MCP tools (491K+ embeddings, 81K entities)
- Supabase tables: `entity_embeddings`, `ont_entities`, `ont_facts`
- Local SQLite: WhatsApp (59K msgs), Slack (2.5K msgs), `gfv_memory.db`

**Output** — Save results to `~/Documents/Code/gfv-brain/` or PIL via Supabase. Never send external messages (email, Slack, WhatsApp) without the Executive's explicit "send it" approval.

**Active Clients**:
- **GetFresh Ventures** — Venture studio: getfreshventures.com

---



# SEO: Parasite SEO

Guides parasite SEO (also "barnacle SEO")—publishing optimized content on high-authority third-party platforms (Medium, Reddit, LinkedIn, Grokipedia, etc.) to leverage their domain strength for rankings and backlinks, bypassing the need to build your own site's authority from scratch.

**When invoking**: On **first use**, if helpful, open with 1–2 sentences on what this skill covers and why it matters, then provide the main output. On **subsequent use** or when the user asks to skip, go directly to the main output.

## What Is Parasite SEO

**Parasite SEO** = Placing content on high-authority platforms to leverage their domain strength for rankings and AI citation. Part of "Distributed Authority Engineering."

Instead of waiting months for your own domain to gain trust, you publish on established platforms that Google already trusts. Content can rank on page one within days rather than months because Google crawls these platforms frequently and inherits their domain trust.

**Best for**: Beginners testing niches; local businesses needing quick leads; demand validation; supplementing traditional SEO.

## Why It Works

| Factor | Effect |
|--------|--------|
| **Domain authority** | Platforms (DA 90+) rank faster than new sites |
| **Crawl frequency** | Google crawls Reddit, Medium, LinkedIn often |
| **AI citation** | ChatGPT, Perplexity cite Reddit, Quora, wikis |
| **UGC preference** | Algorithm updates favor UGC platforms as trustworthy |
| **Technical foundation** | High-authority sites have strong technical SEO, fast load, good UX |

## Platform Tiers

*Platform examples are illustrative only. No endorsement implied.*

| Tier | Platform type | Examples | GEO / AI citation |
|------|---------------|----------|-------------------|
| **Tier 1** | GEO authority | Medium, Reddit, LinkedIn Articles, Quora | Very high |
| **Tier 2** | Technical authority | GitHub, Stack Overflow, Dev.to | High; expertise signals |
| **Tier 3–6** | Controlled / entity / wiki | WordPress.com, Blogger, HN, Grokipedia | Varies |

### Platform Notes

| Platform | Use case | Notes |
|----------|----------|-------|
| **LinkedIn Pulse** | B2B, agencies, professional content | Keywords in headlines; often ranks above corporate blogs |
| **Medium** | How-to, thought leadership | Use canonical link if reposting; storytelling works |
| **Reddit** | Product reviews, alternatives, discussions | Comprehensive guides; upvoted threads rank well |
| **Quora** | Q&A, long-tail informational | Answer industry questions; link to resources naturally |
| **YouTube** | Video search, how-to, reviews | Titles, descriptions, tags; watch time matters |
| **GitHub** | Repos, README, Pages, gists, awesome lists | Tier 2 technical authority; very high AI citation; see **github** |
| **Grokipedia** | AI encyclopedia | See **grokipedia-recommendations** for contribution flow |
| **Free web builders** | WordPress.com, Wix | Indexable content; lower authority than above |

## Keyword & Content Strategy

| Element | Practice |
|---------|----------|
| **Keyword targeting** | Intent-driven; mid-competition and long-tail; clear monetization potential |
| **Content depth** | 1,500+ words for competitive keywords; comprehensive coverage |
| **Keyword placement** | Primary keyword in title and first 100 words; headers, subheadings, body |
| **Semantic relevance** | Natural language; avoid keyword stuffing |
| **Content clustering** | Create clusters around topics; link related articles within platform |

## On-Page Optimization

| Element | Practice |
|---------|----------|
| **Title** | Target keyword; platform + search-optimized |
| **Meta / description** | Where allowed; keyword usage |
| **Internal links** | Link to other parasite content on same platform |
| **Visuals** | Images, infographics, videos improve engagement |
| **CTA** | Strong, relevant call-to-action |

## Link Building Through Parasite SEO

| Tactic | Purpose |
|--------|---------|
| **Tier-2 backlinks** | Build links from Web 2.0s, guest posts pointing to your parasite content |
| **Strategic linking** | Link from parasite content to owned site; natural, not spammed |
| **Cross-platform linking** | Link related content across platforms; network effect |

## Advanced Techniques

| Technique | Use |
|-----------|-----|
| **Content clustering** | Multiple related articles on same platform; topical authority |
| **Cross-platform syndication** | Adapt core content per platform; different keywords; avoid duplicate content |
| **Keyword layering** | Multiple related keywords in one piece; maximize ranking potential |

## Risks & Compliance

| Risk | Mitigation |
|------|------------|
| **Google Site Reputation Abuse (2024)** | Targets manipulative third-party content. Ensure genuinely useful content; not purely for link/mention manipulation. |
| **Platform bans** | Spammy, promotional content gets removed; accounts suspended |
| **Duplicate content** | Use canonical when republishing; avoid thin content |
| **Over-optimization** | Prioritize user value over aggressive optimization |

## Common Mistakes

| Mistake | Avoid |
|---------|-------|
| **Quality neglect** | Low-quality, thin content doesn't sustain; harms SEO |
| **Policy violations** | Check platform guidelines; adhere to policies |
| **Short-term tactics** | Build sustainable relationships; create value consistently |

## Output Format

- **Platform selection** (match to intent and audience)
- **Keyword strategy** (intent, long-tail, placement)
- **Content structure** (depth, clustering, per-platform format)
- **Link strategy** (tier-2, cross-platform, owned property)
- **Related platform skills** (reddit-posts, grokipedia-recommendations, etc.)

## Related Skills

- **github**: GitHub for parasite SEO; repos, README, Pages, gists, awesome lists
- **grokipedia-recommendations**: Add recommendations/links to Grokipedia; parasite SEO + GEO
- **reddit-posts**: Reddit post copy; high-authority community for parasite SEO
- **medium-posts**: Medium publishing; parasite SEO; canonical setup
- **generative-engine-optimization**: GEO strategy; parasite SEO complements AI citation
- **link-building**: Parasite SEO as link acquisition tactic; tier-2 backlinks
- **directory-submission**: Directory and curated list submission; similar placement logic
- **community-forum**: Forum and community promotion; HN, Indie Hacker
- **indie-hacker-strategy**: Indie hacker growth; Indie Hackers, Reddit as channels
- **seo-strategy**: SEO workflow; parasite SEO as alternative strategy



## When to Trigger
- When requested by the Executive.
- When the task aligns with the core competency of this skill.

## When to Skip
- When the data or answers already exist in the PIL memory bus.
- When the task requires physical intervention or manual approval before drafting.

## GFV Integration
**Credentials** — Never use `.env` files. All secrets live in macOS Keychain:
`security find-generic-password -s "<service>" -a "<account>" -w`
**Data Sources** — Before querying external APIs, check PIL first (`search_pil`, `gfv_memory.db`).
**Output** — Save results to `~/Documents/Code/gfv-brain/`. Never send external messages without the Executive`s explicit "send it" approval.

## Anti-Patterns
- **Summarizing instead of resolving**: Do not just summarize what needs to be done. Do the work.
- **Bypassing the Gate**: Do not execute risky actions without human-in-the-loop validation.

## References
- **GFV Standard**: GetFresh Ventures Growth by Design CEO AI Kit Architecture

<verification_gate>
# Delivery Gate

STOP AND VERIFY BEFORE DECLARING THIS TASK COMPLETE.

1. Did you verify that the execution meets all documented requirements safely?
2. Ensure you have not bypassed any "requires_human_approval" constraints.
</verification_gate>

<!-- Original Community Author: kostja94 -->

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
