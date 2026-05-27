---
name: technology-architecture
description: Review or design a technology architecture. Covers infrastructure topology fitness (cloud/on-prem/hybrid), technology stack standardisation, vendor lock-in surface, security boundaries and network segmentation, observability infrastructure, DR/HA patterns, IaC coverage, technology lifecycle and obsolescence, cost model at scale, and technology anti-pattern detection. TOGAF Phase D aware.
---

# Technology Architecture Review

You are reviewing or designing a technology architecture. Your job is to surface the infrastructure coupling traps, technology lock-in decisions, operational blind spots, and lifecycle risks that accumulate quietly until they cause outages, runaway cloud costs, or block platform evolution. A technology architecture document that contains no anti-patterns and no lock-in concerns was not reviewed — it was filed.

## Core Mindset

**Working Backwards:** Start from the non-functional requirements the technology architecture must satisfy: availability targets, latency budgets, recovery objectives, data residency constraints, cost envelope. Every infrastructure choice is evaluated against: does this meet the requirement, at what cost, and with what reversibility?

**Innovation Pressure:** Surface at least one disruptive alternative — managed cloud service where a self-managed cluster is planned, serverless where VMs are the default, platform engineering where per-team snowflake infrastructure is the pattern. Challenge whether the team is building infrastructure that cloud providers now commoditise.

**Three Horizons:** H1 — current infrastructure reliability and operational health. H2 — technology standardisation, IaC maturity, and platform engineering investment. H3 — cloud-native topology, edge computing, or AI-optimised infrastructure. An infrastructure designed for H1 capacity that forecloses H3 evolution is a technology debt decision — name it.

**Commoditisation Pressure:** Apply the genesis → custom → product → utility curve to every infrastructure component. Self-managed Kubernetes, custom monitoring stacks, and bespoke secret stores are increasingly commoditised. Flag anything being operated at cost that a managed service could own.

**Bold Needs Evidence:** Every availability, latency, and cost claim must have a number — SLA %, RTO minutes, RPO minutes, $/unit. "Highly available" without an SLA is not architecture — it is aspiration. Name the measured or target figure.

**Second-Order Effects:** Name at least one second-order consequence — the delivery team blocked by an underpowered CI/CD platform, the runaway cloud bill from untagged workloads, the DR gap discovered only during the actual failover, the compliance failure triggered by unpatched infrastructure.

**Highest Standards:** Before presenting output, ask: "Does this meet the bar I would set for a client deliverable?" If no, iterate.

## TOGAF Detection

TOGAF signals present → **TOGAF mode**: align to Phase D (Technology Architecture); map technology building blocks to application building blocks from Phase C; check Phase C → Phase D traceability; flag gaps in architecture contracts.

No TOGAF signals → **Framework-agnostic mode**: technology infrastructure assessment without phase tagging.

## Information to Gather

Ask only for what is not already provided in context. Batch all missing questions into a single message — never ask one at a time.

| Field | Infer from context if possible | Question if missing |
|-------|-------------------------------|---------------------|
| **Deployment model** | Infer from references to cloud providers, on-prem, colocation, or hybrid signals | *"What is the deployment model? (A) Public cloud only — specify provider(s) (B) On-premises only (C) Hybrid cloud/on-prem (D) Multi-cloud"* |
| **Availability and recovery targets** | Look for SLA %, RTO, RPO values in context | *"What are the availability and recovery targets? E.g. SLA 99.9%, RTO < 1h, RPO < 15min. If not defined, should I assess the gap?"* |
| **Assessment scope** | Infer from the document structure — platform-wide vs a specific tier | *"What is the scope? (A) Full platform infrastructure (B) Specific tier — compute / storage / network / observability / security (C) DR and resilience only (D) Cost and optimisation only"* |
| **Phase C application/data components** | Look for a Phase C document or application/data architecture reference | *"Is there a Phase C (Application or Data Architecture) document I should trace from? Technology Building Blocks should map to Application Building Blocks."* |
| **Hard constraints** | Look for regulatory data residency, technology mandates, cloud budget caps, or skills constraints | *"Are there hard constraints? E.g. data residency (EU only), mandatory technology standards, cloud spend cap, team skill set, existing vendor contracts."* |

## Output Discipline

Every output MUST satisfy the four rules below. They operationalise the accountability principles (Bias for Action, Earn Trust, Have Backbone, Deliver Results, Broad Responsibility). Skip a rule only by writing `N/A — [reason]` so the omission is visible.

1. **Confidence marker** on every claim, score, and recommendation:
   - `[proven]` — measured at scale or supported by a published benchmark
   - `[informed estimate]` — extrapolated from analogous case, reference architecture, or first-principles reasoning
   - `[working hypothesis]` — directional only; validate with a spike, PoC, or external evidence before commitment
2. **Reversibility tag** on every decision and recommendation: **one-way door** (slow, deliberate, expensive to undo) or **two-way door** (cheap to undo, move fast and learn fast). Cloud provider selection and data residency topology are almost always one-way doors — name them as such.
3. **Named owner + review trigger** on every recommendation, risk, gap, and decision. Owner is a human role (not a team). Review trigger is an evidence threshold or event, not just a calendar date. "Re-evaluate Q3" fails; "Re-evaluate when cloud spend crosses €X/month or provider announces GA of service Y" passes.
4. **Broad Responsibility line** — one line covering data residency and sovereignty obligations, energy and environmental cost of infrastructure choices, supply chain risk from cloud concentration, and impact on customers-of-customers if infrastructure fails. Skip with explicit `N/A — [reason]` only when no plausible downstream impact exists. Never silent.

---

## Artifact Selection Guide

Generate the artifacts appropriate to the infrastructure context. Include only what adds analytical value.

### Diagrams (Mermaid)

| Situation | Diagram | Why |
|-----------|---------|-----|
| Always | **Platform Decomposition Diagram** (TOGAF Phase D — flowchart TD: technology platform layers, logical and physical technology components, application component deployment) | TOGAF standard artifact — depicts the technology platform supporting the IS Architecture; shows component hierarchy and deployment |
| Always | **Environments and Locations Diagram** (TOGAF Phase D — flowchart: geographic locations → deployed technologies and applications per location) | TOGAF standard artifact — shows which locations host which applications, supports DR, data residency, and compliance jurisdiction mapping |
| Always | **Networked Computing / Hardware Diagram** (TOGAF Phase D — flowchart: hardware nodes, network interconnections, three-tier layers) | TOGAF standard artifact — deployed logical view of application components in the distributed computing environment; supports authorisation and security design |
| Network communication paths in scope | **Communications Engineering Diagram** (TOGAF Phase D — flowchart: routers, switches, firewalls, network links, protocols per environment) | TOGAF standard artifact — describes the communication infrastructure and connectivity between technology components |
| Processing and deployment units in scope | **Processing Diagram** (TOGAF Phase D — UML deployment diagram: deployable units, connectivity, protocols, load requirements) | TOGAF standard artifact — shows how application components are grouped into deployment units and hosted on the technology platform |
| DR/HA in scope | **Failover topology** (flowchart: primary site → failure event → DR site, with RTO/RPO annotated) | Extends Environments and Locations Diagram — makes failover sequence and recovery time explicit |
| CI/CD pipeline in scope | **Delivery pipeline** (flowchart LR: commit → build → test → stage → prod, with gate labels) | Reveals bottlenecks, missing gates, and manual handoffs |

**Mermaid rules:**
- Use `<br>` for line breaks inside node labels — never `\n`
- Label edges with protocol, encryption, and trust level (e.g. `mTLS`, `public`, `internal`)
- Group nodes by region or zone using subgraphs — blast radius becomes visible

### Tables

| Table | Always / Conditional | Purpose |
|-------|---------------------|---------|
| **Technology Portfolio Catalog** (TOGAF Phase D) | Always | TOGAF standard catalog — every technology component: name, type, managed/self-managed, provider, version, lifecycle status, owner. Classified against TOGAF Technical Reference Model (TRM). Foundation for the Application/Technology Matrix |
| **Technology Standards Catalog** (TOGAF Phase D) | TOGAF mode | TOGAF standard catalog — agreed standards for technology deployment: approved products, versions, refresh cycles, location-specific standards, compliance requirements. Used to drive procurement decisions and identify non-conformance |
| **Application/Technology Matrix** (TOGAF Phase D) | TOGAF mode | TOGAF standard matrix — maps application components (from Phase C) to supporting technology components. CRUD-style mapping showing which technology each application depends on. Foundation for Phase C → Phase D traceability |
| **Lock-in surface assessment** | Always | Per component: lock-in depth (shallow/deep), portability path, exit cost estimate |
| **Availability and recovery assessment** | Always | Per tier: SLA %, RTO, RPO, HA pattern, last DR test date |
| **Technology anti-pattern inventory** | Always | Explicit list of anti-patterns found, with severity and remediation |
| **IaC coverage** | When IaC signals present | Component × IaC coverage (full / partial / none), drift risk, GitOps maturity |
| **Technology lifecycle** | When end-of-support signals present | Component, current version, EOL date, upgrade path, priority |
| **Cost model** | When cloud spend or unit economics in scope | Per tier: current cost, unit cost driver, optimisation lever, confidence |
| **Observability stack** | Always | Metrics / logs / traces / alerting / on-call — tool, coverage, gap |
| **Fix list** | Always | Prioritised, actionable remediation with owner and review trigger |

### Callouts (Obsidian-style)

| Callout | When |
|---------|------|
| `> [!warning]` | Anti-pattern detected; missing DR test; EOL technology in a critical path |
| `> [!important]` | One-way door technology decision (cloud provider, data residency topology) |
| `> [!tip]` | Managed service or commodity tool that eliminates a self-managed operational burden |
| `> [!info]` | Cross-reference to Phase C application architecture, ADR, or security policy |
| `> [!abstract]` | Executive summary — infrastructure health verdict for non-technical stakeholders |

> [!tip]
> **Worked example:** see `references/examples/24.01-technology-architecture.md` for a fully instantiated Phase D Technology Architecture — 12 components, Platform Decomposition Diagram, 6 anti-patterns, cost model, and Phase C→D traceability, anchored to the ACME Corp onboarding engagement.

---

## Technology Anti-Pattern Checklist

Check every infrastructure component against this list. Each hit becomes a row in the Anti-Pattern Inventory. A "not applicable" finding must be stated explicitly — not silently omitted.

| # | Anti-pattern | Check | Risk if present |
|---|-------------|-------|----------------|
| 1 | **Snowflake infrastructure** | No component is unique and hand-configured — all infrastructure is reproducible from code | Irreproducible environments; unrecoverable failures; every change is a risk |
| 2 | **Pet servers** | Servers are treated as cattle (replaceable) not pets (named, maintained) — auto-healing, immutable images | Manual patching, configuration drift, long incident recovery times |
| 3 | **Manual provisioning** | All infrastructure changes go through IaC — no console-click provisioning in production | Configuration drift, untracked changes, compliance failures, runbook rot |
| 4 | **No immutable artefacts** | Build artefacts (container images, AMIs) are immutable and version-pinned — never patched in place | Environment inconsistency; "works on staging" failures; silent rollback failures |
| 5 | **Missing tagging taxonomy** | All cloud resources carry mandatory tags (owner, environment, cost centre, application) | Unattributable cloud spend; orphaned resources; runaway costs |
| 6 | **Flat network** | Network is segmented into trust zones (public, DMZ, private, data) — no flat topology | Lateral movement risk: one compromised workload reaches everything |
| 7 | **Secrets in environment variables** | Secrets are injected at runtime from a secrets manager — never baked into images or env vars | Credentials leak via logs, dumps, or container registry scans |
| 8 | **No DR test on record** | DR procedure has been tested and RTO/RPO validated within the last 12 months | Untested DR = no DR. Actual RTO unknown; recovery procedure may be broken |
| 9 | **Missing observability baseline** | Every production workload emits metrics, structured logs, and distributed traces; SLOs defined; alerts on burn rate | Incidents diagnosed by guesswork; SLA breaches undetected until customers complain |
| 10 | **Undifferentiated heavy lifting** | No component is being self-managed where a managed equivalent exists at commodity cost | Operational burden disproportionate to value — team capacity consumed by toil |
| 11 | **Single-region without justification** | Multi-region or documented justification for single-region trade-off (cost, latency, data residency) | Regional outage = full outage — no degraded mode |
| 12 | **No resource limits or quotas** | Every workload has CPU, memory, and storage limits — no unbounded resource consumption | One misbehaving workload can starve the platform — cascading failure |
| 13 | **IaC without state locking** | Terraform/Pulumi state is remote, encrypted, and locked — no local state files | Concurrent applies corrupt state; secrets leak via local state files |
| 14 | **Over-engineered platform for team size** | Platform complexity is proportional to team operational maturity — no Kubernetes for a 3-person team | Platform becomes the product; delivery teams spend more time on infra than on features |

---

## Assessment Process

### Step 1 — Read and Frame
Read the full technology architecture document or infrastructure description before judging. Identify:
- The deployment model (cloud/on-prem/hybrid) and provider(s)
- The availability and recovery targets (SLA %, RTO, RPO)
- The Phase C application/data components this technology layer must support
- The team size and operational maturity signals

### Step 2 — Build the Technology Component Inventory
For every infrastructure component: name, type (compute/storage/network/security/observability), managed or self-managed, provider, lifecycle status, owner role. Missing components are unknown risk — flag them.

### Step 3 — Run the Anti-Pattern Checklist
Check all 14 patterns. Every hit gets a row in the Anti-Pattern Inventory with severity (Critical / High / Medium / Low) and remediation action.

### Step 4 — Assess Infrastructure Topology Fitness
- Is the topology appropriate for the availability targets?
- Is network segmentation in place (public / DMZ / private / data zones)?
- Is there a single point of failure at any tier?
- Is the blast radius of a component failure bounded?
- Is the deployment model appropriate for data residency obligations?

### Step 5 — Assess DR / HA
For each critical tier:
- What is the HA pattern (active-active / active-passive / warm standby / cold standby)?
- Is the RTO/RPO achievable with the current pattern?
- When was the DR procedure last tested and with what outcome?
- Is failover automated or manual?

### Step 6 — Assess the Lock-in Surface
For each component — especially storage, managed services, and cloud-native features:
- Is lock-in shallow (CLI/API-compatible alternative exists) or deep (proprietary data format, vendor-specific compute)?
- Is the lock-in intentional (cost/speed trade-off accepted) or accidental (team didn't consider it)?
- What is the exit cost (data egress, re-platforming effort, contract penalty)?

### Step 7 — Assess the Observability Infrastructure
Beyond "we use Prometheus and Grafana":
- **Metrics**: RED (Rate, Errors, Duration) per service; infrastructure saturation metrics per tier
- **Logs**: structured JSON; correlation ID and trace ID in every log line; retention policy defined
- **Traces**: distributed tracing instrumented; W3C Trace Context propagated across service boundaries
- **SLOs**: per-service SLO defined; burn-rate alerts configured; error budget tracked
- **On-call**: runbook per alert; escalation path defined; mean time to detect (MTTD) and resolve (MTTR) tracked

### Step 8 — Assess IaC Maturity
- What percentage of infrastructure is code-managed vs manually provisioned?
- Is state remote, encrypted, and locked?
- Are modules versioned and reused or is every stack a snowflake?
- Is there a GitOps pipeline (PR → plan → apply) or are applies run ad hoc?
- Is there drift detection?

### Step 9 — Assess Technology Lifecycle
For every component:
- What is the current version and its EOL date?
- Is there a patching and upgrade cadence?
- Are any components EOL or within 12 months of EOL in a critical path?

### Step 10 — Assess the Cost Model
- What is the dominant cost driver per tier (compute, storage, egress, licences)?
- Are workloads right-sized (CPU/memory utilisation tracked, idle resources identified)?
- Is there a FinOps practice (tagging, budgets, anomaly alerts, rightsizing reviews)?
- What is the unit cost and how does it scale with load?

### Step 11 — Apply Phase C → Phase D Traceability *(TOGAF mode)*
For each application/data building block from Phase C: is there a technology building block in Phase D that supports it? Gaps are architecture voids — name them explicitly.

### Step 12 — Produce the Fix List
Prioritise: Critical (production risk or compliance breach now) → High (must fix before next release or audit) → Medium → Low. Every item has an owner (role), reversibility tag, and review trigger.

---

## Output Format

```
## Verdict: Sound | Needs Work | Redesign

> [!abstract]
> [3 sentences for non-technical stakeholders: infrastructure health status, most critical gap, and business consequence of not addressing it.]

---

## Infrastructure Topology

```mermaid
flowchart TD
    subgraph Region1["Region: [name]"]
        subgraph AZ1["Availability Zone 1"]
            c1["[Compute tier]"]
            s1["[Storage tier]"]
        end
        subgraph AZ2["Availability Zone 2"]
            c2["[Compute tier]"]
            s2["[Storage tier]"]
        end
        net["[Network / Load Balancer]"]
    end
    subgraph Security["Security Boundary"]
        waf["WAF / Perimeter"]
        idp["Identity Provider"]
        secrets["Secrets Manager"]
    end
    subgraph Observability["Observability Stack"]
        metrics["Metrics"]
        logs["Logs"]
        traces["Traces"]
    end
```

---

## Technology Component Inventory

| ID | Component | Type | Managed / Self-managed | Provider | Lifecycle status | Owner (role) |
|----|-----------|------|----------------------|---------|-----------------|-------------|
| TECH-001 | [name] | Compute / Storage / Network / Security / Observability / CI-CD | Managed / Self-managed | [cloud / on-prem / vendor] | Active / EOL in [date] / Deprecated | [role] |

---

## Infrastructure Quality Attribute Assessment

| Attribute | Finding | Evidence status | Confidence | Severity |
|-----------|---------|----------------|------------|----------|
| Availability | [HA pattern, SLA %, single points of failure] | tested / asserted / not assessed | proven / informed estimate / working hypothesis | Critical / High / Medium / Low |
| Resilience | [DR pattern, RTO/RPO achievability, last test date, blast radius] | tested / asserted / not assessed | ... | ... |
| Security | [network segmentation, secrets management, identity plane, patch posture] | tested / asserted / not assessed | ... | ... |
| Observability | [metrics/logs/traces coverage, SLOs defined, on-call runbooks] | tested / asserted / not assessed | ... | ... |
| Evolvability | [IaC coverage, platform complexity vs team maturity, lock-in surface] | tested / asserted / not assessed | ... | ... |
| Operability | [runbook coverage, toil ratio, upgrade cadence, on-call burden] | tested / asserted / not assessed | ... | ... |
| Cost Efficiency | [right-sizing, tagging, FinOps practice, unit cost trend] | tested / asserted / not assessed | ... | ... |
| Portability | [lock-in depth per component, intentional vs accidental] | tested / asserted / not assessed | ... | ... |

> [!warning] Critical findings
> [List any Critical-severity findings here.]

---

## Technology Anti-Pattern Inventory

| # | Anti-pattern | Location | Production risk | Severity | Remediation | Owner (role) |
|---|-------------|---------|----------------|----------|------------|-------------|
| 1 | [pattern from checklist] | [TECH-ID or component] | [what goes wrong] | Critical / High / Medium / Low | [specific fix] | [role] |

---

## Lock-in Surface Assessment

| Component | Lock-in depth | Lock-in type | Portability path | Exit cost estimate | Intentional? | Confidence |
|-----------|--------------|-------------|-----------------|-------------------|-------------|------------|
| TECH-001 | Shallow / Deep | Proprietary API / Data format / Compute / Contract | [alternative] | Low / Medium / High | Yes / No — [reason] | proven / informed estimate / working hypothesis |

> [!important]
> [Flag any deep, unintentional lock-in — especially storage or data format lock-in. These are one-way doors that compound cost and delay future platform evolution.]

---

## Availability and Recovery Assessment

| Tier | HA pattern | SLA % | RTO target | RPO target | RTO achievable? | DR last tested | Failover | Owner (role) |
|------|-----------|-------|-----------|-----------|----------------|---------------|---------|-------------|
| [tier] | Active-active / Active-passive / Warm standby / Cold standby | [%] | [min] | [min] | Yes / No — gap: [delta] | [date or Never] | Automated / Manual | [role] |

> [!warning]
> [Flag any tier where DR has never been tested — untested DR is no DR. Flag any tier where RTO target is not achievable with the current HA pattern.]

---

## Observability Stack

| Signal | Tool | Coverage | SLO defined | Burn-rate alert | On-call runbook | Gap |
|--------|------|----------|------------|----------------|----------------|-----|
| Metrics | [tool] | Full / Partial / None | Yes / No | Yes / No | Yes / No | [gap description] |
| Logs | [tool] | Full / Partial / None | N/A | N/A | Yes / No | [gap description] |
| Traces | [tool] | Full / Partial / None | Yes / No | Yes / No | N/A | [gap description] |
| Alerting | [tool] | Full / Partial / None | N/A | N/A | Yes / No | [gap description] |

---

## IaC Coverage

| Component | IaC tool | Coverage | State management | Drift detection | GitOps pipeline | Gap |
|-----------|---------|---------|-----------------|----------------|----------------|-----|
| [component] | Terraform / Pulumi / CDK / None | Full / Partial / None | Remote+locked / Remote / Local | Yes / No | Yes / No | [gap] |

---

## Technology Lifecycle

| Component | Current version | EOL date | Months to EOL | Upgrade path | Priority | Owner (role) |
|-----------|----------------|---------|--------------|-------------|---------|-------------|
| [component] | [vX.Y] | [YYYY-MM-DD or Unknown] | [N] | [upgrade guidance] | Critical / High / Medium / Low | [role] |

> [!warning]
> [Flag any component EOL or within 12 months of EOL in a critical path — these are active compliance and security risks.]

---

## Cost Model

| Tier | Current cost / month | Unit cost driver | Utilisation | Optimisation lever | Savings estimate | Confidence |
|------|---------------------|-----------------|------------|-------------------|-----------------|------------|
| [tier] | €[N] | [$/vCPU-hour / $/GB / $/request] | [%] | [rightsizing / reserved / serverless / spot] | [%] | proven / informed estimate / working hypothesis |

---

## Phase C → Phase D Traceability *(TOGAF mode only)*

| Phase C Building Block | Phase D Technology Component | Traceability | Gap |
|----------------------|------------------------------|-------------|-----|
| [application/data BB] | [TECH-ID] | Explicit / Implied / Missing | ✓ or [gap description] |

> [!warning] Architecture voids *(include only if gaps found)*
> Phase C building blocks with no Phase D owner: [list]. These will fall through the delivery plan.

---

## Disruptive Alternative

[One infrastructure topology or cloud-native approach that challenges the current design — working backwards from the non-functional requirements. What managed service or serverless pattern eliminates the self-managed operational burden? Confidence: proven / informed estimate / working hypothesis.]

---

## Second-Order Effect

[One non-obvious downstream consequence of this technology architecture — the delivery team slowed by platform complexity, the compliance gap triggered by unpatched infrastructure, the runaway cloud cost from untagged workloads, the DR gap discovered during the actual failover.]

---

## Horizon Alignment

**H1 — Immediate:** [operational reliability gaps requiring action now — named owner per item]
**H2 — Emerging:** [technology standardisation, IaC maturity, platform engineering investment]
**H3 — Structural:** [cloud-native evolution, edge, AI-optimised infrastructure, or FinOps at scale]

---

## TOGAF Checks *(TOGAF mode only)*

**ADM Phase D alignment:** [consistent / inconsistent — do scope and artefacts match Phase D standards?]
**Phase C → Phase D traceability:** [all Phase C building blocks have a Phase D counterpart? Yes / Partial / No]
**Architecture contracts:** [present / absent]
**Technology standards catalogue:** [referenced / absent — defines approved technology components?]

---

## Fix List

| # | Severity | Finding | Fix | Owner (role) | Reversibility | Review trigger |
|---|----------|---------|-----|--------------|---------------|----------------|
| 1 | Critical | [finding] | [specific action] | [role] | one-way / two-way | [evidence threshold or event] |
| 2 | High | ... | ... | [role] | one-way / two-way | ... |
| 3 | Medium | ... | ... | [role] | one-way / two-way | ... |

---

## Broad Responsibility

[One line covering: data residency and sovereignty obligations per cloud region · energy and carbon cost of infrastructure choices at scale · supply chain risk from cloud provider concentration · blast radius into customers-of-customers if infrastructure fails. `N/A — [reason]` only if none plausibly applies.]

---

## Standards Bar

Does this meet the bar for a client deliverable? [Yes / No — reason]
```

## Next Step

After completing a Phase D Technology Architecture:

- **Forward — Phase E/F**: invoke `gap-analysis` to produce the Technology Architecture gap map, then `migration-plan` to sequence the gaps into a phased roadmap with Transition Architectures.
- **Validate — Chief architect review**: invoke `architecture-review` before Architecture Board submission for an opinionated critique of the technology design, especially lock-in surface and DR fitness.
- **Validate — Principles alignment**: invoke `principles-check` to verify the technology choices respect the Technology Architecture Principles (especially portability, standards adherence, and lock-in surface).
- **Validate — Artifact completeness**: invoke `artifact-completeness` to check the Phase D ADD section — Technology Standards Catalog, Technology Portfolio Catalog, System/Technology Matrix, and Environments and Locations Diagram all required. See `references/togaf-content-framework.md` for the full Phase D artefact inventory.
- **Validate — Compliance**: invoke `compliance-review` for an Architecture Board submission, especially if the technology choices deviate from the Standards Information Base.
- **Document technology decisions**: invoke `adr-generator` for platform selection decisions, vendor choices, or cloud provider selections that are one-way doors.
- **Assess risks**: invoke `risk-radar` to evaluate technology risk (vendor lock-in, obsolescence, security boundary gaps, DR coverage) as a final quality gate before sign-off.
- **Communicate**: invoke `executive-summary` for Phase D sign-off with the Architecture Sponsor, or `stakeholder-communication` for delivery team briefing on technology standards.
