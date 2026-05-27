---
name: api-crud-generator
description: Generate a complete CRUD REST API with validation, error handling, auth middleware, tests, and OpenAPI docs. Use when asked to create API endpoints, REST resources, or backend CRUD operations.
---

# API CRUD Generator

Generate production-ready CRUD REST API endpoints. This skill creates complete resource endpoints with validation, authentication, error handling, pagination, and tests.

## When to Use

Trigger when the user asks to:
- Create API endpoints for a resource
- Build REST CRUD operations
- Generate backend routes with validation
- Add a new resource/entity to an existing API

## Tech Stack Detection

Before generating code, detect the project's tech stack:
1. Check for `package.json` -> Node.js (Express, Fastify, Nest)
2. Check for `requirements.txt` or `pyproject.toml` -> Python (FastAPI, Django, Flask)
3. Check for `go.mod` -> Go (Gin, Echo, Chi)
4. Check for `Gemfile` -> Ruby (Rails, Sinatra)
5. If unclear, ask the user which framework to use.

Read the existing project structure to match conventions:
- File naming (camelCase vs snake_case vs kebab-case)
- Directory structure (routes/, controllers/, handlers/)
- Import style (ES modules vs CommonJS vs relative paths)
- Existing middleware patterns
- Database ORM in use (Prisma, TypeORM, SQLAlchemy, GORM, ActiveRecord)

## Resource Definition

For each resource, determine:
1. Resource name (singular and plural forms)
2. Fields with types and constraints:
   - Required vs optional
   - String length limits
   - Number ranges
   - Enum values
   - Unique constraints
   - Default values
3. Relationships to other resources (hasMany, belongsTo, manyToMany)
4. Which fields are searchable/filterable
5. Which fields should be excluded from responses (passwords, internal IDs)

## Endpoint Generation

Generate these endpoints for each resource:

### GET /resources
- Pagination: `?page=1&limit=20` with max limit of 100
- Sorting: `?sort=createdAt&order=desc`
- Filtering: `?status=active&category=tech`
- Search: `?q=search+term` across searchable fields
- Response format:
```json
{
  "data": [...],
  "meta": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "totalPages": 8
  }
}
```

### GET /resources/:id
- Return 404 with `{ "error": "Resource not found" }` if not exists
- Include related resources if `?include=comments,author` is specified

### POST /resources
- Validate all required fields
- Return 400 with field-level errors:
```json
{
  "error": "Validation failed",
  "details": [
    { "field": "email", "message": "Invalid email format" },
    { "field": "name", "message": "Name is required" }
  ]
}
```
- Return 201 with created resource
- Set Location header to `/resources/:id`

### PUT /resources/:id
- Full replacement (all fields required)
- Return 404 if not exists
- Return 200 with updated resource

### PATCH /resources/:id
- Partial update (only provided fields)
- Return 404 if not exists
- Return 200 with updated resource

### DELETE /resources/:id
- Return 404 if not exists
- Return 204 No Content on success
- Soft delete if the resource has a `deletedAt` field

## Authentication and Authorization

Apply auth middleware to all mutating endpoints (POST, PUT, PATCH, DELETE):
1. Check for existing auth middleware in the project
2. If found, use the same pattern
3. If not found, create a simple JWT middleware:
   - Extract token from `Authorization: Bearer <token>` header
   - Verify token signature
   - Attach user to request context
   - Return 401 for missing/invalid tokens
4. Add role-based access control if roles exist:
   - Admin: all operations
   - User: own resources only (filter by userId)
   - Public: read-only (GET endpoints only)

## Input Validation

Validate ALL inputs at the controller/handler level:
- Use the project's existing validation library (Joi, Zod, Pydantic, etc.)
- If no validation library exists, use the framework's built-in validation
- Validate:
  - Required fields are present and non-empty
  - String fields don't exceed max length
  - Number fields are within range
  - Email fields match email regex
  - Enum fields contain valid values
  - Date fields are valid ISO 8601
  - ID fields reference existing resources (foreign key validation)
- Never trust user input -- validate at the boundary, not in the model
- Sanitize string inputs to prevent XSS (strip HTML tags)
- Use parameterized queries to prevent SQL injection (the ORM handles this)

## Error Handling

Implement consistent error responses:
- 400: Validation errors (with field-level details)
- 401: Authentication required
- 403: Insufficient permissions
- 404: Resource not found
- 409: Conflict (duplicate unique field)
- 422: Unprocessable entity (valid format but business rule violation)
- 500: Internal server error (log the actual error, return generic message)

Every error response follows:
```json
{
  "error": "Human-readable message",
  "code": "MACHINE_READABLE_CODE",
  "details": []
}
```

Never expose stack traces, internal paths, or database details in error responses.

## Database Operations

- Use transactions for operations that modify multiple records
- Implement optimistic locking if concurrent updates are expected
- Add database indexes for:
  - Primary keys (auto)
  - Foreign keys
  - Fields used in WHERE clauses (filters, search)
  - Fields used in ORDER BY (sorting)
  - Unique constraints
- Use connection pooling (the ORM usually handles this)
- Handle database connection errors gracefully

## Testing

Write tests for every endpoint:

### Unit Tests
- Validation logic (valid input, missing fields, invalid formats)
- Business logic (authorization rules, soft delete behavior)
- Error handling (each error code scenario)

### Integration Tests
- Full request/response cycle for each endpoint
- Auth middleware (valid token, invalid token, missing token, expired token)
- Pagination (first page, last page, out of range)
- Filtering and sorting
- Related resources (include parameter)
- Error scenarios (404, 409 conflict)

### Test Data
- Use factories or fixtures for test data
- Clean up test data after each test
- Use a separate test database

Ensure at least 80% code coverage across all generated files.

## OpenAPI Documentation

Generate OpenAPI 3.0 spec for all endpoints:
- Include request/response schemas
- Document all query parameters
- Document all error responses
- Add authentication requirements
- Include example values for every field
- Group endpoints by resource tag

If the project uses Swagger UI, register the new endpoints automatically.

## File Organization

Place generated files according to existing project conventions. If no conventions exist, use:

```
src/
├── routes/
│   └── resourceName.routes.ts
├── controllers/
│   └── resourceName.controller.ts
├── models/
│   └── resourceName.model.ts
├── validators/
│   └── resourceName.validator.ts
├── middleware/
│   └── auth.middleware.ts
└── tests/
    ├── resourceName.unit.test.ts
    └── resourceName.integration.test.ts
```

## Checklist Before Completing

- [ ] All 5 CRUD endpoints generated
- [ ] Input validation on all mutating endpoints
- [ ] Auth middleware applied to mutating endpoints
- [ ] Consistent error response format
- [ ] Pagination with meta object on list endpoints
- [ ] Database migration/schema created
- [ ] Unit tests for validation and business logic
- [ ] Integration tests for all endpoints
- [ ] OpenAPI spec updated
- [ ] File naming matches project conventions
- [ ] No hardcoded values (use environment variables or config)
- [ ] No sensitive data in error responses

## Avoid

- Don't generate code that doesn't compile/run
- Don't skip validation on any endpoint
- Don't use string concatenation for SQL queries
- Don't expose internal error details to clients
- Don't forget pagination on list endpoints
- Don't hardcode authentication secrets
- Don't skip tests for error scenarios
- Don't use synchronous file operations in Node.js handlers
- Don't return 200 for creation (use 201)
- Don't return 200 for deletion (use 204)
- Don't forget to set the Location header on POST responses
