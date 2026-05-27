# GuardrailSkill - Proteção e Validação

**Versão:** 1.0.0
**Data:** 06/02/2026
**Status:** Implementado e testado

---

## 📋 Visão Geral

GuardrailSkill é uma skill de **proteção e validação** que serve como guarda-chuva de segurança para OpenClaw Aurora e Hub Enterprise.

### O que protege?

✅ **SQL Injection** - Detecta e bloqueia tentativas de SQL injection
✅ **XSS (Cross-Site Scripting)** - Previne ataques de script injection
✅ **Path Traversal** - Bloqueia tentativas de acesso a diretórios sensíveis
✅ **Command Injection** - Previne execução de comandos do sistema
✅ **Rate Limiting** - Implementa limite de requisições por usuário
✅ **Resource Limits** - Monitora uso de CPU, memória e tempo de execução
✅ **Custom Patterns** - Suporta padrões customizados de detecção

---

## 🚀 Quick Start

### Básico

```typescript
import { createGuardrailSkill } from './skills/guardrail';

// Criar guardrail com configuração padrão
const guardrail = createGuardrailSkill();

// Validar input
const result = await guardrail.validateInput("SELECT * FROM users");
// result.isValid = false (detectou SQL injection)
```

### Com Configuração Custom

```typescript
const guardrail = createGuardrailSkill(
  {
    maxMemoryMB: 256,
    maxRequestsPerMinute: 50,
    maxExecutionTimeMs: 15000,
  },
  {
    enableSQLCheck: true,
    enableXSSCheck: true,
    customPatterns: [/malicious|evil/i],
  }
);
```

---

## 🛡️ Comandos Disponíveis

### 1. `validate` - Validar Input

Valida um input contra anti-patterns de segurança.

```typescript
await guardrail.execute({
  skillId: 'guardrail',
  params: {
    command: 'validate',
    data: "user_input_aqui",
    type: 'sql_injection', // Opcional: validar só este tipo
  },
});
```

**Tipos de validação:**
- `sql_injection` - SQL injection patterns
- `xss` - Cross-site scripting patterns
- `path_traversal` - Directory traversal patterns
- `command_injection` - Command execution patterns
- Omitir `type` = validar todos os tipos

**Response:**
```json
{
  "success": true,
  "data": {
    "validated": true,
    "isValid": false,
    "violations": [
      {
        "pattern": "SQL keyword detected",
        "input": "SELECT * FROM",
        "severity": "critical"
      }
    ]
  }
}
```

---

### 2. `check_rate_limit` - Verificar Rate Limit

Valida se uma requisição está dentro do limite de requisições por minuto.

```typescript
await guardrail.execute({
  skillId: 'guardrail',
  params: {
    command: 'check_rate_limit',
    identifier: 'user@example.com', // Identificador único do usuário/IP
  },
});
```

**Response:**
```json
{
  "success": true,
  "data": {
    "allowed": true,
    "message": "Request allowed"
  }
}
```

Se limite excedido:
```json
{
  "success": true,
  "data": {
    "allowed": false,
    "message": "Rate limit exceeded (100/min)"
  }
}
```

---

### 3. `check_resources` - Verificar Recursos

Valida se o sistema está dentro dos limites de recursos.

```typescript
await guardrail.execute({
  skillId: 'guardrail',
  params: {
    command: 'check_resources',
  },
});
```

**Response:**
```json
{
  "success": true,
  "data": {
    "within": true,
    "usage": {
      "memoryMB": 128.5,
      "cpuPercent": 45.2,
      "executionTimeMs": 1234
    },
    "limits": {
      "maxMemoryMB": 512,
      "maxCpuPercent": 80,
      "maxRequestsPerMinute": 100,
      "maxExecutionTimeMs": 30000,
      "maxFileUploadMB": 50
    }
  }
}
```

---

### 4. `status` - Obter Status Completo

Retorna status completo do guardrail.

```typescript
await guardrail.execute({
  skillId: 'guardrail',
  params: {
    command: 'status',
  },
});
```

**Response:**
```json
{
  "success": true,
  "data": {
    "timestamp": 1707228300000,
    "resourceUsage": {
      "memoryMB": 128.5,
      "cpuPercent": 45.2,
      "requestCount": 45
    },
    "violations": 3,
    "blocked": 2,
    "active": true
  }
}
```

---

## 🔍 Detecção de Anti-Patterns

### SQL Injection

Detecta:
- Caracteres SQL suspeitos: `'`, `--`, `;`, `||`, `*`
- Palavras-chave SQL: `UNION`, `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.

```typescript
// ❌ Bloqueado
"admin' OR '1'='1"
"SELECT * FROM users WHERE id=1"
"'; DROP TABLE users; --"

// ✅ Permitido
"user@example.com"
"My search query"
```

---

### XSS (Cross-Site Scripting)

Detecta:
- Tags `<script>`
- Event handlers (`onclick`, `onload`, `onerror`, etc)
- Tags `<iframe>`

```typescript
// ❌ Bloqueado
"<script>alert('xss')</script>"
"<img src=x onerror='alert()'>"
"<iframe src='malicious.com'></iframe>"

// ✅ Permitido
"<p>Hello World</p>" // Nota: Detecta qualquer HTML, cuidado
"This is safe text"
```

---

### Path Traversal

Detecta:
- Sequences `../` (relative paths)
- URL-encoded: `%2e%2e` (`.` URL-encoded)

```typescript
// ❌ Bloqueado
"../../../etc/passwd"
"..%2f..%2fetc%2fpasswd"

// ✅ Permitido
"/home/user/documents"
"./relative/path"
```

---

### Command Injection

Detecta:
- Caracteres de shell: `;`, `&`, `|`, `` ` ``, `$()`, `()`
- Comandos de sistema: `bash`, `sh`, `cmd`, `powershell`, `exec`, `system`, `eval`

```typescript
// ❌ Bloqueado
"file.txt; rm -rf /"
"$(whoami)"
"`cat /etc/passwd`"

// ✅ Permitido
"Just a normal string"
"user@host"
```

---

## 📊 Limites de Recursos

```typescript
interface ResourceLimits {
  maxMemoryMB: number;           // Limite de memória heap
  maxCpuPercent: number;         // Limite de CPU
  maxRequestsPerMinute: number;  // Taxa de requisições
  maxExecutionTimeMs: number;    // Tempo máximo de execução
  maxFileUploadMB: number;       // Tamanho máximo de upload
}
```

**Padrões:**
```typescript
{
  maxMemoryMB: 512,
  maxCpuPercent: 80,
  maxRequestsPerMinute: 100,
  maxExecutionTimeMs: 30000,  // 30 segundos
  maxFileUploadMB: 50
}
```

---

## 🔐 Configuração de Validação

```typescript
interface ValidationConfig {
  enableSQLCheck: boolean;        // Habilitar SQL injection check
  enableXSSCheck: boolean;        // Habilitar XSS check
  enablePathTraversal: boolean;   // Habilitar path traversal check
  enableCommandInjection: boolean; // Habilitar command injection check
  customPatterns: RegExp[];       // Padrões customizados
}
```

**Padrão:**
```typescript
{
  enableSQLCheck: true,
  enableXSSCheck: true,
  enablePathTraversal: true,
  enableCommandInjection: true,
  customPatterns: []
}
```

---

## 💻 Exemplos de Uso

### Exemplo 1: Validar Entrada de Usuário

```typescript
import { createGuardrailSkill } from './skills/guardrail';

const guardrail = createGuardrailSkill();

// Usuário submete um formulário
const userInput = req.body.search;

const validation = await guardrail.validateInput(userInput);

if (!validation.isValid) {
  return res.status(400).json({
    error: 'Input validation failed',
    violations: validation.violations,
  });
}

// Continuar processamento
db.query(`SELECT * FROM products WHERE name LIKE '%${userInput}%'`);
```

---

### Exemplo 2: Rate Limiting por Usuário

```typescript
const guardrail = createGuardrailSkill({
  maxRequestsPerMinute: 50,
});

// Middleware Express
app.use(async (req, res, next) => {
  const userIdentifier = req.user?.id || req.ip;
  const allowed = guardrail.checkRateLimit(userIdentifier);

  if (!allowed) {
    return res.status(429).json({
      error: 'Too many requests',
      retryAfter: 60,
    });
  }

  next();
});
```

---

### Exemplo 3: Monitorar Saúde do Sistema

```typescript
const guardrail = createGuardrailSkill({
  maxMemoryMB: 512,
  maxExecutionTimeMs: 30000,
});

// Health check endpoint
app.get('/health', async (req, res) => {
  const resources = guardrail.checkResourceLimits();
  const status = guardrail.getStatus();

  if (!resources.within) {
    return res.status(503).json({
      status: 'unhealthy',
      reason: 'Resource limits exceeded',
      usage: resources.usage,
    });
  }

  res.json({
    status: 'healthy',
    guardrail: status,
  });
});
```

---

### Exemplo 4: Padrões Customizados

```typescript
const guardrail = createGuardrailSkill(
  {},
  {
    customPatterns: [
      /credit[\s_-]?card[\s_-]?number/i, // Detectar CC number
      /social[\s_-]?security[\s_-]?number/i, // Detectar SSN
      /password[\s_-]?field/i, // Detectar password fields
    ],
  }
);

// Agora detecta padrões customizados também
const validation = await guardrail.validateInput(
  'please enter your credit card number'
);
// validation.isValid = false
```

---

## 🧪 Testes

```bash
# Rodar testes
npm test -- guardrail

# Rodar com cobertura
npm test -- guardrail --coverage
```

**Cobertura de testes:**
- ✅ SQL Injection detection
- ✅ XSS detection
- ✅ Path Traversal detection
- ✅ Command Injection detection
- ✅ Rate limiting
- ✅ Resource limits
- ✅ Status tracking
- ✅ Edge cases

---

## 🔧 Integração com Hub Enterprise

### Como usar no Hub Enterprise

```typescript
// No orchestrator do Hub Enterprise
import { createGuardrailSkill } from './skills/guardrail';

const guardrail = createGuardrailSkill();

// Antes de executar qualquer comando
async function executeWithGuardrails(command: string, input: string) {
  // 1. Validar input
  const validation = await guardrail.validateInput(input);
  if (!validation.isValid) {
    throw new Error(`Security violation: ${validation.violations[0].pattern}`);
  }

  // 2. Verificar rate limit
  const allowed = guardrail.checkRateLimit(command);
  if (!allowed) {
    throw new Error('Rate limit exceeded');
  }

  // 3. Verificar recursos
  const resources = guardrail.checkResourceLimits();
  if (!resources.within) {
    throw new Error('Resource limits exceeded');
  }

  // 4. Executar comando com segurança
  return await executeCommand(command, input);
}
```

---

## ⚠️ Limitações e Considerações

1. **False Positives**: Alguns inputs válidos podem ser bloqueados (ex: logs contendo SQL)
   - Solução: Use `type` parameter para validar só tipos específicos

2. **Performance**: Validação por regex pode ser lenta com muitos padrões customizados
   - Solução: Use menos padrões customizados, cache resultados

3. **Unicode**: Alguns padrões podem não funcionar bem com Unicode
   - Solução: Testar com seus casos de uso específicos

4. **CPU Monitoring**: CPU percent é simulado (não funciona em todos os SOs)
   - Solução: Implementar via `os.cpus()` ou APM externo

---

## 📚 Referências

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

---

## 🚀 Roadmap

- [ ] Suporte a machine learning para detecção de anomalias
- [ ] Integração com WAF (Web Application Firewall)
- [ ] Métricas de segurança em tempo real
- [ ] Dashboard de violations
- [ ] Alertas por Telegram/Email
- [ ] Persist violations em banco de dados

---

**Desenvolvido com ❤️ para OpenClaw Aurora**
