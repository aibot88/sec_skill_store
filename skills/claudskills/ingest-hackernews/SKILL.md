---
name: ingest-hackernews
description: Extract Hacker News threads (post + comments) for wiki ingestion. Uses Algolia HN API, no auth required.
user-invocable: false
allowed-tools: Bash(curl *)
content-pipeline:
  - pipeline:scan
  - platform:agnostic
  - role:scanner
---

# Ingest Hacker News Thread

Extract the full content of a Hacker News post and its comment tree.

## Extraction Method

1. Parse the URL to extract the item ID:
   - Pattern: `https://news.ycombinator.com/item?id={id}`
   - Also accept bare IDs (just the number)

2. Fetch the full thread via Algolia HN API (free, no auth, returns entire comment tree):
```bash
curl -s "https://hn.algolia.com/api/v1/items/{id}"
```

3. Parse JSON response for the top-level post:
   - `title` — post title
   - `url` — linked URL (if link post; null for Ask HN / Show HN text posts)
   - `author` — HN username of poster
   - `created_at` — ISO timestamp
   - `points` — score
   - `text` — body text (for self/text posts; HTML-encoded)
   - `children` — array of comment objects (recursive)

4. Parse each comment in `children` recursively:
   - `author` — commenter username
   - `text` — comment body (HTML-encoded, strip tags to markdown)
   - `created_at` — timestamp
   - `children` — nested replies
   - Skip items where `author` is null (deleted/dead comments)

5. Convert HTML entities in text fields to readable markdown:
   - `<p>` to double newline
   - `<a href="...">` to `[text](url)` markdown links
   - `<code>` / `<pre>` to backtick code spans / fenced code blocks
   - `<i>` to `*italic*`
   - `&#x27;` and other entities to literal characters

## Building the Markdown Output

Construct a flat markdown representation of the thread with indentation to show nesting depth:

```markdown
# {title}

**Author:** {author} | **Points:** {points} | **Date:** {created_at}
**HN URL:** https://news.ycombinator.com/item?id={id}
**Link:** {url} (if present)

## Post Body
{text content if self-post, otherwise "Link post — see URL above."}

## Comments ({total_comment_count} comments)

**{commenter1}** ({timestamp}):
Comment text here...

> **{reply_author}** ({timestamp}):
> Reply text here, indented with blockquote...
>
> > **{nested_reply_author}** ({timestamp}):
> > Deeper reply, double-indented...

**{commenter2}** ({timestamp}):
Another top-level comment...
```

Use `>` blockquote markers for nesting depth:
- Top-level comments: no prefix
- 1 level deep: `> `
- 2 levels deep: `> > `
- 3+ levels deep: cap at `> > > ` (deeper replies still shown but capped at 3 levels of indent for readability)

## Post-Extraction

- Save to vault's `raw/hn-{id}-{slug}.md` where `{slug}` is a kebab-case version of the title (truncated to ~50 chars), with YAML header:
```yaml
---
source-url: https://news.ycombinator.com/item?id={id}
title: "{title}"
author: "{author}"
date-fetched: {today}
source-type: discussion
points: {points}
comment-count: {total_comments}
linked-url: "{url or none}"
---
```
- Include the full thread content (post + comments) below the frontmatter

## Handling Large Threads

- The Algolia API returns the full tree in one call, but very large threads (1000+ comments) may produce a lot of content.
- For threads with more than 200 top-level comments, include only the top ~100 most substantial comment sub-trees (those with the most replies or longest text) and note the truncation in the raw file.
- Always include a comment count summary at the top of the Comments section.

## Fallback

If the Algolia API fails or returns an error:
1. Try the official HN Firebase API as a fallback (requires multiple calls):
```bash
# Get the item
curl -s "https://hacker-news.firebaseio.com/v0/item/{id}.json"
# Then fetch each child comment by ID from the `kids` array
curl -s "https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
```
2. Note: the Firebase API requires one call per comment (no tree endpoint), so for large threads this is slow. Use only as a fallback.

## Dependencies

None — uses only `curl`.

## See also

- [`ronan-skills/hn-scan`](https://github.com/RonanCodes/ronan-skills/blob/main/skills/hn-scan/SKILL.md) — generic sibling for browsing HN (thread URL, topic search, front page, Show HN, Ask HN) without vault persistence. Use this skill when you want to keep the content.
