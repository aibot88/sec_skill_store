---
name: incident-respond
description: 'End-to-end incident-response playbook for a CVE actively in the wild — confirms urgency via KEV/EPSS/sightings, pulls IOCs and ATT&CK chain, fetches detection rules for installed families, evaluates patch path or workarounds, generates VEX attestation, posts a consolidated report. Use when a CVE goes hot, your dependency is named in a vendor advisory, or the team needs a one-conversation SOC response.'
argument-hint: <vuln-id>
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "incident"
  - "actively exploit"
  - "zero day"
  - "in the wild"
chain:
  - detection-rules
  - verify-fix
  - vex-publish
outputBudget: long
cooldown: per-session
---

# Vulnetix Incident Response Skill

## Use when

- A CVE went hot overnight and you need a complete SOC response in one conversation.
- A vendor advisory names a dependency you ship.
- Active sightings spiked (CrowdSec, Shadowserver) on a vuln you have.
- Building the timeline of "what we knew when" for a post-incident review.
- Coordinating detection + patch + VEX in a single workflow.

## Don't use for

- Routine triage — use `/vulnetix:soc-triage`.
- Single-step actions — use the constituent skills directly (`/vulnetix:fix`, `/vulnetix:detection-rules`, etc.).
- For dormant CVEs (no recent sightings, not in KEV) — the skill exits early and recommends `/vulnetix:remediation` instead.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

A focused playbook when a CVE is hot. Composes IOC pivot, detection rules, fix planning, and VEX in a single linear flow.

## Step 1: Load capabilities + memory

Read `.vulnetix/capabilities.yaml` and `.vulnetix/memory.yaml`. Capture detection_stack, soar, and any prior data on the vuln.

## Step 2: Confirm urgency

```bash
vulnetix vdb sightings "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/sightings.jq"
vulnetix vdb kev get "$ARGUMENTS" -o json 2>/dev/null | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/kev.jq"
```

Decide: **active** (sightings within 30 days OR in KEV) → run all steps. **dormant** → suggest `/vulnetix:remediation` instead and exit.

## Step 3: Containment intel

```bash
vulnetix vdb iocs "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/iocs.jq"
vulnetix vdb attack-techniques "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/attack-techniques.jq"
```

Surface top 5 IOCs and the ATT&CK technique chain.

## Step 4: Detection deployment

If `derived.detection_stack` non-empty, fetch rules for each available family and write to `.vulnetix/detection/$ARGUMENTS/` (delegate to the same logic as `/vulnetix:detection-rules`, inline). Skip families absent from the stack.

## Step 5: Patch path

```bash
vulnetix vdb fixes "$ARGUMENTS" -V v2 -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/fixes.jq"
vulnetix vdb remediation plan "$ARGUMENTS" -V v2 -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/remediation.jq"
```

If a patch is available and the package is in this repo, suggest `/vulnetix:fix $ARGUMENTS` and offer to apply it inline (with user confirmation). If no patch, surface workarounds via `vdb workarounds $ARGUMENTS -V v2`.

## Step 6: VEX

Update memory with the chosen decision (`fix-applied`, `mitigated`, or `under_investigation`). Generate VEX:

```bash
vulnetix triage --provider vulnetix --vex-format openvex -o json > .vulnetix/vex/${ARGUMENTS}.${TIMESTAMP}.vex.json
```

## Step 7: Render incident report

```
Incident: $ARGUMENTS
Status: active | dormant
First sighting: <date>   Sources: <count>
KEV: <yes/no, deadline if any>
ATT&CK: <T-IDs>
Top IOCs: <ips/asns>
Detection rules deployed: <families and counts>
Patch available: <yes/no>
Repo affected: <yes/no, packages>
Decision: <choice>
VEX: <path>
Next:
- /vulnetix:verify-fix <id>
- /vulnetix:vex-publish --upload
```

## Memory update

Append `event: incident-respond` with stage outcomes to the vuln entry. Single consolidated write.

## Edge cases & gotchas

- Stage 1 (parallel intel pull) hits 6 endpoints simultaneously — rate-limit retries will delay the whole batch. Add `--silent` to suppress retry chatter.
- Active classification = KEV-listed OR sightings within 30d OR EPSS > 0.5. Dormant CVEs get a one-line bailout and the skill exits.
- Detection deployment writes to `.vulnetix/detection/<VULN_ID>/` only for families in `derived.detection_stack`. Empty stack = no rule files written.
- Workarounds are pulled via `vdb workarounds <id> -V v2` if no patch is available; the V2 endpoint is partial in some environments.
- VEX is generated even if the user has not made a decision yet — the default mapping uses `status: under_investigation` → `under_investigation`. Pass `--final-only` to publish only decided items.
- Memory coordination: `--disable-memory` on all inner calls, single consolidated write at end with `event: incident-respond`.
