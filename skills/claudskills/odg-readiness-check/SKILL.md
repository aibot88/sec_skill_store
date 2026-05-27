---
name: odg-readiness-check
description: Visualizza e valida lo stato finalization ODG per una giornata specifica — 6 semafori compliance (cast/location/permessi/elementi/mezzi/pasti) + readiness interno + stato firma DP. Riusa engine esistenti T601 Compliance Matrix + T602 finalizationRules. Uso tipico: prima di firmare ODG, Direttore di Produzione invoca la skill per vedere a colpo d'occhio se la giornata è finalizzabile.
---

# Skill: odg-readiness-check

## Scopo

Il flusso firma ODG (T602) richiede che il Direttore di Produzione sappia **in 5 secondi** se una giornata può essere firmata. Questa skill:

1. Carica i moduli engine esistenti (`lib/odg/finalizationRules.ts`, `lib/schedule/compliance/matrix.ts`)
2. Genera uno snapshot testuale readable del `OdgFinalizationState` per il dayNumber richiesto
3. Se invocata in programming context, può validare che la UI (`components/odg/ODGReadinessPanel.tsx`) sta renderizzando correttamente
4. Se invocata in planning context (pre-firma), informa il DP sullo stato 6 semafori + blocker + warnings

## Quando invocarmi

- L'utente dice "odg readiness", "check ODG day N", "semafori firma ODG", "/odg-readiness-check"
- Prima di invocare la UI firma DP su una giornata specifica
- Post-cambiamento upstream (drag strip, revoca permesso) per verificare staleness firma
- In development: come test vitale del compliance matrix engine

## Prerequisiti

- Project esistente con `schedule.strips` popolato (scene + dayBreak)
- `ComplianceContext` completo (permits, castRoster, locationRoster, breakdown, troupe, rentals)
- Opzionale: `signature` esistente su `DayOdg` se già firmato (per test staleness)

## Flusso

### Step 1 — Parse input

Input atteso dall'utente:
- `dayNumber` (numerico, richiesto)
- `projectId` o context corrente (opzionale, default al progetto attivo)

### Step 2 — Invoca engine

Carico via require/import:
```typescript
import { computeFinalizationState, getOdgExportReadiness } from "@/lib/odg/finalizationRules";
import { buildComplianceMatrix, summarizeMatrix } from "@/lib/schedule/compliance/matrix";
```

Esecuzione (pseudocode):
```
1. const project = caricoProgetto(projectId)
2. const state = computeFinalizationState(project, dayNumber)
3. const exportReadiness = getOdgExportReadiness(state)
```

### Step 3 — Rendering testuale output

Output strutturato:

```markdown
## ODG Readiness — Giornata N del DD-MM-YYYY

**Stage**: <missing-odg | incomplete | blocked | ready-to-sign | finalized | stale>
**Can finalize**: <true | false>
**Export readiness**: <ready | draft | stale | blocked>

### 6 Semafori Compliance

- 🟢/🟡/🔴 Cast: <status> — <requirements met count> / <unmet count>
- 🟢/🟡/🔴 Location: <status>
- 🟢/🟡/🔴 Permessi: <status>
- 🟢/🟡/🔴 Elementi Chiave: <status>
- 🟢/🟡/🔴 Mezzi: <status>
- 🟢/🟡/🔴 Pasti: <status>

### Blocker (hard, bloccano firma)
- <lista>

### Warning (accettabili alla firma con DecisionMemo)
- <lista>

### Firma DP
- Presente: <sì/no>
- Firmato da: <signedBy>
- Data firma: <finalizedAt>
- Stato: <valid | stale | missing>
- Se stale: motivo upstream change = <descrizione>
```

### Step 4 — Raccomandazione operativa

Basata su stage + blocker:

- **ready-to-sign** → "Puoi firmare. Invoca modal DirectorOfProductionSignature."
- **blocked** → "Risolvi N blocker prima di firmare: <top 3>. Chiama reparti responsabili."
- **incomplete** → "Completa ODG readiness interno prima: <missing fields>"
- **missing-odg** → "Genera ODG via `generateOdgForDay(N)` dal projectStore."
- **finalized** → "Già firmato da X. Nessuna azione richiesta."
- **stale** → "Stato cambiato dopo firma di X. Ri-firma richiesta (riapri modal pre-fill)."

## Output

Report markdown con 6 semafori + blocker + warnings + raccomandazione.

Non modifica nulla nel progetto (read-only).

## Esempi d'uso

### Esempio 1 — DP matteo, giornata 5

**Utente**: "check ODG day 5"

**Output**:
```
## ODG Readiness — Giornata 5 del 15-05-2026

Stage: **blocked**
Can finalize: false
Export readiness: blocked

### 6 Semafori
- 🔴 Cast: missing (1 unmet) — Marco deal memo scaduto 14-05
- 🟢 Location: ok
- 🟢 Permessi: ok
- 🟡 Elementi chiave: not-configured (SpecialistDealMemo MVP)
- 🔴 Mezzi: missing — veicolo scena senza rental
- 🟡 Pasti: not-configured (MealPlan MVP)

### Blocker
1. [cast] Marco: deal memo scaduto il 2026-05-14 (ripresa 2026-05-15)
2. [mezzi] Picture car "Fiat Panda" in scena ma nessun rental veicoli attivo

### Warning
(nessuno)

### Firma DP
Presente: no

### Raccomandazione
Risolvi 2 blocker prima di firmare:
1. Casting director: rinnova deal memo Marco → oggi
2. Organizzatore generale: conferma rental veicolo → T-24h
Poi ri-esegui check.
```

### Esempio 2 — giornata finalized, upstream change

**Utente**: "check ODG day 3 dopo drag strip"

**Output** identifica `stage: stale` + suggerisce ri-firma.

## Integration con UI

La skill è complementare a `components/odg/ODGReadinessPanel.tsx`:
- UI = display interattivo per uso normale
- Skill = verifica rapida via chat/CLI, test engine, debugging

## Troubleshooting

- **Project not loaded**: skill emette warning + suggerisce caricare progetto
- **Day doesn't exist**: skill ritorna "missing-odg" + suggerisce `generateOdgForDay`
- **ComplianceContext incompleto**: skill segnala campi mancanti nel context

## Related skills

- `/load-production-context` (consigliato prima per contesto MMS/CCNL)
- `/update-todo` (per tracciare decisione post-firma)

## Version + maintenance

- Version: 1.0 (created 2026-04-23 T1703)
- Maintained by: direttore-produzione-agent + workflow-state-machine-agent

## References

- `lib/odg/finalizationRules.ts` (T602 logic)
- `lib/schedule/compliance/matrix.ts` (T601 compliance)
- `content/knowledge-base/set-operations-realtime.md` §2 (ODG sequencing)
- `content/knowledge-base/produzione-italiana-compliance.md` (CCNL + L.977/67 che alimentano compliance matrix)
