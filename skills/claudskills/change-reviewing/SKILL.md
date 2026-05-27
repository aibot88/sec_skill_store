---
name: change-reviewing
description: >-
  Diff-basierter Review von Code-Aenderungen. Identifiziert Risiken,
  Regressionen, Testluecken, Security-Nebenwirkungen und offene Folgearbeiten.
  Verwende diesen Skill wenn der User sagt: "Review", "Code Review",
  "Aenderungen pruefen", "Was habe ich kaputt gemacht", "Diff Review",
  "change-reviewing", "/review".
---

# /change-reviewing — Diff-basierter Code-Review

Du reviewst konkrete Code-Aenderungen (Diffs, Branches, Commits) und
machst Risiken, Regressionen und Folgearbeiten sichtbar.

## Abgrenzung

- **Nicht** codebase-assessing: Dort wird der IST-Zustand breit analysiert.
  Hier fokussierst du auf einen konkreten Diff.
- **Nicht** gap-analyzing: Dort wird Soll gegen Ist verglichen.
  Hier wird ein Diff auf Qualitaet geprueft.
- **Nicht** testing-code: Dort werden Tests geschrieben.
  Hier wird identifiziert wo Tests fehlen.

## Workflow

### Phase 1 — Diff erfassen

1. Bestimme den Scope: Branch, Commit-Range oder unstaged Changes?
2. Lade den Diff:
   - `git diff` fuer unstaged
   - `git diff --staged` fuer staged
   - `git diff main...HEAD` fuer Branch vs. main
   - `git log --oneline main..HEAD` fuer Commit-Uebersicht
3. Identifiziere alle geaenderten Dateien und kategorisiere sie:
   - Produktionscode
   - Tests
   - Konfiguration / Migrations
   - Dokumentation

### Phase 2 — Aenderungen bewerten

Fuer jede signifikante Aenderung pruefe:

**Korrektheit:**

- Tut der Code was er soll?
- Gibt es logische Fehler, Off-by-One, Race Conditions?
- Sind Edge Cases behandelt?

**Sicherheit:**

- Neue Inputs die nicht validiert werden?
- SQL Injection, XSS, Command Injection Risiken?
- Secrets oder sensible Daten exponiert?
- RLS Policies betroffen?

**Architektur:**

- Passt die Aenderung zu bestehenden Patterns?
- Wird Coupling eingefuehrt wo keines sein sollte?
- Sind Abstraktionen sinnvoll oder over-engineered?

**Tests:**

- Werden geaenderte Pfade von Tests abgedeckt?
- Fehlen Tests fuer neue Logik?
- Sind bestehende Tests noch gueltig?

**Folgearbeiten:**

- Braucht es Migrationen?
- Muessen Dokus aktualisiert werden?
- Muessen andere Services deployed werden?
- Sind TypeScript-Typen konsistent?

### Phase 3 — Report schreiben

Erstelle den Report nach dem Template in `templates/review-template.md`.

**Regeln:**

- Positives explizit benennen — nicht nur Probleme.
- Jedes Risiko mit Schweregrad und konkreter Empfehlung.
- Blocker klar von Nice-to-Haves trennen.

### Phase 4 — Ablage (optional)

Nur bei groesseren Reviews als Datei ablegen:
`docs/09_reviews/YYMMDD-<branch-oder-thema>.md` (YYMMDD = rueckwaerts geschriebenes Datum, z.B. `260418-feature-x.md` fuer 2026-04-18 — sortiert chronologisch)

Fuer kleine Reviews reicht die direkte Antwort im Chat.

## Output

Strukturierter Review-Report (im Chat oder als Markdown-Datei).

## Qualitaetskriterien

- [ ] Alle geaenderten Dateien sind erfasst
- [ ] Mindestens 1 positiver Aspekt benannt
- [ ] Risiken haben Schweregrad + Empfehlung
- [ ] Blocker sind klar von Verbesserungen getrennt
- [ ] Fehlende Tests sind identifiziert
