---
name: spring-boot-core
description: Spring Boot 4.0 + Java 25 development - auto-configuration, starters, Actuator, profiles, externalized config, security, and production patterns. Use when building backend apps, creating endpoints, configuring Spring, or asking "how do I set up X?"
---

# Spring Boot Core Skill

Modern backend development with Spring Boot 4.0, Spring Framework 7, Java 25, and Jakarta EE 11.

## Core Workflow

1. **Analyze** - Understand requirements, identify domain model, API contracts, and data flow
2. **Design** - Plan package structure, entity relationships, confirm architecture before coding
3. **Implement** - Build with layered architecture (Controller → Service → Repository)
4. **Secure** - Apply Spring Security 7, Bean Validation, CORS, error handling
5. **Test** - Write unit (JUnit 6), slice (@WebMvcTest, @DataJpaTest), integration (Testcontainers) tests
6. **Deploy** - Configure Docker, Actuator health checks, observability, deploy

## Quick Start Templates

### Application Entry Point
```java
package com.example.myapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyAppApplication {

    public static void main(String[] args) {
        SpringApplication.run(MyAppApplication.class, args);
    }
}
```

### Entity with Auditing
```java
package com.example.myapp.user;

import jakarta.persistence.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "users")
@EntityListeners(AuditingEntityListener.class)
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserRole role = UserRole.USER;

    @Version
    private Long version;

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    @Column(nullable = false)
    private Instant updatedAt;

    protected User() {} // JPA requires no-arg constructor

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    // Getters (no setters for immutable fields)
    public UUID getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public UserRole getRole() { return role; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }

    public void updateName(String name) { this.name = name; }
    public void assignRole(UserRole role) { this.role = role; }
}
```

### Request/Response Records (DTOs)
```java
package com.example.myapp.user.dto;

import jakarta.validation.constraints.*;

public record CreateUserRequest(
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    String name,

    @NotBlank @Email(message = "Valid email is required")
    String email
) {}

public record UserResponse(
    UUID id,
    String name,
    String email,
    String role,
    Instant createdAt
) {
    public static UserResponse from(User user) {
        return new UserResponse(
            user.getId(),
            user.getName(),
            user.getEmail(),
            user.getRole().name(),
            user.getCreatedAt()
        );
    }
}
```

### Repository
```java
package com.example.myapp.user;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.role = :role")
    Page<User> findByRole(@Param("role") UserRole role, Pageable pageable);
}
```

### Service
```java
package com.example.myapp.user;

import com.example.myapp.common.exception.ResourceNotFoundException;
import com.example.myapp.common.exception.DuplicateResourceException;
import com.example.myapp.user.dto.CreateUserRequest;
import com.example.myapp.user.dto.UserResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public Page<UserResponse> findAll(Pageable pageable) {
        return userRepository.findAll(pageable).map(UserResponse::from);
    }

    @Transactional(readOnly = true)
    public UserResponse findById(UUID id) {
        return userRepository.findById(id)
            .map(UserResponse::from)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @Transactional
    public UserResponse create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new DuplicateResourceException("User", "email", request.email());
        }

        var user = new User(request.name(), request.email());
        return UserResponse.from(userRepository.save(user));
    }
}
```

### Controller
```java
package com.example.myapp.user;

import com.example.myapp.user.dto.CreateUserRequest;
import com.example.myapp.user.dto.UserResponse;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public Page<UserResponse> findAll(Pageable pageable) {
        return userService.findAll(pageable);
    }

    @GetMapping("/{id}")
    public UserResponse findById(@PathVariable("id") UUID id) {
        return userService.findById(id);
    }

    @PostMapping
    public ResponseEntity<UserResponse> create(@Valid @RequestBody CreateUserRequest request) {
        var response = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
```

### Global Exception Handler (RFC 9457)
```java
package com.example.myapp.common.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.net.URI;
import java.util.Map;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Resource Not Found");
        problem.setType(URI.create("https://api.example.com/errors/not-found"));
        problem.setProperty("resource", ex.getResourceName());
        return problem;
    }

    @ExceptionHandler(DuplicateResourceException.class)
    public ProblemDetail handleDuplicate(DuplicateResourceException ex) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
        problem.setTitle("Duplicate Resource");
        problem.setType(URI.create("https://api.example.com/errors/duplicate"));
        return problem;
    }

    @Override
    protected ProblemDetail handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex, ...) {
        var errors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(
                e -> e.getField(),
                e -> e.getDefaultMessage(),
                (a, b) -> a
            ));
        var problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, "Validation failed");
        problem.setTitle("Validation Error");
        problem.setType(URI.create("https://api.example.com/errors/validation"));
        problem.setProperty("errors", errors);
        return problem;
    }
}
```

### Security Configuration
```java
package com.example.myapp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable()) // Stateless JWT API
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health/**", "/actuator/info").permitAll()
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/public/**").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    }
}
```

### Application Configuration
```yaml
# application.yml
spring:
  application:
    name: my-service
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}
  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/mydb}
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:secret}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 20000
      idle-timeout: 300000
      max-lifetime: 1200000
  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
    properties:
      hibernate:
        default_batch_fetch_size: 20
        order_inserts: true
        order_updates: true
  flyway:
    enabled: true
    locations: classpath:db/migration
  threads:
    virtual:
      enabled: true

server:
  port: ${SERVER_PORT:8080}
  shutdown: graceful

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  metrics:
    tags:
      application: ${spring.application.name}

springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
```

### Flyway Migration
```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name       VARCHAR(100)    NOT NULL,
    email      VARCHAR(255)    NOT NULL UNIQUE,
    role       VARCHAR(20)     NOT NULL DEFAULT 'USER',
    version    BIGINT          NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_role  ON users (role);
```

## Reference Guide

Load detailed patterns based on context:

| Topic | Reference | When to Load |
|-------|-----------|-------------|
| Configuration | `references/configuration.md` | Profiles, properties, externalized config |
| Architecture | `references/architecture.md` | Package structure, layering, DDD patterns |
| Error Handling | `references/error-handling.md` | RFC 9457, exceptions, validation errors |
| Security | `references/security.md` | Spring Security 7, JWT, CORS, CSRF |
| Data Access | `references/data-access.md` | JPA, Flyway, HikariCP, caching |

## Constraints

### MUST DO
- Constructor injection — no `@Autowired` on fields
- Records for DTOs — no mutable request/response POJOs
- `@Transactional` on service methods — not controllers
- `@Transactional(readOnly = true)` on query-only methods
- `@Valid` on all `@RequestBody` parameters
- RFC 9457 `ProblemDetail` for all error responses
- Flyway migrations for schema changes — `ddl-auto=validate`
- `spring.jpa.open-in-view=false`
- `server.shutdown=graceful`
- Feature-based package structure

### MUST NOT DO
- Field injection (`@Autowired` on fields)
- `WebSecurityConfigurerAdapter` (removed in Spring Security 6+)
- `ddl-auto=create/update` in any profile except local dev
- Raw types (List, Map without generics)
- String concatenation in SQL queries
- `CascadeType.ALL` without careful consideration
- `Optional` as method parameter or entity field
- Catching `Exception` or `Throwable` broadly
- Returning entity objects directly from controllers (use DTOs)
- Hardcoding URLs, credentials, or environment-specific values

## Architecture Patterns

**Project Structure:**
```
src/main/java/com/example/myapp/
  MyAppApplication.java               # @SpringBootApplication (root package)
  config/                              # Configuration classes
    SecurityConfig.java
    OpenApiConfig.java
    WebConfig.java
  common/                              # Shared utilities
    exception/
      GlobalExceptionHandler.java
      ResourceNotFoundException.java
      DuplicateResourceException.java
    dto/
      PageResponse.java
    audit/
      AuditableEntity.java
  user/                                # Feature module
    User.java                          # Entity
    UserRole.java                      # Enum
    UserRepository.java
    UserService.java
    UserController.java
    dto/
      CreateUserRequest.java
      UpdateUserRequest.java
      UserResponse.java
  order/                               # Another feature module
    Order.java
    OrderService.java
    OrderController.java
    ...
src/main/resources/
  application.yml
  application-dev.yml
  application-prod.yml
  db/migration/
    V1__create_users_table.sql
    V2__create_orders_table.sql
src/test/java/                         # Mirrors main package structure
```

**Layered Architecture:**
- Controller → receives HTTP request, validates input, delegates to Service
- Service → business logic, transactions, orchestration
- Repository → data access, queries, persistence
- Entity → JPA-managed domain object
- DTO (Record) → request/response data transfer

**Data Flow:**
- POST → Controller `@Valid` → Service `@Transactional` → Repository → Entity → DB
- GET → Controller → Service `@Transactional(readOnly)` → Repository → Projection/DTO → Response

## Knowledge Base

Spring Boot 4.0, Spring Framework 7.0, Spring Security 7.0, Spring Data JPA 2025.1, Hibernate 7.1, Jakarta EE 11, Java 25, Flyway, HikariCP, SpringDoc OpenAPI 3.0, JUnit 6, Mockito 6, Testcontainers 2.0, Micrometer, OpenTelemetry, Gradle 9.x, Docker
