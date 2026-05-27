---
name: auth-patterns-nextjs
description: Authentication patterns for Next.js applications using NextAuth.js (Auth.js) v5. Covers OAuth providers, credentials auth, middleware protection, session management, and role-based access control. Use when implementing auth in Next.js App Router projects with email/password, social login, JWT, or database sessions.
---

# Auth Patterns — Next.js

Next.js App Router projeleri için authentication pattern'ları. NextAuth.js v5 (Auth.js) temel alınmıştır.

**Not**: Talent Architect Firebase Auth kullanır. Bu skill Next.js App Router + NextAuth.js kullanan genel projeler içindir.

---

## 1. Library Seçimi

| Library               | En İyi Olduğu Durum                   |
| --------------------- | ------------------------------------- |
| NextAuth.js (Auth.js) | Provider-based auth, tam özellik seti |
| Better Auth           | TypeScript-first, plugin ekosistemi   |
| Clerk                 | Managed auth servisi, hızlı kurulum   |
| Lucia                 | Lightweight, tam kontrol              |
| Custom JWT            | Tam kontrol, minimal bağımlılık       |

---

## 2. NextAuth.js v5 Kurulum

```bash
npm install next-auth@beta
```

### Konfigürasyon

```typescript
// auth.ts (root, lib/ veya src/ altında)
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import Google from 'next-auth/providers/google'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    Google({
      clientId: process.env.GOOGLE_ID!,
      clientSecret: process.env.GOOGLE_SECRET!,
    }),
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      authorize: async (credentials) => {
        const user = await getUserByEmail(credentials.email as string)
        if (!user) return null
        const valid = await verifyPassword(credentials.password as string, user.password)
        if (!valid) return null
        return user
      },
    }),
  ],
  callbacks: {
    authorized: async ({ auth }) => !!auth,
  },
})
```

### API Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'

export const { GET, POST } = handlers
```

---

## 3. Middleware ile Route Koruma

```typescript
// middleware.ts
export { auth as middleware } from '@/auth'

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*', '/api/protected/:path*'],
}
```

### Gelişmiş Middleware Pattern

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const protectedRoutes = ['/dashboard', '/settings']
const authRoutes = ['/login', '/signup']

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value
  const { pathname } = request.nextUrl

  // Auth sayfalarından authenticated kullanıcıları yönlendir
  if (authRoutes.some((route) => pathname.startsWith(route))) {
    if (token) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
    return NextResponse.next()
  }

  // Protected route'ları koru
  if (protectedRoutes.some((route) => pathname.startsWith(route))) {
    if (!token) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('callbackUrl', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
```

---

## 4. Session Erişimi

### Server Component'te

```typescript
// app/dashboard/page.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth()

  if (!session) redirect('/login')

  return (
    <div>
      <h1>Hoş geldin, {session.user?.name}</h1>
    </div>
  )
}
```

### Client Component'te

```typescript
// components/user-menu.tsx
'use client'

import { useSession } from 'next-auth/react'

export function UserMenu() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <Skeleton />
  if (!session) return <SignInButton />

  return (
    <div>
      <span>{session.user?.name}</span>
      <SignOutButton />
    </div>
  )
}
```

### Session Provider

```typescript
// app/providers.tsx
'use client'

import { SessionProvider } from 'next-auth/react'

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}

// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

---

## 5. Sign In/Out — Server Action Pattern

```typescript
// components/auth-buttons.tsx
import { signIn, signOut } from '@/auth'

export function SignInButton() {
  return (
    <form
      action={async () => {
        'use server'
        await signIn('github')
      }}
    >
      <button type='submit'>GitHub ile Giriş</button>
    </form>
  )
}

export function SignOutButton() {
  return (
    <form
      action={async () => {
        'use server'
        await signOut()
      }}
    >
      <button type='submit'>Çıkış</button>
    </form>
  )
}
```

---

## 6. Role-Based Access Control

### Session Tipini Genişlet

```typescript
// types/next-auth.d.ts
import { DefaultSession } from 'next-auth'

declare module 'next-auth' {
  interface Session {
    user: {
      role: 'user' | 'admin'
    } & DefaultSession['user']
  }
}

// auth.ts
export const { auth } = NextAuth({
  callbacks: {
    session: ({ session, token }) => ({
      ...session,
      user: {
        ...session.user,
        role: token.role as 'user' | 'admin',
      },
    }),
    jwt: ({ token, user }) => {
      if (user) token.role = (user as any).role
      return token
    },
  },
})
```

### Role Guard Component

```typescript
// components/admin-only.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export async function AdminOnly({ children }: { children: React.ReactNode }) {
  const session = await auth()

  if (session?.user?.role !== 'admin') redirect('/unauthorized')

  return <>{children}</>
}
```

---

## 7. Session Storage Seçenekleri

### JWT (Stateless — Varsayılan)

```typescript
export const { auth } = NextAuth({
  session: { strategy: 'jwt' },
  // JWT cookie'de saklanır, database gerekmez
})
```

### Database Sessions

```typescript
import { PrismaAdapter } from '@auth/prisma-adapter'
import { prisma } from '@/lib/prisma'

export const { auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'database' },
  // Session'lar database'de saklanır
})
```

---

## 8. JWT Middleware Doğrulama

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import { jwtVerify } from 'jose'

const secret = new TextEncoder().encode(process.env.JWT_SECRET!)

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  try {
    await jwtVerify(token, secret)
    return NextResponse.next()
  } catch {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}
```

---

## 9. Custom Login Sayfası

```typescript
// app/login/page.tsx
'use client'

import { signIn } from 'next-auth/react'
import { useSearchParams } from 'next/navigation'

export default function LoginPage() {
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard'

  return (
    <div className='flex flex-col gap-4'>
      <button onClick={() => signIn('github', { callbackUrl })}>
        GitHub ile Giriş
      </button>
      <button onClick={() => signIn('google', { callbackUrl })}>
        Google ile Giriş
      </button>
    </div>
  )
}
```

---

## 10. Güvenlik Kontrol Listesi

- [ ] Production'da HTTPS zorunlu
- [ ] Cookie'ler HttpOnly, Secure, SameSite=Strict
- [ ] CSRF koruması aktif (NextAuth built-in)
- [ ] Redirect URL'leri validate ediliyor
- [ ] Sırlar environment variable'larda
- [ ] Auth endpoint'lerde rate limiting uygulandı
- [ ] Şifreler bcrypt veya argon2 ile hash'lendi
- [ ] Session expiry süresi makul (7 gün önerilen)
