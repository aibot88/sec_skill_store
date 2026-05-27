---
name: configuring-azure-oidc-for-github-actions
description: Sets up branch-scoped Azure OIDC for GitHub Actions — creates service principals, federated credentials bound to each branch's refs/heads/{branch}, generates SQL passwords, and sets GitHub secrets. Use when bootstrapping CI/CD, onboarding a new environment branch, or fixing AADSTS70021 subject mismatches.
---

# Configuring Azure OIDC for GitHub Actions

Sets up secret-less Azure authentication for GitHub Actions. After running these scripts, deploys work via `git push` with no client secrets to rotate.

## Why OIDC

- No client secrets stored in GitHub or in code
- Branch-scoped: the `test` SP can't deploy to `production` and vice versa
- Federated credential subject is bound to `refs/heads/{branch}` exactly — drift causes `AADSTS70021`

## Workflow checklist

Copy this checklist into your response and check items off as you complete them:

```
OIDC + GitHub Actions setup:
- [ ] Step 1: Verify az login + gh auth login (and AZURE_CONFIG_DIR if shared machine)
- [ ] Step 2: Confirm GitHub repo exists, branches (test, production) created
- [ ] Step 3: Run scripts/create-sp-with-oidc.sh → creates test + prod SPs + federated creds
- [ ] Step 4: Run scripts/generate-sql-password.sh → SQL admin passwords
- [ ] Step 5: Run scripts/add-github-secrets.sh → 6 secrets set
- [ ] Step 6: For each additional environment branch (acme-demo, customer-uat, etc.), re-run with that branch name
- [ ] Step 7: First push to test → verify the workflow authenticates (no AADSTS70021)
```

## Setup sequence

Run these scripts in order. Each is idempotent (safe to re-run).

```bash
# Prerequisites: az login and gh auth login already done.
# Use AZURE_CONFIG_DIR if this project shares a machine with others.

export ORG="acme"             # short org prefix
export PROJECT="taskapp"      # short project name
export GITHUB_ORG="myorg"
export REPO="taskapp"

# 1. Create both service principals + federated credentials
bash scripts/create-sp-with-oidc.sh

# 2. Generate SQL admin passwords (test + prod)
bash scripts/generate-sql-password.sh

# 3. Set the 6 GitHub secrets
bash scripts/add-github-secrets.sh
```

Each script prints what it will do, what already exists, and what was created.

## The 6 GitHub secrets

| Secret | Scope | Source |
|--------|-------|--------|
| `AZURE_TENANT_ID` | Both envs | `az account show --query tenantId` |
| `AZURE_SUBSCRIPTION_ID` | Both envs | `az account show --query id` |
| `AZURE_CLIENT_ID_TEST` | Test SP appId | `create-sp-with-oidc.sh` output |
| `AZURE_CLIENT_ID_PROD` | Prod SP appId | `create-sp-with-oidc.sh` output |
| `SQL_ADMIN_PASSWORD_TEST` | Test SQL admin | `generate-sql-password.sh` output |
| `SQL_ADMIN_PASSWORD_PROD` | Prod SQL admin | `generate-sql-password.sh` output |

## Critical: federated credential subject format

Azure rejects the OIDC token if the subject doesn't match **exactly**:

```
repo:{GitHubOrg}/{Repo}:ref:refs/heads/{branch}
```

| Common mistake | Error |
|---------------|-------|
| `ref:refs/heads/main` when workflow pushes from `test` | `AADSTS70021: No matching federated identity record found` |
| `pull_request` subject for branch push | same |
| Extra trailing slash | same |
| Repo case mismatch (`MyOrg` vs `myorg`) | same |

If you see `AADSTS70021`, dump the actual issuer + subject from the failed run, then compare against the federated credential:

```bash
az ad app federated-credential list --id "$CLIENT_ID" -o table
```

## When to use User Access Administrator

The default `Contributor` role is sufficient for SWA + SQL deploys. You need `User Access Administrator` when Bicep contains `Microsoft.Authorization/roleAssignments` resources — typically:

- FC1 Flex Consumption (Function App MI → Storage Blob Data Owner)
- Container Apps Jobs that need `AcrPull` or similar
- Any module that does `roleAssignments` on a child resource

Grant at the smallest scope that works (RG > subscription):

```bash
az role assignment create \
  --assignee "$SP_OID" \
  --role "User Access Administrator" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$ORG-$PROJECT-rg-test"
```

If the RG doesn't exist yet, scope to subscription temporarily.

## SP creation gotcha — WARNING in stdout

`az ad sp create-for-rbac --sdk-auth` prepends a `WARNING:` line to stdout. If that ends up in `AZURE_CREDENTIALS` (the legacy format), authentication silently fails. **OIDC sidesteps this** — we only store the appId, never the SP JSON. But if you ever need `AZURE_CREDENTIALS`, strip the warning:

```bash
az ad sp create-for-rbac ... --sdk-auth 2>/dev/null \
  | python3 -c "import sys,json; d=sys.stdin.read(); print(json.dumps(json.loads(d[d.find('{'):]),indent=2))"
```

## Composes with

- [scaffolding-azure-bicep-infrastructure](../scaffolding-azure-bicep-infrastructure/SKILL.md) — generates the workflow files that consume these secrets
- Microsoft's [`entra-app-registration`](https://github.com/microsoft/azure-skills) — deeper app-registration mechanics
- Microsoft's [`azure-rbac`](https://github.com/microsoft/azure-skills) — RBAC verification on running deployments

## Reference

See [references/federated-credentials.md](references/federated-credentials.md) for the full breakdown of subject formats, audiences, and verification commands.
