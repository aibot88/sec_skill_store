---
name: epistemic-grounding
description: "Use when authoring any artifact that makes claims — skill content, documentation, audit findings, architecture proposals, code review comments. Covers the discipline of grounding every claim to a verifiable source, distinguishing verified-by-evidence from inferred-from-context, using normative vocabulary precisely (RFC 2119 MUST/SHOULD/MAY), and structuring arguments so the warrant from data to claim is visible to a reader. Do NOT use for verification protocol mechanics in this repo (use the verification-protocol rule file), for output-completeness enforcement (use methodology), or for self-scoring on a 1-5 scale (use self-evaluation)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"foundations\",\"domain\":\"foundations/epistemics\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-15\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-15\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"epistemic grounding\\\\\\\",\\\\\\\"claim grounding\\\\\\\",\\\\\\\"source citation\\\\\\\",\\\\\\\"RFC 2119 modality\\\\\\\",\\\\\\\"Toulmin argument\\\\\\\",\\\\\\\"evidence-based assertion\\\\\\\",\\\\\\\"hallucination prevention\\\\\\\",\\\\\\\"normative vocabulary\\\\\\\",\\\\\\\"warrant\\\\\\\",\\\\\\\"epistemic hedge\\\\\\\"]\",\"triggers\":\"[\\\\\\\"ground this claim\\\\\\\",\\\\\\\"cite a source\\\\\\\",\\\\\\\"MUST vs SHOULD\\\\\\\",\\\\\\\"is this verified\\\\\\\",\\\\\\\"how do you know that\\\\\\\"]\",\"examples\":\"[\\\\\\\"before stating that this library supports X, confirm against the actual docs\\\\\\\",\\\\\\\"rewrite this finding so each assertion either cites a file or is marked as inference\\\\\\\",\\\\\\\"should this be a MUST or a SHOULD? what's the strength of the claim?\\\\\\\",\\\\\\\"the agent reported 'fix works' but no test was run — flag the gap in grounding\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"verify every step of an audit task with concrete evidence (use methodology)\\\\\\\",\\\\\\\"decide which lint rule to add for a specific kind of drift (use skill-infrastructure)\\\\\\\",\\\\\\\"evaluate a finished SKILL.md against the comprehension grader (use evaluation)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"methodology\\\\\\\",\\\\\\\"semantics\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"methodology\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"methodology enforces output-level completeness and step-level evidence receipts; epistemic-grounding is the upstream discipline that decides what counts as evidence in the first place.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"semantics\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"semantics owns the rules for naming and meaning-making; epistemic-grounding owns the rules for grounding a claim to a verifiable source.\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"methodology\\\\\\\",\\\\\\\"evaluation\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"Epistemic grounding is to claims what double-entry bookkeeping is to financial transactions — every assertion has a corresponding source on the other side of the ledger, and any entry without its pair is a red flag in the audit.\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"Epistemic grounding is the discipline of binding every assertion to a verifiable source, marking the modality (strength) of the claim, and making the warrant (the inference from source to claim) explicit. It is the practice that turns a generated statement into a defended statement.\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/epistemic-grounding/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/epistemic-grounding/SKILL.md
---

# Epistemic Grounding

## Coverage

The discipline of grounding every claim to a verifiable source, marking the modality (RFC 2119 MUST/SHOULD/MAY) of the claim, and making the warrant from source to claim explicit. Covers the six-primitive Toulmin argument structure (claim/data/warrant/backing/qualifier/rebuttal), the RFC 2119 normative vocabulary, the distinction between verified/inferred/hallucinated, how to hedge honestly without softening, and the failure modes (cargo-cult citation, stale grounding, vibe-based assertion). Applies to any artifact that makes claims: SKILL.md content, code review comments, audit findings, documentation, architecture proposals, agent output.

## Philosophy

Confidence is not evidence. An LLM trained to be helpful produces fluent, confident text whether or not the underlying claim is true — RLHF rewards plausibility, not verification. The result is that ungrounded text is indistinguishable from grounded text by surface signals alone: tone, structure, and vocabulary look identical.

The countermeasure is not to ask the model to "be more careful" (it can't see its own confidence). It is to require structural signals that make grounding state visible: every claim has a source-warrant-qualifier triple in the text, or it carries an explicit hedge ("not verified", "as of 2026-05-15", "inferred from context"). A reader scanning the text can then tell at a glance which claims are grounded and which are not.

This discipline serves three downstream uses: (1) audit and review become tractable because the reviewer knows what to verify; (2) drift detection becomes possible because grounded claims expose their dependencies; (3) downstream agents reading the artifact can decide which claims to trust and which to re-verify.

## The Six-Primitive Argument

Every grounded claim has six primitives, derived from Toulmin's argument structure (1958). Most agent output surfaces only the Claim and silently elides the rest.

| Primitive | What it answers | Example |
|---|---|---|
| **Claim** | What is being asserted? | "HTTP DELETE is idempotent." |
| **Data** | What source supports the claim? | "RFC 9110 § 9.3.5" |
| **Warrant** | What rule connects data to claim? | "RFC 9110 normatively defines HTTP method semantics; § 9.3.5 specifies DELETE's idempotency." |
| **Backing** | What gives the warrant authority? | "IETF standards body; the RFC has been ratified and is the canonical HTTP/1.1 reference." |
| **Qualifier** | How strong is the claim? | "MUST" (per RFC 2119) — DELETE is by-definition idempotent. |
| **Rebuttal** | Under what conditions does the claim fail? | "Server-side state changes that cause subsequent DELETEs to return different status codes do not violate idempotency in the spec sense — idempotency is about the server's resource state, not the response code." |

A grounded version of "HTTP DELETE is idempotent" might read in full: *"DELETE is idempotent (RFC 9110 § 9.3.5, MUST). Repeated calls produce the same resource state; response codes may differ (404 after the first 204), which does not violate spec-level idempotency."* That sentence has all six primitives. The ungrounded version — "DELETE is idempotent" — has only the claim.

In a SKILL.md, you don't enumerate all six explicitly every sentence. You inline them via citation form, qualifier word, and parenthetical rebuttal. The discipline is to write each claim such that the six primitives can be *reconstructed* by a reader, not necessarily that they are all surface-visible.

## RFC 2119 Modality

The normative vocabulary from RFC 2119 gives Qualifiers a shared, machine-readable meaning. Use these words *only* in their RFC 2119 sense; in non-normative writing, use weaker words.

| Word | Meaning |
|---|---|
| **MUST** / **REQUIRED** / **SHALL** | Absolute requirement. The claim is binding; violation breaks the contract. |
| **MUST NOT** / **SHALL NOT** | Absolute prohibition. |
| **SHOULD** / **RECOMMENDED** | Strong recommendation. Violation requires understanding and justifying the deviation. |
| **SHOULD NOT** / **NOT RECOMMENDED** | Strong recommendation against. |
| **MAY** / **OPTIONAL** | Truly optional. Either choice is conformant. |

A skill that says "the handler MUST verify HMAC" makes a different commitment than "the handler should verify HMAC" (lowercase, weak). The capitalized RFC 2119 form has contract weight; the lowercase form is advisory English. Mixing them is a grounding failure.

In SKILL.md authoring, use RFC 2119 vocabulary *only* when the claim is genuinely normative (a protocol requirement, a security invariant, a financial correctness rule). For preferences and patterns, use weaker prose: "prefer", "by default", "in this repo we use".

## Verified vs Inferred vs Asserted

Every claim falls into one of three states. Epistemic grounding requires labeling the state explicitly when it isn't obvious from context.

| State | Definition | Required marker |
|---|---|---|
| **Verified** | The claim was confirmed by a tool call (Read, Grep, curl, test run) in the same writing session or has an attached evidence receipt. | Cite the verification ("ran `npm test`, all 47 passed") or attach the source path with a line range. |
| **Inferred** | The claim is a reasonable conclusion from cited evidence, but the conclusion itself wasn't directly tested. | Mark with "inferred from", "follows from", or a hedge like "likely". |
| **Asserted** | The claim is from the writer's prior knowledge with no in-session verification. | Mark with "as of <date>", "I haven't verified this", or "in my experience". This is the weakest state and should be rare in grounded writing. |

The failure mode is silent state-drift: asserting something as if verified, or inferring something as if asserted. The discipline is to mark the state when it differs from what context implies.

## Failure Modes

| Failure | What it looks like | Why it fails |
|---|---|---|
| **Cargo-cult citation** | A reference is added at the end of a paragraph, but doesn't actually support the specific claims in that paragraph. | The warrant from source to claim is missing; the citation is decorative. |
| **Stale grounding** | A claim cites a source that has since been moved, renamed, or rewritten. | The grounding was once valid but isn't anymore; the reader trusts it without knowing. |
| **Vibe-based assertion** | A claim is stated with no marker, in a context where the reader will assume it's grounded. | Silent state-drift from asserted to verified. |
| **Overstated modality** | "MUST" used for a preference; "MAY" used for a hard requirement. | RFC 2119 vocabulary loses its load-bearing meaning. |
| **Pseudo-hedge** | "Probably", "in most cases", "generally" applied where the writer actually knows the answer. | Soft hedging looks like grounding but obscures the actual state of knowledge. |
| **Citation laundering** | Citing a secondary source (a blog post citing an RFC) without going to the primary. | The chain of warrants is weak; the secondary source may have misread the primary. |
| **Authority projection** | Citing a high-authority source for a claim it doesn't actually make. | The source's authority covers the writer's claim even though the source didn't say it. |

## Verification

After applying this skill, verify:
- [ ] Every claim that would surprise a domain expert has a source attached.
- [ ] RFC 2119 vocabulary is used only in normative claims, not in advisory prose.
- [ ] No paragraph has trailing-citation decoration where the citation doesn't tie to specific claims.
- [ ] Claims that are inference (not from a cited source) are explicitly marked.
- [ ] The strongest claims have the most explicit grounding; the weakest claims have hedges.
- [ ] No "MUST" applies to a preference; no "MAY" applies to a requirement.
- [ ] At least one Rebuttal is acknowledged for the central claim of the artifact.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Enforcing step-level evidence receipts and output completeness | `methodology` | methodology owns the execution discipline; this skill is the upstream grounding discipline that decides what counts as evidence in the first place |
| Naming things precisely (variables, functions, files) | `semantics` | semantics owns naming precision; this skill owns claim grounding |
| Drawing inferences from premises | `reasoning` | reasoning is the cognitive primitive; this skill is the marking discipline for distinguishing inference from observation |
| Verifying that a specific implementation works | `evaluation` or repo-local verification protocol | evaluation owns grader frameworks; this skill is the structural discipline upstream of any verification |
| Designing the rules of a skill audit | `skill-infrastructure` | skill-infrastructure owns lint and census tooling; this skill governs what counts as a grounded claim that lint might check |

## Key Sources

- Toulmin, S. (1958). *The Uses of Argument*. Cambridge University Press. The canonical six-primitive argument structure (claim/data/warrant/backing/qualifier/rebuttal).
- Bradner, S. (1997). [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://datatracker.ietf.org/doc/html/rfc2119). IETF. The standardized MUST/SHOULD/MAY normative vocabulary.
- Leiba, B. (2017). [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://datatracker.ietf.org/doc/html/rfc8174). IETF. Clarifies that only ALL-CAPS forms carry RFC 2119 weight.
- Northeastern University (2025). "AI sycophancy: 58.19% rate across frontier models." The measurement that justifies structural countermeasures over behavioral ones.
- Royal Society Open Science (2025). "LLM summarization bias: overgeneralization in 26-73% of cases." The measurement that justifies explicit source-to-claim warrant tracking.
