---
name: slop-mcp-slop-monitor
description: "Scaffold slop-mcp monitor session — verify PATH binary, choose generic event stream / SLOP polling script / timed session, emit copy-ready Claude Code Monitor({...}) JSON. 搭建 slop-mcp 監視會話。 Use when: starting Claude Code Monitor over slop-mcp, watching git/build/CI events, polling MCP for delta changes, running bounded watch session."
disable-model-invocation: true
---

# Start Slop Monitor

對 `slop-mcp monitor` + `message` 子命令之命令級包裝。本命令不直接調 MCP 元工具 — 而是引導用戶：(a) 確認二進製可達，(b) 擇模式，(c) 拷貝對應 `Monitor({...})` JSON 入 Claude Code 會話。所選腳本內若含 MCP 調用，仍須遵發現先於執行。

## Steps

### Step 0 — Verify `slop-mcp` Binary in PATH (Precondition)

`monitor` 與 `message` 為獨立子命令，**不依賴運行中之 MCP server**，但二進製須在 `PATH`。先運行：

```bash
command -v slop-mcp
```

或 `which slop-mcp`。

- **若返回路徑**（例：`/usr/local/bin/slop-mcp`）→ 進 Step 1。
- **若返回非零退出 / 空輸出** → 停止並告用戶安裝：
  - `make install` — 由上游倉 `~/work/mcps/slop-mcp` 源碼編入 `$GOPATH/bin`，需 `$GOPATH/bin` 在 `PATH`。
  - `npm i -g @standardbeagle/slop-mcp` — 自 npm 全局裝 wrapper。
  - 安裝後重跑 `command -v slop-mcp` 確認，再進 Step 1。

### Step 1 — Choose Mode

詢問用戶意圖，匹配三模式之一：

| Mode 模式 | When 何時 | Source 事件源 |
|-----------|-----------|---------------|
| **A — Generic event stream** 通用事件流 | 由外部源（git hook、build 腳本、CI、file watcher）以 `slop-mcp message "..."` 推送 | shell-driven，monitor 純中繼 |
| **B — SLOP polling script** SLOP 輪詢腳本 | 須輪詢 MCP 工具或 HTTP 端點，按間隔比對 delta | monitor 腳本身體內循環 + `print()` |
| **C — Timed session** 限時會話 | 限定窗口（如部署期、構建期）後自退 | 任一源 + `--timeout=<秒>` |

模式可組合 — Mode A + Mode C 為「限時通用流」，Mode B + Mode C 為「限時輪詢」。

### Step 2 — Build the Command Line

按所選模式組裝 shell 命令：

**Mode A — Generic event stream**：

```bash
slop-mcp monitor
```

外部源以 `slop-mcp message "<text>"` 向同用戶上下文之尾文件追加事件。常見配對：

```bash
# .git/hooks/post-commit
HASH=$(git log -1 --pretty=format:'%h')
slop-mcp message "commit $HASH"
```

或一行鏈：`make build && slop-mcp message "build ok" || slop-mcp message "build failed"`。

**Mode B — SLOP polling script**：

兩種寫法擇一。Inline 適短腳本，文件適長腳本與重用。

```bash
# Inline via -e
slop-mcp monitor -e 'for _ in range(999999999):
    h = myapi.get_health()
    if changed("health", h):
        print("health: " + str(h))
    sleep(30000)'

# Script file
slop-mcp monitor watch-health.slop
```

**前提**：腳本身體內若引 `execute_tool("<mcp>", "<tool>", ...)` 或縮寫 `myapi.get_health()` 形式，所引 MCP/工具須先經元工具驗證 — 詳見 `slop-mcp:discovery-first`。憑記憶填 MCP 名屬禁則。

**Mode C — Timed session**：

```bash
# 自退於 600 秒（10 分鐘）
slop-mcp monitor --timeout=600

# 與 Mode A 組合：限時通用流
slop-mcp monitor --timeout=600

# 與 Mode B 組合：限時輪詢
slop-mcp monitor --timeout=600 watch-health.slop
```

### Step 3 — Emit Claude Code Monitor JSON

按所選模式輸出對應 `Monitor({...})` 塊供用戶拷貝至 Claude Code 會話。**關鍵規則**：`timeout_ms` 須寬於 `--timeout` 秒數對應毫秒（推薦 +60s 緩衝），令 slop-mcp 自退而非被 Monitor 工具強砍。

**Mode A — Generic event stream**：

```javascript
Monitor({
  command: "slop-mcp monitor",
  description: "dev events",
  persistent: true
})
```

**Mode B — SLOP polling script**：

```javascript
Monitor({
  command: "slop-mcp monitor watch-health.slop",
  description: "service health",
  persistent: true
})
```

或 inline 變體 — 用 `-e` 內聯腳本（注意外層雙引號內之單引號）：

```javascript
Monitor({
  command: "slop-mcp monitor -e 'for _ in range(999999999):\n    h = myapi.get_health()\n    if changed(\"health\", h):\n        print(\"health: \" + str(h))\n    sleep(30000)'",
  description: "service health (inline)",
  persistent: true
})
```

**Mode C — Timed session**：

```javascript
Monitor({
  command: "slop-mcp monitor --timeout=600",
  description: "build window",
  timeout_ms: 660000
})
```

組合（B+C）：

```javascript
Monitor({
  command: "slop-mcp monitor --timeout=600 watch-health.slop",
  description: "timed health poll",
  timeout_ms: 660000
})
```

`persistent: true` 令 Monitor 跨對話回合存活；限時模式通常省 `persistent` 或設 `false`，因 `--timeout` 已界定生命。

### Step 4 — Confirm and Hand Off

向用戶呈現：
1. 已選模式（A / B / C 或組合）。
2. shell 命令（如本地測試需要）。
3. `Monitor({...})` JSON 塊（拷貝目標）。
4. 對 Mode B：腳本內 MCP 名與工具名是否已 Step 0-style 驗證之提醒。
5. 對 Mode C：`--timeout=<N>` 與 `timeout_ms=<N*1000+60000>` 對應關係之說明。

## Examples

### Generic stream + git hook 通用流配 git hook

```bash
# 終端啟動
slop-mcp monitor

# .git/hooks/post-commit 推送
slop-mcp message "commit $(git log -1 --pretty=format:'%h: %s')"
```

```javascript
Monitor({
  command: "slop-mcp monitor",
  description: "git events",
  persistent: true
})
```

### SLOP poll multi-MCP with persistent state SLOP 多源輪詢含跨重啟狀態

```python
# watch-multi.slop
last_issues = mem_load("monitor", "issue_count", 0)

for _ in range(999999999):
    issues = github.list_issues(state: "open")
    n = len(issues)
    if n != last_issues:
        print("open issues: " + str(n))
        last_issues = n
        mem_save("monitor", "issue_count", n)

    h = api.get_health()
    if changed("api_health", h["status"]):
        print("api: " + str(h["status"]))

    sleep(30000)
```

```javascript
Monitor({
  command: "slop-mcp monitor watch-multi.slop",
  description: "github + api health",
  persistent: true
})
```

腳本內 `github.list_issues` 與 `api.get_health` 之 MCP 名須會話內已 `manage_mcps list` / `get_metadata` 驗證 — 見 `slop-mcp:discovery-first`。

### Timed deploy window 限時部署窗口

```javascript
Monitor({
  command: "slop-mcp monitor --timeout=900",
  description: "deploy window 15min",
  timeout_ms: 960000
})
```

期間以 `slop-mcp message "deploy: <step>"` 由 CD 腳本或人手推進。

## Forbidden 禁則

1. **跳過 PATH 驗證** — `command -v slop-mcp` 未確認即輸出 `Monitor({...})` 塊，將致 Claude Code 報二進製不存在。Step 0 不可省。
2. **`timeout_ms` 短於 `--timeout` 對應毫秒** — 例 `--timeout=600` 配 `timeout_ms: 60000` 將令 Monitor 工具於 60 秒強砍 slop-mcp，違限時自退語義。`timeout_ms` 須 ≥ `--timeout * 1000 + 60000` 緩衝。
3. **Mode B 腳本含未驗證之 `execute_tool` / MCP 縮寫調用** — 腳本身體內 `execute_tool("<mcp>", "<tool>", ...)` 或 `myapi.foo()` 形式所引 MCP/工具，須會話內已 `manage_mcps list` + `get_metadata verbose:true` 驗證。憑記憶填屬發現先於執行之違規 — 詳見 `slop-mcp:discovery-first`。
4. **Bash 直呼上游 MCP 二進製繞 slop-mcp** — `npx @pkg/foo mcp ...` / `uvx <pkg> mcp` / heredoc 管道注入 MCP 進程 stdin 皆禁。一切 MCP 調用經 slop-mcp 路由。

違規恢復：停止當前動作 → 補 Step 0 PATH 驗證或補 MCP 元工具發現 → 以驗證後參數重發 `Monitor({...})` 塊。

## Related

- Invoke the `Skill` tool with `skill: slop-mcp:event-monitoring` — 完整 monitor + message 子命令參考、四調用形式、`changed()` delta 檢測、`mem_save` / `mem_load` 跨重啟狀態、四事件源 shell 模式（git hook / build / test / 文件監視 Linux+macOS）、recipe 引用 `monitor_poll_delta` 與 `monitor_multi_check`。
- Invoke the `Skill` tool with `skill: slop-mcp:discovery-first` — Mode B 腳本身體內 `execute_tool` 或 MCP 縮寫調用前之元工具強制流程、禁則表、恢復路徑。
- Invoke the `Skill` tool with `skill: slop-mcp:scripting` — SLOP 語言參考，monitor 腳本身體語法同 `run_slop` 腳本；64 KB 身體上限、16 幀遞歸、`print()` 行即通知。
- Invoke the `Skill` tool with `skill: slop-mcp:memory-system` — `mem_save` / `mem_load` 跨進程重啟之持久內存細節、bank 元數據、保留 `_slop.*` 命名空間。
- `/slop-list` — 列已注冊 MCP 服務器，Mode B 腳本所引 MCP 名之驗證入口。
- `/slop-search` — 跨服務器關鍵字搜工具，Mode B 腳本所調工具名之驗證入口。
- `mcp-orchestrator` 代理 — Workflow 7「Set Up Event Monitor」之協調者級調用，含腳本身體內 MCP 調用之發現要求。
