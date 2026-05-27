---
name: nextjs-fullstack-setup
description: Next.js App Router + Bun + Drizzle ORM + Better Auth + Tailwind CSS + Biome ile full-stack proje kurulumu, authentication entegrasyonu ve DB workflow'ları.
license: Apache-2.0
---

# nextjs-fullstack-setup

## Amaç

Sıfırdan bir Next.js (App Router) projesi oluşturur. Bun runtime/package manager, Drizzle ORM, Better Auth, Tailwind CSS ve Biome formatter/linter ile tam entegre, production-ready bir full-stack uygulama iskeleti sağlar. Veritabanı yönetimi (migration, seed, reset) için standart workflow'lar ve script'ler içerir.

## Ne Zaman Kullanılır

- Yeni bir full-stack Next.js projesi başlatılacaksa.
- Bun + Drizzle + Better Auth + Tailwind + Biome standart stack'i isteniyorsa.
- Authentication dahil tutarlı bir proje yapısına ihtiyaç varsa.
- DB migration, seed ve reset workflow'ları standartlaştırılacaksa.

## Ön Koşullar

- Bun >= 1.0 kurulu
- Docker ve Docker Compose kurulu
- Node.js >= 18 (Next.js uyumluluk)

## Sağlanan Template Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `templates/docker-compose.yml` | PostgreSQL 16 container (healthcheck, named volume) |
| `templates/.env.example` | Ortam değişkenleri (secret'sız) |
| `templates/biome.json` | Biome formatter + linter config |
| `templates/tsconfig.json` | TypeScript strict config |
| `templates/drizzle/schema.ts` | Drizzle schema (Post + Auth tabloları) |
| `templates/drizzle/seed.ts` | Örnek seed dosyası |
| `templates/drizzle.config.ts` | drizzle-kit config |
| `scripts/init.sh` | Proje bootstrap |
| `scripts/db-migrate.sh` | Dev/prod migration |
| `scripts/db-reset.sh` | Dev-only DB reset |
| `scripts/db-seed.sh` | Seed çalıştırır |

## Adımlar

### 1. Next.js projesi oluştur

```bash
bun create next-app@latest my-app --typescript --tailwind --eslint=false --app --src-dir --import-alias "@/*"
cd my-app
```

> ESLint devre dışı çünkü Biome kullanılacak.

### 2. ESLint'i kaldır, Biome'u kur

```bash
bun remove eslint eslint-config-next
bun add -d @biomejs/biome
```

`templates/biome.json` dosyasını proje kök dizinine kopyala:

```bash
cp ../templates/biome.json ./biome.json
```

`package.json`'a script'leri ekle:

```json
{
  "scripts": {
    "check": "biome check .",
    "check:fix": "biome check --write .",
    "format": "biome format --write ."
  }
}
```

### 3. Drizzle ORM kur

```bash
bun add drizzle-orm postgres
bun add -d drizzle-kit @paralleldrive/cuid2
```

### 4. Template dosyaları kopyala

```bash
mkdir -p drizzle
cp ../templates/drizzle/schema.ts ./drizzle/schema.ts
cp ../templates/drizzle/seed.ts ./drizzle/seed.ts
cp ../templates/drizzle.config.ts ./drizzle.config.ts
cp ../templates/docker-compose.yml ./docker-compose.yml
cp ../templates/.env.example ./.env.example
cp ../templates/tsconfig.json ./tsconfig.json
cp .env.example .env
```

`.env` dosyasındaki değerleri düzenle.

### 5. Docker Compose ile PostgreSQL başlat

```bash
docker compose up -d
```

Healthcheck ile hazır olmasını bekle:

```bash
until docker compose exec -T postgres pg_isready -U postgres; do sleep 1; done
```

### 6. İlk schema push

```bash
bunx drizzle-kit push
```

### 7. DB client singleton oluştur — `src/lib/db.ts`

```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "@/../drizzle/schema";

const globalForDb = globalThis as unknown as {
  client: ReturnType<typeof postgres> | undefined;
};

const client = globalForDb.client ?? postgres(process.env.DATABASE_URL!);

if (process.env.NODE_ENV !== "production") {
  globalForDb.client = client;
}

export const db = drizzle(client, { schema });
```

### 8. Better Auth kur

```bash
bun add better-auth
```

### 9. Auth config oluştur — `src/lib/auth.ts`

```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "./db";

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg" }),
  emailAndPassword: {
    enabled: true,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 gün
    updateAge: 60 * 60 * 24,      // 1 günde bir yenile
  },
});
```

**Auth stratejisi**: Session-based auth tercih ediliyor:

1. **Revoke kolaylığı** — JWT'de token süresi dolana kadar iptal zor, session anında silinebilir.
2. **Better Auth varsayılanı** — Kütüphanenin birincil ve en iyi test edilmiş yolu.
3. **Server component uyumu** — Next.js App Router'da server component'lerden session'a erişmek doğal.

### 10. Auth client oluştur — `src/lib/auth-client.ts`

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient;
```

### 11. API route handler — `src/app/api/auth/[...all]/route.ts`

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### 12. Auth tabloları

Auth tabloları (users, sessions, accounts, verifications) `drizzle/schema.ts` içinde zaten tanımlı. Migration oluştur:

```bash
bunx drizzle-kit generate --name add-auth-tables
bunx drizzle-kit migrate
```

### 13. Middleware — `src/middleware.ts`

```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

const protectedRoutes = ["/dashboard"];
const authRoutes = ["/sign-in", "/sign-up"];

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  const { pathname } = request.nextUrl;

  // Korumalı route — session yoksa sign-in'e yönlendir
  if (protectedRoutes.some((route) => pathname.startsWith(route))) {
    if (!session) {
      return NextResponse.redirect(new URL("/sign-in", request.url));
    }
  }

  // Auth route — session varsa dashboard'a yönlendir
  if (authRoutes.some((route) => pathname.startsWith(route))) {
    if (session) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/sign-in", "/sign-up"],
};
```

### 14. Ortam değişkenleri

`.env` dosyasına ekle:

```env
BETTER_AUTH_SECRET=generate_a_random_secret_here
BETTER_AUTH_URL=http://localhost:3000
```

Secret üretmek için:

```bash
openssl rand -base64 32
```

### 15. Proje yapısını standartlaştır

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── api/
│       └── auth/
│           └── [...all]/
│               └── route.ts
├── components/
├── lib/
│   ├── db.ts              # Drizzle client singleton
│   ├── auth.ts            # Better Auth config
│   └── auth-client.ts     # Client-side auth
├── middleware.ts
├── types/
└── styles/
drizzle/
├── schema.ts              # Tablo tanımları
├── seed.ts                # Seed dosyası
└── migrations/            # drizzle-kit tarafından oluşturulur
drizzle.config.ts
```

### 16. Doğrulama

```bash
bun dev                                        # Proje çalışıyor mu?
bun run check                                  # Biome hatasız mı?
curl -s http://localhost:3000/api/auth/ok       # Auth endpoint yanıt veriyor mu?
```

## DB Workflow'ları

### Dev vs Prod Politikası

| İşlem | Dev | Prod |
|-------|-----|------|
| `drizzle-kit generate` | Yeni migration oluşturur | Kullanılmaz |
| `drizzle-kit migrate` | Migration uygular | Tek yol |
| `drizzle-kit push` | Hızlı prototyping | Kullanılmaz |
| `db reset` | Serbest | **Engellendi** |
| `db seed` | Serbest | Manuel karar |

### Script Kullanımı

```bash
# Bootstrap (sıfırdan kurulum)
bash scripts/init.sh

# Dev migration (schema değişikliği sonrası)
bash scripts/db-migrate.sh --name add-users

# Prod migration (sadece mevcut migration'ları uygula)
NODE_ENV=production bash scripts/db-migrate.sh

# DB reset (dev-only, tüm veriyi siler)
bash scripts/db-reset.sh

# Seed çalıştır
bash scripts/db-seed.sh
```

## DoD (Definition of Done)

- [ ] `bun dev` ile proje ayağa kalkıyor.
- [ ] Drizzle schema push/migration hatasız çalışıyor.
- [ ] Tailwind sınıfları çalışıyor.
- [ ] `bun run check` (Biome) hatasız geçiyor.
- [ ] PostgreSQL container çalışıyor ve bağlantı başarılı.
- [ ] Proje yapısı standartlaştırılmış (`src/lib`, `src/components`, vb.).
- [ ] Email/password ile kayıt ve giriş çalışıyor.
- [ ] Session oluşturuluyor ve doğrulanıyor.
- [ ] Korumalı route'lara yetkisiz erişim engellenmiş.
- [ ] `BETTER_AUTH_SECRET` `.env.example`'da placeholder olarak mevcut.
- [ ] `docker compose up -d` ile PostgreSQL ayağa kalkıyor.
- [ ] Seed script veritabanını dolduruyor.
- [ ] Dev/prod ortam ayrımı `.env` ile sağlanmış.
