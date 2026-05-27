---
name: "mcp-server-planning"
description: "Plan an MCP server with clear tool scope, auth model, error behavior, evaluation approach, and rollout boundaries."
---

Use this skill when a team wants to expose external capabilities through an MCP server.

Plan in this order:

- define the user tasks the MCP server must unlock
- choose the smallest useful tool surface before chasing endpoint completeness
- specify auth, secret handling, and least-privilege expectations
- design tool schemas and output shape for discoverability and safe automation
- define evaluation cases that prove the server is useful for real agent tasks

Deliver:

- candidate tools and responsibilities
- auth and secret-handling model
- failure and retry expectations
- evaluation plan
- rollout notes and open risks

Avoid:

- exposing raw API coverage without task-level value
- hiding side effects behind vague tool descriptions
- skipping evaluation until after implementation
