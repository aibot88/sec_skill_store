---
name: agentprivacy-understanding-as-key
description: >
  Understanding-as-authentication for 0xagentprivacy RPP. Activates when
  discussing proverb-based access control, demonstrated comprehension as
  credential, the Oracle verification pipeline, viewing key / signing key
  separation in knowledge verification, or how understanding replaces
  passwords.
license: Apache-2.0
metadata:
  version: "5.2"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Key recovery architects, Zcash application developers, cognitive security designers, VRC ceremony builders"
  equation_term: "A(τ) (recovery through understanding), h(τ) (inscription as attestation), R(d) (visibility as disclosure control)"
  template_references: "soulbis, soulbae, cipher, gatekeeper, chronicler, pedagogue, healer"
---

# PVM-V4 Skill — Understanding as Key

**Source:** Privacy Value Model V4 + Signal to Sanctuary (Zypherpunk Hack 2025) + sync.soulbis.com
**Target context:** Key recovery architects, Zcash developers, cognitive security designers, VRC ceremony builders, identity restoration systems
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The paradigm shift from "what you have" to "what you understand." Traditional authentication fights human cognition — random seed phrases are precisely what humans are worst at remembering. Proverb-based trust works WITH cognitive architecture: demonstrated comprehension, relational memory, contextual meaning, bilateral understanding.

This skill specifies the three inscription paths (symmetric, asymmetric, interleaved), the visibility spectrum (0%→100%), φ-derived fragmentation ratios, VRC ceremony types, and the cognitive alignment that makes the whole system adoptable. First implemented at Zypherpunk Hack 2025 as Signal to Sanctuary on Zcash.

The recovery_rpp skill covers the protocol conceptually. This skill covers the implementation: how proverbs are committed onchain, how visibility ratios signal relationship style, and how ceremony types map to trust tiers.

## The cognitive alignment

Humans are terrible at remembering: random strings, seed phrases, long passwords, arbitrary key material.

Humans are excellent at remembering: relationships and their contexts, meaningful phrases and their origins, shared experiences and derived insights, stories and their lessons.

The Relationship Proverb Protocol aligns cryptographic security with cognitive architecture. Recovery becomes a function of understanding, not recall of arbitrary data. The proverb is not a random string — it emerged from engagement with specific content, personal context, the relationship's shared meaning, and the compression process itself. The same cognitive process that generated the original proverb can regenerate it.

## The three inscription paths

Three points on the spectrum from maximum privacy to maximum recoverability:

### Path 1 — Symmetric (Maximum Privacy)

**Structure:** hash(P_first_person || P_sanctuary) → onchain

Both proverbs contribute equally to a single hash. Neither is distinguishable onchain. Observers cannot determine which party initiated, what either proverb contains, or who the counterparties are.

Properties: complete privacy for both parties. Recovery requires both parties. All-or-nothing verification. Use cases: maximum privacy relationships, Blade-tier trust, situations where opacity matters more than recovery.

### Path 2 — Asymmetric (Current Default)

**Structure:** P_first_person → onchain (visible in transparent pool) + hash(P_first_person || P_sanctuary) → commitment

The First Person's proverb appears in cleartext onchain. The Sanctuary's response remains hidden, committed only in the hash. The First Person accepts visibility in exchange for recovery properties.

Properties: First Person proverb visible, Sanctuary hidden in hash. Understanding-based recovery enabled. First Person controls proof of engagement. Use cases: social recovery, progressive trust relationships, verifiable proof of spellbook engagement.

This is the Signal to Sanctuary default. The First Person sends proverb to the Oracle, published in the transparent pool. Oracle returns Sanctuary's response through a shielded channel. Transparent pool inscription contains: First Person proverb (visible) + commitment hash.

### Path 3 — Interleaved (Fragmented Commitment)

**Structure:** visible portion = ending of FP proverb + beginning of Sanctuary proverb. Hidden portion (in hash) = beginning of FP proverb + ending of Sanctuary proverb.

The proverbs fragment and interweave. Your ending with their beginning visible. Your beginning with their ending hidden. Neither party fully exposed, neither fully hidden.

Properties: partial privacy for both. Recovery requires understanding from BOTH. Mutual — neither controls disclosure alone. Creates a "cryptographic handshake" — you see where one ends and the other begins, but not the full journey of either.

**Why this interweave direction:** The visible portion shows how the First Person concluded their understanding and how the Sanctuary began their response. The hidden portion protects how the First Person arrived at their understanding and how the Sanctuary completed their response.

**φ-Derived fragmentation:** Instead of 50/50, golden ratio variants: 38.2% hidden / 61.8% visible (or inverted). The golden ratio governs the fragment boundary itself. The direction of the φ-split signals relationship emphasis.

## The visibility spectrum

The amount revealed is not just a technical parameter — it is a signal about the relationship itself. The cryptographic commitment structure becomes semantic.

| Visibility | Style | Meaning |
|-----------|-------|---------|
| 0% | Discrete | "This exists, but that's all you'll know" |
| 25% | Reserved | "A hint of what we share" |
| 38.2% (φ⁻¹) | Balanced privacy | "Privacy-first, but verifiable" |
| 50% | Mutual | "We're equally exposed" |
| 61.8% (φ) | Balanced openness | "Openness-first, but protected" |
| 75% | Declared | "Mostly visible commitment" |
| 100% | Public | "My understanding is on record" |

**The golden ratio sweet spots:**

38.2% visible (privacy-weighted): enough for a recovery anchor, enough hidden for meaningful privacy. Optimal for sensitive relationships, early trust, careful disclosure.

61.8% visible (openness-weighted): rich recovery context, sacred core preserved. Optimal for public collaborations, mature trust, verifiable commitment.

Hypothesis: these φ-derived points may represent natural attractors — relationship styles that stabilize at golden ratio visibility because they balance competing needs optimally.

**Progression over time:** Relationships may evolve through visibility styles: 0% → 25% (getting to know), 25% → 38.2% (trust growing), 38.2% → 50% (balanced mutual), 50% → 61.8% (comfortable being seen), 61.8% → 100% (public declaration). Each signal updates the onchain record. The history of visibility changes itself becomes meaningful.

## VRC ceremony types

Five ceremony types mapped to the visibility spectrum:

**Shadow Ceremony (0% / Symmetric):** Covert commitment. No identity disclosure. Both parties engage with same tale, each derives proverb independently, exchange through shielded channel. Onchain record: only hash. Use: whistleblower protection, sensitive collaborations, hostile environments.

**Guarded Ceremony (38.2%):** Privacy-weighted golden ratio. Meaning-recoverable with effort. Use: professional relationships, early trust.

**Balanced Ceremony (50% / Interleaved):** Mutual exposure. Neither party controls alone. True bilateral commitment. Use: partnerships, mutual accountability.

**Open Ceremony (61.8%):** Openness-weighted golden ratio. Understanding-recoverable. Use: public collaborations, verifiable trust.

**Declared Ceremony (100% / Asymmetric):** Public record. FP proverb published, Sanctuary response in hash. Use: public endorsements, credential issuance, community membership.

## Key derivation from proverbs

The ceremony produces relationship-specific keys: ceremony_key = derive(hash(P_fp || P_sanctuary), tale_id, timestamp, visibility_ratio).

Properties: deterministic (same inputs = same key), bilateral (requires both proverbs), contextual (bound to specific tale/time), recoverable (understanding regenerates proverbs → regenerates key), private (key never appears onchain, only commitment hash).

## Ceremony progression (trust ladder)

**Signal Phase (0.01 ZEC each):** Multiple signals build trust through Blade → Light → Heavy → Dragon. Each signal demonstrates continued understanding.

**Ceremony Phase (1 ZEC):** Formal bilateral commitment. VRC established with chosen visibility. Key material derived. Relationship anchored onchain.

**Evolution Phase:** May re-ceremony at different visibility. History becomes trust signal. Progressive revelation as trust deepens, or progressive privacy as relationship matures.

## Signal to Sanctuary architecture

The first production implementation (Zypherpunk Hack 2025, Zcash):

1. First Person reads tale at agentprivacy.ai/story, forms proverb from understanding
2. Zodl Wallet (Swordsman): paste memo with proverb, send z→z shielded (0.01 ZEC)
3. Oracle (Viewing Key Only): decrypt memo, fetch canonical from IPFS, AI verifies semantic match. NEVER sees amount/address/timing. Triggers golden split on verification.
4. Signal splits: 61.8% transparent pool (inscription with proverb) + 38.2% shielded pool (protocol operations)
5. VRC Callback: Oracle sends response proverb to FP's z-address. Bilateral VRC established.

**Key separation:** Viewing Key (Mage's sight) = can read memos, verify proverbs, cannot spend, cannot sign. Signing Key (Swordsman's action) = can execute golden split, create inscriptions, only acts upon verified signal. The agent that sees cannot act. The agent that acts only does upon verified signal. Mathematical separation, not policy trust.

## Connection to equation terms

**A(τ):** Each inscription is an attested transition. Ceremony inscriptions contribute to h(τ). The progressive ceremony chain builds temporal memory through demonstrated understanding rather than stored secrets.

**R(d):** The visibility ratio IS the disclosure function. R(d) is directly controlled by the ceremony type chosen. Shadow ceremony: R ≈ 0 (no disclosure). Declared ceremony: R higher but bounded (FP proverb visible, Sanctuary hidden, bilateral reconstruction impossible from one side).

**Φ(Σ):** The ceremony visibility maps to Swordsman/Mage separation. 0% = pure Swordsman (maximum protection). 100% = Mage-enabled recovery. The ratio is the privacy/delegation tradeoff made concrete.

**T(π):** Each ceremony is a transition. Re-ceremony at different visibility is a lattice move. The evolution of visibility over time is a trajectory through disclosure space.

## Entropy and security

Proverbs are not random strings but they are not low-entropy. Proverb formation incorporates: the specific tale/content engaged with, the timing, the participant's unique compression patterns, the relationship's shared chronicles, personal interpretation style.

An attacker would need to: know which content was engaged with, understand the relationship's context, comprehend the principle being compressed, match the compression style. Brute force requires understanding the relationship itself — not just enumerating words.

## The Understanding-as-Key Ceremony (V5.2 — Act XXIX)

Act XXIX introduces the full 5-step Understanding-as-Key ceremony protocol:

### The 5-Step Protocol

**Step 1 — Language Capture**
The seeker expresses comprehension in their own words. Not parroting, but genuine reformulation that demonstrates internalised understanding.

**Step 2 — Constellation Mapping**
The understanding is traced through spell nodes and edges. Where in the spellweb does this comprehension connect? Which proverbs resonate?

**Step 3 — Simultaneous Forging**
Both Swordsman and Mage forge a blade from the same understanding — independently, in parallel. The configurations should converge if understanding is genuine.

**Step 4 — Proverb Inscription**
The shared truth is encoded as a compressed wisdom marker. A new proverb emerges from the ceremony, capturing what was understood.

**Step 5 — Bilateral Witness**
Both parties affirm the shared understanding. The ceremony completes only when both attest to the same outcome.

### Properties

- **Substrate-agnostic:** The ceremony works regardless of underlying technology
- **Substrate-anchored:** Proof exists in the system (onchain, in spellweb, etc.)
- **Bilateral:** Neither party can complete alone
- **Understanding-verified:** Demonstrated comprehension, not possession of secrets

### First Ceremony Performed

Act XXIX records the first Understanding-as-Key ceremony:
- **Understanding:** "The 2D lock will break. The 6D lattice provides dimensional defence."
- **Constellation:** quantum-defence → blade-forge → three-axis-separation
- **Witness:** External paper (Google Quantum AI) + internal architecture
- **Result:** Dragon's flight achieved

## Open problems

1. Entropy quantification — formal measurement of proverb entropy across different content types and relationship contexts.
2. φ-attractor hypothesis — do visibility ratios actually stabilize at golden ratio points or is this observational bias?
3. Interleaved fragment security — does the visible handshake leak enough to reconstruct hidden portions through correlation?
4. Cross-ceremony linkability — can an observer link Shadow ceremonies to the same participant through timing analysis?
5. Scalability — how does ceremony overhead scale with guild size?
6. Cultural universality — does the cognitive alignment hold across languages, cultures, and neurodivergent populations?
7. **V5.2:** Convergence verification — how precisely must the simultaneous forging converge to validate understanding?
8. **V5.2:** Ceremony replay — can the same understanding be ceremonied multiple times with different counterparties?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
