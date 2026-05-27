---
name: innovate-redteam
description: Run the Vibe Innovation Framework red team protocol on any artifact (problem statement, concept, business model, experiment design, prototype, decision). Use when stress-testing an artifact against adversarial framings outside the usual phase Step 7 moment, or as a standalone sanity check before locking an output.
user-invocable: true
argument-hint: "[phase-N section-X | free | decision]"
---

**Target requested:** $ARGUMENTS

Read the following files in order before acting.

1. `.claude/docs/red_team_protocol.md` (the canonical protocol, with question sets per phase and per lens)
2. `.claude/docs/principles_and_antipatterns.md` (the cognitive bias watchlist that the protocol implements)
3. The relevant phase prompt only if a Phase artifact is targeted (for example, `phase_2_ideation.md` for Phase 2 Step 7).

Then execute the protocol exactly as specified there. The protocol is self-contained: triggers, lens catalog, question sets per phase, scoring rubric, output template.

## Operating notes

1. **Input resolution.** Parse the argument into one of three input shapes. `phase-N section-X` resolves to the corresponding ICD section and runs the phase-specific question set. `free` plus a free-text artifact runs the generic set. `decision` plus a pending decision runs the Phase 5 decision question set. If the argument is empty, ask which input shape applies before proceeding.
2. **Lens count.** Use at least three lenses, with at least one user-side, one competitor-side, and one failure-mode lens. Two passes are required if the first pass produces only *Addressed* and *Out of scope* outcomes.
3. **No straw men.** Each lens generates the strongest version of its challenge. Weak challenges are filtered out before presenting to the user.
4. **Logging.** For phase Step 7 invocations, the summary lives inside the phase output. For standalone invocations, log under Section 8 (Decision log) as a Strategic entry with type `Red team`.
5. **Working language.** Detect the user's working language from their last message. Translate the question sets and the summary block into that language. Keep the structure and tone faithful.
6. **Routing.** End with the routing line: proceed to the next step, iterate within the current step, trigger a mini-gate loop-back (use `/innovate-loopback`), or escalate to a kill or pivot decision (use `/innovate-phase 5`).

Respond in the language the user is writing in.
