---
name: thirdit
description: |
  Scans and analyses third-party dependencies and IaC configurations for security vulnerabilities.

  - User asks to scan dependencies, libraries, or third-party components
  - User mentions "thirdit", "SCA", "dependencies", "vulnerable libraries", "CVE"
  - User wants to check IaC files (Dockerfiles, Kubernetes manifests, cloud configs)
  - User asks "what third-party vulnerabilities do I have?"

allowed-tools:
  - Read
  - Grep
  - mcp_veracode_local-sca-scan
  - mcp_veracode_local-sca-findings
  - mcp_veracode_local-iac-findings
license: Apache-2.0
compatibility: Requires Veracode MCP server connection and authenticated Veracode account. Supports SCA and IaC analysis for all major package managers.
metadata:
  author: Dipsylala
  version: 1.0.0
---

# Third-Party Security Advisor

Scans and analyses third-party dependencies and IaC configurations for vulnerabilities and misconfigurations. Covers all major package managers (npm, pip, Maven, Gradle, Go modules, NuGet, etc.) and IaC formats (Dockerfile, Kubernetes, Terraform, etc.).

**Core Principle**: Real-world exploitability matters more than theoretical severity. A medium-CVSS vulnerability actively exploited in the wild outranks a critical-CVSS one with no known exploits.

## Step 1 — Run the scan

Run a local SCA scan against the workspace root. This populates both dependency vulnerability data and IaC misconfiguration data in a single pass.

## Step 2 — Retrieve dependency findings

Retrieve SCA findings with the default page size (10). If the summary indicates more than 10 findings at severity ≥ High, retrieve additional pages to get the full picture before analysing.

## Step 3 — Retrieve IaC findings

Retrieve IaC findings with the default page size (10). IaC issues are separate from dependency vulnerabilities — always check both.

## Step 4 — Prioritise and analyse

### Dependency vulnerability prioritisation

Order findings by this priority sequence:

1. **EPSS score > 0.1** — these have confirmed real-world exploitation activity; treat as urgent regardless of CVSS
2. **CVSS ≥ 7.0 (High/Critical)** with a known fix version available — actionable high risk
3. **CVSS ≥ 7.0 (High/Critical)** with no fix version — flag for replacement or removal consideration
4. **CVSS < 7.0** — lower priority unless EPSS is elevated

For each priority finding, determine the dependency type:
- **Direct dependency**: the application's own package manifest declares it. Upgrade directly.
- **Transitive dependency**: pulled in by another library. First check whether upgrading the *direct* parent to a newer version resolves it without a separate override. If not, identify whether the package manager supports a direct version override.

### IaC misconfiguration analysis

Group IaC findings by file first, then by severity. Common high-value checks to highlight:
- Container running as root
- Privileged containers
- Secrets in environment variables
- Missing resource limits
- Exposed ports without justification

## Step 5 — Present results

Structure your output as:

**Summary**: total dependency vulnerabilities by severity, number with EPSS > 0.1 (real-world risk), total IaC failures — and an overall risk statement in one sentence.

**Priority dependency findings** (top 3–5): for each:
- Component name, current version, affected CVE(s)
- EPSS score and what it means in plain language
- Whether it is direct or transitive, and the fix path
- Suggested safe version if available

**Priority IaC findings** (top 3–5): for each:
- File and check ID
- What the misconfiguration is and why it matters
- Concrete fix (e.g., add `USER nonroot`, remove `privileged: true`)

**What to address next**: recommend whether to use the `fixit` skill for dependency upgrades, or to manually address IaC issues (IaC fixes are typically one-line changes in config files).
