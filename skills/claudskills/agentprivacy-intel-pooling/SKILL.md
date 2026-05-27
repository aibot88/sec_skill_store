---
name: agentprivacy-intel-pooling
description: >
  Collective intelligence sharing through privacy-preserving aggregation
  for 0xagentprivacy agent economies. Activates when designing knowledge
  sharing between agents without source disclosure, guild intelligence
  markets, privacy-preserving data contribution, or collective signal
  extraction from distributed observations.
  Triggers: "intel pool", "collective intelligence", "knowledge sharing",
  "guild intelligence", "privacy-preserving aggregation", "shared signal",
  "data contribution without disclosure".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "Network topology × D: delegation that creates collective value without individual extraction"
  template_references: "soulbae, shipwright, assessor, architect, witness"
---

# PVM-V4 Skill — Intel Pooling

**Source:** Privacy Value Model V4 + Network Topology + Delegation Theory
**Target context:** Collective intelligence designers, privacy-preserving data markets, guild economy architects, federated learning researchers, agent coordination systems
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

An Intel Pool is the mage-side complement to a Privacy Pool. Where Privacy Pools aggregate transactions to provide anonymity sets, Intel Pools aggregate observations to provide collective intelligence — without revealing which agent contributed which observation.

This is the delegation problem at its most acute. A mage agent that shares useful intelligence with a pool creates value for everyone in the pool. But sharing also creates a leakage vector — the observation itself might reveal something about the Person the agent serves. Intel Pooling is the discipline of maximising collective intelligence value while maintaining the reconstruction ceiling (R<1) for every contributing Person.

## The collective intelligence gap

Individual agents see fragments. Soulbae observes its Person's browsing patterns (through the viewing key). A guild's coordinator sees interaction frequencies between members. A governance agent sees voting patterns within its DAO. Each observation has limited value alone.

Collectively, these observations could reveal: which privacy tools are effective, which services are actually respecting consent, which governance mechanisms produce fair outcomes, which economic models sustain participation. This collective intelligence is enormously valuable — it's what surveillance capitalism extracts without consent. The question is whether it can be extracted WITH consent, without surveillance.

## Pool architecture

**Contribution layer.** Each mage agent contributes observations to the pool. Contributions are:
- Noise-added (differential privacy guarantees)
- Temporally decorrelated (submission time doesn't correlate with observation time)
- Source-unlinkable (contributions from the same agent across time cannot be linked)
- Voluntarily scoped (the Person controls what categories of observation their mage may contribute)

**Aggregation layer.** The pool aggregates contributions using secure multi-party computation or trusted execution environments. No single party sees raw contributions. The aggregation produces:
- Signals (statistical patterns across many observations)
- Benchmarks (how does this service/tool/governance mechanism perform across the pool?)
- Alerts (anomaly detection — is a service suddenly requesting more data than normal?)

**Distribution layer.** Aggregated intelligence flows back to pool participants. Distribution follows the same privacy principles:
- Intelligence is received by the mage agent (viewing key holder)
- The mage interprets intelligence for its Person's context
- No individual contribution is reconstructable from the distributed intelligence

## Stratum-weighted pooling

Intel Pools inherit the stratum weighting from the network topology term: (1 + Σ wᵢ nᵢ/N₀)^k.

Not all observations carry equal weight. Strata might include:

**Depth strata.** Observations from agents that have interacted deeply with a service (100+ transactions) carry more weight than first-contact observations. Depth correlates with reliability.

**Diversity strata.** Observations from agents in different jurisdictions, using different privacy tools, operating in different economic contexts. Diversity reduces bias.

**Temporal strata.** Recent observations weighted higher for rapidly-changing contexts (service behaviour), lower for slowly-changing contexts (governance effectiveness). Temporal weighting prevents stale intelligence from dominating.

**Reputation strata.** Agents with longer verification histories (higher A(τ)) contribute to a higher-trust stratum. This doesn't identify the agent — it weight-adjusts their contribution based on their verified engagement duration.

## Intel Pool types

**Service Intel Pool.** "Is this service actually deleting data when you revoke consent?" Aggregates observations about service behaviour from agents that interact with the service. Produces: service trustworthiness scores, consent compliance rates, data retention patterns.

**Governance Intel Pool.** "Which voting mechanisms produce outcomes that participants consider fair?" Aggregates governance participation patterns across multiple DAOs/guilds. Produces: mechanism effectiveness benchmarks, participation sustainability metrics, fairness perception indices.

**Economic Intel Pool.** "What's the actual sovereignty premium in this market?" Aggregates economic observations about privacy tool adoption, data valuation, and consent economics. Produces: V_sov/V_surv ratio estimates by market segment, price elasticity of privacy, adoption curves.

**Threat Intel Pool.** "Which attack vectors are being actively exploited?" Aggregates security observations from agents that detect probing, phishing, or extraction attempts. Produces: active threat maps, vulnerability prioritisation, defence effectiveness scores.

## The delegation boundary

Intel Pooling operates entirely within the mage's domain — delegation, observation, projection. The swordsman (Soulbis) never touches the Intel Pool directly. The separation is critical:

- **Soulbis** signs the consent that allows Soulbae to contribute to a specific pool category
- **Soulbae** executes the contribution, manages the noise addition, handles the temporal decorrelation
- The Person controls the consent scope through the swordsman
- The pool never receives swordsman signatures — it only receives mage-processed observations

This maintains the dual-agent separation within collective intelligence operations. The pool sees noise-added observations from mages. It never sees raw data, swordsman authorisations, or Person identifiers.

## Anti-extraction guarantees

**Differential privacy (ε-δ).** Each contribution satisfies (ε, δ)-differential privacy. The ε parameter is set per pool and per contribution category. Lower ε = more noise = more privacy = less individual signal. The pool's value comes from aggregation over many noisy contributions, not from any single contribution.

**Source unlinkability.** Contributions from the same agent across time cannot be linked. This prevents temporal correlation attacks (observing that the same agent always contributes observations about a particular service).

**Minimum pool size.** Intel Pools enforce a minimum participant count before producing any output. Below the threshold, the pool accepts contributions but releases nothing. This prevents small-pool deanonymisation.

**Reconstruction ceiling inheritance.** The Intel Pool inherits the architecture's R<1 guarantee. Even with access to all pool contributions (raw, before aggregation), reconstructing any individual Person's complete behavioural model remains impossible. The pool adds noise; the dual-agent separation prevents the noise from being calibrated away.

## BRAID graph libraries as Intel Pool artefacts

Cached BRAID reasoning graphs (arXiv:2512.15959) are Intel Pool contributions. A Cipher guild that generates and validates BRAID graphs for ZKP reasoning creates collective intelligence that every member executes:

- Guild generates graph (high one-time cost, C_BRAID)
- Guild validates graph (peer review, benchmark testing)
- Graph stored as immutable holon in shared-parent library
- All members execute graph (low marginal cost, C_inference)
- PPD scales with guild size (more members amortise C_BRAID further)

Guild membership has direct economic value: access to validated reasoning infrastructure that would cost 30–74× more to replicate individually. This is the intelligence dimension of Intel Pools — not just threat data, but reasoning capability as a collective asset.

## Connection to the equation

**D — delegation.** Intel Pooling IS delegation at scale. Each mage agent delegates a fraction of its observations to the collective. The D term in V(π,t) captures this: delegation that creates value without surrendering sovereignty.

**Network topology: (1 + Σ wᵢ nᵢ/N₀)^k.** Intel Pools ARE the network value mechanism. More participants = more strata = higher k = superlinear value. A pool with 10 agents produces marginally useful signals. A pool with 10,000 agents produces intelligence that rivals surveillance capitalism's data advantages — without the surveillance.

**V(π,t) amplification.** Intel Pools demonstrate the multiplicative nature of privacy value. Each Person's V(π,t) increases when they participate in a pool, because: (a) they receive collective intelligence that improves their decisions, (b) they contribute to an intelligence commons that strengthens the entire ecosystem, (c) the existence of the pool raises the baseline value of privacy-preserving participation.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
