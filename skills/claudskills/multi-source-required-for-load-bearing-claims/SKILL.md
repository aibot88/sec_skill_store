---
name: multi-source-required-for-load-bearing-claims
description: "Architecture decisions, security claims, and performance claims must cite at least two independent sources or escalate the gap to the user. A load-bearing claim is one that, if wrong, causes downstream cascade — choosing the wrong session-store changes every middleware that touches the session; picking bcrypt vs argon2 sets a security baseline for every credential write; assuming an O(log n) lookup when the implementation is O(n) breaks every consumer at scale. Silent single-source picks on these claims are the canonical rationalization-trap shape per K2 §3.3 and link to the rationalization-trap-check skill in the knowledge-hygiene plugin (commit b28aa0f). Cites K2 §3.3 (conflict surfacing) and reuses the multi-source-research pipeline. Use when: writing an architectural decision into a spec or design doc, asserting a security primitive selection in code or review, asserting a performance characteristic that downstream consumers will depend on, reviewing a PR whose description or commits introduce a load-bearing assertion, dispatching a subagent that will produce a design doc or ADR. Skip when: the claim is non-load-bearing (typo fix, comment update, docstring rewording), a single authoritative source is genuinely sufficient and explicitly documented as such (e.g., a function's signature read from its own source file via lci_get_context — the source is authoritative because it is the artifact itself), the claim is exploratory and explicitly labeled as a hypothesis rather than a decision."
---

# Multi-Source Required For Load-Bearing Claims

Project-level value-layer rule. Load-bearing claims drive downstream decisions that are expensive to reverse. The discipline of citing at least two independent sources before committing to such a claim is the cheapest available defense against the rationalization-trap failure mode (K2 §3.3, ConflictQA `2604.11209` §4): silently rationalizing one source's claim into a spec because no second source was consulted to disagree.

## Provenance

- **K2 design doc:** `docs/research/K2-knowledge-hygiene-from-papers.md` §3.3 (Rationalization-trap as the sole value-layer rule in the knowledge-hygiene epic — silent single-source picks are the canonical shape this trap takes for load-bearing claims)
- **Source paper:** ConflictQA `(2604.11209)` §4 — quantifies how often LLMs silently rationalize when only one source is presented vs how rarely they rationalize when two contradicting sources are presented in parallel.
- **Reused pipeline:** `plugins/knowledge-hygiene/skills/multi-source-research/SKILL.md` (commit `b28aa0f`) — gather → conflict-detect → synthesize-with-provenance pipeline. This rule is the dev-standards-side pre-commit guidance that triggers that pipeline; the pipeline itself lives in `knowledge-hygiene`.
- **Reused agent:** `plugins/knowledge-hygiene/agents/conflict-detector.md` (same commit) — when two sources disagree, this agent classifies the conflict and recommends a resolution.
- **Reused contract:** brainstorming `<PROVENANCE-CONTRACT>` (commit `ebd136a`) — every cited source carries a provenance value from the 5-form vocabulary (`file:path:line` | `memory:id` | `git:sha` | `web:url` | literal `"guess"`).

## The Value-Layer Rule

> **A load-bearing claim MUST be supported by at least two independent sources, OR the gap MUST be surfaced visibly to the user with an explicit "single-source — please confirm" note. Silent single-source picks on load-bearing claims are forbidden.**

This is the third `must` in the dev-standards plugin (alongside `verification-before-completion` and `no-compression-on-skill-frontmatter`). The `must` is on **visibility**, not on **resolution** — the rule does not require that all conflicts be resolved before commit, only that the gap be surfaced visibly. The user can override.

## What "Load-Bearing" Means Concretely

A claim is load-bearing when, if it turns out to be wrong, the cost of correction extends beyond a local edit. Three named categories cover most cases:

### Category 1 — Architecture decisions

A claim is load-bearing if it constrains the shape of the system: which storage backend, which session model, which serialization format, which message-queue topology, which authn/authz primitive, which inter-service protocol, which build/deploy substrate. Concrete examples:

- "We use Postgres because we need strong consistency on writes." (Single-source: a blog post claiming Postgres beats MySQL on consistency is not enough. Need: official docs + a benchmark or in-repo precedent.)
- "We chose JWT for session because it scales horizontally without server state." (Single-source: a Stack Overflow answer is not enough. Need: official spec + a security-reviewed pattern.)
- "We use Tailwind because the team prefers utility-first CSS." (Single-source: a team preference is not enough as a load-bearing assertion. The claim itself is fine; the load-bearing form would be "Tailwind scales to N components without selector-collision issues" which needs evidence beyond preference.)

### Category 2 — Security claims

A claim is load-bearing if it sets the security baseline for a class of operations: hashing primitive selection, key-derivation function selection, TLS version requirements, CSRF/CORS posture, input-validation rules at trust boundaries, rate-limit thresholds, audit-log requirements. Concrete examples:

- "bcrypt with cost factor 12 is sufficient for our threat model." (Single-source: the bcrypt manpage is not enough. Need: OWASP guidance + a recent benchmark for the deployment hardware.)
- "We rate-limit at 100 req/min because that matches user behavior." (Single-source: a single product-analytics query is not enough. Need: analytics + a security review of the bypass surface.)
- "API keys in headers are sufficient — we don't need OAuth here." (Single-source: a blog post is not enough. Need: official protocol docs + a documented threat model that explicitly excludes the OAuth-relevant attacks.)

### Category 3 — Performance claims

A claim is load-bearing if downstream consumers will plan capacity, scaling, or UX timing around it: algorithmic complexity assertions, latency targets, throughput baselines, memory budgets, cache hit-rate assumptions. Concrete examples:

- "This lookup is O(log n) so it scales fine to 10M entries." (Single-source: reading the function signature is not enough — the implementation behind the signature is the load-bearing fact. Need: signature + implementation read + a benchmark at expected scale.)
- "Redis cache hit rate will be ≥90% so the DB load stays bounded." (Single-source: a vendor blog is not enough. Need: vendor data + an in-repo or representative-workload measurement.)
- "Page load under 2s on 3G — verified by our staging measurement." (Single-source: one staging run is not enough — need at least two independent measurements at different times or different network profiles to rule out a transient.)

## What "Independent Sources" Means

Two sources are **independent** if they do not derive from the same upstream — copying the same Stack Overflow answer twice is one source, not two. Concrete independence tests:

| Source A | Source B | Independent? |
|---|---|---|
| Official docs | A blog post citing those same docs | **No** — the blog post derives from the docs; same upstream. |
| Official docs | An in-repo precedent that uses the feature | **Yes** — the in-repo use is independent evidence that the docs match reality. |
| Two blog posts citing the same paper | — | **No** — both derive from the paper; cite the paper itself plus one independent corroboration. |
| OWASP guidance | A recent benchmark on representative hardware | **Yes** — guidance is normative, benchmark is empirical; different evidence types. |
| `lci_get_context` on the function signature | `Read` of the function body | **Yes if the body shows the actual behavior** — signature is contract, body is implementation; different evidence types corroborating each other. |
| Two LLM-generated summaries of the same source | — | **No** — same upstream, different paraphrases. |
| Memory entry from prior task | Git log of the commit that created the memory entry | **Marginal** — they corroborate the *existence* of a prior decision but not the *correctness* of that decision. Treat as one source for correctness claims. |

When in doubt, ask: "if Source A turned out to be wrong, would Source B also be wrong by the same mistake?" If yes, they are not independent.

## The Escape Valve — When One Source Is Enough

The rule has an explicit escape valve, consistent with the project's soft-guidance posture for everything except the visibility `must`. One source is enough when **both** of the following hold:

1. **The source is the artifact itself.** A function's signature read from its own source file is authoritative for "what is this function's signature" because the source file *is* the function's signature. There is no second source possible. Same for: file contents read directly, environment variable values read at runtime, config values read from the canonical config file.
2. **The claim is scoped to the artifact.** The claim "function `foo` returns `Result<T, E>`" is single-source-ok if read from the function's own definition. The claim "function `foo` is performant under load" is *not* single-source-ok even if the function source is read, because performance is not contained in the signature.

When the escape valve applies, the single source still carries provenance: the citation in the spec / decision / review uses the brainstorming `<PROVENANCE-CONTRACT>` `file:path:line` form to make the artifact-source explicit.

## How To Surface The Gap When You Don't Have Two Sources

When a load-bearing claim must ship and only one source is available, the rule requires **visible gap surfacing**, not silent shipping. The minimum-viable surface:

```markdown
**Single-source claim — please confirm.** The assertion "<claim text>" is supported only by <source A: provenance>. I was unable to find an independent corroborating source within this session's research budget. Three escalation options:

1. **Confirm-as-is** — accept the single-source claim with the visible note kept in the spec / commit / review. The single-source flag stays in the document for future readers.
2. **Defer the claim** — strip the claim from this commit; open a follow-up dart-task to research the second source.
3. **Reframe as hypothesis** — keep the claim but label it explicitly as `hypothesis (single-source)` so downstream consumers know it is not a settled decision.
```

The agent / reviewer / writer picks one of the three and proceeds. The point is the explicit choice; the silent skip is what the rule forbids.

## Interaction With The Knowledge-Hygiene Pipeline

This rule is the **dev-standards trigger** for the multi-source-research pipeline that lives in the `knowledge-hygiene` plugin. The handoff:

1. Writer / reviewer identifies a load-bearing claim per the three categories above.
2. Writer invokes `knowledge-hygiene:multi-source-research` skill with the claim and the load-bearing-ness signal.
3. The skill's pipeline (gather → conflict-detect → synthesize) returns the corroborated claim with provenance per source, OR an "insufficient sources" verdict triggering the gap-surface escape valve above.
4. If the pipeline detects a conflict between two sources, `knowledge-hygiene:conflict-detector` agent classifies the conflict (one of 7 named types) and recommends one of 4 resolutions (`prefer-recent` / `prefer-authoritative` / `escalate-to-user` / `not-applicable`).
5. The recommendation is surfaced visibly in the spec / commit / review per the K2 §3.3 rationalization-trap rule — not silently absorbed.

This rule is the producer-side contract; the knowledge-hygiene plugin is the consumer-side mechanism. Together they implement the K2 multi-source-with-conflict-surfacing pattern at the project level.

## What This Rule Does NOT Cover

- **Non-load-bearing claims.** Typo fixes, comment rewording, docstring updates, log-message edits, formatting changes — these do not need multi-source corroboration. The rule scopes only to claims with downstream cascade.
- **Exploratory hypotheses.** A brainstorm bullet labeled `provenance: guess` per the `<PROVENANCE-CONTRACT>` is already self-flagged as unverified; no multi-source requirement applies until the bullet is promoted to a decision.
- **Implementation details below the architecture line.** "I named this variable `foo` because the surrounding code uses `foo`-prefix" is a local convention, not a load-bearing claim.
- **Hard merge gates.** The rule is enforced by reviewer attention and skill-using subagent discipline, not by a pre-commit hook or merge-blocker. Visible gap surfacing is the gate; the resolution is human-overridable.

## Self-Application

This SKILL.md's own load-bearing claims:

- "Silent single-source picks are the canonical rationalization-trap shape for load-bearing claims" — cited from K2 §3.3 + ConflictQA `2604.11209` §4 (two sources, paper + synthesis doc, independent).
- "The multi-source-research pipeline lives in the knowledge-hygiene plugin" — cited from `plugins/knowledge-hygiene/skills/multi-source-research/SKILL.md` + commit `b28aa0f` (in-repo + git history, independent corroborations).
- "bcrypt example needs OWASP + benchmark" — cited as illustrative, not asserted as a load-bearing decision in this skill itself; the example is meta-evidence for the rule, not a claim the rule makes about bcrypt.

The rule applies its own discipline: every load-bearing claim above is double-cited; the illustrative examples carry their evidence-type label so the reader can distinguish "this is the rule" from "this is what the rule looks like applied."

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| "I read this in one place but I'm pretty sure it's right" | The single source might be right, but the rationalization-trap failure mode is exactly this — the certainty comes from the single source, not from corroboration. Surface the gap. |
| Citing two sources that derive from the same upstream | Not independent; same failure mode if the upstream is wrong. See independence test table above. |
| Treating the rule as a hard merge block | The `must` is on visibility, not on resolution. The user can override; the rule just requires the override be explicit. |
| Auto-running the pipeline on every claim, including non-load-bearing | Bloats research budget without benefit. Apply the load-bearing-ness signal first; only invoke the pipeline when it earns its cost. |
| Using "I asked another LLM and it agreed" as the second source | Same upstream training data is not an independent corroboration. Cite an actual second source (paper, doc, in-repo precedent, measurement). |

## Relationship To Other Skills

- **`knowledge-hygiene:multi-source-research/SKILL.md`** — the consumer pipeline that this rule triggers. Producer-side rule (here) → consumer-side mechanism (there).
- **`knowledge-hygiene:rationalization-trap-check/SKILL.md`** — post-hoc audit for the failure mode this rule prevents. Together they form prevention (this skill) + detection (rationalization-trap-check).
- **`knowledge-hygiene:conflict-detector` agent** — invoked inside the pipeline when two sources disagree.
- **`brainstorming:brainstorming` `<PROVENANCE-CONTRACT>`** — provides the 5-form provenance vocabulary every cited source uses. This rule reuses, does not redefine.
- **`no-compression-on-skill-frontmatter`** (sibling skill) — protects skill-metadata integrity; this rule protects load-bearing-claim integrity. Both are value-layer `must` rules in this plugin.
- **`memories-require-timestamp-and-source`** (sibling skill) — adds temporal grounding to the memory layer so the conflict-detector can prefer recent over stale when two memories disagree. Complementary discipline.
- **`verification-before-completion`** — the other long-standing `must` in this plugin. That rule covers evidence-before-completion-claims; this rule covers source-multiplicity-before-load-bearing-claims. Distinct scopes, same family.
