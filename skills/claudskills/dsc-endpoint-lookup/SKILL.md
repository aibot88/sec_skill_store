---
name: dsc-endpoint-lookup
description: Look up and quote one spec field on one endpoint in a Salesforce API reference published on developer.salesforce.com ("DSC") – OAuth scopes, query params, request body, response schema, auth scheme, HTTP method/path – by reading JSON that `dsc-scrape` produced (or producing it on demand). Works against any DSC reference the scraper can deliver. Invoke whenever answering the user's ask requires knowing what one specific endpoint's spec says about one of those fields, even if the user's surface ask is broader: direct spec-field lookups ("what scopes does shopper-products getProducts need?", "which query params does searchOrders take?", "what auth scheme guards createOrder?"), code-generation asks that reference a named endpoint ("write me a node script that calls getProduct" – quote the spec for the user to write the code against; don't write the code yourself), and how-to asks that are really spec-field questions in disguise ("how do I paginate search results", "what limit does X accept" – quote the relevant param; ask which search endpoint if ambiguous). The reference name can be implicit if the endpoint name is unambiguous. Decline when no endpoint field is in scope at all: concept or comparison questions without a named endpoint ("what's the difference between OCAPI and SCAPI", "what is SLAS"), parsing a user-supplied local file rather than a DSC reference ("parse my ~/work/foo.json"), scraping whole references wholesale (that's `dsc-scrape`), and guides / concept pages / release notes.
---

# DSC Endpoint Lookup

Answer one targeted question about one endpoint in a Salesforce API reference on DSC, fast. The heavy lifting – fetching and parsing the spec – belongs to the shared scrape library at `lib/scrape/` (the same library that backs the `dsc-scrape` Skill). This skill's job is to (a) make sure the endpoint JSON exists locally, (b) pull out the specific field the user is asking about, and (c) answer in prose with the file path so the user can verify.

## Inputs from the user

The user's question usually contains:

- **A reference name** ("shopper-products", "orders", "scapi shopper baskets") – maybe abbreviated, maybe product-branded ("SCAPI Shopper Products" -> `shopper-products`).
- **An operation identifier** ("getProducts", "createOrder", sometimes partial: "the products get endpoint", "that getCustomer call").
- **A concrete question**: what scopes, what params, what body, what response, what method/path, what auth scheme.

Sometimes one of these is missing. See "Disambiguation" below.

## Cache location

Use `~/.cache/dsc-scrape/` as the cache root. Create it if it doesn't exist (scrape will create subdirs itself). This is shared across projects – scraping once benefits future sessions.

Per-reference layout inside the cache mirrors `dsc-scrape`'s output:

```
~/.cache/dsc-scrape/
└── <reference>/
    ├── _index.json           full slug list + title + siblings
    ├── Summary.json          overview prose (NOT an endpoint)
    ├── <operationId>.json    one file per endpoint
    └── types/<TypeName>.json one file per named type
```

## Flow

1. **Pick reference + slug** from the user's question. If either is missing or ambiguous, disambiguate (see below) before running anything.
2. **Always refresh first.** Run `scrapeRefresh` (from `lib/scrape-refresh.js`) against the reference root before querying. The shared scrape library owns a 1-hour TTL matching DSC's upstream `cache-control: max-age=3600`, so when the cache is fresh this costs one `_index.json` read and zero network round-trips. The returned summary has `refreshed: true` (new data fetched) or `refreshed: false` (cache already fresh).
3. **Query locally** by running `scripts/query.js`. If it exits 0, you have the data. If exit 3 (slug not found / ambiguous), use the returned `candidates` to confirm with the user or narrow.
4. **Write the answer in prose**, quoting only the field the user asked about, and cite the public DSC URL – the `url` field in the JSON returned by `query.js`. Never cite the local cache path in your output. (If the user explicitly asks "where's the local copy?", read the absolute path from `query.js`'s `file` field on demand; don't volunteer it.)

### Step 1: Resolve reference + slug

The user's question may name a reference directly ("shopper-products getProducts"), name it under a brand or rebrand ("SCAPI products" → `shopper-products`; "Data Cloud" → Data 360), or leave it implicit ("how do I paginate searches" – which search?). Resolve to a concrete `<reference>/<slug>` pair before any other step.

**Default discovery path: bootstrap via the shared scrape library.** When the reference name isn't already concrete in your context, call `scrapeRefresh` against `https://developer.salesforce.com/docs/apis` first. This writes `~/.cache/dsc-scrape/_catalog.json` listing every product DSC publishes, with each product's `referenceUrl` and a `referenceShape` tag (`area-landing` / `reference-root` / `atlas` / `static-html` / `unknown` – only the first two are scrapeable). Pick the matching product, then scrape its `referenceUrl` (a product-area landing) to get `_landing/<product>_<area>.json`, which lists every reference in that area with its `id`, `title`, and `referenceType` (`rest-oa3` / `rest-raml` / `rest-oa2` are scrapeable; `markdown` isn't). Read these files to anchor your slug pick to ground truth instead of guessing. Both list-only modes share the 1-hour TTL with reference scrapes – once `_catalog.json` exists locally, follow-on discovery in this session is free.

**Shortcut: skip the catalog scrape only if the reference name is already concrete.** If the user explicitly named a Commerce SCAPI reference ("shopper-products", "shopper-baskets", "orders") or one you've already cached this session, you can scrape its reference root directly without going through the catalog. The 1-hour TTL absorbs the cost if you're wrong about cache state.

You can list what's already on disk via `node scripts/list.js ~/.cache/dsc-scrape/` to skip a redundant catalog scrape.

Common name drifts to anchor against the catalog/landing:

| User says | Reference slug |
|---|---|
| "Shopper Products", "SCAPI products", "the products API" | `shopper-products` |
| "Orders API", "SCAPI orders" | `orders` (merchant-facing, under commerce-api) **or** `shopper-orders` (shopper-facing) – different references |
| "Customer Groups" | the operations live in `customers`, not `customer-groups` |
| "Data Cloud X", "Data 360 X" | Data 360 references (Salesforce rebranded) |

The **slug** is typically the `operationId` (`getProducts`, `createOrder`). Fuzzy matching is built in – `query.js` will resolve "products" against the index if there's exactly one match.

### Step 2: Refresh the cache

Use `lib/scrape-refresh.js` to warm the cache before every query. The helper owns the subprocess dance, calls into the shared scrape library at `lib/scrape/scrape.js`, and returns a normalized `{refreshed, reference, format, specUrl, files, cacheRoot}` object. When the cache is still within its 1-hour TTL, `scrapeRefresh` returns `refreshed: false` without fetching – calling it unconditionally is effectively free.

```js
const { scrapeRefresh } = require('./lib/scrape-refresh.js');

const result = await scrapeRefresh({
  referenceUrl: 'https://developer.salesforce.com/docs/<product>/<area>/references/<reference>',
  // scrapeScript defaults to lib/scrape/scrape.js (resolved via require.resolve)
  // cacheRoot defaults to ~/.cache/dsc-scrape
});
```

Scraping the **reference root** (no `?meta=`) writes the whole reference in one pass – Summary + every endpoint + every type + `_index.json`. Do this even if the user only asked about one endpoint. The network cost is identical: the scraper downloads a single static spec file that already contains every operation, and writing one slug vs. all of them is just a parse-time decision. Upsides of the whole-reference scrape:

1. **Slug safety** – if the user's slug guess was slightly off, `_index.json` lets you correct it without a second fetch.
2. **Future cache hits** – any later question about any other endpoint in this reference is free.
3. **Type resolution works** – `--resolve-refs` reads `types/<TypeName>.json`. Those files only exist if the whole reference was scraped.
4. **TTL is cheap.**

Only scrape a single slug (`?meta=<slug>`) if the user explicitly asked for just that one to land on disk.

**If the scrape exits 1 with a 404 on a reference root** (your shortcut path was wrong – misspelled, rebranded, or not in that product area), fall back to the same cascade Step 1 describes: scrape `/docs/apis` for `_catalog.json`, then the product's `referenceUrl` for `_landing/<area>.json`, then the corrected reference root. Don't guess variations by re-scraping them one at a time.

A few products have `/references/` pages but don't appear in the `/docs/apis` catalog – if the catalog has no match for a product the user named, lowercase the user's hint and substring-match it against the keys in `lib/scrape/aliases.js` (the `CATALOG_MISSING_ALIASES` map) for the area-landing URL. Only ask the user for a DSC URL if neither catalog nor alias map resolves the hint.

If `referenceType` is anything other than `rest-oa3`, `rest-raml`, or `rest-oa2` (for example `markdown`), the reference isn't a machine-readable spec the scrape library can deliver – tell the user and stop.

After a successful scrape, run `query.js`. If it can't find the slug, read `_index.json`'s slug list – the user's operation name may also be off (e.g. `searchCustomerGroups` plural vs. `searchCustomerGroup` singular).

### Step 3: Query locally

```bash
node <skill>/scripts/query.js ~/.cache/dsc-scrape/ <reference> <slug> [--field <name>]
```

Match the question to the right field – this keeps the output small and focused:

| User asks... | Use `--field` |
|---|---|
| "what scopes...", "what OAuth...", "which permissions..." | `security` |
| "what params...", "what query params...", "required params..." | `parameters` |
| "what's the request body", "what fields in the POST body" | `body` – add `--resolve-refs` |
| "what response schema", "what does it return", "what's the 200 response" | `responses` – add `--resolve-refs` |
| "HTTP method", "path", "endpoint URL" – any of these alone | `all` (the header is included with every field) |
| "show me the whole endpoint" | `all` or `raw` if they want the full JSON untouched |

**`--resolve-refs` matters a lot for `body` and `responses` questions.** Without it you get back `schemaRef: "#/components/schemas/Product"` and you'd have to read `types/Product.json` separately (and every type it nests) to get real fields. `--resolve-refs` inlines the referenced type in one call, so the user's question ("what does it return?") gets a direct answer from a single script run instead of a chain of file reads.

Examples are stripped by default (they can be huge). Pass `--include-examples` only if the user explicitly wants them.

### Step 4: Answer in prose

Lead with the direct answer, then show the evidence (one-line quote of the relevant JSON shape), then the file path. One or two paragraphs for most questions; grouped bullets when there are many related facts (e.g. long parameter list, wide response type).

**Freshness preamble:** If `scrapeRefresh` returned `refreshed: true` *and* there was a prior cache (i.e. this wasn't a first-ever scrape), open with a single short sentence: *"I refreshed the cache first – the upstream spec had changed."* Then answer. If `refreshed: false`, or if this was the first scrape of this reference, skip the preamble and go straight to the answer. You can tell it's a first-ever scrape if `_index.json` didn't exist before your `scrapeRefresh` call.

**Format guidance – this matters because answers are read in a terminal:**

- Use **prose + bullets**. Skip markdown tables – they render fine in a rendered preview but look like walls of `|` characters in the raw terminal most users are actually reading. Bullets degrade gracefully.
- Use **one-line JSON-ish quotes** (`security: [{ scheme: "X", scopes: [...] }]`) for shape, not full pretty-printed blocks. The user can open the cited file if they want the full thing.
- **Group related fields** when a type is wide (e.g. a Product response with 45 fields). "Scalars: ..., Pricing: ..., Merchandising: ..." beats an alphabetical dump.
- **No hedging preamble.** Don't open with "Based on the cached JSON, I can tell you that..." – just answer.
- **Cite the `url` field** from `query.js`'s structured output at the end, not inline mid-sentence. Never cite the local cache path.

**Example: "what scopes does shopper-products getProducts need?"**

> `getProducts`'s spec lists `sfcc.shopper-products` and `sfcc.shopper-standard` under the `ShopperToken` scheme — either grants access. `sfcc.shopper-standard` is a meta-scope that bundles the common shopper feature scopes (including `sfcc.shopper-products`), so a token with `shopper-standard` covers `getProducts` already; see https://developer.salesforce.com/docs/commerce/commerce-api/guide/standard-shopper-scope.html.
>
> `security: [{ scheme: "ShopperToken", scopes: ["sfcc.shopper-products", "sfcc.shopper-standard"] }]`
>
> Source: https://developer.salesforce.com/docs/commerce/commerce-api/references/shopper-products?meta=getProducts

**Note on `security[]` semantics in practice.** OAS says all scopes within a single `security[]` entry are required together (AND); multiple entries in the array are alternatives (OR). In practice this is almost universally ignored: public REST specs co-list scope alternatives in a single entry rather than producing multiple entries, and the consuming auth servers treat the co-list as OR. Slack's canonical OpenAPI spec, for example, co-lists `chat:write:user` and `chat:write:bot` on `chat.postMessage` (https://github.com/slackapi/slack-api-specs/blob/master/web-api/slack_web_openapi_v2.json), and per https://api.slack.com/methods/chat.postMessage those are alternative token types that can't both be present – AND is impossible. SCAPI follows the same convention: merchant `["sfcc.products", "sfcc.products.rw"]` on a GET means either grants the read; shopper `["sfcc.shopper-products", "sfcc.shopper-standard"]` means either grants the call (shopper-standard is a meta-scope, not a co-required umbrella). Default reading: a co-listed scope set is OR unless you have specific evidence otherwise (a runtime test that fails with one scope missing, or an explicit doc statement that both are required). Don't claim AND just because OAS syntax says AND.

**Example: "what query params does searchOrders take?"**

> `searchOrders` accepts these query params (all optional unless noted):
> - `siteId` (required) – site identifier
> - `q` – free-text search
> - `limit` / `offset` – pagination
>
> Source: https://developer.salesforce.com/docs/commerce/commerce-api/references/shopper-orders?meta=searchOrders

**Example: "what does getProduct return on 200?"** (response-schema question – use `--field responses --resolve-refs` so you can name real fields)

> Returns a `Product` object. Top-level shape:
> - **Identifiers**: `id` (required), `brand`, `manufacturerName`, `upc`, `ean`
> - **Content**: `name`, `shortDescription`, `longDescription`, `pageTitle`, `pageKeywords`
> - **Pricing**: `price`, `priceMax`, `prices` (pricebookId -> number), `tieredPrices`, `currency`
> - **Media**: `imageGroups[]`
> - **Variation** (master/variant products): `variants[]`, `variationAttributes[]`, `master`
> - **Expansion-gated**: `inventory` (availability expansion), `shippingMethods` (shipping_methods expansion)
>
> Also allows `c_*` custom attributes. Other responses: 400, 401, 404.
>
> Source: https://developer.salesforce.com/docs/commerce/commerce-api/references/shopper-products?meta=getProduct (response type `Product`)

Stay terse. Do not dump the whole JSON unless the user asked for it.

## Disambiguation

**Slug ambiguous.** `query.js` exit 3 with `candidates` means the fuzzy match hit more than one slug. Show the user the candidates and ask which they meant. Don't guess.

**Reference ambiguous.** "orders" could be the commerce-api `orders` reference (the merchant-facing order management API) or `shopper-orders` (the shopper-facing one). If the user's question could belong to either, list both and ask. Don't default silently.

**Slug is a type, not an endpoint.** Type slugs are stored as `type:<Name>` and live under `types/`. If the user asks about a shape like "Order" or "Product", they usually mean the type – query with `type:Order`. If unclear whether they want the *endpoint* `getOrders` or the *type* `Order`, ask.

**User said "Summary"** or asked for "the endpoint" without naming one. Summary.json is the reference overview, not an endpoint. Read `_index.json`, pick a verb-shaped slug (starts with `get/create/update/delete/search/list`), and confirm with the user before answering for a specific one.

## When NOT to invoke

- "Scrape this URL" / "get me all the endpoints in X" -> that's `dsc-scrape`, not this.
- Atlas books (URLs with `atlas.` and `.htm`) -> decline, same reasoning as `dsc-scrape`.
- MuleSoft docs (docs.mulesoft.com) -> decline.
- Guides, concept pages, release notes -> decline. This skill only reads the structured output of `/references/` pages.
- "Compare the response body of X and Y" -> you *can* do this by running `query.js` twice, but lean on the JSON – don't invent comparisons beyond what the files support.

## Key invariants

- **All DSC fetches go through the shared scrape library** (via `scrapeRefresh`). Never use `curl`, `WebFetch`, or any other client to read a `developer.salesforce.com` URL – not for discovery, not for verification, not for "just one quick check." The cascade in Step 1 covers every shape (`/docs/apis`, area landing, reference root, single slug) with shared TTL caching. Reaching for curl is a sign you're solving a problem the library already owns.
- Every answer cites the public DSC URL (the `url` field returned by `query.js`). The user should always be able to open it and verify.
- Never fabricate a scope, param, or response. If the file doesn't have the field the user asked about, say "the spec doesn't declare that" and point at the file.
- Default to the smallest useful `--field`. Don't dump the full endpoint JSON unless the user asked to see everything.
- Cache is per-machine, not per-project. Don't scrape into project-local paths unless the user explicitly specifies one.

## Bundled scripts

- `scripts/query.js` – resolve slug, extract field, print digest. Exit codes: 0 found, 2 reference-not-cached, 3 slug-not-found-or-ambiguous.
- `scripts/list.js` – list cached references, or list slugs within a cached reference (optional `--grep` filter).

Both scripts use only Node built-ins. No install needed.
