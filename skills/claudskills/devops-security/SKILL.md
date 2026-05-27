---
name: devops-security
description: Use when called by the devops dispatcher after analysis to audit security posture and select CI security tooling before config generation
---

# DevOps Security Review

## Overview

Runs a security checklist audit and selects appropriate CI security tools. Produces `devops/report/security-findings.json` and security tool configs in `devops/working/ci/security/`. Runs BEFORE `devops-generate` so security tool choices are baked into CI configs.

## Inputs

Read `devops/report/analysis.json` before starting. The relevant fields are:
- `scenario` — "design", "codebase", or "review"
- `choices.cloud_provider` — "AWS", "GCP", "Azure", "Multi-cloud", or "Self-hosted"
- `choices.ci_cd_platform` — "GitHub Actions", "GitLab CI", or "CircleCI"
- `choices.deployment_target` — "Containers", "Kubernetes", "Serverless", or "VMs"
- `detected.has_dockerfile` — true/false

## Security Checklist

Evaluate each item. For codebase and review scenarios, actively read source files and existing configs to check.

Rate each finding: **Critical** / **High** / **Medium** / **Low**. Only write a finding if the item FAILS the check. Items that pass are not included in output.

**Design scenario handling:** For each category that says "design scenario: skip", write no findings for that category. For categories with "design scenario: write Low findings", write a finding with severity "Low", finding "Cannot verify at design stage", and a remediation recommendation.

### Category 1: Secrets & Credentials

- [ ] No hardcoded secrets in source files (grep for patterns: `API_KEY`, `SECRET`, `PASSWORD`, `TOKEN`, `PRIVATE_KEY`, `aws_access_key`, `api_key =`)
- [ ] `.env` files are listed in `.gitignore`
- [ ] CI/CD YAML files do not echo secret values in `run:` steps
- [ ] Secrets referenced by environment variable name, not literal value, in configs

**Severity guide:** Hardcoded secret in source = Critical. .env not gitignored = High. Secret echoed in CI = High. Secrets as literal values in non-CI configs = Medium.

### Category 2: Container Security

**If `detected.has_dockerfile` is false:** Skip this category — write no findings. The devops-generate skill will create a secure Dockerfile.

**If `detected.has_dockerfile` is true:** Check the existing Dockerfile for each item below.

- [ ] App process does not run as root (Dockerfile has `USER` instruction before `CMD`)
- [ ] Base image uses a specific version tag, not `latest`
- [ ] Multi-stage build used to exclude dev dependencies from production image
- [ ] Dockerfile does not EXPOSE more than 2 ports unless the service is a documented multi-port service
- [ ] Base image is official (from Docker Hub official or distroless)

**Severity guide:** Running as root = High. `latest` tag = Medium. No multi-stage build = Medium. EXPOSE more than 2 ports without documentation = Low. Unofficial base image = Medium.

### Category 3: Network Exposure

**Design scenario:** Write Low findings for each item below with finding "Cannot verify at design stage" and a remediation recommendation for implementation time. Do not attempt to verify against source code.

**Codebase / review scenario:** Check framework config files and source files for each item:

- [ ] API endpoints that modify data require authentication middleware
- [ ] Rate limiting configured (check for express-rate-limit, django-ratelimit, etc.)
- [ ] CORS policy is restrictive — not `origin: '*'` in production config
- [ ] HTTPS enforced (HTTP requests redirect to HTTPS)

**Severity guide:** No auth on data-modifying endpoints = Critical. Wildcard CORS in prod = High. No rate limiting = Medium. No HTTPS redirect = Medium.

### Category 4: Dependencies

- [ ] Lockfile present (`package-lock.json`, `yarn.lock`, `poetry.lock`, `go.sum`, `Gemfile.lock`, `Cargo.lock`)
- [ ] No obviously outdated major versions in direct dependencies (check package.json/requirements.txt dates)
- [ ] Dockerfile RUN installs pin package versions (not `pip install requests` without `==version`)

**Severity guide:** No lockfile = High. Unpinned Dockerfile installs = Medium. Outdated major versions = Low.

### Category 5: CI/CD Pipeline

**Design and codebase scenarios:** Skip this category — write no findings. The generated pipeline will include proper controls.

**Review scenario only:** Check existing CI/CD config files for each item:

- [ ] Main/production branch is protected (requires PR review)
- [ ] Production deployments require manual approval gate
- [ ] Docker images are tagged with commit SHA, not `latest`
- [ ] No secrets stored as plain text in CI YAML

**Severity guide:** No prod approval gate = High. Secrets in CI YAML = Critical. Image tagged with `latest` = Medium.

### Category 6: Cloud IAM

**If `choices.cloud_provider` is "Self-hosted" or "Multi-cloud":** Skip this category — write no findings.

**If `choices.cloud_provider` is AWS, GCP, or Azure:** Check existing infra-as-code (terraform/, pulumi/) if present. If no infra-as-code exists, write one Low finding per item below with finding "No infra-as-code found — cannot verify" and a remediation recommendation (e.g., "Use IAM roles with least-privilege — create Terraform IAM module at infra/iam.tf").

- [ ] Service accounts/roles use least-privilege (no `*` wildcard permissions)
- [ ] CI/CD runner role has only the permissions needed to deploy
- [ ] Storage buckets/blobs are not publicly accessible by default
- [ ] No long-lived access keys committed to repository

**Severity guide:** Wildcard IAM permissions = High. Public storage = High. Committed keys = Critical. No infra-as-code for IAM = Low.

### Category 7: OWASP Top 10 (framework-specific)

Apply based on detected framework (from `stack.framework` in analysis.json). For design scenario, write Low findings for each applicable item.

- [ ] **Injection:** ORM or parameterized queries used (no string-concatenated SQL queries visible in source)
- [ ] **Authentication:** Session expiry configured; passwords hashed using bcrypt or argon2
- [ ] **Security Misconfiguration:** Debug mode disabled in production config; detailed error messages not returned to clients
- [ ] **Vulnerable Components:** See Dependencies category — flag unresolved issues here too if dependency findings exist

**Severity guide:** SQL injection risk (string-concatenated queries found) = Critical. Debug mode in prod = High. No password hashing = High. Auth missing session expiry = Medium.

### Category 8: Secrets Management

- [ ] Production secrets stored in secrets manager (not `.env` files committed to repo)
- [ ] Dev secrets in `.env.local` (gitignored), not `.env` (which may be committed)
- [ ] Secret rotation policy exists or is recommended

**Severity guide:** Production secrets in committed env file = Critical. No rotation policy = Low.

## Security Tool Selection

Read `choices.ci_cd_platform` and `choices.deployment_target` from analysis.json to populate `selected_tools`:

| Tool | When to Include |
|---|---|
| **Trivy** | Always — container + dependency CVE scanning |
| **Semgrep** | Always — open source SAST, no account required |
| **CodeQL** | Include if `choices.ci_cd_platform` = "GitHub Actions" |
| **Dependabot** | Include if `choices.ci_cd_platform` = "GitHub Actions" |
| **Snyk** | Include if `choices.ci_cd_platform` = "GitLab CI" or "CircleCI" |
| **Gitleaks** | Always — secrets detection in git history and CI |
| **OWASP ZAP** | Include if `choices.deployment_target` = "Containers" or "Kubernetes" |

## Output

### 1. Write security-findings.json

Create `devops/report/security-findings.json`. Populate `summary` counts from actual findings. Populate `selected_tools` from the tool selection table above using the exact lowercase strings: `trivy`, `semgrep`, `codeql`, `dependabot`, `snyk`, `gitleaks`, `owasp-zap`.

```json
{
  "summary": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  },
  "findings": [
    {
      "category": "Secrets & Credentials",
      "severity": "Critical",
      "finding": "Specific description of what was found",
      "remediation": "Specific fix: e.g., move API_KEY to .env.local and add to .gitignore"
    }
  ],
  "selected_tools": ["trivy", "semgrep", "gitleaks"],
  "scenario": "codebase"
}
```

### 2. Write Gitleaks config

Create `devops/working/ci/security/.gitleaks.toml`:

```toml
title = "Gitleaks Config"

[allowlist]
  description = "Allowlisted paths"
  paths = [
    # devops/working/ is allowlisted because it contains generated tool configs, not application code
    '''devops/working/''',
    '''\.env\.example$''',
  ]
```

### 3. Write Trivy ignore

Create `devops/working/ci/security/.trivyignore`:

```
# Add CVE IDs here to suppress false positives after manual review
# Example: CVE-2023-12345
```

## Confirmation

After writing all output files, tell the user:

```
Security review complete.
  Critical: N | High: N | Medium: N | Low: N
  Tools selected: [list]
  Saved to devops/report/security-findings.json

Top findings:
  [List up to 3 findings, sorted by severity (Critical first, then High, then Medium, then Low). Break ties by listing in checklist order. If fewer than 3 findings total, list all of them.]
  Format each as: [SEVERITY] Category — one-line remediation
```
