---
name: add-function-agent
description: This skill should be used when the user says "add a billing agent", "add a bookkeeping agent", "set up a support tier-1 agent", "add a recruiting agent", "add a compliance agent", "add a CRM agent", "add a contracts agent", "add an analytics agent", "add a marketing email agent", "add a CMS agent", "scaffold a function-specific agent", or wants to add a single business-function agent backed by a verified-write MCP integration. Each agent ships with explicit scope, "what this will NOT do" constraints, and recommended human-in-the-loop checkpoints.
argument-hint: "--function <billing|bookkeeping|support-tier1|recruiting|compliance|crm-ops|contracts|analytics-reporting|marketing-email|web-cms|social-drafts> [--project path/to/project] [--dry-run]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Add Function Agent — Opt-in Business-Function Agent Scaffolding

Scaffold a single business-function agent backed by a verified-write MCP integration. **Each function is opt-in.** The plugin does NOT pretend that "scaffolding a marketing folder" gives you a marketing agent — it gives you nothing until you explicitly add one via this skill, with the MCP wired up and the scope written down.

## What this skill creates per function

For each `--function` you add:

1. **An agent definition** at `<project-or-company>/.claude/agents/<function>-agent.md` — with tools restricted to the relevant MCP, model selection rationale, and a system prompt that describes scope.
2. **An MCP server entry** merged into `.mcp.json` — with environment variables for credentials (never hardcoded).
3. **A `SCOPE.md` file** at `<project-or-company>/.claude/agents/<function>-scope.md` — explicit "what this agent will / will NOT do" + recommended human-in-the-loop checkpoints + escalation rules.
4. **A note in CLAUDE.md** at the appropriate level — telling other agents this function-specific agent exists and when to defer to it.

## Available functions (April 2026)

Only functions with a verified write-capable MCP are supported. If a function isn't in this list, it's because the integration doesn't exist or is read-only.

### Verified write-capable

| `--function` | MCP | Vendor status | Agent can | Agent will NOT |
|---|---|---|---|---|
| `billing` | Stripe MCP (official) | GA | Look up customers, create/void invoices, issue refunds (within limit), pull payment history, manage subscriptions | Issue refunds > configured limit; modify pricing; touch Connect / Treasury without explicit human approval |
| `bookkeeping` | QuickBooks MCP (official Intuit) OR Xero MCP (official) | GA | Reconcile transactions, categorize expenses, generate reports, post journal entries to draft state | Finalize close; modify chart of accounts; file taxes; alter prior-period entries |
| `support-tier1` | Intercom MCP (official) | GA | Look up users, search conversations, draft replies, tag/route tickets, escalate to human queue | Send replies autonomously (drafts only by default); refund or compensate without human; close tickets touching billing/legal |
| `recruiting` | Greenhouse MCP (community, mature) OR Lever MCP (community) | Community | First-pass screening notes, schedule interviews, sync candidate status, generate offer-letter drafts | Make hiring decisions; send rejection emails autonomously; modify job requisitions |
| `compliance` | Vanta MCP (official open-source) OR Drata MCP (official, hosted) | GA | Pull evidence, check control status, generate audit reports, flag missing evidence | Mark controls as compliant; modify policies; respond to auditors |
| `crm-ops` | HubSpot MCP (official) OR Salesforce MCP (official, hosted) | GA / Beta | Update contact/deal records, log activities, run reports, segment lists | Send autonomous outbound; modify pipeline definitions; bulk-delete records |
| `contracts` | DocuSign MCP (official, beta) | Beta | Send pre-approved templates, check signing status, query Navigator agreements, trigger Maestro workflows | Send custom contracts without human review; modify signed documents; legally bind without explicit human send |
| `analytics-reporting` | PostHog OR Mixpanel OR Amplitude OR GA4 MCP (all official) | GA | Run queries, build dashboards, export reports, drill into events | Modify tracking implementation; delete data; share PII outside approved destinations |
| `marketing-email` | Mailchimp MCP (community, mature) OR Customer.io MCP (official) | GA / Community | Build segments, draft campaigns, schedule sends to test segments, pull metrics | Send to full list without human approval; modify suppression list autonomously; touch GDPR / unsubscribe records |
| `web-cms` | Webflow MCP (official) | GA | Read/write CMS items, manage Sites API, publish (with confirmation) | Publish without human approval; modify Designer canvas without MCP Bridge App |
| `social-drafts` | (no MCP for Buffer/Hootsuite — drafts only, written to filesystem) | N/A | Draft posts to a `social-drafts/` folder for human review and manual posting | Post anything autonomously (no integration exists in 2026 for write-capable scheduling) |

### Explicitly NOT supported (and why)

These functions don't get an agent because the integration isn't there:

| Function | Status | Why no agent |
|---|---|---|
| `payroll` | No MCP for Gusto/Rippling write; Deel is read-only | Cannot reliably execute payroll without write APIs |
| `banking-ops` | No MCP for Mercury/Brex/Ramp | Cannot move money out of operating accounts |
| `support-tier2-zendesk` | Zendesk is MCP client, not server | Cannot let Claude act in Zendesk |
| `support-helpscout` | No MCP | No write integration |
| `clm` | No Ironclad MCP (only DocuSign signing) | Contract lifecycle management is human-only |
| `social-scheduling` | No Buffer/Hootsuite MCP | Drafts only — see `social-drafts` |
| `apollo-outbound` | No first-party Apollo MCP | Use `crm-ops` if you sync Apollo data into HubSpot/Salesforce first |

## Workflow

### Step 1: Determine target

Find the right `.claude/agents/` directory. If `--project <path>` is given, use that. Otherwise:
1. Check current directory for `.claude/agents/`
2. Walk up to find a company root (look for `CLAUDE.md` + `.claude/`)
3. Ask the user

### Step 2: Validate function choice

Confirm `--function` is in the supported list above. If not, surface the "not supported" table above and explain why — never silently fall back to a generic template.

### Step 3: Gather function-specific context

Ask the user for:
- **Credentials source** — which env var name will hold the token? (e.g., `STRIPE_SECRET_KEY`, `INTERCOM_ACCESS_TOKEN`)
- **Scope limits** — for `billing`: what's the autonomous refund limit? for `marketing-email`: which segment is the agent allowed to send to without human approval?
- **Escalation channel** — Slack channel, email, or `escalations/` folder where the agent dumps anything outside its scope

In `--dry-run` mode, skip prompts and emit the proposed file contents to stdout instead of writing.

### Step 4: Generate the agent definition

Load `references/function-agent-templates.md` and pick the matching template. Customize:
- Model: Opus for read-heavy / judgment-heavy functions (recruiting, compliance), Sonnet for action-heavy / drafting (billing, bookkeeping, support-tier1)
- Tools: `Read, Grep, Glob, Bash` plus the specific MCP tool prefix (e.g., `mcp__stripe__*`)
- Scope limits from Step 3 inserted into the system prompt

Write to `.claude/agents/<function>-agent.md`.

### Step 5: Write the SCOPE.md companion

Critical step. Write `.claude/agents/<function>-scope.md` containing:
- **Will do** (concrete, scoped list)
- **Will NOT do** (concrete, ban list — taken verbatim from the function's table row above + any user-specified limits)
- **Human-in-the-loop checkpoints** (when the agent must surface something for human approval)
- **Escalation channel** (where things outside scope go)
- **Failure modes** (what to do when the MCP errors, when credentials expire, when rate-limited)

The scope file is the honesty contract. The agent's system prompt references it.

### Step 6: Merge MCP entry into .mcp.json

Read existing `.mcp.json` (or create fresh). Merge in the new server entry from `references/function-agent-templates.md`. Use `${ENV_VAR}` references — never hardcode credentials.

If `.mcp.json` already has a server with the same name, ask before overwriting.

### Step 7: Update CLAUDE.md to register the agent

Add a one-line entry in the appropriate CLAUDE.md (`engineering/<project>/CLAUDE.md` or company root, depending on scope) under an "Agents" section:

```markdown
## Function-Specific Agents
- `billing-agent` — Stripe operations within scope. See `.claude/agents/billing-scope.md` for limits.
```

This tells other agents and humans that the specialist exists.

### Step 8: Validate and report

Run the validators:

```bash
python3 ${plugin_root}/scripts/check-mcp-config.py <project>/.mcp.json
python3 ${plugin_root}/scripts/audit-structure.py <project> --skip-projects --skip-hooks
```

Report:
- File paths created
- Env vars the user must set before invoking the agent
- Recommended next step: test the MCP connection via `/mcp` in Claude Code

### Step 9: Honest summary

Tell the user, verbatim:

> Added `<function>` agent at `<path>`. **Before this is useful:**
> 1. Set the env var(s) listed above
> 2. Restart Claude Code so the MCP server picks up the new config
> 3. Run `/mcp` to verify the server is connected
> 4. Read `<scope-file>` — what this agent will and will NOT do
>
> **The agent does not run autonomously.** You invoke it like any other Claude Code subagent. Recommended human-in-the-loop checkpoints are listed in the scope file.

## What this skill does NOT do

- Does not configure cron / scheduled invocation of the agent (use Routines via claude.ai or the user's scheduler).
- Does not manage credential rotation — that's still your operational responsibility.
- Does not check whether the MCP is currently up — `claude mcp list` and `/mcp` are the verification tools.
- Does not verify the agent's outputs are correct — there is no automated quality gate for "did the bookkeeping reconcile correctly." That's the human-in-the-loop checkpoint's job.
- Does not give you a function that doesn't have a write-capable MCP, no matter how much you ask. See the "Explicitly NOT supported" table.

## Key References

- `references/function-agent-templates.md` — Full agent + MCP + scope templates for each supported function
- Plugin-level `scripts/check-mcp-config.py` — Run after MCP changes
- Plugin-level `scripts/audit-structure.py` — Run after agent file changes
