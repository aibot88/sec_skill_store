---
name: "Governance"
version: "1.4.0"
description: "Enforces engineering standards and code quality policies. Use during code reviews, before commits, when discussing standards or compliance, for quality audits, and when running retrospectives. Trigger phrases include 'run a retro', 'retrospective', 'code review', 'run review', or 'audit standards'."
category: development
tags:
  - governance
  - code-review
  - standards
  - compliance
  - quality
author: Smith Horn
triggers:
  keywords:
    - code review
    - review this
    - commit
    - before I merge
    - standards
    - compliance
    - code quality
    - best practices
    - retro
    - retrospective
    - test edge function
    - edge function test
    - mock Deno
    - Deno is not defined
  explicit:
    - /governance
    - /review
    - /retro
    - /edge-test
composes:
  - linear
---

# Governance Skill

Enforces engineering standards from [standards.md](../../../docs/internal/architecture/standards.md). Identifies all issues and fixes them immediately -- no deferral, no tickets, no asking for permission. All severities are fixed in the same PR.

## Quick Audit

```bash
docker exec skillsmith-dev-1 npm run audit:standards
```

## Pre-Commit Checklist

```bash
docker exec skillsmith-dev-1 npm run typecheck
docker exec skillsmith-dev-1 npm run lint
docker exec skillsmith-dev-1 npm run format:check
docker exec skillsmith-dev-1 npm test
docker exec skillsmith-dev-1 npm run audit:standards
```

## Sub-Documentation

| Document | Contents |
|----------|----------|
| [code-review-template.md](code-review-template.md) | Full code review report template with field descriptions |
| [retro-template.md](retro-template.md) | Full retrospective template with completion checklist |
| [edge-function-test.md](edge-function-test.md) | Edge Function test scaffold generator with vi.hoisted() pattern |

For detailed instructions -- code review workflow, severity guide, zero deferral policy, approach validation rules, retrospective workflow, type safety patterns, and CI failure reference -- see [agent-prompt.md](agent-prompt.md).
