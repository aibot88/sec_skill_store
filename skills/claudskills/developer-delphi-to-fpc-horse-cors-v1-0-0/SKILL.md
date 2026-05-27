---
name: developer-delphi-to-fpc-horse-cors
description: Middleware CORS para Horse. Cobre HorseCORS/CORS, HorseCORSConfig (AllowedOrigin, AllowedMethods, AllowedHeaders, AllowedCredentials, ExposedHeaders), preflight OPTIONS (204) e ordem de registro. Fonte: app/package/docs/pacotes/horse-cors.md.
model: sonnet
thinking: minimal
category: project
license: MIT
copyright: "Copyright (c) 2026 CSL Tech Solutions"
company: "CSL Tech Solutions"
author: "Claiton de Souza Linhares"
---

# developer-delphi-to-fpc-horse-cors

## Versão interna (ficheiro)

| Campo | Valor |
| --- | --- |
| **FileVersion** | 1.0.0 |
| **Política** | `.cursor/VERSION.md` |

## Responsabilidade única

Middleware CORS para Horse: define cabeçalhos `Access-Control-*` e responde a pedidos OPTIONS (preflight) com 204 No Content.

## When to use

- Permitir requests de browsers em domínios diferentes
- Configurar origens, métodos e cabeçalhos permitidos
- Responder a preflight OPTIONS sem bloquear JWT/Auth

## When NOT to use

- Autenticação → `developer-delphi-to-fpc-horse-jwt` ou `developer-delphi-to-fpc-horse-basic-auth`
- Core do servidor → `developer-delphi-to-fpc-horse-core`

## Documento canônico

`app/package/docs/pacotes/horse-cors.md`

---

## HorseCORSConfig — métodos de configuração

| Método | Descrição |
| --- | --- |
| `HorseCORS()` | Acede/cria configuração global |
| `AllowedOrigin(origin)` | Origem(ns) permitida(s) |
| `AllowedCredentials(bool)` | Permitir cookies/credenciais |
| `AllowedHeaders(headers)` | Cabeçalhos aceites (CSV) |
| `AllowedMethods(methods)` | Verbos aceites (CSV) |
| `ExposedHeaders(headers)` | Cabeçalhos expostos ao JS |

---

## Ordem no pipeline

**CORS deve ser o PRIMEIRO middleware** antes de JWT/Auth (garantir que OPTIONS não é bloqueado):

```delphi
THorse
  .Use(CORS)          // 1.º — preflight desbloqueado
  .Use(HorseJWT(...)) // 2.º
  .Use(Jhonson);      // 3.º
```

---

## Exemplos

### CORS mínimo (sem configuração)

```delphi
uses Horse, Horse.CORS;

begin
  THorse.Use(CORS);
  THorse.Get('/ping',
    procedure(Req: THorseRequest; Res: THorseResponse; Next: TProc)
    begin
      Res.Send('pong');
    end);
  THorse.Listen(9000);
end.
```

### Configuração completa (produção)

```delphi
uses Horse, Horse.CORS;

begin
  HorseCORS
    .AllowedOrigin('https://app.gestorerp.pt')
    .AllowedCredentials('true')
    .AllowedHeaders('Content-Type, Authorization, X-Requested-With')
    .AllowedMethods('GET, POST, PUT, DELETE, PATCH, OPTIONS')
    .ExposedHeaders('X-Total-Count, X-Paginate');

  THorse.Use(CORS);
  THorse.Listen(9000);
end.
```

### Desenvolvimento (wildcard)

```delphi
HorseCORS
  .AllowedOrigin('*')
  .AllowedMethods('*')
  .AllowedHeaders('*');

THorse.Use(CORS);
```

### Exemplos de configuração individual

```delphi
// Origem específica
HorseCORS.AllowedOrigin('https://app.gestorerp.pt');

// Múltiplas origens não suportadas diretamente — usar '*' ou proxy
HorseCORS.AllowedOrigin('*'); // apenas dev

// Credentials (AllowedOrigin NÃO pode ser '*' com credentials = true)
HorseCORS.AllowedCredentials(True);
// → Access-Control-Allow-Credentials: true

// Cabeçalhos
HorseCORS.AllowedHeaders('Content-Type, Authorization, X-Requested-With, X-API-Key');

// Métodos
HorseCORS.AllowedMethods('GET, POST, PUT, DELETE, PATCH, OPTIONS');

// Expor cabeçalhos para o JS
HorseCORS.ExposedHeaders('X-Total-Count, X-Paginate, X-Request-Id');
```

### Lazarus / FPC

```delphi
{$MODE DELPHI}{$H+}
uses Horse, Horse.CORS, SysUtils;

begin
  THorse.Use(CORS);
  THorse.Get('/ping', GetPing);
  THorse.Listen(9000);
end.
```

---

## Fluxo CORS

```
OPTIONS /api/users
  → Middleware CORS define Access-Control-* headers
  → Responde 204 No Content (EHorseCallbackInterrupted)
  → Handler da rota NÃO é chamado

GET /api/users + Origin: https://app.gestorerp.pt
  → Middleware CORS define headers
  → Chama Next() → handler executa normalmente
```

---

## Notas GestorERP

- Em produção: `AllowedOrigin` restrito ao domínio do frontend Vue.js
- Em dev/staging: `'*'` ou lista explícita
- Registar CORS **antes** de JWT/Basic Auth — garantir que preflight OPTIONS não é bloqueado
- `unit` a usar: `Horse.CORS`

---

## Changelog (este arquivo)

- 1.0.0 (12/04/2026): Criação — skill middleware CORS.
