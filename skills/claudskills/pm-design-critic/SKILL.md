---
name: pm-design-critic
description: Critically review the user-facing surface of a PRD, design spec, or feature proposal against behavioral and UX principles. Use when a PM has a solution in hand and wants the design layer pressure-tested — defaults, friction placement, choice architecture, information density, AI surface decisions, peak-and-end moments. Distinct from pm-red-team (strategy adversary) and pm-evaluator (rubric scoring); this skill stays at the design layer and asks whether the design works with human cognition or against it. Returns the three load-bearing design holes with specific re-writes.
---

# PM design critic

Runs a behavioral and UX review on the surface of a product — the moments a user actually touches. Most PM reviews stop at "is this the right problem and the right strategy." This skill picks up at the layer below: given the strategy is right, is the design choosing the right defaults, putting friction in the right places, framing the right tradeoffs, and ending the right way?

Adjacent to `pm-red-team` but narrower. Red-team challenges the strategy. This skill challenges the surface. Both can be run on the same artifact; they'll surface different holes.

## When to use

Use this when:
- A PRD or design spec is drafted and the user wants a design-layer pass before circulation
- A new feature is heading to launch and the user wants one last review of the UX surface
- The feature involves an AI-driven interaction and the user wants the AI surface specifically critiqued
- The user has a draft that "doesn't feel right" but can't name why — the issue is often a design-principle violation, not a strategy gap

Don't use this when:
- The problem isn't framed yet — run `pm-decision-coach` or `decision-making/problem-framing.md` first; design critique on a wrong problem is wasted
- The user wants strategy-level adversarial pressure — use `pm-red-team` instead
- The user wants the five-criterion rubric scored — use `pm-evaluator`
- The product is API/backend-only with no user-facing surface — this skill has nothing to grab

## How to apply

### 1. Map the moments first

Before critiquing anything, name the user-facing moments in the design. A moment is a place where the user has to decide, act, or absorb information. Common moments: onboarding, first action, recurring action, error, recovery, end of flow, return-to-flow.

For each moment, write one line: *who is the user, what are they trying to do, what is the system asking of them*. If the doc doesn't make this obvious, that's the first hole — flag it before going further.

### 2. Run the behavioral checklist

Reference `decision-making/behavioral-design.md`. For each moment, ask:

- **Choice architecture:** How many options are presented? More than 5 in a decision moment is a flag.
- **Defaults:** What's the default? Is it the choice that serves the user's stated goal, or the choice that maximizes a system goal?
- **Framing:** Are deviations framed as "spend" or as "violation"? Punitive framing reduces engagement.
- **Friction placement:** Is friction where the user wants it (deliberate commitment) or where the system wants it (data collection)? Mismatch is a hole.
- **Peak and end:** What is the last thing the user sees in this flow? What is the highest emotional moment? Both shape what the user remembers, often more than the average experience.
- **Endowment:** Does the user own the outputs of their actions, or does the system own them on their behalf?
- **Pre-commitment:** Are there willpower-heavy decisions that could be moved earlier in the journey?

### 3. Run the AI-surface checklist (if applicable)

Reference `decision-making/ai-integration.md`. If the design includes AI features, check:

- Does the AI live inside the existing flow as labels, ranges, and suggestions — or is it bolted on as a separate chatbot?
- Is confidence shown when it's low? An AI estimate presented as a fact is a hole.
- Can the user override the AI's output at the point of decision?
- What's the fallback when the model is uncertain or fails? "Block the user" is a hole; "category default with a note" is not.
- Does the user see the model, or only the outcome? Surfacing the model is usually a hole, not a feature.

### 4. Find three load-bearing design holes

Same discipline as `pm-red-team`: quality over quantity. The first pass usually already caught the obvious surface issues (color, copy typo, missing screen). The job here is the three holes that, if surfaced in a design review, would force a re-think of how the feature works.

Useful filters:

- **Which moment, if mis-designed, would silently lose users without a clear failure signal?** Onboarding drop, first-action confusion, and end-of-flow ambiguity are the usual suspects.
- **Where is the design fighting human cognition** (asking for too much attention at the wrong moment, presenting too many options when one would do, framing a loss when a spend would do)?
- **Where is the design taking choice away** that should be left with the user (hidden options, paternalistic blocks, forced consent flows)?
- **Where is the AI surface untrustworthy** (no confidence, no override, no graceful failure)?

### 5. Keep what's strong

Same rule as red-team: design critique is more credible when it names the parts that already work. If a flow has a clean peak-and-end design, say so. If the defaults are well-chosen, name them. Calling out two or three things that are strong makes the three holes land harder.

### 6. Re-write, don't advise

A design critique that ends with "consider revising the onboarding" is useless. For each hole, write:

- **The moment:** which screen / flow step / decision point
- **The miss:** which behavioral principle is being violated, in one sentence
- **The re-write:** the specific design change. *"Replace the modal asking for permissions on first launch with an in-context permission ask at the moment the user tries to use the feature that needs it. Reduces drop because the user has already committed to a goal."*

If the right move is *don't ship this design yet*, say so directly.

## Output structure

```
## TL;DR
[One paragraph honest take. Does the design hold up at the surface, given the strategy is right? Yes / partially / no — and the one moment that most determines the answer.]

## The moments mapped
[List of the key user-facing moments in this design, one line each. If a moment was missing from the spec, flag it here.]

## What the design gets right
[Two or three specific design choices that work. Be concrete — name the moment and the principle it honors.]

## Three load-bearing design holes
For each (max three; quality > quantity):

**[Hole 1 — short title]**
- *The moment:* [which screen, flow step, or decision point]
- *The miss:* [the behavioral principle being violated, in one sentence]
- *Why it matters:* [the consequence — drop-off, lost trust, broken muscle memory, etc.]
- *Re-write:* [the specific design change, written so a designer could execute it without re-asking]

## AI surface check
[Optional — only if the design includes AI. One short paragraph: does the AI sit inside flows, show confidence, allow override, fall back gracefully? Name failures directly.]

## What I'd change before the design review
[The 1–3 concrete actions. Each one must be a design move a designer could pick up. "Move the cohort-selection step before the email collection" beats "rethink onboarding."]

## Verdict
[Ship / revise the design / rethink the surface / kill, with one sentence of reasoning.]
```

## What good looks like

- **Three holes, not fifteen.** Bikeshedding (font, color, microcopy minutiae) dilutes the load-bearing critiques. If a minor copy fix doesn't earn its own bullet on the basis of a real behavioral principle, leave it out.
- **Behavioral principle named for every critique.** "This onboarding is too long" is bikeshedding. "Onboarding asks for three willpower-heavy decisions before the user has done anything successful — violates pre-commitment and burns the endowment effect before it can build" is a critique.
- **Specific re-writes.** A re-write that a designer can execute without re-asking. Not "consider simplifying" — *"collapse the three setup questions to one: goal. Defer pace and source until after the first successful action."*
- **Distinguishes design holes from strategy holes.** If the issue is "wrong target user," route to `pm-red-team` or `decision-making/problem-framing.md`. Don't smuggle a strategy critique into a design critique.
- **Cites the repo.** When naming a principle, point at `decision-making/behavioral-design.md` § [principle] so the reviewer can deepen the read. Same for AI surface critiques and `decision-making/ai-integration.md`.

## Anti-patterns

- **Bikeshedding.** Critiquing color, font, microcopy choices without a behavioral case. Visual polish is real work; it's not what this skill is for. Save it for a design review.
- **Smuggling strategy critique into design critique.** "The target user is wrong" is a `pm-red-team` issue. If the design layer is being asked to fix a strategy hole, name that explicitly and stop the design critique there.
- **Demanding the design serve every principle.** Some principles are in tension (e.g. low friction vs. deliberate commitment). The right output is a posture critique — "this design is positioned for low friction but is asking for high commitment at moment X" — not a demand that all principles be honored everywhere.
- **Refusing to acknowledge strong design.** Most design specs that reach review have at least one or two well-designed moments. Naming them is part of the critique's credibility.
- **Critiquing the AI surface without using the AI checklist.** Vague concerns about AI ("feels gimmicky") aren't critiques. Run the four-rule check (confidence, override, fallback, invisibility) and name which rule the surface violates.
- **Hostile tone for show.** This skill is opinionated about design, not adversarial about the designer. Direct, specific, principle-grounded — not theatrical.

## Chain with pm-red-team

For a high-stakes feature heading to launch, run `pm-design-critic` and `pm-red-team` as a pair. Design critic stress-tests the surface; red-team stress-tests the strategy. Both will find different holes. Run design critic first if the strategy is settled and the design is the riskier surface; run red-team first if the strategy is the riskier surface and the design is downstream of it.

If both skills surface the same hole, it's almost certainly real, and the right move is usually to defer the launch until it's closed.

## How to invoke

Common invocation patterns:

- *"Use pm-design-critic on this PRD before I send it to design review."*
- *"I have a feature spec involving AI. Use pm-design-critic on the AI surface specifically."*
- *"This onboarding feels off but I can't name why. Run pm-design-critic on it."*
- *"Use pm-prd-drafter to draft the PRD, then pm-design-critic on the result."*

If the user invokes this skill on an artifact that has no user-facing surface (a backend service spec, a pure infra change), respond: *"This skill works on user-facing surfaces. The artifact you've shared doesn't have one I can grab. Did you mean `pm-evaluator` for the rubric pass, or `pm-red-team` for strategy critique?"*
