---
name: canopy
description: Authors, validates, improves, scaffolds, and refactors Canopy skills using a structured control-flow notation (IF, ELSE_IF, ELSE, SWITCH, CASE, DEFAULT, FOR_EACH, BREAK, END, ASK, SHOW_PLAN, VERIFY_EXPECTED). Use when creating, modifying, debugging, or reviewing skills under `.claude/skills/` or `.github/skills/`, when the user mentions canopy, ops, control-flow notation, or skill scaffolding, or asks to convert a regular skill into a Canopy skill (and vice versa). Supports both Claude Code and GitHub Copilot.
license: MIT
compatibility: Requires the canopy-runtime skill (published at github.com/kostiantyn-matsebora/claude-canopy). Install with any agentskills.io-compatible tool — e.g. `gh skill install`, `git clone`, the repo's `install.sh`/`install.ps1`, or the Claude Code plugin marketplace. Supports Claude Code and GitHub Copilot.
allowed-tools: Read Write Edit Glob Grep Bash
metadata:
  version: "0.18.0"
  author: kostiantyn-matsebora
---

> **Runtime required.** This skill uses Canopy tree notation; canopy-runtime must be active.
>
> **Detect canopy-runtime** — present if either:
> - `canopy-runtime/SKILL.md` exists under `.claude/skills/`, `.github/skills/`, or `.agents/skills/`, OR
> - a canopy-runtime marker block exists in `CLAUDE.md` or `.github/copilot-instructions.md`.
>
> **If neither is present** — install canopy-runtime first (see the `compatibility` field for the source and install options), then re-invoke this skill.
>
> Do not interpret the `## Tree` without canopy-runtime active.

$ARGUMENTS

---

## Agent

**explore** — execute `FETCH_DISPATCH_CONTEXT`. Output contract: `assets/schemas/dispatch-schema.json`.

---

## Tree

* canopy
  * EXPLORE >> context
  * IF << context.operation requires an explicit skill name (IMPROVE, MODIFY, VALIDATE, SCAFFOLD, CONVERT_TO_CANOPY, CONVERT_TO_REGULAR) AND context.target_skill is null
    * ASK << Which skill should I {context.operation}? Please name it explicitly.
  * IF << context.platform == "claude"
    * Read `../canopy-runtime/SKILL.md` for the canopy execution engine overview
    * Read `../canopy-runtime/references/runtime-claude.md` for Claude Code runtime rules
    * Read `../canopy-runtime/references/framework-ops.md` for primitive spec
    * Read `../canopy-runtime/references/skill-resources.md` for category semantics, op lookup chain, tree format, subagent contract
  * ELSE
    * Read `../canopy-runtime/SKILL.md` for the canopy execution engine overview
    * Read `../canopy-runtime/references/runtime-copilot.md` for Copilot runtime rules
    * Read `../canopy-runtime/references/framework-ops.md` for primitive spec
    * Read `../canopy-runtime/references/skill-resources.md` for category semantics, op lookup chain, tree format, subagent contract
  * SWITCH << context.operation
    * CASE << "CREATE"
      * Read `references/ops/create.md` and execute the CREATE procedure
    * CASE << "MODIFY"
      * Read `references/ops/modify.md` and execute the MODIFY procedure
    * CASE << "SCAFFOLD"
      * Read `references/ops/scaffold.md` and execute the SCAFFOLD procedure
    * CASE << "CONVERT_TO_CANOPY"
      * Read `references/ops/convert-to-canopy.md` and execute the CONVERT_TO_CANOPY procedure
    * CASE << "VALIDATE"
      * Read `references/ops/validate.md` and execute the VALIDATE procedure
    * CASE << "IMPROVE"
      * Read `references/ops/improve.md` and execute the IMPROVE procedure
    * CASE << "ADVISE"
      * Read `references/ops/advise.md` and execute the ADVISE procedure
    * CASE << "REFACTOR_SKILLS"
      * Read `references/ops/refactor-skills.md` and execute the REFACTOR_SKILLS procedure
    * CASE << "CONVERT_TO_REGULAR"
      * Read `references/ops/convert-to-regular.md` and execute the CONVERT_TO_REGULAR procedure
    * CASE << "ACTIVATE"
      * Read `references/ops/activate.md` and execute the ACTIVATE procedure
    * CASE << "HELP"
      * Read `references/ops/help.md` and execute the HELP procedure
    * DEFAULT
      * ASK << Could not determine the operation. What would you like to do? | Create a skill | Modify a skill | Scaffold a skill | Validate a skill | Improve a skill | Advise | Refactor skills | Convert to regular | Activate runtime | Help

## Rules

- Never overwrite existing files without confirmation
- For ops that target a specific skill (IMPROVE, MODIFY, VALIDATE, SCAFFOLD, CONVERT_TO_CANOPY, CONVERT_TO_REGULAR): if the skill name is not stated explicitly, ASK before proceeding — never infer from natural language descriptions or loop over multiple skills
- Always show a plan before making any changes
- Preserve the skill's existing tree syntax style (markdown list vs box-drawing) unless the user asks to switch
- Preserve the skill's existing directory layout (legacy flat vs. standard `scripts/`/`references/`/`assets/`) during MODIFY — IMPROVE may migrate it on user opt-in
- Do not change a skill's logic or intent during CONVERT_TO_CANOPY, MODIFY, or VALIDATE
- SKILL.md must contain only orchestration — no inline JSON, YAML, tables, scripts, or templates
- Skill files must be exactly `SKILL.md` (uppercase) — case-sensitive filesystems require this
- Skills with `## Tree` must have a `compatibility` field declaring canopy-runtime requirement and a safety preamble guard block at the top of the body
- Frontmatter root contains only spec-allowed fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`); `argument-hint` and `user-invocable` go inside `metadata`
- Framework primitives (IF, ELSE_IF, ELSE, SWITCH, CASE, DEFAULT, FOR_EACH, BREAK, END, ASK, SHOW_PLAN, VERIFY_EXPECTED) are never defined in skill or project ops — they live in `../canopy-runtime/references/framework-ops.md` (loaded up-front by the tree; ops can reference by bare name `framework-ops.md`)
- Before creating any op or resource file, consult `framework-ops.md` (already in context) and any existing project-wide ops the consumer has defined — reference shared content, never duplicate it
- After any change to a skill or agent file, verify every `Read \`<category-path>/<file>\`` reference and every op procedure path still resolves to an existing file
- The platform runtime spec (`../canopy-runtime/references/runtime-claude.md` or `../canopy-runtime/references/runtime-copilot.md`) is loaded up-front by this skill's tree and is in context for every op procedure

## Response: operation | platform | target_skill | outcome
