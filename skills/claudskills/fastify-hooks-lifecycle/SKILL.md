---
name: fastify-hooks-lifecycle
description: >
  This skill should be used when implementing Fastify hooks, understanding hook execution order, using onRequest/preParsing/preValidation/preHandler/preSerialization/onError/onSend/onResponse hooks, using onReady/onListen/onClose/onRoute/onRegister application hooks, debugging hook chain issues, adding authentication hooks, implementing request lifecycle interceptors, working with Fastify lifecycle events, or understanding when request.body is available.
---

# Fastify Hook Lifecycle Reference

You are working with Fastify's hook system. Follow every rule in this document precisely. Violations of the critical rules below cause silent double executions, lost context, and runtime exceptions that are difficult to trace.

## General Hook Rules (CRITICAL)

Obey these rules in every hook you write. There are no exceptions.

- NEVER mix async/await with the `done` callback. If the hook function is declared `async`, do not accept or call `done`. If the hook uses `done`, do not use `async` or return a Promise. Mixing the two causes double execution of downstream hooks and handlers.
- NEVER use arrow functions as hook handlers. Arrow functions do not bind `this`, which means you lose access to the Fastify instance context (`this` is the encapsulating Fastify server). Always use `function` declarations or expressions.
- When you need to short-circuit the request lifecycle from an async hook, call `reply.send()` and then `return reply`. If you forget `return reply`, Fastify continues executing the remaining lifecycle, resulting in double execution and potential "Reply already sent" errors.
- Hooks can be either global or encapsulated. A hook registered inside a plugin that uses `fastify-plugin` (which breaks encapsulation) becomes global. A hook registered inside a normal plugin is scoped to that plugin and its children only. Be intentional about which you need.
- Every hook that accepts a `done` callback MUST call it. Failing to call `done` hangs the request indefinitely.
- Do not perform heavy synchronous work inside hooks. Fastify is single-threaded; blocking the event loop in a hook blocks all concurrent requests.

## Request/Reply Hooks (Execution Order)

These hooks execute in the order listed below for every incoming request. Understand exactly where in the lifecycle each hook fires and what data is available at that point.

### 1. onRequest

This is the first hook that fires, before any parsing occurs.

- Signature: `function (request, reply, done)` (or `async function (request, reply)`)
- `request.body` is UNDEFINED at this point. The request body has not been parsed yet. Do not attempt to read it.
- `request.params`, `request.query`, and `request.headers` ARE available.
- Use this hook for: early authentication checks (e.g., verifying a JWT before doing any work), request logging, IP-based rate limiting, early redirects, and attaching request-scoped metadata.
- To deny a request, call `reply.code(401).send({ error: 'Unauthorized' })` and `return reply` (in async hooks) or call `done(error)` (in callback hooks).

### 2. preParsing

This hook fires before the body parsing phase begins.

- Signature: `function (request, reply, payload, done)` (or `async function (request, reply, payload)`)
- `payload` is the raw incoming request stream (a Node.js Readable stream). You can replace it with a different stream (e.g., for decompression or decryption).
- `request.body` is still UNDEFINED. Parsing has not happened yet.
- If you return or pass a new payload via `done`, it MUST be a stream. You cannot return a plain object or string here.
- When returning a modified stream, you MUST set the `receivedEncodedLength` property on the new stream to enable proper Content-Length validation. Example: `newStream.receivedEncodedLength = oldStream.receivedEncodedLength || 0`.
- Use this hook for: decompressing custom encodings, decrypting request bodies, or injecting a proxy stream for request body auditing.

### 3. preValidation

This hook fires after the body has been parsed but BEFORE JSON Schema validation runs.

- Signature: `function (request, reply, done)` (or `async function (request, reply)`)
- `request.body` IS available and contains the parsed body. This is the earliest point where you can read the body.
- Use this hook for: sanitizing or transforming the body before schema validation, injecting default values into the body so they pass schema checks, stripping unexpected fields, or performing custom validation logic that must run before the schema.
- If you modify `request.body` here, the modified version is what the schema validator will see.

### 4. preHandler

This hook fires after schema validation succeeds, immediately before your route handler executes.

- Signature: `function (request, reply, done)` (or `async function (request, reply)`)
- `request.body`, `request.params`, and `request.querystring` are all fully parsed, typed, and schema-validated at this point.
- Use this hook for: authorization and permission checks that depend on the validated request data, loading the authenticated user from the database and attaching it to `request.user`, checking resource ownership, and performing any pre-handler logic that depends on a fully validated request.
- This is the most common hook for authentication/authorization middleware. If you need to check permissions based on the request body or params, do it here.

### 5. preSerialization

This hook fires after the route handler returns its payload but before Fastify serializes it to JSON.

- Signature: `function (request, reply, payload, done)` (or `async function (request, reply, payload)`)
- `payload` is the JavaScript object returned by your route handler.
- This hook is NOT called if the handler returned a string, Buffer, stream, or null. It only fires for object payloads that need JSON serialization.
- Use this hook for: wrapping all responses in a standard envelope (e.g., `{ data: payload, meta: { ... } }`), adding pagination metadata, or injecting HATEOAS links into response objects.
- Return the modified payload from the async function or pass it as the second argument to `done`.

### 6. onError

This hook fires when an exception occurs during the request lifecycle, BEFORE the custom error handler runs.

- Signature: `function (request, reply, error, done)` (or `async function (request, reply, error)`)
- You CANNOT call `reply.send()` inside this hook. Doing so throws an exception. The error handler is responsible for sending the response.
- You CANNOT pass an error to `done(err)` in this hook. Passing an error into the done callback is not supported and will cause undefined behavior.
- Use this hook exclusively for: error telemetry and observability (sending errors to Sentry, Datadog, etc.), audit logging of failures, and incrementing error counters for monitoring.
- If you need to modify the error response, do that in the custom error handler (`setErrorHandler`), not here.

### 7. onSend

This hook fires right before the response is written to the socket.

- Signature: `function (request, reply, payload, done)` (or `async function (request, reply, payload)`)
- `payload` is the final serialized value (a string or Buffer). If the handler returned a stream, `payload` is that stream.
- You can modify the payload here, but the replacement MUST be one of: string, Buffer, stream, ReadableStream, Response, or null. You cannot return a plain JavaScript object.
- Use this hook for: setting final response headers (e.g., `reply.header('X-Request-Id', id)`), replacing or clearing the response payload, compressing the response, or adding security headers.
- If you set the payload to null, ensure the Content-Length header is also removed or set to 0.

### 8. onResponse

This hook fires after the response has been completely sent to the client.

- Signature: `function (request, reply, done)` (or `async function (request, reply)`)
- You CANNOT send any data at this point. The HTTP transaction is finished. Calling `reply.send()` here will throw.
- Use this hook for: recording response time metrics, flushing audit logs, emitting analytics events, and cleaning up request-scoped resources.
- `reply.elapsedTime` gives you the time in milliseconds since the request started, which is useful for latency metrics.

### 9. onTimeout

This hook fires when a request exceeds the configured `connectionTimeout` and the socket is hung up.

- You CANNOT send any data. The connection is already closed.
- Signature: `function (request, reply, done)` (or `async function (request, reply)`)
- Use this hook for: observability and alerting on slow requests, logging which routes are timing out, and canceling in-progress operations.
- You must configure `connectionTimeout` on the Fastify instance for this hook to fire.

### 10. onRequestAbort

This hook fires when the client prematurely closes the connection before the response is sent.

- You CANNOT send any data. The client has disconnected.
- Signature: `function (request, reply, done)` (or `async function (request, reply)`)
- Use this hook for: aborting expensive in-progress database queries, cleaning up file uploads that were interrupted, releasing held resources, and logging abandoned requests for monitoring.

## Application Hooks

These hooks are not tied to individual requests. They fire during server lifecycle events.

### onReady

- Fires before the server starts listening for connections (or when `fastify.ready()` is called explicitly).
- At this point, all plugins are guaranteed to be fully loaded. The plugin tree is finalized.
- You CANNOT register new routes, hooks, or plugins at this point. The server configuration is frozen.
- Signature: `function (done)` (or `async function ()`) -- note there is no `request` or `reply`.
- Use this hook for: verifying external service connectivity (database ping, cache ping), warming caches, logging startup diagnostics, and running database migrations.

### onListen

- Fires when the server starts listening on its configured port.
- Hooks run sequentially in registration order.
- Errors thrown inside this hook are logged but IGNORED. The server continues booting regardless. Do not rely on this hook for critical initialization that must succeed.
- Use this hook for: logging the listening address, notifying a service registry, or triggering post-boot healthcheck pings.

### onClose

- Fires when `fastify.close()` is called, after the server has stopped accepting new connections and all in-flight requests have completed.
- Signature: `function (instance, done)` (or `async function (instance)`)
- Hooks execute in REVERSE order of registration. Child plugin teardown runs before parent teardown. This ensures dependencies are released in the correct order.
- Use this hook for: closing database connection pools, releasing file handles, flushing buffered logs, disconnecting from message queues, and any graceful shutdown cleanup.

### onRoute

- Fires synchronously every time a new route is registered.
- Signature: `function (routeOptions)` -- there is NO `done` callback. This is purely synchronous.
- `routeOptions` contains the full route configuration: `method`, `url`, `schema`, `handler`, `preHandler`, etc.
- You can mutate the `routeOptions` object to dynamically modify routes as they are registered.
- Use this hook for: dynamically injecting hooks into routes based on metadata, building route registries for documentation generators, enforcing naming conventions, and adding default schema properties.

### onRegister

- Fires when a new plugin is registered and a new encapsulation context is created.
- Executes BEFORE the plugin code itself runs.
- This hook is NOT triggered for plugins wrapped with `fastify-plugin` (since `fastify-plugin` prevents the creation of a new encapsulation context).
- Use this hook for: initializing plugin-scoped state, setting up context-specific decorators, and debugging plugin registration order.

## Common Mistakes You Must Enforce Against

When writing or reviewing Fastify hook code, actively check for and prevent these errors:

1. **Accessing `request.body` in `onRequest` or `preParsing`**: The body is always undefined at these stages. If you need the body, use `preValidation` or later.
2. **Calling `reply.send()` in `onError`**: This throws an exception. The error handler sends the response, not the `onError` hook.
3. **Sending data in `onResponse`, `onTimeout`, or `onRequestAbort`**: The connection is already closed or the response already sent. Any attempt to send data will throw.
4. **Using `async function` AND calling `done()`**: Pick one paradigm. Async functions signal completion by resolving/rejecting the returned promise. Calling `done()` inside an async function causes the hook to complete twice.
5. **Forgetting `return reply` after `reply.send()` in async hooks**: Without the return, Fastify does not know you are short-circuiting and continues executing the remaining lifecycle.
6. **Using arrow functions for hooks**: Arrow functions inherit `this` from the enclosing scope, not the Fastify instance. You lose access to decorators, server config, and other instance properties via `this`.
7. **Returning a non-stream value from `preParsing`**: The return value must be a stream. Returning an object or string will cause an error.
8. **Returning a plain object from `onSend`**: The payload at `onSend` must be a string, Buffer, stream, ReadableStream, Response, or null. Objects are not valid.
9. **Forgetting to call `done()` in callback-style hooks**: This hangs the request indefinitely with no error message.
10. **Registering routes or hooks inside `onReady`**: The server configuration is frozen at this point. New registrations are silently ignored or throw.

## Hook Registration Patterns

When registering hooks, follow these patterns:

```javascript
// CORRECT: named function, preserves this binding
fastify.addHook('onRequest', function onRequestAuth(request, reply, done) {
  // this === fastify instance
  done()
})

// CORRECT: async without done
fastify.addHook('preHandler', async function preHandlerAuth(request, reply) {
  const user = await this.db.findUser(request.headers.authorization)
  if (!user) {
    reply.code(401).send({ error: 'Unauthorized' })
    return reply  // REQUIRED: signals short-circuit
  }
  request.user = user
})

// WRONG: arrow function loses this
fastify.addHook('onRequest', async (request, reply) => {
  this.log.info('request')  // this is NOT fastify
})

// WRONG: async + done = double execution
fastify.addHook('onRequest', async function (request, reply, done) {
  await someAsyncWork()
  done()  // BUG: promise resolution AND done both signal completion
})
```

## Scoped vs Global Hooks

Understand the encapsulation rules:

- A hook added at the root Fastify instance applies to ALL routes.
- A hook added inside a plugin applies only to routes registered in that plugin and its children.
- If the plugin is wrapped with `fastify-plugin`, the hook "leaks" to the parent context and behaves as if registered there.
- Use encapsulation intentionally: authentication hooks for a specific API version should be scoped to that version's plugin, not applied globally.
