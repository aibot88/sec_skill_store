---
name: vidis-check
version: 0.1.0
description: |
  Validates a web app or codebase against the VIDIS Prüfkriterien V0.2 (eduCheck digital).
  Checks all criteria from both Prüfbereiche: Recht & Datenschutz and IT-Sicherheit.
  Produces a structured compliance report with PASS / FAIL / MANUELL (needs human review) for each criterion.
  Use when asked to "vidis check", "VIDIS prüfen", "eduCheck prüfen", or "VIDIS-Kriterien".
---

# /vidis-check — VIDIS Prüfkriterien Compliance Check

Du führst jetzt eine vollständige VIDIS Prüfkriterien-Prüfung (V0.2) durch.

## Schritt 1 — Zielgruppe klären

Falls nicht aus dem Kontext klar, frage zuerst:
> "Richtet sich das Angebot an **Schülerinnen und Schüler (SuS)**, **Lehrkräfte**, oder **beide**?"

Die Antwort bestimmt, welche Kriterien mit strengeren Anforderungen gelten (SuS dürfen keine Einwilligungen geben).

## Schritt 2 — Codebase analysieren

Untersuche den Code systematisch:
- Suche nach Cookies, localStorage, sessionStorage, IndexedDB
- Suche nach Script-Tags, fetch/XHR-Calls, iframe-Einbindungen (Drittinhalte/CDN)
- Suche nach Tracking-Bibliotheken (Google Analytics, Matomo, Hotjar, Meta Pixel, etc.)
- Prüfe HTTP/HTTPS-Konfiguration (nginx/apache config, next.config, vite.config, etc.)
- Suche nach TLS-Konfigurationen
- Prüfe auf In-App-Purchase-Mechanismen, Werbebanner, Affiliate-Links
- Suche nach Impressum und Datenschutzerklärung im Code/Content
- Prüfe IP-Logging / Request-Logging Retention-Konfiguration

## Schritt 3 — Bericht ausgeben

Gib den Bericht in diesem exakten Format aus:

```
VIDIS Prüfkriterien V0.2 — Compliance Report
Zielgruppe: [SuS / Lehrkräfte / beide]
Datum: [heute]

═══ PRÜFBEREICH: RECHT & DATENSCHUTZ ═══

── Content Delivery Network ──
[RDS-CDN-379] CDN nur zur Bereitstellung von Inhalten
  Status: PASS / FAIL / MANUELL
  Befund: [ein Satz]

── Cookies & Co. ──
[RDS-CUC-371] Nicht essenzielle Cookies          MUSS
[RDS-CUC-372] Cookies allgemein                  MUSS
[RDS-CUC-373] Trackingpixel                      MUSS
[RDS-CUC-374] Local Browser Storage              MUSS
[RDS-CUC-375] Informationen auf Endeinrichtung   MUSS
[RDS-CUC-376] Browserfingerprints                MUSS
[RDS-CUC-377] Trackingmechanismen (nicht pädag.) MUSS
[RDS-CUC-453] Beschreibung aller Cookies         MUSS
  (je Kriterium: Status + ein-Satz-Befund)

── Datenerhebung und -verarbeitung ──
[RDS-DEV-380] Datenerhebung und -verarbeitung    MUSS
[RDS-DEV-381] Daten nach Beendigung Zusammenarb. MUSS
[RDS-DEV-466] Sichere Datenverarbeitung          MUSS

── Datenschutzorganisation ──
[RDS-DSO-383] Benennung Datenschutzbeauftragter  MUSS

── Dienstleister ──
[RDS-DIL-356] AV-Vertrag vorhanden               MUSS
[RDS-DIL-357] Mutterunternehmen Drittländer       MUSS
[RDS-DIL-358] Subdienstleister Drittländer        MUSS

── Drittinhalte ──
[RDS-DRI-378] Einbindung von Drittinhalten        MUSS

── Einwilligung ──
[RDS-EWG-382] Keinerlei Einwilligung durch SuS   MUSS

── Informationspflichten ──
[RDS-IPF-364] Leicht auffindbares Impressum      MUSS
[RDS-IPF-365] Leicht auffindbare Datenschutzerkl. MUSS
[RDS-IPF-366] Vollständiges Impressum            MUSS
[RDS-IPF-367] Vollständige Datenschutzerklärung  MUSS

── Kostenpflichtige Bestandteile ──
[RDS-KBT-386] Kostenpflichtige Zusatzangebote    MUSS

── Nutzungsbedingungen und AGB ──
[RDS-AGB-368] AGB: Datenschutzkonform            MUSS
[RDS-AGB-369] AGB: AVV-konform                   MUSS

── Speicherung ──
[RDS-SPE-370] IP-Adresse / http-requests ≤7 Tage MUSS

── Umsetzung von Betroffenenrechten ──
[RDS-UBR-387] Datenexport / Portierung           SOLL
[RDS-UBR-388] Betroffenenrechte (Filter/Sperre)  MUSS

── Verbotene Inhalte ──
[RDS-VIN-354] Jugendmedienschutz                 MUSS

── Werbefreiheit ──
[RDS-WER-384] Werbefreiheit                      MUSS
[RDS-WER-385] Verweise auf Werbeinhalte          MUSS

═══ PRÜFBEREICH: IT-SICHERHEIT ═══

── Systemhärtung ──
[ITS-SHR-362] Sichere Webserver (Heartbleed etc.) MUSS

── Verschlüsselung ──
[ITS-ENC-359] Website nur über HTTPS             MUSS
[ITS-ENC-360] HTTP → HTTPS Redirect              MUSS
[ITS-ENC-361] Ablehnen veralteter TLS/SSL        MUSS

═══ ZUSAMMENFASSUNG ═══
PASS:    X Kriterien
FAIL:    X Kriterien  ← blockiert VIDIS-Zulassung
MANUELL: X Kriterien  ← manuelle Prüfung erforderlich

VIDIS-Zulassung: MÖGLICH / NICHT MÖGLICH (solange FAIL-Kriterien offen)

── FAIL-Kriterien (priorisiert beheben) ──
1. [ID] Kurze Problembeschreibung → empfohlene Maßnahme
...

── MANUELL zu prüfen ──
1. [ID] Was genau geprüft werden muss (z.B. AV-Vertrag mit Dienstleister X vorhanden?)
...
```

## Kriterien-Details für die Bewertung

### Was PASS bedeutet
- Code-basiert prüfbar und Anforderung erfüllt
- Konfiguration ist korrekt gesetzt

### Was FAIL bedeutet  
- Code-Evidenz für Verletzung gefunden (z.B. Google Analytics Script ohne Consent für SuS)
- Konfiguration eindeutig falsch (z.B. HTTP ohne Redirect)

### Was MANUELL bedeutet
- Nicht aus Code ableitbar (z.B. ob AV-Verträge existieren)
- Rechtliche Dokumente vorhanden aber Vollständigkeit unklar
- Externe Dienstleister erkannt, aber Drittland-Status unbekannt

## Kriterien-Referenz

### RDS-CDN-379
Kein CDN einsetzen, das nicht ausschließlich der Bereitstellung von Inhalten dient. CDN muss auch Anforderungen des Prüfbereichs "Dienstleister" erfüllen.
→ Code-Check: `<script src="...cdn...">`, externe Font-/Asset-URLs, package.json externe CDN-Referenzen

### RDS-CUC-371 — RDS-CUC-377 (SuS-Zielgruppe)
Bei SuS: **Keine** nicht-essenziellen Cookies, Trackingpixel, localStorage/sessionStorage (wenn Einwilligung nötig), Fingerprinting, Tracking außer pädagogisch notwendig.
Bei Lehrkräften: Einwilligung darf eingeholt werden.
→ Code-Check: cookie-Setter, `document.cookie`, `localStorage.setItem`, Fingerprint-Libraries, Analytics-Scripts

### RDS-CUC-453
Alle Cookies im Angebot in der Datenschutzerklärung beschrieben.
→ Manuell: Datenschutzerklärung lesen + gefundene Cookies abgleichen

### RDS-DEV-380
Daten ausschließlich für Nutzungszweck, nicht für Werbung.
→ Code-Check: Werbenetze, AdSense, Affiliate-Tracking, Data-Broker-APIs

### RDS-DEV-381
Nach Vertragsende: Daten löschen oder herausgeben (Wahl des Auftraggebers).
→ Manuell: Vertragsunterlagen, Offboarding-Prozess

### RDS-DEV-466
Keine Server/Datenverarbeitung in unsicheren Drittländern (inkl. Sub- und Mutterunternehmen).
→ Code-Check: Hosting-Konfiguration, Cloud-Provider, Datenbankverbindungen

### RDS-DSO-383
Kontaktdaten des Datenschutzbeauftragten bereitstellen.
→ Code-Check: Impressum/Datenschutzerklärung auf DSB-Kontakt prüfen

### RDS-DIL-356
Nur Dienstleister mit AV-Vertrag gem. Art. 28 Abs. 3 DSGVO.
→ Manuell: Dienstleisterliste + AVV-Nachweise

### RDS-DIL-357 / RDS-DIL-358
Verbundene Unternehmen/Subdienstleister in Drittländern: Zugriff ausgeschlossen oder zusätzliche Schutzmaßnahmen nachgewiesen.
→ Manuell: Konzernstruktur der genutzten Dienstleister prüfen

### RDS-DRI-378
Keine Drittinhalte die Einwilligung erfordern (für SuS). Ausnahme: ausschließlich Lehrkräfte.
→ Code-Check: `<iframe>`, externe `<script>`, `<img src="...externe-domain...">`, fetch zu Drittdomains

### RDS-EWG-382
Keine Datenverarbeitung, in die SuS einwilligen können (auch kein Consent-Banner).
→ Code-Check: Cookie-Banner-Code, Consent-Management-Bibliotheken (OneTrust, CookieBot, etc.)

### RDS-IPF-364 / RDS-IPF-365
Impressum und Datenschutzerklärung von allen Seiten erreichbar (auch responsive).
→ Code-Check: Footer-Links, Navigation, ob beide URLs in allen Templates vorhanden

### RDS-IPF-366
Impressum mit allen §§ 5, 6 DDG-Pflichtangaben (Name, Anschrift, Kontakt, Vertretungsberechtigte).
→ Manuell: Impressum-Inhalt prüfen

### RDS-IPF-367
Datenschutzerklärung mit allen Art. 13/14 DSGVO-Pflichtangaben.
→ Manuell: Datenschutzerklärung-Inhalt prüfen

### RDS-KBT-386
Keine In-App-Käufe, Freemium-Modelle oder kostenpflichtige Upgrades für SuS.
→ Code-Check: Payment-APIs, Stripe/PayPal-Integrationen, Upgrade-Flows, Feature-Flags hinter Paywall

### RDS-AGB-368 / RDS-AGB-369
AGB/Nutzungsbedingungen datenschutzkonform und AVV-konform.
→ Manuell: AGB-Inhalt prüfen

### RDS-SPE-370
IP-Adresse und HTTP-Request-Logs max. 7 Tage gespeichert.
→ Code-Check: Log-Retention-Konfiguration, nginx/apache log settings, Datenbankeinträge mit IP

### RDS-UBR-387 (SOLL)
Datenexport-Funktion vorhanden und funktionsfähig.
→ Code-Check: Export-Endpunkte, Download-Buttons für Nutzerdaten

### RDS-UBR-388
Betroffenenrechte technisch umsetzbar: Filterung, Suche, Sperrung von Daten.
→ Code-Check: Admin-Interface, DSGVO-Request-Handling

### RDS-VIN-354
Angebot jugendmedienschutzrechtlich unbedenklich (kein Extremismus, Pornografie, Diskriminierung, etc.)
→ Manuell: Content-Review

### RDS-WER-384
Digitales Bildungsangebot ist werbefrei.
→ Code-Check: Ad-Netzwerke, AdSense, Banner-Ads, gesponserte Inhalte

### RDS-WER-385
Keine Verlinkung auf werbefinanzierte Zielseiten für SuS.
→ Code-Check: Externe Links analysieren

### ITS-SHR-362
Webserver gegen bekannte Schwachstellen abgesichert (Heartbleed, CRIME, Downgrade-Angriffe). Patchmechanismen etabliert.
→ Code-Check: Server-Konfigurationsdateien, Dependency-Versionen, Security-Headers

### ITS-ENC-359
Alle Seiten ausschließlich über HTTPS erreichbar.
→ Code-Check: Server-Config, .htaccess, next.config.js, Middleware

### ITS-ENC-360
HTTP-Anfragen werden auf HTTPS umgeleitet.
→ Code-Check: Redirect-Konfiguration in Server/Framework

### ITS-ENC-361
Veraltete TLS/SSL-Protokolle (SSLv2, SSLv3, TLS 1.0, TLS 1.1) werden abgelehnt.
→ Code-Check: SSL-Konfiguration (nginx ssl_protocols, apache SSLProtocol)

## Hinweise

- Fokus auf **MUSS**-Kriterien — diese sind für VIDIS-Zulassung zwingend
- RDS-UBR-387 ist **SOLL** — empfohlen aber kein Ausschlusskriterium
- Scope "Angebot" = prüfbar aus Code; Scope "Anbieter" = meist nur manuell prüfbar
- Bei Unsicherheit lieber MANUELL als PASS — falsche Sicherheit ist schädlicher als offene Fragen
