---
name: canopy-runtime
description: Canopy framework execution engine. Interprets canopy-flavored skills (any SKILL.md with a `## Tree` section) at runtime — platform detection, section semantics (`## Agent`/`## Tree`/`## Rules`/`## Response:`), tree notation (`<<`, `>>`, `|`), control-flow primitives (`IF`/`ELSE_IF`/`ELSE`/`SWITCH`/`CASE`/`DEFAULT`/`FOR_EACH`/`BREAK`/`END`), interaction primitives (`ASK`/`SHOW_PLAN`), execution primitives (`EXPLORE`/`VERIFY_EXPECTED`), op lookup chain, category directory semantics, subagent contract. Install this to execute existing canopy skills. Install `canopy` (the authoring agent) too if you need to create/edit/manage them.
license: MIT
compatibility: Root dependency — declares no upstream skill requirement. Self-contained for activation, bundling its own marker-block content at `assets/constants/marker-block.md`. Supports Claude Code and GitHub Copilot; halts on unsupported hosts.
metadata:
  version: "0.18.0"
  author: kostiantyn-matsebora
  user-invocable: "false"
---

# Canopy Runtime

The execution engine for canopy-flavored skills. Any skill whose `SKILL.md` declares a `## Tree` section is canopy-flavored and relies on this spec.

## Skills root resolution

`<skills-root>` is the directory containing this `canopy-runtime/SKILL.md`. Recognized roots, first match wins:

- `.agents/skills/` — cross-agent install (gh skill install default on Copilot and other hosts since gh 2.91)
- `.claude/skills/` — Claude Code
- `.github/skills/` — GitHub Copilot

All path references in this spec (e.g. `<skills-root>/canopy-runtime/references/...`) resolve relative to the matched root. Skills installed at any of the three locations are equally valid; what matters is consistency within a single project.

## Platform detection (runtime self-identification)

The active platform is **not** derived from the skills-root path. The agent self-identifies which host it is and applies the matching runtime spec:

- Claude Code → apply `<skills-root>/canopy-runtime/references/runtime-claude.md`
- GitHub Copilot → apply `<skills-root>/canopy-runtime/references/runtime-copilot.md`
- Other hosts → **halt** with error: "This skill requires canopy-runtime, which currently supports Claude Code and GitHub Copilot only."

Signals an agent may use to identify itself (any one is sufficient):

- Self-knowledge — the agent knows which product it is (Claude Code, Copilot, etc.)
- Tool surface — native subagent / Task-tool capability is present on Claude Code
- Workspace markers — `CLAUDE.md` at project root with the canopy-runtime marker block indicates Claude Code is the host; `.github/copilot-instructions.md` with the marker block indicates Copilot

## Activation

Activation is **agent-mediated**, not install-tool-mediated. This section is a contract that an agent runs the **first time it loads `canopy-runtime/SKILL.md`** in a given workspace. Pure CLI install paths (`gh skill install`, `install.sh`/`install.ps1`, plugin marketplace) only place files on disk — they do not (and cannot) execute this section. The marker block lands in the workspace's instructions file the first time an agent loads this SKILL.md and runs the steps below.

On first load by an agent, ensure the canopy-runtime marker block is present in the active platform's instructions file. This makes future sessions auto-load the runtime without rerunning this step.

1. Identify the active platform per **Platform detection** above.
2. Resolve the marker destination:
   - Claude Code → `CLAUDE.md` at the project root
   - GitHub Copilot → `.github/copilot-instructions.md`
3. If the destination file does not contain `<!-- canopy-runtime-begin -->`, write the canonical marker block defined in `assets/constants/marker-block.md` (alongside this `SKILL.md`). Apply the idempotent-write contract: CREATE if absent, APPEND if no markers, REPLACE if exactly one marker pair exists, WARN if multiple, REFUSE if mismatched.
4. Idempotent — running on a fully activated project is a no-op.

This replaces explicit `/canopy activate` once an agent has loaded the runtime at least once. For plugin and `gh skill install` paths the install itself is just file placement; the marker block is written when the next agent invocation loads this SKILL.md and runs Activation. The `install.sh` / `install.ps1` paths additionally write the marker block during install (since those scripts run in a shell context and have no agent), so for those paths the project is already fully activated when the install completes.

## What the runtime defines

- **Sections** — `## Agent` (optional explore subagent), `## Tree` (sequential execution pipeline), `## Rules` (skill-wide invariants), `## Response:` (output format). See `references/skill-resources.md`.
- **Notation** — `<<` input source/options, `>>` captured output/displayed fields, `|` separator. See `references/skill-resources.md`.
- **Control-flow primitives** — `IF`, `ELSE_IF`, `ELSE`, `SWITCH`, `CASE`, `DEFAULT`, `FOR_EACH`, `BREAK`, `END`. See `references/framework-ops.md`.
- **Interaction primitives** — `ASK`, `SHOW_PLAN`. See `references/framework-ops.md`.
- **Execution primitives** — `EXPLORE` (first node when `## Agent` declares `**explore**`), `VERIFY_EXPECTED`. See `references/framework-ops.md`.
- **Op lookup chain** — `<skill>/references/ops.md` (or `<skill>/references/ops/<name>.md`) → consumer-defined cross-skill ops → `references/framework-ops.md` for framework primitives. See `references/skill-resources.md`. Older skills with `<skill>/ops.md` at root remain supported for backward compatibility.
- **Category directories** — `scripts/` (executable code), `references/` (docs loaded on demand, including `ops.md`/`ops/`), `assets/` (static resources: `templates/`, `constants/`, `schemas/`, `checklists/`, `policies/`, `verify/`). Each has defined behavior. See `references/skill-resources.md`.
- **Tree syntax** — markdown-list (`*` nested bullets) and box-drawing (fenced tree characters). Both recognized. See `references/skill-resources.md`.
- **Preamble** — text between frontmatter and `## Tree` parses `$ARGUMENTS`. Canopy-flavored skills additionally include a safety preamble that halts execution on agents without canopy-runtime loaded. See `references/skill-resources.md`.
- **Subagent contract** — `## Agent` declaring `**explore**` requires `EXPLORE >> context` as first tree node and schema at `assets/schemas/explore-schema.json`. See `references/skill-resources.md`.
- **Platform-specific execution** — Claude uses native subagents; Copilot falls back to inline sequential reading. See `references/runtime-claude.md` and `references/runtime-copilot.md`.

## Not a user-invocable skill

`canopy-runtime` is hidden from the `/` menu (`metadata.user-invocable: "false"`). It is loaded:
- Ambiently via the `canopy-runtime` marker block (written by the **Activation** section above on first run, or by install scripts).
- Explicitly by the `canopy` authoring agent and `canopy-debug` trace skill at the top of their trees.
- On-demand by Claude's skill-description discovery when a canopy-flavored skill is invoked.
