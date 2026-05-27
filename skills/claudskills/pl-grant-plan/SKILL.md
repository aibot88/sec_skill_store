---
name: pl-grant-plan
description: "Interactive planner for Polish national grants: FESL/FERS/NOWEFIO/NIW/CERV/ESC/KPO/FEnIKS/RITA/Slaskie Lokalnie. Decision tree for program selection, indicator mapping, budget planning. Triggers: plan projekt krajowy, zaplanuj FESL, plan FERS, plan NOWEFIO, nowy wniosek krajowy, grant krajowy."
---

# PL Grant Plan — Interactive Polish National Grant Planner

Interaktywny planer projektow krajowych: FESL, FERS, NOWEFIO, NIW/Korpus Solidarnosci, CERV, ESC, KPO, FEnIKS, RITA, Slaskie Lokalnie.

---

## Dependency

**FIRST invoke grant-core** for shared writing rules. All text output MUST pass through grant-core:
- forbidden-words.md — no banned phrases
- writing-patterns.md — rotation of 5 patterns
- anti-ai-naturalness.md — natural, human-like language
- quality-checks.md — 15-point pre-submission checklist

---

## 6-Step Interactive Flow

Work through steps sequentially. At each step ASK the user before proceeding. Never skip steps.

### STEP 1: Choose Program

**Goal:** Select the right grant program based on organization profile and project goals.

Actions:
1. Ask: "Jaki rodzaj projektu planujesz? (integracja spoleczna / edukacja / wolontariat / srodowisko / cyfryzacja / spoleczenstwo obywatelskie)"
2. Ask: "Jaki region? (cala Polska / woj. slaskie / Partnerstwo Wschodnie)"
3. Ask: "Jaki budzet orientacyjny? (do 7.5K / do 40K / do 400K / do 1.2M / powyzej 1M)"
4. Reference `rules/program-catalog.md` for decision tree:
   - NGO spoleczenstwo obywatelskie, maly budzet -> NOWEFIO P1-P3 lub Slaskie Lokalnie
   - NGO regranterzy, duzy budzet -> NOWEFIO P4
   - Aktywna integracja, woj. slaskie -> FESL 7.2
   - Edukacja, transformacja, woj. slaskie -> FESL 6.x / 10.x
   - Kompetencje cyfrowe -> FERS 1.9 lub KPO C2.1.3
   - Wolontariat -> NIW/Korpus Solidarnosci lub ESC
   - Srodowisko, GOZ -> FEnIKS
   - Prawa obywatelskie, UE -> CERV
   - Wspolpraca z krajami Partnerstwa Wschodniego -> RITA
5. Confirm selected program with user

**Output:** Confirmed program name + key parameters (budzet, system skladania, wklad wlasny)

---

### STEP 2: Define Problem and Needs

**Goal:** Sformulowac problem spoleczny, na ktory odpowiada projekt.

Actions:
1. Ask: "Jaki problem chcesz rozwiazac? Opisz w 2-3 zdaniach."
2. Ask: "Czy masz dane/diagnoze potwierdzajaca problem? (badania, statystyki GUS, dane lokalne)"
3. Ask: "Kto jest grupa docelowa? Ile osob/organizacji?"
4. Verify alignment with program priorities:
   - FESL: zgodnosc z SZOP, cele szczegolowe dzialania
   - NOWEFIO: zgodnosc z priorytetami P1-P4
   - FERS: zgodnosc z celami szczegolowymi dzialania
   - FEnIKS: zgodnosc DNSH, cele srodowiskowe
5. Help formulate problem using evidence-based language (nie "wedlug nas" ale "dane GUS wskazuja")

**Output:** Problem statement, target group profile, data sources

---

### STEP 3: Map Indicators and Results

**Goal:** Zdefiniowac wskazniki produktu i rezultatu zgodne z programem.

Actions:
1. Reference program-specific indicator catalogs:
   - FESL: wskazniki z SZOP, obligatoryjne i wybrane
   - FERS: wskazniki CST2021
   - NOWEFIO: wskazniki twarde i miekkie (mierzalne)
   - FEnIKS: wskazniki srodowiskowe + DNSH
2. Ask: "Jakie konkretne produkty powstana? (szkolenia, publikacje, narzedzia, events)"
3. For each product define: indicator name, unit, target value, measurement method
4. Map indicators to evaluation criteria weights (see program-specific rules)
5. Ensure minimum required indicators are covered

**Output:** Indicator matrix (name, value, source, verification method)

---

### STEP 4: Design Activities

**Goal:** Zaplanowac dzialania projektowe i harmonogram.

Actions:
1. Based on problem + indicators, propose activity structure:
   - Task 1: Rekrutacja i diagnoza
   - Task 2-N: Dzialania merytoryczne (szkolenia, warsztaty, doradztwo, etc.)
   - Task N+1: Ewaluacja i upowszechnianie
2. For each task define: opis, okres, odpowiedzialny, koszty szacunkowe
3. Build Gantt-style timeline
4. Check compliance with program rules:
   - FESL: kwoty ryczaltowe dla projektow <200K EUR
   - NOWEFIO: max 20% koszty administracyjne
   - FEnIKS: 5-letnia trwalosc
5. Verify accessibility requirements (FESL: Standard Minimum, dostepnosc)

**Output:** Activity plan with timeline, responsibilities, cost estimates

---

### STEP 5: Plan Budget

**Goal:** Stworzyc budzet zgodny z zasadami programu.

Actions:
1. Reference `rules/budget-rules-pl.md` for program-specific rules
2. For each activity, assign cost categories:
   - Koszty personelu (wynagrodzenia, umowy zlecenia)
   - Koszty merytoryczne (materialy, catering, druk, transport)
   - Koszty posrednie (FESL ryczalt %, FEnIKS 7%)
   - Sprzet i wyposazenie (limity cross-financing)
3. Check: wklad wlasny (NOWEFIO P2-P3: min 10%, FEnIKS: 15%, FESL: wg dzialania)
4. Check: standard cen rynkowych (FESL) lub limity programowe
5. Verify: eligible vs ineligible costs per program
6. Calculate total + verify within program limits

**Output:** Budget table (category, unit, quantity, unit cost, total, funding source)

---

### STEP 6: Generate Concept Note

**Goal:** Wygenerowac strukturalny dokument koncepcyjny.

Actions:
1. Compile all data from Steps 1-5
2. Generate `concept-[PROGRAM]-[ACRONYM].md` with sections:
   - Tytul projektu i akronim
   - Program i dzialanie
   - Wnioskodawca (i partnerzy jesli dotyczy)
   - Diagnoza problemu i potrzeb
   - Cele (ogolny + szczegolowe w formacie SMART)
   - Grupa docelowa z charakterystyka
   - Dzialania i harmonogram
   - Wskazniki produktu i rezultatu
   - Budzet (podsumowanie)
   - Analiza ryzyka
   - Trwalosc rezultatow
   - Informacja i promocja (zgodna z wymaganiami programu)
3. Run grant-core quality checks
4. Save to user's preferred location

**Output:** Complete concept note ready for team review

---

## Quick Reference

| Step | Pytanie kluczowe | Plik regul |
|------|-------------------|------------|
| 1 | Jaki program? | program-catalog.md |
| 2 | Jaki problem? | fesl-specs / fers-specs / nowefio-specs |
| 3 | Jakie wskazniki? | program-specific specs |
| 4 | Jakie dzialania? | program-specific specs |
| 5 | Jaki budzet? | budget-rules-pl.md |
| 6 | Generuj concept note | ALL rules |

---

## Error Recovery

- If user changes program mid-flow -> go back to Step 1, keep Step 2 data if still relevant
- If budget exceeds program limits -> reduce scope or split into phases
- If indicators don't match program catalog -> suggest closest valid indicators
- If organization not eligible -> suggest alternative program from catalog
