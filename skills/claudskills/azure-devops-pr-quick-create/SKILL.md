---
name: azure-devops-pr-quick-create
description: Create pull requests quickly in Azure DevOps repositories using Azure CLI (`az repos pr create`) with reliable auth fallbacks. Use this skill whenever the user asks to create/open/raise a PR for Azure DevOps, especially when they mention PAT auth, `TF_VAR_devops_user_pat_163ent`, `AZURE_DEVOPS_EXT_PAT`, or sourcing `~/dotfiles/sp/163ent-devops.sp`. Prefer this skill over GitHub CLI or GitKraken tools for Azure DevOps remotes.
categories: [github]
agents: [copilot]
metadata:
  source: custom
  scope: global
---

# Azure DevOps PR Quick Create

Use this workflow to create PRs quickly and predictably for Azure DevOps repos.

## Core rule

Use Azure CLI only for PR creation in Azure DevOps repos:
- Use `az repos pr create`
- Do not use GitHub CLI for Azure DevOps remotes
- Do not use GitKraken tools unless the user explicitly requests it

## Input expectations

Collect or infer these values:
- Source branch
- Target branch — **ask the user if not explicitly stated**. Do not assume the current base branch is the right target. Default to the repo's default branch (check `az repos show --query defaultBranch`) only if the user has not specified one.
- PR title
- PR description/body

**Work item org/project — always ask** before creating a task/work item if the user has not explicitly named an org and project. The git remote org (e.g. `SSC-CTO-ESLZ`) is NOT necessarily the same org where work items live (e.g. `Azure163ent-CloudOperations/Activities`).

## Fast workflow

1. Verify repo status is ready.
2. Ensure source branch exists and is pushed.
3. Authenticate Azure DevOps CLI (PAT env first, then fallback source file).
4. Create PR with `az repos pr create`.
5. Return PR id and web URL.

## Step 0: Ensure azure-devops CLI extension is installed

Before any `az repos` or `az boards` command, verify the extension is present:

```bash
az extension show --name azure-devops &>/dev/null || az extension add --name azure-devops --yes
```

This is required on every machine where the extension has not been explicitly installed.

## Step 1: Repo preflight

Run:

```bash
git status -sb
git rev-parse --abbrev-ref HEAD
git remote -v
```

Confirm:
- Correct source branch
- Branch is pushed to origin
- Remote is Azure DevOps (`dev.azure.com`)

If source branch is not pushed, run:

```bash
git push -u origin <source-branch>
```

**Verify target branch exists in ADO** before attempting PR creation:

```bash
az repos ref list \
  --organization "https://dev.azure.com/<org>" \
  --project "<project>" \
  --repository "<repo>" \
  --filter "heads/<target-branch>" \
  --query "[].name" -o json
```

If the result is `[]`, push the target branch first:

```bash
git push origin <target-branch>
```

## Step 2: Derive Azure DevOps metadata from origin URL

Expected remote format:

```text
https://<optional-user>@dev.azure.com/<org>/<project>/_git/<repo>
```

Extract:
- Organization URL: `https://dev.azure.com/<org>`
- Project: `<project>`
- Repository: `<repo>`

## Step 3: Authentication strategy (in order)

Try auth methods in this sequence:

1. If `AZURE_DEVOPS_EXT_PAT` already set, use it.
2. Else if `TF_VAR_devops_user_pat_163ent` is set, export it to `AZURE_DEVOPS_EXT_PAT`.
3. Else source credentials file and retry:

```bash
source ~/dotfiles/sp/163ent-devops.sp
```

Then check again for PAT env presence.

If still missing, ask user to export PAT in terminal and retry.

## Step 4: Create PR

Use:

```bash
az repos pr create \
  --organization "https://dev.azure.com/<org>" \
  --project "<project>" \
  --repository "<repo>" \
  --source-branch "<source-branch>" \
  --target-branch "<target-branch>" \
  --title "<title>" \
  --description "<description>" \
  --output json
```

If command output is truncated or terminal closes unexpectedly, verify creation with:

```bash
az repos pr list \
  --organization "https://dev.azure.com/<org>" \
  --project "<project>" \
  --repository "<repo>" \
  --source-branch "<source-branch>" \
  --status active \
  --output json
```

## Step 5: Return a usable PR link

From PR id `<id>`, build the web URL:

```text
https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<id>
```

Always return:
- PR id
- Title
- Source -> target branch
- Web URL

## Step 6 (optional): Link a work item to the PR

To look up an existing PR by ID (omit `--project` — it is not a valid flag for `az repos pr show`):

```bash
az repos pr show \
  --organization "https://dev.azure.com/<org>" \
  --id <pr-id> \
  --output json
```

To link a work item to a PR, use `az repos pr work-item add` (NOT `az repos pr update --work-items`):

```bash
az repos pr work-item add \
  --organization "https://dev.azure.com/<org>" \
  --id <pr-id> \
  --work-items <work-item-id> \
  --output json
```

To create a work item (Task) as a child of an existing Epic:

```bash
# 1. Create the Task
az boards work-item create \
  --organization "https://dev.azure.com/<org>" \
  --project "<project>" \
  --type "Task" \
  --title "<title>" \
  --description "<description>" \
  --output json

# 2. Set parent Epic (use the Task id returned above)
az boards work-item relation add \
  --organization "https://dev.azure.com/<org>" \
  --id <task-id> \
  --relation-type "parent" \
  --target-id <epic-id> \
  --output json

# 3. Link Task to PR
az repos pr work-item add \
  --organization "https://dev.azure.com/<org>" \
  --id <pr-id> \
  --work-items <task-id> \
  --output json
```

## Copy/paste helper block

Use this helper when the user asks for a quick PR and values are already known:

```bash
set -e
az extension show --name azure-devops &>/dev/null || az extension add --name azure-devops --yes
source ~/dotfiles/sp/163ent-devops.sp || true
if [[ -z "$AZURE_DEVOPS_EXT_PAT" && -n "$TF_VAR_devops_user_pat_163ent" ]]; then
  export AZURE_DEVOPS_EXT_PAT="$TF_VAR_devops_user_pat_163ent"
fi
if [[ -z "$AZURE_DEVOPS_EXT_PAT" ]]; then
  echo "Missing Azure DevOps PAT env (AZURE_DEVOPS_EXT_PAT or TF_VAR_devops_user_pat_163ent)."
  exit 1
fi

az repos pr create \
  --organization "https://dev.azure.com/<org>" \
  --project "<project>" \
  --repository "<repo>" \
  --source-branch "<source-branch>" \
  --target-branch "<target-branch>" \
  --title "<title>" \
  --description "<description>" \
  --output json
```

## Changing a PR's target branch after creation

`az repos pr update` does **not** support `--target-branch`. Use the REST API instead:

```bash
az rest \
  --method PATCH \
  --uri "https://dev.azure.com/<org>/<project>/_apis/git/repositories/<repo>/pullRequests/<pr-id>?api-version=7.1" \
  --headers "Content-Type=application/json" \
  --body '{"targetRefName": "refs/heads/<new-target>"}' \
  --resource 499b84ac-1321-427f-aa17-267ca6975798
```

## Cross-org work item linking

`az repos pr work-item add` only works when the PR repo and the work item are in the **same ADO org**. If they are in different orgs, the link must be added manually in the PR UI.

## Safety and behavior notes

- Never print PAT values in output.
- If authentication fails, report the exact blocker and next fix.
- Keep PR body concise and based on actual changed files (`git status --short` + `git diff --name-only`).
- If user asks to use Azure CLI, do not route through other PR tools.
