---
name: spam-und-massen-anfrage-filter
description: "Erkennt Spam-Muster in eingehenden Mandantenanfragen: Werbung, Spamfilter-Umgehung, klassische 419-Scams, automatisierte Recruiter-Mails, Massen-Mandantenanfragen und Phishing. Kennzeichnet die Anfrage zur Aussortierung ohne Erstantwort. Laedt wenn der Nutzer 'Spam pruefen', 'verdaechtige Anfrage', 'Scam-Mail', '419-Betrug', 'Massen-Anfrage erkennen' oder 'Phishing Kanzlei' sagt."
---

# Spam-und-Massen-Anfrage-Filter

Dieser Skill erkennt und kennzeichnet eingehende E-Mails, die keine legitimen Mandantenanfragen sind. Bei positiver Spam-Erkennung wird keine Erstantwort generiert; stattdessen erhält das Sekretariat eine Aussortierungsempfehlung.

## Spam-Muster-Katalog

### Kategorie 1: Klassischer 419-Scam (Vorschussbetrug)

Kennzeichen:
- Absender aus Drittländern, die nicht zum Sachverhalt passen
- Schilderung großer Summen, die „transferiert" werden sollen
- Anfrage nach Treuhandkonto, Bankkontodaten oder Vorleistungen
- Formulierungen: „millions of dollars", „strictly confidential", „God bless you"
- Regelmäßig schlechtes Deutsch oder maschinell übersetzter Text

Aktion: `SPAM — 419-SCAM`

### Kategorie 2: Automatisierte Massen-Mandantenanfragen

Kennzeichen:
- Identischer Wortlaut in mehreren eingehenden Mails
- Merkmale automatisierter Erstellung: fehlende Personalisierung, Template-Formulierungen
- Ungewöhnliche Absenderadressen (zufällige Zeichenfolgen, zahlreiche Ziffern)
- Keine konkreten Sachverhaltsdaten

Aktion: `SPAM — MASSEN-ANFRAGE`

### Kategorie 3: Werbung und Newsletter

Kennzeichen:
- Angebotscharakter: Dienstleistungen, Produkte, Software für die Kanzlei
- Opt-out-Link vorhanden
- „Unsubscribe"- oder „Abbestellen"-Hinweis
- Absender ist erkennbar ein Unternehmen, nicht eine Privatperson

Aktion: `KEIN-SPAM — WERBUNG` (gesonderter Kanal; kein Erstantwort-Prozess)

### Kategorie 4: Automatisierte Recruiter-Mails

Kennzeichen:
- Angebot von Kandidaten für offene Stellen
- Formulierungen wie „Ich bin auf Ihr Unternehmen aufmerksam geworden"
- Anhänge mit Lebenslauf ohne Bezug zu einer Stellenausschreibung
- Häufig über LinkedIn- oder XING-Weiterleitungen

Aktion: `KEIN-SPAM — RECRUITER` (Weiterleitung an HR-Kanal)

### Kategorie 5: Phishing-Versuche

Kennzeichen:
- Links zu gefälschten Webseiten (URL-Check: Domain nicht zur angeblichen Organisation passend)
- Dringende Aufforderung, Zugangsdaten einzugeben
- Drohende Konsequenzen bei Nicht-Antwort innerhalb kurzer Frist
- Absender gibt sich als bekannte Institution aus (Finanzamt, Gericht, Strafverfolgungsbehörde)

Aktion: `SPAM — PHISHING` und: Hinweis an Kanzlei-IT

### Kategorie 6: Spamfilter-Umgehungsversuche

Kennzeichen:
- Wörter mit Ziffern statt Buchstaben: „R3cht", „An1walt"
- Unsichtbare Zeichen, übermäßige HTML-Formatierung
- Betreff-Zeile in Großbuchstaben: „DRINGEND!!!" ohne Substanz
- Mehrfache Leerzeichen oder Zeilenumbrüche zur Zeichentrennung

Aktion: `SPAM — FILTER-UMGEHUNG`

## Positive-Signal-Liste (kein Spam)

Die folgenden Merkmale sprechen gegen Spam:
- Konkreter Sachverhalt mit Datum, Personen, Ort
- Deutschsprachig oder in einer der unterstützten Sprachen (EN, FR, IT)
- Persönliche Anrede oder Selbstvorstellung
- Reale Absender-Domain (kein Wegwerf-Mail-Dienst)
- Anhang mit relevanten Dokumenten (Kündigung, Bescheid, Vertrag)

## Ausgabeformat

```
SPAM-CHECK ERGEBNIS
===================
Status:      [KLAR / VERDÄCHTIG / SPAM — TYP]
Konfidenz:   [HOCH / MITTEL / NIEDRIG]
Erkannte Muster: [Liste der erkannten Muster oder „keine"]
Empfehlung:  [Normale Bearbeitung / Manuelle Prüfung / Aussortieren / IT-Meldung]
```

## Verhalten bei SPAM-Erkennung

1. Keine Erstantwort generieren.
2. Skeleton-Eintrag im CRM nur mit Status „SPAM" und Typ; keine vollständige Datenerfassung.
3. Sekretariat erhält Hinweis mit Aussortierungsempfehlung.
4. Bei Phishing: zusätzliche Meldung an die Kanzlei-IT.
5. Bei VERDÄCHTIG (nicht eindeutig): Empfehlung zur manuellen Prüfung durch Rechtsanwalt oder erfahrene Mitarbeitende vor Beantwortung.

## Falsch-Positiv-Schutz

Der Filter ist bewusst konservativ eingestellt. Im Zweifel lieber `VERDÄCHTIG` als `SPAM` — echte Anfragen dürfen nicht unbeantwortet aussortiert werden. Die Endentscheidung liegt immer beim Sekretariat.

## Verweise auf andere Skills

- `anfrage-eingang-parser` — liefert den geparsten Text für die Filter-Analyse
- `folgekorrespondenz-vorbereiten` — erhält den Spam-Status
- `dringlichkeitsmarker` — läuft nur bei KLAR-Status
- `erstantwort-generator` — wird nur bei KLAR-Status ausgeführt
