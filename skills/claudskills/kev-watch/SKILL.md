---
name: kev-watch
description: 'CISA + EU KEV (Known Exploited Vulnerabilities) catalog watch — pull recent KEV additions, intersect with installed dependencies, surface entries with imminent due dates. Use when checking if you have KEV-listed CVEs in your repo, monitoring CISA additions on a schedule, or producing a deadline-driven action list with `--since` filtering.'
argument-hint: "[--since YYYY-MM-DD] [--catalog cisa|eu|all]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
triggers:
  - "kev"
  - "known exploited"
  - "cisa kev"
chain:
  - soc-triage
  - fix
outputBudget: short
cooldown: per-session
---

# Vulnetix KEV Watch Skill

## Use when

- You want to know "are any of our deps in CISA KEV right now?".
- Monitoring CISA additions since a date (`--since 2026-04-01`).
- Producing a deadline-driven action list — items with KEV due dates within 14 days.
- Choosing between competing CVEs to patch first based on KEV listing.
- Pre-audit: ensuring no KEV items remain open past their due date.

## Don't use for

- Per-CVE enrichment — use `/vulnetix:vuln`.
- Daily SOC pull — use `/vulnetix:soc-triage` (KEV is one signal among many there).
- Single-KEV lookup by CVE — use `vulnetix vdb kev get <id>` directly.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Pulls the KEV catalog and intersects with installed packages — the "what's on fire and is it in my repo?" view.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Use `derived.primary_package_manager` to focus the lockfile scan.

## Step 2: Pull KEV catalog

```bash
vulnetix vdb kev list $ARGUMENTS -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/kev.jq"
```

Honor `--since`, `--catalog`. Default `--catalog all`, `--since` = 30 days ago.

## Step 3: Cross-reference repo

For each KEV entry:
1. Extract affected package names.
2. Grep lockfiles for matches (npm: package-lock.json/pnpm-lock.yaml; pypi: poetry.lock/uv.lock; etc.).
3. Mark presence: direct / transitive / not-found.

If `.vulnetix/scans/*.cdx.json` SBOM exists, prefer that for matching.

## Step 4: Render report

```
KEV catalog hits (window: <since>)
Total KEV entries scanned: N | In your repo: M

| CVE | Package | Installed | KEV deadline | Days remaining | Action |
```

Highlight rows where deadline is < 14 days as URGENT.

## Step 5: Suggested follow-ups

- Each in-repo KEV item → `/vulnetix:fix <id>` and `/vulnetix:detection-rules <id>` (if detection stack present)
- Past-deadline items → escalate via `/vulnetix:incident-respond <id>` (agent)

## Memory update

For each in-repo match, ensure a memory entry exists with a `kev_deadline` field and `event: kev-watch` history line.

## Edge cases & gotchas

- `vdb kev list -o json` writes to file `json`; use `-o /dev/stdout`.
- `vdb kev list` returns multi-source items (CISA, vulncheck, Vulnetix-internal); `dueDate` is populated only for CISA-source entries. Other sources have `dueDate: null`.
- `requiredAction` is null for non-CISA sources; only CISA mandates carry the action text.
- The Vulnetix KEV catalog is the V2 endpoint (`vdb kev list --catalog vulnetix`) and is BROADER than CISA KEV — includes weaponised CVEs not yet in CISA.
- `knownRansomwareCampaignUse` is `"Known"` / `"Unknown"` (strings, not booleans). Check string equality, not truthiness.
- `--since` filter is server-side and very fast; client-side date math will be slower for large catalogs.
