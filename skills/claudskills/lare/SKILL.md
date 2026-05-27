---
name: lare
description: >
  Legal-specific Argument Ranking Engine. Hodnotí právní argumenty 17-sloupcovým
  scoringem (síla, bezpečnost, dopad, riziko + 10 legal-specific kritérií:
  Compliance s novelou 2026, Evidence backing, Time-sensitivity, per-document
  mapping, R-static/R-reversal split, Tom-weight bonus, C-XX/M-XX/N-XX/D-XX
  integrace). Output: priorizovaný seznam argumentů s kategoriemi
  CORE/SUPPORT/CONTEXT/EXCLUDED/SUMMARY a per-document bundles
  (PR/§909/40_06/195). Použití: pre-prioritizace argumentů před F11.x review,
  Phase 2 Verify input, DÁVKA 3, výživné L04, AT podání.

  VŽDY použij tento skill, když Tom (nebo legal/strat) zmíní:
  /lare, lare, argument ranking, ARE matrix, score arguments, prioritize arguments,
  argument bundle, CORE/SUPPORT/CONTEXT/EXCLUDED, ARE_F11, LARE_F11,
  legal argument evaluation, argument scoring, compliance scoring, Tom-weight.
---

# LARE — Legal-specific Argument Ranking Engine

Skill pro **systematické hodnocení a prioritizaci právních argumentů** napříč podáními. Rozšiřuje generický ARE (Argument Ranking Engine z ChatGPT brainstormu 28.4.) o 10 legal-specific kritérií.

## Trigger

Tom napíše: `/lare`, `lare`, "score arguments", "rank arguments", "argument bundle pro DÁVKU X", "prioritize argumenty"

## Vstupy

Skill očekává:
1. **Seznam argumentů** — z `F11_1_NEAPLIKOVANE_ZMENY_PREHLED.md` (53+ kandidátů C-XX/M-XX/N-XX/D-XX/DON'T-XX) NEBO ručně dodaný seznam
2. **Risk assessment** — `99_risk_assessment_PO_F11_0c.md` (známá rizika k jednotlivým argumentům)
3. **Matrix doplnění** — `MATICE_DOPLNENI.md` (P0/P1/P2/P3 priority + status)
4. **Tmonkey extracts** — relevantní soubory z `tmonkey_legal/extracts/` (Tomův intent + ChatGPT vstupy)
5. **Legal okruhy** — `legal_okruhy_v6.json` (paragraf → argument mapping)
6. **Compliance reference** — zákon 268/2025 Sb. (novela účinná 1.1.2026)

## 17-sloupcový framework

### Standard ARE (7 sloupců)

| # | Sloupec | Škála | Popis |
|---|---------|-------|-------|
| 1 | Argument | text | Krátký název / formulace argumentu |
| 2 | S — Síla | 1-5 | Síla podpory pro náš návrh (1=slabá, 5=core) |
| 3 | B — Bezpečnost | 1-5 | Riziko že nás argument poškodí (1=vysoké, 5=bezpečné) |
| 4 | D — Dopad | 1-5 | Dopad na finální rozhodnutí soudu (1=marginální, 5=rozhodující) |
| 5 | R — Riziko | 1-5 | Riziko obrácení proti nám (1=vysoké riziko reversal, 5=stabilní) |
| 6 | Score | num | Vážené skóre (viz vzorec níže) |
| 7 | Category | enum | CORE / SUPPORT / CONTEXT / EXCLUDED / SUMMARY |

### Legal extras (10 sloupců)

| # | Sloupec | Škála | Popis |
|---|---------|-------|-------|
| 8 | C — Compliance | 1-5 | Soulad s novelou 2026 (zák. 268/2025 Sb.) — 1=v rozporu, 5=plně compliant |
| 9 | E — Evidence | enum/list | Backing přílohy: P10, P14, P15, P16... (NULL = bez evidence) |
| 10 | T — Time-sensitivity | 1-5 | Naléhavost (1=dlouhodobé, 5=lhůta běží: § 465f/1=7 dnů, 88+ dní izolace) |
| 11 | Doc-PR | bool | Patří do podání PR (§465a/468b) |
| 12 | Doc-§909 | bool | Patří do návrhu §909 NOZ |
| 13 | Doc-40_06 | bool | Patří do PO naléhavý 40_06 |
| 14 | Doc-195 | bool | Patří do reakce na přípis č.l. 195 |
| 15 | R-type | enum | static (statický fakt) / reversal (může se obrátit, např. emoční formulace) |
| 16 | Tom-weight | 0 / +0.3 | Bonus pro argumenty splňující Tomovy preference (skromnost, ne maximalismus, ne emoční útok) |
| 17 | Lik-tag | text | C-XX / M-XX / N-XX / D-XX / DON'T-XX z F11_1_NEAPLIKOVANE_ZMENY_PREHLED |

## Score vzorec

```
Score_base = (S × 0.30) + (D × 0.30) + (B × 0.20) + (R × 0.10) + (T × 0.10)
Score_legal = Score_base × C_factor + Tom_weight + Evidence_bonus

C_factor = C / 5.0                                    # compliance multiplier (0.2 - 1.0)
Tom_weight = +0.3 pokud splňuje skromnost, jinak 0
Evidence_bonus = +0.2 pokud E ≠ NULL (má přílohu)
```

## Kategorizace (automatická dle Score)

| Score | Category | Akce |
|-------|----------|------|
| ≥ 4.5 | **CORE** | MUSÍ být v hlavním textu podání, prominent placement |
| 3.5-4.4 | **SUPPORT** | Podpůrný argument, druhá vrstva |
| 2.5-3.4 | **CONTEXT** | Pozadí, chronologie, NE jako primary argument |
| < 2.5 | **EXCLUDED** | Vyřadit z aktuálního podání (ne nutně navždy) |
| meta | **SUMMARY** | Shrnutí na konci podání (1-3 odstavce, ne new arguments) |

## Workflow

### Krok 1: Inventura argumentů
- Načti `F11_1_NEAPLIKOVANE_ZMENY_PREHLED.md`
- Načti `MATICE_DOPLNENI.md`
- Doplň manuálně dodané argumenty (z tmonkey extracts, Tomových komentářů)
- Output: pracovní seznam (CSV / Python list)

### Krok 2: Skórování
Pro každý argument:
1. Hodnotit **S, B, D, R, C, T** (1-5 dle definicí)
2. Identifikovat **E** (přílohy které argument backují) — link na P-XX
3. Mapovat **Doc-PR/§909/40_06/195** (může být ve více současně)
4. Klasifikovat **R-type** (static vs. reversal — emoční argumenty často reversal)
5. Aplikovat **Tom-weight** (+0.3 pokud splňuje skromnost — žádné emoční útoky, žádné maximalistické formulace, žádné předbíhání diagnóz)
6. Připojit **Lik-tag** (C-XX/M-XX/N-XX/D-XX/DON'T-XX)
7. Vypočítat **Score**
8. Přiřadit **Category**

### Krok 3: Compliance check (KRITICKÉ)
Pro každý argument C < 3 → **STOP a re-formulovat**, jinak vyřadit. Konkrétně kontrolovat:
- Soulad s § 465a-j ZŘS (PR — Předběžné rozhodnutí, novela 2026)
- Žádné citování paragrafů zrušených novelou 268/2025 Sb.
- Žádná zamlčená procesní pravidla

### Krok 4: DON'T check (formulační zákazy)
Pro každý argument grep proti DON'T-01 až DON'T-14 (z F11_1_NEAPLIKOVANE_ZMENY_PREHLED). Hit = re-formulovat nebo EXCLUDED.

### Krok 5: Per-document bundle
Pro každý cílový dokument (PR / §909 / 40_06 / 195):
- Filtruj argumenty s `Doc-X = true`
- Seřaď dle Score sestupně
- Limit (např. CORE max 8, SUPPORT max 12, CONTEXT max 6)
- Output: `LARE_F11_<doc>.md` se sestavou (Argument | Score | Category | Lik-tag | E)

### Krok 6: Audit log
Zapsat do `LARE_audit_<timestamp>.txt`:
- Kdo (instance), kdy, kolik argumentů
- Distribuce Score (avg, median, min, max)
- Compliance failures (C < 3) + důvody
- DON'T hits + akce
- Tom-weight bonus distribuce

## Výstupy

V adresáři `<rizeni>/optimize_output_F11/LARE/`:
- `LARE_F11_master.csv` — všech 17 sloupců, master matrix
- `LARE_F11_PR.md` — bundle pro PR podání (Score-řazený, kategorizovaný)
- `LARE_F11_§909.md` — bundle pro §909 návrh
- `LARE_F11_40_06.md` — bundle pro PO naléhavý
- `LARE_F11_195.md` — bundle pro reakci na č.l. 195
- `LARE_audit_<timestamp>.txt` — audit log
- `LARE_excluded.md` — vyřazené argumenty s důvodem (pro DÁVKU 3 nebo budoucí podání)

## Pravidla pro instance

- **Strat/Legal používá** LARE jako **decision support**, NE jako autoritativní filtr. Score je vstup pro lidské rozhodnutí Toma + Lika.
- **Tom má final say** — může override jakýkoliv Score / Category. Override se loguje do audit (důvod).
- **NEZAPRACOVÁVAT EXCLUDED do podání** bez explicitního Tomova „beru zpět EXCLUDED" — i když Score pak třeba poroste díky novému evidence.
- **Compliance failure** (C < 3) = HARD BLOCK, nikdy nelze override bez právního přepisu.
- **DON'T hit** = HARD BLOCK, re-formulovat povinné.

## Integrace s ostatními skills

- **filing-pipeline Phase 1.4 Zestihlení** — LARE běží v této fázi nebo těsně před ní (vstup: po inventuře, po konsolidaci, ale před zestihlením)
- **locks-workflow F10.2 STRAT lock** — strat při LOCK 2 ověřuje že texty obsahují LARE-CORE argumenty a NE EXCLUDED
- **legal_compliance_check.py** — paralelní k LARE Compliance sloupci, ne náhrada (compliance check je deterministický grep paragrafů, LARE je hodnotící)

## Engine implementace (volitelné)

Skill funguje **manuálně i automatizovaně**. Pro automatizaci coder vyvíjí `arematrix.py` (queue task #2316, P2):
- Vstup: F11_1_NEAPLIKOVANE_ZMENY_PREHLED.md, 99_risk_assessment, MATICE_DOPLNENI, extrakty, legal_okruhy_v6.json
- Output: ARE_F11_1.xlsx + per-document bundles + audit log
- Reusable pro DÁVKU 3, výživné L04, AT podání

Bez `arematrix.py` skill běží v Claude Code session manuálně (legal/strat instance).

## Reference

- ChatGPT zdroj: `tmonkey_legal/extracts/2026-04-28_navrh_na_po_styk_legal.md` (linie 1212+ ARE/RDT toolkit)
- Lik LEGAL_NOTES: `C:/Users/tom/Documents/tmonkey_legal/ARE_toolkit_20260428/LEGAL_NOTES.md`
- Original ARE template (ChatGPT): `L:/Lukasek/Downloads/ARE_toolkit.zip`
- Lik msg #35 (28.4. 08:12): `C:/Users/tom/Documents/instance_comm.json`
- Strat ideas: `L:/Lukasek/T000_Strat/ideas.md` #12 (ARE), #13 (ALRSS)
- F11_1 přehled: `C:/Users/tom/Documents/rizeni/pece_Matousek_909/doplneni_c1/F11_1_NEAPLIKOVANE_ZMENY_PREHLED.md`

## Verzování LARE

LARE skill samotný má verze (jak se vyvíjí — přidávají sloupce, mění váhy):

| Version | Datum | Změna |
|---------|-------|-------|
| v1.0 | 2026-04-28 | Initial — 17 sloupců, Score vzorec, 5 kategorií, per-document mapping, Tom-weight |

Nová verze = update tohoto SKILL.md + bump version.
