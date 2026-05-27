---
name: provider-id-oauth
description: |
  ขั้นตอนการติดตั้งและตั้งค่า Provider ID OAuth (ผ่าน Health ID / moph.id.th) ด้วย Auth.js (next-auth v5)
  ใน Next.js App Router — ครอบคลุม: การติดตั้ง package, การสร้างปุ่ม Login, การ redirect ไปยัง
  OAuth Provider, การรับ callback พร้อม exchange token, การดึง profile จาก provider.id.th,
  และการสร้าง session ด้วย Auth.js Credentials Provider + JWT Strategy.
---

# Provider ID OAuth with Auth.js (Next.js App Router)

## ภาพรวมสถาปัตยกรรม (Architecture Overview)

ระบบนี้ใช้ **OAuth Authorization Code Flow** ดังนี้:

```
┌────────────────┐       ┌─────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│  Login Button  │──①──▶│  moph.id.th     │──②──▶│  /api/auth/      │──③──▶│  provider.id.th  │
│  (Server       │       │  OAuth Redirect  │       │  healthid        │       │  Token + Profile │
│   Action)      │       │                  │◀──②──│  (Callback)      │◀──③──│                  │
└────────────────┘       └─────────────────┘       └──────┬───────────┘       └──────────────────┘
                                                          │④
                                                   ┌──────▼───────────┐
                                                   │  Auth.js signIn  │
                                                   │  (Credentials)   │
                                                   │  → JWT Session   │
                                                   └──────────────────┘
```

**Flow อธิบาย:**

1. ① User กดปุ่ม Login → Server Action ตั้ง cookie แล้ว redirect ไปยัง `moph.id.th/oauth/redirect`
2. ② User ให้สิทธิ์ที่ moph.id.th → redirect กลับมายัง `/api/auth/healthid?code=xxx`
3. ③ Route handler นำ `code` ไป exchange token กับ `moph.id.th/api/v1/token` แล้วใช้ token ดึง profile จาก `provider.id.th`
4. ④ นำ profile ที่ได้มาเรียก `signIn('credentials', ...)` ของ Auth.js เพื่อสร้าง JWT session

---

## ขั้นตอนที่ 1: ติดตั้ง Auth.js (next-auth v5)

### 1.1 ติดตั้ง Package

```bash
npm install next-auth@latest
```

> **หมายเหตุ:** Auth.js v5 (ชื่อ package ยังเป็น `next-auth`) รองรับ Next.js App Router โดยตรง
> ณ เวลาที่เขียน ใช้เวอร์ชัน `next-auth@5.0.0-beta.28` หรือใหม่กว่า

### 1.2 ตั้งค่า Environment Variables

สร้าง/แก้ไขไฟล์ `.env.local`:

```env
# ===== Auth.js =====
# สร้างด้วย: openssl rand -base64 32
AUTH_SECRET=your_random_secret_here

# ===== Health ID (moph.id.th) =====
HEALTH_CLIENT_ID=your_health_client_id
HEALTH_CLIENT_SECRET=your_health_client_secret
HEALTH_REDIRECT_URI=http://localhost:3000/api/auth/healthid

# ===== Provider ID (provider.id.th) =====
PROVIDER_CLIENT_ID=your_provider_client_id
PROVIDER_CLIENT_SECRET=your_provider_client_secret
```

> **สำคัญ:** `HEALTH_REDIRECT_URI` ต้องตรงกับที่ลงทะเบียนไว้กับ moph.id.th
> สำหรับ production ให้เปลี่ยนเป็น `https://yourdomain.com/api/auth/healthid`

### 1.3 สร้างไฟล์ Auth Config — `src/authConfig.ts`

```typescript
import NextAuth, { type Session, type NextAuthConfig } from "next-auth";
import type { JWT } from "next-auth/jwt";
import CredentialsProvider from "next-auth/providers/credentials";

const authOptions: NextAuthConfig = {
  session: {
    strategy: "jwt",
    maxAge: 60 * 60 * 25, // 25 ชั่วโมง
  },
  providers: [
    CredentialsProvider({
      async authorize(credentials) {
        // รองรับ login จาก Health ID (OAuth callback)
        if (credentials["cred-way"] === "health-id") {
          return {
            name: (credentials.username as string) || "health-id",
            profile: credentials.profile!,
          };
        }

        // รองรับ login แบบ username/password (ถ้าต้องการ)
        if (credentials["cred-way"] === "user-pass") {
          // TODO: ตรวจสอบ username/password กับฐานข้อมูล
          return null;
        }

        return null;
      },
    }),
    // เพิ่ม Provider อื่นได้ตามต้องการ เช่น Google, GitHub, Line
  ],
  callbacks: {
    async jwt({ token, user }: { token: JWT; user?: any }) {
      if (user) {
        // เก็บ profile ลง JWT token ตอน login ครั้งแรก
        token.profile = (user as any).profile;
      }
      return token;
    },
    async session({ session, token }: { session: Session; token: JWT }) {
      if (token && session.user) {
        // ส่ง profile ไปให้ client ผ่าน session
        (session.user as any).profile = (token as any).profile;
      }
      return session;
    },
  },
};

export const { handlers, auth, signIn, signOut } = NextAuth(authOptions);
```

**หลักการสำคัญ:**

- ใช้ `CredentialsProvider` เป็น "ทางเข้า" ของ Auth.js — ไม่ได้หมายความว่า login ด้วย password เท่านั้น
- ใช้ค่า `credentials['cred-way']` เพื่อแยกว่า login มาจากทางไหน (health-id, user-pass, ...)
- เก็บ `profile` (JSON string) ลงใน JWT token ผ่าน `jwt` callback
- ส่ง `profile` ให้ client ผ่าน `session` callback

### 1.4 สร้าง Route Handler — `src/app/api/auth/[...nextauth]/route.ts`

```typescript
import { handlers } from "@/authConfig";

export const { GET, POST } = handlers;
```

> ไฟล์นี้ทำหน้าที่ expose GET/POST handlers ของ Auth.js ที่ path `/api/auth/*`

---

## ขั้นตอนที่ 2: สร้างปุ่ม Login (Server Action)

### 2.1 สร้าง Server Action — `src/app/actions/sign-in.ts`

```typescript
"use server";

import { redirect } from "next/navigation";
import { cookies } from "next/headers";

export const signInWithHealthId = async (formData: FormData) => {
  const department = formData.get("department") as string;
  const redirectTo = (formData.get("redirectTo") as string) || "/home";

  // เก็บข้อมูลลง cookie เพื่อใช้หลัง OAuth redirect กลับมา
  const cookieStore = await cookies();
  cookieStore.set("selectedDepartment", department, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 60 * 60 * 24, // 24 ชั่วโมง
  });
  cookieStore.set("redirectTo", redirectTo, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 60 * 60 * 24,
  });

  // Redirect ไปยัง moph.id.th OAuth page
  const clientId = process.env.HEALTH_CLIENT_ID;
  const redirectUri = process.env.HEALTH_REDIRECT_URI;
  const url = `https://moph.id.th/oauth/redirect?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code`;
  redirect(url);
};
```

**หลักการสำคัญ:**

- ใช้ `'use server'` ทำให้เป็น Server Action — ปลอดภัย ไม่เปิดเผย env ให้ client
- เก็บ `department` และ `redirectTo` ลง cookie ก่อน redirect เพราะหลัง OAuth callback กลับมาจะไม่มี `formData` แล้ว
- Redirect ไปยัง `moph.id.th/oauth/redirect` พร้อม `client_id`, `redirect_uri`, `response_type=code`

### 2.2 สร้างหน้า Login — `src/app/login/page.tsx`

```tsx
"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { LogIn, UserPlus } from "lucide-react";
import { useSession } from "next-auth/react";
import { signInWithHealthId } from "../actions/sign-in";

export default function LoginPage() {
  const router = useRouter();
  const { status } = useSession();

  useEffect(() => {
    // ถ้า login แล้ว redirect ไป /home
    if (status === "authenticated") {
      router.replace("/home");
    }
  }, [status, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold text-center mb-8">เข้าสู่ระบบ</h2>

        <div className="space-y-4">
          {/* ปุ่มเข้าสู่ระบบ */}
          <form action={signInWithHealthId}>
            <input type="hidden" name="department" value="" />
            <input type="hidden" name="redirectTo" value="/home" />
            <button
              type="submit"
              className="w-full px-6 py-4 bg-green-600 text-white rounded-xl 
                         hover:bg-green-700 transition-all flex items-center 
                         justify-center gap-3 font-semibold text-lg shadow-md 
                         hover:shadow-lg cursor-pointer"
            >
              <LogIn size={24} />
              เข้าสู่ระบบ
            </button>
          </form>

          {/* ปุ่มลงทะเบียน */}
          <form action={signInWithHealthId}>
            <input type="hidden" name="department" value="register" />
            <input type="hidden" name="redirectTo" value="/profile" />
            <button
              type="submit"
              className="w-full px-6 py-4 bg-blue-600 text-white rounded-xl 
                         hover:bg-blue-700 transition-all flex items-center 
                         justify-center gap-3 font-semibold text-lg shadow-md 
                         hover:shadow-lg cursor-pointer"
            >
              <UserPlus size={24} />
              ลงทะเบียนผู้ใช้งาน
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
```

**หลักการสำคัญ:**

- ใช้ `form action={signInWithHealthId}` เพื่อ submit ไปที่ Server Action
- ส่งค่า `department` และ `redirectTo` เป็น hidden fields
- ใช้ `useSession()` ตรวจสอบว่า login แล้วหรือยัง (ต้องมี `SessionProvider` ใน layout)
- ปุ่มต่างๆ ส่ง `department` ต่างกัน เพื่อแยก flow (login ปกติ vs ลงทะเบียน)

---

## ขั้นตอนที่ 3: สร้าง OAuth Callback Endpoint

### 3.1 สร้าง Route Handler — `src/app/api/auth/healthid/route.ts`

```typescript
import { NextRequest, NextResponse } from "next/server";
import { signIn } from "@/authConfig";
import { cookies } from "next/headers";

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const code = searchParams.get("code");

  // อ่าน redirectTo จาก cookie (ตั้งไว้ตอน Server Action)
  const cookieStore = await cookies();
  const redirectTo = cookieStore.get("redirectTo")?.value || "/home";

  if (!code) {
    return NextResponse.json(
      { error: "Authorization code is missing" },
      { status: 400 },
    );
  }

  // ──────────────────────────────────────
  // Step 3.1: Exchange code → Health ID Access Token
  // ──────────────────────────────────────
  const tokenResponse = await fetch("https://moph.id.th/api/v1/token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      grant_type: "authorization_code",
      code: code,
      redirect_uri: process.env.HEALTH_REDIRECT_URI,
      client_id: process.env.HEALTH_CLIENT_ID,
      client_secret: process.env.HEALTH_CLIENT_SECRET,
    }),
  });
  const tokenData = await tokenResponse.json();

  if (!tokenResponse.ok) {
    return NextResponse.json(
      { error: tokenData.error || "Failed to fetch Health ID token" },
      { status: tokenResponse.status },
    );
  }

  // ──────────────────────────────────────
  // Step 3.2: ใช้ Health ID token → ขอ Provider ID Access Token
  // ──────────────────────────────────────
  const providerTokenResponse = await fetch(
    "https://provider.id.th/api/v1/services/token",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_id: process.env.PROVIDER_CLIENT_ID,
        secret_key: process.env.PROVIDER_CLIENT_SECRET,
        token_by: "Health ID",
        token: tokenData.data.access_token,
      }),
    },
  );
  const providerTokenData = await providerTokenResponse.json();

  if (!providerTokenResponse.ok) {
    return NextResponse.json(
      { error: providerTokenData.error || "Failed to fetch provider token" },
      { status: providerTokenResponse.status },
    );
  }

  // ──────────────────────────────────────
  // Step 3.3: ใช้ Provider ID token → ดึง Profile
  // ──────────────────────────────────────
  const profileResponse = await fetch(
    "https://provider.id.th/api/v1/services/profile?position_type=1",
    {
      method: "GET",
      headers: {
        "client-id": process.env.PROVIDER_CLIENT_ID!,
        "secret-key": process.env.PROVIDER_CLIENT_SECRET!,
        Authorization: `Bearer ${providerTokenData.data.access_token}`,
      },
    },
  );
  const profileData = await profileResponse.json();

  if (!profileResponse.ok) {
    return NextResponse.json(
      { error: profileData.error || "Failed to fetch profile data" },
      { status: profileResponse.status },
    );
  }

  // ──────────────────────────────────────
  // Step 3.4: สร้าง Auth.js Session ด้วย Credentials signIn
  // ──────────────────────────────────────
  const res = await signIn("credentials", {
    "cred-way": "health-id",
    profile: JSON.stringify(profileData.data),
    redirectTo: redirectTo,
  });

  return res;
}
```

**หลักการสำคัญ (Token Exchange 3 ขั้นตอน):**

| ขั้นตอน | Endpoint                                 | ส่งอะไร                             | ได้อะไร                    |
| ------- | ---------------------------------------- | ----------------------------------- | -------------------------- |
| 3.1     | `moph.id.th/api/v1/token`                | `code` (จาก OAuth redirect)         | Health ID `access_token`   |
| 3.2     | `provider.id.th/api/v1/services/token`   | Health ID `access_token`            | Provider ID `access_token` |
| 3.3     | `provider.id.th/api/v1/services/profile` | Provider ID `access_token` (Bearer) | User Profile Data          |

> **สำคัญ:** ขั้นตอนที่ 3.2 ใช้ field name `secret_key` (ไม่ใช่ `client_secret`)
> ขั้นตอนที่ 3.3 ใช้ headers `client-id` และ `secret-key` (kebab-case)

---

## ขั้นตอนที่ 4: Auth.js Session Management

### 4.1 JWT Callbacks (ในไฟล์ authConfig.ts)

Auth.js ใช้ JWT strategy ในการจัดการ session:

```
User Login ── authorize() ─┐
                            ▼
                     jwt() callback ── เก็บ profile ลง token
                            │
                            ▼
                     session() callback ── ส่ง profile ให้ client
                            │
                            ▼
                     Session Object ── { user: { name, profile, ... } }
```

**jwt callback** — ถูกเรียกทุกครั้งที่มี token request:

- ตอน login ครั้งแรก: `user` object จะมีค่า → เก็บข้อมูลลง `token`
- ตอน refresh token: `user` จะเป็น `undefined` → return token เดิม

**session callback** — ถูกเรียกทุกครั้งที่ client ขอ session:

- คัดลอกข้อมูลจาก `token` → `session.user`

### 4.2 การใช้ Session ฝั่ง Client

```tsx
"use client";
import { useSession } from "next-auth/react";

export default function ProfilePage() {
  const { data: session } = useSession();

  if (!session) return <div>กรุณาเข้าสู่ระบบ</div>;

  const profile = JSON.parse((session.user as any).profile || "{}");

  return (
    <div>
      <p>
        ชื่อ: {profile.first_name} {profile.last_name}
      </p>
      <p>Provider ID: {profile.provider_id}</p>
    </div>
  );
}
```

### 4.3 การใช้ Session ฝั่ง Server

```typescript
import { auth } from "@/authConfig";

export default async function ServerPage() {
  const session = await auth();

  if (!session) {
    // redirect หรือ return unauthorized
  }

  const profile = JSON.parse((session.user as any).profile || "{}");
  // ใช้ profile ได้ตรงนี้
}
```

### 4.4 SessionProvider (จำเป็นสำหรับ Client Components)

ต้องเพิ่ม `SessionProvider` ใน root layout:

```tsx
// src/app/layout.tsx
import { SessionProvider } from "next-auth/react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
```

### 4.5 Sign Out

```typescript
// Server Action
import { signOut } from '@/authConfig';

export async function handleSignOut() {
  await signOut({ redirectTo: '/login' });
}

// Client Component
import { signOut } from 'next-auth/react';

<button onClick={() => signOut({ callbackUrl: '/login' })}>
  ออกจากระบบ
</button>
```

---

## ขั้นตอนที่ 5: Protecting Routes (ป้องกัน Route)

> **⚠️ Next.js 16 เปลี่ยนชื่อ:** ตั้งแต่ Next.js 16 เป็นต้นไป `middleware.ts` ถูก **deprecated** และเปลี่ยนชื่อเป็น `proxy.ts`
> Functionality ทั้งหมดยังเหมือนเดิม แค่เปลี่ยนชื่อไฟล์และ function

Auth.js v5 + Next.js 16 มี **4 วิธี** ป้องกันหน้าที่ต้อง login ก่อนเข้าถึง:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    วิธีป้องกัน Route ทั้ง 4 แบบ                      │
├───────────────────┬──────────────────────────────────────────────────┤
│  ① Proxy (proxy.ts)│  ป้องกัน ทุกหน้า ก่อน render (แนะนำ)           │
│  ② Server Component│  ตรวจสอบ session ในแต่ละ page component        │
│  ③ API Route       │  ป้องกัน API endpoint                           │
│  ④ authorized cb   │  ตรวจสอบใน authConfig.ts callback               │
└───────────────────┴──────────────────────────────────────────────────┘
```

### 5.1 วิธีที่ 1: Proxy (แนะนำ — ป้องกันทุก Route)

สร้างไฟล์ `src/proxy.ts` (ต้องอยู่ใน root ของ `src/` หรือ root ของ project):

#### แบบที่ 1: Simple — redirect ทุกหน้าไป login

```typescript
// src/proxy.ts
import { auth } from "@/authConfig";

export default auth((req) => {
  // req.auth มีข้อมูล session (หรือ null ถ้ายังไม่ login)
  // ถ้าไม่มี session → Auth.js จะ redirect ไปหน้า sign-in อัตโนมัติ
});

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

> วิธีนี้จะป้องกันทุกหน้ายกเว้น `api`, `_next/static`, `_next/image`, `favicon.ico`
> ถ้าไม่มี session จะ redirect ไปหน้า sign-in อัตโนมัติ

#### แบบที่ 2: Custom Logic — เลือกหน้าที่ต้อง protect

```typescript
// src/proxy.ts
import { auth } from "@/authConfig";

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const { pathname } = req.nextUrl;

  // หน้าที่ไม่ต้อง login (public routes)
  const publicRoutes = ["/", "/login", "/register", "/about"];
  const isPublicRoute = publicRoutes.includes(pathname);

  // ถ้าไม่ public และยังไม่ login → redirect ไป /login
  if (!isPublicRoute && !isLoggedIn) {
    const loginUrl = new URL("/login", req.nextUrl.origin);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return Response.redirect(loginUrl);
  }

  // ถ้า login แล้วแต่เข้าหน้า /login → redirect ไป /home
  if (isLoggedIn && pathname === "/login") {
    return Response.redirect(new URL("/home", req.nextUrl.origin));
  }
});

export const config = {
  matcher: ["/((?!api/auth|_next/static|_next/image|favicon.ico).*)"],
};
```

**หลักการสำคัญ:**

- `auth()` wrapper ทำให้ `req.auth` มีข้อมูล session (หรือ `null` ถ้า ยังไม่ login)
- `matcher` กำหนดว่า proxy จะทำงานกับ path ไหนบ้าง (ใช้ regex)
- **ห้าม** block path `/api/auth/*` เพราะเป็น endpoint ของ Auth.js เอง
- สามารถเพิ่ม `callbackUrl` ไว้ใน URL เพื่อ redirect กลับหลัง login

#### แบบที่ 3: Protect เฉพาะบาง path patterns

```typescript
// src/proxy.ts
import { auth } from "@/authConfig";

export default auth((req) => {
  if (!req.auth) {
    return Response.redirect(new URL("/login", req.nextUrl.origin));
  }
});

export const config = {
  matcher: [
    "/dashboard/:path*", // protect ทุกหน้าภายใต้ /dashboard
    "/profile/:path*", // protect ทุกหน้าภายใต้ /profile
    "/admin/:path*", // protect ทุกหน้าภายใต้ /admin
    "/api/protected/:path*", // protect API routes เฉพาะกลุ่ม
  ],
};
```

> วิธีนี้เหมาะเมื่อมีหลายหน้า public และต้องการ protect เฉพาะบางกลุ่ม

### 5.2 วิธีที่ 2: Server Component — ตรวจ session ในแต่ละ page

เหมาะสำหรับ protect เฉพาะบางหน้า หรือแสดงเนื้อหาต่างกันตาม login status:

```typescript
// src/app/dashboard/page.tsx
import { auth } from "@/authConfig";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  // ถ้ายังไม่ login → redirect ไป /login
  if (!session) {
    redirect("/login");
  }

  const profile = JSON.parse((session.user as any).profile || "{}");

  return (
    <div>
      <h1>Dashboard</h1>
      <p>ยินดีต้อนรับ {profile.first_name} {profile.last_name}</p>
    </div>
  );
}
```

**ข้อดี:**

- ควบคุมได้ละเอียดในแต่ละหน้า
- สามารถแสดงเนื้อหาต่างกันสำหรับ logged-in vs guest

**ข้อเสีย:**

- ต้องเขียนซ้ำทุกหน้าที่ต้องการ protect
- หน้าจะ render ก่อนแล้วค่อย redirect (ช้ากว่า proxy)

### 5.3 วิธีที่ 3: API Route Protection

ป้องกัน API endpoint ไม่ให้ถูกเรียกโดยไม่ได้ login:

```typescript
// src/app/api/protected/data/route.ts
import { auth } from "@/authConfig";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await auth();

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const profile = JSON.parse((session.user as any).profile || "{}");

  // ดำเนินการต่อ — user ผ่านการ authenticate แล้ว
  return NextResponse.json({
    message: "Protected data",
    user: profile.first_name,
  });
}
```

### 5.4 วิธีที่ 4: `authorized` Callback (ใน authConfig.ts)

เพิ่ม `authorized` callback ใน `authConfig.ts` เพื่อป้องกัน route ระดับ config:

```typescript
// src/authConfig.ts — เพิ่มใน callbacks
const authOptions: NextAuthConfig = {
  // ... providers, session, etc.
  pages: {
    signIn: "/login", // กำหนดหน้า login custom
  },
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isOnProtected =
        nextUrl.pathname.startsWith("/dashboard") ||
        nextUrl.pathname.startsWith("/profile") ||
        nextUrl.pathname.startsWith("/admin");

      if (isOnProtected) {
        if (isLoggedIn) return true; // อนุญาต
        return false; // redirect ไป signIn page
      }

      return true; // อนุญาตหน้า public
    },
    // ... jwt, session callbacks
  },
};
```

> **หมายเหตุ:** วิธีนี้ทำงานร่วมกับ proxy — ต้อง export proxy function ด้วย
> `authorized` callback จะถูกเรียกโดย proxy อัตโนมัติ

ใช้ร่วมกับ proxy แบบ simple:

```typescript
// src/proxy.ts
import { auth } from "@/authConfig";

export default auth((req) => {
  // authorized callback ใน authConfig.ts จะถูกเรียกอัตโนมัติ
});

export const config = {
  matcher: ["/((?!api/auth|_next/static|_next/image|favicon.ico).*)"],
};
```

### 5.5 ตารางเปรียบเทียบ

| วิธี                      | เมื่อไรใช้                 | ข้อดี                          | ข้อเสีย                 |
| ------------------------- | -------------------------- | ------------------------------ | ----------------------- |
| **① Proxy**               | ป้องกันทุกหน้า / กลุ่มหน้า | เร็วที่สุด ทำงานก่อน render    | จำกัดเฉพาะ Edge Runtime |
| **② Server Component**    | ป้องกันเฉพาะบางหน้า        | ยืดหยุ่นสูง แสดง UI ต่างกันได้ | ต้องเขียนซ้ำทุกหน้า     |
| **③ API Route**           | ป้องกัน API endpoint       | เหมาะกับ REST API              | ใช้ได้เฉพาะ API routes  |
| **④ authorized callback** | กำหนด logic รวมศูนย์       | config ที่เดียว ใช้ได้ทั้งระบบ | ต้องใช้คู่กับ proxy     |

### 5.6 แนะนำ: ใช้ Proxy + Server Component ร่วมกัน

ในทางปฏิบัติ ให้ใช้ **Proxy** เป็น "ด่านแรก" และ **Server Component** เป็น "ด่านที่สอง":

```
Request
  │
  ▼
┌──────────────────────────────┐
│  Proxy (ด่านที่ 1)            │  ← เร็ว, block ก่อน render
│  ตรวจ: login แล้วหรือยัง?     │
│  ถ้ายัง → redirect /login     │
└──────────────┬───────────────┘
               │ ผ่าน
               ▼
┌──────────────────────────────┐
│  Server Component (ด่านที่ 2) │  ← ละเอียด, ตรวจ role/permission
│  ตรวจ: session มี role ที่     │
│  เหมาะสมไหม?                  │
└──────────────────────────────┘
```

ตัวอย่าง Role-based protection ใน Server Component:

```typescript
// src/app/admin/page.tsx
import { auth } from "@/authConfig";
import { redirect } from "next/navigation";

export default async function AdminPage() {
  const session = await auth();
  if (!session) redirect("/login");

  const profile = JSON.parse((session.user as any).profile || "{}");

  // ตรวจสอบ role — ต้องเป็น admin
  if (profile.role !== 'admin') {
    redirect("/unauthorized");
  }

  return <div>Admin Dashboard</div>;
}
```

---

## โครงสร้างไฟล์ทั้งหมด

```
src/
├── authConfig.ts                          # Auth.js configuration + NextAuth export
├── proxy.ts                               # Route protection proxy (Next.js 16+)
├── app/
│   ├── layout.tsx                         # SessionProvider wrapper
│   ├── login/
│   │   └── page.tsx                       # หน้า Login (Client Component)
│   ├── actions/
│   │   └── sign-in.ts                     # Server Action: redirect to OAuth
│   └── api/
│       └── auth/
│           ├── [...nextauth]/
│           │   └── route.ts               # Auth.js route handler (GET, POST)
│           └── healthid/
│               └── route.ts               # OAuth callback: token exchange + signIn
```

---

## Environment Variables อ้างอิง

| ชื่อ                     | คำอธิบาย                      | ตัวอย่าง                                  |
| ------------------------ | ----------------------------- | ----------------------------------------- |
| `AUTH_SECRET`            | Secret สำหรับ encrypt JWT     | `openssl rand -base64 32`                 |
| `HEALTH_CLIENT_ID`       | Client ID จาก moph.id.th      | -                                         |
| `HEALTH_CLIENT_SECRET`   | Client Secret จาก moph.id.th  | -                                         |
| `HEALTH_REDIRECT_URI`    | OAuth callback URL            | `http://localhost:3000/api/auth/healthid` |
| `PROVIDER_CLIENT_ID`     | Client ID จาก provider.id.th  | -                                         |
| `PROVIDER_CLIENT_SECRET` | Secret Key จาก provider.id.th | -                                         |

---

## API Endpoints อ้างอิง

### moph.id.th (Health ID)

| Endpoint                            | Method         | คำอธิบาย                   |
| ----------------------------------- | -------------- | -------------------------- |
| `https://moph.id.th/oauth/redirect` | GET (redirect) | หน้า OAuth consent         |
| `https://moph.id.th/api/v1/token`   | POST           | แลก code เป็น access_token |

**Token Request Body:**

```json
{
  "grant_type": "authorization_code",
  "code": "<authorization_code>",
  "redirect_uri": "<HEALTH_REDIRECT_URI>",
  "client_id": "<HEALTH_CLIENT_ID>",
  "client_secret": "<HEALTH_CLIENT_SECRET>"
}
```

### provider.id.th (Provider ID)

| Endpoint                                         | Method | คำอธิบาย                                |
| ------------------------------------------------ | ------ | --------------------------------------- |
| `https://provider.id.th/api/v1/services/token`   | POST   | แลก Health ID token เป็น Provider token |
| `https://provider.id.th/api/v1/services/profile` | GET    | ดึง profile ด้วย Provider token         |

**Provider Token Request Body:**

```json
{
  "client_id": "<PROVIDER_CLIENT_ID>",
  "secret_key": "<PROVIDER_CLIENT_SECRET>",
  "token_by": "Health ID",
  "token": "<health_id_access_token>"
}
```

**Profile Request Headers:**

```
client-id: <PROVIDER_CLIENT_ID>
secret-key: <PROVIDER_CLIENT_SECRET>
Authorization: Bearer <provider_access_token>
```

---

## Troubleshooting

### ปัญหาที่พบบ่อย

1. **`AUTH_SECRET` ไม่ได้ตั้งค่า**
   - Error: `[auth][error] MissingSecret`
   - แก้: เพิ่ม `AUTH_SECRET` ใน `.env.local`

2. **Redirect URI ไม่ตรง**
   - Error: moph.id.th ส่ง error กลับมา
   - แก้: ตรวจสอบว่า `HEALTH_REDIRECT_URI` ตรงกับที่ลงทะเบียนไว้ทุกตัวอักษร

3. **field name ผิด ใน Provider ID API**
   - ใช้ `secret_key` (ไม่ใช่ `client_secret`) ใน token request
   - ใช้ `secret-key` (kebab-case) ใน profile request header

4. **Cookie หายหลัง OAuth redirect**
   - ตรวจสอบว่า `sameSite: 'lax'` (ไม่ใช่ `strict`)
   - ตรวจสอบว่า `secure: true` เฉพาะ production

5. **Session ว่าง / profile เป็น undefined**
   - ตรวจสอบว่ามี `SessionProvider` ใน layout.tsx
   - ตรวจสอบว่า `jwt` callback เก็บ `token.profile` ถูกต้อง

---

## เพิ่มเติม: ตัวอย่างการเพิ่ม Department ลงใน Session

ถ้าต้องการเก็บ `department` ลง session ด้วย:

```typescript
// ใน authConfig.ts — jwt callback
async jwt({ token, user }) {
  if (user) {
    token.profile = (user as any).profile;

    // อ่าน department จาก cookie
    const cookieStore = await cookies();
    const department = cookieStore.get('selectedDepartment')?.value;
    if (department) {
      (token as any).ssj_department = department;
      cookieStore.delete('selectedDepartment'); // ลบ cookie หลังอ่าน
    }
  }
  return token;
},

// ใน authConfig.ts — session callback
async session({ session, token }) {
  if (token && session.user) {
    (session.user as any).profile = (token as any).profile;
    (session.user as any).ssj_department = (token as any).ssj_department;
  }
  return session;
},
```

---

## เพิ่มเติม: ตัวอย่างการ Track Login ลงฐานข้อมูล (Prisma)

```typescript
// ใน jwt callback — หลังจาก set token.profile
try {
  const profile =
    typeof (user as any).profile === "string"
      ? JSON.parse((user as any).profile)
      : (user as any).profile;

  const providerId = profile.provider_id || profile.sub || user.name;

  await prisma.accountUser.updateMany({
    where: { provider_id: providerId, active: true },
    data: {
      last_login: new Date(),
      login_count: { increment: 1 },
    },
  });
} catch (error) {
  console.error("Error updating login tracking:", error);
}
```
