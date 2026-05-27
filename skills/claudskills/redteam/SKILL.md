---
name: redteam
description: Spawn a one-shot red-team subagent to challenge a milestone result. Calibrated to return "nothing substantive" when the work is sound — does not invent issues to seem thorough. Use at goal-locked, major-result, or pre-write-up milestones, or whenever you want a deliberate adversarial check on something specific.
level: below
---

# Redteam

A one-shot subagent that challenges work at a milestone. The main agent decides when to spawn it; the subagent reads the relevant artifacts and returns either "nothing substantive to challenge" or a list of concrete findings.

## When to spawn

Run a redteam at **milestones**, not continuously:

- **Goal locked.** Right after `init_research(goal)` — is the goal well-posed, are there obvious framings being missed?
- **Major established result.** A claim has been verified and is about to anchor downstream work. Worth one challenge before it becomes load-bearing.
- **Before write-up.** The conclusion is drafted and you're about to present it. Last pass before it leaves your hands.
- **When the user asks.** "Can you push back on this?" → spawn a redteam.

Do *not* run redteam continuously. An agent told to find mistakes will find phantom ones if asked too often. Milestone cadence preserves signal.

## How to spawn

```
Task(
  subagent_type="redteam",
  prompt=(
    "Milestone: <what was just reached>\n"
    "Artifact to challenge: <file path or claim ID or excerpt>\n"
    "Optional axis to focus on: <e.g. 'unstated assumptions', 'alternative methods'>\n"
    "\n"
    "Return your verdict and any findings per the output format in your "
    "system prompt. Empty findings is the right answer if the work is sound."
  )
)
```

The subagent reads the artifact, decides whether there's anything substantive to challenge, and returns a structured report. It does not write to research state or modify any files.

## Reading the result

The subagent returns one of four verdicts:

- **"nothing substantive to challenge"** — the work is sound. Move on. Logging this in `workspace/research/redteam.log` is optional (one line if you want a record).
- **"minor presentational notes only"** — clarity could improve but the conclusion holds. Apply if it helps the next reader.
- **"issues worth addressing"** — concrete findings that should be resolved before the work is final.
- **"concerns that block the conclusion"** — the result is in question. Re-open the analysis.

If the verdict is "issues worth addressing" or higher, treat each `must-address` finding as a new claim to investigate — verify, refute, or reframe.

## Manual invocation

`/redteam` runs a single redteam pass against whatever the main agent thinks is the current milestone. The user can also pass an explicit target:

```
/redteam workspace/research/established.md C3
/redteam "the conclusion that the period scales as L/g"
```

## Hard rules

- **Milestone-only by default.** Don't spawn redteam mid-derivation.
- **Trust empty verdicts.** If the subagent says "nothing substantive," don't ask again with a leading prompt to extract findings.
- **One axis per spawn.** If you want to challenge both methodology and assumptions, spawn twice with different focus axes — keeps each pass calibrated.
- **The subagent is read-only.** Do not ask it to write to research state or files.
