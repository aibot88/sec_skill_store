# Agent Skill

本文档是面向通用 Python Agent 系统的 `Agent Skill` 设计规范。

本文档关注 `Agent Skills` 本身，不依赖任何具体项目实现，也不绑定某个特定框架、目录结构或运行时。目标是为开发者提供一套可以直接落地的 `Skill` 设计、定义、治理与演进规则，使 `Skill` 成为 Agent 系统中的稳定能力抽象，而不是临时拼接的函数集合。

`Agent Skill` 的核心理念来自 Agent Skills 生态：将一项可复用能力封装为一个可被发现、理解、选择、加载、执行和治理的能力单元。它既可以承载 instruction，也可以承载结构化 schema 与 executable handler，还可以作为 workflow 组成部分被更高层 Agent 编排。

---

# 1. Overview

在 Agent 系统中，`Skill` 的定义是：

> 一个可复用、可组合、可路由、可执行、可治理的能力单元，用于让 Agent 以稳定方式完成某一类任务。

一个完整的 `Skill` 应当回答以下问题：

- 这个能力做什么
- 在什么任务条件下应该被选中
- 接受什么输入
- 产生什么输出
- 通过什么 `handler` 执行
- 有哪些 side effects
- 需要哪些权限、依赖与上下文

`Skill` 在 Agent 系统中承担三种核心角色：

- `Capability packaging`
  把一项能力打包成可复用单元，例如 `web_search`、`file_read`、`document_summarize`、`robot_plan_navigation`。
- `Routing target`
  为 Agent、Router 或 Planner 提供可选择目标，使系统能够从当前任务中判断“是否应使用该 Skill”。
- `Execution boundary`
  提供结构化输入输出边界，使校验、权限控制、异常归一化、监控和审计都可统一接入。

`Skill` 与 `function`、`tool`、`API` 的区别：

- `function`
  `function` 是实现细节，解决局部逻辑。`Skill` 是 Agent 可感知的能力抽象，内部可以调用多个 `function`。
- `tool`
  `tool` 是底层操作单元，例如发请求、读文件、执行 shell。`Skill` 可以编排一个或多个 `tool`。
- `API`
  `API` 是外部系统提供的接口。`Skill` 可以依赖 `API`，但 `Skill` 本身是面向 Agent 的能力契约。

简化理解：

- `function` 回答“如何实现一段逻辑”
- `tool` 回答“如何执行一个底层动作”
- `API` 回答“如何访问一个外部系统”
- `Skill` 回答“Agent 如何稳定完成一类任务”

规范要求：

- 任何希望被 Agent 发现、选择、复用、治理的能力，都应设计为 `Skill`
- 任何只存在于局部实现、没有独立 schema 和 metadata 的代码，不应被当作 `Skill`
- 一旦某项能力被定义为 `Skill`，就必须接受统一的注册、执行、监控和生命周期治理

---

# 2. Design Principles

`Skill` 设计必须遵循以下原则。

- `Skill 是能力单元，不是普通函数`
  `Skill` 应表达一项完整能力，而不是对现有函数做浅包装。

- `Skill 必须可复用`
  `Skill` 不应只服务某一轮对话或某一个临时任务实例，而应可被不同 Agent 流程稳定复用。

- `Skill 必须可组合`
  `Skill` 应能被更大 workflow、planner、router 或 sub-agent 编排。

- `Skill 必须结构化`
  可执行 `Skill` 必须具备明确的 `input_schema` 和 `output_schema`。单纯自然语言说明不足以支撑工程化执行。

- `Skill 必须具备明确执行语义`
  side effects、权限、超时、异常、幂等性和资源边界必须可见，不能隐藏在实现细节中。

- `Skill 应尽量减少隐式状态`
  `Skill` 不应依赖未声明的全局变量、隐式 context、神秘环境变量或不可见单例。

- `Skill 应控制 side effects`
  优先设计为纯能力；必须产生 side effects 时，应明确声明影响范围、权限要求和回滚策略。

- `Skill 应支持 progressive disclosure`
  在 routing 阶段，应优先使用 `name`、`description`、tags 等轻量信息进行筛选，而不是一次性暴露全部实现细节。

- `Skill 应可测试`
  schema、handler、execution flow 必须能独立于完整 Agent 主循环进行测试。

强制性规范：

- `Must`
  每个可执行 `Skill` 必须有稳定 `name`、清晰 `description`、显式 `handler`、结构化 `input_schema`、结构化 `output_schema`
- `Must`
  每个 `Skill` 必须能被独立注册、独立调用、独立测试
- `Must`
  每个存在 side effects 的 `Skill` 必须声明权限边界和影响范围
- `Must Not`
  `Skill` 不得把核心输入隐藏在 prompt 文本、全局状态或隐式 context 中
- `Should`
  `Skill` 应优先组合已有能力，而不是复制底层逻辑
- `Should`
  `Skill` 应具备明确版本和 replacement 策略

---

# 3. Skill Definition

一个完整 `Skill` 通常包含两层定义：

- `External definition`
  面向 portable packaging 的定义，例如 `SKILL.md`、metadata、instruction、triggering information。
- `Internal definition`
  面向 runtime execution 的定义，例如 Python model、schema、registry entry、handler reference。

## 3.1 Core Fields

每个可执行 `Skill` 至少应包含以下核心字段。

- `name`
  唯一标识。用于注册、查询、路由、监控与版本管理。

- `description`
  面向 routing 的简明描述，必须清楚表达“什么时候应该调用这个 Skill”。

- `input_schema`
  结构化输入契约，定义字段、类型、约束、默认值与校验规则。

- `output_schema`
  结构化输出契约，定义下游可以依赖的稳定结果结构。

- `handler`
  实际执行逻辑的 Python callable 或 entrypoint。

- `metadata`
  用于承载扩展配置，例如 `version`、`tags`、`required_permissions`、`timeout`、`owner`、`status` 等。

推荐扩展字段：

- `version`
  `Skill` 版本号，建议使用 semver。

- `tags`
  可用于搜索、筛选和路由增强的标签集合。

- `required_permissions`
  执行前必须满足的权限集合。

- `allowed_tools`
  当前 `Skill` 允许调用的 `tool` 范围。

- `entrypoint`
  可被 runtime 解析的 Python import 路径，格式建议为 `module.submodule:function`。

- `examples`
  输入示例、输出示例、触发示例与失败示例。

字段规范要求：

- `name`
  必须全局唯一，必须稳定，禁止带用户信息、环境信息、随机后缀
- `description`
  必须描述触发条件、适用任务和边界，禁止写成空泛宣传语
- `input_schema`
  必须表达真实执行所需最小输入，禁止依赖“调用方自己知道还要传什么”
- `output_schema`
  必须表达下游可依赖结果，禁止返回无结构自由文本让下游自行猜测
- `handler`
  必须可解析、可测试、可追踪，禁止通过隐式脚本拼接执行
- `metadata`
  只应用于扩展属性，不得替代核心字段

一个合格的 `Skill` 定义必须同时满足：

- `Completeness`
  足以支持 discovery、routing、execution、monitoring
- `Determinism`
  在相同输入和依赖条件下，行为应尽量可预期
- `Observability`
  结果、错误和性能特征可追踪
- `Governability`
  可被 enable、disable、deprecate、replace、audit

## 3.2 推荐实现方式

推荐使用：

- `Pydantic`
  用于 `input_schema`、`output_schema`、输入校验和 JSON schema 导出
- `dataclass`
  用于运行时 `Skill` 记录对象、执行结果对象等
- `Enum`
  用于 `SkillCategory`、`SkillStatus`、`SideEffectLevel`
- `pathlib.Path`
  用于文件、目录或资源定位

示例：

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SkillCategory(StrEnum):
    TOOL = "tool"
    WORKFLOW = "workflow"
    KNOWLEDGE = "knowledge"
    SYSTEM = "system"


class WebSearchInput(BaseModel):
    query: str = Field(description="自然语言搜索请求。")
    top_k: int = Field(default=5, ge=1, le=20, description="返回结果数量上限。")


class WebSearchOutput(BaseModel):
    results: list[dict[str, Any]] = Field(description="标准化后的搜索结果列表。")


@dataclass(frozen=True, slots=True)
class RuntimeSkill:
    name: str
    description: str
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]
    handler: str
    metadata: dict[str, str] = field(default_factory=dict)
```

实现规则：

- portable 定义负责 discovery 和 instruction packaging
- runtime 定义负责 typed execution
- 不要把 instruction contract 与 execution contract 混成同一层

## 3.3 Skill Contract Requirements

### 3.3.1 Routing Contract

Routing contract 决定 Agent 能否正确选中一个 `Skill`。

必须包含：

- 可区分的 `name`
- 高辨识度 `description`
- 必要的 tags 或 category 信息

要求：

- `description` 必须回答“什么时候用”
- `description` 必须包含领域语义，而不是只写“处理任务”
- `description` 不得同时覆盖多个无关任务

### 3.3.2 Execution Contract

Execution contract 决定系统能否稳定执行一个 `Skill`。

必须包含：

- `input_schema`
- `output_schema`
- `handler`
- side effect 说明
- permission 要求

要求：

- `handler` 的输入输出语义必须与 schema 一致
- schema 变化必须受 version 管理
- 任何 breaking change 都必须通过 version 或 replacement 明确体现

### 3.3.3 Operational Contract

Operational contract 决定该 `Skill` 是否适合进入生产系统。

必须包含：

- owner 或责任归属
- version
- status
- monitoring 指标
- 失败语义说明

要求：

- 无 owner 的 `Skill` 不应进入生产
- 无测试的 `Skill` 不应进入默认启用状态
- 无 telemetry 的高风险 `Skill` 不应进入自动调用链路

---

# 4. Skill Categories

可按能力性质将 `Skill` 划分为四类。

## 4.1 Tool Skills

`Tool Skill` 是对单一底层能力的稳定封装。

特点：

- 功能聚焦
- schema 清晰
- side effects 明确
- 常常直接对应一个 `tool adapter` 或领域服务

适用场景：

- `web_search`
- `file_read`
- `db_query`
- `send_email`

## 4.2 Workflow Skills

`Workflow Skill` 负责将多个步骤、多个 `tool` 或多个下层 `Skill` 组合成更高层能力。

特点：

- 包含多步 orchestration
- 复用价值高
- 通常包含 retry、fallback、post-processing

适用场景：

- `research_and_summarize`
- `plan_and_execute_code_fix`
- `robot_pick_and_place`

## 4.3 Knowledge Skills

`Knowledge Skill` 封装领域知识、推理模板、知识检索策略或专家型 instruction。

特点：

- 副作用低
- routing 价值高
- 常与 retrieval 或 structured post-processing 结合

适用场景：

- `medical_guideline_lookup`
- `legal_clause_explainer`
- `robot_fault_diagnosis_guide`

## 4.4 System Skills

`System Skill` 服务于 Agent 系统本身，而非直接面向业务任务。

特点：

- 偏内部运行时能力
- 常见于 planning、memory、safety、governance、recovery

适用场景：

- `context_compaction`
- `safety_policy_check`
- `task_router`
- `session_recovery`

---

# 5. Skill Lifecycle

`Skill` 生命周期通常包括以下阶段。

## 5.1 Define

开发者需要完成：

- 编写 portable definition
- 编写 `handler`
- 定义 `input_schema` 与 `output_schema`
- 补充 `metadata`
- 补充示例与测试

定义阶段必须满足：

- 名称唯一
- 描述可用于 routing
- 可执行入口明确
- 输入输出结构明确
- 权限边界明确

定义验收标准：

- portable definition 可以被 loader 正确发现和解析
- runtime 定义可以被 registry 正确注册
- `handler` 可被 executor 正确调用
- 输入输出 schema 至少有一组有效测试样例
- 失败路径至少有一组异常测试样例

## 5.2 Register

`Skill` 被构造成 runtime object 后，需要注册到 `SkillRegistry`。

注册阶段包括：

- 唯一性校验
- metadata 校验
- source 记录
- enabled 状态初始化

注册阶段禁止：

- 用重复名称覆盖现有 `Skill` 而无显式 replace 策略
- 注册缺失核心字段的半成品 `Skill`
- 把 schema 不完整或 discovery 失败对象写入 registry

## 5.3 Discover

`SkillLoader` 负责从配置 source 中发现 `Skill`。

discovery 阶段负责：

- 文件发现
- frontmatter 或 manifest 解析
- schema 校验
- runtime object 构建

discovery 规范：

- 解析失败必须可定位到文件路径与错误原因
- 无效 `Skill` 必须被显式记录，不能静默吞掉
- source 与来源目录必须可追踪

## 5.4 Execute

执行阶段由 `SkillExecutor` 或等价执行层负责。

执行阶段至少应包括：

- 输入校验
- 权限校验
- `handler` 解析
- `handler` 调用
- 输出校验
- 异常归一化

执行阶段规范：

- 不允许绕过 `input_schema` 直接执行 `handler`
- 不允许绕过权限检查执行高风险 `Skill`
- 不允许把未校验输出直接交给下游 workflow
- 必须区分业务失败、系统失败、权限失败、依赖失败

## 5.5 Monitor

每次执行都应产出可观测数据。

建议最少记录：

- `skill_name`
- `version`
- latency
- success / failure
- error class
- source
- permission context

监控阶段规范：

- 每次调用都必须生成 execution record
- 高风险 `Skill` 必须记录审计信息
- 监控数据必须足以支持问题回放与责任定位

## 5.6 Deprecate

过时 `Skill` 不应直接静默删除，而应进入 `deprecated` 状态。

下线规范：

- 在 `metadata` 中标记 `status=deprecated`
- 指定 replacement skill
- 明确移除时间点

下线阶段禁止：

- 直接删除仍在生产链路中的 `Skill`
- 不通知调用方就改变返回结构
- 不保留迁移路径就强制切换 replacement

---

# 6. Skill Management

推荐将 `Skill` 管理拆分为三层。

## 6.1 SkillRegistry

`SkillRegistry` 是运行时 `Skill` 的权威索引。

职责：

- register / unregister
- 唯一性控制
- enabled 状态维护
- 按名称获取 `Skill`
- 列表查询与筛选
- 为 routing 提供轻量匹配能力

不应承担：

- 文件解析
- `handler` 执行
- 复杂业务逻辑

## 6.2 SkillManager

`SkillManager` 是对外暴露的统一管理入口。

职责：

- 协调 `SkillLoader` 与 `SkillRegistry`
- 提供 `load`、`reload`、`enable`、`disable`、`select` 等统一 API
- 作为 Agent 或 Router 对接 `Skill` 子系统的入口

不应承担：

- 解析细节
- `handler` 执行逻辑
- 具体业务能力实现

## 6.3 SkillExecutor

`SkillExecutor` 是执行边界层。

职责：

- 按 `input_schema` 校验输入
- 解析 `handler` 或 `entrypoint`
- 注入 runtime context
- 检查权限与 timeout
- 调用执行逻辑
- 按 `output_schema` 校验输出
- 统一异常格式
- 记录 telemetry

建议接口：

```python
from pydantic import BaseModel


class SkillExecutor:
    async def execute(
        self,
        skill: "RuntimeSkill",
        payload: dict,
        *,
        context: dict | None = None,
    ) -> BaseModel:
        ...
```

职责边界总结：

- `Loader` 负责加载
- `Registry` 负责索引
- `Manager` 负责编排与对外接口
- `Executor` 负责执行

---

# 7. Skill Invocation Flow

标准调用链路如下：

`User → Agent → Router → SkillManager → SkillExecutor → Result`

步骤说明：

1. `User`
   用户提交自然语言请求或结构化任务。
2. `Agent`
   Agent 解析任务意图，判断是否需要调用 `Skill`。
3. `Router`
   Router 根据 `name`、`description`、`tags`、上下文状态与策略规则选出候选 `Skill`。
4. `SkillManager`
   `SkillManager` 解析目标 `Skill`，并检查其是否可用、是否启用。
5. `SkillExecutor`
   `SkillExecutor` 对输入做 schema 校验，执行 `handler`，处理权限、超时、异常和输出校验。
6. `Result`
   结构化结果返回给 Agent，Agent 再决定是直接回答用户，还是继续规划后续步骤。

职责边界：

- Router 解决“选哪个”
- Manager 解决“拿到哪个定义”
- Executor 解决“怎么执行”
- Agent 决定“如何消费结果”

---

# 8. Input / Output Schema Design

可执行 `Skill` 必须使用结构化输入输出。

原因：

- 保证输入可校验
- 保证输出可消费
- 降低 prompt 歧义
- 支持 tool calling
- 支持 telemetry 与 tracing
- 支持 workflow 组合
- 支持自动生成文档和 JSON schema

推荐方案：

- 使用 `Pydantic BaseModel`
- 使用 `Field` 提供 description 与约束
- 避免公共接口直接暴露 `dict[str, Any]`
- 保持字段最小但完整

示例：

```python
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    path: str = Field(description="绝对路径或工作区相对路径。")
    encoding: str = Field(default="utf-8", description="文件读取编码。")


class ReadFileOutput(BaseModel):
    content: str = Field(description="读取到的文本内容。")
    size_bytes: int = Field(ge=0, description="文件大小，单位为 byte。")
```

Schema 设计规则：

- 输入字段必须最少但足够
- 输出字段必须稳定、可机读
- optional 字段必须有明确语义
- 有限类别应使用 `Enum`
- 错误信息应在错误模型或异常语义中体现，不应隐藏在随意字符串里

Schema 强制规范：

- 输入字段命名必须自解释，禁止使用 `data`、`info`、`payload2` 等含糊名称
- 输出字段必须面向消费方设计，而不是直接暴露内部中间变量
- 同一个 `Skill` 的输出结构必须在同一 version 下保持稳定
- 当字段可为空时，必须说明“为空代表什么”
- 当字段有默认值时，默认值必须符合真实业务语义

---

# 9. Skill Naming Conventions

`Skill` 命名必须稳定、清晰、可扩展。

命名规则：

- 使用小写
- runtime Python 标识建议使用 `snake_case`
- external portable package 名称可使用 `kebab-case`
- 优先使用“动词 + 名词”或“领域 + 动作”
- 禁止使用 `helper`、`misc`、`common_task` 这类语义模糊名称

推荐示例：

- `web_search`
- `file_read`
- `file_write`
- `code_execute`
- `document_summarize`
- `robot_plan_navigation`
- `robot_execute_grasp`

鼓励采用 domain-based naming：

- `web_search`
- `browser_extract_content`
- `filesystem_read_text`
- `knowledge_retrieve_policy`
- `workflow_research_and_summarize`

命名一致性要求：

- external name 与 runtime name 的映射必须稳定
- registry key 必须统一归一化
- 同一语义能力不得出现多个近义重复命名

---

# 10. Best Practices

- `保持单一职责`
  一个 `Skill` 只解决一类清晰能力。

- `显式定义 schema`
  每个可执行 `Skill` 都必须定义 `input_schema` 和 `output_schema`。

- `明确 side effects`
  写文件、发网络请求、执行命令、修改状态都必须可见、可审计。

- `优先组合而不是复制`
  `Workflow Skill` 应优先组合已有 `Skill` 或 service，而不是复制下层逻辑。

- `description 为 routing 服务`
  `description` 应描述触发场景，而不是实现细节。

- `handler 接口保持稳定`
  非 breaking change 不应随意修改输入输出语义。

- `可测试`
  schema、handler、executor flow 应分别测试。

- `可观测`
  所有执行都应留下 logs、metrics 或 tracing 线索。

- `输出结构稳定`
  即使内部依赖 LLM，返回结果也必须符合稳定结构。

- `版本管理严格`
  输出语义变化、权限变化、行为变化应通过 version 明确体现。

Skill 交付检查清单：

- 是否有唯一 `name`
- 是否有高辨识度 `description`
- 是否定义 `input_schema`
- 是否定义 `output_schema`
- 是否有可执行 `handler`
- 是否声明 side effects
- 是否声明 permissions
- 是否有示例输入输出
- 是否有单元测试
- 是否有失败测试
- 是否可被 registry 管理
- 是否可被 executor 监控

---

# 11. Anti-Patterns

以下写法属于明确禁止的错误模式。

- `把 Skill 当成普通函数`
  只有函数实现，没有 schema、metadata、routing 信息和执行边界，不是合格 `Skill`。

- `没有 input_schema / output_schema`
  只收一个松散 `dict`，再返回一个松散 `dict`，会使 orchestration 与 validation 失控。

- `没有 docstring 或 operational description`
  如果开发者无法判断“什么时候该用它”，说明这个 `Skill` 定义不完整。

- `过度耦合 Agent`
  `Skill` 不能强依赖某个具体 Planner、Prompt 模板或内部单例。

- `隐式依赖 context`
  如果执行依赖 session、user identity、permission、env var，必须在 contract 或执行接口中显式体现。

- `过于庞大的 mega-skill`
  一个 `Skill` 中混入多个不相关能力，会导致职责失控。

- `隐藏 side effects`
  未声明就偷偷写文件、发请求、改数据库，是高风险设计。

- `仅靠 LLM 自由生成输出`
  需要 machine-consumable 结果时，必须用 schema 验证，而不能完全信任自由文本。

- `description 过宽`
  描述过宽会导致 routing 误触发，损害系统稳定性。

- `不做 version 管理`
  行为语义已变但 identifier 不变，会直接破坏下游调用。

- `把 metadata 当垃圾桶`
  任意字段都塞入 `metadata`，会破坏 contract 清晰度与类型安全。

- `输出依赖 prompt 偶然性`
  如果 `output_schema` 要求结构化结果，但实现完全依赖 prompt“希望模型刚好返回正确格式”，这是不合格设计。

- `没有治理状态`
  无 `enabled`、`deprecated`、`replacement`、`status` 语义的 `Skill` 无法进入长期维护体系。

---

# 12. Example Skill

下面给出一个完整示例，演示 `Skill` 的定义、schema、handler、注册与调用。

## 12.1 Definition

`SKILL.md`

```md
---
name: document-summarize
description: Summarize long text documents into a concise structured summary when the user asks for key points, abstract, or digest.
allowed-tools: llm.generate file.read
metadata:
  version: 1.0.0
  tags: summarization,document
  required-permissions: tool:file.read tool:llm.generate
  entrypoint: skills.document_summarize:run
---

Use this skill when the task is to summarize a document, article, report, or note.
Always preserve key conclusions, risks, and next actions.
```

## 12.2 Schema

```python
from pydantic import BaseModel, Field


class DocumentSummarizeInput(BaseModel):
    text: str = Field(description="待总结的完整文档内容。")
    max_bullets: int = Field(default=5, ge=1, le=10, description="摘要要点数量上限。")


class DocumentSummarizeOutput(BaseModel):
    summary: str = Field(description="高层摘要。")
    key_points: list[str] = Field(description="提取出的关键结论列表。")
```

## 12.3 Handler

```python
from __future__ import annotations


async def run(payload: DocumentSummarizeInput, context: dict | None = None) -> DocumentSummarizeOutput:
    text = payload.text.strip()
    sentences = [part.strip() for part in text.split(".") if part.strip()]
    key_points = sentences[: payload.max_bullets]
    summary = " ".join(key_points[:3])
    return DocumentSummarizeOutput(summary=summary, key_points=key_points)
```

## 12.4 Register

```python
registry = SkillRegistry()
registry.register(runtime_skill)
```

## 12.5 Invoke

```python
executor = SkillExecutor()
result = await executor.execute(
    runtime_skill,
    {
        "text": "Agent Skills package reusable capabilities for intelligent systems.",
        "max_bullets": 3,
    },
)
```

---

# 13. Integration with LLM / Tool Calling

`Skill` 是连接高层 Agent reasoning 与底层 tool execution 的中间层。

## 13.1 Skill 如何暴露给 LLM

在初始 routing 阶段，建议只暴露有限信息：

- `name`
- `description`
- `tags`
- `category`

当某个 `Skill` 被选中后，再加载：

- 完整 instruction
- `input_schema`
- execution metadata

这样做符合 `progressive disclosure` 设计，也能避免上下文膨胀。

## 13.2 Skill 如何用于 function calling

在 LLM function calling 场景下，可做如下映射：

- `name` 对应 tool/function name
- `description` 对应 tool description
- `input_schema` 对应 JSON schema parameters
- `output_schema` 用于执行后的结果校验

示例：

```python
def skill_to_tool_schema(skill: RuntimeSkill) -> dict:
    return {
        "type": "function",
        "function": {
            "name": skill.name,
            "description": skill.description,
            "parameters": skill.input_schema.model_json_schema(),
        },
    }
```

## 13.3 运行时建议

- 不要一次性把所有已安装 `Skill` 都暴露给 LLM
- 应先由 Router 或 Manager 选出候选集
- 执行前必须校验 arguments
- 执行后必须校验 result
- 所有 model-triggered invocation 都必须可追踪

---

# 14. Future Extensions

`Skill` 系统后续可扩展到以下方向。

- `Plugin System`
  把 `Skill` 打包为可安装插件，并支持隔离依赖。

- `Remote Skills`
  支持通过 RPC、HTTP、MCP、消息队列等方式远程执行 `Skill`。

- `Skill Marketplace`
  支持 skill repository、签名校验、审核流程与 trust policy。

- `Versioning`
  提供更完善的 semver 与 migration 机制。

- `Capability Policy Layer`
  基于用户角色、环境与风险级别决定是否允许执行某个 `Skill`。

- `Skill Graph`
  显式支持多 `Skill` DAG 或 workflow graph 编排。

- `Execution Sandbox`
  对高风险 `Skill` 提供隔离执行环境，例如 shell、browser automation、code execution。
