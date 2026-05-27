---
name: slop-coder-slop-write
description: "\"Write SLOP code with AI assistance - generates correct, safe, and idiomatic SLOP code. AI輔助生成正確、安全、慣用的SLOP代碼。Use when: generating new SLOP programs from requirements, scaffolding agents/pipelines/batch processors.\""
disable-model-invocation: true
---

# Write SLOP Code

按需求生成SLOP代碼。此命令助汝編寫正確、安全、慣用之SLOP代碼。

## Usage

```bash
/slop-write <description of what you want>
```

## Examples

```bash
/slop-write an agent that summarizes articles
/slop-write a data pipeline that filters and transforms user records
/slop-write a batch processor that calls an API with rate limiting
```

## What You Should Do

編寫SLOP代碼時，遵循以下準則：

### 1. Understand the Requirements

- 輸入為何？
- 輸出為何？
- 是否涉及外部服務（LLM、API、MCP）？
- 是否有性能約束（速率限制、超時）？

### 2. Apply SLOP Best Practices

**Always:**
- 以`limit()`、`rate()`或有界集合限制所有循環
- 使用`emit`進行流式輸出
- 以`try/catch`處理錯誤
- LLM調用定義模式

**Prefer:**
- 管道優於嵌套循環
- 簡單轉換用lambda函數
- 分支用`match`表達式
- 有意義的變量名

### 3. Structure the Code

```python
# 1. Define helper functions first
def process_item(item):
    ...

def validate(data):
    ...

# 2. Main logic
items = get_items()

for item in items with limit(1000):
    result = process_item(item)
    emit result

# 3. Final output
emit(status: "complete")
```

### 4. Use Appropriate Patterns

**For AI agents:**
```python
def agent(input):
    response = llm.call(
        prompt: input,
        schema: {output: string}
    )
    return response.output

result = agent(user_input)
emit result
```

**For data pipelines:**
```python
result = data
    | filter(x -> condition(x))
    | map(x -> transform(x))
    | take(limit)

emit result
```

**For batch processing:**
```python
for item in items with limit(1000), rate(10/s):
    try:
        result = process(item)
        emit(item: item.id, status: "success")
    catch:
        emit(item: item.id, status: "failed")
```

**For MCP services:**
```python
result = service.method(arg1: val1, arg2: val2)
emit result
```

## Code Generation Template

生成SLOP代碼時，按以下格式輸出：

```python
# Description: <what the code does>
# Input: <expected input>
# Output: <what is emitted>

# Helper functions
def helper_function():
    ...

# Main logic
# ... processing code ...

# Output
emit(result: result, status: "complete")
```

## Validation Checklist

呈現代碼前，驗證：

- [ ] 所有循環有界（limit、rate或有限集合）
- [ ] LLM調用已定義模式
- [ ] 危險操作有錯誤處理
- [ ] 變量作用域正確
- [ ] 輸出使用emit語句
- [ ] 無無限遞歸可能
- [ ] 字符串插值使用`{variable}`語法
- [ ] 管道正確使用`|`運算符
- [ ] Lambda語法為`x -> expression`或`(a, b) -> expression`

## Common Mistakes to Avoid

### Wrong: Unbounded loop
```python
# BAD
for item in stream:
    process(item)

# GOOD
for item in stream with limit(1000):
    process(item)
```

### Wrong: Missing schema
```python
# BAD
response = llm.call(prompt: "Question")

# GOOD
response = llm.call(
    prompt: "Question",
    schema: {answer: string}
)
```

### Wrong: Silent failures
```python
# BAD
result = risky_call()

# GOOD
try:
    result = risky_call()
catch:
    emit(error: "Call failed")
    stop
```

### Wrong: Incorrect string interpolation
```python
# BAD
msg = "Hello " + name + "!"
msg = f"Hello {name}!"

# GOOD
msg = "Hello, {name}!"
```

### Wrong: Incorrect lambda syntax
```python
# BAD
items.map(x => x * 2)
items.map(lambda x: x * 2)

# GOOD
items | map(x -> x * 2)
```
