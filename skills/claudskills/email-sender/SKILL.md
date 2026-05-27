---
name: email-sender
description: Send and read emails via SMTP/IMAP using configured accounts (Web.de, Gmail, etc.). Supports plain text, HTML emails, attachments, CC/BCC, IMAP reading, searching, thread tracking, and summarization. Features retry-logic, timeout handling, and proper logging. Uses credentials from .env file.
version: 3.0
---

# Email Skill v3.0

Vollständiger E-Mail-Support: Senden **und** Lesen. SMTP + IMAP mit konfigurierten Accounts aus der .env Datei.

## ✨ Features v3.0

### Senden (SMTP)
- ✉️ **HTML-E-Mails** – HTML-Formatierung mit Plain-Text-Fallback
- 📎 **Anhänge** – Mehrere Dateianhänge pro E-Mail
- 📋 **CC/BCC** – Mehrere Empfänger
- 🔁 **Retry-Logik** – Automatische Wiederholung bei Verbindungsfehlern (Exponential Backoff)
- ⏱️ **Timeout-Handling** – Konfigurierbare Timeouts
- ✅ **E-Mail-Validierung** – Regex-Prüfung aller Adressen

### Lesen (IMAP) — NEU!
- 📬 **Ungelesene E-Mails** abrufen
- 🔍 **Suche** nach Betreff, Absender, Datum
- 📁 **Ordner auflisten** und wechseln
- 🧵 **Thread-Verfolgung** (Message-ID, References)
- 📝 **Zusammenfassung** generieren
- ✅ **Als gelesen markieren**
- 📎 **Anhänge** erkennen und Informationen anzeigen
- 📊 **JSON-Ausgabe** für programmatische Verarbeitung

## Voraussetzungen

### SMTP/IMAP-Zugangsdaten in .env eintragen

```bash
# Web.de
WEBDE_EMAIL=deine-email@web.de
WEBDE_PASSWORD=dein_passwort

# Gmail (App-Passwort nötig!)
GMAIL_EMAIL=dein.name@gmail.com
GMAIL_PASSWORD=dein_app_passwort

# GMX
GMX_EMAIL=deine-email@gmx.de
GMX_PASSWORD=dein_passwort
```

**Wichtig für Gmail:**
- Normales Passwort funktioniert NICHT
- 2FA aktivieren → App-Passwort erstellen → Dieses verwenden

### Python-Abhängigkeiten

Keine zusätzlichen Packages nötig – nutzt nur Python Standardlib!

## Schnellstart — Senden

```bash
# Einfache Text-E-Mail
python3 skills/email-sender/scripts/send_email_v2.py \
    --to empfaenger@example.com \
    --subject "Hallo" \
    --body "Das ist ein Test"

# HTML-E-Mail
python3 skills/email-sender/scripts/send_email_v2.py \
    --to freund@gmail.com \
    --subject "Schicke Nachricht" \
    --body "<h1>Hallo!</h1><p>Wie geht's?</p>" \
    --html

# Mit Anhängen
python3 skills/email-sender/scripts/send_email_v2.py \
    --to chef@firma.de \
    --subject "Bericht" \
    --body "Siehe Anhang" \
    --attach /tmp/report.pdf \
    --attach /tmp/chart.png

# Mit CC und BCC
python3 skills/email-sender/scripts/send_email_v2.py \
    --to chef@firma.de \
    --cc "assistent@firma.de, sekretaerin@firma.de" \
    --bcc "archiv@firma.de" \
    --subject "Bericht" \
    --body "Inhalt hier"
```

## Schnellstart — Lesen (IMAP)

```bash
# Ungelesene E-Mails
python3 skills/email-sender/scripts/imap_reader.py --unread

# Letzte 5 ungelesene E-Mails
python3 skills/email-sender/scripts/imap_reader.py --unread --limit 5

# Alle E-Mails der letzten 3 Tage
python3 skills/email-sender/scripts/imap_reader.py --all --since 3

# Nach Absender suchen
python3 skills/email-sender/scripts/imap_reader.py --from "amazon"

# Nach Betreff suchen
python3 skills/email-sender/scripts/imap_reader.py --subject "Bestellung"

# Als JSON ausgeben (für programmatische Verarbeitung)
python3 skills/email-sender/scripts/imap_reader.py --unread --json

# Vollständigen Body anzeigen
python3 skills/email-sender/scripts/imap_reader.py --unread --full

# Ordner auflisten
python3 skills/email-sender/scripts/imap_reader.py --folders

# Als gelesen markieren
python3 skills/email-sender/scripts/imap_reader.py --unread --mark-read
```

## Parameter — Senden (send_email_v2.py)

| Parameter | Kurzform | Beschreibung |
|-----------|----------|--------------|
| `--to` | `-t` | Empfänger E-Mail (erforderlich) |
| `--subject` | `-s` | Betreff |
| `--body` | `-b` | Nachrichtentext |
| `--body-file` | `-f` | Text aus Datei laden |
| `--provider` | `-p` | Anbieter: webde, gmail, gmx, custom (Default: webde) |
| `--from` | | Absender überschreiben |
| `--cc` | | CC Empfänger (kommagetrennt) |
| `--bcc` | | BCC Empfänger (kommagetrennt) |
| `--html` | | E-Mail als HTML senden |
| `--attach` | `-a` | Dateianhang (mehrfach verwendbar) |
| `--timeout` | | Timeout in Sekunden (Default: 30) |
| `--retries` | | Maximale Retry-Versuche (Default: 3) |
| `--verbose` | `-v` | Detaillierte Ausgabe |

## Parameter — Lesen (imap_reader.py)

| Parameter | Beschreibung |
|-----------|--------------|
| `--folders` | IMAP-Ordner auflisten |
| `--unread` | Nur ungelesene E-Mails |
| `--all` | Alle E-Mails (auch gelesene) |
| `--from` | Nach Absender filtern |
| `--subject` | Nach Betreff filtern |
| `--since` | Letzte N Tage (Default: 7) |
| `--folder` | IMAP-Ordner (Default: INBOX) |
| `--limit` | Maximale Anzahl E-Mails (Default: 10) |
| `--mark-read` | Als gelesen markieren |
| `--json` | Als JSON ausgeben |
| `--full` | Vollständigen Body anzeigen |
| `--provider` | E-Mail Provider (Default: webde) |
| `--verbose` | Detaillierte Ausgabe |

## Python API

### Senden

```python
from skills.email-sender.scripts.send_email_v2 import send_email_with_retry

# Einfach
send_email_with_retry(
    to="empfaenger@example.com",
    subject="Hallo",
    body="Das ist ein Test",
    provider="webde"
)

# Mit HTML und Anhängen
send_email_with_retry(
    to="chef@firma.de",
    cc=["assistent@firma.de"],
    subject="Bericht",
    body="<h1>Status</h1><p>Alles OK!</p>",
    html=True,
    attachments=["/tmp/report.pdf", "/tmp/chart.png"],
    provider="webde",
)
```

### Lesen

```python
from skills.email-sender.scripts.imap_reader import read_emails, summarize_emails

# Ungelesene E-Mails holen
emails = read_emails(
    provider="webde",
    folder="INBOX",
    unread_only=True,
    limit=5,
    search_subject="Rechnung",
)

# Zusammenfassung generieren
print(summarize_emails(emails, max_body_length=200))

# Als JSON
from skills.email-sender.scripts.imap_reader import emails_to_json
print(emails_to_json(emails))
```

## Fehlerbehebung

| Fehler | Lösung |
|--------|--------|
| "Authentication failed" | Passwort prüfen, für Gmail App-Passwort verwenden |
| "Connection refused" | Firewall/SMTP-Port prüfen (meist 587 oder 465) |
| "Recipient rejected" | Empfänger-Adresse auf Tippfehler prüfen |
| "SSL error" | Port auf 465 (SSL) oder 587 (STARTTLS) ändern |
| IMAP "Connection refused" | IMAP-Port prüfen (meist 993) |
| IMAP "Folder not found" | `--folders` aufrufen für verfügbare Ordner |
| Anhang "nicht gefunden" | Dateipfad prüfen (muss absolut sein) |

## Sicherheitshinweise

⚠️ **Wichtig:**
- `.env` Datei niemals committen (ist bereits in .gitignore)
- Keine E-Mail-Adressen oder Passwörter in Code/Chat schreiben
- Für Gmail immer App-Passwörter verwenden
- IMAP-Credentials sind dieselben wie SMTP (meistens)

## Changelog

### v3.0 (23.04.2026)
- ✅ **IMAP-Reader** — E-Mails lesen, suchen, zusammenfassen
- ✅ **Attachments** — Mehrere Dateianhänge beim Senden
- ✅ **JSON-Ausgabe** — Programmatische Verarbeitung
- ✅ **Thread-Verfolgung** — Message-ID/References-basiert
- ✅ **Ordner-Verwaltung** — Liste und Wechsel

### v2.0 (21.04.2026)
- ✅ Retry-Logik mit Exponential Backoff
- ✅ Timeout-Handling für SMTP-Verbindungen
- ✅ Professionelles Logging
- ✅ HTML-E-Mail Unterstützung
- ✅ CC und BCC Felder
- ✅ E-Mail-Validierung

### v1.0
- Initiale Version mit Basis-Funktionalität

---

*E-Mail-Senden UND -Lesen – der vollständige Butler-Service!* 📧🎩