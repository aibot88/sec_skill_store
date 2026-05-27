---
name: agentprivacy-forensic-defense
description: >
  Incident response, breach containment, damage assessment, and evidence
  preservation for 0xagentprivacy swordsman operations. Activates when a
  privacy breach is detected or suspected, when designing post-compromise
  recovery procedures, when building forensic audit capabilities, or when
  the swordsman must shift from prevention to damage control.
  Triggers: "breach", "incident response", "compromise", "forensic",
  "damage assessment", "evidence preservation", "post-compromise",
  "breach containment", "data exposure", "leak detection".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "h(τ) — integrity under stress; R(d) — bounding reconstruction after breach"
  template_references: "soulbis, sentinel, sith, witness, ranger, archer"
---

# PVM-V4 Skill — Forensic Defense

**Source:** Privacy Value Model V4 + Dark Forest Strategy + Threat Adversarial Modelling
**Target context:** Incident response architects, privacy breach investigators, post-compromise recovery designers, forensic auditors, adversarial simulation builders
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Prevention fails. Every security architecture must plan for the moment when an adversary gets through. Forensic defense is what the swordsman does AFTER the boundary is breached: contain the damage, preserve the evidence, assess what was exposed, and restore sovereignty as quickly as possible.

This is the least-discussed skill because it acknowledges failure. But it is arguably the most important — a system that recovers gracefully from compromise protects sovereignty over time far better than a system that is impenetrable until it isn't.

## The breach detection surface

Before forensic response begins, the breach must be detected. Detection sources include:

**Anomaly signals from boundary enforcement.** Requests succeeding that should have been blocked. Authorisations appearing without the swordsman's signature. Disclosure volumes exceeding consent scope. These are direct signals — something bypassed the enforcement pipeline.

**Metadata correlation alerts.** The Sentinel detects unexpected correlation between the swordsman's operations and external observations. A third party seems to know when consent was granted before the consent was acted on. Timing patterns suggest an observer inside the decision pipeline.

**Trust graph anomalies.** A counterparty's behaviour changes in ways that suggest they have information they shouldn't. A service starts requesting data categories it never requested before — as if it learned what data exists. Social engineering attempts targeting the Person's bilateral relationships suggest reconnaissance from leaked trust graph data.

**External notification.** A counterparty reports a breach on their end. A security researcher publishes a vulnerability in a dependency the architecture uses. A regulator issues an alert about a compromised service in the Person's consent network.

**Red team findings.** The Sith's adversarial simulations identify a vulnerability that may have already been exploited. The distinction between "could be exploited" and "has been exploited" is the difference between patching and forensics.

## The incident response sequence

**Phase 1 — Containment (minutes).** Stop the bleeding. The swordsman executes emergency procedures:
- Revoke all session keys (boundary_enforcement Stage 6 enters lockdown)
- Suspend all active delegation keys pending assessment
- Activate elevated threat level across the entire enforcement pipeline
- Isolate the compromised component (if identified) from the rest of the key hierarchy
- The principle: assume the worst, contain broadly, refine later

**Phase 2 — Assessment (hours).** Determine scope. What was compromised?
- **Key material assessment.** Which keys may have been exposed? Check the key hierarchy — if a parent key is compromised, all child keys are presumed compromised (cascade assumption). If only a leaf key, the blast radius is bounded.
- **Data exposure assessment.** What data flowed through the compromised channel? Cross-reference the audit trail (boundary_enforcement logs) with the compromise timeline. Every allow decision during the exposure window is potentially compromised data.
- **Reconstruction impact.** Calculate the maximum R(d) given the exposed data. How much of the Person's behavioural model could an adversary reconstruct from what was leaked? If R(d) still holds below 1 even with the breach data, the architecture's guarantees survived. If R(d) approaches 1, the Person needs to know.

**Phase 3 — Evidence preservation (concurrent with Phase 2).** Forensic integrity requires preserving evidence before it degrades:
- Snapshot the audit trail at the moment of detection (immutable copy)
- Record the swordsman's state at detection: active keys, active consents, active delegations, threat level
- Document the detection signal chain: what triggered the detection, when, through which channel
- Hash and timestamp all evidence — the Witness creates a verified record of the incident

**Phase 4 — Notification (hours to days).** Who needs to know?
- The Person — always, immediately, with honest assessment of exposure
- Counterparties whose data may have been exposed — within the timeframe required by applicable regulation and bilateral agreements
- The trust graph — affected bilateral relationships receive targeted notification through VRC channels
- Regulatory bodies — if required by jurisdiction

**Phase 5 — Remediation (days to weeks).** Restore sovereignty:
- Rotate all compromised keys (key_ceremony rotation protocol)
- Revoke and reissue all credentials that touched compromised key material
- Re-establish bilateral relationships through fresh VRC ceremonies if trust graph data was exposed
- Update boundary enforcement policies to address the exploitation vector
- Commission the Sith to simulate the attack and verify the remediation closes the vector

**Phase 6 — Post-incident review (weeks).** What went wrong? What worked?
- Root cause analysis: how did the adversary get through?
- Detection latency: how long between compromise and detection? Every hour of latency increased exposure.
- Containment effectiveness: did the emergency procedures limit the blast radius?
- Recovery completeness: is the Person's sovereignty fully restored?
- Architecture lessons: does this incident reveal a structural weakness that requires architectural change?

## Blast radius calculus

The blast radius of a breach depends on what was compromised:

**Session key compromise.** Smallest blast radius. Only the single session's transactions are exposed. No cascade. The session key expires naturally and the damage is bounded by the session's scope.

**Delegation key compromise.** Bounded by the delegation's scope and temporal bound. If the delegation was "health data disclosure to Provider X for 30 days," the maximum exposure is that specific data category to that specific entity for that time window.

**Domain key compromise.** All operations within that domain are potentially exposed. If the identity domain key is compromised, all VRC inscriptions signed by that key are suspect. Requires full domain key rotation and credential reissuance.

**Master key compromise.** Maximum blast radius. All derived keys are presumed compromised. Full key tree regeneration. Fresh genesis ceremony. All bilateral relationships must be re-established. This is the sovereignty equivalent of starting over — the most catastrophic failure mode.

**Viewing key compromise.** Different from signing key compromise. The adversary can SEE but not AUTHORISE. They can read what the mage reads — the Person's data as interpreted by Soulbae — but they cannot sign anything, cannot authorise disclosures, cannot impersonate the swordsman. The breach is observational, not operational. Still serious (confidentiality lost) but the integrity of the protection system remains intact.

## The forensic-privacy tension

Forensic investigation inherently conflicts with privacy: you need to examine data to determine what was exposed, but examining data is itself a privacy operation. The architecture resolves this through:

**Self-forensics.** The Person's swordsman conducts the forensic investigation using the Person's own keys. No external investigator needs access. The audit trail is encrypted to the Person — only they can decrypt and examine it.

**Scoped investigation.** If the Person engages external forensic assistance (a trusted security firm, a guild's incident response team), the assistance operates through a delegation key with explicit forensic scope: "This key can read my audit trail for the period [start] to [end], for the purpose of breach investigation, for 14 days." The delegation is bounded, temporal, and revocable.

**Evidence without exposure.** Zero-knowledge techniques can prove breach properties without revealing breach details. "I can prove that fewer than N records were exposed" without revealing which records or their contents. This enables regulatory compliance and counterparty notification without compounding the breach.

## Connection to the equation

**h(τ) — integrity.** A breach tests integrity under stress. The h(τ) fraction measures how well the architecture's guarantees survive real adversarial contact. A system that detects quickly, contains effectively, and recovers completely maintains high h(τ) even through incidents. A system that discovers breaches months later, contains poorly, and never fully recovers shows declining h(τ).

**R(d) — reconstruction ceiling.** The forensic assessment's most critical output: does R<1 still hold after accounting for the breach data? If yes, the architecture's core guarantee survived. If no, the Person must be informed that their behavioural model may be substantially reconstructable — the sovereignty guarantee was temporarily violated.

**e^{-λt} — temporal decay.** Time is the forensic defender's ally. Exposed data decays in relevance. A breach that exposed 30 days of browsing data is less damaging a year later than a day later — the browsing patterns have changed, the data is stale. The temporal decay term models this recovery: V(π,t) begins climbing back toward pre-breach levels as the exposed data ages.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
