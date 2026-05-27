---
name: slop-mcp-scripting
description: "SLOP scripting language for automating multi-MCP workflows via run_slop, authoring custom tool bodies, calling memory primitives from scripts. SLOP 腳本語言。 Use when: writing inline scripts, running .slop files, chaining MCP tool calls, exploring built-in functions, authoring custom_tool body, mem_save/mem_load from SLOP, emit return value, pipe transforms."
disable-model-invocation: true
---

# SLOP Scripting Guide

SLOP 語言令多工具工作流跨所有已注冊 MCP 服務器自動化。腳本經 `run_slop` 工具運行，亦作 `customize_tools` 所定義之自定義工具 body，可訪問每個已注冊 MCP 及持久記憶層。

## Running Scripts

### Inline Script

```
mcp__plugin_slop-mcp_slop-mcp__run_slop
  script: "tools.list()"
```

### Script File

```
mcp__plugin_slop-mcp_slop-mcp__run_slop
  file_path: "/path/to/script.slop"
```

## SLOP Language Basics

SLOP 為腳本語言，內置數據操作、字串處理及 MCP 工具執行函數。

### Exploring Built-in Functions

列函數類別：

```
mcp__plugin_slop-mcp_slop-mcp__slop_reference
  list_categories: true
```

Categories: math, string, list, map, random, type, json, regex, time, encoding, functional, crypto, slop.

搜索函數：

```
mcp__plugin_slop-mcp_slop-mcp__slop_reference
  query: "split"
  verbose: true
```

取單個函數詳情：

```
mcp__plugin_slop-mcp_slop-mcp__slop_help
  name: "map"
```

### Calling MCP Tools from SLOP

SLOP 腳本可調用任何已注冊 MCP 服務器上的任何工具。確切語法取決於 SLOP 運行時中工具的暴露方式。用 `slop_reference` 加 `category: "slop"` 查 MCP 集成函數：

```
mcp__plugin_slop-mcp_slop-mcp__slop_reference
  category: "slop"
  verbose: true
```

### Example: Sequential Workflow

```python
// Read a file, process it, write the result
content = tools.call("filesystem", "read_file", { "path": "input.txt" })
lines = split(content, "\n")
filtered = filter(lines, fn(line) { contains(line, "TODO") })
result = join(filtered, "\n")
tools.call("filesystem", "write_file", { "path": "todos.txt", "content": result })
```

### Example: Search and Aggregate

```python
// Search across multiple servers
results = tools.call("lci", "search", { "query": "error handling" })
count = len(results)
print("Found " + str(count) + " matches")
```

### Example: Data Processing Pipeline

```python
// Use built-in functions for data transformation
data = json_parse(tools.call("filesystem", "read_file", { "path": "data.json" }))
names = map(data, fn(item) { item.name })
sorted = sort(names)
json_stringify(sorted)
```

## Built-in Function Reference

以下工具探索完整標準庫：

| Tool | Purpose |
|------|---------|
| `slop_reference` with `list_categories: true` | 查所有函數類別 |
| `slop_reference` with `query: "..."` | 按名稱/描述搜索函數 |
| `slop_reference` with `category: "string"` | 列某類別函數 |
| `slop_help` with `name: "fn_name"` | 單個函數完整文檔 |

### Common Categories

- **string**: split, join, trim, replace, contains, starts_with, ends_with, upper, lower
- **list**: map, filter, reduce, sort, reverse, flatten, unique, zip
- **map**: keys, values, entries, merge, get, set
- **json**: json_parse, json_stringify
- **regex**: regex_match, regex_replace, regex_find
- **time**: now, format_time, parse_time
- **type**: type_of, to_string, to_number, to_bool
- **functional**: map, filter, reduce, compose, pipe

## Script Files

存腳本為 `.slop` 文件，以 `run_slop` 運行：

```
mcp__plugin_slop-mcp_slop-mcp__run_slop
  file_path: "./scripts/my-workflow.slop"
```

腳本最終表達式值作為結果返回。

## Custom Tool Bodies

自定義工具 body 為 SLOP 腳本，由 `customize_tools` 之 `define_custom` action 保存、於 `execute_tool` 調用該自定義工具時運行。輸入驗證後入 `args` map；最終表達式（或 `emit(...)` 輸出）作為返回值。上游 MCP 工具不變 — 自定義工具僅為 SLOP 腳本包裝層，可組合多 MCP 調用為單一暴露工具。

### Syntax Rules

- **No `$`-prefixed variables.** 變量為純標識符：`doc`, `pages`, `result`。與某些 SLOP 方言不同，此處無 `$` 前綴。
- **Map/object field access uses bracket notation:** `args["file_key"]`, `page["name"]`。無點式 `args.file_key`。
- **Pipe operator `|` chains transforms:** `items | filter(|x| x["active"]) | map(|x| x["name"])`。管道將左值作為首參傳入右函數。
- **Anonymous functions use `|param|` syntax:** `map(list, |item| item["id"])`。body 為單表達式，自動返回。
- **`emit(named: value, other: ...)`** 設命名輸出字段；省略 `emit` 則最後求值表達式為返回值。一 body 內僅一種模式。
- **`execute_tool(mcp, tool, args_map)`** 於 body 內可調用 — 此乃自定義工具組合其他 MCP 之機制。返回值為該工具之完整響應 map。
- **Scalar shorthand binding with name collision is silently skipped.** 綁頂層變量與 SLOP 內置同名者（`map`, `len`, `filter`, ...）遭跳過並記警告。如需 `args` 內 `map` 字段，直接以 `args["map"]` 訪問，勿作 `map = args["map"]` 綁定。

### Resource Limits

- **Body size cap 64 KB** by default. 超限則 `define_custom` 拒受。環境變量 `SLOP_MAX_CUSTOM_BODY` 可提升（例如 `SLOP_MAX_CUSTOM_BODY=131072` 設 128 KB）。body 大於上限者應存為 recipe 文件，以 `run_slop recipe:"<name>"` 調用而非塞入 `define_custom`。
- **Recursion depth guard 16 frames.** 自定義工具可調其他自定義工具，但調用棧深過 16 frames 者返 `ErrCustomToolRecursion` — 為已知錯誤，非堆棧溢出。互遞歸兩工具超過此限亦觸發。

### Example: Composite Body Calling Two MCPs

拉 GitHub 開放 issue，附帶 lci 倉庫統計：

```python
// args: {repo: "owner/name"}
issues = execute_tool("github", "list_issues", {repo: args["repo"], state: "open"})
stats = execute_tool("lci", "stats", {path: args["repo"]})
titles = issues | map(|i| i["title"])
emit(
    count: len(issues),
    titles: titles,
    symbols: stats["symbol_count"]
)
```

`execute_tool` 兩次分別拉 github 與 lci；管道提取 title；`emit` 構造結構化返回值。代理調此自定義工具只見 `{repo}` 單參 schema，不見 github/lci 細節。

## Memory Access from SLOP

持久記憶 `mem_*` 函數於任何 `run_slop` 腳本內皆可調，自定義工具 body 內亦可。腳本藉此存 last-seen 游標、緩存昂貴查詢、或為 monitor 腳本保存跨進程狀態。詳見 `memory-system` 技能。

### mem_save(bank, key, value, description:, schema:)

存值至 `~/.config/slop-mcp/memory/<bank>.json` 之 bank/key。`description:` 與 `schema:` 為可選 kwargs — 省略者**保留既有元數據不變**（非破壞性更新）。`size` 字段自動計算為序列化字節數，無須傳入。

```python
// 首次保存寫全元數據
mem_save("monitor", "last_commit", "abc123",
         description: "Last seen HEAD sha from poll-git.slop",
         schema: "string")

// 後續更新僅傳值，元數據保留
mem_save("monitor", "last_commit", "def456")
```

### mem_load(bank, key, default_value)

取值，鍵缺則返 `default_value` — 不拋異常。首次運行無狀態時用此平滑啟動：

```python
last = mem_load("monitor", "last_commit", "")
if last == "":
    print("first run")
```

### Discovery Primitives

三函數為零成本探查 — 不加載值即可查元數據。用於自定義工具 body 判斷既存狀態、或於腳本中列 bank 內容：

- `mem_info(bank, key)` — 返單條目之 `description` / `schema` / `size` / `created_at` / `updated_at` map，**不含值**。探大 blob 元數據而不付加載代價。
- `mem_list(bank, pattern: "")` — 列 bank 全部條目元數據。可選 glob `pattern` 過濾鍵名；輸出按鍵排序。
- `mem_search(query, bank: "", include_values: false)` — 跨 bank（或單 bank 若傳 `bank:`）大小寫不敏感子串搜索，匹配鍵名與描述。`include_values: true` 時亦搜索序列化值內容。

```python
// 探 monitor bank 全部 last_* 游標
for e in mem_list("monitor", pattern: "last_*"):
    print(e["key"] + " (" + e["description"] + ")")
```

詳見 `memory-system` 技能。

### Reserved `_slop.*` Banks

以 `_slop.` 開頭之 bank 名為 slop-mcp 定制層保留。自定義工具 body 內可以 `mem_get` **讀取** `_slop.*`（例如查既有覆蓋），但 `mem_save` / `mem_delete` 寫入 `_slop.*` 遭拒。寫路徑強制經 `customize_tools` 元工具 — 其在正確 scope 下更新覆蓋索引、刷新上游 schema 哈希、觸發 stale 檢測。

### Example: Counter with Description

載計數器、遞增、保存。首次保存附描述，後續更新僅傳值：

```python
count = mem_load("stats", "page_views", 0)
count = count + 1
if count == 1:
    mem_save("stats", "page_views", count,
             description: "Total landing page visits observed by tracker.slop",
             schema: "integer")
else:
    mem_save("stats", "page_views", count)
print("views: " + str(count))
```

第二分支省 kwargs — 既有 `description` / `schema` / `created_at` 原封不動，僅 `updated_at` 與 `size` 刷新。

## Practical Patterns

### Tool Discovery Script

```python
// Find all file-related tools
tools.search("file")
```

### Multi-Server Coordination

```python
// Get data from one server, process with another
raw = tools.call("api-server", "fetch_data", { "endpoint": "/users" })
parsed = json_parse(raw)
tools.call("filesystem", "write_file", {
  "path": "users.json",
  "content": json_stringify(parsed, 2)
})
```

### Error Handling

SLOP 腳本應處理 MCP 工具調用錯誤。查 SLOP 參考中錯誤處理構造：

```
mcp__plugin_slop-mcp_slop-mcp__slop_reference
  query: "error"
  verbose: true
```

## Cross-references

- Invoke the `Skill` tool with `skill: slop-mcp:tool-customization` — `customize_tools` 元工具之 canonical reference，含 8 actions、3 scope 精度表、pack 導出/導入、staleness 檢測。自定義工具 body 之宿主。
- Invoke the `Skill` tool with `skill: slop-mcp:memory-system` — 雙層記憶深度指南：會話 `store_*` 與持久 `mem_*`、元數據 / 發現原語、memory-cli 互操作、`_slop.*` 寫屏障。
- Invoke the `Skill` tool with `skill: slop-mcp:discovery-first` — `execute_tool` 前須先 `get_metadata` / `search_tools`。SLOP 腳本中 `tools.call` / `execute_tool` 亦遵此律。
- Invoke the `Skill` tool with `skill: slop-mcp:event-monitoring` — `slop-mcp monitor` 子命令運行之 monitor 腳本亦為 SLOP，以 `mem_save` / `mem_load` 存 last-seen 游標跨進程重啟不丟狀態。
