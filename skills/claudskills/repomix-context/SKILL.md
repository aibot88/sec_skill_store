---
name: repomix-context
version: 0.1.0
category: 90-meta
created: 2026-05-23
description: |
  TRIGGER: "analise meu repo inteiro", "repomix", "empacotar código", "passar repo para LLM", "compress repo", "share with AI". Usa Repomix para empacotar repo em um único arquivo (XML/JSON/Markdown) otimizado para context window de LLM, com filtros por extensão/path e remoção de comentários/secrets.
triggers: ["repomix", "empacotar repo", "passar repo para llm", "analisar repo inteiro", "code share", "context pack"]
verification: pnpm dlx repomix gera arquivo em <output> com tokens estimados; pode ser lido por Claude/GPT sem truncar; secrets removidos; binários/lockfiles ignorados; estatística de tokens reportada
inputs:
  scope: "all | src-only | specific-paths"
  output_format: "xml (default) | markdown | json | plain"
  include_patterns: "globs (opcional)"
  exclude_patterns: "globs (opcional)"
  remove_comments: "true para máxima compressão"
outputs:
  packed_file: "repomix-output.xml ou similar"
  token_stats: "contagem por arquivo + total"
---

## When to use

- Análise de arquitetura: "veja meu repo todo e me diga onde melhorar"
- Code review por LLM antes de PR
- Migração de codebase para nova stack (LLM precisa ver tudo)
- Onboarding rápido em projeto novo
- Compartilhar repo para chat (sem subir Git inteiro)

## When NOT to use

- Tarefa pontual em 2-3 arquivos → leia direto, não empacote
- Repo >2GB ou >500k linhas → use filtros agressivos OU divida por módulo
- Necessita acesso a git history → repomix só captura snapshot atual
- Compliance: arquivos sensíveis precisam de revisão manual antes de exportar

## Por que Repomix

- **Single-file output** otimizado para LLM
- **Filtros nativos** (gitignore-aware, custom patterns)
- **Remoção de comentários** (compressão extra)
- **Contagem de tokens** (saiba se cabe no context)
- **Hospedado**: site `repomix.com` faz o mesmo via web
- **Alternativas**: `git-bundle`, `code2prompt`, manual concat

## Steps

1. **Instalar (one-off):**
   ```powershell
   pnpm dlx repomix
   ```
   Sem instalação permanente — sempre rodar via `pnpm dlx`.
2. **Rodar na raiz do projeto target** (NÃO no tahara_skills se for analisar outro projeto):
   ```powershell
   cd C:\Users\Tahara\projetos\<projeto-target>
   pnpm dlx repomix
   ```
   Gera `repomix-output.xml` com TODO o repo (respeitando `.gitignore`).
3. **Filtros úteis:**
   ```powershell
   # Só src/, ignora tests
   pnpm dlx repomix --include "src/**" --ignore "**/*.test.*,**/node_modules/**"

   # Output como markdown
   pnpm dlx repomix --style markdown

   # Remove comentários (mais compactação)
   pnpm dlx repomix --remove-comments

   # Limita por tamanho (skip arquivos grandes)
   pnpm dlx repomix --max-file-size 100000
   ```
4. **Config persistente** (`repomix.config.json`):
   ```json
   {
     "output": {
       "filePath": "repomix-output.xml",
       "style": "xml",
       "removeComments": true,
       "showLineNumbers": false
     },
     "include": ["src/**", "*.md"],
     "ignore": {
       "useGitignore": true,
       "customPatterns": [
         "**/*.test.ts",
         "**/*.spec.ts",
         "**/__snapshots__/**",
         "**/.env*",
         "**/dist/**"
       ]
     },
     "tokenCount": { "encoding": "o200k_base" }
   }
   ```
5. **Antes de compartilhar:**
   - `grep -i "sk-" repomix-output.xml` — caça API keys vazadas
   - `grep -i "password\|secret\|token" repomix-output.xml | head` — confere
   - Se achou: ajuste filtros e regenera
6. **Validar token count:**
   ```powershell
   # repomix mostra estatísticas no final do run
   # exemplo: "Total tokens: 142,318"
   ```
   Compare com limite do modelo alvo (Claude Opus 4.7 1M context = bem confortável; GPT-4 128k é apertado).
7. **Passar para LLM:**
   - Claude: anexar arquivo ou paste em system prompt
   - Use prompt como: *"Aqui está o repo. Aponte 3 melhorias críticas com file:line."*

## Anti-patterns

- ❌ Empacotar antes de filtrar (token count explode com node_modules, dist, lockfiles)
- ❌ Esquecer de verificar secrets antes de subir output para chat público
- ❌ Usar para tarefa que cabe em 3 arquivos (overkill — leia direto)
- ❌ Não usar config persistente em repo recorrente (reescrever flags cansa)
- ❌ Confiar que `.gitignore` cobre tudo — credenciais podem estar em arquivos não-ignorados

## Verification

1. Output file gerado, tamanho razoável (KB-MB, não GB)
2. Total tokens reportado < limite do modelo destino
3. Grep por padrões de secret retorna 0 matches
4. node_modules, dist, .env não aparecem
5. Estrutura legível (header + tree + files)

## Example

```
User: "Quero o Claude analisar todo o barberia-saas"

Skill:
  cd C:\Users\Tahara\projetos\barberia-saas
  pnpm dlx repomix --style markdown --remove-comments --ignore "**/test/**,**/node_modules/**"
  → repomix-output.md, 78k tokens
  → grep "sk-\|whsec_" → 0 matches ✓
  → cola no Claude Code com prompt "audite arquitetura, segurança, perf"
```

## Notes

- **CI integration**: rode repomix automaticamente após release; armazene snapshot para análise histórica
- **Privacy**: NUNCA suba output gerado a paste-bin público sem revisar secrets
- **Comparison repomix vs code2prompt vs git archive**: repomix é mais LLM-otimizado
- **Repomix server mode**: serve repos via API local; útil para integração com MCP custom
- **Tokenizer**: padrão usa `o200k_base` (GPT-4o). Para Claude, ratio é similar; estimativa boa.

## Sources

- https://repomix.com/
- https://github.com/yamadashy/repomix
- Related: [[lean-context-mgmt]] · [[security-review-product]]
