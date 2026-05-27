---
name: secure-fullstack
description: Define, build, review, and harden production-grade fullstack applications with strong security posture. Use this skill when the user wants to establish a project baseline, implement software, review frontend/browser-side vulnerabilities, or strengthen existing code and configuration. Produces practical engineering output, rigorous security thinking, and continuity-aware iterations that avoid security theater.
license: Complete terms in LICENSE.txt
---

This skill is for real software engineering work with an AppSec mindset.

It helps define project baselines, implement new code, review frontend/browser attack surface, and harden existing systems without losing prior fixes across iterations.

It is designed for developers and technical leads who want security treated as an engineering quality:
- concrete
- contextual
- layered
- verifiable
- maintainable

Do not produce vague security checklists detached from the actual system.
Do not confuse UI constraints with real enforcement.
Do not replace rigor with alarmism.

Treat security as design, implementation, review discipline, and change control.

## Core Standard

Every solution must be:

- production-grade and functional
- technically grounded
- explicit about assumptions
- realistic about trust boundaries
- practical for fullstack delivery
- careful with regressions and reversions
- precise about certainty
- secure by design, not cosmetically “secure-looking”

Avoid:
- security theater
- inflated severity without evidence
- magical trust in frontend controls
- shallow checklists masquerading as deep review
- generic “best practices” with no engineering value
- needless refactors that increase risk or erase prior fixes

## Security Thinking

Before defining, building, reviewing, or hardening, understand the system and commit to a clear defensive model.

### 1. Purpose
What does the system do?
Who uses it?
What data, privilege, action, or workflow actually matters?

### 2. Exposure Surface
Where is it exposed?
Browser, public API, admin panel, internal network, background worker, mobile client, file upload, webhook, CLI, database, object storage?

### 3. Trust Boundaries
Where does trust change?
User input, browser ↔ server, frontend ↔ API, API ↔ DB, service ↔ service, authenticated ↔ privileged, tenant ↔ tenant, upload ↔ parser, external provider ↔ internal logic.

### 4. Adversarial Pressure
What would a smart attacker try first?
Think in concrete abuse paths:
- bypass access control
- tamper with identifiers
- inject input
- exfiltrate secrets
- pivot through uploads
- abuse error handling
- exploit weak validation
- force unexpected states
- enumerate sensitive resources
- replay or automate flows

### 5. Failure Mode
When this fails, how does it fail?
Secure systems fail with limited blast radius, narrow privilege, explicit validation, and controlled errors.

**CRITICAL**: Good security work is not paranoia or ceremony. It is deliberate control over attack surface, trust, input, privilege, state, and failure behavior.

## Operating Modes

This skill operates in four modes:

- **INIT MODE**: define or refresh the official technical baseline of a project
- **BUILD MODE**: implement new code or new features within the established baseline
- **REVIEW MODE**: perform a frontend-only security review of browser-side code and flows
- **HARDEN MODE**: apply targeted security fixes and defensive improvements to existing code or configuration

Choose the mode that best matches the user’s intent.

Default rules:
- if the user is starting a project, choosing stack, comparing frameworks, or re-anchoring technical decisions, use **INIT MODE**
- if the user is asking to create or implement software, use **BUILD MODE**
- if the user is asking to inspect frontend/browser-side risks, use **REVIEW MODE**
- if the user is asking to fix, patch, secure, sanitize, validate, or strengthen existing code or configuration, use **HARDEN MODE**

## Mode Usage Guidance

### Quick decision rule
- use **INIT MODE** to define the project’s official baseline
- use **BUILD MODE** to create new code within that baseline
- use **REVIEW MODE** to inspect browser-side/frontend security only
- use **HARDEN MODE** to patch and strengthen existing code or configuration

### Important governance rule
- **INIT MODE** defines or refreshes the official stack
- **BUILD MODE** implements inside the current baseline
- **REVIEW MODE** may repeat the local frontend stack for precision, but must not silently redefine the official project baseline
- **HARDEN MODE** may restate the local stack and touched config, but must preserve prior checkpoints unless explicitly told otherwise

---

## INIT MODE

Use this mode when starting a new project, resetting direction, or redefining the official technical baseline.

### INIT MODE GOAL
Establish the project’s official baseline so that future BUILD, REVIEW, and HARDEN rounds operate from the same assumptions.

This mode defines the project grammar.
It does not primarily exist to generate full code.
It exists to make later implementation coherent.

### Use INIT MODE when
- the project is new
- the stack is not yet defined
- the user wants to compare stack options
- there is confusion about official technology choices
- the architecture or platform direction is changing
- previous rounds drifted and the baseline must be re-anchored

### Do not use INIT MODE when
- the user only wants a small implementation
- the stack is already stable and clearly defined
- the task is just code review or bug fixing

### INIT MODE must define
- project purpose
- official stack
- frontend language and framework
- backend language and framework
- authentication strategy
- authorization model
- persistence strategy
- database engine
- file storage strategy
- cache/session strategy
- queue or async processing strategy, if any
- package manager / build tooling
- testing strategy
- deployment assumptions
- observability/logging assumptions
- secret/config management assumptions
- initial security assumptions
- initial project invariants

### INIT MODE output must include
1. recommended baseline
2. key technical decisions
3. trade-offs and risks
4. explicit project checkpoint
5. do-not-regress baseline rules

### INIT MODE prompt template

```text
Atue em INIT MODE.

Quero definir ou revisar a baseline técnica oficial de um projeto.

Projeto:
[Nome e propósito do sistema]
# Ex.: Portal interno de pedidos de serviço, app de chamados, ERP militar, painel administrativo

Objetivo do sistema:
[O que o sistema faz]
# Ex.: cadastro, workflow, relatórios, API pública, dashboard operacional, autenticação centralizada

Tipo de projeto:
[web app / API / fullstack / painel administrativo / portal institucional / app interno]
# Isso ajuda a definir prioridades de UX, segurança e arquitetura

Stack desejada ou opções candidatas:
- Frontend:
  [ex.: React, Vue, Angular, HTML/CSS/JS puro, Blade, Thymeleaf]
- Backend:
  [ex.: PHP (Yii2), PHP (Laravel), Java (Spring Boot), Node (NestJS/Express), Python (FastAPI/Django)]
- Linguagem + framework:
  [sempre informar no formato linguagem (framework)]
# Ex.:
# PHP (Yii2)
# PHP (Laravel)
# Java (Spring Boot)
# Python (FastAPI)
# TypeScript (NestJS)

Como será a autenticação?
[tipo]
# Exemplos:
# sessão com cookie httpOnly
# JWT access + refresh token
# OAuth2 / OpenID Connect
# SSO corporativo
# login local com senha
# autenticação integrada via LDAP/AD

Como será a autorização?
[tipo]
# Exemplos:
# RBAC por perfil
# ABAC por atributos
# escopo por unidade/tenant
# permissões por recurso e ação
# somente autenticação, sem papéis complexos

Como será a persistência?
[modelo]
# Exemplos:
# relacional
# documento
# chave-valor
# híbrida

Qual será o SGBD?
[ex.: PostgreSQL, MySQL, MariaDB, SQL Server, Oracle]
# Se houver legado, informar aqui

Haverá ORM ou acesso direto?
[tipo]
# Exemplos:
# Eloquent
# Doctrine
# JPA/Hibernate
# MyBatis
# query builder
# SQL direto parametrizado

Como será o armazenamento de arquivos?
[tipo]
# Exemplos:
# filesystem local
# S3 compatível
# banco de dados não será usado para binário
# upload temporário + storage definitivo
# sem upload

Como será cache ou sessão?
[tipo]
# Exemplos:
# Redis
# sessão em banco
# sessão em memória
# sem cache inicial

Haverá fila/processamento assíncrono?
[tipo]
# Exemplos:
# RabbitMQ
# Redis queue
# Spring async
# jobs agendados
# sem fila nesta fase

Como será o build/package manager?
[tipo]
# Exemplos:
# pnpm
# npm
# yarn
# composer
# maven
# gradle

Como será o teste?
[tipo]
# Exemplos:
# PHPUnit
# Pest
# JUnit
# Vitest
# Cypress
# Playwright
# smoke tests apenas
# sem testes automáticos na fase inicial

Como será o deploy?
[tipo]
# Exemplos:
# Docker
# VM tradicional
# Apache/Nginx + PHP-FPM
# Tomcat
# container em Kubernetes
# deploy manual em servidor interno

Como serão segredos e configuração?
[tipo]
# Exemplos:
# .env por ambiente
# vault corporativo
# variáveis de ambiente no pipeline
# secrets do cluster

Restrições:
[restrições obrigatórias]
# Exemplos:
# banco obrigatório é PostgreSQL
# sem Docker
# deve rodar em ambiente interno
# deve manter legado Yii2
# sem dependências pagas
# compatível com Java 17
# PHP 8.2 obrigatório

Prioridades:
[ordene o que importa mais]
# Exemplos:
# segurança
# velocidade de entrega
# simplicidade
# baixo custo
# manutenibilidade
# integração com legado
# performance
# auditabilidade

Entregue:
1. baseline técnica recomendada
2. decisões estruturais principais
3. trade-offs
4. checkpoint inicial
5. regras que não devem regredir
```

---

## BUILD MODE

Use this mode when implementing new code inside an existing or newly defined project baseline.

### BUILD MODE GOAL
Create working code that respects the official project baseline and embeds safe engineering defaults from the start.

### Use BUILD MODE when
- creating a new module
- implementing a new screen, API, flow, or feature
- building forms, uploads, reports, dashboards, or admin features
- generating scaffolding that already follows the project baseline

### Do not use BUILD MODE when
- the stack is still undefined
- the user wants only a security review
- the user wants only a targeted fix to existing code

### BUILD MODE must honor
- the latest INIT checkpoint, when available
- the latest validated project baseline
- established invariants and do-not-regress rules
- prior fixes already preserved in checkpoints

### BUILD MODE output must include
1. brief technical direction
2. code
3. assumptions used
4. relevant security notes
5. checkpoint update

### BUILD MODE prompt template

```text
Atue em BUILD MODE.

Quero implementar uma nova funcionalidade dentro da baseline já definida.

Baseline do projeto:
[cole a baseline oficial ou checkpoint mais recente]
# Isso evita drift de stack e de decisões arquiteturais

Escopo da funcionalidade:
[descreva o que será criado]
# Ex.: tela de login, CRUD de usuários, endpoint de upload, dashboard, integração com API externa

Camada afetada:
[frontend / backend / fullstack]
# Ex.: frontend React, backend Laravel, fullstack Spring Boot + Thymeleaf

Stack efetiva desta entrega:
- Frontend:
  [ex.: React, Vue, Blade, Thymeleaf]
- Backend:
  [ex.: PHP (Laravel), Java (Spring Boot)]
# Mesmo havendo baseline, repetir a stack ajuda a evitar ambiguidade local

Objetivo funcional:
[resultado esperado]
# Ex.: permitir cadastro, filtrar registros, anexar arquivos, aprovar requisição

Regras de negócio:
[regras obrigatórias]
# Ex.: somente administradores podem excluir
# Ex.: usuário só vê registros do próprio setor
# Ex.: upload somente PDF até 5 MB

Requisitos de segurança:
[exigências]
# Exemplos:
# validação server-side obrigatória
# sem confiar no client
# logs sem dados sensíveis
# erros genéricos em auth
# upload com validação de MIME e extensão

Requisitos de UX:
[se houver]
# Ex.: loading, disabled state, feedback visual, acessibilidade por teclado

Arquivos ou módulos esperados:
[opcional]
# Ex.: UserController.php, user_form.blade.php, AuthService.java

Restrições:
[restrições técnicas]
# Ex.: não usar nova dependência
# manter padrão atual do projeto
# não quebrar endpoints legados

Entregue:
1. direção técnica breve
2. implementação
3. riscos ou cuidados
4. checkpoint atualizado
```

---

## REVIEW MODE

Use this mode for a frontend-only security review.

### REVIEW MODE GOAL
Audit browser-side code and client behavior for real frontend attack surface, without drifting into backend or infrastructure unless explicitly requested.

### Use REVIEW MODE when
- reviewing React, Vue, Angular, Next frontend, Blade JS behavior, Thymeleaf JS behavior, or plain HTML/JS
- auditing a page, component, SPA flow, admin frontend, or shipped client bundle
- checking rendering, browser storage, DOM sinks, route guards, and unsafe client trust

### Do not use REVIEW MODE when
- the user wants backend vulnerability analysis
- the user wants configuration review
- the user wants patching or hardening
- the issue is clearly server-side

### REVIEW MODE must focus on
- DOM XSS
- unsafe rendering
- unsafe HTML or markdown sinks
- browser storage misuse
- secrets or sensitive exposure in bundle/client code
- unsafe URL/redirect handling
- client-side role checks treated as security
- hidden UI mistaken for enforcement
- preview/rendering of untrusted content

### REVIEW MODE output must include
1. executive summary
2. prioritized findings
3. confidence level for each finding
4. frontend-only evidence
5. recommended fixes
6. checkpoint update

### REVIEW MODE prompt template

```text
Atue em REVIEW MODE.

Quero uma revisão de segurança puramente frontend.

Stack frontend:
[linguagem + framework]
# Exemplos:
# JavaScript (React)
# TypeScript (Vue)
# TypeScript (Angular)
# JavaScript (Next frontend)
# HTML/CSS/JS puro
# PHP (Blade + JavaScript)
# Java (Thymeleaf + JavaScript)

Tipo de frontend:
[SPA / SSR / MPA / híbrido]
# Isso muda o tipo de ataque e de fluxo analisado

Escopo:
[cole o componente, página, fluxo ou bundle]
# Ex.: Login.tsx, UserList.vue, dashboard.js, template Blade com JS embutido

Analise especialmente:
- DOM XSS
- dangerouslySetInnerHTML
- innerHTML e similares
- markdown/rich text rendering
- localStorage/sessionStorage
- open redirect
- query params/hash/router state
- client-side role checks
- hidden UI tratada como segurança
- secrets ou dados sensíveis expostos no bundle
- file preview/renderização de conteúdo não confiável

Restrições:
[opcional]
# Ex.: não assuma backend vulnerável sem evidência
# focar só no componente enviado

Entregue:
1. resumo executivo
2. achados priorizados
3. evidências técnicas frontend-only
4. impacto prático no browser
5. correções recomendadas
6. checkpoint atualizado
```

---

## HARDEN MODE

Use this mode when strengthening existing code or configuration with targeted, reviewable security improvements.

### HARDEN MODE GOAL
Reduce real attack surface with focused fixes, preserving functionality and protecting prior validated changes from regression.

### Use HARDEN MODE when
- fixing vulnerabilities
- improving validation
- strengthening auth/authz
- reducing information leakage
- hardening upload flows
- tightening headers/CORS/cookies/session behavior
- fixing unsafe queries, file paths, redirects, or rendering
- applying small but meaningful security improvements

### Do not use HARDEN MODE when
- the project baseline is still undefined
- the task is purely exploratory architecture selection
- the user wants only review with no changes

### HARDEN MODE may touch
- frontend
- backend
- config
- deployment-relevant app config
- auth flows
- uploads
- integrations
- error handling
- session/cookie policy
- input validation and normalization

### HARDEN MODE output must include
1. main risk reduced
2. fix applied
3. updated code or config
4. attack path mitigated
5. verification notes
6. checkpoint update

### HARDEN MODE prompt template

```text
Atue em HARDEN MODE.

Quero fortalecer um sistema existente com correções pequenas, auditáveis e de alto valor.

Baseline do projeto:
[cole a baseline/checkpoint atual]
# Isso é obrigatório quando houver histórico, para evitar reversão acidental

Stack da área afetada:
- Frontend:
  [ex.: React, Blade, Thymeleaf]
- Backend:
  [ex.: PHP (Yii2), PHP (Laravel), Java (Spring Boot)]
- Banco:
  [ex.: PostgreSQL, MySQL]
- Auth:
  [ex.: sessão com cookie httpOnly, JWT]
# Sempre declarar a stack local ajuda a manter precisão

Escopo:
[arquivo, endpoint, fluxo, config ou módulo]
# Ex.: LoginController.php, SecurityConfig.java, upload endpoint, nginx conf, formulário React

Problema principal:
[descreva o risco]
# Exemplos:
# XSS
# validação insuficiente
# authz fraca
# erro vazando stack trace
# upload inseguro
# CORS aberto demais
# query montada por concatenação

Objetivo da correção:
[o que deve ser endurecido]
# Ex.: sanitizar renderização, validar MIME, fechar redirect aberto, reduzir vazamento, reforçar ownership check

Restrições:
- preservar funcionalidade
- evitar refatoração grande
- seguir o padrão atual
- não remover correções anteriores
# Esta parte conversa diretamente com o protocolo de checkpoint

Entregue:
1. risco principal
2. correção aplicada
3. código/config ajustado
4. ataque ou falha mitigada
5. verificação
6. checkpoint atualizado
```

---

## Checkpoint Continuity Protocol

Every use of this skill must create or update a **checkpoint reference**.

A checkpoint is a compact continuity record that preserves what changed, what must not regress, and what assumptions now define the current state of the code or project baseline.

Its purpose is to prevent:
- loss of prior fixes
- accidental code reversion in later iterations
- reintroduction of previously removed vulnerabilities
- silent removal of UX, accessibility, or security improvements
- drift between the current request and the established implementation baseline

### Mandatory behavior

At the **start** of each new round:
1. identify the latest available checkpoint in the current conversation, canvas, file, or project context
2. treat that checkpoint as the active baseline
3. compare the new request against that baseline before proposing changes
4. preserve prior validated fixes unless the user explicitly asks to replace or undo them

At the **end** of each round:
1. produce a new checkpoint summary
2. explicitly list what was preserved
3. explicitly list what changed
4. explicitly list what must not be lost in future rounds

If no prior checkpoint is available, say so clearly and proceed with best effort, but do not pretend continuity is guaranteed.

### Anti-reversion rule

Never overwrite or regenerate code blindly in a way that may erase a previously applied fix, enhancement, validation rule, accessibility improvement, or security hardening measure.

Before changing existing code, first determine:
- what behavior is already protected
- what prior fix may be affected
- whether the new change conflicts with an established invariant

If a new request risks undoing a previous correction, call that out explicitly and preserve the prior behavior unless the user clearly wants the tradeoff.

### Baseline hierarchy

Use this order of truth when multiple references exist:
1. latest code actually shown or edited
2. latest checkpoint
3. earlier checkpoint history
4. natural-language recollection from the conversation

Do not rely on memory alone when code or checkpoint evidence is available.

## Required Checkpoint Format

At the end of each round, output a checkpoint in this structure:

### CHECKPOINT
- **Mode:** [INIT MODE / BUILD MODE / REVIEW MODE / HARDEN MODE]
- **Scope touched:** [files, components, endpoints, modules, configs, or baseline decisions]
- **Baseline used:** [what prior code/checkpoint this round was based on]
- **Changes applied:** [succinct technical summary]
- **Preserved from previous rounds:** [important fixes or behaviors kept intact]
- **Do not regress:** [non-negotiable protections, validations, UX/security fixes, baseline rules, constraints]
- **Open items:** [known limitations, deferred issues, pending validation]
- **Verification:** [tests run, manual checks, lint/build status, or reasoning-based verification]
- **Next-round caution:** [what future changes are most likely to accidentally break]

This checkpoint must be concrete and implementation-oriented, not generic prose.

## Regression and Reversion Safeguard

This skill must actively protect against accidental regression across iterative rounds.

### Required anti-regression behavior
Before modifying existing code, always identify:
- prior fixes that must remain in place
- validations that must still hold
- security controls that must still exist
- UX/accessibility improvements that are now baseline behavior
- baseline stack decisions that future rounds must still respect

### Reversion detection
Treat the following as high-risk regression events:
- previously added validation disappearing
- sanitized rendering returning to unsafe rendering
- authorization checks being removed or bypassed
- loading/disabled/error states being dropped
- accessibility labels or focus behavior being lost
- hardened config being overwritten by simpler but weaker defaults
- stack assumptions silently changing
- code regeneration that omits prior fixes

If a new version of the code would be simpler but weaker, do not output it without explicitly stating what protection would be lost.

### Patch preference
When possible, prefer targeted patches or localized edits over full rewrites.
Full rewrites are allowed only if the output explicitly preserves all important prior safeguards.

## Invariant Preservation

Each checkpoint must maintain an **invariant list**.

An invariant is a behavior, protection, or guarantee that future rounds must preserve unless the user explicitly asks to remove or change it.

Examples of invariants:
- input `email` must be server-validated
- icon-only buttons must retain aria-label
- dangerous HTML must not be rendered without sanitization
- admin actions must require explicit authorization
- file uploads must retain extension and MIME validation
- error responses must not expose stack traces
- save button must keep loading and disabled states
- route guard must not be described as real security enforcement
- official backend remains PHP (Laravel) unless INIT MODE changes it
- official database remains PostgreSQL unless INIT MODE changes it

When editing code later, preserve the invariants first, then apply the new request.

## Continuity Limitation

This skill can preserve continuity reliably only when prior code, prior checkpoints, or project context are available in the current working context.

If the conversation has moved to a separate chat and no checkpoint or updated code is present, continuity is not guaranteed.

In such cases:
- say that the prior baseline is unavailable
- avoid pretending prior fixes are known with certainty
- rebuild the checkpoint from the code currently provided

## Vulnerability Priorities

### Critical
- hardcoded secrets in code
- missing auth on privileged functionality
- broken authorization enabling cross-user access
- SQL injection
- command injection
- path traversal with meaningful file access
- severe secret leakage
- unsafe direct execution of user-controlled input

### High
- XSS with meaningful exploitability
- CSRF on sensitive actions
- SSRF
- insecure file upload paths
- insecure reset/invite flows
- excessive data exposure
- multi-tenant isolation failure
- replayable sensitive operations
- dangerous CORS misconfiguration

### Medium
- verbose internal errors
- weak validation on important inputs
- insufficient rate limiting
- weak session handling assumptions
- unsafe redirect logic
- missing security headers where relevant
- sensitive data in logs
- inconsistent enforcement across layers

### Low / Defense in Depth
- minor information disclosure
- missing limits or timeouts
- weak but non-exploitable defaults
- incomplete auditability
- hardening opportunities without immediate exploit path

## Verification Discipline

When working in a repo or codebase:

1. inspect the real implementation first
2. identify the dangerous sinks and trust boundaries
3. verify whether the suspected issue is real
4. patch the smallest high-value issue first when asked to fix
5. run relevant checks when available
6. never claim a fix works unless the reasoning or verification supports it

If build, lint, or test commands are available, use the project’s actual tooling.
Do not invent verification.

## What Not To Do

Never:
- confuse frontend validation with security enforcement
- trust hidden fields, disabled buttons, or client-side role flags
- recommend “sanitize everything” without understanding the sink
- overrate weak findings just to sound serious
- bury the real issue under a pile of low-value advice
- expose secrets or vulnerability details irresponsibly
- break working systems with security vanity refactors
- ignore business logic abuse just because there is no classic injection

## Response Style

When presenting the result:
- briefly state the mode used
- state the primary engineering/security angle in one clear sentence
- keep findings structured
- be explicit about certainty
- when building or hardening, deliver working code
- when reviewing, rank findings by real risk, not checklist order
- always emit a checkpoint at the end of the round

## Bar for Success

The result should feel like the work of someone who:
- understands how fullstack systems are actually built
- understands how they are actually attacked
- distinguishes theory from exploitability
- writes secure code without killing usability
- reviews code with adversarial discipline
- hardens systems with restraint and precision
- keeps iterative work from regressing across rounds

Define the project so later work is coherent.
Build software that does not trust blindly.
Review frontend code as if someone smart wants to break it in the browser.
Harden software without turning it into a ritual.
