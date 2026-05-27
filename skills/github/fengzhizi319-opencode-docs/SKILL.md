<!--
Generated documentation: plan skill used by the `plan` agent.
Place in repository docs/ directory as requested by user.
-->
# Plan skill (for the plan agent)

This document explains the "plan" skill and how the OpenCode `plan` agent uses skills to help create, store, and act on plans. It covers discovery, authoring, invocation, permissions, integration patterns (Plan → Build workflow), security considerations, and troubleshooting.

## Overview

- What is a "skill"?
  - A skill is a directory that contains a `SKILL.md` file (Markdown with YAML frontmatter) and optionally bundled resources (scripts, templates, references).
  - Skills provide domain-specific instructions, workflows, and helper assets that the LLM can load into the conversation context.

- What is the "plan" skill?
  - "Plan" skill is a planning-focused skill or set of skills authors can provide that contain templates, workflows, and examples specifically designed to help the `plan` agent produce high-quality, actionable plans.
  - The `plan` agent uses skills to inject structured guidance (templates, checklists, constraints) into system or assistant prompts so the model can output plans in the desired format and location.

## How skills are discovered and loaded

- Discovery sources (order / locations):
  - Project-local skill directories: `.opencode/skill/` and `.opencode/skills/` (both supported).
  - Claude/Agents-compatible directories: `.claude/skills/` and `.agents/skills/`.
  - Configured skill paths in your opencode config (`cfg.skills.paths`). Paths may be absolute or relative to the project directory.
  - Remote skill URLs configured in `cfg.skills.urls` and pulled via the discovery mechanism.
  - Global user directories under the user home (e.g. `~/.claude/skills`, `~/.agents/skills`).

- Implementation notes (for maintainers):
  - Skills are detected by scanning for `SKILL.md` files (see `src/skill/index.ts`).
  - The skill loader parses YAML frontmatter and exposes `Skill.Info` objects with `{ name, description, location, content }`.
  - `Skill.fmt(list, { verbose })` formats the available skills for inclusion in tool descriptions or system prompts.

## What the Skill tool returns

- The `skill` tool (Tool id: `skill`) is the LLM-invokable tool to load a skill during a session.
- When invoked it accepts `{ name: string }` and returns an object that includes:
  - `title`: a short title like `Loaded skill: <name>`
  - `output`: a string that contains a `<skill_content name="...">` block with the skill's markdown content and a sampled `<skill_files>` list containing a small set of paths in XML-like tags.
  - `metadata`: object `{ name, dir }` where `dir` is the skill directory.

- Example of returned output (structure):

```xml
<skill_content name="example-plan-skill">
# Skill: example-plan-skill

... (SKILL.md content here) ...

Base directory for this skill: file:///.../path/to/skill/

<skill_files>
<file>/abs/path/to/skill/template.md</file>
<file>/abs/path/to/skill/scripts/generate.sh</file>
 ...
</skill_files>
</skill_content>
```

- Sampling limit: when returning the files list, the implementation samples up to 10 files from the skill directory (see `src/tool/skill.ts`, `limit = 10`).

## Permission interaction with the `plan` agent

- The `plan` agent has a tailored permission ruleset that is intentionally restrictive:
  - `edit` is denied for all general files but allowed for plan locations:
    - `.opencode/plans/*.md` (project-local plans) and the global plans directory under `Global.Path.data/plans`.
  - `plan_enter` and `plan_exit` are special permissions used to control switching into/out of plan mode.
  - `question` is typically allowed so the plan agent can ask clarifying questions.

- Skill loading requires asking the user for permission to load that skill in the current session. The `skill` tool calls `ctx.ask({ permission: 'skill', patterns: [params.name], always: [params.name], ... })` before returning content. This ensures the user (or host policy) consents to the skill being injected.

## Where plan files live

- Plan files are written to either:
  - Project worktree: `<project>/.opencode/plans/<timestamp>-<slug>.md` when the project is a git repo (or when working in a worktree).
  - Global plans directory: `<Global.Path.data>/plans/<timestamp>-<slug>.md` when no project worktree is present.

- Use `Session.plan({ slug, time })` helper to compute the canonical path.

## How to author a planning-focused SKILL.md

The typical `SKILL.md` is a Markdown document with YAML frontmatter. At minimum, frontmatter must include:

```yaml
---
name: my-plan-skill
description: Templates and workflows to produce structured implementation plans
---
```

Recommended structure inside the Markdown content:

- Title and short intro
- When to use this skill (scenarios)
- Plan templates (markdown snippets you expect the model to emit), e.g.:
  - Problem statement
  - Goals (success criteria)
  - Constraints
  - Step-by-step tasks
  - Acceptance criteria and tests
- Example plan(s)
- Files and templates (paths relative to skill base, e.g. `templates/plan-template.md`)
- Scripts or helper commands (in `scripts/`)

Best practices:
- Keep guidance prescriptive and structured (models follow explicit patterns well).
- Provide one or more ready-to-fill templates the model can copy into `.opencode/plans/`.
- Provide examples of expected file names and folder layout.
- Use relative paths in examples and mention that they are relative to the skill base directory.

### Minimal SKILL.md example

```md
---
name: plan-templates
description: Planning templates and checklists for engineering tasks
---

# Plan Templates

## When to use
Use this skill when the user requests a multi-step implementation plan, tests, or a migration strategy.

## Plan Template: simple

### Problem
Describe the issue.

### Goal
State success criteria.

### Steps
- Step 1: ...
- Step 2: ...

### Tests / Acceptance
- Add unit tests: ...

## Example
Below is an example plan for adding a new API endpoint.

```
Problem: Add POST /items to create items.
Goal: ...
Steps:
- Create route
...etc
```

```

Place auxiliary resources under `templates/` or `scripts/` in the same skill directory.
```

### Advanced SKILL.md example (with templates and usage notes)

Include another fenced example showing `templates/plan.md` content and a sample script layout.

```md
---
name: plan-advanced
description: Advanced planning skill with templates and CI checklist
---

# Advanced Planning Skill

## Templates

Add `templates/implementation-plan.md` and `templates/test-plan.md`.

## Usage
When asked for a plan, the model should:
1. Choose an appropriate template.
2. Fill the sections.
3. Write the result to `.opencode/plans/<timestamp>-<slug>.md`.

```

Notes:
- Keep template placeholders explicit like `{{goal}}` to make it easy for the model to substitute.

```

## Invoking and using the skill from a session

Typical flow when the user asks for a plan:

1. User asks: "Please make an implementation plan for X and save it as a plan file."
2. The model recognizes a matching skill and calls the `skill` tool with `{ name: '<skill-name>' }`.
3. The `skill` tool asks for permission and returns the skill content and a sampled file list.
4. The model uses the skill content (templates, examples) to generate a plan.
5. With the `plan` agent, the generated plan is written to `.opencode/plans/<timestamp>-<slug>.md` (allowed by the `plan` agent permission set).
6. When planning is finished, `plan_exit` permission lets the agent request to switch back to the `build` agent to implement the plan.

Example prompt patterns that work well:

```text
Please create a detailed implementation plan for adding a payment integration. Use the "plan-templates" skill and save the plan to .opencode/plans/payment-integration.md. Do not write code — only the plan.
```

Or shorter, letting the agent detect the skill:

```text
Plan: Add payment integration. Produce steps, tests, and files to create. Save plan to .opencode/plans/payment-integration.md.
```

## Integration: Plan → Build workflow

- Common workflow:
  1. Use the `plan` agent (it will not edit code except allowed plan files) to research and write a plan.
 2. Review the plan with the user; if accepted, call `plan_exit` to request switching to the `build` agent.
 3. Switch to `build` agent which has broader `edit` permissions and can implement the plan (create files, run scripts, edit code).

- The codebase includes examples and tests demonstrating this workflow (see `packages/opencode/test-kimi-execution.ts` for a real-world test harness).

## Security and permission considerations

- Skills can contain arbitrary files and scripts. Loading a skill injects its content into the conversation, which has security implications.

- The `skill` tool explicitly asks for permission before loading, via `ctx.ask({ permission: 'skill', patterns: [params.name], always: [params.name], ... })`.

- Default permission model for agents:
  - `external_directory` resources are generally `ask` (or `allow` for whitelisted skill dirs).
  - `plan` agent is intentionally restrictive: `edit` is denied except for plan files.

- Skill discovery respects configured whitelisted directories and will log missing or invalid `SKILL.md` files.

## Troubleshooting and testing tips

- If your skill is not discovered:
  - Ensure `SKILL.md` exists and begins with YAML frontmatter containing `name` and `description`.
  - Put the skill under one of the supported directories: `.opencode/skill`, `.opencode/skills`, `.claude/skills`, `.agents/skills`, or add a path to `cfg.skills.paths`.

- If the `skill` tool fails to return files or returns an empty content block:
  - Check that `SKILL.md` content is valid and not missing frontmatter (invalid frontmatter is skipped by the loader).
  - Review logs for `Skill` module errors — they emit helpful messages when parsing fails.

- Testing locally:
  - Create a temporary project directory with `.opencode/skill/<name>/SKILL.md` and run session tests or use the `skill` tool via the CLI session to load it.
  - Unit tests in the repo exercise skill discovery (see `packages/opencode/test/skill/skill.test.ts`).

## Example: full sample SKILL.md for a plan skill

This is a ready-to-drop `SKILL.md` you can use or adapt. Place it under `.opencode/skills/plan-skill/SKILL.md`.

```md
---
name: plan-skill
description: Planning templates and checklists to help the plan agent produce structured, actionable plans.
---

# Plan Skill: templates and examples

## Overview
This skill contains templates and sample plans to help the model produce consistent, reviewable plans.

## Template: implementation-plan.md

### Problem
Describe the problem or feature request.

### Goal
State clear success criteria.

### Constraints
List constraints (time, backward-compatibility, API limits).

### Tasks
- Task 1: Describe and owner
- Task 2: Describe and estimate

### Acceptance
- Tests or manual verification steps.

## Example Plan: add-search-endpoint

Problem: Add a /search endpoint to query items.

Goal: ...

Steps:
- Design API
- Implement route
- Add tests

## Templates and scripts
- `templates/implementation-plan.md` — filled by the model
- `scripts/ci-checklist.sh` — optional helper script

## Usage notes
When asked for a plan, models should pick the `implementation-plan.md` template and write the filled plan to `.opencode/plans/<timestamp>-<slug>.md`.

```

## Final notes

Skills are a lightweight, powerful mechanism to provide the model with curated domain knowledge and templates. When combined with the `plan` agent's restrictive edit policy and the `plan → build` workflow, they enable a safe, auditable way to let models produce plans and only modify code when explicitly approved.

If you want, I can:
- Add a concrete sample skill directory under `packages/opencode/skills/` in this repo (example files), or
- Generate a small test harness that demonstrates loading and using the sample plan skill.

---

Document generated and saved to `docs/plan-skill.md`.

---

# 中文翻译（Chinese translation）

下面是本文档的中文翻译，便于中文读者参考。

（注意：此处为译文，英文原文在上方。如需修改，请同时更新两处以保持一致。）

## 概述

- 什么是 "skill"？
  - skill 是一个目录，包含 `SKILL.md`（带 YAML frontmatter 的 Markdown）以及可选的资源（脚本、模板、参考资料）。
  - Skills 为 LLM 提供领域专用的指令、工作流和辅助资产，模型可以在对话中加载这些内容以辅助生成更符合要求的输出。

- 什么是 "plan" skill？
  - "Plan" skill 是专注于规划的 skill，包含模板、工作清单和示例，帮助 `plan` agent 生成高质量、可执行的计划。
  - `plan` agent 使用 skill 将结构化指导（如模板、检查表、约束）注入 system/assistant 提示中，以便模型按期望格式和位置生成计划。

## skill 的发现与加载

- 发现来源（优先与位置）：
  - 项目内 skill 目录：`.opencode/skill/` 或 `.opencode/skills/`。
  - 兼容 Claude/Agents 的目录：`.claude/skills/` 和 `.agents/skills/`。
  - 在 opencode 配置中指定的路径（`cfg.skills.paths`），可为绝对或相对项目目录。
  - 配置的远程 skill URL（`cfg.skills.urls`），通过发现机制拉取。
  - 全局用户目录（例如 `~/.claude/skills`、`~/.agents/skills`）。

- 维护者实现要点：
  - Skill 的检测通过扫描 `SKILL.md` 实现（参见 `src/skill/index.ts`）。
  - 加载器解析 YAML frontmatter，并以 `Skill.Info` 对象暴露 `{ name, description, location, content }`。
  - `Skill.fmt(list, { verbose })` 用于把可用技能格式化，供工具描述或系统提示使用。

## `skill` 工具返回的内容

- `skill` 工具（Tool id: `skill`）是 LLM 在会话中调用以加载 skill 的工具。
- 调用入参：`{ name: string }`，返回的对象通常包含：
  - `title`：例如 `Loaded skill: <name>` 的短标题。
  - `output`：字符串，包含一个 `<skill_content name="...">` 块，内含 skill 的 Markdown 内容以及采样的 `<skill_files>`（用 XML-like 标签列出若干文件路径）。
  - `metadata`：对象 `{ name, dir }`，其中 `dir` 为 skill 的目录路径。

- 返回示例结构（摘要）：

```xml
<skill_content name="example-plan-skill">
# Skill: example-plan-skill

... (SKILL.md 内容)...

Base directory for this skill: file:///.../path/to/skill/

<skill_files>
<file>/abs/path/to/skill/template.md</file>
<file>/abs/path/to/skill/scripts/generate.sh</file>
 ...
</skill_files>
</skill_content>
```

- 采样限制：当返回文件列表时，loader 会采样至多 10 个文件（见 `src/tool/skill.ts` 中的 `limit = 10` 设置）。

## 与 `plan` agent 的权限交互

- `plan` agent 使用专门的、相对严格的权限规则：
  - 默认对大多数文件的 `edit` 权限被拒绝，但允许对计划相关位置进行写入：
    - 项目内 `.opencode/plans/*.md`（项目工作区内的计划文件）以及全局数据目录下的 `plans`（例如 `Global.Path.data/plans`）。
  - `plan_enter` 和 `plan_exit` 为特殊权限，用于控制进入/退出计划模式。
  - `question`（提问）通常被允许，便于 agent 询问澄清问题。

- 加载 skill 时需要用户许可：`skill` 工具在返回内容前会调用 `ctx.ask({ permission: 'skill', patterns: [params.name], always: [params.name], ... })`。这保证在会话中注入 skill 内容前获得用户或主机策略的同意。

## 计划文件的存放位置

- 计划文件会写入以下位置之一：
  - 项目工作树：`<project>/.opencode/plans/<timestamp>-<slug>.md`（当仓库为 git repo 或工作树存在时）。
  - 全局计划目录：`<Global.Path.data>/plans/<timestamp>-<slug>.md`（当没有项目工作树时）。

- 使用 `Session.plan({ slug, time })` 辅助函数来计算规范路径。

## 如何编写适合规划的 `SKILL.md`

典型的 `SKILL.md` 是带 YAML frontmatter 的 Markdown 文档。最少 frontmatter 应包含：

```yaml
---
name: my-plan-skill
description: Templates and workflows to produce structured implementation plans
---
```

推荐结构：

- 标题和简介
- 使用场景（何时使用该 skill）
- 计划模板（模型应输出的 Markdown 片段），例如：
  - 问题陈述
  - 目标（成功标准）
  - 约束
  - 逐步任务
  - 验收标准与测试
- 示例计划
- 文件与模板（相对于 skill 根目录的路径，例如 `templates/plan-template.md`）
- 脚本或辅助命令（放在 `scripts/`）

最佳实践：
- 指导应具有可被模型遵循的结构化格式（模型更容易遵循明确模板）。
- 提供可直接填充的模板，方便模型将结果写入 `.opencode/plans/`。
- 在示例中使用相对路径并注明这些路径相对于 skill 根目录。

### 最简 `SKILL.md` 示例

```md
---
name: plan-templates
description: Planning templates and checklists for engineering tasks
---

# Plan Templates

## When to use
Use this skill when the user requests a multi-step implementation plan, tests, or a migration strategy.

## Plan Template: simple

### Problem
Describe the issue.

### Goal
State success criteria.

### Steps
- Step 1: ...
- Step 2: ...

### Tests / Acceptance
- Add unit tests: ...

## Example
Below is an example plan for adding a new API endpoint.

```
Problem: Add POST /items to create items.
Goal: ...
Steps:
- Create route
...etc
```

```

Place auxiliary resources under `templates/` or `scripts/` in the same skill directory.
```

### 进阶 `SKILL.md` 示例（含模板与使用说明）

可以包含另一个代码块示例，展示 `templates/plan.md` 的内容和脚本布局。

```md
---
name: plan-advanced
description: Advanced planning skill with templates and CI checklist
---

# Advanced Planning Skill

## Templates

Add `templates/implementation-plan.md` and `templates/test-plan.md`.

## Usage
When asked for a plan, the model should:
1. Choose an appropriate template.
2. Fill the sections.
3. Write the result to `.opencode/plans/<timestamp>-<slug>.md`.

```

注意：使用占位符（如 `{{goal}}`）可以帮助模型明确替换位置。

## 在会话中调用并使用 skill

用户请求计划时的典型流程：

1. 用户："请为 X 制定一个实施计划并保存为计划文件。"
2. 模型识别到匹配的 skill，调用 `skill` 工具：`{ name: '<skill-name>' }`。
3. `skill` 工具请求许可并返回 skill 内容与采样文件列表。
4. 模型使用 skill 内容（模板、示例）生成计划文本。
5. 对于 `plan` agent，生成的计划会被写入 `.opencode/plans/<timestamp>-<slug>.md`（`plan` agent 的权限集允许写入此位置）。
6. 完成计划后，`plan_exit` 权限允许 agent 请求切换到 `build` agent 去实现计划。

示例提示模板（推荐模式）：

```text
Please create a detailed implementation plan for adding a payment integration. Use the "plan-templates" skill and save the plan to .opencode/plans/payment-integration.md. Do not write code — only the plan.
```

或更简略的形式，让 agent 自行检测 skill：

```text
Plan: Add payment integration. Produce steps, tests, and files to create. Save plan to .opencode/plans/payment-integration.md.
```

## 集成：Plan → Build 工作流

- 常见工作流：
  1. 使用 `plan` agent（该 agent 除计划文件外不会编辑其他代码）来调研并撰写计划。
  2. 与用户一起审阅计划；若接受，调用 `plan_exit` 请求切换到 `build` agent。
  3. 切换到 `build` agent，`build` agent 拥有更宽泛的 `edit` 权限，可以实现计划（创建文件、运行脚本、修改代码）。

- 代码库中包含演示该工作流的示例与测试（参见 `packages/opencode/test-kimi-execution.ts`，它是一个真实的测试用例框架）。

## 安全与权限注意事项

- Skills 可能包含任意文件与脚本。加载 skill 会将其内容注入会话，这带来潜在的安全风险。

- `skill` 工具在加载前会明确请求许可：`ctx.ask({ permission: 'skill', patterns: [params.name], always: [params.name], ... })`。

- 对 agent 的默认权限模型：
  - 外部目录资源通常需要 `ask`（或对于白名单目录可 `allow`）。
  - `plan` agent 被设计为限制型：`edit` 默认拒绝，除非是计划文件相关路径。

- Skill 发现过程会遵循白名单配置并在解析失败时记录日志。

## 故障排查与测试建议

- 如果 skill 未被发现：
  - 确认 `SKILL.md` 存在并且以 YAML frontmatter 开头，包含 `name` 与 `description`。
  - 将 skill 放在支持的目录之一：`.opencode/skill`、`.opencode/skills`、`.claude/skills`、`.agents/skills`，或将路径添加到 `cfg.skills.paths`。

- 如果 `skill` 工具未返回文件或返回空内容块：
  - 检查 `SKILL.md` 内容是否合法，frontmatter 是否缺失（解析失败会导致 loader 跳过该 skill）。
  - 查看 Skill 模块的日志 —— 解析错误会有提示信息。

- 本地测试：
  - 在一个临时项目目录下创建 `.opencode/skill/<name>/SKILL.md`，然后运行会话测试或通过 CLI 会话使用 `skill` 工具加载它。
  - 仓库中的单元测试覆盖 skill 发现（参见 `packages/opencode/test/skill/skill.test.ts`）。

## 示例：可直接使用的 plan skill（SKILL.md）

下面是一个可直接放入 `.opencode/skills/plan-skill/SKILL.md` 的 `SKILL.md` 示例：

```md
---
name: plan-skill
description: Planning templates and checklists to help the plan agent produce structured, actionable plans.
---

# Plan Skill: templates and examples

## Overview
This skill contains templates and sample plans to help the model produce consistent, reviewable plans.

## Template: implementation-plan.md

### Problem
Describe the problem or feature request.

### Goal
State clear success criteria.

### Constraints
List constraints (time, backward-compatibility, API limits).

### Tasks
- Task 1: Describe and owner
- Task 2: Describe and estimate

### Acceptance
- Tests or manual verification steps.

## Example Plan: add-search-endpoint

Problem: Add a /search endpoint to query items.

Goal: ...

Steps:
- Design API
- Implement route
- Add tests

## Templates and scripts
- `templates/implementation-plan.md` — filled by the model
- `scripts/ci-checklist.sh` — optional helper script

## Usage notes
When asked for a plan, models should pick the `implementation-plan.md` template and write the filled plan to `.opencode/plans/<timestamp>-<slug>.md`.

```

## 最后说明

Skills 是一种轻量且强大的机制，可向模型提供策划好的领域知识和模板。结合 `plan` agent 的限制型编辑策略与 `plan → build` 工作流，能以安全、可审计的方式让模型产出计划，并在获得明确批准后再修改代码。

如果你希望，我可以：
- 在仓库中添加一个示例 skill 目录（`packages/opencode/skills/` 下的示例文件），或
- 生成一个简单的测试套件，展示如何加载并使用该计划 skill。

---

文档由仓库助手生成并保存在 `docs/plan-skill.md`（包含英文与中文）。
