---
name: legit-api-token-jwt
description: Obtains a Legit JWT for APEX/Sogo API by building a JWS compatible with Etna AMS JwtFactory and POSTing to the Legit token endpoint. Use when the user needs Legit auth, cc/token, SharedSecret JWS, or debugging 401 from Legit.
---

# Legit API token (JWT)

## When to use

- Нужен **Bearer JWT** для вызовов APEX (Atlas и др.) через Legit.
- Отладка **401** на `.../legit/api/v1/cc/token` (часто неверный формат JWS).

## Критично: формат JWS как в `JwtFactory` (AMS)

Подпись должна совпадать с `Etna.AccountManagement.Apex.ApexServices.Legit.JwtFactory`:

- Заголовок JSON: `{"cty":"JWS","alg":"HS512"}` (не `typ: JWT` из старых Postman-скриптов).
- Тело JSON: `username`, `entity`, `datetime` — где `datetime` в формате ISO **UTC** (`DateTime.UtcNow.ToString("o")` в C#).
- Подпись: **HMAC-SHA512** от ASCII-строки `{headerBase64url}.{bodyBase64url}`, ключ — **SharedSecret** (байты ASCII).
- Кодирование частей: Base64URL (без padding), как `Base64UrlEncoder` в .NET.

Тело запроса к Legit: `{"jws":"<полная_строка_jws>"}`.

## Endpoint

`POST {LegitBase}/legit/api/v1/cc/token`

Пример базы (QA): `https://sogowebapiserver-qa.azurewebsites.net` → полный URL:
`https://sogowebapiserver-qa.azurewebsites.net/legit/api/v1/cc/token`

В AMS `LegitApi` использует `client.BaseAddress = new Uri(config.EndpointUri, "legit/")` и `PostAsync("api/v1/cc/token", ...)`.

## Заголовки

- `Content-Type: application/json`
- `SharedSecret: <значение из конфигурации Apex/Legit, не коммитить>`

## Автоматический запрос токена

Цель: **не собирать JWS руками** каждый раз.

1. **Postman (рекомендуется)**
   - **Pre-request**: скрипт строит JWS (как `JwtFactory`) и кладёт в переменную, например `jws`.
   - **Body**: `{"jws":"{{jws}}"}` — без правок перед Send.
   - **Post-response**: `pm.globals.set("JWT", pm.response.text())` — дальше в коллекции используйте `{{JWT}}` в заголовке `Authorization: Bearer {{JWT}}` — **токен подставляется автоматически** после каждого успешного вызова.

2. **Одна команда Node** (ниже): из env читает секреты, сам строит JWS, делает `POST` и печатает только JWT — пригодно для пайпов и CI.

## Пример curl (если JWS уже в переменной окружения)

```bash
curl -sS -X POST "%LEGIT_BASE%/legit/api/v1/cc/token" ^
  -H "Content-Type: application/json" ^
  -H "SharedSecret: %APEX_SHARED_SECRET%" ^
  --data-raw "{\"jws\":\"%JWS%\"}"
```

Ответ — **сырой текст**, это и есть JWT (кладётся в `Authorization: Bearer ...`).

## Генерация JWS (Node.js, совместимо с JwtFactory)

Требуется Node.js. Секрет и учётные данные — из конфига, не из репозитория:

```javascript
const crypto = require("crypto");
const sharedSecret = process.env.APEX_SHARED_SECRET;
const header = { cty: "JWS", alg: "HS512" };
const body = {
  username: process.env.APEX_LEGIT_USERNAME,
  entity: process.env.APEX_LEGIT_ENTITY,
  datetime: new Date().toISOString(),
};
const h = Buffer.from(JSON.stringify(header)).toString("base64url");
const p = Buffer.from(JSON.stringify(body)).toString("base64url");
const sig = crypto.createHmac("sha512", sharedSecret).update(`${h}.${p}`).digest("base64url");
console.log(`${h}.${p}.${sig}`);
```

## Получить JWT одним скриптом (автоматически)

Node 18+ (`APEX_*` задать в окружении). Оберните в async или сохраните как `.mjs`:

```javascript
const crypto = require("crypto");
(async () => {
  const base = process.env.LEGIT_BASE || "https://sogowebapiserver-qa.azurewebsites.net";
  const secret = process.env.APEX_SHARED_SECRET;
  const header = { cty: "JWS", alg: "HS512" };
  const body = {
    username: process.env.APEX_LEGIT_USERNAME,
    entity: process.env.APEX_LEGIT_ENTITY,
    datetime: new Date().toISOString(),
  };
  const h = Buffer.from(JSON.stringify(header)).toString("base64url");
  const p = Buffer.from(JSON.stringify(body)).toString("base64url");
  const jws = `${h}.${p}.${crypto.createHmac("sha512", secret).update(`${h}.${p}`).digest("base64url")}`;
  const res = await fetch(`${base}/legit/api/v1/cc/token`, {
    method: "POST",
    headers: { "Content-Type": "application/json", SharedSecret: secret },
    body: JSON.stringify({ jws }),
  });
  if (!res.ok) throw new Error(await res.text());
  process.stdout.write(await res.text());
})();
```

Вывод — только JWT; перенаправьте в переменную (`for /f` в cmd, `$env:` в PowerShell) для следующего шага.

## Связь с кодом

- `LegitApi.LoginAsync` — тело `{ jws: JwtFactory.Create(...) }`, ответ сохраняется как токен.
- См. также навык **atlas-status-req** для проверки статуса заявки после получения JWT.
