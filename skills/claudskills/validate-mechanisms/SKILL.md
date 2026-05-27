---
name: validate-mechanisms
description: >
  Periodic smoke test for behavioral mechanism compliance.
  Scans the workspace for statically-detectable violations of rules in mechanism-registry.md.
  Use when: (1) user says "validate mechanisms", "檢查機制", "/validate-mechanisms",
  (2) as part of a periodic health check, (3) after major framework changes.
metadata:
  author: Polaris
  version: 1.0.0
user-invocable: true
---

# Validate Mechanisms — Behavioral Compliance Smoke Test

Layer 3 of the mechanism protection system (alongside rules + post-task audit). Runs statically-checkable canary signals from `rules/mechanism-registry.md`.

## When to Run

- After a major Polaris version update
- Periodically (e.g., weekly) as a health check
- When you suspect mechanisms have drifted

## Steps

### Step 1: Load Mechanism Registry

Read `.claude/rules/mechanism-registry.md` to get the full list of mechanisms and their canary signals.

### Step 2: Run Static Checks

Execute the following checks that can be verified without a live conversation:

#### 2a. Scope Header Enforcement (`scope-header-enforcement`)

For each company directory under `.claude/rules/{company}/`:
- List all `.md` files
- Check each for `> **Scope:` header pattern
- 🔴 FAIL if any file is missing the header

#### 2b. Bash Command Patterns (`no-cd-in-bash`)

Read `.claude/settings.json` and `.claude/settings.local.json` (if exists):
- Check `permissions.allow` patterns for `cd *` patterns
- 🟡 WARN if `cd * &&` patterns exist (encourages `cd` usage)
- ✅ PASS if no `cd`-encouraging patterns found

#### 2c. Skill Routing Table Completeness (`skill-first-invoke`, `no-manual-skill-steps`)

Read `rules/skill-routing.md` routing table. For each skill listed:
- Verify the skill directory exists under `.claude/skills/`
- Verify the SKILL.md file exists and has a `description:` in frontmatter
- 🔴 FAIL if a routed skill doesn't exist
- 🟡 WARN if a skill exists but is not in the routing table (may be internal)

#### 2d. Memory Company Isolation (`memory-company-hard-skip`)

Scan all memory files in the memory directory:
- Read each file's frontmatter
- If content references company-specific identifiers (JIRA project keys, repo names, org names) but lacks `company:` field → 🟡 WARN
- Cross-reference with workspace-config.yaml company list

#### 2e. Sub-agent Role Definitions (`model-tier-selection`, `delegate-exploration`)

Read `skills/references/sub-agent-roles.md`:
- Verify it defines the 3 mandatory standards (Completion Envelope, Model Tier Selection, Context Isolation)
- Verify specialized protocols exist (QA Challenger/Resolver, Architect Challenger, Critic)
- 🟡 WARN if mandatory standards section or specialized protocols are missing

#### 2f. Feedback Memory Frontmatter (`feedback-trigger-count-update`, `graduation-at-three-triggers`)

Scan all feedback-type memory files:
- Check each has `trigger_count` and `last_triggered` fields
- 🟡 WARN if any feedback memory is missing these fields
- 🔴 FAIL if any feedback memory has `trigger_count >= 3` (should have been graduated)

#### 2g. Mechanism Registry Freshness

Compare the mechanism IDs in the registry against actual rule files:
- For each mechanism, verify the source file still exists
- For each mechanism, verify the referenced section still exists (grep for key phrases)
- 🟡 WARN if a mechanism references a deleted/renamed section

#### 2h. Dev-Guide Ghost References

Grep all SKILL.md files for `dev-guide`:
- 🔴 FAIL if any reference to `dev-guide` SKILL.md is found (this was a v1.11.0 drift issue)

#### 2i. Hardcoded Path Detection

Grep all generic SKILL.md files (excluding `{company}/`) for `~/work/`:
- 🔴 FAIL if any `~/work/` literal path is found (should use `{base_dir}`)
- Exclude intentional documentation references (e.g., "do NOT hardcode `~/work/`")

### Step 3: Generate Report

Produce a structured report:

```
## Mechanism Compliance Report

Date: {today}
Registry version: {from mechanism-registry.md}
Checks run: {count}

### Results

| Check | Mechanism ID | Status | Details |
|-------|-------------|--------|---------|
| Scope headers | scope-header-enforcement | ✅ PASS | 5/5 files OK |
| Bash patterns | no-cd-in-bash | ✅ PASS | No cd patterns |
| ... | ... | ... | ... |

### Summary
- ✅ PASS: {count}
- 🟡 WARN: {count}
- 🔴 FAIL: {count}

### Recommended Actions
{For each FAIL/WARN, one-line fix suggestion}
```

### Step 4: Suggest Fixes

For each 🔴 FAIL:
- Propose a specific fix (which file to edit, what to change)
- Ask user for confirmation before applying

For each 🟡 WARN:
- Note in report but don't block

## Relationship to Other Skills

- **`/validate-isolation`** — focuses on multi-company isolation (scope headers, memory tags, cross-company conflicts). Overlaps with checks 2a and 2d here, but validate-mechanisms is broader
- **Post-task audit** (in `feedback-and-memory.md`) — runs after each task, checks conversation-level canaries. validate-mechanisms checks static/workspace-level canaries

## What This Does NOT Check

Conversation-level mechanisms that require observing live behavior:
- `skill-first-invoke` (would need to observe tool call order)
- `delegate-exploration` (would need to count consecutive Read calls)
- `post-task-feedback-reflection` (would need to observe end-of-task behavior)
- `no-file-reread` (would need to track file reads across conversation)

These are covered by the post-task audit (Layer 2), not this skill (Layer 3).
