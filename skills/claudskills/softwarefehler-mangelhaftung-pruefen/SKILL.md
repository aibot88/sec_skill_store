---
name: softwarefehler-mangelhaftung-pruefen
description: Strukturierte Pruefung bei mangelhafter Software. Bestimmt Vertragstyp (Kaufrecht §§ 433 ff. BGB bei Software-Erwerb auf Datentraeger Werkvertrag §§ 631 ff. BGB bei Individualsoftware oder Anpassung Dienstvertrag bei Beratung Mietrecht §§ 535 ff. BGB bei SaaS und ASP). Pruefraster Mangelbegriff fuer Software Pflichtenhefte Spezifikationen Funktionalitaet Performance Sicherheit. Nachbesserungsrecht Frist Selbstvornahme Minderung Ruecktritt Schadensersatz. Open-Source-Compliance GPL AGPL MIT Apache Verjaehrung zwei Jahre § 438 BGB Kauf oder § 634a BGB Werk fuenf Jahre bei Bauwerks-aehnlicher Software.
---

# Softwarefehler — Mangelhaftung prüfen

## Zweck

Software-Mängel sind häufige Streitthema — Bugs Performance-Probleme Schnittstellen-Defekt Sicherheitslücke. Der erste Schritt ist immer: welcher Vertragstyp liegt zugrunde?

## Eingaben

- Vertrag mit Anlagen (Pflichtenheft Service Level Agreement)
- Lizenzbedingungen (kommerziell Open-Source)
- Lieferung Datum Übergabe Abnahme
- Mangelbeschreibung Fehlerprotokoll Logfiles
- Korrespondenz Service-Tickets
- Nachbesserungsversuche bisheriger Behebungsstand

## Schritt 1 — Vertragstyp bestimmen

| Konstellation | Vertragstyp |
|---|---|
| Standardsoftware auf Datenträger | Kaufrecht §§ 433 ff. BGB BGH VIII ZR 6/89 |
| Standardsoftware-Download Lizenz-überlassung dauernd | Kaufrecht analog BGH VIII ZR 50/13 |
| Individualsoftware-Erstellung | Werkvertrag §§ 631 ff. BGB |
| Software-Anpassung Customizing | Werkvertrag §§ 631 ff. BGB |
| SaaS Software-as-a-Service | Mietrecht §§ 535 ff. BGB BGH XII ZR 120/04 ASP |
| Beratungs-/Implementierungsleistung | Dienstvertrag § 611 BGB (häufig im Bündel mit Werkvertrag) |
| Wartungs-Vertrag | Werk- oder Dienstvertrag — je nach Erfolgsbezug |
| Lizenz-Überlassung zeitlich befristet | Mietrecht/Pacht analog |

## Schritt 2 — Mangelbegriff

### Kauf § 434 BGB

- Vereinbarte Beschaffenheit (Pflichtenheft)
- Vertraglich vorausgesetzte Verwendung
- Übliche Beschaffenheit / vergleichbarer Software
- Werbeaussagen

### Werk § 633 BGB

- Vereinbarte Beschaffenheit
- Vertraglich vorausgesetzte Verwendung
- Übliche Beschaffenheit

### SaaS Miete § 536 BGB

- Vereinbarte Beschaffenheit
- Tauglichkeit zum vertragsgemäßen Gebrauch
- Mangelfreie Bereitstellung

### Software-spezifisches

- Bugs mit Ausfallzeit
- Performance unter Belastung
- Datenschutz Sicherheit (Sicherheitslücke kann Mangel sein — BGH VIII ZR 30/12 vergleichbare Logik)
- Schnittstellen funktionieren nicht
- Datenmigration unvollständig
- Dokumentation fehlt / fehlerhaft

## Schritt 3 — Abnahme bei Werkvertrag

- Erforderlich bei Werkvertrag § 640 BGB
- **Abnahmefähigkeit** wenn Hauptfunktion erbracht und nur unwesentliche Mängel
- **Konkludente Abnahme** bei Ingebrauchnahme produktiv ohne wesentliche Rüge
- Vorbehaltsregelung § 640 Abs. 3 BGB

## Schritt 4 — Mangelrüge

### Kauf — Untersuchungs- und Rügeobliegenheit § 377 HGB

- Bei beidseitig kaufmännischem Geschäft Pflicht
- Unverzüglich nach Lieferung (auf Software bezogen typisch nach Inbetriebnahme)
- Bei versteckten Mängeln nach Entdeckung

### Werk — Mangelrüge an sich

- Substanziiert (Sympomtheorie BGH VII ZR 41/02)
- Fristsetzung zur Nachbesserung

## Schritt 5 — Nachbesserungsrecht

- Erstmal Nacherfüllung § 439 BGB / § 635 BGB
- Verkäufer Wahlrecht (Kauf) — Unternehmer Wahlrecht (Werk)
- Frist setzen — angemessen unter Berücksichtigung Schwere Komplexität
- Zwei Versuche im Kauf typisch BGH VIII ZR 159/97

## Schritt 6 — Sekundärrechte

- **Minderung** § 441 BGB / § 638 BGB
- **Rücktritt** § 437 Nr. 2 BGB / § 636 BGB
- **Schadensersatz statt der Leistung** § 437 Nr. 3 BGB / § 281 BGB
- **Schadensersatz neben der Leistung** § 280 Abs. 1 BGB (Mangelfolgeschaden)
- **Selbstvornahme** § 637 BGB Werkvertrag — Vorschuss-Anspruch

## Schritt 7 — Verjährung

- **Kauf** zwei Jahre § 438 BGB ab Übergabe
- **Werk** zwei Jahre § 634a BGB ab Abnahme
- **Werk Bauwerk-Software** fünf Jahre — strittig ob ERP-Implementierung dazu zählt (eher nicht — BGH X ZR 76/05)
- **Miete** drei Jahre § 195 BGB

## Schritt 8 — AGB-Kontrolle

- Häufige unwirksame Klauseln in IT-AGB:
  - Vollständige Haftungsfreizeichnung § 309 Nr. 7 BGB
  - "Wie besichtigt" beim Verbrauchsgüterkauf
  - Verkürzte Verjährung unter ein Jahr
  - Pauschalierter Schadensersatz nicht angemessen § 309 Nr. 5 BGB
  - Einseitiges Leistungsänderungsrecht § 308 Nr. 4 BGB

## Schritt 9 — Open-Source-Compliance

- Lizenzpflicht prüfen (GPL AGPL LGPL MIT BSD Apache)
- Bei Verletzung Unterlassung Auskunft Schadensersatz
- Heise GMBH Urteil OLG Frankfurt 11 W 22/05 (älterer Klassiker)
- D-Link / Versia-Linux-Urteil LG München I (klassische OSS-Compliance-Pflicht)

## Schritt 10 — Datenschutz-Mangel

- Sicherheits-Lücke ist potentieller Mangel
- DSGVO-Verstoß durch Software kann Mangel sein wenn vertraglich Sicherheitsstandard zugesagt
- Verweis Datenschutz-Plugin für Vertiefung

## Schritt 11 — SLA-Verletzungen bei SaaS

- Verfügbarkeit kommentiert in Prozent
- Reaktionszeit-Stufen
- Vertragsstrafe Service Credits
- Sonderkündigungsrecht bei wiederholter SLA-Verletzung

## Ausgabe

- `software-mangel-analyse.md` mit Vertragstyp-Bestimmung
- Tabelle pro Mangel mit Bewertung und Anspruchsempfehlung
- Mangelrüge / Fristsetzung als Entwurf
- Klage-/Schadensersatz-Berechnung
- Frist im Fristenbuch (Verjährung zwei oder fünf Jahre)
- Bei Open-Source: Compliance-Empfehlung

## Quellen

- BGB §§ 280 281 433 437 438 439 535 536 611 631–650 634a
- HGB § 377
- DSGVO Art. 32 (Sicherheit)
- BGH VIII. Zivilsenat VII. Zivilsenat X. Zivilsenat
- Marly Praxishandbuch Softwarerecht
- Schneider IT-Recht
