---
name: api-contract-init
description: Generate API_CONTRACT.md by scanning existing routes and controllers
argument-hint: [shared|root — where to create the file]
---

Generate an `API_CONTRACT.md` by scanning the **real** codebase. Never fabricate endpoints or types.

## 1. Detect the backend stack

| File | Stack |
|---|---|
| `package.json` with `@nestjs/core` | NestJS |
| `package.json` with `express`/`fastify` | Express/Fastify |
| `composer.json` | CakePHP / Laravel |
| `pyproject.toml` or `requirements.txt` with `django`/`fastapi`/`flask` | Python |
| `go.mod` | Go |
| `Cargo.toml` with `actix`/`axum`/`rocket` | Rust |
| `Gemfile` with `rails` | Rails |

## 2. Scan routes and controllers

| Stack | Where to look |
|---|---|
| NestJS | `*.controller.ts` — decorators `@Get`, `@Post`, `@Put`, `@Delete`, `@Patch` |
| Express/Fastify | `routes/**`, `router/**` — `router.get()`, `app.post()`, etc. |
| CakePHP/Laravel | `*Controller.php` — public methods, `routes/*.php` |
| Django | `urls.py` — `urlpatterns`, `ViewSet` classes |
| FastAPI | `*.py` — `@app.get`, `@router.post`, etc. |
| Go | `*_handler.go`, `*_router.go` — `HandleFunc`, `mux.Handle` |
| Rails | `config/routes.rb` — resources, get/post/put/delete |
| Rust | `routes/*.rs` — handler functions, route macros |

## 3. For each endpoint, extract

- HTTP method and path
- Request body / query params (from DTOs, structs, dataclasses, type annotations)
- Response type (if detectable)
- Auth requirement (if detectable)
- If a type cannot be determined, write `// TODO: define type` — **NEVER fabricate**

## 4. Generate the contract

Use this format:

```markdown
# API Contract — [Project Name]

Source of truth for backend/frontend communication.

## Global Conventions
- Base URL: [detected or TODO]
- Auth: [detected or TODO]
- Response format: [detected or standard JSON]
- Error format: [detected or TODO]

## [Domain — grouped by controller/router]

### [METHOD] [path]

**Request:**
\`\`\`[lang]
[body type / query params]
\`\`\`

**Response:**
\`\`\`[lang]
[response type]
\`\`\`

**Auth:** [required/optional/none]
**Notes:** [if applicable]

---

## Changelog

| Date | Change | Side |
|------|--------|------|
| [today] | Initial generation from code | backend |
```

## 5. Placement

- If argument is `shared` or no argument: propose `shared/API_CONTRACT.md`
- If argument is `root`: propose `API_CONTRACT.md` at project root

**Present the generated contract and wait for user validation before writing.**
