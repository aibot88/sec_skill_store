---
name: bmad-pipeline
description: >
  Orchestriert den kompletten BMAD-Entwicklungszyklus als automatische Pipeline:
  bmad-create-story → bmad-testarch-atdd → bmad-dev-story → bmad-testarch-test-review
  → bmad-code-review → bmad-security-review (Kassandra, conditional), jeweils in frischem Kontext.
  Führt git add nach dev-story aus. Der Code-Review-Skill fixt Minor Issues selbst
  ("fixe minor issues instantly"). Pausiert nur bei Major/Critical Issues (User-Entscheidung),
  am Epic-Ende zwingend mit Kassandra-Security-Review und danach für die Retrospektive
  (liest sprint-status.yaml).
  Trigger: "bmad pipeline", "bmad run", "bmad start", "story pipeline", "neues feature",
  "story durchlaufen", "pipeline starten", immer wenn der User den kompletten BMAD-Flow
  starten will ohne jeden Schritt einzeln aufzurufen.
---

# BMAD Pipeline Skill

Dieser Skill orchestriert den vollständigen BMAD-Entwicklungszyklus in einer einzigen
Ausführung. Jeder Schritt läuft in einem eigenen, frischen Subagenten-Kontext.

## Ablauf-Übersicht

```
[1] bmad-create-story        (Sonnet, frischer Kontext)
          ↓
[1b] Matrix-Gate (Oracle)    (Sonnet, frischer Kontext)  ← nur wenn Matrix-Feature
     Spec-Anforderungen, Fehlercodes, Testfälle → MATRIX_ORACLE_CONTEXT
          ↓
[2] bmad-testarch-atdd       (Sonnet, frischer Kontext)  ← TEA Gate 1
    failing tests generieren + stagen (+ Oracle-Findings wenn Matrix)
          ↓
[3] bmad-dev-story           (Sonnet, frischer Kontext)
          ↓
       rtk git add .
          ↓
[4] bmad-testarch-test-review (Sonnet, frischer Kontext) ← TEA Gate 2
    Test-Qualität prüfen, Findings ausgeben
          ↓
[5] bmad-code-review         (Opus, frischer Kontext)
    "fixe minor issues instantly"
    → Minor Issues werden vom Skill selbst gefixt
          ↓
       rtk git add .
          ↓
[5b] Security-Review-Gate (conditional)  ← SEC Gate 1
     Story-Frontmatter `security_review` prüfen (required/optional/not-needed)
     oder Heuristik über Dateipfade der Änderung.
     Falls required oder vom User bestätigt optional:
       → bmad-security-review (Kassandra) — staged diff
       → CRITICAL blockiert den Commit; HIGH konfigurierbar
       → Report nach _bmad-output/.../security-reports/
          ↓
    Major/Critical/HIGH Issues aus [5] oder [5b] gefunden?
       Ja  → Pause, User entscheidet
       Nein → sprint-status.yaml aktualisieren (Story → done, last_updated, Kommentarzeile)
              ↓
              rtk git add sprint-status.yaml
              ↓
              rtk git commit
          ↓
[6] Epic-Check: sprint-status.yaml
       Epic fertig? → [6b] Kassandra am Epic-Ende  ← SEC Gate 2
                     (zwingend, unabhängig von Story-Flags)
                     mit Diff-Range-Override: rtk git diff <epic-base>..HEAD
                     → epic-{N}-security-review-{date}.md wird erzeugt
                     → CRITICAL/HIGH = Pause, User entscheidet
                     → Danach Pause für Retrospektive
       Sonst       → ✅ Fertig, nächste Story bereit
```

---

## Schritt-für-Schritt-Anleitung

### Vorbereitung

Bestimme die BMAD-Skill-Pfade:

```bash
rtk find . -name "SKILL.md" -type f
```

Erwartete Pfade:
- `skills/bmad-create-story/SKILL.md`
- `skills/bmad-testarch-atdd/SKILL.md`
- `skills/bmad-dev-story/SKILL.md`
- `skills/bmad-testarch-test-review/SKILL.md`
- `skills/bmad-code-review/SKILL.md`
- `skills/bmad-security-review/SKILL.md` (Kassandra)

Halte den Story-Titel oder die Feature-Beschreibung vom User fest – sie wird an alle
Subagenten weitergegeben.

---

### Schritt 1: bmad-create-story

**Modell:** `claude-sonnet-4-6` | **Kontext:** frisch (Task-Tool)

```
Lies und befolge die Anweisungen aus .claude/skills/bmad-create-story/SKILL.md.
Feature/Story: [FEATURE_BESCHREIBUNG_VOM_USER]
Arbeite das vollständig durch und beende dann.
```

Warte auf Fertigstellung. Notiere den Namen der erstellten Story-Datei:

```bash
rtk git status
```

Zeige: `✓ Schritt 1: Story erstellt → [story-datei.md]`

---

### Schritt 1b: Matrix-Gate — Oracle-Konsultation (conditional)

**Modell:** `claude-sonnet-4-6` | **Kontext:** frisch (Task-Tool)

**Erkennung:** Prüfe ob die Story ein Matrix-API-Feature beschreibt:

```bash
rtk grep -i "_matrix/\|m\.room\.\|m\.login\|event_type\|txnId\|sync.*since\|matrix.*spec" [STORY_DATEI_AUS_SCHRITT_1]
```

Matrix-Bezug liegt vor wenn: Endpoint-Pfade wie `/_matrix/client/`, Event-Typen wie `m.room.*`, Matrix-Fehlercodes (`M_FORBIDDEN` etc.) oder Matrix-Konzepte (sync, txnId, power_levels) im Story-Text erwähnt werden.

**Wenn kein Matrix-Bezug:**

`⏭️ Schritt 1b: Matrix-Gate übersprungen — kein Matrix-Feature.`  
`MATRIX_ORACLE_CONTEXT = null`  
Fahre direkt mit Schritt 2 fort.

**Wenn Matrix-Feature erkannt:**

```
Lies und befolge die Anweisungen aus skills/agent-oracle/SKILL.md.

Du bist die Oracle — Matrix Client-Server API v1.18 Expertin.
Die folgende Story beschreibt ein Matrix-Feature für den Nebu-Server.

Story-Datei: [STORY_DATEI_AUS_SCHRITT_1]

Führe für diese Story aus:
1. Spec Lookup (lade references/spec-lookup.md): Welche Matrix CS API v1.18
   Endpoints, Event-Typen und Verhaltensregeln sind relevant?
   Liste alle MUST-Anforderungen für dieses Feature.
2. Test Guidance (lade references/test-guidance.md): Welche spec-definierten
   Fehlercodes, HTTP-Status-Codes und Edge Cases MÜSSEN als Tests abgedeckt sein?

Gib das Ergebnis als kompaktes Markdown zurück (max. 40 Zeilen).
Keine Prosa — nur Anforderungen und Testfälle als Listen. Beende dann.
```

Warte auf Fertigstellung. Speichere die Ausgabe als `MATRIX_ORACLE_CONTEXT`.

Zeige: `✓ Schritt 1b: Oracle konsultiert — Matrix-Spec-Context erfasst.`

---

### Schritt 2: bmad-testarch-atdd (TEA Gate 1 — Failing Tests)

**Modell:** `claude-sonnet-4-6` | **Kontext:** frisch (Task-Tool) | **Pflicht**

**Ausnahme:** Reine Infrastruktur-Stories ohne beobachtbares Verhalten (z.B. nur Dockerfile, nur Migration ohne Logik) können übersprungen werden. Dann Ausgabe:
`⏭️ Schritt 2: Infra-only Story — ATDD übersprungen.`

Für alle anderen Stories:

```
Lies und befolge die Anweisungen aus .claude/skills/bmad-testarch-atdd/SKILL.md
(oder den ATDD workflow.md falls SKILL.md nicht existiert).
Story-Datei: [STORY_DATEI_AUS_SCHRITT_1]
Generiere failing Acceptance Tests für alle Acceptance Criteria der Story.
Die Tests müssen FAILING sein bevor Implementation-Code existiert.

[NUR WENN MATRIX_ORACLE_CONTEXT VORHANDEN — sonst diesen Block weglassen:]
Matrix Spec-Anforderungen (aus Oracle, v1.18):
[MATRIX_ORACLE_CONTEXT]
Stelle sicher, dass ALLE spec-definierten Fehlercodes, HTTP-Status-Codes
und Edge Cases oben als eigene failing Tests abgedeckt sind.
Die Matrix-Spezifikation definiert explizit welche Fehlerantworten auf welche
Eingaben zu erfolgen haben — teste nicht nur den Happy-Path.

Beende nach Generierung der Tests.
```

Warte auf Fertigstellung.

Zeige: `✓ Schritt 2: Failing Acceptance Tests generiert.`

---

### Schritt 3: bmad-dev-story + git add

**Modell:** `claude-sonnet-4-6` | **Kontext:** frisch (Task-Tool)

```
Lies und befolge die Anweisungen aus .claude/skills/bmad-dev-story/SKILL.md.
Implementiere die zuletzt erstellte Story vollständig.
Die failing Acceptance Tests aus Schritt 2 sind bereits vorhanden —
implementiere gegen diese Tests bis sie grün sind.
Beende nach Abschluss der Implementierung.
```

Warte auf Fertigstellung. Danach:

```bash
[ -f /tmp/bmad-session-env.sh ] && source /tmp/bmad-session-env.sh
rtk git add .
rtk git status
```

Zeige: `✓ Schritt 3: Implementierung abgeschlossen, git add ausgeführt.`

---

### Schritt 4: bmad-testarch-test-review (TEA Gate 2 — Test-Qualität)

**Modell:** `claude-sonnet-4-6` | **Kontext:** frisch (Task-Tool) | **Pflicht**

```
Lies und befolge die Anweisungen aus .claude/skills/bmad-testarch-test-review/SKILL.md
(oder den test-review workflow.md falls SKILL.md nicht existiert).
Reviewe alle gestagten Test-Dateien (git diff --staged).
Prüfe insbesondere:
- Hat jedes Acceptance Criterion der Story mindestens einen Test?
- Gibt es Hard Waits, versteckte Assertions oder nicht-deterministische Tests?
- Haben GenServer-State-Stories einen Crash/Restart-Test?
- Wird Cookie-Forging oder DB-Seeding als Shortcut verwendet?
Klassifiziere jeden Fund als MAJOR, MINOR oder INFO.
MAJOR: fehlendes Test-Coverage für ein Acceptance Criterion.
Gib das vollständige Ergebnis aus und beende dann.
```

Warte auf die vollständige Ausgabe. Speichere die Findings für Schritt 5.

**Wenn MAJOR Findings im Test-Review:**

```
⚠️ bmad-testarch-test-review hat MAJOR Test-Lücken gefunden (siehe oben).
Empfehlung: Behebe fehlende Test-Coverage vor dem Code-Review.
Tippe "weiter" um trotzdem mit dem Code-Review fortzufahren,
oder behebe die Lücken und starte Schritt 4 neu.
```

Stoppe und warte. Bei "weiter": fahre mit Schritt 5 fort.

**Wenn keine MAJOR Findings:**

Zeige: `✓ Schritt 4: Test-Review bestanden. Findings werden an Code-Review übergeben.`

---

### Schritt 5: bmad-code-review (inkl. Minor-Issue-Fix)

**Modell:** `claude-opus-4-7` | **Kontext:** frisch (Task-Tool)

Übergib die Findings aus Schritt 4 an den Code-Review-Agent:

```
[OLLAMA-PRÄAMBEL wenn OLLAMA_MODE=true]

Lies und befolge die Anweisungen aus .claude/skills/bmad-code-review/SKILL.md.
fixe minor issues instantly
Reviewe alle gestagten Änderungen (git diff --staged).

Test-Review Findings (aus bmad-testarch-test-review):
[FINDINGS_AUS_SCHRITT_4]

[NUR WENN MATRIX_ORACLE_CONTEXT VORHANDEN — sonst diesen Block weglassen:]
Matrix Spec-Anforderungen (aus Oracle, v1.18):
[MATRIX_ORACLE_CONTEXT]
Prüfe ob die Implementierung ALLEN oben genannten MUST-Anforderungen der
Matrix Client-Server API v1.18 entspricht. Jede Abweichung ist ein Finding.
Fehlende Fehlercodes (z.B. falsches errcode, falscher HTTP-Status) = MAJOR.

Berücksichtige diese Test-Findings in deinem Review.
Gib das vollständige Ergebnis aus. Klassifiziere jeden Fund explizit als
MAJOR, MINOR oder INFO – damit die Pipeline die Schwere eindeutig erkennen kann.
```

Der Skill fixt Minor Issues selbst während des Reviews. Warte auf die vollständige Ausgabe.

Danach in jedem Fall:

```bash
[ -f /tmp/bmad-session-env.sh ] && source /tmp/bmad-session-env.sh
rtk git add .
rtk git status
```

---

### Schritt 5b: Security-Review-Gate (SEC Gate 1 — pro Story, conditional)

**Modell:** `claude-opus-4-7` | **Kontext:** frisch (Task-Tool)

**Ziel:** Security-sensitive Stories bekommen ein zweites, fokussiertes Review. Nicht-sensitive Stories überspringen den Schritt.

#### Entscheidung: braucht die Story ein Security-Review?

1. **Prüfe die Story-Datei auf Frontmatter-Flag** `security_review`:
    - `required` → SEC Gate 1 ausführen
    - `optional` → Nutzer einmalig fragen: "Story ist als optional markiert — Security-Review jetzt laufen lassen? [Y/n]"
    - `not-needed` → Gate überspringen, Zeile ausgeben: `⏭️ Schritt 5b: Security-Review übersprungen (Story flagged `not-needed`).`
    - **Flag fehlt:** Auto-Klassifikation (siehe unten).

2. **Auto-Klassifikation** (wenn Frontmatter-Flag fehlt). Lese die gestagten Dateinamen:

```bash
rtk git diff --staged --name-only
```

Markiere als `required`, wenn **mindestens einer** zutrifft:
- Datei liegt unter `gateway/internal/auth/`, `gateway/internal/middleware/`, `gateway/internal/admin/`, `gateway/internal/db/`
- Neue HTTP-Route in `gateway/cmd/gateway/main.go` (`mux.Handle` oder `mux.HandleFunc` Zeilen hinzugefügt)
- Datei liegt unter `core/apps/signature/` oder `core/apps/permissions/`
- Elixir `.ex`-Datei `imports :crypto` oder nutzt `Plug.Conn` auf externem Input
- Neue SQL-Migration unter `gateway/migrations/`
- Sonst: `not-needed`. Gate überspringen mit kurzer Begründung.

#### Security-Review durchführen

Falls `required` oder vom User bestätigt:

```
Lies und befolge die Anweisungen aus .claude/skills/bmad-security-review/SKILL.md.
Reviewe alle gestagten Änderungen (git diff --staged).

Kassandra (die Skill-Persona) kennt den vollen Security-Scope: OWASP Top 10, ASVS L2,
CWE Top 25, STRIDE, NIST SP 800-53 plus die Nebu-spezifischen Invarianten
(Compliance RSP, Audit-Immutability, OIDC-Validierung, Matrix Power Levels,
Crypto-Primitive, Secrets-Hygiene). Frameworks werden nach betroffener Komponente
gewichtet — keine blinde Checkliste.

Kassandra schreibt den Report als Markdown-Audit-Artefakt nach
_bmad-output/implementation-artifacts/security-reports/{story-id-or-date}-security-review.md
— auch bei null Findings (Audit-Trail).

Gib am Ende zurück:
- Classification: CRITICAL | HIGH | CLEAN
- Pfad zum Report
- Severity-Zähler
```

Warte auf Fertigstellung.

**Wenn Classification = CRITICAL:**

```
🔴 Kassandra hat CRITICAL Findings gefunden — Report: [pfad]
Pipeline gestoppt. User-Entscheidung erforderlich:
  (a) fixen und neu starten
  (b) akzeptieren mit schriftlicher Begründung
  (c) als Follow-up-Story in nächstes Epic verschieben
Tippe "weiter" um trotzdem zu commiten.
```

Stoppe und warte. Bei "weiter": fahre fort.

**Wenn Classification = HIGH:**

Kassandra respektiert `blocking_severity` aus `.claude/security-agent.yaml` (Default: `CRITICAL`). HIGH warnt, blockiert aber nur wenn `blocking_severity: HIGH` konfiguriert ist. Übernimm Kassandras Entscheidung 1:1 — wenn Kassandra sagt "Pipeline darf durchlaufen", zeige die Warnung und fahre fort.

**Wenn Classification = CLEAN:**

Zeige: `✓ Schritt 5b: Kassandra — clean.`

```bash
[ -f /tmp/bmad-session-env.sh ] && source /tmp/bmad-session-env.sh
rtk git add .
```

---

### Schritt 6: Review-Auswertung

Analysiere die Ausgaben aus Schritt 4 (Test-Review), Schritt 5 (Code-Review) **und Schritt 5b (Security-Review, falls ausgeführt)** auf **Major / Critical / High Issues**:

- Schlüsselwörter: `MAJOR`, `Critical`, `CRITICAL`, `HIGH severity`, `🔴`, `blocking`
- Abschnitte: `## Major Issues`, `## Critical Issues`, `### Blocking Problems`, `## CRITICAL`, `## HIGH`
- Aussagen wie "must be fixed before merging"

**Wenn blockierende Issues gefunden (aus einem der Reviews):**

```
⚠️ Blockierende Issues gefunden (MAJOR/CRITICAL/HIGH — siehe oben).
Pipeline gestoppt. Bitte behebe die Issues und starte neu –
oder tippe "weiter" um trotzdem zu commiten.
```

Stoppe und warte. Bei "weiter": fahre mit dem Commit fort.

**Wenn keine blockierenden Issues:**

Zeige: `✓ Kein blockierendes Issue – commite automatisch.`

**Vor jedem Commit: sprint-status.yaml aktualisieren** (gilt genauso im "weiter"-Fall aus dem Stop oben).

```bash
rtk read _bmad-output/implementation-artifacts/sprint-status.yaml
```

1. **Story-Status im `development_status:`-Block auf `done` setzen.**
   Der YAML-Key enthält den vollen Slug, z.B. `5-24-sso-redirect-scheme-allowlist: done`.
   Story-ID und Slug kommen aus der in Schritt 1 erstellten Story-Datei.

2. **`last_updated:` auf das heutige Datum setzen** — kommt zweimal in der Datei vor:
    - als Kommentar am Dateianfang (`# last_updated: YYYY-MM-DD`)
    - als YAML-Feld (`last_updated: YYYY-MM-DD`)

3. **Neue Kommentarzeile direkt unter dem `last_updated`-Kommentar einfügen**, im bestehenden Format:

   ```
   # story {STORY_ID} done (pipeline: {KURZE_ZUSAMMENFASSUNG}): {YYYY-MM-DD}
   ```

   Beispiele für `{KURZE_ZUSAMMENFASSUNG}` aus der Historie:
    - `ATDD+Dev+Code+Security CLEAN`
    - `CLEAN, Bootstrap replay entry points closed`
    - `2 MINOR fixed — handler alloc + base.html inline style`
    - `2 MAJOR + HIGH fixed, 2 rounds Kassandra`
    - `3 rounds — real sql.Tx via runInTx injection`

4. **Stagen:**

```bash
   rtk git add _bmad-output/implementation-artifacts/sprint-status.yaml
   ```

Zeige: `✓ sprint-status.yaml aktualisiert ({STORY_ID} → done).`

**Dann commiten:**

```bash
rtk git commit -m "$(cat <<'EOF'
[KURZE_ZUSAMMENFASSUNG_AUS_STORY_ODER_REVIEW]
EOF
)"
```

Keine `Co-Authored-By`-Zeile anhängen.

Zeige: `✓ Commit erstellt.`

---

### Schritt 7: Epic-Status prüfen

```bash
rtk read _bmad-output/implementation-artifacts/sprint-status.yaml
```

Suche in der YAML nach dem Feld `epic-{N}-retrospective` (z.B. `epic-1-retrospective`).
Die Epic-Nummer entnimmst du dem Namen der aktuellen Story oder der sprint-status.yaml selbst.

**Retro ist fällig, wenn:**
Der Eintrag, der in der Datei direkt **vor** `epic-{N}-retrospective` steht (also die letzte
Story des Epics), soeben auf `done` gesetzt wurde – sprich: die Story, die wir gerade
committed haben, ist genau diese letzte Story.

**Epic abgeschlossen:**

**Zuerst: Schritt 7b — Epic-Ende Security-Review (SEC Gate 2, zwingend)**

Dies läuft unabhängig von Story-Flags — jedes Epic bekommt am Ende ein ganzheitliches Security-Review.

1. Bestimme die Base-Referenz für den Epic-Diff:

```bash
rtk git log --grep="epic-{N-1}-retrospective\|retrospektive" --oneline
```

    - Falls unklar: frage den User: "Epic-Diff-Basis? (commit-sha oder Tag)"

2. Führe Kassandra mit Epic-Diff-Range-Override aus:

```
Lies und befolge die Anweisungen aus .claude/skills/bmad-security-review/SKILL.md.

**Caller-Overrides** (siehe Phase 1 in Kassandras workflow.md):
- Diff-Range: statt `git diff --staged`, reviewe `git diff <epic-base>..HEAD`
- Report-Filename-Prefix: `epic-{N}-security-review-{YYYY-MM-DD}`

Zusätzlicher Analyse-Fokus über Kassandras Standard-Scope hinaus:
- ganzheitliche Angriffsflächen, die über einzelne Stories hinweg entstehen
- Kombinationen neuer Endpoints, die zusammen Auth-Bypass ermöglichen
- neue DB-Migrationen, die RLS / Policies brechen
- neue gRPC-Handler, die Middleware umgehen
- kumulative Secrets- oder Crypto-Verschiebungen

Kassandra schreibt den Report nach
_bmad-output/implementation-artifacts/security-reports/epic-{N}-security-review-{YYYY-MM-DD}.md
(Audit-Artefakt, auch bei null Findings).

Gib Classification (CRITICAL | HIGH | CLEAN) und Report-Pfad zurück.
```

3. (Der Report wird von Kassandra selbst geschrieben — kein separater Pipeline-Schreibschritt.)

4. Auswertung:
    - **CRITICAL oder HIGH gefunden:** Stoppe mit

      ```
      🔴 Epic-Ende Security-Review hat CRITICAL/HIGH Findings.
      Epic kann nicht abgeschlossen werden ohne User-Entscheidung.
      Optionen:
        (a) Follow-up-Stories in Epic {N+1} anlegen (empfohlen)
        (b) Begründete Akzeptanz als Risiko dokumentieren
      Tippe "weiter" um die Retrospektive trotzdem zu starten.
      ```

    - **Nur MEDIUM/LOW oder null Findings:** Weiter zur Retrospektive.

**Dann: Retrospektive**

```
🏁 Epic abgeschlossen!
Security-Review-Artefakt: epic-{N}-security-review-{YYYY-MM-DD}.md
Alle Stories sind erledigt. Zeit für die Retrospektive.
Führe außerdem /bmad-testarch-trace aus, um die Traceability-Matrix für das Epic zu erstellen.
Wenn du fertig bist, starte den nächsten Epic mit "bmad pipeline".
```

Stoppe hier und warte auf den User.

**Epic läuft noch:**

```
✅ Story abgeschlossen. Nächste Story starten? [Y/n]
```

- Bei `Y` oder Enter: Starte die Pipeline von vorne (Schritt 1: bmad-create-story).
- Bei `n`: Beende die Pipeline.

---

## Fehlerbehandlung

- **Subagent schlägt fehl:** Zeige die vollständige Fehlermeldung. Stoppe, User entscheidet.
- **git add / git commit schlägt fehl:** Zeige den git-Fehler. Stoppe, warte auf User-Aktion.
- **sprint-status.yaml nicht vorhanden:** `ℹ️ sprint-status.yaml nicht gefunden – Epic-Check übersprungen.`
- **SKILL.md / workflow.md nicht gefunden:** Melde den fehlenden Pfad und stoppe.
- **bmad-testarch-atdd nicht verfügbar:** `⚠️ ATDD-Skill nicht gefunden – TEA Gate 1 übersprungen. Stelle sicher, dass Acceptance Tests manuell vor der Implementierung existieren.`
- **bmad-testarch-test-review nicht verfügbar:** `⚠️ Test-Review-Skill nicht gefunden – TEA Gate 2 übersprungen.`

---

## Modell-Übersicht

| Schritt                      | Modell            |
|------------------------------|-------------------|
| bmad-create-story            | claude-sonnet-4-6 |
| Matrix-Gate Oracle (Schritt 1b, nur bei Matrix-Stories) | claude-sonnet-4-6 |
| bmad-testarch-atdd           | claude-sonnet-4-6 |
| bmad-dev-story               | claude-sonnet-4-6 |
| bmad-testarch-test-review    | claude-sonnet-4-6 |
| bmad-code-review             | claude-opus-4-7   |
| bmad-security-review (Kassandra, Gate 1 & 2) | per `.claude/security-agent.yaml` (Default: claude-opus-4-7) |

---

## Wichtige Hinweise

- Gib dem User nach jedem Schritt ein kurzes Status-Update.
- Die Feature-Beschreibung des Users muss an alle Subagenten weitergegeben werden.
- Alle Schritte laufen **sequenziell** – kein paralleles Starten von Subagenten.
- Die Findings aus dem Test-Review (Schritt 4) **müssen** an den Code-Review-Agent (Schritt 5) übergeben werden.
- `rtk git add .` nach dem Code-Review ist immer auszuführen, unabhängig davon ob
  Minor Issues gefunden wurden oder nicht – es schadet nicht und stellt Vollständigkeit sicher.
- **TEA Gate 1 (ATDD)** erzeugt failing Tests — der Dev-Agent implementiert gegen diese.
  Ohne failing Tests kein klares Definition of Done.
- **TEA Gate 2 (Test-Review)** läuft vor dem Code-Review, damit Test-Lücken frühzeitig
  erkannt werden und der Code-Reviewer sich auf Logik konzentrieren kann.
- **SEC Gate 1 (Story-Security-Review)** ist conditional und läuft nach dem Code-Review.
  Entscheidung per Story-Frontmatter-Flag `security_review` oder per Heuristik über
  die gestagten Dateipfade. Blockiert den Commit bei CRITICAL/HIGH.
- **SEC Gate 2 (Epic-Ende-Security-Review)** ist zwingend, unabhängig von Story-Flags.
  Läuft vor der Retrospektive mit dem gesamten Epic-Diff. Erzeugt immer ein
  `epic-{N}-security-review-{date}.md` Audit-Artefakt.