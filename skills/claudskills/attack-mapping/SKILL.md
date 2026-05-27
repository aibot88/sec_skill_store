---
name: attack-mapping
description: 'MITRE ATT&CK technique mapping for a CVE or every entry in `.vulnetix/memory.yaml`. Use when planning detection coverage gaps, mapping a CVE to defender controls, building an executive heatmap of repo risk by tactic, or correlating with internal D3FEND counter-techniques.'
argument-hint: "[<vuln-id>] | [--all-tracked]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
triggers:
  - "map to ATT&CK"
  - "attack mapping"
  - "techniques used"
  - "mitre"
chain:
  - vuln
  - detection-rules
outputBudget: short
cooldown: per-session
---

# Vulnetix ATT&CK Mapping Skill

## Use when

- You need to know which ATT&CK techniques a CVE enables (Initial Access? Execution? Persistence?).
- Building an executive heatmap: which tactics dominate this repo's risk profile.
- Mapping current detection coverage gaps via ATT&CK → D3FEND.
- Correlating multiple CVEs to a shared technique chain (e.g. T1190 + T1059).
- Producing input for a purple-team exercise.

## Don't use for

- Generating detection rules for the IDS — use `/vulnetix:detection-rules`.
- Single-CVE deep-dive — use `/vulnetix:exploits`.
- IOC pivots — use `/vulnetix:ioc-pivot`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Produces an ATT&CK technique view of repo risk. Run with a single vuln-id for a focused mapping, or `--all-tracked` to roll up every entry in `.vulnetix/memory.yaml`.

## Step 1: Decide mode

If `$ARGUMENTS` matches a vuln-id pattern → single mode. Else if it contains `--all-tracked` → roll-up mode reading every `vulnerabilities.*` entry in `.vulnetix/memory.yaml` (skip those with status `not_affected` or `fixed`).

## Step 2: Fetch ATT&CK data per vuln

```bash
vulnetix vdb attack-techniques "$VULN_ID" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/attack-techniques.jq"
```

Capture: technique IDs (T####), tactic, sub-technique, observed-in-wild count.

## Step 3: Render

**Single mode** — table of techniques with tactic + observation count. Mermaid flowchart from kill-chain tactic → technique → vuln.

**Roll-up mode** — a heatmap-style table:

```
| Technique | Tactic | Vuln count | Top affected packages |
|-----------|--------|-----------|----------------------|
| T1190 | Initial Access | 5 | log4j-core, struts2 |
```

Ranking: by vuln count descending. Top 20 only; total in summary footer.

## Step 4: Suggested follow-ups

- For high-frequency techniques → fetch detection rules for the top vulns: `/vulnetix:detection-rules <id>`
- For Initial Access / Execution tactics → `/vulnetix:soc-triage --severity critical`

## Memory update

Append `event: attack-mapping` with technique IDs to each touched vuln entry.

## Edge cases & gotchas

- `vdb attack-techniques <id>` (bare) returns help text. Use `vdb attack-techniques get <id>`.
- `vdb attack-techniques get <id> -o json` writes to file `json`; use `-o /dev/stdout`.
- `.attackTechniques[]` is OFTEN EMPTY for older CVEs (pre-2024 enrichment gap) — empty array does not mean "no techniques associated", it means "no mapping captured in this corpus".
- `--all-tracked` mode reads memory.yaml and can be slow for repos with 100+ tracked vulns; one network round-trip per vuln.
- Technique names (`name` field) are sometimes null in the response; the jq filter falls back gracefully.
- D3FEND counter-techniques are referenced but not inlined — the skill links to the MITRE D3FEND page rather than embedding the full counter-technique catalog.
