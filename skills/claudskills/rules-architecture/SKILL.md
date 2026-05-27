---
name: rules-architecture
description: Non-negotiable Jardis architecture rules — five constitutional pillars, hexagonal dependency direction, Closure-Orchestrator pattern. Consult before authoring any new class or reviewing existing code.
zone: crosscut
prerequisites: []
next: []
---

## Scope

Applies to Jardis packages (`JardisAdapter/*`, `JardisSupport/*`, `JardisTools/*`) and library code inside the hexagonal cake. The five pillars (§1) also hold on the Designer-generated Domain layer, but the physical directory contract there is different — see `platform-implementation`.

### 1. Five pillars

1. **Separation of Concerns** — different responsibilities → different components. Cross-cutting via Decorator/Middleware.
2. **Single Responsibility** — one class = one reason to change. "And"-test: description contains "and" → split.
3. **Composition over Inheritance** — interfaces, Constructor Injection, runtime replaceability. **No traits.** `abstract` only for Exception hierarchies. `static` only for VO named constructors.
4. **Data-Behavior Separation** — DTOs / Entities / VOs hold data. Services operate on data. Persistence external via Repository. Entities have no business methods.
5. **Explicit Dependencies** — Constructor Injection for everything. Infrastructure behind interfaces. No implicit access to outside state.

```
PHP 8.3+ | declare(strict_types=1) | PHPStan Level 8 | PSR-4/PSR-12 | Coverage ≥ 80%
```

### 2. Hexagonal layout

Dependency arrows point **inward** to the Core. Core never imports Adapter code.

```
JardisCore\*              -> Domain Layer
JardisSupport\Contract\*  -> Contracts (interfaces, ports)
JardisSupport\*           -> Application / Support
JardisAdapter\*           -> Infrastructure
JardisTools\*             -> Development Tools

JardisTools -> JardisAdapter -> JardisSupport -> JardisCore
                    |               |              |
          JardisSupport\Contract <-<-<-----------<-<
```

Adapters implement Contracts. Any inner-layer `use` pointing outward is a review blocker.

### 3. Closure-Orchestrator pattern

**Closure** — atomic unit. Class with `__invoke()` as the only public entry point. Name = what it does (`BuildKey`, `ValidatePath`). IPO. No `run()` / `execute()` / `handle()`. No second public method.

```php
final class BuildKey
{
    public function __invoke(string $prefix, string $path): string
    {
        return $this->normalize($prefix) . '/' . ltrim($path, '/');
    }
    private function normalize(string $prefix): string { return rtrim($prefix, '/'); }
}
```

**Orchestrator** — composition. Consumes Closures, **no own logic**. Closures bound in constructor via first-class callable syntax.

```php
final class Filesystem
{
    private readonly Closure $buildPath;
    private readonly Closure $validatePath;

    public function __construct(string $root)
    {
        $this->buildPath    = (new BuildFullPath($root))->__invoke(...);
        $this->validatePath = (new ValidatePath())->__invoke(...);
    }

    public function read(string $path): string
    {
        $fullPath = ($this->buildPath)($path);
        return file_get_contents(($this->validatePath)($fullPath));
    }
}
```

Multi-method interfaces (`hash`/`verify`/`needsRehash`) → each method delegates to its own Closure. Closures may wrap other Closures (Decorator: Retry wraps Transport).

### 4. Directory structure

```
src/
├── Orchestrator1.php         ← root-namespace Orchestrator
├── Handler/                  ← ALL Closures, category subdirs
│   └── Feature1/DoSomething.php
├── Data/                     ← VOs, Enums, Builders
└── Exception/
tests/Support/                ← Test fakes (NOT in src/)
```

### 5. Anti-patterns

| Anti-pattern | Solution |
|---|---|
| Private method identical in 3+ classes | Extract Closure |
| Closure with 2+ public methods | Split |
| Orchestrator with own business logic | Move to Closure |
| Closure > 150 lines | Extract sub-Closures |
| Handlers scattered in feature dirs | Centralise under `Handler/` |
| VOs/Enums in feature dirs | Centralise under `Data/` |
| Test fakes in `src/` | Move to `tests/Support/` |
| `new Handler()` direct call | Bind via `(new Handler())->__invoke(...)` |

### 6. Per-class checklist

- [ ] PHP 8.3+, `declare(strict_types=1)`, PHPStan Level 8 passes
- [ ] PSR-4 namespace matches path
- [ ] Correct layer, dependency direction respected
- [ ] Orchestrator (logic-free, root ns) **or** Closure (`__invoke`, under `Handler/`)
- [ ] All dependencies via Constructor Injection
- [ ] No trait, no `abstract` (except Exception), no `static` (except VO named constructor)
- [ ] If Decorator: outer wraps inner via same signature
