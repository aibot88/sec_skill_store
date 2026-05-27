---
name: babeliocli-setup
description: "Install babeliocli, authenticate against Babelio (password or SSO cookie import), and manage the local session file. Use this skill when a user asks to install, log in, set up, connect, or recover a Babelio CLI session — including cases where the Babelio account is linked to Google or Facebook and a classic login is impossible."
---

# babeliocli — Setup, Authentication, Session Management

`babeliocli` is a read-only CLI for babelio.com. It does not use an official API: instead, it logs into the regular web form (or reuses cookies from the user's browser) and parses HTML pages.

## Install

One-liner (macOS or Linux, amd64 or arm64):

```bash
curl -fsSL https://raw.githubusercontent.com/yoanbernabeu/babeliocli/main/install.sh | sh
```

Or with Go:

```bash
go install github.com/yoanbernabeu/babeliocli@latest
```

Or grab a binary from the [GitHub releases](https://github.com/yoanbernabeu/babeliocli/releases).

## Authentication path 1 — username & password

```bash
babeliocli login --username 'pseudo_or_email'
# Password is prompted (hidden) unless --password-stdin or BABELIO_PASSWORD is set.
```

For scripts, prefer stdin so the password never appears on a process list:

```bash
printf '%s' "$BABELIO_PASSWORD" | babeliocli login --username "$BABELIO_USERNAME" --password-stdin
```

Environment variables: `BABELIO_USERNAME`, `BABELIO_PASSWORD`.

## Authentication path 2 — SSO (Google / Facebook)

Babelio supports Google and Facebook login. `babeliocli` does not implement the full OAuth flow; instead, the user imports the cookies they already have in their browser.

1. User signs into babelio.com as usual.
2. User copies the following cookies from DevTools → Application → Cookies → `https://www.babelio.com`:
   - `PHPSESSID`
   - `bbac`
   - `id_user`
   - `bbacml` (optional)
3. Run:

```bash
babeliocli session import \
  --phpsessid 'XXX' \
  --bbac 'YYY' \
  --id-user 'NNN' \
  --username 'pseudo'
```

Or provide a JSON export from an extension like "EditThisCookie":

```bash
babeliocli session import --cookie-file cookies.json --username 'pseudo'
```

The session is verified by hitting `/mabibliotheque.php` and confirming we are not redirected to the login page.

## Inspect and clear the session

```bash
babeliocli whoami   # shows username, id_user, saved_at
babeliocli logout   # removes ~/.config/babeliocli/session.json
```

The session file lives at `$XDG_CONFIG_HOME/babeliocli/session.json` (usually `~/.config/babeliocli/session.json` on Linux/macOS) with mode `0600`. Do **not** commit it to a repository.

## Session expired?

If any read command returns `session expired: run babeliocli login or babeliocli session import again`, re-authenticate. Babelio's session TTL is finite, so expect periodic re-logins.

## Output format

Every command defaults to JSON. Pass `-f text` for a readable terminal view. Errors go to stderr so that stdout stays valid JSON:

```bash
babeliocli whoami 2>/dev/null | jq .username
```

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `login failed: check username and password` | Wrong credentials, or the account is SSO-only → use `session import` |
| `imported cookies are not authenticated (redirected to login)` | Cookies expired or copied wrong; re-copy from browser |
| `no saved session (run babeliocli login first)` | Nothing has ever been stored; run `login` or `session import` |
| Partial or garbled accents | Should not happen: the CLI handles ISO-8859-1. File a bug with the URL. |
