---
name: "flutter-db"
description: "Local database and persistence selection for Flutter including SharedPreferences, SecureStorage, Hive, and Drift. Use when implementing offline storage, encrypted data persistence, or choosing between key-value and relational local databases."
metadata:
  last_modified: "2026-03-12 11:18:17 (GMT+8)"
---

# Database Architecture Guide (Flutter)

## Goal
Implement robust, scalable, and secure local persistence strategies for Flutter applications. This skill ensures developers choose the optimal storage engine—balancing simple key-value settings, encrypted sensitive data, high-performance NoSQL object stores, and complex relational databases.

## Process

### 🚀 High-Level Workflow
Selecting the right persistence layer depends on data sensitivity, complexity, and relationship depth.

### Phase 1: Key-Value Persistence (Simple & Secure)
Use lightweight stores for settings and sensitive credentials.
- [Shared Preferences Guide](./references/shared-preferences.md) - Non-sensitive settings and flags using static wrappers.
- [Secure Storage Guide](./references/secure-storage.md) - Encrypted storage for tokens and passwords.

### Phase 2: High-Performance Object Storage (NoSQL)
For local-first apps requiring fast read/write of large datasets without complex relations.
- [Hive CE (Synchronous NoSQL)](./references/hive-ce.md) - Blazing fast object store for local caching and offline data.

### Phase 3: Complex Relational Schemas (SQL)
For apps requiring strict data integrity, transactions, and complex queries.
- [Drift (Reactive SQL)](./references/drift.md) - Type-safe relational database built on top of SQLite.

---

## 📚 Documentation Library
Refer to these specialized resources to implement your chosen persistence strategy:

- [🗄️ Database Architecture Overview](./references/databases-overview.md)
- [⚙️ Shared Preferences](./references/shared-preferences.md)
- [🔐 Secure Storage (Encrypted)](./references/secure-storage.md)
- [🐝 Hive CE Best Practices](./references/hive-ce.md)
- [🐘 Drift (SQL) Best Practices](./references/drift.md)

## Constraints
* **Type Safety**: Prohibit raw `dynamic` data access. Always use generated classes (Drift) or typed static wrappers (SharedPreferences/SecureStorage).
* **Sensitivity Awareness**: Force use of `Secure Storage` for any tokens, passwords, or PII. Never store sensitive data in SharedPreferences or unencrypted Hive boxes.
* **Singleton Access**: Access storage instances via DI (Riverpod) or strictly defined static classes to prevent key fragmentation.
* **Performance Balance**: Use NoSQL (Hive) for high-frequency reads and SQL (Drift) for complex relationships. Don't over-engineer simple apps with SQL.
