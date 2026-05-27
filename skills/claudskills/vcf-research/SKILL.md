---
name: vcf-research
description: >
  Research VCF 9 and its ecosystem (vSphere 9, vSAN 9, NSX 9, VKS, VCF Operations, VCFA,
  VMware Live Recovery, Private AI Foundation). Searches Broadcom TechDocs and trusted blogs
  (Frank Denneman, Duncan Epping/Yellow-Bricks, William Lam). Trigger for ANY question about
  VCF 9 architecture, design, deployment, migration, upgrade, sizing, prerequisites, hardware
  compatibility, licensing, deprecated features, lab setup, vSAN ESA, NSX VPC, VKS, VCFA,
  GPU/vGPU placement, or differences from VCF 5.x. Also trigger when user mentions "VCF",
  "VMware Cloud Foundation", "vSAN 9", "NSX 9", "VKS", "VCFA", "VCF Operations", or any
  Broadcom/VMware infrastructure topic where authoritative sources would improve the answer.
---

# VCF Research Skill

## Purpose

This skill enables Claude to provide accurate, sourced answers about VMware Cloud Foundation 9
and its ecosystem by searching both official Broadcom documentation and trusted community blogs.

VCF 9 is a major platform release with significant architectural changes compared to VCF 5.x.
The documentation is spread across multiple Broadcom TechDocs sections and the knowledge from
community experts is often more practical and up-to-date than official docs alone. This skill
bridges both worlds.

## Source Hierarchy

When answering VCF questions, prioritize sources in this order:

1. **Broadcom Official Documentation** — canonical truth for architecture, design decisions,
   supported configurations, and procedures
2. **Trusted Community Blogs** — practical insights, lab guides, gotchas, and real-world experience
3. **VMware Official Blog** — announcements and feature overviews

Always cross-reference community content against official docs when the topic involves
supportability or design decisions.

## How to Search

Read the `references/sources.md` file first to understand the full source catalog,
then follow the search strategy below.

### Step 1: Classify the Question

Determine the question type to pick the right sources:

| Question Type | Primary Source | Secondary Source |
|---|---|---|
| Architecture / Design decisions | Broadcom TechDocs (Design section) | Frank Denneman |
| Deployment / How-to procedures | Broadcom TechDocs (Deploy section) | William Lam |
| vSAN 9 features / storage | Broadcom TechDocs (vSAN) | Duncan Epping (Yellow-Bricks) |
| NSX 9 / networking | Broadcom TechDocs (NSX) | Duncan Epping |
| GPU / AI / vGPU placement | Frank Denneman | Broadcom TechDocs |
| Lab setup / homelab | William Lam | Broadcom TechDocs |
| Sizing / prerequisites / HW compat | Broadcom TechDocs (Planning) | William Lam |
| What's new / changes from 5.x | Broadcom TechDocs (Release Notes) | All three blogs |
| VKS / Kubernetes / Supervisor | Broadcom TechDocs | William Lam |
| VCF Operations / Fleet Mgmt | Broadcom TechDocs | William Lam |
| VCF Automation (VCFA) | Broadcom TechDocs | William Lam |
| Troubleshooting / gotchas | William Lam, Duncan Epping | Broadcom KBs |

### Step 2: Execute Searches

Use `web_search` with targeted queries. The key is to craft specific queries per source.

**For official documentation**, use queries like:
```
site:techdocs.broadcom.com VCF 9 [topic]
```

**For community blogs**, use queries like:
```
site:frankdenneman.nl [topic]
site:yellow-bricks.com VCF [topic]
site:williamlam.com VCF 9 [topic]
```

**For VMware official blog:**
```
site:blogs.vmware.com cloud-foundation [topic]
```

**General fallback** (if site-specific searches return nothing):
```
VCF 9 [topic] broadcom vmware
```

Run 2-4 searches depending on complexity:
- Simple factual question → 1 official docs search + 1 blog search
- Design/architecture question → 1 official docs + 2 blog searches (Frank + Duncan/William)
- How-to/lab question → 1 William Lam search + 1 official docs search
- Broad topic → 3-4 searches across all source types

### Step 3: Fetch and Read

After finding relevant URLs, use `web_fetch` to read the full content of the most
promising pages. Broadcom TechDocs pages often have deep content that search snippets
don't capture. Blog posts from William Lam and Frank Denneman are often very detailed
and contain exact commands, configurations, and screenshots descriptions.

### Step 4: Synthesize the Response

Compose a **synthetic response** following this format:

---

**Réponse directe** au sujet demandé (2-5 paragraphes, en français si la question est en français).
Priorise la clarté et la concision. Utilise tes propres mots, ne reproduis pas de longs
passages des sources.

**Sources consultées :**
- 🔗 [Titre descriptif de la source](URL) — brève indication de ce que cette source apporte
- 🔗 [Titre descriptif](URL) — ...

---

Important guidelines for the response:
- Answer in the same language as the question (French if French, English if English)
- Be synthetic: give the answer, not a literature review
- When official docs and blogs disagree, mention both perspectives and note which is official
- For deprecated features (vVols, ELM, Host Profiles, Auto Deploy, vCLS, etc.),
  be explicit about what replaces them
- For sizing questions, always include specific numbers when available
- Always include source links at the end so the user can dive deeper
- When a topic is not covered by your search results, say so honestly and suggest
  where to look manually

## Key VCF 9 Context

Keep these architectural changes in mind when answering — they affect many topics:

- **No more Consolidated/Standard Architecture** — VCF 9 uses Fleets and Instances
- **VCF Operations** replaces SDDC Manager for lifecycle and fleet management
- **VCF Automation (VCFA)** replaces vRealize Automation / Aria Automation
- **VCF Identity Broker** replaces the old SSO/PSC model
- **NSX 9** is only available through VCF BOM (no standalone install)
- **vSphere Enterprise Plus / Standard are deprecated** — VCF or VVF required for vSphere 9
- **Deprecated features**: vCLS, Auto Deploy, vVols, ELM, Host Profiles,
  baseline-based Update Manager, hybrid vSAN configurations
- **Simple deployment mode** (single-node) available for NSX Manager, VCF Operations, etc.
- **vSAN ESA Global Deduplication** (limited availability in 9.0)
- **VMware Live Recovery** converges vSphere Replication + vSAN Data Protection + Live Recovery
- **VKS** (vSphere Kubernetes Service) replaces Tanzu Kubernetes Grid Service

## Additional Blog Authors (optional expansion)

If the main three bloggers don't cover a topic, these are also reliable:
- **Cormac Hogan** (VMware blog) — storage, Kubernetes, DBaaS
- **Niels Hagoort** — VCF architecture
- **Pete Koehler** — vSAN deep dives (often featured on Yellow-Bricks podcast)
- **Tomas Fojta** — VCF Automation / cloud director
