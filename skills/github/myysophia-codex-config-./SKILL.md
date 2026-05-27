# Autonomous Skill (自主技能) 使用指南

**Autonomous Skill** 是一个用于处理复杂、长时任务的工具。它允许 Codex 在“非交互模式”下连续运行多个会话，自动分解任务、执行代码、跟踪进度，直到目标完成。

## 核心功能

*   **自动任务分解**：通过“初始化者 (Initializer)”智能分析需求，生成详细的任务清单 (`task_list.md`)。
*   **自主循环执行**：通过“执行者 (Executor)”自动读取清单，逐项执行，并在一个会话结束后自动开启下一个会话。
*   **断点续传**：所有状态保存在磁盘上，支持随时中断和恢复。

## 快速开始

所有操作均通过 `run-session.sh` 脚本完成。

### 1. 启动新任务

只需描述你想做什么，脚本会自动生成任务名并开始执行。

```bash
# 进入脚本目录 (或者直接使用绝对路径)
cd skills/autonomous-skill/scripts/

# 启动任务
./run-session.sh "为待办事项应用构建一个 REST API"
```

### 2. 查看任务列表

查看当前所有任务的状态（进行中、已完成）。

```bash
./run-session.sh --list
```

### 3. 继续已有任务

如果任务被中断（例如按了 Ctrl+C），或者是分阶段进行的，可以使用 `--continue` 继续。

```bash
# 先查看任务名
./run-session.sh --list

# 继续指定任务
./run-session.sh --task-name build-rest-api --continue
```

## 进阶用法

### 启用网络访问
如果任务需要访问互联网（例如抓取网页、API 交互），需要添加 `--network` 参数。
*注意：这将使用危险的无沙箱模式，请确保你信任该操作。*

```bash
./run-session.sh --network "分析 GitHub 上最新的热门 React 库"
```

### 恢复上一次的会话上下文
默认情况下，每次“执行者”会话都是新的（为了节省 Token），只读取 `task_list.md` 和 `progress.md`。如果你希望保留上一次对话的完整上下文（例如为了不仅关注任务清单，还要记住刚才的对话细节），可以使用 `--resume-last`。

```bash
./run-session.sh --task-name my-task --continue --resume-last
```

## Claude Skill 使用说明

当你希望“使用 Claude 或 Claude Code 来完成任务”（例如实现功能、代码审查、批量修改），可以使用 `claude-skill`。它基于 Claude Code CLI 的无交互模式执行，默认开启 `acceptEdits`，会自动接受文件编辑权限。

### 1. 环境准备

先确认 Claude Code CLI 已安装：

```bash
claude --version
```

如果未安装：

```bash
npm install -g @anthropic-ai/claude-code
```

### 2. 基础用法（推荐）

直接用 `-p` 传入任务描述，并允许常用工具：

```bash
claude -p "实现登录功能并补充测试" \
  --permission-mode acceptEdits \
  --allowedTools "Read,Write,Edit,Bash"
```

### 3. 指定可用工具（更安全）

只允许读取和运行特定命令：

```bash
claude -p "运行测试并分析失败原因" \
  --permission-mode acceptEdits \
  --allowedTools "Read,Bash(npm test)"
```

### 4. 只读分析模式（不改代码）

```bash
claude -p "分析项目架构并给出优化建议" \
  --permission-mode plan \
  --allowedTools "Read"
```

### 5. 多轮会话（续接）

```bash
claude --continue \
  --permission-mode acceptEdits \
  "继续完成剩余任务并补充测试"
```

### 6. 输出 JSON 结构（自动化集成）

```bash
claude -p "输出安全审查报告" \
  --output-format json \
  --allowedTools "Read"
```

### 7. 适用场景建议

- 代码实现：`acceptEdits + Read/Write/Edit/Bash`
- 代码审查：`plan + Read`
- 批量修改：`acceptEdits + Read/Write/Edit`
- 运行测试：`acceptEdits + Read + Bash(npm test)`

## 目录结构说明

任务数据存储在项目根目录下的 `.autonomous/` 文件夹中：

```text
project-root/
└── .autonomous/
    ├── my-task-name/
    │   ├── task_list.md        # [核心] 任务清单，用于追踪进度
    │   ├── progress.md         # [记录] 每次会话的执行笔记
    │   ├── session.id          # [系统] 用于恢复会话的 ID
    │   └── session.log         # [日志] 完整的执行日志
    └── ...
```

## 常见问题

1.  **如何修改计划？**
    你可以直接编辑 `.autonomous/<任务名>/task_list.md` 文件。你可以添加、删除任务，或者手动标记某些任务为已完成 (`[x]`)。

2.  **任务卡住了怎么办？**
    *   检查 `.autonomous/<任务名>/session.log` 查看报错。
    *   尝试删除 `session.id` 文件，强制开启一个全新的会话（不携带历史上下文）。

3.  **如何完全重置一个任务？**
    直接删除对应的 `.autonomous/<任务名>/` 目录即可。
