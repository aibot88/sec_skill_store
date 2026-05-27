---
name: principle-design-patterns
description: Design patterns — Gang of Four and beyond. Strategy, factory method, observer, decorator, adapter, facade, template method, command, repository, dependency injection. Auto-load when designing class structure, refactoring toward a pattern, or evaluating whether a pattern applies.
---

# Design Patterns — the ones worth knowing

Patterns are vocabulary, not goals. Reach for one only when the problem it solves is actually present.

## Strategy
**Problem:** an algorithm varies independently of its caller.
**Use when:** multiple interchangeable behaviors selected at runtime (pricing rules, compression, sort orders).
**Overkill when:** there is only one strategy.
**Modern alternative:** a first-class function or lambda.

## Factory Method
**Problem:** construction is non-trivial or must be swappable.
**Use when:** the concrete type depends on input or config.
**Overkill when:** `new Thing()` works and always will.
**Modern alternative:** a constructor function plus DI at the composition root.

## Observer
**Problem:** many objects need to react to a state change.
**Use when:** loose coupling between emitter and listeners (UI, domain events).
**Overkill when:** one listener, ever — call it directly.
**Modern alternative:** language-native events, reactive streams, domain events on a bus.

## Decorator
**Problem:** add behavior without subclassing the world.
**Use when:** stacking optional behavior — caching, logging, retries around a core call.
**Overkill when:** no composition, one behavior.
**Modern alternative:** middleware chains, higher-order functions.

## Adapter
**Problem:** two interfaces should work together but don't.
**Use when:** integrating a third-party or legacy API into your domain types.
**Overkill when:** you control both sides — just change one.

## Facade
**Problem:** a subsystem has too many moving parts for its callers.
**Use when:** simplifying a complex API for the common 80%.
**Overkill when:** the facade just forwards one call.

## Template Method
**Problem:** the skeleton of an algorithm is fixed but steps vary.
**Use when:** several variants share a clear sequence.
**Overkill when:** the sequence is two steps.
**Warning:** easy to abuse — prefer Strategy when steps are independent.

## Command
**Problem:** parameterize, queue, log, or undo actions.
**Use when:** task queues, undo/redo, transactional operations.
**Overkill when:** you just want to call a function.

## Repository
**Problem:** domain code should not depend on storage details.
**Use when:** persisting aggregates behind a collection-like interface.
**Overkill when:** a single SQL query in a single place.

## Dependency Injection (essential, not GoF)
**Problem:** classes that new-up their own collaborators are untestable and rigid.
**Use when:** wiring side-effecting collaborators (clocks, IDs, repositories, gateways).
**Overkill when:** constructing simple value objects.
**Anti-pattern:** heavyweight DI frameworks for small apps — constructor injection at `main()` is usually enough.

## Anti-patterns worth naming
- **Singleton** — almost always a disguised global; prefer a single instance composed at the root.
- **God object** — one class that does everything; split by change vector.
- **Pattern-itis** — five patterns where a function would do.
