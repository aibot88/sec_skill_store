---
name: scanit
description: |
  Packages and runs a local SAST pipeline scan to identify source code vulnerabilities.

  - User asks to scan the codebase, run a scan, or check for vulnerabilities
  - User mentions "scanit", "pipeline scan", "SAST scan", "scan my code"
  - User wants to know if their code has security issues before committing or deploying

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - mcp_veracode_package-workspace
  - mcp_veracode_pipeline-scan
  - mcp_veracode_pipeline-findings
license: Apache-2.0
compatibility: Requires Veracode MCP server connection and authenticated Veracode account. Supports SAST scanning for all major languages.
metadata:
  author: Dipsylala
  version: 1.0.0
---

# SAST Pipeline Scanner

Packages the workspace and runs a Veracode pipeline SAST scan to identify source code vulnerabilities.

**Scope**: This skill covers static analysis (SAST) only. For third-party dependency and IaC scanning, use the `thirdit` skill instead.

## Step 1 — Package the workspace

Package the workspace source code into a scan artifact. The packager auto-detects languages and build systems. If packaging fails, read the error — the most common causes are a missing build output directory or an unsupported project structure, both of which have actionable error messages.

## Step 2 — Run the scan

Run the pipeline scan in **synchronous mode** so the user receives results in the same session without needing to poll or return later. If packaging fails, read the error before retrying — the most common causes are a missing build output or an unsupported project structure.

## Step 3 — Retrieve results

Once the scan completes, retrieve findings immediately. If no findings are returned, confirm the scan completed cleanly and the application passes policy.

If the scan fails (not packaging — the scan itself), report the error message directly. Do not retry automatically.

## Constraints

- Do NOT run a local SCA scan — that is the `thirdit` skill's responsibility.
- Do NOT package and scan if the user only asked to check existing results — use the `reportit` skill for that.
- Do NOT suggest retrying a failed package step by modifying scan parameters — diagnose the actual packaging error first.
