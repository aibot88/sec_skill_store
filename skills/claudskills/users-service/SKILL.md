---
name: users-service
description: This skill should be used when the user asks to "add an endpoint to users", "create a route in users service", "write tests for users", "test users service", "add auth to a route", "work on users API", or mentions the users service, Fastify routes, or user management functionality.
---

# Users Service Development Skill

This skill provides patterns and workflows for developing the Users Service, a Fastify-based REST API at `services/users/` that handles user management with Auth0 authentication and Prisma ORM.

## Service Overview

**Location**: `services/users/`
**Framework**: Fastify v5 with TypeScript
**Database**: PostgreSQL via Prisma
**Auth**: Auth0 JWT verification with jose
**Port**: 3001 (API docs at http://localhost:3001/docs)

### Key Files

| File | Purpose |
|------|---------|
| `src/app.ts` | Fastify app setup, plugin registration |
| `src/routes/users.ts` | User CRUD endpoints and auth endpoints |
| `src/services/user.ts` | Business logic (Prisma operations) |
| `src/schemas/index.ts` | OpenAPI schema definitions |
| `prisma/schema.prisma` | Database schema |

## Adding New Endpoints

### Route Structure Pattern

Follow this pattern when adding new routes to `src/routes/users.ts`:

```typescript
fastify.get<{
  Params: { id: string };           // URL params
  Querystring: { page?: string };   // Query params
  Body: CreateUserRequest;          // Request body
  Reply: ApiResponse<User> | ApiError;  // Response types
}>(
  "/endpoint-path",
  {
    preHandler: verifyAuth,  // Add for protected routes
    schema: {
      summary: "Short action description",
      operationId: "uniqueOperationName",
      description: "Detailed description for API docs.",
      tags: ["Users"],
      security: [{ bearerAuth: [] }],  // Add for auth routes
      params: { /* JSON Schema */ },
      body: { /* JSON Schema */ },
      response: {
        200: {
          description: "Success case",
          type: "object",
          properties: {
            data: { $ref: "User#" },  // Reference shared schemas
          },
        },
        404: { $ref: "Error#" },
      },
    },
  },
  async (request, reply) => {
    // Implementation
  }
);
```

### Adding a Protected Endpoint

Protected endpoints require JWT authentication. Add `preHandler: verifyAuth` and `security` schema:

```typescript
fastify.get<{ Reply: ApiResponse<User> }>(
  "/me/profile",
  {
    preHandler: verifyAuth,  // JWT verification
    schema: {
      summary: "Get extended profile",
      operationId: "getExtendedProfile",
      tags: ["Users"],
      security: [{ bearerAuth: [] }],  // Documents auth requirement
      response: {
        200: { /* ... */ },
        401: { $ref: "Error#" },
      },
    },
  },
  async (request, reply) => {
    const authUser = request.user;
    if (!authUser?.email) {
      return reply.code(401).send({
        error: "Unauthorized",
        message: "Authentication required",
        statusCode: 401,
      });
    }
    // ... implementation
  }
);
```

### Adding Service Methods

Add business logic to `src/services/user.ts`. Always use `mapPrismaUser()` to convert Prisma types:

```typescript
async getByUsername(username: string): Promise<User | null> {
  const user = await prisma.user.findFirst({
    where: { username },
  });
  return user ? mapPrismaUser(user) : null;
},
```

### Shared Types

Import types from `@mbe/types`:

```typescript
import type {
  User,
  CreateUserRequest,
  UpdateUserRequest,
  ApiResponse,
  ApiError,
  PaginatedResponse,
} from "@mbe/types";
```

## Testing

### Test Commands

```bash
cd services/users

pnpm test                          # Run all tests
pnpm test:watch                    # Watch mode
pnpm test:coverage                 # Coverage report
npx vitest run src/routes/users.test.ts  # Single file
npx vitest --grep "GET /v1/users"  # Match pattern
```

### Test Structure Pattern

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import type { FastifyInstance } from "fastify";
import { buildApp } from "../app.js";
import { userService } from "../services/user.js";

// Mock the service layer
vi.mock("../services/user.js", () => ({
  userService: {
    list: vi.fn(),
    getById: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
}));

describe("User Routes", () => {
  let app: FastifyInstance;

  beforeEach(async () => {
    app = await buildApp({ logger: false });
    await app.ready();
  });

  afterEach(async () => {
    await app.close();
    vi.clearAllMocks();
  });

  describe("GET /v1/users", () => {
    it("should return paginated users", async () => {
      const mockUsers = [
        { id: "1", email: "test@example.com", /* ... */ },
      ];

      vi.mocked(userService.list).mockResolvedValueOnce({
        data: mockUsers,
        pagination: { page: 1, limit: 10, total: 1, /* ... */ },
      });

      const response = await app.inject({
        method: "GET",
        url: "/v1/users",
      });

      expect(response.statusCode).toBe(200);
      expect(JSON.parse(response.body)).toEqual({
        data: mockUsers,
        pagination: expect.any(Object),
      });
    });
  });
});
```

### Testing Protected Routes

Mock the auth layer or test 401 responses:

```typescript
it("should return 401 without auth header", async () => {
  const response = await app.inject({
    method: "GET",
    url: "/v1/users/me",
  });

  expect(response.statusCode).toBe(401);
});
```

## Auth0 Integration

### Environment Variables

```bash
AUTH_AUTHORITY=https://dev-ytbgmz5ls3wh4xdx.us.auth0.com
AUTH_AUDIENCE=https://api.mattbutlerengineering.com
```

### How Auth Works

1. Client gets JWT from Auth0
2. Client sends `Authorization: Bearer <token>` header
3. `verifyAuth` preHandler validates token via JWKS
4. `request.user` populated with user info from JWT claims

### JWT Payload Structure

```typescript
interface JWTPayload {
  sub: string;           // User ID (from Auth0)
  email: string;         // Email address
  email_verified: boolean;
  name?: string;
  picture?: string;
  // ... other claims
}
```

### Accessing Auth User

In protected routes, access the authenticated user:

```typescript
async (request, reply) => {
  const authUser = request.user;
  // authUser.id, authUser.email, authUser.name, etc.
}
```

## Database Schema

Current User model in `prisma/schema.prisma`:

```prisma
model User {
  id             String   @id @default(cuid())
  email          String   @unique
  name           String?
  picture        String?
  emailVerified  Boolean  @default(false)
  preferences    Json     @default("{}")
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt
}
```

For schema changes, use the `prisma-migrations` skill.

## API Endpoints Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/v1/users` | No | List users (paginated) |
| GET | `/v1/users/:id` | No | Get user by ID |
| POST | `/v1/users` | No | Create user |
| PATCH | `/v1/users/:id` | No | Update user |
| DELETE | `/v1/users/:id` | No | Delete user |
| GET | `/v1/users/me` | Yes | Get current user (auto-creates) |
| PATCH | `/v1/users/me/preferences` | Yes | Update preferences |
| GET | `/health` | No | Health check |

## Common Development Tasks

### Start Development Server

```bash
cd services/users
pnpm dev
```

### Check Code Quality

```bash
pnpm lint      # ESLint
pnpm typecheck # TypeScript
```

### Open API Docs

Navigate to http://localhost:3001/docs for interactive Scalar API documentation.

### Database Operations

```bash
pnpm db:studio     # Visual database browser
pnpm db:push       # Quick schema sync (dev only)
pnpm db:migrate    # Create migration (see prisma-migrations skill)
```

## Error Response Format

All errors follow this structure:

```typescript
{
  error: "Not Found",      // HTTP status text
  message: "User not found", // Human-readable message
  statusCode: 404          // HTTP status code
}
```

## Quick Checklist for New Endpoints

1. [ ] Add TypeScript types for Params/Body/Reply
2. [ ] Include OpenAPI schema with summary, description, tags
3. [ ] Add `preHandler: verifyAuth` if protected
4. [ ] Add `security: [{ bearerAuth: [] }]` if protected
5. [ ] Handle all error cases (400, 401, 404, 500)
6. [ ] Add service method if new business logic needed
7. [ ] Write tests with mocked service layer
8. [ ] Run `pnpm test` and `pnpm typecheck`
