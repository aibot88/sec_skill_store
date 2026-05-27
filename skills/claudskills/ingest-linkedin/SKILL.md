---
name: ingest-linkedin
description: Ingest LinkedIn posts into the wiki. Supports pasted text or cookie-based auth for URL fetching.
user-invocable: false
allowed-tools: Bash(curl *) Read Write Edit Glob Grep
content-pipeline:
  - pipeline:scan
  - platform:linkedin
  - role:scanner
---

# Ingest LinkedIn Post

Extract LinkedIn post content and create wiki pages.

## Detect Input Type

- Input starts with `http` → **URL approach** (cookie auth)
- Otherwise → **Pasted text** (always works)

## Approach 1: Pasted Text

Parse the pasted content to extract:
- **Author name** — first line or clearly identifiable name
- **Post text** — main body
- **Date** — if visible, otherwise use today
- **Hashtags** — extract any #hashtags for tags

## Approach 2: Cookie-Based Auth (URL)

1. Use the `firefox-cookies` skill to get cookies for `linkedin.com`
2. Fetch the post:
```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "$COOKIE_HEADER" "<linkedin-url>"
```
3. Parse HTML — try in order:
   - JSON-LD (`<script type="application/ld+json">`)
   - Post content in `feed-shared-update-v2__description` divs
   - Author from `feed-shared-actor__name` spans
4. **If auth fails** (403, empty, no cookies): tell user to paste the post text and re-run. Stop.

## Save Raw Content

Save to `$VAULT/raw/linkedin-<author-slug>-<date>.md`:
```yaml
---
source-url: "<linkedin-url or 'pasted'>"
title: "<post summary>"
author: "<author-name>"
date-fetched: <today>
source-type: social
platform: linkedin
---
```

## Create Wiki Source Note

Create `$VAULT/wiki/sources/linkedin-<title-slug>.md`:
```yaml
---
title: "<Post Summary>"
date-created: <today>
date-modified: <today>
page-type: source-note
domain: <vault-default-domain>
tags: [linkedin, <hashtags>, <topic-tags>]
sources: ["<linkedin-url>"]
related: []
source-type: social
author: "<Author Name>"
date-accessed: <today>
raw-file: "raw/linkedin-<author-slug>-<date>.md"
---
```

Sections: **Author** (name + headline), **Post** (full text), **Key Takeaways** (3-5 bullets), **Sources** (link).

## Notes

- Pasted text is the most reliable method — LinkedIn HTML changes frequently
- Never store cookies or auth tokens in wiki pages or raw files

## Dependencies

- `curl` — HTTP requests
- `firefox-cookies` skill — optional, for URL-based fetching

## See also

- [`ronan-skills/linkedin-scan`](https://github.com/RonanCodes/ronan-skills/blob/main/skills/linkedin-scan/SKILL.md) — generic sibling for reading LinkedIn posts (URL with cookie auth, pasted text, or profile feed) without vault persistence. Use this skill when you want to keep the content.
