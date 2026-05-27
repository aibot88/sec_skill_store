---
name: hooman-skills
description: Manage Hooman skills under ~/.hooman/skills. Use when the user asks to list, search, add, install, create, update, remove, inspect, or author Hooman skills and SKILL.md files.
---

# Hooman Skills

Use this skill when the user asks you to inspect, install, remove, create, or change Hooman's skills.

## Source Of Truth

- Hooman user-installed skills live under `~/.hooman/skills`.
- Each installed skill is a directory directly under `~/.hooman/skills`.
- Each skill directory must contain a `SKILL.md` file.
- Built-in skills shipped with Hooman are separate from user-installed skills. Do not edit bundled skill files when the user means their installed skills.

Example layout:

```text
~/.hooman/skills/
  code-review/
    SKILL.md
    reference.md
  jira-workflow/
    SKILL.md
```

## Operating Rules

1. Use the `skills` CLI for catalog search, installs, listing, and removal when the user asks for those operations.
2. Run every `skills` CLI command with working directory `~/.hooman` so the OpenClaw layout maps to `~/.hooman/skills`.
3. Hooman discovers installed skills by scanning direct child directories under `~/.hooman/skills` for `SKILL.md`.
4. Preserve unrelated skill folders and files.
5. Treat files inside a skill directory as user data. Read before overwriting.
6. Never delete a skill folder unless the user explicitly asks to remove that skill.
7. For custom local authoring or edits, create/edit files directly under `~/.hooman/skills/<folder>`.
8. Any skill install, removal, creation, or edit requires restarting the running Hooman agent/session before the available-skills prompt changes.

## Exact CLI Commands

Use these commands for Hooman skill management:

Working directory:

```bash
mkdir -p ~/.hooman && cd ~/.hooman
```

Run the following commands from that directory. If using a shell tool that supports a working-directory option, set it to `~/.hooman` instead of relying on a previous `cd`.

List installed skills:

```bash
npx --yes skills@latest list --json -a openclaw
```

Search the public skills catalog:

```bash
npx --yes skills@latest find "query"
```

Add/install a skill into Hooman:

```bash
npx --yes skills@latest add "<source>" -y -a openclaw --copy
```

Remove a skill:

```bash
npx --yes skills@latest remove "<skill-or-folder>" -y
```

Command notes:

- `<source>` can be a package source accepted by the skills CLI, such as `owner/repo`, a GitHub URL, or a local path.
- Use `--copy` for Hooman installs so skill files are copied into `~/.hooman/skills` instead of relying on symlinks.
- If `list --json` fails or output is not useful, inspect `~/.hooman/skills` directly.
- After installing or removing, verify the result by checking `~/.hooman/skills/<folder>/SKILL.md`.

## SKILL.md Shape

Every `SKILL.md` should start with YAML frontmatter:

```markdown
---
name: skill-name
description: What this skill does and when Hooman should use it.
---

# Skill Title

Instructions for the agent.
```

Rules:

- `name` should be lowercase words separated by hyphens when possible.
- `description` should be specific and include trigger scenarios, because Hooman uses it to decide when the skill applies.
- Keep the main `SKILL.md` focused. Put long references in nearby files such as `reference.md` and link to them.
- Use relative links only inside the same skill directory.

## Listing Skills

To list installed skills without relying on CLI output:

1. Open `~/.hooman/skills`.
2. For each direct child directory, look for `SKILL.md`.
3. Read each `SKILL.md` frontmatter.
4. Report the frontmatter `name`, `description`, folder name, and `SKILL.md` path.

Ignore files and directories that do not contain `SKILL.md`.

## Creating A Skill Manually

Create a new skill by making a directory under `~/.hooman/skills`:

```text
~/.hooman/skills/<folder>/SKILL.md
```

Use a safe folder name:

- lowercase letters, numbers, and hyphens
- no slashes
- no `..`
- no spaces

Minimal example:

```markdown
---
name: pull-request-review
description: Review pull requests for correctness, maintainability, tests, and project conventions. Use when the user asks to review a PR, diff, branch, or code changes.
---

# Pull Request Review

When reviewing code, lead with findings ordered by severity. Focus on bugs,
regressions, missing tests, and maintainability risks.
```

Creation checklist:

- Clarify the skill's purpose, trigger scenarios, and expected behavior.
- Choose a folder name that is short, lowercase, and hyphenated.
- Write a specific frontmatter `description` that includes when to use the skill.
- Keep `SKILL.md` concise and actionable.
- Put longer reference material in files next to `SKILL.md`, such as `reference.md` or `examples.md`.
- Link supporting files with relative links.
- Avoid time-sensitive claims unless the skill explicitly needs them.
- Do not include secrets in skill files.

## Updating A Skill

To update an installed skill:

1. Locate the folder under `~/.hooman/skills`.
2. Read its current `SKILL.md` and any referenced files.
3. Make the smallest edit that satisfies the request.
4. Preserve frontmatter unless the user asked to rename or retarget the skill.
5. Keep supporting files in the same skill directory.

If changing the frontmatter `name`, consider whether the folder name should also change. Rename only when the user asks or the old folder name is clearly wrong.

## Installing By Copying Or CLI

Prefer the CLI for normal installs:

```bash
npx --yes skills@latest add "<source>" -y -a openclaw --copy
```

To install from a local skill directory manually:

1. Verify the source directory contains `SKILL.md`.
2. Choose a destination folder under `~/.hooman/skills`.
3. Copy the skill directory into that destination.
4. If the destination already exists, ask before replacing or merge carefully after reading both copies.

For GitHub or web sources, prefer `skills add`. Fetch or clone manually only when the user asks or the CLI cannot handle the source. After retrieval, install by copying the actual skill directory into `~/.hooman/skills`.

## Removing A Skill

To remove a skill:

1. Confirm the exact skill name or folder.
2. Prefer the CLI removal command:

```bash
npx --yes skills@latest remove "<skill-or-folder>" -y
```

3. Verify the folder is gone from `~/.hooman/skills`.
4. If manual deletion is required, verify the folder contains `SKILL.md` and delete only that folder.

Do not remove built-in Hooman skills or unrelated folders.

## Common Mistakes

- Do not create a single `~/.hooman/skills/SKILL.md`; each skill needs its own folder.
- Do not put installed Hooman skills under Cursor's `~/.cursor/skills` directory.
- Do not edit bundled Hooman skills when the user asked to install or update a personal skill.
- Do not assume a catalog result is installed. A skill is installed only when its folder exists under `~/.hooman/skills` with `SKILL.md`.
