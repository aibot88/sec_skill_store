---
name: anomaly-report
description: Formátování nálezu (z bug-hunter / dead-code-hunter / perf-hunter / security-auditor / ručního pozorování) do bloku v <connector>/docs/anomalies.md + draft Jira issue body. Přiděluje [CONN-NNN] ID lokálně per connector podle pořadí v existujícím anomalies.md.
---

# /anomaly-report

Skill převádí ⚠️ nález z hunters nebo ručního pozorování na strukturovaný blok v `<connector>/docs/anomalies.md`. Formálně psaný (3. osoba, pasivní rod), s evidencí `path:line`, severity, statusem. Po zápisu navrhuje navázat `/jira-from-context --from anomaly`.

## Kdy použít

- Po `bug-hunter` / `dead-code-hunter` / `perf-hunter` / `security-auditor` findings, které vyžadují formalizaci.
- Při ručním objevu (uživatel řekne „⚠️", „anomálie", „bug v X", „divně se chová Y").
- Před založením Jira ticketu — anomaly entry je primární evidence, Jira jen zrcadlí.

Aktivace: `/anomaly-report <connector> [...args]` nebo automaticky při ⚠️/anomaly frázích.

## Vstupy

- **`<connector>`** (povinné) — název adresáře v `${PROJECT_ROOT}/Connectors/`.
- **`--from <source>`** (volitelné) — `bug-hunter | dead-code-hunter | perf-hunter | security-auditor | manual`. Default `manual`.
- **`--source <path>`** (volitelné) — cesta k hunter reportu nebo investigation souboru, ze kterého se má finding extrahovat.
- **`--severity <level>`** (volitelné) — `kriticka | vysoka | stredni | nizka`. Pokud nezadán, odvodit z hunter severity (high→vysoka, med→stredni, low→nizka) nebo se zeptat.

## Workflow

1. **Resolve cest** — `<connector>/docs/anomalies.md`. Pokud chybí, načíst šablonu z `${PROJECT_ROOT}/Connectors.Analyst/templates/connector-docs/anomalies.md.tmpl` a navrhnout vytvoření prázdné kostry (s explicit souhlasem).
2. **Přidělit ID** — scan existujícího `anomalies.md` na `\[CONN-(\d+)\]`, najít max NNN, přidělit `max+1` (3-místné, padováno nulami: `CONN-001`, `CONN-042`). Per-connector lokální namespace — kolize napříč connectory nevadí (každý má vlastní `anomalies.md`).
3. **Extrakce findingu** — pokud `--source` zadán, načíst soubor a vytáhnout: stručný titul, evidence `path:line`, snippet, severity, předpokládaný root cause. Jinak vyžádat od uživatele (vstupy: titul, evidence, popis).
4. **Sestavit blok** podle struktury níže.
5. **Předložit ke schválení** (viz [`feedback_approval_first`](../../memory/feedback_approval_first.md)) — ukázat:
   - cílový soubor a `[CONN-NNN]` ID,
   - rozsah (append entry / vytvořit nový soubor z šablony),
   - preview prvních ~15 řádků bloku,
   - otázku „zapsat?".
6. **Po souhlasu** — append do `anomalies.md` (`Edit` na soubor; pokud nově vytvářen, `Write` s šablonou + první entry). Update přehledové tabulky na začátku souboru.
7. **Navrhnout navázat** — `/jira-from-context --from anomaly --source <connector>/docs/anomalies.md#CONN-NNN`. Bez auto-spuštění.

## Struktura entry

```markdown
### `[CONN-NNN]` — <stručný titul, 1 řádek>

**Závažnost:** <🔴 KRITICKÁ | 🟠 VYSOKÁ | 🟡 STŘEDNÍ | 🟢 NÍZKÁ>
**Status:** open
**Aktualizováno:** <YYYY-MM-DD>
**Vlastník:** nepřiřazeno
**Zdroj nálezu:** <bug-hunter | manual | …>

**Popis:**
<2-5 vět, 3. osoba pasivní rod, žádné „my"/„Novák"/„tým".>

**Místo v kódu / DB:**
- `path/to/File.cs:42`
- `[Schema].[dbo].[StoredProc]` (pokud relevantní)

**Snippet:**
` ` `csharp
<10-20 řádků nejvíce ilustrativního kódu>
` ` `

**Reprodukce:**
<krok-po-kroku nebo SQL dotaz pro ověření, ne-li jasné z evidence>

**Dopad:**
<funkční / datový / bezpečnostní; recoverable yes/no>

**Předpokládaný root cause:**
<hypotéza, jasně označená jako hypotéza, ne fakt>

**Navržené řešení:**
1. <krátkodobě>
2. <dlouhodobě / prevence>

**Související tickety:**
<prázdné při založení; /jira-from-context sem zapíše Jira URL>
```

## Pravidla obsahu

- **Formální 3. osoba, pasivní rod** — [`feedback_no_personification`](../../memory/feedback_no_personification.md). Žádné „myslíme", „Novák zjistil", „při analýze jsme našli". Místo toho „Při statické analýze byl identifikován…".
- **Path:line evidence povinná** — bez ní entry neuvádět.
- **Hypotézy explicitně označit** jako hypotézy, ne fakta („pravděpodobně copy-paste chyba", ne „je to copy-paste chyba").
- **Severity mapování** z hunter reportů:
  - security-auditor High / bug-hunter P3 (`throw ex`) / kritická data loss → 🔴 KRITICKÁ
  - bug-hunter High (P1, P6) / perf High N+1 v hot pathu → 🟠 VYSOKÁ
  - bug-hunter Med / perf Med / security Med → 🟡 STŘEDNÍ
  - bug-hunter Low / dead-code Low / cosmetic → 🟢 NÍZKÁ

## Gates

- **1 schválení uživatelem před zápisem.** Žádný auto-apply.
- **Žádný Jira write** v tomto skillu — pouze `<connector>/docs/anomalies.md`. Jira navazuje `/jira-from-context` (viz [`feedback_no_jira_writes`](../../memory/feedback_no_jira_writes.md)).
- Při vytváření nového `anomalies.md` z šablony → samostatný gate (souhlas s kostrou + souhlas s první entry).

## Výstupní artefakty

- Nový blok v `<connector>/docs/anomalies.md` (případně nově vytvořený soubor z šablony).
- Updatovaná přehledová tabulka na začátku souboru.
- Update statistik (pokud existují).
- Návrh příkazu `/jira-from-context --from anomaly ...` v terminálu (ne write).

## Návaznosti

- **Před:** typicky `bug-hunter` / `perf-hunter` / `security-auditor` / `dead-code-hunter` reporty (Phase 2).
- **Po:** `/jira-from-context --from anomaly` (Phase 3) — založení Jira ticketu se zpětným odkazem.
- **Volitelně:** skill může na vyžádání spustit příslušného huntera před formalizací (pokud uživatel řekne „⚠️ něco divného v X.cs" bez konkrétního finding).
