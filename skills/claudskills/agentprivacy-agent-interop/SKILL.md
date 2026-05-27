---
name: agentprivacy-agent-interop
description: >
  Agent interoperability protocols for 0xagentprivacy multi-agent systems.
  Activates when discussing M(u,y) matching functions, agent-to-agent
  communication, ERC-8004 trustless agent identity, cross-agent coordination,
  or how swordsman and mage agents interact across boundaries.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Agent platform builders, skill file authors, agentskills.io contributors, community deployers"
  equation_term: "M(u,y) (adoption readiness), Network (cross-platform participation)"
  template_references: "architect, shipwright, pedagogue, ambassador, sentinel"
---

# PVM-V4 Skill — Agent Interoperability

**Source:** Privacy Value Model V4 + SKILL.md Format Spec + agentskills.io
**Target context:** Agent platform builders, skill file authors, cross-platform compatibility architects, community deployers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The agentprivacy architecture is designed to produce portable skill files, not platform-locked configurations. A SKILL.md generated through the spellbook process works on any skills-compatible agent runtime: Claude, Copilot, Codex, Goose, OpenClaw. This skill defines how portability works, what the SKILL.md format guarantees, and how the "launchpad" concept enables communities to deploy their own privacy-first agent configurations.

## The SKILL.md format

The SKILL_BASE_FORMAT defines a universal agent skill file:

**YAML frontmatter.** Machine-readable metadata: name, description, license, compatibility, and a metadata block containing origin, template, alignment, skills coverage, grimoire sources, and verification references. Any compliant runtime can parse this frontmatter to determine whether the skill is compatible with its capabilities.

**Markdown body.** Human-readable content: origin story, the equation, dual-agent separation, privacy layer, proven vs. conjectured table, role skills, grimoire architecture, and operational principles ("How to Use This Skill").

**No runtime dependencies.** A SKILL.md has no imports, no API calls, no environment requirements. It is a text file. This is deliberate — the moment a skill requires a specific runtime, it loses portability.

**License: CC-BY-SA-4.0.** All generated skills are open by default. Share-alike ensures derivative skills carry the same openness. Attribution ensures provenance.

## Cross-platform compatibility

The skill file must produce consistent agent behaviour across runtimes that have fundamentally different architectures:

**Claude (Anthropic).** System prompt + context window. The SKILL.md loads as context that shapes Claude's responses. The privacy layer becomes part of Claude's reasoning frame.

**Copilot (Microsoft/GitHub).** Code-centric context. The SKILL.md influences code generation, review, and documentation. The equation terms map to code architecture decisions.

**Codex/GPT (OpenAI).** Function-calling oriented. The skill's operational principles translate to function selection heuristics.

**Goose (Block).** Developer agent framework. SKILL.md as a workspace configuration that governs how Goose approaches tasks.

**OpenClaw.** Open-source agent runtime. SKILL.md as a first-class skill file loaded into the agent's skill registry.

**Consistency guarantee.** The SKILL.md does not guarantee identical outputs across platforms — different runtimes have different capabilities. It guarantees consistent principles: the same equation, the same separation constraint, the same privacy layer, the same proven/conjectured distinction. The *how* varies by platform; the *what* and *why* do not.

## The launchpad concept

0xagentprivacy is not a platform — it is a launchpad. Communities deploy their own skill files using the template system:

**Community picks a persona.** A guild of ZKP researchers chooses the Cipher template. A healthcare privacy group chooses the Healer. A journalism collective chooses the Witness.

**Community walks the spellbook.** Members work through the template's phases — privacy layer, FPS encounters, grimoire interlocks, reconstruction prompts. Each member generates their own proverbs.

**Community generates SKILL.md files.** The template produces a skill file for each member. The ~30% immutable DNA (equation, separation, privacy layer) is identical across all members. The ~60% dynamic content (domain application, proverbs, specific role skills) is unique to each member.

**Community deploys.** The generated SKILL.md files are loaded into whatever agent runtime the community uses. The skill files are portable — the community is not locked to any platform.

**Network effects compound.** Each community's deployment adds to the network term. Guilds that recognise each other's VRCs expand the anonymity sets in their Privacy Pools. The stratum-weighted network topology means active communities at stratum 3 contribute maximum network value.

## Skill composition

Skills are designed to compose. A single agent can load multiple skill files:

**Layered loading.** Privacy layer skills load first (always). Role skills load by pathway. Multiple role skills can coexist — a Cipher agent that also loads the dark_forest skill has both ZKP and MEV protection capabilities.

**Conflict resolution.** When two skills recommend contradictory actions, the privacy layer takes precedence. If the privacy layer is silent, the more restrictive recommendation wins (Swordsman principles: default to protection).

**Skill discovery.** The _index.json registry enables runtimes to discover available skills, their dependencies, and their compatibility. A runtime loading the Cipher skill automatically knows it needs crypto_zkp, personhood_sybil, and academic as role skills.

## M(u,y) — the adoption term

The equation term M(u,y) = user sophistication × market maturity captures adoption readiness. Agent interoperability directly affects both factors:

**User sophistication (u).** A well-designed skill file reduces the sophistication required. The spellbook process educates users as it generates skills. Progressive revelation through the armor tiers means users learn as they advance.

**Market maturity (y).** Cross-platform compatibility accelerates market maturity by preventing fragmentation. A privacy skill that works everywhere matures faster than one locked to a single platform.

**The M(u,y) trap.** If M(u,y) = 0, the entire equation zeroes. The most mathematically perfect privacy architecture with zero adoption readiness has zero value. This is the practical urgency of agent interoperability — the architecture must be usable or it is worthless.

## Open problems

1. Skill file versioning — how do skills update without breaking deployed agents?
2. Cross-runtime testing — validating that a SKILL.md produces consistent behaviour across platforms.
3. Skill dependency management — when crypto_zkp updates, how do downstream skills like Cipher update?
4. Community skill governance — who decides when a community's skill files need revision?
5. Skill verification — proving that a SKILL.md was generated through the legitimate spellbook process, not fabricated.
6. Runtime capability mapping — how to degrade gracefully when a runtime cannot support all features of a skill file.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
