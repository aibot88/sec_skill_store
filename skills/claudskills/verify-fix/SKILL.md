---
name: verify-fix
description: 'Post-fix verification — re-scan the repo, gate on `--exploits weaponized --severity high`, recheck the specific CVE against the new installed version, write the verdict to `.vulnetix/memory.yaml`. Use when confirming a fix landed, validating a version bump did not introduce regressions, or producing a clean-scan attestation for compliance.'
argument-hint: <vuln-id>
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "verify fix"
  - "confirm fix"
  - "fix worked"
  - "exploit gone"
chain:
  - vex-publish
outputBudget: short
cooldown: per-session
---

# Vulnetix Fix Verification Skill

## Use when

- You just applied a fix via `/vulnetix:fix` and need PASS/FAIL confirmation.
- Validating a peer-dep upgrade chain did not introduce new vulnerabilities.
- Producing a clean-scan attestation for a compliance bundle.
- Pre-release: confirming all triaged P1/P2 items are resolved.
- Setting decision status from `under_investigation` to `fixed` with audit trail.

## Don't use for

- Initial scanning — use `/vulnetix:scan` or `/vulnetix:soc-triage`.
- Applying the fix — use `/vulnetix:fix` first.
- Multi-CVE upgrade verification — use `@dep-upgrade-orchestrator` agent.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

Run after `/vulnetix:fix` (or any manual remediation) to confirm the vulnerability is gone and no regressions appeared.

## Step 1: Load capabilities + memory

Read `.vulnetix/capabilities.yaml` and `.vulnetix/memory.yaml`. Find the entry for `$ARGUMENTS`. Capture: package, fixed_version, manifest path.

## Step 2: Pre-flight

```bash
# Ensure the manifest changed since last scan
git diff --name-only HEAD~5 -- "<manifest_path>" 2>/dev/null
```

If no recent change to the manifest, warn the user and proceed.

## Step 3: Run gated scan

```bash
vulnetix scan \
  --evaluate-sca \
  --severity high \
  --exploits weaponized \
  -o json
```

Capture exit code. Non-zero means a critical/high vuln with weaponized exploit signal still present.

## Step 4: Targeted recheck of the specific CVE

```bash
vulnetix vdb fixes "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/fixes.jq"
vulnetix vdb vuln "$ARGUMENTS" -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/vuln.jq"
```

Cross-check: does the *new* installed version fall outside the affected range?

## Step 5: Render verdict

```
Fix verification: <PASS | FAIL>
Vuln: $ARGUMENTS
Package: <name>
Pre-fix version: <prev>
Post-fix version: <new>
Affected range: <range>
Within affected range now? <yes/no>
Scan gate (high+weaponized): <pass/fail>
Other regressions introduced: <count>  (list top 5 if any)
```

## Step 6: Update memory

- On PASS: set `status: fixed`, `decision.choice: fix-applied`, append `event: fix-verified`.
- On FAIL: keep `status: affected`, append `event: fix-verification-failed` with reason.

## Step 7: Follow-ups on FAIL

- Suggest `/vulnetix:dep-resolve` if version bump is blocked by a transitive constraint.
- Suggest `/vulnetix:safe-harbor-resolver` (agent) if multiple manifests conflict.

## Edge cases & gotchas

- The gated scan (`scan --exploits weaponized --severity high`) returns exit code 1 on findings — wrap with `|| true` if you want to capture without aborting the surrounding shell.
- Recheck calls `vdb fixes` and `vdb vuln` — pipe both through the jq filters to avoid 4MB raw payloads in your context.
- `decision.choice: fix-applied` is one of 8 closed-enum values — never write arbitrary strings; the dashboard skill renders them under "Unknown".
- If the manifest was edited but the lockfile not regenerated (`npm install` was skipped), the scan reports the OLD vulnerability even though the manifest looks correct. Always run `<pm> install` before verify.
- Cross-check: the affected range in the vuln response should EXCLUDE the post-fix version. If both old and new versions are in the range, the bump did not reach a safe version.
- Memory write is single-consolidated at the end (with `--disable-memory` on inner CLI calls) — never run verify-fix concurrently from the same session.
