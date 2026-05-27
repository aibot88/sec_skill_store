---
name: remix-middlewares
description: Reference card for every middleware shipped by Remix v3 — `logger`, `compression`, `staticFiles`, `formData`, `methodOverride`, `session`, `csrf`, `cop`, `cors`, `asyncContext`, `auth`, `requireAuth` — with canonical stack ordering and pointers to deep docs. Plus the contract for writing your own. Load whenever the user is composing or editing the middleware stack in `app/router.ts`, debugging request flow, choosing between similar middlewares (`cop` vs `csrf`, custom vs built-in), or about to install Express middlewares (helmet, morgan, body-parser, cookie-parser, multer) — Remix already ships equivalents. Also load if the user asks "what middleware comes with Remix?" or "where does X go in the stack?".
---

# Middlewares

Every middleware shipped by `remix`, in canonical stack order (top runs first). The table is the answer to "do I need to install X?" — almost always no, Remix already has it.

## The canonical stack

| Order | Middleware | Import | What it does | Deep doc |
|------:|---|---|---|---|
| 5  | `cors()`           | `remix/cors-middleware`           | Adds CORS response headers; short-circuits preflight `OPTIONS`. **First** so preflights skip everything else. | [security](../security/SKILL.md) |
| 10 | `logger()`         | `remix/logger-middleware`          | Request/response logging (method, path, status, duration). | this skill |
| 15 | `cop()`            | `remix/cop-middleware`             | Tokenless cross-origin protection via `Sec-Fetch-Site`/`Origin`. Cheap reject before session work. | [security](../security/SKILL.md) |
| 20 | `compression()`    | `remix/compression-middleware`     | gzip/br encoding for text-like responses. | this skill |
| 30 | `staticFiles(...)` | `remix/static-middleware`          | Serves `./public` and exits chain on hit. | this skill |
| 40 | `formData({...})`  | `remix/form-data-middleware`       | Parses `multipart/form-data` and `application/x-www-form-urlencoded`; streams file uploads to a handler. | [forms](../forms/SKILL.md) |
| 50 | `methodOverride()` | `remix/method-override-middleware` | Promotes `_method=PUT/PATCH/DELETE` form field to the HTTP method. **After `formData`.** | this skill |
| 60 | `session(...)`     | `remix/session-middleware`         | Loads + saves the session cookie. **Before auth and csrf.** | [sessions](../sessions/SKILL.md) |
| 65 | `csrf()`           | `remix/csrf-middleware`            | Synchronizer-token CSRF validation. **After `session`** (token lives in session). | [security](../security/SKILL.md) |
| 70 | `asyncContext()`   | `remix/async-context-middleware`   | Stores `RequestContext` in `AsyncLocalStorage` so helpers can call `getContext()` without threading. | this skill |
| 80 | `auth({...})`      | `remix/auth-middleware`            | Resolves identity from session/bearer schemes; populates `Auth` on the context. | [auth](../auth/SKILL.md) |
| —  | `requireAuth(...)` | `remix/auth-middleware`            | Per-route guard. Returns 401/redirect when unauthenticated. | [auth](../auth/SKILL.md) |

You'll write your own middlewares too — `loadDatabase()`, `loadCurrentTenant()`, request-id, error boundary, etc. Those go at the end (after `asyncContext`, before `auth` if they enrich the context for auth schemes). See [references/custom-middleware.md](./references/custom-middleware.md).

## Production stack — copy/paste

```ts
import { asyncContext }   from 'remix/async-context-middleware'
import { compression }    from 'remix/compression-middleware'
import { createRouter }   from 'remix/fetch-router'
import { formData }       from 'remix/form-data-middleware'
import { logger }         from 'remix/logger-middleware'
import { methodOverride } from 'remix/method-override-middleware'
import { staticFiles }    from 'remix/static-middleware'
import { session }        from 'remix/session-middleware'
import { csrf }           from 'remix/csrf-middleware'

export function createAppRouter() {
  const middleware = []

  if (process.env.NODE_ENV !== 'production') middleware.push(logger())
  middleware.push(compression())
  middleware.push(staticFiles('./public', { cacheControl: 'public, max-age=3600' }))
  middleware.push(formData({}))
  middleware.push(methodOverride())
  middleware.push(session(sessionCookie, sessionStorage))
  middleware.push(csrf())
  middleware.push(asyncContext())
  middleware.push(loadDatabase())     // your custom middleware
  middleware.push(loadAuth())         // wraps auth({...schemes})

  return createRouter({ middleware })
}
```

Add `cors()` first if your API is consumed by browsers at other origins. Add `cop()` after `logger` if you want fast tokenless cross-origin rejection in front of `csrf()`.

## When NOT to use the canonical stack

- **Pure JSON API.** Drop `staticFiles`, `formData`, `methodOverride`. Maybe drop `csrf` (use bearer tokens + `cors`).
- **Serverless edge.** Drop `compression` (your platform's CDN handles it). Drop `staticFiles` (CDN handles it).
- **Webhook endpoint.** Skip `session`, `csrf`, `auth`. Validate the sender's signature manually inside the handler.

## Cross-cutting tips (deep doc: [references/ordering.md](./references/ordering.md))

- **`logger` first** — so you log everything including static hits and rejects.
- **`compression` early** — once headers are written, can't add `Content-Encoding`.
- **`staticFiles` before business logic** — let `/assets/*` exit cheap.
- **`methodOverride` after `formData`** — needs the parsed `_method` field.
- **`session` before `auth` and `csrf`** — both read from the session.
- **`asyncContext` high enough** that downstream middleware can use `getContext()`.

## Built-in middlewares that don't belong in the canonical stack

Some middlewares are situational, not always-on:

| Middleware | Use it when |
|---|---|
| `requireAuth(...)` | Per-protected-route or per-controller, not global |
| `cors(...)` | API needs cross-origin access from browser JS |
| `cop(...)` | Want tokenless cross-origin defense |

## Writing your own

A middleware is `(ctx, next) => Promise<Response>`. Set values on the context with `ctx.set(Key, value)`; downstream handlers read with `ctx.get(Key)`. See [references/custom-middleware.md](./references/custom-middleware.md) for patterns (inject context, short-circuit, post-process headers, error boundary, request-id, etc.).

## Further reading

- [references/built-ins.md](./references/built-ins.md) — full options for every shipped middleware
- [references/custom-middleware.md](./references/custom-middleware.md) — patterns for writing your own
- [references/ordering.md](./references/ordering.md) — common ordering bugs, what comes before/after what
- Sub-skills with their own deep doc: [security](../security/SKILL.md), [sessions](../sessions/SKILL.md), [auth](../auth/SKILL.md), [forms](../forms/SKILL.md)
