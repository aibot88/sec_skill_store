---
name: innovate-loopback
description: Run the Vibe Innovation Framework mini-gate assessment to scope, justify, and execute a loop-back. Use when evidence in the current phase suggests an earlier phase's output is wrong, when a red-team challenge cannot be addressed in the current phase, or when an assumption from an earlier phase has been falsified.
user-invocable: true
argument-hint: "[trigger evidence]"
---

**Loop-back trigger:** $ARGUMENTS

Read the following files in order before acting.

1. `.claude/docs/loop_back_protocol.md` (the canonical runbook with the eight-step mini-gate)
2. `.claude/docs/orchestrator.md` (the *Loop-back and iteration protocol* section, for budget rules and escalation options)
3. `.claude/docs/principles_and_antipatterns.md` (Principle 8: iteration has a budget)
4. The current ICD Section 7 (Iteration log) and the relevant earlier phase prompt only after the target phase is identified.

Then execute the runbook exactly as specified there. The runbook is self-contained: trigger confirmation, type and target identification, scope, carry-forward inventory, budget check, re-entry pre-amble, forward propagation, and logging.

## Operating notes

1. **Budget enforcement is non-negotiable.** Maximum 2 intra-phase iterations, maximum 2 inter-phase loop-backs to the same target, maximum 5 total inter-phase loop-backs. The kill threshold rule (any assumption falsified in two separate cycles is dead) applies regardless of remaining budget.
2. **Pause, do not reset.** The current phase's output is preserved and marked *provisional*. The phase resumes after the loop-back resolves. Do not delete the in-progress work.
3. **Re-entry pre-amble is verbatim.** When the user runs `/innovate-phase N` for the target phase, the Step 1 pre-amble must include all five fields from runbook Step 6. Do not paraphrase.
4. **Logging is mandatory.** Append a row to ICD Section 7 with the loop type, from-phase, to-phase, trigger evidence, scope, and outcome. Update iteration counters. Add a Section 9 (Changelog) entry with the same date.
5. **Escalation handling.** If a budget limit is reached, do not loop back. Surface the four escalation options (accept lower TRL, grant one more iteration with specific evidence expected, pivot, or kill) and let the user decide. Do not pre-empt the decision.
6. **Working language.** Detect the user's working language and translate the eight runbook prompts. Keep the structure faithful and the prompts terse.

Respond in the language the user is writing in.
