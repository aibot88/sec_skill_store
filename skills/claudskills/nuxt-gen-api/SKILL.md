---
name: nuxt-gen-api
description: Gera uma rota de API Nitro para projetos Nuxt com o handler correto — autenticado (defineAuthenticatedEventHandler), seguro (defineSecuredEventHandler) ou público — seguindo as convenções de nomenclatura e estrutura do projeto.
---

# nuxt-gen-api — Gerar API Route Nitro

Você está gerando uma rota de API Nitro. Siga as convenções do projeto rigorosamente.

## 1. Coletar informações

Extraia dos argumentos ou pergunte ao usuário:

1. **Recurso** — nome do recurso em inglês, singular (ex: `product`, `order`, `category`)
2. **Método HTTP** — GET, POST, PUT, DELETE (ou múltiplos para scaffold CRUD completo)
3. **Tem parâmetro de rota?** — ex: `/api/admin/products/[id]`
4. **Tipo de proteção:**
   - `authenticated` — requer Firebase Auth + verifica claims (padrão para rotas protegidas)
   - `secured` — requer apenas App Check (sem auth de usuário)
   - `public` — sem proteção
5. **Claim necessário** — `sudo`, ou nenhum (só para `authenticated`)
6. **Onde criar** — ex: `server/api/admin/`, `server/api/me/`, `server/api/`
7. **O que faz** — descrição breve da lógica (ex: "lista produtos ativos ordenados por nome")

## 2. Regras de nomenclatura

```
server/api/admin/products.get.ts           # GET  /api/admin/products
server/api/admin/products.post.ts          # POST /api/admin/products
server/api/admin/products/[id].get.ts      # GET  /api/admin/products/:id
server/api/admin/products/[id].put.ts      # PUT  /api/admin/products/:id
server/api/admin/products/[id].delete.ts   # DELETE /api/admin/products/:id
```

- Recurso sempre em **inglês**
- Kebab-case para recursos compostos (`blog-posts`, `order-items`)
- Nunca use português na URL

## 3. Templates por tipo de proteção

### Handler autenticado com claim sudo (padrão para rotas protegidas)

```typescript
// GET /api/admin/[recurso]
export default defineAuthenticatedEventHandler(async (event, context) => {
  if (!context.claims.sudo) {
    throw createError({ status: 403, message: 'Acesso negado' })
  }

  const { data, error } = await db()
    .from('[tabela]')
    .select('*')
    .order('[campo]')

  if (error) {
    throw createError({ status: 500, message: error.message })
  }

  return { data }
})
```

### Handler autenticado sem claim específico (apenas login)

```typescript
export default defineAuthenticatedEventHandler(async (event, context) => {
  const userId = context.claims.uid
  // lógica
})
```

### Handler seguro (App Check apenas, sem auth de usuário)

```typescript
export default defineSecuredEventHandler(async (event) => {
  // lógica sem contexto de usuário
})
```

### Handler público

```typescript
export default defineEventHandler(async (event) => {
  // lógica pública
})
```

## 4. Templates por método HTTP

### GET — listar recursos

```typescript
export default defineAuthenticatedEventHandler(async (event, context) => {
  if (!context.claims.sudo) {
    throw createError({ status: 403, message: 'Acesso negado' })
  }

  const query = getQuery(event)
  const page = Number(query.page) || 1
  const limit = Number(query.limit) || 20

  const { data, error, count } = await db()
    .from('[tabela]')
    .select('*', { count: 'exact' })
    .range((page - 1) * limit, page * limit - 1)
    .order('created_at', { ascending: false })

  if (error) {
    throw createError({ status: 500, message: error.message })
  }

  return { data, total: count, page, limit }
})
```

### GET — buscar por ID

```typescript
export default defineAuthenticatedEventHandler(async (event, context) => {
  if (!context.claims.sudo) {
    throw createError({ status: 403, message: 'Acesso negado' })
  }

  const { id } = getRouterParams(event)

  const { data, error } = await db()
    .from('[tabela]')
    .select('*')
    .eq('id', id)
    .single()

  if (error || !data) {
    throw createError({ status: 404, message: '[Recurso] não encontrado' })
  }

  return { data }
})
```

### POST — criar recurso

```typescript
import { z } from 'zod'  // se o projeto usar zod

export default defineAuthenticatedEventHandler(async (event, context) => {
  if (!context.claims.sudo) {
    throw createError({ status: 403, message: 'Acesso negado' })
  }

  const body = await readBody(event)

  // Validação básica
  if (!body.[campo_obrigatorio]) {
    throw createError({ status: 400, message: '[campo] é obrigatório' })
  }

  const { data, error } = await db()
    .from('[tabela]')
    .insert({
      // campos aqui
    })
    .select()
    .single()

  if (error) {
    throw createError({ status: 500, message: error.message })
  }

  return { data }
})
```

### PUT — atualizar recurso

```typescript
export default defineAuthenticatedEventHandler(async (event, context) => {
  if (!context.claims.sudo) {
    throw createError({ status: 403, message: 'Acesso negado' })
  }

  const { id } = getRouterParams(event)
  const body = await readBody(event)

  const { data, error } = await db()
    .from('[tabela]')
    .update({
      // campos atualizáveis aqui
      updated_at: new Date().toISOString(),
    })
    .eq('id', id)
    .select()
    .single()

  if (error) {
    throw createError({ status: 500, message: error.message })
  }

  if (!data) {
    throw createError({ status: 404, message: '[Recurso] não encontrado' })
  }

  return { data }
})
```

### DELETE — remover recurso

```typescript
export default defineAuthenticatedEventHandler(async (event, context) => {
  if (!context.claims.sudo) {
    throw createError({ status: 403, message: 'Acesso negado' })
  }

  const { id } = getRouterParams(event)

  const { error } = await db()
    .from('[tabela]')
    .delete()
    .eq('id', id)

  if (error) {
    throw createError({ status: 500, message: error.message })
  }

  return { success: true }
})
```

## 5. Scaffold CRUD completo

Se o usuário pedir CRUD completo, gere todos os 5 arquivos de uma vez:

```
server/api/admin/[recurso].get.ts
server/api/admin/[recurso].post.ts
server/api/admin/[recurso]/[id].get.ts
server/api/admin/[recurso]/[id].put.ts
server/api/admin/[recurso]/[id].delete.ts
```

## 6. Verificações antes de criar

- O recurso está em inglês? Se não, converta.
- O diretório existe? Se não, crie-o.
- Já existe um arquivo com esse nome? Se sim, avise o usuário antes de sobrescrever.

## 7. Após criar

Informe:
- Caminho completo do(s) arquivo(s) criado(s)
- URL(s) que serão expostas
- Tipo de proteção aplicada
- Se precisa registrar a rota no `routeRules` do `nuxt.config.ts`
