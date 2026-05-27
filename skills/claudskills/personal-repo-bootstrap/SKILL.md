---
description: Bootstrap a new personal repo with industry-best-practice docs and defensive .gitignore. Routes by repo type (scratch / personal-published / portfolio-public). Ensures secrets/PII protection from the first commit. Triggered by 'create new repo', 'bootstrap [name]', '/repo-bootstrap'.
---

# personal-repo-bootstrap

Scaffolds a new repo with the right docs from day 1. "I'll add docs later" never works.

## Trigger phrases

- "Create a new repo for [purpose]"
- "Bootstrap [name]"
- `/repo-bootstrap [name]`

## Repo types

| Type | Purpose | Visibility | Docs scope |
|---|---|---|---|
| `scratch` | Throwaway exploration | Local-only, no remote | Minimal — README, .gitignore |
| `personal-published` | Personal projects on GitHub, low-traffic | Public or private GitHub | README, LICENSE, .gitignore, AGENTS.md |
| `portfolio-public` | Public portfolio piece, intended for recruiter visibility | Public, polished | All of the above + ARCHITECTURE.md, demo, screenshots |
| `learning` | Coursework, tutorials, learning artefacts | Local or private | README, minimal |

## Process

### Step 1 — Interview

Ask 4 questions:

1. **Type:** scratch / personal-published / portfolio-public / learning?
2. **Name + slug** (lowercase-kebab, will become repo name)
3. **One-line purpose** (will go in README + GitHub description)
4. **Tech stack** (so .gitignore can be tuned — Python, Node, Rust, etc.)

### Step 2 — Generate folder + git init

```bash
mkdir -p ~/Documents/OpenCode\ Working\ Folder/{slug}
cd ~/Documents/OpenCode\ Working\ Folder/{slug}
git init
```

For `portfolio-public`, use `~/Projects/{slug}/` IF the repo will have launchd agents or daemon dependencies. Otherwise OWF.

### Step 3 — Generate baseline files

**`.gitignore`** — defensive baseline + tech-stack-specific:

```
# Defensive baseline (every personal repo)
.env
.env.*
*.key
*.pem
*.p12
.DS_Store
master-cv*.md
master-cv*.pdf
master-cv*.docx
.career/
**/private/
**/secrets/
*.log
.vscode/
.idea/

# Tech-stack additions (Node example)
node_modules/
dist/
build/
*.tsbuildinfo
.npm

# Tech-stack additions (Python example)
__pycache__/
*.py[cod]
*$py.class
.Python
*.egg-info/
.pytest_cache/
.venv/
venv/
```

**`README.md`** — populated template:

```markdown
# {Name}

[One-line purpose from interview]

## Status

🚧 [scratch / WIP / stable]

## Quick start

[For personal-published+: minimal install + run instructions]

## Architecture

[For portfolio-public: link to ARCHITECTURE.md]

## License

[For personal-published+: see LICENSE]
```

**`LICENSE`** (personal-published / portfolio-public only) — MIT default, prompt to confirm.

**`AGENTS.md`** (personal-published / portfolio-public) — minimal project-level rules:

```markdown
# Project AGENTS — {Name}

## Conventions

- [Tech-stack-specific conventions]

## Build / test

[Commands]

## Anything else AI should know

- [...]
```

**`ARCHITECTURE.md`** (portfolio-public only) — section scaffold:

```markdown
# Architecture

## Overview

## Components

## Data flow

## Trade-offs and decisions
```

### Step 4 — Pre-flight scan

Before saying "done":

1. **Em-dash scan** — README and AGENTS.md should be em-dash-free if intended for public/recruiter visibility
2. **PII scan** — no phone, address, real email beyond Josh's standard one
3. **Secrets scan** — no inline tokens / keys / passwords
4. **License match** — if portfolio-public, confirm MIT (or alternative) is set

### Step 5 — First commit

Initial commit message: `Initial commit: scaffolding`

```bash
git add .
git commit -m "Initial commit: scaffolding for {Name}"
```

DO NOT push to remote yet. That requires Josh's confirmation per the safety rules.

### Step 6 — Output

```markdown
**Repo bootstrapped** at `[path]`

**Type:** [type]
**Files created:**
- README.md ([N] lines)
- .gitignore ([N] entries, defensive baseline + [stack]-specific)
- AGENTS.md (minimal) [if applicable]
- LICENSE (MIT) [if applicable]
- ARCHITECTURE.md [if applicable]

**Pre-flight scan:** all green ✅

**Next steps:**
- [ ] Review README — fill in the [TODO] sections
- [ ] If GitHub remote desired, create the repo on GitHub then `git remote add origin ...`
- [ ] First feature commit when ready
```

## Discipline

- The defensive .gitignore is non-negotiable. Even for scratch repos. Cost of a leaked .env is higher than 5 lines of gitignore.
- Master-CV files are git-ignored by default. To explicitly include a sanitized version in a portfolio repo, name it differently (e.g., `resume-public.md`) and add to .gitignore exception.
- For portfolio-public, the README quality bar is high. Recruiters read these. Josh should review thoroughly.
