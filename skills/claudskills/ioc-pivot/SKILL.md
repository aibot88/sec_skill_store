---
name: ioc-pivot
description: 'IOC pivots for a CVE — top IPs, ASNs, geo distribution, ATT&CK technique chain, Shadowserver scan counts (1d/7d/30d/90d averages), CrowdSec community sightings, merged in-the-wild timeline. Optional STIX 2.1 bundle export for Splunk / Sentinel / Cortex / Tines ingestion. Use when investigating an active CVE, building a blocklist, exporting to SOAR, or correlating with internal SIEM logs.'
argument-hint: <vuln-id>
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "ioc"
  - "sightings"
  - "indicators of compromise"
  - "stix"
chain:
  - detection-rules
  - attack-mapping
outputBudget: medium
cooldown: per-session
---

# Vulnetix IOC Pivot Skill

## Use when

- A CVE is actively exploited and you need a blocklist of attacker IPs/ASNs to feed your edge firewall.
- Exporting to STIX 2.1 for Splunk / Sentinel / Cortex / Tines ingestion.
- Building a geo-distribution view of attack origin for an executive brief.
- Correlating CrowdSec community sightings with internal SIEM detections.
- Mapping the ATT&CK technique chain associated with the exploit.

## Don't use for

- Generating detection rules for the IDS — use `/vulnetix:detection-rules`.
- Single-CVE enrichment without IOC focus — use `/vulnetix:vuln`.
- Cross-CVE IOC search by country/ASN — use `vulnetix vdb iocs list` directly (this skill is per-CVE).

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Builds a SOC-grade IOC view for a single CVE — combines `vdb iocs` (CrowdSec sightings + Shadowserver counts) and `vdb sightings` (merged timeline) into a single report. Exports STIX bundle when the user has a SOAR sink.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Capture `derived.soar` to decide STIX export; capture `derived.detection_stack` to suggest follow-up rule fetches.

## Step 2: Fetch IOCs

```bash
vulnetix vdb iocs "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/iocs.jq"
```

Pass through optional flags: `--country`, `--asn`, `--limit`, `--since`. Capture: top IPs, ASNs, country distribution, ATT&CK techniques observed, Shadowserver scan counts.

## Step 3: Fetch sightings timeline

```bash
vulnetix vdb sightings "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/sightings.jq"
```

Merge timeline events (first-seen, peak, last-seen) by source.

## Step 4: Render SOC report

Sections:
- **Summary** — first-seen, last-seen, peak day, total Shadowserver scans
- **Top IOCs** — IPs / ASNs / countries (top 10 each, in tables)
- **ATT&CK techniques** — list with counts
- **Sources** — CrowdSec, Shadowserver, etc.
- **Timeline** — Mermaid `gantt` or `timeline` diagram if 5+ events

## Step 5: STIX export (conditional)

If `derived.soar == "stix"` OR user passes `--format stix`:

```bash
vulnetix vdb iocs list --cve-id "$ARGUMENTS" --format stix > .vulnetix/iocs/${ARGUMENTS}.stix.json
```

Note the file path in the report and suggest the user import into Splunk / Sentinel / Cortex / Tines.

## Step 6: Suggested follow-ups

- If `detection_stack` non-empty → `/vulnetix:detection-rules $ARGUMENTS`
- If active in-the-wild → `/vulnetix:incident-respond $ARGUMENTS` (agent)
- If installed in repo (cross-check `memory.yaml`) → `/vulnetix:verify-fix $ARGUMENTS` after patch

## Memory update

Append `event: ioc-pivot` to the vuln entry with summary stats (peak day, top country, source count).

## Edge cases & gotchas

- `vdb iocs <id>` (bare arg) returns help text. Use `vdb iocs get <id>` for per-CVE; or `vdb iocs list --cve-id <id>` for cross-CVE search.
- `vdb iocs get <id> -o json` writes to a file LITERALLY named `json` in cwd. Use `-o /dev/stdout` to pipe.
- Server caps `.sightings[]` at ~200 entries per CVE; the API has more — paginate with `vdb iocs list --limit/--offset` if needed.
- STIX export needs `--format stix` on the LIST endpoint (`vdb iocs list --cve-id <id> --format stix`), not the GET endpoint.
- Older CVEs return empty `.sightings[]` even when actively exploited — Shadowserver/CrowdSec data is recent-only (post-2024).
- `shadowserver.topCountries` is sometimes an empty array even when scans are detected — the field is populated lazily on the server.
