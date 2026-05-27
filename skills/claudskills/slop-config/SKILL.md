---
name: slop-mcp-slop-config
description: "KDL config reference for slop-mcp scopes, manage_mcps params, auth, metadata. 配置格式、範圍、認證、元數據之參考。 Use when: registering servers, inspecting auth, understanding KDL format, checking scope behavior."
disable-model-invocation: true
---

# slop-mcp Configuration Reference

slop-mcp 以 KDL 格式存持久配置，分兩域。自 v0.14.0 起，slop-mcp 暴露 **9 meta-tools**（`manage_mcps`、`auth_mcp`、`get_metadata`、`search_tools`、`execute_tool`、`run_slop`、`slop_reference`、`slop_help`、`customize_tools`）。KDL 配置定 **哪些 MCP 存在**；保留內存域 `_slop.*`（由 `customize_tools` 管）定 **其工具如何呈現**。二層共存、互補。

## Config File Locations

| Scope | File | Purpose |
|-------|------|---------|
| User | `~/.config/slop-mcp/config.kdl` | 通用於所有項目 |
| Project | `.slop-mcp.kdl` (project root) | 僅限本項目 |

項目域配置疊加用戶域。同名 MCP 服務器，項目域優先。

## KDL Config Format

### Command-based MCP Server

```kdl
mcp "server-name" {
  command "npx"
  args "-y" "@namespace/package@latest" "mcp"
}
```

### Command with Environment Variables

```kdl
mcp "github" {
  command "npx"
  args "-y" "@modelcontextprotocol/server-github"
  env {
    GITHUB_TOKEN "${GITHUB_TOKEN}"
  }
}
```

### Local Binary

```kdl
mcp "my-server" {
  command "/usr/local/bin/my-mcp-server"
  args "--port" "3000"
}
```

### SSE or Streamable HTTP

```kdl
mcp "remote" type="sse" {
  url "https://mcp.example.com/sse"
}

mcp "streamable" type="streamable" {
  url "https://mcp.example.com/mcp"
}
```

### Dynamic Server (always re-fetch tools)

```kdl
mcp "evolving-server" dynamic=true {
  command "npx"
  args "-y" "@namespace/package@latest" "mcp"
}
```

## manage_mcps Parameters

`manage_mcps` 工具為服務器管理程序接口。

### Register

```
mcp__plugin_slop-mcp_slop-mcp__manage_mcps
  action: "register"
  name: "server-name"        # required, unique identifier
  type: "command"             # "command" (default), "sse", "streamable"
  command: "npx"              # executable (for command type)
  args: ["-y", "pkg", "mcp"] # command arguments
  url: "https://..."          # server URL (for sse/streamable)
  env: { "KEY": "val" }       # environment variables
  headers: { "K": "V" }      # HTTP headers (for sse/streamable)
  scope: "user"               # "memory" (default), "user", "project"
  dynamic: false              # true to always re-fetch tool list
```

### Unregister

```
mcp__plugin_slop-mcp_slop-mcp__manage_mcps
  action: "unregister"
  name: "server-name"
```

### Reconnect

```
mcp__plugin_slop-mcp_slop-mcp__manage_mcps
  action: "reconnect"
  name: "server-name"
```

### List All

```
mcp__plugin_slop-mcp_slop-mcp__manage_mcps
  action: "list"
```

### Status of One

```
mcp__plugin_slop-mcp_slop-mcp__manage_mcps
  action: "status"
  name: "server-name"
```

## Authentication

OAuth 所需服務器，執行登錄：

```
mcp__plugin_slop-mcp_slop-mcp__auth_mcp
  action: "login"
  name: "server-name"
```

查驗認證狀態：

```
mcp__plugin_slop-mcp_slop-mcp__auth_mcp
  action: "status"
  name: "server-name"
```

列所有已認證服務器：

```
mcp__plugin_slop-mcp_slop-mcp__auth_mcp
  action: "list"
```

## Metadata Inspection

取服務器工具元數據：

```
mcp__plugin_slop-mcp_slop-mcp__get_metadata
  mcp_name: "server-name"          # optional: filter to one server
  tool_name: "tool-name"           # optional: filter to one tool
  verbose: true                    # include full input schemas
  file_path: "/tmp/metadata.json"  # optional: write to file
```

## Scope Behavior

- **memory**: 僅存當次 slop-mcp 會話，宜用於測試。
- **user**: 寫入 `~/.config/slop-mcp/config.kdl`，重啟存，全項目可用。
- **project**: 寫入當前目錄之 `.slop-mcp.kdl`，重啟存，僅本項目可用。

啟動時三域合併。用 `manage_mcps` `action: "list"` 觀合併結果。

## Customization Scopes

KDL 域管註冊之 MCP。`customize_tools`（第九元工具）將覆蓋與自定義工具寫入獨立之 **memory-layer scopes**，各域一組 `_slop.*` JSON 文件。此域與 KDL 域正交：KDL 定 MCP 存在與否，memory `_slop.*` 定其工具描述與 `_custom` 工具如何出現。

| Scope | Directory | Files | Commit Policy |
|-------|-----------|-------|---------------|
| user | `~/.config/slop-mcp/memory/_slop/` | `_slop.overrides.json`, `_slop.tools.json` | NOT committed; personal to this machine/user |
| project | `<repo>/.slop-mcp/memory/_slop/` | `_slop.overrides.json`, `_slop.tools.json` | COMMITTED; team-shared baseline |
| local | `<repo>/.slop-mcp/memory.local/_slop/` | `_slop.overrides.json`, `_slop.tools.json` | gitignored; per-developer within-repo |

**Precedence**: `local > project > user`。同一 `(mcp, tool)` 覆蓋或同一 `_custom` 工具名，本地覆蓋倉庫、倉庫覆蓋用戶。

調用 `customize_tools` 時以 `scope` 參數選域（默認 `project`）；導出 `action: "export"` 與導入 `action: "import"` 亦按域操作，便於團隊共享定制包。

## Reserved `_slop.*` Banks

保留內存 bank `_slop.*`（具體為 `_slop.overrides`、`_slop.tools`）之寫路徑受限：

- **寫屏障**：`mem_save`、`mem_delete`、以及 `memory-cli` 對 `_slop.*` bank 之寫入請求一律拒絕。
- **讀允許**：自定義工具之 SLOP body 可以 `mem_get`（及同等讀取原語）讀取 `_slop.*`，用以自省已定義之覆蓋或工具。
- **唯一寫路徑**：所有寫入須通過 `customize_tools` 元工具（`set_override` / `remove_override` / `define_custom` / `remove_custom` / `import` 等操作），以維持元數據一致、域路由正確、包格式可逆。

詳見 `tool-customization` 技能之 action 表與 `memory-system` 技能之保留域語義。

## Cross-references

- Invoke the `Skill` tool with `skill: slop-mcp:tool-customization` — `customize_tools` 元工具之八操作、包導出導入、staleness 檢測。
- Invoke the `Skill` tool with `skill: slop-mcp:memory-system` — 持久內存兩層、保留 `_slop.*` 之寫屏障語義、memory-cli 互操作。
- Invoke the `Skill` tool with `skill: slop-mcp:discovery-first` — 調 `execute_tool` 前先經 `get_metadata` / `search_tools` 之強制發現流程。
- `mcp-orchestrator` agent — Workflow 6「Customize Tool Descriptions」將本技能之域與寫路徑規則接入完整協調流程。
