---
name: hyper-implement
description: Execute a plan task-by-task using fresh subagents, with spec compliance + code quality reviews between tasks. Use when the user invokes /hyperclaude:hyper-implement, or when about to start a multi-task implementation from a plan in .hyperclaude/plans/. Skip for single-step trivia or fast prototyping.
---

# hyper-implement

Plan execution gate. Reads a plan, dispatches a fresh subagent per task, runs two reviews (spec compliance, then code quality) before marking each task complete. The hyperclaude-native equivalent of superpowers' subagent-driven-development — but using our own agents (`implementer`, `verifier`) and our own gate skills.

## When to use

- User typed `/hyperclaude:hyper-implement [path]`.
- A multi-task plan exists (typically in `.hyperclaude/plans/`) and you're about to execute it.

Skip when:
- The plan is one step — just do it directly.
- Tasks are tightly coupled and benefit from shared context.
- You're prototyping; reviews are overhead at this stage.

## How to invoke

**Invocation argument:** $ARGUMENTS

### Step 1 — Resolve the plan path

In priority order:

1. If $ARGUMENTS is non-empty, treat it as a path and use it.
2. Else, find the most recent plan via the Bash tool:

   ```bash
   ls -1t .hyperclaude/plans/*.md 2>/dev/null | head -1
   ```

3. If nothing found, tell the user: "No plan file found. Write your plan to `.hyperclaude/plans/<slug>.md` first." Stop.

### Step 2 — Parse and track

Read the plan with the Read tool. Extract every `## Task N: <title>` section with its full text — files-to-create/modify, step-by-step checkboxes, verification commands, commit message.

Use TodoWrite to create a todo per task. Mark the first as `in_progress`.

### Step 3 — Per-task loop

For EACH task in order:

1. **Implementer.** Dispatch via the Agent tool. Prefer `subagent_type: hyperclaude:implementer`. Prompt MUST include:
   - The full task text (paste it; do not make the subagent re-read the plan file).
   - Project context: where this fits, recent commits, base SHA before this task.
   - Global constraints from the plan's preamble (zero deps, sandbox rules, no `commands/` directory, etc.).
   - A self-review checklist before reporting back.
   - Expected report format: status (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), files changed, test counts, commit SHA.

2. **Spec compliance review.** Once implementer reports DONE, dispatch a fresh **general-purpose** subagent (NOT the verifier — verifier runs tests, doesn't compare to spec). Prompt:
   - The full task text.
   - The implementer's report (verbatim).
   - The git SHA range (`<base>..<head>`).
   - Instruction: read the actual code; don't trust the report. Look for missing requirements AND unrequested extras.
   - Expected outcome: ✅ compliant, or ❌ with specific file:line issues.

   If issues found → re-dispatch the implementer with the fix list → re-review. Loop until ✅.

3. **Code quality review.** After spec ✅, dispatch another fresh general-purpose subagent. Focus on:
   - Clarity (names, decomposition, file responsibility).
   - Test quality (do tests verify behavior, not types?).
   - YAGNI (any unrequested abstractions or features?).
   - Consistency with existing codebase style.
   - Severity-tagged issues: Critical / Important / Minor.

   Loop until reviewer approves (Minor-only is acceptable; Critical/Important must be fixed).

4. **Verifier (optional, when applicable).** If the task added tests or build steps, dispatch `subagent_type: hyperclaude:verifier`. Verifier runs `node --test`, `bash scripts/test/smoke.sh`, lint, etc. and reports PASS / PARTIAL / FAIL with verbatim output. Verifier never modifies files.

5. **Mark task complete in TodoWrite.** Move on.

### Step 4 — Final pass

After all tasks:

- Run `bash scripts/test/smoke.sh` (or whatever the plan defines as final acceptance) and confirm 0 failures.
- If `/hyperclaude:hyper-code-review` is available, run it for a Codex-side review of the entire diff. Useful catch for cross-task issues.
- If the plan's final task includes a tag step (`git tag -a vX.Y.Z`), do NOT push it; leave that to the user.

## Rules

- **Fresh subagent per task.** Don't reuse implementer subagents across tasks — context pollution kills focus.
- **Two reviews per task.** Spec compliance FIRST (catches scope drift), then code quality (catches style/clarity). Skipping either means you'll ship bugs.
- **Don't trust implementer self-reports.** Reviewers must read the actual code.
- **Fix loops are mandatory.** Reviewer ❌ → implementer fixes → re-review. No "close enough."
- **Continuous execution.** Don't pause to ask the user between tasks — execute the whole plan. Stop only on BLOCKED, genuine ambiguity, or all tasks done.
- **Never push.** Tags and pushes are user actions. The skill creates them locally only if the plan says to.

## Anti-patterns

- Using `verifier` agent for code review. Wrong role — verifier runs tests, doesn't critique code.
- Skipping spec compliance review because "the plan was clear." It never is.
- Single subagent handling multiple tasks (the whole reason we don't do manual orchestration).
- Marking a task complete with reviewer issues still open.
- Following the implementer's own model selection. Pick model per task complexity at dispatch time:
  - Mechanical (1-2 files, exact spec): haiku
  - Standard (multi-file, integration): sonnet
  - Architectural / judgment-heavy: opus

## Reference

The v0.1 implementation history (`d5754a2..461df61`) was produced with this exact flow (under superpowers:subagent-driven-development at the time). 11 tasks, ~33 subagent dispatches, two real bugs caught by reviews before they hit main.
