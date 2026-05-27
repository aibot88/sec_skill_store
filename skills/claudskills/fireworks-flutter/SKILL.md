---
name: fireworks-flutter
version: 3.0.0
author: mneme
description: Use when building Flutter/Dart apps, debugging Flutter issues, reviewing Flutter PRs, choosing state management, testing widgets/providers, optimizing Flutter performance, or auditing mobile security. Covers Flutter 3.38, Dart 3.10, Riverpod 3.0, BLoC 9.x, GoRouter, clean architecture, Impeller, OWASP Mobile Top 10.
triggers:
  - flutter
  - dart
  - widget
  - riverpod
  - bloc
  - mobile
  - ios
  - android
  - pubspec
  - freezed
  - go_router
  - pigeon
  - impeller
tags:
  - flutter
  - dart
  - mobile
  - state-management
  - riverpod
  - bloc
  - widgets
  - testing
  - ios
  - android
---

# Fireworks Flutter v3.0 — Master Skill

> The definitive Flutter & Dart development skill for Claude Code.
> Covers architecture, state management, navigation, animations, platform channels, testing, premium UI, and security.
> **Compound skill** — auto-chains to `fireworks-test`, `fireworks-security`, `fireworks-debug` when relevant.

---

## 1. Flutter Development Protocol

Every Flutter task follows this pipeline:

1. **Understand** — Read the requirement. Clarify ambiguity before writing code.
2. **Architect** — Choose architecture pattern (clean arch for features, simple for prototypes).
3. **Scaffold** — Create directory structure, define models, interfaces, and routes.
4. **Implement** — Write code feature-by-feature, smallest testable unit first.
5. **Test** — Widget tests for every screen, unit tests for logic, integration tests for flows.
6. **Analyze** — Run `flutter analyze` — zero warnings, zero errors.
7. **Verify** — Run on device/emulator. Check both light AND dark themes.
8. **Deploy** — Build release, test release mode, deliver.

### Mandatory Commands Before Claiming Done

```bash
flutter analyze          # Must show: No issues found!
flutter test             # Must show: All tests passed!
dart format lib/ test/   # Code must be formatted
```

### Dart 3.7-3.10 Language Features

| Feature | Dart | Example |
|---|---|---|
| Wildcard `_` | 3.7 | `for (final (name, _, _) in records)` |
| New formatter | 3.7 | Better trailing comma handling |
| Null-aware collections | 3.8 | `[?Text(subtitle), ...?extraTags]` |
| Dot shorthands | 3.10 | `.all(16)` instead of `EdgeInsets.all(16)` |
| Augmentations | 3.10 | Replaces cancelled macros, same codegen workflow |
| Build hooks | 3.10 | Native code compilation without shell scripts |

See `references/dart-modern-features.md` for full examples and migration tips.

### Decision: When NOT to Use Flutter

- Pure backend service -> Use Dart server (shelf/dart_frog) or other backend
- Simple static website -> Use HTML/CSS or Next.js
- Heavy 3D graphics -> Use Unity/Unreal with Flutter embedding
- Native-only feature -> Write platform channel, not pure Flutter

---

## 2. Project Structure (Clean Architecture)

```
lib/
  core/                         # Shared across ALL features
    constants/
      app_constants.dart        # App-wide constants
      api_endpoints.dart        # API URLs
    error/
      exceptions.dart           # Custom exceptions
      failures.dart             # Failure classes for Either
    theme/
      app_theme.dart            # ThemeData for light/dark
      app_colors.dart           # ColorScheme definitions
      app_text_styles.dart      # TextTheme definitions
      theme_extensions.dart     # Custom ThemeExtension<T>
    utils/
      extensions.dart           # Dart extension methods
      validators.dart           # Form validators
      formatters.dart           # Date, currency formatters
    widgets/                    # Shared reusable widgets
      app_button.dart
      app_text_field.dart
      loading_indicator.dart
      error_widget.dart
      shimmer_loading.dart
  features/                     # Feature-first organization
    auth/
      data/
        datasources/
          auth_remote_datasource.dart
          auth_local_datasource.dart
        models/
          user_model.dart       # JSON serialization, fromJson/toJson
        repositories/
          auth_repository_impl.dart
      domain/
        entities/
          user.dart             # Pure Dart class, no dependencies
        repositories/
          auth_repository.dart  # Abstract interface
        usecases/
          login_usecase.dart
          logout_usecase.dart
          get_current_user_usecase.dart
      presentation/
        pages/
          login_page.dart
          register_page.dart
        widgets/
          login_form.dart
          social_login_buttons.dart
        providers/              # Riverpod providers (or bloc/)
          auth_provider.dart
          auth_state.dart
    home/
      data/
      domain/
      presentation/
    settings/
      data/
      domain/
      presentation/
  app.dart                      # MaterialApp.router setup
  main.dart                     # Entry point, ProviderScope
test/
  core/
    utils/
  features/
    auth/
      data/
        repositories/
      domain/
        usecases/
      presentation/
        pages/
    home/
  helpers/
    test_helpers.dart           # Shared test utilities
    pump_app.dart               # Helper to pump widget with providers
    mock_data.dart              # Shared mock data
integration_test/
  app_test.dart
```

### When to Use Clean Architecture

| Project Size | Recommendation |
|-------------|---------------|
| Prototype / POC | Single folder, no layers. Speed over structure. |
| Small app (< 5 screens) | Feature folders with simple separation. |
| Medium app (5-20 screens) | Full clean architecture per feature. |
| Enterprise app (20+ screens) | Clean architecture + modular packages. |

---

## 3. State Management Decision Tree

| Scenario | Recommended | Why |
|----------|------------|-----|
| Simple local UI state (toggle, counter) | `setState` / `ValueNotifier` | Minimal overhead, no dependencies |
| Form state with validation | `TextEditingController` + `ValueNotifier` | Built-in, no extra packages |
| Feature-level state with async | **Riverpod 3.0** | Compile-time safety, auto-disposal, no BuildContext |
| Enterprise/regulated app (audit trail) | **BLoC 9.0** | Event-driven, strict separation, replay/undo |
| Legacy app with existing Provider | **Provider** | Don't rewrite what works |
| Global app state (auth, theme, locale) | **Riverpod** | Dependency injection built-in, testable |
| Real-time data (WebSocket, Firestore) | **Riverpod StreamProvider** or **BLoC** | Stream-native support |
| Complex UI with many interdependent states | **Riverpod** | Provider composition, granular rebuilds |

### Key Rule: Never Mix State Management Libraries

Pick ONE primary state management solution per project. Using Riverpod + BLoC + Provider in the same app creates confusion.

---

---

## Full Reference

For complete patterns, examples, and advanced usage, see [`references/full-guide.md`](./references/full-guide.md).
Read that file when you need deeper context than the summary above.
