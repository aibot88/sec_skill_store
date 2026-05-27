---
name: backend-architect-implementation-patterns
description: Reference patterns for clean architecture, dependency injection, repository pattern, domain-driven design, error handling, security best practices (parameterized queries, no hardcoded secrets), and common backend anti-patterns. Preloaded into the backend-architect subagent so layer-placement, pattern-selection, and anti-pattern-avoidance decisions during TDD Green phase implementation happen without on-demand reference loads.
version: "1.0"
---

# Implementation Patterns for Backend Architect

**Status**: Preloaded skill (BA-015) | **Agent**: backend-architect

---

## Clean Architecture (Layered)

```
Infrastructure Layer (Repositories, APIs, File I/O)
  Application Layer (Use Cases, Services, DTOs)
    Domain Layer (Entities, Business Logic, Domain Events)

Dependency Flow: Infrastructure -> Application -> Domain
NEVER reverse: Domain MUST NOT depend on Infrastructure
```

## Dependency Injection

**WRONG (Direct Instantiation):**
```python
class OrderService:
    def __init__(self):
        self.repository = OrderRepository()  # Hard dependency!
```

**CORRECT (Dependency Injection):**
```python
class OrderService:
    def __init__(self, repository: IOrderRepository):
        self.repository = repository  # Injected dependency
```

## Single Responsibility Principle

Each class should have ONE reason to change:
- **Entity**: Manages its own state and business rules
- **Repository**: Handles data persistence only
- **Service**: Orchestrates use case only
- **Controller**: Handles HTTP concerns only

## Repository Pattern

**Interface (Domain Layer):**
```python
from abc import ABC, abstractmethod

class IOrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
```

**Implementation (Infrastructure Layer):**
```python
class SqlOrderRepository(IOrderRepository):
    def __init__(self, db_connection):
        self.db = db_connection

    def get_by_id(self, order_id: int) -> Order:
        # Database query logic
        pass

    def save(self, order: Order) -> None:
        # Database save logic
        pass
```

## Domain-Driven Design (DDD)

**Entity (Domain Layer):**
```python
class Order:
    def __init__(self, order_id: int, customer_id: int):
        self.id = order_id
        self.customer_id = customer_id
        self.items = []
        self.status = OrderStatus.PENDING

    def add_item(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items.append(OrderItem(product, quantity))

    def calculate_total(self) -> Decimal:
        return sum(item.get_subtotal() for item in self.items)

    def submit(self):
        if not self.items:
            raise InvalidOperationError("Cannot submit empty order")
        self.status = OrderStatus.SUBMITTED
```

**Value Object (Domain Layer):**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency is required")

    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

## Error Handling

**Domain Exceptions:**
```python
class DomainException(Exception):
    """Base class for domain-specific errors"""
    pass

class InvalidOperationError(DomainException):
    """Operation not allowed in current state"""
    pass

class ValidationError(DomainException):
    """Business rule validation failed"""
    pass
```

## Security Best Practices

### Parameterized Queries (Prevent SQL Injection)
```python
# WRONG: query = f"SELECT * FROM users WHERE email = '{email}'"
# CORRECT:
query = "SELECT * FROM users WHERE email = :email"
result = session.execute(query, {"email": email})
```

### No Hardcoded Secrets
```python
import os
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ConfigurationError("API_KEY not configured")
```

## Anti-Patterns to Avoid

### God Object (>500 lines)
Split into focused classes: OrderService, ShippingCalculator, PaymentProcessor, EmailNotifier.

### Circular Dependencies
Use IDs or one-way dependency instead of bidirectional object references.

### Anemic Domain Model
Entities MUST contain business logic, not just getters/setters. Put calculations, validations, and state transitions in the entity.
