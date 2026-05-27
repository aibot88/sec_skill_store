---
name: node-api-review
description: Node.js (Express/Fastify) backend review — async, validation, memory, security, observability.
---

# Node API Review

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md` default-load
sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı **Critical / High / Medium /
Low + kanıt** formatında olmak zorunda — spekülatif Critical yasak. Sahiplik dışı bulgu
ilgili agent'a delege; karar yetkisi eşiği aşılırsa **kullanıcı onayı zorunlu**.

## Ne Zaman Kullanılır
- PR review
- Memory leak şüphesi
- Yeni endpoint
- Audit prod hazırlık

## Workflow
1. **Statik**
   - `tsc --noEmit`, eslint
   - `npm audit --omit=dev`
2. **Async**
   - `await` üstüne try/catch
   - `Promise.all` vs `allSettled`
   - `unhandledRejection` listener
3. **Input**
   - zod/valibot schema her endpoint
   - File upload size + mime + path sanitize
4. **Memory**
   - Stream büyük payload
   - Buffer.allocUnsafe sadece güvenli
   - Heap snapshot komutu (`kill -USR2 <pid>` Node inspect veya `clinic heapprofile`)
5. **Security**
   - Helmet, CORS allowlist, rate limit
   - JWT alg
6. **Observability**
   - pino JSON
   - request id middleware
   - metric expose (`prom-client`)

## Checklist
- [ ] TS strict + noUncheckedIndexedAccess
- [ ] Validation tüm boundary
- [ ] Helmet + CORS + rate limit
- [ ] Stream upload/download büyük payload
- [ ] Logger PII redact
- [ ] Config zod validate
- [ ] Graceful shutdown SIGTERM
- [ ] Test vitest + supertest
- [ ] Dep audit clean

## Antipattern
- `fs.readFileSync` request handler içinde
- `child_process.exec` user input
- `JSON.parse` try/catch'siz
- Global mutable cache (no TTL)
- `process.exit` library kodda
- `Promise.all` partial fail tüm batch'i kaybeder
- `console.log` prod
- `require('dotenv').config()` lib kodu içinde

## Örnek Agent Davranışı
```
User: /node-review src/routes/upload.ts
Agent:
1. Detect: fs.readFileSync(req.body.path) — path traversal + sync
2. Detect: validation yok
3. Suggest: pipeline + zod schema + size limit
4. Diff
```

## Çıktı Formatı
```markdown
# Node Review: <path>

## Critical/High/Medium/Low
## Diff
## Test plan
```
