---
name: supabase-auth
description: >
  This skill should be used when configuring Supabase authentication, setting up auth providers,
  managing users, working with JWTs, or implementing auth flows in applications.
  Trigger when: "Supabase auth", "authentication", "sign up", "sign in", "OAuth provider",
  "auth configuration", "JWT", "auth.users", "auth.uid()", "secret key", "service role key",
  "publishable key", "anon key", "user management", "auth hooks", "Custom Access Token Hook",
  "asymmetric JWT", "JWKS", "JWT signing keys", "anonymous sign-in", "is_anonymous",
  "MFA", "TOTP", "WebAuthn", "passkey", "AAL1", "AAL2",
  "email templates", "social login", "magic link", "password reset", "auth middleware",
  or implementing any authentication with Supabase.
---

# Supabase Authentication

Guidance for configuring and implementing Supabase Auth, managing users, and integrating auth providers. Pinned to April 2026 platform state.

## Overview

Supabase Auth provides a complete authentication system with email/password, magic links, OAuth providers, phone auth, SSO, anonymous sign-in, and MFA (TOTP, Phone, WebAuthn). It manages the `auth.users` table and issues JWTs for API authorization.

## Auth Architecture

```
Client App → Supabase Auth API → auth.users table
                ↓
            JWT issued (ES256/RS256 by default for new projects)
                ↓
            RLS policies check (select auth.uid()) against table data
```

**Key concept:** Authentication (who is the user) is handled by Supabase Auth. Authorization (what can the user do) is handled by RLS policies referencing `(select auth.uid())` and JWT claims.

## API keys (April 2026)

Supabase ships two key models — see the `supabase-projects` skill for the full breakdown. Quick summary:

| Key | Format | Use |
|-----|--------|-----|
| **Publishable** | `sb_publishable_*` | Browser/mobile clients (modern) |
| **Anon** (legacy) | `eyJ...` JWT | Browser/mobile clients (legacy projects) |
| **Secret** | `sb_secret_*` | Edge Functions/server (modern; bypasses RLS) |
| **Service role** (legacy) | `eyJ...` JWT | Edge Functions/server (legacy; bypasses RLS) |

Both formats coexist on the same project. Projects restored after Nov 1, 2025 only get the modern format.

## Asymmetric JWT signing (default since May 1, 2025)

New projects sign JWTs with **ES256 or RS256**, exposing a JWKS endpoint:

```
https://<project>.supabase.co/auth/v1/.well-known/jwks.json
```

Server-side code verifies tokens by fetching the JWKS — no shared secret. Projects created before May 1, 2025 still use HS256 unless migrated; the dashboard offers a one-click upgrade. Asymmetric verification is what makes things like third-party server-side rendering and per-region key rotation reasonable.

## Client-Side Auth (supabase-js)

### Sign Up

```typescript
const { data, error } = await supabase.auth.signUp({
  email: "user@example.com",
  password: "<your-password>",
});
```

### Sign In (Email/Password)

```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email: "user@example.com",
  password: "<your-password>",
});
```

### Sign In (OAuth)

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: "google",
  options: {
    redirectTo: "https://myapp.com/auth/callback",
  },
});
```

### Sign In (Magic Link)

```typescript
const { data, error } = await supabase.auth.signInWithOtp({
  email: "user@example.com",
});
```

### Sign In Anonymously (GA)

```typescript
const { data, error } = await supabase.auth.signInAnonymously();
```

The user gets a real `auth.users` row with `is_anonymous = true`. Their JWT carries `is_anonymous: true` — usable in RLS:

```sql
-- Restrict a write path to non-anonymous users
create policy "Real users can post"
  on public.posts for insert
  to authenticated
  with check ((select auth.jwt() ->> 'is_anonymous')::boolean = false);
```

Anonymous users can be linked to a real account later (`updateUser` with email/password). Built-in rate limit: 30 requests/hour/IP — add CAPTCHA / Turnstile to harden.

### Sign Out

```typescript
const { error } = await supabase.auth.signOut();
```

### Get Current User

```typescript
const { data: { user } } = await supabase.auth.getUser();
```

### Listen for Auth Changes

```typescript
supabase.auth.onAuthStateChange((event, session) => {
  if (event === "SIGNED_IN") {
    // Handle sign in
  }
});
```

## Multi-Factor Authentication (MFA)

Supabase MFA supports three factor types:

| Factor | Description | When to use |
|--------|-------------|-------------|
| **TOTP** | Time-based codes (Google Authenticator, 1Password, etc.) | Default second factor |
| **Phone** | SMS or WhatsApp OTP | Lower-friction second factor for consumer apps |
| **WebAuthn (Passkeys)** | Platform passkeys (Touch ID, Face ID, Windows Hello, security keys) | Highest assurance, increasingly preferred |

The auth model uses **AAL1 / AAL2** (Authentication Assurance Level):
- AAL1 = single factor (password / OAuth / magic link)
- AAL2 = two factors (password + TOTP, or passkey)

```typescript
// Enroll TOTP
const { data, error } = await supabase.auth.mfa.enroll({ factorType: "totp" });
// data.totp.qr_code is a data URL for the QR code

// Challenge + verify
const { data: challenge } = await supabase.auth.mfa.challenge({ factorId: data.id });
await supabase.auth.mfa.verify({ factorId: data.id, challengeId: challenge.id, code: "123456" });
```

Gate sensitive routes by checking the AAL claim:
```typescript
const { data: { aal } } = await supabase.auth.mfa.getAuthenticatorAssuranceLevel();
if (aal.currentLevel !== "aal2") { /* prompt for second factor */ }
```

## Server-Side Auth

### Verifying Users in Edge Functions

```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY")!,
    {
      global: {
        headers: { Authorization: req.headers.get("Authorization")! },
      },
    }
  );

  const { data: { user }, error } = await supabase.auth.getUser();
  if (error || !user) {
    return new Response("Unauthorized", { status: 401 });
  }

  // User is authenticated, proceed...
});
```

### Secret Key (Admin Operations)

The secret key (`sb_secret_*` or legacy `service_role` JWT) bypasses RLS. Use it only server-side for admin operations:

```typescript
const supabaseAdmin = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

// Admin: list all users
const { data: { users } } = await supabaseAdmin.auth.admin.listUsers();
```

**Never expose secret/service-role keys to the client.** Caught by `scripts/check-secret-leaks.py`.

## Auth Hooks (April 2026 — six hooks supported)

Auth Hooks let you extend the auth flow with Postgres functions or HTTP webhooks:

| Hook | When it runs | Use for |
|------|-------------|---------|
| `before-user-created` | Before a new user is inserted | Validate signups, enforce email allowlists |
| `custom-access-token` | Every JWT mint | Add custom claims (RBAC, tenant_id, etc.) |
| `send-email` | Outbound auth emails | Custom templates, third-party email service |
| `send-sms` | Outbound auth SMS | Custom SMS provider |
| `password-verification-attempt` | Every password sign-in attempt | Rate limiting, breach checks |
| `mfa-verification-attempt` | Every MFA challenge | Rate limiting, anomaly detection |

The **Custom Access Token Hook** is the recommended way to do RBAC — see the security skill for the full pattern.

## Auth Configuration (config.toml)

Configure auth for local development in `supabase/config.toml`:

```toml
[auth]
enabled = true
site_url = "http://localhost:3000"
additional_redirect_urls = ["http://localhost:3000/auth/callback"]
jwt_expiry = 3600
enable_signup = true
enable_anonymous_sign_ins = false   # Opt in if you want anonymous auth

[auth.email]
enable_signup = true
double_confirm_changes = true
enable_confirmations = false  # Set true for production

[auth.external.google]
enabled = true
client_id = "env(GOOGLE_CLIENT_ID)"
secret = "env(GOOGLE_CLIENT_SECRET)"
redirect_uri = ""  # Uses default

[auth.mfa]
max_enrolled_factors = 10

[auth.mfa.totp]
enroll_enabled = true
verify_enabled = true

[auth.mfa.phone]
enroll_enabled = false   # Requires phone provider configured

[auth.mfa.web_authn]
enroll_enabled = true
verify_enabled = true
```

## Supported Providers

| Provider | Config Key | Notes |
|----------|-----------|-------|
| Email/Password | `[auth.email]` | Built-in, always available |
| Phone/SMS | `[auth.sms]` | Requires Twilio, MessageBird, Vonage, or Textlocal |
| Google | `[auth.external.google]` | OAuth 2.0 — most common redirect-URI mismatch |
| GitHub | `[auth.external.github]` | OAuth 2.0 |
| Apple | `[auth.external.apple]` | Key + Team ID rotation pitfall |
| Discord | `[auth.external.discord]` | OAuth 2.0 |
| Twitter/X | `[auth.external.twitter]` | OAuth 2.0 |
| Azure AD | `[auth.external.azure]` | OAuth 2.0 / OIDC |
| LinkedIn (OIDC) | `[auth.external.linkedin_oidc]` | OIDC; legacy `linkedin` provider deprecated |
| SAML SSO | Dashboard config | Enterprise; metadata URL drift is the common failure |

## User Management via SQL

Query and manage users using MCP `execute_sql`:

```sql
-- List recent signups
SELECT id, email, created_at, last_sign_in_at, is_anonymous
FROM auth.users
ORDER BY created_at DESC
LIMIT 20;

-- Count users by provider
SELECT raw_app_meta_data->>'provider' as provider, count(*)
FROM auth.users
GROUP BY provider;

-- Check user metadata (DO NOT use raw_user_meta_data in RLS — user-writable)
SELECT id, email, raw_app_meta_data, raw_user_meta_data
FROM auth.users
WHERE email = 'user@example.com';
```

## Auth + RLS Integration

The core pattern: RLS policies use `(select auth.uid())` to reference the current authenticated user. **Always wrap in subquery** for initPlan caching (Splinter lint 0003).

```sql
-- Users can only read their own profile
create policy "Users read own profile"
  on public.profiles for select
  to authenticated
  using ((select auth.uid()) = id);

-- Users can only insert their own profile
create policy "Users insert own profile"
  on public.profiles for insert
  to authenticated
  with check ((select auth.uid()) = id);
```

See the security skill for the full RLS pattern catalog.

## Auth Logs (MCP)

```
mcp__supabase__get_logs(project_id: "<id>", service: "auth")
```

Returns auth-related logs from the last 24 hours. Useful for debugging sign-in failures, provider issues, and JWT problems.

## Common Auth Patterns

### Profile Creation on Sign-Up (Database Trigger)

```sql
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, display_name, email)
  values (
    new.id,
    new.raw_user_meta_data->>'full_name',  -- OK in trigger; user controls only their own
    new.email
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

**Note:** reading `raw_user_meta_data` is acceptable in a trigger that fires on the user's own insert — they can only set their own metadata. **Never** read it in an RLS policy on another table where a user could attacker-control the value (Splinter lint 0015).

### Protected API Route Pattern

```typescript
// Middleware pattern for edge functions
function requireAuth(handler: (req: Request, user: User) => Promise<Response>) {
  return async (req: Request) => {
    const supabase = createClient(/* ... with auth header */);
    const { data: { user }, error } = await supabase.auth.getUser();
    if (!user) return new Response("Unauthorized", { status: 401 });
    return handler(req, user);
  };
}
```

## Searching Supabase Auth Docs (MCP)

For the latest auth documentation, use:
```
mcp__supabase__search_docs(query: "auth <specific topic>")
```
