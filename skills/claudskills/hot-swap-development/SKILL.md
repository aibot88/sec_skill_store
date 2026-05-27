---
name: mcp-tester-hot-swap-development
description: "Iterative MCP server replacement without client restart or session loss. 熱換伺服器，不斷客端，不失狀態。 Use when: developing MCP servers iteratively, replacing server binary mid-session, avoiding reconnection overhead."
disable-model-invocation: true
---

# Hot-Swap MCP Development Workflow

引導開發者行熱換工作流，以 mcp-debug 為器。

## Overview

熱換開發，替換 MCP 伺服器實作，無須：
- 重啟 Claude Code 或他 MCP 客端
- 丟棄除錯歷史
- 更改工具名或前綴

## The Problem

舊式 MCP 開發流程：
1. 改程式碼
2. 重建伺服器
3. 重啟伺服器
4. 重連客端
5. 復原狀態
6. 測試更動
7. 往復...

每輪迭代耗時於重連與狀態復原。

## The Solution

mcp-debug 開熱換之道：
1. 改程式碼
2. 重建伺服器
3. 呼叫 `server_disconnect` 繼以 `server_reconnect`
4. 即刻測試

客端持連，狀態保全。

## Workflow Steps

### 1. Initial Setup

先加入開發伺服器：

```
Use server_add tool:
- name: "myserver"
- command: "go run ./cmd/server" (or your dev command)
```

### 2. Development Cycle

每改程式碼後：

1. **建新版本**
   ```bash
   go build -o ./bin/server-v2 ./cmd/server
   # or: npm run build
   # or: cargo build --release
   ```

2. **斷當前伺服器**
   ```
   Use server_disconnect tool:
   - name: "myserver"
   ```
   工具仍登記，呼叫暫佇。

3. **以新執行檔重連**
   ```
   Use server_reconnect tool:
   - name: "myserver"
   - command: "./bin/server-v2"
   ```

4. **驗工具可用**
   ```
   Use server_list tool to confirm connection
   Test a tool to verify functionality
   ```

### 3. Debugging Changes

以除錯工具驗行為：

- `debug_logs` — 檢視請求/回應流量
- `debug_status` — 查連線健康
- `schema_validate` — 驗模式更動

## Server Management Tools

### server_add

動態加入新伺服器：
```
server_add with:
- name: "myserver"
- command: "python server.py"
```

### server_disconnect

暫停伺服器（工具仍登記）：
```
server_disconnect with:
- name: "myserver"
```

### server_reconnect

以新執行檔重連：
```
server_reconnect with:
- name: "myserver"
- command: "./new-binary"
```

### server_list

列所有伺服器及狀態：
```
server_list
```

### server_remove

完全移除伺服器：
```
server_remove with:
- name: "myserver"
```

## Workflow Patterns

### Pattern 1: Watch and Rebuild

```bash
# Terminal 1: Watch and rebuild
watchexec -e go -- go build -o bin/myserver ./cmd/server

# In Claude Code: After each rebuild
# Call server_disconnect then server_reconnect
```

### Pattern 2: A/B Testing

1. 測版本 A
2. 以 server_reconnect 熱換至版本 B
3. 測版本 B
4. 以 debug_logs 比對行為

### Pattern 3: Debug Mode Toggle

```
# Normal mode
server_reconnect with command="./server"

# Debug mode with extra logging
server_reconnect with command="./server --debug --verbose"
```

## Best Practices

1. **用版本化執行檔** — 命名含版本，便於回滾
2. **換後查日誌** — 驗無流量錯誤
3. **先測關鍵工具** — 確認核心功能
4. **保留前版執行檔** — 問題時快速回滾

## Troubleshooting

**伺服器不重連：**
- 查命令路徑正確否
- 驗執行檔有執行權限
- 查有無埠衝突（若用網路）

**換後工具消失：**
- 伺服器或已更改工具定義
- 以 `server_list` 查現有工具
- 查伺服器日誌中初始化錯誤

**意外行為：**
- 以 `debug_logs` 比對換前換後請求
- 驗模式未作不相容更改
