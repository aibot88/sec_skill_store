---
name: dark-factories-publish
description: Versioniert alle Dark-Factories aus ~/Projects/dark-factories/ nach meokemmer-jpg/kemmer-knowledge-system GitHub (Subdir dark-factories/). Filtert Runtime-State (runs/, output/, learnings/, __pycache__, .venv, STOP.flag, secrets). Triggers "publish dark factories", "push dfs", "versioniere dark-factories".
version: 1.0.0
crux-mk: true
aktiviert: 2026-04-19
meta-ebene: E2
---

# Skill: dark-factories-publish [CRUX-MK]

## Zweck

Martin-Direktive 2026-04-19: *"Bitte auch alle Dark Faktories auf GitHub Versionieren"*.

Schwester-Skill zu `github-bauplan-publish`. Pusht nur `dark-factories/`-Subtree.

## Scope

**Source:** `C:/Users/marti/Projects/dark-factories/DF-*`
**Target:** `github.com/meokemmer-jpg/kemmer-knowledge-system` → `dark-factories/`

**Aktuell versioniert:** DF-02, DF-03, DF-04, DF-05, DF-07, DF-08 (6 DFs, 336 kB Code).

## Filter (kritisch fuer Security)

**Was NICHT gepusht wird:**
- `runs/` + `output/` + `learnings/` — Runtime-State (kann Martin-privat sein)
- `__pycache__/` + `*.pyc` + `.venv/` — Python-Build-Artefakte
- `STOP.flag` — Local-only Kill-Switch
- `.env` + `*.env.*` + `*.key` + `*.pem` — Secrets
- `logs/` + `*.log` — Debug-Output

**Was gepusht wird:**
- `config.py`, `run.py`, `*.py` (code)
- `README.md`, `WARGAME.md` (docs)
- `*.bat`, `*.ps1`, `*.sh` (setup scripts)
- `.yaml`, `.toml`, `.json` (config, wenn nicht secret)

## Pre-Flight-Checks

1. **Secret-Scan:** `grep -rEn "xai-[a-zA-Z0-9]{20,}|sk-[a-zA-Z0-9]{20,}|gho_[a-zA-Z0-9]{20,}"` → muss **empty** sein
2. **Size-Check:** jede DF <5 MB (ohne Runtime-State)
3. **Gitignore-Check:** `dark-factories/.gitignore` muss existieren

## Workflow

```bash
# 1. Clone repo
cd /tmp && rm -rf kks-df && gh repo clone meokemmer-jpg/kemmer-knowledge-system kks-df
cd kks-df && mkdir -p dark-factories

# 2. Copy filtered
for DF in DF-02-kpm-shadow DF-03-longevity-research DF-04-bias-calibration \
         DF-05-auto-commit-push DF-07-model-audit DF-08-docs-generator; do
  SRC="/c/Users/marti/Projects/dark-factories/$DF"
  DST="dark-factories/$DF"
  [ -d "$SRC" ] && mkdir -p "$DST" && \
    (cd "$SRC" && find . -type f \
      ! -path "./runs/*" ! -path "./output/*" ! -path "./learnings/*" \
      ! -path "./__pycache__/*" ! -path "*/__pycache__/*" \
      ! -name "*.pyc" ! -name "STOP.flag" ! -name "*.env" \
      ! -path "./.venv/*" \
      -exec cp --parents "{}" "/tmp/kks-df/$DST/" \;)
done

# 3. Secret-Scan
cd /tmp/kks-df
grep -rEn "xai-[a-zA-Z0-9]{20,}|sk-[a-zA-Z0-9]{20,}|gho_[a-zA-Z0-9]{20,}" dark-factories/ \
  && { echo "SECRETS FOUND — ABORT"; exit 1; }

# 4. Commit + Push
git add dark-factories/
git commit -m "dark-factories: sync <timestamp> [CRUX-MK]"
git push origin main
```

## Integration mit DF-08

DF-08 (Docs-Generator) hat dark-factories/ als Target (`TARGET_REPOS` in config.py).
**Konsequenz:** Wenn DF-08 weekly-scan laeuft, werden fuer JEDE DF automatisch
README + CONTRIBUTING + Flow-Tests generiert (Copilot-Delegate, 0 Claude-Tokens).

## Schedule-Empfehlung

**Option A — Manuell** (nach jedem groesseren DF-Update):
```
Skill-Trigger: "publish dark factories"
```

**Option B — Scheduled** (weekly Sonntag 05:00 nach DF-08):
```powershell
schtasks /create /tn "DarkFactories-Publish" ^
  /tr "bash C:\Users\marti\.claude\scripts\publish-dark-factories.sh" ^
  /sc weekly /d SUN /st 05:00 /f
```

## rho-Impact

- **Versioning-Value:** Git-History pro DF = Evolution-Tracking + Rollback-Fähigkeit
- **Cross-Device-Sync:** Martin kann auf anderen Geraeten DFs clonen + starten
- **Disaster-Recovery:** Bei HD-Verlust sind alle DFs wiederherstellbar
- **Zusammenarbeit:** Future Dev-Helfer koennen PRs erstellen
- **Token-Kosten:** 0 (gh-api + filesystem, kein LLM)

## Falsifikations-Bedingung

- Secret-Scan catcht einen Key → Rule-Verscharfung + F11/F12-Analogie-Update
- Push-Failure repeated → Token-Scope-Check noetig
- Runtime-State versehentlich gepusht → .gitignore erweitern

## Beziehung

- **Schwester-Skill:** `github-bauplan-publish` (Bauplaene/Findings)
- **Target-Integration:** DF-08-docs-generator liest dark-factories/ als Scan-Target
- **Rule:** `rules/kb-hygiene.md` (SUPERSEDED-Disziplin + Canon-Prinzip)

[CRUX-MK]
