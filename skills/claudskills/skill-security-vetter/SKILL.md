---
name: skill-security-vetter
description: Sistema de validação de segurança para skills — Bianinho Vetter. Valida skills antes de instalar, detecta padrões maliciosos (exfiltração, injection, shell injection, commands destrutivos), audit das já instaladas, e integração automática no workflow de instalação. CORREIGIDO E AMPLIADO em 19/04/2026.
category: security
tags: [segurança, skills, validação, injection, exfiltração, supply-chain]
---

# Skill Security Vetter — Bianinho

## O que é

Sistema de validação de segurança para todas as skills baixadas de fontes externas (GitHub, ClawHub, etc.).

Antes de qualquer skill ser instalada, é escaneada para:
- **Exfiltração de dados** — API keys, tokens, passwords hardcoded
- **Prompt injection** — override de system prompt, bypass de instruções
- **Command injection** — `curl|bash`, `wget|bash`, `$()|bash`
- **Shell injection** — `subprocess(shell=True)`, `eval()`, `exec()`, `base64+exec`
- **Comandos destrutivos** — `rm -rf /`, `dd`, `fdisk`, `mkfs`, `shred`
- **Persistência maliciosa** — crontab, systemd, `.bashrc` injection
- **Secrets em variáveis de ambiente** — chaves de serviços conocidas
- **Ofuscação** — hex escapes, caracteres não-ASCII anómalos
- **Steganography** — ocultação de dados em imagens
- **SSH backdoor** — modificação de `authorized_keys`, `sshd_config`

## Scripts

- `scripts/skills_guard.py` — scanner principal
- `scripts/integrate_hermes.py` — integração com workflow de install do Hermes

## Uso

### 1. Validar skill antes de instalar
```bash
python3 ~/.hermes/scripts/skills_guard.py /caminho/para/skill --verbose
```

### 2. Auditar todas as skills instaladas
```bash
python3 ~/.hermes/scripts/skills_guard.py --check-installed
```

### 3. Validar com source info (trust level)
```bash
python3 ~/.hermes/scripts/skills_guard.py /caminho/para/skill \
  --source-type github \
  --source-id "openai/skills/k8s"
```

### 4. Output JSON (para integração)
```bash
python3 ~/.hermes/scripts/skills_guard.py /caminho/para/skill --json
```

## Trust Levels

| Level | Source | Auto-approve |
|-------|--------|-------------|
| `builtin` | Hermes built-in | ✅ Sempre |
| `official` | optional-skills/ repo | ✅ Se sem critical |
| `trusted` | openai/skills, anthropics/skills | ✅ Se sem critical |
| `community` | ClawHub, GitHub, outros | ❌ Requer validação |
| `unknown` | Source não verificado | ❌ Validação máxima |

## Verdicts

- `APPROVED` — Score ≥70, sem critical/high → instalar
- `LOW_RISK` — Só low findings → Caution, mas instalar ok
- `CAUTION` — Medium findings → Rever documentação
- `REVIEW_REQUIRED` — High findings → Revisar antes de instalar
- `BLOCKED` — Critical findings → NÃO instalar

## Integração Automática

O script `integrate_hermes.py` adiciona hooks ao `hermes skills install`:
- Executa `skills_guard.py` antes de instalar
- Se verdict=BLOQUEADO → aborta installation
- Se verdict=REVIEW_REQUIRED → pide confirmação
- Log de auditoria em `~/.hermes/skills/.hub/audit.log`

## Padrões Detectados (40+ rules)

### Critical
- AWS keys, GitHub tokens, private keys hardcoded
- Prompt injection (`ignore previous`, `disregard instructions`)
- Command injection (`|bash`, `|sh`, `$()|`)
- eval/exec, base64+exec, compile+exec
- dd/fdisk/mkfs/shred
- SSH authorized_keys modification

### High
- API keys / passwords hardcoded
- subprocess(shell=True)
- curl/wget/nc para downloads
- crontab com injection
- Writing to /etc, /usr, /var
- .bashrc / .profile injection
- sudo python/bash

### Medium
- subnetcom com curl/wget/nc
- Hex escapes em strings
- Muitos caracteres não-ASCII consecutivos

## Pitfalls

- Ficheiros `.md`, `.json`, `.yaml` são ignorados (não executáveis)
- Só exts de código são escaneadas (.py, .sh, .js, .ts, etc.)
- False positives em placeholders são filtrados (os.environ, {{key}})
- Markdown README são ignorados propositadamente

## Audit Log

Every install/validation is logged to:
`~/.hermes/skills/.hub/audit.log`

Format: JSON lines com timestamp, event, skill, details, verdict.

## Quando Usar

- **ANTES de instalar** qualquer skill do GitHub, ClawHub, ou source desconhecido
- **Após instalar** — para auditar skills existentes
- **Semanalmente** — como verificação de segurança
- **Antes de executar** uma skill nova pela primeira vez
