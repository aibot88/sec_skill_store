---
name: backstage-docs
description: |
  Consulta a documentação completa do Backstage (Spotify's developer portal, CNCF) em 489 markdown pages locais offline. Use SEMPRE que o usuário perguntar sobre Backstage — instalação, plugins, frontend system (alpha), backend system, software catalog, software templates, scaffolder, techdocs, search, permissions, auth providers (GitHub, Okta, GitLab, etc), kubernetes plugin, integrations (GitHub/GitLab/Bitbucket/Azure/AWS S3), deployment, configuration, ou qualquer tópico Backstage. Cobre também o deploy NXT específico em backstage.plataforma.app. Use também em dúvidas tipo "como faço X no Backstage", "qual a config Y do Backstage", "como criar plugin Backstage", "como customizar tema Backstage" — mesmo se a pergunta não usar a palavra "Backstage" mas o contexto deixar claro (ex: usuário trabalhando em /root/nxt/terminal.net.br/recursos/backstage/).
---

# Backstage Documentation — local offline corpus

Documentação oficial do Backstage (489 markdown pages extraídas de https://backstage.io/docs em 2026-05-01) disponível 100% offline em `/root/nxt/terminal.net.br/recursos/backstage/_docs/`. Esta skill mapeia cada categoria pra caminhos exatos de arquivos pra você poder responder perguntas específicas sem fetch externo.

## Como usar esta skill

1. **Identifique a categoria** da pergunta usando o mapa em `references/MAP.md`
2. **Leia o arquivo específico** com a tool Read (não use Glob/Grep gigante — a estrutura já indica onde está o conteúdo)
3. **Cite o caminho** no answer pro usuário (formato: `recursos/backstage/_docs/<categoria>/<file>.md`) pra que ele possa abrir e verificar
4. Se a pergunta cruzar categorias (ex: "auth + permissions"), leia ambos arquivos relevantes

## Atalhos por intent

| Intent do usuário | Onde olhar primeiro |
|---|---|
| "Como instalar / criar app novo" | `getting-started/` |
| "Como funciona o frontend system / extensions / blueprints" | `frontend-system/architecture__*.md` |
| "Como criar plugin frontend" | `frontend-system/building-plugins__*.md` + `frontend-system/building-apps__*.md` |
| "Como funciona backend system" | `backend-system/architecture__*.md` |
| "Como criar plugin backend" | `backend-system/building-plugins-and-modules__*.md` + `backend-system/building-backends__*.md` |
| "Software Catalog / entidades / kinds" | `features/software-catalog__*.md` |
| "Software Templates / scaffolder / wizard" | `features/software-templates__*.md` |
| "TechDocs / docs as code / MkDocs integration" | `features/techdocs__*.md` |
| "Search" | `features/search__*.md` |
| "Auth provider X" (github, okta, google, gitlab, ldap, oauth2-proxy) | `auth/<provider>.md` |
| "Permissions / RBAC" | `permissions/`, `tutorial--using-permissions-in-your-plugin/` |
| "Integration X" (github, gitlab, bitbucket-cloud, bitbucket-server, gitea, gerrit, azure, aws-s3, google-gcs, azure-blob-storage) | `integrations/<provider>__*.md` ou top-level `<provider>/` |
| "Kubernetes plugin" | `features/kubernetes__*.md` |
| "Deployment / docker / k8s deploy / heroku" | `deployment/`, `getting-started/deployment-*.md` |
| "Notifications" | `notifications/` |
| "Configuration / app-config.yaml / env vars" | `conf/`, `configuration/`, `configuring-backstage/` |
| "CLI / `backstage-cli` commands" | `tooling/`, `backstage-cli/` |
| "Architecture decisions / why X exists" | `architecture-decisions/`, `architecture-decision-records--adrs-/` |
| "Tutorial X" | `tutorials/` |
| "Golden Path / best practices" | `golden-path/` |

## Mapa completo

Pra detalhamento de cada categoria + arquivos, leia: `references/MAP.md`

## Contexto NXT-specific

O deploy Backstage NXT roda em `backstage.plataforma.app` com:
- Código: `/root/nxt/terminal.net.br/recursos/backstage/services/backstage/app/`
- Catalog source: `recursos/<slug>/index.v2.json` (1107 items) + 360 Systems + 360 Groups
- Seed script: `projetos/catalogo.plataforma.app/scripts/seed-backstage-catalog.ts`
- Theme NXT: zinc + lime `#deff3f` em `app/packages/app/src/modules/theme/index.tsx`
- Reverse proxy: `services/backstage/caddy.conf` importado em `/etc/caddy/Caddyfile`
- Service: `/etc/systemd/system/backstage.service`
- DB: Postgres container `backstage-db` na porta 5440
- Doc operacional: `services/backstage/CLAUDE.md`

Pra perguntas operacionais (restart, regen catalog, debug logs), leia esse `CLAUDE.md` antes — é mais relevante que a doc oficial pra esses casos.

## Quando NÃO usar esta skill

- Pergunta sobre outra ferramenta (Datasette, MkDocs, Backrest) — use a skill correspondente ou `recursos/<slug>/CLAUDE.md`
- Perguntas sobre Backstage roadmap futuro / `/next/` previews — não capturado (skipped no extract)
- Changelog detalhado por release — `_docs/releases/` foi pulado; use `npx @backstage/cli versions:check` ou github upstream

## Atualização do corpus

Re-extrair se necessário (incremento mensal):
```bash
cd /root/nxt/terminal.net.br/recursos/backstage
bash _docs/_extract.sh
```

Lê `_docs/_sitemap.txt` (489 URLs) e re-baixa via `curl + pandoc` paralelo.
