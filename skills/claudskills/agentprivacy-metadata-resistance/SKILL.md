---
name: agentprivacy-metadata-resistance
description: >
  Traffic analysis resistance, timing obfuscation, and metadata stripping
  for 0xagentprivacy swordsman operations. Activates when designing
  defences against metadata correlation, implementing mixnet routing,
  padding strategies, timing decorrelation, or any protection that targets
  the signals AROUND encrypted content rather than the content itself.
  Triggers: "metadata", "traffic analysis", "timing attack", "correlation",
  "mixnet", "padding", "network fingerprint", "side channel", "metadata leakage".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "R(d) — metadata is the reconstruction vector that bypasses content encryption"
  template_references: "soulbis, sentinel, ranger, sith, warden, archer"
---

# PVM-V4 Skill — Metadata Resistance

**Source:** Privacy Value Model V4 + Dark Forest Strategy + Threat Adversarial Modelling
**Target context:** Network privacy engineers, mixnet designers, traffic analysis researchers, browser privacy builders, anti-surveillance infrastructure architects
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Encrypting content is necessary but nowhere near sufficient. The envelope tells a story even when the letter is sealed. Who talks to whom, when, how often, for how long, from where, using what device — this metadata is often more revealing than content itself. Intelligence agencies have stated publicly that they "kill people based on metadata."

Metadata resistance is the swordsman's discipline of stripping, obfuscating, and decorrelating the signals that surround encrypted content. Where crypto_zkp protects what is said, metadata resistance protects that anything was said at all.

## The metadata attack surface

Every digital interaction produces metadata across multiple layers:

**Network layer.** IP addresses, connection timing, packet sizes, TLS fingerprints, DNS queries. An observer who sees Alice connect to a Zcash node at 14:03 knows Alice uses Zcash — even though the transaction content is shielded. The content privacy is irrelevant; the connection metadata is the signal.

**Application layer.** Access patterns, query frequencies, data volumes, API call sequences. A health app that queries a diabetes database every morning reveals a diagnosis — even if every query is encrypted. The pattern IS the data.

**Temporal layer.** When actions occur, how they cluster, what precedes and follows them. A Person who searches for "divorce lawyer" and then changes their insurance beneficiary within the same week has revealed their intent through timing — no content decryption needed.

**Social layer.** Who interacts with whom, how often, in what sequence. Communication graphs reveal organisational structure, influence networks, and relationship intensity — all without reading a single message.

**Device layer.** Hardware fingerprints, screen resolution, installed fonts, battery status, sensor data. Each device characteristic narrows the anonymity set. Enough characteristics, combined, uniquely identify a device across contexts.

## Defence primitives

**Mixing.** Route communications through intermediate nodes that batch, reorder, and relay messages. The observer sees messages enter and leave the mix, but cannot correlate specific inputs to specific outputs. Mixnets (Nym, Loopix) provide formal anonymity guarantees against traffic analysis.

**Padding.** Normalise packet sizes and communication volumes. If all messages are the same size (padded to a fixed length), packet size analysis reveals nothing. If all time slots produce the same traffic volume (cover traffic fills empty slots), timing analysis reveals nothing. Padding trades bandwidth for privacy.

**Timing decorrelation.** Break the temporal link between cause and effect. If a Person observes something and contributes to an Intel Pool, the contribution should be delayed by a randomised interval — not sent immediately. The delay breaks the temporal correlation between observation and contribution.

**Onion routing.** Wrap communications in multiple encryption layers, each removable only by a specific relay. No single relay knows both origin and destination. Tor is the canonical implementation; the architecture may use Tor, I2P, or custom onion routing depending on the threat model.

**Dummy traffic.** Generate synthetic communications that are indistinguishable from real ones. If the network sees 100 messages and only 10 are real, traffic analysis must somehow distinguish real from dummy — a fundamentally harder problem than analysing a stream where every message is real.

## Metadata resistance by persona

**Warden 🗡️🌐** — Browser-level metadata. User agent normalisation, canvas fingerprint resistance, WebRTC leak prevention, cookie isolation, referrer stripping. The Warden's browser agent produces a metadata profile that is indistinguishable from millions of other users. First-party isolation ensures that metadata from site A cannot be correlated with metadata from site B.

**Sentinel 🗡️🛡️** — Infrastructure-level metadata. Network traffic analysis resistance at the infrastructure layer. TEE attestation that proves computation happened without revealing what was computed. The Sentinel designs the mixnet routing, the padding schedules, the cover traffic generation.

**Ranger 🗡️🌲** — Dark forest metadata. Operational security for high-threat environments. Timing patterns that don't reveal activity cycles. Location metadata that doesn't reveal physical position. The Ranger's strategy is to make the Person's metadata footprint indistinguishable from background noise.

**Archer 🗡️🎯** — Precision metadata control. When a disclosure MUST happen (the Person authorises it), the Archer ensures the metadata residue is minimal. One data point delivered. No connection metadata. No timing correlation. No device fingerprint. The Archer's precision operation leaves no metadata shadow.

**Sith 🗡️🔴** — Metadata attack research. The Sith models the adversary's metadata analysis capabilities. What can a global passive adversary learn from traffic patterns? What can a compromised relay learn from message timing? The Sith's red team identifies metadata vulnerabilities before adversaries exploit them.

## The metadata hierarchy of needs

Not all metadata is equally dangerous. The swordsman prioritises defence based on reconstruction potential:

**Critical (defend always).** Social graph metadata — who talks to whom. This is the highest-value metadata for adversaries. It reveals relationships, organisational structure, and influence networks. Defend with mixing and cover traffic.

**High (defend by default).** Temporal patterns — when activity happens. Activity timing reveals routines, interests, and intent. Defend with timing decorrelation and dummy traffic.

**Medium (defend when relevant).** Volume patterns — how much data moves. Transaction volumes can reveal economic activity. Communication volumes can reveal relationship intensity. Defend with padding.

**Low (defend on request).** Device metadata — what hardware is used. Device fingerprinting is primarily a tracking mechanism, not an intelligence mechanism. Defend with browser normalisation (Warden's domain).

## Formal guarantees

Metadata resistance can provide formal privacy guarantees when the underlying primitives are properly configured:

**k-anonymity.** The Person's metadata is indistinguishable from at least k-1 other Persons' metadata. Achieved through mixing with a pool of at least k participants.

**Differential privacy (ε).** The presence or absence of the Person's communication in the network changes any observer's output by at most factor e^ε. Achieved through cover traffic calibrated to the ε parameter.

**Unlinkability.** Two actions by the same Person cannot be linked by any observer. Achieved through independent mixing paths for each action, with no shared metadata between paths.

## The reconstruction connection

Metadata is the primary reconstruction vector that bypasses content encryption. The reconstruction ceiling R<1 holds only if metadata analysis cannot fill the gap left by content protection. If content is perfectly encrypted but metadata is fully exposed, R can approach 1 through metadata alone — the swordsman has failed.

The R<1 proof assumes bounded metadata leakage. This skill operationalises that assumption: these are the specific defences that keep metadata leakage within the bounds the proof requires.

## Connection to the equation

**R(d) — reconstruction.** Metadata is how adversaries reconstruct behavioural models when content is encrypted. Every metadata defence directly reduces R(d). The reconstruction ceiling R<1 holds only if metadata resistance is maintained alongside content privacy.

**P — protection.** Content encryption provides P for message content. Metadata resistance provides P for message context. Total protection requires both: P_content × P_metadata. If either approaches zero, the product approaches zero.

**I(S;M|π) — mutual information.** The information-theoretic separation between swordsman and mage observation sets must hold at the metadata level as well as the content level. If the swordsman's signing patterns (timing, frequency) leak metadata about the mage's observation patterns, the separation weakens. Metadata resistance maintains the informational gap.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
