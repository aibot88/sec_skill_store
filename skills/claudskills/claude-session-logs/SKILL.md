---
name: claude-session-logs
description: >
  Access Claude Code session logs (JSONL transcripts and SQLite FTS index) for
  cross-session context, handoff, and memory retrieval.
  Use when: resuming work from a previous session, finding past decisions,
  referencing prior implementations, or building session continuity.
  Skip when: data is in PIL memory (check gfv_memory.db first).
---

# Claude Session Logs

> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure.

### GFV Infrastructure Integration

**Data Locations**:
```bash
# Claude Code session logs (JSONL)
~/.claude/projects/-Users-$USER-Documents-Code/

# Indexed transcripts (SQLite FTS)
~/Documents/Code/gfv-brain/data/transcripts.db

# PIL memory (higher-level, consolidated)
~/Documents/Code/gfv-brain/data/gfv_memory.db
```

---

## Overview

Claude Code stores session transcripts as JSONL files. These are indexed into a SQLite FTS database for fast full-text search. This skill covers reading raw logs, querying the FTS index, and extracting actionable context from past sessions.

## Priority Order for Context Retrieval

```
1. PIL Memory (gfv_memory.db)     ← Curated, high-signal
2. Transcripts Index (transcripts.db) ← Full session history
3. Raw JSONL Logs                  ← Last resort, verbose
```

Always check PIL memory first — it contains distilled knowledge from past sessions.

## Reading Raw Logs

```bash
# Find recent session files
ls -lt ~/.claude/projects/-Users-$USER-Documents-Code/*.jsonl | head -5

# Read a specific session
cat ~/.claude/projects/-Users-$USER-Documents-Code/session_id.jsonl | python3 -m json.tool
```

### JSONL Format

Each line is a JSON object:
```json
{
  "role": "user|assistant",
  "content": "message text",
  "timestamp": "2026-04-17T14:30:00Z",
  "tool_calls": [...]
}
```

## Querying the FTS Index

```python
import sqlite3

db = sqlite3.connect(os.path.expanduser(
    '~/Documents/Code/gfv-brain/data/transcripts.db'
))

# Full-text search
results = db.execute("""
    SELECT session_id, timestamp, content, rank
    FROM transcripts_fts
    WHERE transcripts_fts MATCH ?
    ORDER BY rank
    LIMIT 20
""", ("Acme Corp attribution",)).fetchall()

for session_id, ts, content, rank in results:
    print(f"[{ts}] Session {session_id[:8]}... (rank={rank})")
    print(f"  {content[:200]}")
```

## Querying PIL Memory

```python
db = sqlite3.connect(os.path.expanduser(
    '~/Documents/Code/gfv-brain/data/gfv_memory.db'
))

# Search by topic
results = db.execute("""
    SELECT category, key, content, created_at
    FROM memories
    WHERE content LIKE ?
    ORDER BY created_at DESC
    LIMIT 10
""", ("%vertex ai%",)).fetchall()
```

Or use the MCP tool:
```
query_memory(query="vertex ai migration", category="architecture", limit=10)
```

## Writing Session Context

At the end of each session, write key findings to memory:

```python
# Via claude_memory.py
python3 ~/Documents/Code/gfv-brain/scripts/claude_memory.py write \
    --category "architecture" \
    --key "vertex-ai-migration" \
    --content "Migrated LLM calls to Vertex AI via ADC. Embeddings stay on AI Studio (3072-dim). Project: nth-record-492622-j3."
```

## Common Queries

```bash
# Find when we last worked on a topic
python3 ~/Documents/Code/gfv-brain/scripts/claude_memory.py context --limit=10

# Search across all sessions for a keyword
grep -rl "ServiceTitan" ~/.claude/projects/-Users-$USER-Documents-Code/*.jsonl

# Find sessions by date
ls -lt ~/.claude/projects/-Users-$USER-Documents-Code/*.jsonl | head -20
```

## Anti-Patterns
- ❌ Reading raw JSONL when PIL memory has the answer
- ❌ Not writing session summaries at end of work
- ❌ Trusting old session data without verifying current state
- ❌ Searching raw logs for data that should be in Supabase ontology

## Related Skills
- **gfv-dream-mode**: Consolidates session fragments into durable PIL knowledge
- **pil-memory-bus**: 4-tier memory hierarchy for context retrieval
- **supabase-access**: Persistent ontology (more durable than session logs)

## References
- **Session Protocol**: `/session-protocol` workflow
- **Memory Script**: `~/Documents/Code/gfv-brain/scripts/claude_memory.py`
- **GFV Standard**: Session Persistence rule (write to JSONL at session end)


<verification_gate>
# Delivery Gate

STOP AND VERIFY BEFORE DECLARING THIS TASK COMPLETE.

1. Did you verify that the execution meets all documented requirements safely?
2. Ensure you have not bypassed any "requires_human_approval" constraints.
</verification_gate>

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
