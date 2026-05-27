---
name: pm-red-team
description: Adversarially re-review a PM artifact, recommendation, or AI-generated critique that already exists. Use as a second pass after another skill (pm-evaluator, pm-prd-drafter, pm-decision-coach, pm-value-hypothesis-tester) has produced output, or on any external AI output the user wants pressure-tested before deferring to it. Plays the role of a hostile exec, skeptical board member, or competing PM — looking for what the first pass missed, what bias it brought, and what would not survive a real review. Returns the three load-bearing holes, what's already strong enough to keep, and the specific re-writes that would close the gaps.
---

# PM red team

Runs an adversarial second pass on something that has already been written or critiqued. The goal is not to be contrarian — it's to surface the parts of the analysis that wouldn't survive a hostile reviewer (an exec, a board member, a sharp peer PM, a competitor strategist). Adapted from the chief-of-staff pattern of critically evaluating AI output rather than deferring to it.

The skill is opinionated. It will disagree with the prior pass when it has reason to. It will keep what's strong. It will not generate noise just to look productive.

## When to use

Use this when:
- A primary PM skill (`pm-evaluator`, `pm-prd-drafter`, `pm-decision-coach`, `pm-value-hypothesis-tester`, `pm-metrics-critic`, `pm-launch-reviewer`) has produced an evaluation or draft, and the user wants it pressure-tested before sending up the chain
- The user has pasted an **external AI output** (ChatGPT, Gemini, another Claude session) and wants it challenged rather than trusted
- The user has written their own draft and wants an adversarial read before circulating
- A recommendation feels right but the user wants to make sure they're not just being told what they wanted to hear

Don't use this when:
- No prior analysis exists yet — run the primary skill first, then chain to this
- The user wants the artifact written from scratch — use `pm-prd-drafter` or `pm-decision-coach`
- The user wants emotional support — they want adversarial pushback, not validation, but make sure that's actually what they want
- The artifact is genuinely strong and the prior pass already caught the issues. In that case, say so and don't manufacture critiques

## How to apply

### 1. Read the artifact and the prior analysis as separate inputs

Treat them as two distinct objects:
- **The original artifact** (the memo, PRD, recommendation, dashboard, metrics list, claim).
- **The prior analysis** (what the previous skill, the user, or an external AI said about it).

Most red-team failures come from skipping step one and just re-critiquing the prior analysis without going back to the source. Read both.

### 2. Run a different lens than the first pass

The first pass usually applied one of the repo's primary lenses (rubric scoring, problem framing, value-hypothesis stress test). The second pass should pick a *different* lens, not run the same one harder.

Useful lenses to switch to, depending on what the first pass used:

- **If the first pass applied the five-criterion rubric** (`rubrics/pm-evaluation-rubric.md`): run the **stakeholder lens** — whose perspective is missing? Procurement, support, sales reps, finance, regulatory, downstream teams. (See `cross-functional/stakeholder-alignment.md` § "Bundle thinking.")
- **If the first pass focused on user problem and value**: run the **business viability lens** — unit economics, GTM motion, distribution, sales-rep economics, pricing power. (See `decision-making/value-hypothesis.md` and `decision-making/competitive-moat.md`.)
- **If the first pass focused on strategy and metrics**: run the **execution lens** — what does the team's history say about its ability to deliver? Engineering morale, dependencies, "this time is different" credibility. (See `cross-functional/engineering-partnership.md` and `cross-functional/failure-management.md`.)
- **If the first pass focused on the proposal**: run the **counter-recommendation lens** — what's the strongest version of the option that *wasn't* picked? Steel-man it before red-teaming it.
- **If the first pass focused on metrics**: run the **gaming lens** — how would a team optimize this metric while making the underlying outcome worse? (See `decision-making/metrics.md` § "When the metrics are lying.")

### 3. Find the three load-bearing holes, not fifteen small ones

Volume is not value. The first pass already caught the obvious issues. The job here is to find the **two or three most consequential gaps** — the ones that, if exposed in an exec review, would derail the recommendation.

Useful filters:

- **What's missing that would matter more than what's already covered?**
- **What assumption is being treated as evidence?**
- **What stakeholder would disagree, and what would they say?**
- **What's the falsifying answer the prior pass didn't ask for?**
- **What would survive a 1.5× more competent competitor / hostile reviewer / skeptical exec?**

### 4. Keep what's strong

Adversarial review is not blanket disagreement. If the first pass got the diagnosis right, say so. If a section is already tight, don't manufacture a critique. Calling out three things that are *good enough to keep* makes the three things that are *not* land harder.

### 5. Recommend specific re-writes

A red-team review that ends with "consider revising" is useless. Specify:

- **Section / claim:** which line of the artifact
- **The hole:** what's wrong or weak
- **The re-write:** the actual replacement line, written in the user's voice as best as you can match it

If the right move is *don't ship this*, say so directly: *"The load-bearing assumption is a guess; the recommendation is not yet ready. Defer until [specific test] runs."*

### 6. Push back on the prior pass when warranted

If the prior analysis is itself wrong — too lenient, off-target, applying the wrong framework — name it. *"The prior pass scored this 4/5 on Criterion 3, but the bundle effect on the primary product is unaddressed; on the rubric as written, this should be at most 2/5."*

This is the chief-of-staff pattern made explicit: critically evaluate the prior AI output, do not defer to it.

## Output structure

```
## TL;DR
[One paragraph honest take. Does the artifact, after the prior critique, hold up under a hostile reviewer? Yes / partially / no — and the one thing that most determines the answer.]

## What the prior pass got right
[Two or three specific things that are already strong enough to keep. Be concrete — quote or cite.]

## What the prior pass missed
For each (max three; quality > quantity):

**[Hole 1 — short title]**
- *Where:* [the specific section, claim, or metric in the original artifact]
- *The miss:* [what's wrong or absent, in one or two sentences]
- *Why it matters:* [the consequence — what an exec / board member / competitor would do with it]
- *Re-write:* [the specific replacement line or the specific test that would close the gap]

## Where the prior pass itself went off
[Optional. If the prior critique is itself weak — wrong framework, lenient grading, missed lens — name it. One or two paragraphs.]

## What I'd do before sending this up the chain
[The 1-3 concrete actions. Each one must be doable. "Run the bundle-effect analysis on the primary product" beats "consider bundle effects." Pre-commit a kill criterion. Re-run the value-hypothesis test on a tighter segment. Etc.]

## Verdict
[Ship / revise / defer / kill, with one sentence of reasoning. Take a position.]
```

## What good looks like

- **Three holes, not fifteen.** Volume is the failure mode. A red-team review that lists every minor issue dilutes the load-bearing ones.
- **Specific re-writes, not advice.** "Revise the success metrics" is useless. "Replace 'increase engagement' with 'free-to-paid conversion at premium tier ≥ 8% in the strategic segment by Q3'" is the bar.
- **Different lens than the first pass.** If the first pass scored a rubric, the red-team applies a stakeholder or viability or execution lens. Same lens harder = same blind spots.
- **Willing to disagree with the prior critique.** This is the point of the skill. If the previous reviewer was too kind, say so. The user will get more value from honest disagreement than polite consensus.
- **Acknowledges what's strong.** Not every section is broken. Calling out the strong parts makes the critique credible.
- **Cites the repo.** When pointing at a missed lens, name the file (`cross-functional/stakeholder-alignment.md`, `decision-making/value-hypothesis.md`, etc.) so the user can deepen the read.

## Anti-patterns

- **Running the same lens as the first pass, harder.** This produces minor adjustments to a critique that already exists. Use a different lens.
- **Manufacturing critiques to look thorough.** If the artifact is genuinely strong, say *"the prior pass caught the real issues; ship it."* That's a more credible result than three confected concerns.
- **Pure contrarianism.** Disagreeing for its own sake. The point is to find what's actually missing, not to be the skeptic in the room.
- **"Consider X" advice without re-writes.** If the user has to translate the critique into a concrete change, the skill didn't finish its job.
- **Deferring to the prior AI output.** This is the failure the skill is built to prevent. The first pass is input data, not a verdict.
- **Validating because the user clearly wants to ship.** If the recommendation isn't ready, the right output is "defer," not "ship with caveats." Caveats get stripped from decks; verdicts don't.
- **Hostile-for-show prose.** The skill is adversarial in *substance*, not in *tone*. Direct, specific, opinionated — not theatrical.

## How to invoke

Common invocation patterns:

- *"Use pm-evaluator on this strategy memo, then pm-red-team on the result."*
- *"This is a critique another AI gave me of my PRD. Use pm-red-team to challenge it."*
- *"Run pm-red-team on this draft before I send it up."*
- *"I'm about to commit to option B. Use pm-red-team on the recommendation."*

If the user invokes this skill without first having a primary analysis in scope, ask: *"What's the prior analysis (the artifact and any existing critique)? I need both to run a useful second pass."*
