---
name: test-fuzz
description: Feed random/invalid inputs to find unexpected crashes. Use when testing input handling, security, or finding edge case bugs.
license: MIT
metadata:
  author: vant
  version: "1.0"
---

# Test Fuzz

> Random input testing.

## When To Use

- Input validation
- Security testing
- Edge cases

## Fuzz Techniques

### 1. Random Data

```javascript
fuzz('email', () => randomEmail())
fuzz('number', () => randomInt())
```

### 2. Invalid Inputs

```javascript
fuzz('sql', () => "' OR '1'='1")
fuzz('xss', () => "<script>alert(1)</script>")
```

### 3. Mutation

```javascript
fuzz('mutation', () => mutate(existing))
```

---

## Tools

| Tool | Use |
|------|-----|
| AFL | Binary fuzzing |
| libFuzzer | LLVM fuzzing |
| Jest QuickCheck | Property-based |
| fast-check | Node fuzzing |

---

## Output

```
## Fuzz Tests

| Input | Result |
|-------|--------|
| [n] inputs | [n] crashes |
| [n] timeouts | [n] hangs |

### Vulnerabilities
- [list]
```

**Role**: Fuzz Tester  
**Input**: Target  
**Output**: Crashes