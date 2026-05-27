---
name: security-baseline-dev
description: Базовая безопасность в реализации — валидация входных данных (Zod), secrets management, безопасные ошибки, auth/authz patterns, XSS/injection prevention, dependency audit, secure headers. DO/DON'T примеры. Активируй при написании любого кода, работающего с пользовательским вводом, auth, секретами, или при вопросах «как сделать безопасно».
---

# Skill: Security Baseline (Dev)

Конкретные DO/DON'T паттерны безопасности для каждодневной разработки.

**Разделы:**
1. [Input Validation](#1-input-validation)
2. [Secrets Management](#2-secrets-management)
3. [Безопасные ошибки](#3-безопасные-ошибки)
4. [Auth/AuthZ](#4-authauthz)
5. [XSS Prevention](#5-xss-prevention)
6. [Injection Prevention](#6-injection-prevention)
7. [Secure Headers](#7-secure-headers)
8. [Dependency Security](#8-dependency-security)
9. [Logging Security](#9-logging-security)
10. [Anti-patterns](#10-anti-patterns)

---

## 1. Input Validation

### ✅ DO: валидация на границе (API / form) через Zod

```js
import { z } from 'zod';

// ✅ Whitelist schema — разрешаем только известные поля
const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(1).max(100).trim(),
    email: z.string().email().toLowerCase(),
    age: z.number().int().min(13).max(150).optional(),
    role: z.enum(['user', 'admin']).default('user'),
  }),
});

// ✅ Парсим и получаем типизированные данные
const result = createUserSchema.safeParse({ body: req.body });
if (!result.success) {
  return res.status(400).json({ errors: result.error.flatten().fieldErrors });
}
const { name, email, age, role } = result.data.body; // ← safe
```

### ❌ DON'T: доверять входным данным

```js
// ❌ Нет валидации — любые данные попадают в DB
app.post('/api/users', (req, res) => {
  db.users.insert(req.body); // ❌ req.body может содержать isAdmin: true
});

// ❌ Ручная валидация — неполная, ошибкоёмкая
if (req.body.email && typeof req.body.email === 'string') {
  // ❌ не проверяет формат email, не trim, не lowercase
}

// ✅ Zod + validate middleware (см. $node-express-beast-practices)
app.post('/api/users', validate(createUserSchema), controller.create);
```

### ✅ DO: sanitize для HTML (если принимаете rich text)

```js
import DOMPurify from 'isomorphic-dompurify';

/**
 * Очищает HTML от XSS-векторов.
 * @param {string} dirty - пользовательский HTML.
 * @returns {string} безопасный HTML.
 */
function sanitizeHtml(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'target'],
  });
}
```

---

## 2. Secrets Management

### ✅ DO: env variables + validation

```js
// config/env.js
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  API_KEY: z.string().min(16),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

const result = envSchema.safeParse(process.env);
if (!result.success) {
  console.error('❌ Missing/invalid env vars:', result.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = Object.freeze(result.data);
```

### ✅ DO: .gitignore для секретов

```gitignore
# Secrets — NEVER commit
.env
.env.local
.env.production
*.pem
*.key
credentials.json
service-account.json
```

### ❌ DON'T: секреты в коде

```js
// ❌ Хардкод секретов
const API_KEY = 'sk-1234567890abcdef';  // ❌ НИКОГДА
const dbUrl = 'mongodb://user:password@host:27017/db';  // ❌

// ✅ Из env
const API_KEY = config.API_KEY;
const dbUrl = config.DATABASE_URL;

// ❌ Секреты в логах / ошибках
logger.info({ apiKey: config.API_KEY }); // ❌ утечка
throw new Error(`Auth failed for key: ${apiKey}`); // ❌ утечка
```

---

## 3. Безопасные ошибки

### ✅ DO: разделять operational и programmer errors

```js
// ✅ Для клиента — безопасное сообщение
// Для логов — полная информация

export function errorHandler(logger) {
  return (err, req, res, _next) => {
    // Operational — показываем клиенту
    if (err.isOperational) {
      return res.status(err.statusCode).json({
        error: err.message,
        // ✅ Без stack trace, без SQL, без внутренних деталей
      });
    }

    // Programmer error — скрываем от клиента
    logger.error({
      err,          // ← полный stack trace в логи
      requestId: req.id,
      method: req.method,
      url: req.originalUrl,
    });

    res.status(500).json({
      error: 'Internal server error',
      // ❌ NEVER: error: err.message, stack: err.stack
    });
  };
}
```

### ❌ DON'T: утекать внутренности

```js
// ❌ SQL ошибка видна пользователю
res.status(500).json({
  error: 'duplicate key value violates unique constraint "users_email_key"'
});

// ❌ Stack trace видна
res.status(500).json({
  error: err.message,
  stack: err.stack,  // ❌ НИКОГДА
});

// ❌ Разная реакция на "user not found" vs "wrong password"
// → выдаёт информацию об аккаунтах (user enumeration)
if (!user) return res.status(404).json({ error: 'User not found' });
if (!passwordMatch) return res.status(401).json({ error: 'Wrong password' });

// ✅ Одинаковое сообщение
return res.status(401).json({ error: 'Invalid credentials' });
```

---

## 4. Auth/AuthZ

### ✅ DO: JWT в httpOnly cookie (не localStorage)

```js
// ✅ Установка JWT в httpOnly cookie
res.cookie('token', jwt, {
  httpOnly: true,   // ✅ недоступна из JS (XSS protection)
  secure: true,     // ✅ только HTTPS
  sameSite: 'lax',  // ✅ CSRF protection
  maxAge: 7 * 24 * 60 * 60 * 1000,  // 7 days
  path: '/',
});

// ❌ JWT в localStorage — уязвим к XSS
localStorage.setItem('token', jwt); // ❌ любой JS может прочитать
```

### ✅ DO: authZ проверки ДО операций

```js
// ✅ Проверяем права ПЕРЕД выполнением операции
async function deleteCoupon(req, res) {
  const coupon = await couponService.getById(req.params.id);

  // AuthZ: только владелец или admin
  if (coupon.ownerId !== req.user.id && req.user.role !== 'admin') {
    throw new ForbiddenError('You can only delete your own coupons');
  }

  await couponService.remove(coupon.id);
  res.status(204).end();
}

// ❌ IDOR — нет проверки владельца
async function deleteCoupon(req, res) {
  await couponService.remove(req.params.id); // любой может удалить любой купон
}
```

### ✅ DO: password hashing

```js
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

/**
 * Хеширует пароль через bcrypt.
 * @param {string} password - plain text пароль.
 * @returns {Promise<string>} хеш.
 */
async function hashPassword(password) {
  return bcrypt.hash(password, SALT_ROUNDS);
}

/**
 * Сравнивает пароль с хешем.
 * @param {string} password - plain text.
 * @param {string} hash - bcrypt хеш.
 * @returns {Promise<boolean>}
 */
async function verifyPassword(password, hash) {
  return bcrypt.compare(password, hash);
}

// ❌ НИКОГДА: MD5, SHA-1, plain text
```

---

## 5. XSS Prevention

### ✅ DO: React автоматически escapes JSX

```jsx
// ✅ React escapes по умолчанию — безопасно
return <p>{userInput}</p>; // <script>alert('xss')</script> → text

// ❌ dangerouslySetInnerHTML — XSS если input не sanitized
return <div dangerouslySetInnerHTML={{ __html: userInput }} />; // ❌

// ✅ Если НЕОБХОДИМО вставить HTML — sanitize через DOMPurify
import DOMPurify from 'dompurify';
return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />;
```

### ✅ DO: CSP header

```js
// Helmet автоматически ставит CSP
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],         // без 'unsafe-inline'!
      styleSrc: ["'self'", "'unsafe-inline'"],  // CSS может потребовать inline
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.example.com"],
    },
  },
}));
```

---

## 6. Injection Prevention

### ✅ DO: параметризованные запросы

```js
// ✅ SQL — параметризация (никогда конкатенация)
const user = await db.query('SELECT * FROM users WHERE email = $1', [email]);

// ❌ SQL injection
const user = await db.query(`SELECT * FROM users WHERE email = '${email}'`);
// email = "'; DROP TABLE users; --"

// ✅ MongoDB — не допускать операторы в пользовательском вводе
const user = await db.users.findOne({ email: String(email) }); // ✅ явное приведение

// ❌ NoSQL injection
const user = await db.users.findOne({ email: req.body.email });
// req.body.email = { $ne: "" } → возвращает первого пользователя

// ✅ Command injection prevention — никогда не exec(userInput)
import { execFile } from 'node:child_process';
execFile('convert', [inputPath, outputPath], callback); // ✅ args как массив

// ❌ Command injection
exec(`convert ${userInput} output.png`); // ❌ userInput = "; rm -rf /"
```

---

## 7. Secure Headers

### ✅ DO: helmet.js (минимальная настройка)

```js
import helmet from 'helmet';

// ✅ Helmet устанавливает все необходимые security headers:
// - Content-Security-Policy
// - X-Content-Type-Options: nosniff
// - X-Frame-Options: SAMEORIGIN
// - Strict-Transport-Security (HSTS)
// - X-XSS-Protection (deprecated, но не мешает)
// - Referrer-Policy
app.use(helmet());
```

### ✅ DO: CORS — whitelist origins

```js
import cors from 'cors';

// ✅ Whitelist конкретных origin
app.use(cors({
  origin: ['https://myapp.com', 'https://admin.myapp.com'],
  methods: ['GET', 'POST', 'PATCH', 'DELETE'],
  credentials: true,  // для httpOnly cookies
}));

// ❌ Открытый CORS в production
app.use(cors({ origin: '*' })); // ❌ любой сайт может делать запросы
```

---

## 8. Dependency Security

### ✅ DO: регулярный audit

```bash
# npm
npm audit                  # проверить уязвимости
npm audit fix              # автофикс
npm audit --production     # только production deps

# package.json — lock versions
npm install --save-exact   # точные версии, не ^
```

### ✅ DO: минимизировать зависимости

```js
// ❌ Устанавливать lodash ради одной функции
import _ from 'lodash';
const unique = _.uniq(arr);

// ✅ Нативный JS
const unique = [...new Set(arr)];

// ❌ moment.js (300KB) для форматирования даты
import moment from 'moment';

// ✅ Intl.DateTimeFormat (встроенный, 0KB)
new Intl.DateTimeFormat('ru', { dateStyle: 'short' }).format(date);
```

### ✅ DO: lockfile в репозитории

```gitignore
# ✅ Lockfile ДОЛЖЕН быть в git (reproducible builds)
# НЕ добавляй в .gitignore:
# package-lock.json   ← НУЖЕН в git
# bun.lockb           ← НУЖЕН в git
```

---

## 9. Logging Security

### ✅ DO: sanitize логи от PII и секретов

```js
/**
 * Фильтрует чувствительные поля из объекта для логирования.
 * @param {object} obj - объект для логирования.
 * @returns {object} очищенный объект.
 */
function sanitizeForLog(obj) {
  const SENSITIVE_KEYS = ['password', 'token', 'secret', 'apiKey', 'authorization',
    'cookie', 'ssn', 'creditCard', 'cardNumber', 'cvv'];

  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => {
      if (SENSITIVE_KEYS.some((s) => key.toLowerCase().includes(s))) {
        return [key, '[REDACTED]'];
      }
      if (typeof value === 'object' && value !== null) {
        return [key, sanitizeForLog(value)];
      }
      return [key, value];
    })
  );
}

// Использование:
logger.info(sanitizeForLog({ email: 'user@example.com', password: '123', token: 'abc' }));
// { email: 'user@example.com', password: '[REDACTED]', token: '[REDACTED]' }
```

### ✅ DO: pino redact (автоматическая фильтрация)

```js
import pino from 'pino';

const logger = pino({
  redact: {
    paths: ['req.headers.authorization', 'req.headers.cookie', '*.password', '*.token', '*.secret'],
    censor: '[REDACTED]',
  },
});
```

---

## 10. Anti-patterns

| ❌ Anti-pattern | ✅ Решение |
|----------------|-----------|
| `req.body` без валидации | Zod schema + validate middleware |
| Секреты в коде / git | env vars + .gitignore + validation |
| Stack trace в response | Разные ответы для operational/programmer errors |
| JWT в localStorage | httpOnly + secure + sameSite cookie |
| `SELECT * WHERE id = '${id}'` | Параметризованные запросы |
| `exec(userInput)` | `execFile(cmd, [args])` |
| `cors({ origin: '*' })` в prod | Whitelist origins |
| PII в логах | Redact / sanitizeForLog |
| `lodash` ради 1 функции | Нативный JS/ES2025 |
| Нет npm audit | CI pipeline + регулярный audit |
| `md5(password)` | bcrypt/argon2 с salt |
| Разные ошибки для login | Единое «Invalid credentials» |

---

## Краткий чеклист (каждый PR)

- [ ] Input validated (Zod / whitelist schema)?
- [ ] No secrets in code / logs / errors?
- [ ] Errors don't leak internals?
- [ ] AuthZ checked before operation?
- [ ] No raw SQL/command concatenation?
- [ ] Dependencies audited?
- [ ] Sensitive data redacted from logs?

---

## См. также
- `$security-review` — полный security review чеклист (Reviewer gate)
- `$node-express-beast-practices` — Express middleware pipeline, error handler
- `$observability-logging` — structured logging с redaction
- `$es2025-beast-practices` — безопасная работа с данными