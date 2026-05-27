---
name: ingest-devto
description: Extract article content from dev.to posts for wiki ingestion. Uses dev.to public API, no auth required.
user-invocable: false
allowed-tools: Bash(curl *)
content-pipeline:
  - pipeline:scan
  - platform:devto
  - role:scanner
---

# Ingest Dev.to Article

Extract the full content of a dev.to article using the public API.

## URL Detection

Matches URLs with these patterns:
- `https://dev.to/{username}/{article-slug}`
- `https://dev.to/{username}/{article-slug}-{id}`
- `https://www.dev.to/{username}/{article-slug}`

## Extraction Method

1. Parse the URL to extract the username and article slug:
   - Pattern: `https://dev.to/{username}/{article-slug}`
   - Strip any query parameters or fragments

2. Fetch the article via the dev.to public API using the path:
```bash
curl -s "https://dev.to/api/articles/{username}/{article-slug}"
```

This returns a JSON object with the full article content.

3. Parse JSON response:
   - `title` — article title
   - `description` — short description/subtitle
   - `body_markdown` — full article content in markdown (this is the primary content)
   - `body_html` — HTML version (fallback if markdown is insufficient)
   - `user.name` — author's display name
   - `user.username` — author's dev.to username
   - `published_at` — ISO 8601 publish date
   - `edited_at` — last edit date (if edited)
   - `tags` — array of tag strings
   - `canonical_url` — canonical URL (may differ if cross-posted)
   - `cover_image` — cover image URL (if present)
   - `positive_reactions_count` — total reactions
   - `comments_count` — number of comments
   - `reading_time_minutes` — estimated read time
   - `url` — the dev.to URL

4. The `body_markdown` field contains the raw markdown as written by the author, which is the cleanest source. Use this directly as the article content.

## Image Handling

After extracting the article content from `body_markdown`:

1. **Find image URLs** in the markdown:
   - `![alt](https://...)` markdown image syntax
   - dev.to often hosts images at `https://res.cloudinary.com/practicaldev/...` or `https://dev-to-uploads.s3.amazonaws.com/...`

2. **Download each image** to vault's `raw/assets/`:
```bash
VAULT="vaults/<vault-name>"
mkdir -p "$VAULT/raw/assets"

# For each image URL:
FILENAME="<article-slug>-img-<NN>.<ext>"
curl -sL -o "$VAULT/raw/assets/$FILENAME" "<image-url>"
```

3. **Replace remote URLs** with local paths in the raw markdown:
```markdown
# Before:
![diagram](https://res.cloudinary.com/practicaldev/image/fetch/...)

# After:
![diagram](assets/devto-article-slug-img-01.png)
```

4. **Download cover image** if present:
```bash
curl -sL -o "$VAULT/raw/assets/<article-slug>-cover.<ext>" "<cover_image_url>"
```

5. **Skip images that are:**
   - Already local paths
   - Tracking pixels or tiny icons (< 1KB)
   - Data URIs (base64 embedded)
   - dev.to UI elements (avatars, badges, etc.)

## Post-Extraction

- Save to vault's `raw/devto-{article-slug}.md` with YAML header:
```yaml
---
source-url: <dev.to-url>
title: "<title>"
author: "<name> (@<username>)"
date-fetched: <today>
source-type: article
published: <published_at>
tags: [<tag1>, <tag2>, ...]
reactions: <positive_reactions_count>
comments: <comments_count>
reading-time: <reading_time_minutes>min
canonical-url: "<canonical_url>"
images-downloaded: <count>
---
```

- Below the frontmatter, include the `body_markdown` content directly (it's already markdown)
- If the article has a cover image, include it at the top of the content

## Fallback Chain

1. **dev.to API by path** (best): `curl -s "https://dev.to/api/articles/{username}/{slug}"` — returns full markdown, no auth needed
2. **dev.to API search by URL**: `curl -s "https://dev.to/api/articles?url=<canonical-url>"` — returns array, use first result, then fetch full article by ID: `curl -s "https://dev.to/api/articles/{id}"`
3. **Web scraping** (last resort): `curl -sL "<dev.to-url>"` — the article content is in the page HTML within `<div id="article-body">`. Extract readable content as per `ingest-web` skill.

## Dependencies

None — uses only `curl`.
