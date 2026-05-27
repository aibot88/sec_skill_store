---
name: init-skill
description: |
  Claude Code 自进化系统初始化技能。为任意项目搭建完整的自进化开发环境，
  包括：认知核心(CLAUDE.md)、权限配置(settings.json)、路径作用域规则(rules/)、
  专用子智能体(agents/)、工作流(skills/)、记忆系统(memory/)。当用户说"初始化自进化系统"、
  "搭建Claude Code进化环境"、"设置项目进化配置"、"启用自进化"时触发。
---

# Claude Code 自进化系统

一键为项目搭建完整的自进化开发环境，让 Claude Code 具备自我学习、持续进化的能力。

## 核心架构

系统由四层组成：

| 层级 | 组件 | 作用 |
|-----|------|-----|
| 认知核心 | CLAUDE.md | 决策框架 + 完成标准 + 编码规范 |
| 专用子智能体 | agents/ | architect(规划) + reviewer(审查) |
| 路径作用域规则 | rules/ | 安全/API/性能规则按需加载 |
| 进化引擎 | skills/evolution + memory/ | 验证扫描 + 纠正捕获 + 自动晋升 |

## 初始化流程

### Step 1: 检查项目结构

首先确认目标项目目录，检查是否有 .claude 目录。

### Step 2: 收集项目信息

向用户确认以下信息（必须）：

1. 构建命令：npm run build? make? pnpm build?
2. 测试命令：npm test? pytest? go test?
3. 目录结构：src/? lib/? api/? 告知实际结构
4. 技术栈：TypeScript? Python? Go? Rust?

### Step 3: 创建文件夹结构

```bash
mkdir -p .claude/rules
mkdir -p .claude/agents
mkdir -p .claude/skills/evolution
mkdir -p .claude/skills/evolve
mkdir -p .claude/skills/review
mkdir -p .claude/skills/boot
mkdir -p .claude/skills/fix-issue
mkdir -p .claude/memory
```

### Step 4: 生成配置文件

#### 4.1 CLAUDE.md（认知核心）

项目根目录的 CLAUDE.md，包含：
- 决策框架（写代码前必做：grep 查模式 → 评估影响 → 最小改动 → 验证计划）
- 完成标准（typecheck + lint + test 全通过）
- 编码规范（根据技术栈定制）
- 自进化协议（观察→记录→验证→晋升）

必须替换占位符为用户的实际命令和目录结构。

#### 4.2 .claude/settings.json

权限配置 + 钩子配置：
- allow: 允许的命令模式
- deny: 禁止的命令（rm -rf, force push 等）
- hooks: SessionStart/PreToolUse/Stop 钩子

#### 4.3 .claude/rules/

路径作用域规则（选择性创建）：
- core-invariants.md - 压缩不变规则
- security.md - 安全规则
- api-design.md - API 设计模式
- performance.md - 性能规则

#### 4.4 .claude/agents/

专用子智能体：
- architect.md - 复杂任务规划智能体
- reviewer.md - 代码审查智能体

#### 4.5 .claude/skills/

工作流技能：
- evolution/SKILL.md - 进化引擎
- evolve/SKILL.md - 进化审计命令
- review/SKILL.md - 提交前审查
- boot/SKILL.md - 会话预热
- fix-issue/SKILL.md - GitHub Issue 修复

#### 4.6 .claude/memory/

记忆系统文件：
- README.md - 记忆系统协议
- learned-rules.md - 已学规则
- evolution-log.md - 进化决策日志
- corrections.jsonl - 用户纠正记录
- observations.jsonl - 已验证发现

### Step 5: 添加 .gitignore

建议添加到项目 .gitignore：
```
.claude/memory/observations.jsonl
.claude/memory/corrections.jsonl
.claude/memory/violations.jsonl
.claude/memory/sessions.jsonl
```

## 文件模板

### CLAUDE.md 模板

```markdown
# Self-Evolving Engineering System

You are a principal engineer that gets smarter every session.

## Before You Write Any Code

1. **Grep first.** Search for existing patterns before creating anything.
2. **Blast radius.** What depends on what you're changing?
3. **Ask, don't assume.** One clarifying question, then move.
4. **Smallest change.** Solve what's asked, no bonus refactors.
5. **Verification plan.** How will you prove this works?

## Commands
# 替换为用户的实际命令
npm run dev
npm run test
npm run lint
npm run build

## Architecture
# 替换为用户的实际目录结构
src/
  core/      # Pure business logic
  api/       # HTTP handlers
  services/  # External boundaries

## Conventions
- TypeScript strict. No any.
- Error pattern: { data: T | null, error: AppError | null }
- Validation: zod on every external input

## Completion Criteria
ALL must pass:
1. npm run typecheck - zero errors
2. npm run lint - zero errors
3. npm run test - all pass

## Self-Evolution Protocol
1. **Observe.** Log patterns to .claude/memory/observations.jsonl
2. **Learn from corrections.** Log to corrections.jsonl
3. **Consult memory.** Read learned-rules.md at session start
4. **Verify rules.** Run verification sweep
```

### settings.json 模板

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(git push --force *)",
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  },
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo \"[EVOLUTION] READ .claude/memory/learned-rules.md\""
      }]
    }]
  }
}
```

## 使用方式

用户在项目目录启动 Claude Code 时：
1. 自动加载 CLAUDE.md 中的决策框架和完成标准
2. SessionStart 钩子触发时自动运行验证扫描
3. 用户纠正时自动记录到 corrections.jsonl
4. 第二次相同纠正时自动晋升到 learned-rules.md
5. 每周末运行 /evolve 审计

## 验证初始化

1. 问 Claude："你的完成标准是什么？" → 应列出检查项
2. 让 Claude 添加工具函数 → 应先 grep 查模式
3. 纠正 Claude 一次 → 检查 corrections.jsonl 有记录
