---
name: notion-cli
description: Access Notion via the 4ier/notion-cli Go binary. Use when user wants to search Notion, query databases, read pages, export data, manage blocks, or add comments from the command line. TRIGGERS - notion search, query database, read page, notion export, notion blocks, notion comments, notion cli.
allowed-tools: Read, Bash, Glob, Grep
---

# Notion CLI

Fast, agent-friendly access to Notion via the `4ier/notion-cli` Go binary. Single static binary, sub-second startup, auto-JSON when piped.

> **Self-Evolving Skill**: Fix this file immediately if instructions drift. Do not defer.

## When to Use

Use this skill when the user wants to interact with Notion from the command line — searching pages, querying databases, reading content, exporting data, managing blocks, or adding comments. This wraps the Go binary `notion` (installed via `brew install 4ier/tap/notion-cli`).

Do NOT use this skill for programmatic Python automation with the Notion SDK — use `productivity-tools:notion-sdk` instead. This skill is for CLI-first, pipe-friendly operations.

## Preflight

Before any operation, verify the CLI is authenticated:

```bash
notion auth status
```

If not authenticated, retrieve the token from Doppler and authenticate:

```bash
doppler secrets get NOTION_API_TOKEN --project claude-config --config prd --plain | notion auth login --with-token
```

Fallback: prompt the user for their integration token.

## Output Formats

The CLI auto-detects context:

- **TTY** (interactive terminal): colored tables
- **Piped** (to `jq`, file, etc.): clean JSON

Force a format with `--format`:

| Flag             | Output      |
| ---------------- | ----------- |
| `--format json`  | JSON        |
| `--format table` | ASCII table |
| `--format md`    | Markdown    |
| `--format text`  | Plain text  |

For agent consumption, always pipe or use `--format json` to get structured output.

## Core Commands

### Search

```bash
notion search "meeting notes"                  # Search by title
notion search --type page "roadmap"            # Pages only
notion search --type database                  # List all databases
notion search --all                            # Fetch all results (paginated)
notion search --limit 20 "query"               # Limit results
```

### Pages

```bash
notion page view <page-id|url>                 # View page content (blocks as markdown)
notion page props <page-id|url>                # Show page properties
notion page create --parent <id> --title "X"   # Create a page
notion page set <id> --prop 'Status=Done'      # Set property
notion page edit <id>                          # Edit in $EDITOR
notion page move <id> --to <parent-id>         # Move page
notion page delete <id>                        # Archive page
notion page restore <id>                       # Restore archived page
notion page open <id>                          # Open in browser
notion page list                               # List accessible pages
```

### Databases

```bash
notion db list                                 # List all databases
notion db view <db-id|url>                     # Show schema
notion db query <db-id|url>                    # Query all rows
notion db query <id> --filter 'Status=Done'    # Simple filter
notion db query <id> --filter 'Date>=2026-01-01' --sort 'Date:desc'
notion db query <id> --filter-json '{"or":[...]}' # Complex filters
notion db query <id> --all                     # Fetch all pages
notion db export <id> --format csv -o data.csv # Export to CSV
notion db export <id> --format json            # Export to JSON
notion db export <id> --format md              # Export to Markdown table
notion db add <id> --prop 'Name=Task' --prop 'Status=Todo'  # Add row
notion db add-bulk <id> --file rows.json       # Bulk add from JSON
```

**Filter operators**: `=` `!=` `>` `>=` `<` `<=` `~=` (contains)

Multiple `--filter` flags are AND-combined. For OR logic, use `--filter-json`.

### Blocks

```bash
notion block list <page-id|url>                # List child blocks
notion block list <id> --depth 3               # Recursive (3 levels)
notion block get <block-id>                    # Get specific block
notion block append <page-id> --md "# Hello"   # Append markdown
notion block insert <after-block-id> --md "X"  # Insert after block
notion block delete <block-id>                 # Delete block
notion block move <block-id> --to <parent-id>  # Move block
```

### Comments

```bash
notion comment list <page-id>                  # List comments
notion comment add <page-id> --body "text"     # Add comment
notion comment reply <comment-id> --body "X"   # Reply to comment
```

### Users

```bash
notion user me                                 # Current bot user
notion user list                               # Workspace users
notion user get <user-id>                      # User details
```

### Files

```bash
notion file upload <file-path>                 # Upload file
notion file list                               # List uploads
```

### Raw API (escape hatch)

```bash
notion api GET /v1/users/me
notion api POST /v1/search --body '{"query":"test"}'
echo '{"query":"test"}' | notion api POST /v1/search
```

## ID Resolution

The CLI accepts both Notion URLs and raw IDs interchangeably:

```bash
notion page view https://www.notion.so/My-Page-abc123def456
notion page view abc123def456
```

## Common Patterns

### Export entire database to JSON

```bash
notion db export <db-id> --format json -o database.json
```

### Search and pipe to jq

```bash
notion search "project" --format json | jq '.results[] | {title: .properties.title.title[0].plain_text, url: .url}'
```

### List all databases with their IDs

```bash
notion search --type database --all --format json | jq '.results[] | {id: .id, title: .title[0].plain_text}'
```

### Recursive page content dump

```bash
notion block list <page-id> --depth 10 --format md
```

## Credential Storage

| Store   | Location                             | Purpose          |
| ------- | ------------------------------------ | ---------------- |
| Doppler | `claude-config/prd:NOTION_API_TOKEN` | SSoT for token   |
| CLI     | `~/.config/notion/credentials.json`  | Local auth cache |

Token format: `ntn_*` (Notion internal integration token).

## Troubleshooting

| Issue              | Fix                                                                  |
| ------------------ | -------------------------------------------------------------------- |
| `unauthorized`     | Token expired/revoked — regenerate at notion.so/profile/integrations |
| `object not found` | Page not connected to integration — add via page menu > Connections  |
| `rate_limited`     | CLI auto-retries; for bulk ops use `--limit` to reduce batch size    |
| `validation_error` | Check property names match schema: `notion db view <id>`             |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** If the CLI interface drifted, update usage examples and command tables.
3. **Was a workaround needed?** If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
