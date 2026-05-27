---
name: ios-data
description: >
  iOS data persistence expert skill covering SwiftData (@Model, ModelContainer, @Query, #Predicate, migrations, CloudKit),
  Core Data (NSPersistentContainer, NSFetchRequest, batch operations, CloudKit), UserDefaults/@AppStorage,
  FileManager (app sandbox directories), Keychain for sensitive data, iCloud key-value storage, and SQLite/GRDB.
  Use this skill whenever the user needs to persist data, create data models, query databases, handle migrations,
  sync with iCloud, or choose a storage strategy. Triggers on: SwiftData, Core Data, @Model, @Query, #Predicate,
  ModelContainer, NSManagedObject, NSFetchRequest, UserDefaults, @AppStorage, FileManager, documents directory,
  Keychain, iCloud sync, SQLite, GRDB, persistence, database, migration, schema, data model, fetch, save, delete,
  storage, cache, offline, or any iOS data storage question.
---

# iOS Data Persistence Skill

## Storage Selection Guide

| Data Type | Storage | Why |
|-----------|---------|-----|
| User preferences | UserDefaults / @AppStorage | Simple, auto-loaded at launch |
| Preferences synced across devices | NSUbiquitousKeyValueStore | Simple iCloud sync, <1MB |
| Passwords, tokens, API keys | Keychain | Encrypted, survives reinstall |
| Structured app data (iOS 17+) | SwiftData | Modern, declarative, queryable |
| Structured app data (iOS 16-) | Core Data | Mature, proven, stable |
| Large files (images, video, PDFs) | FileManager | Direct file I/O, no DB overhead |
| Complex queries, cross-platform | SQLite (GRDB) | Full SQL control, lightweight |
| Public/shared CloudKit data | Core Data + NSPersistentCloudKitContainer | SwiftData only supports private DB |

## Decision Flowchart

```
Is the data sensitive (tokens, passwords, keys)?
  YES → Keychain (NEVER UserDefaults)
  NO ↓

Is it a simple user preference (theme, flag, small string)?
  YES → Need sync across devices?
    YES → NSUbiquitousKeyValueStore
    NO  → @AppStorage / UserDefaults
  NO ↓

Is it a large binary file (image, video, PDF)?
  YES → FileManager (store path/URL reference in DB if needed)
  NO ↓

Is it structured/relational data?
  YES → iOS 17+ minimum?
    YES → SwiftData
    NO  → Core Data
  NO ↓

Need full SQL control or cross-platform DB?
  YES → SQLite via GRDB.swift
  NO  → Codable + FileManager (JSON/plist file)
```

## Core Rules

### General
- Use SwiftData for new iOS 17+ projects -- simpler API than Core Data
- Use Keychain for ALL sensitive data (tokens, passwords, API keys) -- NEVER UserDefaults
- Use @AppStorage only for simple preferences -- not large data or collections
- Store large blobs (images, video) on disk via FileManager, keep only the path/URL in DB
- Always handle persistence errors -- do not force-try in production

### SwiftData Rules
- Always use `isStoredInMemoryOnly: true` for test ModelContainers
- Use `@ModelActor` for background SwiftData operations -- Model objects are NOT Sendable
- Pass `PersistentIdentifier` (Sendable) between actors, not model objects
- Use `FetchDescriptor.fetchLimit` for pagination -- never fetch all records unbounded
- CloudKit models: all properties must have defaults or be optional, no `.unique`
- Add `#Index` (iOS 18+) on frequently queried properties for performance
- Prefer `@Transient` for computed/cached properties that should not be persisted

### Core Data Rules
- Batch operations (`NSBatchInsertRequest`, etc.) bypass validation -- use for bulk imports (10x faster)
- Always merge batch operation results into viewContext via `NSManagedObjectContext.mergeChanges`
- Use `fetchBatchSize` (default 0 = fetch all) -- set to ~20 for table/collection views
- Use `newBackgroundContext()` or `performBackgroundTask` for writes -- never block main thread
- Set `automaticallyMergesChangesFromParent = true` on viewContext for auto UI refresh

### Storage Rules
- UserDefaults synchronize is unnecessary since iOS 12 -- system handles it
- FileManager: use `.applicationSupportDirectory` for internal data, `.documentDirectory` for user-visible files
- `tmp/` and `Library/Caches/` can be purged by system -- do not store critical data there
- iCloud KVS: 1MB total limit, 1024 keys max, values up to 1MB each
- GRDB: use `ValueObservation` for reactive SwiftUI integration

## SwiftData Quick Reference

### Define a Model
```swift
import SwiftData

@Model
final class Task {
    var title: String
    var isCompleted: Bool = false
    var createdAt: Date = Date.now
    @Attribute(.externalStorage) var imageData: Data?
    @Relationship(deleteRule: .cascade, inverse: \Tag.tasks)
    var tags: [Tag] = []

    init(title: String) {
        self.title = title
    }
}

@Model
final class Tag {
    @Attribute(.unique) var name: String
    var tasks: [Task] = []

    init(name: String) {
        self.name = name
    }
}
```

### Setup Container
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: [Task.self, Tag.self])
    }
}
```

### Query and Mutate
```swift
struct TaskListView: View {
    @Query(sort: \Task.createdAt, order: .reverse)
    private var tasks: [Task]
    @Environment(\.modelContext) private var context

    var body: some View {
        List(tasks) { task in
            Text(task.title)
        }
    }

    func addTask(title: String) {
        let task = Task(title: title)
        context.insert(task)
        // autosave handles the rest
    }

    func deleteTask(_ task: Task) {
        context.delete(task)
    }
}
```

### Predicate
```swift
let incomplete = #Predicate<Task> { !$0.isCompleted }
let search = #Predicate<Task> { task in
    task.title.localizedStandardContains("meeting")
}
```

See [references/swiftdata.md](references/swiftdata.md) for full details.

## Core Data Quick Reference

### Setup
```swift
let container = NSPersistentContainer(name: "Model")
container.loadPersistentStores { _, error in
    if let error { fatalError("Store failed: \(error)") }
}
container.viewContext.automaticallyMergesChangesFromParent = true
```

### Fetch
```swift
let request = NSFetchRequest<Task>(entityName: "Task")
request.predicate = NSPredicate(format: "isCompleted == %@", NSNumber(value: false))
request.sortDescriptors = [NSSortDescriptor(keyPath: \Task.createdAt, ascending: false)]
request.fetchBatchSize = 20
let tasks = try context.fetch(request)
```

### Batch Insert (Bulk Performance)
```swift
let request = NSBatchInsertRequest(entity: Task.entity(), objects: dictionaries)
request.resultType = .objectIDs
let result = try context.execute(request) as! NSBatchInsertResult
let changes = [NSInsertedObjectIDsKey: result.objectIDs!]
NSManagedObjectContext.mergeChanges(fromRemoteContextSave: changes, into: [viewContext])
```

See [references/coredata.md](references/coredata.md) for full details.

## Other Storage Quick Reference

### @AppStorage
```swift
struct SettingsView: View {
    @AppStorage("isDarkMode") private var isDarkMode = false
    @AppStorage("username") private var username = ""

    var body: some View {
        Toggle("Dark Mode", isOn: $isDarkMode)
    }
}
```

### Keychain (via wrapper)
```swift
func saveToKeychain(account: String, data: Data) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecValueData as String: data
    ]
    SecItemDelete(query as CFDictionary)
    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else {
        throw KeychainError.saveFailed(status)
    }
}
```

### FileManager -- Save Codable
```swift
func save<T: Encodable>(_ object: T, to filename: String) throws {
    let url = FileManager.default
        .urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        .appendingPathComponent(filename)
    try FileManager.default.createDirectory(
        at: url.deletingLastPathComponent(),
        withIntermediateDirectories: true
    )
    let data = try JSONEncoder().encode(object)
    try data.write(to: url, options: .atomic)
}
```

See [references/storage.md](references/storage.md) for full details.

## Common Patterns

### Repository Pattern (SwiftData)
```swift
@ModelActor
actor TaskRepository {
    func create(title: String) throws -> PersistentIdentifier {
        let task = Task(title: title)
        modelContext.insert(task)
        try modelContext.save()
        return task.persistentModelID
    }

    func fetchIncomplete() throws -> [PersistentIdentifier] {
        let descriptor = FetchDescriptor<Task>(
            predicate: #Predicate { !$0.isCompleted },
            sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
        )
        return try modelContext.fetch(descriptor).map(\.persistentModelID)
    }

    func complete(id: PersistentIdentifier) throws {
        guard let task = modelContext.model(for: id) as? Task else { return }
        task.isCompleted = true
        try modelContext.save()
    }
}
```

### Offline-First Architecture
```swift
// 1. Define local SwiftData model as source of truth
// 2. Sync layer: fetch from API → upsert into SwiftData
// 3. UI reads only from SwiftData via @Query
// 4. Writes go to SwiftData first, then queue API calls
// 5. Use ModelContext.enumerate for large dataset processing
```

### Test Container
```swift
@MainActor
func makeTestContainer() throws -> ModelContainer {
    let config = ModelConfiguration(isStoredInMemoryOnly: true)
    let container = try ModelContainer(
        for: Task.self, Tag.self,
        configurations: config
    )
    return container
}
```

## Performance Checklist

- [ ] Use `fetchLimit` on all list queries -- never fetch unbounded
- [ ] Add `#Index` (iOS 18) or Core Data indexes on frequently filtered/sorted properties
- [ ] Use `@Attribute(.externalStorage)` for Data properties > a few KB
- [ ] Use `@ModelActor` / background context for writes > 100 objects
- [ ] Use `enumerate()` instead of `fetch()` for processing large datasets (controls memory)
- [ ] Set `fetchBatchSize = 20` on Core Data fetch requests for lists
- [ ] Use batch operations for bulk imports (Core Data)
- [ ] Profile with Instruments > Core Data template to find slow fetches

## Migration Checklist

### SwiftData
1. Create a new `VersionedSchema` conforming type for each schema version
2. Define `SchemaMigrationPlan` with ordered list of schemas
3. Use `.lightweight` stage when only adding/renaming properties
4. Use `.custom` stage when transforming data between versions
5. Pass migration plan to `ModelContainer` configuration

### Core Data
1. Lightweight: adding optional attributes, adding entities -- automatic, no code needed
2. Heavyweight: create mapping model (.xcmappingmodel) for complex changes
3. Always test migration with production-size dataset before release

## File References

- [SwiftData Deep Dive](references/swiftdata.md) -- @Model, @Query, #Predicate, migrations, CloudKit, concurrency
- [Core Data Deep Dive](references/coredata.md) -- NSPersistentContainer, fetching, batch ops, CloudKit, migrations
- [Storage Options](references/storage.md) -- UserDefaults, @AppStorage, FileManager, Keychain, iCloud KVS, SQLite/GRDB
