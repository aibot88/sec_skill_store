---
name: frontend-skill
description: >-
  Implementa frontends Next.js (App Router) com UI alinhada ao design system, Atomic Design, TypeScript,
  SCSS, ShadCN sem Tailwind, DTOs Zod, React Hook Form, middleware/auth, RBAC na UI,
  estados de carregamento/erro e SSE quando o produto exigir. Use ao criar ou alterar
  páginas, componentes, hooks, integração com API ou qualquer UI neste repositório.
---

# Skill — Frontend (Next.js, monorepo EmpregaNet)

Documento único: regras para humanos e para o agente de IA. Mantém o mesmo conteúdo de referência.

## Quando esta skill se aplica

Qualquer trabalho no frontend: novas telas, componentes, hooks, camada de API, fluxos de autenticação, tempo real (SSE) ou refatorações que toquem na UI.

## Alinhamento com o agente

Para **implementação**, siga as mesmas regras do agente **`frontend-engineer`**. Leia e respeite [`docs/agents/frontend-engineer.md`](../../agents/frontend-engineer.md) antes de escrever código (stack, o que evitar, organização de pastas).

## Resumo

- Usar o perfil **`frontend-engineer`** para implementação (link acima).
- Respeitar a estrutura do monorepo em `frontend/`.
- **Não** introduzir Tailwind nem expandir o seu uso.
- **SCSS** e componentes no estilo ShadCN/Radix já adaptados ao projeto.
- Acessibilidade e estados de UI (carregamento, erro, vazio, retry) sempre explícitos.

## Regras obrigatórias

- **Arquitetura**: estrutura por **feature**; separação clara entre UI, lógica de aplicação e **serviços** (cliente HTTP em `frontend/src/services/`, barril conforme convenção do repositório).
- **Estilo**: **SCSS** + padrões ShadCN já usados. **Não introduzir Tailwind.**
- **Tipos nas fronteiras**: DTOs tipados com **Zod** (validar entradas da API e variáveis de ambiente quando fizer sentido).
- **Acessibilidade**: HTML semântico, rótulos, teclado, foco em overlays; ARIA só quando a semântica nativa não bastar.
- **UX**: estados explícitos de **carregamento**, **vazio**, **erro** e **retry** — nunca falha silenciosa nem tela em branco.

## Checklist de entrega de feature

Use como guia ao construir uma feature:

1. [ ] **Pasta da feature** — `features/<feature>/` (ou convenção do projeto): UI, hooks, tipos e serviços específicos colocados juntos.
2. [ ] **Componentes de UI** — peças enxutas e apresentacionais; reutilizar primitivos do design system.
3. [ ] **Lógica** — hooks e/ou serviços pequenos para dados, validação e efeitos colaterais (não dentro de árvores JSX grandes).
4. [ ] **Camada de API** — cliente centralizado; requisições/respostas tipadas (Zod); evitar `fetch` espalhado sem padrão.
5. [ ] **Carregamento / erro** — UI de pendência e falha; política de reconexão se usar streams.
6. [ ] **Acessibilidade** — teclado e leitor de ecrã nas partes interativas.
7. [ ] **SSE** — só se o produto exigir push no servidor: reutilizar ou criar hook/serviço com backoff, reconexão e erro visível.

## Sempre incluir (quando relevante)

- **Pastas claras** — limites entre `components/`, hooks/serviços por feature; API + Zod por domínio em `services/<domínio>/` (`*-api.ts`, `*-schema.ts`); tipos locais na feature quando fizer sentido.
- **Middleware / auth** — middleware do Next.js em rotas protegidas; sessão ou JWT conforme padrão do projeto.
- **UI por papéis** — menus, ações e rotas condicionadas a papéis/permissões; centralizar verificações de capacidade; evitar strings mágicas duplicadas.

## Stack técnica (estrita)

| Usar | Não usar |
|------|----------|
| Next.js App Router, TypeScript | Tailwind (novo ou expansão) |
| SCSS para estilo | Lógica de negócio inchada em componentes de UI |
| ShadCN adaptado a SCSS | Acoplamento forte a detalhes internos do backend |
| Zod para DTOs / validação | — |
| React Hook Form + resolvers Zod | — |

## Expectativas de saída

- Seguir naming, layout de ficheiros e estilo de imports já existentes no repositório.
- Texto voltado ao utilizador em **português (Brasil)** quando o produto for em português.
- Explicar só estrutura ou limites de estado não óbvios; priorizar código que funciona.
