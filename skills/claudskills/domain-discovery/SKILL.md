---
name: domain-discovery
description: DDD/Event Storming skill dlya issledovaniya novogo domena ili bounded context. Ispol'zuj pri zaprose "novyj domen", "event storming", "bounded context", "issledovaniye domena", "domain discovery", "UL nuzhna", "vocabulary".
---

# Domain discovery skill

## When to invoke

Invoked by `domain-researcher` agent, or when operator says:
- "новый bounded context"
- "event storming"
- "исследуем домен"
- "нужна Ubiquitous Language"

## Hard prerequisites

Before starting, verify:

1. `docs/domain/` directory exists (or will be created).
2. The BC name is known. Ask if not.
3. Confirm this is not existing BC evolution — for evolution, use `/plan` and update existing `overview.md`.

## Five-phase interview

### Phase 1: Actors (5 min)

Ask:
> Кто взаимодействует с этим BC? Внешние акторы, внутренние сервисы, автоматические процессы. Минимум 3.

Record as `- ActorName: role (human/service/scheduler/external-system)`.

### Phase 2: Events (past tense, 20 min)

Ask:
> Event Storming. Что уже произошло, что важно для этого BC? В прошедшем времени. Не "выставить счёт" (это команда), а "СчётВыставлен" (это событие).

Cycle through colors:
- **Orange (события)** — что произошло
- **Blue (команды)** — что вызывает событие (в повелительном наклонении)
- **Lilac (политики)** — "когда X, тогда Y"
- **Yellow (агрегаты)** — кто хранит инварианты
- **Green (read models)** — что потребляется для чтения
- **Red (горячие точки)** — неопределённости, разногласия, неизвестное

REFUSE to proceed if < 5 events. Keep pressing until operator surfaces more.

### Phase 3: Boundary (10 min)

Ask:
> Что входит в scope этого BC и что специально НЕ входит? Где проходит граница? И самое важное: **какой термин меняет смысл при переходе через эту границу?** Если ни один — возможно, это не отдельный BC.

Example: "Customer" inside Sales BC = покупатель; "Customer" inside Support BC = тикет-автор. Same word, different concept.

### Phase 4: Ubiquitous Language (15 min)

Ask:
> Минимум 5 терминов. Определения — на языке бизнеса, не технологий. "Order is a Go struct" — плохо. "Order is a customer's commitment to purchase that triggers fulfillment" — хорошо.

Build a table:
| Term | Business definition | Aliases to avoid |

REFUSE if < 5 real terms.

### Phase 5: Context map edges (10 min)

For each other BC the current one interacts with, ask:
> Какой паттерн связи? Shared Kernel / Customer-Supplier / Conformist / Anticorruption Layer / Open Host Service / Published Language / Separate Ways / Big Ball of Mud.

If operator doesn't know these patterns, briefly explain — but insist on picking one. "Just use" is not a pattern.

## Output

Write `docs/domain/<bc-name>/overview.md` per the section table below. This table is the authoritative output schema; `domain-researcher.md` agent output format is a subset used for the discovery phase only.

The output document must include all of the following sections. Sections marked **[discovery]** are produced from the interview. Sections marked **[post-interview]** are authored after the interview using empirical sources (code, ADRs, principles).

| Section | Source | Minimum content |
|---|---|---|
| Purpose | [discovery] Phase 3 | One paragraph: what the BC owns and explicitly does NOT own |
| Actors | [discovery] Phase 1 | ≥ 3 actors with role and authority |
| Commands and Domain Events | [discovery] Phase 2 | ≥ 5 events; commands paired with their emitted events |
| Boundary | [discovery] Phase 3 | In-scope list, out-of-scope list, terms that change meaning at the boundary |
| Aggregate Root | [discovery] Phase 2 | Invariants enumerated explicitly as checkable conditions |
| Policies | [discovery] Phase 2 | Trigger → action pairs (when X, then Y) |
| Context Map | [discovery] Phase 5 | DDD pattern named for each external BC edge |
| **Use Cases** | [post-interview] | ≥ 5 UCs; each with Actor, Preconditions, Main scenario, Alternatives, Postconditions |
| **Domain Data Model** | [post-interview] | Key entities with attributes and valid states; invariants enumerated per entity |
| **Interface Contracts** | [post-interview] | One row per external interface; columns: Operations, Handled failures, Unhandled failures (sourced from code, not inferred) |
| **NFR** | [post-interview] | Only mechanically-verified constraints cited to an existing check or ADR; speculative constraints dropped |
| **Internal Compliance** | [post-interview] | Table: Norm \| Enforcement type \| Artifact \| Honor-system gap? — every DoD norm must appear |
| Red Hotspots | [discovery] | Explicit unresolved questions; "none" requires justification |

**Note on Security:** if the BC has a security model documented in ADRs or runbooks, add a `## Security` section with one-line pointers only — no duplication of content from the source documents. This section is optional for new BCs with no established security model.

## Hand-off

> Domain overview написан в `docs/domain/<bc>/overview.md`. Следующий шаг: `@agent-domain-reviewer docs/domain/<bc>/overview.md`. Если одобрит — commit и продолжайте на `/plan` уровне.

## Hard rules

- НЕ пропускайте phase, даже под давлением "у меня мало времени".
- НЕ принимайте "это очевидно" как ответ. Event Storming очевидное ловит в первой фазе; проблемы — в следующих.
- НЕ проектируйте implementation. Tables, APIs, code — всё в downstream.
- НЕ допускайте БГ (Big Ball of Mud) как постоянный паттерн — это временный статус, требующий рефакторинга.
