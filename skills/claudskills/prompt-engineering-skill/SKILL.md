---
description: Publishable Prompt Engineering skill package that compiles a user request into a ready-to-use high-quality Prompt, with support for diagnosis, module injection, debugging, and evaluation.
---

# Prompt Engineering Skill Package

## 1. Package Summary

`Prompt Engineering Skill Package` 是一个面向真实工作场景的可复用技能包。它接收用户的一句需求、一个问题、一个模糊目标，自动识别任务类型、输出目标、质量目标和高风险失败模式，再装配合适的控制模块，最终输出一份可以直接复制使用的成品 Prompt。

这个 skill package 的核心定位不是 Prompt 教程，也不是模板库，而是一个 Prompt Compiler。用户输入的是自然语言需求，输出的是结构完整、可直接使用、可调试、可评估的最终 Prompt。

## 2. What This Package Does

本技能包负责：

- 将一句需求编译成成品 Prompt
- 将模糊问题升级成结构完整 Prompt
- 自动补齐角色定义、问题重定义、认知路径、质量门槛和文风约束
- 根据任务类型自动装配控制模块
- 根据失败模式自动生成修复路径
- 对已有 Prompt 做系统化调试
- 对 Prompt 或输出做结构化评估

## 3. What This Package Does Not Do

本技能包不直接负责：

- 替用户完成原任务本身
- 保证任何底层模型都产出同等质量结果
- 在缺失上下文时生成绝对正确的事实判断
- 替代具体领域知识本身

也就是说，它负责编译 Prompt，不直接代替目标任务执行。

## 4. Recommended Trigger Conditions

当用户出现以下意图时，建议触发本技能包：

- 想把一句需求或问题转换成高质量 Prompt
- 想让系统自动补足 Prompt 结构
- 想调试已有 Prompt，而不是重写答案
- 想把 Prompt Engineering 变成标准化工作流
- 想系统化积累 Prompt 方法与模块

典型触发语包括：

- “帮我把这个需求变成一个高质量 prompt”
- “我只给一句话，你帮我生成成品提示词”
- “把这个问题升级成可直接使用的 Prompt”
- “这个 Prompt 不够好，帮我调试”
- “我想系统化做提示词工程”

## 5. Input Contract

本技能包必须接受以下输入形态：

- 一句话需求
- 一个问题
- 一段原始任务描述
- 一段已有 Prompt
- 原始任务 + 当前 Prompt + 当前输出

如果输入信息不足，系统必须自动补足最常见且最有价值的控制结构，而不是要求用户先学习 Prompt Engineering 术语。

## 6. Output Contract

### Default Output

默认输出两部分：

```text
诊断摘要：
- 任务类型：
- 输出产物：
- 质量目标：
- 高风险失败模式：

可直接使用的最终 Prompt：
【完整成品 Prompt】
```

### Prompt-Only Output

如果用户明确只需要成品 Prompt，则只输出最终 Prompt。

### Debug Output

如果用户输入的是已有 Prompt 或 bad output，则输出：

```text
失败模式判断：
缺失控制层：
最小必要修复：
修复后的 Prompt：
```

### Evaluation Output

如果用户要求评估 Prompt 或输出质量，则输出：

```text
评分项：
总分：
最主要缺陷：
最优先补的控制层：
```

## 7. Runtime Protocol

本技能包在运行时应遵循以下协议：

### Step 1: Identify Task Type

识别用户输入更接近哪一类任务：

- 算法分析型
- 源码分析型
- 架构规格型
- 商业洞察型
- A 股分析型
- 通用深度分析型
- 写作生成型
- Prompt 调试型
- 其他

### Step 2: Identify Intended Output

识别用户真正想要的输出产物：

- 分析文章
- 研究报告
- 规格文档
- 评审意见
- 决策建议
- 可直接使用的 Prompt
- 调试后的 Prompt
- 其他

### Step 3: Identify Quality Priority

识别用户更看重什么：

- 深度
- 可执行性
- 批判性
- 清晰度
- 自然文风
- 结构完整
- 决策价值

### Step 4: Predict Failure Modes

预判任务最容易滑向哪些低质量输出：

- 表层复述
- 模板腔
- 正确废话
- 伪深度
- 无批判赞美
- 面面俱到无判断
- 不可执行
- 风格不稳

### Step 5: Inject Control Modules

从控制模块层中自动选择合适模块：

- 问题重定义
- 认知下钻
- 关键点优先
- 批判性
- 信息密度
- 边界与验证
- 可执行性
- 风格控制

### Step 6: Assemble Final Prompt

将模块装配进以下五层结构：

- 角色层
- 问题重定义层
- 认知路径层
- 质量门槛层
- 全局文风层

### Step 7: Return Final Artifact

输出完整、可直接复制使用的最终 Prompt。

## 8. Default Module Routing

```text
算法分析型
默认注入：问题重定义 + 认知下钻 + 关键点优先 + 边界与验证 + 风格控制

源码分析型
默认注入：问题重定义 + 认知下钻 + 批判性 + 关键点优先 + 风格控制

架构规格型
默认注入：问题重定义 + 批判性 + 边界与验证 + 可执行性 + 风格控制

商业洞察型
默认注入：问题重定义 + 认知下钻 + 关键点优先 + 批判性 + 风格控制

A 股分析型
默认注入：问题重定义 + 关键点优先 + 批判性 + 边界与验证 + 可执行性 + 风格控制

通用深度分析型
默认注入：问题重定义 + 认知下钻 + 关键点优先 + 边界与验证 + 风格控制

写作生成型
默认注入：风格控制 + 信息密度

Prompt 调试型
默认注入：失败模式识别 + 缺失控制层判断 + 最小必要修复
```

## 9. Failure Mode Repair Routing

```text
表层复述 -> 问题重定义 + 认知下钻
模板腔 -> 风格控制 + 信息密度
正确废话 -> 信息密度 + 关键点优先
伪深度 -> 边界与验证 + 认知下钻
无批判赞美 -> 批判性
面面俱到无判断 -> 关键点优先 + 信息密度
不可执行 -> 可执行性 + 边界与验证
风格不稳 -> 风格控制
```

## 10. Default Invocation Template

这是本技能包最推荐的总调用模板：

```text
我会给你一句需求、一个问题，或者一个模糊目标。

你的任务不是直接回答，而是先把它编译成一份可以直接使用的高质量 Prompt。

你必须自动完成以下工作：
1. 识别任务类型
2. 识别用户真正想要的输出产物
3. 识别用户最在意的质量目标
4. 识别这个任务最容易出现的低质量输出
5. 自动补足最合适的角色定义、问题重定义、认知路径、质量门槛和文风约束
6. 输出一份可以直接复制使用的最终 Prompt

请优先遵守以下原则：
- 用户的描述是起点，不是边界
- 不要停留在表层复述，先识别问题本质
- 不要输出模板腔、正确废话或伪深度
- 如果任务需要判断或建议，必须补足边界、失效条件和可执行性
- 正文风格应自然、连贯、信息密度高

输出格式必须严格如下：

诊断摘要：
- 任务类型：
- 输出产物：
- 质量目标：
- 高风险失败模式：

可直接使用的最终 Prompt：
【在这里输出完整成品 Prompt】
```

## 11. Debug Mode Invocation

```text
下面我会给你三个内容：
1. 原始任务
2. 当前 Prompt
3. 当前输出

你的任务不是重写答案，而是先做 Prompt Debugging。

请按以下步骤输出：
1. 当前输出最主要的失败模式是什么
2. 这个失败模式最可能来自 Prompt 缺少哪类约束
3. 应做哪些最小必要修改
4. 为什么这些修改有效
5. 输出修复后的 Prompt
```

## 12. Evaluation Mode Invocation

```text
请基于以下维度评估这个 Prompt 或输出：
1. 是否真正回答了问题本质
2. 是否识别了关键约束、边界、代价与失败模式
3. 是否有足够的信息密度
4. 是否给出了明确判断
5. 是否具备可执行性或可决策性
6. 是否文风自然，避免模板腔与 AI 味
7. 是否整体稳定

请输出：
- 每项 1-5 分
- 总分
- 最主要缺陷
- 最优先补的控制层
```

## 13. Behavior Modes

### Default Mode

输入极少时，自动补结构并输出诊断摘要 + 成品 Prompt。

### Prompt-Only Mode

用户只要成品时，仅输出最终 Prompt。

### Transparent Mode

用户希望理解系统判断时，保留诊断摘要。

### Refinement Mode

用户已有 Prompt 或 bad output 时，切换到调试模式。

### Evaluation Mode

用户关心 Prompt 是否足够好时，切换到评估模式。

## 14. Quality Requirements

本技能包输出的最终 Prompt 必须满足以下要求：

- 不只是头衔堆砌
- 不只是任务复述
- 必须包含明确控制结构
- 必须能压制高频失败模式
- 必须能直接复制使用
- 必须尽量减少模板腔
- 必须在必要时收敛为可执行判断

## 15. Integration Guidance

如果要将本技能包接入应用、网页、插件或自动化系统，推荐暴露最少的前台复杂度：

- 一个输入框，接收一句需求
- 一个可选开关，选择是否显示诊断摘要
- 一个输出区，返回最终 Prompt

内部实现时，应复用：

- 任务识别
- 模块路由
- 五层 Prompt 装配
- 调试模式
- 评估模式

对最终用户来说，它应表现得像一个 Prompt Compiler，而不是一个复杂工具箱。

## 16. Release Positioning

这个 skill package 适合被描述为：

- 用一句需求生成高质量成品 Prompt 的技能包
- 带控制模块注入的 Prompt 编译器
- 支持生成、调试、评估三种模式的 Prompt Engineering skill

## 17. Final Principle

这个技能包的本质，不是写 Prompt，而是编译 Prompt。

只要它能把自然语言需求稳定转换成高质量成品 Prompt，并且输出过程可解释、可调试、可复用，这个 skill package 就达到了它的发布标准。
