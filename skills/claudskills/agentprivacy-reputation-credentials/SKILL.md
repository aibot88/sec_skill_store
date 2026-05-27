---
name: agentprivacy-reputation-credentials
description: >
  Reputation and credential evolution (SBT→VRC) for 0xagentprivacy.
  Activates when discussing soulbound tokens, verifiable credentials,
  credential lifecycle, reputation staking, progressive credential trust, or
  the evolution from static credentials to living relationship records.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Credential system designers, reputation economists, SBT researchers, onchain identity architects, BGIN IKP contributors"
  equation_term: "C (credential verifiability), A(τ) (reputation as verified history), Network (reputation network effects)"
  template_references: "gatekeeper, ambassador, assessor, pedagogue, witness, architect"
---

# PVM-V4 Skill — Reputation Credentials

**Source:** Privacy Value Model V4 + BGIN IKP SBT Study Report + "Genesis of a Soul System" (Feb 2023)
**Target context:** Credential system designers, reputation economists, SBT researchers, onchain identity architects
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The intellectual lineage from Soulbound Tokens (SBTs) through BGIN multi-stakeholder research to Verifiable Relationship Credentials (VRCs). This skill traces how "reputation value" — non-capital, non-transferable value derived from contributions, relationships, and demonstrated understanding — evolved from a token primitive into a bilateral trust protocol.

The SBT research was formative. It identified the problem (Web3's hyper-financialisation and lack of social coordination tools) and proposed non-transferable tokens as a solution. The agentprivacy architecture extends this by recognising that unilateral tokens issued by authorities reproduce the surveillance model, and that bilateral credentials created through demonstrated understanding solve the problem without creating new power asymmetries.

## SBT origins

Weyl, Ohlhaver, and Buterin's "Decentralized Society: Finding Web3's Soul" (2022) introduced SBTs: non-transferable tokens that represent commitments, credentials, and affiliations. The thesis: Web3 has lacked facilities for social coordination, permitting plutocratic governance and superficial pseudonymous interactions.

**The BGIN IKP Study Report (2023):** 50+ contributors across BGIN's Identity, Key Management & Privacy working group produced the first multi-stakeholder analysis of SBT implications. Key findings:

"A token is revocable if an issuer can burn the token and re-issue it to a new wallet. Burning and re-issuing would make sense when keys are lost or compromised, and the issuer has an interest in ensuring the tokens are not financialised."

The study evaluated technical, social, and ethical considerations of tokenising "reputation value" — drawing from Szabo (1996), Cameron (2005), Sakimura (2021), and EIPs. Cautionary warnings: SBTs are closely related to consequential matters (digital identity). Multi-stakeholder collaboration is essential.

**The privacy gap identified:** "We initially assume publicity despite our deep interest in privacy because it is technically simpler to validate as a proof-of-concept." The SBT paper itself acknowledged that the public-by-default model was a temporary simplification, not a design goal.

## The SBT → VRC evolution

The agentprivacy architecture builds on SBTs but inverts the authority model:

| Property | SBT | VRC |
|----------|-----|-----|
| Issuance | Unilateral (issuer → holder) | Bilateral (both parties co-create) |
| Authority | Centralised issuer | No central authority |
| Privacy | Public by default | Private by default (shielded) |
| Revocability | Issuer-controlled | Bilateral (both must agree, or time-gated) |
| Transferability | Non-transferable | Non-transferable (same) |
| Recovery | Issuer re-issues | Understanding-based (RPP) |
| Trust model | Holder trusts issuer | Both parties trust the relationship |
| Accumulation | Token count | A(τ) = α · ln(1+\|τ\|) · h(τ) |

**Key insight:** SBTs solve the transferability problem (reputation should not be tradeable) but create a new power asymmetry (the issuer controls the credential). VRCs solve both by making credentials bilateral — no issuer, no authority, just two parties attesting to a shared truth.

## Reputation value

The BGIN study introduced "reputation value" — non-capital value derived from demonstrated contributions, relationships, and community membership. This is distinct from financial capital (tradeable), social capital (broad and diffuse), and intellectual capital (knowledge held).

**Reputation value properties:** Non-transferable (cannot be sold or given away), context-specific (meaningful in a specific community), accretive (builds over time through contributions), verifiable (can be proven to third parties), and privacy-sensitive (the specifics of contributions may be confidential even when the reputation is public).

PVM-V4 formalises reputation value through A(τ) — the temporal memory term. Reputation is not a score assigned by an authority. It is the logarithmic accumulation of verified interactions over time, gated by h(τ) (the proportion of interactions carrying cryptographic attestation).

## Privacy-preserving reputation

The core tension: reputation requires visibility (others must know you have it) but the details behind reputation require privacy (the specific contributions, positions, and relationships that built the reputation may be sensitive).

**Governance example (BGIN context):** A participant builds reputation through constructive contributions to working group discussions. Other participants should know "this person contributes valuably to governance." But the specific positions taken on contested topics — which may reveal competitive strategy — should remain private (Agentic Chatham House Rule).

**PVM-V4 resolution:** Selective disclosure. Prove reputation level without revealing the specific contributions that built it. "My A(τ) exceeds threshold T" without "here are the 47 specific interactions that compose it." This is a ZKP application: prove a property of the reputation (it exceeds a threshold) without revealing the data (the interaction history).

**Stratum-weighted reputation:** From the network_topology skill, agents at different sovereignty strata contribute different network weights. Reputation earned at higher strata (more sovereignty dimensions active, more complex interactions, heavier armor tier) carries more weight than reputation earned at lower strata. This is not elitism — it is information-theoretic: complex interactions signal more about capability than simple ones.

## The guild credential system

Guilds deploy their own credential systems using the template infrastructure:

**Guild-specific reputation:** Each guild defines what constitutes valuable contribution in its domain. A ZKP research guild values proof system contributions. A governance guild values deliberation quality. A dark forest guild values operational security. The A(τ) accumulates differently in each context.

**Cross-guild portability:** Reputation in one guild can be presented (via selective disclosure) to another guild without revealing the specific contributions. "I am a verified Heavy-tier contributor to Guild A" is a credential that Guild B can use for admission decisions without needing to audit Guild A's internal records.

**Guild entry through understanding:** The proverbiogenesis and understanding_as_key skills describe how guild entry works through demonstrated comprehension rather than credential presentation. The seeker must show they understand the guild's domain, not just that they hold a token.

## Connection to equation terms

**C (credential verifiability).** Reputation credentials are the primary content of C. Higher proof quality (ZK-backed, bilateral, temporally attested) means higher C. The SBT→VRC evolution increases C by making credentials bilateral and cryptographically attested rather than authority-issued.

**A(τ) (temporal memory).** Reputation IS temporal memory. The logarithmic accumulation means early contributions matter most (diminishing marginal return). The h(τ) gate means only cryptographically attested contributions count. This formalises what reputation systems have always known informally: reputation is slow to build, fast to lose, and impossible to fake over time.

**Network term.** Reputation creates network effects. A network where participants have high, verifiable reputation is more valuable per-member than one where reputation is unverifiable. The stratum weighting amplifies this: a few highly-reputed participants at stratum 3+ contribute more to network value than many unverified participants at stratum 0-1.

## Historical context

The Soulbis journey: started as a soulbound token research community (2022), produced the BGIN IKP study report with 50+ global contributors (2023), evolved through the IKP working group (privacymage as Co-Chair) toward bilateral credential systems, culminated in the VRC architecture and RPP protocol (2025-2026).

"SBTs are closely related to consequential matters, for one digital identity, a wide range of multi-stakeholders should come together." This BGIN principle — multi-stakeholder collaboration on identity systems — runs through the entire lineage from SBT research to VRC deployment.

## Open problems

1. Reputation decay — should reputation degrade over time like other PVM-V4 terms (e^{-λt})?
2. Negative reputation — how to encode and verify that an agent has been harmful without creating a blacklist system.
3. Reputation inflation — as guild membership grows, does reputation become less meaningful?
4. Cross-context reputation transfer — what are the limits of selective disclosure when contexts are very different?
5. Sybil reputation — can an attacker build legitimate reputation across multiple identities to amplify their effective standing?
6. Regulatory status — are onchain reputation credentials subject to "right to be forgotten" regulations?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
