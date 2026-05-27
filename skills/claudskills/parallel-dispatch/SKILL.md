---
name: parallel-dispatch
description: 把工作拆成安全、独立、可并行的子任务，并协调 subagent 避免重复劳动和冲突修改。适用于 Claude Code 通过清晰 delegation 能显著加速复杂任务时。
---

# 并行分发

只有在并行确实有价值时，才使用这个 skill。

适合触发的场景：

- there are multiple independent questions to answer
- implementation can be split into disjoint areas
- sidecar verification can run while local work continues

不要只是因为系统支持 subagent，就滥用这个 skill。

## 目标

在不重复劳动、不阻塞关键路径、不制造冲突改动的前提下，提高吞吐。

## 工作流

1. 先决定本地先做什么。
   找出下一步关键路径，能本地做就优先本地做。

2. 识别哪些工作适合并行。
   常见候选包括：
   - bounded research questions
   - disjoint file edits
   - verification that can run in the background

3. 给每个子任务清晰定边界。
   每个 delegation 至少要说明：
   - exact objective
   - expected output
   - file ownership or read-only scope
   - constraints and non-goals

4. 避免重叠。
   除非不可避免，否则两个 subagent 不应拥有同一写区域。

5. 本地继续推进。
   除非下一步真的依赖 agent 结果，否则不要停下来干等。

6. 谨慎集成返回结果。
   先 review，再适配当前工作区状态，再继续往下走。

## Claude Code 对应关系

- 只有在环境支持 subagent 时才使用
- 优先把侧车工作委派出去，而不是把立刻阻塞主线的任务外包
- 如果上下文连续性有帮助，优先复用已有 subagent
- 不再需要的 subagent 要及时关闭

## 约束

- 不要委派模糊、开放、无边界的任务
- 除非必要，不要把你立刻依赖的阻塞任务交给 subagent
- 不要在 subagent 里重复本地已经在做的工作
- 不要让并行把 ownership 和 verification 责任变模糊
