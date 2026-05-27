---
name: legal-total-analysis
description: Lean meta-skill pre-flight audit DÁVKY právního podání před F1X.4 capsule build a ISDS odesláním. Generuje GO/NO-GO verdict ze 3 unique kroků (DON'T grep, Cross-check, Verdict) + reuse existing optimize/audit výstupů 91-99 + audit_report. Trigger: "total analysis", "total analyza", "pre-flight", "GO/NO-GO check", "before capsule", "before ISDS", "F13 audit", "audit dávky".
---

# Legal Total Analysis — Lean pre-flight audit

Meta-skill který spojí **existující výstupy** (`91_redundancy_analysis.md` až `99_risk_assessment.md` + `kontrola_*_audit_report.md`) s **3 unique kroky** (DON'T grep, Cross-check, Verdict) a vytvoří **master report s GO/NO-GO doporučením**.

## Princip — varianta C (lean)

Skill **NEDUPLIKUJE** práci, kterou už dělají jiné skripty (optimize, risk-assessment, compliance). Místo toho:

1. **Načte signály** z existing 91-99 + audit_report (skóre, warnings, blockery)
2. **Provede 3 unique kroky**, které žádný jiný skript nedělá
3. **Sloučí vše** do GO/NO-GO master reportu

Ušetří 4-6 hodin manuálního auditu na ~30 s automatu.

## Kdy spustit

- **Před F1X.4 capsule build** (povinný pre-flight gate)
- **Před ISDS odesláním** (final check)
- **Po každé F1X.Y build iteraci** (validation gate)
- Tom napíše: "total analysis", "pre-flight", "GO/NO-GO check", "audit dávky"

## Použití

```bash
# Plná analýza DÁVKY (auto-detect existing výstupů)
python total_analysis.py \
  --folder rizeni/pece_Matousek_909/doplneni_c1/optimize_output_F13/ \
  --matrix rizeni/pece_Matousek_909/doplneni_c1/ARE_F11_1_LEGAL.md \
  --prehled rizeni/pece_Matousek_909/doplneni_c1/F11_1_NEAPLIKOVANE_ZMENY_PREHLED.md

# Inline bash wrapper (pre-flight check)
bash total_analysis.sh F13
```

### Parametry

| Parametr | Default | Popis |
|----------|---------|-------|
| `--folder` | (povinný) | Adresář s dokumenty DÁVKY (např. `optimize_output_F13/`) |
| `--matrix` | (povinný) | ARE matice s CORE argumenty + DON'T list |
| `--prehled` | (povinný) | Master přehled neaplikovaných změn |
| `--optimize-dir` | (auto: `optimize_output_F11/`) | Adresář s existing 91-99 výstupy |
| `--audit-report` | (auto-detect `kontrola_*_audit_report.md`) | Existing audit report |
| `--cross` | (auto: předchozí F-verze) | Předchozí dávka pro N-XX cross-check |
| `--mode` | `full` | `full` / `quick` (jen DON'T + Verdict, bez Cross-check) |
| `--strict` | false | GO vyžaduje 100% pass všech checků |
| `--output` | (auto: `total_analysis_<ts>/`) | Výstupní adresář |

## Workflow — 3 unique kroky + reuse

### Krok R — Reuse existing výstupů (~5 s)

Načte signály z existing souborů:

| Soubor | Signál |
|--------|--------|
| `91_redundancy_analysis.md` | redundance score, duplicitní pasáže |
| `92_impact_simulation.md` | predikce dopadu změn |
| `93_optimization_log.md` | log aplikovaných změn |
| `94_optimization_report.md` | overall optimize verdict |
| `96_matrix_updates.md` | matrix delta |
| `97_distribution_report.md` | per-document distribuce |
| `98_preflight_report.md` | pre-existing preflight signály |
| `99_risk_assessment_*.md` | M-XX risk matice (RED/ORANGE/YELLOW) |
| `kontrola_*_audit_report.md` | audit findings |

Z každého extrahuje: score (pokud je), warnings count, RED/ORANGE markery, GO/NO-GO hints.

### Krok 1 — DON'T grep (~10 s)

Pro všech **N DON'T zákazů** z `--matrix` (sekce A.4.1) provede regex grep přes všechny `.md` v `--folder`:
- detekuje varianty (lemma stem matching: "zatajuje" / "zatajila" / "zataj")
- reportuje: soubor, řádek, kontext (3 řádky před/po)
- **Hard-fail rule:** počet violations > 0 → automaticky NO_GO

### Krok 2 — Cross-check s předchozí dávkou (~15 s)

Pokud `--cross` zadáno (nebo auto-detect předchozí F-verze):
- porovná petitové formulace (regex `\\bnavrh(uje[mnt]?|ujeme)?\\b` → následující odstavec)
- detekuje rozpory v narativu (datum, dny, sp. zn., osoby)
- detekuje opuštěné argumenty (CORE z předchozí, který v aktuální není)

### Krok 3 — GO/NO-GO verdict (~5 s)

Sloučí signály z Reuse + 3 unique kroků do `go_no_go.json`:

```json
{
  "verdict": "GO" | "CONDITIONAL_GO" | "NO_GO",
  "scores": {
    "reuse_aggregated": {...},
    "dont_violations": {"count": 0, "status": "OK"},
    "crosscheck": {"conflicts": 0, "status": "OK"}
  },
  "blocking_issues": [],
  "warnings": [],
  "next_steps": [],
  "recommendation": "..."
}
```

### Vetovací logika (hard-fail rules)

- DON'T violations > 0 → **NO_GO** (vždy)
- Reuse signál RED v 99_risk → **NO_GO**
- Compliance score (z 94_optimization nebo audit) < 80 → **NO_GO**
- Cross-check rozpor v petitu → **NO_GO**
- Capsule blocker count (z 98_preflight) > 3 → **NO_GO**
- Jinak: warnings > 0 → **CONDITIONAL_GO**, jinak **GO**

## Výstupy

```
total_analysis_<YYYY-MM-DD_HHMM>/
├── TOTAL_ANALYSIS_REPORT.md       # Master report (executive summary, score karty, top issues)
├── go_no_go.json                  # Machine-readable verdict
├── 03_dont_violations.md          # Krok 1 detail
├── 05_crosscheck.md               # Krok 2 detail (jen full mode)
└── reuse_signals.json             # Krok R extrahované signály
```

## Integrace

### Volá

| Tool | Účel | Závislost |
|------|------|-----------|
| `legal_compliance_check.py` | Compliance re-check (pokud audit_report chybí) | volitelná |
| `git log` (pokud .git) | Cross-check baseline | volitelná |

### Předává handoff

| Cíl | Triger | Payload |
|-----|--------|---------|
| `locks-workflow F10.2 STRAT` | verdict = GO/CONDITIONAL_GO | `go_no_go.json` |
| `filing-pipeline Phase 2 Verify` | verdict = CONDITIONAL_GO | warnings list |
| `t002 capsule build` | verdict = GO + Tom approval | folder path + verdict |

### Skill NIKDY:

- Neodesílá podání (STOP ORDER #1452 platí absolutně)
- Nepřepisuje source dokumenty v `--folder` (read-only)
- Nepřejmenuje soubory (versioning dělá legal/strat ručně)
- Nepřebírá rozhodnutí Toma (verdict = doporučení, ne automat)

## Volání ze skill toolu

Když Tom napíše trigger ("total analysis", "pre-flight", "GO/NO-GO check"), spusť:

```bash
python C:/Users/tom/.claude/plugins/marketplaces/lg13/plugins/lg13-skills/skills/legal-total-analysis/scripts/total_analysis.py \
  --folder <DÁVKA folder> \
  --matrix <ARE matice> \
  --prehled <přehled>
```

Pokud Tom nezadá vstupy → ptej se postupně (folder, matrix, prehled).

## Známá omezení

- **DON'T grep** používá lemma stem (regex) — pokud zákaz není v matrix, neodchytí
- **Reuse signal extrakce** je heuristická (regex přes markdown) — pokud se formát 91-99 změní, parser potřebuje update
- **Cross-check** porovnává jen markdown text, ne PDF
- **Verdict je doporučení** — final autorita Tom + locks-workflow

## Konfigurace pro různé DÁVKY

Skill je generic. Pro každou DÁVKU se nastavují vstupy:

| DÁVKA | --folder | --matrix | --optimize-dir |
|-------|----------|----------|----------------|
| F13 (DÁVKA 2) | `optimize_output_F13/` | `ARE_F11_1_LEGAL.md` | `optimize_output_F11/` |
| Budoucí F14 | `optimize_output_F14/` | `ARE_F14_LEGAL.md` | `optimize_output_F13/` |
| AT podání | `at_podani/` | `ARE_AT_LEGAL.md` | (žádný — použij `--no-reuse`) |

---

*Lean varianta C — neopakuje práci jiných skriptů, pouze 3 unique kroky + integrace existing výstupů. Source: LEGAL_TOTAL_ANALYSIS_SKILL_SPEC.md (full 9-krok varianta), Tom architectural decision 2026-04-28.*
