---
name: remix-cookies
description: Cookies in Remix v3 via `remix/cookie` — the low-level building block sessions, auth, and CSRF build on. `createCookie(name, options)` for signed cookies (HMAC `secrets` array, rotation playbook), `parse(headerValue)` from incoming requests, `serialize(value, props?)` for `Set-Cookie` headers, plus attributes (`httpOnly`, `secure`, `sameSite: 'Lax' | 'Strict' | 'None'`, `maxAge`, `expires`, `path`, `domain`, `priority`, `partitioned`). Load whenever the user is reading/writing cookies directly (locale prefs, dark-mode flag, consent banner, A/B bucket, "remember me", feature flag), configuring the session cookie, rotating signing secrets, or debugging cookies missing in production (`secure: true` over HTTP, `SameSite` mismatch). For signed sessions see /remix:sessions; for the typed `Cookie` / `SetCookie` header parsers see /remix:headers.
---

# Cookies

`remix/cookie` is the low-level building block. Sessions, auth, and CSRF protection all hang off `Cookie` instances internally — and you can use them directly for anything else (locale prefs, dark-mode flag, A/B bucket, …).

## Imports

```ts
import { createCookie } from 'remix/cookie'
```

## Create a cookie

```ts
const sessionCookie = createCookie('__session', {
  secrets:  ['s3cret1'],         // required for signed cookies
  httpOnly: true,
  secure:   true,
  sameSite: 'Lax',
  path:     '/',
  maxAge:   60 * 60 * 24 * 30,   // 30 days
})
```

| Option     | Notes                                                                    |
|-----------|--------------------------------------------------------------------------|
| `secrets`  | Array of HMAC keys. First entry signs new cookies. Others verify old ones — that's how rotation works (prepend a new key, leave the old one for a transition window). |
| `httpOnly` | Hides the cookie from JS — set to `true` for anything sensitive.          |
| `secure`   | HTTPS-only. `true` in prod, `false` for local HTTP.                        |
| `sameSite` | `'Strict'` / `'Lax'` / `'None'` (capitalised per the type). `'Lax'` is the safe default for top-level nav flows. |
| `maxAge`   | Seconds. Omit for a session cookie (dies with the browser).                |
| `path`     | Defaults to `/`.                                                         |
| `domain`   | Set for cross-subdomain cookies.                                          |

## Parse from a request

```ts
const value = await sessionCookie.parse(request.headers.get('Cookie'))
// value is `null` if the cookie is absent or the signature is invalid
```

## Serialize for a response

```ts
const setCookie = await sessionCookie.serialize({ userId: 42 })

return new Response('OK', {
  headers: { 'Set-Cookie': setCookie },
})
```

Pass an empty value + `maxAge: 0` to clear a cookie.

## Secret rotation

You're rotating a cookie secret. The procedure:

1. **Prepend** the new secret to the `secrets` array. Don't replace.
   ```ts
   secrets: [process.env.NEW_SECRET!, process.env.OLD_SECRET!]
   ```
2. Deploy. All *new* cookies are signed with `NEW_SECRET`. Existing cookies signed with `OLD_SECRET` still verify.
3. After the rollout window (`maxAge` is a good upper bound), drop `OLD_SECRET`.

If you replace instead of prepending, every active session is invalidated.

## Sessions use this under the hood

```ts
import { createCookie } from 'remix/cookie'
import { createCookieSessionStorage } from 'remix/session/cookie-storage'
import { session } from 'remix/session-middleware'

const sessionCookie = createCookie('__session', {
  secrets: [process.env.SESSION_SECRET!],
  httpOnly: true,
  secure:   true,
  sameSite: 'Lax',
})
const sessionStorage = createCookieSessionStorage()

createRouter({ middleware: [session(sessionCookie, sessionStorage)] })
```

The session middleware calls `parse` on the way in and `serialize` on the way out for you.

## A self-contained example — locale preference

```ts
// app/cookies/locale.ts
import { createCookie } from 'remix/cookie'

export const localeCookie = createCookie('locale', {
  maxAge: 60 * 60 * 24 * 365,   // 1 year
  path:   '/',
  sameSite: 'Lax',
  // No `secrets` → unsigned, fine for a non-sensitive preference
})
```

```ts
// reading
const locale = (await localeCookie.parse(request.headers.get('Cookie'))) ?? 'en'

// writing
return new Response(html, {
  headers: { 'Set-Cookie': await localeCookie.serialize('fr') },
})
```

## Common pitfalls

- **Forgetting `secrets` on a session cookie.** Signed cookies *require* `secrets`. Sessions in particular must be signed.
- **Mixing signed and unsigned.** A given cookie is either signed or not — don't flip mid-deployment without rotating the name.
- **`secure: true` over local HTTP.** Browsers silently drop the cookie. Use `secure: process.env.NODE_ENV === 'production'`.
- **Long `maxAge` on JWT-style sessions.** If you store auth state in the cookie itself, treat the cookie as a credential and keep `maxAge` short or pair with a server-side store.

## Further reading

- `references/options.md` — every attribute, with browser-compatibility notes
- `references/rotation.md` — secret-rotation playbook
- See also: [sessions](../sessions/SKILL.md), [auth](../auth/SKILL.md)
