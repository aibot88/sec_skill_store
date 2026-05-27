---
name: go-strict
description: >
  Go coding standards, clean code, and security rules. Use when writing, reviewing,
  or refactoring Go code. Covers error handling (wrapping with %w), package organization
  (internal/pkg split), concurrency safety (sync.RWMutex, goroutine lifecycle), Gin
  handler patterns, input validation, structured logging with zerolog, graceful shutdown,
  and naming conventions. Derived from production Go services.
---

# Go Strict Standard

Rules extracted from 2 production Go services.

## CRITICAL: Error Handling

### GO-01: Always wrap errors with context

```go
// BAD: no context, impossible to trace
if err != nil {
    return err
}

// GOOD: fmt.Errorf with %w for wrapping
store, err := createStore(path)
if err != nil {
    return nil, fmt.Errorf("create store: %w", err)
}

// GOOD: multiple levels of context
session, err := validateToken(token)
if err != nil {
    return fmt.Errorf("validate session for user %s: %w", userID, err)
}
```

### GO-02: Check errors immediately, never defer

```go
// BAD: error ignored
json.Unmarshal(data, &result)

// GOOD
if err := json.Unmarshal(data, &result); err != nil {
    return fmt.Errorf("unmarshal response: %w", err)
}
```

### GO-03: Drain response bodies for connection reuse

```go
resp, err := http.Get(url)
if err != nil {
    return fmt.Errorf("request failed: %w", err)
}
defer resp.Body.Close()

if resp.StatusCode != http.StatusOK {
    io.Copy(io.Discard, resp.Body) // DRAIN before closing
    return fmt.Errorf("unexpected status: %d", resp.StatusCode)
}
```

### GO-04: Typed errors for API responses

```go
type APIError struct {
    Status  int    `json:"status"`
    Message string `json:"message"`
    Code    string `json:"code,omitempty"`
}

func (e *APIError) Error() string {
    return fmt.Sprintf("[%d] %s", e.Status, e.Message)
}

func SendError(c *gin.Context, status int, message string) {
    c.JSON(status, APIError{Status: status, Message: message})
}
```

## CRITICAL: Package Organization

### GO-05: internal/ for private, pkg/ for reusable

```
project/
├── cmd/
│   └── server/
│       └── main.go              # Entry point only: no logic
├── internal/
│   ├── handlers/                # HTTP handlers (Gin)
│   ├── middleware/              # Auth, rate limit, CORS, validation
│   ├── services/                # Business logic
│   ├── models/                  # Data structures
│   ├── config/                  # Env var loading
│   └── utils/                   # Helpers
├── pkg/
│   ├── redis/                   # Reusable Redis client
│   └── sqlite/                  # Reusable SQLite wrapper
├── go.mod
└── go.sum
```

`internal/` prevents import from outside the module. Use it.

### GO-06: main.go is thin: wire and run

```go
func main() {
    cfg := config.Load()
    redisClient := redis.NewClient(cfg.RedisURL)
    handlers := handlers.NewHandlers(redisClient, cfg)

    router := setupRouter(handlers, cfg)

    srv := &http.Server{Addr: ":" + cfg.Port, Handler: router}
    go func() { srv.ListenAndServe() }()

    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
}
```

## HIGH: Concurrency Safety

### GO-07: sync.RWMutex: read lock for reads, write lock for writes

```go
type RateLimiter struct {
    mu      sync.RWMutex
    entries map[string]*entry
}

func (rl *RateLimiter) GetLimiter(key string) *entry {
    rl.mu.RLock()
    e, ok := rl.entries[key]
    rl.mu.RUnlock()
    if ok { return e }

    rl.mu.Lock()
    defer rl.mu.Unlock()
    // Double-check after acquiring write lock
    if e, ok := rl.entries[key]; ok { return e }
    e = &entry{/* ... */}
    rl.entries[key] = e
    return e
}
```

Pattern: RLock → check → RUnlock → Lock → double-check → create.

### GO-08: Background goroutines with proper lifecycle

```go
func (rl *RateLimiter) evictLoop(interval, maxAge time.Duration) {
    ticker := time.NewTicker(interval)
    defer ticker.Stop()

    for range ticker.C {
        rl.mu.Lock()
        now := time.Now()
        for key, e := range rl.entries {
            if now.Sub(e.lastAccess) > maxAge {
                delete(rl.entries, key)
            }
        }
        rl.mu.Unlock()
    }
}

// Start with: go rl.evictLoop(5*time.Minute, 10*time.Minute)
```

### GO-09: Graceful shutdown with context

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

if err := srv.Shutdown(ctx); err != nil {
    log.Fatal().Err(err).Msg("server forced to shutdown")
}
```

## HIGH: HTTP Handler Patterns (Gin)

### GO-10: Constructor injection for handlers

```go
type Handlers struct {
    redis  *redis.Client
    config *config.Config
    sqlite *sqlite.Client
}

func NewHandlers(r *redis.Client, cfg *config.Config, s *sqlite.Client) *Handlers {
    return &Handlers{redis: r, config: cfg, sqlite: s}
}
```

### GO-11: Middleware chaining

```go
router := gin.New()
router.Use(middleware.CORS())
router.Use(middleware.InjectConfig(cfg))

// Group with shared auth
internal := router.Group("/", middleware.InternalAuth(cfg))
internal.GET("/validate-token", h.ValidateToken)

// Per-route rate limiting
router.POST("/login", middleware.RateLimit(10, time.Minute), h.Login)
```

### GO-12: Input validation in middleware

```go
func ValidateLicenseKey() gin.HandlerFunc {
    pattern := regexp.MustCompile(`^A-[A-Z0-9]{6}-[A-Z0-9]{8}-[A-Z0-9]{7}$`)
    return func(c *gin.Context) {
        key := c.Query("license_key")
        if key == "" {
            key = c.PostForm("license_key")
        }
        if !pattern.MatchString(key) {
            c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid license format"})
            c.Abort()
            return
        }
        c.Set("license_key", key)
        c.Next()
    }
}
```

Compile regex once in closure, not per-request.

## MEDIUM: Naming Conventions

### GO-13: Follow Go idioms strictly

```go
// Receivers: single letter matching type
func (rl *RateLimiter) GetLimiter(key string) { ... }
func (m *Manager) CreateInstance(cfg Config) { ... }
func (h *Handlers) ValidateToken(c *gin.Context) { ... }

// Constructors: NewType()
func NewHandlers(...) *Handlers { ... }
func NewRateLimiter(max int) *RateLimiter { ... }

// Getters: no Get prefix (unless disambiguating)
func (u *User) Name() string { return u.name }       // Not GetName()
func (u *User) SetName(n string) { u.name = n }      // Set prefix OK

// Boolean: use Is/Has/Can
func (s *Session) IsExpired() bool { ... }
func (u *User) HasPermission(p string) bool { ... }

// Packages: lowercase, no underscores
package handlers  // Not package http_handlers
package middleware // Not package Middleware

// Constants: PascalCase (exported), camelCase (unexported)
const MaxRetries = 3
const defaultTimeout = 30 * time.Second
```

### GO-14: Use typed structs, not `gin.H{}` in hot paths

```go
// BAD: heap allocation per response
c.JSON(200, gin.H{"status": "ok", "data": result})

// GOOD: stack-allocated struct
type Response struct {
    Status string      `json:"status"`
    Data   interface{} `json:"data"`
}
c.JSON(200, Response{Status: "ok", Data: result})
```

## MEDIUM: Logging

### GO-15: Use zerolog for structured logging

```go
import "github.com/rs/zerolog"

// Setup
logger := zerolog.New(os.Stderr).With().Timestamp().Logger()

// Usage
logger.Info().Str("component", "auth").Str("user", userID).Msg("login successful")
logger.Error().Err(err).Str("endpoint", path).Msg("request failed")
logger.Warn().Int("attempts", count).Msg("approaching rate limit")
```

Never `log.Printf` in production: it's unstructured and hard to query.

### GO-16: Component context in loggers

```go
func NewManager(logger zerolog.Logger) *Manager {
    return &Manager{
        log: logger.With().Str("component", "instance-mgr").Logger(),
    }
}
```

## Security Rules

### GO-17: No secrets in source code

```go
// BAD
const apiKey = "sk-abc123..."

// GOOD
apiKey := os.Getenv("API_KEY")
if apiKey == "" {
    log.Fatal().Msg("API_KEY environment variable required")
}
```

### GO-18: Validate all external input

Never trust query params, POST bodies, or headers. Validate format, length, and type.

### GO-19: Use `http.StatusXxx` constants

```go
// BAD
c.JSON(401, gin.H{"error": "unauthorized"})

// GOOD
c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
```

## HIGH: Context and Error Plumbing

### GO-20: `context.Context` is the first argument

```go
// BAD: caller cannot cancel or propagate deadlines
func FetchUser(id string) (*User, error) { ... }

// GOOD
func FetchUser(ctx context.Context, id string) (*User, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    return doRequest(req)
}
```

In handlers, derive from the request: `ctx := c.Request.Context()`. Never call `context.Background()` inside a request path.

### GO-21: Inspect wrapped errors with `errors.Is` / `errors.As`

```go
// Sentinel error
var ErrNotFound = errors.New("not found")

if err != nil {
    if errors.Is(err, ErrNotFound) {
        return c.JSON(http.StatusNotFound, ...)
    }
    var apiErr *APIError
    if errors.As(err, &apiErr) {
        return c.JSON(apiErr.Status, apiErr)
    }
    return c.JSON(http.StatusInternalServerError, ...)
}
```

`==` comparison on wrapped errors fails. Always unwrap with `Is`/`As`.

### GO-22a: `log/slog` is the structured logger, not third-party libs

```go
// Old: zerolog / zap / logrus
// New (Go 1.21+): stdlib log/slog
import "log/slog"

logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
slog.SetDefault(logger)

slog.Info("user signed in", "user_id", uid, "tenant", tenantID)
slog.Error("save failed", "err", err, "request_id", reqID)
```

`slog` covers JSON output, log levels, attribute groups, and context propagation. New code should not pull in zerolog or zap unless there's a specific reason.

### GO-22b: `math/rand/v2` for non-cryptographic randomness

```go
// BAD: math/rand needs explicit seeding, has known bias issues
import "math/rand"

// GOOD: math/rand/v2 (Go 1.22+) seeds from a CSPRNG by default
import "math/rand/v2"

n := rand.IntN(100)        // 0..99
shuffled := rand.Perm(10)  // permutation
```

For tokens, secrets, or anything cryptographic, still use `crypto/rand`.

### GO-22c: `os.Root` for filesystem-confined access (Go 1.24+)

```go
// Confine FS access to a directory, prevents path traversal
root, err := os.OpenRoot("/var/app/uploads")
if err != nil {
    return err
}
defer root.Close()

// All operations resolve relative to root, ".." escapes are blocked
f, err := root.Open(userPath)
```

Use `os.Root` for any filesystem code that touches user-supplied paths.

### GO-22ca: Go 1.26 highlights (Feb 2026)

- **Green Tea garbage collector** is now default. Real-world programs see 10-40% lower GC overhead, no source change required.
- **`crypto/hpke`** stdlib package implements RFC 9180 Hybrid Public Key Encryption with post-quantum hybrid KEMs. Use this for new key-agreement code instead of pulling in `cloudflare/circl`.
- **`new(expr)`**: `new` accepts an expression and returns a pointer to its initial value. Replaces `x := expr; p := &x`.
- **Self-referencing generic types**: a type can name itself in its own type-parameter list. Simplifies trees, graphs, and CRTP-style APIs.
- **`GOEXPERIMENT=simd`** opens the experimental `simd/archsimd` package. Useful for hot loops, still subject to change.
- **cgo overhead** down ~30% baseline. Tighten cgo budgets accordingly.

### GO-22d: `range` over functions and integers

```go
// Go 1.22+: range over int
for i := range 10 { ... }

// Go 1.23+: range over function (custom iterators)
for k, v := range myMap.All() {
    fmt.Println(k, v)
}

// Define an iterator
func (m *Map[K, V]) All() iter.Seq2[K, V] {
    return func(yield func(K, V) bool) {
        for k, v := range m.data {
            if !yield(k, v) { return }
        }
    }
}
```

Replaces hand-rolled `Iterator` interfaces. Pair with the `iter` package.

### GO-22e: Never expose `/debug/pprof` publicly

```go
// BAD: pprof leaks heap, goroutine names, source paths to anyone
import _ "net/http/pprof"
http.ListenAndServe(":8080", nil)

// GOOD: separate port, bound to localhost or behind auth
go http.ListenAndServe("127.0.0.1:6060", nil)
```

Same for `expvar`. Either gate behind auth middleware or bind to loopback.

## Vulnerability Checklist

- [ ] All errors wrapped with `fmt.Errorf("context: %w", err)`
- [ ] Response bodies drained before close (`io.Copy(io.Discard, resp.Body)`)
- [ ] No secrets in source (use env vars)
- [ ] Input validated in middleware (regex compiled once)
- [ ] RWMutex with double-check locking pattern
- [ ] Background goroutines have shutdown mechanism
- [ ] Graceful shutdown with 30s timeout
- [ ] Structured logging (zerolog, not fmt/log)
- [ ] No `gin.H{}` in hot paths (use typed structs)
- [ ] `c.Abort()` called after error responses in middleware
