<command-name>expanso-skill</command-name>

# Expanso Skills Slash Command

This skill provides access to the Expanso Skills Marketplace - 172+ pre-built data processing pipelines.

## Usage

```
/expanso-skill [subcommand] [options]
```

### Subcommands

#### List Skills by Category
```
/expanso-skill list [category]
```

Categories: `ai`, `security`, `transforms`, `utilities`, `workflows`

Example:
```
/expanso-skill list ai
/expanso-skill list security
/expanso-skill list  # lists all categories with counts
```

#### Show Skill Details
```
/expanso-skill show <skill-name>
```

Example:
```
/expanso-skill show text-summarize
/expanso-skill show cve-scan
```

#### Search Skills
```
/expanso-skill search <query>
```

Example:
```
/expanso-skill search json
/expanso-skill search pii
```

#### Generate Invocation Code
```
/expanso-skill invoke <skill-name> [--mcp|--cli]
```

Example:
```
/expanso-skill invoke text-embed --cli
/expanso-skill invoke morning-briefing --mcp
```

## Response Format

When the user invokes this command, you should:

1. **For `list`**: Show a table of skills in the category with name, description
2. **For `show`**: Display full skill details including inputs, outputs, credentials, backends
3. **For `search`**: Show matching skills across all categories
4. **For `invoke`**: Generate ready-to-use code for CLI or MCP invocation

## Implementation

The skill catalog is available at:
- Full: https://raw.githubusercontent.com/expanso-io/expanso-skills/main/catalog.json
- Minimal: https://raw.githubusercontent.com/expanso-io/expanso-skills/main/catalog-minimal.json

Use WebFetch to retrieve the catalog when needed.

## Example Interactions

### User: `/expanso-skill list security`

**Response:**
| Skill | Description |
|-------|-------------|
| `cve-scan` | Scan SBOM for known CVE vulnerabilities |
| `pii-detect` | Detect PII in text |
| `pii-redact` | Redact sensitive information |
| `sign-envelope` | Cryptographically sign data |
| `verify-signature` | Verify cryptographic signatures |
| `audit-envelope` | Create audit trail for data |
| `secrets-scan` | Detect leaked secrets in code |
| `sbom-generate` | Generate software bill of materials |
| `policy-check` | Check data against security policies |
| `jwt-verify` | Verify JWT tokens |
| `tls-inspect` | Inspect TLS certificates |
| `log-sanitize` | Sanitize logs of sensitive data |
| `hash-digest` | Generate cryptographic hashes |
| `password-generate` | Generate secure passwords |

### User: `/expanso-skill show text-embed`

**Response:**
## text-embed

**Description:** Generate embedding vectors from text for RAG and semantic search

**Category:** ai | **Version:** 1.0.0

### Inputs
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `text` | string | yes | - | Text to embed (up to 8191 tokens) |
| `model` | string | no | text-embedding-3-small | Embedding model to use |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `embedding` | array | Vector embedding (1536 or 3072 dimensions) |
| `metadata` | object | Model info, dimensions, token count |

### Credentials
| Name | Required | Description |
|------|----------|-------------|
| `OPENAI_API_KEY` | no | OpenAI API key (not required if using Ollama) |

### Backends
- **openai** (remote): Requires OPENAI_API_KEY
- **ollama** (local): Supports nomic-embed-text, all-minilm

### User: `/expanso-skill invoke text-embed --cli`

**Response:**
```bash
# CLI invocation for text-embed

# Set credentials (if using OpenAI)
expanso credentials set OPENAI_API_KEY sk-your-key-here

# Run the skill
echo '{"text": "Your text to embed here"}' | \
  expanso run https://raw.githubusercontent.com/expanso-io/expanso-skills/main/skills/ai/text-embed/pipeline-cli.yaml

# Or with local Ollama backend
EXPANSO_BACKEND=ollama echo '{"text": "Your text here"}' | \
  expanso run https://raw.githubusercontent.com/expanso-io/expanso-skills/main/skills/ai/text-embed/pipeline-cli.yaml
```

## Notes

- Skills are hosted at https://github.com/expanso-io/expanso-skills
- All skills support both CLI and MCP modes
- Credentials are stored locally and never transmitted
- Many AI skills support local Ollama backends for fully offline operation
