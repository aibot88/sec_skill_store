---
name: hook-context-attachment-injection
description: "Surface hook-provided startup context by packaging it as metadata attachments before the agent's first request."
metadata:
  author: ychampion
---

# SKILL: Hook Context Attachment Injection
**Domain:** multi-agent
**Trigger:** Use when startup hooks generate extra context that a child agent should see before it makes its first model request.
**Source Pattern:** Distilled from reviewed startup-hook context seeding flows.

## Core Method
Collect any hook-provided context while the child agent is starting, combine it into a structured metadata attachment, and inject that attachment into the initial conversation state before the query loop begins. This lets startup hooks enrich the child agent without mutating shared parent state or pretending the hook output came from the user. Keeping the payload as metadata preserves provenance and keeps the startup context easy to reason about.

## Key Rules
- Gather hook output before the first request so the initial reasoning step sees the same context as later logging and transcript paths.
- Package hook output as metadata attachments, not as synthetic user or assistant text.
- Keep attachment construction deterministic so retries and resumes produce the same startup context.

## Example Application
If a startup hook gathers repository hints and policy notes for a spawned coding agent, inject them as one metadata attachment before the child begins planning.

## Anti-Patterns (What NOT to do)
- Do not append startup hook context after the first model turn.
- Do not mix hook metadata into user-authored content.
- Do not mutate shared parent conversation state just to deliver child-specific startup hints.
