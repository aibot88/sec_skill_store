---
name: github-skills-installer
description: Instalar skills de repositórios GitHub externos para ~/.aionui-config/skills — inclui Antigravity (1445+ skills), addyosmani, Orchestra Research, Cybersecurity, Marketing, e outros. Usa npx para Antigravity e git clone para os restantes.
category: productivity
---

# GitHub Skills Installer

Instala skills de repositórios GitHub públicos no directório de skills do AionUI: `~/.aionui-config/skills/`.

## Fontes Disponíveis

| Fonte | Skills | Install | Tempo |
|-------|--------|---------|-------|
| **antigravity-awesome-skills** | 1,445+ | `npx antigravity-awesome-skills --path ~/.aionui-config/skills` | ~1 min |
| addyosmani/agent-skills | ~20 | git clone + copy | ~10s |
| Orchestra-Research/AI-Research-SKILLs | ~90 | git clone + copy (formato especial) | ~10s |
| mukul975/Anthropic-Cybersecurity-Skills | 754 | git clone + copy | ~10s |
| coreyhaines31/marketingskills | ~50 | git clone + copy | ~10s |
| Leonxlnx/taste-skill | ~20 | git clone + copy | ~5s |
| mvanhorn/last30days-skill | 1 | git clone + copy | ~5s |

## Workflow: Instalação Completa

### Passo 1 — Antigravity (sempre primeiro, é o maior)

Executar em **background** enquanto se clona os outros em paralelo:

```bash
npx antigravity-awesome-skills --path ~/.aionui-config/skills 2>&1 | tail -5
```

Usar `background=true` na chamada terminal — demora ~1 min mas não bloqueia.

### Passo 2 — Repos restantes em paralelo

```bash
# addyosmani/agent-skills
git clone --depth 1 https://github.com/addyosmani/agent-skills.git /tmp/agent-skills
cp -r /tmp/agent-skills/skills/* ~/.aionui-config/skills/

# Orchestra AI Research (estrutura especial: directorias numeradas)
git clone --depth 1 https://github.com/Orchestra-Research/AI-Research-SKILLs.git /tmp/ai-research-skills
for dir in /tmp/ai-research-skills/*/; do
    skill_name=$(basename "$dir" | sed 's/^[0-9]*-//')
    cp -r "$dir" ~/.aionui-config/skills/"$skill_name" 2>/dev/null
done

# Cybersecurity Skills
git clone --depth 1 https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git /tmp/cybersec
cp -r /tmp/cybersec/skills/* ~/.aionui-config/skills/

# Marketing Skills
git clone --depth 1 https://github.com/coreyhaines31/marketingskills.git /tmp/marketing
cp -r /tmp/marketing/skills/* ~/.aionui-config/skills/

# Taste Skill
git clone --depth 1 https://github.com/Leonxlnx/taste-skill.git /tmp/taste
mkdir -p ~/.aionui-config/skills/taste-skill
cp -r /tmp/taste/* ~/.aionui-config/skills/taste-skill/

# Last30days
git clone --depth 1 https://github.com/mvanhorn/last30days-skill.git /tmp/last30
mkdir -p ~/.aionui-config/skills/last30days
cp -r /tmp/last30/* ~/.aionui-config/skills/last30days/
```

### Passo 3 — Verificar

```bash
ls ~/.aionui-config/skills/ | wc -l
# Esperado: ~2360+ skills após instalação completa
```

## Estruturas de Repos GitHub (GOTCHAS)

Nem todos os repos têm `skills/` à raiz. Três padrões comuns:

1. **`skills/` à raiz** (addyosmani, cybersec, marketing) → `cp -r repo/skills/* dest/`
2. **Directórios numerados** (Orchestra: `01-model-architecture/`) → iterar e renomear com `sed 's/^[0-9]*-//'`
3. **Tudo num subdir** (taste-skill: `skills/` dentro de `taste-skill/`) → copiar o repo inteiro para o dest

**Verificar sempre com `ls repo/` antes de copiar.**

## Antigravity — Opções Úteis

```bash
# Instalar só skills de uma categoria
npx antigravity-awesome-skills --path ~/.aionui-config/skills --category development,backend

# Filtrar por risk (safe,none vs medium,high)
npx antigravity-awesome-skills --path ~/.aionui-config/skills --risk safe,none

# Versão específica
npx antigravity-awesome-skills --path ~/.aionui-config/skills --version 4.6.0

# Help
npx antigravity-awesome-skills --help
```

## Verificação Pós-Instalação

```python
import os
skills_dir = '/Users/alvarobiano/.aionui-config/skills'
count = len(os.listdir(skills_dir))
print(f"Total: {count} skills")
```

## Atualização

```bash
# Antigravity — nova versão
npx antigravity-awesome-skills --path ~/.aionui-config/skills

# Repo específico — pull + recopy
cd /tmp/agent-skills && git pull
cp -r /tmp/agent-skills/skills/* ~/.aionui-config/skills/
```

## Descobertas desta Sessão

- Antigravity (1445+ skills) é de longe a fonte mais densa — instalar sempre primeiro
- addyosmani/agent-skills inclui lifecycle completo: spec→plan→build→test→review→ship
- Orchestra AI Research SKILLs mapeia para o pipeline completo de ML/AI research
- Last30days skill tem suporte explícito para Hermes Agent (ler SKILL.md para setup)
- Taste Skill melhora radicalmente outputs de UI/design — anti-slop

## Referências

- Antigravity: https://github.com/sickn33/antigravity-awesome-skills
- addyosmani: https://github.com/addyosmani/agent-skills
- Orchestra: https://github.com/Orchestra-Research/AI-Research-SKILLs
- Cybersecurity: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
- Marketing: https://github.com/coreyhaines31/marketingskills
- Taste: https://github.com/Leonxlnx/taste-skill
- Last30days: https://github.com/mvanhorn/last30days-skill
