---
name: agentprivacy-shared-parent-patterns
description: >
  O(1) collective data structures that avoid N-squared coupling for guilds, pools,
  and agent swarms. Activates when discussing shared-parent holon architecture,
  LoadHolonsForParentAsync patterns, guild memory, Intel Pool holons, scalable
  collective intelligence, or any design requiring many-to-one data relationships
  without pairwise links.
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy + OASIS Holonic Architecture"
  author: "Mitchell Travers / Max Gershfield integration"
  affiliation: "0xagentprivacy, BGIN, OASIS"
  status: "integration_draft"
  target_context: "Collective intelligence architects, DAO infrastructure, multi-agent coordination, scaling system designers"
  equation_term: "Network (scaling without coupling), Intel Pool architecture"
  template_references: "architect, shipwright, weaver, assessor, sentinel"
---

# PVM-V4 Skill — Shared-Parent Patterns

**Source:** Privacy Value Model V4 + OASIS Holonic Architecture Whitepaper v1.2
**Target context:** Collective intelligence architects, DAO infrastructure, multi-agent coordination
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The network topology skill covers stratum-weighted graphs. The intel pooling skill covers collective intelligence. But neither specifies the data structure pattern that makes O(1) collective memory possible. Shared-parent patterns fill this gap — the holonic architecture's solution to N² scaling problems.

The problem: N agents want to share state. Pairwise approach: N(N-1)/2 links. With 1,000 agents: 499,500 links. Adding agent 1,001: 1,000 new links. Quadratic scaling kills collective structures.

The solution: shared-parent holon. N children + 1 parent = N+1 holons. Adding agent 1,001: 1 new child holon. Constant-time scaling.

## The shared-parent pattern

**Parent holon.** Represents the collective structure (guild, pool, swarm, coordination group). Contains collective metadata: membership rules, governance policies, access control.

**Child holons.** Represent individual contributions (member state, individual intelligence, per-agent data). Each child has `ParentHolonId` pointing to the parent.

**Query pattern.** `LoadHolonsForParentAsync(parentId, HolonType)` retrieves all children of a given type. The parent defines the collection; children populate it.

**No pairwise links.** Children don't reference each other. They reference the parent. The parent provides the coordination surface without requiring N² relationships.

## Scaling analysis

| Agents | Pairwise Links | Shared-Parent Holons | Savings |
|--------|---------------|---------------------|---------|
| 10 | 45 | 11 | 4x |
| 100 | 4,950 | 101 | 49x |
| 1,000 | 499,500 | 1,001 | 499x |
| 10,000 | 49,995,000 | 10,001 | 4,999x |

The savings grow with scale. For large collectives, pairwise is infeasible; shared-parent is mandatory.

## Intel Pool as shared-parent

Intel Pools are the canonical example:

**Pool parent holon:**
- `HolonType: IntelPool`
- MetaData: pool name, threat domain, membership policy, contribution rules
- Content: aggregate statistics, pool governance, access credentials

**Contribution child holons:**
- `HolonType: ThreatIntel`
- `ParentHolonId: pool_guid`
- MetaData: threat category, confidence, affected protocols, timestamp
- Content: threat details, evidence, recommended mitigations

**Privacy guarantee:** No contributor identity in child holon structure. Attribution via ZK proof of pool membership, not by inspecting holon metadata.

**Operational flow:**
1. Agent detects threat → creates child holon → sets ParentHolonId to pool → saves
2. Other agents query pool → `LoadHolonsForParentAsync(poolId, ThreatIntel)` → receive all contributions
3. Adding contributor 1,001: one new child, zero new links, O(1) operation

## Guild memory as shared-parent

Guilds need collective memory:

**Guild parent holon:**
- `HolonType: GuildMemory`
- MetaData: guild identity, specialisation, membership tier requirements
- Content: guild charter, governance rules, shared resources

**Member contribution holons:**
- `HolonType: GuildContribution`
- Types: ReasoningGraph, VerifiedCircuit, ThreatAnalysis, ProvenPattern
- Each contribution is a child of the guild memory parent

**Governance integration:** Shipwright persona governs who can create children, who can query, who can modify the parent. The shared-parent structure enables governance without N² permission matrices.

## Agent swarm coordination

Multi-agent systems need coordination state:

**Swarm parent holon:**
- `HolonType: SwarmCoordination`
- MetaData: swarm task, coordination protocol, membership
- Content: task specification, current state, completion criteria

**Agent state holons:**
- `HolonType: AgentState`
- Each agent maintains their state as a child of the swarm
- State updates: modify own child holon
- Coordination: read sibling holons via parent query

**Scaling benefit:** A 100-agent swarm has 101 holons. Adding 10 agents adds 10 holons. No explosion of coordination links.

## Hierarchical shared-parents

Shared-parent patterns compose hierarchically:

```
Organisation Parent
├── Guild A Parent
│   ├── Member 1 Contribution
│   ├── Member 2 Contribution
│   └── ...
├── Guild B Parent
│   ├── Member 1 Contribution
│   └── ...
└── Intel Pool Parent
    ├── Contribution 1
    └── ...
```

**Query patterns:**
- All guilds: `LoadHolonsForParentAsync(orgId, Guild)`
- All contributions in Guild A: `LoadHolonsForParentAsync(guildAId, Contribution)`
- All intel: `LoadHolonsForParentAsync(poolId, ThreatIntel)`

**Governance inheritance:** Policies flow down the hierarchy. Organisation-level rules constrain guild-level rules which constrain member contributions.

## Privacy in shared-parent structures

Shared-parent enables collective intelligence without surveillance:

**Child anonymity.** Children don't contain contributor identity. The contribution exists; its author is protected.

**Access control at parent.** The parent holon's MetaData specifies who can query children. Non-members can't enumerate the collective's contents.

**Aggregate-only queries.** Some parent configurations allow aggregate queries (count, statistics) without exposing individual children. "How many threat reports?" without "which agents contributed?"

**Contribution mixing.** New children can be added through a mixer — the parent accepts contributions without linking them to specific agents.

## Integration with existing skills

**network_topology:** Stratum-weighted graphs describe network structure. Shared-parent patterns describe data structure. Complementary: the network topology operates over shared-parent data.

**intel_pooling:** Intel Pools ARE shared-parent structures. This skill specifies the implementation pattern.

**plurality_cooperative:** Quadratic funding, plural voting require aggregating many individual preferences. Shared-parent patterns are the data structure for plurality mechanisms.

**hitchhiker_governance:** Heart of Gold governance operates over shared-parent structures. Governance decisions affect parent holon policies; members contribute through children.

**data_dignity:** Data as the 7th capital. Your data (your child holons) lives in collective structures (shared parents) without surrendering ownership. The shared-parent pattern enables collective benefit with individual sovereignty.

**sovereignty_economics:** Economic value from collective structures. Shared-parent patterns make collective value possible at scale without N² coordination costs.

## Operational patterns

**Adding a member.** Create child holon with ParentHolonId → member is now part of collective → no existing holons modified → O(1).

**Removing a member.** Delete or archive member's child holons → member no longer in queries → parent unchanged → O(1).

**Querying collective.** `LoadHolonsForParentAsync()` → all current children → O(N) read, but no N² storage.

**Governance update.** Modify parent holon → new policies apply to all children → O(1) governance propagation.

## Open problems

1. **Child ordering** — do children have an order? How to paginate `LoadHolonsForParentAsync` results?
2. **Parent update rights** — who can modify the parent? How is this governed?
3. **Cross-parent queries** — querying across multiple parent structures? Joins without N² explosion?
4. **Orphan children** — what happens if a parent is deleted? Children become unreachable?
5. **Migration between parents** — can a child change parents? What are the semantics?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
