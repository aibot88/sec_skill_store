---
name: triangulate
description: "Use BEFORE shipping high-stakes output, considering an architectural alternative, working with compliance/legal/safety-critical content, or stuck in a debug loop >2 cycles — fork the question to an independent source of truth (different model, fresh subagent, docs) before trusting your first answer. The meta-decision skill that fires existing review skills (second-opinion, adversarial-reviewer, dispatching-parallel-agents) at the right moments. Anchoring on first instinct is a known LLM failure mode; the cost of a 30-second outside review is far lower than the cost of shipping the wrong pattern."
author: dan-zimon
license: MIT
version: 1.0.0
---

# Triangulate

> Verify a claim by checking 2+ independent sources, before committing to your first answer.

## Why this exists

LLMs anchor on first instinct. When you produce output AND evaluate it, your evaluation runs on the same weights that produced it — same blind spots, same biases, same shortcuts. **Self-review under those conditions is rubber-stamp review.**

The mature move is to **fork the question** at specific trigger points: route it to a different model (different weights), a fresh subagent (different context), or external docs (different epistemology) BEFORE committing.

This skill is the discipline to know **when to fork** and **what counts as an independent source.**

## Trigger points — fire AUTOMATICALLY when ANY hold

### 1. Compliance, legal, regulatory, or safety-critical copy

SEC/FINRA disclosures, OBA-walled bios, privacy policies, terms of service, medical/financial advice, liability-relevant language, public bios that will be cross-checked against authoritative records (BrokerCheck, court records, Form ADV).

**Why:** asymmetric cost. One bad sentence = regulator screenshot, reviewer rejection, lawsuit, BrokerCheck-falsifiable claim. Self-review here is malpractice.

**Action:** invoke `second-opinion` (Codex + Gemini cross-model review) OR spawn a fresh-context `code-reviewer` subagent with the SPECIFIC compliance constraints listed. NEVER skip.

### 2. Architectural decision with a viable alternative pattern

"Should I use SSE streaming or polling?" / "Class component or hook?" / "Fixed-duration cinematic or real progress events?" / "Server-rendered or client-rendered?" Whenever there's a genuinely real alternative, that alternative's existence IS the trigger.

**Why:** if the alternative exists, your first instinct may be the inferior instinct. The 12-seconds-of-animation-theater vs SSE-streaming-real-progress class of mistake.

**Action:** explicitly surface to the user: "I'm leaning toward A. Viable alternative B exists. Want me to spawn a planning agent / Codex session with the same problem statement and compare?" Don't ship the first design just because it's first.

### 3. Image / video / creative prompt engineering

Grok Imagine prompts, nano-banana prompts, hero images, brand assets, video generation. Anywhere prompt-engineering = search in latent space.

**Why:** one prompt is one sample. Variety produces better results.

**Action:** spawn 2-3 parallel agents with DIFFERENT prompt strategies (constraint-heavy / evocative / technical). Pick the winner. Cost: a few cents. Savings: hours of iteration.

### 4. Debug loop > 2 cycles on the same problem

Same test failing with marginally different errors after 3+ retries. Same UI bug surviving 3+ attempted fixes. Same deploy failing for unclear reasons.

**Why:** when you're stuck, the bias is to retry with marginal variation. Tunnel vision. Fresh context breaks it. Different weights break shared blind spots.

**Action:** spawn a fresh agent with a CLEAN problem statement (no debug history). Or invoke `second-opinion` to run the same problem through Codex / Gemini. Different inductive biases catch what same-model retries miss.

### 5. Cross-cutting decision affecting multiple stakeholders

API contract changes, schema migrations, brand-pixel decisions, hiring decisions surfaced as architectural choices, anything where multiple owners have legitimate input.

**Why:** consensus illusion. The agent who proposed the change can't see impact across all stakeholders.

**Action:** dispatch perspective-specific subagents (one per stakeholder concern) and synthesize. This is `adversarial-reviewer` for non-code surfaces.

### 6. Verifying async state changes after a triggering action

Deploys, publishes, DNS changes, cache invalidations, webhook propagation, replicated database writes — anywhere you triggered something and want to confirm "did it happen?"

**Why:** async systems have eventual consistency, not synchronous. Polling at T+5 seconds when propagation takes 2 minutes returns stale data, which produces wrong conclusions, which produce wrong actions. **"Sometimes you have to go slow to go fast."**

**Action:** before checking, estimate the system's propagation window. WAIT that window before drawing conclusions. If you must check early, label the result PROVISIONAL.

Reference table — typical propagation windows:

| Operation | First-check | Full-confidence |
|---|---|---|
| Vercel production deploy | 90-120s | 3-5 min |
| Vercel CDN edge invalidation | 60-120s | 2-3 min |
| GitHub deployments API record | 30-60s | 90s |
| npm registry availability | 30-60s | 90s |
| DNS TTL propagation | 60-300s | 5-15 min |
| Supabase RLS / migration | <1s | 5s |
| Database read replica lag | 100ms-1s | 2s |
| Stripe webhook delivery | 1-30s | 60s |
| Email delivery (transactional) | 30s-5min | 15 min |

**The cache-buster trap:** appending `?cb=...` does NOT defeat server-side static-page generation. If `X-Vercel-Cache: HIT` after a cache-buster, the page is being served from a build that hasn't regenerated yet. Wait, don't keep busting.

**Anti-pattern:** polling in a tight loop to "race" propagation. That hits rate limits, produces false-failure conclusions, and burns trust with the user when you say "didn't work" before the system finished.

## What counts as an "outside source"

Listed in increasing distance from your weights:

| Source | When to use | Tradeoff |
|---|---|---|
| **External documentation / source code** | API behavior, library specifics | Authoritative; settles vs. plausibly-hallucinated |
| **Different model (Codex, Gemini, GPT)** | Architectural alternatives, debug loops, prompt variety | **Different inductive biases; orthogonal blind spots.** The strongest fork. |
| **Fresh subagent (same model, no context)** | Compliance copy review, code review on isolated diff | Same weights but fresh context breaks anchoring on conversation |
| **Different agent role / persona** | Adversarial review, multi-perspective synthesis | Persona shift forces different priors |
| **The user** | Genuinely ambiguous design questions | Highest cost (their time), highest signal — reserve for actual ambiguity |

**Principle:** the further from your weights, the more independent the source.

A fresh Claude subagent ≠ a different model. Both have value, but they're not interchangeable. **For genuinely cross-cutting decisions, prefer different-model.** Codex + Gemini are 2 prompts away via `second-opinion`.

## The maturity test

At any decision point, ask:

> **"Would another model — running the same prompt with no context from this conversation — produce a meaningfully different answer here?"**

- **Yes →** fork the question. Use one of the actions above.
- **No →** ship.

This is the gating question. It costs 2 seconds. It catches the class of mistake where shipping the first answer feels productive but produces inferior output.

## How to invoke (concrete actions)

| Trigger | Tool / Pattern |
|---|---|
| Compliance copy review | `Skill: second-opinion` with focus="general", scope="branch diff" |
| Code review before merge | `Skill: adversarial-reviewer` OR `Skill: second-opinion` (Codex+Gemini) |
| Architectural fork | `Agent` tool, `subagent_type: feature-dev:code-architect` with the same problem statement, no context from this conversation |
| Image prompt variety | 2-3 parallel `Agent` calls, each with a different prompt-engineering strategy |
| Debug loop break | Fresh `Agent` call with isolated problem statement, OR `second-opinion` for cross-model debug |
| Cross-cutting decision | `Skill: dispatching-parallel-agents` (one agent per stakeholder concern) |

## Anti-patterns

- **Forking on routine work** — CSS edits, copy tweaks, dep bumps, single-line fixes. Reserved for trigger points above.
- **Rubber-stamping outside review** — if a different model disagrees with your approach, that disagreement is load-bearing input. Investigate, don't dismiss.
- **Menu-padding** — don't surface "want me to check with X?" as filler. Only when there's genuine value at stake.
- **Outsourcing the decision** — outside review is INPUT to your judgment, not a replacement. You synthesize.
- **Forking after the user said ship** — outside review BEFORE the ship decision; once shipping, ship.
- **Over-forking on green-light architecture** — if you're in a happy path with no viable alternative, no fork needed.

## Origin — the moment that taught this skill

Real moment, Teranode AI project, 2026-04-29.

Built a 12-second fixed-duration cinematic for the reliability-graph Council run. Medallion pulses on each role for 2.4s in sequence, results show. Looked good. Shipped.

In parallel, a Codex session on the same code arrived at a different answer: replace the fixed cinematic with Server-Sent Events from the actual Council run. Pulse the medallion on the role that's *actually* running.

Codex's pattern was materially better. The fixed-duration cinematic was *animation theater* — the medallion lying about what was happening. SSE made it honest.

The fork-the-question moment I (Claude) missed: at the point of designing the timing model, there was a viable alternative (real progress events). **Trigger #2 fired. I didn't fork.** Codex did the work I should have done myself, and the resulting code was better.

The lesson: **the cost of the 30-second pause to fork the question is much lower than the cost of shipping the inferior pattern.**

Dan Zimon (founder, Teranode AI) named this skill that night. The pattern Teranode ships at the product level — five independent reasoning roles forking advisory questions — is the same pattern this skill ships at the developer level. Same principle, two scales.

## Cross-references

- **`second-opinion`** (trailofbits/skills) — when the trigger is "code-review before merge" → cross-model fork via Codex CLI + Gemini CLI. Triangulate is the meta-skill that fires it.
- **`adversarial-reviewer`** (engineering-team) — when the trigger is "code review with persona shift" → 3 hostile personas. Triangulate fires it on code; it doesn't cover non-code surfaces.
- **`dispatching-parallel-agents`** (superpowers) — when the fork produces 3+ independent agents → this skill governs how to dispatch them.
- **`brainstorming`** (superpowers) — when the trigger is "we don't yet know the design space" → brainstorm-first, then triangulate-on-finalists.

## See also

- [`references/teranode-routing-layer.md`](references/teranode-routing-layer.md) — strategic note on how this principle scales into a learning routing layer at the product level. Teranode AI productizes the pattern: which model excels at which question, learned from every API call.

## License

MIT. Free to use, fork, modify, redistribute. Attribution appreciated but not required.
