---
name: test-integration
description: Test how components work together. Test database + API, auth + user service, etc. Use when testing multi-component flows or after unit tests pass.
license: MIT
metadata:
  author: vant
  version: "1.0"
---

# Integration Test

> Components working together.

## When To Use

- Multi-component flows
- After unit tests pass
- Before e2e tests

## What To Test

### 1. Database + API

```javascript
test('user created in DB', async () => {
  const user = await userService.create({ email: 'test@example.com' })
  const inDb = await db.users.find(user.id)
  expect(inDb).toEqual(user)
})
```

### 2. Auth + User Service

```javascript
test('login returns user', async () => {
  const session = await auth.login('test@example.com', 'password')
  expect(session.user.email).toBe('test@example.com')
})
```

### 3. Queue + Worker

```javascript
test('job processed', async () => {
  const job = await queue.add({ task: 'process' })
  await worker.process(job.id)
  expect(job.status).toBe('complete')
})
```

---

## Output

```
## Integration Tests

| Flow | Status |
|------|--------|
| DB + API | [PASS/FAIL] |
| Auth + User | [PASS/FAIL] |
| Queue + Worker | [PASS/FAIL] |

### Time
[n] seconds
```

**Role**: Integration Tester  
**Input**: Components  
**Output**: Integration results