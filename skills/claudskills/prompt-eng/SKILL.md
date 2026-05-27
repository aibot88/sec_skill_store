---
name: prompt-eng
description: |
  Prompt engineering specialist for system prompt optimization. Designs effective prompts, A/B testing, prompt injection detection, AI response quality.
  Triggers: 'prompt', 'system prompt', 'AI quality', 'prompt injection', 'LLM output'.
  Use when: creating/improving prompts, testing effectiveness, debugging poor AI responses, securing against injection.
allowed-tools:
  - Read
  - Grep
  - Edit
context:
  - path: config/llm-models.php
  - path: config/tools.php
  - path: config/agent-prompts.php
---

# Prompt Engineering

System prompt optimization specialist for BotFacebook.

## MCP Tools Available

- **context7**: `query-docs` - Get latest OpenAI/Anthropic prompt engineering docs
- **sentry**: `search_issues` - Find AI response quality issues
- **claude-mem**: `search`, `get_observations` - Search past prompt iterations

## Memory Search (Before Starting)

**Always search memory first** to find past prompt iterations and improvements.

### Recommended Searches

```
# Search for prompt changes
search(query="prompt optimization", project="bot-fb", type="feature", limit=5)

# Find A/B test results
search(query="prompt test", project="bot-fb", concepts=["trade-off"], limit=5)
```

### Search by Scenario

| Scenario | Search Query |
|----------|--------------|
| Improving prompts | `search(query="prompt improvement", project="bot-fb", type="feature", limit=5)` |
| Injection prevention | `search(query="prompt injection", project="bot-fb", type="bugfix", limit=5)` |
| Quality issues | `search(query="AI response quality", project="bot-fb", concepts=["problem-solution"], limit=5)` |

## Quick Start

เมื่อปรับ prompt ให้คิด:
1. **เป้าหมายคืออะไร?** → Define success criteria
2. **Context ครบไหม?** → Add necessary context
3. **วัดผลได้ไหม?** → Create test cases

## Core Principles

| Principle | Description |
|-----------|-------------|
| Be Specific | ระบุงานชัดเจน ไม่กว้างเกินไป |
| Provide Examples | ให้ตัวอย่าง 2-3 คู่ input/output |
| Set Boundaries | กำหนดข้อห้ามชัดเจน |
| Define Persona | ระบุบทบาท น้ำเสียง ภาษา |

**Full patterns & templates:** See [PROMPT_PATTERNS.md](PROMPT_PATTERNS.md)

## A/B Testing

| Metric | Description |
|--------|-------------|
| Response accuracy | ตอบตรงคำถามไหม |
| Tone consistency | น้ำเสียงคงที่ไหม |
| User satisfaction | ลูกค้าพอใจไหม |
| Escalation rate | ส่งต่อคนบ่อยไหม |

**Test framework & analysis:** See [TESTING_GUIDE.md](TESTING_GUIDE.md)

## Security (Injection Protection)

| Strategy | Purpose |
|----------|---------|
| Input Sanitization | Remove dangerous chars |
| Delimiter Usage | Separate user input |
| Pattern Detection | Detect attack patterns |
| Output Validation | Check for leaks |

**Full security guide:** See [SECURITY.md](SECURITY.md)

## Common Tasks

| Task | Steps |
|------|-------|
| Create prompt | Goal → Persona → Knowledge → Examples → Constraints |
| Improve prompt | Collect failures → Identify pattern → Fix → A/B test |
| Debug response | Check context → Check examples → Check model |
| Secure prompt | Delimiters → Sanitize → Detect → Validate |

## Debug Checklist

- [ ] Knowledge base complete?
- [ ] Examples representative?
- [ ] Boundaries appropriate?
- [ ] Model suitable for task?

## Second AI Prompt Patterns

Second AI checks use specialized prompt templates for verification:

| Service | Prompt Pattern | Purpose |
|---------|---------------|---------|
| `FactCheckService` | KB context + claim extraction | Verify factual accuracy against knowledge base |
| `PolicyCheckService` | Policy rules + response analysis | Check business rule compliance |
| `PersonalityCheckService` | Brand guidelines + tone analysis | Ensure brand consistency |
| `UnifiedCheckService` | Combined single-call prompt | All checks in one LLM call (2+ checks) |

### PromptInjectionDetector

`app/Services/SecondAI/PromptInjectionDetector.php` runs BEFORE Second AI checks:
- Pattern-based detection (regex) for common injection attempts
- Detects role-playing attacks, system prompt extraction, instruction override
- Lightweight (no LLM call) — runs on every incoming user message

## Key Files

| File | Purpose |
|------|---------|
| `config/agent-prompts.php` | Agent prompt templates (Thai/English) |
| `flows.system_prompt` column | System prompt storage (Flow model, not Bot) |
| `app/Services/SecondAI/` | AI verification pipeline |
| `app/Services/SecondAI/PromptInjectionDetector.php` | Injection detection (regex-based) |
| `app/Services/SecondAI/UnifiedCheckService.php` | Single-call unified mode |

