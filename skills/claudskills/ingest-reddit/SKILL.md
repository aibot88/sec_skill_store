---
name: ingest-reddit
description: Extract post and comments from Reddit threads for wiki ingestion. Appends .json to any Reddit URL, no auth required for public subreddits.
user-invocable: false
allowed-tools: Bash(curl *)
content-pipeline:
  - pipeline:scan
  - platform:reddit
  - role:scanner
---

# Ingest Reddit Thread

Extract the full post content and comment tree from a Reddit thread.

## Extraction Method

1. Parse the URL to extract the thread path:
   - Pattern: `https://www.reddit.com/r/{subreddit}/comments/{id}/{slug}/`
   - Also handles: `https://old.reddit.com/...`, `https://reddit.com/...`
   - Strip trailing query parameters

2. Fetch via JSON endpoint (no auth needed for public subreddits):
```bash
curl -sL -H "User-Agent: llm-wiki-bot/1.0" \
  "https://www.reddit.com/r/{subreddit}/comments/{id}/{slug}.json?sort=top&limit=500"
```

3. Parse JSON response:
   - **Element `[0]`** — the post:
     - `[0].data.children[0].data.title` — post title
     - `[0].data.children[0].data.selftext` — post body (markdown)
     - `[0].data.children[0].data.author` — poster username
     - `[0].data.children[0].data.subreddit` — subreddit name
     - `[0].data.children[0].data.score` — upvotes
     - `[0].data.children[0].data.created_utc` — timestamp
     - `[0].data.children[0].data.url` — link URL (for link posts)
     - `[0].data.children[0].data.is_self` — true if text post, false if link post
     - `[0].data.children[0].data.num_comments` — comment count
   - **Element `[1]`** — the comment tree:
     - `[1].data.children[]` — top-level comments
     - Each comment: `.data.author`, `.data.body`, `.data.score`, `.data.created_utc`
     - Each comment may have `.data.replies` — a nested object with the same structure
     - Recursively traverse `.data.replies.data.children[]` to build nested markdown

4. Build the comment tree as nested markdown:
   - Traverse comments recursively
   - For each comment, render as a blockquote with author and score
   - Use indentation (nested blockquotes) for reply depth
   - **Skip "more" stubs** — comments where `kind === "more"` (these are placeholders for additional comments in large threads; acceptable to skip for v1)

### Comment Rendering Format

```markdown
## Comments

> **u/username** (42 points)
> Comment text here, which may span
> multiple lines.

> > **u/replier** (15 points)
> > This is a reply to the above comment.

> > > **u/deep-replier** (8 points)
> > > And this is a nested reply.

> **u/another-top-level** (30 points)
> Another top-level comment.
```

Cap rendering at 4 levels of nesting depth to keep output readable. For deeper replies, flatten them at the 4th level.

## Post-Extraction

- Save to vault's `raw/<subreddit>-<slug>.md` with YAML header:
```yaml
---
source-url: <reddit-thread-url>
title: "<post-title>"
author: "u/<username>"
subreddit: "r/<subreddit>"
date-fetched: <today>
source-type: discussion
score: <post-score>
num-comments: <comment-count>
---
```

- Include the full post body followed by the rendered comment tree
- For link posts (not self posts), include the linked URL prominently at the top of the raw file

## Fallback

If the `.json` endpoint returns a 429 (rate limit) or error:
1. Wait briefly and retry once
2. If still failing, try `old.reddit.com` as the domain:
```bash
curl -sL -H "User-Agent: llm-wiki-bot/1.0" \
  "https://old.reddit.com/r/{subreddit}/comments/{id}/{slug}.json?sort=top&limit=500"
```
3. If all attempts fail, report the error and suggest the user try again later or paste the content manually

## Dependencies

None — uses only `curl`.

## See also

- [`ronan-skills/reddit-scan`](https://github.com/RonanCodes/ronan-skills/blob/main/skills/reddit-scan/SKILL.md) — generic sibling for browsing Reddit (thread URL, subreddit listing, topic search) without vault persistence. Use this skill when you want to keep the content.
