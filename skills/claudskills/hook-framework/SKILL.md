---
description: Hook Framework do $100M Leads — 3 tipos de hook (dream outcome, problem, secret). Use para gerar headlines de LP, hooks de ads (especialmente short-form), subject lines de email, primeiras frases de copy.
---

# Hook Framework

Fonte: Alex Hormozi, *$100M Leads* (Magnetic Reasons + Lead Magnet hooks) + *$100M Offers* (Naming).

## Os 3 tipos de hook

### 1. Dream Outcome Hook
**Estrutura:** "Como [pessoa específica] alcançou [resultado específico] em [tempo] sem [obstáculo comum]"

Exemplos:
- "Como closers iniciantes passaram de R$ 8k pra R$ 23k MRR em 47 dias sem mudar de empresa"
- "Como freelancers de design fecharam contratos de R$ 50k+ sem cold email"

**Quando usar:** audience aspiracional, cliente já vê o desejo claramente.

### 2. Problem Hook
**Estrutura:** "Pare de [comportamento errado]. O problema não é [diagnóstico raso], é [diagnóstico real]."

Exemplos:
- "Pare de ler livro de vendas. O problema do seu closer não é técnica, é objeção de preço."
- "Pare de gastar em ads. Sua LP perde 80% do tráfego porque a oferta está fraca."

**Quando usar:** audience cética, cliente já tentou outras coisas, precisa de reframe.

### 3. Secret Hook
**Estrutura:** "A coisa que [autoridade/grupo] não conta sobre [tópico relevante]"

Exemplos:
- "A coisa que os top closers de SaaS não contam sobre objeção de preço"
- "O número que sua planilha de pricing está mentindo pra você"

**Quando usar:** audience curiosa, tópico onde existe percepção de informação oculta.

## Anti-padrões (descarta automaticamente)

- "Descubra o segredo de X" (genérico, sem especificidade)
- "Você quer ganhar mais?" (yes/no genérico)
- "Hoje vou te ensinar..." (anti-hook, mata atenção)
- Emoji excessivo
- TUDO EM CAIXA ALTA
- Pergunta retórica óbvia

## Critérios de qualidade

Um hook bom passa em 3 testes:

1. **Especificidade numérica:** tem número (idade, valor, tempo, %, quantidade)
2. **Tweet test:** o hook lê isoladamente como tweet/post? Se sim, OK.
3. **Curiosity gap:** o leitor PRECISA saber o que vem depois?

## Workflow batch (15 hooks)

Quando comando `/hormozi-gtm:hooks` for invocado:

1. Coleta ICP + oferta + transformação prometida
2. Gera 5 hooks por tipo (5 dream + 5 problem + 5 secret) = 15 total
3. Especifica para cada hook:
   - Ângulo (dream/problem/secret)
   - Mecanismo (qual emoção/pensamento aciona)
   - Onde usar (LP headline / ad hook / email subject)
4. Identifica top 3 do agent com justificativa

Quantidades configuráveis via `--n=N` (default 15).

## Aplicação por caso de uso

| Caso | Como usar Hook Framework |
|---|---|
| LP de vendas | Primary headline + sub-headline testam 3 tipos diferentes. Winner rotates |
| Roteiro de ad | Primeiros 3 segundos = hook. Short-form vive ou morre aqui |
| Hooks batch | 15-20 variantes pra teste A/B |

## Especialização por plataforma

| Plataforma | Tipo de hook que tende a vencer |
|---|---|
| Reels / TikTok | Problem hook (reframe rápido) |
| YouTube | Dream outcome hook (longo formato suporta) |
| LP headline | Dream outcome hook (alta especificidade) |
| Email subject | Secret hook (curiosity > especificidade) |

## Referência detalhada

Veja `reference/100m-leads-extracts.md` (seção Magnetic Reasons + Hook Mechanics).
