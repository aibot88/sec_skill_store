# Adding a skill (submodule workflow)

Every skill in this repository (except `_template`) **must** be added as a
[git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules). This
ensures the source code is fully auditable — each skill points to a specific
commit in its own repository, with full history and provenance.

## 1. Create the skill repository

Start a **new** GitHub repository for the skill. Use the `_template` directory
as your starting point:

```bash
# Copy the template into a new local repo
cp -r skills/_template /tmp/my-skill
cd /tmp/my-skill
git init && git add . && git commit -m "Initial skill from _template"
```

Push it to GitHub (e.g., `https://github.com/<org>/deerflow-skill-<name>`).

> **Tip:** You can also use GitHub's "Use this template" feature if the
> `_template` directory is published as a template repository.

## 2. Customize the skill

In the new repository, replace all `<skill-name>` placeholders and implement
your skill following the [skill standard](skill-standard.md).

## 3. Add the skill as a submodule

Back in this repository:

```bash
git submodule add https://github.com/<org>/deerflow-skill-<name>.git skills/<name>
git commit -m "Add <name> skill as submodule"
```

## 4. Run the security audit locally

Before opening a PR, verify that the skill image passes the security audit:

```bash
cd skills/<name>
make audit   # generates SBOM with Syft and scans for CVEs with Grype
```

The `audit` target:
1. Builds the skill Docker image.
2. Runs [Syft](https://github.com/anchore/syft) to produce a Software Bill of
   Materials (`sbom-<name>.spdx.json`).
3. Runs [Grype](https://github.com/anchore/grype) to scan for known
   vulnerabilities and fails if any **Critical** severity CVE is found.

If Grype reports critical findings, update the skill's base image or dependencies
to resolve them before adding the submodule to this repository.

> **CI enforcement:** The `Security Audit` workflow automatically builds and scans
> every changed skill on PRs and pushes to `main`. The `GHCR Publish` workflow
> additionally gates image publishing on a passing Grype scan.

## 5. Updating a skill

To pull the latest commit from a skill's upstream repository:

```bash
cd skills/<name>
git pull origin main
cd ../..
git add skills/<name>
git commit -m "Update <name> skill to latest"
```

## 6. Cloning this repository

Anyone cloning `deerflow-skills` should initialize submodules:

```bash
git clone --recurse-submodules https://github.com/8r4n/deerflow-skills.git
# Or, after a regular clone:
git submodule update --init --recursive
```

## Why submodules?

| Benefit | Detail |
|---------|--------|
| **Auditability** | Each skill pins to an exact commit SHA — you can inspect the full history of every dependency. |
| **Separation of concerns** | Skill authors iterate in their own repo; this repo only tracks which version is blessed. |
| **Reproducibility** | A checkout of this repo at any commit produces the exact same set of skill sources. |
