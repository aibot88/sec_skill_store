---
name: security-scan
description: Scan a local code or plugin directory for third-party dependencies, lockfiles, extensions, workflow actions, container definitions, risky install hooks, suspicious code patterns, and unusually powerful permissions. Use when the user wants a security-oriented pass over a repository, generated app, browser extension, IDE plugin, CI workflow, Docker setup, or other development folder to identify what is installed and what deserves deeper review.
---

# Security Scan

Version: `1.0.0`

Run the bundled scanner first, then manually validate anything high-signal before drawing conclusions.

Answer two questions:

1. What third-party code or add-ons are present?
2. Which files or package sources deserve closer review?

## Quick Start

1. Run `python3 scripts/security_scan.py <target-path>`.
2. Read `Findings by Severity` and `Flagged Files` first, then use `Third-Party Inventory` to understand both manifests and lockfiles.
3. Open the referenced files for any `high` or `medium` issue.
4. Describe findings as `flagged`, `suspicious`, `risky`, or `requires review`.
5. Do not call code or a package malicious without direct evidence.

## What The Script Covers

Inventory these common ecosystems and add-on formats:

- `package.json` dependencies and npm lifecycle scripts
- `package-lock.json`, `yarn.lock`, and `pnpm-lock.yaml`
- `requirements*.txt` and `pyproject.toml`
- `poetry.lock`
- `Cargo.toml` and `Cargo.lock`
- `Gemfile` and `Gemfile.lock`
- `go.mod`, `composer.json`, `pom.xml`, `build.gradle*`, and `Package.swift`
- `.csproj` and `packages.config`
- Browser extension `manifest.json`
- JetBrains `plugin.xml`
- GitHub Actions workflow files in `.github/workflows/*.yml`
- `Dockerfile*`, `docker-compose.yml`, and `compose.yaml`

Flag these local risk indicators:

- Direct URL, Git, or repo-based dependency sources
- Lockfiles that resolve packages to direct tarballs, repositories, or other non-registry sources
- Suspicious install hooks like `preinstall` or `postinstall`
- Shell pipelines that download and execute remote code
- Dynamic execution patterns like `eval`, `new Function`, or subprocess spawning
- Large base64-like blobs in source
- Sensitive browser extension permissions such as `<all_urls>`, `debugger`, `nativeMessaging`, or `proxy`
- GitHub Actions that use third-party actions without a full commit SHA pin
- Docker and Compose configurations that use floating base images, remote `ADD`, privileged mode, host namespaces, root users, or dangerous host mounts

## Expected Workflow

### 1. Run the local scan

Prefer text output:

```bash
python3 scripts/security_scan.py <target-path>
```

Use JSON only when another tool will consume the results:

```bash
python3 scripts/security_scan.py <target-path> --format json
```

### 2. Validate high-signal findings

For each `high` or `medium` finding:

- Open the referenced file.
- Confirm the pattern is real and not benign test data.
- Explain why it matters in plain language.
- State what additional review is still needed if certainty is limited.

### 3. Deliver a careful report

Always include:

- The list of directories scanned
- The flagged files, with why they were flagged
- The full file list
- Each noteworthy finding attached to the file where it was found
- A concise inventory of third-party components
- A short note on scan limits

## Response Template

Use this structure when summarizing results:

```markdown
Directories scanned
- <directory>

Flagged files
- <file>: <severity> <issue>

Files scanned
- <file>: OK
- <file>: <severity> <issue>

Third-party inventory
- <component>: <ecosystem/type>, version/source, where it was found

Limits
- This is a local heuristic scan. It can identify risky patterns, but it cannot prove a package is malicious without stronger evidence.
```

## When To Go Beyond The Script

Inspect files manually when:

- The project uses an unsupported dependency format
- The scanner flags lifecycle scripts or extension permissions
- The code downloads executables, runs shell commands, or decodes hidden payloads
- The user specifically asks whether a package is known to be malicious

If browsing is available and the user wants deeper verification, confirm package ownership and advisories through official registries, vendor docs, and the source repository.
