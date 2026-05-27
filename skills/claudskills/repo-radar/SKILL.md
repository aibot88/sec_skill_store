---
name: repo-radar
description: Analisa e classifica um repositório GitHub via repo-radar CLI (SQLite + LLM), registrando o veredito em PROJECT_EVALUATIONS.md
version: 1.0.0
owner: platform-governance
tier: full
source: .enterprise/governance/agent-skills/repo-radar/SKILL.md
quick: .enterprise/governance/agent-skills/repo-radar/SKILL-QUICK.md
portable: true
license: Apache-2.0
---

# repo-radar — Guia Completo

## Quando usar

Carregue esta skill quando o usuário pedir:
- repo-radar, avaliar repositório, analisar repo, classificar repo
- score repo, evaluate repo, rate repository
- quero saber se vale usar X, análise de projeto open-source

---

## PASSO 0 — Identificar o repositório

Se `$ARGUMENTS` contiver uma URL GitHub, usar diretamente.
Se não, perguntar: "Qual é a URL do repositório a avaliar?"

---

## PASSO 1 — Verificar instalação do CLI

```bash
which repo-radar && repo-radar --version
```

Se não instalado:

```bash
# Verificar se o source existe
ls /opt/references/repo-radar 2>/dev/null || \
  git clone https://github.com/marciohideaki/repo-radar /opt/references/repo-radar

pip install -e /opt/references/repo-radar
```

---

## PASSO 2 — Garantir configuração do .env

```bash
ls /opt/references/repo-radar/.env 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

Se `NOT_FOUND`, criar a partir do exemplo:

```bash
cp /opt/references/repo-radar/.env.example /opt/references/repo-radar/.env
```

Configurar `LLM_PROVIDER` conforme o agente em execução:

| Agente | LLM_PROVIDER | API Key |
|--------|-------------|---------|
| Claude Code | `claude` | `ANTHROPIC_API_KEY` |
| Codex | `openai` | `OPENAI_API_KEY` |
| Gemini CLI | `gemini` | `GEMINI_API_KEY` |
| Ollama local | `ollama` | — |

---

## PASSO 3 — Executar análise

```bash
cd /opt/references/repo-radar
repo-radar add "<url-do-repositorio>"
```

O CLI irá:
1. Buscar metadados via GitHub API (stars, forks, contributors, releases, language, license)
2. Clonar repositório em `repos/`
3. Calcular scores heurísticos: `interest`, `doc`, `code`, `coherence`, `maturity`
4. Consultar LLM para veredito final (classificação + rationale)
5. Persistir em SQLite (`data/radar.db`) — append-only

---

## PASSO 4 — Exibir resultado

```bash
repo-radar show <nome-do-repo>
```

Anotar:
- Classificação: `INTERESTING` | `INCORPORATE` | `WATCH` | `REDUNDANT` | `DISCARD`
- Scores individuais (0–10 cada)
- Rationale do LLM
- Metadados (stars, forks, language, license, last push)

---

## PASSO 5 — Exportar para PROJECT_EVALUATIONS.md

Arquivo destino: `/opt/references/PROJECT_EVALUATIONS.md`

**Se o repositório JÁ EXISTE no arquivo → atualizar a entrada existente.**
**Se é novo → adicionar ao final.**

Template obrigatório:

```markdown
## owner/repo

- Local path: `/opt/references/<nome>`
- Status: `adopt` | `partial` | `reject`
- Priority: `high` | `medium` | `low`
- Recommended action: <ação objetiva em uma frase>

#### What To Reuse

- <item concreto com contexto — baseado no rationale do LLM e evidências reais>

#### What To Avoid

- <item concreto com contexto>

#### Risks

- <risco específico identificado>

#### Evidence

- `path/to/file`: <nota objetiva sobre o arquivo>

#### Notes

- Scores: interest=X doc=X code=X coherence=X maturity=X
- Stars: X | Forks: X | Contributors: X | Releases: X
- Language: X | License: X | LLM: <provider>
- Last push: YYYY-MM-DD
- radar.db: `/opt/references/repo-radar/data/radar.db`
```

**Mapeamento de classificação:**

| CLI Output | Status | Priority (guideline) |
|-----------|--------|---------------------|
| INTERESTING | adopt | high |
| INCORPORATE | partial | medium |
| WATCH | partial | low |
| REDUNDANT | reject | low |
| DISCARD | reject | low |

---

## Regras de governança

| Regra | Detalhe |
|-------|---------|
| SQLite é fonte primária | PROJECT_EVALUATIONS.md é relatório derivado — nunca editar sem consultar o DB |
| Sem duplicatas | Se entry existe, atualizar — nunca adicionar segundo bloco para mesmo repo |
| Evidência real | Citar arquivos reais encontrados no clone — não inventar caminhos |
| Scores obrigatórios | Sempre incluir `interest=X doc=X code=X coherence=X maturity=X` nas Notes |
| Rationale como base | Usar o texto do LLM como fonte para What To Reuse / What To Avoid |


## Quick Mode

For low-context activation, load `.enterprise/governance/agent-skills/repo-radar/SKILL-QUICK.md` or `QUICK.md` first. Load this full skill for deep analysis, violation fixing, or formal review gates.

