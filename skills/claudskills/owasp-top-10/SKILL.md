---
name: owasp-top-10
description: Revisa código contra as 10 falhas mais comuns antes de merge
roles: [dev, qa, cto]
---
Checklist antes de mergear endpoint novo:

1. **Injection**: SQL com parameter binding, nunca string concat. Shell com `shlex.split`.
2. **Broken Auth**: rate limit, lockout após N tentativas, sessions com expiração.
3. **Sensitive Data**: HTTPS obrigatório, senha com bcrypt/argon2, PII criptografada at rest.
4. **XXE/SSRF**: validar URLs externas (whitelist de host), parser XML sem entity expansion.
5. **Broken Access**: autorização por **recurso** (não só por rota).
6. **Misconfig**: headers de segurança, CORS restritivo, debug OFF em prod.
7. **XSS**: template com escape automático; nunca `innerHTML = userInput`.
8. **Deserialization**: nunca `pickle.loads`/`yaml.load` em input externo. Use schemas (Pydantic/Zod).
9. **CVE Components**: `npm audit`/`pip-audit`/`cargo audit` em CI.
10. **Logging**: sem PII, com correlation ID, com timestamp UTC.
