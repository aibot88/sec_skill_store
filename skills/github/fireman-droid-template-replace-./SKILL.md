# Agent Skill 实习方向分析与强化计划

以 Agent Skill（AI 操作页面功能）作为前端实习核心亮点，分析当前项目现状并提出强化建议。

---

## 一、为什么有搞头？

- **行业趋势**：2025-2026 AI Agent 是最热方向之一（Anthropic Computer Use、Google Mariner、Manus 等）
- **前端稀缺性**：大多数前端只会调 API 展示结果，能做 Agent + Tool Calling + 流式渲染的人很少
- **全栈能力证明**：你的项目横跨前后端，展示了完整的 AI 工程能力

## 二、当前已实现的 Agent 能力

| 能力 | 技术点 | 面试价值 |
|------|--------|----------|
| Agent Loop | 最多 5 轮自动循环 | ⭐⭐⭐ 核心亮点 |
| Function Calling | Kimi API tool_calls | ⭐⭐⭐ 核心亮点 |
| 流式 SSE | 实时推送 thinking/content/action | ⭐⭐⭐ 核心亮点 |
| 4 个 Skill | listTemplates/listCases/createCase/openCase | ⭐⭐ 不错，但可以更多 |
| 增量 JSON 解析 | 流式中提取已完成字段 | ⭐⭐⭐ 技术深度 |
| Markdown 渲染 | markdown-it + v-html | ⭐ 基础能力 |
| 思考过程展示 | reasoning_content 折叠卡片 | ⭐⭐ 加分项 |

## 三、和面试官聊什么（话术参考）

1. **Agent 架构**："我的 AI 助手不是简单的问答，而是一个 Agent 循环——AI 可以自主决定调用哪个工具，拿到结果后继续推理，直到给出最终回答。"
2. **为什么用 Function Calling 而不是正则提取**："结构化输出，AI 返回标准 JSON，不会出现解析错误。"
3. **流式体验**："用户不需要等 AI 全部想完，思考过程、内容、工具调用都是实时推送的。"
4. **前端如何处理 Agent 事件**："前端用 SSE 接收 6 种事件类型（thinking/content/action/field/error/done），分别渲染到不同 UI 组件。"

## 四、当前不足 & 强化建议（优先级排序）

### P0 - 必须做（面试基本盘）
1. **增加更多 Agent Skill**
   - `searchCase` - 按关键词搜索案卷
   - `getCaseDetail` - 查看案卷详情
   - `deleteCase` - 删除案卷（带确认）
   - `fillCaseField` - AI 直接填充某个案卷的某个字段
   - **目标**：从 4 个 → 8-10 个，覆盖 CRUD + 搜索 + 导航

2. **前端 Action 渲染**
   - 工具调用时显示一个"正在执行 xxx..."的动画卡片
   - 工具返回结果后展示结构化数据（表格/卡片），而不是纯文本
   - `openCase` 返回后自动跳转到对应页面

3. **错误处理 & 边界情况**
   - AI 返回了不存在的 case_id 怎么办？
   - 工具执行失败后 Agent 能否自动重试或给出友好提示？

### P1 - 加分项（脱颖而出）
4. **多轮工具链**
   - 用户说"帮我用离婚协议模板创建一个李某诉张某的案卷"
   - Agent 应该：listTemplates → 找到离婚协议 ID → createCase → 返回结果
   - 这就是**真正的 Agent**：自主规划多步操作

5. **用户确认机制**
   - 对危险操作（createCase/deleteCase）弹出确认对话框
   - 用户确认后才真正执行
   - 这体现**安全意识**，面试加分

6. **会话记忆**
   - 当前 history 只传最近 20 条，每次刷新就丢了
   - 可以做服务端持久化，或者至少让 AI 记住"上次创建的案卷是哪个"

### P2 - 锦上添花
7. **Agent 可观测性面板**
   - 在 UI 上展示 Agent 的决策过程：第几轮、调用了什么工具、耗时多少
   - 类似 LangSmith 的 trace 视图，面试时 demo 效果极好

8. **Streaming Tool Calls**
   - 工具参数也是流式拼接的（你已经实现了），可以在前端实时显示参数的生成过程

## 五、面试项目介绍模板

> "我做了一个法律文书平台，核心亮点是 **AI Agent 系统**。
> 用户只需要用自然语言描述需求，AI 会自动调用平台 API 来完成操作——
> 比如查模板、创建案卷、填充字段，整个过程是 **多轮自主决策** 的。
> 
> 技术上，后端用 Node.js 实现了 Agent Loop + Function Calling，
> 前端用 Vue3 + SSE 做了流式渲染，包括思考过程、内容、工具调用动画。
> 
> 我认为 AI Agent 是前端的下一个重要方向——
> 以后用户不需要点按钮，直接说话就能操作整个系统。"

---

## 六、实施顺序建议

1. 先把 P0 的 1-3 做完（2-3 天）
2. 录一个完整的 demo 视频（Agent 多轮工具调用的全流程）
3. 再做 P1 的 4-5（1-2 天）
4. P2 看时间，有就做
