---
name: dringlichkeitsmarker
description: "Erkennt Fristen und Eile-Signale in Mandantenanfragen: Hauptverhandlung naechste Woche, Kuendigungsfrist laeuft, Haftungsfalle, Zwangsvollstreckung, Insolvenzantrag. Setzt Dringlichkeitsstufe HOCH/MITTEL/NIEDRIG und markiert: Anwalt muss sofort anrufen statt auf E-Mail zu warten. Laedt wenn der Nutzer 'Dringlichkeit pruefen', 'Frist erkannt', 'Sofortmassnahme Mandant', 'Fristproblem Erstanfrage' oder 'Eilbedarf Anfrage' sagt."
---

# Dringlichkeitsmarker

Dieser Skill erkennt Eile- und Fristen-Signale in der Eingangsanfrage und setzt eine Dringlichkeitsstufe. Bei hoher Dringlichkeit ist ein sofortiger Anwaltsrückruf erforderlich — die anfragende Person darf nicht auf eine E-Mail-Antwort warten.

## Dringlichkeitsstufen

| Stufe | Kriterium | Konsequenz |
|---|---|---|
| **HOCH** | Konkrete Frist, bevorstehender Termin, Haftungsrisiko | Anwalt ruft sofort zurück; Erstantwort enthält Sofortruf-Hinweis |
| **MITTEL** | Zeitdruck erkennbar, aber keine akute Frist | Rückmeldung innerhalb 24 Stunden |
| **NIEDRIG** | Kein Zeitdruck erkennbar | Normale Bearbeitungsreihenfolge |
| **UNBEKANNT** | Keine Zeitangaben in der Anfrage | Wie MITTEL behandeln |

## Eile-Signale: Explizite Nennungen (HOCH)

### Gerichtstermine und Verhandlungen

- „Hauptverhandlung nächste Woche" / „Termin beim Amtsgericht am [Datum]"
- „einstweilige Verfügung wurde zugestellt"
- „Versäumnisurteil droht" / „ich war nicht bei der Verhandlung"
- „Berufungsfrist läuft ab"
- „Einspruchsfrist gegen den Strafbefehl"

### Vertragsfristen

- „Kündigungsfrist läuft" / „Kündigung zum [Datum]"
- „Vertragsfrist endet diese Woche"
- „Widerspruchsfrist" / „Einspruchsfrist"
- „Rückgabefrist" / „Mängelrüge muss raus"

### Vollstreckung und Insolvenz

- „Zwangsvollstreckung eingeleitet" / „Gerichtsvollzieher war da"
- „Pfändung meines Kontos"
- „Insolvenzantrag wurde gestellt"
- „Pfändungs- und Überweisungsbeschluss erhalten"

### Strafrechtliche Ereignisse

- „bin vorgestern verhaftet worden" / „sitze in Untersuchungshaft"
- „Haftprüfungstermin" / „Haftbefehl"
- „Polizei hat mich heute befragt"
- „Vorladung als Beschuldigter erhalten"

### Behördliche Fristsetzungen

- „Behörde hat mir Frist bis [Datum] gesetzt"
- „Bescheid mit Rechtsmittelfrist erhalten"
- „Widerspruchsfrist gegen Bescheid läuft"
- „Abschiebungsandrohung" / „Ausreisefrist"

## Eile-Signale: Zeitwörter und Adverbien (HOCH oder MITTEL)

| Signal | Stufe |
|---|---|
| „sofort", „dringend", „heute noch", „jetzt" | HOCH |
| „diese Woche", „nächste Woche", „bis Freitag" | HOCH |
| „bald", „in Kürze", „demnächst" | MITTEL |
| „in den nächsten Wochen", „nächsten Monat" | MITTEL |
| „irgendwann", „wenn Sie Zeit haben" | NIEDRIG |

## Haftungsfall-Signale (immer HOCH)

- „Ich werde verklagt" / „mir wurde eine Klage angekündigt"
- „Abmahnung erhalten"
- „Schadensersatzforderung" über einem relevanten Betrag
- „Vertragsstrafe droht"
- „mein Unternehmen ist in Gefahr"

## Ausgabeformat

```
DRINGLICHKEIT
=============
Stufe:        [HOCH / MITTEL / NIEDRIG / UNBEKANNT]
Frist/Termin: [Datum und Art oder „nicht erkannt"]
Signal:       [Zitat des Eile-Signals aus der Anfrage oder „keins"]
Begründung:   [Kurze Erklärung der Bewertung]

MASSNAHMEN:
  [x] Sofortiger Anwaltsrückruf erforderlich — NICHT auf E-Mail warten
  [ ] Rückmeldung innerhalb 24 Stunden
  [ ] Normale Bearbeitung
  [ ] Frist im Kalender eintragen: [Datum]
```

## Hinweis-Text für die Erstantwort-Mail (bei HOCH)

```
WICHTIG: Aus Ihrer Anfrage haben wir entnommen, dass möglicherweise eine
Frist oder ein wichtiger Termin unmittelbar bevorsteht. Bitte rufen Sie
uns umgehend unter [SEKRETARIATS-TELEFON] an. Warten Sie bitte nicht auf
eine Antwort per E-Mail — Fristen können nicht durch eine
Eingangsbestätigung gewahrt werden.
```

## Hinweis für das Sekretariat (Interne Notiz bei HOCH)

```
INTERN — SOFORTMASSNAHME ERFORDERLICH
Rechtsanwalt/Rechtsanwältin muss diese Person sofort zurückrufen.
Mögliche Frist: [Datum/Zeitfenster]
Mögliches Risiko: [Kurzbeschreibung aus dem Signal]
Telefon der anfragenden Person: [aus Parsing]
```

## Falsch-Negativ-Schutz

Bei Unsicherheit über die Dringlichkeit: Eher MITTEL als NIEDRIG. Bei Unsicherheit ob MITTEL oder HOCH: Eher HOCH. Der Schaden durch übersehene Fristen ist größer als der Aufwand eines unnötigen Sofortrückrufs.

## Verweise auf andere Skills

- `anfrage-eingang-parser` — Datenquelle
- `erstantwort-generator` — empfängt die Dringlichkeitsstufe und Hinweis-Texte
- `folgekorrespondenz-vorbereiten` — Dringlichkeitsstufe im CRM-Eintrag
- `mandatsverhaeltnis-hinweis` — bei HOCH: Langform mit Frist-Warnung
