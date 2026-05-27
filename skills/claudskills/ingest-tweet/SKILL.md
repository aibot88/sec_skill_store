---
name: ingest-tweet
description: Extract full text from X/Twitter posts for wiki ingestion. Uses FXTwitter API, no auth required.
user-invocable: false
allowed-tools: Bash(curl *)
---

# Ingest Tweet

Extract the full text of an X/Twitter post.

## Extraction Method

1. Parse the URL to extract username and tweet ID:
   - Pattern: `https://x.com/{user}/status/{id}` or `https://twitter.com/{user}/status/{id}`
   - Strip query parameters (`?s=46`, `?t=...`)

2. Fetch via FXTwitter API (free, no auth, returns full text including long "note tweets"):
```bash
curl -s "https://api.fxtwitter.com/{user}/status/{id}"
```

3. Parse JSON response:
   - `tweet.text` — full tweet text (with expanded URLs, not t.co links)
   - `tweet.author.name` / `tweet.author.screen_name` — author
   - `tweet.created_at` — date
   - `tweet.likes`, `tweet.retweets`, `tweet.replies` — engagement
   - `tweet.quote` — quoted tweet (if present)
   - `tweet.media` — images/videos (if present)

## Post-Extraction

- Save to vault's `raw/<author>-tweet-<id>.md` with YAML header:
```yaml
---
source-url: <tweet-url>
title: "<author> tweet on <topic>"
author: "<name> (@<screen_name>)"
date-fetched: <today>
source-type: tweet
---
```
- Include quoted tweet text if present
- Note engagement stats in the source-note

## Fallback

If FXTwitter fails, use oEmbed (truncates long tweets):
```bash
curl -s "https://publish.x.com/oembed?url=<original-url>"
```

## Dependencies

None — uses only `curl`.

## See also

- [`ronan-skills/x-scan`](https://github.com/RonanCodes/ronan-skills/blob/main/skills/x-scan/SKILL.md) — generic sibling for browsing tweets (URL, user timeline, topic search) without vault persistence. Use this skill when you want to keep the content.
