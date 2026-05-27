# AI热点情报台 Skill 封装说明

> 目的：这份文档用于说明当前已落地的工作区原生 Skill 封装结果，并保留能力边界、触发语句、参数映射与工作流示例，供后续维护与扩展参考。

## 当前落地状态

当前项目已经落地 1 个工作区原生 Agent Skill：

- `.github/skills/hot-monitor/SKILL.md`

随包附带文件：

- `.github/skills/hot-monitor/references/api-contract.md`
- `.github/skills/hot-monitor/evals/evals.json`

当前封装策略：

- 使用 1 个总 Skill 覆盖“查热点 / 管监控 / 配系统 / 触发扫描”四类意图
- 优先通过本地 HTTP API 执行，不依赖前端 UI 点击
- 兼容 `http://localhost:8000` 与 `http://localhost:8001` 两个端口
- 删除监控项时要求二次确认

已完成的联测范围：

- 状态读取
- 热点查询
- 监控新增与删除
- 扫描触发
- 设置更新

测试邮件未纳入自动联测默认步骤，因为会产生真实外部副作用。

## 1. Skill 目标

AI热点情报台面向 AI 编程博主，核心目标是把“发现热点、追踪关键词、确认系统状态、触发扫描”这四类动作封装成可复用的 Agent Skill。

技能不应依赖前端点击完成业务，而应直接调用后端 HTTP API。

## 2. 推荐拆分方式

建议至少拆成 4 个能力块，也可以合并为 1 个总 skill 后在内部路由：

| 能力块   | 主要用途                                           | 推荐接口                                                                   |
| -------- | -------------------------------------------------- | -------------------------------------------------------------------------- |
| 热点查询 | 查询热点列表、按条件筛选、读取热点详情             | `GET /api/v1/topics`、`GET /api/v1/topics/{id}`                            |
| 监控管理 | 添加关键词/账号、启停监控、删除监控、查看命中      | `GET/POST/PATCH/DELETE /api/v1/keywords`、`GET /api/v1/keywords/{id}/hits` |
| 系统配置 | 读取配置、更新扫描参数、更新通知参数、发送测试邮件 | `GET/PUT /api/v1/settings`、`POST /api/v1/settings/test-email`             |
| 扫描控制 | 手动触发扫描、查看扫描执行状态、读取调度器状态     | `POST /api/v1/topics/scan`、`GET /api/v1/settings/status`                  |

## 3. 触发语句建议

下面这些自然语言，应该能稳定触发 skill：

- 帮我看一下今天有哪些 AI 热点
- 找热度大于 7 的热点
- 看看哪些热点是监控词命中的
- 帮我添加一个关键词监控：GPT-5
- 帮我监控 OpenAI 的 X 账号
- 把某个关键词监控停掉
- 立刻刷新热点
- 看一下现在系统有没有在扫描
- 帮我把扫描间隔改成 6 小时
- 发一封测试邮件看看通知通不通

## 4. 输入输出约定

### 4.1 查询类输出

查询热点或命中记录时，建议 skill 输出统一字段：

- 标题
- 来源名称
- 来源类型
- 热度分数
- 发现时间
- 发布时间（如果有）
- AI 摘要
- 是否监控词命中
- 是否已推送
- 原始链接

如果是列表结果，默认返回 5 到 10 条，除非用户明确要求更多。

### 4.2 变更类输出

新增、更新、删除或触发扫描时，建议输出：

- 动作是否成功
- 目标对象是谁
- 实际生效的关键参数
- 若失败，返回后端 message 或 detail

## 5. 安全与确认策略

- 新增关键词、更新设置、触发扫描：可以直接执行，但执行后要回显结果
- 删除关键词：建议先确认目标条目，避免误删
- 修改系统设置：如果用户没有给出完整值，skill 应先追问，而不是猜测
- 当热点扫描已经在执行时，skill 不应重复触发，而应转为说明当前状态

## 6. 真实接口规格

### 6.1 查询热点

```http
GET /api/v1/topics?limit=20&min_heat=5&sort=heat
```

支持参数：

| 参数         | 类型   | 说明                                         |
| ------------ | ------ | -------------------------------------------- |
| limit        | int    | 返回条数，默认 50                            |
| offset       | int    | 分页偏移                                     |
| min_heat     | int    | 最低热度过滤                                 |
| sort         | string | `newest` / `heat` / `matched` / `unnotified` |
| source_names | string | 多来源过滤，逗号分隔                         |
| keyword_mode | string | `all` / `matched` / `unmatched`              |
| time_range   | string | `all` / `6h` / `24h` / `48h` / `7d`          |
| tag          | string | 单标签过滤                                   |
| q            | string | 标题和摘要搜索                               |

返回字段重点：

```json
{
  "id": 1,
  "title": "Anthropic Launches Claude Opus 4.7",
  "summary": "Anthropic 发布新模型并强调安全能力。",
  "raw_content": "...",
  "source_url": "https://...",
  "source_name": "Anthropic Blog",
  "source_type": "官方",
  "heat_score": 8,
  "tags": ["Claude", "AI Safety"],
  "is_notified": false,
  "keyword_id": null,
  "published_at": "2026-04-21T08:00:00Z",
  "relevance_score": null,
  "relevance_reason": null,
  "engagement": { "likes": 320 },
  "source_metrics": {},
  "discovered_at": "2026-04-21T09:12:52Z"
}
```

### 6.2 手动触发扫描

```http
POST /api/v1/topics/scan
```

成功返回：

```json
{ "message": "扫描任务已触发，正在后台执行", "triggered": true }
```

如果已有扫描在执行中：

```json
{ "message": "已有扫描任务正在执行，请稍后查看结果", "triggered": false }
```

### 6.3 监控词管理

```http
GET    /api/v1/keywords
POST   /api/v1/keywords
PATCH  /api/v1/keywords/{id}
DELETE /api/v1/keywords/{id}
GET    /api/v1/keywords/{id}/hits
```

新增关键词示例：

```json
{ "keyword": "GPT-5", "type": "keyword", "enabled": true }
```

新增账号示例：

```json
{
  "keyword": "OpenAI 官方",
  "type": "account",
  "platform": "twitter",
  "account_id": "openai",
  "enabled": true
}
```

关键词列表筛选参数：

| 参数     | 类型   | 说明                           |
| -------- | ------ | ------------------------------ |
| enabled  | string | `all` / `enabled` / `disabled` |
| type     | string | `all` / `keyword` / `account`  |
| platform | string | 平台精确过滤                   |
| search   | string | 名称或账号 ID 搜索             |
| sort     | string | `created_desc` / `created_asc` |

### 6.4 系统设置

```http
GET  /api/v1/settings
PUT  /api/v1/settings
POST /api/v1/settings/test-email
GET  /api/v1/settings/status
```

状态返回重点字段：

```json
{
  "scheduler_running": true,
  "next_run": "2026-04-21T09:55:00Z",
  "total_topics": 67,
  "total_keywords": 5,
  "scan_running": false,
  "scan_started_at": "2026-04-21T08:55:40Z",
  "scan_finished_at": "2026-04-21T08:57:01Z",
  "last_scan_success_at": "2026-04-21T08:57:01Z",
  "last_scan_duration_seconds": 81.0,
  "last_scan_error": null
}
```

## 7. 推荐工作流模板

### 7.1 “刷新热点”

1. `POST /api/v1/topics/scan`
2. 如果 `triggered=true`，再调用 `GET /api/v1/settings/status` 轮询扫描状态
3. 当 `scan_running=false` 时，向用户回报扫描完成情况

### 7.2 “帮我监控某个关键词”

1. 检查用户给出的词或账号信息是否完整
2. 调用 `POST /api/v1/keywords`
3. 返回新增条目 ID、监控类型、启用状态

### 7.3 “今天有哪些值得写的热点”

1. 调用 `GET /api/v1/topics`
2. 默认带上适度筛选，如 `sort=heat` 或 `time_range=24h`
3. 输出结构化列表，而不是直接回传原始 JSON

## 8. Base URL 约定

- 默认：`http://localhost:8000`
- 备用：`http://localhost:8001`

如果 skill 运行时默认端口访问失败，应允许切换 base URL，而不是直接判定服务不可用。

## 9. 封装建议

- 如果你打算做一个总 skill，description 应明确覆盖“热点、监控词、扫描、设置、系统状态”这些触发词
- 如果你打算拆 skill，优先拆成“热点查询”和“监控管理”两大块，配置与扫描控制可作为附属能力
- 最终 SKILL.md 应尽量直接复用这份文档里的能力边界、参数表和工作流模板，减少二次整理
