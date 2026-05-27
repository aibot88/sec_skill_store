---
name: ingest-gist
description: Extract content from GitHub gists for wiki ingestion. Uses raw URL fetch, no auth required.
user-invocable: false
allowed-tools: Bash(curl *) Bash(gh *)
---

# Ingest GitHub Gist

Extract raw content from a GitHub gist.

## Extraction Method

1. Parse the URL to extract username and gist ID:
   - Pattern: `https://gist.github.com/{user}/{gist_id}`

2. Fetch via raw URL (most reliable, bypasses API rate limits):
```bash
curl -sL "https://gist.githubusercontent.com/{user}/{gist_id}/raw/"
```

3. If username is unknown, get it via API:
```bash
gh api "/gists/{gist_id}" --jq '.owner.login'
```

4. For multi-file gists, list files first:
```bash
gh gist view {gist_id} --files
```
Then fetch each file separately.

## Post-Extraction

- Save to vault's `raw/<descriptive-name>.md` with YAML header:
```yaml
---
source-url: <gist-url>
title: "<gist-description or filename>"
author: "<github-username>"
date-fetched: <today>
source-type: gist
---
```

## Fallback Chain

1. Raw URL (`gist.githubusercontent.com`) — best, no API needed
2. `gh gist view {id} --raw` — uses gh CLI auth
3. `gh api "/gists/{id}" --jq '.files | to_entries[] | .value.content'`

## Dependencies

None for primary method (curl only). `gh` CLI optional for fallbacks.
