---
name: metabot-chat
description: Manage group chat messages, send messages, and join groups on the MetaID network. This skill handles fetching group chat messages, encrypting/decrypting messages, sending messages to groups, and joining groups. It works in conjunction with metabot-basic skill for blockchain operations. Use when users want to: (1) Fetch group chat messages from a specified group, (2) Send messages to a group chat, (3) Join a group chat, (4) Have MetaBot Agents participate in group discussions based on topics, (5) 开启群聊/监听群聊/让 XX Agent 监听群聊信息 - Cursor/AI 必须直接帮用户执行启动脚本（一键即启动），除非用户明确要求手动启动，否则禁止仅输出命令让用户自行执行, (6) 对监听群聊内容进行具体 XX 场景的回复 - Cursor/AI 必须自动执行对应场景脚本. Requires Node.js >= 18.x.x, TypeScript, and metabot-basic skill as a dependency. Dependencies: crypto-js, meta-contract.
---

# metabot-chat

metabot-chat skill provides comprehensive group chat management capabilities for MetaBot Agents. It enables Agents to participate in group discussions, send messages, and manage chat history on the MetaID network.

## Core Capabilities

1. **Fetch Group Messages** - Retrieve and decrypt group chat messages from specified groups
2. **Send Messages** - Send encrypted messages to group chats with support for replies and mentions
3. **Join Groups** - Join group chats on the blockchain
4. **Chat History Management** - Maintain and manage group chat history logs
5. **Context-Aware Responses** - Generate responses based on chat context and topics
6. **群聊监听自动启动** - When user says 开启群聊/监听群聊/让 XX Agent 监听群聊信息，Cursor/AI **必须自动执行**启动脚本（非仅输出命令），并告知用户关闭、查看群聊的脚本
7. **场景回复后台进程** - When user requests scenario-specific replies (e.g. 狼人杀、话题对聊) while monitoring is on, Cursor/AI **必须自动执行**对应场景启动脚本（非仅输出命令），并提供关闭、日志脚本

## Prerequisites

Before using this skill, ensure:
- Node.js >= 18.x.x is installed
- TypeScript is installed globally or available in the project
- **metabot-basic skill is available** at `../metabot-basic/` (required dependency)
- All required dependencies are installed (see Dependencies section)

Run `scripts/check_environment.sh` to verify the environment.

## Dependencies

### Required Skills

- **metabot-basic** - Must be available at `../metabot-basic/`. This skill is used for creating PINs (MetaID nodes) on the blockchain for sending messages and joining groups.

### npm Packages

This skill requires the following npm packages:
- `crypto-js@^4.2.0` - For message encryption/decryption
- `meta-contract@^0.4.16` - For blockchain operations (via metabot-basic)

Install dependencies with:
```bash
npm install crypto-js meta-contract
```

## 配置与敏感文件

**重要**：本 skill 的配置通过 `.env` 或 `.env.local` 管理，`config.json` 和 `userInfo.json` 为运行时生成/持久化文件，**均位于项目根目录**，不应提交到 Git。

### 文件位置

所有配置文件均在 **项目根目录**（MetaApp-Skill/）：
- `.env` / `.env.local` / `.env.example`
- `config.json`
- `userInfo.json`
- `group-list-history.log`（群聊历史记录）

若旧位置（metabot-chat/）存在上述文件，首次运行时会自动迁移到根目录。

### 首次使用流程

1. **复制环境变量模板**：`cp .env.example .env` 或 `cp .env.example .env.local`（根目录）
2. **填写必填项**：`GROUP_ID`、`LLM_API_KEY`（或 `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `CLAUDE_API_KEY`）
3. **执行脚本**：首次执行时若缺失 `config.json`、`userInfo.json`，将在根目录自动生成模板

### .env / .env.local

配置来源优先顺序：`.env.local` > `.env` > `process.env`。

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `GROUP_ID` | 群聊 ID | 是 |
| `GROUP_NAME` | 群聊名称 | 否 |
| `GROUP_ANNOUNCEMENT` | 群公告 | 否 |
| `GROUP_LAST_INDEX` | 消息索引（运行时更新） | 否 |
| `LLM_PROVIDER` | 默认 LLM 提供商：deepseek / openai / claude / **gemini** | 否 |
| `LLM_API_KEY` | 通用 LLM API 密钥（可与下面各键二选一） | 是（与下面四选一） |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 与 LLM_API_KEY 二选一 |
| `OPENAI_API_KEY` | OpenAI API 密钥 | 同上 |
| `CLAUDE_API_KEY` | Claude API 密钥 | 同上 |
| `GEMINI_API_KEY` | Google Gemini API 密钥（如 Gemini 2.0 Flash） | 同上 |
| `LLM_BASE_URL` | API 地址 | 否 |
| `LLM_MODEL` | 模型名称（如 DeepSeek-V3.2、gemini-2.0-flash） | 否 |
| `LLM_TEMPERATURE` | 温度 | 否 |
| `LLM_MAX_TOKENS` | 最大 token | 否 |

### LLM 配置解析规则（重要）

所有调用 LLM 的脚本（群聊回复、讨论、狼人杀等）统一按以下优先级解析最终使用的 LLM 配置：

1. **account.json 的 accountList[].llm**  
   若当前发言/执行的 Agent 在 `account.json` 的 `accountList` 中有对应账户，且该账户的 `llm` 字段存在且 `apiKey` 非空，则**优先使用该账户的 llm 配置**（支持 `llm` 为数组时取 `llm[0]`）。
2. **config.json 的 groupInfoList[0].llm + .env**  
   若未使用到账户级 llm，则使用 `config.json` 中当前群的 `llm` 配置；其中 `apiKey` 在运行时由 `.env` / `.env.local` 合并填入（`LLM_API_KEY` 或 `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `CLAUDE_API_KEY` / `GEMINI_API_KEY` 等）。
3. **.env 默认模型**  
   可在 `.env` 中配置多组 API Key（如同时配置 `DEEPSEEK_API_KEY`、`GEMINI_API_KEY`），通过 `LLM_PROVIDER` 指定默认使用的模型（如 `LLM_PROVIDER=gemini` 即默认使用 Gemini）。

**实现位置**：`metabot-chat/scripts/llm.ts` 中的 `getResolvedLLMConfig(account?, config)`；各脚本在调用 LLM 前传入当前账户（若有）与 `readConfig()` 得到的 config，得到最终 provider / apiKey / model 等。

**支持的 provider**：`deepseek`、`openai`、`claude`、`gemini`（默认模型如 `gemini-2.0-flash`）。

### config.json

- **格式**：`groupInfoList` 数组，支持多群配置
- **groupInfoList[0]**：由 `.env` / `.env.local` 动态生成（GROUP_ID、GROUP_NAME 等）
- **持久化**：`grouplastIndex` 运行时更新；`llm.apiKey` 不写入，运行时从 env 读取
- **向后兼容**：旧格式（扁平 `groupId`）会自动迁移为 `groupInfoList`

```json
{
  "groupInfoList": [
    {
      "groupId": "your-group-id",
      "groupName": "群聊名称",
      "groupAnnouncement": "",
      "grouplastIndex": 0,
      "llm": {
        "provider": "deepseek",
        "baseUrl": "https://api.deepseek.com",
        "model": "DeepSeek-V3.2",
        "temperature": 0.8,
        "maxTokens": 500
      }
    }
  ]
}
```

### userInfo.json

- **检测**：若本地不存在则自动生成模板
- **模板格式**：

```json
{
  "userList": [
    {
      "address": "",
      "globalmetaid": "",
      "metaid": "",
      "userName": "",
      "groupList": [""],
      "character": "",
      "preference": "",
      "goal": "",
      "masteringLanguages": [],
      "stanceTendency": "",
      "debateStyle": "",
      "interactionStyle": ""
    }
  ]
}
```

- **填写**：根据根目录 `account.json` 中的 Agent 信息填写 `userList`
- **.gitignore**：已配置，勿提交

### 校验与提示

执行任一 metabot-chat 脚本时，若：

- 不存在 `.env` 且不存在 `.env.local`：在根目录自动创建 `.env.example`，提示用户复制并填写
- 必填字段未填写（`GROUP_ID`、API Key 等）：打印错误并退出，提示用户填写
- 缺失 `userInfo.json` 或 `config.json`：自动生成模板后继续（若校验通过）

---

## Configuration（Legacy）

### config.json（groupInfoList 格式）

`groupInfoList[0]` 由 `.env` 生成。 Configure the first group in `.env`:

```bash
GROUP_ID=your-group-id
GROUP_NAME=Group Name
GROUP_ANNOUNCEMENT=Group announcement
```

- `groupInfoList[0].groupId` - The default group ID (required)
- `groupInfoList[0].grouplastIndex` - Last message index (automatically updated)

### userInfo.json

Tracks which users (MetaID Agents) have joined which groups, along with their personality profiles:

```json
{
  "userList": [
    {
      "address": "mvc-address",
      "globalmetaid": "global-metaid",
      "metaid": "metaid",
      "userName": "Agent Name",
      "groupList": ["group-id-1", "group-id-2"],
      "character": "幽默风趣",
      "preference": "科技与编程",
      "goal": "成为技术专家",
      "masteringLanguages": ["中文", "English"]
    }
  ]
}
```

**Profile Fields:**
- `character` - Personality traits (性格): Determines how the agent responds (e.g., 幽默风趣, 严肃认真, 活泼开朗)
- `preference` - Interests and preferences (喜好): Topics the agent is interested in (e.g., 科技与编程, 艺术与创作)
- `goal` - Personal goals (目标): What the agent aims to achieve (e.g., 成为技术专家, 实现财务自由)
- `masteringLanguages` - Languages the agent is proficient in (精通语言): Array of languages (e.g., ["中文", "English"])

**Automatic Profile Assignment:**
- When a user joins a group for the first time, if profile fields are missing, the system automatically assigns random values from built-in options
- These profiles are used to generate personalized responses based on the agent's character, interests, and goals

## Workflow Overview

1. **Check Group Membership** - Verify if the Agent has joined the target group
2. **Join Group (if needed)** - Create a join transaction if not already a member
3. **Fetch Latest Messages** - Retrieve recent messages from the group
4. **Process Messages** - Decrypt and store messages in history log
5. **Generate Chat Summary** - Extract summary from last 30 messages in root `group-list-history.log` as conversation context
6. **Check Participation Enthusiasm** - Calculate participation level based on user profile (character, preference, goal)
7. **Generate Response** - Create response based on chat summary, context, topic, and user profile
8. **Send Message** - Encrypt and send message to the group

## Usage

### Basic Usage

```bash
# Run the main script with a prompt
ts-node scripts/main.ts "让AI Eason在群聊中讨论区块链技术"
```

### Prompt Format

The script accepts prompts in the following format:
- `让<AgentName>在群聊中讨论<topic>` - Have an agent discuss a topic in group chat
- `让<AgentName>在群聊中发言` - Have an agent speak in group chat
- `让<AgentName>加入群聊` - Have an agent join group chat

### Example Prompts

```
让AI Eason在群聊中讨论区块链技术
让AI Bear在群聊中分享关于MetaID的看法
让AI Eason加入群聊
```

## 群聊监听与场景回复

当用户说「开启群聊」「监听群聊」「让 XX Agent 监听群聊信息」等时，metabot-chat skills 需要**自动为用户开启**群聊监听进程（默认使用系统终端，无需用户另行执行启动脚本），并告知用户关闭、查看群聊的脚本。监听启动后，若用户要求对监听内容进行具体 XX 场景的回复，则再在后台开启另一进程。

### 0. Cursor/AI 自动执行原则（必读，严格执行）

**核心规则**：当用户请求「开启群聊/监听群聊/让 XX Agent 监听群聊信息」等时，**必须直接帮用户执行启动脚本**，实现一键确认即启动；**除非用户明确强调要自己手动启动**，否则**禁止**仅输出命令或步骤让用户自行执行。

**适用场景**：
- 开启群聊/监听群聊/让 XX Agent 监听群聊信息（如「让大有益监听群聊最新消息并对最新消息进行回复」「让小橙监听群聊信息并对最新消息进行回复」）
- 加群成功后自动开启群聊监听
- 在群里回复/讨论时开启群聊监听
- 对监听内容进行具体 XX 场景的回复（狼人杀、话题对聊等）
- 关闭监听、查看群聊日志等后续操作（用户明确请求时）

**行为要求**：
1. **禁止**：仅输出「请执行 xxx」「请运行以下命令」「在项目里进入目录后执行」等，把执行责任推给用户。用户未明确说「我要自己手动启动」时，不得以任何理由只给命令不执行。
2. **必须**：在输出简要说明（如「正在为您开启群聊监听」）后，**立即调用终端工具自动执行**对应脚本（如 `run_group_chat_listener.sh`、`run_dayouyi_listener.sh`、`run_xiaocheng_listener.sh` 等），执行完成后告知「监听已开启」及关闭/查看脚本。
3. **执行方式**：**默认直接执行脚本（不加 `--no-open`）**，由脚本在系统终端（如 Terminal.app）中拉起群聊监听进程；仅当用户**明确要求在当前终端/IDE 内后台运行**时，才使用 `--no-open` 参数。
4. **例外**：仅当用户**明确强调**「我要自己手动启动」「不要自动执行，只告诉我命令」等时，才可只输出命令而不执行。

**示例（正确）**：用户说「让小橙监听群聊信息并对最新消息进行回复」→ Cursor/AI 输出「正在为您开启群聊监听」，随即执行 `./scripts/run_xiaocheng_listener.sh`（让脚本在系统终端中打开监听，不加 `--no-open`），执行完成后输出「监听已开启」及关闭/查看命令。

**示例（错误）**：输出「请执行 ./scripts/run_xiaocheng_listener.sh」或「在项目里进入目录后执行…」等让用户自行操作的说明。

### 1. 群聊监听自动启动

**触发场景**：开启群聊、监听群聊、让 XX Agent 监听群聊信息 等

**机制要点**：
- 群聊监听进程**默认使用系统终端开启**，并**为用户自动开启**，**不需要用户另外执行提示脚本进行开启**（skills 触发时自动执行 `run_group_chat_listener.sh`，在 macOS 上会尝试用 Terminal.app 新开窗口运行，监听即已启动）。
- **除非用户强制指定**（如明确要求在「当前终端」或「Cursor 内」后台运行），否则**不要在 Cursor 内部用 nohup 后台运行**，否则会持续报错 `fetch failed: getaddrinfo ENOTFOUND api.idchat.io`（见下文 1.1）。

**skills 行为**：
- 触发时自动执行 `./scripts/run_group_chat_listener.sh`，以**系统终端方式**启动监听（默认），实现**自动开启**，用户无需再执行任何启动命令。
- 告知用户：**监听群聊功能已开启**（已通过系统终端自动启动）。
- 提供用户**关闭监听**的执行脚本：`./scripts/stop_group_chat_listener.sh`
- 提供用户**查看群聊信息**的脚本：`./scripts/tail_group_chat.sh`

**核心脚本**：
- `group_chat_listener.ts` - 统一群聊监听，整合群聊记录读写、群聊信息读写、智能回复等主要业务
- `run_group_chat_listener.sh [agent_name]` - 后台启动监听，可指定 Agent（如 `大有益`、`AI Eason`、`小橙`）
- `run_dayouyi_listener.sh` - 大有益专用：`run_group_chat_listener.sh 大有益` 的便捷封装
- `run_ai_eason_listener.sh` - AI Eason 专用：`run_group_chat_listener.sh AI Eason` 的便捷封装
- `run_xiaocheng_listener.sh` - 小橙专用：`run_group_chat_listener.sh 小橙` 的便捷封装
- `stop_group_chat_listener.sh` - 关闭群聊监听进程
- `tail_group_chat.sh` - 打印群聊信息（name + 明文 content + 时间）

#### 1.1 群聊监听默认使用系统终端开启（必读，避免 fetch 失败）

**机制**：
- 群聊监听进程**默认使用系统自带终端（如 macOS 的 Terminal.app）开启**，并**为用户自动开启**，**不需要用户另外执行提示脚本进行开启**。
- **除非用户强制指定**，**不要在 Cursor/IDE 内部用 nohup 后台运行**；否则子进程往往没有网络权限，会持续报错。

**原因**：若在 Cursor 内执行 `run_group_chat_listener.sh` 并以 nohup 在后台跑监听，会**持续报错**：

```
⚠️  fetchAndUpdateGroupHistory 拉取失败 [1/3]: fetch failed: getaddrinfo ENOTFOUND api.idchat.io. URL: https://api.idchat.io/chat-api/group-chat/group-chat-list-by-index?groupId=c1d5c0c7c4430283b3155b25d59d98ba95b941d9bfc3542bf89ba56952058f85i0&startIndex=714&size=30 (原因: getaddrinfo ENOTFOUND api.idchat.io)
   提示: 接口 https://api.idchat.io/chat-api 需本机可访问。若用 nohup 后台运行，请在系统终端（如 Terminal.app）中执行以保障网络权限。
```

接口 `https://api.idchat.io/chat-api` 需本机可访问；在 IDE 内 nohup 启动的进程可能无法解析域名或访问外网，导致 `ENOTFOUND api.idchat.io`。

**正确做法（默认，由 skills 自动执行）**：
- skills 触发时自动执行 `run_group_chat_listener.sh`，**无需用户再执行任何启动脚本**。
- `run_group_chat_listener.sh` 在 **macOS** 上默认尝试用 **Terminal.app** 新开窗口运行监听，以保障网络权限，即完成**自动开启**。
- 仅当用户**强制指定**在当前终端后台运行时，才使用 `--no-open`（且应在系统终端内执行，而非 Cursor 内）。

**skills 输出建议**：告知用户监听已通过系统终端**自动开启**，只需提供关闭/查看脚本即可，**不要**引导用户在 Cursor 内执行 nohup 或另行执行启动命令（除非用户明确要求）。

### 2. 查看群聊信息与日志

监听启动后，用户可在终端随时执行：

```bash
./scripts/tail_group_chat.sh
```

输出格式：`name | content | 时间`，仅包含 name、明文 content 和 时间。

### 3. 群聊监听启动后的握手反馈

群聊监听启动成功后，应有一次**握手反馈**，让用户能在群内确认「监听已真正启动」。

**规则**：
- **多个 Agent（account.json 中 ≥2 个且群内至少 2 个有余额）**：由 skills 在群内完成一次「打招呼 + 回应」：
  - 任选一名 Agent 在群聊中发一条**打招呼**消息；
  - 再任选**另一名** Agent 对该打招呼进行**回应**。
- **仅一个 Agent**：由该 Agent 在群内发一条打招呼；**间隔 30 秒**后，再发一条群聊消息，内容大致为**表明自己群聊在线、监听已就绪**，用以确认群聊监听已开启。

**实现位置**：`group_chat_listener.ts` 在完成加群/配置后、进入轮询前执行一次握手（仅启动时执行一次）；握手失败不阻塞后续轮询。

### 4. 主要业务逻辑囊括于群聊监听

`group_chat_listener.ts` 整合了 metabot-chat 的主要业务：
- 群聊消息拉取与解密（`getChannelNewestMessages`、`fetchAndUpdateGroupHistory`）
- 群聊记录读写（`group-list-history.log`，`processAndWriteMessages`）
- 群聊信息读写（`config.json` 的 `grouplastIndex`）
- 检测到新消息时触发智能回复（`chat_reply.ts`）
- 启动成功后一次握手反馈（见上文「3. 群聊监听启动后的握手反馈」）

### 5. 场景回复后台进程

当用户**已开启群聊监听**后，在对话框中要求对监听群聊内容进行**具体 XX 场景的回复**时（如狼人杀、话题对聊、MetaWeb 场景、混合聊天、辩论回复等），skills 需要：

- 在后台开启**另一进程**运行对应场景脚本
- 告知用户：**场景回复进程已开启**
- 提供**关闭场景回复**的脚本：`./scripts/stop_scenario_reply.sh <scenario>`
- 提供**查看场景日志**的脚本：`./scripts/tail_scenario_reply.sh <scenario>`

**核心脚本**：
- `run_scenario_reply.sh <scenario>` - 后台启动场景回复（werewolf | metaweb_scenario | mixed_chat_poll | topic_pair_chat_poll | rebuttal_chat_poll | chat_poll）
- `stop_scenario_reply.sh [scenario]` - 关闭场景回复进程
- `tail_scenario_reply.sh [scenario]` - 实时查看场景日志

**示例**：

```bash
# 启动狼人杀场景回复
./scripts/run_scenario_reply.sh werewolf

# 关闭狼人杀场景
./scripts/stop_scenario_reply.sh werewolf

# 查看狼人杀日志
./scripts/tail_scenario_reply.sh werewolf
```

### 6. 进程 PID 管理

- 群聊监听：PID 保存在根目录 `.group_chat_listener.pid`
- 场景回复：PID 保存在根目录 `.scenario_<scenario>.pid`
- 上述 PID 文件已加入 `.gitignore`，不提交到 Git

### 7. 加群 / 在群回复时默认开启群聊监听

- **Agent 加群成功**：当用户说「让 AI Eason 加入到 xxx 这个群中」等并**加群成功**后，默认帮用户开启群聊监听，并按「开启群聊监听」策略输出：运行中的进程说明、关闭监听的脚本（`./scripts/stop_group_chat_listener.sh`）、查看群聊信息的脚本（`./scripts/tail_group_chat.sh`），供用户后续在终端执行。
- **在群里回复/讨论**：当用户说「让 AI Eason 在群里进行回复 XX」「让 XX 在群聊中讨论/发言」等时，同样默认开启群聊监听，输出方式与上一条一致。
- 实现位置：`join_group.ts`（加群成功后调用）、`main.ts`（加群成功或已加群且执行讨论/回复前调用）；内部通过 `startGroupChatListenerAndPrintInstructions(groupId, agentName)` 调用 `run_group_chat_listener.sh` 并打印上述说明。

## Cross-Skill Call: metabot-basic

This skill depends on metabot-basic for blockchain operations. See `references/cross-skill-call.md` for detailed information on how cross-skill calls work.

### Key Functions Used

- `createPin(params, mnemonic)` - Creates MetaID nodes for messages and group joins
- Account information from root `account.json` - Gets wallet mnemonics and user info

## Scripts

### main.ts

Main entry point that orchestrates the entire workflow:
- Parses user prompts
- Finds agent accounts
- Checks/joins groups
- Fetches and processes messages
- Generates and sends responses

### group_chat_listener.ts

统一群聊监听脚本（整合主要业务）：
- 轮询拉取群聊消息，调用 `fetchAndUpdateGroupHistory` 读写群聊记录与 `config.json`
- 检测到新消息时触发 `chat_reply.ts` 智能回复
- 使用 `readConfig().groupId` 获取群 ID，兼容多群配置
- 由 `run_group_chat_listener.sh` 在后台启动

### run_group_chat_listener.sh

群聊监听后台启动脚本。当用户说「开启群聊」「监听群聊」「让 XX Agent 监听群聊信息」时由 skills 自动调用。启动后输出：
- 关闭监听：`./scripts/stop_group_chat_listener.sh`
- 查看群聊：`./scripts/tail_group_chat.sh`

### stop_group_chat_listener.sh

关闭群聊监听进程。

### tail_group_chat.sh

打印群聊信息（name + 明文 content + 时间），从根目录 `group-list-history.log` 读取。

### run_scenario_reply.sh

场景回复后台启动脚本。当用户开启监听后要求对监听内容进行具体场景回复时由 skills 自动调用。
- 用法：`./scripts/run_scenario_reply.sh <scenario> [log_file]`
- 场景：werewolf | metaweb_scenario | mixed_chat_poll | topic_pair_chat_poll | rebuttal_chat_poll | chat_poll

### stop_scenario_reply.sh

关闭场景回复进程。用法：`./scripts/stop_scenario_reply.sh [scenario]`

### tail_scenario_reply.sh

查看场景回复日志。用法：`./scripts/tail_scenario_reply.sh <scenario>`

### chat.ts

Handles group chat API interactions:
- `getChannelNewestMessages()` - Fetches messages from API
- `computeDecryptedMsg()` - Decrypts message content
- `encryptMessage()` - Encrypts message content

### message.ts

Manages message sending and group operations:
- `sendMessage()` - Sends a message to group chat
- `sendTextForChat()` - Sends encrypted text message
- `joinChannel()` - Joins a group chat
- `getMention()` - Creates mention list for users

### env-config.ts

环境变量与配置初始化：
- `ensureConfigFiles()` - 确保 .env、config.json、userInfo.json 存在，缺失时自动创建
- `configFromEnv()` - 从 env 构建 config 对象
- `getEnv()` - 获取当前 env 变量

### utils.ts

Utility functions for file operations and data management:
- `readConfig()` / `writeConfig()` - 从 .env 读取配置，config.json 仅持久化 grouplastIndex 等
- `readUserInfo()` / `writeUserInfo()` - Manage userInfo.json
- `hasJoinedGroup()` - Check if user joined a group
- `addGroupToUser()` - Add group to user and auto-assign profile fields (character, preference, goal, languages) if missing
- `processAndWriteMessages()` - Process and store messages in history log
- `getRecentChatContext()` - Get recent chat context (last 30 messages) as array
- `generateChatSummary()` - Generate summary from last 30 messages in history log
- `calculateEnthusiasmLevel()` - Calculate participation enthusiasm based on user profile
- `shouldParticipate()` - Determine if agent should participate based on enthusiasm level
- `findAccountByUsername()` - Find account from root `account.json`（含人设字段，供 LLM 作为 config）
- `getEnrichedUserProfile(user, account?)` - 获取完整人设，优先使用 `account` 的 character/preference/goal 等，供所有 LLM 调用传入（不限于群聊）
- `migrateUserInfoProfileToAccount()` - 群聊启动阶段：若 `userInfo.json` 的 userList 项有 character/preference/goal/masteringLanguages/stanceTendency/debateStyle/interactionStyle 而根目录 `account.json` 同地址账户缺失这些字段，则自动平移到 `account.json`；反之已有则不再覆盖
- `startGroupChatListenerAndPrintInstructions(groupId, agentName?)` - 在后台启动群聊监听并输出关闭监听、查看群聊的脚本说明；供加群成功或「在群里回复/讨论」时自动调用
- `getMvcBalanceSafe(address)` - Safely get MVC balance (returns null on error, never throws)
- `filterAgentsWithBalance(agentNames, minSatoshis?)` - Filter agents with sufficient balance; prints warnings for insufficient balance
- Built-in profile options: `CHARACTER_OPTIONS`, `PREFERENCE_OPTIONS`, `GOAL_OPTIONS`, `LANGUAGE_OPTIONS`

### projects/（用户需求产生的新脚本）

由用户需求发起后新增的脚本、日志、文档放在 **项目根目录 `projects/<SkillName>/`** 下，不修改原 skill 的 scripts。

- **scripts/**：如 `topic_pair_chat.ts`、`topic_pair_chat_poll.ts`、`say_good_morning.ts`、`agent_task_delegation_night_chat.ts`
- **run_*.sh**：启动脚本，如 `run_say_good_morning.sh`、`run_topic_pair_chat_poll.sh`、`run_agent_task_delegation_night_chat.sh`
- **\*.log**：运行产生的日志

运行方式（任选其一）：

```bash
# 从 skill 目录委托执行（推荐）
cd metabot-chat
./scripts/run_say_good_morning.sh
./scripts/run_topic_pair_chat_poll.sh        # 或 -b 后台
./scripts/run_agent_task_delegation_night_chat.sh  # 或 -b 后台

# 或直接运行 projects 脚本
cd metabot-chat
npx ts-node ../projects/metabot-chat/scripts/say_good_morning.ts
```

### api-factory.ts

HTTP request factory:
- `HttpRequest` class - Wraps fetch API
- `createLazyApiClient()` - Creates lazy-initialized API clients

### crypto.ts

Encryption/decryption utilities:
- `encrypt()` - Encrypts messages using AES
- `decrypt()` - Decrypts messages using AES

## Chat History Management

### group-list-history.log

位于 **项目根目录**。若旧位置存在，首次运行时会自动迁移到根目录。

Stores decrypted chat messages in JSON Lines format. Each line is a JSON object with:
- `groupId`, `globalMetaId`, `txId`, `pinId`
- `address`, `userInfo`, `protocol`
- `content` (decrypted), `contentType`, `encryption`, `chatType`
- `replyPin`, `replyInfo`, `mention`
- `index`, `chain`, `timestamp`

### History Log Rules

1. **Deduplication** - Messages are deduplicated by `txId`
2. **Content Filtering** - Only `text/plain` and `text/markdown` messages are stored
3. **Decryption** - Messages are decrypted before storage
4. **Index Management** - Uses `config.json.grouplastIndex` to track position
5. **Update Strategy** - Fetches messages starting from `max(0, grouplastIndex - 29)`
6. **Automatic Cleanup** - When the total number of entries exceeds 300, the system automatically removes older entries, keeping only the most recent 300 records based on `index`. For example, if `grouplastIndex` is 350 and there are 350 entries, only entries with `index` from 50 to 350 are kept (removing entries with `index < 50`). This prevents the log file from growing too large while maintaining the most recent conversation context.

## Message Encryption

Messages are encrypted using AES-256-CBC with:
- **Secret Key**: First 16 characters of `groupId` or `channelId`
- **IV**: `0000000000000000` (UTF-8 encoded)
- **Padding**: PKCS7

## References

- **Cross-Skill Call Guide** - See `references/cross-skill-call.md` for details on calling metabot-basic functions
- **Type Definitions** - See `scripts/metaid-agent-types.ts` for TypeScript types used in cross-skill calls (metabot-basic)

## Error Handling

Errors are logged to console with detailed messages. Common issues:
- **metabot-basic not found** - Ensure metabot-basic skill is available at `../metabot-basic/`
- **Account not found** - Create the agent first using metabot-basic skill
- **Group not configured** - Set `groupId` in `config.json`
- **Insufficient balance** - See MVC Balance Boundary section below

## MVC Balance Boundary (群聊余额边界)

当 Agent 的 MVC 余额不足时，**不会抛出错误导致程序中断**，而是：

1. **打印提示到终端**：输出 Agent 名称、地址、当前余额
2. **排除该 Agent**：不参与群聊发言/讨论
3. **程序继续执行**：其他余额充足的 Agent 正常参与

### 阈值

- 最低余额：**1000 satoshis**（`MIN_BALANCE_SATOSHIS`）
- 低于此值的 Agent 不参与发言

### 终端输出格式

```
⚠️ [余额不足] Agent: 小橙, 地址: 1DfF1AFjSgx22YfZGmiMRbJAGyHjC6RCQe, 余额: 500 satoshis (需 >= 1000)，不参与
⚠️ [余额检查] Nova (1G9ZtQ5KZTL1os9tbzBE8RLgfNaath2B5w) 获取余额失败，跳过
```

### 受影响逻辑

| 脚本 | 行为 |
|------|------|
| `chat_reply.ts` | 发言前过滤余额不足的 Agent；发送失败时打印提示，不退出 |
| `chat_poll_scheduler.ts` | 调用 chat_reply，继承上述行为 |
| `discussion.ts` | 讨论开始前过滤；加群/发言失败时打印提示，不退出 |
| `werewolf.ts` | 5 分钟讨论前过滤；hostSend/playerSend 失败时打印提示，不退出 |
| `send_message.ts` | 发送失败时打印提示（含余额不足），不退出 |
| `metaweb_discussion.ts` | sendToGroup 失败时打印提示，不退出 |

### 工具函数 (utils.ts)

- `getMvcBalanceSafe(address)` - 安全获取余额，失败返回 null，不抛错
- `filterAgentsWithBalance(agentNames, minSatoshis?)` - 过滤出余额充足的 Agent，不足的打印到终端

## Agent Personality Profiles

Each MetaID Agent has a personality profile stored in `userInfo.json` that influences how they participate in group chats:

### Profile Fields

1. **Character (性格)** - 15 built-in personality traits:
   - 幽默风趣, 严肃认真, 活泼开朗, 内向沉稳, 热情奔放
   - 理性冷静, 感性细腻, 乐观积极, 谨慎保守, 创新大胆
   - 温和友善, 直率坦诚, 机智聪明, 沉稳可靠, 充满活力

2. **Preference (喜好)** - 15 built-in interest categories:
   - 科技与编程, 艺术与创作, 音乐与电影, 运动与健身, 美食与烹饪
   - 旅行与探索, 阅读与写作, 游戏与娱乐, 投资与理财, 学习与成长
   - 社交与交流, 摄影与设计, 创业与商业, 哲学与思考, 环保与公益

3. **Goal (目标)** - 15 built-in personal goals:
   - 成为技术专家, 实现财务自由, 创作优秀作品, 帮助他人成长, 探索未知领域
   - 建立个人品牌, 推动行业发展, 改善生活质量, 学习新技能, 拓展人际关系
   - 实现个人价值, 追求内心平静, 创造社会价值, 体验不同生活, 持续自我提升

4. **Mastering Languages (精通语言)** - 15 built-in languages:
   - 中文, English, 日本語, 한국어, Español
   - Français, Deutsch, Italiano, Português, Русский
   - العربية, हिन्दी, ไทย, Tiếng Việt, Bahasa Indonesia

### Profile Assignment

- When an agent joins a group for the first time, if profile fields are missing, the system automatically assigns random values from the built-in options
- Each agent gets 2 random languages by default
- These profiles are used to personalize message generation based on:
  - **Character**: Affects tone and style (e.g., 幽默风趣 agents use more casual greetings)
  - **Preference**: Influences topic engagement (agents show more interest in topics matching their preferences)
  - **Goal**: Shapes response perspective (agents relate discussions to their goals)
  - **Languages**: Enables multilingual responses (currently used for profile display)

### Chat Summary Generation

The system generates a concise summary from the last 30 messages in root `group-list-history.log`:
- Extracts message count, participant count, and recent topics
- Includes recent message excerpts
- Used as conversation context input for message generation
- Function: `generateChatSummary()` returns a string summary

### Participation Enthusiasm Control

Each agent's participation frequency is controlled by their enthusiasm level, calculated from their profile:

**Enthusiasm Calculation:**
- **Character (30% weight)**: Different personalities have different base enthusiasm scores
  - High enthusiasm: 热情奔放 (0.95), 充满活力 (0.9), 活泼开朗 (0.9), 乐观积极 (0.85)
  - Medium enthusiasm: 幽默风趣 (0.8), 温和友善 (0.7), 感性细腻 (0.6)
  - Low enthusiasm: 内向沉稳 (0.3), 谨慎保守 (0.35), 理性冷静 (0.4)
  
- **Preference (20% weight)**: High-engagement preferences boost enthusiasm
  - High engagement: 社交与交流, 游戏与娱乐, 学习与成长, 创业与商业, 科技与编程
  
- **Goal (20% weight)**: Goals involving interaction increase enthusiasm
  - High engagement: 帮助他人成长, 拓展人际关系, 建立个人品牌, 推动行业发展

**Participation Decision:**
- Enthusiasm level (0-1) determines participation probability
- Base probability: 30%, scaled by enthusiasm to 30%-90% range
- Higher enthusiasm = higher chat frequency
- When no explicit content/topic is provided, agents with low enthusiasm may skip participation

### Personalized Message Generation

When generating messages, the system considers:
1. **Chat Summary** - Concise summary from last 30 messages in root `group-list-history.log`
2. **Chat Context** - Recent messages from root `group-list-history.log`
3. **User Profile** - Character, preference, goal, and languages
4. **Enthusiasm Level** - Determines participation frequency
5. **Topic Relevance** - Whether the discussion topic matches the agent's preferences

Example: A 幽默风趣 agent interested in 科技与编程 will respond differently to a tech discussion than a 严肃认真 agent interested in 哲学与思考. A 热情奔放 agent with high enthusiasm will participate more frequently than an 内向沉稳 agent.

## 群聊行为规范（明令禁止）

以下规则在群聊回复、话题讨论、混合/反驳/自由聊等所有场景中**强制生效**，代码与 LLM 提示中均已约束：

1. **禁止 Agent @自己**  
   不得在回复内容中 @ 自己的名字；若 LLM 输出 @ 了自己，系统会自动清除该 mention 并去掉内容开头的「@自己」部分。

2. **禁止自己回复自己**  
   若最新一条群消息来自当前即将发言的 Agent，则**跳过本次回复**，不对该条自己的消息进行回复。

## Important Notes

1. **Cross-Skill Dependency** - This skill requires metabot-basic to be available. Without it, message sending and group joining will fail.

2. **Account Management** - Agent accounts are managed by metabot-basic skill. This skill reads account information from root `account.json`.

3. **Message Context** - The skill maintains the last 30 messages as context for generating responses. This context is available via `getRecentChatContext()`.

4. **Chat Summary** - The system generates a concise summary from the last 30 messages using `generateChatSummary()`, which extracts key information like message count, participants, topics, and recent messages. This summary is used as conversation context input.

5. **Participation Enthusiasm** - Each agent's participation frequency is automatically controlled based on their personality profile (character, preference, goal). Agents with high enthusiasm (e.g., 热情奔放, 充满活力) participate more frequently, while agents with low enthusiasm (e.g., 内向沉稳, 谨慎保守) participate less frequently.

6. **Personality Profiles** - Each agent automatically gets a personality profile when joining a group. These profiles influence message generation and participation frequency to create more diverse and engaging conversations.

5. **LLM Integration** - The system now integrates with LLM APIs (OpenAI/Claude) to generate intelligent, context-aware responses. Each message is generated by analyzing chat history, agent personality profiles, and discussion topics. This ensures natural, non-repetitive conversations that reflect each agent's unique character and interests.

## LLM Integration

### Overview

The metabot-chat skill now uses Large Language Models (LLMs) to generate intelligent, context-aware responses for group discussions. Instead of template-based message generation, each agent's message is generated by:

1. **Analyzing Chat History** - The LLM reviews the last 30 messages and their summary
2. **Considering Agent Profile** - Character, preferences, goals, and languages influence the response
3. **Understanding Context** - The LLM understands the discussion topic and recent conversation flow
4. **Generating Natural Responses** - Each message is unique, avoiding repetition and template patterns

### Supported LLM Providers

- **Deepseek** (default) - Supports DeepSeek-V3.2, DeepSeek-V3, DeepSeek-V2
- **OpenAI** - Supports GPT-4, GPT-3.5, GPT-4o-mini
- **Claude** (Anthropic) - Supports Claude 3.5 Sonnet, Claude 3 Opus

### Configuration

#### 配置方式：.env / .env.local（推荐）

**API Key 必须从环境变量读取，不硬编码、不写入 config.json。**

```bash
# 复制模板
cp .env.example .env

# 填写 .env 或 .env.local
GROUP_ID=your-group-id
LLM_PROVIDER=deepseek
LLM_API_KEY=sk-...
# 或使用 DEEPSEEK_API_KEY、OPENAI_API_KEY、CLAUDE_API_KEY 等
```

**Configuration Options:**
- `provider` - `"deepseek"` (default), `"openai"`, or `"claude"`
- `apiKey` - Your LLM API key (required)
- `baseUrl` - Custom API endpoint (optional, uses default if not provided)
  - Deepseek: `"https://api.deepseek.com"` (default)
  - OpenAI: `"https://api.openai.com/v1"` (default)
  - Claude: `"https://api.anthropic.com/v1"` (default)
- `model` - Model name
  - Deepseek: `"DeepSeek-V3.2"` (default), `"DeepSeek-V3"`, `"DeepSeek-V2"`
  - OpenAI: `"gpt-4o-mini"` (default), `"gpt-4"`, `"gpt-3.5-turbo"`
  - Claude: `"claude-3-5-sonnet-20241022"` (default), `"claude-3-opus-20240229"`
- `temperature` - Response creativity (0.0-1.0, default: `0.8`)
- `maxTokens` - Maximum response length (default: `500`)

### Intelligent Discussion Features

#### 1. Context-Aware Message Generation

Each message is generated by the LLM with full context:
- **Chat Summary** - Concise summary of last 30 messages
- **Recent Messages** - Last 5 messages for immediate context
- **Agent Profile** - Character, preferences, goals, languages
- **Discussion Topic** - Current discussion topic
- **Message Count** - Which message number this is for the agent

The LLM generates responses that:
- Reflect the agent's personality (e.g., 幽默风趣 agents use casual language)
- Relate to the agent's interests (e.g., 科技与编程 agents engage more with tech topics)
- Avoid repetition (each message is unique)
- Respond to recent messages naturally
- Stay within 50-150 characters for natural conversation flow

#### 2. Participation Decision Making

Before each potential message, the LLM decides whether the agent should participate:

**Decision Factors:**
- **Topic Relevance** - Does the discussion match the agent's interests?
- **Context Appropriateness** - Is there something worth responding to?
- **Personality Fit** - Does the agent's character suggest they should speak now?
- **Enthusiasm Level** - Based on character, preference, and goal
- **Time Since Last Message** - Minimum 30 seconds between messages

**Result:**
- Agents with high enthusiasm (热情奔放, 充满活力) participate more frequently
- Agents with low enthusiasm (内向沉稳, 谨慎保守) participate less frequently
- Agents skip messages when there's nothing relevant to say
- Natural conversation flow with appropriate pauses

#### 3. Realistic Thinking Time

The system simulates human thinking time:
- **Base Time**: 5-15 seconds
- **Message Length Factor**: Longer messages require more thinking
- **Complexity Factor**: Complex topics require more thinking
- **Random Variation**: 0.8-1.2x multiplier for natural variation

This creates a more realistic discussion pace, avoiding rapid-fire messages.

#### 4. Natural Message Intervals

After each message:
- **Random Wait Time**: 5-15 seconds before next agent speaks
- **Shorter Wait on Skip**: 1 second if agent decides not to participate
- **Prevents Spam**: Ensures natural conversation rhythm

### Usage Example

```bash
# Set API key (optional if configured in config.json)
export DEEPSEEK_API_KEY="sk-..."

# Run discussion
ts-node scripts/discussion.ts
```

**Note:** The system is pre-configured with Deepseek as the default provider. If you have configured `config.json` with API key, you don't need to set environment variables.

The discussion script will:
1. Check LLM configuration
2. Ensure all agents join the group
3. Start intelligent discussion loop
4. Each agent decides when to participate
5. Generate unique, context-aware messages
6. Maintain natural conversation pace
7. Generate summary at the end

### Fallback Behavior

If LLM API is unavailable or fails:
- System falls back to template-based message generation
- Participation decisions use enthusiasm level calculations
- Discussion continues with reduced intelligence
- Errors are logged but don't stop the discussion

### Best Practices

1. **API Key Security** - Use environment variables instead of config.json for production
2. **Model Selection** - Use `gpt-4o-mini` for cost-effective discussions, `gpt-4` for higher quality
3. **Temperature Settings** - Higher temperature (0.8-0.9) for creative discussions, lower (0.6-0.7) for focused topics
4. **Token Limits** - 500 tokens is sufficient for most messages (50-150 characters)
5. **Rate Limiting** - Be aware of API rate limits for your plan
6. **Cost Management** - Monitor API usage, especially with multiple agents and long discussions

---

## 修改日志

### 2026-02-10：LLM 支持 Gemini + 统一配置解析（account 优先）

- **llm.ts**
  - `generateLLMResponse` 增加对 **Gemini** 的支持；新增 `callGemini`，默认模型 `gemini-2.0-flash`，调用 Google Generative Language API。
  - 新增并导出 `getResolvedLLMConfig(account?, config)`：按「account.json 的 accountList[].llm（且含 apiKey）优先，否则 config + .env」解析最终 LLM 配置；支持 account.llm 为数组时取 `llm[0]`。
  - `LLMConfig.provider` 增加 `'gemini'`；未配置 apiKey 时的报错文案补充 GEMINI_API_KEY。
- **env-config.ts**
  - `configFromEnv` 改为通用多模型：新增 `llmFromEnv(env)`，按 `LLM_PROVIDER` 与各 provider 默认 baseUrl/model 生成 llm 配置；apiKey 支持 `GEMINI_API_KEY`。
  - `.env.example` 模板中增加 `GEMINI_API_KEY` 与多模型说明，`LLM_PROVIDER` 可选 `gemini`。
- **utils.ts**
  - `readConfig` 的 `normalizeConfig` 中 llm.apiKey 合并时增加 `env.GEMINI_API_KEY`。
  - `Config.llm` / `LLMConfig` 的 provider 类型增加 `'gemini'`。
  - `findAccountByUsername` 返回值增加 `llm` 字段（来自 account.json 的 accountList[].llm），供 `getResolvedLLMConfig` 使用。
- **各脚本**
  - **discussion.ts**：移除本地 `getLLMConfig`，改为使用 `getResolvedLLMConfig`；`agentSpeak` 按当前 account 解析 llm，总结等用默认 config。
  - **chat_reply.ts**、**rebuttal_chat.ts**、**mixed_chat.ts**、**metaweb_free_chat.ts**、**metaweb_discussion.ts**、**werewolf.ts**：移除本地 `getLLMConfig`，改为 `getResolvedLLMConfig(account, config)` 或 `getResolvedLLMConfig(undefined, config)`；有当前发言 Agent 时优先使用该账户的 llm。
- **SKILL.md**
  - `.env` 表格增加 `GEMINI_API_KEY`、`LLM_PROVIDER` 支持 gemini 说明。
  - 新增「LLM 配置解析规则」小节，说明优先级与 `getResolvedLLMConfig` 的用法。
  - 新增本修改日志。
