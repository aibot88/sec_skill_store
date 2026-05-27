---
name: nps-skill
description: Skill para produzir uma plataforma de pesquisa NPS com PHP Slim, SQLite, HTMX, VanJS e Squeleton.dev, incluindo home showcase, admin completo, widget embed e gatilhos de exibição.
---

# NPS com Squeleton.dev

## Objetivo

Construir um sistema de pesquisas estilo SurveyMonkey focado em NPS, com:

- Home de showcase das bibliotecas do Squeleton.dev.
- Painel administrativo para gestão de projetos, pesquisas, perguntas e respostas.
- Widget JavaScript embutível para coleta de respostas em qualquer site.

Tecnologias obrigatorias:

- Backend: PHP Slim + SQLite.
- Infra: Docker com PHP 8.x + Nginx.
- Frontend: HTMX, VanJS e Squeleton.dev.

## Regra critica de nomenclatura

Sempre utilizar o nome correto da base visual e do ecossistema: Squeleton.dev.
Nunca usar "Skeleton.dev".

## Escopo funcional

### 1. Home Page (Showcase)

A home deve demonstrar visualmente os recursos da stack:

- Animacoes com Wow2 (`.wow`) em secoes e cards.
- Carrossel com Embla Carousel para tipos de pesquisa/casos de uso.
- Contadores animados com Counter-Up2 usando dados reais do SQLite.
- Integracao com YouTube (ID `DMrJUyg7TYM`) com gatilho automatico `after_completed_video` ao concluir o video.
- Botoes de simulacao para disparar gatilhos manuais e abrir pesquisas em modal.

### 2. Sistema administrativo

#### 2.1. Autenticacao

- Login via sessao PHP (`$_SESSION`).
- Credenciais vindas do `.env`: `ADMIN_USER` e `ADMIN_PASS`.
- Middleware para proteger todas as rotas de admin.

#### 2.2. Gestao de projetos

- Criar, listar e visualizar projetos.
- Gerar chave unica de integracao por projeto (API key/public key para widget JS).

#### 2.3. Gestao de pesquisas

- Criar varias pesquisas por projeto.
- Configurar gatilho por pesquisa:
	- `on_load`
	- `after_completed_video`
	- `before_cancel`

#### 2.4. Editor de perguntas

Tipos de pergunta suportados:

- Nota (`0-10`)
- Estrelas (`0-5`)
- Input de texto
- Select
- Checkbox
- Radio

Configuracoes por campo:

- Obrigatorio (`required`)
- Logica condicional (exemplo: exibir pergunta de follow-up se nota `< 5`)

#### 2.5. Dashboard

- Cards com estatisticas gerais (respostas, taxa de conclusao, media NPS etc.).
- Lista de respostas recentes.
- Uso de Counter-Up2 para animacao de numeros.
- Uso consistente de icones nativos do Squeleton (`iccon-*`).

### 3. Widget de integracao (embed JS)

Implementado com VanJS, com foco em leveza e renderizacao dinamica.

Responsabilidades:

- Buscar configuracao da pesquisa via API.
- Renderizar formulario dinamicamente com base no schema.
- Aplicar regras condicionais em tempo real.
- Capturar metadados de contexto:
	- URL da pagina
	- gatilho disparado
	- identificador de usuario/sessao quando disponivel
- Enviar respostas via `POST` para API Slim.

## Requisitos tecnicos

### Backend e API

- Slim para roteamento e middlewares.
- SQLite para persistencia de projetos, pesquisas, perguntas e submissoes.
- API mista:
	- JSON para widget
	- respostas HTMX para telas de admin

### Infra e setup

Disponibilizar comando unico de inicializacao (`Makefile` ou `setup.sh`) que execute:

- Instalacao de dependencias (`composer` e `npm`, quando necessario)
- Geracao/configuracao do `.env`
- Migracoes e seed com dados realistas
- Subida dos containers Docker

## Diretrizes de UX/UI

- Cor primaria: azul.
- Erros e avisos com alertas nativos do Squeleton.dev.
- Sucesso com Toastify-js.
- Estados de carregamento com HTMX (`hx-indicator` e spinners visuais).
- Formularios e modais com foco em clareza e baixa friccao.

## Criterios minimos de aceite

- Login admin funcional com sessao e rotas protegidas.
- CRUD basico de projetos e pesquisas operando no SQLite.
- Editor de perguntas com campos obrigatorios e logica condicional.
- Widget carregando pesquisa via API e salvando respostas.
- Gatilho `after_completed_video` acionando pesquisa apos fim do video YouTube.
- Dashboard exibindo estatisticas reais e respostas recentes.
- Setup de ambiente funcionando por comando unico.

## Referencias

- Squeleton.dev
- Video de referencia: YouTube `DMrJUyg7TYM`

