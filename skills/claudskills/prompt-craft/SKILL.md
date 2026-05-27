---
name: prompt-craft
description: "Write and refine production-grade prompts and tool definitions for Claude. Use when the user needs to craft a system prompt, improve an existing prompt, design tool schemas (ACI), or apply techniques like few-shot, XML structuring, role prompting, or chain-of-thought. Covers Claude 4.6 specifics. Do NOT use for skill authoring (use skill-author) or agent architecture (use agent-patterns)."
requiredApps: []
---

# Prompt Craft

Write production-grade prompts for Claude's latest models. Based on Anthropic's official prompting best practices (April 2026, Claude 4.6).

## Golden Rule

> Show your prompt to a colleague with minimal context. If they'd be confused, Claude will be too.

## Prompt Structure Template

```xml
<system>
  [Role definition — one sentence]
  [Key constraints and rules]
  [Output format specification]
</system>

<context>
  [Background the model needs — documents, data, history]
</context>

<examples>
  <example>
    <input>[Sample input]</input>
    <output>[Desired output]</output>
  </example>
</examples>

<instructions>
  [The actual task — clear, sequential steps]
</instructions>
```

**Document placement**: Long documents go at the TOP, queries at the BOTTOM. This improves quality by up to 30%.

## Core Techniques

### 1. Be Explicit, Not Implicit

Claude 4.6 is literal. It follows precise instructions rather than inferring intent.

| Instead of | Write |
|---|---|
| "Make it good" | "Write in active voice, under 200 words, with one concrete example per point" |
| "Don't use markdown" | "Write in flowing prose paragraphs with no bullet points" |
| "Be thorough" | "Cover all three scenarios: success, partial failure, and complete failure" |

Say what **to do**, not what **not** to do. Provide the **why** behind instructions — Claude generalizes from motivation.

### 2. XML Tags for Structure

Wrap distinct content types in descriptive tags. This eliminates ambiguity.

- `<instructions>`, `<context>`, `<input>`, `<output>` — top-level sections
- `<documents>` → `<document index="1">` → `<source>`, `<document_content>` — multi-doc inputs
- `<example>` inside `<examples>` — few-shot examples
- `<rules>`, `<constraints>` — hard requirements
- Custom tags work too: `<smoothly_flowing_prose_paragraphs>` steers format

### 3. Few-Shot Examples (3-5)

Examples are the most reliable way to steer format, tone, and structure.

**Requirements**:
- **Relevant**: Mirror real use cases
- **Diverse**: Cover edge cases, avoid unintended patterns
- **Wrapped**: Use `<example>` tags to distinguish from instructions

### 4. Role Prompting

One sentence in the system prompt focuses behavior:

```
You are a senior security engineer reviewing code for vulnerabilities.
```

### 5. Chain-of-Thought

For complex reasoning, ask Claude to work step-by-step. But prefer **adaptive thinking** (`thinking: {type: "adaptive"}`) over manual CoT — it outperforms in internal evals.

Guide thinking with:
```
"Choose an approach and commit to it. Avoid revisiting decisions
unless new information directly contradicts your reasoning."
```

## Claude 4.6 Specifics

### Prefills Are Gone
No more prefilling the assistant turn. Migrate to:
- Format control → explicit formatting instructions
- No preamble → "Begin your response with..."
- Continuations → provide context in user message

### Concise by Default
Claude 4.6 is more direct, less verbose. If you want detail:
```
"After completing a task with tool use, provide a quick summary of the work done."
```

### Opus Overthinks
Opus 4.6 does extensive upfront exploration. To control:
- Remove "If in doubt, use [tool]" → now causes overtriggering
- Replace "Default to using [tool]" with "Use [tool] when it would enhance understanding"
- Lower `effort` setting as a fallback

### Parallel Tool Calling
Claude excels at parallel execution. Boost to ~100% with:
```
"If no dependencies between calls, make all independent calls in parallel."
```

## Tool Design (ACI)

> Invest as much effort in Agent-Computer Interface as you would in Human-Computer Interface.

### Tool Description Principles

1. **Claude's perspective**: Is it obvious how to use this tool from the description alone?
2. **Great docstrings**: Write like you're onboarding a junior dev
3. **Natural formats**: Keep close to what the model sees in training data (not JSON-escaped code)
4. **Room to think**: Give enough output tokens before the model paints itself into a corner
5. **Poka-yoke**: Make mistakes structurally impossible (absolute paths > relative paths)
6. **Test and iterate**: Run many inputs, observe actual mistakes, fix the tool design

### Tool Schema Tips

| Do | Don't |
|---|---|
| Use descriptive parameter names | `param1`, `data`, `input` |
| Include example usage in description | Assume the model will figure it out |
| Require absolute file paths | Accept relative paths (Claude loses track after `cd`) |
| Return concise, meaningful results | Dump entire API responses |
| Namespace tools by function area | Mix unrelated tools together |

## Prompt Optimization Workflow

1. **Define success criteria** before writing the prompt
2. **Write a first draft** — clear, explicit, structured
3. **Test with real inputs** — observe actual failures
4. **Add examples** targeting the failure modes
5. **Iterate** — each fix should address a specific observed problem
6. **Measure** — use evals, not vibes

## Output Format Control

Ranked by effectiveness:
1. XML format indicators: `<smoothly_flowing_prose_paragraphs>`
2. Explicit format instructions: "Respond in JSON with keys: name, score, reasoning"
3. Match prompt style to desired output style (remove markdown from prompt → less markdown in output)
4. Few-shot examples showing exact format

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Vague instructions ("be helpful") | Specific criteria ("respond in ≤3 sentences with one actionable suggestion") |
| Over-prompting tools ("CRITICAL: MUST use this tool") | Normal language ("Use this tool when...") |
| Relying on prefills for format | Explicit format instructions |
| Single example | 3-5 diverse examples |
| Mixing instructions with data | XML tags to separate concerns |
| Long prompt with no structure | Hierarchical XML sections |
