---
name: incident-to-prompt
description: Use this skill to convert a security incident or public vulnerability pattern into reusable audit prompts, checklists, tests, and AGENTS.md rules. Do not use it to generate exploit instructions.
---

# incident-to-prompt

## English

### Purpose

Convert incidents into durable review material.

### Workflow

1. Summarize the incident pattern.
2. Identify affected domains.
3. Map to code shapes.
4. Generate checklist items.
5. Generate prompt rules.
6. Generate regression/fuzz/invariant test ideas.
7. Generate AGENTS.md rule updates.
8. Mark human-review requirements.

### Safety rules

Do not include exploit payloads beyond defensive reproduction summaries.


### Canonical finding format

```yaml
id: F-001
severity: Critical | High | Medium | Low | Informational
confidence: High | Medium | Low
category:
affected_code:
root_cause:
exploit_path:
preconditions:
impact:
evidence:
minimal_fix:
regression_test:
auto_fix_suitability: Safe | Needs Human Review | Do Not Auto-Fix
notes:
```

### v0.6 operational guardrails

- Keep the skill within its stated trigger conditions and the user's explicitly provided scope.
- Preserve project safety boundaries: audit-only by default; Do not execute exploits, Do not auto-merge, Do not upload private source code or secrets, and do not scan unrelated repositories without explicit user request.
- Ask for explicit human approval before patching high-risk auth, IAM, governance, funds, terminal, or agent-tooling behavior.
- Report validation performed, files changed, residual risk, and any skipped future-phase work when finished.

## 中文

### 目的

使用这个 skill 进行安全事件转 prompt 和规则更新。它应该帮助审查者把输入边界、风险证据、影响、修复建议和回归测试组织成可复核的安全输出。

### 触发条件

适用于 把安全事件、公开漏洞模式或内部 postmortem 转成 checklist、prompt rule、test idea 和 AGENTS.md rule。如果请求超出这些边界，先说明范围差异，并选择更合适的 prompt、skill 或人工 review 路径。

### 不适用场景

不要用于生成 exploit 指令、攻击 payload、生产攻击步骤或可滥用的绕过教程。不要把这个 skill 当作自动扫描整个仓库、执行 exploit、上传私有源码或 secrets、自动提交、自动推送或 auto-merge 的许可。

### 操作流程

1. 明确用户给出的目标、允许查看的材料和不能触碰的范围。
2. 收集必要上下文，但只读取完成任务所需的文件、diff、workflow、fixture 或文档。
3. 识别 trust boundary、privileged operation、sensitive data、preconditions 和 security impact。
4. 只报告有 evidence 的 finding；缺少上下文时写 question 或 assumption。
5. 为 confirmed issue 提出 minimal fix，并规划能捕捉同类事件的 regression、fuzz、invariant 或 review scenario。
6. 完成后报告验证输出、残余风险和需要人工确认的事项。

### 安全规则

默认 audit-only。未经明确授权，不 patch、不 commit、不 push、不创建 PR、不 merge。不要执行 exploit，不要访问生产系统，不要打印 secrets。涉及 IAM、authz 模型、资金、治理、terminal 执行或 agent-tooling 权限的修复必须进入人工 review。

### 输出要求

使用 canonical finding format。每个 finding 都要包含 severity、confidence、category、affected_code、root_cause、exploit_path、preconditions、impact、evidence、minimal_fix、regression_test、auto_fix_suitability 和 notes。
