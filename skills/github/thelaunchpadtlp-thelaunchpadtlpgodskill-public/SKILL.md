---
name: universal-creation-framework
version: 1.0.0
description: >
  Activates for ANY project involving research, design, development, or creation across
  all domains and all AI platforms. Routes to the appropriate domain workflow (software,
  physical-creative, hybrid, media, business, events, or scientific) and manages the full
  lifecycle from discovery through deployment and iteration. Use this skill when starting
  any new project, when unclear which workflow to follow, or when a project spans multiple
  domains. Compatible with: Manus, Claude, Claude Code, OpenAI Codex, ChatGPT, Gemini,
  Gemini Code Assist, Google Stitch, Google Jules, Google Firebase Studio, Google Vertex AI,
  Google AI Edge, Google Antigravity, Perplexity, Cursor, Windsurf, VS Code Copilot,
  JetBrains AI, and any MCP-compatible agent.
author: Universal Creation Framework Initiative
license: MIT
tags: [universal, creation, development, research, design, planning, all-domains, all-platforms]
---

# Universal Creation Framework — Mega-Skill

> **The meta-pattern beneath all creation:** Diverge then converge. Commit resources
> progressively as uncertainty decreases. Validate through prototyping before full
> commitment. Separate the act of creation from the act of evaluation. This framework
> codifies that meta-pattern into a machine-readable format any AI platform can execute.

---

## 0. How to Use This Skill

This skill operates as a **universal entry point** for any creative or technical project.
It does not replace domain expertise — it orchestrates it. The framework:

1. **Classifies** your project type using the decision tree in Section 1.
2. **Routes** to the appropriate domain workflow (Section 3).
3. **Enforces** six universal phases with explicit quality gates (Section 2).
4. **Adapts** depth and formality based on scale, risk, and complexity (Section 1.2).
5. **Leverages** platform-specific capabilities through thin adapter guidance (Section 5).

**Platform invocation:**
- Claude / Claude Code: Place this file in `.claude/skills/universal-creation-framework/SKILL.md`
- OpenAI Codex: Place in `.agents/skills/universal-creation-framework/SKILL.md`
- Manus: Paste the relevant section as a natural-language task description
- ChatGPT: Use as a Custom GPT system prompt or upload as a knowledge file
- Gemini / Firebase Studio: Reference as `airules.md` or project instructions
- Any platform: Copy the relevant phase and domain section into your system prompt

---

## 1. Project Classifier — Entry Point

### 1.1 Primary Classification (What is the primary output?)

Answer the first applicable question to determine your domain:

| Question | If YES → Domain |
|---|---|
| Is the primary output **running software** (app, API, OS, platform, tool)? | `SOFTWARE` |
| Is the primary output a **physical object** (product, building, garment, artwork)? | `PHYSICAL-CREATIVE` |
| Does the project require **both physical AND digital** outputs? | `HYBRID` |
| Is the primary output **content or media** (video, podcast, book, article, course)? | `MEDIA` |
| Is the primary output a **business system, brand, or service**? | `BUSINESS` |
| Is the primary output **scientific knowledge** (research, study, protocol, paper)? | `SCIENTIFIC` |
| Is the primary output an **event, experience, or personal project**? | `EVENTS` |

### 1.2 Secondary Classification (How deep should we go?)

Evaluate three dimensions to determine workflow depth:

**Scale:**
- `PERSONAL` — Solo creator, no formal governance needed
- `TEAM` — 2–20 people, lightweight coordination required
- `ENTERPRISE` — 20+ people or external stakeholders, full governance required

**Risk:**
- `EXPERIMENTAL` — Failure is acceptable and informative
- `LOW` — Failure has minor consequences
- `MEDIUM` — Failure has significant but recoverable consequences
- `HIGH` — Failure has major financial, reputational, or safety consequences
- `SAFETY-CRITICAL` — Failure could harm people (medical, aerospace, infrastructure)

**Complexity:**
- `LIGHT` — Single-phase or single-deliverable work (birthday party, simple blog post)
- `STANDARD` — Multi-phase work with clear dependencies (mobile app, marketing campaign)
- `DEEP` — Multi-team, multi-year, or multi-domain work (operating system, new medicine)

**Depth matrix:**

| Scale + Risk + Complexity | Workflow Mode |
|---|---|
| Personal + Experimental/Low + Light | **Express** — abbreviated phases, plain language, minimal gates |
| Team + Low/Medium + Standard | **Standard** — full phases, structured gates, moderate documentation |
| Enterprise + Medium/High + Deep | **Rigorous** — formal reviews, comprehensive QA, full documentation |
| Any + Safety-Critical + Any | **Safety** — mandatory external review, FMEA, regulatory compliance |

---

## 2. The Six Universal Phases

Every project — from a birthday party to an operating system — follows this structure.
Depth and formality adapt; the structure does not.

---

### Phase 1 — Discovery & Research

**Purpose:** Understand the problem space before committing to a solution.

**Universal activities:**
- Define the problem statement in one sentence
- Identify the primary stakeholders and their needs
- Survey the existing landscape (competitors, precedents, prior art)
- Surface key constraints (time, budget, technology, regulation, physics)
- Assess initial feasibility
- Document what success looks like

**Domain adaptations:**
- Software: Requirements gathering, user research, technical landscape survey
- Physical-Creative: Reference research, cultural/historical context, material feasibility
- Media: Audience analysis, competitive content audit, platform research
- Scientific: Literature review (use Elicit, Semantic Scholar, PubMed), hypothesis formulation
- Business: Market analysis, customer discovery, competitive intelligence
- Events: Vision definition, venue research, stakeholder alignment

**Recommended tools by platform:**
- Perplexity Deep Research (138M+ papers via Elicit integration)
- Claude with web search for competitive analysis
- Google Scholar, PubMed, ChEMBL for scientific domains
- SimilarWeb, SEMrush for market/content research

**Gate 1 — Go/Hold/Kill decision:**

| Criterion | Required for GO |
|---|---|
| Problem statement | Defined in ≤2 sentences |
| Evidence of viability | At least 3 supporting data points |
| Initial feasibility | No blocking constraints identified |
| Key constraints | Documented |
| Stakeholder alignment | Primary stakeholder has reviewed |

---

### Phase 2 — Scoping & Planning

**Purpose:** Define exactly what will be built, how, by whom, and when.

> **Critical principle:** Planning should consume approximately **60–75% of total effort**
> for optimal outcomes. Premature execution is the single most common cause of project
> failure in AI-assisted work. (Source: Addy Osmani's AI-assisted development research)

**Universal activities:**
- Define scope boundaries (what is IN and explicitly what is OUT)
- Create a work breakdown structure (WBS) with dependencies
- Estimate resources: time, compute, cost, people
- Select the technology/methodology stack
- Identify and document risks with mitigations
- Define "done" criteria for each deliverable
- Establish communication and review cadence
- Create the project timeline with milestones

**Domain adaptations:**
- Software: Architecture decision records (ADRs), API contracts, data models, security threat model
- Physical-Creative: Material specifications, production timeline, supplier research, safety review
- Hybrid: Synchronization checkpoints where physical and digital streams must align; note that **physical components cannot be patched after manufacturing** — lock physical decisions earlier
- Scientific: Experimental design, statistical power analysis, IRB/ethics review if human subjects
- Business: Business model canvas, financial projections, go-to-market strategy, legal structure
- Events: Budget breakdown, vendor contracts, contingency plans, run-of-show document

**Gate 2 criteria:**

| Criterion | Required for GO |
|---|---|
| Scope document | Written and approved |
| Architecture/design direction | Chosen with rationale |
| Resource plan | In place with contingency |
| Risk register | Populated with mitigations |
| "Done" definition | Explicit for each deliverable |
| Timeline | Created with milestones |

---

### Phase 3 — Design & Prototyping

**Purpose:** Create tangible proof-of-concept before full resource commitment.

**Universal principle:** Never commit full resources to an unvalidated concept.
A prototype that fails is a success — it saved you from building the wrong thing.

**Universal activities:**
- Create the lowest-fidelity prototype that can answer your riskiest question
- Test the prototype against Gate 3 criteria
- Iterate until the concept is validated
- Document design decisions and rationale
- Obtain stakeholder approval before proceeding

**Domain adaptations:**
- Software: Wireframes → clickable prototype → technical spike → MVP; use Stitch for UI-to-code
- Physical-Creative: Sketches → mood boards → material samples → scale model → pilot piece
- Media: Outline → script → storyboard → pilot episode or sample chapter
- Scientific: Protocol draft → pilot study → statistical validation → peer pre-review
- Business: Business model canvas → landing page test → customer interviews → financial model
- Events: Venue walkthrough → vendor quotes → mock run-of-show

**Recommended tools:**
- Google Stitch: Text/image to high-fidelity UI in minutes
- Figma + Claude: Design system generation
- Claude Artifacts: Interactive HTML/React prototypes
- Manus: End-to-end prototype generation from description

**Gate 3 criteria:**

| Criterion | Required for GO |
|---|---|
| Prototype exists | Tangible, testable artifact created |
| Riskiest assumption tested | Evidence gathered |
| Feasibility confirmed | Within constraints |
| Stakeholder approval | Obtained |
| Technical risks | Retired or mitigated |

---

### Phase 4 — Production & Development

**Purpose:** Full-scale creation with iterative cycles and quality checkpoints.

**Universal principle:** Work in manageable units with clear dependencies.
Follow the universal "prototype → test → iterate" loop at every scale.

**Universal activities:**
- Break work into units of ≤2 weeks (sprints, chapters, episodes, batches)
- Implement with continuous integration of feedback
- Conduct milestone reviews at each unit boundary
- Track progress against the plan; escalate deviations early
- Maintain a living artifact tracker (decisions, blockers, progress)
- Enforce mandatory human checkpoints after every 3–4 AI iterations

**Domain adaptations:**
- Software: Sprint-based development, TDD, code review, CI/CD pipeline; use Claude Code or Codex for implementation, Jules for async bug fixes
- Physical-Creative: Asset production with periodic review; separate AI-as-ideation from AI-as-production; note AI images lack individual layers (use masking workflows); upscale for print resolution
- Media: Asset production → rough cut/draft → review → polish; multi-format adaptation from single source
- Scientific: Data collection → analysis → interpretation → manuscript; enforce reproducibility documentation
- Business: Build → measure → learn cycles; CRM configuration, brand asset production
- Events: Vendor coordination, logistics execution, rehearsals

**Context engineering for long production phases:**
- Use **compaction** when context window approaches limit (summarize + reinitiate)
- Use **structured note-taking** (NOTES.md or artifact-tracker) for persistent state
- Use **sub-agent delegation** for deep exploration tasks (each sub-agent returns 1,000–2,000 token summary)
- Enforce **just-in-time retrieval** — maintain file paths and queries, not full content in context

**Gate 4 criteria:**

| Criterion | Required for GO |
|---|---|
| Milestone reviews | All passed |
| Quality checkpoints | Met per domain QA standards |
| Scope adherence | Within approved boundaries |
| Artifact tracker | Up to date |
| Human review | Completed at each 3–4 AI iteration threshold |

---

### Phase 5 — Testing & Validation

**Purpose:** Domain-appropriate quality assurance before release.

**Four-layer QA architecture:**

**Layer 1 — Deterministic validation (run first, no AI tokens consumed):**
- Software: Compile, lint, type-check, unit tests, integration tests, security scan, accessibility audit
- Content: Plagiarism check, readability score, fact extraction, brand compliance
- Design: WCAG compliance, responsive layout verification, print resolution check
- Science: Statistical tests, data integrity checks, reproducibility verification
- Physical: Dimensional tolerance check, material compatibility, safety compliance

**Layer 2 — AI-as-judge evaluation (semantic quality):**
Score each output 1–5 on these seven dimensions:
1. **Accuracy/Faithfulness** — Does it correctly represent facts and sources?
2. **Relevance** — Does it address the actual need?
3. **Completeness** — Are all required elements present?
4. **Coherence** — Is it internally consistent and logically structured?
5. **Originality** — Does it add genuine value beyond recombination?
6. **Bias/Fairness** — Are perspectives balanced and assumptions examined?
7. **Actionability** — Can the intended audience act on this?

Minimum acceptable score: 4/5 on Accuracy, 3/5 on all others.

**Layer 3 — Human review at gates (ConSiDERS framework):**
- **C**onsistency: Same criteria applied across all outputs
- **S**coring criteria: Explicit rubric shared with reviewers
- **D**ifferentiating: Rubric distinguishes good from excellent
- **E**thical considerations: Bias, privacy, safety reviewed
- **R**eproducibility: Another reviewer would reach same conclusion
- **S**calability: Review process can handle volume

**Layer 4 — Continuous monitoring (post-launch):**
- Track drift, performance degradation, and anomalies
- Mandatory human review after 3–4 AI iterations without intervention
- Domain-specific: A/B testing for software/media, citation provenance for science, brand compliance for business

**Gate 5 criteria:**

| Criterion | Required for GO |
|---|---|
| Layer 1 validation | All checks pass |
| Layer 2 AI scoring | Meets minimum thresholds |
| Layer 3 human review | Completed per ConSiDERS |
| User acceptance | Validated with target users |
| Compliance | All regulatory requirements met |
| Blocking defects | Zero |

---

### Phase 6 — Launch & Iteration

**Purpose:** Release, monitor, and feed learnings back into the system.

**Universal activities:**
- Execute the launch/release/publication/deployment plan
- Activate monitoring and feedback collection
- Conduct post-launch retrospective (within 2 weeks)
- Prioritize iteration backlog based on observed outcomes
- **Update this SKILL.md based on observed failures** — treat skills as living code

**Domain adaptations:**
- Software: Phased rollout, feature flags, error monitoring, performance dashboards
- Physical-Creative: Exhibition, publication, distribution; document production notes for future runs
- Media: Multi-platform distribution, SEO optimization, analytics tracking, audience feedback
- Scientific: Peer review submission, preprint posting, data/code release, replication invitation
- Business: Go-to-market execution, PR/communications, customer onboarding, KPI tracking
- Events: Day-of execution, post-event survey, vendor debrief, documentation for next edition

**Skill improvement protocol (after every project):**
1. List every instruction in this SKILL.md that the AI followed correctly without being told
2. Remove those instructions (the model no longer needs them)
3. List every failure mode observed
4. Add specific instructions to prevent those failures
5. Test the updated skill with a fresh AI instance before deploying

**Gate 6 criteria:**

| Criterion | Required for CLOSE |
|---|---|
| Launch checklist | Complete |
| Monitoring | Active |
| Stakeholder sign-off | Obtained |
| Retrospective | Completed |
| Iteration backlog | Prioritized |
| Skill updated | Based on retrospective findings |

---

## 3. Domain Skill Modules

### 3.1 SOFTWARE — Apps, APIs, Platforms, Operating Systems, Tools

**When to use:** Primary output is running code. Includes: mobile apps, web apps, APIs, CLIs, operating systems, compilers, databases, developer tools, AI agents, automation workflows.

**Phase adaptations:**
- Phase 1: User stories, technical landscape, security threat model
- Phase 2: Architecture Decision Records (ADRs), API contracts, data models, test strategy
- Phase 3: Wireframes → technical spike → MVP; validate with real users
- Phase 4: TDD, code review, CI/CD, sprint ceremonies
- Phase 5: Automated test suite, security scan, performance benchmarks, accessibility audit
- Phase 6: Phased rollout, feature flags, SLOs, runbook

**Quality criteria:**
- All tests passing (unit, integration, e2e)
- No critical/high security vulnerabilities (OWASP Top 10)
- Code review approval from qualified reviewer
- Performance benchmarks met (define specific thresholds)
- Accessibility: WCAG 2.1 AA minimum
- Documentation: README, API docs, architecture diagram

**Recommended tools:**
- Implementation: Claude Code, OpenAI Codex, Cursor, Windsurf
- Async tasks: Google Jules (up to 60 concurrent on Ultra tier)
- Research: Perplexity for technology decisions
- Design: Google Stitch for UI generation
- Backend: Firebase Studio, Google Cloud Run
- Testing: Claude Code for test generation, Jules for bug fixes

**Anti-patterns:**
- Starting implementation before architecture is documented
- Skipping the test strategy in Phase 2
- Using AI to generate tests without reviewing them
- Deploying without monitoring in place
- Treating AI-generated code as reviewed code

**Common deliverables by phase:**
1. PRD, user stories, technical landscape doc
2. Architecture diagram, ADRs, data model, API spec, test plan
3. Wireframes, technical spike, MVP
4. Working software with tests, CI/CD pipeline
5. Test report, security audit, performance report
6. Deployed application, runbook, monitoring dashboard

---

### 3.2 PHYSICAL-CREATIVE — Art, Architecture, Products, Fashion, Industrial Design

**When to use:** Primary output is a physical object or experience. Includes: paintings, sculptures, buildings, furniture, clothing, jewelry, vehicles, consumer products, packaging.

**Critical asymmetry:** Physical components cannot be "patched" after production. Lock physical design decisions earlier than digital ones. Material selection, structural decisions, and manufacturing tolerances must be finalized before production begins.

**Phase adaptations:**
- Phase 1: Reference research (historical, cultural, material), mood boards, constraint mapping
- Phase 2: Material specifications, production timeline, supplier research, safety/regulatory review
- Phase 3: Sketches → CAD/technical drawings → material samples → scale model → pilot piece
- Phase 4: Production with periodic quality checks; separate AI-as-ideation from AI-as-production
- Phase 5: Dimensional tolerance, material compatibility, safety compliance, user testing
- Phase 6: Exhibition/distribution, documentation, production notes for future runs

**AI-specific notes:**
- AI-generated images lack individual layers — use masking workflows for production
- Upscale to minimum 300 DPI for print production
- Use AI for ideation and reference generation, not final production files
- Physical safety standards vary by domain — always verify with domain expert

**Quality criteria:**
- Dimensional tolerances within specification
- Material compatibility verified
- Safety compliance documented
- Prototype user-tested
- Production documentation complete

---

### 3.3 HYBRID — Physical + Digital Products

**When to use:** Project requires both physical and digital deliverables that must work together. Includes: board games with apps, illustrated books with AR, smart home devices, wearables, interactive installations.

**Critical principle:** Establish explicit synchronization checkpoints where physical and digital streams must align. Physical decisions must be locked before digital work that depends on them can proceed.

**Synchronization checkpoints:**
- After Phase 2: Physical specs locked → digital team can begin dependent work
- After Phase 3: Physical prototype validated → digital prototype can reference real dimensions
- After Phase 4: Physical production complete → digital integration testing can begin
- After Phase 5: Both streams validated → combined user testing

**Anti-patterns:**
- Letting digital work proceed on assumptions about physical specs
- Discovering physical/digital incompatibility in Phase 5
- Not documenting which decisions are physical-locked vs. digital-flexible

---

### 3.4 MEDIA — Content, Video, Podcast, Books, Courses, Social

**When to use:** Primary output is content consumed by an audience. Includes: YouTube videos, podcasts, books, articles, courses, social media campaigns, newsletters, films, music.

**Unique capability:** Multi-format adaptation from single source content. One well-structured piece of content can become: long-form article, video script, social posts, newsletter, podcast outline, slide deck.

**Platform-specific formatting rules:**
- YouTube: SEO-optimized title/description, chapters at 10-min intervals, thumbnail A/B test
- TikTok/Reels: Hook within first 3 seconds, vertical format, captions mandatory
- Instagram: Carousel for depth, single image for emotion, hashtag strategy (5–10 relevant)
- Podcast: RSS-ready, transcription for SEO, show notes with timestamps
- Newsletter: Subject line A/B test, preview text optimization, plain-text fallback
- LinkedIn: Professional tone, data-backed claims, engagement question at end

**Quality criteria:**
- Readability score appropriate for target audience
- Fact claims verified with sources
- Brand voice consistency score ≥ 4/5
- Platform format requirements met
- Engagement metrics baseline established

---

### 3.5 SCIENTIFIC — Research, Engineering, Medicine, Technology Standards

**When to use:** Primary output is new knowledge, validated protocols, or technology standards. Includes: academic papers, clinical trials, engineering specifications, coding language design, protocol standards.

**Epistemic rigor requirements:**
- Distinguish AI prediction from AI understanding in all outputs
- Require provenance tracking for all factual claims
- Mandate reproducibility documentation
- Never present AI-generated hypotheses as validated findings

**Phase adaptations:**
- Phase 1: Literature review via Elicit (138M+ papers), hypothesis formulation, gap analysis
- Phase 2: Experimental design, statistical power analysis, IRB/ethics review, pre-registration
- Phase 3: Pilot study, protocol validation, instrument calibration
- Phase 4: Data collection, analysis, interpretation; enforce lab notebook discipline
- Phase 5: Statistical validation, peer pre-review, reproducibility check, citation audit
- Phase 6: Peer review submission, preprint, data/code release, replication invitation

**Quality criteria:**
- All claims traceable to primary sources
- Statistical methods appropriate and pre-specified
- Reproducibility package (data + code + environment) complete
- Peer pre-review completed
- Conflicts of interest disclosed

---

### 3.6 BUSINESS — Ventures, Brands, Services, Operations

**When to use:** Primary output is a business system, brand identity, or service design. Includes: startups, brand development, service design, marketing systems, operational workflows, SaaS platforms.

**Phase adaptations:**
- Phase 1: Market analysis, customer discovery, competitive intelligence, regulatory landscape
- Phase 2: Business model canvas, financial projections, legal structure, go-to-market strategy
- Phase 3: Landing page test, customer interviews, financial model validation, brand prototype
- Phase 4: Build → measure → learn cycles; CRM configuration, brand asset production
- Phase 5: Market validation, financial model stress test, brand compliance audit
- Phase 6: Go-to-market execution, PR/communications, customer onboarding, KPI tracking

**Quality criteria:**
- Business model validated with real customer conversations
- Financial model stress-tested with pessimistic scenarios
- Legal structure reviewed by qualified counsel
- Brand identity consistent across all touchpoints
- Data privacy compliance documented (GDPR, CCPA as applicable)

---

### 3.7 EVENTS — Events, Experiences, Personal Projects

**When to use:** Primary output is an event, experience, or personal project. Includes: conferences, weddings, exhibitions, travel, personal development projects.

**Workflow mode:** Express or Standard (rarely Rigorous). Use plain language, template-driven approaches, and simplified gates.

**Phase adaptations:**
- Phase 1: Vision definition, venue research, stakeholder alignment, budget envelope
- Phase 2: Budget breakdown, vendor shortlist, timeline, contingency plans
- Phase 3: Venue walkthrough, vendor quotes, mock run-of-show
- Phase 4: Vendor coordination, logistics execution, rehearsals
- Phase 5: Dress rehearsal, contingency review, day-of checklist
- Phase 6: Day-of execution, post-event survey, vendor debrief

**Human judgment is irreplaceable for:** taste, atmosphere, interpersonal dynamics, and crisis management.

---

## 4. Context Engineering Principles

These principles apply to ALL platforms and ALL domains. They determine how effectively
the AI uses its finite attention budget.

### 4.1 Minimal High-Signal Context

Never load instructions the AI already knows. Each skill encodes only domain-specific
procedural knowledge the model wouldn't know otherwise.

- Project facts → CLAUDE.md / AGENTS.md / project instructions (always loaded)
- Specialized workflows → skills (loaded on demand)
- Reference material → separate files (loaded only when explicitly needed)

### 4.2 Just-in-Time Retrieval

Maintain lightweight identifiers (file paths, search queries, URLs) and use tools to
dynamically load data at runtime. Never front-load all project context.

```
# Good: reference, don't embed
See: ./references/api-spec.yaml
Run: grep -r "authentication" ./src

# Bad: paste entire files into context
[3,000 lines of API spec pasted here]
```

### 4.3 Structured Note-Taking for Long-Horizon Tasks

Maintain a persistent NOTES.md or artifact-tracker outside the context window:

```markdown
# Project State — [Project Name]
Last updated: [date]

## Current phase: [phase name]
## Completed: [list]
## In progress: [list]
## Blocked: [list with blockers]
## Key decisions: [ADRs or equivalent]
## Next actions: [prioritized list]
```

### 4.4 Sub-Agent Delegation

For deep exploration tasks, fork to sub-agents with clean context windows.
Each sub-agent may use tens of thousands of tokens internally but returns
a condensed summary of 1,000–2,000 tokens to the main agent.

### 4.5 Compaction for Long Sessions

When context window approaches limit:
1. Pass message history to model for summarization
2. Preserve: architectural decisions, unresolved issues, implementation details
3. Discard: redundant tool outputs, superseded drafts, raw search results
4. Reinitiate with compressed context + 5 most recently accessed files

### 4.6 The 3–4 Iteration Rule

Research shows diminishing returns and compounding error risk after 3–4 AI iterations
without human intervention. Enforce mandatory human checkpoints at this threshold.

### 4.7 Start Minimal, Add Based on Failures

> "Start by testing a minimal prompt with the best model available to see how it performs
> on your task, and then add clear instructions and examples to improve performance based
> on failure modes found during initial testing." — Anthropic Engineering

Never add instructions preemptively. Add them only when you observe a specific failure.

---

## 5. Platform-Specific Guidance

### 5.1 Claude / Claude Code

**Skill location:** `.claude/skills/universal-creation-framework/SKILL.md`
**Always-loaded context:** `CLAUDE.md` (project conventions)
**Context budget:** First 5,000 tokens per skill within 25,000-token combined budget after compaction
**Unique strengths:** Extended thinking, XML-structured instructions, richest MCP ecosystem, Artifacts for interactive outputs
**Invocation:** Skills auto-activate based on description match; explicit invocation via `/skill-name`
**Best for:** Complex reasoning, nuanced writing, multi-step research, interactive prototypes

```yaml
# CLAUDE.md template for this framework
project: [name]
domain: [SOFTWARE|PHYSICAL|HYBRID|MEDIA|SCIENTIFIC|BUSINESS|EVENTS]
phase: [1-6]
scale: [PERSONAL|TEAM|ENTERPRISE]
risk: [EXPERIMENTAL|LOW|MEDIUM|HIGH|SAFETY-CRITICAL]
complexity: [LIGHT|STANDARD|DEEP]
artifact_tracker: ./NOTES.md
```

### 5.2 OpenAI Codex

**Skill location:** `.agents/skills/universal-creation-framework/SKILL.md`
**Invocation:** Explicit via `$universal-creation-framework` syntax
**Unique strengths:** Cloud-based parallel execution, two-phase sandbox (network during setup, offline during execution), Automations for scheduled work
**Parallel tasks:** Up to 60 concurrent on appropriate tier
**Best for:** Autonomous coding tasks, parallel test generation, scheduled background work

```yaml
# .agents/skills/universal-creation-framework/agents/openai.yaml
name: universal-creation-framework
description: Universal project lifecycle framework for all domains
invocation: explicit
parallel: true
sandbox: isolated
```

### 5.3 Google Ecosystem

**Chain:** Stitch (design) → Firebase Studio / Antigravity (development) → Firebase (backend) → Cloud Run (production)
**Jules:** Async coding tasks via GitHub integration, up to 60 concurrent tasks
**Gemini:** 1M+ token context window enables loading entire codebases
**Stitch adapter:** `.stitch/DESIGN.md` stores design system tokens
**Firebase adapter:** `airules.md` configures Firebase Studio behavior
**Best for:** Full-stack Google Cloud projects, large codebase analysis, parallel async development

### 5.4 ChatGPT / Custom GPTs

**Mapping:** Core instructions → GPT system prompt; domain skills → uploadable knowledge files
**Canvas:** Use for visual code/writing collaboration
**Best for:** Consumer-facing applications, broad accessibility, GPT Store distribution

### 5.5 Manus

**Mapping:** Natural-language task descriptions (no file-based skill system)
**Unique strengths:** Highest-autonomy tier — plans, executes, and delivers end-to-end without intervention
**Best for:** Complete project execution from description, multi-agent orchestration

**Manus task template:**
```
Project: [name]
Domain: [domain]
Phase: [current phase]
Context: [brief project state]
Task: [specific deliverable needed]
Quality criteria: [from Phase N gate]
Constraints: [time, budget, technical]
```

### 5.6 Perplexity

**Role in framework:** Primary research engine for Phase 1 (Discovery)
**Deep Research:** Synthesizes 138M+ papers via Elicit integration
**Best for:** Literature review, competitive analysis, technology research, fact verification

### 5.7 Apple Xcode + Claude Agent SDK

**Integration:** Xcode 26.3+ exposes capabilities via MCP
**Agent SDK phases:** Gather Context → Plan → Execute → Verify (mirrors framework phases)
**Best for:** Native iOS/macOS development with AI assistance

---

## 6. The Interoperability Stack

```
┌─────────────────────────────────────────────────────┐
│                  SKILLS LAYER                        │
│  What to do — domain workflows, phase gates, QA     │
│  (This document + domain sub-skills)                │
├─────────────────────────────────────────────────────┤
│                   MCP LAYER                          │
│  Tool access — GitHub, Figma, Jira, databases,      │
│  cloud services, any API (10,000+ MCP servers)      │
├─────────────────────────────────────────────────────┤
│                   A2A LAYER                          │
│  Agent collaboration — multi-agent orchestration    │
│  Agent Cards at /.well-known/agent.json             │
│  (150+ organizations including Adobe, SAP, SF)      │
└─────────────────────────────────────────────────────┘
```

**Skills + MCP + A2A = Complete stack:**
- Skills define WHAT to do
- MCP provides TOOL ACCESS
- A2A enables AGENT COLLABORATION

---

## 7. Quality Assurance Checklists

### Universal Pre-Launch Checklist

- [ ] All Phase 1–5 gate criteria documented and signed off
- [ ] Layer 1 deterministic validation: all checks pass
- [ ] Layer 2 AI scoring: all dimensions ≥ minimum threshold
- [ ] Layer 3 human review: ConSiDERS framework applied
- [ ] Monitoring/feedback system: active
- [ ] Rollback plan: documented and tested
- [ ] Stakeholder sign-off: obtained
- [ ] Artifact tracker: complete and archived
- [ ] Retrospective: scheduled

### Skill Improvement Checklist (post-project)

- [ ] List instructions followed correctly without being told → remove them
- [ ] List observed failure modes → add specific instructions
- [ ] Test updated skill with fresh AI instance
- [ ] Version the updated skill (git tag)
- [ ] Share improvements with team

---

## 8. Prompt Templates

### Project Kickoff Template

```
I'm starting a new project. Please activate the Universal Creation Framework.

Project name: [name]
One-sentence description: [description]
Primary output type: [software/physical/media/scientific/business/events/hybrid]
Scale: [personal/team/enterprise]
Risk level: [experimental/low/medium/high/safety-critical]
Timeline: [duration]
Key constraints: [list]

Please:
1. Confirm the domain classification
2. Identify the appropriate workflow depth (Express/Standard/Rigorous/Safety)
3. Run Phase 1 — Discovery & Research
4. Present Gate 1 criteria and ask for confirmation before proceeding
```

### Phase Transition Template

```
We are completing Phase [N] of the Universal Creation Framework.

Project: [name]
Domain: [domain]
Current phase output: [brief summary]

Please:
1. Evaluate Gate [N] criteria (list each criterion and status)
2. Identify any criteria not yet met
3. Recommend: GO / HOLD / KILL with rationale
4. If GO: outline Phase [N+1] plan
```

### QA Evaluation Template

```
Please evaluate the following output using the Universal Creation Framework QA system.

Output type: [type]
Domain: [domain]
Output: [paste output or reference file]

Evaluate:
1. Layer 1: List all deterministic checks applicable to this output type
2. Layer 2: Score 1-5 on each of the 7 dimensions with specific evidence
3. Layer 3: Identify what human review is needed per ConSiDERS
4. Overall recommendation: PASS / REVISE / REJECT with specific improvements
```

### Skill Update Template

```
Post-project retrospective for Universal Creation Framework skill update.

Project completed: [name]
Domain: [domain]
Duration: [duration]

Please analyze:
1. Which framework instructions did the AI follow correctly without being told? (candidates for removal)
2. What failure modes were observed? (candidates for new instructions)
3. Which gate criteria were most/least useful?
4. What domain-specific patterns should be added?
5. Draft the specific SKILL.md edits needed
```

---

## 9. Anti-Patterns (Universal)

These failure modes appear across all domains and all platforms:

| Anti-Pattern | Consequence | Prevention |
|---|---|---|
| Premature execution (skipping Phase 2) | Building the wrong thing | Enforce 60-75% planning effort rule |
| Context bloat | Degraded AI performance | Progressive disclosure; just-in-time retrieval |
| No human checkpoints | Compounding errors | Mandatory review after 3-4 AI iterations |
| Vague "done" criteria | Endless scope creep | Define explicit Gate criteria before starting |
| Treating AI output as reviewed output | Quality failures | Layer 1+2+3 QA before any gate transition |
| Single-agent for deep exploration | Context pollution | Sub-agent delegation with summary returns |
| Static skills | Skill obsolescence | Post-project retrospective + skill update |
| Physical/digital sync failure (Hybrid) | Manufacturing defects | Lock physical specs before digital work proceeds |
| Front-loading all context | Attention budget waste | Maintain references, not content, in context |
| Adding instructions preemptively | Brittle prompts | Add only based on observed failures |

---

## 10. Future-Proofing Mechanisms

This framework is designed to evolve. Three mechanisms ensure longevity:

**New domains:** Create a new `SKILL.md` in `domains/` and update the project classifier.
No existing skills need modification. New skills add only ~100 tokens of metadata overhead.

**Platform changes:** Absorbed by the adapter layer (Section 5). When a new AI platform
emerges, add a thin adapter. Core skills remain unchanged.

**Model improvements:** Following Anthropic's guidance — "harnesses should be frequently
questioned as models improve." Run the Skill Improvement Checklist after every project.
Remove instructions the model follows correctly without being told. The framework gets
leaner and more powerful over time.

---

## References

1. Anthropic Engineering. "Effective Context Engineering for AI Agents." Sep 29, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
2. Anthropic. "Claude Skills." https://claude.com/skills
3. Anthropic. "Configuration and Multi-File Skills." https://claude.com/resources/tutorials/configuration-and-multi-file-skills
4. OpenAI. "Codex Best Practices." https://developers.openai.com/codex/learn/best-practices
5. OpenAI. "Codex Skills." https://developers.openai.com/codex/skills
6. Google Labs. "Stitch Skills." https://github.com/google-labs-code/stitch-skills
7. travisvn. "Awesome Claude Skills." https://github.com/travisvn/awesome-claude-skills (11.3k stars)
8. Anthropic. "The Complete Guide to Building Skills for Claude." https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
9. Cooper, R.G. "Stage-Gate® New Product Development Process." Product Development Institute.
10. Osmani, A. "AI-Assisted Development Research." (Planning = 60-75% of effort finding)
11. ACL 2024. "ConSiDERS-The-Human Framework for Human Evaluation."
12. Linux Foundation. "Agentic AI Foundation — MCP and A2A Standards."
13. Google. "Agent-to-Agent (A2A) Protocol v0.3." April 2025.
14. McKinsey. "Rule-based workflow engines outperform letting AI decide 'what comes next'."
