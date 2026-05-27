---
name: audit-trail-protokoll
description: "Fuehrt das Audit-Trail-Protokoll des Wuerfels — jeder Reviewlauf jede Prompt-Aenderung jede Pruefer-Abnahme jeder Cache-Treffer jede Hash-Pruefung wird unveraenderlich protokolliert. Spalten pro Eintrag: Zeitstempel Aktion Verantwortlicher Wuerfelversion Prompt-Version Modell-Version Eingangs-Hash Ausgangs-Hash Begruendung. Ablage als `audit-trail.jsonl` (append-only) und als `audit-trail.md` (menschenlesbar). Pflichteintrag vor jeder Mandatsuebergabe. Erlaubt Nachweis gegenueber Mandant Pruefer Aufsicht und Versicherung dass der Wuerfel reproduzierbar entstand."
---

# /tabellenreview-3d:audit-trail-protokoll

## Zweck

Wer mit KI Verträge prüft muss später erklären können wie das Ergebnis zustande kam. Dieser Skill ist die Erklärung — Append-only-Log für den gesamten Lebenszyklus des Würfels.

## Ereignistypen

### Würfel-Lebenszyklus

- `würfel.erstellt` — Würfel-Schema neu angelegt
- `würfel.dimension-erweitert` — Spalte / Zeile / Arbeitsblatt hinzugefügt
- `würfel.dimension-gekuerzt` — Spalte / Zeile / Arbeitsblatt entfernt
- `würfel.archiviert` — Würfel abgeschlossen

### Prompts

- `prompt.erstellt` — neuer Spalten- oder Zeilenprompt definiert
- `prompt.geändert` — Prompt-Wortlaut geändert (Versions-ID erhöht)
- `prompt.deaktiviert` — Prompt aus aktivem Schema genommen

### Reviewlauf

- `lauf.gestartet` — Reviewlauf begonnen, mit Würfel-Snapshot-Hash
- `lauf.beendet` — Reviewlauf beendet, mit Ergebnis-Hash
- `lauf.fehler` — Reviewlauf abgebrochen, mit Fehlermeldung

### Caching

- `cache.treffer` — Zelle aus Cache übernommen, Quell-Zell-ID
- `cache.invalidiert` — Cache-Eintrag verworfen weil Prompt-Version geändert

### Prüfer-Workflow

- `prüferflag.gesetzt` — Zelle braucht menschliche Prüfung, Grund
- `prüferabnahme.eingegeben` — Prüfer hat abgehakt, Prüfer-ID und Entscheidung
- `prüfer.kommentar` — Prüfer-Kommentar zu Zelle

### Belegkette

- `datei.gehasht` — Hash einer Quelldatei berechnet
- `hash-bruch` — Quelldatei-Hash weicht vom registrierten Hash ab (Manipulationsverdacht)

## Pflichtfelder pro Eintrag

```json
{
  "zeitstempel": "2026-05-20T14:23:11Z",
  "aktion": "lauf.beendet",
  "verantwortlicher": "system",
  "würfel-version": "v3",
  "prompt-version": "p12",
  "modell-version": "claude-opus-4-7",
  "eingangs-hash": "sha256:...",
  "ausgangs-hash": "sha256:...",
  "anzahl-zellen": 4176,
  "anzahl-prüferflag": 87,
  "begründung": "Standardlauf nach Schema-Änderung Spalte 'MAC'"
}
```

## Ablage

- `audit-trail.jsonl` — append-only, eine JSON-Zeile pro Ereignis. Nie ändern, nur anhängen.
- `audit-trail.md` — periodisch zu menschenlesbarem Markdown verdichtet (z. B. wochenweise).

## Integritaet

- Jeder Eintrag enthält den Hash des vorherigen Eintrags (Chain-of-Trust). Wer einen Eintrag ändert bricht die Kette.
- Optional: kryptografische Signatur des Prüfers bei Abnahme-Ereignissen.

## Verwendung

- Pflicht vor jeder Mandatsübergabe — der Prüfer signiert den letzten Audit-Stand.
- Bei Beschwerden Aufsicht oder Haftungsfrage rückverfolgbar nachweisen welcher Reviewlauf welchen Output produziert hat.
- Verhindert dass Prompts schleichend geändert werden und alte Zellen `nicht mehr nachvollziehbar` sind.
