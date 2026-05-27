---
name: auth-supabase-complete
description: Production-ready Supabase authentication for Next.js 14+ with RLS patterns, session management, OAuth flows, and comprehensive testing. Includes server-side auth helpers, API middleware, and route protection.
effort: high
license: MIT
---

# Auth Supabase Complete

Complete Supabase authentication patterns for Next.js applications with server-side rendering, Row Level Security, and production-ready examples.

## When to Use

Use this skill when building Next.js applications that need:
- User authentication (email/password + OAuth)
- Server-side auth with Next.js 14+ App Router
- Row Level Security (RLS) patterns
- Protected API routes with middleware
- Admin/role-based access control
- Session management in middleware
- Profile management

**Don't use this skill if:**
- You're using Next.js Pages Router (this uses App Router only)
- You need a different auth provider (not Supabase)
- You're building a simple static site without auth

## Stack

- Next.js 14+ (App Router)
- Supabase Auth + Database
- TypeScript (strict mode)
- @supabase/ssr (Server-Side Rendering)
- @supabase/supabase-js
- Vitest (testing)

## Quick Start

### 1. Install Dependencies

```bash
npm install @supabase/ssr @supabase/supabase-js
npm install -D @project-forge/auth-supabase-complete
```

### 2. Setup Environment Variables

```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # For admin operations
```

### 3. Create Configuration

```typescript
// lib/config.ts
export const supabaseConfig = {
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
}
```

### 4. Use in Server Components

```typescript
import { getUser } from '@project-forge/auth-supabase-complete/auth'
import { supabaseConfig } from '@/lib/config'

export default async function DashboardPage() {
  const user = await getUser(supabaseConfig)

  if (!user) redirect('/auth/login')

  return <div>Welcome {user.email}</div>
}
```

### 5. Protect API Routes

```typescript
import { requireAuth } from '@project-forge/auth-supabase-complete/require-auth'
import { supabaseConfig } from '@/lib/config'

export async function GET(request: NextRequest) {
  const { user, error, supabase } = await requireAuth(supabaseConfig, request)

  if (error) return error  // 401 Unauthorized

  // Use authenticated supabase client with RLS
  const { data } = await supabase.from('posts').select('*')
  return NextResponse.json({ data })
}
```

## Key Features

### Three Server Clients

The skill provides three types of Supabase clients for different Next.js contexts:

1. **Server Component Client** - Uses `cookies()` from `next/headers`
```typescript
import { createClient } from '@project-forge/auth-supabase-complete/server'
const supabase = await createClient(config)
```

2. **Route Handler Client** - Uses `NextRequest` cookies
```typescript
import { createRouteHandlerClient } from '@project-forge/auth-supabase-complete/server'
const supabase = createRouteHandlerClient(config, request, response)
```

3. **Service Role Client** - Bypasses RLS for admin operations
```typescript
import { createServiceClient } from '@project-forge/auth-supabase-complete/server'
const supabase = createServiceClient(config)
```

### Auth Utilities

Five helper functions for common auth operations:

- `signOut(config, redirectUrl?)` - Sign out with redirect
- `getUser(config)` - Get current authenticated user
- `getProfile<T>(config, tableName?)` - Fetch user profile
- `getUserWithProfile<T>(config, tableName?)` - Get user + profile together
- `getSupabaseClient<DB>(config)` - Get Supabase client instance

### API Middleware

Two middleware functions for protecting API routes:

- `requireAuth(config, request?)` - Require authentication
- `requireAdminAuth(config, request?, options?)` - Require admin privileges

Both return:
```typescript
{ user: User, error: null, supabase: Client } |
{ user: null, error: NextResponse, supabase: null }
```

### Route Protection

Utilities for middleware route matching:

- `isPublicRoute(pathname, publicRoutes?)` - Check if route is public
- `isProtectedRoute(pathname, publicRoutes?)` - Check if route needs auth
- `createRouteMatcher(publicRoutes)` - Create custom matcher
- `DEFAULT_PUBLIC_ROUTES` - Standard public routes

## Architecture Principles

### Configuration Pattern

All functions accept explicit configuration objects instead of hard-coded `process.env`:

```typescript
// ✅ Good - Explicit configuration
const config = {
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
}
const user = await getUser(config)

// ❌ Bad - Hard-coded env vars inside skill
const user = await getUser() // Would read process.env internally
```

**Benefits:**
- Testable (inject mock config)
- Flexible (multi-tenant, different Supabase projects)
- Explicit dependencies

### TypeScript Generics

All clients support generic Database types for type-safe queries:

```typescript
import type { Database } from '@/types/database'

const supabase = await createClient<Database>(config)
const { data } = await supabase.from('posts').select('*')
// data is fully typed based on your Database schema
```

### Zero Path Aliases

The skill has no internal `@/` path aliases - fully portable across projects.

### Customizable Admin Checks

Admin middleware supports custom table and field names:

```typescript
await requireAdminAuth(config, request, {
  profilesTable: 'user_profiles',  // Default: 'profiles'
  adminField: 'role',              // Default: 'is_admin'
})
```

## Examples

The skill includes 7 production-ready examples in `examples/`:

1. **Browser Auth Forms** (`01-browser-auth.tsx`)
   - Sign in/up forms with validation
   - Password strength indicator
   - Email verification flow
   - Password reset

2. **Server Components** (`02-server-component-auth.tsx`)
   - Protected pages
   - Profile fetching
   - User header component
   - Conditional content

3. **API Routes** (`03-api-route-auth.ts`)
   - GET/POST/PATCH/DELETE with requireAuth
   - Input validation
   - Error handling
   - Pagination

4. **Admin API Routes** (`04-admin-api-route.ts`)
   - User management
   - Role updates
   - Bulk operations
   - Audit logging

5. **Middleware** (`05-middleware.ts`)
   - Session refresh
   - Protected routes
   - Admin routes
   - Role-based access (8 examples)

6. **OAuth Social Auth** (`06-social-auth.tsx`)
   - Google, GitHub, Twitter, Discord
   - Link/unlink accounts
   - Provider info

7. **Profile Setup** (`07-profile-setup.tsx`)
   - Multi-step onboarding
   - Avatar upload
   - Username validation
   - Preferences

## Testing

The skill has **97% test coverage** with 74 tests:

```bash
npm test              # Run all tests
npm test -- --coverage  # With coverage report
```

**Test structure:**
- Unit tests for each module (route-matcher, client, server, auth, require-auth)
- Integration tests (index exports)
- E2E tests (auth flows: signup, login, OAuth, password reset)

## References

For detailed implementation guides, see:

- **RLS Setup & Patterns** → `references/RLS_PATTERNS.md`
  - Database schema (profiles table)
  - RLS policies (read own, admin read all, etc.)
  - Multi-tenant patterns
  - Performance optimization
  - Common pitfalls

- **Session Management** → `references/MIDDLEWARE_GUIDE.md`
  - Session refresh patterns
  - Protected routes
  - Role-based access control
  - Performance optimization
  - Error handling
  - Production middleware

## Common Patterns

### Pattern 1: Protected Server Component

```typescript
import { getUser } from '@project-forge/auth-supabase-complete/auth'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const user = await getUser(config)
  if (!user) redirect('/auth/login')

  return <div>Protected content for {user.email}</div>
}
```

### Pattern 2: API Route with Auth

```typescript
import { requireAuth } from '@project-forge/auth-supabase-complete/require-auth'

export async function POST(request: NextRequest) {
  const { user, error, supabase } = await requireAuth(config, request)
  if (error) return error

  const body = await request.json()
  const { data } = await supabase.from('posts').insert({
    user_id: user.id,
    ...body
  })

  return NextResponse.json(data)
}
```

### Pattern 3: Admin-Only Route

```typescript
import { requireAdminAuth } from '@project-forge/auth-supabase-complete/require-auth'

export async function DELETE(request: NextRequest) {
  const { user, error, supabase } = await requireAdminAuth(config, request)
  if (error) return error

  // Admin operations with service role
  // RLS is bypassed
}
```

### Pattern 4: Middleware Session Refresh

```typescript
import { createRouteHandlerClient } from '@project-forge/auth-supabase-complete/server'
import { isPublicRoute } from '@project-forge/auth-supabase-complete/route-matcher'

export async function middleware(request: NextRequest) {
  if (isPublicRoute(request.nextUrl.pathname)) {
    return NextResponse.next()
  }

  const response = NextResponse.next()
  const supabase = createRouteHandlerClient(config, request, response)

  // Refreshes session automatically
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.redirect(new URL('/auth/login', request.url))
  }

  return response
}
```

## Troubleshooting

**Session not refreshing?**
- Ensure you pass `response` to `createRouteHandlerClient()`
- Return the same `response` object from middleware

**401 errors in API routes?**
- Check cookies are being sent from client
- Verify `NEXT_PUBLIC_SUPABASE_URL` is public (client-side accessible)
- Use `requireAuth()` with `request` parameter

**RLS blocking queries?**
- Use `createServiceClient()` for admin operations (bypasses RLS)
- Check RLS policies are configured correctly (see `references/RLS_PATTERNS.md`)

**TypeScript errors?**
- Generate Database types: `npx supabase gen types typescript --project-id your-project > types/database.ts`
- Use generic: `createClient<Database>(config)`

## License

MIT - See LICENSE file for details

---

**Documentation Version:** 1.0.0
**Last Updated:** 2026-01-17
**Skill Compatibility:** Claude Code 2.1+, Claude Desktop, Claude.ai Pro/Max
