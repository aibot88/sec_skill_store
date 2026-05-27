---
name: Auth.js (NextAuth v5)
description: Guía oficial de Auth.js v5 para autenticación en aplicaciones modernas con soporte para Prisma Adapter
---

# Auth.js v5 - Guía de Implementación

Auth.js (anteriormente NextAuth.js) es la solución estándar para autenticación en aplicaciones modernas, con un enfoque renovado en el App Router de Next.js.

## 1. Instalación de Dependencias

Para instalar la versión v5 (NextAuth @beta) y el adaptador de Prisma:

```bash
npm install next-auth@beta @auth/prisma-adapter
```

## 2. Configuración Centralizada

Se recomienda dividir la configuración en dos archivos para evitar problemas de dependencias circulares y compatibilidad con el Edge Runtime (Middleware).

### `auth.config.ts` (Configuración compartida)
Este archivo contiene la lógica que es compatible con el Edge Runtime (ej. Providers).

```typescript
import type { NextAuthConfig } from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";

export default {
  providers: [
    GitHub,
    Google,
    // Otros providers compatibles con Edge
  ],
} satisfies NextAuthConfig;
```

### `auth.ts` (Configuración principal)
Aquí se añade el adaptador de base de datos (Prisma).

```typescript
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma"; // IMPORTANTE: Tu instancia de Prisma configurada
import authConfig from "./auth.config";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: "jwt" }, // O "database" si prefieres persistir sesiones
  ...authConfig,
});
```

## 3. Integración con Next.js (API Routes)

Crea el archivo `app/api/auth/[...nextauth]/route.ts`:

```typescript
import { handlers } from "@/auth"; // Referencia a tu archivo auth.ts
export const { GET, POST } = handlers;
```

## 4. Middleware (Protección de Rutas)

Crea el archivo `middleware.ts` en la raíz de tu proyecto para manejar la protección de rutas de forma global.

```typescript
import NextAuth from "next-auth";
import authConfig from "./auth.config";

export const { auth: middleware } = NextAuth(authConfig);

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

## 5. Variables de Entorno `.env`

Auth.js v5 requiere obligatoriamente una clave secreta.

```env
# Clave generada con: npx auth secret
AUTH_SECRET="tu_secreto_super_seguro"

# Credenciales de Providers
AUTH_GITHUB_ID="tu_id"
AUTH_GITHUB_SECRET="tu_secreto"

AUTH_GOOGLE_ID="tu_id"
AUTH_GOOGLE_SECRET="tu_secreto"
```

## 6. Uso en Componentes (Server & Client)

### Server Component (Recomendado)
```typescript
import { auth } from "@/auth";

export default async function Page() {
  const session = await auth();
  
  if (!session) return <div>No autenticado</div>;
  
  return <div>Hola, {session.user?.name}</div>;
}
```

### Client Component
```typescript
"use client";
import { useSession } from "next-auth/react";

export default function ClientSideComponent() {
  const { data: session } = useSession();
  
  return <pre>{JSON.stringify(session, null, 2)}</pre>;
}
```

## 7. Mejores Prácticas
1.  **Diferenciación auth.ts vs auth.config.ts**: Mantén el adaptador de base de datos solo en `auth.ts` para que el middleware (que usa `auth.config.ts`) no falle al intentar cargar drivers de base de datos no compatibles con Edge.
2.  **Seguridad**: Nunca expongas el `AUTH_SECRET` en el cliente.
3.  **Sesiones en DB vs JWT**: Si usas `PrismaAdapter`, por defecto se guardarán sesiones en la DB. Cambia a `strategy: "jwt"` si prefieres sesiones ligeras y stateless.
