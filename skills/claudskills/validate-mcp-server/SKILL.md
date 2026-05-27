---
name: mcp-tester-validate-mcp-server
description: "Validate MCP server connection, tool discovery, schema correctness, and functional behavior. 驗 MCP 伺服器連線、工具發現、模式正確性及功能行為。 Use when: verifying new MCP server implementation, checking schema compliance, testing tool error handling."
disable-model-invocation: true
---

# Validating MCP Server Implementations

助以 mcp-debug 工具驗 MCP 伺服器實作。

## Validation Checklist

### 1. Connection Validation

先驗伺服器正常連線：

```
Use server_add tool:
- name: "test-server"
- command: "<server command>"

Then use server_list to verify connection
```

查：
- 伺服器出現於列表
- 狀態顯示 "connected"
- 工具已被發現

### 2. Tool Discovery Validation

連線後驗工具正確暴露：

```
Use server_list to see all tools
```

查每工具具備：
- 清晰描述性名稱
- 正確前綴已應用
- 無重複名稱

### 3. Schema Validation

驗所有工具模式為有效 JSON Schema：

```
Use schema_validate tool:
- server: "test-server"
(omit tool parameter to validate all)
```

尋：
- 所有模式通過驗證
- 無缺少必要欄位
- 型別定義正確

### 4. Individual Tool Schema Validation

關鍵工具逐一驗模式：

```
Use schema_validate tool:
- server: "test-server"
- tool: "process_data"
```

### 5. Input Validation Testing

測模式正確驗輸入：

```
Use schema_validate tool:
- server: "test-server"
- tool: "process_data"
- input: '{"data": [1, 2, 3]}'
```

同時測：
- 有效輸入（應通過）
- 無效輸入（應以清晰錯誤失敗）

## Common Schema Issues

### Missing Required Properties
```json
// Bad - no required array
{"type": "object", "properties": {...}}

// Good
{"type": "object", "properties": {...}, "required": ["data"]}
```

### Incorrect Type Definitions
```json
// Bad - accepts anything
{"type": "object"}

// Good - specific properties
{"type": "object", "properties": {"name": {"type": "string"}}}
```

### Missing Descriptions
```json
// Bad - no context for AI
{"type": "string"}

// Good - helps AI understand usage
{"type": "string", "description": "User's full name"}
```

## Functional Validation

模式驗證後，測實際工具呼叫：

1. **基本功能** — 工具能用否？
2. **錯誤處理** — 是否返回正確錯誤？
3. **邊緣情況** — 空輸入、大輸入、特殊字元

每次測試後以 `debug_logs` 查實際 JSON-RPC 流量。

## Validation Report Template

驗後彙整：

```
Server: <name>
Status: <connected/error>
Tools discovered: <count>

Schema Validation:
- Passed: <count>
- Failed: <count with details>

Functional Tests:
- <tool>: <pass/fail with notes>
```
