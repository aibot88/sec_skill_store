---
name: deploying-fc1-flex-consumption-functions
description: Deploys standalone Azure Function Apps on Flex Consumption (FC1) for workloads SWA managed functions can't handle — timer triggers, queue triggers, AI workloads, long-running operations. Provisions via ARM REST API or Bicep because az CLI flags silently fall back to deprecated Y1/Dynamic. Includes the forbidden-app-settings list, the ESM-vs-CommonJS module setting, and managed-identity storage authentication. Use when adding a non-HTTP trigger, exceeding the 30s SWA limit, or fixing a Function App that the CLI placed on the wrong plan.
---

# Deploying FC1 Flex Consumption Function Apps

Use FC1 when SWA managed functions don't fit: timer triggers, queue triggers, AI workloads, or anything that runs longer than 30 seconds.

## Workflow checklist

Copy this checklist and tick items off:

```
FC1 Flex Consumption provisioning:
- [ ] Step 1: Confirm SP has User Access Administrator at the RG scope (needed for MI role assignments)
- [ ] Step 2: Deploy storage account with the deployment container (storage-for-fc1.bicep)
- [ ] Step 3: Deploy FC1 plan + Function App via Bicep (NEVER az CLI — it silently mis-creates the plan)
- [ ] Step 4: Verify properties.sku == "FlexConsumption" with az functionapp show
- [ ] Step 5: Confirm FUNCTIONS_WORKER_RUNTIME is NOT in app settings
- [ ] Step 6: Confirm package.json has "main": "dist/index.js" + "type": "module" (FC1 = ESM)
- [ ] Step 7: Confirm src/index.ts imports every function file with .js extensions
- [ ] Step 8: Deploy code via Azure/functions-action@v1.5.2+; check log for "Detected function app sku: FlexConsumption"
- [ ] Step 9: Wait up to 10 min for MI role assignment propagation if first call fails
```

## Why this is hard

Azure Flex Consumption (FC1) looks similar to deprecated Linux Consumption (Y1) in the portal but behaves completely differently:

| | Linux Consumption (Y1) | Flex Consumption (FC1) |
|---|---|---|
| Status | **Deprecated** | Current, recommended |
| Deployment | `WEBSITE_RUN_FROM_PACKAGE` | **One Deploy** (blob-based) |
| `FUNCTIONS_WORKER_RUNTIME` | Required | **Forbidden** |
| CLI creation | Works | **Silently fails** to wrong plan |
| Storage auth | Connection string | `__accountName` (Managed Identity) |

## The CLI silently creates the wrong plan

**`az functionapp create --flexconsumption-location`** silently places the app on `AustraliaEastLinuxDynamicPlan` (Y1/Dynamic) without error. Tested CLI v2.83.0.

**`az appservice plan create --sku FC1`** returns no error but the plan is "Not Found" when queried.

**Always use ARM REST API or Bicep.** See [references/arm-rest-walkthrough.md](references/arm-rest-walkthrough.md) for the REST approach and [templates/flexConsumption.bicep](templates/flexConsumption.bicep) for the Bicep approach.

## App settings — forbidden values

```
DO set:
  AzureWebJobsStorage__accountName = <storage>    (DOUBLE underscore, MI auth)
  SQL_CONNECTION_STRING = <value>
  AI_PROJECT_ENDPOINT = <value>

DO NOT set:
  FUNCTIONS_WORKER_RUNTIME         — FORBIDDEN, causes "malformed content"
  WEBSITE_RUN_FROM_PACKAGE         — Y1 only
  WEBSITE_ENABLE_SYNC_UPDATE_SITE  — Y1 only
```

Runtime is declared in `functionAppConfig.runtime` on the resource, not in app settings. See [references/forbidden-settings.md](references/forbidden-settings.md).

## Code structure (FC1 = ESM)

```json
// package.json
{ "main": "dist/index.js", "type": "module" }
```

```typescript
// src/index.ts — ESM imports with .js extensions
import './functions/myFunction.js';
```

```json
// tsconfig.json
{ "compilerOptions": { "module": "ES2022", "moduleResolution": "node" } }
```

**SWA managed functions use CommonJS; standalone FC1 uses ESM.** They are not interchangeable.

## Required RBAC

| Role | Scope | Purpose |
|------|-------|---------|
| Storage Blob Data Owner | Function App's storage account | Host lease + deployment blob |
| Storage Blob Data Contributor | User blob storage | Read/write user blobs |

The deploying SP needs `User Access Administrator` to create these role assignments in Bicep. See [configuring-azure-oidc-for-github-actions](../configuring-azure-oidc-for-github-actions/SKILL.md).

RBAC propagation can take up to 10 minutes after deploy. If the app fails to start immediately, wait and retry before debugging.

## Can't change hosting plan on an existing app

If an app was accidentally created on Y1, you **must delete and recreate it**. The hosting plan cannot be migrated. If the name is soft-deleted (~24h), use a new name.

## Verification

```bash
az functionapp show --name "$FUNCTION_APP_NAME" --resource-group "$RESOURCE_GROUP" \
  --query "{sku:properties.sku, serverFarm:properties.serverFarmId}" -o json
# properties.sku MUST be "FlexConsumption"
# serverFarmId must NOT end with "LinuxDynamicPlan"
```

In the Actions log:
```
Detected function app sku: FlexConsumption   ← correct
Package deployment using One Deploy initiated.
```

If you see `Detected function app sku: Consumption` — wrong plan. Recreate.

## Composes with

- [scaffolding-azure-bicep-infrastructure](../scaffolding-azure-bicep-infrastructure/SKILL.md) — for the modular toggle to add FC1 to a project
- [configuring-azure-oidc-for-github-actions](../configuring-azure-oidc-for-github-actions/SKILL.md) — User Access Administrator grant for MI role assignments
- [diagnosing-azure-deployment-failures](../diagnosing-azure-deployment-failures/SKILL.md) — for FC1-specific failure modes

## Checklist

- [ ] FC1 plan created via ARM REST API or Bicep (not CLI)
- [ ] Function app created via ARM with explicit `serverFarmId`
- [ ] `properties.sku = "FlexConsumption"` confirmed
- [ ] `FUNCTIONS_WORKER_RUNTIME` is NOT in app settings
- [ ] `AzureWebJobsStorage__accountName` used (double underscore)
- [ ] Managed identity has Storage Blob Data Owner
- [ ] SP has User Access Administrator at RG scope
- [ ] `package.json` has `"main": "dist/index.js"` and `"type": "module"`
- [ ] `src/index.ts` imports all function files with `.js` extensions
- [ ] Actions log shows `FlexConsumption` detection
