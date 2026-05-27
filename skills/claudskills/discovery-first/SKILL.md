---
name: slop-mcp-discovery-first
description: "Force MCP discovery via get_metadata or search_tools before any execute_tool call. 調用前必先經 slop-mcp 元工具發現，禁直呼 MCP 二進製。 Use when: user names MCP server, user asks to call MCP tool, user asks to run MCP command, agent about to invoke execute_tool, agent about to shell out to MCP binary."
disable-model-invocation: true
---

# Discovery-First Protocol

此技能強制任何 MCP 工具調用前，先經 slop-mcp 元工具查驗。目的：禁止繞道 bash 直呼 MCP 二進製，禁止憑猜測調用未驗證之 schema。

> 核心原則：未經元工具確認之 `mcp_name`、`tool_name`、參數 schema — 皆不可信。Fail fast, verify first.

## Use When

觸發本技能之情境：

- 用戶以名稱提及 MCP 服務器（例：「用 github 服務器」、「跑 filesystem 的 read_file」）
- 用戶要求調用某工具但未給 schema
- 用戶要求執行某 MCP 命令
- 代理即將調用 `execute_tool`
- 代理即將 `bash` 調用 `npx @xxx/... mcp ...` 或類似 MCP 二進製
- 代理即將將數據 `echo` 管道至 MCP 進程

## Mandatory Flow

每次 MCP 工具調用前，按順序執行以下檢查。**跳步即違規。**

### (1) Server Name Unverified → List Servers

若本會話中未以元工具確認服務器存在：

```
mcp__plugin_slop-mcp_slop-mcp__manage_mcps
  action: "list"
```

返回所有已注冊服務器及其連接狀態。若目標服務器不在列表，應注冊（見 `slop-config` 技能）而非直呼二進製。

### (2) Server Known, Tools Not Enumerated → Get Metadata

若服務器已知但未列其工具：

```
mcp__plugin_slop-mcp_slop-mcp__get_metadata
  mcp_name: "<server>"
```

返回該服務器之工具清單。記錄此會話已枚舉之服務器。

### (3) Tool Name Known, Schema Unverified → Get Verbose Metadata

即使工具名稱熟悉，**本會話中未見 schema 者，即為未驗證**：

```
mcp__plugin_slop-mcp_slop-mcp__get_metadata
  mcp_name: "<server>"
  tool_name: "<tool>"
  verbose: true
```

返回完整 input schema — 參數名、類型、必填與否、描述。上游 schema 可能已變，此步不得省。

### (4) Then and Only Then → Execute

schema 確認後，方可調用：

```
mcp__plugin_slop-mcp_slop-mcp__execute_tool
  mcp_name: "<server>"
  tool_name: "<tool>"
  parameters: { ... }   # keys match verified schema exactly
```

> **Parameter field is `parameters`, not `arguments`.** See [Common Errors](#common-errors) below.

### Alternative: Capability Discovery → Search Tools

若目標為能力探索（尚不知用哪工具）：

```
mcp__plugin_slop-mcp_slop-mcp__search_tools
  query: "<keywords>"
```

選中候選後，仍須執行步驟 (3) 驗證 schema，再執行 (4)。

## DENY List

以下行為 **禁止**，遇之即停並改用元工具：

1. **直呼 MCP 二進製** — `bash` 調用 `npx @xxx/pkg mcp ...`、`uvx <pkg> mcp`、或任何 `<mcp-binary> mcp` 形式繞過 slop-mcp 者。
2. **Echo-pipe 注入** — `echo '{...}' | <mcp-binary>`、`printf ... | npx ...` 或 heredoc 至 MCP 進程之 stdin。
3. **猜測參數名** — 未見元工具返回之 schema 前，不得憑「通常叫 path」、「大概是 query」臆造鍵名。
4. **未驗證 execute_tool** — 本會話中 `mcp_name` 或 `tool_name` 未經 `manage_mcps list` / `get_metadata` 返回確認，即禁調 `execute_tool`。
5. **跳過 verbose schema 檢查** — 即使工具名在列表中，`verbose: true` 未執行則參數結構未知，禁憑記憶調用。
6. **跨會話記憶假設** — 上次會話見過之 schema 不等於此次有效；每會話重新驗證。

## Good vs Bad

### Pair 1 — User asks to read a file via filesystem server

**Bad**（直呼二進製）：

```bash
npx -y @modelcontextprotocol/server-filesystem mcp <<'EOF'
{"method":"tools/call","params":{"name":"read_file","arguments":{"path":"/etc/hosts"}}}
EOF
```

**Good**（經元工具）：

```
# (1) 若需要：manage_mcps action:"list" 確認 filesystem 已注冊
# (2) get_metadata mcp_name:"filesystem" tool_name:"read_file" verbose:true
# (3) 根據返回之 schema：
mcp__plugin_slop-mcp_slop-mcp__execute_tool
  mcp_name: "filesystem"
  tool_name: "read_file"
  parameters: { "path": "/etc/hosts" }
```

### Pair 2 — User: "用 github 服務器開 issue"

**Bad**（憑記憶猜參數）：

```
mcp__plugin_slop-mcp_slop-mcp__execute_tool
  mcp_name: "github"
  tool_name: "create_issue"
  parameters: { "repo": "owner/name", "title": "Bug", "body": "..." }
# 未驗證 schema — 參數鍵名可能為 "repository" 或 "owner"+"name" 分離
```

**Good**（先驗 schema）：

```
mcp__plugin_slop-mcp_slop-mcp__get_metadata
  mcp_name: "github"
  tool_name: "create_issue"
  verbose: true
# 讀 schema，得確切鍵名與必填項，再調 execute_tool
```

### Pair 3 — User: "找個能解析 PDF 的工具"

**Bad**（假定存在並直呼）：

```bash
npx -y some-pdf-mcp mcp
```

**Good**（能力發現 → schema 驗證 → 執行）：

```
# (a) search_tools query:"pdf parse extract"
# (b) 選候選後：get_metadata mcp_name:"<chosen>" tool_name:"<tool>" verbose:true
# (c) execute_tool with verified arguments
```

## Recovery

若已違規（已 shell 出或已盲調 execute_tool 失敗）：

1. 停止。
2. 執行步驟 (1) → (3) 補足發現。
3. 以驗證後之 schema 重試。
4. 將違規模式記入本會話筆記，勿復蹈。

## Common Errors

These wrong-key mistakes silently drop the payload in naive validators; `execute_tool` rejects them with a hint naming the correct field.

| Wrong | Right | Symptom when wrong |
|-------|-------|--------------------|
| `arguments: {...}` ❌ | `parameters: {...}` ✅ | Tool runs with empty params, returns generic "missing required field" from downstream MCP |
| `args: {...}` ❌ | `parameters: {...}` ✅ | Same as above |
| `input: {...}` ❌ | `parameters: {...}` ✅ | Same as above |
| `js: "..."` ❌ | `code: "..."` ✅ | JS-exec tools reject `js`; schema uses `code` |
| `last: N` ❌ | `limit: N` ✅ | Log/list tools ignore `last` silently; `limit` is canonical |

If `execute_tool` replies `unexpected field "arguments" -- execute_tool expects 'parameters'`, rewrap the payload under the `parameters` key — do not retry with the same shape.

## Related

- `/slop-search` — 跨服務器關鍵字搜索工具（步驟「Alternative」之命令形式）。
- `/slop-list` — 列已注冊服務器（步驟 (1) 之命令形式）。
- Invoke the `Skill` tool with `skill: slop-mcp:slop-config` — KDL 配置、`manage_mcps` 參數、元數據檢查詳解。
- Invoke the `Skill` tool with `skill: slop-mcp:scripting` — 多工具編排經 `run_slop`，發現仍須先行。
- `mcp-orchestrator` 代理 — 注冊/發現/執行/排障之完整協調者。
