---
name: new-service-route
description: Scaffold a new Fastify route in services/{reservations,users,agent} matching the house pattern — schema validation, auth, error envelope per ADR-002, SSE broadcast (if reservations), tests
disable-model-invocation: true
---

# /new-service-route — add a Fastify route to a service

Generates a new route handler in one of the monorepo's Fastify services that matches the conventions of existing routes.

## Gather context

Ask the user (or accept as args) if not obvious from the task:

1. **Which service?** One of `reservations`, `users`, `agent`.
2. **HTTP method + path.** e.g., `POST /api/v1/floor-plans/:id/clone`.
3. **What it does.** One sentence — becomes the OpenAPI `summary`.
4. **Request body / params / querystring** — the shapes that need validation.
5. **Response shape** — what gets returned on success.
6. **Auth?** Nearly always yes. `preHandler: [fastify.requireAuth]`.
7. **Should it emit an SSE event?** reservations service only — e.g., `floor-plan:created`.

## Route shape (example — adapt to the specific service)

```typescript
fastify.post<{
  Params: { id: string };
  Body: CloneFloorPlanRequest;
  Reply: ApiResponse<FloorPlan> | ApiError;
}>(
  "/:id/clone",
  {
    preHandler: [fastify.requireAuth],
    schema: {
      summary: "Clone a floor plan",
      operationId: "cloneFloorPlan",
      description: "Duplicates a floor plan and all its tables.",
      tags: ["Floor Plans"],
      params: {
        type: "object",
        required: ["id"],
        properties: { id: { type: "string" } },
      },
      body: {
        type: "object",
        properties: { name: { type: "string" } },
      },
      response: {
        201: { /* FloorPlan */ },
        404: { /* ApiError */ },
      },
    },
  },
  async (request, reply) => {
    const result = await floorPlanService.clone(request.params.id, request.body);
    if (!result) {
      return reply.code(404).send(createProblemDetails({
        type: "floor-plan-not-found",
        title: "Floor plan not found",
        status: 404,
        instance: request.url,
      }));
    }
    // Emit SSE if this service broadcasts (reservations only)
    fastify.sseBroadcaster?.emit("floor-plan:created", result);
    return reply.code(201).send({ success: true, data: result });
  }
);
```

## Rules

- **Always validate via `schema`.** Fastify's schema is enforced at request time — don't validate manually in the handler.
- **Always use the ApiResponse / ApiError envelope from `@mbe/types`** per ADR-002. No bare objects, no HTTP-only error responses.
- **Use `createProblemDetails` for errors** — it produces RFC 7807 problem-details format that the edge router surfaces to clients.
- **Prisma calls inside a transaction when the route writes to multiple tables.** `prisma.$transaction([...])` or the callback form.
- **SSE emission (reservations only) happens AFTER the DB commit succeeds** — never inside the transaction.
- **Auth is required for everything except `/health` and `/api/v1/availability`** (the booking widget needs unauthenticated availability lookups).
- **Add the route to the correct file.** `src/routes/<domain>.ts` — one file per domain (reservations, tables, venues, floor-plans, etc.).
- **Register route-level tests in `src/routes/<domain>.test.ts`** — use `app.inject()` pattern established elsewhere; mock the service layer.

## Checklist after scaffolding

- [ ] Route schema matches request/response types exactly
- [ ] Auth preHandler present (unless explicitly public)
- [ ] Error cases return ApiError via `createProblemDetails`
- [ ] Success returns ApiResponse envelope
- [ ] If multi-write, wrapped in Prisma transaction
- [ ] SSE event emitted post-commit (reservations only)
- [ ] Tests cover: happy path, auth failure, validation failure, not-found, conflict
- [ ] `pnpm test` passes inside the service directory
- [ ] `pnpm typecheck` passes

## When to use

Use for any new server-side endpoint. Examples from the backlog:
- #586 `POST /api/v1/floor-plans/:id/clone`
- New reservation state transitions
- New guest CRM endpoints
