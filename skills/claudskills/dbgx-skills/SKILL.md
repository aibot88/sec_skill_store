---
name: dbgx-skills
description: dbgx-mcp 通用操作技能。用于通过 MCP 调用 WinDbg 命令，在 TTD 场景稳定跳转时间位置，并在 `dx ...SeekTo()` 不稳定时使用安全替代流程（`TimeStart` 查询 + `!tt` 跳转）。
---

# dbgx-mcp 通用技能

按以下规则执行，优先稳定性和可恢复性。

## 1. 命令执行策略

- 先执行只读、轻量命令验证链路，例如 `? 1+1`、`dq`、`lm`。
- 高风险命令拆分为“查询”和“执行”两步，不在同一条命令里做复杂动作。
- 每次仅推进一个诊断假设，避免一次提交多条长耗时命令。

## 2. TTD 稳定跳转（替代 `SeekTo`）

不要直接执行：
```text
dx @$cursession.TTD....SeekTo()
```

使用两步法：

1. 查询目标位置：
```text
dx -r1 @$cursession.TTD.Calls(<addr>).First().TimeStart
```

2. 提取 `Sequence`:`Steps` 后执行跳转：
```text
!tt <Sequence:Steps>
```

3. 验证当前位置：
```text
!tt
```
