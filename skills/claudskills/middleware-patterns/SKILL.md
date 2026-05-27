---
name: middleware-patterns
description: "Use when designing or reviewing Next.js middleware (`middleware.ts`): cross-cutting request/response transforms before route resolution, Edge Runtime constraints, `matcher` config, `NextRequest`/`NextResponse` API, the four response shapes (next/rewrite/redirect/direct), canonical patterns (auth gate, locale routing, A/B testing, header injection, geo-routing, bot blocking), and the design rule that middleware is for cross-cutting concerns across many routes — never per-route business logic. Do NOT use for per-route HTTP endpoint logic (use route-handler-design), Server Action mutations (use server-actions-design), abstract HTTP semantics (use http-semantics), CSP and hardening (use security-fundamentals), or the cross-cutting streaming model (use streaming-architecture)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"engineering\",\"domain\":\"engineering/frontend\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-17\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-17\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"Next.js middleware\\\\\\\",\\\\\\\"middleware.ts file\\\\\\\",\\\\\\\"NextRequest NextResponse\\\\\\\",\\\\\\\"matcher config middleware\\\\\\\",\\\\\\\"Edge Runtime constraints\\\\\\\",\\\\\\\"NextResponse.redirect rewrite next\\\\\\\",\\\\\\\"auth check before route\\\\\\\",\\\\\\\"locale routing i18n middleware\\\\\\\",\\\\\\\"A/B testing variant rewrite\\\\\\\",\\\\\\\"CSP nonce middleware\\\\\\\",\\\\\\\"geo-routing X-Vercel-IP-Country\\\\\\\",\\\\\\\"request header injection\\\\\\\",\\\\\\\"bot blocking middleware\\\\\\\",\\\\\\\"middleware cookie set\\\\\\\"]\",\"triggers\":\"[\\\\\\\"how do I redirect unauthenticated users to login in Next.js\\\\\\\",\\\\\\\"how do I run code before every request in Next.js\\\\\\\",\\\\\\\"how do I set security headers globally in Next.js\\\\\\\",\\\\\\\"how do I do locale routing in App Router\\\\\\\",\\\\\\\"how do I do an A/B test with rewrites\\\\\\\",\\\\\\\"why does my middleware run on static assets\\\\\\\",\\\\\\\"can middleware do a database query\\\\\\\",\\\\\\\"how do I generate a CSP nonce per request\\\\\\\"]\",\"examples\":\"[\\\\\\\"design middleware that redirects unauthenticated users to /login while letting public routes through, configured via a matcher\\\\\\\",\\\\\\\"add a middleware that generates a per-request CSP nonce and injects it into both the request and response headers\\\\\\\",\\\\\\\"implement locale routing that detects Accept-Language and rewrites /about to /en/about for new visitors\\\\\\\",\\\\\\\"add bot blocking that returns 403 for known scraper user-agents while letting search-engine bots through\\\\\\\",\\\\\\\"tune a middleware that runs on every request down to 5ms so it stops adding latency to image fetches\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"implement a /api/posts POST endpoint (use route-handler-design)\\\\\\\",\\\\\\\"implement a delete-comment mutation triggered from a form button (use server-actions-design)\\\\\\\",\\\\\\\"explain what an HTTP 308 means vs 307 (use http-semantics)\\\\\\\",\\\\\\\"design the full CSP policy and the rest of the security-header strategy (use security-fundamentals)\\\\\\\",\\\\\\\"design a long-lived SSE stream from middleware (use streaming-architecture)\\\\\\\",\\\\\\\"design the CSP policy, threat model, or OWASP audit for a system (use security-fundamentals)\\\\\\\",\\\\\\\"decide what an HTTP method, status code, or header should mean per RFC 9110 (use http-semantics)\\\\\\\",\\\\\\\"design signature verification, idempotency, or retry semantics for vendor webhooks (use webhook-integration)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"route-handler-design\\\\\\\",\\\\\\\"server-actions-design\\\\\\\",\\\\\\\"http-semantics\\\\\\\",\\\\\\\"security-fundamentals\\\\\\\",\\\\\\\"server-components-design\\\\\\\",\\\\\\\"client-server-boundary\\\\\\\",\\\\\\\"webhook-integration\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"route-handler-design\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"middleware runs once before route resolution and applies to many routes via a matcher; route-handler-design runs for one route and one method after route resolution. Middleware owns the cross-cutting layer (auth gate, locale rewrite, header injection); route handlers own the per-route logic. They compose: middleware passes through to the handler, the handler executes, the response flows back.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"server-actions-design\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"server-actions-design owns the internal-mutation surface invoked from the app's own UI; middleware is the cross-cutting request preprocessor that runs before any route or action. A Server Action call passes through middleware on its way to the server.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"server-components-design\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"server-components-design owns the render path that produces a page; middleware runs upstream of render and can rewrite, redirect, or pass through. Middleware does not replace render; it gates and rewrites it.\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"code-review\\\\\\\",\\\\\\\"security-fundamentals\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"Middleware is to a Next.js app what a building's lobby concierge is to its offices — every visitor passes through the lobby before reaching any specific floor; the concierge can check ID badges (auth gate), redirect visitors to the right elevator (locale or A/B rewrite), hand out lanyards with security policies attached (CSP nonce, request-ID header), or turn away bad-faith visitors at the door (bot block). The concierge cannot do the work of any specific office (per-route business logic) — that happens after the visitor gets off the elevator — but they enforce the rules that apply to every floor.\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"Next.js middleware is a single async function exported as default from `middleware.ts` at the project root that runs on the Edge Runtime before route resolution for every request matching its `matcher` config. It receives a `NextRequest` and returns a `NextResponse` (or implicitly `NextResponse.next()`), and can do four things: pass through (`next`), rewrite to a different internal path (`rewrite`), redirect to a different URL (`redirect`), or short-circuit with a direct response. It runs once per request before any page render, Server Component fetch, Server Action, or Route Handler executes — making it the only place to apply genuinely cross-cutting concerns without per-route ceremony.\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/middleware-patterns/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/middleware-patterns/SKILL.md
  skill_graph_export_description: shortened for Agent Skills 1024-character description limit; canonical source keeps the full routing contract
  skill_graph_canonical_description_length: "1178"
---

# Middleware Patterns

## Coverage

The discipline of designing Next.js middleware: the one-file-per-project contract (`middleware.ts` at the root or under `src/`, single default export), the Edge Runtime constraints that govern what code can and cannot run there, the `matcher` config that filters which paths trigger middleware, the `NextRequest` / `NextResponse` API surface (cookies, geo, IP, headers), the four response shapes (`next`, `rewrite`, `redirect`, direct response), the canonical pattern library (authentication gate, locale routing, A/B testing, security header injection, geo-routing, bot blocking, request-id correlation), the performance discipline that every matched request pays the cost, and the central design rule: middleware is for cross-cutting concerns that apply across many routes — never for per-route business logic.

## Philosophy

The Pages Router's request lifecycle was: server hits `getServerSideProps`, which returns props, which render the page. The App Router added more layers (Server Components, Server Actions, Route Handlers), but kept one thing constant — they all run *after* the route is resolved.

Middleware runs *before*. It is the only layer where you can intercept a request without knowing which route it will eventually hit. That makes it the right home for concerns that apply across the entire app or large subsets of it: "every request needs an auth check", "every request needs a request-id header", "every request to `/admin/*` needs a role check", "every page needs a CSP nonce".

The architectural trade is **breadth for power**. Middleware:

- Runs on the Edge Runtime — limited APIs, no Node-specific dependencies, no large packages.
- Runs on every matched request — performance ceiling matters because the cost multiplies.
- Has no per-route knowledge until the rewrite/redirect resolves — cannot read route-specific params or query the database for that route's data.
- Cannot read the response body — it sits in front of the response, not over it.

In exchange, it can shape the entire request/response edge in a single place. Done well, it removes ceremony from every route; done badly, it adds latency to every request and concentrates business logic in a file that's hard to test.

**The discipline of middleware is to keep it small, fast, and cross-cutting.** When a piece of logic only applies to one route, it does not belong here. When it requires a database lookup that adds 50ms, it does not belong here. When the code is hard to reason about, it definitely does not belong here.

## The File Contract

```ts
// middleware.ts (project root, or src/ if using src layout)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  // ... transform or gate the request ...
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

- **One file per project.** There is no chain of middleware files. Compose multiple concerns inside a single `middleware` function.
- **Default export.** The named export pattern (`export async function middleware`) and the default export both work; pick one.
- **`config.matcher`** filters which paths trigger middleware. **Critical**: the default — no matcher — runs on every single request including static assets. Always set a matcher.

### Matcher syntax

```ts
export const config = {
  matcher: [
    '/dashboard/:path*',                                          // glob
    '/((?!api|_next/static|_next/image|favicon.ico).*)',          // negative lookahead — everything except these
    {
      source: '/api/admin/:path*',
      missing: [{ type: 'header', key: 'next-action' }],          // exclude Server Action calls
    },
  ],
}
```

Matchers compile to regular expressions at build time. They cannot use runtime values. Complex negative lookaheads are common because the default-matches-everything behavior is rarely what you want — image fetches, static assets, prefetch requests, and webhook routes should usually be excluded.

The biggest middleware footgun is forgetting to exclude `/_next/static` and `/_next/image`, which makes every image fetch run middleware code on the hot path.

## The Four Response Shapes

```ts
import { NextResponse } from 'next/server'

// 1. Pass through — let the request continue to its route
return NextResponse.next()

// 2. Rewrite — internally route to a different path; URL bar unchanged
return NextResponse.rewrite(new URL('/en/about', request.url))

// 3. Redirect — send a 30x to the browser; URL bar changes
return NextResponse.redirect(new URL('/login', request.url))

// 4. Direct response — short-circuit; return a response without hitting any route
return new NextResponse('Forbidden', { status: 403 })
```

Choose based on what the user should see and what should change:

| Goal | Use |
|---|---|
| Continue to the originally requested route, possibly with modified headers/cookies | `next()` (often with `.headers.set()` on the response) |
| Serve a different route's content under the same URL (A/B test, locale variant, feature flag) | `rewrite` |
| Send the user to a different URL (login redirect, canonical redirect, locale-detection redirect) | `redirect` |
| Block the request entirely (rate limit hit, bot blocked, missing auth on protected API) | direct response with appropriate status |

**Rewrite vs redirect** is a load-bearing distinction: rewrites are invisible to the user (the URL stays the same), redirects are visible (the URL changes and the browser does a second request). If you want the user to see they've been moved (`/old-path` → `/new-path`), redirect. If you want to keep their URL and serve different content (A/B variant, internal locale path), rewrite.

## Edge Runtime Constraints

Middleware runs on Edge. Things to know:

| Capability | Available |
|---|---|
| `fetch` | ✅ |
| Web Crypto (`crypto.subtle`, `crypto.randomUUID`) | ✅ |
| Web Streams (`ReadableStream`, `TransformStream`) | ✅ |
| `URL`, `URLSearchParams`, `Request`, `Response` | ✅ |
| `setTimeout` / `setInterval` | ⚠️ best-effort, may not fire after response |
| Node `crypto` module | ❌ |
| Node `fs`, `child_process`, `net`, `dns` | ❌ |
| Most npm packages that aren't pure JS | ❌ |
| Large bundle sizes | ❌ (Vercel: ~1MB ceiling on middleware code) |

Middleware code is bundled and shipped to Edge nodes globally. Cold-start is fast (~10–50ms) but the trade is a tight capability surface. Anything you import — including transitive dependencies — must be Edge-compatible. A single `import` of a Node-only package breaks the build.

**Practical consequence**: don't reach for ORMs, full SDKs, or complex libraries in middleware. Hand-roll the small piece you need (decode a JWT, hash a token, parse a cookie). If the work genuinely needs Node — verifying a webhook signature with a vendor SDK, hitting a database — push it down into a Route Handler or Server Action instead.

## The Canonical Pattern Library

### 1. Authentication gate

```ts
export async function middleware(request: NextRequest) {
  const session = request.cookies.get('session')?.value
  const { pathname } = request.nextUrl

  const isProtected = pathname.startsWith('/dashboard') || pathname.startsWith('/admin')
  if (isProtected && !session) {
    const url = new URL('/login', request.url)
    url.searchParams.set('redirectTo', pathname)
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
}
```

The session cookie is *checked*, not *verified*. Cryptographic verification belongs inside the routes — middleware is for fast cookie presence checks. A signed-cookie verification that requires a JWT library is fine if the library is Edge-compatible; a database lookup to validate the session is not — that 50ms hits every protected page load.

### 2. Locale routing

```ts
const LOCALES = ['en', 'es', 'fr', 'de']
const DEFAULT_LOCALE = 'en'

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const hasLocale = LOCALES.some((l) => pathname.startsWith(`/${l}/`) || pathname === `/${l}`)
  if (hasLocale) return NextResponse.next()

  const accept = request.headers.get('accept-language') ?? ''
  const detected = LOCALES.find((l) => accept.includes(l)) ?? DEFAULT_LOCALE

  return NextResponse.redirect(new URL(`/${detected}${pathname}`, request.url))
}
```

A first-visit user lands on `/about`, gets redirected to `/en/about`. Subsequent visits to locale-prefixed paths pass through. The redirect-once pattern keeps the URL canonical and lets the rest of the app assume locale is in the path.

### 3. A/B testing via rewrite

```ts
export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname !== '/pricing') return NextResponse.next()

  let variant = request.cookies.get('pricing-variant')?.value
  if (!variant) {
    variant = Math.random() < 0.5 ? 'a' : 'b'
  }

  const url = new URL(`/pricing-${variant}`, request.url)
  const response = NextResponse.rewrite(url)
  response.cookies.set('pricing-variant', variant, { maxAge: 60 * 60 * 24 * 30 })
  return response
}
```

The user sees `/pricing` in their URL bar but receives `/pricing-a` or `/pricing-b`. The cookie pins their variant so subsequent visits are consistent. The rewrite preserves the canonical URL for analytics and sharing.

### 4. Security header injection (with per-request CSP nonce)

```ts
export async function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64')

  const csp = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'`,
    `style-src 'self' 'nonce-${nonce}'`,
    `img-src 'self' blob: data:`,
    `font-src 'self'`,
    `object-src 'none'`,
    `base-uri 'self'`,
    `form-action 'self'`,
    `frame-ancestors 'none'`,
    `upgrade-insecure-requests`,
  ].join('; ')

  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-nonce', nonce)
  requestHeaders.set('content-security-policy', csp)

  const response = NextResponse.next({ request: { headers: requestHeaders } })
  response.headers.set('content-security-policy', csp)
  response.headers.set('x-content-type-options', 'nosniff')
  response.headers.set('referrer-policy', 'strict-origin-when-cross-origin')
  response.headers.set('permissions-policy', 'camera=(), microphone=(), geolocation=()')
  return response
}
```

The nonce flows to the request headers (so Server Components can read it via `headers()` and inject it into `<script>` tags) and to the response headers (so the browser enforces the CSP). The policy itself is just an example; the actual rules belong to the broader security strategy in `security-fundamentals`.

### 5. Geo-routing

```ts
export async function middleware(request: NextRequest) {
  const country = request.geo?.country ?? 'US'   // populated by Vercel

  if (country === 'GB' && !request.nextUrl.pathname.startsWith('/uk')) {
    return NextResponse.redirect(new URL(`/uk${request.nextUrl.pathname}`, request.url))
  }

  return NextResponse.next()
}
```

`request.geo` is populated by Vercel from the request's IP-derived location. On other hosts it may be undefined — read it defensively.

### 6. Bot blocking

```ts
const BLOCKED_AGENTS = [/AhrefsBot/i, /SemrushBot/i, /MJ12bot/i]

export async function middleware(request: NextRequest) {
  const ua = request.headers.get('user-agent') ?? ''
  if (BLOCKED_AGENTS.some((re) => re.test(ua))) {
    return new NextResponse('Forbidden', { status: 403 })
  }
  return NextResponse.next()
}
```

UA strings are trivially spoofable — bot blocking via user-agent works for honest crawlers but does not stop adversaries. Use this for noise reduction, not security.

### 7. Request-ID correlation

```ts
export async function middleware(request: NextRequest) {
  const requestId = request.headers.get('x-request-id') ?? crypto.randomUUID()
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-request-id', requestId)

  const response = NextResponse.next({ request: { headers: requestHeaders } })
  response.headers.set('x-request-id', requestId)
  return response
}
```

The request-id flows through to the route (readable via `headers()`) and back out to the client (visible in DevTools). Pair with structured logging that includes the id, and you get end-to-end traceability.

## Composing Multiple Concerns

There is one `middleware.ts`. Combine concerns inside it — typically in a clear order:

```ts
export async function middleware(request: NextRequest) {
  // 1. Block bots first — fast reject
  const ua = request.headers.get('user-agent') ?? ''
  if (BLOCKED_AGENTS.some((re) => re.test(ua))) {
    return new NextResponse('Forbidden', { status: 403 })
  }

  // 2. Locale detection — redirect once for first-visit users
  const localeRedirect = applyLocaleRouting(request)
  if (localeRedirect) return localeRedirect

  // 3. Auth gate — redirect to login for protected routes
  const authRedirect = applyAuthGate(request)
  if (authRedirect) return authRedirect

  // 4. Pass through with security headers + request-id
  return applyHeaders(request)
}
```

Each helper returns either a short-circuit `NextResponse` or `null` (continue). The shape is a small chain of guards; the file stays readable. When the chain grows past ~5 concerns, it's a signal that the middleware is doing too much — push something down to per-route logic or to a separate request-time hook.

## Performance Discipline

Every matched request pays the middleware cost. Three rules:

1. **Tune the matcher.** If only `/dashboard/*` needs auth, match only `/dashboard/*`. Don't run auth checks against image fetches.
2. **Cap the time budget.** Target <10ms p99 for middleware execution. Slow middleware degrades every page on the site.
3. **No database calls.** A network round-trip in middleware is a tax on every request. Cache aggressively; use signed cookies that carry the data middleware needs without a lookup; defer DB checks to the route.

The performance budget is invisible until you load-test the site and see middleware dominate the latency profile. Build it in from the start.

## Common Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---|---|---|
| No matcher — middleware runs on `/_next/static`, `/_next/image`, `/favicon.ico` | Adds latency to every image fetch and static asset | Set a matcher with negative lookahead excluding `_next` paths and assets |
| Database query in middleware | Network round-trip on every request | Use signed cookies that carry the data, or push the lookup down to the route |
| Putting per-route business logic in middleware | Centralized file that hides the logic from the route that owns it | Move to the route; keep middleware for genuine cross-cutting |
| Importing a Node-only package | Edge build fails | Use Edge-compatible alternatives, or move the work to a Route Handler |
| Verifying a JWT signature against a remote JWKS endpoint without caching | Network call per request | Cache the JWKS in memory; or defer verification to the route |
| `redirect` when `rewrite` was meant (or vice versa) | URL changes when it shouldn't, or stays the same when it should | Choose based on whether the user should see the URL change |
| Forgetting to copy headers to the response when modifying request headers | Request-side changes invisible to client | Use `NextResponse.next({ request: { headers: ... } })` AND set the same on `response.headers` if the client needs to see them |
| Setting cookies on the request — middleware can't modify the request cookies the client sees | Cookie set silently lost | Set cookies on the response via `response.cookies.set(...)` |
| Running middleware on webhook routes that need raw body access | Middleware can consume the body or otherwise interfere with HMAC verification | Exclude webhook paths from the matcher |
| Single 100-line middleware doing 8 different things | Untestable, slow, hard to reason about | Decompose into named helpers; consider whether some concerns belong per-route |

## Verification

After applying this skill, verify:

- [ ] `config.matcher` is set and excludes `_next/static`, `_next/image`, `favicon.ico`, and any other paths that don't need middleware (typically webhooks).
- [ ] No database queries or other I/O that adds >10ms to the request happen inside middleware.
- [ ] All imported packages are Edge-Runtime-compatible (no Node `crypto`, `fs`, `child_process`, `net`).
- [ ] Cookies that need to reach the client are set on the response (`response.cookies.set`), not on the request.
- [ ] Modified request headers use `NextResponse.next({ request: { headers } })` so they flow to the route.
- [ ] The choice between `rewrite` and `redirect` matches whether the URL should visibly change.
- [ ] Webhook routes are excluded from the matcher to preserve raw-body access.
- [ ] Multiple concerns are decomposed into named helpers; one concern per helper.
- [ ] Auth checks are fast cookie/signature checks, not database lookups — deeper verification is deferred to the route.
- [ ] Security-header injection (if used) coordinates with the broader security strategy defined in `security-fundamentals`.

## Grounding Sources

- Next.js docs — [Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware). The canonical reference for the `middleware.ts` convention.
- Next.js docs — [Matcher config](https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher). The path-filtering rules.
- Vercel docs — [Edge Runtime API reference](https://vercel.com/docs/functions/runtimes/edge-runtime). The capability surface middleware runs against.
- MDN — [Fetch API: Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) and [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response). The Web-standard interface underlying `NextRequest`/`NextResponse`.
- RFC 9110 — [HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110). The protocol middleware operates on — methods, status codes, headers.
- OWASP — [Secure Headers Project](https://owasp.org/www-project-secure-headers/). The canonical reference for the security-header set middleware can inject.
- Vercel — [Building a strict CSP with nonces in Next.js](https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy). The canonical per-request nonce pattern.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Per-route HTTP endpoint logic — JSON APIs, webhook handlers, streaming responses | `route-handler-design` | Route Handlers own per-route per-method logic; middleware owns cross-cutting preprocessing. |
| Internal mutations triggered from this app's UI | `server-actions-design` | Server Actions are the in-app mutation surface; middleware sits upstream of them but does not replace them. |
| Understanding what each HTTP status or method means in the abstract | `http-semantics` | http-semantics owns the protocol; this skill owns honoring it in middleware. |
| Designing the full Content Security Policy or the broader hardening discipline | `security-fundamentals` | security-fundamentals owns the policy; middleware is one delivery surface. |
| The cross-cutting streaming model (Web Streams, SSE, backpressure) | `streaming-architecture` | Middleware can set headers for streamed responses but does not author the streaming logic. |
| The serialization/directive mechanics of `'use client'` and `'use server'` | `client-server-boundary` | Different boundary — that's the bundler component split, not the HTTP request edge. |
| The full webhook reliability story (HMAC verification, idempotency, retries) | `webhook-integration` | Webhook routes should generally be excluded from middleware; their handler owns the reliability discipline. |
