---
name: safe-version
description: 'Find the newest version of a package that is free of known vulnerabilities, capped by a `--max-major-bump` policy. Use when picking an upgrade target for a vulnerable dep, evaluating major-version churn risk, generating a "safe pin" for a lockfile, or building an `overrides` block.'
argument-hint: <package-name> [--ecosystem npm|pypi|...] [--max-major-bump 1]
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
triggers:
  - "safe version"
  - "newest safe"
  - "latest safe"
  - "upgrade target"
chain:
  - fix
  - dep-resolve
outputBudget: short
cooldown: per-session
---

# Vulnetix Safe Version Skill

## Use when

- Picking the upgrade target: "what is the newest safe version of express?".
- Building a pnpm/yarn override block with the safe version as the target.
- Evaluating major-version churn — `--max-major-bump 1` keeps you near the current major.
- Cross-checking which versions in a range are actually clean (the safe set is sometimes non-contiguous).
- Pre-pin decision: would pinning to vX.Y skip a known-vulnerable interval?

## Don't use for

- Listing every version — use `vulnetix vdb versions <package>`.
- Applying the bump — use `/vulnetix:fix` or `/vulnetix:dep-resolve`.
- Single-CVE lookup — use `/vulnetix:vuln`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

## Step 1: Load capabilities

Default `--ecosystem` from `derived.primary_package_manager`.

## Step 2: Pull versions and vulns

```bash
vulnetix vdb versions "$PACKAGE" --ecosystem "$ECO" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/versions.jq"
vulnetix vdb vulns "$PACKAGE" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/vulns.jq"
vulnetix vdb purl "pkg:${ECO}/${PACKAGE}@latest" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/purl.jq"
```

## Step 3: Compute safe set

For each version in the version list:
- Mark unsafe if any known vuln's affected range includes it
- Apply `--max-major-bump` cap (default 1) to limit churn

Pick the newest safe version that doesn't exceed the major-bump cap.

## Step 4: Render

```
Safe version of <package> (<ecosystem>):
Currently installed: <ver>
Latest published:   <ver>
Recommended safe:   <ver>   (skipping vulnerable: 4.16.0–4.17.2 affected by CVE-…)
Major-bump cap:     <n>
```

Suggest `/vulnetix:fix` or `/vulnetix:dep-resolve` to apply the bump.

## No memory writes

Read-only.

## Edge cases & gotchas

- `--max-major-bump` defaults to 1; pass 0 to stay within the current major (patch + minor only).
- Read-only — does not modify any manifests.
- Safe-version computation excludes pre-release tags (`-beta`, `-rc`); pass `--include-prerelease` to include them.
- `vdb versions <package>` returns versions across ALL ecosystems for the same package name — filter by `--ecosystem` to scope.
- Some versions in the response have `ecosystem: ""` (empty) for CVE-affected versions that do not map cleanly to a registry — ignore those for safe-version selection.
- Returns the NEWEST safe version, not the LOWEST-RISK — for risk-averse pinning, take the second-newest safe version (gives one minor of community soak time).
