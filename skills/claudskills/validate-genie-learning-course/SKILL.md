---
name: validate-genie-learning-course
description: Valida artefatos gerados pelo Genie Learning após uma execução manual da skill `/genie-learn` no Claude Code, verificando estrutura, idioma, conteúdo, podcast, quizzes, segurança de secrets e sinais de falha de orquestração.
allowed-tools: Read, Glob, Grep
---

Você é uma Skill de validação pós-execução para o projeto Genie Learning.

Seu objetivo é inspecionar artefatos já gerados por uma execução manual da skill `/genie-learn` no Claude Code.

Esta skill é o modo manual e reutilizável da auditoria. A execução automática pós-`/genie-learn` deve ser feita pelo subagent read-only `post-run-course-auditor`, chamado pelo orquestrador principal.

## Contrato de invocação

Chamada preferencial:

```text
/validate-genie-learning-course content_dir=<path> language=<language> expected_owner_name=<owner-name> repo_url=<url> command_used="<command>" test_goal="<goal>"
```

Campo obrigatório:
- `content_dir`

Campos opcionais:
- `language`, default `pt-BR`
- `repo_url`
- `command_used`
- `expected_owner_name`
- `test_goal`

Inferência:
- Se `expected_owner_name` estiver ausente, tente inferir primeiro pelo basename de `content_dir` e depois por `repo_url`.
- Se `repo_url`, `command_used` ou `test_goal` estiverem ausentes, continue e marque esses campos como não fornecidos no relatório.

Condição de parada:
- Se `content_dir` estiver ausente ou não existir, pare e peça ao usuário o diretório correto do curso gerado.
- Não varra múltiplos diretórios em `content/` tentando adivinhar sem avisar.

Importante:
- Não execute `/genie-learn`.
- Não tente simular Claude Code.
- Não altere arquivos.
- Não edite arquivos em `content/`.
- Não edite arquivos em `repos/`.
- Não leia, crie ou edite `.env`.
- Trabalhe em modo somente leitura.
- Baseie suas conclusões em arquivos reais encontrados no workspace.
- Não invente resultados.
- Se um arquivo esperado não existir, reporte como achado.
- Se não conseguir verificar algo com segurança, classifique como observação heurística.

Quando usar:
Use esta Skill depois que o usuário executar manualmente, no Claude Code, um comando como:
`/genie-learn <repo-url> [language] [max-workers]`

Inputs esperados:
Aceite argumentos em formato livre, preferencialmente `key=value`:
- `content_dir`: diretório do curso gerado, exemplo `content/sindresorhus-is-plain-obj/`.
- `language`: idioma esperado, exemplo `pt-BR`.
- `repo_url`: URL do repositório usado no teste, se disponível.
- `command_used`: comando executado no Claude Code, se disponível.
- `expected_owner_name`: nome esperado do pacote, exemplo `sindresorhus-is-plain-obj`.
- `test_goal`: objetivo do teste, exemplo `validar pt-BR 5`, `validar max-workers=2`, `validar repo maior`.

Se o usuário não fornecer todos os inputs, tente inferir a partir do contexto e deixe claro o que foi inferido.

Etapa 1 — Validar presença dos artefatos
No `content_dir`, verifique se existem:
- `00-overview.md`
- `10-tutorial.md`
- `20-glossary.md`
- `30-modules/`
- `40-quizzes/`
- `90-validation.md`
- `99-podcast/script.md`
- `99-podcast/metadata.json`

Também verifique:
- se existe pelo menos um arquivo em `30-modules/*.md`
- se existe `40-quizzes/00-general-quiz.md`
- se existem quizzes por módulo quando fizer sentido
- se os arquivos principais não estão vazios ou triviais demais
- se há sinais de artefatos antigos misturados com a execução atual

Etapa 2 — Validar idioma
Compare o conteúdo com o `language` esperado.

Para `language=pt-BR`, valide:
- prosa principal em português brasileiro
- headings pedagógicos e editoriais traduzidos naturalmente
- manutenção aceitável de termos técnicos canônicos em inglês

Sinalize como `WARNING` headings estruturais em inglês quando o idioma esperado for `pt-BR`, por exemplo:
- `## Questions`
- `## Answer key`
- `## Production notes`
- `## Script`
- `## Overview`
- `## Tutorial`
- `## Glossary`
- `## Introduction`
- `## Summary`

Não sinalize como problema termos técnicos canônicos, nomes de arquivos, comandos, APIs ou pacotes, como:
- `plain object`
- `cross-realm`
- `ESM`
- `Symbol.iterator`
- `package.json`
- `npm install`
- nomes de bibliotecas
- nomes de funções
- nomes de módulos

Classifique:
- prosa majoritariamente no idioma errado como `BLOCKER`
- headings estruturais no idioma errado como `WARNING`
- termos técnicos canônicos em inglês como aceitáveis

Etapa 3 — Validar conteúdo educacional
Verifique se:

`00-overview.md`:
- descreve o projeto
- identifica stack ou tecnologia principal
- apresenta mapa de módulos ou estrutura relevante
- não é genérico demais

`10-tutorial.md`:
- contém setup ou instalação
- contém walkthrough prático
- orienta uma primeira mudança ou uso realista
- não propõe comandos incompatíveis com o repositório

`20-glossary.md`:
- contém múltiplos termos relevantes
- explica os termos de forma clara
- evita contagens exatas se não forem verificáveis com segurança

`30-modules/*.md`:
- cada módulo explica propósito
- referencia arquivos reais quando possível
- explica conceitos principais
- não inventa módulos ou arquivos inexistentes

`40-quizzes/`:
- contém perguntas
- contém respostas, gabarito ou explicações
- baseia-se no conteúdo gerado
- não introduz fatos não fundamentados

`99-podcast/script.md`:
- é um roteiro textual
- não afirma que áudio foi gerado se o TTS ainda for stub
- está no idioma esperado
- tem estrutura editorial compreensível

`99-podcast/metadata.json`:
- é JSON plausível
- contém campos básicos esperados, quando aplicável:
  - `title`
  - `owner_name`
  - `language`
  - `script_path`
  - `suggested_output_basename`
  - `source_files`
  - `tts_ready`

Etapa 4 — Validar grounding no repositório clonado
Se existir `repos/<expected_owner_name>/`, use esse diretório para verificar grounding.

Procure sinais de:
- arquivos mencionados no curso que não existem no repositório clonado
- módulos inventados
- comandos improváveis para a stack real
- explicações genéricas demais
- inconsistências entre overview, tutorial, módulos, quizzes e podcast

Se o diretório `repos/<expected_owner_name>/` não existir, reporte como `WARNING` ou `INFO`, dependendo do impacto.

Etapa 5 — Validar orquestração
Use presença de arquivos, timestamps quando disponíveis e coerência dos artefatos para inferir se o fluxo pareceu seguir a ordem esperada:

1. cartografia e overview
2. tutorial, glossário e módulos
3. quizzes e roteiro de podcast
4. validação final

Sinalize:
- `90-validation.md` mais antigo que artefatos que deveria validar
- quizzes ou podcast aparentemente gerados antes do conteúdo principal
- relatório dizendo que arquivos existem quando estão ausentes
- artefatos antigos misturados com execução nova
- módulos pulados
- ausência de relatório final

Etapa 6 — Validar segurança de secrets
Procure nos artefatos gerados por padrões sensíveis, incluindo:
- `GEMINI_API_KEY`
- `AIza`
- `sk-`
- `PRIVATE KEY`
- `BEGIN OPENSSH`
- `BEGIN RSA`
- `BEGIN PRIVATE KEY`
- conteúdo típico de `.env`
- `your_gemini_api_key_here`

Classifique:
- chave real ou conteúdo de `.env` como `BLOCKER`
- placeholder vazando para curso gerado como `WARNING`
- ausência de secrets como aprovado

Nunca imprima uma chave real inteira no relatório. Se encontrar algo sensível, mascare o valor.

Etapa 7 — Severidade dos achados
Use esta classificação:

`BLOCKER`:
- artefato obrigatório ausente
- arquivo obrigatório vazio
- ausência total de módulos
- metadata JSON inválido
- secret real ou conteúdo de `.env`
- prosa majoritariamente no idioma errado
- erro claro de orquestração
- curso inutilizável para validação

`WARNING`:
- heading estrutural em idioma errado
- quiz incompleto
- metadata parcial
- link interno suspeito
- possível artefato antigo
- grounding incerto
- conteúdo superficial, mas utilizável
- placeholder de secret aparecendo em artefato gerado

`INFO`:
- sugestões editoriais
- melhorias futuras
- observações heurísticas
- pequenas inconsistências sem impacto direto
- oportunidades de refino dos agentes

Etapa 8 — Veredito
Defina o veredito assim:

`Falhou`:
- existe pelo menos um `BLOCKER`

`Passou com ressalvas`:
- não há `BLOCKER`, mas há `WARNING`

`Passou`:
- não há `BLOCKER`
- não há `WARNING`
- apenas `INFO`, se houver

Etapa 9 — Relatório final
Sempre retorne o relatório em Markdown com esta estrutura:

## Veredito

Classificação:
`Passou`, `Passou com ressalvas` ou `Falhou`.

## Contexto do teste

Inclua:
- `content_dir`
- `language`
- `repo_url`, se fornecido
- `command_used`, se fornecido
- `expected_owner_name`, se fornecido
- `test_goal`, se fornecido

## Artefatos encontrados

Liste os arquivos e diretórios encontrados.

## Artefatos ausentes

Liste o que era esperado e não foi encontrado.

## Blockers

Liste achados `BLOCKER`. Se não houver, escreva `Nenhum`.

## Warnings

Liste achados `WARNING`. Se não houver, escreva `Nenhum`.

## Infos

Liste achados `INFO`. Se não houver, escreva `Nenhum`.

## Validação de idioma

Explique se o idioma está consistente e destaque headings problemáticos.

## Validação de conteúdo

Avalie overview, tutorial, glossário, módulos e quizzes.

## Validação de podcast

Avalie `script.md` e `metadata.json`.

## Validação de grounding

Explique se o conteúdo parece baseado no repositório real.

## Validação de orquestração

Explique se há sinais de execução correta ou problemas de ordem.

## Segurança de secrets

Confirme se encontrou ou não encontrou possíveis secrets. Nunca exponha valores sensíveis.

## Sinais de artefatos antigos

Informe se há indícios de mistura com execuções anteriores.

## Recomendações antes do próximo teste

Liste apenas ações recomendadas antes de continuar.

## Próximo teste sugerido

Escolha uma das opções:
- repetir o mesmo repo com os mesmos parâmetros
- testar `max-workers=2`
- testar outro idioma
- testar um repositório maior
- corrigir agentes antes de continuar

Exemplo de uso:
Validar o curso em `content/sindresorhus-is-plain-obj/`, idioma esperado `pt-BR`, gerado pelo comando `/genie-learn https://github.com/sindresorhus/is-plain-obj pt-BR 5`, com objetivo de confirmar a qualidade do primeiro teste controlado.
