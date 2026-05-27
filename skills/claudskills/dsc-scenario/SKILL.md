---
name: dsc-scenario
description: Build a multi-call repro plan against a Salesforce API reference published on developer.salesforce.com ("DSC"). Invoke when the user wants to reproduce a customer flow on a sandbox and needs to know which supporting API calls to make, in what order, with which scopes, and how IDs thread through the chain – examples: "repro a registered shopper adding a promo coupon and checking out", "what do I need to call before `createOrder`", "prerequisites for `createOrder`" (treat "prerequisites" or "prereqs" of a target op as a multi-call request even if the user says just that word), "build me a scenario around this cURL", "chain of calls to get from X to Y". Accepts an operationId, a natural-language goal, or a sample cURL/HTTP request as the target. Runs a type-graph walk (structural dependencies) and composes a linear plan + runnable cURL block. Every step cited to a public developer.salesforce.com URL. Works against any DSC reference `dsc-scrape` can deliver. Not for scraping a reference wholesale (that's `dsc-scrape`), not for answering one-off "what does this endpoint require" lookups like "what scopes does X need" (that's `dsc-endpoint-lookup` – single-endpoint, no ordering), not for diagnosing why an existing request is failing (that's `dsc-triage`), and not for *authoring a runnable demo/repro script* the user will paste into a terminal – even if the subject is a Salesforce API on DSC (that's `stepped-demo-script`; this skill produces the *plan* of calls, not the paste-and-run bash).
---

# DSC Scenario Composer

Produce a plan of SCAPI / OCAPI calls – in order, with scope union, ID threading, and a runnable cURL block – to reach a target state. Every claim backed by a public `developer.salesforce.com` URL.

## When to use

The user is trying to reproduce a customer flow on a sandbox and needs to know:
- Which API calls must happen *before* the target operation can succeed.
- Which scopes the sandbox's SLAS/OAuth client must be configured with.
- Where each input to the target (basket IDs, customer IDs, line-item IDs) comes from.

Or the user pastes a cURL command and asks "what else do I need to call to make this work."

## Inputs

Ask for missing bits only when the skill can't proceed:

- **Target** – one of:
  - An operationId (`createOrder`, `shopper-baskets.addItemToBasket`).
  - A natural-language goal ("registered shopper adds a coupon and checks out"). You resolve this to an operationId by matching against `_index.json.title` + Summary prose across cached references; ask the user to confirm before proceeding.
  - A sample request (cURL, raw HTTP). Use `lib/parse-request.js` + `lib/resolve-slug.js` to map it to a slug.
- **Reference URL** – the developer.salesforce.com URL of the reference containing the target. Usually inferrable from the request path or operationId's reference prefix.

## Flow

1. **Resolve target** to `{reference, targetSlug}`. For natural-language goals, match titles + Summary prose and confirm with the user.
2. **Run the type-graph walk.** You have two options:
   - **Preferred (sub-agent):** read `scripts/walk-via-agent.md` and pass the parameterized prompt to Claude's `Agent` tool. The sub-agent returns `{nodes, edges, externalInputs}`. Pass that as `graph` in the scenario.js input.
   - **Fallback (local):** omit `graph` – `scenario.js` will run `walkTypes` locally. Same algorithm, but the JSON reads happen in your context.
3. **Invoke `scenario.js`**:

   ```bash
   node ~/.claude/skills/dsc-scenario/scripts/scenario.js <<'EOF'
   {
     "target": "createOrder",
     "referenceUrl": "https://developer.salesforce.com/docs/commerce/commerce-api/references/shopper-orders",
     "graph": { "nodes": [], "edges": [] },
     "cacheRoot": "/Users/<you>/.cache/dsc-scrape"
   }
   EOF
   ```
4. **Layer business-logic ordering.** The structural plan from Step 3 may need reordering based on rules stated in the Summary or endpoint `description` prose. Apply constraints only when they're *quoted* from the docs; otherwise leave the structural order as-is and annotate as "no explicit ordering constraint found – structural only." Never invent constraints.
5. **Compose the output** per the template below. Cite only the URLs in `sources[]`; never cite local paths.

## Output composition

scenario.js emits `{plan, runnable, sources}`. Wrap it for the user like this:

```
## Scenario: <short NL description of the goal>

Target: <METHOD> <path>   (<reference>.<operationId>)
References involved: <reference list>
Combined scopes required: <plan.combinedScopes>

## Plan

1. **<Step title>.** <operationId>.
   - Method/path: <step.method> <step.path>
   - Spec: <step.specUrl>
   - Produces: <producedTypes names / relevant response fields>
   - Why: <one line, quoting structural evidence OR a sentence from Summary/description>

2. ... (one block per step.)

## Run it

<fenced bash block with plan.runnable pasted verbatim>

## Sources
- <url 1>
- <url 2>
```

When a step's only evidence is `{kind: 'structural', ...}`, the "Why" line should read: "<consumer> requires <field> in the request; this step's response provides it." When you add a business-logic constraint from prose, quote the relevant sentence and cite the Summary or endpoint URL inline.

## Cross-reference walks

If the sub-agent returns `externalInputs: [...]` (e.g. `access_token` originating from `shopper-login` / SLAS), the outer conversation should warm the cache for that reference (via `scrapeRefresh`) and re-run the scenario. The skill itself doesn't auto-scrape cross-reference deps – it surfaces them and asks you to proceed. SLAS is the most common case.

## What this skill doesn't do

- **Doesn't run the plan.** Output is a plan + runnable snippet; the engineer executes it in their sandbox.
- **Doesn't invent ordering constraints.** If the type graph has no edge and the prose has no ordering statement, the skill emits the structural order and annotates it as such.
- **Doesn't resolve environment-specific values** (site-ID, client-ID, auth flavor). Those become placeholders in the cURL block; the legend at the bottom names each.
- **Doesn't cite local cache paths.** `sources[]` only.
- **Doesn't auto-scrape cross-reference dependencies.** If the walk surfaces an `externalInputs` entry (e.g. SLAS for `access_token`), the skill flags it and asks you to scrape that reference separately; it does not transparently expand into a multi-reference plan.

## Prerequisites

Same as `dsc-triage`: `~/.cache/dsc-scrape/` writable, Node.js. The shared scrape library ships with this skill via `lib -> ../_shared`.

## Key invariants

- **All DSC fetches go through the shared scrape library** (via `scrapeRefresh`). Never use `curl`, `WebFetch`, or any other client to read a `developer.salesforce.com` URL. When the user names a target you can't resolve, cascade through the library's discovery modes (`/docs/apis` → `lib/scrape/aliases.js` for catalog-missing products → product-area landing → reference root); don't reach for curl as a shortcut.
- Cite only the public DSC URLs in `sources[]`; never cite local cache paths.
