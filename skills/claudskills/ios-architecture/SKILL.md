---
name: ios-architecture
description: >
  iOS app architecture expert skill covering MVVM with @Observable, Clean Architecture, The Composable Architecture (TCA),
  modular architecture with SPM, Repository pattern, Coordinator/Router pattern, Dependency Injection (Factory, Environment),
  error handling patterns, and protocol-oriented programming. Use this skill when the user architects an iOS app, designs
  feature modules, sets up project structure, implements MVVM/Clean/TCA patterns, creates repositories or use cases,
  or asks about iOS code organization. Triggers on: architecture, MVVM, clean architecture, TCA, composable architecture,
  repository pattern, coordinator, dependency injection, DI, view model, use case, interactor, modular, SPM package,
  feature module, project structure, folder structure, app architecture, design pattern, unidirectional data flow,
  reducer, store, or any iOS app structure discussion.
---

# iOS Architecture Skill

You are an iOS architecture expert. Apply the patterns and principles below when helping the user design, scaffold, or refactor an iOS application.

---

## Architecture Selection Guide

| Project Size | Team | Recommended | Reference |
|---|---|---|---|
| Small (1 dev, <10 screens) | Solo | MVVM + @Observable | `references/mvvm.md` |
| Medium (2-4 devs, 10-30 screens) | Small team | MVVM + Clean layers | `references/mvvm.md` + `references/clean.md` |
| Large (5+ devs, 30+ screens) | Large team | Clean + SPM modules or TCA | `references/clean.md` + `references/modular.md` |
| Complex state management | Any | TCA | `references/tca.md` |

---

## Core Rules

1. **Default to MVVM + @Observable** for new projects (simplest, Apple-recommended since iOS 17).
2. **ViewModels must NEVER import SwiftUI** -- `import Foundation` only. They expose published state; the View observes it.
3. **Use protocols for all external dependencies** (networking, storage, location, etc.) -- this enables unit testing with mocks.
4. **Domain layer must not import any framework** -- pure Swift only. No UIKit, no SwiftUI, no Combine (unless Combine is used as a reactive primitive in the domain boundary).
5. **Use SPM local packages** for modules when the codebase exceeds ~50k LOC or the team has 3+ developers.
6. **Feature modules never depend on each other** -- they depend only on shared/core modules. Communication goes through a coordinator, router, or parent.
7. **Repository pattern for ALL data access** -- the rest of the app never talks to URLSession, CoreData, or Keychain directly.
8. **Error types flow outward**: `NetworkError` -> `DomainError` -> user-facing localized string. Never expose raw HTTP codes to the UI.
9. **One ViewModel per screen** (not per view). Small subviews can read from the parent ViewModel or accept plain value types.
10. **Prefer value types** (structs, enums) for models and state. Use classes only for reference semantics (ViewModels, services, managers).

---

## Decision Logic

Use this flowchart to decide which reference file to consult:

```
START
  |
  v
Is the question about project-wide architecture or choosing a pattern?
  YES -> Read this file (SKILL.md) first, then the relevant reference.
  NO  -> Continue below.
  |
  v
Is the question about MVVM, @Observable, ViewModels, or View-ViewModel binding?
  YES -> Read references/mvvm.md
  |
  v
Is the question about Clean Architecture, layers, Use Cases, domain entities, or DTOs?
  YES -> Read references/clean.md
  |
  v
Is the question about TCA, Reducers, Store, @ObservableState, Effects, or ComposableArchitecture?
  YES -> Read references/tca.md
  |
  v
Is the question about SPM modules, Package.swift, feature modules, or build times?
  YES -> Read references/modular.md
  |
  v
Is the question about Repository, Coordinator, DI, error handling, POP, or code organization?
  YES -> Read references/patterns.md
  |
  v
Read the most relevant reference based on context, or consult multiple if the question spans areas.
```

---

## Folder Structure Templates

### Simple MVVM (Small project)

```
MyApp/
├── App/
│   ├── MyAppApp.swift
│   └── AppDelegate.swift          (if needed)
├── Features/
│   ├── Home/
│   │   ├── HomeView.swift
│   │   ├── HomeViewModel.swift
│   │   └── Components/            (small subviews)
│   ├── Profile/
│   │   ├── ProfileView.swift
│   │   └── ProfileViewModel.swift
│   └── Settings/
│       ├── SettingsView.swift
│       └── SettingsViewModel.swift
├── Models/
│   ├── User.swift
│   └── Product.swift
├── Services/
│   ├── NetworkService.swift
│   ├── AuthService.swift
│   └── Protocols/
│       ├── NetworkServiceProtocol.swift
│       └── AuthServiceProtocol.swift
├── Repositories/
│   ├── UserRepository.swift
│   └── ProductRepository.swift
├── Utilities/
│   ├── Extensions/
│   └── Helpers/
└── Resources/
    ├── Assets.xcassets
    └── Localizable.xcstrings
```

### Clean Architecture (Medium/Large project)

```
MyApp/
├── App/
│   ├── MyAppApp.swift
│   ├── DIContainer.swift
│   └── AppCoordinator.swift
├── Domain/                        (NO framework imports)
│   ├── Entities/
│   │   ├── User.swift
│   │   └── Product.swift
│   ├── UseCases/
│   │   ├── FetchUserUseCase.swift
│   │   └── PlaceOrderUseCase.swift
│   ├── Repositories/              (protocols only)
│   │   ├── UserRepositoryProtocol.swift
│   │   └── ProductRepositoryProtocol.swift
│   └── Errors/
│       └── DomainError.swift
├── Data/
│   ├── Network/
│   │   ├── APIClient.swift
│   │   ├── Endpoints/
│   │   └── DTOs/
│   ├── Persistence/
│   │   ├── CoreDataStack.swift
│   │   └── UserDAO.swift
│   ├── Repositories/              (implementations)
│   │   ├── UserRepository.swift
│   │   └── ProductRepository.swift
│   └── Mappers/
│       ├── UserMapper.swift
│       └── ProductMapper.swift
├── Presentation/
│   ├── Features/
│   │   ├── Home/
│   │   │   ├── HomeView.swift
│   │   │   └── HomeViewModel.swift
│   │   └── Profile/
│   │       ├── ProfileView.swift
│   │       └── ProfileViewModel.swift
│   ├── Navigation/
│   │   └── Router.swift
│   └── DesignSystem/
│       ├── Components/
│       └── Theme.swift
└── Resources/
```

### TCA (Complex state management)

```
MyApp/
├── App/
│   ├── MyAppApp.swift
│   └── AppFeature.swift           (root reducer)
├── Features/
│   ├── Home/
│   │   ├── HomeFeature.swift      (State, Action, Reducer)
│   │   └── HomeView.swift
│   ├── Profile/
│   │   ├── ProfileFeature.swift
│   │   └── ProfileView.swift
│   └── Auth/
│       ├── AuthFeature.swift
│       └── AuthView.swift
├── Shared/
│   ├── Models/
│   ├── Clients/                   (Dependencies)
│   │   ├── APIClient.swift
│   │   └── UserDefaultsClient.swift
│   └── Components/
└── Resources/
```

---

## Anti-Patterns to Watch For

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Massive ViewController/View | Unreadable, untestable | Extract ViewModel + services |
| ViewModel imports SwiftUI | Couples logic to UI framework | Import Foundation only |
| Singletons for everything | Hidden dependencies, hard to test | Protocol + DI |
| Feature A imports Feature B | Tight coupling, circular deps | Shared module or coordinator |
| Network calls in ViewModel | ViewModel does too much | Repository/Service layer |
| Force unwrapping optionals | Crashes in production | Guard/if-let + error handling |
| God model (one huge struct) | Hard to maintain | Split into domain entities |
| Skipping protocols | Cannot mock, cannot test | Protocol for every external dep |

---

## Testing Strategy per Architecture

| Architecture | Unit Test Target | What to Test |
|---|---|---|
| MVVM | ViewModels | State transitions, service calls, error handling |
| Clean | UseCases + ViewModels | Business logic in isolation, correct layer interaction |
| TCA | Reducers via TestStore | State changes, effects, action sequences |
| All | Repositories (with mocks) | Data mapping, caching logic, error propagation |

---

## Quick Decisions

- **@Observable vs ObservableObject?** -> Use @Observable (iOS 17+). Fall back to ObservableObject only for iOS 16 support.
- **Combine vs async/await?** -> Prefer async/await. Use Combine only for reactive streams (e.g., search debounce, real-time updates).
- **SwiftData vs CoreData?** -> SwiftData for new projects targeting iOS 17+. CoreData if you need CloudKit advanced features or support iOS 16.
- **Factory vs Environment for DI?** -> Factory for services/repositories (app-wide). Environment for design-system values (colors, spacing).
- **Coordinator vs NavigationStack?** -> NavigationStack with a Router @Observable for most SwiftUI apps. UIKit Coordinator only for UIKit-heavy projects.
- **When to add TCA?** -> When you need exhaustive testing of state + effects, or the app has complex interdependent state.
- **When to modularize?** -> When build times exceed 30s, or multiple devs step on each other in the same target.

---

## References

Read the appropriate reference file for detailed patterns, code examples, and implementation guidance:

- `references/mvvm.md` -- MVVM with @Observable, ViewModel patterns, testing
- `references/clean.md` -- Clean Architecture layers, DI, Use Cases
- `references/tca.md` -- The Composable Architecture patterns
- `references/modular.md` -- SPM modules, feature modules, build optimization
- `references/patterns.md` -- Repository, Coordinator, error handling, POP, DI, code organization
