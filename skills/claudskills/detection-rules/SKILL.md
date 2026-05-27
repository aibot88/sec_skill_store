---
name: detection-rules
description: 'IDS/IPS detection content for a CVE — Snort/Suricata-compatible rules, YARA signatures, ProjectDiscovery Nuclei templates, traffic-filter rules. Capability-aware: skips families when the binary is not installed (no Snort = no Snort output). Use when deploying defences for a CVE without a patch, augmenting SAST with active detection, or feeding the SOC engineering pipeline.'
argument-hint: <vuln-id>
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "detection rules"
  - "snort"
  - "yara"
  - "nuclei"
  - "ids rules"
chain:
  - exploit-test
  - verify-fix
outputBudget: short
cooldown: per-session
---

# Vulnetix Detection Rules Skill

## Use when

- A CVE has no patch yet and you need detection-only mitigation.
- Augmenting SAST with active runtime detection (Snort/Suricata).
- Feeding the SOC engineering pipeline with rule files.
- Building a Nuclei scan template for an authorised target assessment.
- Hardening a YARA ruleset against a newly-discovered malware family.

## Don't use for

- Executing the rules — this skill writes files; the user runs the engine.
- Patching the underlying issue — use `/vulnetix:fix`.
- Single-CVE enrichment — use `/vulnetix:vuln`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Pulls IDS/IPS, malware-detection, and active-scan content for a CVE. Capability-aware: only fetches rule families the user can actually use.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Capture `derived.detection_stack`. If empty, prompt:

```
No detection tooling found (snort, suricata, yara, nuclei, semgrep). I can still fetch the raw rules — proceed?
```

If the user accepts, treat the stack as `[snort, yara, nuclei]` for completeness. Otherwise abort with a one-liner pointing at install docs.

## Step 2: Fetch each available family

For each family in `detection_stack`:

```bash
# Snort/Suricata
vulnetix vdb snort-rules get "$ARGUMENTS" -o json
vulnetix vdb traffic-filters "$ARGUMENTS" -o json

# YARA
vulnetix vdb yara-rules get "$ARGUMENTS" -o json

# Nuclei
vulnetix vdb nuclei get "$ARGUMENTS" -o json
```

Skip families absent from `detection_stack` to avoid wasted API calls.

## Step 3: Save rule files (raw form)

Write rule content to `.vulnetix/detection/<VULN_ID>/`:
- `snort.rules` (concat of all Snort rule bodies)
- `suricata.rules` (if family present)
- `vuln.yar` (concat of YARA rules)
- `nuclei-<id>.yaml` (one per template)

Use `--format rules` / `--format yaml` against the same subcommand:

```bash
vulnetix vdb snort-rules list --cve-id "$ARGUMENTS" --format rules > .vulnetix/detection/$ARGUMENTS/snort.rules
vulnetix vdb yara-rules list --cve-id "$ARGUMENTS" --format rules > .vulnetix/detection/$ARGUMENTS/vuln.yar
vulnetix vdb nuclei get "$ARGUMENTS" --format yaml > .vulnetix/detection/$ARGUMENTS/nuclei.yaml
```

## Step 4: Render report

For each family, list:
- Rule count + highest signature severity
- File path on disk
- A copy-pasteable invocation hint based on installed binaries:
  - `snort -c snort.conf -A console` (only if `binaries.snort: true`)
  - `yara vuln.yar /path/to/scan` (only if `binaries.yara: true`)
  - `nuclei -t .vulnetix/detection/$ARGUMENTS/nuclei.yaml -u <target>` (only if `binaries.nuclei: true`)

## Step 5: Memory update

Append `event: detection-rules` with counts per family to the vuln entry.

## Notes

- This skill never executes rules. The user (or `/vulnetix:exploit-test`) runs them.
- Filter is honest: if YARA is missing, the YARA section is omitted from the report and from disk writes.

## Edge cases & gotchas

- Each family is fetched ONLY if the binary is in `derived.detection_stack`. Override by passing `--force` if you want raw rule output regardless.
- `vdb snort-rules`, `vdb yara-rules`, `vdb nuclei` accept `--format rules|yaml` for non-JSON output (the engine's native format).
- Some CVEs return zero rules across all families — that means no community detection content exists, not that the skill failed.
- YARA rules can have multiple hash-only matchers; if your YARA build was compiled without hash-module support, those rules fail silently.
- Nuclei templates require a target URL/IP at invocation time; the skill produces the template, not the scan.
- `vdb traffic-filters <id>` returns Snort-format rules tagged for Suricata compatibility — confirm Suricata accepts the rule before deploying to Suricata.
