---
name: symphony-claude-lane
description: Teach an orchestrator smart multi-model dispatch for Symphony + Linear workflows. Use when an agent needs to route tasks to Claude or Codex based on task characteristics, create a durable routing profile, and define visual verification, privacy, and closeout rules for a mixed-model repo.
metadata:
  short-description: Smart multi-model dispatch for Symphony + Linear
---

# Symphony + Claude Lane

Use this skill when a team has **Symphony + Linear** and wants their orchestrator to **pick the right agent for each task** — routing work to Claude Code or Codex based on what the task actually needs, not just a static label.

This skill also works for teams that want to run **Claude-only** workers without Codex.

## Prerequisites

- The target repo already uses Symphony + Linear, or is clearly intended to.
- The target repo has a place for durable orchestration guidance such as `AGENTS.md` or `.orchestration/`.
- At least one of Claude Code or Codex can be run as a worker against the repo.
- Browser verification can be done with Playwright or an equivalent automation path (recommended but not required).

If those conditions are not true, explain the gap and stop or redirect to a more appropriate setup skill.

## Required workflow

1. Inspect the target repo, existing `AGENTS.md`, workflow docs, and issue contract.
2. Confirm the repo is a real candidate for multi-model dispatch, not just a generic coding repo.
3. Confirm the base Symphony workflow already has workspace bootstrap assertions, a no-progress stop-loss, and a stable issue contract before adding model routing.
4. Analyze the repo's work patterns to recommend a routing strategy. Consider what types of tasks appear in the backlog: bounded implementation, UI/frontend, complex reasoning, browser-dependent verification, code review, documentation, security-sensitive changes, E2E testing.
5. Ask the user about their routing preferences: should the orchestrator analyze task characteristics automatically, or use label-only routing? Which agent capabilities matter most for this repo? Is this a mixed-model or Claude-only setup?
6. Create or update a repo-local routing profile from `assets/claude-lane-profile.example.yaml`, including routing strategy, model selection criteria, privacy rules, and cleanup or retention rules for that adopter's actual storage hotspots.
7. Prefer same-project label-filtered routing when labels are used. Recommend a separate queue or Linear project only when the adopter needs stronger operational separation.
8. Add routing and dispatch guidance to the target repo's orchestration docs. Use `assets/claude-lane-guidance.snippet.md` as a starting point. Do not hardcode repo specifics back into this shared skill.
9. Help the adopter set up Claude worker launch capability. Use `references/worker-launch.md` for the secure launch pattern and `assets/claude-worker.reference.sh` as a starting point for the launcher script. Use `assets/worker-prompt.template.md` as the basis for worker prompts. Adapt all paths, auth, and MCP config to the adopter's environment.
10. For tickets that affect rendered output, default to Playwright-based verification before closeout.
11. Define closeout, retry, `In Review`, and cleanup behavior as part of the routing contract, including how worktrees, snapshots, and other heavy local artifacts are removed safely.

## Safety defaults

- Route based on task characteristics by default. Use labels as overrides, not as the sole routing mechanism.
- When task characteristics are ambiguous and no label override exists, prefer the safer choice: Codex for bounded sandbox-compatible work, Claude for anything requiring tools, browser access, or deep reasoning.
- Keep ambiguous tickets in the more conservative path until the repo proves the routing is stable.
- Persist user routing choices into the repo-local profile, not only in chat.
- Inherit the base workflow guardrails instead of treating any model's lane as exempt from them.
- Prefer operator-reviewed closeout unless the adopter already has a safe self-close path.
- If issue state cannot be confirmed during closeout or cleanup, preserve artifacts and stop rather than guessing.
- Do not assume every adopter's storage pressure looks the same; document repo-specific cleanup hotspots in the repo-local profile.
- Do not put secrets, credentials, tokens, session cookies, personal data, or raw customer payloads into issues, comments, screenshots, traces, or other artifacts.

## Reference map

- Read `references/setup.md` first when deciding whether the target repo is ready.
- Read `references/routing.md` before analyzing work patterns or asking the user about routing preferences.
- Read `references/dispatch.md` when defining queue split, model selection, and worker lifecycle.
- Read `references/worker-launch.md` when helping the adopter set up the Claude worker launcher, MCP config, or security practices.
- Read `references/visual-verification.md` before writing browser-verification policy.
- Read `references/closeout.md` when defining `In Review`, outcome blocks, retry behavior, or self-close rules.
- Read `references/troubleshooting.md` when a worker stalls, exhausts turns, or drifts from the routing contract.
- Read `references/examples.md` when you need concrete ticket-routing examples or model selection patterns.

## Output expectations

When this skill is applied well, the target repo should end up with:

- a working Claude worker launch setup (launcher script, MCP config, prompt template)
- a durable routing profile with model selection criteria
- clear routing rules — task-characteristic analysis, label overrides, or both
- explicit privacy and redaction rules for all worker artifacts
- repo-local orchestration guidance describing what each model handles and why
- a Playwright-first visual verification rule for tickets that affect rendered output
- inherited base-workflow guardrails called out explicitly
- explicit closeout and retry behavior for all workers regardless of model
- a documented fallback for control-plane outages or missing tracker state
- a cleanup and retention policy that covers worktrees, snapshots, and repo-specific storage hotspots
