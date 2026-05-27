---
name: rust-strict
description: >
  Rust security, strictness, and vulnerability prevention rules. Use when writing,
  reviewing, or auditing Rust code. Complements rust-skills (179 general rules) with
  security-focused rules: unsafe audit, unwrap/expect bans, error handling hierarchy,
  secret handling, concurrency safety, input validation for Tauri commands, and
  release profile hardening. Derived from production Rust projects.
---

# Rust Strict Standard

Security and strictness rules complementing the existing `rust-skills` (179 rules).
These rules are derived from 5 production Rust projects.

## CRITICAL: Workspace Lint Configuration

Every Rust project must configure workspace lints. Baseline:

```toml
# Cargo.toml (workspace root)
[workspace.lints.rust]
unsafe_code = "deny"              # No unsafe in production code
unused_qualifications = "deny"

[workspace.lints.clippy]
unwrap_used = "deny"              # Force proper error handling
expect_used = "deny"              # Same: use ? or ok_or_else()
```

Per-crate opt-in:
```toml
# crates/my-crate/Cargo.toml
[lints]
workspace = true
```

### Exceptions (feature-gated, never blanket)

```rust
// FFI crate only: deny everywhere else
#![cfg_attr(feature = "local-llm", allow(unsafe_code))]

// Static initialization (regex, lazy): this is the ONLY acceptable expect()
static PATTERN: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"...").expect("regex must compile") // Bug if this fails
});
```

## CRITICAL: Error Handling Hierarchy

### Rule: Library crates use `thiserror`, app crates use `anyhow`

```rust
// Library crate: structured errors
#[derive(Debug, thiserror::Error)]
pub enum GatewayError {
    #[error("authentication required")]
    AuthRequired,

    #[error("rate limited: retry after {retry_after_ms}ms")]
    RateLimited { retry_after_ms: u64 },

    #[error("payload too large: {size} exceeds {max} bytes")]
    PayloadTooLarge { size: usize, max: usize },
}

impl GatewayError {
    pub fn status_code(&self) -> StatusCode { /* match self */ }
    pub fn is_retryable(&self) -> bool { matches!(self, Self::RateLimited { .. }) }
}

// App crate: flexible propagation
fn main() -> anyhow::Result<()> {
    let config = load_config().context("failed to load configuration")?;
    Ok(())
}
```

### Rule: Tauri commands return `Result<T, String>`

```rust
#[tauri::command]
pub async fn my_command(
    state: tauri::State<'_, AppState>,
) -> Result<ResponseData, String> {
    let data = do_work().map_err(|e| format!("operation failed: {e}"))?;
    Ok(data)
}
```

Tauri serializes errors as strings: this is the framework constraint, not a hack.

### Rule: Never `Box<dyn Error>`: use domain-specific enums

```rust
// BAD
fn process() -> Result<(), Box<dyn std::error::Error>> { ... }

// GOOD
fn process() -> Result<(), GatewayError> { ... }
```

## CRITICAL: Unsafe Audit Rules

### When unsafe is acceptable (with mandatory SAFETY comment)

```rust
// 1. SIMD intrinsics with runtime feature detection
#[target_feature(enable = "avx2,fma")]
unsafe fn cosine_similarity_avx2(a: &[f32], b: &[f32]) -> f64 {
    // SAFETY: AVX2 feature verified by caller via is_x86_feature_detected!
    let va = unsafe { _mm256_loadu_ps(a_ptr.add(offset)) };
    // offset < chunks*8 <= n: bounds checked by loop structure
}

// 2. Test-only env manipulation (with guard lock)
#[cfg(test)]
fn test_env_var() {
    let _guard = env_lock(); // Prevents test race conditions
    // SAFETY: env_lock serializes all env var access in tests
    unsafe { std::env::set_var("KEY", "value") };
}
```

### When unsafe is NEVER acceptable

- String/buffer manipulation (use safe APIs)
- Pointer arithmetic without bounds proof
- `transmute` (almost always wrong: use `From`/`Into`)
- Implementing `Send`/`Sync` manually (unless wrapping C FFI)
- `unsafe impl` without audited invariants

## HIGH: Concurrency Safety

### Rule: Never hold RwLock/Mutex across `.await`

```rust
// BAD: deadlock risk
let mut data = state.data.write().await;
data.insert(key, value);
let json = serde_json::to_string(&*data)?;
tokio::fs::write(path, json).await; // STILL LOCKED

// GOOD: clone, drop, then write
let json = {
    let mut data = state.data.write().await;
    data.insert(key, value);
    serde_json::to_string(&*data)?
}; // Lock dropped
tokio::fs::write(path, json).await;
```

### Rule: Never hold RwLock across disk I/O

```rust
// BAD
let mut cookies = state.cookies.write().await;
cookies.insert(name, result);
std::fs::write(&path, serde_json::to_string(&*cookies)?); // SYNC I/O WHILE LOCKED

// GOOD
let json = {
    let mut cookies = state.cookies.write().await;
    cookies.insert(name, result);
    serde_json::to_string(&*cookies)?
};
tokio::fs::write(&path, json).await;
```

### Rule: Use atomics for flags/counters, RwLock for data

```rust
pub struct AppState {
    // Atomics: lock-free for simple state
    pub is_running: AtomicBool,
    pub connection_count: AtomicUsize,

    // RwLock: for collections and complex data
    pub sessions: RwLock<HashMap<String, Session>>,

    // Watch channel: for shutdown signaling
    pub shutdown: watch::Sender<bool>,
}
```

### Rule: BoundedMap for all caches (prevent memory leaks)

```rust
// BAD: unbounded HashMap cache
let cache: HashMap<String, CachedValue> = HashMap::new();

// GOOD: bounded with capacity + TTL
let cache = BoundedMap::new(1000, Duration::from_secs(300));
```

## HIGH: Secret Handling

### Rule: Secrets in Keychain, never plain files

```rust
// macOS: system `security` CLI (subprocess, not FFI)
#[cfg(target_os = "macos")]
fn keychain_get(account: &str) -> Result<Option<String>, String> {
    let output = Command::new("security")
        .args(["find-generic-password", "-s", "AppName", "-a", account, "-w"])
        .output()
        .map_err(|e| format!("keychain read failed: {e}"))?;
    // ...
}

// Fallback: Tauri plugin-store (encrypted)
#[cfg(not(target_os = "macos"))]
fn save_fallback(app: &AppHandle, name: &str, value: &str) -> Result<(), String> { ... }
```

### Rule: Use `obfstr!()` for hardcoded strings in binary

```rust
// BAD: visible in binary strings
let api_url = "https://api.internal.example.com/v2";

// GOOD: obfuscated at compile time
let api_url = obfstr::obfstr!("https://api.internal.example.com/v2");
```

### Rule: Validate empty strings on secret storage

```rust
pub fn save_secret(name: &str, value: &str) -> Result<(), String> {
    let trimmed = value.trim();
    if trimmed.is_empty() {
        return Err("Secret value cannot be empty".to_string());
    }
    // Proceed with trimmed value
}
```

## HIGH: Input Validation (Tauri Commands)

### Rule: Enum-constrain all command inputs

```rust
// BAD: arbitrary string input
#[tauri::command]
fn spawn_agent(agent: String) -> Result<(), String> {
    Command::new(&agent).spawn(); // COMMAND INJECTION
}

// GOOD: enum-constrained
#[derive(Debug, Clone, Deserialize)]
pub enum AgentType { Claude, Codex, Opencode }

#[tauri::command]
fn spawn_agent(agent: AgentType) -> Result<(), String> {
    let binary = match agent {
        AgentType::Claude => "claude",
        AgentType::Codex => "codex",
        AgentType::Opencode => "opencode",
    };
    // Safe: only known values
}
```

### Rule: Use `tempfile` crate for temp files

```rust
// BAD: predictable path, symlink attacks
std::fs::write("/tmp/prompt.txt", prompt)?;

// GOOD: unpredictable, auto-cleanup
let mut tmp = tempfile::NamedTempFile::new()
    .map_err(|e| format!("temp file failed: {e}"))?;
writeln!(tmp, "{}", prompt)?;
let path = tmp.path().to_string_lossy().to_string();
```

## MEDIUM: Dependency Rules

### Rule: Explicit feature control

```toml
# BAD: pulls in everything
reqwest = "0.12"

# GOOD: only what you need
reqwest = { version = "0.12", default-features = false, features = ["json", "stream", "rustls-tls"] }
```

### Rule: `rustls-tls` over `native-tls`

Pure Rust TLS stack: no OpenSSL dependency, auditable, consistent behavior.

### Rule: Workspace dependency inheritance

```toml
# Workspace Cargo.toml
[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }

# Crate Cargo.toml
[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
```

## HIGH: Type Safety Patterns

### Rule: Newtype for IDs and units

```rust
// BAD: any UUID can be passed where any ID is expected
pub fn ban_user(uid: Uuid, by: Uuid) { ... }

// GOOD: type system rejects swapped arguments
pub struct UserId(Uuid);
pub struct AdminId(Uuid);

pub fn ban_user(uid: UserId, by: AdminId) { ... }
```

Same pattern for units: `Bytes(u64)`, `Millis(u64)`, `RetryCount(u32)`.

### Rule: `#[must_use]` on results that should not be silently dropped

```rust
#[must_use = "builder is incomplete until .build() is called"]
pub struct RequestBuilder { ... }

#[must_use]
pub fn try_acquire(&self) -> Option<Lease> { ... }
```

`Result<T, E>` already has `#[must_use]`. Add it to builders, locks, and validation outcomes.

### Rule: Explicit overflow handling on arithmetic

```rust
// BAD: wraps silently in release mode
let next = current + delta;

// GOOD: pick the semantic you mean
let next = current.checked_add(delta).ok_or(Error::Overflow)?;  // fail
let next = current.saturating_add(delta);                        // clamp
let next = current.wrapping_add(delta);                          // wrap (rare, document why)
```

Default to `checked_*` for anything user-influenced (sizes, counts, indices).

## HIGH: Edition 2024

Edition 2024 ships with Rust 1.85 (Feb 2025). Current stable is **1.95.0**. New crates start at edition 2024 with current stable. Migration changes that affect strict-mode rules:

### Rule: Wrap external symbols in `unsafe extern "C"` blocks

```rust
// BAD: edition 2024 hard error
extern "C" { fn external_fn(); }

// GOOD
unsafe extern "C" {
    fn external_fn();
}
```

Forces the FFI declaration site to acknowledge unsafety.

### Rule: `unsafe_op_in_unsafe_fn` is warn-by-default

Inside `unsafe fn`, every individual unsafe operation now needs its own `unsafe { ... }` block. This makes the audit surface explicit, do not bypass with `#[allow]`.

### Rule: Capture lifetimes explicitly with `use<...>` on RPIT

```rust
// Edition 2024: opaque return types capture all generic params by default
fn parse(s: &str) -> impl Iterator<Item = &str> + use<'_> { ... }
```

The `use<>` syntax is the escape hatch for the new capture rules. Reach for it when the inferred capture set is wrong.

### Rule: `gen` is a reserved keyword

If you have variables, functions, or modules named `gen`, rename them before migrating.

### Rule: `tracing` for structured logs, not `log` or `env_logger`

```rust
use tracing::{info, instrument, warn};

#[instrument(skip(state), fields(user_id = %req.user_id))]
async fn handler(state: AppState, req: Request) -> Result<Response, Error> {
    info!("processing request");
    ...
}
```

`tracing` is the de-facto standard. Pair with `tracing-subscriber` for output and `tracing-opentelemetry` for distributed tracing.

## MEDIUM: Release Profile

### Desktop apps (smallest binary)

```toml
[profile.release]
strip = true
lto = true            # Full LTO
codegen-units = 1
opt-level = 3
panic = "abort"        # No unwinding
```

### Server/gateway (balanced)

```toml
[profile.release]
strip = true
lto = "thin"          # Faster compile than full LTO
codegen-units = 1
```

### Dev profile (fast compile)

```toml
[profile.dev.package."*"]
opt-level = 3         # Optimize deps in dev (faster runtime)
```

## Vulnerability Checklist

- [ ] No `unsafe` blocks without SAFETY comments and justification
- [ ] No `.unwrap()` or `.expect()` in production (deny via lint)
- [ ] No string-constructed commands (enum-constrained)
- [ ] No predictable temp file paths (use `tempfile` crate)
- [ ] No secrets in source code (use env vars, Keychain, obfstr)
- [ ] No unbounded caches (use BoundedMap with capacity + TTL)
- [ ] No locks held across `.await` or disk I/O
- [ ] CSP configured in `tauri.conf.json` (for Tauri apps)
- [ ] `cargo audit` passes with no advisories
- [ ] `cargo clippy -- -D warnings` clean
