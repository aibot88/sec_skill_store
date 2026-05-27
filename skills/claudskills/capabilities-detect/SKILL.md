---
name: capabilities-detect
description: 'Detect installed security binaries (nuclei, snort, yara, semgrep, syft, grype, trivy, cosign, gh, package managers) and repo signals (manifests, Dockerfiles, IaC, CI configs); write .vulnetix/capabilities.yaml. Use when starting a session, after installing a new tool (brew install yara), when other Pix skills emit "unknown capability" notes, or to force-refresh stale capability state.'
user-invocable: true
allowed-tools: Bash, Read
model: haiku
triggers:
  - "capabilities"
  - "probe environment"
  - "what tools"
  - "detect tools"
chain:
  - dashboard
outputBudget: short
cooldown: per-session
---

# Vulnetix Capabilities Detector

## Use when

- A session just started and `.vulnetix/capabilities.yaml` does not exist or is older than 24h.
- A new security tool was just installed (`brew install yara`, `pip install semgrep`) and you want subsequent Pix calls to pick it up.
- The repo gained a new manifest type, Dockerfile, or `*.tf` file and you want downstream skills to scope their behaviour.
- You need to inspect what Pix currently believes about the environment before debugging a skill.
- A downstream skill reports "unknown capability" or fetches rule families you cannot use.

## Don't use for

- Actually scanning code or dependencies — use `/vulnetix:sast-scan`, `/vulnetix:sca-scan`, or `/vulnetix:scan`.
- Running individual CLI lookups — use `/vulnetix:vuln`, `/vulnetix:exploits`, etc.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

This skill re-runs the capability probe and updates `.vulnetix/capabilities.yaml`. The file is read by every other Pix skill, hook, command, and agent to scope which Vulnetix CLI subcommands and external integrations (nuclei, snort, yara, semgrep, syft, grype, trivy, cosign, gh, package managers) are meaningful for the user's environment.

The session-start hook normally handles this automatically. Run this skill manually when:

- A new tool was just installed (e.g. `brew install yara`) and you want Pix to use it.
- The repo gained a new manifest, Dockerfile, or IaC layout.
- You want to inspect what Pix currently believes about your environment.

## Workflow

### Step 1: Force a refresh

```bash
VULNETIX_FORCE_DETECT=1 bash "${CLAUDE_PLUGIN_ROOT}/hooks/capabilities-detect.sh" --announce
```

If `${CLAUDE_PLUGIN_ROOT}` is not set in the user's shell, locate the plugin root via `$HOME/.claude/plugins/vulnetix` or run the script directly from the plugin checkout.

### Step 2: Render the result

Read `.vulnetix/capabilities.yaml` and present a compact summary to the user:

```
Capabilities (detected <timestamp>):
- Package manager: <derived.primary_package_manager>
- Containers in repo: <derived.has_containers>
- IaC in repo: <derived.has_iac>
- CI configured: <derived.has_ci>
- Detection stack: <derived.detection_stack>
- SBOM stack: <derived.sbom_stack>
- SOAR sink: <derived.soar>
- Vulnetix auth: <derived.auth_status>
```

Then surface relevant follow-ups based on what was found, e.g. "Trivy is installed — `/vulnetix:container-scan` will compose its output", "No SAST binary detected — `/vulnetix:sast-scan` will use built-in Vulnetix rules only".

### Step 3: Output policy

This skill never modifies application code, manifests, or memory.yaml. It only refreshes `capabilities.yaml`.

## Schema reference

See `website/content/docs/data-structures/capabilities-yaml.md` for the full schema. Three top-level sections: `binaries`, `repo`, `derived`. The `derived.detection_stack`, `derived.sbom_stack`, `derived.primary_package_manager`, and `derived.has_*` flags are the fields most other skills consult.

## Edge cases & gotchas

- `command -v` runs in the user's shell; binaries surfaced only via fish functions or zsh autoload may not be detected. Re-run via `VULNETIX_FORCE_DETECT=1 ...` after installing.
- Cache TTL is 24h. A fresh tool install during a session needs a manual re-detect.
- Probes 41 binaries × 30 repo signals. On very large monorepos the find pass can take 1-2 seconds — first-session cost only.
- Auth-status probe ignores VULNETIX_API_KEY in non-interactive shells if the env var is set after shell start.
- The `derived.detection_stack` array reflects callable binaries only — having a `*.rules` file in the repo without `snort` installed still yields an empty detection stack.
