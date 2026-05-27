---
name: wp-review
description: >
  WordPress theme and plugin review skill. Detects whether a target path is a
  theme or plugin, runs security and standards checks, scores the findings, and
  writes a markdown report. Use when the user wants to review a WordPress theme
  or plugin directory, generate a code review report, inspect WordPress
  security posture, or compare review strictness with selectable security
  levels.
allowed-tools: Read, Grep, Glob, Bash, Write
---

# WP Review

Use this skill when the user provides a path to a WordPress theme or plugin and wants a review report.

## When To Use

Use `wp-review` when the user asks to:

- review a WordPress theme
- review a WordPress plugin
- scan a WordPress project for security issues
- generate a WordPress review report
- run a basic, standard, or high security review

If the user gives only a project path, default to a markdown report with `standard` security.

## Commands

Run the unified dispatcher:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress-project"
```

Full review command:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-full-review.ps1" -Path "C:\path\to\wordpress-project"
```

Quick security-only command:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-quick-review.ps1" -Path "C:\path\to\wordpress-project"
```

Security review strictness:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress-project" -SecurityLevel basic
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress-project" -SecurityLevel standard
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress-project" -SecurityLevel high
```

JSON output:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress-project" -SecurityLevel standard -PrintJson
```

## Workflow

1. Verify the provided path exists and points to a WordPress theme or plugin directory.
2. Default to `standard` security unless the user explicitly asks for `basic` or `high`.
3. Run `run-review.ps1` with the requested security level.
4. Prefer markdown output unless the user explicitly asks for JSON.
5. If markdown output is used, tell the user where `review.report.md` was written.
6. If JSON output is used, summarize the main findings and score instead of dumping raw JSON unless the user asked for it.

Use `run-full-review.ps1` when the user wants the broadest currently implemented pass.
Use `run-quick-review.ps1` when the user wants a fast `basic` security-only pass.

## Recommended Defaults

- `basic` for quick confidence checks when the user wants fewer false positives
- `standard` for normal review runs
- `high` for exploratory review when the user wants broader triage and accepts noisier findings

## Examples

Theme review:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress\wp-content\themes\your-theme" -SecurityLevel standard
```

Plugin review:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress\wp-content\plugins\your-plugin" -SecurityLevel standard
```

High-security JSON review:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\wp-review\run-review.ps1" -Path "C:\path\to\wordpress-project" -SecurityLevel high -PrintJson
```

## Security Levels

- `basic`: high-confidence checks only, quietest output
- `standard`: balanced default mode
- `high`: broader, noisier review for manual triage

`CriticalOnly` skips standards review. It does not filter security findings to literal `critical` severity values.

## Output

- Markdown report: `review.report.md` in the target project directory by default
- JSON: theme/plugin fingerprint, security findings, standards findings, and combined score
