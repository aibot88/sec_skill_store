---
name: naming-conventions
description: Use when performing a full naming audit across a codebase, stack profile, or API surface for convention compliance
version: 1.0.0
owner: platform-governance
tier: full
source: .enterprise/governance/agent-skills/naming-conventions/SKILL.md
quick: .enterprise/governance/agent-skills/naming-conventions/SKILL-QUICK.md
portable: true
license: Apache-2.0
---

# Naming Conventions

## When to use
Use this skill when:
- reviewing code for naming compliance
- generating new code artifacts (classes, functions, files, modules)
- onboarding a new stack or language
- enforcing naming in PR review

---

## 1. Universal Semantic Rules (All Stacks)

- NC-01: All names MUST be in **English**.
- NC-02: Names MUST be **descriptive and self-documenting** — the name must reveal intent.
- NC-03: Abbreviations are FORBIDDEN unless universally known: `id`, `url`, `dto`, `api`, `http`, `io`, `db`.
- NC-04: Generic names are FORBIDDEN: `Utils`, `Helpers`, `Manager`, `Common`, `Data`, `Info`, `Handler` (standalone), `Service` (standalone).
- NC-05: Names MUST reflect the **business concept**, not the technical role alone.

### Architectural Concept Naming (mandatory across all stacks)
- NC-06: **Commands** — imperative present tense: `PlaceOrder`, `CancelSubscription`, `UpdateUserProfile`
- NC-07: **Events** — past tense fact: `OrderPlaced`, `SubscriptionCancelled`, `PaymentFailed`
- NC-08: **Queries** — noun or interrogative: `GetOrderById`, `ListActiveSubscriptions`, `FindUserByEmail`
- NC-09: **Aggregates** — singular noun representing the root concept: `Order`, `Customer`, `Payment`
- NC-10: **Repositories** — `I<Aggregate>Repository` (interface) / `<Aggregate>Repository` (implementation)
- NC-11: **Value Objects** — noun describing the value: `Money`, `EmailAddress`, `PhoneNumber`
- NC-12: **DTOs** — suffixed with `Dto` or `Request`/`Response`: `CreateOrderRequest`, `OrderSummaryDto`
- NC-13: **Handlers** — `<Command/Query>Handler`: `PlaceOrderHandler`, `GetOrderByIdHandler`
- NC-14: **Validators** — `<Command/Query>Validator`: `PlaceOrderValidator`
- NC-15: **Ports (interfaces)** — describe capability: `IEmailSender`, `IPaymentGateway`, `IEventPublisher`

---

## 2. C# / .NET Profile

- NC-16: Classes, interfaces, enums, structs, records: `PascalCase`
- NC-17: Public and private methods, properties: `PascalCase`
- NC-18: Private fields: `_camelCase` (underscore prefix)
- NC-19: Local variables and parameters: `camelCase`
- NC-20: Constants: `PascalCase` (C# convention) or `UPPER_SNAKE_CASE` (avoid mixing)
- NC-21: Interfaces: always prefixed with `I` — `IOrderRepository`, `IEmailSender`
- NC-22: Async methods: always suffixed with `Async` — `GetOrderAsync`, `SaveAsync`
- NC-23: Namespaces: `CompanyName.Product.Module.Layer`
- NC-24: Files: one public type per file, file name matches type name

---

## 3. Flutter / Dart Profile

- NC-25: Classes, enums, mixins, extensions: `PascalCase`
- NC-26: Functions, variables, parameters, named constructors: `camelCase`
- NC-27: Private members (class-level): `_camelCase`
- NC-28: Files and folders: `snake_case`
- NC-29: Constant values: `camelCase` (Dart convention for `const`)
- NC-30: Widget classes: `PascalCase`, suffix reflects type — `OrderListScreen`, `PaymentButton`
- NC-31: BLoC/Cubit: `<Feature>Bloc`, `<Feature>Cubit`, `<Feature>State`, `<Feature>Event`
- NC-32: Repository interfaces: `<Feature>Repository` (abstract), `<Feature>RepositoryImpl` (implementation)

---

## 4. React Native / TypeScript Profile

- NC-33: Components (functional and class): `PascalCase`
- NC-34: Custom hooks: `useCamelCase` — `useOrderList`, `useAuthSession`
- NC-35: Regular functions, variables, parameters: `camelCase`
- NC-36: Types and Interfaces: `PascalCase` — `OrderItem`, `UserProfile`
- NC-37: Enums: `PascalCase` members (TypeScript convention)
- NC-38: Folders: `kebab-case` — `order-list/`, `auth-session/`
- NC-39: Files for components: `PascalCase.tsx` — `OrderCard.tsx`
- NC-40: Files for hooks: `useCamelCase.ts` — `useOrderList.ts`
- NC-41: Files for utilities/services: `camelCase.ts`
- NC-42: Constants: `UPPER_SNAKE_CASE` for module-level constants

---

## 5. Java Profile

- NC-43: Classes, interfaces, enums, annotations: `PascalCase`
- NC-44: Methods and variables: `camelCase`
- NC-45: Constants (`static final`): `UPPER_SNAKE_CASE`
- NC-46: Packages: `lowercase.dotted.reverse.domain` — `com.company.product.module`
- NC-47: Interfaces: descriptive noun or capability — `OrderRepository`, `PaymentGateway` (no `I` prefix in Java idiom)
- NC-48: Abstract classes: prefixed with `Abstract` or suffixed with `Base` where appropriate
- NC-49: Test classes: suffixed with `Test` — `OrderServiceTest`

---

## 6. Go Profile

- NC-50: Exported (public) identifiers: `PascalCase`
- NC-51: Unexported (package-private) identifiers: `camelCase`
- NC-52: Acronyms: keep consistent casing — `HTTPClient` or `httpClient` (not `HttpClient`)
- NC-53: Interfaces: short, descriptive nouns; `-er` suffix is idiomatic for single-method interfaces: `Reader`, `Writer`, `Stringer`
- NC-54: Files: `snake_case.go` — `order_repository.go`, `payment_handler.go`
- NC-55: Packages: short, lowercase, single word — `order`, `payment`, `auth`
- NC-56: Test files: `_test.go` suffix — `order_handler_test.go`
- NC-57: Avoid stutter: if package is `order`, don't name the type `OrderOrder`

---

## 7. PHP Profile

- NC-58: Classes, interfaces, traits, enums: `PascalCase`
- NC-59: Methods and functions: `camelCase`
- NC-60: Variables: `camelCase` (or `$camelCase` with PHP's dollar prefix)
- NC-61: Constants: `UPPER_SNAKE_CASE`
- NC-62: Interfaces: suffixed with `Interface` — `OrderRepositoryInterface`
- NC-63: Namespaces: `PascalCase` segments — `App\Domain\Order`
- NC-64: Files: `PascalCase.php` matching class name

---

## 8. C++ Profile

- NC-65: Classes and structs: `PascalCase`
- NC-66: Public methods and functions: `PascalCase` or `camelCase` (choose one, be consistent per project)
- NC-67: Member variables: `camelCase_` (trailing underscore) or `m_camelCase` (choose one per project)
- NC-68: Constants and enums: `kPascalCase` (Google style) or `UPPER_SNAKE_CASE`
- NC-69: Namespaces: `snake_case` or `lowercase`
- NC-70: Header files: `PascalCase.h` or `snake_case.h` (be consistent per project)
- NC-71: Source files: match header file naming

---

## Examples

✅ Good (C#): `PlaceOrderCommand`, `PlaceOrderHandler`, `IOrderRepository`, `_orderService`
✅ Good (Dart): `order_repository.dart`, `class OrderRepository`, `Future<Order> getByIdAsync()`
✅ Good (TS): `OrderCard.tsx`, `useOrderList.ts`, `type OrderItem`

❌ Bad: `OrderManager` (generic role noun)
❌ Bad: `GetData()` (no domain meaning)
❌ Bad: `orderPayed` (misspelling + wrong tense — should be `OrderPaymentConfirmed`)
❌ Bad: `Utils.cs` with 30 unrelated functions


## Quick Mode

For low-context activation, load `.enterprise/governance/agent-skills/naming-conventions/SKILL-QUICK.md` or `QUICK.md` first. Load this full skill for deep analysis, violation fixing, or formal review gates.

