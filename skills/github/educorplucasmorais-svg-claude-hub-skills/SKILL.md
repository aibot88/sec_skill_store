---
name: security-audit
description: Auditoria de segurança, análise de vulnerabilidades OWASP, proteção de dados e hardening
version: 1.0.0
tags: [security, owasp, vulnerability, pentest, hardening]
---

# 🔐 Skill: Auditoria de Segurança

## Ativação
Use quando: "segurança", "vulnerabilidade", "OWASP", "CVE", "autenticação", "autorização", "injeção"

## OWASP Top 10 - Checklist Completo

### A01: Broken Access Control
```typescript
// ❌ VULNERÁVEL: usuário pode acessar dados de outro
app.get('/api/orders/:id', async (req, res) => {
  const order = await db.order.findById(req.params.id)
  res.json(order)
})

// ✅ SEGURO: verificar ownership
app.get('/api/orders/:id', authenticate, async (req, res) => {
  const order = await db.order.findFirst({
    where: { id: req.params.id, userId: req.user.id } // ← ownership check
  })
  if (!order) return res.status(403).json({ error: 'Forbidden' })
  res.json(order)
})
```

### A02: Cryptographic Failures
```typescript
// ❌ NUNCA: senha em plain text ou MD5
const hash = md5(password)

// ✅ SEMPRE: bcrypt com custo ≥ 12
import bcrypt from 'bcrypt'
const hash = await bcrypt.hash(password, 12)
const valid = await bcrypt.compare(inputPassword, hash)

// ✅ Dados sensíveis em trânsito: HTTPS obrigatório
// ✅ Dados sensíveis em repouso: encrypt com AES-256
```

### A03: Injection (SQL, XSS, Command)
```typescript
// ❌ SQL Injection
const users = await db.query(`SELECT * FROM users WHERE email = '${email}'`)

// ✅ Parametrizado (Prisma/TypeORM fazem isso automaticamente)
const users = await prisma.user.findMany({ where: { email } })

// ❌ XSS
element.innerHTML = userInput

// ✅ Sanitize
import DOMPurify from 'dompurify'
element.innerHTML = DOMPurify.sanitize(userInput)
```

### A04: Insecure Design
- Design para falha segura (fail-secure)
- Princípio do menor privilégio
- Defense in depth: múltiplas camadas de segurança
- Separar admin de usuário regular por rotas/middleware diferentes

### A05: Security Misconfiguration
```typescript
// ❌ Debug habilitado em produção
app.use(morgan('dev')) // em produção

// ✅ Configuração por ambiente
if (process.env.NODE_ENV !== 'production') {
  app.use(morgan('dev'))
}

// ✅ Helmet para headers HTTP seguros
import helmet from 'helmet'
app.use(helmet())

// ✅ CORS restritivo
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }))
```

### A06: Vulnerable Components
```bash
# Verificar dependências com vulnerabilidades
npm audit
npm audit fix

# Verificar CVEs conhecidos
npx snyk test
```

### A07: Authentication Failures
```typescript
// ✅ JWT seguro
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET!,
  { 
    expiresIn: '15m',      // Access token curto
    algorithm: 'HS256'
  }
)

// ✅ Refresh token rotation
// ✅ Rate limiting em login
import rateLimit from 'express-rate-limit'
const loginLimiter = rateLimit({ windowMs: 15*60*1000, max: 5 })
app.use('/api/auth/login', loginLimiter)

// ✅ Account lockout após N tentativas
```

### A08: Software and Data Integrity
```typescript
// ✅ Validação de entrada em TODAS as rotas
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(2).max(100).regex(/^[a-zA-ZÀ-ÿ\s]+$/)
})

app.post('/api/users', (req, res) => {
  const result = createUserSchema.safeParse(req.body)
  if (!result.success) return res.status(400).json(result.error)
  // ... use result.data (typed and validated)
})
```

### A09: Logging & Monitoring
```typescript
// ✅ Log eventos de segurança (sem dados sensíveis)
logger.warn('Failed login attempt', { 
  email: obfuscateEmail(email),
  ip: req.ip,
  timestamp: new Date()
})

// ✅ NÃO logar:
// - Senhas, tokens, cartões de crédito
// - CPF/dados pessoais completos
// - Conteúdo de mensagens privadas
```

### A10: SSRF (Server-Side Request Forgery)
```typescript
// ✅ Whitelist de domínios permitidos para fetch externo
const ALLOWED_DOMAINS = ['api.stripe.com', 'api.sendgrid.com']
function validateUrl(url: string): boolean {
  const { hostname } = new URL(url)
  return ALLOWED_DOMAINS.includes(hostname)
}
```

## Checklist de Auditoria Rápida
- [ ] Senhas com bcrypt ≥ 12 rounds?
- [ ] JWT com expiração curta + refresh token?
- [ ] Rate limiting em endpoints sensíveis?
- [ ] Validação de entrada com Zod/Joi?
- [ ] Helmet configurado?
- [ ] CORS restritivo?
- [ ] Secrets em variáveis de ambiente (.env)?
- [ ] npm audit sem HIGH/CRITICAL?
- [ ] HTTPS em produção?
- [ ] Logs sem dados sensíveis?

### Regras desta Skill
- Segurança não é opcional — é requisito de qualidade
- Nunca confie em input do cliente (valide sempre no server)
- Princípio do menor privilégio em tudo
- Falha aberta é pior que falha fechada
