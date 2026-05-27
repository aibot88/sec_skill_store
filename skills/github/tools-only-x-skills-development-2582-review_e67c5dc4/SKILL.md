# /review - Unified Multi-Purpose Review (Token-effizient)

Delegiert Reviews an externes Python-Skript. Minimale Claude-Token-Nutzung.

## Ablauf

1. Frage User: "Welche Datei(en)?" (falls nicht angegeben)
2. Frage User: "Welcher Review-Typ?" [code/security/plan]
3. Zeige ZWEI Empfehlungen: bestes bezahltes UND bestes freies Modell
4. Frage ob OK oder anderes
5. Fuehre `python scripts/codex_review.py` aus
6. Zeige Ergebnis OHNE Nachbearbeitung

## Review-Typen mit Empfehlungen (Feb 2026)

| Typ | Best Paid | Best Free | Beschreibung |
|-----|-----------|-----------|--------------|
| `code` | `codex-5.2` (Codex) | `mimo-v2` (MiMo, #1 SWE-bench) | Code Review (Security, Performance, Maintainability) |
| `security` | `o3` (Reasoning) | `deepseek-r1` (Reasoning) | OWASP Top 10, Secrets, Injection, Auth |
| `plan` | `o3` (Reasoning) | `deepseek-r1` (Reasoning) | Architektur, Feasibility, Risk Assessment |

**WICHTIG**: Biete dem User IMMER beide Optionen an (paid + free). Codex immer als Premium-Code-Option nennen.

## Modell-Optionen

### Code Review
| Modell | Preis | Notizen |
|--------|-------|---------|
| `mimo-v2` | FREE | MiMo v2 Flash - #1 SWE-bench (EMPFOHLEN FREE) |
| `devstral` | FREE | Mistral Devstral - Agentic Coding |
| `deepseek-r1` | FREE | DeepSeek R1 reasoning |
| `qwen3-coder` | FREE | 480B MoE Code-Gen |
| `gpt-oss` | FREE | OpenAI open-weight 120B |
| `codex-5.2` | $0.0018/1K | OpenAI Codex 5.2 (EMPFOHLEN PAID) |
| `codex-5.3` | TBD | OpenAI Codex 5.3 (API-Rollout Feb 2026) |
| `codestral` | $0.0003/1K | Mistral code specialist |
| `qwen-coder` | $0.0010/1K | Qwen3 Coder+ |

### Security Review
| Modell | Preis | Notizen |
|--------|-------|---------|
| `deepseek-r1` | FREE | Reasoning (EMPFOHLEN FREE) |
| `llama-405b` | FREE | Meta LLaMA 405B |
| `o3` | $0.002/1K | OpenAI o3 (EMPFOHLEN PAID) |
| `o3-deep` | $0.01/1K | Deep security analysis |
| `codex-5.2` | $0.0018/1K | OpenAI Codex 5.2 |
| `codex-5.3` | TBD | OpenAI Codex 5.3 |
| `gemini-3-pro` | $0.002/1K | Google Gemini 3 Pro |

### Plan/Architecture Review
| Modell | Preis | Notizen |
|--------|-------|---------|
| `deepseek-r1` | FREE | Best reasoning (EMPFOHLEN FREE) |
| `gpt-oss` | FREE | OpenAI open-weight 120B |
| `llama-405b` | FREE | Meta LLaMA 405B |
| `o3` | $0.002/1K | OpenAI o3 (EMPFOHLEN PAID) |
| `codex-5.2` | $0.0018/1K | OpenAI Codex 5.2 |
| `codex-5.3` | TBD | OpenAI Codex 5.3 |
| `gemini-3-pro` | $0.002/1K | Gemini 3 Pro |

## Anweisungen

WICHTIG: Fuehre NUR diese Schritte aus. Keine zusaetzliche Analyse.

```bash
# Code Review (bestes freies Modell)
python scripts/codex_review.py --file "PFAD" --type code --best-free

# Code Review (bestes bezahltes Modell)
python scripts/codex_review.py --file "PFAD" --type code --best

# Security Review
python scripts/codex_review.py --file "PFAD" --type security

# Plan/Architecture Review
python scripts/codex_review.py --file "PFAD" --type plan

# Mit spezifischem Modell
python scripts/codex_review.py --file "PFAD" --type security --model o3

# Alias-Shortcuts (gpt-5.2-codex → codex-5.2, mimo → mimo-v2)
python scripts/codex_review.py --file "PFAD" --model codex
python scripts/codex_review.py --file "PFAD" --model mimo

# Verfuegbare Modelle anzeigen
python scripts/codex_review.py --list-models
python scripts/codex_review.py --list-models --type security
```

## Quick Flags

| Flag | Beschreibung |
|------|-------------|
| `--best` | Bestes bezahltes Modell pro Review-Typ |
| `--best-free` | Bestes freies Modell pro Review-Typ |
| `--model NAME` | Spezifisches Modell (akzeptiert Aliases) |

## Beispiel-Interaktion

```
User: /review
Claude: Welche Datei?
User: backend/app/routers/auth.py
Claude: Review-Typ? [code/security/plan]
User: security
Claude: Empfehlungen:
  - Best Paid: o3 (OpenAI, $0.002/1K)
  - Best Free: deepseek-r1
  Welches Modell?
User: deepseek-r1
Claude: [fuehrt Bash aus, zeigt Output]
```

## KEINE zusaetzliche Verarbeitung

- NICHT den Output zusammenfassen
- NICHT eigene Analyse hinzufuegen
- NICHT Token fuer Erklaerungen verschwenden
- NUR das Skript-Ergebnis anzeigen
