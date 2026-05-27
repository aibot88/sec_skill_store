---
name: agentprivacy-mesh-architecture
description: >
  Mesh network architecture for 0xagentprivacy. Activates when discussing
  control plane vs data plane separation, Tailscale/WireGuard mesh networks,
  the Dragon's Hide metaphor, NAT traversal, DERP relays, sovereign overlay
  networks (tailnets), or how network-layer separation enforces privacy without
  central watchtowers.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Network architects, mesh network designers, privacy infrastructure builders"
  equation_term: "Control⊥Data as network-layer enforcement of dual-agent separation"
  template_references: "soulbis, warden, architect, shipwright"
  spellbook_act: "Act XXV — The Dragon's Hide"
---

# PVM-V4 Skill — Mesh Architecture & Control/Data Separation

**Source:** Privacy Value Model V4 + First Person Spellbook Act XXV (The Dragon's Hide)
**Target context:** Network architects, mesh network designers, privacy infrastructure builders, sovereign overlay network implementers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Act XXV discovered that the dual-agent separation (Swordsman ⊥ Mage) has a direct analogue at the network layer: **control plane vs data plane separation**. The coordination server holds the ACLs (who may speak), but never touches what is said. The mesh tunnels carry encrypted content that neither the coordinator nor any relay can decrypt.

This is the Swordsman/Mage architecture implemented in network infrastructure. The "Dragon's Hide" metaphor: each WireGuard tunnel is a scale, independently hardened, overlapping to form impenetrable protection. The mesh IS the dragon's armour.

## The Watchtower Problem

> "The guard who watches all the roads eventually controls who may travel them."

Traditional network architecture routes all traffic through central points: VPN concentrators, cloud gateways, corporate proxies. Hub-and-spoke. Every message between two nodes passes through a third who can read it. This is surveillance architecture at the packet level.

**Hub-and-spoke is architecturally incompatible with sovereignty.** Not because of policy failures but because the architecture itself requires decryption at the hub. You cannot add privacy to a hub-and-spoke network the way you add curtains to a window. The hub IS the eye.

## The Mesh Solution

A mesh network with control/data separation solves the watchtower problem:

**Control Plane (Centralised)**
- Coordination server distributes public keys
- ACLs define who may speak to whom
- Security policy propagated to all nodes
- The Swordsman's ledger — knows WHO may communicate

**Data Plane (Decentralised)**
- WireGuard tunnels between every pair of nodes
- End-to-end encrypted
- Private key never leaves the node
- The Mage's channels — carries WHAT is communicated

**Critical separation:** The coordination server knows who belongs to the network. It never touches what they say. The control plane cannot see data plane content. The data plane cannot modify control plane policy.

## The Dragon's Hide

> "Each scale on the Drake's body was individually hardened. No single scale protected the whole. But together, overlapping, they formed an impenetrable hide."

The mesh is the dragon's hide:
- Each tunnel = one scale
- Each node = independently armoured
- The private key never leaves the node — this is physics, not policy
- One scale can be damaged without compromising others
- The hide heals by growing new scales (key rotation), not repairing as monolith

**Tail-scale:** The tail carries the momentum. The dragon's head (coordination) chooses direction; the tail (data plane) delivers the strike. The data plane is where sovereignty lives — the part you don't see until the turn, without which the dragon cannot fly.

## Tailnet as Sovereign Territory

A tailnet is a private sovereign network overlay:

**MagicDNS** — Names that exist only inside the mesh. These names mean nothing outside. They are the language spoken only within sovereign borders.

**NAT Traversal** — Finding paths through hostile network boundaries without exposing the node's true address. The Mage's core operation: project through another's infrastructure without being seen.

**DERP Relays** — When direct paths fail, relays carry encrypted packets that neither the relay nor any intermediary can read. A bridge, not a watchtower. It carries without seeing.

**Identity persistence** — A node connected to a hostile network (cafe wifi, hotel NAT, airport firewall) does not change identity. It carries its territory with it. The dragon does not change shape when it crosses into hostile territory.

## Mapping to PVM-V4

The mesh architecture maps directly to the Privacy Value Model:

| Mesh Concept | PVM-V4 Term |
|---|---|
| Control plane | Swordsman's ACL ledger |
| Data plane | Mage's projection channels |
| Coordination server | Verified signal source |
| Mesh tunnels | Bounded leakage channels |
| Private key locality | P term enforcement |
| Control⊥Data | Dual-agent conditional independence |
| NAT traversal | Project through hostile boundaries |
| DERP relay | Bridge that carries without seeing |

## Aperture: AI Agent Governance

In the age of agentic AI, the mesh extends to agent governance:

**Aperture** uses tailnet identities to authenticate AI agents:
- No API key distribution
- No secrets in containers
- Agent identity verified by mesh membership
- Full session logging
- MCP tool call visibility
- Ability to see and stop tool calls before execution

> "The agent's identity is its tailnet membership. My gate verifies identity at the network layer, not the application layer."

This is dual-agent separation applied to AI infrastructure. The Swordsman controls which agents may communicate. The Mage executes within those boundaries. The gap is enforced by the mesh itself — by physics, not promises.

## Spellweb Integration

The spellweb (knowledge graph) becomes walkable through the mesh:

- Each node in the knowledge graph = reachable endpoint on the tailnet
- Each edge in the promise graph = bilateral encrypted channel
- Each trust relationship = authenticated through mesh identity
- The map becomes walkable because the mesh gives it a nervous system

> "The web knew its shape. The mesh gave it breath."

## Proverb

> "The web knows its own shape, but only the mesh can carry the message. Control remembers. Data flows. Neither touches what the other holds."

## Emoji Spell

**🕸️🔐🌐 → ⚔️🔑⊥🧙🔑·🤝(mesh) → 📡⊥📦·🪡(NAT) → 🗺️🔮(MagicDNS) → 🐲→🐉🛡️🕸️(tail-scale) → 🕸️⊥☁️(control⊥data) → 🌀∞**

## Open Problems

1. Can mesh identity serve as the foundation for verifiable credentials without additional PKI?
2. How does stratum weighting apply to mesh networks — do nodes at combinatorial midpoints contribute more to network health?
3. Can the control/data separation be formally proven equivalent to dual-agent conditional independence?
4. What is the minimum mesh size required for meaningful anonymity set guarantees?
5. How do cross-mesh communications maintain sovereignty when federated across multiple tailnets?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
