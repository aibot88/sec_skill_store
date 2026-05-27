---
name: kairos:revisar
description: >
  Revisão de código abrangente: qualidade + compliance + segurança.
  Classifica achados por severidade. Combina revisão de código genérica
  com validação de domínio regulado. Use quando o usuário disser "kairos
  revisar", "revisar código", "code review", "review de segurança".
argument-hint: "[arquivo, diretório, ou 'last-commit']"
user-invocable: true
disable-model-invocation: true
---

# KairOS — Revisão de Código (Qualidade + Compliance + Segurança)

Alvo: **$ARGUMENTS**

Se `$ARGUMENTS` é "last-commit":
```bash
FILES=$(git diff --name-only HEAD~1)
```

## Dimensão 1: Qualidade de Código

- Componentes duplicados? (Anti-Vibe Coding)
- Responsabilidades misturadas?
- Engenharia excessiva?
- TypeScript strict (nada de `any`, `as any`, `@ts-ignore`)?
- Tratamento de erros completo?
- Nomenclatura consistente com projeto?

## Dimensão 2: Compliance de Domínio

Carregue os guardrails do domínio instalado (`.kairos/dominio/*/guardrails.yaml`):
- Assertions do domínio estão sendo seguidas?
- Referências legais nos comentários quando aplicável?
- Cálculos regulatórios corretos?
- Formatos obrigatórios respeitados?

## Dimensão 3: Segurança (LGPD + OWASP)

- Políticas RLS em tabelas com dados pessoais?
- Endpoints validam autenticação?
- Dados sensíveis criptografados em repouso?
- Logs NÃO expõem dados pessoais?
- SQL Injection, XSS, Command Injection?
- Secrets fixos no código?
- CORS configurado corretamente?

## Dimensão 4: Desempenho

- Queries N+1?
- Re-renders desnecessários?
- Tamanho do bundle impactado?
- Timeouts adequados?

## Saída — Achados por Severidade

```
## Revisão: {alvo} — {data}

### 🔴 BLOQUEANTE ({N}) — Corrigir ANTES de merge
{arquivo}:{linha} — {descrição do problema}
Sugestão: {como corrigir}

### 🟡 ALERTA ({N}) — Deveria corrigir
{arquivo}:{linha} — {descrição do problema}
Sugestão: {como corrigir}

### 🟢 SUGESTÃO ({N}) — Melhoria opcional
{arquivo}:{linha} — {descrição do problema}
Sugestão: {como corrigir}

### Pontuação: {N}/10
- Qualidade:   {N}/10
- Compliance:  {N}/10
- Segurança:   {N}/10
- Desempenho:  {N}/10
```

## Idioma

TODAS as mensagens em Português do Brasil.
