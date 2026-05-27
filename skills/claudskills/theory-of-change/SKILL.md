---
name: theory-of-change
description: Constrói teoria da mudança (insumos → atividades → resultados → impactos) e deriva indicadores de monitoramento com desagregações por grupo vulnerabilizado. Para planejamento de políticas, programas e projetos de impacto social.
---

# Teoria da Mudança e Indicadores de Monitoramento

## Quando usar esta skill

Esta skill apoia o trabalho de **construir teoria da mudança (ToC)** e **derivar indicadores de monitoramento** a partir dela, quando uma política, programa ou projeto precisa de lógica causal explícita antes de ir pra implementação ou avaliação.

- Formular ou reformular **política pública, programa social ou projeto de impacto**
- Transformar objetivos genéricos ("reduzir evasão escolar", "melhorar qualidade da atenção básica") em **lógica causal explícita** com pressupostos nomeados
- Derivar **indicadores de monitoramento** alinhados a cada nível lógico, com desagregações por grupo vulnerabilizado
- **Revisar ToC existente** contra a lente de equidade (ver variante em `references/variantes.md`)
- Preparar **validação coletiva** da ToC com stakeholders (a skill produz o kit de facilitação)

Sinais típicos na conversa do usuário:

- "Preciso montar a teoria da mudança desse programa"
- "Temos os objetivos definidos mas faltam indicadores"
- "Como saber se a política está funcionando?"
- "A secretaria cobrou um modelo lógico pro projeto"
- "Precisamos revisar a ToC do ano passado antes da nova rodada de planejamento"
- "Os pressupostos do programa nunca foram explicitados"

## Pré-requisitos

Antes de começar, o usuário precisa ter:

1. **Objetivos iniciais** — mesmo que em formato disperso (anotações de oficina, bullet points de email, trechos de relatório, mandato institucional). Não precisa ser uma lista polida; a skill trata os dois casos.

2. **Contexto mínimo do problema** — o que a política/programa quer enfrentar, em termos concretos. Número, diagnóstico, testemunho — qualquer coisa que ancore a discussão no mundo real.

3. **Noção dos grupos afetados** — quem são as pessoas impactadas pela intervenção. A skill vai pedir que você os nomeie explicitamente logo na Etapa 2 (não serve "a população").

4. **Tempo para validação coletiva com stakeholders** — após a Etapa 5, a skill força um checkpoint humano obrigatório. A ToC precisa ser debatida com quem vai implementar e com quem vai ser afetado antes de prosseguir pros indicadores. Pular este passo é AI work slop disfarçado.

5. **Disposição para marcar hipóteses como `[suposição]`** — boa parte do trabalho de ToC é explicitar o que assumimos sem provar. Se você quer uma ToC "certa" sem marcas de incerteza, esta skill não serve.

## Princípios invioláveis

Estas 6 regras valem em TODAS as etapas. Não negocie.

1. **Nunca inventar fato ou causalidade.** Se não está nos insumos, escreva "não encontrado". Não preencher elos causais com conhecimento geral do modelo — é o jeito mais rápido de construir uma ToC bonita e irreal.

2. **Toda hipótese marcada como `[suposição]`.** Inferências, generalizações e pressupostos não verificados carregam a marca explícita + uma frase justificando por que a inferência é razoável. Na ToC, isso vale especialmente para elos causais (`se X então Y`) que não têm evidência direta nos insumos.

3. **Formato se–então–porque para toda ligação causal.** Fiel ao Caso 6 do livro. Evita atalhos do tipo "X leva a Y" sem explicitar o mecanismo. Se você não consegue escrever o "porque", provavelmente o elo é suposição não auditada.

4. **Distinção rigorosa de níveis lógicos.** Insumo ≠ atividade ≠ produto ≠ resultado intermediário ≠ impacto. Misturar níveis é o erro mais comum em ToC mal feita e contamina os indicadores derivados. Cada indicador precisa estar no nível lógico do objetivo que acompanha (ou em nível adjacente, justificado).

5. **Lente de equidade e justiça social em todas as etapas.** A ToC nomeia explicitamente grupos afetados, diferencia impactos por grupo vulnerabilizado, examina relações de poder nos pressupostos e carrega desagregações obrigatórias nos indicadores. A Etapa 4 é dedicada à auditoria estrutural; os hooks nas Etapas 2, 6 e 7 reforçam o método nas decisões críticas. Ver `docs/equity-lens.md` para critérios operacionais. **Esta não é uma regra opcional** — skills de impacto social sem lente de equidade operacional reproduzem desigualdades.

6. **ToC é artefato deliberativo, não produto final do modelo.** O kit de reunião na Etapa 5 e o checkpoint humano obrigatório existem porque a validação coletiva com stakeholders é parte da skill, não um adendo. Entregar uma ToC "pronta" sem esse passo fere o princípio da legitimidade e transforma a skill em produção de AI work slop com consequências reais sobre pessoas.

## O workflow (7 etapas)

O trabalho é organizado em 7 etapas sequenciais, agrupadas em dois sub-arcos: as Etapas 1-5 constroem e validam a Teoria da Mudança; um **checkpoint humano obrigatório** separa os dois arcos; as Etapas 6-7 derivam indicadores a partir da ToC já validada. Cada etapa tem um **objetivo** específico, um **prompt sugerido** pronto para copiar e um **output esperado** que serve de insumo para a etapa seguinte. Os prompts usam tags XML (`<escopo>`, `<modo_input>`, `<caminho>`, `<equidade_etapa2>`, `<auditoria_equidade>` etc.) para reduzir ambiguidade — é uma prática recomendada pela Anthropic para entradas estruturadas e saídas mais confiáveis. **Não pule etapas**, especialmente o checkpoint entre a Etapa 5 e a 6 — fichas técnicas de indicadores derivadas de uma ToC não validada são retrabalho garantido.

### Etapa 1 — Configuração, escopo e modo de entrada

**Objetivo:** Estabelecer as regras do trabalho com o modelo, capturar o escopo rico da ToC a ser construída (programa/política, problema-alvo, público afetado, horizonte temporal, stakeholders, contexto territorial), e **declarar o modo de input** — `estruturado` (usuário já tem objetivos e problemas padronizados) ou `disperso` (usuário tem anotações, emails, relatórios brutos). A declaração é visível e auditável.

**Prompt sugerido:**

```
Você é especialista em estratégia, monitoramento e avaliação de
políticas públicas e projetos de impacto social. Trabalhe em português
claro e inclusivo. Sua tarefa nesta conversa é apoiar a construção de
uma Teoria da Mudança e a derivação de indicadores de monitoramento.
Antes de começar, leia e concorde com os princípios abaixo — eles
valem para todas as respostas desta conversa.

<principios>
1. Nunca inventar fato ou causalidade. Se não está nos insumos,
   escreva "não encontrado". Não preencher elos causais com
   conhecimento geral.
2. Toda hipótese marcada como [suposição], com uma frase justificando
   por que a inferência é razoável.
3. Formato se–então–porque para toda ligação causal. Sem atalho.
4. Distinção rigorosa de níveis lógicos: insumo ≠ atividade ≠ produto
   ≠ resultado intermediário ≠ impacto.
5. Lente de equidade em todas as etapas: nomear grupos afetados,
   diferenciar impactos por grupo vulnerabilizado, examinar relações
   de poder nos pressupostos, carregar desagregações obrigatórias
   nos indicadores.
6. ToC é artefato deliberativo: o kit de reunião da Etapa 5 e o
   checkpoint humano obrigatório são parte da skill, não opcionais.
</principios>

Agora preciso que você preencha o escopo da ToC com base no que eu
já te contei. Se algum campo estiver indefinido, pergunte.

<escopo>
  <programa_ou_politica>...</programa_ou_politica>
  <problema_alvo>...</problema_alvo>
  <publico_afetado>...</publico_afetado>
  <horizonte_temporal>...</horizonte_temporal>
  <stakeholders_criticos>...</stakeholders_criticos>
  <contexto_territorial>...</contexto_territorial>
</escopo>

<modo_input>estruturado|disperso</modo_input>

- "estruturado" significa que você já tem objetivos e problemas
  prioritários padronizados, e vai passá-los direto.
- "disperso" significa que você tem anotações, emails, relatórios
  brutos ou outras entradas não-estruturadas, e a próxima etapa vai
  extrair os objetivos e problemas desses insumos primeiro.

Se concordar com as regras, responda "OK – regras definidas" e aguarde
os insumos.
```

**Output esperado:** Confirmação "OK – regras definidas" + blocos `<escopo>` e `<modo_input>` preenchidos, prontos para serem referenciados nas etapas seguintes.

### Etapa 2 — Estruturação e organização de insumos

**Objetivo:** Organizar objetivos e problemas prioritários em texto corrido com vínculos iniciais de causa-efeito, padronizados em formato que alimenta a Etapa 3. Comportamento bifurca pelo `<modo_input>` declarado na Etapa 1: se `disperso`, primeiro extrai objetivos e problemas dos insumos brutos; se `estruturado`, pula direto pra padronização.

**Prompt sugerido:**

```
Agora vamos estruturar os insumos. O comportamento depende do
<modo_input> declarado na Etapa 1.

SE modo_input = "disperso":
  Leia os insumos brutos que vou colar abaixo (anotações, emails,
  trechos de relatório, notas de oficina) e EXTRAIA, nesta ordem:
  (a) lista de objetivos candidatos
  (b) lista de problemas prioritários que a política/programa enfrenta
  Padronize cada objetivo em UMA frase no formato:
    "<verbo de ação> <público> <indicador numérico ou qualitativo>
     <horizonte temporal>"
  Exemplo: "Reduzir em 30% a taxa de evasão escolar entre estudantes
  do 1º ano do ensino médio público da rede estadual até 2028."
  Priorize os problemas pela frequência com que aparecem nos insumos
  e pela gravidade aparente (nomeada por quem escreveu o insumo).

SE modo_input = "estruturado":
  Receba a lista de objetivos e problemas já padronizados pelo usuário
  e padronize SÓ o formato (verbo de ação + público + indicador +
  horizonte), sem extração prévia.

EM AMBOS OS CASOS, depois da padronização produza:

1. <objetivos> Lista numerada de objetivos padronizados </objetivos>
2. <problemas> Lista numerada de problemas priorizados </problemas>
3. <vinculos_iniciais>
   Texto corrido (máx. 2 parágrafos) indicando quais problemas
   parecem conectados a quais objetivos, usando [suposição] para
   inferências.
   </vinculos_iniciais>

4. <equidade_etapa2>
   Esta é uma seção OBRIGATÓRIA. Responda às 3 perguntas abaixo
   explicitamente:

   (a) Quais grupos afetados pelo problema NÃO aparecem nos objetivos
       padronizados? Nomeie com especificidade (ex: "mães adolescentes
       trabalhadoras", "estudantes com deficiência", "meninos negros
       de periferia" — não use "a população" ou "os estudantes").

   (b) Por que esses grupos podem ter sido omitidos? Escolha entre:
       - viés de quem formulou os objetivos (perspectiva limitada)
       - dado ausente sobre o grupo (invisibilidade estatística)
       - decisão deliberada (fora do escopo declarado)
       E justifique em 1 frase.

   (c) Há ausências que comprometem a lógica causal da ToC? Ou seja:
       se um grupo não está nos objetivos mas é um dos mais afetados
       pelo problema, a ToC falha por construção. Nomeie os casos
       críticos.
   </equidade_etapa2>

Use "não encontrado" onde o material original não der base para
responder e [suposição] quando estiver inferindo.
```

**Output esperado:** Listas padronizadas de objetivos e problemas + texto de vínculos iniciais + seção `<equidade_etapa2>` respondendo às 3 perguntas obrigatórias.

### Etapa 3 — Caminhos causais alternativos

**Objetivo:** Propor 3 a 5 caminhos de mudança alternativos no formato **se–então–porque**, variando grau de alcance (conservador, intermediário, ambicioso). Fiel ao Caso 6 Etapa 3 do livro.

**Prompt sugerido:**

```
A partir dos objetivos e problemas organizados na Etapa 2, proponha
3 a 5 caminhos de mudança alternativos. Regras:

- PELO MENOS um caminho conservador (muda pouco, risco baixo,
  aproveita estruturas existentes)
- PELO MENOS um caminho intermediário (mudança moderada, risco
  médio, combina estruturas existentes com inovações pontuais)
- PELO MENOS um caminho ambicioso (muda muito, risco alto, requer
  mudanças estruturais ou novos recursos)

Para cada caminho, produza um BLOCO TEXTUAL NUMERADO (não tabela —
frases curtas são mais úteis nessa etapa):

<caminho id="1" grau="conservador">
  Nome curto: [título do caminho em 5-8 palavras]

  Lógica causal (se–então–porque):
  SE [insumo/atividade principal]
  ENTÃO [resultado intermediário esperado]
  PORQUE [mecanismo causal que conecta os dois — este é o elo
         fundamental; se você não consegue escrever o porque,
         marque [suposição] e explique por que é plausível]

  Riscos principais: [2-3 riscos concretos, um por frase curta]

  Lacunas de informação: [use [suposição] em cada lacuna]
</caminho>

Repita para os caminhos 2, 3, 4 e 5 (se aplicável).

NÃO use tabelas nesta etapa. NÃO preencha colunas vazias com texto
genérico. Se você não tem base pra um elo causal, marque [suposição]
e explique em uma frase por que a inferência é razoável.

Evite lógicas mágicas (do tipo "oferecer curso → reduzir pobreza"
sem explicar o mecanismo intermediário). Se o mecanismo exige
vários passos intermediários, descreva-os encadeados:
SE A → ENTÃO B → ENTÃO C → ENTÃO impacto.
```

**Output esperado:** 3-5 blocos `<caminho>` numerados, cada um com nome curto, lógica causal se-então-porque explícita, riscos e lacunas marcadas.

### Etapa 4 — Pressupostos, riscos e auditoria de equidade

**Objetivo:** Para cada caminho da Etapa 3, explicitar pressupostos críticos + riscos + resposta institucional possível; ADICIONALMENTE, fazer auditoria estrutural de equidade da lógica causal com 4 perguntas obrigatórias. Esta é a **etapa dedicada à operacionalização da equidade** na skill.

**Prompt sugerido:**

```
Agora vamos auditar cada caminho da Etapa 3. Para cada caminho,
produza DUAS subseções.

SUBSEÇÃO A — PRESSUPOSTOS E RISCOS:

Para cada caminho, liste:

<pressupostos caminho_id="N">
  1. [Pressuposto 1] — verificável por: [como verificaria]
     risco se falhar: [consequência]
     resposta institucional: [o que a equipe pode fazer]
  2. [Pressuposto 2] — verificável por: ...
  3. [Pressuposto 3] — verificável por: ...
</pressupostos>

Use linguagem direta, sem jargão. Use [suposição] quando a
verificação depende de julgamento técnico sem base empírica.

SUBSEÇÃO B — AUDITORIA DE EQUIDADE:

Esta subseção é OBRIGATÓRIA e tem 4 perguntas a serem respondidas
explicitamente para cada caminho. Não pule nenhuma. Seja concreto.

<auditoria_equidade caminho_id="N">
  (a) Quem ganha e quem perde neste caminho?
      Nomeie grupos concretos, não generalidades. Exemplos:
      - "Famílias com mãe trabalhadora ganham acesso; mães
         adolescentes solteiras perdem porque o caminho pressupõe
         disponibilidade de acompanhamento familiar".
      - "Escolas da capital ganham capacidade técnica; escolas
         rurais ficam fora do alcance imediato do caminho".

  (b) Quais pressupostos escondem relação de poder estrutural?
      Liste os pressupostos da Subseção A que, quando examinados,
      dependem de relações desiguais de poder. Exemplos:
      - "Assumir que a família adere depende de tempo, informação
         e recursos que não são distribuídos igualmente".
      - "Assumir que o gestor municipal coopera depende de relação
         partidária favorável com o gestor estadual".

  (c) Quais grupos vulnerabilizados esta ToC ignora ou trata como
      beneficiários passivos (em vez de agentes)?
      Nomeie grupos. Se a ToC trata pessoas como "recebedoras do
      benefício" sem agência, diga isso explicitamente.

  (d) Este caminho reproduz viés de paternalismo (decidir pelo
      outro sem consulta) ou de postergação de desigualdades
      ("primeiro resolvemos o geral, depois pensamos nas
      desigualdades")? Se sim, onde.
</auditoria_equidade>

REGRA FINAL DA ETAPA 4:

Se a auditoria de equidade identificar que os caminhos da Etapa 3
são ESTRUTURALMENTE viesados (ex: todos os caminhos assumem algo
que exclui sistematicamente um grupo afetado), você DEVE
recomendar explicitamente retorno à Etapa 3 para regenerar ou
ajustar os caminhos, ANTES de prosseguir para a Etapa 5.

Termine a resposta com:

<recomendacao_ajuste>
  prosseguir | retornar_etapa_3
</recomendacao_ajuste>

Se for "retornar_etapa_3", explique em 3-5 linhas o que precisa
mudar nos caminhos antes de prosseguir.
```

**Output esperado:** Para cada caminho, subseção A (pressupostos + riscos + resposta) + subseção B (`<auditoria_equidade>` com as 4 perguntas respondidas) + `<recomendacao_ajuste>` ao final.

### Etapa 5 — Síntese ToC + kit de validação coletiva *(CHECKPOINT HUMANO FORTE)*

**Objetivo:** Consolidar a ToC em artefato final (texto corrido + tabela do livro) + produzir o kit de facilitação para reunião de validação coletiva (pauta, perguntas críticas, versão acessível, roteiro de dissensos). Termina com trigger explícito de checkpoint humano obrigatório.

**Prompt sugerido:**

```
Agora vamos consolidar a ToC e preparar o material pra validação
coletiva. Produza 3 partes, nesta ordem:

PARTE 1 — SÍNTESE DA TOC:

1a. <toc_texto_corrido>
    Um parágrafo articulando insumos → atividades → resultados
    intermediários → impactos em uma única cadeia lógica, com
    rastreabilidade (cite os IDs dos caminhos quando apropriado).
    Use linguagem técnica mas acessível a gestores.
    </toc_texto_corrido>

1b. <toc_tabela>
    Tabela Markdown no formato do livro, COLUNAS EXATAMENTE ASSIM:

    | Insumos | Atividades | Resultados intermediários | Impactos | Pressupostos críticos | Indicadores-chave iniciais | Riscos |

    Cada célula cita entre parênteses os identificadores do caminho
    ou objetivo de origem (ex: "capacitação de professores (C2)").
    Indicadores-chave iniciais são pares resultado–indicador de alto
    nível (máx 3-4 linhas, não detalhe — detalhamento é nas Etapas
    6-7). Fiel ao Caso 6 Etapa 6 do livro.
    </toc_tabela>

PARTE 2 — KIT DE VALIDAÇÃO COLETIVA:

2a. <pauta_reuniao duracao="90min">
    Reunião de validação coletiva da ToC. Estrutura:

    1. Abertura e contextualização (10 min)
    2. Apresentação da ToC consolidada (15 min)
    3. Debate estruturado pelas perguntas críticas (50 min)
    4. Consolidação de dissensos e decisões de ajuste (10 min)
    5. Próximos passos e checkpoints (5 min)

    Inclua sugestões de quem convidar (perfis, não nomes) e material
    de preparação a enviar antes.
    </pauta_reuniao>

2b. <perguntas_criticas>
    Entre 5 e 8 perguntas críticas para jogar no grupo, focadas nos
    PRESSUPOSTOS MAIS FRÁGEIS e nos GRUPOS AUSENTES identificados
    na Etapa 2 e 4. Cada pergunta deve ser:
    - Específica (não "o que vocês acham?")
    - Focada em uma decisão ou um pressuposto
    - Fácil de responder por alguém não-técnico

    Exemplo: "A ToC assume que a família está disponível para
    acompanhar o/a estudante nas buscas ativas. Esse pressuposto
    vale para 100% dos estudantes-alvo ou só para um subgrupo?
    Quem fica fora?"
    </perguntas_criticas>

2c. <versao_acessivel>
    Versão da ToC em linguagem acessível para stakeholders
    não-técnicos (nível de leitura ~8ª série). Frases curtas,
    sem jargão de M&A, exemplos concretos. Máximo 300 palavras.
    Estrutura sugerida:
      - Qual é o problema que queremos resolver?
      - O que queremos que mude?
      - O que vamos fazer?
      - O que precisa ser verdade pra isso funcionar?
      - Como vamos saber se funcionou?
    </versao_acessivel>

2d. <roteiro_dissensos>
    Template com 4 colunas para registrar o debate da reunião:

    | Ponto debatido | Posição majoritária | Dissenso registrado | Decisão de ajuste |

    Esta tabela é entregue em branco — é instrumento pra o
    facilitador humano preencher durante a reunião.
    </roteiro_dissensos>

PARTE 3 — TRIGGER DE CHECKPOINT HUMANO:

Termine a resposta com este bloco EXATO (copie palavra por palavra):

---

**⛔ PARE AQUI. Esta é a parte mais importante do método.**

A Teoria da Mudança NÃO está pronta até ser validada coletivamente
com stakeholders. O kit acima existe pra você rodar essa validação.

Antes de prosseguir para a Etapa 6 (derivação de indicadores),
você PRECISA:

1. Rodar a reunião de validação usando a pauta, as perguntas
   críticas e a versão acessível produzidas na Parte 2.
2. Registrar dissensos e decisões de ajuste no roteiro.
3. Se a ToC mudou substancialmente após o debate, VOLTAR para
   a Etapa 3 e regenerar os caminhos causais antes de prosseguir.
4. Só avançar para a Etapa 6 quando a ToC refletir o consenso
   (ou o dissenso registrado) do grupo validador.

Pular este checkpoint é o jeito mais rápido de produzir fichas
técnicas de indicadores sobre uma ToC que a equipe vai rejeitar
depois. Retrabalho garantido — e, pior, legitimidade perdida.

Ver `references/variantes.md` se este é um caso de **revisão de
ToC existente** em vez de criação do zero.

---
```

**Output esperado:** ToC consolidada (texto + tabela) + kit completo (pauta, perguntas críticas, versão acessível, roteiro de dissensos em branco) + trigger de checkpoint explícito no formato exato acima.

### Etapa 6 — Derivação de indicadores por nível lógico

**Objetivo:** A partir da ToC **já validada coletivamente** na Etapa 5, gerar 2-4 indicadores candidatos por objetivo no nível lógico apropriado, com desagregações obrigatórias por grupo vulnerabilizado. Fiel ao Caso 7 Etapas 2-3 do livro, com equity hook forte.

**Prompt sugerido:**

```
A ToC foi validada coletivamente? Se não, volte para a Etapa 5
e rode o checkpoint antes de prosseguir.

Se sim, vamos derivar os indicadores. Para cada objetivo da ToC
validada, produza:

Passo 1 — Classificação em nível lógico:
  Classifique o objetivo em UM destes níveis:
  - insumo (recursos, financiamento, pessoal)
  - processo (atividades realizadas)
  - produto (entregas imediatas)
  - resultado intermediário (mudança nos beneficiários direto
    da intervenção, prazo médio)
  - impacto (mudança na condição social mais ampla, prazo longo)

Passo 2 — Geração de 2 a 4 indicadores candidatos:
  Cada indicador deve estar NO MESMO NÍVEL LÓGICO do objetivo.
  Quando fizer sentido, adicione 1 indicador complementar no
  nível seguinte para triangulação (ex: indicador de produto
  que ajuda a monitorar se o resultado intermediário vai
  acontecer).

Formato de saída — tabela Markdown:

| Objetivo | Nível lógico | Indicador | Tipo | Definição simples | Fórmula (numerador/denominador) | Unidade | Fonte de dados | Periodicidade | Desagregações mínimas |

REGRAS OBRIGATÓRIAS:

(a) Tipo = "quantitativo" | "qualitativo"

(b) Desagregações mínimas: escolha entre os 6 eixos abaixo,
    obrigatoriamente. Justifique quando excluir alguma:
    - território
    - raça/cor
    - gênero
    - renda
    - pessoa com deficiência
    - faixa etária

    Para cada indicador, a coluna "Desagregações mínimas" deve
    listar quais eixos se aplicam. Se algum NÃO se aplica,
    inclua uma nota "(exclui: <eixo> porque <motivo em 1 frase>)".
    REGRA DURA: "não se aplica" sozinho não serve. Precisa ter
    motivo.

(c) Fórmula: quando for quantitativo, escreva numerador/denominador
    explícitos. Ex: "n° de estudantes contatados pela busca ativa /
    n° de estudantes em risco identificados no semestre × 100".
    Quando for qualitativo, descreva o método de coleta em 1 frase.

(d) Fonte de dados: seja específico. Não "sistema de gestão" —
    sim "Censo Escolar (INEP)" ou "Sistema Municipal de Registro
    Escolar". Use "não encontrado" quando a fonte ainda precisa
    ser definida.

(e) Se não conseguir propor indicador para um nível lógico (ex:
    impacto de longuíssimo prazo sem métrica viável), escreva
    "não encontrado" + explicação da dificuldade + sugestão
    de indicador-proxy.

Repita a tabela para cada objetivo da ToC validada.
```

**Output esperado:** Tabela de indicadores candidatos por objetivo, com 2-4 indicadores por linha, classificação de nível lógico, desagregações obrigatórias justificadas (não cosméticas) e fontes de dados específicas.

### Etapa 7 — Triagem, fichas técnicas e autoverificação

**Objetivo:** Três sub-tarefas: (a) triagem dos indicadores candidatos da Etapa 6 por 5 critérios de qualidade com notas 0/1/2; (b) fichas técnicas completas dos priorizados; (c) autoverificação estruturada contra os 6 princípios invioláveis. Fiel ao Caso 7 Etapas 4-5 do livro + autoverificação padrão do repo.

**Prompt sugerido:**

```
Agora a etapa final. Três sub-tarefas obrigatórias.

SUB-TAREFA 1 — TRIAGEM POR QUALIDADE E VIABILIDADE:

Para cada indicador candidato da Etapa 6, atribua uma nota
(0 = fraco, 1 = médio, 2 = forte) em CADA UM dos 5 critérios:

- Relevância ao objetivo
- Clareza de definição
- Mensurabilidade com os dados disponíveis
- Comparabilidade ao longo do tempo
- Custo/viabilidade de coleta

Produza tabela:

| Indicador | Relevância | Clareza | Mensurabilidade | Comparabilidade | Custo/Viabilidade | Total | Decisão |

Decisão = PRIORIZAR | REVER | DESCARTAR
- PRIORIZAR: soma ≥ 7
- REVER: soma 4-6, explicar em 1 frase o que rever
- DESCARTAR: soma ≤ 3 ou qualquer nota 0 em um critério crítico
  (relevância, clareza)

Para cada linha com nota 0 em qualquer critério, explique em 1
frase o motivo do corte. Elimine redundâncias (indicadores que
medem a mesma coisa com nomes diferentes — escolha o mais claro
e descarte os outros).

SUB-TAREFA 2 — FICHAS TÉCNICAS DOS PRIORIZADOS:

Para cada indicador PRIORIZADO, produza a ficha técnica completa:

<ficha_tecnica id="IND_XXX">
  Nome: [nome curto, inequívoco]
  Objetivo ligado: [referência à ToC]
  Nível lógico: [insumo/processo/produto/resultado intermediário/impacto]
  Definição operacional: [UMA frase, sem ambiguidade]
  Fórmula: [numerador/denominador explícitos ou método de coleta qualitativa]
  Unidade: [unidade de medida, ex: "%", "pessoas", "eventos"]
  Fonte de verificação: [sistema ou método específico]
  Linha de base: [valor se conhecido, "não encontrado" se não]
  Meta inicial: [valor com [suposição] se for referência inicial]
  Periodicidade: [mensal, trimestral, anual, bienal]
  Desagregações obrigatórias: [listar os eixos + justificativa das exclusões]
  Responsável pela atualização: [área, função ou parceiro]
  Observações sobre vieses e limites éticos:
    Campo OBRIGATÓRIO. Pense sobre riscos de uso indevido do
    indicador. Exemplos:
    - "Indicador de matrícula de pessoas com deficiência pode
       incentivar matrícula sem garantir permanência — monitorar
       junto com indicador de permanência."
    - "Taxa de evasão por raça/cor pode expor estudantes negros
       a estigmatização se usada sem contexto histórico de
       desigualdade estrutural."
    Se você não consegue pensar em um risco, o indicador
    provavelmente não foi examinado de verdade. Pare e pense.
</ficha_tecnica>

SUB-TAREFA 3 — AUTOVERIFICAÇÃO ESTRUTURADA:

Produza tabela de autoverificação contra os 6 princípios invioláveis:

| Princípio | Cumprido? (Sim/Parcial/Não) | Evidência da verificação | Ajustes necessários |

Uma linha por princípio. Para cada linha:
- Cite pelo menos um trecho CONCRETO da ToC ou das fichas
  técnicas que sustenta o "cumprido".
- "Parcial" é resposta válida e até desejável quando há espaço
  pra melhoria — indique o que está ok e o que ainda precisa
  ajuste.
- Se detectar violação, proponha a correção específica.

Princípio 5 (lente de equidade) MERECE atenção especial: cite
exatamente onde na ToC e nos indicadores a equidade foi
operacionalizada concretamente (não só mencionada).

FECHAMENTO:

Termine com esta mensagem (copie verbatim):

"A ToC, o kit de reunião, os indicadores e as fichas técnicas
estão prontos para revisão humana final. Antes de publicar
ou repassar a stakeholders, rode o checklist completo em
references/checklist.md. Especial atenção à regra de ouro
no final do checklist — se itens críticos não podem ser
marcados, a saída é rascunho até corrigir."
```

**Output esperado:** Três partes — tabela de triagem com notas e decisões + fichas técnicas completas dos priorizados (com campo de observações sobre vieses preenchido substantivamente) + relatório de autoverificação estruturado cobrindo os 6 princípios.

## Checkpoints de validação humana

Pontos onde o humano DEVE revisar antes de avançar para a próxima etapa. Pular estes checkpoints é o caminho direto pro **AI work slop**.

- **Após Etapa 2 (Estruturação de insumos)** — Verifique: a lista de objetivos padronizados captura o que a política realmente pretende? Os problemas priorizados refletem a realidade do contexto? Se o modo foi `disperso`, a extração a partir dos insumos brutos foi fiel aos originais ou inventou coisas? Os grupos ausentes nomeados em `<equidade_etapa2>` batem com sua percepção?

- **Após Etapa 5 (Síntese + kit) — CHECKPOINT FORTE E OBRIGATÓRIO:** A reunião de validação coletiva com stakeholders DEVE acontecer antes de prosseguir pra Etapa 6. Não é sugestão, é parte do método. Verifique: a ToC consolidada reflete o debate? Dissensos foram registrados no roteiro? Decisões de ajuste foram documentadas? Se a ToC mudou substancialmente, retorne à Etapa 3. **Pular este checkpoint = AI work slop com consequências reais sobre pessoas.** Para revisão de ToC existente, ver `references/variantes.md`.

- **Após Etapa 7 (Fichas técnicas + autoverificação)** — Verifique: a triagem dos indicadores é defensável (as notas refletem o que você sabe do contexto)? As fichas técnicas têm fórmulas claras, fontes específicas, linha de base registrada ou "não encontrado"? O campo "observações sobre vieses" das fichas foi preenchido substantivamente (não copiou o exemplo)? O relatório de autoverificação apontou pontos reais de fragilidade? Rode o checklist completo em `references/checklist.md` antes de publicar.

**Regra geral:** Se você não teve tempo de validar um checkpoint, não prossiga. Use a saída da etapa anterior como rascunho interno até a validação ser feita.

## Falhas comuns

Anti-patterns específicos desta skill que o modelo (ou o humano confiando no modelo sem checar) pode cometer:

1. **Confusão de níveis lógicos.** O modelo mistura atividade com produto ("capacitar professores" como resultado) ou produto com impacto ("1000 alunos atendidos" como impacto de programa de qualidade educacional). O erro propaga pros indicadores e inviabiliza o monitoramento. *Mitigação:* Etapa 3 exige se–então–porque explícito; Etapa 6 exige classificação do objetivo e indicador no mesmo nível lógico, com justificativa quando for nível adjacente.

2. **Caminhos causais mágicos.** A ToC pula de insumo direto pra impacto sem explicar o mecanismo intermediário ("oferecer curso" → "reduzir pobreza"). O modelo preenche a lacuna com retórica. *Mitigação:* Etapa 3 força 3-5 caminhos alternativos com lógica causal explícita no formato se-então-porque; Etapa 4 obriga pressupostos nomeados que revelam onde estão os saltos lógicos.

3. **Pressupostos invisíveis e ingênuos.** A ToC assume que "as famílias vão aderir", "o sistema municipal vai aceitar", "o orçamento vai sair" — sem nomear como pressupostos críticos que podem falhar. *Mitigação:* Etapa 4 obriga listar pressupostos + verificação possível + riscos + resposta institucional por caminho. A auditoria de equidade da mesma etapa força o exame de pressupostos que escondem relações de poder.

4. **Indicador desalinhado com nível lógico do objetivo.** O objetivo é de resultado intermediário ("melhorar aprendizagem") e o indicador proposto é de produto ("n° de aulas ministradas") — fácil de medir, não mede o que importa. *Mitigação:* Etapa 6 exige classificação explícita do objetivo em um dos 5 níveis lógicos e indicador no mesmo nível, justificado quando for adjacente.

5. **Desagregação cosmética.** Fichas técnicas listam "desagregar por gênero, raça, território" sem pensar se faz sentido pro indicador específico, e depois ninguém coleta. *Mitigação:* Etapa 6 exige justificativa por desagregação excluída; Etapa 7 inclui campo obrigatório "observações sobre vieses" que força exame dos riscos de uso indevido do indicador, incluindo riscos de desagregação mal-pensada.

6. **ToC aceita sem debate coletivo.** O usuário roda a skill em isolamento, recebe a ToC polida da Etapa 5 e publica sem validação com stakeholders. O kit de reunião fica no arquivo, a legitimidade evapora. *Mitigação:* Etapa 5 termina com trigger de checkpoint obrigatório + princípio inviolável #6 + esta falha comum documentada. A skill **trata** a validação coletiva como parte do método, não como passo opcional.

## Arquivos complementares

- **`references/exemplos.md`** — Uma execução completa desta skill em um caso realista: desenho de um programa municipal de redução de evasão no ensino médio público. Mostra input bruto (modo `disperso`), extração de objetivos, 3 caminhos causais alternativos (conservador, intermediário, ambicioso), auditoria de equidade que força ajuste nos caminhos, ToC consolidada, kit de reunião, indicadores priorizados com desagregações e fichas técnicas. Todo o conteúdo é fictício — disclaimer no topo.

- **`references/variantes.md`** — 4 adaptações do workflow base: (1) revisão de ToC existente, (2) ToC para OSC pequena sem equipe de M&A, (3) ToC para projeto com doador internacional (LogFrame/Kellogg esperados), (4) ToC de portfólio multi-programa.

- **`references/checklist.md`** — Checklist de validação humana em duas seções (técnica + equidade) + regra de ouro final. Use DEPOIS da Etapa 7, antes de entregar ao stakeholder final. Se itens críticos não podem ser marcados, a ToC e os indicadores viram rascunho até corrigir.

---

**Cadeia com outras skills do repo:**
- **Upstream (input para esta skill):** `evidence-synthesis` (síntese do diagnóstico) ou `qualitative-analysis` (percepções de stakeholders) alimentam os insumos da Etapa 2.
- **Downstream (consome saída desta skill):** `project-structuring` (usa os objetivos + ToC validada pra derivar entregáveis e cronograma) e `strategic-planning` (usa a ToC + indicadores pra derivar KPIs estratégicos e OPIs operacionais).

---

*Baseada nos casos de uso 6 ("Construção de Teoria da Mudança") e 7 ("Definição de Indicadores de Monitoramento") do livro* Inteligência Artificial para Impacto Social *(Castro, 2025), fundidos em uma skill única. Modernizada com práticas atuais de prompting (XML tags, autoverificação estruturada, lente de equidade operacional em etapa dedicada, checkpoint humano forte, manejo explícito de "não sei").*
