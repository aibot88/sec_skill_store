---
name: cve
description: "Assess a CVE for exposure, exploitability, and remediation options across one or more repositories."
---

# CVE Triage

Use this skill when asked to investigate a vulnerability advisory (CVE), determine whether it affects your systems, and recommend a concrete response.

## Scope

This workflow is intentionally generic:
- no dependency on a specific MCP server
- no dependency on proprietary search tool names
- supports fallback paths when specialized tooling is unavailable

## Inputs

- `cveId` (for example `CVE-2026-12345`)
- optional target scope: one repo, multiple repos, or organization-wide
- optional severity/urgency constraints from the requester

## Workflow

### 1) Collect authoritative advisory details

Gather baseline facts from public advisory sources:
- NVD
- MITRE CVE
- GitHub Advisory Database
- vendor/runtime advisories when applicable

Capture:
- affected package/runtime and vulnerable versions
- fixed version(s) or mitigation status
- CVSS/vector and known exploit context

### 2) Identify potential exposure in your codebases

Use semantic code search if available. If unavailable, use repository-native search and dependency manifests.

Look for usage through:
- dependency manifests (`package.json`, `go.mod`, `pyproject.toml`, etc.)
- lockfiles
- container base images
- IaC and deployment manifests
- direct imports/usages in code

### 3) Determine actual exposure

For each impacted repo/service, classify:
- direct dependency vs transitive dependency
- production/runtime path vs dev/test-only path
- reachable attack surface vs non-reachable code path

### 4) Evaluate exploitability

Assess exploitability in context:
- Is vulnerable functionality reachable?
- Is attacker-controlled input involved?
- Is the component externally exposed?
- Are mitigating controls present (WAF, authz, network isolation, sandboxing)?
- Are there known active exploits?

### 5) Propose remediation options

Provide options with tradeoffs:
- upgrade to fixed version
- temporary mitigation/workaround
- compensating controls
- risk acceptance with explicit rationale and expiration date

Include rollout impact notes (breaking changes, migration risks, test scope).

## Output

Write `docs/cve-[CVE-ID].md` using this structure:

```markdown
# CVE Assessment: [CVE-ID]

## Advisory Snapshot
- Vulnerability: [summary]
- Affected components: [list]
- Fixed versions: [list or none]
- Severity: [score + rating]

## Exposure Summary
| Repo/Service | Dependency Type | Runtime Scope | Potentially Affected |
|--------------|-----------------|---------------|----------------------|
| ... | direct/transitive | prod/dev/test | yes/no |

## Exploitability Assessment
- Reachable path: [yes/no + why]
- External exposure: [yes/no + why]
- Existing mitigations: [list]
- Exploit activity observed: [yes/no/unknown]

## Risk Decision
- Status: [Action Required | Mitigated | Monitor | Not Applicable]
- Reasoning: [concise rationale]

## Recommended Actions
1. [Action]
2. [Action]
3. [Action]

## Verification Plan
- [How to validate remediation]
- [What tests/checks to run]
- [What evidence confirms closure]
```

## Quality Rules

- Be explicit about unknowns; do not guess exploitability.
- Distinguish "installed" from "exploitable".
- Distinguish production risk from dev/test-only risk.
- Prefer actionable recommendations over generic warnings.
- If no fix exists, provide mitigation and monitoring guidance.
