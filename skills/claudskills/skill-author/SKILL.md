---
name: skill-author
description: "Create and refine high-quality Agent Skills (SKILL.md + bundled resources). Use when the user wants to create a new skill, improve an existing one, or turn a workflow into a reusable skill package. Covers structure, progressive disclosure, conciseness, feedback loops, and the quality checklist. Do NOT use for skill validation (use skill-check) or for prompt engineering (use prompt-craft)."
requiredApps: []
---

# Skill Author

Create skills that Claude can discover and use reliably. Based on Anthropic's official Agent Skills best practices (April 2026).

## Core Philosophy

1. **Claude is already smart** — only add context it doesn't have
2. **Context window is a shared resource** — every token competes with conversation, other skills, and system prompt
3. **Test with real usage, not assumptions** — iterate based on observed agent behavior

## Skill Creation Workflow

1. **Identify the pattern**: Complete a task manually with Claude. Note what context you repeatedly provided (schemas, rules, conventions, sequences).
2. **Draft SKILL.md**: Write frontmatter + body following the structure below.
3. **Apply conciseness pass**: For every paragraph, ask "Does Claude need this?" Remove what it already knows.
4. **Set degrees of freedom**: Match specificity to task fragility (see Freedom Levels below).
5. **Bundle resources**: Move detailed references and scripts to separate files. Keep SKILL.md as the table of contents.
6. **Test with fresh context**: Use the skill on a real task in a new session. Observe what Claude misses, over-reads, or ignores.
7. **Iterate**: Refine based on observed behavior, not assumptions.
8. **Validate**: Run `skill-check` to catch structural issues.

## SKILL.md Structure

```yaml
---
name: lowercase-hyphenated     # 3-64 chars, no reserved words
description: "Action verb + what it does + 'Use when...' trigger. Max 1024 chars."
requiredApps: [app-slug]       # Optional: connected accounts needed
---
```

**Body sections** (not all required, pick what fits):

| Section | Purpose | When to include |
|---------|---------|-----------------|
| Quick start | Fastest path to using the skill | Always |
| Steps / Workflow | Sequential procedure with checklist | Multi-step tasks |
| Rules / Constraints | Hard requirements | When consistency matters |
| Output | Concrete output example | When skill produces artifacts |
| References | Links to bundled files | When >500 lines needed |
| Errors / Limitations | Known failure modes | When edge cases exist |

## Freedom Levels

Match specificity to how fragile the operation is:

| Level | When | Instruction style |
|-------|------|-------------------|
| **High** | Multiple valid approaches, context-dependent | Text guidance, heuristics |
| **Medium** | Preferred pattern exists, some variation OK | Pseudocode or parameterized scripts |
| **Low** | Fragile operations, exact sequence required | Specific scripts, minimal parameters |

Analogy: narrow bridge with cliffs (low freedom) vs open field (high freedom).

## Progressive Disclosure

SKILL.md = table of contents. Detailed content lives in separate files.

```
my-skill/
├── SKILL.md              # Overview + workflow (<500 lines)
├── references/
│   ├── api-reference.md  # Loaded when Claude needs API details
│   └── schemas.md        # Loaded when Claude needs data shapes
├── scripts/
│   └── validate.py       # Executed (not read into context)
└── cache/
    └── user-ids.json     # Discovered data, reused across runs
```

**Rules**:
- Keep references ONE level deep from SKILL.md (no nested chains)
- Reference files >100 lines should have a table of contents
- Scripts are executed via bash, not loaded into context (only output consumes tokens)
- Make execution intent clear: "Run `validate.py`" (execute) vs "See `validate.py`" (read)

## Description Writing

The description is how Claude selects this skill from 100+ options. It must work as a standalone trigger.

- **Third person**: "Processes Excel files..." not "I can help you..."
- **Action verb first**: "Extract, Generate, Validate, Transform..."
- **Include trigger**: "Use when..." clause
- **Include negative trigger**: "Do NOT use for..." when confusion is likely
- **Be specific**: Include key terms Claude would match against

## Feedback Loops

For quality-critical tasks, always include a validation cycle:

```
Produce output → Validate (script or checklist) → Fix errors → Repeat
```

For batch/destructive operations, use **plan-validate-execute**:
1. Analyze input → create plan file (e.g., `changes.json`)
2. Validate plan with script → catch errors before execution
3. Execute only after validation passes

## Common Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Explaining what Claude already knows | Delete it |
| Hardcoded dates or versions | Use "old patterns" section or omit |
| Inconsistent terminology (mix "field"/"box"/"element") | Pick one term, use consistently |
| Multiple approaches offered when one is best | Pick the best, commit to it |
| Magic numbers without justification | Document the reasoning |
| Deeply nested file references | Flatten to one level from SKILL.md |
| Assuming packages are installed | Check availability, document deps |

## Quality Checklist

Before shipping a skill:

- [ ] Description: action verb + what + "Use when..." + "Do NOT use for..."
- [ ] SKILL.md body: under 500 lines
- [ ] Each paragraph earns its token cost
- [ ] Freedom level matches task fragility
- [ ] References are one level deep
- [ ] Scripts handle errors explicitly (no punting to Claude)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Tested with real usage in fresh context
- [ ] Feedback loop included for quality-critical outputs
- [ ] `skill-check` validation passed
