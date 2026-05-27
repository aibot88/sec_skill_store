---
name: preboot-query
description: "Skill do używania biblioteki preboot-query. Użyj tego skilla zawsze gdy użytkownik chce implementować dynamiczne filtrowanie, sortowanie, paginację, repozytorium z wyszukiwaniem, REST API z filtrowaniem, projekcje, eksport danych, lub pracuje z Spring Data JDBC i potrzebuje dynamicznych zapytań. Obejmuje: FilterableRepository, FilterableUuidRepository, FilterCriteria, SearchParams, SearchRequest, FilterableController, CrudFilterableController, UuidFilterableController, CrudUuidFilterableController, AggregateReference, projekcje SpEL, SortOrder, eksport danych. Triggeruje się na: dynamic filtering, search, pagination, sorting, filterable repository, criteria query, Spring Data JDBC query, REST API search, CRUD controller, export CSV XLSX, projection, aggregate reference, UUID repository, database view, ILIKE, between, IN operator, nested filtering, OR AND conditions, complex query, SearchParams, FilterCriteria, findAll with filters, page size, unpaged."
---

# preboot-query

Moduł rozszerzający Spring Data JDBC o dynamiczne filtrowanie, sortowanie, paginację i projekcje. Generuje SQL w runtime na podstawie kryteriów — bez pisania custom queries. Optymalizowany pod PostgreSQL.

## Zależność Maven

```xml
<dependency>
    <groupId>io.preboot</groupId>
    <artifactId>preboot-query</artifactId>
</dependency>
```

Wersje zarządzane przez `preboot-bom` — nie podawaj `<version>`.

Wymaga: `preboot-core`, `preboot-exporters-api` (transitive), `spring-boot-starter-data-jdbc`, `postgresql`.
Opcjonalnie: `spring-boot-starter-web` (dla kontrolerów REST), `springdoc-openapi` (dla OpenAPI docs).

## Szybki start

### 1. Zdefiniuj encję

```java
@Table("orders")
@Data
public class Order {
    @Id
    private Long id;
    private String orderNumber;
    private BigDecimal amount;
    private String status;
    private LocalDateTime createdAt;

    @MappedCollection(idColumn = "order_id")
    private Set<OrderItem> orderItems = new HashSet<>();
}
```

### 2. Stwórz interfejs repozytorium

```java
public interface OrderRepository extends FilterableRepository<Order, Long> {}
```

### 3. Zaimplementuj repozytorium

```java
@Repository
class OrderRepositoryImpl extends FilterableFragmentImpl<Order, Long> {
    public OrderRepositoryImpl(FilterableFragmentContext context) {
        super(context, Order.class);
    }
}
```

### 4. Filtruj

```java
SearchParams params = SearchParams.criteria(
    FilterCriteria.eq("status", "COMPLETED"),
    FilterCriteria.gt("amount", new BigDecimal("100"))
).build();

Page<Order> orders = orderRepository.findAll(params);
```

### 5. (Opcjonalnie) Wystaw REST API

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController extends CrudFilterableController<Order, Long> {
    public OrderController(OrderRepository repository) {
        super(repository);
    }
}
```

Gotowe endpointy: `GET /{id}`, `POST /search`, `POST /find`, `POST /count`, `POST /`, `PUT /{id}`, `PATCH /{id}`, `DELETE /{id}`.

## Główne koncepty

### Architektura

```
FilterableRepository<T, ID>
├── extends CrudRepository<T, ID>         — standardowe CRUD
└── extends FilterableFragment<T>          — dynamiczne filtrowanie
    ├── findAll(SearchParams)              → Page<T>
    ├── findAllAsStream(SearchParams)      → Stream<T>
    ├── findOne(SearchParams)              → Optional<T>
    ├── count(SearchParams)                → long
    ├── findAllProjectedBy(params, type)   → Page<P>
    └── findOneProjectedBy(params, type)   → Optional<P>

FilterableUuidRepository<T extends HasUuid, ID>
├── extends FilterableRepository<T, ID>
└── extends UuidRepository<T>              — findByUuid, existsByUuid, deleteByUuid
```

### Kluczowe klasy

| Klasa | Rola |
|-------|------|
| `FilterableRepository<T, ID>` | Interfejs repozytorium — CrudRepository + filtrowanie |
| `FilterableUuidRepository<T, ID>` | Jak wyżej + operacje UUID |
| `FilterableFragmentImpl<T, ID>` | Implementacja bazowa — rozszerzasz ją w swoim repo |
| `FilterableUuidFragmentImpl<T, ID>` | Jak wyżej + UUID (findByUuid, deleteByUuid) |
| `FilterableFragmentContext` | `@Service` — agreguje wszystkie zależności (JdbcTemplate, SqlBuilder, etc.) |
| `SearchParams` | Parametry wyszukiwania — filtry, paginacja, sortowanie |
| `FilterCriteria` | Kryterium filtrowania — operatory eq, neq, like, gt, lt, between, in, etc. |
| `SortOrder` | Sortowanie — `SortOrder.asc("field")`, `SortOrder.desc("field")` |
| `@AggregateReference` | Adnotacja — relacja do innego agregatu (JOIN w zapytaniach) |
| `HasUuid` | Interfejs — encja z UUID (getUuid/setUuid) |
| `FilterableController<T, ID>` | REST controller — read-only z filtrowaniem |
| `CrudFilterableController<T, ID>` | REST controller — pełne CRUD + filtrowanie |
| `UuidFilterableController<T, ID>` | REST controller — read-only z UUID |
| `CrudUuidFilterableController<T, ID>` | REST controller — pełne CRUD z UUID |
| `SearchRequest` | Record — JSON body dla POST /search |
| `ExportRequest` | Record — JSON body dla POST /export/{format} |

### Hierarchia kontrolerów

```
FilterableController<T, ID>              — GET /{id}, POST /search, /find, /count, /export
└── CrudFilterableController<T, ID>      — + POST /, PUT /{id}, PATCH /{id}, DELETE /{id}

UuidFilterableController<T, ID>          — GET /{uuid}, POST /search, /find, /count, /export
└── CrudUuidFilterableController<T, ID>  — + POST /, PUT /{uuid}, PATCH /{uuid}, DELETE /{uuid}
```

### Operatory filtrowania

| Operator | Metoda | SQL | Opis |
|----------|--------|-----|------|
| `eq` | `FilterCriteria.eq(field, value)` | `= :val` | Equals (case-sensitive) |
| `neq` | `FilterCriteria.neq(field, value)` | `!= :val` | Not equals |
| `eqic` | `FilterCriteria.eqic(field, value)` | `LOWER(col) = LOWER(:val)` | Equals (case-insensitive) |
| `like` | `FilterCriteria.like(field, value)` | `ILIKE :val%` | Pattern matching (case-insensitive) |
| `gt` | `FilterCriteria.gt(field, value)` | `> :val` | Greater than |
| `lt` | `FilterCriteria.lt(field, value)` | `< :val` | Less than |
| `gte` | `FilterCriteria.gte(field, value)` | `>= :val` | Greater than or equal |
| `lte` | `FilterCriteria.lte(field, value)` | `<= :val` | Less than or equal |
| `between` | `FilterCriteria.between(field, from, to)` | `BETWEEN :from AND :to` | Between (inclusive) |
| `in` | `FilterCriteria.in(field, values...)` | `IN (:vals)` | Value in set |
| `notin` | `FilterCriteria.notIn(field, values...)` | `NOT IN (:vals)` | Value not in set |
| `ao` | `FilterCriteria.ao(field, values...)` | `&& ARRAY[:vals]` | Array overlap (PostgreSQL) |
| `isnull` | `FilterCriteria.isNull(field)` | `IS NULL` | Is null |
| `isnotnull` | `FilterCriteria.isNotNull(field)` | `IS NOT NULL` | Is not null |

### Logiczne AND/OR

```java
// OR
FilterCriteria.or(List.of(
    FilterCriteria.eq("status", "COMPLETED"),
    FilterCriteria.eq("status", "PENDING")
));

// AND (explicit)
FilterCriteria.and(List.of(
    FilterCriteria.eq("status", "COMPLETED"),
    FilterCriteria.gt("amount", 200)
));

// Domyślnie wiele kryteriów w SearchParams.criteria() = AND
SearchParams.criteria(
    FilterCriteria.eq("status", "COMPLETED"),   // AND
    FilterCriteria.gt("amount", 200)             // AND
).build();
```

### Zależności od innych modułów PreBoot

- **preboot-core** (wymagane) — `JsonMapper`, utilities
- **preboot-exporters-api** (wymagane) — `DataExporter` interfejs dla eksportu danych
- **preboot-securedata** (opcjonalnie) — rozszerza o multi-tenant security

## Typowe przepływy

### Filtrowanie + paginacja + sortowanie

```java
SearchParams params = SearchParams.builder()
    .page(0)
    .size(20)
    .sort(List.of(SortOrder.desc("amount"), SortOrder.asc("status")))
    .filters(List.of(
        FilterCriteria.eq("status", "COMPLETED"),
        FilterCriteria.gt("amount", new BigDecimal("100"))
    ))
    .build();

Page<Order> result = orderRepository.findAll(params);
```

### Encja z UUID

```java
@Table("orders")
public class Order implements HasUuid {
    @Id private Long id;
    private UUID uuid;
    // ... pola

    @Override public UUID getUuid() { return uuid; }
    @Override public void setUuid(UUID uuid) { this.uuid = uuid; }
}

public interface OrderRepository extends FilterableUuidRepository<Order, Long> {}

@Repository
class OrderRepositoryImpl extends FilterableUuidFragmentImpl<Order, Long> {
    public OrderRepositoryImpl(FilterableFragmentContext context) {
        super(context, Order.class);
    }
}

// Użycie:
Optional<Order> order = orderRepository.findByUuid(uuid);
orderRepository.deleteByUuid(uuid);
```

### Projekcje z @Value (SpEL)

```java
public interface OrderSummary {
    String getOrderNumber();
    BigDecimal getAmount();

    @Value("#{target.amount > 150 ? 'High Value' : 'Standard'}")
    String getValueCategory();
}

Page<OrderSummary> summaries = orderRepository.findAllProjectedBy(
    SearchParams.empty(), OrderSummary.class
);
```

### REST API — JSON request

```json
POST /api/orders/search
{
  "page": 0,
  "size": 20,
  "sort": [
    {"field": "amount", "direction": "DESC"}
  ],
  "filters": [
    {"field": "status", "operator": "eq", "value": "COMPLETED"},
    {"field": "amount", "operator": "gt", "value": 100}
  ]
}
```

### Nested filtering (relacje)

```java
SearchParams params = SearchParams.criteria(
    FilterCriteria.eq("orderItems.productCode", "PROD-A"),
    FilterCriteria.gt("orderItems.quantity", 3)
).build();

Page<Order> orders = orderRepository.findAll(params);
```

### Database views

```java
@Table("v_order_summary")
@Data
public class OrderSummaryView {
    @Id private Long id;
    @Column("order_number") private String orderNumber;
    private BigDecimal amount;
    private String status;
    @Column("item_count") private Long itemCount;
}

public interface OrderSummaryViewRepository extends FilterableRepository<OrderSummaryView, Long> {}

@Repository
class OrderSummaryViewRepositoryImpl extends FilterableFragmentImpl<OrderSummaryView, Long> {
    public OrderSummaryViewRepositoryImpl(FilterableFragmentContext context) {
        super(context, OrderSummaryView.class);
    }
}
```

## Pułapki i częste błędy

1. **Brak implementacji repozytorium** — sam interfejs `extends FilterableRepository` nie wystarczy. Musisz stworzyć `*Impl` rozszerzający `FilterableFragmentImpl`. Nazwa klasy MUSI kończyć się na `Impl` i odpowiadać nazwie interfejsu.

2. **`@Immutable` na encji widoku** — NIE używaj `@Immutable` z Spring Data JDBC na encjach widoków. W Spring Data JDBC 4.0.0 powoduje to null we wszystkich polach.

3. **Nazewnictwo kolumn w widokach** — jeśli kolumna widoku ma alias inny niż snake_case pola Java, użyj `@Column("alias")`. Spring Data JDBC konwertuje `camelCase` → `snake_case` automatycznie.

4. **like operator dodaje `%` automatycznie** — `FilterCriteria.like("name", "ORD")` generuje `ILIKE 'ORD%'`. Nie dodawaj `%` sam.

5. **UUID entity bez HasUuid** — jeśli chcesz `findByUuid()`, encja MUSI implementować `HasUuid`, repo `FilterableUuidRepository`, impl `FilterableUuidFragmentImpl`.

6. **Async EventPublisher z kontrolerami eksportu** — asynchroniczny eksport wymaga `QueryControllersPort` — bez niego `isAsyncExportSupported()` zwraca `false`.

7. **Max page size** — domyślnie 100. Przekroczenie zwraca 400 Bad Request. Override `getMaxPageSize()` w kontrolerze jeśli potrzebujesz więcej.

8. **Sort precedence** — gdy podasz zarówno `sortField`/`sortDirection` jak i `sort`, `sort` wygrywa. `sortField`/`sortDirection` jest deprecated.

9. **Brak `FilterableFragmentContext` beana** — ten bean jest `@Service` i wymaga `NamedParameterJdbcTemplate`, `SqlBuilder`, `RelationalMappingContext`, `JdbcConverter`, `ConversionService`, `JdbcAggregateTemplate`, `PropertyResolver` w kontekście. Wszystkie są auto-konfigurowane przez Spring Boot.

10. **between z null** — `FilterCriteria.between(field, null, to)` rzuci `IllegalArgumentException`. Oba argumenty muszą być non-null.

## Kiedy sięgnąć do references/

- **api-reference.md** — pełne sygnatury metod, parametry, wyjątki, hierarchia kontrolerów, hooki CRUD
- **examples.md** — kompletne przykłady: filtrowanie, OR/AND, projekcje, @AggregateReference, kontrolery REST, JSON requests, widoki bazodanowe, eksport, testowanie
