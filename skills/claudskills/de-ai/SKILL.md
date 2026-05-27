---
name: de-ai
description: Transform AI-sounding text into human, authentic writing while preserving meaning and facts. Focuses on quality improvement over detection evasion. Supports multiple languages (English, Russian, German, Spanish, French). Use when the user asks to humanize text, remove AI tells, make writing sound more human, or de-AI content.
allowed-tools: Read, Write, Bash
---

Follow the full instructions in `/Users/dandaka/.claude/skills/de-ai/system.md`.

When invoked with `/de-ai`:
- If the user passes `--file <path>`, read that file and humanize its content
- If the user passes inline text after `/de-ai`, use that as the input
- If no input is provided, ask the user to provide text or a file path
- Default: interactive mode (ask clarifying questions before processing)
- Output: revised text only, unless `--explain` flag is set

Supported flags: `--file <path>`, `--language <en|ru|de|es|fr>`, `--register <personal|essay|critique|narrative|technical|academic>`, `--interactive <true|false>`, `--explain <true|false>`
