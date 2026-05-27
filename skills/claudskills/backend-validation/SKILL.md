---
name: backend-validation
description: Use this skill when validating a backend API or WebSocket endpoint end-to-end, including acquiring an OIDC bearer token for authenticated calls. Trigger whenever the user asks to test/validate/smoke-check a backend, write a Hurl test, hit a WebSocket, acquire an access token, exercise an OIDC flow, debug a 401, or verify an endpoint works with real auth. Applies to projects that use Hurl for HTTP tests, websocat for WebSocket probes, and oauth2c or curl-based flows for token acquisition (Authentik, Keycloak, Okta, Auth0, any RFC 6749 / OIDC Core provider). Prefer this skill over ad-hoc curl + bash when the user has more than one endpoint to check, chained auth flows, or anything resembling a regression test — because the Hurl + cached-refresh-token pattern is 10× less code and survives the next session.
---

# Backend Validation

For CLI-driven validation of backends behind OIDC auth. Deliberately tool-specific — Hurl, websocat, oauth2c. If the project has already picked Bruno/Postman/Insomnia, stop and use those instead; don't fork the tooling.

## Framing before you test

Before picking flags and writing assertions, work the change as a thinking exercise — the tools come after.

1. **What feature does this change represent?** State it as a user-visible effect, not a function signature. If you can't state it that way, you don't yet know what to validate.
2. **What does success look like?** Be concrete — "a new session appears with status 'active' within 2s" beats "it works." Vague success criteria produce vague tests.
3. **Validate in two passes.** User-lens: drive the feature as a user would (for backend, that often means exercising the endpoints the UI calls, in the order and shape the UI sends them). System-lens: verify the system did the right thing underneath — status codes, DB rows, WS events, logs clean. Bugs hide in exactly one of these; running both catches them.
4. **Check 2–3 adjacent paths.** A `/sessions POST` probably affects the `/sessions/mine` listing, any subscribed realtime channel, caches. Don't attempt full regression — pick nearby behaviors that would obviously break.
5. **Cover realistic failure modes** (missing auth, invalid body, not-found, race on a shared resource), not exhaustive ones. One test per failure class beats ten happy-path tests.
6. **Skip what can't plausibly break from this change.** Judgment, not ritual.

## When in doubt, run `--help`

Flags drift between tool versions and training data. For anything beyond the common invocations below — reconnect behavior, mTLS, a subprotocol you haven't used, a new oauth2c flag — run `hurl --help`, `websocat --help`, or `oauth2c --help` first rather than guessing. One `--help` call is cheaper than a debug session chasing a flag that changed meaning.

## The stack

The tools are committed: **Hurl** for HTTP tests, **websocat** for WebSocket probes, **oauth2c** for OIDC token flows. All three are cross-platform (Rust/Go binaries). The only OS-specific surface is how the refresh token is cached:

- **macOS**: `security add-generic-password` / `security find-generic-password` (macOS Keychain)
- **Linux**: `secret-tool` (libsecret / GNOME Keyring) — install with `apt install libsecret-tools` or equivalent
- **Windows**: `cmdkey` + PowerShell's `CredentialManager` module, or WSL users reuse the Linux path

The reference script (`references/token-script.sh`) uses the macOS `security` command directly. On Linux/Windows, swap those two calls for the platform equivalent; the auth flow itself is identical.

## The three orthogonal concerns

Keep these separate in your head and in the code:

1. **Token acquisition** — auth-code + PKCE with the refresh token cached in OS-native secret storage (see above). No passwords in env files, no ROPC against public clients (it fails — see below).
2. **HTTP validation** — `.hurl` files with `[Captures]` for chaining auth into calls and `[Asserts]` for pass/fail.
3. **WebSocket probes** — `websocat` one-shots with `Authorization: Bearer` header; scripted with `-n1`, interactive without.

## Decision tree

| Situation | Reach for |
|---|---|
| "Does this endpoint work with auth?" | `oauth2c` for token, then `hurl` or `xh` |
| "Is the WebSocket responding?" | `websocat` with bearer header |
| "Write tests for this API" | `.hurl` files with `[Captures]` + `[Asserts]` |
| Debugging a 401 | Decode JWT claims; check `iss`, `aud`, `exp`, `email_verified` |

## The auth-code + PKCE pattern (why and how)

Public PKCE clients — which most SPAs and mobile apps use at runtime — **refuse ROPC (password grant)**. Don't waste cycles trying `grant_type=password`: Authentik and most IdPs return `invalid_grant` regardless of whether credentials are right, identical error for every failure mode.

The pattern that works: authorization-code + PKCE for the initial browser login, then a cached refresh_token for silent renewals. Oauth2c handles the browser dance; the resulting refresh_token lives in OS secret storage (service name `<project>-refresh-token`) and gets rotated on each use.

Non-obvious flags:

- **`--prompt login`** on oauth2c forces a fresh sign-in prompt. Without it, an already-logged-in admin session in the browser gets used — the cached token ends up being for the wrong identity. This bit me once and will bite again without the flag.
- **`--login-hint <username>`** pre-fills the username field, useful when multiple accounts exist.
- **`offline_access`** scope is required to receive a `refresh_token` at all.
- **Redirect URI** — the OIDC provider must whitelist `http://localhost:9876/callback` (oauth2c's default) in Strict mode.
- **`email_verified: true`** must be set on the test user's attributes in the IdP. Many backends reject JWTs where this claim is false. In Authentik: Directory → Users → Attributes → `email_verified: true` (plain YAML, not wrapped in brackets — that's a list).

A full reference script lives in `references/token-script.sh`.

## Hurl patterns

One file per scenario (`smoke.hurl`, `sessions-crud.hurl`). Parameterize `base_url` and `token` as `--variable` so the same file runs anywhere. `[Captures]` chains response values into later requests; `[Asserts]` defines pass/fail.

```hurl
GET {{base_url}}/api/me
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.id" isString
```

Run: `hurl --test --variable token=$TOKEN --variable base_url=$BASE_URL *.hurl`.

See `references/hurl-patterns.md` for captures chaining, retries, GraphQL, parallel runs, CI output.

## WebSocket patterns

The one thing that's non-obvious: headers go via `-H`, which is how you pass the bearer. Everything else is either in `websocat --help` or `references/websocat-patterns.md`.

```bash
echo '{"op":"ping"}' | websocat -n1 -H "Authorization: Bearer $TOKEN" ws://.../endpoint
```

For subprotocols (`graphql-transport-ws`), mTLS (use `wscat` instead), auto-reconnect, ping/pong: see the reference.

## When NOT to use this skill

- Project uses Bruno/Postman/newman/Insomnia — use those.
- Backend has no auth — plain `curl` or `xh` is enough.
- UI validation — use Playwright MCP or an in-house browser tool.
- CI secret storage — keychain is developer-machine-only; CI needs a secret manager.

## References

- `references/token-script.sh` — complete bash script for token acquisition + refresh caching
- `references/hurl-patterns.md` — captures, assertions, retries, GraphQL, parallel, CI
- `references/websocat-patterns.md` — subprotocols, mTLS, reconnect, debugging
- `references/oidc-token-flows.md` — grant-type comparison, 401 debugging, discovery endpoint
