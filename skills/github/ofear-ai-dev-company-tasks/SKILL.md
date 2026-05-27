# Task: Security/Dependency Audit Before Deploy

**Priority:** High
**Category:** Security
**Effort:** Small — one new skill + one babysitter gate

## Problem

Current security model defends against agent misbehavior (command blocklist, path sandbox,
TruffleHog). It does NOT protect against supply chain risk:

- Dependency CVEs
- Malicious npm packages
- Unsafe Docker base images

A Developer could introduce a vulnerable dependency and it would pass review, QA, and deploy.

## What to Build

A `security-audit` skill that runs before DevOps deploys.

### Tools to invoke (per stack, auto-detected)

| Stack   | Command                        |
| ------- | ------------------------------ |
| Node.js | `npm audit --audit-level=high` |
| Python  | `pip-audit`                    |
| Rust    | `cargo audit`                  |
| Docker  | `trivy image <image>`          |
| General | `trivy fs .`                   |

### Integration points

1. Add `security_audit_passed` as a new babysitter gate in `devops` agent (mirrors Developer's
   babysitter gates)
2. If audit finds HIGH/CRITICAL CVEs → post `[ESCALATION]` to Linear, block deploy
3. If audit finds MODERATE → post warning comment, allow deploy
4. Audit result summary appended to the deploy comment

### Files to change

- `extensions/clawe-scheduler/src/guards/babysitter.ts` — add `security_audit_passed` gate
- `skills/security-audit/SKILL.md` — new skill
- `extensions/clawe-scheduler/src/agents/tool-executor.ts` — add audit commands to allowed list

## Acceptance Criteria

- [ ] `npm audit` runs automatically before every deploy on Node.js projects
- [ ] HIGH/CRITICAL CVEs block the deploy with an `[ESCALATION]` comment
- [ ] Audit result is visible in the Linear deploy comment
- [ ] Gate is skipped gracefully if stack is undetected (no false blocks)
