---
name: fix-guardrails
description: Fix all guardrail findings (make lint, make test, make sast) across repositories. Use when the user asks to fix linting errors, test failures, SAST findings, or run the full guardrail remediation workflow.
---

Fix all guardrail findings (`make lint`, `make test`, `make sast`) across one or more repositories. This is a complete, repeatable workflow: sync with main, run all guardrails, fix every finding, update documentation, commit following standards, push, and create PRs.

For guardrail tools, refer to the CI/CD rule and Security rule. For commit conventions, refer to the Git Flow rule. For changelog updates, refer to the Documentation rule.

## Vendor Detection

Auto-detect the Git hosting vendor from `git remote get-url origin` to determine the correct PR creation CLI:

| Remote URL contains                    | Vendor       | PR CLI                                     |
|----------------------------------------|--------------|--------------------------------------------|
| `github.com`                           | GitHub       | `gh pr create`                             |
| `dev.azure.com` or `ssh.dev.azure.com` | Azure DevOps | `az repos pr create`                       |
| `gitlab.com` or `gitlab`               | GitLab       | `glab mr create`                           |
| Other                                  | Unknown      | Skip PR, report branch for manual creation |

---

## Step-by-step Workflow (repeat for every repository)

### Step 1 -- Sync with the default branch

```bash
cd <REPO_PATH>
git checkout <default-branch>
git fetch --all
git pull --rebase
```

- Detect the default branch with `git symbolic-ref refs/remotes/origin/HEAD` (strip `refs/remotes/origin/`). Fall back to `main` if unavailable.
- If `pull --rebase` fails due to conflicts, report the failure and **skip this repo**.

### Step 2 -- Run all three guardrails

Run them **in this exact order**. Each gate must be evaluated independently -- even if one passes, the others may fail.

#### Gate 1: Lint

```bash
make lint
```

- Timeout: **3 minutes**.
- Parse the output. Record every finding with **file path**, **line number**, **rule**, and **message**.
- NEVER invoke linter binaries directly. Always use `make lint`.

#### Gate 2: Test

```bash
make test
```

- Timeout: **5 minutes**.
- Record any failing test names and error messages.
- NEVER invoke test runners directly. Always use `make test`.

#### Gate 3: SAST

```bash
make sast
```

- Timeout: **10 minutes** -- SAST is the slowest gate (it runs CodeQL, Semgrep, Trivy, Hadolint, and Gitleaks).
- Parse the output. Record every finding with **tool name**, **rule ID**, **file path**, **line number**, and **description**.
- NEVER invoke SAST tools directly. Always use `make sast`.

#### Decision point

- If **all three gates pass** with 0 findings: print `<repo>: SKIP(clean)` and move to the next repo.
- If **any gate has findings**: proceed to Step 3.

### Step 3 -- Create the feature branch

```bash
git checkout -b fix/<scope>
```

**Branch naming rules** (from the Git Flow rule):

- Format: `type/scope`
- Choose the scope based on what was found:
  - Lint-only findings: `fix/lint-findings`
  - SAST-only findings: `fix/sast-findings`
  - Test-only findings: `fix/test-findings`
  - Mixed findings: `fix/guardrail-findings`
  - If a specific tool dominates: `fix/codeql-findings`, `fix/semgrep-findings`, etc.
- The branch type is always `fix` for guardrail remediation.

### Step 4 -- Fix each finding

Read the affected files, understand the context, and apply a **minimal, targeted fix** for each finding. Never refactor surrounding code.

#### 4a. Lint fix patterns

| Linter / Rule                       | Root Cause                                       | Fix                                                            |
|-------------------------------------|--------------------------------------------------|----------------------------------------------------------------|
| `unused variable/import`            | Dead code left after refactoring                 | Remove the unused variable or import                           |
| `ineffectual assignment`            | Variable assigned but never read                 | Remove assignment or use the value                             |
| `errcheck` / unchecked error        | Return value of error-returning function ignored | Assign to `err` and handle it, or explicitly ignore with `_ =` |
| `staticcheck` / deprecated API      | Using deprecated function                        | Replace with the recommended alternative                       |
| `govet` / struct field alignment    | Struct fields not optimally ordered              | Reorder fields by size (largest first)                         |
| `revive` / exported without comment | Exported symbol missing doc comment              | Add a doc comment starting with the symbol name                |

#### 4b. Test fix patterns

| Failure Type              | Root Cause                                           | Fix                                                                                                    |
|---------------------------|------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Assertion mismatch        | Code behavior changed but test not updated           | Update the test expectation to match the new correct behavior, or fix the code if the test was correct |
| Compilation error in test | Test references a removed/renamed symbol             | Update the test to use the new symbol                                                                  |
| Timeout                   | Test relies on external service or has infinite loop | Fix the logic or add proper mocking                                                                    |
| Race condition            | Shared state across parallel tests                   | Add proper synchronization or use `t.Parallel()` correctly                                             |

**Important:** Tests must follow BDD structure (`// given`, `// when`, `// then`). If you modify a test, preserve or add this structure.

#### 4c. SAST fix patterns

**CodeQL:**

| Rule                             | Root Cause                                                                                                 | Fix                                                                                                                                    |
|----------------------------------|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `go/useless-assignment-to-field` | Value receiver stores a parameter in a struct field used only through method values on the same local copy | Remove the struct field. Replace callback methods with **inline closures** capturing the parameter.                                    |
| `go/disabled-certificate-check`  | `InsecureSkipVerify: true` hardcoded in `tls.Config`                                                       | Replace the hardcoded `true` with a configurable setting field. Add `// #nosec G402 -- controlled via configuration` on the same line. |
| `go/sql-injection`               | String concatenation in SQL queries                                                                        | Use parameterized queries (`$1`, `$2`) or whitelist-validated identifiers                                                              |
| `go/path-injection`              | Unsanitized user input in file paths                                                                       | Sanitize with `filepath.Clean` and validate against an allowed base path                                                               |
| `go/log-injection`               | User-controlled input directly in log messages                                                             | Use structured logging fields instead of string interpolation                                                                          |

**Semgrep:**

| Pattern                       | Root Cause                                                            | Fix                                                        |
|-------------------------------|-----------------------------------------------------------------------|------------------------------------------------------------|
| Hardcoded secret / credential | API key, password, or token in source code                            | Move to environment variable or secret manager             |
| OWASP rule violation          | Insecure coding pattern (e.g., weak crypto, missing input validation) | Apply the recommendation from the Semgrep rule description |
| Anti-pattern                  | Code smell flagged by Semgrep rules                                   | Refactor to the recommended pattern                        |

**Trivy (IaC scanning):**

| Finding                     | Root Cause                                           | Fix                                                        |
|-----------------------------|------------------------------------------------------|------------------------------------------------------------|
| Dockerfile misconfiguration | Running as root, unpinned base image, etc.           | Pin image tags, add `USER nonroot`, use multi-stage builds |
| Kubernetes misconfiguration | Missing resource limits, privileged containers, etc. | Add resource limits, set `securityContext` properly        |
| Terraform misconfiguration  | Missing encryption, overly permissive IAM, etc.      | Enable encryption, restrict IAM policies                   |

**Hadolint (Dockerfile):**

| Rule     | Root Cause                          | Fix                                   |
|----------|-------------------------------------|---------------------------------------|
| `DL3007` | Using `latest` tag                  | Pin to a specific version             |
| `DL3008` | Unpinned `apt-get install`          | Pin package versions                  |
| `DL3025` | Using `CMD` instead of `ENTRYPOINT` | Use `ENTRYPOINT` for the main command |
| `SC2086` | Unquoted variable in `RUN`          | Quote the variable                    |

**Gitleaks (secrets):**

| Finding                   | Root Cause                             | Fix                                                                                |
|---------------------------|----------------------------------------|------------------------------------------------------------------------------------|
| Secret detected in source | Hardcoded secret, API key, or password | Remove from source, add to `.gitignore`, rotate the exposed credential immediately |
| Secret in git history     | Previously committed secret            | Remove with `git filter-branch` or BFG, then rotate credentials                    |

For **any rule not listed above**: analyze the code, apply a minimal fix, and document the new pattern in the commit message body.

### Step 5 -- Verify build

Run the appropriate build verification for the detected language:

| Language              | Build command                        |
|-----------------------|--------------------------------------|
| Go                    | `go build ./...`                     |
| JavaScript/TypeScript | `npm run build` or `yarn build`      |
| Python                | `python -m py_compile <main-module>` |
| Java                  | `./gradlew build` or `mvn compile`   |

If compilation fails, diagnose and fix before proceeding.

### Step 6 -- Re-run the failing guardrails

After applying fixes, re-run **only the guardrails that originally failed**:

```bash
make lint   # if lint had findings
make test   # if tests were failing
make sast   # if SAST had findings
```

If new findings appear, fix them. Repeat until all three gates pass. If you cannot resolve a finding after 2 attempts, document it and proceed -- the PR description should note unresolved items.

### Step 7 -- Update CHANGELOG.md

Read the existing `CHANGELOG.md`. Under `## [Unreleased]`, add entries in the appropriate category. Follow the Documentation rule for changelog conventions:

- Use **simple past tense**: "fixed", "removed", "replaced"
- Start each entry with a **lowercase verb**
- Use [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) categories

### Step 8 -- Stage and commit

Stage only the files you changed. Follow the Git Flow rule for commit message format:

- Format: `fix(<scope>): <subject in simple past tense>`
- Use bullet points for multi-file changes

### Step 9 -- Push the branch

```bash
GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=15" git push -u origin <branch> --force
```

- `--force` is safe because this is a **new branch we just created**

### Step 10 -- Restore the original branch

```bash
git checkout <default-branch>
```

### Step 11 -- Create Pull Request

Use the detected vendor CLI (GitHub: `gh pr create`, Azure DevOps: `az repos pr create`, GitLab: `glab mr create`).

**PR title rules:**

- Format: `fix(<scope>): resolved <tool/gate> findings`
- Under 70 characters
- Simple past tense, lowercase

## Error Handling

| Situation                                      | Action                                                                                    |
|------------------------------------------------|-------------------------------------------------------------------------------------------|
| `git pull --rebase` fails                      | Print `FAIL(rebase conflict)`, restore branch, skip repo                                  |
| `make lint` times out                          | Print `FAIL(lint timeout)`, skip repo                                                     |
| `make test` times out                          | Print `FAIL(test timeout)`, skip repo                                                     |
| `make sast` times out                          | Print `FAIL(sast timeout)`, skip repo                                                     |
| Build fails after fix                          | Diagnose and fix; if unresolvable, print `FAIL(build)`, restore branch, skip repo         |
| Re-run still has findings after 2 fix attempts | Document unresolved items in PR description, proceed with commit                          |
| `git push` fails                               | Print `FAIL(push: <error>)`, restore branch, skip repo                                    |
| PR creation fails                              | Print `FAIL(pr: <error>)` but branch is already pushed -- report for manual PR creation   |
| Unknown rule from any tool                     | Read and analyze the code, apply minimal fix, document in commit message                  |
| Gitleaks finds a real secret                   | **Stop immediately**, warn the user, do NOT commit the secret -- it must be rotated first |
