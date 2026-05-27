---
name: preboot-core
description: "Skill do używania biblioteki preboot-core. Użyj tego skilla zawsze gdy użytkownik chce cache z TTL, rate limiting, synchronizację dostępu po kluczu, transakcje programowe, hashowanie parametrów, walidację beanów, konfigurację Jacksona, lub pracuje z infrastrukturą współbieżności. Obejmuje: TTLMap, AccessSynchronizer, RateLimiter, TransactionWrapper, HashUtils, BeanValidator, JsonMapperFactory, JacksonCustomizerAutoConfiguration. Triggeruje się na: TTL cache, rate limiter, token bucket, key-based lock, synchronizacja po kluczu, ReentrantLock, virtual threads, transakcje programowe, REQUIRES_NEW, SHA-1 hash, bean validation, Jackson 3, JsonMapper, auto-configuration, preboot-core, concurrent access, cache eviction, composite key, fair lock."
---

# preboot-core

Moduł fundacyjny PreBoot.io — dostarcza infrastrukturę współbieżności (TTL cache, rate limiter, key-based synchronization), wrappery transakcyjne, narzędzia hashujące, walidację beanów i auto-konfigurację Jacksona 3.

## Zależność Maven

```xml
<dependency>
    <groupId>io.preboot</groupId>
    <artifactId>preboot-core</artifactId>
</dependency>
```

Wersje zarządzane przez `preboot-bom` — nie podawaj `<version>`.

Zależności `provided` — Twój projekt musi mieć Spring Boot Starter. Opcjonalnie `spring-boot-starter-json` dla konfiguracji Jacksona.

## Szybki start

### 1. TTL Cache — cache z automatycznym wygasaniem

```java
// Cache wygasający po 60 sekundach
TTLMap<String, UserSession> sessions = new TTLMap<>(60);

sessions.put("user-123", session);
sessions.put("user-456", anotherSession, 120); // nadpisanie TTL na 120s

UserSession s = sessions.get("user-123"); // null jeśli wygasł
```

### 2. Key-based synchronization — blokowanie po kluczu zasobu

```java
@Service
public class OrderService {
    private final AccessSynchronizer sync = new AccessSynchronizer();

    public Order processOrder(String orderId) {
        return sync.synchronize(orderId, () -> {
            // tylko jeden wątek na dany orderId
            return doExpensiveWork(orderId);
        });
    }
}
```

### 3. Rate limiter — ograniczanie żądań per klient

```java
RateLimiter limiter = new RateLimiter(10); // 10 req/s domyślnie

limiter.acquire("client-A");           // blokuje jeśli limit
boolean ok = limiter.tryAcquire("B");  // nie blokuje, zwraca false
String result = limiter.executeWithRateLimit("C", () -> callApi());
```

### 4. Programowe transakcje

```java
@Service
public class MyService {
    private final TransactionWrapper tx;

    public void doWork() {
        tx.doInTransaction(() -> {
            repo.save(entity);
            repo.delete(old);
        });

        // wymusza nową transakcję (np. dla audytu)
        tx.doAlwaysInNewTransaction(() -> auditRepo.save(log));
    }
}
```

## Główne koncepty

### Auto-konfiguracja

`preboot-core` rejestruje się automatycznie przez Spring Boot auto-configuration (`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`):

1. **PreBootAutoConfiguration** — `@ComponentScan("io.preboot")` — skanuje wszystkie moduły preboot
2. **JsonMapperAutoConfiguration** — rejestruje domyślny `JsonMapper` bean (Jackson 3) jeśli brak
3. **JacksonCustomizerAutoConfiguration** — wyłącza `FAIL_ON_NULL_FOR_PRIMITIVES` (Jackson 3 domyślnie rzuca błąd na null → boolean)

### Współbieżność (pakiet `io.preboot.core.concurent`)

| Klasa | Wzorzec | Zastosowanie |
|-------|---------|-------------|
| `AccessSynchronizer` | Key-based locking z ReentrantLock | Zapobieganie race conditions na tym samym zasobie |
| `RateLimiter` | Token bucket | Ograniczanie API calls per klient |

Oba zaprojektowane z myślą o **Java 21 virtual threads** (ReentrantLock zamiast synchronized).

### Kolekcje (pakiet `io.preboot.core.colections`)

`TTLMap<K, V>` — thread-safe cache z:
- Per-entry TTL (nadpisywalny)
- Background cleanup co 1 sekundę (shared scheduler)
- Opcjonalny eviction callback (`BiConsumer<K, V>`)
- Shutdown hook dla graceful cleanup

### Transakcje (pakiet `io.preboot.core.transaction`)

`TransactionWrapper` — interfejs do programowego zarządzania transakcjami:
- `doInTransaction()` — `@Transactional` (REQUIRED)
- `doAlwaysInNewTransaction()` — `@Transactional(propagation = REQUIRES_NEW)`

Przydatne gdy `@Transactional` na metodzie nie wystarczy (np. część logiki w nowej transakcji).

### Narzędzia

| Klasa | Opis |
|-------|------|
| `HashUtils.getHash(Map)` | SHA-1 hash z parametrów, niezależny od kolejności kluczy |
| `BeanValidator.validate(Object)` | Jakarta Bean Validation — rzuca `ConstraintViolationException` |
| `JsonMapperFactory.createJsonMapper()` | Fabryka skonfigurowanego Jackson 3 `JsonMapper` |

## Typowe przepływy

### Cache sesji z callbackiem na eviction

```java
TTLMap<String, WebSocketSession> activeSessions = new TTLMap<>(300,
    (sessionId, session) -> {
        session.close();
        log.info("Session {} expired", sessionId);
    }
);
```

### Synchronizacja po kluczu złożonym

```java
import static io.preboot.core.concurent.AccessSynchronizer.compositeKey;

sync.synchronize(compositeKey("tenant", tenantId, "order", orderId), () -> {
    // lock per (tenant + order) combo
    return processOrder(tenantId, orderId);
});
```

### Rate limit z custom limitem per klient

```java
RateLimiter limiter = new RateLimiter(5);       // 5 req/s default
limiter.setRateLimit("premium-client", 100);     // premium = 100 req/s

limiter.executeWithRateLimit(clientId, () -> externalApiCall());
```

### Hashowanie parametrów zapytania (cache key)

```java
Map<String, String> params = Map.of("page", "1", "size", "20", "sort", "name");
String cacheKey = HashUtils.getHash(params);
// Zawsze ten sam hash niezależnie od kolejności kluczy w Map
```

### Walidacja obiektu bez Spring kontekstu

```java
@NotNull String name;
@Min(0) int age;

MyDto dto = new MyDto(null, -1);
BeanValidator.validate(dto); // rzuci ConstraintViolationException
```

## Pułapki i częste błędy

1. **TTLMap.close()** — zawsze wywołuj `close()` gdy kończysz używanie mapy (np. w `@PreDestroy`). Inaczej eviction callbacks mogą nie zostać wywołane.

2. **TTLMap.shutdownCleanupService()** — statyczny shutdown. Nie wywoływaj ręcznie — jest automatyczny shutdown hook. Wywołanie zamknie cleanup dla WSZYSTKICH instancji TTLMap.

3. **AccessSynchronizer nie jest distributed** — działa tylko w ramach jednej JVM. Dla distributed locking użyj Redis/Zookeeper.

4. **RateLimiter nie jest distributed** — analogicznie, per-JVM. Dla API gateway rate limiting użyj dedykowanego rozwiązania.

5. **TransactionWrapper wymaga Spring context** — nie zadziała w unit testach bez Spring. Mockuj interfejs `TransactionWrapper` w testach.

6. **Jackson 3 (nie 2)** — `JsonMapperFactory` i auto-konfiguracja używają `tools.jackson.databind` (Jackson 3), nie `com.fasterxml.jackson` (Jackson 2). Upewnij się, że Twój projekt ma Jackson 3 na classpath.

7. **Pakiet `concurent`** — literówka w nazwie (brak drugiego 'r'), ale jest zamierzona i stabilna.

## Kiedy sięgnąć do references/

- **api-reference.md** — pełne sygnatury metod, typy parametrów, wyjątki, szczegóły implementacji
- **examples.md** — więcej przykładów użycia, scenariusze zaawansowane, wzorce integracji z innymi modułami preboot
