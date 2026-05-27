---
name: super-geo-agent-readiness
description: Generative Engine Optimization plus agent readiness. Use this skill whenever the user asks about GEO, AEO, LLMO, optimizing content for AI search engines (ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, Copilot), getting cited by LLMs, brand mentions in AI responses, llms.txt, robots.txt for AI crawlers, Schema.org JSON-LD, FAST framework, agent readiness, MCP server discovery, Web Bot Auth, OAuth for agents, API Catalog, agentic commerce (x402, ACP, UCP), Markdown content negotiation, or auditing a site or page for AI visibility. Also trigger when the user says "AI SEO", asks how to "rank in ChatGPT", "show up in Perplexity", "appear in AI Overviews", or wants a site to "speak to AI agents". Trigger even when the request is implicit, such as "review this article so AI search picks it up" or "make our docs agent-friendly".
---

# Super GEO Agent Readiness

Generative Engine Optimization (GEO) plus agent readiness. One skill, four optimization surfaces: content, technical site, platform tactics, and the agent layer.

## What GEO is

Generative Engine Optimization is the practice of improving a brand's visibility, citation rate, and recommendation frequency inside AI-powered answer engines. SEO targeted blue links. GEO targets the answers themselves and the entities that LLMs choose to mention.

The boundary keeps growing. Sites are no longer optimized only for human readers and search crawlers. They are also optimized for AI agents that fetch, read, authenticate, transact, and act on behalf of users. This skill treats both as one continuous problem.

### GEO vs SEO vs AEO vs Agent Readiness

| Surface | Target | What gets optimized | Primary metric |
|---|---|---|---|
| SEO | Google, Bing | Keywords, links, technical SEO | Rankings, CTR |
| AEO | Voice assistants, featured snippets | Q&A format, structured data | Featured snippet appearances |
| GEO | ChatGPT, Perplexity, Claude, AI Overviews, Gemini | Authority, quotability, factual accuracy, entity clarity | AI citation rate, brand mentions |
| Agent Readiness | AI agents that fetch and act | MCP servers, OAuth flows, machine-readable APIs, Markdown content, agentic payments | Pass rate on agentready.org / isitagentready.com checks |

### Google's published guidance: policy document vs engineering reality

Google publishes its own [GEO optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide). It says AI Overviews and AI Mode are part of Google Search, classic SEO is the strategy, and certain practices are myths:

- llms.txt files or other "special" AI markup
- Content chunking
- Rewriting content for AI
- Structured data added specifically for AI (still useful for rich results in classic Search)
- Pursuing inauthentic mentions across the web

Read this as policy guidance, not engineering reality. Google's published documents have a 20-year history of diverging from algorithm behavior. Several concrete signals undercut the "myths" framing:

- Google's John Mueller publicly calls markdown pages "a stupid idea." Google's Addy Osmani publicly recommends "Markdown over HTML... creating llms.txt as a discovery layer." Two Googlers, opposite advice, both speaking on the record.
- Google's Lighthouse tool checks for `llms.txt` when scoring agentic browsing capability, and the developer documentation recommends it.
- Anthropic's voluntarily-published Claude system prompt contains explicit arbitration rules: present-day questions require search regardless of model confidence, original sources beat aggregators, and "heavily-SEO'd topics like product recommendations" are treated with skepticism. These are not described in Google's guide but are present in the engineering reality of frontier models.
- Modern retrieval architecture (RAG, passage retrieval, source reranking, documented in academic literature since 2020) operates on extracted chunks regardless of whether the model is told to "think about chunks." Content that cannot be cleanly extracted at the section level never enters the retrieval pool.

Operational conclusion is unchanged from before: calibrate per engine. For Google AI Overviews and AI Mode, classic SEO at peak quality is the foundation. For ChatGPT (85% of AI referral traffic), Perplexity, Claude, and training corpora, the additional surfaces in this skill apply. The corrected framing is sharper: Google's AI guide tells you what is defensible to do in front of regulators and what the SEO conference circuit will repeat back at you; the engineering tells you what the model actually rewards. Both descriptions are accurate; they serve different purposes. See `content-strategy.md` for the three-layer arbitration model that explains why the engineering reality differs from the policy.

Google does endorse the agent-readiness layer separately, pointing to [web.dev's agent-friendly site UX guide](https://web.dev/articles/ai-agent-site-ux) and the Universal Commerce Protocol.

## When to use this skill

Use it when the user wants any of the following.

Content work: write or rewrite a page so AI engines cite it. Optimize a definition, FAQ, comparison, or thought-leadership piece for quotability. Apply E-E-A-T. Diagnose why a page is invisible to AI search.

Technical work: implement Schema.org JSON-LD. Configure robots.txt for AI crawlers. Build llms.txt or llms-full.txt. Apply the FAST framework. Audit Core Web Vitals or SSR coverage for AI crawler readability.

Agent work: make a site readable by agents. Set up Markdown content negotiation. Publish an MCP Server Card. Expose an API Catalog. Wire OAuth discovery. Add Web Bot Auth. Accept agentic payments.

Strategy work: prioritize quick wins, build a roadmap, choose a measurement stack, set up GA4 tracking for AI referrals, pick the right monitoring tools, compare platform behavior.

If the request is ambiguous, ask one focused question before loading reference files. The most useful disambiguator: "Are you optimizing content, the technical site, or making the site usable by AI agents?"

## How to use this skill

Read the routing table, then load only the reference files that match the request. Do not bulk-load. Each reference file is self-contained.

| Reference file | Load when |
|---|---|
| `references/content-strategy.md` | Writing, rewriting, auditing content; questions about authority, quotability, E-E-A-T, content types likely to earn citations |
| `references/structured-data.md` | Implementing Schema.org JSON-LD; choosing the right schema type; questions about Article, FAQ, Organization, Product, HowTo, Speakable, Person |
| `references/ai-crawlers-and-llmstxt.md` | Configuring robots.txt for AI crawlers; building llms.txt / llms-full.txt; Content Signals; per-directory llms.txt strategy for large sites |
| `references/technical-implementation.md` | Page speed, semantic HTML, SSR/SSG/ISR, URL structure, FAST framework, Core Web Vitals, image alt text, sitemap |
| `references/agent-readiness.md` | MCP Server Card, Markdown content negotiation, /index.md fallback, Web Bot Auth, OAuth Authorization Server Metadata, API Catalog, x402, ACP, UCP, agent skills index |
| `references/platforms.md` | Platform-specific tactics for ChatGPT, Perplexity, Google AI Overviews, Google AI Mode, Claude, Gemini, Copilot; citation patterns; AI referral traffic share |
| `references/measurement.md` | GA4 setup, AI referral tracking, KPIs, monitoring tools, industry benchmarks |
| `references/audit-checklist.md` | Full pre-publish, technical, and post-publish audit; AI search readiness score |
| `references/templates.md` | Ready-to-paste robots.txt, llms.txt, JSON-LD, FAQ schema, MCP Server Card, OAuth metadata, x402 response |

For a complete audit, load `audit-checklist.md` first. It links into the other references where details are needed.

## Core principles (apply on every output)

Four content pillars. Authority. Quotability. Comprehensiveness. Structure. The full treatment is in `content-strategy.md`. The short version: cite real sources, lead with the answer, cover the topic deeply, use semantic structure.

Four agent-readiness dimensions (Cloudflare's framing). Discoverability. Content accessibility. Bot access control. Capabilities. The detail is in `agent-readiness.md`. The short version: tell agents where to look, give them parseable content, declare what bots can do, expose tools and APIs they can call.

The FAST framework for crawlability. Fetchable, Accessible, Structured, Trim. A page that fails FAST will not be cited reliably regardless of content quality. Detail is in `technical-implementation.md`.

## Quick wins (recommend in this order)

When the user asks "where do I start", recommend in this order. Each step is high leverage and cheap to ship.

Step 1: Assessment. Load the user's top 20 pages with JavaScript disabled. What remains is roughly what AI crawlers see. Benchmark current AI citation rate with at least one tool from `measurement.md`. Score the homepage at isitagentready.com.

Step 2: Quick wins. Update robots.txt to allow GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, anthropic-ai, PerplexityBot, Google-Extended, Applebot-Extended, and CCBot. Publish llms.txt at site root. Add FAQ schema to the top five content pages. Get Core Web Vitals passing.

Step 3: Structural. Implement Article, Organization, and Product (if commerce) Schema.org markup site-wide. Ensure SSR or SSG for all content paths. For large doc sites, split llms.txt by top-level directory and add /index.md Markdown content negotiation. For agent-facing products, publish an MCP Server Card and OAuth discovery document.

## When acting as auditor

The typical audit flow:

1. Confirm the URL or content scope with the user.
2. Load `audit-checklist.md`.
3. Run the checks in order: content, structured data, crawlability, llms.txt, agent readiness, measurement.
4. Produce a report with three sections: what passes, what fails (with severity), and a prioritized fix list mapped to the relevant reference file.
5. For each fix, offer to generate the implementation (code, JSON-LD block, robots.txt, llms.txt, etc.) using `templates.md`.

When the user gives a single URL and asks for an audit, web_fetch the URL first. Inspect the rendered HTML. Check the response headers. Look for /robots.txt, /llms.txt, /sitemap.xml, and `.well-known/` paths. Use real evidence from the fetch, not assumptions.

## When acting as content writer or optimizer

Workflow:

1. Identify the target query or buyer-journey stage (awareness, consideration, decision).
2. Choose the content type from `content-strategy.md` ("Content types most likely to earn AI citations").
3. Apply the four pillars during drafting, not as a post-edit pass.
4. Add Schema.org JSON-LD before publish (see `structured-data.md`).
5. Verify against the publish checklist in `audit-checklist.md`.

For B2B service businesses (the most common case for this skill's target users), prioritize: original research, case studies, thought leadership with named author, comparison content, and deep how-to guides. Skip thin definitional content unless paired with original insight.

## When acting as technical implementer

Workflow:

1. Diagnose first with the FAST framework. If the page fails Fetchable, nothing else matters until that is fixed.
2. Use `templates.md` for ready-to-paste configurations.
3. Validate JSON-LD with Google Rich Results Test. Validate llms.txt against the spec at llmstxt.org.
4. For SPAs (React, Vue, Angular), force the SSR/SSG conversation. Client-rendered content is invisible to GPTBot, ClaudeBot, and PerplexityBot.
5. For large documentation sites, follow Cloudflare's pattern in `agent-readiness.md`: per-directory llms.txt, /index.md content negotiation, hidden agent directives.

## Output conventions

These apply to all artifacts this skill produces.

No em dashes. Replace with commas, colons, parentheses, or a sentence break. The dash character is a strong tell of AI-generated copy and pattern-matches against detection tools.

Remove AI-writing tells: inflated symbolism, promotional language ("revolutionize", "unleash", "unlock"), superficial -ing analyses, vague attributions ("experts say", "studies show" without a link), rule of three filler, negative parallelisms ("not just X, but Y"), excessive conjunctive phrases ("furthermore", "additionally", "moreover" in every paragraph), sycophantic openings.

Match the user's language. Default to English. Use Brazilian Portuguese when the user writes in Portuguese or when the output is for a Brazilian audience.

When producing code, configuration, or schemas, use the templates in `templates.md` as the source of truth. Adapt names and URLs to the user's domain. Do not invent fields.

Cite real, current data. Industry stats change quickly. For any benchmark older than the data in `measurement.md`, web_search before quoting it.

When the user shares a URL, fetch it. Do not infer the contents.

## Caveats and limits

GEO is not a substitute for product, brand, or marketing fundamentals. A weak product will not earn AI citations regardless of optimization quality. AI engines disproportionately favor brands with existing third-party presence (earned media, Reddit, Quora, Wikipedia). For emerging brands, expect hedging language ("might be worth considering") until enough independent mentions accumulate. The fix is sustained authority-building, not more pages.

AI engine behavior changes monthly. The platform-specific guidance in `platforms.md` is dated material. Confirm current behavior with a fresh web_search before making big claims about how a specific engine ranks or cites.

This skill does not promise rankings, citations, traffic, or revenue. It captures the current best-known practices, which the user must apply, ship, measure, and iterate on.
