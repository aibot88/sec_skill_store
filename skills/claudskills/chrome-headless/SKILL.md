---
name: chrome-headless
description: "Fetch rendered public web pages via isolated headless Chrome. Default for 'fetch this URL', 'what does this page say', 'scrape this page'. Lighter than Playwright MCP, works in dispatch jobs. Routes authenticated hosts to claude --chrome. Escalates to Playwright MCP only for clicks, form fills, or multi-page flows."
---

# Chrome Headless Fetch

Default tool for rendering public web pages and returning DOM. Isolated, profile-less, works identically in foreground sessions and dispatch jobs.

Phase 0 result (Chrome 147, 2026-04-20): `--virtual-time-budget` returns 0 bytes and is broken. Plain `--dump-dom` with no timing flags returns full post-hydration DOM for both static pages and React SPAs. Use no timing flags.

## Use this for

Public URL, need rendered DOM (including JS-rendered SPAs), no interaction required. Foreground or dispatched.

## Escalate when

- Clicks, form fills, multi-step flow, viewport screenshots, network inspection: Playwright MCP. Announce: "Escalating to Playwright MCP because [specific reason]."
- Logged-in session needed (Gmail, Notion, HubSpot, Vercel dashboard, GA4, Figma web, authenticated GitHub, LinkedIn, Slack, Linear, Productive, Instantly, Apollo, Granola, Atlassian): stop, tell user to use `/chrome` or relaunch with `claude --chrome`. Do not fetch.

Never silently fall back to Playwright for a plain fetch. Dispatched jobs must always use this skill; Playwright MCP is interactive-only and fails under dispatch.

## Authenticated-host detection

Parse the URL hostname. Match via `endsWith` against these suffixes (not substring, not exact):

`.google.com`, `mail.google.com`, `.notion.so`, `.notion.site`, `app.hubspot.com`, `vercel.com`, `.figma.com`, `.linkedin.com`, `app.slack.com`, `linear.app`, `app.productive.io`, `instantly.ai`, `apollo.io`, `app.granola.ai`, `.atlassian.net`

For `github.com`: match only if path starts with `/settings`, `/pulls`, `/notifications`, or contains `/private`. Public GitHub URLs are fine.

If matched: "This host typically requires login. Headless Chrome will only see the login page. Use `claude --chrome` or `/chrome` in-session for authenticated access. Proceed anyway? (yes/no)." Do not fetch unless user confirms.

## URL validation

Accept only `http://` or `https://`. Reject `file://`, `javascript:`, userinfo URLs (`https://user:pass@host`), and bare hostnames.

## Fetch procedure

1. **Preflight status check** (captures real HTTP status, which `--dump-dom` hides):
   ```bash
   CHROME_VERSION=$("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version | awk '{print $3}')
   UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${CHROME_VERSION} Safari/537.36"
   curl -sIL --max-time 10 -A "$UA" "$URL" -o /dev/null -w "%{http_code} %{url_effective}\n"
   ```
   - Non-2xx: report and stop.
   - Final URL hostname differs from initial and matches auth-host list: report as "redirect to login," stop.
   - `Content-Type` is `application/pdf`, `application/octet-stream`, or any non-`text/html`: report "binary content, not HTML" and stop.

2. **Fetch**:
   ```bash
   eval "$(/opt/homebrew/bin/brew shellenv)"
   USER_DATA_DIR=$(mktemp -d /tmp/chrome-headless-XXXXXX)
   CACHE_DIR=$(mktemp -d /tmp/chrome-cache-XXXXXX)
   STDERR_LOG=$(mktemp /tmp/chrome-stderr-XXXXXX)
   trap 'rm -rf "$USER_DATA_DIR" "$CACHE_DIR"; rm -f "$STDERR_LOG"' EXIT

   gtimeout --kill-after=5 20 \
     "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless=new \
     --disable-gpu \
     --dump-dom \
     --user-data-dir="$USER_DATA_DIR" \
     --disk-cache-dir="$CACHE_DIR" \
     --user-agent="$UA" \
     "$URL" 2>"$STDERR_LOG"
   ```
   - `gtimeout 20`: hard wall-clock kill. Chrome's `--timeout` flag is not a process killer.
   - Per-invocation `--user-data-dir`: prevents concurrent-dispatch contention on Chrome's singleton lock.
   - No `--no-sandbox`: unneeded and reduces security on macOS.
   - No timing flags: `--virtual-time-budget` is broken on Chrome 147+ headless=new.

3. **Post-fetch scan** (detect login pages and bot-protection challenges that return 200):
   - Login signals: `type="password"` input, `<form action*="login"`, title containing "Sign in" or "Log in"
   - Bot-challenge signals: `cf-chl-`, `"Checking your browser"`, `__cf_chl_jschl_tk__`, `px-captcha`, `data-sitekey` with hCaptcha/reCAPTCHA
   - If either matches, report the challenge type and route accordingly. Do not pretend the returned HTML is content.

4. **Content cleanup** (before output): strip `<script>`, `<style>`, `<svg>` elements. Reduces output by 40-80% on typical pages without losing readable content.

## Output handling

- Cleaned DOM <= 50 KB: return inline.
- Over 50 KB: write to `~/Claude-Stuff/chrome-headless/<YYYYMMDD-HHMMSS>-<hostname>-<path-hash>.html`. Hostname sanitized to `[a-z0-9.-]`, truncated to 63 chars. Path-hash is `sha1sum` first 8 chars.
- Always report: URL, HTTP status from preflight, final URL (if redirected), byte count, `<title>`, and first 2 KB of `<body>` as preview.

## Error handling

- Chrome binary missing: probe with `--version` first. Report path and version output. Stop.
- `curl` preflight fails (DNS, SSL, non-2xx): report status, stop. Do not launch Chrome.
- `gtimeout` fires (20s wall-clock): report timeout, suggest Playwright for pages that require full settle. Stop.
- Empty or tiny DOM (< 2 KB after cleanup): flag as suspicious, include stderr excerpt, ask before escalating.
- Stderr parsed for `net::ERR_` and `ERR_CERT_` markers, summarized in output. Never piped to stdout.

## Examples

**Public static page:**
```
/chrome-headless https://example.com
```
Preflight 200, inline DOM return, ~1 KB after cleanup.

**Dispatched fetch:**
```
/dispatch "Use /chrome-headless on https://news.ycombinator.com. Summarize top 5 stories. Write to ~/Claude-Stuff/hn-summary.md"
```
DOM spills to file, summarizer reads from file. Isolated `--user-data-dir` runs safely alongside other dispatched fetches.

**Concurrent dispatch limit:** macOS headless Chrome saturates at 2-3 simultaneous instances. Three parallel fetches will all timeout. If a dispatch job needs multiple URLs, fetch them sequentially, not in parallel subshells.

**Authenticated host routing:**
```
/chrome-headless https://mail.google.com/mail/u/0/
```
"This host typically requires login..." prompt. No fetch unless confirmed.

**Bot-protection detection:**
```
/chrome-headless https://some-cloudflare-protected-site.com
```
Preflight 200, post-scan matches `cf-chl-`. Reports: "Page served a Cloudflare challenge. Escalate to `claude --chrome`."
