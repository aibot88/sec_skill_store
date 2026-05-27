---
name: security-first
description: Sempre considera vetores OWASP top-10 ao escrever/revisar código
roles: [dev, qa]
---
Antes de declarar uma task como pronta, passe pela checklist de
segurança abaixo. Se algum item se aplica e não foi tratado, adicione
ao `next_agent_input` como bloqueio explícito.

**Checklist (OWASP-derived):**

1. **Input validation** — toda entrada externa (HTTP, CLI, arquivo)
   tem validação de tipo + bounds + sanitização? Falhar fechado.
2. **SQL injection** — query parameterizada? Nunca interpolação direta
   de input em string SQL.
3. **Command injection** — `subprocess.run` com shell=True? Use args
   como lista, não string concatenada com input.
4. **Path traversal** — paths construídos com input externo passam por
   `Path().resolve()` + check contra root permitido?
5. **Secrets em código** — strings tipo `sk-...`, `ghp_...`, JWT, db
   urls com password commitados? Use env var ou keychain.
6. **AuthN/AuthZ** — endpoint novo tem decorator/middleware de auth?
   Verifica `owner == current_user` em recursos privados?
7. **CSRF/CORS** — endpoint state-changing aceita GET? CORS aberto pra
   `*` em prod?
8. **Logging sensível** — request body com password/token vai pro log
   estruturado?
9. **Deserialização insegura** — uso de formatos que executam código
   arbitrário (pickle/yaml unsafe load) sobre input externo? Prefira
   JSON ou YAML safe loader.
10. **Rate limiting** — endpoint pesado/auth tem rate limit?

Quando algum item aplica e foi tratado, **mencione** em uma frase no
`actions_taken` (ex: "auth/login.py: input validado com Pydantic,
SQL parameterizado").

Quando aplica e NÃO foi tratado, **levante** como `clarifying_questions`
ou `human_dependencies` ANTES de finalizar a task.

Princípio: segurança é parte da definição de "pronto", não polish
opcional.
