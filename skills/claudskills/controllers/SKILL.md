---
name: remix-controllers
description: Controllers in Remix v3 — the `.tsx` files under `app/controllers/` that handle requests. Covers the `Controller<typeof routes.X, AppContext>` shape, action handler signatures (`{ get, params, request, url }`), reading middleware-provided values with `get(Database)` / `get(Session)` / `get(Auth)` / `get(FormData)`, returning responses via `render(<Page/>)` / `redirect(...)` / `Response.json(...)`, nested controllers, per-controller middleware (`requireAuth`, etc.), and the typed `routes.X.href(params)` URL builder. Load whenever the user is creating, editing, or debugging anything under `app/controllers/`, or comparing to Express route handlers / Next.js page+route handlers / Rails controllers / Hono handlers. Also load when the user asks "where does business logic go" or "how do I get the current user in an action".
---

# Controllers

A controller is a `.tsx` file that exports a `default { actions, middleware? } satisfies Controller<typeof routes.X, AppContext>`. Controllers mirror the shape of the route map and are bound to it in `app/router.ts` with `router.map(routes.X, controllerX)`.

## Imports

```ts
import type { Controller } from 'remix/fetch-router'
import { redirect } from 'remix/response/redirect'
import * as s from 'remix/data-schema'
import * as f from 'remix/data-schema/form-data'
import { Database } from 'remix/data-table'
import { Session } from 'remix/session'
import { Auth } from 'remix/auth-middleware'

import type { AppContext } from '../router.ts'
import { routes } from '../routes.ts'
import { render } from '../utils/render.tsx'
```

## Minimal controller

```tsx
// app/controllers/home.tsx
import type { Controller } from 'remix/fetch-router'
import type { AppContext } from '../router.ts'
import { routes } from '../routes.ts'
import { render } from '../utils/render.tsx'
import { HomePage } from '../views/home-page.tsx'

export default {
  actions: {
    index() {
      return render(<HomePage />)
    },
  },
} satisfies Controller<typeof routes.home, AppContext>
```

## Action signature

Each action receives an object with:

| Field      | Type / What it is                                  |
|-----------|----------------------------------------------------|
| `get`     | `<K>(key: Key<K>) => K` — pull values from context (e.g. `get(Database)`) |
| `params`  | Typed params parsed from the route pattern         |
| `request` | The raw Web `Request`                              |
| `url`     | The parsed `URL` of the request                    |

Return value is a `Response` (usually built via `render(<Page/>)`, `redirect(...)`, or a manual `new Response(...)`).

## Mirroring a route map

If a route map has nested entries, the controller mirrors that shape:

```tsx
// app/controllers/admin/books/controller.tsx
import type { Controller } from 'remix/fetch-router'
import * as s from 'remix/data-schema'
import * as f from 'remix/data-schema/form-data'
import { Database } from 'remix/data-table'
import { redirect } from 'remix/response/redirect'

import type { AppContext } from '../../../router.ts'
import { routes } from '../../../routes.ts'
import { books } from '../../../data/schema.ts'
import { render } from '../../../utils/render.tsx'

import { AdminBooksIndexPage } from './views/index-page.tsx'
import { AdminBookShowPage }  from './views/show-page.tsx'
import { AdminBookNewPage }   from './views/new-page.tsx'

const bookSchema = f.object({
  slug:          f.field(s.string()),
  title:         f.field(s.string()),
  author:        f.field(s.string()),
  description:   f.field(s.string()),
  price:         f.field(s.string()),
  genre:         f.field(s.string()),
  isbn:          f.field(s.string()),
  publishedYear: f.field(s.string()),
  cover:         f.field(s.string().nullable()),
  inStock:       f.field(s.boolean()),
})

export default {
  actions: {
    async index({ get }) {
      const db = get(Database)
      const allBooks = await db.findMany(books, { orderBy: ['id', 'asc'] })
      return render(<AdminBooksIndexPage books={allBooks} />)
    },

    new() {
      return render(<AdminBookNewPage />)
    },

    async create({ get }) {
      const db = get(Database)
      const formData = get(FormData)
      const parsed = s.parseSafe(bookSchema, formData)
      if (!parsed.success) {
        return render(<AdminBookNewPage errors={parsed.issues} />, { status: 400 })
      }
      const { price, publishedYear, cover, ...rest } = parsed.value
      await db.create(books, {
        ...rest,
        price: parseFloat(price),
        cover_url: cover ?? '/images/placeholder.jpg',
        image_urls: JSON.stringify([]),
        published_year: parseInt(publishedYear, 10),
      })
      return redirect(routes.admin.books.index.href())
    },

    async show({ get, params }) {
      const db = get(Database)
      const book = await db.find(books, params.bookId)
      if (!book) return new Response('Not found', { status: 404 })
      return render(<AdminBookShowPage book={book} />)
    },
  },
} satisfies Controller<typeof routes.admin.books>
```

## Controller-level middleware

A controller can declare middleware that runs before *any* of its actions (and any nested sub-controllers). Useful for guards like `requireAuth` or for hydrating per-request state.

```tsx
import { requireAuth } from 'remix/auth-middleware'

export default {
  middleware: [requireAuth()],
  actions: {
    index({ get }) { /* … */ },
    settings: {
      // nested controller — its own middleware can stack
      middleware: [/* … */],
      actions: { /* … */ },
    },
  },
} satisfies Controller<typeof routes.account>
```

Execution order: global router middleware → matched controller chain (parent → child) → action.

## Reading typed context with `get(Key)`

Anything a middleware puts on the request context is fetched in actions via `get(Key)`. Common keys:

```ts
const db       = get(Database)   // remix/data-table — provided by your db middleware
const session  = get(Session)    // remix/session — provided by session() middleware
const formData = get(FormData)   // a parsed FormData — provided by formData() middleware
const auth     = get(Auth)       // current Auth state — provided by auth() middleware
```

If a key is missing from context the call throws. That's a wiring bug — fix the middleware stack in `app/router.ts`.

## Common return shapes

```tsx
// HTML page
return render(<Page />)

// HTML with a non-200 status (validation error, conflict, not-found)
return render(<NewBookPage errors={parsed.issues} />, { status: 400 })

// Redirect (after a successful POST, login, etc.)
return redirect(routes.admin.books.index.href())

// Bare response for 404s, JSON APIs, downloads, etc.
return new Response('Not found', { status: 404 })
return Response.json({ ok: true })
```

`routes.X.href(params?)` produces a typed URL. Always prefer it over hand-rolled paths — the compiler will tell you when you've broken a link.

## Returning HTML without JSX

For small endpoints (webhooks, RSS, email previews), skip the JSX pipeline and use the `html` tagged template:

```ts
import { html } from 'remix/html-template'
import { createHtmlResponse } from 'remix/response/html'

return createHtmlResponse(html`<h1>Hello ${name}</h1>`)
```

See [templating](../templating/SKILL.md) for the full story.

## Further reading

- `references/controller-types.md` — `Controller<Routes, Context>`, action shape, nested mirror rules
- `references/render-utility.md` — building `app/utils/render.tsx` around `renderToStream`
- `references/context-keys.md` — the standard set of `Key`s exposed by built-in middleware
- See also: [templating](../templating/SKILL.md) (HTML responses without JSX), [headers](../headers/SKILL.md) (typed parsers for Accept, CacheControl, etc.)
