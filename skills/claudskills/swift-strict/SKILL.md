---
name: swift-strict
description: >
  Swift/SwiftUI strictness, clean code, and security rules. Use when writing, reviewing,
  or refactoring Swift code in iOS/macOS projects. Covers force unwrap prevention,
  @Observable vs ObservableObject patterns, access control, concurrency safety
  (@MainActor, actors, Sendable), error handling with typed enums, memory leak
  prevention, guard-first style, and naming conventions. Derived from production iOS apps.
---

# Swift Strict Standard

Rules extracted from 3 production SwiftUI iOS apps.

## CRITICAL: Unwrapping Rules

### SW-01: Never force unwrap in production code

```swift
// BAD
let name = user!.name
let url = URL(string: urlString)!
let day = calendar.date(byAdding: .day, value: -1, to: date)!

// GOOD
guard let name = user?.name else { return }
guard let url = URL(string: urlString) else {
    throw AppError.invalidURL(urlString)
}
guard let day = calendar.date(byAdding: .day, value: -1, to: date) else { return }
```

Exceptions (very rare, must justify):
- `fatalError()` in `required init?(coder:)` for programmatic-only views
- `@IBOutlet` connections (but prefer programmatic UI)

### SW-02: Use `guard let` for early returns, `if let` for scoped binding

```swift
// GOOD: guard for early exit (preferred pattern)
func listNotes(in folder: String) -> [Note] {
    guard let root = cloud.stikRoot else { return [] }
    guard let files = try? fm.contentsOfDirectory(at: root) else { return [] }
    return files.filter { ... }
}

// GOOD: if let when value only needed in branch
if let fileName = removed.photoFilename {
    let url = Self.photosDir.appendingPathComponent(fileName)
    try? fm.removeItem(at: url)
}
```

Default to guard. Use if-let only when the value is needed for one branch.

### SW-03: Avoid `try?` for critical operations

```swift
// BAD: silently swallows error
try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)

// GOOD: handle or propagate
do {
    try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
} catch {
    logger.error("Failed to create directory: \(error)")
    throw AppError.fileSystemError(error)
}

// ACCEPTABLE: truly optional operations
try? fm.removeItem(at: tempFile) // Cleanup, failure is OK
```

## CRITICAL: Error Handling

### SW-04: Custom error enums with LocalizedError

```swift
enum AppError: LocalizedError {
    case invalidFolderName
    case containerUnavailable
    case networkUnavailable
    case unauthorized
    case serverError(Int)

    var errorDescription: String? {
        switch self {
        case .invalidFolderName: String(localized: "error_invalid_folder")
        case .containerUnavailable: String(localized: "error_container")
        case .networkUnavailable: String(localized: "error_network")
        case .unauthorized: String(localized: "error_unauthorized")
        case .serverError(let code): String(localized: "error_server \(code)")
        }
    }
}
```

### SW-05: Use Result type for async callbacks

```swift
func handleAppleSignIn(result: Result<ASAuthorization, Error>) async {
    switch result {
    case .success(let auth):
        await processAppleCredential(auth)
    case .failure(let error):
        lastError = .unknown(error)
    }
}
```

## HIGH: State Management

### SW-06: Use @Observable (iOS 17+), not ObservableObject

```swift
// BAD: old pattern
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false
}
// Requires @StateObject in view

// GOOD: modern pattern
@Observable
final class ViewModel {
    var items: [Item] = []
    var isLoading = false
}
// Uses @State in view (simpler)
```

@ObservationIgnored for non-reactive internals:
```swift
@Observable final class EditorViewModel {
    var content: String = ""

    @ObservationIgnored
    private var autosaveTask: Task<Void, Never>?
}
```

### SW-07: @State for view-local, @Environment for injected

```swift
struct HomeView: View {
    @State private var viewModel = HomeViewModel()    // View owns it
    @Environment(\.dismiss) private var dismiss        // System injection

    var body: some View { ... }
}
```

Never use `@StateObject` in new code targeting iOS 17+.

### SW-08: Singletons must be @Observable with private(set)

```swift
@Observable final class SavedStore {
    static let shared = SavedStore()

    private(set) var savedQuoteIds: [Int] = []    // Read-only externally
    private(set) var folders: [SavedFolder] = []

    private init() { load() }

    func addToSaved(_ id: Int) {
        savedQuoteIds.append(id)
        persist()
    }
}
```

## HIGH: Concurrency Safety

### SW-09: @MainActor on ViewModels and UI-updating services

```swift
@Observable
@MainActor
final class AuthController {
    private(set) var isAuthenticated = false
    private(set) var lastError: AuthError?

    func signIn() async {
        // Already on MainActor: no dispatch needed
        isLoading = true
        defer { isLoading = false }
        // ...
    }
}
```

### SW-10: Use actors for thread-safe services

```swift
actor APIClient {
    static let shared = APIClient()
    private let session = URLSession.shared

    func fetch<T: Decodable>(_ endpoint: String) async throws -> T {
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

### SW-11: No redundant MainActor.run

```swift
// BAD: function is already @MainActor
@MainActor func update() async {
    await MainActor.run { isLoading = true }  // REDUNDANT
}

// GOOD
@MainActor func update() async {
    isLoading = true  // Already on MainActor
}
```

### SW-12: Task cancellation with [weak self]

```swift
private func scheduleAutosave() {
    autosaveTask?.cancel()
    autosaveTask = Task { @MainActor [weak self] in
        try? await Task.sleep(for: .seconds(1.5))
        guard !Task.isCancelled else { return }
        self?.saveIfDirty()
    }
}
```

Always:
- Cancel previous task before creating new one
- Check `Task.isCancelled` after sleep/await
- Use `[weak self]` to prevent retain cycles

## HIGH: Access Control

### SW-13: Default to private, widen intentionally

```swift
@Observable final class EditorViewModel {
    var content: String = ""               // Internal: views in same module need it
    private(set) var isDirty = false        // Readable externally, writable internally only
    private var autosaveTask: Task<Void, Never>?  // Implementation detail

    private func scheduleAutosave() { ... } // Internal helper
    func save() throws { ... }              // Public API
}
```

Rules:
- `private` for implementation details (helpers, tasks, caches)
- `private(set)` for state that views read but shouldn't mutate
- Internal (default) for module-scoped access
- `public` only for framework/library APIs

### SW-14: `final` on classes by default

```swift
// GOOD: prevents unintended subclassing
@Observable final class HomeViewModel { ... }

// Only omit final when subclassing is intentional
class BaseViewController: UIViewController { ... }
```

## MEDIUM: Memory Management

### SW-15: [weak self] in all async closures

```swift
// BAD: potential retain cycle
NotificationCenter.default.addObserver(forName: .didChange, object: nil, queue: .main) { _ in
    self.reload() // Strong capture
}

// GOOD
NotificationCenter.default.addObserver(forName: .didChange, object: nil, queue: .main) { [weak self] _ in
    self?.reload()
}
```

### SW-16: Use .task { } for view lifecycle async work

```swift
// GOOD: auto-cancelled on disappear
List(viewModel.items) { item in ItemRow(item: item) }
    .task { await viewModel.loadItems() }

// BAD: manual Task management in onAppear
.onAppear {
    Task { await viewModel.loadItems() } // Not cancelled on disappear!
}
```

## MEDIUM: Naming & Style

### SW-17: Boolean properties use `is`, `has`, `can`, `should` prefix

```swift
var isLoading = false
var isDirty = false
var isSynced = true
var hasCompletedOnboarding = false
var canEdit: Bool { ... }
```

### SW-18: Verbs for actions, nouns for properties

```swift
// Methods
func save() throws { ... }
func loadItems() async { ... }
func handleAppleSignIn(result:) async { ... }

// Properties
var folders: [String] = []
var selectedFolder: String?
var errorMessage: String?
```

### SW-19: Use `.task { }` modifier, not `onAppear` + Task

```swift
// BAD
.onAppear { Task { await vm.load() } }

// GOOD
.task { await vm.load() }
```

## Security & Vulnerability Rules

### SW-20: Never store secrets in UserDefaults

```swift
// BAD
UserDefaults.standard.set(apiKey, forKey: "api_key")

// GOOD: Keychain
try keychain.set(apiKey, key: "api_key")

// ACCEPTABLE: non-sensitive preferences only
@AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
```

### SW-21: Validate URLs before loading

```swift
guard let url = URL(string: input), url.scheme == "https" else {
    throw AppError.invalidURL(input)
}
```

### SW-22: Use App Transport Security (no exceptions)

Never add `NSAllowsArbitraryLoads` to Info.plist unless connecting to local dev servers.

## HIGH: Swift 6 Concurrency

### SW-23: Sendable conformance on shared types

Swift 6 strict concurrency requires types crossing actor boundaries to be `Sendable`.

```swift
// Value types: derive automatically
struct UserSession: Sendable {
    let id: UUID
    let token: String
}

// Reference types: declare and enforce immutability
final class Config: Sendable {
    let endpoint: URL
    let timeout: TimeInterval
    init(endpoint: URL, timeout: TimeInterval) {
        self.endpoint = endpoint
        self.timeout = timeout
    }
}

// When mutation is needed, use an actor
actor TokenStore {
    private var tokens: [String: Token] = [:]
    func get(_ key: String) -> Token? { tokens[key] }
}
```

`@unchecked Sendable` only with a written justification (e.g. internal lock).

### SW-24: `some P` for return position, `any P` for storage

```swift
// GOOD: opaque, no boxing, generic specialization
func makeView() -> some View { Text("hello") }

// GOOD: existential, needed for heterogeneous storage
var providers: [any AuthProvider] = []

// BAD: existential where opaque would do (boxes for nothing)
func makeView() -> any View { Text("hello") }
```

Default to `some`. Reach for `any` only when the concrete type must vary at runtime.

### SW-25: Privacy manifest for App Store submission

Add `PrivacyInfo.xcprivacy` listing tracking domains, required reason APIs, and collected data types. Apple rejects submissions missing required-reason API declarations (`UserDefaults`, `FileTimestamp`, `SystemBootTime`, `DiskSpace`).

### SW-26: Typed throws for domain errors (Swift 6+)

```swift
// BAD: untyped, callers must handle any Error
func parse(_ data: Data) throws -> Config { ... }

// GOOD: typed, exhaustive at the call site
enum ConfigError: Error {
    case invalidJSON
    case missingField(String)
    case versionMismatch(found: Int, expected: Int)
}

func parse(_ data: Data) throws(ConfigError) -> Config { ... }

do {
    let cfg = try parse(data)
} catch .missingField(let f) {
    // Compiler knows the cases, no fallback needed
}
```

Reach for typed throws on library boundaries and parsers. Stay untyped at top-level UI handlers where any error can bubble up.

### SW-27: Compile with strict concurrency complete and warnings as errors

```
// Package.swift
.target(
    name: "MyLib",
    swiftSettings: [
        .swiftLanguageMode(.v6),
        .enableUpcomingFeature("StrictConcurrency"),
        .unsafeFlags(["-warnings-as-errors"], .when(configuration: .release)),
    ]
)
```

Swift 6 language mode + `StrictConcurrency` catches data races at compile time. New code starts here.

### SW-28: Use Swift 6.2 features for fixed-size and approachable concurrency

Swift 6.2 (released 2025) is the current stable. Highlights worth adopting:

- **`InlineArray<N, T>`**: stack-allocated fixed-size arrays, no heap allocation, compile-time bounds. Use for small fixed buffers (RGB triples, fixed-width tokens, register sets).
- **Approachable concurrency defaults**: per-target setting that runs `nonisolated` synchronous code on the calling actor by default. Reduces incidental `await`s without giving up data-race safety.
- **WebAssembly target**: Swift compiles to WASM for browser and edge use cases.
- **C++ interop**: deeper than 6.0, viable for new bridges to existing C++ libraries.
- **Containerization**: official Apple project for running Linux containers natively on Apple silicon, written in Swift. Useful for build/test pipelines without Docker Desktop.

## Vulnerability Checklist

- [ ] No force unwraps (`!`) in production code
- [ ] No `try?` on critical operations (file creation, auth, data save)
- [ ] No secrets in UserDefaults (use Keychain)
- [ ] No strong self capture in async closures
- [ ] All ViewModels use `@Observable` + `final`
- [ ] UI-updating code is `@MainActor` or on `MainActor.run`
- [ ] All `.task { }` work checks cancellation
- [ ] Access control: private by default
- [ ] No `NSAllowsArbitraryLoads` in Info.plist
