# MACP Research Assistant — Skill Definition

## Identity

- **Name:** MACP Research Assistant
- **Version:** 0.1.0-alpha
- **Author:** YSenseAI / FLYWHEEL TEAM
- **License:** MIT
- **Repository:** https://github.com/creator35lwb-web/macp-research-assistant

## Description

A CLI tool for tracking AI-powered research with complete citation provenance. It enables multi-agent research workflows where each AI assistant's contributions are tracked, traced, and recallable.

## Prerequisites

- Python 3.10+
- `pip install -r requirements.txt` (installs `requests`, `jsonschema`)

## Commands

### `discover` — Find and store research papers

Discovers papers from HuggingFace, arXiv, or the hysts/daily-papers dataset (12,700+ curated papers). Stores them in `.macp/research_papers.json` and auto-creates knowledge tree directories.

```bash
# By date (HuggingFace Daily Papers)
python tools/macp_cli.py discover --date 2026-02-15

# By date range
python tools/macp_cli.py discover --date-range 2026-02-10:2026-02-15

# By search query (HuggingFace Paper Search API)
python tools/macp_cli.py discover --query "multi-agent systems" --limit 5

# By arXiv ID
python tools/macp_cli.py discover --arxiv-id 2602.06570

# Search hysts/daily-papers dataset (12,700+ papers with abstracts)
python tools/macp_cli.py discover --hysts "multi-agent collaboration" --limit 5

# hysts dataset by date
python tools/macp_cli.py discover --hysts-date 2025-02-14

# Cross-pipeline discovery (conflict detection)
python tools/macp_cli.py discover --arxiv-id 2501.04306 --hysts "LLM scientific research"
```

**Output:** Papers are added to `.macp/research_papers.json` with deduplication. Each paper gets a directory in `.macp/research/{slug}/` (knowledge tree).

### `analyze` — AI-powered paper analysis

Sends a paper's abstract to an LLM for automated summarization, insight extraction, methodology identification, and research gap detection. Auto-creates a learning session with the results.

```bash
# Analyze a paper (auto-selects free-tier provider)
export GEMINI_API_KEY=your-key-here
python tools/macp_cli.py analyze 2602.06570

# Use a specific provider
python tools/macp_cli.py analyze 2602.06570 --provider anthropic

# Skip consent prompt (for automation)
python tools/macp_cli.py analyze 2602.06570 --yes
```

**Parameters:**
- `arxiv_id` (required): arXiv ID of the paper (must be in KB or will be auto-fetched)
- `--provider`: LLM provider — `gemini` (free, default), `anthropic`, `openai`
- `--yes` / `-y`: Skip the consent confirmation prompt

**Environment Variables (BYOK):**
- `GEMINI_API_KEY` — Google Gemini (free tier, recommended)
- `ANTHROPIC_API_KEY` — Anthropic Claude (paid)
- `OPENAI_API_KEY` — OpenAI (paid)

**Output:** Returns structured analysis (summary, key insights, methodology, research gaps, strength score). Automatically creates a learning session in `.macp/learning_log.json` and updates the paper status to `analyzed`.

**Consent:** By default, prompts the user before sending any data to external APIs. Use `--yes` to skip for automation.

### `handoff` — Multi-agent research handoff

Creates a structured handoff record when passing research context between agents. Captures completed work, pending actions, relevant papers, and a snapshot of the knowledge base state.

```bash
python tools/macp_cli.py handoff \
  --from claude --to gemini \
  --summary "Completed analysis of 5 transformer papers" \
  --completed "Analyzed papers;Built knowledge graph" \
  --pending "Review research gaps;Export report" \
  --papers 2602.06570,2602.07890
```

**Parameters:**
- `--from` (required): Agent initiating the handoff
- `--to` (required): Agent receiving the handoff
- `--summary` / `-s` (required): Summary of the research task or context
- `--completed`: Semicolon-separated list of completed actions
- `--pending`: Semicolon-separated list of pending actions for the receiving agent
- `--papers` / `-p`: Comma-separated arXiv IDs relevant to this handoff

**Output:** Creates a handoff record in `.macp/handoffs.json` with a knowledge base state snapshot (paper count, session count, citation count).

### `learn` — Record a learning insight

Records an insight linked to specific papers, creating a learning session in `.macp/learning_log.json`.

```bash
python tools/macp_cli.py learn "T-Score 0.3-0.5 is optimal for conflict data" \
  --papers 2602.06570,2602.07890 \
  --agent claude \
  --tags ai-alignment,conflict-data
```

**Parameters:**
- `summary` (required): The key insight text
- `--papers` / `-p` (required): Comma-separated arXiv IDs
- `--agent` / `-a`: Which AI produced this insight (default: "human")
- `--tags` / `-t`: Comma-separated tags
- `--insight` / `-i`: Concise key insight (defaults to summary)
- `--force` / `-f`: Add even if papers aren't in the knowledge base

### `cite` — Record a citation

Links a paper to a project or document with context.

```bash
python tools/macp_cli.py cite 2602.06570 \
  --project "GODELAI C-S-P Design" \
  --context "T-Score range used for conflict data collection" \
  --agent manus-ai
```

**Parameters:**
- `arxiv_id` (required): The arXiv ID of the cited paper
- `--project` / `-p` (required): Name of the project citing this paper
- `--context` / `-c` (required): How the paper is being used
- `--agent` / `-a`: Which agent made the citation (default: "human")

### `recall` — Search the knowledge base

Natural language search across papers, learning sessions, citations, and handoffs. Searches enriched fields including abstracts, insights, tags, methodology, research gaps, and handoff context.

```bash
python tools/macp_cli.py recall "conflict data for AI alignment" --limit 10
```

**Parameters:**
- `question` (required): Natural language search query
- `--limit` / `-l`: Max results per category (default: 5)

### `status` — View knowledge base status

Shows paper counts, learning sessions, citations, and recent activity.

```bash
python tools/macp_cli.py status
```

### `export` — Export knowledge base to Markdown report

Generates a clean, readable Markdown research report from the knowledge base. Supports filtering by tag and named research directories.

```bash
# Full report (saved to .macp/exports/)
python tools/macp_cli.py export

# Named research directory (creates .macp/research/{slug}/report.md)
python tools/macp_cli.py export --title "GodelAI Research Showcase"

# Filter by tag
python tools/macp_cli.py export --tag agentic-ai

# Custom output path
python tools/macp_cli.py export --output report.md
```

**Parameters:**
- `--title`: Research title — creates named directory in `.macp/research/` (knowledge tree)
- `--output` / `-o`: Custom output file path (default: `.macp/exports/research_report_{timestamp}.md`)
- `--tag` / `-t`: Filter report to only include sessions/papers with this tag

**Output:** Generates a Markdown report with sections for Summary, Papers (with abstracts and insights), Learning Sessions (with analysis details), Citations (as table), and Handoffs.

## Knowledge Tree

The MACP Research Assistant auto-creates a knowledge tree under `.macp/research/`:

```
.macp/research/
  llm4sr-a-survey-on-large.../      <- Analyzed paper (deep root)
    paper.json                       <- Paper metadata
    analysis.json                    <- AI analysis history
    README.md                        <- Human-readable summary
  octotools-an-agentic.../          <- Analyzed paper (deep root)
    paper.json
    analysis.json
    README.md
  godelai-research-showcase/        <- Named research export
    report.md                        <- Full Markdown report
  mindagent-emergent.../            <- Discovered paper (shallow root)
    paper.json
    README.md
```

Each paper gets its own directory that grows as research deepens: discovery creates `paper.json`, analysis adds `analysis.json`, and exports create `report.md` — like roots growing deeper.

## Data Files

All data is stored in `.macp/` and validated against JSON schemas in `schemas/`.

| File | Schema | Purpose |
|------|--------|---------|
| `.macp/research_papers.json` | `schemas/research_papers_schema.json` | Discovered and analyzed papers |
| `.macp/learning_log.json` | `schemas/learning_log_schema.json` | Learning sessions and insights |
| `.macp/citations.json` | `schemas/citations_schema.json` | Citation records |
| `.macp/knowledge_graph.json` | `schemas/knowledge_graph_schema.json` | Relationship graph |
| `.macp/handoffs.json` | `schemas/handoffs_schema.json` | Agent handoff records |

## Typical Workflow

```
1. discover  → Find papers (Conflict phase)
2. analyze   → AI-powered insight extraction (Synthesis phase, automated)
3. learn     → Manual insight recording (Synthesis phase, human)
4. cite      → Apply to projects (Propagation phase)
5. handoff   → Pass context between agents (Proto-A2A)
6. recall    → Query knowledge base anytime
7. export    → Generate Markdown research report
8. status    → Monitor progress
```

## Security

- All inputs are validated and sanitized
- JSON writes use atomic operations (temp file + rename)
- All data validated against JSON schemas before write
- No subprocess calls — all API access via HTTP
- No API keys required (uses free-tier HuggingFace + arXiv APIs)

## Integration Points

- **MACP Protocol:** `.macp/` directory follows MACP v2.0 specification
- **Knowledge Graph:** Run `python tools/knowledge_graph.py` to generate relationship graph + Mermaid diagram
- **VerifiMind-PEAS:** Validated by X-Z-CS RefleXion Trinity (see `peas/` directory)
