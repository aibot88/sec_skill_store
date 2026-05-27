---
name: dep-add-guard
description: 'Pre-add risk gate for a new dependency — composes vuln history (`vdb vulns`), AI-malware check (`vdb ai-malware`), license compatibility, EOL status, maintainer health, version-lag — into one ALLOW/WARN/BLOCK verdict. Use when about to `npm install` / `pip install` / `cargo add` something new, vetting alternatives, or hardening the CI pre-add policy.'
argument-hint: <package-name> [--version X] [--ecosystem npm|pypi|...]
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "add dependency"
  - "install package"
  - "new dep"
  - "add library"
  - "require package"
chain:
  - package-search
  - dep-resolve
outputBudget: short
cooldown: per-session
---

# Vulnetix Dependency-Add Guard Skill

## Use when

- Stop-think: about to run `npm install` / `pip install` / `cargo add` something new.
- Choosing between candidate packages (Pix verdict tells you which is safer).
- CI policy: block PRs that add packages flagged BLOCK.
- Auditing a recently-added dep that was not gated at addition time.
- Cross-checking the `dep-install-gate` hook's warning with full-detail follow-up.

## Don't use for

- Generic package info — use `/vulnetix:package-search`.
- Resolving a conflict — use `/vulnetix:dep-resolve`.
- Single-CVE lookup — use `/vulnetix:vuln`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Refines `/vulnetix:package-search` into an explicit "should I add this?" verdict.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Default `--ecosystem` from `derived.primary_package_manager` if not provided.

## Step 2: Parallel intelligence pulls

```bash
vulnetix vdb packages search "$PACKAGE" --ecosystem "$ECO" -o json & | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/packages.jq"
vulnetix vdb vulns "$PACKAGE" -o json & | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/vulns.jq"
vulnetix vdb ai-malware list --package "$PACKAGE" -o json & | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/ai-list.jq"
vulnetix vdb purl "pkg:${ECO}/${PACKAGE}@${VERSION:-latest}" -o json & | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/purl.jq"
wait
```

## Step 3: Apply gates

Verdict = WORST of these checks:
- **block**: known malware/typosquat hit
- **block**: critical CVE in target version with no fix
- **warn**: copyleft license against permissive codebase
- **warn**: low maintainer-health (single maintainer, no commits in 12mo, low downloads)
- **warn**: EOL upstream
- **warn**: version-lag (>3 minor versions behind)
- **allow**: none of the above

## Step 4: Render

```
Dependency: <package>@<version> (<ecosystem>)

Verdict: ALLOW | WARN | BLOCK

| Check | Result | Detail |
| Vuln history | 3 known | 0 affecting target version |
| Malware / typosquat | clean | no AI-malware family hit |
| License | MIT | OK |
| Maintainer health | 1 maintainer, last commit 14mo ago | warn |
| EOL | not EOL | OK |
| Version lag | latest=4.2.0, requested=4.0.1 | OK |
```

If BLOCK, refuse and suggest alternatives via `vulnetix vdb packages search --ecosystem $ECO --safe`.

## Memory update

Append `event: dep-add-guard` to `.vulnetix/memory.yaml` with the verdict and rationale.

## Edge cases & gotchas

- Verdict logic = max(any BLOCK signal, all WARN signals, baseline ALLOW). One BLOCK signal forces BLOCK regardless of others.
- BLOCK triggers: malware/typosquat hit OR critical CVE with no fix in target version.
- WARN triggers: copyleft license vs permissive codebase, single-maintainer-no-recent-commits, EOL upstream, version-lag > 3 minor versions.
- Maintainer-health signals come from package-registry metadata — npm download count, last-publish date. Newer packages with one maintainer can be unfairly flagged.
- 4 parallel CLI calls — sequential pacing helps on rate-limited tiers.
- Memory write records the verdict + rationale even if the user decides not to install — useful for retrospective review.
