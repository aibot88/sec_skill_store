---
name: typosquat-check
description: 'Typosquat and malicious-package detection across installed dependencies (or a single prospective addition) — cross-checks AI-malware family intelligence, package-name similarity to known popular packages, low maintainer-health signals. Use when auditing a freshly-onboarded repo, vetting a single suspicious package, gating CI on supply-chain risk, or investigating an incident.'
argument-hint: "[<package-name>] | [--installed]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "typosquat"
  - "malicious package"
  - "supply chain"
  - "typo squatting"
chain:
  - dep-add-guard
outputBudget: short
cooldown: per-session
---

# Vulnetix Typosquat Check Skill

## Use when

- Onboarding: scan all installed deps for typosquat/malware matches.
- Vetting a single package that looks suspicious (`react-utill`, `lodash-utility`, etc.).
- CI gate: block any installed dep flagged BLOCK.
- Post-incident: cross-reference your installed deps against newly-discovered malware families.
- Investigating a single package after a vendor advisory mentions name-similarity attacks.

## Don't use for

- CVE-based vulnerability scanning — use `/vulnetix:sca-scan`.
- Generic package risk before adding — use `/vulnetix:dep-add-guard`.
- Detecting compromised packages via runtime behaviour — Pix is static-only.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

## Step 1: Decide mode

- Single-package: `$ARGUMENTS` is a name → check just that.
- `--installed`: read lockfile (per `derived.primary_package_manager`), check every direct dep.

## Step 2: Run gated scan + AI-malware lookup

```bash
vulnetix scan --block-malware -o json
vulnetix vdb ai-malware list -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/ai-list.jq"
vulnetix vdb packages search "$PACKAGE" --ecosystem "$ECO" -o json   # for similarity hits | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/packages.jq"
```

The `packages search` response includes typosquat-similarity scores against well-known package names.

## Step 3: Render

```
| Package | Version | Verdict | Reason |
| react-utill | 1.0.0 | BLOCK | typosquat of react-util (similarity 0.92), 0 stars, 14d old |
```

Verdicts: ALLOW / WARN / BLOCK.

## Step 4: Memory + .gitignore note

Append `event: typosquat-check` with verdicts to memory. If any BLOCK, surface a strong suggestion to remove the package and check git history (`git log -p -- <package-manifest-path>`).

## Edge cases & gotchas

- Similarity scoring is heuristic (Levenshtein + popularity weighting). Borderline names need human review.
- `--installed` mode reads the lockfile per `derived.primary_package_manager` — make sure the lockfile is up-to-date.
- `vdb ai-malware list --package <name>` returns matches across ecosystems; filter by `--ecosystem` for accuracy.
- BLOCK verdict is rare and high-signal; treat as urgent. Most flagged packages are WARN (borderline name + low maintainer signal).
- Removing a flagged package is destructive — review `git log -p -- <manifest>` BEFORE deletion to understand what code depends on it.
- False positives: legitimate packages with similar names to popular ones (e.g. typescript-eslint vs typescript) can score high — manual triage needed.
