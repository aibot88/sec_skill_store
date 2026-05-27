---
name: sast-scan
description: 'Static application security testing (SAST) for changed source files — Vulnetix''s built-in rule set plus optional Semgrep augmentation when `.semgrep` config is present. Use when reviewing a PR for code-level vulnerabilities, scanning a feature branch before merge, gating CI on critical findings, or running rule-specific checks for a known weakness class.'
argument-hint: "[--rule-id ID] [--paths file1 file2] [--baseline]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "sast"
  - "static analysis"
  - "scan source"
chain:
  - secure-code-write
  - verify-fix
outputBudget: medium
cooldown: per-session
---

# Vulnetix SAST Skill

## Use when

- Pre-commit / pre-merge: scan changed source files for SAST findings.
- Targeted rule check: "did we just write an XXE pattern?" via `--rule-id VNX-XXE-001`.
- CI gate: exit non-zero if SAST finds critical-severity issues.
- Audit a specific weakness class with `--paths <dir> --rule-id VNX-CWE-89-*`.
- Augment Vulnetix's rules with the repo's own Semgrep policy.

## Don't use for

- Dependency vulnerability scanning — use `/vulnetix:sca-scan`.
- Secret detection — use `/vulnetix:secret-scan`.
- Container/IaC scanning — use `/vulnetix:container-scan` / `/vulnetix:iac-scan`.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Static analysis on source code. Capability-aware: optionally augmented with the user's own Semgrep rules.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Note `binaries.semgrep`, `repo.semgrep_config`.

## Step 2: Decide scope

If `--paths` given → scan those paths. Else scan files changed since `git merge-base origin/main HEAD` (or whole repo if not a git repo).

## Step 3: Run scan

```bash
vulnetix sast --paths "$PATHS" -o json-sarif > .vulnetix/sast.${TIMESTAMP}.sarif
```

If `--rule-id` provided, pass through.
If `--baseline`, also run `vulnetix scan --evaluate-sast --list-default-rules -o json` to record the rule set used.

## Step 4: Augment with local Semgrep (conditional)

If `binaries.semgrep: true` AND `repo.semgrep_config: true`:

```bash
semgrep --config .semgrep --json --quiet "$PATHS" > .vulnetix/sast.semgrep.${TIMESTAMP}.json
```

Merge findings into the SARIF report (de-duped by file:line:rule).

## Step 5: Render

| Severity | Rule | File:Line | Message | Source |

Group by severity (critical → low). Suggest `/vulnetix:secure-code-write` for repeated rule violations.

## Memory update

If running on a PR / branch, write a `.vulnetix/sast/<branch>.summary.yaml` with finding counts so `/vulnetix:code-review-security` can pick it up.

## Edge cases & gotchas

- Scope defaults to files changed vs `origin/main`; pass `--paths` for explicit scope. CWD without a manifest = empty results.
- Output is SARIF — pipe through a SARIF viewer (VS Code SARIF Viewer extension) or render the JSON yourself.
- Semgrep augmentation requires `binaries.semgrep: true` AND `repo.semgrep_config: true`. Otherwise the skill silently runs Vulnetix rules only.
- Built-in rules are organisation-agnostic; rule IDs like `VNX-GQL-004` (GraphQL injection) are not customisable per-repo.
- Findings are deduped by `<file>:<line>:<rule_id>` across both sources — same logical finding from Semgrep + Vulnetix appears once.
- Performance: 10K+ file repos benefit from `--paths "src/**/*.ts"` instead of full-repo scan.
