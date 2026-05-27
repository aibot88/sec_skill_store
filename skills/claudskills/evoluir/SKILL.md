---
name: kairos:evoluir
description: Evolui autonomamente os prompts dos agentes de runtime usando assertions binárias definidas pelo squad negocial. Inspirado no AutoResearch + binary evals. Use quando o usuário disser "kairos evoluir", "melhorar prompt", "evoluir agente", "evoluir diana", "otimizar prompts", "melhorar classificação", "melhorar acurácia dos agentes", ou quiser que os system prompts dos agentes melhorem automaticamente com base em cenários de teste do domínio.
disable-model-invocation: true
---

# KairOS-AI — Evoluir (AutoResearch para Prompts de Agentes)

Loop autônomo que evolui os system prompts dos agentes de runtime (DIANA, PEDRO, NORMA, etc.) usando **assertions binárias** definidas pelo squad negocial e **análise de falhas** antes de cada variante.

## O Diferencial

O squad negocial NÃO roda durante o loop — ele define os critérios ANTES:
- **Agente de domínio** define cenários de classificação com resposta esperada
- **Agente regulatório** define critérios legais que o output deve atender
- **Agente auditor** define checklist de conformidade
- **Gabriel [IA]** executa o loop usando esses critérios como assertions binárias

O resultado: prompts que melhoram sozinhos durante a noite, testados contra critérios reais de domínio.

## Como Usar

### Passo 1: Definir assertions (com squad negocial)

```
/kairos:rodar negocial
Preciso que o squad defina cenários de teste para o agente DIANA.
Para cada cenário, diga: input, resposta esperada, e critérios de validação.
```

O squad negocial gera um arquivo de cenários:

```
/kairos:evoluir diana --preparar
```

Isso cria a estrutura:

```
kairos/evolucao/diana/
├── prompt-atual.txt           ← system prompt atual do DIANA
├── cenarios.jsonl             ← cenários de teste (do squad negocial)
├── assertions.md              ← critérios binários (do squad negocial)
├── candidatos/                ← variantes geradas pelo loop
├── historico/                 ← versões anteriores com score no nome
└── resultados.tsv             ← log de todas as iterações
```

### Passo 2: Executar o loop

```
/kairos:evoluir diana
```

Ou para rodar durante a noite sem interrupção:

```
/kairos:evoluir diana --noturno --max-ciclos=50
```

## Estrutura dos Cenários (cenarios.jsonl)

Cada cenário é um teste real definido pelo squad negocial:

```jsonl
{"id": "c001", "input": {"cnae": "4120-4/00", "perigo": "Queda de andaime a 8m", "setor": "obras"}, "esperado": {"categoria": "acidental", "severidade_min": 4}}
{"id": "c002", "input": {"cnae": "8610-1/01", "perigo": "Exposição a agente biológico", "setor": "enfermaria"}, "esperado": {"categoria": "biologico"}}
{"id": "c003", "input": {"cnae": "2599-3/99", "perigo": "Ruído acima de 85dB por 6h/dia", "setor": "produção"}, "esperado": {"categoria": "fisico", "severidade_min": 2}}
{"id": "c004", "input": {"cnae": "4120-4/00", "perigo": "Pressão por prazo, assédio moral do encarregado", "setor": "escritório"}, "esperado": {"categoria": "psicossocial"}}
```

## Assertions Binárias (assertions.md)

Critérios sim/não que todo output deve atender:

```markdown
## Assertions para DIANA

1. **Categoria correta**: output.categoria == cenario.esperado.categoria → True/False
2. **Severidade mínima**: output.severidade >= cenario.esperado.severidade_min → True/False
3. **Fonte geradora presente**: output.fonte_geradora não está vazio → True/False
4. **Medida existente registrada**: output.medida_existente existe (mesmo que "Nenhuma") → True/False
5. **Não afirma segurança**: output NÃO contém "ambiente seguro" ou "sem risco" → True/False
6. **Hierarquia respeitada**: se sugere medida, segue ordem eliminação→...→EPI → True/False
7. **Formato JSON válido**: output é JSON parseável → True/False
```

**Pass rate = % de cenários onde TODAS as assertions retornam True.**

## Loop de Evolução

```
PARA CADA CICLO:

  0. CIRCUIT BREAKER
     Atualizar .kairos/estado/loop-state.json com ciclo atual, custos, etc.
     Chamar: bash ${CLAUDE_PLUGIN_ROOT}/scripts/circuit-breaker.sh
     Se retornar PARAR → interromper loop com mensagem ao usuário
     Se retornar OK → prosseguir

  1. ANALISAR FALHAS
     Ler resultados.tsv e cenarios com assertion failures
     Consultar ANTI-PADRÕES relevantes:
       bash ${CLAUDE_PLUGIN_ROOT}/scripts/aprendizado-consultar.sh "<agente> <contexto>"
     Se encontrar anti-padrões, NÃO repetir abordagens que falharam.
     Identificar padrões:
     - Qual assertion falha mais?
     - Quais tipos de cenário estão falhando?
     - O que os cenários que falham têm em comum?
     Escrever análise em kairos/evolucao/<agente>/analise-falhas.md

  2. GERAR 3 VARIANTES
     Cada variante muda UMA coisa no system prompt
     Cada variante tem um comentário no topo: "Hipótese: ..."
     VERIFICAR contra anti-padrões: se variante proposta é similar
     a um anti-padrão registrado, descartar ANTES de avaliar.
     Salvar em candidatos/v[N]a.txt, v[N]b.txt, v[N]c.txt
     
     Exemplos de mudanças:
     - Adicionar regra explícita para o padrão de falha
     - Adicionar few-shot example do cenário que falha
     - Reordenar seções do prompt
     - Explicitar uma instrução que estava implícita
     - Adicionar constraint de output format

  3. AVALIAR CADA VARIANTE
     Para cada variante:
       - Chamar Claude API com o prompt candidato
       - Passar cada cenário como input
       - Rodar todas as assertions no output
       - Calcular pass rate
     
     Registrar: variante, pass_rate, assertions_detalhadas

  4. SELECIONAR MELHOR
     Se alguma variante > pass rate atual:
       - Copiar para prompt-atual.txt
       - Mover versão anterior para historico/ com score no nome
       - Registrar no Radar
     Se nenhuma melhorou:
       - Registrar tentativa
       - Após 3 ciclos sem melhoria: registrar anti-padrão da abordagem dominante
         bash ${CLAUDE_PLUGIN_ROOT}/scripts/aprendizado-anti-padrao.sh \
           "evolucao" "<agente>" "<contexto>" "<abordagem>" "<motivo>"
       - Tentar mudança estrutural

  5. REGISTRAR NO TSV
     iteracao  variante  pass_rate  delta  status  hipotese
     0         -         65.0%      0.0    baseline estado inicial
     1         v1b       72.5%      +7.5   manter  "regra explícita para queda >2m"
     2         v2a       72.5%      0.0    descartar "reordenar seções"
     3         v3c       80.0%      +7.5   manter  "few-shot para psicossocial"

  6. REGRESSION CHECK (após cada "keep")
     Se variante foi aceita (keep):
       a. Carregar `.kairos/config/regression.yaml` para threshold e config
       b. Carregar golden dataset de `kairos/evolucao/<agente>/golden-dataset.jsonl`
          Se não existir golden dataset, usar dataset completo
       c. Rodar TODAS as assertions do golden/completo com a variante aceita
          Usar Haiku para economia (suficiente para avaliação de regression)
       d. Comparar pass rate geral com baseline geral
       e. Se pass rate geral caiu > threshold (default 2pts):
          → REVERTER variante (desfazer keep)
          → Registrar: "variante melhorou X mas piorou Y — revertida"
          → Registrar abordagem como anti-padrão
       f. Se pass rate geral manteve ou subiu:
          → CONFIRMAR keep
          → Atualizar baseline geral
          → Atualizar relatório de versões do golden dataset

  7. ATUALIZAR RELATÓRIO DE VERSÕES
     Após cada keep confirmado, atualizar histórico:
       | Versão | Data | Golden Pass Rate | Total Pass Rate | Notas |

     Release gate: pass rate golden >= 90% para considerar agente pronto.
```

## Resumo a cada 5 ciclos

```
=== KairOS Evolução — DIANA (ciclo 15) ===
Pass rate: 65.0% → 87.5% (+22.5%)
Mantidas: 6 | Descartadas: 8 | Sem mudança: 1
Assertion com mais falhas: "categoria correta" (3 cenários restantes)
Cenários ainda falhando:
  c012: "vibração de corpo inteiro" → classifica como "ergonômico" (esperado: "físico")
  c019: "trabalho noturno + monotonia" → classifica como "ergonômico" (esperado: "psicossocial")
  c023: "calor extremo em fundição" → severidade 2 (esperado: ≥3)
```

## Integração com Agent Teams

Para evoluir múltiplos agentes em paralelo:

```
/kairos:evoluir todos --noturno

KairOS: Criando Agent Team de evolução...

  Teammate 1: Gabriel → evoluindo DIANA (classificação de riscos)
  Teammate 2: Gabriel → evoluindo PEDRO (geração de PGR)
  Teammate 3: Gabriel → evoluindo NORMA (mapeamento de NRs)
  Teammate 4: Gabriel → evoluindo CAIO (análise de incidentes)

  4 agentes evoluindo em paralelo durante a noite.
  Resultados amanhã às 8h.
```

## Integração com Radar

Cada ciclo de evolução gera entrada no audit log:

```yaml
- timestamp: "..."
  tipo: evolucao_ciclo
  agente: diana
  ciclo: 15
  pass_rate_antes: 82.5
  pass_rate_depois: 87.5
  delta: +5.0
  status: manter
  hipotese: "few-shot example para cenário de risco psicossocial"
  variante: v15b
  cenarios_total: 40
  cenarios_passando: 35
  custo_tokens: 28500
  custo_usd: 0.85
```

## Smart Model Routing

O loop de evolução usa **routing inteligente** para reduzir custos em ~50%:

| Etapa | Tier | Modelo | Justificativa |
|-------|------|--------|---------------|
| `analisar_falhas` | standard | Sonnet | Análise de padrões em resultados |
| `gerar_variantes` | deep | Opus | Raciocínio profundo para criar hipóteses |
| `avaliar_cenario` (complexo) | standard | Sonnet | Avaliação com assertions binárias |
| `avaliar_cenario` (simples) | fast | Haiku | Cenários já convergidos ou triviais |
| `registrar_resultado` | local | — | Sem chamada de API |

Para consultar o modelo adequado, use:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/model-router.sh <tipo_tarefa>
```

Tipos de tarefa do evoluir:
- `evoluir_gerar_variantes` → Opus (deep)
- `evoluir_avaliar_variantes` → Sonnet (standard)
- `glossario` → Haiku (fast)

O `/kairos:radar` mostra custo por tier ao final do loop.

## Custo Estimado (com Model Routing)

- Gerar variantes (Opus): 3 chamadas × 30 ciclos ≈ $4.50
- Avaliar cenários complexos (Sonnet): 60 chamadas × 30 ciclos ≈ $1.80
- Avaliar cenários simples (Haiku): 60 chamadas × 30 ciclos ≈ $0.30
- **Total: ~$6.60/noite (economia de ~56% vs. tudo Opus)**
- Resultado esperado: +15-25 pontos de pass rate

## Quando Usar

| Cenário | Comando |
|---------|---------|
| Melhorar classificação de riscos do DIANA | `/kairos:evoluir diana` |
| Melhorar qualidade do PGR gerado pelo PEDRO | `/kairos:evoluir pedro` |
| Melhorar precisão do mapeamento CNAE da NORMA | `/kairos:evoluir norma` |
| Melhorar análise de causa raiz do CAIO | `/kairos:evoluir caio` |
| Evoluir todos os agentes (noturno) | `/kairos:evoluir todos --noturno` |
| Preparar cenários com squad negocial | `/kairos:evoluir diana --preparar` |

## Fluxo Completo

```
1. /kairos:rodar negocial
   "Definam cenários de teste para o agente DIANA"
   → Squad negocial gera cenarios.jsonl + assertions.md

2. /kairos:evoluir diana --preparar
   → Cria estrutura em kairos/evolucao/diana/

3. /kairos:evoluir diana --noturno --max-ciclos=30
   → Gabriel roda o loop durante a noite

4. Manhã seguinte:
   /kairos:radar "resultados da evolução do diana"
   → Radar mostra: pass rate subiu de 65% para 87.5%
     Melhor variante: v15b (few-shot psicossocial)
     Custo: $3.20 em tokens

5. /kairos:rodar negocial
   "Squad, validem o DIANA atualizado com cenários novos"
   → Squad negocial testa com cenários que o loop não tinha
   → Se encontrar falhas, adiciona novos cenários
   → Repete o loop na próxima noite
```

## Confidence Score

Os outputs gerados durante avaliação devem incluir `confidence` (0.0-1.0).
Consultar `.kairos/config/confidence.yaml` para thresholds e regras.

Assertions adicionais de confidence (IDs 28-31):
- **confidence_presente**: output inclui campo confidence
- **confidence_coerente**: confiança baixa quando cenário é ambíguo
- **review_quando_baixo**: outputs com confidence < 0.65 marcados para revisão
- **guardrail_prevalece**: se contradiz guardrail, confidence = 0.0

## Golden Dataset

Cada agente pode ter um golden dataset imutável em:
`kairos/evolucao/<agente>/golden-dataset.jsonl`

Regras (consultar `.kairos/config/golden-dataset.yaml`):
- NUNCA adicionar/remover cenários automaticamente
- Alterações somente com aprovação explícita do PO
- Cobrir todas as categorias + edge cases + anti-hallucination
- Release gate: pass rate golden >= 90% para produção

Para consultar: `/kairos:radar "golden dataset <agente>"`

## Feedback de Produção

Cenários gerados pelo pipeline de feedback (`.kairos/config/feedback.yaml`)
são incorporados ao `cenarios.jsonl` após aprovação humana.
Isso alimenta o loop com dados de uso real, não só teóricos.

## Learning Loop — Registro Automático

Após um ciclo de evolução bem-sucedido (delta > +5pts), registrar automaticamente
o padrão aprendido usando:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/aprendizado-registrar.sh \
  "evolucao" "<agente>" "<contexto>" "<padrão>" "<spec>"
```

Exemplo: se few-shot para psicossocial melhorou pass rate em 8pts, registrar:
- domínio: evolucao
- agente: gabriel
- contexto: "DIANA classificação psicossocial"
- padrão: "Few-shot com exemplo de assédio moral melhorou pass rate em 8pts"
- spec: "evolucao-diana"

Tudo em Português do Brasil.
