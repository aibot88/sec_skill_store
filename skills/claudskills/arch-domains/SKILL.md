---
name: arch-domains
description: "Required for any work in src/domains/. Covers business rule ownership, port type placement, two injection styles, and intra-domain composition."
paths:
  - 'src/domains/**/*.ts'
---

## Role

Owns all business rules — session lifecycle, agent execution, pipeline orchestration, analysis, and tooling. Never touches raw I/O (files, processes, APIs) directly; always delegates to repository interfaces or functions.

## Import Rules

| May import | Must NOT import |
|-----------|----------------|
| `domains/ports` (intra), `repositories/ports`, `types`, `errors`, `utils`, `constants` | `cli`, `services`, `infrastructures` |

## Injection Styles

**Style A — interface injection** (repository is class-based with `IXxxRepository`)

```ts
import type { ISessionRepository } from '@src/repositories/ports/session'

export class SessionDomain implements ISessionDomain {
  constructor(private sessionRepo: ISessionRepository) {}  // inject interface, not concrete class
}
```

**Style B — function-based** (repository exposes plain exported functions)

```ts
import { saveSession, loadSession } from '@src/repositories/sessions'

export class SomeDomain implements ISomeDomain {
  constructor(private dir: string) {}
  async get(id: string) { return loadSession(this.dir, id) }
}
```

Choose Style A when the repository is a class; Style B when it exposes plain functions. Never call filesystem APIs or spawn processes directly.

## Port Placement

- Domain ports → `src/domains/ports/<name>.ts` (consumed by `services/`)
- Repository ports → `src/repositories/ports/<name>.ts` (consumed by `domains/`)
- Never define `IXxx` inside a domain implementation file

## Intra-Domain Composition

Inject other domains by their port type from `domains/ports/`, never the concrete class:

```ts
import type { ISessionDomain } from '@src/domains/ports/session'

export class AnalyzeDomain implements IAnalyzeDomain {
  constructor(private sessionDomain: ISessionDomain) {}  // ✓ port type
}
// ✗ Bad: import { SessionDomain } from '@src/domains/session' + new SessionDomain(...)
```

A domain with pure business logic may inject only other domain ports and no repository — both patterns are valid.

## Prohibitions

- Never import from `cli`, `services`, or `infrastructures`
- Never import `zod` — validation belongs in `validators/`
- Never access the filesystem, spawn processes, or call external APIs directly
- Never read `process.env`
- Never expose transport variants in a repository port — single abstract method only
- Never define `IXxx` in a domain implementation file
- Never import or instantiate a concrete repository class (`new XxxRepository()`)
- Never call into `services/` — domains sit below services in the dependency chain

## References

- [`references/session-field-migration.md`](./references/session-field-migration.md) — lazy `normalize()` pattern for renaming a persisted session JSON field
