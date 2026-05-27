---
name: remix-templating
description: Server-side HTML templating in Remix v3 via `remix/html-template` — the `` html`...` `` tagged template literal with automatic XSS-safe escaping, `html.raw` for trusted fragments, composable `SafeHtml` branded values, the `isSafeHtml` type guard, and integration with `createHtmlResponse` from `remix/response/html` for endpoints that return HTML without spinning up the JSX runtime. Load whenever the user is building HTML responses without JSX (webhooks, RSS feeds, sitemaps, email bodies, OG/Twitter previews, HTMX fragments, server-rendered snippets), generating safe HTML from user input, composing reusable HTML helpers, deciding when to use JSX vs templates, or about to install `handlebars`, `ejs`, `mustache`, `pug`, `nunjucks`, `lit-html`, `escape-html`, `xss`, `sanitize-html`, `dompurify` (for server output). For full-page interactive UIs, use /remix:ui (JSX) instead.
---

# Templating

`remix/html-template` is a safe-by-default tagged template literal for building HTML strings. Use it when you want to return HTML without spinning up the JSX runtime — small endpoints, email bodies, RSS feeds, snippets sent to HTMX-style clients.

## Imports

```ts
import { html, isSafeHtml, type SafeHtml } from 'remix/html-template'
import { createHtmlResponse } from 'remix/response/html'
```

## XSS-safe by default

```ts
const userInput = '<script>alert("XSS")</script>'
const greeting = html`<h1>Hello ${userInput}!</h1>`

String(greeting)
// → '<h1>Hello &lt;script&gt;alert("XSS")&lt;/script&gt;!</h1>'
```

Every interpolated value is escaped. You don't have to remember.

## Composing fragments

`SafeHtml` values nested into another `html` template don't get double-escaped:

```ts
const title = html`<h1>My Title</h1>`
const para  = html`<p>Hello ${userName}</p>`

const page = html`
  <main>
    ${title}
    ${para}
  </main>
`
```

The branded `SafeHtml` type tells `html` "I'm already safe, don't escape me again."

## `html.raw` — when you know it's trusted

For pre-escaped HTML or trusted assets (e.g. an SVG icon you control):

```ts
const icon = '<svg viewBox="0 0 16 16">...</svg>'   // from your codebase, not user input
const button = html.raw`<button>${icon} Click me</button>`
```

**Never** use `html.raw` with user input or any value that traversed the network.

## Returning HTML from an action

Pair with `createHtmlResponse` from `remix/response/html`:

```ts
import { createHtmlResponse } from 'remix/response/html'

export function contactPage(ctx: RequestContext) {
  return createHtmlResponse(html`
    <!doctype html>
    <html lang="en">
      <head><title>Contact</title></head>
      <body>
        <h1>Contact us</h1>
        <form method="post" action="${routes.contact.action.href()}">
          <input type="hidden" name="_csrf" value="${getCsrfToken(ctx)}" />
          <input name="email" type="email" required />
          <textarea name="message" required></textarea>
          <button type="submit">Send</button>
        </form>
      </body>
    </html>
  `)
}
```

`createHtmlResponse` sets `Content-Type: text/html; charset=utf-8` and accepts a `SafeHtml`, plain string, or `ReadableStream`.

## Arrays interpolate cleanly

```ts
const items = ['apple', 'banana', 'cherry']
const list = html`
  <ul>
    ${items.map((item) => html`<li>${item}</li>`)}
  </ul>
`
```

Arrays of `SafeHtml` are joined without separators. Use `.join('')` only if you specifically need a separator.

## When to use JSX vs `html`

| Use JSX (`remix/ui`) when... | Use `html` template when... |
|---|---|
| Multi-page app with shared `Document` shell | One-off HTML responses (webhooks, emails, RSS) |
| Components compose visually | Output is template-shaped, no component tree |
| You want client hydration | Server-only render, no JS |
| You want the two-phase setup/render model | You're building a string |

Both can coexist — a JSX page can include `html.raw\`...\`` for a trusted snippet; an `html`-based response can read from helpers that return `SafeHtml`.

## Type guard

```ts
function render(value: unknown) {
  if (isSafeHtml(value)) {
    return createHtmlResponse(value)
  }
  return new Response(String(value), { headers: { 'Content-Type': 'text/plain' } })
}
```

## Further reading

- [`references/safe-html.md`](./references/safe-html.md) — full escape semantics, composition rules, common patterns
- See also: [ui](../ui/SKILL.md) for JSX, [controllers](../controllers/SKILL.md) for the action context, [security](../security/SKILL.md) for `getCsrfToken`
