---
name: ingest-github-discussions
description: Extract content from GitHub Discussion threads for wiki ingestion. Uses gh CLI GraphQL API, authenticated via gh auth.
user-invocable: false
allowed-tools: Bash(gh *)
content-pipeline:
  - pipeline:scan
  - platform:agnostic
  - role:scanner
---

# Ingest GitHub Discussion

Extract the full content of a GitHub Discussion thread, including all comments and nested replies.

## Extraction Method

1. Parse the URL to extract owner, repo, and discussion number:
   - Pattern: `https://github.com/{owner}/{repo}/discussions/{number}`

2. Fetch via GraphQL using `gh api graphql`:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      title
      body
      createdAt
      author { login }
      url
      category { name }
      labels(first: 10) { nodes { name } }
      comments(first: 100) {
        totalCount
        pageInfo { hasNextPage endCursor }
        nodes {
          body
          createdAt
          author { login }
          replies(first: 100) {
            nodes {
              body
              createdAt
              author { login }
            }
          }
        }
      }
    }
  }
}' -F owner='{owner}' -F repo='{repo}' -F number={number}
```

3. Parse JSON response:
   - `.data.repository.discussion.title` — discussion title
   - `.data.repository.discussion.body` — opening post body (markdown)
   - `.data.repository.discussion.author.login` — author username
   - `.data.repository.discussion.createdAt` — creation date
   - `.data.repository.discussion.category.name` — category (e.g. "Ideas", "Q&A")
   - `.data.repository.discussion.labels` — labels
   - `.data.repository.discussion.comments.nodes[]` — top-level comments
   - Each comment's `.replies.nodes[]` — nested replies (max 2 levels deep)

## Pagination for Large Threads

If `comments.pageInfo.hasNextPage` is `true`, fetch additional pages using the `endCursor`:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!, $after: String!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      comments(first: 100, after: $after) {
        totalCount
        pageInfo { hasNextPage endCursor }
        nodes {
          body
          createdAt
          author { login }
          replies(first: 100) {
            nodes {
              body
              createdAt
              author { login }
            }
          }
        }
      }
    }
  }
}' -F owner='{owner}' -F repo='{repo}' -F number={number} -f after='{endCursor}'
```

Repeat until `hasNextPage` is `false`.

## Post-Extraction

- Save to vault's `raw/<owner>-<repo>-discussion-<number>.md` with YAML header:
```yaml
---
source-url: <discussion-url>
title: "<discussion-title>"
author: "<github-username>"
date-fetched: <today>
source-type: discussion
category: "<category-name>"
comment-count: <total-count>
---
```

- Format the raw file as:
  - Opening post body (attributed to author)
  - Each comment as a section with author and timestamp
  - Nested replies indented under their parent comment
  - Preserve original markdown formatting in all bodies

### Raw File Format

```markdown
---
source-url: https://github.com/owner/repo/discussions/123
title: "Discussion Title"
author: "username"
date-fetched: 2026-04-14
source-type: discussion
category: "Ideas"
comment-count: 42
---

# Discussion Title

**@username** — 2026-04-10

<opening post body>

---

## Comments

### @commenter1 — 2026-04-10

<comment body>

> **@replier1** — 2026-04-11
>
> <reply body>

> **@replier2** — 2026-04-11
>
> <reply body>

---

### @commenter2 — 2026-04-11

<comment body>
```

## Dependencies

Requires `gh` CLI (authenticated). No additional tools needed.
