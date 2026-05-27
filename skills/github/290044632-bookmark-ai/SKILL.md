# Skill

## 什么是Skill？

```mermaid
flowchart LR
A["Skill"]

A-->|作用|A1>"一种轻量级的开放格式，可通过专业知识和工作流程扩展 AI 代理的功能"]

A-->|本质|A2{{"一个至少包含SKILL.md文件以及其他非必须资源的文件目录"}}
```

## 为什么要使用Skill？

```mermaid
flowchart LR

A["Skill"]
A-->|特点|A1("Domain expertise（领域专业知识）")-->|解释|A11>"将某一领域内专业知识收集为可重用的指令和资源"]
A-->|特点|A2("Repeatable workflows（可重复的工作流）")-->|解释|A21>"将多步骤任务转化为一致、可审计的流程"]
A-->|特点|A3("Cross-product reuse（跨产品可重用）")-->|解释|A31>"只需创建一次技能，即可在任何兼容该技能的代理中使用它"]
```

## Skill如何工作？

```mermaid
flowchart LR
    s["Skill"] -.工作流程.-> one
    subgraph one["第一步"]
        direction TB
        A(("Discovery/发现"))-.->|解释|A1>"启动时代理只加载每一个可用Skill的名称和描述，
            便于知道什么时候可以使用."]

    end
    subgraph two["第二步"]
        direction TB
        B(("Activation/激活"))-.->|解释|B1>"当任务与技能描述相符时，
         代理会将完整的SKILL.md指令解读到上下文中"]

    end
    subgraph three["第三步"]
       direction TB
       C(("Execution/执行"))-.->|解释|C1>"代理程序会按照指令执行，
         并可根据需要选择性地执行捆绑代码或加载引用文件"] 
    end
one-->two-->three
```

## Skill文件结构

```mermaid
flowchart LR
    A["Skill"]-.组织结构.->folder
    subgraph folder["目录结构"]
        direction TB
        root[📁 skill-name]
        root --> core[📄 SKILL.md]-->core_doc[["必须，元数据和指令"]]
        root --> scripts[📁 scripts]-->scripts_doc[["可执行代码目录"]]
        root --> references[📁 references]-->references_doc[["文档目录"]]
        root --> assets[📁 assets]-->assets_doc[["模板、资源目录"]]
        root --> other[📁/📄 ...]-->other_doc[["其他任何文件和目录"]]
    end
    
classDef required color:red,stroke:red
classDef optional stroke-dasharray: 5 5
class core,core_doc required
class scripts,references,assets,other optional
```

## Skill.md

```mermaid
flowchart LR
    A["Skill.md"]
    A-->|Yaml格式|A1["Metadata"]-.->A11{{"---
    name: Skill名称，
    description: Skill描述
    ...
    ---
    "}}
    A-->|Markdown格式|A2["Instructions"]-.->A21{{"Markdown语法格式片段"}}
```
- Metadata属性列表

| 属性名           | 是否必填 | 描述                       | 要求                                                                                               |
|---------------|------|--------------------------|--------------------------------------------------------------------------------------------------|
| name          | √    | Skill名称                  | 最多64个字符； <br/>只能使用小写字母、数字、连字符(-)；<br/>不能使用连字符(-)开始和结尾；<br/>不能包含连续的连字符(--)；<br/>必须保持与Skill根目录名一致； |
| description   | √    | 描述信息                     | 最多1024个字符；<br/>应当描述Skill能做什么以及什么时候使用；<br/>应包含有助于代理识别相关任务的特定关键词;                                  |
| license       |      | 许可证                      |                                                                                                  |
| compatibility |      | 兼容性描述，如Skill依赖的运行环境，依赖包等 | 最多500字符；                                                                                         |
| metadata      |      | 可选的附加元数据                 | yaml格式的key:value键值对                                                                              |
| allowed-tools |      | 一系列以空格分隔的、预先批准运行的工具      | **试验阶段**                                                                                         |

```yaml
---
name: my-skill
description: 支持读取MySQL数据库表结构生成Mybatis相关文件。在基于Mybatis和MySQL开发Java项目时使用。
license: Apache License 2.0
compatibility: 需要MySQL8.0+、JDK21+、SpringBoot4.x、MyBatis3.x
metadata:
  author: yiduo
  email: yiduo@projdk.com
---
```

## Skill Description编写黄金原则

```mermaid
flowchart LR
    A["Skill黄金原则"]
    A-->A1("Use imperative phrasing（使用祈使句）")-.解释.->A11>"把描述写成指令：
    告诉代理在什么时候使用Skill，而不是Skill可以做什么"]
    A-->A2("Focus on user intent, not implementation
    （关注用户意图，而非具体实现）")-.解释.->A21>"描述用户想要达成的目标，而不是技能的内部机制。
    智能体会根据用户的需求进行匹配."]
    A-->A3("Err on the side of being pushy
    （宁可强势一点）")-.解释.->A31>"明确列出Skill适用的上下文，包括用户没有直接提及领域的情况"]
    A-->A4("Keep it concise（尽量简洁）")-.解释.->A41>"既要足够长以涵盖技能的范围，
    又要足够短以避免在涉及多个技能时使智能体的上下文信息过于冗杂"]
```

## Skill Script设计原则

```mermaid
flowchart LR
    A["Skill Script核心设计原则"]
    A-->A1("Avoid interactive prompts
    （避免交互提升模式）")
    A1-.->|解释|A11>"Agent操作在非交互式Shell环境，
      无法响应 TTY 提示、密码对话框或确认菜单；
      如果脚本阻塞在交互式输入上，将被无限期地挂起。"]
      
    A-->A2("Document usage with --help
    （使用--help参数查看脚本使用方法）")
    A2-.->|解释|A21>"--help输出是Agent学习脚本使用方法的唯一途径"]
    
    A-->A3("Write helpful error messages
    （输出有用的错误信息）")
    A3-.->|解释|A31>"错误信息会直接影响Agent的下一次尝试；
    错误信息应该明确告诉Agent下一步如何处理；
    而非模棱两可的简单错误提示"]
    
    A-->A4("Use structured output
    （使用结构化输出）")
    A4-.->|解释|A41>"优先使用标准数据结构（如：json,xml等）；
    能同时被Agent和标准工具解析（如：jq,awk等）"]
    
    A-->A5("Separate data from diagnostics
    （诊断数据与输出分离）")
    A5-.->|解释|A51>"调试信息输出到stderr，输出结果输出到stdout；
    代理即可捕获清晰可解析的输出数据，
    有可以在需要时访问调试日志信息"]
```
```mermaid
flowchart LR
    A["Skill Script设计原则"]
    
    A-->A1("Idempotency
    （幂等性）")
    A1-.->|解释|A11>"Agent可能会重复执行脚本"]

    A-->A2("Input constraints
    （约束输入）")
    A2-.->|解释|A21>"用明确的错误拒绝不明确的输入，尽量使用枚举和闭集"]

    A-->A3("Dry-run support
    （支持试运行）")
    A3-.->|解释|A31>"对于破坏性或有状态的操作，
    --dry-run标志可以让Agent预览将要发生的事情"]

    A-->A4("Meaningful exit codes
    （有意义的退出码）")
    A4-.->|解释|A41>"不同的失败类型（未找到、参数无效、身份验证失败）使用不同的退出代码，
    并在`--help`输出中进行说明，以便代理程序了解每个代码的含义"]

    A-->A5("Safe defaults
    （安全的默认值）")
    A5-.->|解释|A51>"考虑破坏性操作是否需要明确的确认标志（--confirm、--force）
    或其他与风险级别相适应的安全措施"]

    A-->A6("Predictable output size
    （可预测的输出规模）")
    A6-.->|解释|A61>"许多Agent会自动截断超出阈值（例如，10-30K字符）的工具输出，
    可能会丢失关键信息；
    如果脚本产生大量输出，则默认为摘要或合理的限制，
    并支持像——offset这样的标志，以便Agent可以在需要时请求更多信息；
    如果输出很大且不适合分页，则要求Agent传递——output标志，
    以显式地选择加入标准输出"]
```