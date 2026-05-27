---
name: mcp-tester-hot-swap
description: "\"Hot-swap MCP server binary without disconnecting clients. 熱換MCP伺服器二進位，不斷客端連接。 Use when: hot swap mcp server, update mcp without restart, replace mcp binary, reload mcp server, live update mcp\""
disable-model-invocation: true
arguments: " - name: server-name description: Name of the server to hot-swap required: true - name: new-command description: New command to launch the updated server required: true"
---

# Hot-Swap MCP Server

熱換 MCP 伺服器，以新實作替換，不中斷客端。

## Instructions

1. 先以 `server_list` 查當前伺服器狀態，確認伺服器存在。

2. 以 `server_disconnect`，傳入：
   - `name`：{{server-name}}

   優雅斷連伺服器，同時保留工具登記。

3. 以 `server_reconnect`，傳入：
   - `name`：{{server-name}}
   - `command`：{{new-command}}

   連接至新伺服器實作。

4. 以 `server_list` 驗換成功，報告：
   - 工具是否仍可用
   - 可用工具之任何變動
   - 連線狀態

## Hot-Swap Workflow

實現快速開發，無需重啟除錯工作階段：

```
1. Make code changes to your MCP server
2. Build new binary: go build -o server-v2 ./cmd/server
3. /hot-swap myserver "./server-v2"
4. Continue testing - tool names remain the same!
```

## Why Hot-Swap?

- 無需重啟 MCP 客端（Claude Code 等）
- 工具名與前綴保持一致
- 迭代週期更快
- 即刻測試更動，無重連延遲
