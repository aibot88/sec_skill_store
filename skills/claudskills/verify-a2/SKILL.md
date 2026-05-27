---
name: verify-a2
description: Verify adoption criterion A2 (Agent-Authored Contributions) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify A2 — Agent-Authored Contributions

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No agent-authored code in git history; all commits are purely human-written |
| 1 | Occasional co-authored commits; agents contributed to fewer than 25% of recent changes |
| 2 | Regular agent contributions; agents co-authored 25–75% of recent changes |
| 3 | Agents autonomously create pull requests; more than 75% of implementation work has significant agent involvement |

"Recent" = last 90 days or last 50 commits, whichever covers more changes.

## Evidence

### Total commits in the last 90 days
!`git log --oneline --since="90 days ago" 2>/dev/null | wc -l || echo "(git not available or no history)"`

### Total commits (last 50, for young repos)
!`git log --oneline -50 2>/dev/null | wc -l || echo "(no git history)"`

### Agent co-authored commits (last 90 days)
!`git log --since="90 days ago" --format="%H %s" 2>/dev/null | head -5 || echo "(no recent commits)"`
!`git log --since="90 days ago" --format="%B" 2>/dev/null | grep -ic "co-authored-by\|🤖\|generated with\|claude\|copilot\|github-actions\[bot\]" 2>/dev/null || echo "0"`

### Co-authored commit messages (sample)
!`git log --since="90 days ago" --format="%s%n%b" 2>/dev/null | grep -i "co-authored-by\|🤖\|generated with claude\|copilot" | head -20 || echo "(no agent co-authorship markers found)"`

### Agent-authored commits in last 50 commits
!`git log -50 --format="%B" 2>/dev/null | grep -ic "co-authored-by.*claude\|co-authored-by.*copilot\|co-authored-by.*anthropic\|🤖\|generated with claude" 2>/dev/null || echo "0"`

### PR descriptions indicating agent implementation (if PRs exist as merge commits)
!`git log --since="90 days ago" --merges --format="%s %b" 2>/dev/null | grep -i "claude\|copilot\|agent\|🤖" | head -10 || echo "(no agent-attributed merge commits)"`

### Presence of autonomous PR-creation tooling
!`ls .github/workflows/ 2>/dev/null && grep -l -i "claude\|copilot\|agent\|openai" .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | head -5 || echo "(no agent-invoking workflows found)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for A2.

Key calculation: divide agent-co-authored commit count by total recent commit count to get the percentage.

Scoring guide:
- **Level 0**: Zero agent-authored commits in git history — no co-authorship markers, no bot commits, no agent-attributed changes.
- **Level 1**: Agent co-authorship markers exist in fewer than 25% of recent commits. Occasional use, not yet habitual.
- **Level 2**: Agent co-authorship markers exist in 25–75% of recent commits. Habitual use across a significant portion of implementation work.
- **Level 3**: Agent co-authorship markers exist in more than 75% of recent commits, OR evidence of autonomous PR creation (bot-authored PRs, agent-triggering workflows that open PRs).

Report in exactly this format:

**A2 — Agent-Authored Contributions**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence, including the calculated percentage if possible]
