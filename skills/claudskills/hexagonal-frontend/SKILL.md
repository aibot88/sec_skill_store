---
name: hexagonal-frontend
description: >
  Guía de arquitectura hexagonal para aplicaciones React + TypeScript. Activa esta skill cuando el usuario pida crear, estructurar o agregar cualquier módulo o feature en el frontend: login, registro, listado de productos, pagos, perfil de usuario, carrito, o cualquier nueva pantalla/funcionalidad. También activa cuando el usuario pregunte cómo organizar carpetas, cómo separar lógica de la UI, cómo preparar código para integrar con una API o microservicio más adelante, o cuando mencione "arquitectura hexagonal", "ports and adapters", "casos de uso", "repositorio", "adaptador" o "mock". Usar aunque el usuario solo diga "quiero hacer el módulo de X" sin mencionar arquitectura — esta skill debe aplicarse siempre en este proyecto.
---

# Arquitectura Hexagonal — Frontend React + TypeScript

## Principio central

La lógica de negocio **no sabe** de dónde vienen los datos ni cómo se muestran.
La UI **no sabe** si los datos vienen de una API real, un mock o localStorage.

```
UI → Hook → UseCase → [Puerto] → Adaptador (Mock hoy / API mañana)
```

---

## Estructura de carpetas por módulo

Cada feature vive en su propio conjunto de capas. La estructura siempre es la misma:

```
src/
├── domain/
│   └── {modulo}/
│       ├── {Entidad}.ts          # Tipos/interfaces de negocio
│       └── {Modulo}Repository.ts # Puerto: contrato que define la app
│
├── application/
│   └── {modulo}/
│       ├── {Accion}UseCase.ts    # Caso de uso puro (lógica de negocio)
│       └── {OtraAccion}UseCase.ts
│
├── infrastructure/
│   └── {modulo}/
│       ├── Mock{Modulo}Repository.ts  # Adaptador actual (sin API)
│       └── Api{Modulo}Repository.ts   # Adaptador futuro (microservicio)
│
└── ui/
    └── {modulo}/
        ├── hooks/
        │   └── use{Accion}.ts    # Conecta UI ↔ caso de uso
        └── components/
            ├── {Modulo}Page.tsx
            └── {Modulo}Form.tsx  # o List, Card, etc.
```

**Regla de dependencias:**
- `domain` no importa nada de las otras capas
- `application` solo importa de `domain`
- `infrastructure` implementa los puertos de `domain`
- `ui` solo importa de `application` y `domain` (nunca de `infrastructure` directamente, excepto para inyectar el adaptador en el hook)

---

## Proceso para crear cualquier módulo

Seguir siempre en este orden:

### 1. Domain — definir entidad y puerto

```typescript
// domain/{modulo}/{Entidad}.ts
export interface {Entidad} {
  id: string
  // ...campos de negocio
}

export interface {EntidadInput} {
  // campos que entran (formulario, params, etc.)
}
```

```typescript
// domain/{modulo}/{Modulo}Repository.ts
import { {Entidad}, {EntidadInput} } from './{Entidad}'

export interface {Modulo}Repository {
  // métodos que la app necesita — verbos de negocio, no técnicos
  // Ejemplos: login(), getAll(), getById(), create(), update(), remove()
}
```

### 2. Application — caso de uso

```typescript
// application/{modulo}/{Accion}UseCase.ts
import { {Modulo}Repository } from '../../domain/{modulo}/{Modulo}Repository'

export class {Accion}UseCase {
  constructor(private readonly repo: {Modulo}Repository) {}

  async execute(input: {EntidadInput}): Promise<{Entidad}> {
    // 1. Validaciones de dominio (lanzar Error si falla)
    // 2. Llamar al repo
    // 3. Retornar resultado
    return this.repo.{metodo}(input)
  }
}
```

### 3. Infrastructure — adaptador mock

```typescript
// infrastructure/{modulo}/Mock{Modulo}Repository.ts
import { {Modulo}Repository } from '../../domain/{modulo}/{Modulo}Repository'

export class Mock{Modulo}Repository implements {Modulo}Repository {
  // Datos en memoria o localStorage
  // Simular delay: await new Promise(r => setTimeout(r, 600))
  // Simular errores para probar el manejo de estados
}
```

### 4. UI — hook

```typescript
// ui/{modulo}/hooks/use{Accion}.ts
import { useState } from 'react'
import { {Accion}UseCase } from '../../../application/{modulo}/{Accion}UseCase'
import { Mock{Modulo}Repository } from '../../../infrastructure/{modulo}/Mock{Modulo}Repository'

// ÚNICO lugar donde se inyecta el adaptador
// Cuando llegue la API: cambiar Mock por Api — nada más cambia
const repo = new Mock{Modulo}Repository()
const useCase = new {Accion}UseCase(repo)

export function use{Accion}() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<{Entidad} | null>(null)

  const execute = async (input: {EntidadInput}) => {
    setLoading(true)
    setError(null)
    try {
      const result = await useCase.execute(input)
      setData(result)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Error inesperado')
    } finally {
      setLoading(false)
    }
  }

  return { execute, loading, error, data }
}
```

### 5. UI — componente

```tsx
// ui/{modulo}/components/{Modulo}Form.tsx (o Page, List, Card)
import { use{Accion} } from '../hooks/use{Accion}'

export function {Modulo}Form() {
  const { execute, loading, error, data } = use{Accion}()
  // Solo maneja estado visual, nunca lógica de negocio
}
```

---

## Cómo migrar de Mock a API real

Cuando estén listos los microservicios, el proceso es:

1. Crear `Api{Modulo}Repository.ts` en `infrastructure/{modulo}/`
2. Implementar la misma interface del puerto con `fetch` real
3. En el hook, cambiar **una sola línea**:
   ```typescript
   // Antes:
   const repo = new Mock{Modulo}Repository()
   // Después:
   const repo = new Api{Modulo}Repository()
   ```
4. **No tocar nada más** — UseCase, componentes y hooks quedan igual

---

## Módulos de referencia

Ver ejemplos completos y listos para copiar en `references/`:

| Módulo | Archivo | Cuándo leer |
|---|---|---|
| Auth (login/registro) | `references/auth.md` | Módulos de autenticación |
| Listados (productos, beats) | `references/list.md` | Listar, filtrar, paginar items |
| Formularios (crear/editar) | `references/form.md` | Crear o editar cualquier entidad |
| Pagos | `references/payments.md` | Checkout, órdenes, transacciones |

---

## Errores comunes — nunca hacer esto

```typescript
// ❌ MAL: lógica de negocio en el componente
function LoginForm() {
  const handleSubmit = async () => {
    const res = await fetch('/api/login', { body: JSON.stringify({email, password}) })
    // ...
  }
}

// ❌ MAL: el useCase llama fetch directamente
class LoginUseCase {
  async execute() {
    const res = await fetch('/api/login') // rompe la separación
  }
}

// ❌ MAL: el componente importa el repositorio
import { MockAuthRepository } from '../../../infrastructure/auth/MockAuthRepository'
// Los componentes nunca deben conocer la infraestructura

// ✅ BIEN: componente → hook → useCase → [puerto] → adaptador
```