---
name: validate
description: >
  Framework health check combining isolation and mechanism compliance.
  Two modes: (1) Isolation — scan for multi-company contamination (scope headers,
  memory tags, cross-company conflicts). (2) Mechanisms — static smoke test of
  behavioral canaries from mechanism-registry.md.
  Trigger: "validate", "檢查", "health check", "validate isolation", "檢查隔離",
  "validate mechanisms", "檢查機制", "/validate".
metadata:
  author: Polaris
  version: 1.0.0
user-invocable: true
---

# Validate — Framework Health Check

Two modes, run individually or together.

## Mode Selection

| Input | Mode |
|-------|------|
| "validate" / "檢查" | Run both |
| "validate isolation" / "檢查隔離" | Isolation only |
| "validate mechanisms" / "檢查機制" | Mechanisms only |

---

## Mode 1: Isolation

Scans for multi-company contamination issues.

### Checks

1. **L2 scope headers** — every `.md` in `.claude/rules/{company}/` must have `> **Scope: {company}**`
2. **Cross-company conflicts** — contradictory rules across companies, hardcoded cross-company references
3. **Memory company tags** — company-specific memories must have `company:` frontmatter
4. **MEMORY.md index format** — company-scoped entries need `[company]` prefix
5. **User data leak** — run `scripts/scan-user-data-leak.sh` to detect hardcoded user-specific data (GitHub username, email) in shared rules. See DP-007

### Report format

```
### Isolation
✅ {company-a}: 5/5 scope headers OK
🔴 {company-b}: 2/4 missing scope headers
🟡 3 memories appear company-specific but lack company: field
```

---

## Mode 2: Mechanisms

Static smoke test of canaries from `rules/mechanism-registry.md`.

### Checks

1. **Scope headers** (overlaps isolation mode — skip if already run)
2. **Bash patterns** — check settings.json for `cd *` patterns that encourage `cd` usage
3. **Skill routing completeness** — every routed skill exists, every skill has routing entry
4. **Memory company isolation** — same as isolation mode (skip if already run)
5. **Sub-agent role definitions** — `sub-agent-roles.md` has mandatory standards
6. **Feedback memory frontmatter** — `trigger_count` + `last_triggered` present
7. **Registry freshness** — mechanism source files still exist
8. **Ghost references** — no references to deleted skills (e.g., `dev-guide`)
9. **Hardcoded paths** — no `~/work/` literals in generic SKILL.md files
10. **Hooks in settings.local.json** — scan each project's `.claude/settings.local.json` for a top-level `hooks` key → 🟡 WARN. All hooks must live in `settings.json`; `settings.local.json` with `hooks` causes shallow merge to silently override the entire `hooks` object, disabling all shared PostToolUse/PreToolUse hooks
11. **L2 embedding integrity** — run `scripts/validate-l2-embedding.sh` against `skills/references/l2-embedding-registry.md`. Validates every registered DP-030 canary's script exists, SKILL.md step anchor matches, L1 hook file + settings.json registration exist, and Layer declaration is consistent. Exit 1 → 🔴 FAIL (surface per-entry errors to user); exit 2 → 🔴 FAIL (registry meta error)

### Report format

```
### Mechanisms
| Check | Status | Details |
|-------|--------|---------|
| Scope headers | ✅ PASS | 5/5 OK |
| Bash patterns | ✅ PASS | No cd patterns |
| Routing table | 🟡 WARN | 2 skills not in routing |
| ... | ... | ... |
```

---

## Combined Summary

```
## Validate Report — {date}

{isolation results}
{mechanism results}

Summary: {total} checks | {pass} ✅ | {warn} 🟡 | {fail} 🔴
```

For each 🔴 FAIL: propose a specific fix, ask user before applying.
For each 🟡 WARN: note in report, don't block.

## What This Does NOT Check

Conversation-level mechanisms (skill-first-invoke, delegate-exploration, etc.) require observing live behavior — covered by post-task audit, not this skill.

## Post-Task Reflection (required)

> **Non-optional.** Execute before reporting task completion.

Run the checklist in [post-task-reflection-checkpoint.md](../references/post-task-reflection-checkpoint.md).
