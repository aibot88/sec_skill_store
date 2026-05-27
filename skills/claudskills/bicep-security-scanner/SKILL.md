---
name: bicep-security-scanner
description: >
  Scans Azure Bicep templates for security misconfigurations and compliance violations.
  Detects issues like public endpoints, missing encryption, overly permissive access,
  disabled logging, and insecure defaults. Produces a prioritized findings report with
  remediation guidance. USE FOR: Bicep security review, IaC security scanning,
  Azure resource hardening, pre-deployment security checks, compliance validation.
allowed-tools: Read, Grep, Glob, Bash, Edit
version: 1.0.0
---

# Bicep Security Scanner

Analyze Azure Bicep templates for security misconfigurations, compliance gaps, and hardening opportunities. This skill scans `.bicep` files in the repository, identifies security issues, and provides actionable remediation with corrected Bicep snippets.

## When to Use

- Before deploying Bicep templates to any environment
- During pull request review of infrastructure changes
- When auditing existing IaC for security posture
- When preparing for compliance assessments (CIS, Azure Security Benchmark)

## Analysis Procedure

### Step 1: Discover Bicep Files

Use glob to find all `.bicep` files in the repository:

```
**/*.bicep
```

Also check for `bicepconfig.json` to understand any linter rules already in place.

### Step 2: Run the Python Scanner

Execute the embedded Python scanner against discovered files to extract resource definitions and flag known anti-patterns:

```bash
python3 "$(dirname "$0")/scripts/scan_bicep.py" --path <repo-root>
```

The scanner checks for:
- Storage accounts without HTTPS-only enforcement
- Storage accounts with blob public access enabled
- SQL servers without auditing enabled
- Key Vaults with soft delete disabled
- Network Security Groups with unrestricted inbound rules (0.0.0.0/0 on sensitive ports)
- App Services without HTTPS enforcement
- Virtual Machines without disk encryption
- Public IP addresses on resources that should be private
- Missing diagnostic settings / logging
- Resources deployed without managed identity

### Step 3: Deep Analysis

For each Bicep file, perform contextual analysis beyond pattern matching:

1. **Parameter defaults** — Check if security-sensitive parameters have insecure defaults
2. **Conditional deployments** — Verify security controls aren't conditionally skipped
3. **Module references** — Trace module calls to ensure child modules are also secure
4. **Output exposure** — Flag any outputs that leak secrets, connection strings, or keys
5. **API versions** — Flag deprecated API versions that may lack security features

### Step 4: Generate Report

Produce a findings report organized by severity:

#### Severity Levels

| Level | Description |
|-------|-------------|
| 🔴 Critical | Immediate risk — public exposure, missing encryption at rest, credential leakage |
| 🟠 High | Significant risk — overly permissive network rules, disabled logging |
| 🟡 Medium | Moderate risk — missing best practices, insecure defaults |
| 🔵 Low | Informational — optimization opportunities, minor hardening |

#### Report Format

For each finding:

```
### [SEVERITY] Finding Title

**Resource**: `resource.symbolicName` (resource type)
**File**: `path/to/file.bicep` (line N)
**Issue**: Description of the security concern
**Risk**: What could go wrong if unaddressed
**Remediation**:

\`\`\`bicep
// Corrected configuration
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  properties: {
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
  }
}
\`\`\`
```

### Step 5: Offer Remediation

After presenting findings, offer to apply fixes directly to the Bicep files using the Edit tool. Group fixes by file and apply them in order.

## Security Rules Reference

### Storage Accounts
- `supportsHttpsTrafficOnly` must be `true`
- `allowBlobPublicAccess` must be `false`
- `minimumTlsVersion` must be `TLS1_2`
- `networkAcls.defaultAction` should be `Deny`
- Encryption with customer-managed keys for sensitive data

### Key Vault
- `enableSoftDelete` must be `true`
- `enablePurgeProtection` must be `true`
- `enableRbacAuthorization` should be `true`
- Network ACLs should restrict access

### SQL / Database
- `minimalTlsVersion` must be `1.2`
- Auditing and threat detection must be enabled
- Transparent Data Encryption must be enabled
- Azure AD admin should be configured

### App Service / Function App
- `httpsOnly` must be `true`
- `minTlsVersion` must be `1.2`
- Managed identity should be enabled
- `ftpsState` should be `Disabled` or `FtpsOnly`

### Network Security Groups
- No inbound `Allow` rules from `*` or `0.0.0.0/0` to ports 22, 3389, 1433, 3306, 5432
- Deny-all rules should be present as the lowest priority

### Virtual Machines
- OS disk encryption must be enabled
- Managed identity should be used instead of credentials
- Boot diagnostics should be enabled

## Boundaries

- Do NOT modify files without user consent
- Do NOT execute Bicep deployments
- Do NOT access Azure subscriptions or resource groups
- Focus only on static analysis of Bicep template content
