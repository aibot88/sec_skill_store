---
name: criacao-faq-coordenacao
description: Cria e revisa FAQs institucionais para coordenação de curso com análise criteriosa, rastreabilidade e foco operacional. Use esta skill sempre que o usuário pedir FAQ, perguntas frequentes, guia de atendimento, respostas padrão de secretaria/coordenação, ou transformar normas/procedimentos em linguagem clara e acionável.
---

Esta skill estrutura a elaboração de FAQs com profundidade analítica, evitando respostas superficiais e sem base documental.

## Objetivo da skill

Produzir FAQs que sejam:

- **claras** para o público final;
- **corretas** em relação à norma/procedimento;
- **acionáveis** para atendimento;
- **rastreáveis** (com links de arquivo clicáveis);
- **reutilizáveis** entre coordenação, secretaria e docentes.

## Quando usar

Use quando houver pedido de:

- criação de FAQ do zero;
- revisão/atualização de FAQ existente;
- padronização de respostas frequentes da coordenação;
- conversão de norma em orientação para estudante.

Não use para responder consulta normativa sem verificar os atos. Se houver dúvida sobre artigo, prazo, competência, vigência, alteração/revogação ou conflito entre normas, carregue a skill [`ufms-docs`](../ufms-docs/SKILL.md) e siga seu fluxo.

## Profundidade mínima obrigatória (análise criteriosa)

Antes de redigir o FAQ final, execute estas 7 etapas:

1. **Definir escopo da demanda**
   - Tema central e limites (ex.: regime especial na graduação, não pós-graduação).
   - Período de interesse (importante para vigência).

2. **Mapear público e decisores**
   - Quem pergunta (estudante, docente, secretaria).
   - Quem analisa/decide (coordenação, colegiado, pró-reitoria).

3. **Levantamento de fontes**
   - Ler índice e README(s) relevantes antes dos atos completos.
   - Selecionar normas principais e, se houver, atos alteradores.

4. **Validar vigência e cadeia de alterações**
   - Confirmar se o ato está vigente.
   - Confirmar alterações, retificações, revogações e consolidações.
   - Declarar limite quando não for possível comprovar cadeia completa.

5. **Extrair regras operacionais**
   - Elegibilidade (quem pode solicitar).
   - Condições de aplicação.
   - Prazos e marcos de contagem.
   - Documentos obrigatórios.
   - Fluxo de tramitação (protocolo -> análise -> decisão -> comunicação).
   - Consequências de deferimento e indeferimento.

6. **Identificar pontos de risco de interpretação**
   - Termos ambíguos.
   - Exceções e casos limítrofes.
   - Dependência de norma externa não presente no acervo.

7. **Só então redigir o FAQ final**
   - Linguagem simples, sem perder exatidão normativa.
   - Cada resposta deve orientar o próximo passo prático.

## Matriz obrigatória de rastreabilidade (pergunta -> dispositivo)

Antes de finalizar, monte obrigatoriamente uma matriz com:

- Pergunta da FAQ;
- Regra sintetizada em 1 frase;
- Dispositivo de base (ato + artigo/parágrafo/inciso);
- Trecho-chave da norma (1-2 linhas, quando houver).

Sem essa matriz, a FAQ não deve ser considerada pronta.

## Critérios de completude mínima (Gate de qualidade)

Considere a FAQ **aprovada** somente quando atingir todos os itens abaixo:

1. **Cobertura funcional**: responde quem pode solicitar, condições, prazo, documentos, protocolo, análise/decisão e indeferimento.
2. **Rastreabilidade**: toda resposta normativa aponta base documental.
3. **Acionabilidade**: cada resposta deixa explícito o próximo passo do leitor.
4. **Temporalidade**: vigência e recorte temporal foram verificados (quando aplicável).
5. **Clareza**: sem jargão desnecessário e sem ambiguidade relevante.

Se qualquer item falhar, revisar antes de entregar.

## Estrutura de saída obrigatória

Entregue nesta ordem:

1. **Análise prévia resumida**
   - Escopo
   - Público-alvo
   - Matriz de regras (quem/prazo/documentos/decisão)
   - Matriz de rastreabilidade (pergunta -> dispositivo)
   - Riscos e limites

2. **FAQ final (Markdown)**
   - Use [`references/TEMPLATE_FAQ.md`](references/TEMPLATE_FAQ.md)

3. **Observações de aplicação**
   - O que a coordenação pode customizar localmente (contatos, canais, formulários).

4. **Referências de base**
   - Links clicáveis (Markdown) dos arquivos usados.
   - Referencie diretamente os documentos normativos aplicados (ex.: PDFs), sem incluir `README.md` na lista final de referências.

- Para PDFs, use o **título do PDF** como texto do link (ex.: `[RESOLUÇÃO (COGRAD) n 430_ de 16-12-2021.](caminho/arquivo.pdf)`).
  - Para arquivos não-PDF que forem indispensáveis, use o nome do arquivo como texto do link.

1. **Limites**
   - Lacunas documentais, necessidade de fonte externa, conflitos não resolvidos.

## Destino dos arquivos gerados

Ao salvar entregáveis finais, usar sempre [`docs/faq/`](../../../docs/faq/).

Padrão recomendado de nome:

- [`docs/faq/<TEMA>.md`](../../../docs/faq/)

Não gerar arquivo separado de análise (`ANALISE_<TEMA>.md`). A análise prévia deve aparecer apenas no corpo da resposta, antes do FAQ final.

## Atualização obrigatória do índice de FAQs

Sempre que criar, renomear ou remover uma FAQ em [`docs/faq/`](../../../docs/faq/), atualizar na mesma entrega o arquivo [`docs/faq/README.md`](../../../docs/faq/README.md).

Atualizações mínimas obrigatórias no índice:

- tabela **FAQs por tema**;
- campo `ultima_revisao`;
- seção **Tags sugeridas para indexação**, quando o novo tema introduzir tag nova ou tornar alguma tag obsoleta.

Se a FAQ mudar de nome, tema ou escopo, refletir imediatamente essa alteração no índice para evitar links quebrados e inconsistências de catalogação.

## Regras de redação

- Perguntas em linguagem natural (como o usuário realmente pergunta).
- Respostas entre 3 e 8 linhas, objetivas.
- Quando houver frontmatter com `title`, não repetir o título no corpo do FAQ.
- O `title` do frontmatter deve ser curto e escaneável (preferência: 2 a 5 palavras).
- Evitar contexto redundante no `title` (ex.: "na graduação", "da UFMS", nome completo do curso) quando esse contexto já estiver em `tema` e `Objetivo`.
- Redigir todo o conteúdo final em **português (Brasil)**.
- Aplicar acentuação e ortografia corretamente antes de entregar (incluindo títulos, perguntas, respostas, frontmatter e checklist).
- Destaque prazos em **negrito**.
- Liste documentos e passos em bullets quando aplicável.
- Use condicional explícita: "Se X, então Y".
- Evite frases vagas como "procure o setor responsável" sem indicar próximo passo.
- Inclua, sempre que possível, a linha **Base:** ao final de cada resposta normativa.
- Quando houver dispositivo normativo, prefira citar artigo/parágrafo/inciso de forma completa.

## Revisão editorial obrigatória

Antes da entrega final, fazer uma passada de revisão editorial para garantir:

- consistência de idioma (sem trechos em inglês ou mistura indevida de idiomas);
- acentuação correta (ex.: "coordenacao" -> "coordenação", "analise" -> "análise");
- concordância nominal e verbal;
- pontuação e clareza frasal.

## Checklist de qualidade antes de finalizar

- [ ] A conclusão de cada resposta bate com a fonte?
- [ ] Prazo, marco de contagem e exceções estão claros?
- [ ] O leitor sabe exatamente o que fazer agora?
- [ ] Linguagem sem jargão desnecessário?
- [ ] O texto final está integralmente em português e com acentuação correta?
- [ ] Referências com links clicáveis foram listadas, usando o título do PDF como texto do link quando aplicável e sem `README.md`?
- [ ] Limites e incertezas foram explicitados?
- [ ] A matriz pergunta -> dispositivo foi preenchida?
- [ ] A FAQ passou no Gate de completude mínima?
- [ ] O `docs/faq/README.md` foi atualizado quando houve inclusão, renomeação ou remoção de FAQ?
- [ ] O `title` está curto, claro e sem redundância de contexto?

## Iteração curta obrigatória (teste -> ajuste -> reteste)

Quando esta skill for criada/atualizada, execute um ciclo mínimo:

1. **Teste inicial** com 2-3 prompts realistas de coordenação.
2. **Diagnóstico**: registrar falhas por critério (cobertura, rastreabilidade, acionabilidade, clareza).
3. **Ajuste da skill/templates** para corrigir as falhas.
4. **Reteste** com os mesmos prompts e comparar melhoria.

Formato de registro sugerido:

- Iteração 1 (baseline): pontos fortes, falhas, decisões de ajuste.
- Iteração 2 (após ajuste): o que melhorou, o que falta.

Só considerar a skill pronta quando a iteração 2 atender integralmente o Gate de completude mínima.

## Organização de arquivos

- **Documentos FAQ gerados para uso institucional**: salvar em [`docs/faq/`](../../../docs/faq/) (não misturar com arquivos da skill).

## Recursos da skill

- [`references/TEMPLATE_ANALISE_FAQ.md`](references/TEMPLATE_ANALISE_FAQ.md)
- [`references/TEMPLATE_FAQ.md`](references/TEMPLATE_FAQ.md)
