---
name: auth-architecture
description: LiteLLM-RS Authentication Architecture. Covers JWT + API Key + RBAC multi-method auth, rate limiting with DashMap, middleware pipeline, and secure credential management.
---

# Authentication Architecture Guide

## Overview

LiteLLM-RS implements a multi-layered authentication system supporting JWT tokens, API keys, and Role-Based Access Control (RBAC) with lock-free rate limiting.

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Request                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Auth Middleware                               │
│  1. Extract credentials (JWT/API Key)                           │
│  2. Validate credentials                                         │
│  3. Load user context                                           │
│  4. Check rate limits                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RBAC Middleware                                │
│  1. Check required permissions                                   │
│  2. Validate resource access                                     │
│  3. Log access attempt                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Handler                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Key Authentication

### Key Generation

```rust
use rand::Rng;

pub fn generate_api_key() -> String {
    const CHARSET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    const KEY_LENGTH: usize = 64;

    let mut rng = rand::thread_rng();
    let key: String = (0..KEY_LENGTH)
        .map(|_| {
            let idx = rng.gen_range(0..CHARSET.len());
            CHARSET[idx] as char
        })
        .collect();

    format!("sk-{}", key)  // Prefix for easy identification
}
```

### Key Storage

```rust
use argon2::{Argon2, PasswordHasher, password_hash::SaltString};
use rand_core::OsRng;

pub struct ApiKeyManager {
    storage: Arc<dyn KeyStorage>,
    hasher: Argon2<'static>,
}

impl ApiKeyManager {
    pub fn new(storage: Arc<dyn KeyStorage>) -> Self {
        Self {
            storage,
            hasher: Argon2::default(),
        }
    }

    pub async fn create_key(&self, user_id: &str, name: &str) -> Result<ApiKey, AuthError> {
        let raw_key = generate_api_key();
        let salt = SaltString::generate(&mut OsRng);
        let hash = self.hasher
            .hash_password(raw_key.as_bytes(), &salt)
            .map_err(|e| AuthError::Internal(e.to_string()))?
            .to_string();

        let key = ApiKey {
            id: uuid::Uuid::new_v4().to_string(),
            user_id: user_id.to_string(),
            name: name.to_string(),
            key_hash: hash,
            prefix: raw_key[..10].to_string(),  // Store prefix for lookup
            created_at: chrono::Utc::now(),
            expires_at: None,
            last_used_at: None,
            permissions: vec![],
        };

        self.storage.store_key(&key).await?;

        // Return the raw key only once - user must save it
        Ok(ApiKey {
            key_hash: raw_key,  // Return raw key instead of hash
            ..key
        })
    }

    pub async fn validate_key(&self, raw_key: &str) -> Result<ApiKey, AuthError> {
        let prefix = &raw_key[..10.min(raw_key.len())];
        let key = self.storage
            .get_key_by_prefix(prefix)
            .await?
            .ok_or(AuthError::InvalidCredentials)?;

        // Verify the hash
        let parsed_hash = argon2::PasswordHash::new(&key.key_hash)
            .map_err(|_| AuthError::InvalidCredentials)?;

        self.hasher
            .verify_password(raw_key.as_bytes(), &parsed_hash)
            .map_err(|_| AuthError::InvalidCredentials)?;

        // Check expiration
        if let Some(expires_at) = key.expires_at {
            if expires_at < chrono::Utc::now() {
                return Err(AuthError::ExpiredCredentials);
            }
        }

        // Update last used timestamp
        self.storage.update_last_used(&key.id).await?;

        Ok(key)
    }
}
```

### API Key Middleware

```rust
use actix_web::{HttpRequest, HttpMessage, dev::ServiceRequest};

pub async fn api_key_middleware(
    req: ServiceRequest,
    key_manager: Arc<ApiKeyManager>,
) -> Result<ServiceRequest, AuthError> {
    // Extract API key from header
    let api_key = req
        .headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|s| s.strip_prefix("Bearer "))
        .ok_or(AuthError::MissingCredentials)?;

    // Validate key
    let key = key_manager.validate_key(api_key).await?;

    // Store user context in request extensions
    req.extensions_mut().insert(AuthContext {
        user_id: key.user_id.clone(),
        permissions: key.permissions.clone(),
        auth_method: AuthMethod::ApiKey,
    });

    Ok(req)
}
```

---

## JWT Authentication

### Token Structure

```rust
use serde::{Deserialize, Serialize};
use jsonwebtoken::{encode, decode, Header, Algorithm, Validation, EncodingKey, DecodingKey};

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String,          // User ID
    pub exp: usize,           // Expiration timestamp
    pub iat: usize,           // Issued at timestamp
    pub iss: String,          // Issuer
    pub aud: String,          // Audience
    pub roles: Vec<String>,   // User roles
    pub permissions: Vec<String>,  // Direct permissions
}

pub struct JwtManager {
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    issuer: String,
    audience: String,
    token_expiry: Duration,
}

impl JwtManager {
    pub fn new(secret: &[u8], issuer: String, audience: String) -> Self {
        Self {
            encoding_key: EncodingKey::from_secret(secret),
            decoding_key: DecodingKey::from_secret(secret),
            issuer,
            audience,
            token_expiry: Duration::from_secs(3600),  // 1 hour default
        }
    }

    pub fn create_token(&self, user_id: &str, roles: Vec<String>, permissions: Vec<String>) -> Result<String, AuthError> {
        let now = chrono::Utc::now();
        let claims = Claims {
            sub: user_id.to_string(),
            exp: (now + chrono::Duration::from_std(self.token_expiry).unwrap()).timestamp() as usize,
            iat: now.timestamp() as usize,
            iss: self.issuer.clone(),
            aud: self.audience.clone(),
            roles,
            permissions,
        };

        encode(&Header::new(Algorithm::HS256), &claims, &self.encoding_key)
            .map_err(|e| AuthError::TokenCreation(e.to_string()))
    }

    pub fn validate_token(&self, token: &str) -> Result<Claims, AuthError> {
        let mut validation = Validation::new(Algorithm::HS256);
        validation.set_issuer(&[&self.issuer]);
        validation.set_audience(&[&self.audience]);

        decode::<Claims>(token, &self.decoding_key, &validation)
            .map(|data| data.claims)
            .map_err(|e| match e.kind() {
                jsonwebtoken::errors::ErrorKind::ExpiredSignature => AuthError::ExpiredCredentials,
                jsonwebtoken::errors::ErrorKind::InvalidToken => AuthError::InvalidCredentials,
                _ => AuthError::TokenValidation(e.to_string()),
            })
    }
}
```

### JWT Middleware

```rust
pub async fn jwt_middleware(
    req: ServiceRequest,
    jwt_manager: Arc<JwtManager>,
) -> Result<ServiceRequest, AuthError> {
    let token = req
        .headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|s| s.strip_prefix("Bearer "))
        .ok_or(AuthError::MissingCredentials)?;

    let claims = jwt_manager.validate_token(token)?;

    req.extensions_mut().insert(AuthContext {
        user_id: claims.sub,
        permissions: claims.permissions,
        auth_method: AuthMethod::Jwt,
    });

    Ok(req)
}
```

---

## Role-Based Access Control (RBAC)

### Permission Model

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Role {
    pub id: String,
    pub name: String,
    pub permissions: Vec<Permission>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum Permission {
    // Chat permissions
    ChatCompletion,
    ChatCompletionStream,

    // Embedding permissions
    Embeddings,

    // Model permissions
    ListModels,
    GetModelInfo,

    // Admin permissions
    ManageUsers,
    ManageApiKeys,
    ViewMetrics,
    ConfigureProviders,

    // Provider-specific
    UseProvider(String),
    UseModel(String),
}

pub struct RbacManager {
    roles: DashMap<String, Role>,
    user_roles: DashMap<String, Vec<String>>,
}

impl RbacManager {
    pub fn has_permission(&self, user_id: &str, permission: &Permission) -> bool {
        let user_role_ids = match self.user_roles.get(user_id) {
            Some(roles) => roles.clone(),
            None => return false,
        };

        for role_id in user_role_ids {
            if let Some(role) = self.roles.get(&role_id) {
                if role.permissions.contains(permission) {
                    return true;
                }
            }
        }

        false
    }

    pub fn check_permission(&self, user_id: &str, permission: &Permission) -> Result<(), AuthError> {
        if self.has_permission(user_id, permission) {
            Ok(())
        } else {
            Err(AuthError::InsufficientPermissions)
        }
    }
}
```

### RBAC Middleware

```rust
pub fn require_permission(permission: Permission) -> impl Fn(ServiceRequest) -> Result<ServiceRequest, AuthError> {
    move |req: ServiceRequest| {
        let auth_context = req
            .extensions()
            .get::<AuthContext>()
            .ok_or(AuthError::MissingContext)?
            .clone();

        if !auth_context.permissions.contains(&permission.to_string()) {
            return Err(AuthError::InsufficientPermissions);
        }

        Ok(req)
    }
}

// Usage in route configuration
app.route(
    "/chat/completions",
    web::post()
        .wrap(require_permission(Permission::ChatCompletion))
        .to(chat_completion_handler)
)
```

---

## Rate Limiting

### Lock-Free Rate Limiter

```rust
use dashmap::DashMap;
use std::sync::atomic::{AtomicU64, Ordering};

pub struct RateLimiter {
    // Key: user_id or api_key, Value: (request_count, window_start)
    counters: DashMap<String, RateState>,
    config: RateLimitConfig,
}

struct RateState {
    request_count: AtomicU64,
    token_count: AtomicU64,
    window_start: AtomicU64,
}

#[derive(Clone)]
pub struct RateLimitConfig {
    pub requests_per_minute: u64,
    pub tokens_per_minute: u64,
    pub window_size: Duration,
}

impl RateLimiter {
    pub fn new(config: RateLimitConfig) -> Self {
        Self {
            counters: DashMap::new(),
            config,
        }
    }

    pub fn check_rate_limit(&self, key: &str) -> Result<(), RateLimitError> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let state = self.counters.entry(key.to_string()).or_insert_with(|| {
            RateState {
                request_count: AtomicU64::new(0),
                token_count: AtomicU64::new(0),
                window_start: AtomicU64::new(now),
            }
        });

        let window_start = state.window_start.load(Ordering::SeqCst);
        let window_size_secs = self.config.window_size.as_secs();

        // Reset window if expired
        if now - window_start >= window_size_secs {
            state.request_count.store(0, Ordering::SeqCst);
            state.token_count.store(0, Ordering::SeqCst);
            state.window_start.store(now, Ordering::SeqCst);
        }

        // Check request count
        let current_requests = state.request_count.fetch_add(1, Ordering::SeqCst);
        if current_requests >= self.config.requests_per_minute {
            state.request_count.fetch_sub(1, Ordering::SeqCst);
            let retry_after = window_size_secs - (now - window_start);
            return Err(RateLimitError::RequestsExceeded {
                limit: self.config.requests_per_minute,
                retry_after,
            });
        }

        Ok(())
    }

    pub fn record_tokens(&self, key: &str, tokens: u64) -> Result<(), RateLimitError> {
        if let Some(state) = self.counters.get(key) {
            let current_tokens = state.token_count.fetch_add(tokens, Ordering::SeqCst);
            if current_tokens + tokens > self.config.tokens_per_minute {
                state.token_count.fetch_sub(tokens, Ordering::SeqCst);
                return Err(RateLimitError::TokensExceeded {
                    limit: self.config.tokens_per_minute,
                });
            }
        }
        Ok(())
    }

    pub fn get_remaining(&self, key: &str) -> RateLimitInfo {
        self.counters
            .get(key)
            .map(|state| {
                let now = SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .unwrap()
                    .as_secs();
                let window_start = state.window_start.load(Ordering::SeqCst);
                let reset_at = window_start + self.config.window_size.as_secs();

                RateLimitInfo {
                    remaining_requests: self.config.requests_per_minute
                        .saturating_sub(state.request_count.load(Ordering::SeqCst)),
                    remaining_tokens: self.config.tokens_per_minute
                        .saturating_sub(state.token_count.load(Ordering::SeqCst)),
                    reset_at,
                }
            })
            .unwrap_or(RateLimitInfo {
                remaining_requests: self.config.requests_per_minute,
                remaining_tokens: self.config.tokens_per_minute,
                reset_at: 0,
            })
    }
}
```

### Rate Limit Middleware

```rust
pub async fn rate_limit_middleware(
    req: ServiceRequest,
    rate_limiter: Arc<RateLimiter>,
) -> Result<ServiceRequest, actix_web::Error> {
    let auth_context = req
        .extensions()
        .get::<AuthContext>()
        .ok_or(AuthError::MissingContext)?;

    rate_limiter
        .check_rate_limit(&auth_context.user_id)
        .map_err(|e| {
            let response = actix_web::HttpResponse::TooManyRequests()
                .insert_header(("Retry-After", e.retry_after().to_string()))
                .insert_header(("X-RateLimit-Limit", rate_limiter.config.requests_per_minute.to_string()))
                .insert_header(("X-RateLimit-Remaining", "0"))
                .json(json!({
                    "error": {
                        "message": "Rate limit exceeded",
                        "type": "rate_limit_error",
                        "code": "rate_limit_exceeded"
                    }
                }));
            actix_web::error::InternalError::from_response(e, response).into()
        })?;

    Ok(req)
}
```

---

## Middleware Pipeline

### Combined Auth Middleware

```rust
pub struct AuthMiddleware {
    api_key_manager: Arc<ApiKeyManager>,
    jwt_manager: Arc<JwtManager>,
    rbac_manager: Arc<RbacManager>,
    rate_limiter: Arc<RateLimiter>,
}

impl AuthMiddleware {
    pub async fn authenticate(&self, req: &ServiceRequest) -> Result<AuthContext, AuthError> {
        let auth_header = req
            .headers()
            .get("Authorization")
            .and_then(|h| h.to_str().ok())
            .ok_or(AuthError::MissingCredentials)?;

        // Determine auth method and validate
        let context = if auth_header.starts_with("Bearer sk-") {
            // API Key
            let key = auth_header.strip_prefix("Bearer ").unwrap();
            let api_key = self.api_key_manager.validate_key(key).await?;
            AuthContext {
                user_id: api_key.user_id,
                permissions: api_key.permissions,
                auth_method: AuthMethod::ApiKey,
            }
        } else if auth_header.starts_with("Bearer ey") {
            // JWT (starts with "ey" after base64 encoding)
            let token = auth_header.strip_prefix("Bearer ").unwrap();
            let claims = self.jwt_manager.validate_token(token)?;
            AuthContext {
                user_id: claims.sub,
                permissions: claims.permissions,
                auth_method: AuthMethod::Jwt,
            }
        } else {
            return Err(AuthError::InvalidCredentials);
        };

        // Check rate limits
        self.rate_limiter.check_rate_limit(&context.user_id)?;

        Ok(context)
    }

    pub fn authorize(&self, context: &AuthContext, required: &Permission) -> Result<(), AuthError> {
        if context.permissions.contains(&required.to_string()) {
            Ok(())
        } else {
            self.rbac_manager.check_permission(&context.user_id, required)
        }
    }
}
```

---

## Configuration

### Auth Configuration

```yaml
auth:
  enabled: true

  jwt:
    secret: ${JWT_SECRET}  # Must be at least 64 characters
    issuer: "litellm-gateway"
    audience: "litellm-api"
    token_expiry_seconds: 3600

  api_key:
    enabled: true
    key_length: 64
    prefix: "sk-"

  rate_limiting:
    enabled: true
    requests_per_minute: 60
    tokens_per_minute: 100000
    window_size_seconds: 60

  rbac:
    enabled: true
    default_role: "user"
    roles:
      - name: "admin"
        permissions:
          - "*"  # All permissions
      - name: "user"
        permissions:
          - "chat_completion"
          - "chat_completion_stream"
          - "embeddings"
          - "list_models"
      - name: "readonly"
        permissions:
          - "list_models"
          - "get_model_info"
```

---

## Security Best Practices

### 1. Secure Secret Generation

```rust
use rand::RngCore;

pub fn generate_jwt_secret() -> String {
    let mut secret = [0u8; 64];
    rand::thread_rng().fill_bytes(&mut secret);
    base64::encode(secret)
}
```

### 2. Constant-Time Comparison

```rust
use subtle::ConstantTimeEq;

fn secure_compare(a: &[u8], b: &[u8]) -> bool {
    a.ct_eq(b).into()
}
```

### 3. Key Rotation

```rust
impl ApiKeyManager {
    pub async fn rotate_key(&self, key_id: &str) -> Result<ApiKey, AuthError> {
        // Create new key
        let old_key = self.storage.get_key(key_id).await?
            .ok_or(AuthError::KeyNotFound)?;

        let new_key = self.create_key(&old_key.user_id, &format!("{} (rotated)", old_key.name)).await?;

        // Mark old key for delayed deletion
        self.storage.mark_for_deletion(key_id, Duration::from_secs(86400)).await?;

        Ok(new_key)
    }
}
```

### 4. Audit Logging

```rust
pub struct AuthAuditLog {
    logger: Arc<dyn AuditLogger>,
}

impl AuthAuditLog {
    pub fn log_auth_success(&self, context: &AuthContext, endpoint: &str) {
        self.logger.log(AuditEvent {
            event_type: "auth_success",
            user_id: &context.user_id,
            auth_method: &context.auth_method.to_string(),
            endpoint,
            timestamp: chrono::Utc::now(),
            success: true,
            error: None,
        });
    }

    pub fn log_auth_failure(&self, error: &AuthError, endpoint: &str) {
        self.logger.log(AuditEvent {
            event_type: "auth_failure",
            user_id: "unknown",
            auth_method: "unknown",
            endpoint,
            timestamp: chrono::Utc::now(),
            success: false,
            error: Some(error.to_string()),
        });
    }
}
```

---

## Error Types

```rust
#[derive(Debug, thiserror::Error)]
pub enum AuthError {
    #[error("Missing credentials")]
    MissingCredentials,

    #[error("Invalid credentials")]
    InvalidCredentials,

    #[error("Expired credentials")]
    ExpiredCredentials,

    #[error("Insufficient permissions")]
    InsufficientPermissions,

    #[error("Token creation failed: {0}")]
    TokenCreation(String),

    #[error("Token validation failed: {0}")]
    TokenValidation(String),

    #[error("Rate limit exceeded")]
    RateLimitExceeded,

    #[error("Key not found")]
    KeyNotFound,

    #[error("Missing auth context")]
    MissingContext,

    #[error("Internal error: {0}")]
    Internal(String),
}
```
