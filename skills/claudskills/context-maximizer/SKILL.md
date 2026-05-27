---
name: context-maximizer
description: Exploit the 1M token context (Opus 4.6 / Sonnet 4.6) for full codebase awareness in SpecKit. Intelligently loads constitution, specs, skills, and codebase files while staying within token limits. Prioritizes critical files and provides context usage reports.
effort: medium
---

# Context Maximizer

Leverage the 1M token context window (GA since March 2026, available on both Opus 4.6 and Sonnet 4.6) to provide full codebase awareness during spec generation, planning, and development. With 64k default output tokens (up to 128k on Opus 4.6) and support for up to 600 images/PDF pages per request, smart loading strategies ensure the most relevant context is always available.

## When to Use

- During spec generation (specify skill)
- When creating technical plans (plan skill)
- Before implementing features that require understanding multiple systems
- When analyzing dependencies across the codebase
- For comprehensive code reviews requiring full context

## Context Budget

Total available: **1,000,000 tokens** (~4,000,000 characters)

### Priority Levels

1. **Critical** (always loaded): Constitution, active specs, current plan
2. **High**: Skills relevant to feature domain
3. **Medium**: Codebase files matching feature patterns
4. **Low**: Documentation, references, examples

### Token Allocation Strategy

```
Constitution:       ~10,000 tokens   (1%)
Active Specs:       ~50,000 tokens   (5%)
Current Plan:       ~20,000 tokens   (2%)
Skills (3-5):      ~100,000 tokens  (10%)
Codebase:          ~700,000 tokens  (70%)
Documentation:      ~50,000 tokens   (5%)
Buffer:             ~70,000 tokens   (7%)
```

## Features

### 1. Context Budget Calculator

Analyzes project structure and estimates token usage:

```bash
python scripts/analyze_context.py /path/to/project
```

Output:
```json
{
  "total_tokens": 850000,
  "by_category": {
    "constitution": 8500,
    "specs": 42000,
    "skills": 95000,
    "codebase": 650000,
    "docs": 54500
  },
  "within_limit": true,
  "utilization": "85%"
}
```

### 2. Smart Loading Strategy

Automatically determines what to load based on feature domain:

```bash
python scripts/analyze_context.py /path/to/project --feature "posts-crud"
```

Output includes prioritized file list:
```json
{
  "loading_plan": {
    "critical": [
      "constitution.yml",
      "specs/1-posts-crud/prd.json",
      "specs/1-posts-crud/plan.json"
    ],
    "high": [
      "skills/speckit/specify/",
      "skills/speckit/plan/",
      "skills/database/"
    ],
    "medium": [
      "src/db/schema/posts.ts",
      "src/lib/services/posts.ts",
      "src/app/api/posts/"
    ],
    "low": [
      "docs/database.md",
      "docs/api-integrations.md"
    ]
  }
}
```

### 3. Context Report

Shows what's loaded and provides optimization suggestions:

```bash
python scripts/analyze_context.py /path/to/project --report
```

Output:
```json
{
  "loaded": {
    "files": 156,
    "total_tokens": 820000,
    "breakdown": {
      "constitution": { "tokens": 8500, "percentage": 1.0 },
      "specs": { "tokens": 42000, "percentage": 5.1 },
      "skills": { "tokens": 95000, "percentage": 11.6 },
      "codebase": { "tokens": 620000, "percentage": 75.6 },
      "docs": { "tokens": 54500, "percentage": 6.6 }
    }
  },
  "warnings": [],
  "suggestions": [
    "Consider excluding test fixtures to save ~15,000 tokens",
    "Large component files could be summarized to save ~25,000 tokens"
  ]
}
```

### 4. Exclusion Patterns

Automatically excludes non-essential files:

- `node_modules/`, `.git/`, `dist/`, `build/`
- `*.lock`, `package-lock.json`, `yarn.lock`
- Binary files: `*.png`, `*.jpg`, `*.pdf`, `*.zip`
- Large generated files
- Vendored dependencies
- Test fixtures (optional)

## Usage in SpecKit

### During Specification

```bash
# Load full context for spec generation
python scripts/analyze_context.py . --feature "user-auth" --output loading-plan.json

# Use in specify prompt
/specify --context loading-plan.json
```

### During Planning

```bash
# Load context for technical planning
python scripts/analyze_context.py . --spec specs/2-user-auth/prd.json --output plan-context.json

# Use in plan prompt
/plan --context plan-context.json
```

### During Implementation

```bash
# Load context for specific sub-story
python scripts/analyze_context.py . --task "US-001-1" --output task-context.json
```

## Token Estimation

Uses industry-standard approximation:
- **1 token ≈ 4 characters** (for English text and code)
- Actual usage may vary by ±15% depending on content type

More accurate estimation:
- Source code: 1 token ≈ 3.5-4 characters
- Documentation: 1 token ≈ 4-5 characters
- JSON/structured data: 1 token ≈ 3-4 characters

## Pattern Matching

Feature domain → relevant files:

| Domain | Patterns |
|--------|----------|
| `database` | `schema/`, `migrations/`, `*.sql`, `db/` |
| `api` | `api/`, `routes/`, `actions/`, `services/` |
| `auth` | `auth/`, `middleware/`, `lib/auth` |
| `frontend` | `components/`, `app/`, `pages/`, `ui/` |
| `posts` | `posts`, `content`, `articles` |
| `users` | `users`, `profiles`, `accounts` |
| `payments` | `payments`, `billing`, `stripe` |

## Advanced Usage

### Custom Prioritization

Create a `.context-priority.json` file in your project:

```json
{
  "always_include": [
    "src/lib/constants.ts",
    "src/types/index.ts"
  ],
  "always_exclude": [
    "src/legacy/",
    "scripts/one-time/"
  ],
  "domain_patterns": {
    "posts": ["posts", "articles", "content", "editor"],
    "users": ["users", "profiles", "auth", "accounts"]
  }
}
```

### Context Optimization Tips

1. **Summarize large generated files**: Instead of loading full Prisma clients or type definitions, load summaries
2. **Skip test fixtures**: Exclude `__fixtures__/`, `__mocks__/` if not needed
3. **Compress documentation**: Load only relevant sections of large docs
4. **Use references**: Load file summaries with references to full content

## Integration with Ralph++

Context maximizer integrates with ralph-agent-teams:

```python
# In team orchestrator
context_plan = load_context_plan("loading-plan.json")
agent_config = {
    "context_files": context_plan["high"] + context_plan["medium"],
    "max_context_tokens": 900000
}
spawn_agent(story, config=agent_config)
```

## Performance

- **Analysis time**: ~2-5 seconds for 500 files
- **Loading time**: Instant (plan generation only)
- **Memory usage**: Minimal (file scanning, not loading)

## Warnings

The tool will warn when:
- Total estimated tokens exceed 950,000 (95% capacity)
- Single file exceeds 100,000 tokens
- Excluded patterns might contain relevant files
- Domain patterns match too many files (>200)

## References

See `references/loading-strategies.md` for detailed strategies and case studies.
