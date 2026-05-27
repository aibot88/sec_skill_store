---
name: pr-security-review
description: Use this skill to review a PR or diff for security regressions. Do not use it for full-repository audits or legal contract review.
---

# pr-security-review

## English

### Purpose

Review the current PR, diff, or changed-files summary for security regressions.

### When to use

- The user asks to review a PR.
- The user asks whether a diff introduces security risk.
- The user asks for blocking issues or missing tests.

### When not to use

- Full-repository audits.
- Smart-contract protocol audits.
- Legal contract review.
- Requests to auto-fix every issue.

### Workflow

1. Identify changed files and affected call paths.
2. Classify PR risk level L0-L3.
3. Check authz, data access, secrets, dependencies, dangerous sinks, and missing tests.
4. Output blocking issues and non-blocking issues.
5. Do not modify files.

### Output format

- Risk level
- Blocking issues
- Non-blocking issues
- Missing tests
- Security boundary changes
- Verdict: approve / approve with comments / request changes

### Safety rules

Default audit-only. Do not commit, push, merge, or edit files.


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

使用这个 skill 进行PR 安全审查。它应该帮助审查者把输入边界、风险证据、影响、修复建议和回归测试组织成可复核的安全输出。

### 触发条件

适用于 已有 PR、diff 或 changed-files summary，需要判断安全回归、blocking issue 和 missing tests。如果请求超出这些边界，先说明范围差异，并选择更合适的 prompt、skill 或人工 review 路径。

### 不适用场景

不要用于完整仓库审计、智能合约协议深审、法律合同 review 或自动修复全部问题。不要把这个 skill 当作自动扫描整个仓库、执行 exploit、上传私有源码或 secrets、自动提交、自动推送或 auto-merge 的许可。

### 操作流程

1. 明确用户给出的目标、允许查看的材料和不能触碰的范围。
2. 收集必要上下文，但只读取完成任务所需的文件、diff、workflow、fixture 或文档。
3. 识别 trust boundary、privileged operation、sensitive data、preconditions 和 security impact。
4. 只报告有 evidence 的 finding；缺少上下文时写 question 或 assumption。
5. 为 confirmed issue 提出 minimal fix，并规划与 blocking issue 对应的最小回归测试和直接受影响调用路径测试。
6. 完成后报告验证输出、残余风险和需要人工确认的事项。

### 安全规则

默认 audit-only。未经明确授权，不 patch、不 commit、不 push、不创建 PR、不 merge。不要执行 exploit，不要访问生产系统，不要打印 secrets。涉及 IAM、authz 模型、资金、治理、terminal 执行或 agent-tooling 权限的修复必须进入人工 review。

### 输出要求

使用 canonical finding format。每个 finding 都要包含 severity、confidence、category、affected_code、root_cause、exploit_path、preconditions、impact、evidence、minimal_fix、regression_test、auto_fix_suitability 和 notes。
