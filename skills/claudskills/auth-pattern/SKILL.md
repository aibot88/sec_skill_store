---
name: auth-pattern
description: Auth reference สำหรับโปรเจกต์ KAM-WEB-SCHOOLJOB — Dual Auth (Supabase + Prisma), signup/signin flow, useAuthStore interface, role-based guard, redirect pattern ใช้เพื่อลด Token โดยไม่ต้องอ่านโค้ด auth ซ้ำทุก session และป้องกัน bug จาก dual-system mismatch
---

# Auth Pattern — KAM-WEB-SCHOOLJOB

## Architecture: Dual Auth

```
[Client] → POST /api/v1/authenticate/signin
              │
              ├─ 1. Supabase Auth  → session token + user.id (uid)
              │       ↳ supabase.auth.signInWithPassword({ email, password })
              │
              ├─ 2. Prisma Profile → ดึง role + fullName จาก DB
              │       ↳ prisma.profile.findUnique({ where: { userId: uid } })
              │
              └─ 3. Merge & Return → { user_id, email, role, full_name }
                      ↳ role มาจาก user_metadata (Supabase) || profile.role (Prisma)
```

**หลักสำคัญ:** Supabase จัดการ credential/session, Prisma จัดการ profile data
Prisma failure ≠ auth failure (non-critical — ไม่ throw ถ้า Prisma ล้มเหลว)

---

## File Locations

| ไฟล์ | หน้าที่ |
|------|---------|
| `app/lib/supabase.ts` | Supabase client (ANON key) |
| `app/api/v1/authenticate/signup/route.ts` | POST /api/v1/authenticate/signup |
| `app/api/v1/authenticate/signin/route.ts` | POST /api/v1/authenticate/signin |
| `app/api/v1/authenticate/service/authenticate-service.ts` | AuthenticateService class |
| `app/api/v1/authenticate/validation/authenticate-schema.ts` | Zod schemas |
| `app/stores/auth-store.ts` | Zustand store (localStorage persist) |
| `app/components/layouts/layout-selector.tsx` | Route guard + layout selector |
| `app/pages/signin/_components/signin-form.tsx` | Signin UI + redirect logic |

---

## Supabase Client

```typescript
// app/lib/supabase.ts
import { createClient } from "@supabase/supabase-js";
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
);
```

> ใช้ ANON key เท่านั้น (client-side safe)
> SUPABASE_SERVICE_ROLE_KEY ไม่ถูกใช้งานใน codebase ปัจจุบัน

---

## Signup Flow

### Zod Schema
```typescript
// role alias: TEACHER → EMPLOYEE, SCHOOL → EMPLOYER (preprocess)
signupSchema: { email, password (min 6), full_name, role: "EMPLOYEE"|"EMPLOYER"|"ADMIN" }
```

### Service: `authService.signup(input)`
```typescript
// 1. supabase.auth.signUp({ email, password, options: { data: { full_name, role } } })
//    → user.id = Supabase UID (uuid)
//    → role + full_name บันทึกใน user_metadata ของ Supabase

// 2. prisma.profile.upsert({ where: { userId }, create/update: { email, firstName, role } })
//    → Prisma failure ไม่ throw (warn only)
//    → password field = "" (ไม่เก็บ password ใน Prisma)

// 3. Return: { id: supabaseUID, email }
```

### API Response (201)
```typescript
{
  status_code: 201,
  data: { user_id, email, full_name, role }
}
// Error → 400 พร้อม message_th ภาษาไทย
```

### Supabase Error Mapping
| Supabase message | Thai message |
|-----------------|--------------|
| "already registered" | "อีเมลนี้ถูกลงทะเบียนแล้ว" |
| "Password should be at least" | "รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร" |
| "invalid email" | "อีเมลไม่ถูกต้อง" |
| "Invalid login credentials" | "อีเมลหรือรหัสผ่านไม่ถูกต้อง" |
| "Email not confirmed" | "โปรดยืนยันอีเมลของคุณก่อน" |

---

## Signin Flow

### Service: `authService.signin(input)`
```typescript
// 1. supabase.auth.signInWithPassword({ email, password })
//    → data.user.id = Supabase UID
//    → data.session = access/refresh token
//    → data.user.user_metadata = { full_name, role } (บันทึกตอน signup)

// 2. prisma.profile.findUnique({ where: { userId: data.user.id } })
//    → ดึง role, firstName เป็น fallback
//    → Prisma failure ไม่ throw (warn only)

// 3. Merge priority:
//    full_name = user_metadata.full_name || profile.firstName || ""
//    role      = user_metadata.role      || profile.role      || "EMPLOYEE"
```

### API Response (200)
```typescript
{
  status_code: 200,
  data: { user_id, email, role, full_name }
  // ❌ ไม่คืน session token ไปฝั่ง client (Supabase จัดการ cookie เอง)
}
// Error → 401
```

---

## useAuthStore Interface

```typescript
// app/stores/auth-store.ts
// Persisted ใน localStorage key: "auth-store"

interface User {
  user_id: string;   // Supabase UID
  email: string;
  full_name: string;
  role: string;      // "EMPLOYEE" | "EMPLOYER" | "ADMIN"
  is_first_login?: boolean;
}

interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User) => void;
  setFirstLogin: (isFirst: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(persist(..., { name: "auth-store" }));
```

### การใช้งาน
```typescript
// อ่าน user ใน component
const { user, isAuthenticated } = useAuthStore();

// อ่านใน callback / outside component
const user = useAuthStore.getState().user;

// ตั้งค่าหลัง signin สำเร็จ
setUser({ user_id, email, full_name, role, is_first_login: false });

// Logout
useAuthStore.getState().logout();
```

---

## Role-Based Guard Pattern

### Layout-level Guard (`layout-selector.tsx`)
```typescript
// ทำงานบน client-side เท่านั้น (รอ isMounted ก่อน)
// Admin route guard:
if (!user) → redirect "/pages/signin?redirect=<current_path>"
if (user.role !== "ADMIN") → redirect ROLE_HOME[user.role]

// Layouts:
// isAdminRoute || user.role === "ADMIN" → <AdminLayout>
// ทุกกรณีอื่น → <LandingLayout>
```

### Role Home Map
```typescript
const ROLE_HOME: Record<string, string> = {
  EMPLOYEE: "/pages/employee/profile",
  EMPLOYER: "/pages/employer/profile",
  ADMIN: "/pages/admin",
};
```

### Route Guard ใน API (server-side)
```typescript
// ดึง userId จาก query/body → ตรวจ role จาก Prisma
const profile = await prisma.profile.findUnique({ where: { userId } });
if (!profile) return Response.json({ status_code: 401, ... }, { status: 401 });
if (profile.role !== UserRole.EMPLOYER)
  return Response.json({ status_code: 403, ... }, { status: 403 });
```

### Role Check ใน Frontend Component
```typescript
const { user } = useAuthStore();
if (user?.role !== "EMPLOYER") return null; // หรือ redirect
// แสดง content เฉพาะ role
{user?.role === "EMPLOYEE" && <ApplyButton />}
```

---

## Signin Redirect Logic

```
1. มี ?redirect=<url> param → decode แล้ว push ไป
2. ไม่มี → ดู role จาก store:
   EMPLOYEE → /pages/employee/profile
   EMPLOYER → /pages/employer/profile (first_login check)
   ADMIN    → /pages/admin
```

```typescript
// ตัวอย่าง redirect เมื่อยังไม่ login (protected page)
router.push(`/pages/signin?redirect=${encodeURIComponent(pathname)}`);
```

---

## Common Bugs ที่ต้องระวัง

| สถานการณ์ | Bug | วิธีหลีกเลี่ยง |
|-----------|-----|----------------|
| อ่าน `user` ใน callback | `user` เป็น stale closure | ใช้ `useAuthStore.getState().user` |
| Guard ก่อน hydrate | redirect ผิดพลาด | ตรวจ `isMounted` ก่อนทุกครั้ง |
| Prisma fail ตอน signup | ไม่มี Profile ใน DB | signup ยังสำเร็จ แต่ต้อง handle ใน API ที่ต้องการ profile |
| role จาก Supabase metadata ≠ Prisma | ข้อมูลไม่ตรง | อัปเดตทั้งสองที่เมื่อเปลี่ยน role |
| `user_id` vs `id` | Profile.id ≠ Profile.userId | `userId` = Supabase UID, `id` = Prisma UUID |

---

## Environment Variables (Auth-related)

```env
NEXT_PUBLIC_SUPABASE_URL=          # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=     # Public anon key (safe for client)
SUPABASE_SERVICE_ROLE_KEY=         # Service role (ยังไม่ได้ใช้)
```
