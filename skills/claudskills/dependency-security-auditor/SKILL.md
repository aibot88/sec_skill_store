---
name: dependency-security-auditor
description: "Audit dependency CVEs across Node, Python, Flutter/Dart, and mixed repos; design OSV/native audit hooks for pre-push and CI."
---

# Dependency Security Auditor

Audit application dependencies for known vulnerabilities and freshness risk, then produce a workflow that can run locally, in a git hook, or in CI. Prefer report-first behavior; ask before changing dependencies, lockfiles, hooks, or CI config.

## When To Use

Use this when asked to check package CVEs, scan `package.json`, scan `requirements.txt`, scan `pubspec.yaml`, add dependency security CI, add a Husky/pre-push security hook, or create a stack-aware audit workflow.

## Core Workflow

1. Detect ecosystems from lockfiles and manifests:
   - Node: `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`.
   - Python: `requirements.txt`, `poetry.lock`, `uv.lock`, `Pipfile.lock`, `pyproject.toml`.
   - Flutter/Dart: `pubspec.yaml`, `pubspec.lock`.
2. Scan lockfiles first. If a project has only a manifest and no lockfile, report weak evidence because exact resolved versions are unknown. For Python, `pyproject.toml` is only a detection signal unless paired with a lockfile or pinned requirements.
3. Run a broad scanner:
   - Prefer OSV-Scanner for cross-ecosystem CVE detection.
   - Use Trivy as an optional CI backstop for repository, container, and SBOM scans.
4. Run native audits when available:
   - Node: `npm audit --package-lock-only --json`, `pnpm audit --json`, or `yarn npm audit --recursive --json` (`--all` too for Yarn workspaces).
   - Python: `pip-audit` for environments, requirements files, or local project lockfiles via `--locked`.
   - Flutter/Dart: OSV-Scanner on `pubspec.lock`; use `dart pub outdated --json` or `flutter pub outdated --json` for freshness, not CVE truth.
5. Detect runtime/tool versions when freshness mode is enabled: Node/npm/pnpm/Yarn/Bun, Python/pip-audit, Flutter/Dart.
6. Compare current locked or installed versions against latest available versions when the ecosystem can do so:
   - Node: `npm outdated --json` or `pnpm outdated --format json`.
   - Yarn: skip freshness; Yarn npm plugin does not provide a supported `outdated` command.
   - Flutter/Dart: `dart pub outdated --json` or `flutter pub outdated --json`.
   - Python: installed environment freshness when available; do not confuse this with lockfile CVE truth.
7. Normalize findings by package, version, ecosystem, advisory ID, severity, fixed version, scanner source, and dependency path when available.
8. Separate **vulnerable** from **outdated**. Outdated packages are freshness risk, not CVEs.
9. Recommend remediation without applying it unless the user approves package changes.

## Bundled Tool

Use `scripts/dependency_audit.py` for deterministic discovery and scanner orchestration. It detects stacks, runtime tools, installed scanners, writes a JSON report, and can fail by severity threshold.

When the skill is installed outside the target repo, set `DEPENDENCY_AUDIT_SCRIPT` to the script location and call `python3 "$DEPENDENCY_AUDIT_SCRIPT"` from hooks or CI. Do not assume `skills/dependency-security-auditor/...` exists in every audited repository.

Example:

```bash
python3 skills/dependency-security-auditor/scripts/dependency_audit.py --root . --fail-on high --report dependency-security-report.json
```

Fast hook example:

```bash
python3 skills/dependency-security-auditor/scripts/dependency_audit.py --root . --mode pre-push --skip-freshness --fail-on high
```

CI freshness example:

```bash
python3 skills/dependency-security-auditor/scripts/dependency_audit.py --root . --mode ci --fail-on high --report dependency-security-report.json
```

Useful flags:

- `--dry-run`: discover projects and show what would be scanned without running scanners.
- `--skip-freshness`: skip runtime/latest-version checks for fast hooks.
- `--freshness`: force runtime/latest-version checks.
- `--fail-on-major-outdated`: fail when freshness checks find major-version lag.
- `--skip-osv` / `--skip-native`: run only native audits or only OSV-Scanner.
- `--verbose`: print scanner discovery, command execution, missing tools, and non-fatal diagnostics to stderr.

For Husky, pre-commit, and GitHub Actions examples, see `references/hook-and-ci-examples.md`.
For scanner selection and policy guidance, see `references/scanner-policy.md`.

## Output

Return:

- **Status:** clean, vulnerable, weak evidence, scanner unavailable, scanner error, or dry run.
- **Detected Stacks:** ecosystem, project path, and lockfile status.
- **Runtime:** installed runtime and package-manager versions when checked.
- **Findings:** severity-ordered CVEs/GHSAs with package, version, path, fixed versions, and source scanner.
- **Freshness:** current/wanted/latest versions and whether lag is patch, minor, or major.
- **False Positive Notes:** why a finding may or may not affect runtime.
- **Remediation Plan:** minimal safe upgrades or overrides, plus required verification commands.
- **Hook/CI Plan:** where to attach quick checks versus full scans.

## Hook Policy

- `pre-commit`: keep fast; scan only changed lockfiles or run secrets checks.
- `pre-push`: run dependency CVE scan and fail on high/critical by default; skip freshness unless the repo is small.
- PR CI: run full dependency audit plus runtime/freshness checks; fail on high/critical or newly introduced vulnerabilities.
- Scheduled CI: run full OSV plus optional Trivy/native audits and freshness checks; report all severities and stale major lines.

## Guardrails

- Do not install tools, edit hooks, edit lockfiles, or upgrade packages without explicit approval.
- Do not treat outdated packages as vulnerabilities unless a vulnerability advisory applies.
- Do not claim “no issues” from one scanner alone; name the data sources checked.
- Prefer patched minor/patch releases before major upgrades.
- For Node, do not blindly run `npm audit fix --force`; review suggested downgrades or major jumps.
- For Flutter/Dart applications, require `pubspec.lock` for actionable CVE scanning.
- Treat Python freshness as installed-environment freshness, not lockfile CVE evidence.
- Treat dependency-free CVSS v4 parsing as severity-gate fallback; prefer scanner-provided severity when available.
- Scanner command failures return `scanner_error` and should fail hooks/CI until rerun or triaged.

## Scanner Unavailable Policy

- Do not install OSV-Scanner, pip-audit, package managers, or other tools without explicit approval.
- If OSV-Scanner is missing, run available native audits and mark the evidence as incomplete.
- If no CVE scanner for the detected stack is available, return `scanner_unavailable` and provide exact install/setup options.
- If only manifests are present without lockfiles, return `weak_evidence` and explain that exact vulnerable versions are unknown.

## Final Checks

- Findings are tied to exact locked versions.
- Missing lockfiles are reported.
- Runtime/freshness checks are clearly separated from CVEs.
- Scanner sources are named.
- Recommended hook/CI placement matches scan cost.
- Any proposed dependency changes include verification commands.
