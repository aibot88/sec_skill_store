---
name: improve-a2
description: Improve adoption criterion A2 (Agent-Authored Contributions) by setting up the tooling and guidance that enables and tracks agent contributions. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---

# Improve A2 — Agent-Authored Contributions

## Current State

### Git co-authorship in recent history
!`git log --since="90 days ago" --oneline 2>/dev/null | wc -l || echo "0 total"`
!`git log --since="90 days ago" --format="%B" 2>/dev/null | grep -ic "co-authored-by\|🤖\|claude\|copilot" 2>/dev/null || echo "0 agent commits"`
!`git log -10 --format="%s %b" 2>/dev/null | head -20 || echo "(no recent commits)"`

### Agent context file
!`ls CLAUDE.md AGENTS.md 2>/dev/null || echo "(none)"`
!`grep -i "co-author\|commit\|git\|agent\|claude" CLAUDE.md AGENTS.md 2>/dev/null | head -10 || echo "(no commit guidance)"`

### Git config (co-authorship setup)
!`git config --global user.email 2>/dev/null || echo "(no git config)"`
!`ls .git/hooks/prepare-commit-msg 2>/dev/null && echo "(prepare-commit-msg hook exists)" || echo "(no prepare-commit-msg hook)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: 0% agent co-authorship in recent commits
- Level 1: < 25% of recent commits have agent markers
- Level 2: 25–75% of recent commits have agent markers
- Level 3: > 75%, or evidence of autonomous PR creation

Note: Levels 2 and 3 require genuine changes in how the team uses agents — they cannot be achieved by tooling alone. This skill focuses on enabling and encouraging agent contributions through tooling and guidance.

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
The goal is to set up the infrastructure so agents can start contributing:

1. **Update CLAUDE.md** (create if absent) with a git workflow section:
   ```markdown
   ## Git Workflow
   
   When committing changes, always add a co-authorship trailer:
   ```
   git commit -m "feat: description
   
   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```
   
   Or use the shorthand when Claude Code generates the commit message automatically.
   ```

2. **Create a git commit message template** at `.git/commit_template.txt`:
   ```
   # <type>: <subject>
   #
   # Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```
   Then configure it: `git config commit.template .git/commit_template.txt`
   (Note: this is local to the repo — add instructions to CLAUDE.md for new contributors)

3. **Create a basic implementation skill** (`.claude/skills/implement-task/SKILL.md`) if none exists, to give agents a reusable workflow for making contributions. Use the do-next-task pattern as a model.

**If current level is 1 → raise to 2:**
Level 2 requires 25–75% agent involvement. The tooling is already in place; the bottleneck is habitual use:

1. **Strengthen CLAUDE.md** with explicit guidance that agent use is the default, not the exception:
   ```markdown
   ## Development Workflow
   
   Agent use is the default for all implementation work. For each task:
   1. Assign the task to Claude Code via /do-next-task or by describing the task
   2. Review the resulting diff rather than writing code from scratch
   3. Humans focus on requirements, architecture decisions, and code review
   ```

2. **Create a GitHub Actions workflow** that checks for co-authorship markers and adds a reminder comment on PRs that lack them:
   Create `.github/workflows/agent-adoption.yml`:
   ```yaml
   name: Agent Adoption Check
   on: [pull_request]
   jobs:
     check-co-authorship:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 20
         - name: Check for agent co-authorship
           run: |
             count=$(git log origin/${{ github.base_ref }}..HEAD --format="%B" | grep -ic "co-authored-by" || echo 0)
             total=$(git log origin/${{ github.base_ref }}..HEAD --oneline | wc -l)
             echo "Agent commits: $count / $total"
             if [ "$count" -eq 0 ] && [ "$total" -gt 0 ]; then
               echo "::notice::No agent co-authorship detected in this PR. Consider using Claude Code for implementation."
             fi
   ```

**If current level is 2 → raise to 3:**
Level 3 requires > 75% agent involvement or autonomous PR creation. Focus on autonomous PR creation:

1. Create `.github/workflows/agent-implement.yml` — a workflow triggered by issue labelling that uses a Claude Code agent to implement the issue and open a PR:
   ```yaml
   name: Agent Implementation
   on:
     issues:
       types: [labeled]
   jobs:
     implement:
       if: github.event.label.name == 'agent-implement'
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Implement issue with agent
           # Uses Claude Code CLI or Anthropic API
           # See CLAUDE.md for implementation details
           run: echo "Configure your agent implementation step here"
   ```

2. Add documentation to CLAUDE.md explaining the `agent-implement` label workflow.

**If already at level 3:**
Report that A2 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level, and what human behavior changes are additionally needed.
