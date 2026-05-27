---
name: threat-feed
description: 'Daily threat-intel digest — AI-discovered vulnerabilities, AI-in-the-wild exploitation observations, AI-authored malware families, exploit-trends rollup, vendor-trends month-over-month deltas. Use when producing a weekly security newsletter, scanning for novel threats, monitoring vendors with rising CVE counts, or tracking AI-discovered vulns from the researcher leaderboard.'
argument-hint: "[--vendor X] [--ecosystem Y] [--limit N]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
triggers:
  - "threat intel"
  - "threat feed"
  - "weekly digest"
  - "ai discoveries"
chain:
  - soc-triage
  - kev-watch
outputBudget: medium
cooldown: per-session
---

# Vulnetix Threat Feed Skill

## Use when

- Producing a weekly threat-intel digest for the team.
- Scanning for novel AI-discovered vulnerabilities since last week.
- Monitoring a specific vendor (`--vendor microsoft`) for rising CVE counts.
- Tracking AI-authored malware families relevant to your stack.
- Spotting in-the-wild exploitation observations from the AI corpus.

## Don't use for

- Single-CVE deep-dive — use `/vulnetix:vuln` or `/vulnetix:exploits`.
- Repo-specific intersection — use `/vulnetix:soc-triage` or `/vulnetix:kev-watch`.
- Detection rule generation — use `/vulnetix:detection-rules`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Compact daily digest — five concurrent VDB calls merged into one report.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Use `derived.primary_package_manager` to choose default `--ecosystem` if not provided.

## Step 2: Fetch in parallel

```bash
vulnetix vdb ai-discoveries -o json --limit 20 | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/ai-list.jq"
vulnetix vdb ai-in-wild -o json --limit 20 | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/ai-list.jq"
vulnetix vdb ai-malware -o json --limit 10 | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/ai-list.jq"
vulnetix vdb exploit-trends -o json
vulnetix vdb vendor-trends -o json
```

Honor user `--vendor`, `--ecosystem` flags by passing them to each call where supported.

## Step 3: Render digest

Sections, each at most 5 rows:

1. **Newly discovered (AI researchers)** — CVE, package, CVSS, researcher
2. **Active in the wild** — CVE, package, sightings count, first-seen
3. **Malware families (AI-authored / AI-runtime)** — family, package targets, severity
4. **Exploit trends (rollup)** — Mermaid pie or bar chart by severity tier
5. **Vendor trends** — top 5 vendors by month-over-month CVE delta

## Step 4: Repo overlay (one extra section)

For each item across sections, mark `In repo?` if affected package is in lockfiles. Surface only the in-repo subset in a final "Concerns for this repo" table.

## No memory writes

This skill is read-only. No memory.yaml update.

## Edge cases & gotchas

- Five parallel VDB calls — `ai-discoveries`, `ai-in-wild`, `ai-malware`, `exploit-trends`, `vendor-trends`. Stagger by 1s if hitting community-tier rate limits.
- `vdb ai-discoveries` lists CVEs WITH a researcher attribution; absence does not mean undiscovered, it means "no AI researcher claimed it in our corpus".
- `vdb ai-malware` covers AI-authored OR AI-runtime-targeted families; the `.family` field disambiguates.
- `exploit-trends` rollup is a severity-tier histogram by count, not per-CVE — pair with `exploits-search` for drill-down.
- For `--vendor` filtering across the four AI endpoints, the field name varies (`vendor` vs `vendorProject` vs `productVendor`); the jq filter normalises to `.package // .family`.
- No user-specific filtering — `--ecosystem` is the only narrowing arg. Cross-correlate with installed deps client-side.
