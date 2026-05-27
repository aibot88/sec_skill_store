---
name: install-department
description: "Install a department's slice of the company brain via multi-agent probes of the head's connected tools (Notion, HubSpot, Linear, Slack, Granola, Gmail, etc., via Syroco Connect / Pipedream) plus a structured methodology interview. Produces a Department Spec the runtime can index — covering tools-in-use, roles, cadence, decision flow, taxonomy, automations, and metrics. Use when a department head bootstraps their function into the brain — typically the first install per function (Marketing, Sales, Product, Engineering, Finance, CSM, Support). Do NOT use for one-off knowledge capture, code-context indexing (use context-engineering), or updating an already-installed department."
requiredApps: [pipedream]
---

# Install Department

Capture *how a department actually works* — tools, methodology, roles,
cadence, taxonomy, automations, metrics — into a structured spec the
company brain can index. The dept head leads; the skill orchestrates
sub-agents that probe each connected tool in parallel.

## Quick start

The head of the department being installed runs:

```
install-department --department <function>
```

Example: `install-department --department product`. The skill walks the
head through five phases (Connect → Probe → Interview → Synthesize →
Validate). Total time: 60–90 min, mostly background. The output is one
markdown file (`department-spec.md`) plus one JSON manifest
(`department.json`) written to the brain.

## What gets installed

A **Department Spec** with seven canonical sections:

| Section | What it captures |
|---|---|
| Tools | Inventory of tools the dept uses, with what data lives in each |
| Roles | Who-does-what, distinguishing accountable vs consulted |
| Cadence | Recurring meetings, reviews, cycles, deadlines |
| Pipeline | The sequential stages work moves through (e.g. Signal → Opportunity → Solution → PRD → Delivery → Release for Product) |
| Taxonomy | The categories/themes/tags the department classifies work by |
| Automations | What runs without human intervention (cron jobs, webhooks, integrations) |
| Metrics | What the dept reports on, and what thresholds matter |

This format is canonical — the runtime indexes against these section
names. Other downstream skills (`find-links`, `audit-process`,
`sota-search`) consume Department Specs and assume this shape.

## How it works (5 phases)

### Phase 1 — Connect (5 min, blocking)

Verify the head has authorized at least one tool via Pipedream / Syroco
Connect. The skill calls `pipedream.list_connected_accounts` for the
head's identity and emits a tool inventory.

**Refusal path**: if zero tools are connected, the skill stops and
prints connection instructions. Do not proceed to Phase 2 with no tools.

**Soft warning**: if fewer than 3 tools are connected, warn the head
that the resulting Department Spec will be thin. Most departments use 5+
tools day-to-day.

### Phase 2 — Probe (10–30 min, background)

For each connected tool, the skill launches a sub-agent (one per tool,
in parallel) that introspects the tool through its MCP surface. The
probe collects:

- **What entities exist**: databases, projects, channels, lists, boards
- **Volume signal**: rough item counts per entity
- **Recency signal**: latest activity timestamp per entity
- **Access signal**: which entities the head reads vs writes
- **Cross-references**: which entities link to which (Notion mentions,
  HubSpot deal-to-contact, Linear issue-to-project)

Sub-agents write JSONL probe results to `cache/probe/<tool>.jsonl`. See
[`references/tool-probes.md`](./references/tool-probes.md) for the
per-tool probe contract and the supported tool list.

The human is **not in the loop during Phase 2**. Phase 2 is the longest
phase by clock time and the shortest by attention cost.

### Phase 3 — Interview (30–60 min, blocking)

The skill walks the head through seven structured prompts — one per
Department Spec section — showing them their probed tool inventory and
asking how it maps to their actual work. See
[`references/interview-prompts.md`](./references/interview-prompts.md)
for the prompt list and follow-up rules.

This is **not a free-form chat**. Each prompt has a required answer
shape (e.g., for Cadence: at least one recurring meeting with frequency,
attendees, and trigger; for Pipeline: ordered list of stages with the
event that moves work from one stage to the next).

If the head answers vaguely ("we just figure it out as we go"), the
skill asks the standardized follow-up from
[`references/interview-prompts.md`](./references/interview-prompts.md)
to extract the implicit pattern. Do not accept "no methodology" as an
answer — every functioning department has one, even if it's never been
written down.

### Phase 4 — Synthesize (background, 1–2 min)

The skill drafts the Department Spec by:

1. Filling each of the 7 sections from the matching interview answer.
2. Cross-referencing the tool inventory: every claim in the interview
   that references a tool must point to a probed entity (e.g., if the
   head says "Signals live in Notion", the synthesizer verifies a Notion
   database called Signals or similar exists in the probe results).
3. Flagging unverified claims for re-interview — these go to a
   `??-needs-verification.md` annex, not into the spec body.

See [`references/department-spec-template.md`](./references/department-spec-template.md)
for the canonical output structure.

### Phase 5 — Validate + Commit (10–15 min, blocking)

The skill prints the draft and asks the head to review. Iterate on the
spec until the head accepts it (`/scripts/validate.py` enforces all 7
sections present and non-empty). On acceptance, write to:

- `<brain-root>/departments/<function>/department-spec.md` — the human
  doc
- `<brain-root>/departments/<function>/department.json` — the machine
  manifest the runtime indexes against

Do not commit a partial spec. Do not commit without the head's explicit
acceptance.

## Rules

| Rule | Why |
|---|---|
| The dept head is the only authoritative interviewer | Methodology authority cannot be delegated. A PM, contractor, or CEO running it for the head gets *their* view, not the head's. If the head can't make the interview phase, reschedule — do not run with a delegate. |
| All 7 sections must be non-empty before commit | The runtime assumes the canonical shape. Empty sections silently break downstream skills. |
| Probed tool inventory must back every tool claim | Prevents the spec from describing aspirational tools the dept doesn't actually use. |
| Sub-agents write to `cache/probe/`, not the brain | Probe results are working state, not knowledge. The brain only sees the validated spec. |
| The skill never sends messages, edits records, or modifies tool state | Probes are read-only. The skill installs *understanding*, not *changes*. |
| Re-running for an already-installed department is a no-op with a warning | Use `refresh-department` (v0.2) for updates. Re-installing destroys human-validated context. |

## Output

Two files per install, written to the brain:

**`department-spec.md`** — markdown with the 7 canonical sections.
Render-ready for humans. Indexable by the runtime. Example structure
in [`references/department-spec-template.md`](./references/department-spec-template.md).

**`department.json`** — machine manifest:

```json
{
  "department": "product",
  "head": "Victor Grosjean",
  "installed_at": "ISO-8601 timestamp",
  "spec_version": "1.0",
  "tools": [
    { "name": "notion", "entities": ["Signals", "Opportunities", "Solutions", "Deliveries"], "access": "rw" },
    { "name": "hubspot", "entities": ["Companies", "Deals"], "access": "r" },
    { "name": "linear", "entities": ["Issues", "Projects"], "access": "rw" }
  ],
  "pipeline_stages": ["Signal", "Opportunity", "Solution", "PRD", "Delivery", "Release"],
  "cadence": [
    { "name": "Daily Sync", "frequency": "daily 07:00 CET", "trigger": "cron" },
    { "name": "Weekly Re-rank", "frequency": "Monday 08:00 CET", "trigger": "cron" },
    { "name": "Betting Table", "frequency": "weekly", "trigger": "calendar" }
  ],
  "metrics": [
    { "name": "ARR at stake per theme", "source": "hubspot.deals", "threshold": null },
    { "name": "Notes sent rate", "source": "notion.deliveries", "threshold": "100%" }
  ]
}
```

## Prerequisites

- Python 3.10+
- `pip install "mcp[cli]" requests pyyaml`
- A Pipedream / Syroco Connect account on the dept head's identity, with
  at least one tool authorized.
- Write access to the brain location (`<brain-root>/departments/`).

## Scripts

| Script | Purpose |
|---|---|
| `scripts/install_department.py` | CLI entry point; orchestrates the 5 phases |
| `scripts/probe_tool.py` | Generic per-tool probe; dispatches to tool-specific MCP calls |
| `scripts/interview.py` | Runs the structured 7-section interview |
| `scripts/synthesize.py` | Produces `department-spec.md` + `department.json` from probe + interview outputs |
| `scripts/validate.py` | Refuses incomplete specs (all 7 sections non-empty, every tool claim backed by a probe entity) |

## References

- [`references/tool-probes.md`](./references/tool-probes.md) — supported
  tools and what each probe collects
- [`references/interview-prompts.md`](./references/interview-prompts.md)
  — the 7 interview prompts with follow-ups
- [`references/department-spec-template.md`](./references/department-spec-template.md)
  — canonical output structure
- [`references/methodology-patterns.md`](./references/methodology-patterns.md)
  — common cadence patterns by function
- [`references/role-taxonomies.md`](./references/role-taxonomies.md) —
  common role splits per function
- [`references/example-product-spec.md`](./references/example-product-spec.md)
  — a worked example built from the manual prior art at
  `syroco-product-ops/README.md`

## Errors and limitations

| Failure mode | What happens | What to do |
|---|---|---|
| Head has no tools connected | Phase 1 stops with connect-instructions | Authorize tools in Pipedream / Syroco Connect, retry |
| Head abandons mid-interview | Partial probe results in `cache/probe/`; no spec committed | Resume by re-running; the skill restores from cache |
| Probe sub-agent fails for one tool | That tool is excluded from the spec; warning emitted | Manually inspect the failing tool, retry single-tool probe via `probe_tool.py --tool <name>` |
| Interview answers contradict probed inventory | Synthesizer flags claims to `??-needs-verification.md`; spec body omits them | Re-interview the affected sections |
| Two heads claim the same department | The skill refuses; one head must be designated as authoritative | Resolve org-chart ambiguity outside the skill, then re-run |

## Anabasis conformance

This skill is the canonical reference implementation of `install-department`
in the [Anabasis spec](https://github.com/VictorGjn/anabasis/blob/main/spec/reference-skills/install-department.md)
at `spec v0.1`. The skill follows the [agentskills.io](https://agentskills.io/)
SKILL.md format with no Anabasis-specific frontmatter additions —
Anabasis-conformant skills are simply well-formed agentskills.io skills.

The Anabasis runtime invokes this skill once per department to bootstrap
the brain. install-department remains independently useful — a single
team can run it without an Anabasis runtime and get a usable Department
Spec markdown file out the other end.
