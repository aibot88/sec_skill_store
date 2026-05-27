---
name: tom-und-zertifizierungen-pruefen
description: "Pruefe technische und organisatorische Massnahmen des KI-Anbieters und seine Zertifizierungen. Maßstab Art. 32 DS-GVO ISO 27001 BSI C5 (Cloud Computing Compliance Criteria Catalogue) SOC zwei Typ zwei TISAX. Zentral fuer Berufsrecht no training Zero-Retention EU-Hosting Verschluesselung Loeschkonzept Audit-Recht. DAV-Stellungnahme Seite dreizehn vierzehn."
---

# TOM und Zertifizierungen prüfen

## Disclaimer

Diese Forprüfung ist keine Rechtsberatung, sondern strukturierte Argumentationshilfe für das Anbietergespräch. Die abschließende berufsrechtliche und strafrechtliche Beurteilung bleibt der inhabilen Kanzlei beziehungsweise einer beauftragten Spezialkanzlei vorbehalten.

## Norm und Rahmen

Berufsrechtlich verlangt die Sorgfaltspflicht bei der Dienstleisterauswahl (Abs. 2 der jeweiligen Dienstleisterregelung), dass die technische und organisatorische Sicherheit des Anbieters überzeugt. Datenschutzrechtlich präzisiert das Art. 32 DS-GVO. Die DAV-Stellungnahme 32/2025 (Seite 13) stellt klar: Die Verschlüsselung darf nicht so weit gefordert werden, dass sie die KI-Dienstleistung entwertet. Eine Ende-zu-Ende-Verschlüsselung, die das KI-System-Inferencing unmöglich macht, ist berufsrechtlich nicht zu verlangen.

## "no training" — Zentralfrage

Nach DAV S. 14 ist die Übermittlung von Mandatsdaten zu Trainingszwecken nicht von der Erforderlichkeitsschwelle des Abs. 1 gedeckt. Daher muss der Vertrag eine **"no training"-Klausel** enthalten — eine ausdrückliche Verpflichtung des Anbieters, eingegebene Mandatsdaten nicht zum Training des Modells zu verwenden. Bei API-Aufrufen an Drittmodelle (etwa OpenAI Azure Service) ist zusätzlich der "no training"-Status des Drittmodells nachzuweisen.

## Zero Retention

Die Speicherdauer eingegebener Mandatsdaten beim Anbieter ist möglichst gering zu halten. Optimal: "Zero Retention" — die Daten werden nach der Verarbeitung sofort gelöscht (typisch 0 oder 30 Sekunden nach Abschluss der API-Anfrage). Andernfalls eine konkrete kurze Frist (24 Stunden, sieben Tage). Pauschalfristen wie "bis zu 90 Tage" sind problematisch.

## Zertifizierungen

### ISO 27001

Internationaler Standard für Informationssicherheitsmanagementsysteme. **Mindeststandard**. Prüfen: Geltungsbereich (alle relevanten Standorte und Systeme), Zertifizierungsstelle (akkreditiert), Ausstellungsdatum (höchstens drei Jahre alt), Anhang A Controls relevant.

### BSI C5 (Cloud Computing Compliance Criteria Catalogue)

Vom BSI entwickelter Standard für Cloud-Anbieter. Für Berufsgeheimnisträger besonders aussagekräftig, weil deutsche behördliche Standardkriterien. Es gibt Typ-1- und Typ-2-Testate; Typ 2 ist der Goldstandard.

### SOC 2 Typ 2

US-Standard, oft bei US-Anbietern vorhanden. Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy. Bei US-Anbietern Mindestnachweis, aber nicht spezifisch genug für deutsches Berufsrecht.

### TISAX

Branchenstandard der Automobilindustrie. Für Legal-AI selten einschlägig, aber bei Mandanten aus der Automotive-Branche relevant.

### EU Cloud Code of Conduct

DSGVO-spezifisches Konformitätsverfahren nach Art. 40 DS-GVO. Hilfreich, aber keine eigenständige Sicherheitszertifizierung.

## Konkrete Prüfpunkte

### EU-Hosting

- Speicherort der Daten ausschließlich in EU/EWR?
- Auch Backups in EU/EWR?
- Verarbeitung (Inferencing) in EU/EWR?
- Vertraglich abgesichert oder nur als Selbstauskunft?

### Verschlüsselung

- Transportverschlüsselung TLS aktuell (mindestens TLS einskommadrei)
- Verschlüsselung im Ruhezustand (AES 256)
- Schlüsselverwaltung: Anbieter oder Kanzlei (Bring-your-own-key)?

### Zugriffskontrolle

- Rollenbasierte Zugriffskontrolle beim Anbieter
- Audit-Logs aller Zugriffe auf Mandatsdaten
- Vier-Augen-Prinzip bei Administratorenzugriffen
- Mitarbeiter-Verpflichtungen (Verschwiegenheit, Background Check)

### Löschkonzept

- Auf Anforderung der Kanzlei
- Automatisch nach Vertragsende
- Bestätigung der Löschung durch Anbieter (Löschprotokoll)
- Auch in Backups und Logs

### Audit-Recht

- Recht der Kanzlei zur Auditierung
- Vorhandene Testate als Surrogat (typisch)
- Mindestens jährliche Aktualisierung der Testate

### Meldepflichten

- Information bei Sicherheitsvorfällen (24 bis 48 Stunden)
- Information bei Behördenanfragen
- Information bei Subunternehmerwechsel

## Prüfschema

| Punkt | Status | Ampel | Bemerkung |
|---|---|---|---|
| "no training"-Klausel | | | |
| Zero Retention oder kurze Frist | | | |
| ISO 27001 (akt. Testat) | | | |
| BSI C5 (Typ 2 bevorzugt) | | | |
| SOC 2 Typ 2 | | | |
| EU-Hosting vertraglich | | | |
| Verschlüsselung TLS plus Rest | | | |
| Audit-Logs | | | |
| Löschkonzept | | | |
| Meldepflicht Sicherheitsvorfall | | | |
| Audit-Recht | | | |

## Typische Lücken

- "Wir nehmen Sicherheit ernst" ohne Zertifikat
- ISO-Zertifikat nur für Hauptsitz, nicht für Verarbeitungsstandort
- Trust Center mit Versprechen, die nicht im Vertrag stehen
- Löschung nur "auf Anforderung", keine automatische
- Keine "no training"-Klausel für das verwendete Modell

## Output

Tabellarische Bewertung. Defizite landen im Rückfragebrief mit der Aufforderung, Zertifikate, Geltungsbereiche und Vertragsklauseln vorzulegen.
