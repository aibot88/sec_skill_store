---
name: kairos:aprender
description: >
  Auto-extração de padrões de domínio regulado. Quando o dev resolve um
  problema complexo de compliance, extrai como padrão reutilizável que é
  auto-injetado em situações similares. Use quando o usuário disser "kairos
  aprender", "extrair padrão", "registrar padrão", "salvar como padrão".
argument-hint: "[descrição do padrão a extrair]"
user-invocable: true
disable-model-invocation: false
---

# KairOS — Aprendizado de Padrões de Domínio

O dev descreveu: **$ARGUMENTS**

## Etapa 1: Análise do Padrão

1. Identifique o **PROBLEMA** que foi resolvido
2. Identifique a **SOLUÇÃO** implementada
3. Identifique as **ASSERTIONS** que se aplicam
4. Identifique as **CONDIÇÕES** em que este padrão se aplica

## Etapa 2: Extração como Padrão Reutilizável

Registre em `.kairos/aprendizado/padroes.yaml`:

```yaml
- slug: "{slug}"
  dominio: "{domínio}"
  criado_em: "{data}"
  palavras_chave: ["...", "..."]
  assertions: ["LGPD-002", "..."]
  problema: "{descrição do problema}"
  solucao: "{descrição da solução}"
  codigo_referencia: "{trecho de código real do projeto}"
  armadilhas: "{o que NÃO fazer}"
  uso_count: 0
```

## Etapa 3: Portão de Qualidade

Antes de salvar, verificar:
- [ ] O padrão é GENÉRICO o suficiente para reutilização?
- [ ] O padrão é ESPECÍFICO o suficiente para ser útil?
- [ ] As assertions estão corretamente vinculadas?
- [ ] O código de referência é limpo?
- [ ] Não duplica um padrão já existente?

Se algum portão falha → refinar ou descartar.

## Regras de Ciclo de Vida

- Padrões são AUTO-INJETADOS quando palavras-chave casam com a tarefa
- Padrões com `uso_count > 5` → candidatos a PROMOÇÃO para skill oficial
- Padrões com `uso_count = 0` após 30 dias → candidatos a LIMPEZA
- NUNCA armazene dados pessoais ou secrets em padrões

## Saída

```
══════════════════════════════════════════
  KairOS Aprender — Padrão Extraído
══════════════════════════════════════════

  Padrão:        {slug}
  Domínio:       {domínio}
  Palavras-chave:{lista}
  Assertions:    {IDs}

══════════════════════════════════════════
```

## Idioma

TODAS as mensagens em Português do Brasil.
