---
name: cs-customer-escalation
description: Empacota uma escalação para Devs, Produto ou Davidson com contexto completo. Use quando um bug precisa de atenção além do suporte normal, vários clientes reportam o mesmo problema, um cliente está ameaçando cancelar, ou um problema ficou sem resolução além do SLA. / Package an escalation for engineering, product, or leadership with full context. Use when a bug needs engineering attention beyond normal support, multiple customers report the same issue, a customer is threatening to churn, or an issue has sat unresolved past its SLA.
argument-hint: "<resumo do problema> [nome do cliente]"
---

# /cs-customer-escalation

> Se encontrar integrações não configuradas, verifique [CONNECTORS.md](../../CONNECTORS.md).

Empacotar um problema de suporte em um briefing de escalação estruturado para Devs, Produto ou Davidson (liderança). Coleta contexto, estrutura passos de reprodução, avalia impacto de negócio e identifica o alvo de escalação correto.

## Usage

```
/cs-customer-escalation <descrição do problema> [nome do cliente ou conta]
```

Exemplos:
- `/cs-customer-escalation API retornando erros 500 intermitentemente para conta Acme`
- `/cs-customer-escalation Exportação de dados com linhas faltando — 3 clientes reportaram essa semana`
- `/cs-customer-escalation Loop de login SSO afetando todos os clientes Enterprise`
- `/cs-customer-escalation Cliente ameaçando cancelar por falta de feature de audit log`

## Workflow

### 1. Entender o Problema

Analisar o input e determinar:

- **O que está quebrado ou é necessário**: O problema técnico ou de produto central
- **Quem está afetado**: Cliente(s) específico(s), segmento ou todos os usuários
- **Por quanto tempo**: Quando começou? Há quanto tempo o cliente está esperando?
- **O que foi tentado**: Qualquer troubleshooting ou workarounds tentados
- **Por que escalar agora**: O que torna isso necessário além do suporte normal

Usar os critérios "Quando Escalar vs. Tratar no Suporte" abaixo para confirmar que a escalação é warranted.

### 2. Coletar Contexto

Reunir informações relevantes de fontes disponíveis:

- **int-evo-crm** (`/int-evo-crm`): Tickets relacionados, timeline de comunicações, troubleshooting anterior
- **int-evo-crm** (contexto de conta): Detalhes da conta, contatos principais, escalações anteriores
- **discord-get-messages** (`/discord-get-messages`): Discussões internas sobre esse problema, relatos similares de outros clientes
- **int-whatsapp** (`/int-whatsapp`): Discussões em grupos de suporte ou alertas de clientes
- **int-linear-review** (`/int-linear-review`) ou **Linear MCP**: Bug reports ou feature requests relacionados, status de engineering
- **Notion MCP**: Problemas conhecidos ou workarounds, documentação relevante

### 3. Avaliar Impacto de Negócio

Usando as dimensões de impacto abaixo, quantificar:

- **Amplitude**: Quantos clientes/usuários afetados? Crescendo?
- **Profundidade**: Bloqueado vs. inconvenienciado?
- **Duração**: Há quanto tempo está acontecendo?
- **Receita**: ARR em risco? Negociações pendentes afetadas?
- **Pressão de tempo**: Há prazo?

### 4. Determinar Alvo de Escalação

Usando os níveis de escalação abaixo, identificar o alvo correto: Suporte Tier 2, Devs, Produto, Segurança ou Davidson.

### 5. Estruturar Passos de Reprodução (para bugs)

Se o problema é um bug, seguir as boas práticas de passos de reprodução abaixo para documentar repro steps claros com detalhes de ambiente e evidências.

### 6. Gerar Briefing de Escalação

```
## ESCALAÇÃO: [Resumo em uma linha]

**Severidade:** [Crítico / Alto / Médio]
**Time alvo:** [Devs / Produto / Segurança / Davidson]
**Reportado por:** [Seu nome/time]
**Data:** [Data de hoje]

### Impacto
- **Clientes afetados:** [Quem e quantos]
- **Impacto no workflow:** [O que eles não conseguem fazer]
- **Receita em risco:** [Se aplicável]
- **Tempo na fila:** [Há quanto tempo é um problema]

### Descrição do Problema
[Descrição clara e concisa do problema — 3-5 frases]

### O Que Foi Tentado
1. [Passo de troubleshooting e resultado]
2. [Passo de troubleshooting e resultado]
3. [Passo de troubleshooting e resultado]

### Passos de Reprodução
[Se aplicável — seguir o formato abaixo]
1. [Passo]
2. [Passo]
3. [Passo]
Esperado: [X]
Atual: [Y]
Ambiente: [Detalhes]

### Comunicação com o Cliente
- **Última atualização ao cliente:** [Data e o que foi comunicado]
- **Expectativa do cliente:** [O que esperam e para quando]
- **Risco de escalação:** [Vão escalar mais se não resolvido até X?]

### O Que é Necessário
- [Pedido específico — "investigar causa raiz", "priorizar fix",
  "tomar decisão de produto sobre X", "aprovar exceção para Y"]
- **Prazo:** [Quando precisam de resolução ou atualização]

### Contexto de Suporte
- [Tickets relacionados ou links]
- [Threads de discussão interna]
- [Documentação ou logs]
```

### 7. Oferecer Próximos Passos

Após gerar a escalação:
- "Quer que eu poste isso no canal Discord do time alvo?"
- "Devo atualizar o cliente com uma resposta interina?"
- "Quer que eu configure um lembrete de acompanhamento para verificar isso?"
- "Devo redigir uma atualização para o cliente com o status atual?"

---

## Quando Escalar vs. Tratar no Suporte

### Tratar no Suporte Quando:
- O problema tem uma solução documentada ou workaround conhecido
- É um problema de configuração ou setup que você pode resolver
- O cliente precisa de orientação ou treinamento, não de um fix
- O problema é uma limitação conhecida com alternativa documentada
- Tickets similares anteriores foram resolvidos no nível de suporte

### Escalar Quando:
- **Técnico**: Bug confirmado que precisa de correção de código, investigação de infraestrutura necessária, corrupção ou perda de dados
- **Complexidade**: Problema além da capacidade de diagnóstico do suporte, requer acesso que o suporte não tem, envolve implementação customizada
- **Impacto**: Vários clientes afetados, sistema em produção fora do ar, integridade de dados em risco, preocupação de segurança
- **Negócio**: Cliente de alto valor em risco, breach de SLA iminente ou ocorrido, cliente solicitando envolvimento executivo
- **Tempo**: Problema aberto além do SLA, cliente esperando por tempo irrazoável, canais normais de suporte não progredindo
- **Padrão**: Mesmo problema reportado por 3+ clientes, problema recorrente que supostamente foi corrigido, severidade crescente ao longo do tempo

## Níveis de Escalação (Evolution Context)

### Suporte → Suporte Sênior (Escalação Interna)
**De:** Suporte frontline
**Para:** Suporte sênior / especialistas técnicos de suporte
**Quando:** Problema requer investigação mais profunda, conhecimento especializado de produto, ou troubleshooting avançado
**O que incluir:** Resumo do ticket, passos já tentados, contexto do cliente

### Suporte Sênior → Devs (Engineering)
**De:** Suporte sênior
**Para:** Time de Devs (área de produto relevante)
**Quando:** Bug confirmado, problema de infraestrutura, precisa de mudança de código, requer investigação em nível de sistema
**O que incluir:** Passos completos de reprodução, detalhes de ambiente, logs ou mensagens de erro, impacto de negócio, timeline do cliente

### Suporte Sênior → Produto
**De:** Suporte sênior
**Para:** Product management
**Quando:** Gap de feature causando dor ao cliente, decisão de design necessária, workflow não corresponde às expectativas do cliente, necessidades concorrentes de clientes requerem priorização
**O que incluir:** Caso de uso do cliente, impacto de negócio, frequência da solicitação, pressão competitiva (se conhecida)

### Qualquer Nível → Segurança
**De:** Qualquer nível de suporte
**Para:** Time de segurança
**Quando:** Potencial exposição de dados, acesso não autorizado, relatório de vulnerabilidade, preocupação de compliance (LGPD, etc.)
**O que incluir:** O que foi observado, quem/o que está potencialmente afetado, medidas de contenção imediata tomadas, avaliação de urgência
**Nota:** Escalações de segurança ignoram a progressão normal de níveis — escalar imediatamente independente do seu nível

### Qualquer Nível → Davidson (Liderança)
**De:** Qualquer nível (geralmente suporte sênior ou gerente)
**Para:** Davidson
**Quando:** Cliente de alta receita ameaçando cancelar, breach de SLA em conta crítica, decisão cross-funcional necessária, exceção à política necessária, risco de PR ou legal
**O que incluir:** Contexto completo de negócio, receita em risco, o que foi tentado, decisão ou ação específica necessária, prazo

## Avaliação de Impacto de Negócio

Ao escalar, quantificar o impacto onde possível:

### Dimensões de Impacto

| Dimensão | Perguntas a Responder |
|-----------|-------------------|
| **Amplitude** | Quantos clientes/usuários são afetados? Está crescendo? |
| **Profundidade** | Qual é a gravidade do impacto? Bloqueados vs. inconvenienciados? |
| **Duração** | Há quanto tempo está acontecendo? Quando se torna crítico? |
| **Receita** | Qual é o ARR em risco? Há negociações pendentes afetadas? |
| **Reputação** | Pode se tornar público? É um cliente de referência? |
| **Contratual** | SLAs estão sendo violados? Há obrigações contratuais? |

### Resumo de Severidade

- **Crítico**: Produção fora do ar, dados em risco, brecha de segurança, ou vários clientes de alto valor afetados. Precisa de atenção imediata.
- **Alto**: Funcionalidade principal quebrada, cliente-chave bloqueado, SLA em risco. Precisa de atenção no mesmo dia.
- **Médio**: Problema significativo com workaround, impacto importante mas não urgente. Precisa de atenção nessa semana.

## Escrevendo Passos de Reprodução

Bons passos de reprodução são a coisa mais valiosa numa escalação de bug. Seguir essas práticas:

1. **Começar de um estado limpo**: Descrever o ponto de partida (tipo de conta, configuração, permissões)
2. **Ser específico**: "Clicar no botão Exportar no canto superior direito da página Dashboard" não "tentar exportar"
3. **Incluir valores exatos**: Usar inputs específicos, datas, IDs — não "inserir algum dado"
4. **Anotar o ambiente**: Browser, OS, tipo de conta, feature flags, nível de plano
5. **Capturar a frequência**: Sempre reproduzível? Intermitente? Apenas sob certas condições?
6. **Incluir evidências**: Screenshots, mensagens de erro (texto exato), network logs, console output
7. **Anotar o que foi descartado**: "Testado no Chrome e Firefox — mesmo comportamento" "Não é específico da conta — reproduzido na conta de teste"

## Cadência de Acompanhamento Após Escalação

Não escalar e esquecer. Manter a titularidade do relacionamento com o cliente.

| Severidade | Acompanhamento Interno | Atualização ao Cliente |
|----------|-------------------|-----------------|
| **Crítico** | A cada 2 horas | A cada 2-4 horas (ou por SLA) |
| **Alto** | A cada 4 horas | A cada 4-8 horas |
| **Médio** | Diariamente | A cada 1-2 dias úteis |

### Ações de Acompanhamento
- Verificar com o time receptor o progresso
- Atualizar o cliente mesmo sem novas informações ("Ainda investigando — aqui está o que sabemos até agora")
- Ajustar severidade se a situação muda (melhor ou pior)
- Documentar todas as atualizações no ticket para trilha de auditoria
- Fechar o loop quando resolvido: confirmar com o cliente, atualizar rastreamento interno, capturar aprendizados

## De-escalação

Nem toda escalação permanece escalada. De-escalar quando:
- A causa raiz é encontrada e é um problema resolvível pelo suporte
- Um workaround é encontrado que desbloqueia o cliente
- O problema se resolve por conta própria (mas ainda documentar causa raiz)
- Novas informações mudam a avaliação de severidade

Ao de-escalar:
- Notificar o time para o qual escalou
- Atualizar o ticket com a resolução
- Informar o cliente sobre a resolução
- Documentar o que foi aprendido para referência futura

## Boas Práticas de Escalação

1. Sempre quantificar o impacto — escalações vagas são despriorizadas
2. Incluir passos de reprodução para bugs — isso é a coisa #1 que os Devs precisam
3. Ser claro sobre o que você precisa — "investigar" vs. "corrigir" vs. "decidir" são pedidos diferentes
4. Definir e comunicar um prazo — urgência sem prazo é ambígua
5. Manter a titularidade do relacionamento com o cliente mesmo após escalar o problema técnico
6. Acompanhar proativamente — não esperar o time receptor vir até você
7. Documentar tudo — a trilha de escalação é valiosa para detecção de padrões e melhoria de processo
