---
name: transparency-audit
description: Prüft die Transparenz-Compliance des Menschlichkeit Österreich Projekts — ZVR-Nummer 1182213083, Vereinsstatuten, Datenschutzerklärung und Impressum auf Vollständigkeit und Korrektheit. Wird aufgerufen bei `/transparency-audit`.
argument-hint: '[vollständig|schnell|datenschutz|impressum]'
allowed-tools:
  - Read
  - Grep
  - Bash
  - WebFetch
---

# Transparency Audit für Menschlichkeit Österreich

Du führst eine strukturierte Transparenz-Prüfung für den Verein Menschlichkeit Österreich durch.

## Vereinsdaten (unveränderlich)

- **ZVR-Nummer**: 1182213083
- **Vereinsname**: Menschlichkeit Österreich
- **Domain**: menschlichkeit-oesterreich.at
- **Datenschutz-URL**: https://menschlichkeit-oesterreich.at/datenschutz
- **Impressum-URL**: https://menschlichkeit-oesterreich.at/impressum

---

## Prüfschritt 1 — ZVR-Nummer in allen relevanten Dateien

Prüfe ob ZVR-Nummer `1182213083` vorkommt in:

```bash
rg -n "1182213083" apps/website/src
rg -n "1182213083" apps/crm
rg -n "1182213083" . -g "*.md"
rg -n "1182213083" . -g "*.html"
```

**Erwartete Fundorte:**

- [ ] Impressum-Seite (Website)
- [ ] Datenschutzerklärung (Website)
- [ ] CRM-Kontakt-Header (`apps/crm/`)
- [ ] CLAUDE.md oder README

Fehlende Fundorte als `[FEHLT]` markieren.

---

## Prüfschritt 2 — Impressum-Vollständigkeit (§ 5 ECG Österreich)

Lies die Impressum-Datei(en):

```bash
Get-ChildItem -Recurse -Path . -Include "impressum*","Impressum*" | Select-Object -First 5 -ExpandProperty FullName
```

**Pflichtangaben gemäß § 5 ECG:**

- [ ] Vereinsname vollständig
- [ ] ZVR-Nummer: 1182213083
- [ ] Zuständige Aufsichtsbehörde
- [ ] Vertretungsberechtigte Person(en) / Vorstand
- [ ] Postanschrift
- [ ] E-Mail-Adresse
- [ ] Angabe des Vereinszwecks
- [ ] Vereinssitz / Bundesland

Jedes fehlende Pflichtfeld als `[FEHLT — § 5 ECG]` kennzeichnen.

---

## Prüfschritt 3 — Datenschutzerklärung (DSGVO Art. 13/14)

```bash
Get-ChildItem -Recurse -Path . -Include "datenschutz*","Datenschutz*" | Select-Object -First 5 -ExpandProperty FullName
Get-ChildItem -Recurse -Path . -Include "privacy*" | Select-Object -First 5 -ExpandProperty FullName
```

**Pflichtinhalte gemäß DSGVO:**

- [ ] Verantwortlicher (Name + Adresse)
- [ ] Datenschutzbeauftragter oder Kontakt
- [ ] Zweck und Rechtsgrundlage der Verarbeitung
- [ ] Empfänger / Weitergabe an Dritte (Stripe, PayPal, CiviCRM)
- [ ] Speicherdauer
- [ ] Betroffenenrechte (Art. 15-22 DSGVO)
- [ ] Recht auf Beschwerde bei der Datenschutzbehörde Österreich
- [ ] Hinweis auf Cookie-Verwendung
- [ ] Einwilligungswiderruf (Newsletter)

---

## Prüfschritt 4 — Vereinsstatuten-Referenz

```bash
Get-ChildItem -Recurse -Path . -Include "statuten*","Statuten*","satzung*" | Select-Object -First 5 -ExpandProperty FullName
rg -n "Statuten|Vereinsstatut" . -g "*.md" | Select-Object -First 10
```

Prüfe ob die Statuten:

- [ ] Im Repository vorhanden oder verlinkt sind
- [ ] Den aktuellen Vereinszweck korrekt beschreiben
- [ ] Mit den CLAUDE.md-Angaben übereinstimmen

---

## Prüfschritt 5 — Cookie-Banner und Einwilligung

```bash
rg -n "cookie|Cookie|Einwilligung|consent" apps/website/src | Select-Object -First 20
```

- [ ] Cookie-Banner mit Opt-In (nicht nur Opt-Out)
- [ ] Granulare Auswahl (notwendig / Analyse / Marketing)
- [ ] Einwilligung wird gespeichert und abrufbar

---

## Ausgabe

Erstelle einen strukturierten Bericht:

```
# Transparenz-Audit Menschlichkeit Österreich
Datum: [heute]
ZVR-Nummer: 1182213083

## Zusammenfassung
✅ Bestanden: X Prüfpunkte
⚠️  Warnung: X Punkte
❌ Fehler: X Pflichtangaben fehlen

## Details
[Alle Findings mit Dateipfad und Zeile]

## Empfehlungen
[Priorisierte Behebungsschritte]
```

Alle Ausgaben auf **Österreichisches Deutsch**.
