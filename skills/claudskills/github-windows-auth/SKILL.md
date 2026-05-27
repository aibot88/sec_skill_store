---
name: github-windows-auth
description: Diagnose and fix GitHub authentication issues on Windows when pushing fails with "Repository not found" or wrong-account errors. Use when git push fails despite the repo existing, when multiple GitHub accounts are in play (personal + org), or when Windows Credential Manager has stale credentials. Trigger on phrases like "push failed", "repository not found", "wrong account", "gh auth", "credential", "git push 403", or any push error after a gh auth login.
categories: [git, github, windows]
metadata:
  source: custom
  scope: global
---

# GitHub Windows Auth — Diagnose & Fix

Fix `git push` failures on Windows caused by stale credentials or mismatched GitHub accounts.

## The pattern

On Windows, git uses the **Windows Credential Manager** as its credential store. When multiple GitHub accounts are in use (e.g. personal `bmaltais` and org `bernardmaltais`), the stored credential can belong to the wrong account — and `gh auth switch` alone doesn't fix it because git bypasses `gh` and reads the cached token directly.

The fix is always the same three steps:
1. Clear the stale Windows credential
2. Tell git to use `gh` as its credential helper going forward
3. Push

## Diagnostic process

### Step 1 — Identify which account the remote needs

```powershell
git -C <repo-path> remote get-url origin
```

The org/user in the URL tells you which `gh` account must be active.

### Step 2 — Check which accounts `gh` knows about

```powershell
gh auth status
```

Look for the account matching the remote. If it's not listed, authenticate it first:

```powershell
gh auth login
```

### Step 3 — Switch `gh` active account if needed

```powershell
gh auth switch --user <username>
```

### Step 4 — Clear stale Windows credential and wire `gh` as helper

```powershell
cmdkey /delete:LegacyGeneric:target=git:https://github.com
gh auth setup-git
```

### Step 5 — Push

```powershell
git -C <repo-path> push
```

## Notes

- `gh auth setup-git` writes `gh auth git-credential` as the credential helper in the global git config. It persists — you only need to run it once per machine (or after `cmdkey /delete` wipes the old entry).
- If you have **two org accounts** (e.g. `bmaltais` and `bernardmaltais`), the active `gh` account at push time determines which token git uses. Switch before pushing to the other org.
- If `gh` is not on `PATH` in the current shell, reload it first:
  ```powershell
  $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","Machine")
  ```

## Quick reference — full fix in one line

```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","Machine")
gh auth switch --user <username>
cmdkey /delete:LegacyGeneric:target=git:https://github.com
gh auth setup-git
git -C <repo-path> push
```
