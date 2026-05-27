---
name: cosmos:singularity
description: QuantumAgent — Declare a macro-scale singularity event that reshapes project context. Singularities are project-level events (migration, paradigm shift, compliance change) that invalidate prior insights and inject new constraints into all future cosmos spawns.
---

# cosmos:singularity

Declare a project-level quantum singularity. Singularities are events that *reshape the solution space itself* — major migrations, paradigm shifts, compliance changes, framework upgrades. After a singularity, insights from before the event may be stale.

This is the macro-scale layer of QuantumAgent. While `/cosmos spawn` operates at the universe scale (N parallel implementations), `/cosmos singularity` operates at the project scale (events that affect ALL future explorations).

## Trigger

`/cosmos singularity --name "<event>" --invalidates "<pattern1,pattern2,...>" [--trigger "<reason>"] [--description "<text>"]`

Examples:

```bash
/cosmos singularity --name "auth-migration-v2" \
  --trigger "compliance-2026-Q3" \
  --invalidates "session-based-auth,pre-2026-cookie-policy" \
  --description "All session-based auth retired. JWT-only going forward."

/cosmos singularity --name "framework-upgrade-next15" \
  --trigger "performance-mandate" \
  --invalidates "pages-router,getServerSideProps-patterns"
```

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Parse arguments

From the trigger message, extract:
- `--name` *(required)* — short identifier, kebab-case (e.g., `auth-migration-v2`)
- `--invalidates` *(required)* — comma-separated patterns/tags this event invalidates
- `--trigger` *(optional)* — what caused this singularity (compliance, performance, etc.)
- `--description` *(optional)* — free-text explanation

If `--name` or `--invalidates` missing:
```
❌ Singularity requires --name and --invalidates.
   Usage: /cosmos singularity --name "<event>" --invalidates "<patterns>"
```

### Step 3 — Prepare quantum memory

```bash
mkdir -p <repo_root>/.quantum/singularities
touch <repo_root>/.quantum/singularities/events.jsonl
```

### Step 4 — Generate ISO timestamp

Capture current timestamp in ISO 8601 format (UTC, e.g., `2026-05-12T14:32:00Z`). Store as `<ts>`.

### Step 5 — Append singularity event

Build the JSON event:

```json
{
  "name": "<name>",
  "ts": "<ts>",
  "trigger": "<trigger or null>",
  "invalidates": ["<pattern1>", "<pattern2>", ...],
  "description": "<description or null>"
}
```

Append to events file:

```bash
echo '<json>' >> <repo_root>/.quantum/singularities/events.jsonl
```

**Important:** Always append, never overwrite. The events log is the project's macro-scale history — it must be append-only for audit integrity.

### Step 6 — Check for active cosmos

```bash
git -C <repo_root> worktree list | grep -E '\[cosmos/' || true
```

If active cosmos worktrees exist, output a warning:

```
⚠️  Active cosmos detected: <list>
   This singularity will NOT retroactively affect running cosmos.
   New /cosmos spawn calls will inherit the singularity automatically.
   To apply to current cosmos: run /cosmos stop, then /cosmos spawn again.
```

If no active cosmos, skip this step.

### Step 7 — Confirm declaration

Output:

```
☄️  Singularity declared

   Name:        <name>
   Timestamp:   <ts>
   Trigger:     <trigger or "(unspecified)">
   Invalidates: <invalidates>

   Description: <description or "(none)">

🌌 All future /cosmos spawn calls will inherit this singularity as macro context.
   Insights matching invalidated patterns will be treated as pre-singularity (stale).

   Logged at: .quantum/singularities/events.jsonl
```

## When to use

**Good fit:**
- Major migration completed (auth system, database, framework)
- Compliance requirement changed (GDPR, SOC2, HIPAA scope shift)
- Architectural paradigm transition (monolith → microservices, REST → GraphQL)
- Performance contract changed (new SLA, hard latency ceiling)
- Security incident response (token format change, key rotation event)

**Not a fit:**
- Routine code changes (use git commits, not singularities)
- Single-feature additions (these don't invalidate prior context)
- Bug fixes (these are insights, not singularities)
- Personal preferences (singularities are project-wide, not per-developer)

## Why this matters

Without macro-scale events, every `/cosmos spawn` starts from the same baseline. Insights from 6 months ago — when the project used cookies for auth — would still inform new explorations, even though cookies are no longer relevant.

Singularities establish *temporal coherence*: cosmos automatically know "we're in the post-migration era" without manual context-pasting. This is the General Relativity of QuantumAgent — the constraints curve the solution space, and singularities mark phase transitions in that curvature.

## Format reference

`.quantum/singularities/events.jsonl` is append-only JSONL. Each line:

```json
{"name":"<kebab-case-id>","ts":"<ISO-8601>","trigger":"<reason>","invalidates":["<pattern>",...],"description":"<text>"}
```

All future `/cosmos spawn` and `/cosmos observe` operations read this file to inject macro context.
