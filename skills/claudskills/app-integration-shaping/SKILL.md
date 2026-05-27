---
name: "app-integration-shaping"
description: "Decide how an external app or service should be integrated, including boundaries, auth scopes, ownership, and failure handling."
---

Use this skill when deciding whether a new external integration belongs in the system and how it should be shaped.

Compare these options explicitly:

- direct API client inside the application
- separate service or worker
- MCP server or connector-style integration
- no integration yet because the problem is still underspecified

Checklist:

- define the user or system workflow that needs the integration
- identify data movement, ownership, and trust boundaries
- specify required auth scopes and whether they are acceptable
- call out rate limits, retries, partial failure, and observability needs
- end with the recommended integration style and why it is the least-wrong option

Avoid:

- defaulting to MCP because it is fashionable
- burying auth scope risk inside implementation detail
- merging integration design with product prioritization
