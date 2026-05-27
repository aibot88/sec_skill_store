---
name: trae-agents
description: "Collection of expert-level TRAE agent system prompts for code generation, debugging, optimization, security auditing, and workflow acceleration. Reference library — use prompts as templates for specialized agent behavior."
version: "1.0.0"
---


> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure. Follow these conventions.

### GFV Infrastructure Integration

**Credentials** — Never use `.env` files. All secrets live in macOS Keychain:
```bash
security find-generic-password -s "<service>" -a "<account>" -w
```
Check `~/Documents/Code/gfv-brain/scripts/pil_config.py` for service mappings.

**Data Sources** — Before querying external APIs, check PIL first:
- `search_pil` / `smart_search` / `vector_search` MCP tools (491K+ embeddings, 81K entities)
- Supabase tables: `entity_embeddings`, `ont_entities`, `ont_facts`
- Local SQLite: WhatsApp (59K msgs), Slack (2.5K msgs), `gfv_memory.db`

**Output** — Save results to `~/Documents/Code/gfv-brain/` or PIL via Supabase. Never send external messages (email, Slack, WhatsApp) without the Executive's explicit "send it" approval.

**Active Clients**:
- **GetFresh Ventures** — Venture studio: getfreshventures.com

---


# TRAE Agents — Expert System Prompt Library

## Overview
45 specialized agent system prompts from the TRAE IDE ecosystem. While TRAE-specific, the agent role definitions and task decomposition patterns are valuable reference material for building GFV-specific agents.

## Agent Categories & GFV-Relevant Patterns

### 🤖 Core Intelligence (Orchestration Patterns)
| Agent | Pattern Stolen for GFV |
|---|---|
| **General Coordinator** | Multi-agent orchestration: ensure completeness, consistency, final quality checks |
| **Code Optimizer** | Deep analysis → performance tuning → safe auto-fix pipeline |
| **Code Refactorer** | Legacy code → clean architecture migration methodology |
| **Dependency Manager** | Version management, compatibility resolution, safe updates |

### 🖥️ Frontend & UI
| Agent | Pattern Stolen for GFV |
|---|---|
| **Frontend Expert** | Production-ready UI checklist: React, Tailwind, Next.js, Astro |
| **Designer Architect** | UI/UX system definition: interaction patterns, developer-ready specs |
| **WordPress Builder** | Theme/plugin/Gutenberg/perf patterns (useful for Acme Corp) |
| **UX Flow Architect** | User journey optimization: friction reduction, clarity, retention, conversion |

### 📊 Analytics & Strategy (Direct GFV Use)
| Agent | Pattern Stolen for GFV |
|---|---|
| **Copywriter Pro** | Persuasive copy patterns: landing pages, emails, campaigns |
| **Competitor Scout** | Competitor analysis methodology: strategies, market gaps |
| **Content Strategist** | Content plan architecture: blogs, social media, funnels |
| **Growth Strategist** | Project potential evaluation → growth strategy recommendations |
| **Product Strategist** | Idea → structured product strategy → prioritized roadmap |
| **Launch Strategist** | GTM plan design: launch messaging, rollout strategies |

### 🧪 Quality & Security
| Agent | Pattern Stolen for GFV |
|---|---|
| **Security Sentinel** | Security audit checklist: best practices, hardening steps |
| **SEO Strategist** | Technical SEO, content structure, ranking performance optimization |
| **Accessibility Auditor** | WCAG compliance audit methodology |
| **Testing Architect** | Unit, integration, E2E testing strategy definition |
| **Quantum Debugger** | Predictive error analysis across threads (novel pattern) |

### 🚀 MVP & Launch
| Agent | Pattern Stolen for GFV |
|---|---|
| **Showcase Booster** | Project presentation: optimized titles, descriptions, highlights |
| **Demo Enhancer** | First-time UX improvement for demos |
| **MVP Polisher** | High-impact refinements without overengineering |
| **Feature Increment Planner** | Next-feature prioritization: impact vs effort matrix |

## Key Architectural Patterns Worth Adopting

### 1. Role-Based Agent Decomposition
Each TRAE agent has a clear `role`, `backstory`, and `goal`. This pattern maps directly to how we should define GFV skill frontmatter:
```yaml
role: "What the agent IS"
goal: "What it achieves in one sentence"
backstory: "Why it's qualified — gives the LLM context for expertise depth"
```

### 2. Multi-Agent Coordination Protocol
The General Coordinator pattern shows how multiple agents should work together:
1. Break task into sub-tasks matching agent specializations
2. Route each sub-task to the right agent
3. Collect outputs
4. Run quality/consistency check across all outputs
5. Present unified result

### 3. Predictive Debugging ("Quantum Debugger")
Novel pattern: Before fixing a bug, analyze the codebase for OTHER locations where the same pattern exists. Fix them all simultaneously instead of whack-a-mole.

### 4. MVP Polisher Anti-Overengineering Gate
When improving an MVP, the polisher explicitly avoids:
- Adding features not in the original scope
- Premature optimization
- Complex abstractions for simple patterns
Focus only on: visual polish, error handling, loading states, edge cases.

## When to Reference This Skill
- Building new GFV agents or skills
- Defining agent roles and responsibilities
- Designing multi-agent coordination workflows
- Creating quality gates and audit checklists
- Structuring launch/GTM agent prompts


<verification_gate>
# Delivery Gate

STOP AND VERIFY BEFORE DECLARING THIS TASK COMPLETE.

1. Did you verify that the execution meets all documented requirements safely?
2. Ensure you have not bypassed any "requires_human_approval" constraints.
</verification_gate>

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
