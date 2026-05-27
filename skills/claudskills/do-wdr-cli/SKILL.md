---
name: do-wdr-cli
description: Use the do-wdr (Web Documentation Resolver) CLI binary to resolve URLs and queries into markdown documentation. Use when you need fast command-line access to web documentation resolution, prefer compiled binary over Python, or need to integrate do-wdr into shell scripts and automation.
license: MIT
compatibility: Rust stable, cross-platform Linux/macOS/Windows
allowed-tools: Bash(do-wdr:*) Read
metadata:
  author: d-oit
  version: "0.1.0"
  source: https://github.com/d-oit/do-web-doc-resolver/tree/main/cli
---

# WDR CLI Skill

Fast compiled Rust CLI for resolving web URLs and queries into markdown documentation.

## When to use this skill

Activate this skill when you need to:
- Resolve a URL or query to markdown from the command line
- Integrate documentation resolution into shell scripts
- Get faster performance than the Python implementation
- Use CLI-specific features (metrics, cache stats, provider selection)
- Build automation workflows with do-wdr

## Prerequisites

Build the CLI first:
```bash
cd cli && cargo build --release
# Binary: cli/target/release/do-wdr
```

Or ensure `do-wdr` is in your PATH.

## Commands

### resolve

Resolve a URL or query to markdown documentation.

```bash
do-wdr resolve <INPUT> [OPTIONS]
```

**Arguments:**
- `<INPUT>`: URL or query string to resolve

**Options:**
- `-o, --output <FILE>`: Output file (stdout if not specified)
- `-p, --provider <PROVIDER>`: Specific provider to use
- `--skip <PROVIDERS>`: Skip providers (comma-separated)
- `--providers-order <PROVIDERS>`: Custom provider order
- `--max-chars <N>`: Maximum output characters
- `--min-chars <N>`: Minimum content length
- `--profile <PROFILE>`: Execution profile (free, balanced, fast, quality)
- `--json`: Output as JSON
- `--metrics-json`: Output metrics as JSON
- `--metrics-file <FILE>`: Save metrics to file
- `--skip-cache`: Skip semantic cache
- `--synthesize`: Synthesize multiple results using AI
- `--quality-threshold <F>`: Quality threshold for content scoring
- `--max-provider-attempts <N>`: Maximum provider attempts
- `--max-paid-attempts <N>`: Maximum paid provider attempts
- `--max-total-latency-ms <MS>`: Maximum total latency in milliseconds
- `--disable-routing-memory`: Disable routing memory

### providers

List all available providers and their status.

```bash
do-wdr providers
```

### config

Show current configuration.

```bash
do-wdr config
```

### cache-stats

Show semantic cache statistics.

```bash
do-wdr cache-stats
```

## Examples

### Basic Usage

```bash
# Resolve a URL
do-wdr resolve "https://docs.rs/tokio/latest/tokio/"

# Resolve a query
do-wdr resolve "Rust async runtime comparison"

# JSON output
do-wdr resolve "Python web frameworks" --json
```

### Provider Selection

```bash
# Use specific provider
do-wdr resolve "query" --provider exa_mcp

# Skip providers
do-wdr resolve "query" --skip tavily,serper

# Custom provider order
do-wdr resolve "query" --providers-order duckduckgo,exa_mcp,tavily
```

### Output Options

```bash
# Save to file
do-wdr resolve "https://example.com" --output result.md

# JSON output to file
do-wdr resolve "query" --json --output results.json

# Include metrics
do-wdr resolve "query" --json --metrics-json
```

### Performance Profiles

```bash
# Free tier only (no API keys needed)
do-wdr resolve "query" --profile free

# Balanced speed and quality
do-wdr resolve "query" --profile balanced

# Fast results
do-wdr resolve "query" --profile fast

# High quality results
do-wdr resolve "query" --profile quality
```

### Advanced Features

```bash
# Synthesize multiple results
do-wdr resolve "query" --synthesize

# Skip cache
do-wdr resolve "query" --skip-cache

# Save metrics for analysis
do-wdr resolve "query" --metrics-file metrics.json
```

## Available Providers

| Provider | Type | Free | Description |
|----------|------|------|-------------|
| `exa_mcp` | Query | Yes | Exa MCP (free, no key) |
| `exa` | Query | No | Exa SDK (requires API key) |
| `tavily` | Query | No | Tavily comprehensive search |
| `serper` | Query | No | Google search via Serper |
| `duckduckgo` | Query | Yes | DuckDuckGo search |
| `mistral_websearch` | Query | No | Mistral AI search |
| `llms_txt` | URL | Yes | llms.txt structured docs |
| `jina` | URL | Yes | Jina Reader |
| `firecrawl` | URL | No | Firecrawl extraction |
| `direct_fetch` | URL | Yes | Direct HTML fetch |
| `mistral_browser` | URL | No | Mistral browser agent |
| `docling` | URL | No | Docling document processing |
| `ocr` | URL | No | OCR text extraction |

## Execution Profiles

| Profile | Description |
|---------|-------------|
| `free` | Use only free providers (exa_mcp, duckduckgo, llms_txt, jina, direct_fetch) |
| `balanced` | Balance between free and paid providers |
| `fast` | Prioritize speed over cost |
| `quality` | Prioritize quality over cost |

## Output Format

### Text Output (default)

Returns markdown content directly:
```markdown
# Documentation Title

Content extracted from the URL...
```

### JSON Output

```json
{
  "url": "https://example.com/docs",
  "content": "# Documentation\n\n...",
  "source": "exa_mcp",
  "score": 0.87,
  "metrics": {
    "latency_ms": 1234,
    "providers_attempted": ["exa_mcp"],
    "cache_hit": false
  }
}
```

## Configuration

Configuration is loaded from (in order):
1. CLI arguments
2. Environment variables
3. `cli/config.toml`
4. Defaults

### Environment Variables

```bash
# Provider API keys (all optional)
export EXA_API_KEY="your_key"
export TAVILY_API_KEY="your_key"
export SERPER_API_KEY="your_key"
export FIRECRAWL_API_KEY="your_key"
export MISTRAL_API_KEY="your_key"
```

## Verbose Logging

Use `-v` flags for debugging:

```bash
# Info level
do-wdr resolve "query" -v

# Debug level
do-wdr resolve "query" -vv

# Trace level
do-wdr resolve "query" -vvv
```

## Integration with Scripts

```bash
#!/bin/bash
# Example: Resolve and process results

RESULT=$(do-wdr resolve "Rust web frameworks" --json)
echo "$RESULT" | jq '.content' > frameworks.md

# Use in pipeline
do-wdr resolve "API documentation" | grep -A5 "## Authentication"
```

## Related Skills

- `do-web-doc-resolver`: Python implementation with same functionality
- `agent-browser`: Browser automation for complex web interactions
