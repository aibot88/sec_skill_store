---
name: lovable-supabase-integration
description: Integração entre projetos Lovable e Supabase, guiando conexão, auth, storage, Edge Functions e segurança (RLS) conforme documentação oficial do Lovable.
---

# Lovable + Supabase Integration

## Quando ativar este skill

Ative este skill quando o usuário:

- Mencionar **Lovable** e **Supabase** juntos, por exemplo:
  - "Conectar Lovable ao Supabase"
  - "Configurar backend Supabase no meu app Lovable"
  - "Como salvar dados do meu app Lovable no Supabase?"
  - "Quero usar autenticação do Supabase com o Lovable"
- Falar sobre:
  - Edge Functions no Supabase para app gerado no Lovable
  - Armazenar imagens/arquivos do app Lovable no Supabase Storage
  - Aplicar RLS/policies nas tabelas geradas pelo Lovable
- Usar prompts típicos do Lovable que envolvem backend, por exemplo:
  - "Add login"
  - "Add feedback form and save responses in a database table."
  - "Allow users to create posts and store them in the database."

Se o contexto for apenas "Supabase genérico" (sem Lovable), prefira skills específicos de Supabase/Postgres já existentes no projeto.

## Objetivos principais

Quando este skill estiver ativo, o agente deve ajudar o usuário a:

1. **Conectar Lovable ↔ Supabase**
   - Explicar como:
     - Criar uma conta e projeto no Supabase.
     - No editor do Lovable, abrir **Settings → Integrations → Supabase** e clicar em **Connect Supabase**.
     - Autorizar o Lovable na conta Supabase e selecionar/criar um projeto.
   - Lembrar que a confirmação típica é algo como "✅ Supabase connected" no chat do Lovable.

2. **Configurar autenticação (Auth)**
   - No Supabase:
     - Habilitar email/password em **Authentication → Settings/Email**.
     - Em ambiente de desenvolvimento, opcionalmente desabilitar "Confirm email" para facilitar testes.
     - Habilitar provedores OAuth (Google, GitHub etc.) em **Authentication → Providers** quando o usuário quiser "Sign in with Google" e similares.
   - No Lovable:
     - Orientar o usuário a pedir coisas como "Add login" ou "Add a 'Sign in with Google' button to the login page." para gerar as telas de auth já integradas com Supabase.

3. **Criar e aplicar schemas de dados**
   - Deixar claro o fluxo recomendado de trabalho:
     1. Usuário descreve a feature no Lovable (por exemplo: "Add a feedback form and save responses in a database table.").
     2. Lovable gera um snippet de **SQL** para criar/alterar tabelas.
     3. Usuário copia esse SQL e executa no Supabase em **SQL Editor**.
     4. Usuário confirma no Lovable que executou o SQL; o Lovable então termina de conectar o UI com a tabela.
   - Reforçar:
     - Verificar o resultado em **Table Editor** do Supabase.
     - Usar o AI SQL Assistant do Supabase se precisar de queries avançadas ou customizadas.

4. **Armazenar arquivos com Supabase Storage**
   - Sugerir Storage para uploads de:
     - Fotos de perfil.
     - Imagens de produtos/conteúdo.
     - Outros anexos.
   - Lembrar:
     - Na tier gratuita, uploads até ~50MB por arquivo (bom para imagens e mídias leves).
     - Organização em buckets (públicos ou privados) com regras de acesso.
   - Exemplos de requests ao Lovable que o agente pode sugerir:
     - "Add a profile picture upload to the account settings page."

5. **Gerenciar secrets (API Keys & config sensível)**
   - Enfatizar que segredos **nunca** devem ir para o código-fonte ou para o frontend.
   - Orientar o usuário a cadastrar API keys (Stripe, OpenAI, etc.) no secret manager de Edge Functions do Supabase.
   - Explicar que Edge Functions poderão ler esses secrets via ambiente seguro.

6. **Criar backend customizado com Edge Functions**
   - Pedir que o usuário descreva a lógica desejada em linguagem natural, por exemplo:
     - "When a user submits the feedback form, analyze the text using OpenAI and store a sentiment score."
   - Explicar que:
     - O Lovable pode gerar uma Supabase Edge Function que implementa essa lógica.
     - A aplicação Lovable chamará essa função no momento adequado (submit de formulário, webhook etc.).
     - Logs e erros da função podem ser inspecionados em **Supabase → Functions → Logs**.

7. **Segurança e RLS antes de produção**
   - Sempre reforçar que, para produção, é obrigatório:
     - Ativar Row Level Security (RLS) nas tabelas sensíveis.
     - Criar policies que garantam que cada usuário só acesse os próprios dados (ou dados do tenant correto, se multi-tenant).
   - Apontar para o caminho no painel:
     - **Supabase → Tabela → RLS/Policies** ou **Auth → Policies**, dependendo da UI.
   - Sugerir políticas básicas, por exemplo:
     - SELECT/INSERT/UPDATE/DELETE permitidos apenas se `auth.uid()` bater com o owner/user_id do registro.

8. **Escalabilidade e integrações externas**
   - Lembrar que Supabase é um Postgres gerenciado e escala via planos pagos.
   - Explicar que, com o Supabase conectado:
     - As tabelas ganham REST APIs automáticas.
     - É possível integrar com ferramentas como Zapier, Make.com e outros via HTTP.
   - Sugerir Edge Functions como camada de orquestração quando a lógica for mais complexa.

## Comportamento esperado do agente

Quando este skill estiver ativo, o agente deve:

- **Responder sempre em Português (pt-BR)**, de forma direta e pragmática.
- **Evitar pedir ou exibir segredos** (chaves API, tokens, etc.).
- Sempre que possível, responder em formato de **passo a passo curto** (checklist) para ações que envolvem Lovable + Supabase.
- Referenciar a documentação oficial quando agregar valor:
  - `https://docs.lovable.dev/integrations/supabase`
- Incentivar boas práticas:
  - RLS antes de produção.
  - Usar ambientes separados (ex.: branches do Supabase) para testes de schema arriscados.
  - Não depender apenas de validação no frontend para segurança.

## Exemplos de prompts que devem acionar este skill

- "Quero conectar meu app do Lovable a um banco Supabase, como faço?"
- "O Lovable gerou um SQL para criar a tabela de feedback, onde eu executo isso no Supabase?"
- "Adicione login no meu app Lovable usando Supabase."
- "Quero salvar imagens de perfil dos usuários do Lovable no Supabase Storage."
- "Preciso de uma Edge Function no Supabase que processe pagamentos com Stripe para meu app do Lovable."
- "Como aplicar RLS nas tabelas geradas pelo Lovable para que cada usuário veja só os próprios dados?"

## Links de referência

- Documentação oficial Lovable + Supabase: `https://docs.lovable.dev/integrations/supabase`
- Supabase: `https://supabase.com/`

