---
name: oss-security-audit
description: Audits the CI/CD pipeline, repository, release process, automations, and dependency hygiene of an open-source software supply chain, then produces an elegant HTML report of findings and recommendations. Use this skill whenever the user asks to assess, audit, review, harden, or evaluate the security of a repository, its GitHub Actions or GitLab CI pipelines, its release process, its supply chain, or its overall security posture — even if they don't use the word "audit." Also trigger on phrases like "is this repo secure," "check our CI," "supply chain review," "harden our release," "review our workflows," or when a user points at a repo and asks what they should fix.
---

# OSS Security Audit

Assess an open-source repository's supply chain security posture and produce an HTML report. The methodology is drawn from Astral's ["Open source security at Astral"](https://astral.sh/blog/open-source-security-at-astral) (April 2026), which distills hard-won practices from maintaining Ruff, uv, and ty in the wake of the Ultralytics, tj-actions, Nx, Trivy, and LiteLLM supply chain attacks.

The audit is LLM-driven. You are the auditor: there is no bundled scanner. Your job is to read the repo, query the forge (GitHub or GitLab) with whatever read-only tools are available, reason about the findings in the context of the framework below, and render a report.

## Posture

Approach this like a thoughtful security engineer doing a friendly review for a team that cares. Not a scanner spraying CVEs. Not a lecture. Findings should feel earned — each one tied to a concrete attacker capability or a concrete incident, with a concrete fix. If a repo is already doing something well, say so; the report is not just a list of sins.

## Workflow

### 1. Preflight: figure out what you can see

Before touching anything, determine what you have access to and ask for what you don't.

Default assumptions:
- The repo is the current working directory.
- On GitHub, the `gh` CLI is installed and authenticated (`gh auth status`). On GitLab, the `glab` CLI.
- You have read access to the repo's files and git history.
- Org-level, ruleset, and settings APIs may or may not be reachable depending on the user's role.

Run a quick probe:
1. Detect the forge — look for `.github/`, `.gitlab-ci.yml`, the remote URL.
2. Confirm CLI auth (`gh auth status` / `glab auth status`).
3. Try one low-privilege read against the forge API (e.g. `gh repo view --json nameWithOwner,visibility,defaultBranchRef`). If it fails, stop and ask the user to authenticate.
4. Try one org-scoped read (e.g. rulesets, org settings). If it fails, note that organizational controls will be audited from repo-visible evidence only, and tell the user what you can't see.

Then tell the user, in one short message:
- What forge and repo you detected
- What you have access to
- What you'd like access to but don't (and the exact command they can run to grant it, or a note that org-admin access is required)
- That all actions will be read-only, and you will not modify the repo or any settings

Wait for confirmation before proceeding to the audit. The user is trusting you to poke at their infrastructure; earn it by being explicit.

### 2. Audit: five domains

Work through these five domains. They are ordered by typical blast radius, not by how much work they take. For each, gather evidence, reason about gaps, and record findings with severity, evidence, and remediation.

Do not mechanically check every item. Use judgment. A tiny single-maintainer project and a multi-org monorepo should not receive the same recommendations — scale the rigor to the project.

#### Domain 1 — CI/CD workflow security

What you're looking for:

- **Dangerous triggers.** `pull_request_target`, `workflow_run`, `issue_comment` on public repos. These mix untrusted input with privileged tokens and are the root of nearly every well-known Actions compromise (Ultralytics, tj-actions, Nx began with pwn requests). Ask: does this workflow *actually need* the privileged context, or could it use `pull_request` and post results via job summaries / logs instead? Legitimate uses (cross-repo comments on third-party PRs) should move to a GitHub App — flag this as an "Automations" finding in Domain 4.
- **Unpinned actions.** Any `uses:` line that references a tag or branch rather than a full 40-character commit SHA is mutable and therefore a supply chain risk. Check every workflow file. Note: pinning the top-level action is necessary but not sufficient — the actions *it* calls internally must also be pinned, and GitHub's "require actions to be pinned to a full-length commit SHA" org policy is the only hard gate that enforces this transitively.
- **Impostor commits.** A pinned SHA that doesn't actually exist in the upstream repo's history (a fork commit masquerading as upstream). This is the class of bug `zizmor`'s `impostor-commit` audit catches. You likely can't cryptographically verify every pin by hand, but you can spot-check the riskiest ones and recommend `zizmor` + the org-level pin policy as the durable fix.
- **Immutability gaps inside pinned actions.** A pinned action that internally downloads a binary from a mutable URL (e.g. `gh release download latest`) punches a hole through the hash pin. This is subtle and rarely caught by tooling. Scan action sources for curl/wget/release-download patterns when the action is privileged. Recommend that upstreams embed a URL→hash map so the binary becomes part of the action's immutable state.
- **Permissions hygiene.** The default should be `permissions: {}` at the top of every workflow, with jobs broadening only what they need. Check the org default (`gh api /orgs/{org}/actions/permissions/workflow` if accessible) — it should be read-only. A workflow with no explicit `permissions:` block inherits the org default, which on many orgs is still `write-all`.
- **Secret isolation.** Secrets should live in deployment environments scoped to the jobs that need them, not as org- or repo-wide secrets available to every workflow run. A compromised lint job should not be able to read the PyPI token.
- **Caching in release paths.** Release workflows should not consume the Actions cache. Cache poisoning is a realistic pivot and has been used in the wild; the tradeoff of slightly slower releases is worth it.

Tools worth recommending (not required to run): `zizmor` for static analysis of workflows, `pinact` for automatic pinning.

#### Domain 2 — Repository and organizational controls

- **Branch protection on `main` (or default).** No force-push. PR required. No admin bypass. Check `gh api /repos/{owner}/{repo}/rules/branches/main` if accessible.
- **Tag protection / immutable tags.** Tags cannot be moved or deleted once created. The Trivy attack force-pushed over existing tags — this is the specific control that blocks that pivot.
- **Release tag gating.** Release tags should only come into existence *after* a successful release deployment, not before. This prevents an attacker from manually creating a tag to trigger a malicious release pathway.
- **Branch pattern bans.** Patterns like `advisory-*` or `internal-*` should be forbidden on public repos to prevent premature disclosure of in-flight security work.
- **Admin bypass.** All of the above must apply to admins. A ruleset that exempts admins is a ruleset that exempts whoever compromises an admin account.
- **2FA enforcement.** Org-level 2FA should be required and should be at least TOTP-strength. Phishing-resistant (WebAuthn / passkeys) is better where the forge supports enforcing it.
- **Admin sprawl.** Count org admins and repo admins. More admins = more accounts an attacker can target. Not every maintainer needs admin.

Much of this is only visible if the running user has org-admin privileges. When you can't see it, say so in the report and recommend the user verify manually — don't silently downgrade to a pass.

#### Domain 3 — Release security

- **Long-lived publishing credentials.** Any `PYPI_TOKEN`, `NPM_TOKEN`, `CARGO_TOKEN`, etc. stored as a secret is a liability. The target state is Trusted Publishing / OIDC to PyPI, crates.io, NPM, RubyGems, GHCR — whichever registries apply. Trusted Publishing eliminates the single most common post-compromise spread vector.
- **Deployment environments.** Release jobs should run in a dedicated environment (e.g. `release`), separate from test/lint environments, so a compromised linter never sees release secrets.
- **Two-person approval.** The release environment should require approval from at least one other privileged member. For fan-out release matrices (where GitHub fires an approval per job), recommend the `release-gate` → `release` hop via a minimal GitHub App, which is Astral's pattern.
- **Main-branch restriction on release.** Release deployments should only be creatable from `main`, never from a side branch.
- **Immutable releases.** On GitHub, the "immutable releases" feature should be on. This blocks the common attacker move of force-pushing a malicious build over a previously published release (used in the recent Trivy attack).
- **Attestations.** Sigstore-based build attestations (or PEP 740 attestations for PyPI) provide a cryptographic link from artifact to workflow. Not all projects need them, but any project shipping binaries should be generating them.
- **Installer integrity.** If the project ships a `curl | sh` installer, it should embed checksums of the binaries it downloads. Note the footnote caveat in the Astral post: if the installer is served from the same host as the binaries, the checksums primarily help downstream vendorers, not the `curl | sh` user.
- **Knock-on publishing.** Docs sites, version manifests, pre-commit hook repos, Homebrew taps — all of these are privileged writes that deserve the same discipline as the primary release. Fine-grained PATs issued to dedicated bot accounts, not personal tokens.

#### Domain 4 — Automations (GitHub Apps vs Actions)

The core insight from the blog: some things simply cannot be done securely in GitHub Actions. Leaving comments on third-party PRs, reacting to untrusted events with privileged credentials, doing anything that mixes attacker-controlled content with secrets. For these, the correct pattern is a separate GitHub App (or webhook consumer) that receives the same webhook payloads but runs in an isolated environment.

When you find a workflow straining against Actions' security model (typically a `pull_request_target` with elaborate sandboxing), recommend moving it to an App. Flag the caveat: an App does not eliminate credentials, it just moves them. The App itself still needs to be developed with a security mindset (input validation, no SQLi, no prompt injection into LLM calls, no running untrusted code with privileged tokens).

#### Domain 5 — Dependency hygiene

- **Automated updates.** Dependabot, Renovate, or equivalent should be configured. Absence is a finding.
- **Cooldowns.** Updates should not be applied immediately on release. A cooldown window (Renovate's `minimumReleaseAge`, Dependabot's equivalent, `uv`'s built-in support) is the single best defense against temporarily-compromised upstreams — the window during which a malicious release is most likely to be live. First-party dependencies can relax this; third-party should not.
- **Vulnerability surfacing.** Known vulns should be getting flagged (Dependabot alerts, `cargo audit`, `pip-audit`, etc.).
- **Dependency footprint.** Look at what's actually pulled in. Binary blobs, features enabled that aren't used, transitive crates for functionality the project doesn't exercise. Conservative dependency posture is a real control, not just aesthetics.
- **Upstream relationships.** Harder to audit from outside, but note whether the project contributes back to its upstreams — a healthy bidirectional relationship is how ecosystem security actually improves.

### 3. Severity

Assign each finding one of:

- **Critical** — direct path to supply chain compromise. Long-lived publishing token in a workflow reachable by `pull_request_target`. Unpinned third-party action in the release path. No 2FA on the org.
- **High** — meaningful blast radius amplifier. Unpinned actions generally. No deployment environments. Single-approver releases. Mutable release tags.
- **Medium** — real weakness without an obvious direct exploit today. No cooldowns. No attestations. Admin sprawl. Cache usage in release path.
- **Low** — hygiene and hardening. Missing `permissions: {}` default on workflows that happen to only read. Absent branch pattern bans. Documentation of release process.
- **Info / Strength** — things the project is already doing right. Include these. A report that's all negatives reads as noise.

Severity should reflect *this* project's risk, not a generic checklist. A single-maintainer CLI with no release automation does not have the same release-security surface as a tool downloaded millions of times per week.

### 4. Report

Render the final output to `oss-security-audit-report.html` in the repo root (or a path the user requests) using `assets/report-template.html` as the starting point. The template is self-contained — no external CSS, no webfonts, no JS frameworks. Fill in the placeholders and inject the findings.

**Structure, in order:**

1. **Header** — project name, forge, commit SHA audited, date, auditor note (one line: "Automated review based on the Astral OSS security framework").
2. **Executive summary** — 3–5 sentences. The shape of the posture, not a count. "This repo has strong branch protection and uses Trusted Publishing for PyPI, but every workflow uses unpinned actions and there is no two-person approval on release." Then the severity counts.
3. **Findings**, grouped by severity, Critical → Info. Each finding card contains:
   - **Title** — short, specific. "Release workflow uses mutable action tag", not "Unpinned action".
   - **Where** — file path(s) and line number(s), or the setting being referenced. Use `path:line` format.
   - **What** — one or two sentences on what was observed.
   - **Why it matters** — tied to a concrete attacker capability or a named incident. This is the part that earns the finding.
   - **Recommendation** — concrete and copy-pasteable where possible. Code blocks for YAML snippets. A `gh` or `glab` command where that's the fix. A link to the feature's docs where configuration is involved.
4. **Strengths** — what the project is already doing right, as a short list.
5. **Out of scope / not checked** — anything you couldn't verify (org-level settings you lacked access to, etc.). This is important for honesty and to give the user a manual follow-up list.
6. **Appendix: raw evidence** — collapsed by default. Workflow inventory, pinning status table, trigger inventory. This is where the "technical" lives, so the body of the report can stay readable.

**Visual principles** (these are baked into the template; don't override them):

- System font stack. `-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`.
- Neutral palette — ink on near-white, one cool accent for headings, muted severity chips (no screaming red). Severity is conveyed by label + a thin colored left border, not by background fill.
- Generous whitespace, left-aligned, single column, max-width ~760px for body text. Findings can break out slightly wider for code blocks.
- No emoji. No icons beyond a simple severity chip. No gradients. No "dashboard" feel.
- Code blocks in a monospace stack with a light surface, not a dark terminal look.

The report should look like something you would send to a CTO, not a pentest tool's default export.

## Closing the loop

After writing the report, tell the user:
- Where the report is
- The headline finding (the single thing you'd fix first)
- Anything you needed to skip because of access limits, with the exact command or setting they'd need to grant or check manually

Keep the closing message short. The report is the deliverable; don't re-summarize it in chat.

## When things don't fit

If the repo is fundamentally different from the model this framework assumes (no CI at all, a mirror of an upstream, a personal dotfiles repo, a template repo, a Rust crate with no releases), say so plainly and scope the audit down. Don't invent findings to fill sections. An honest "this repo has no release process, so Domain 3 is not applicable" is more valuable than a fabricated recommendation. The goal is useful security advice, not a uniform report.
