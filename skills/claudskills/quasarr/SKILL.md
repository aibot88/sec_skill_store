---
name: quasarr
description: Setup, configure, debug and extend Quasarr — the bridge that connects JDownloader with Radarr, Sonarr and LazyLibrarian via a fake Newznab indexer and SABnzbd client interface. Also handles CAPTCHA-protected link decryption. Use this skill whenever the user mentions Quasarr, asks about connecting JDownloader with Radarr/Sonarr, needs help with hostname configuration, FlareSolverr, download categories, notifications, SponsorsHelper, or any Quasarr-related topic.
---

# Quasarr Skill

**Repo:** https://github.com/rix1337/Quasarr  
**Zweck:** Quasarr täuscht Radarr/Sonarr/LazyLibrarian vor, ein Newznab-Indexer **und** ein SABnzbd-Client zu sein. In Wirklichkeit scrapt es deutsche Hoster-Seiten und schickt die gefundenen Links via MyJDownloader an JDownloader weiter.

---

## Architektur im Überblick

```
Radarr/Sonarr  ←→  Quasarr (Newznab + SABnzbd)  ←→  JDownloader (via MyJD API)
                        ↕
                   Scraper-Quellen (Hoster-Sites)
                        ↕
                   FlareSolverr (für Cloudflare-Sites)
```

Quasarr **kennt keine echten NZB- oder Torrent-Dateien**. Es ist komplett Hoster-basiert.

---

## Deployment (Docker — empfohlen für Unraid/BigServer)

```yaml
services:
  quasarr:
    container_name: 'Quasarr'
    image: 'ghcr.io/rix1337/quasarr:latest'
    ports:
      - '8080:8080'
    volumes:
      - '/mnt/user/appdata/quasarr/config:/config:rw'
    environment:
      - 'DOCKER=true'
      - 'INTERNAL_ADDRESS=http://192.168.1.144:8080'   # LAN-IP:Port → für Radarr/Sonarr
      - 'EXTERNAL_ADDRESS=https://quasarr.deine-domain.de'  # optional, für Web-UI
      - 'USER=admin'
      - 'PASS=sicheres-passwort'
      - 'AUTH=form'          # form | header | none
      - 'TZ=Europe/Berlin'

  # Optional: SponsorsHelper (nur für GitHub-Sponsoren)
  sponsorshelper:
    container_name: 'SponsorsHelper'
    image: 'ghcr.io/rix1337/sponsors-helper:latest'
    restart: unless-stopped
    depends_on:
      - quasarr
    volumes:
      - '/mnt/user/appdata/quasarr/sponsorshelper:/config'
    environment:
      - 'QUASARR_URL=http://192.168.1.144:8080'
      - 'QUASARR_API_KEY=<api-key-aus-quasarr-ui>'
      - 'FLARESOLVERR_URL=http://flaresolverr:8191/v1'
      - 'APIKEY_2CAPTCHA=<2captcha-key>'
      - 'TZ=Europe/Berlin'
```

**Wichtig:** `INTERNAL_ADDRESS` ist Pflicht bei Docker. Radarr/Sonarr müssen diese URL erreichen können.

### Pip-Installation (alternativ)
```bash
pip install quasarr
quasarr
```

---

## Ersteinrichtung (Reihenfolge)

1. **FlareSolverr** starten (für AL-Seite erforderlich): `http://host:8191/v1`
2. **JDownloader 2** starten & mit my.jdownloader.org verbinden
3. **Quasarr** starten → Web-UI öffnen
4. Im Web-UI:
   - **Hostnames** setzen (mindestens eine Quelle)
   - **FlareSolverr-URL** konfigurieren
   - **JDownloader-Zugangsdaten** eintragen & Gerät auswählen
5. **Radarr/Sonarr** konfigurieren (siehe unten)

---

## Radarr / Sonarr Konfiguration

Quasarr als **Newznab-Indexer** hinzufügen:
- URL: `http://<INTERNAL_ADDRESS>`
- API Key: aus dem Quasarr-Web-UI

Quasarr als **SABnzbd-Download-Client** hinzufügen:
- URL/Port: aus `INTERNAL_ADDRESS` (Host + Port)
- API Key: gleicher API Key

**Wichtig für Sonarr:** Alle Serien auf Serientyp **Standard** setzen. Anime/Absolut wird nicht unterstützt.

---

## LazyLibrarian Konfiguration

SABnzbd+ Downloader:
- URL/Port aus `INTERNAL_ADDRESS`
- API Key: gleicher Key
- Kategorie: `docs` (verhindert Konflikte mit Radarr/Sonarr)

Newznab Provider:
- URL + API Key wie oben
- Test & Speichern

Unter Importing → `Enable OpenLibrary api` aktivieren, `OpenLibrary` als primäre Quelle setzen.

---

## Quellen / Hostnames

Quasarr unterstützt diese Quellen-Kürzel:

| Kürzel | Login nötig | Besonderheit |
|--------|-------------|--------------|
| `al`   | ✅ Ja       | Braucht FlareSolverr (Cloudflare) |
| `at`   | ❌ Nein     | |
| `by`   | ❌ Nein     | |
| `dd`   | ✅ Ja       | |
| `dj`   | ✅ Ja       | Teilt Credentials mit `sj` (JUNKIES-Section) |
| `dl`   | ✅ Ja       | |
| `dt`   | ❌ Nein     | |
| `dw`   | ❌ Nein     | |
| `he`   | ❌ Nein     | |
| `hs`   | ❌ Nein     | |
| `mb`   | ❌ Nein     | |
| `nk`   | ❌ Nein     | |
| `nx`   | ✅ Ja       | |
| `rm`   | ❌ Nein     | |
| `sf`   | ❌ Nein     | |
| `sj`   | ✅ Ja       | Teilt Credentials mit `dj` (JUNKIES-Section) |
| `sl`   | ❌ Nein     | |
| `wd`   | ❌ Nein     | |
| `wx`   | ❌ Nein     | |

Hostnames als reinen Domain-Namen eintragen, z.B. `example.com` (kein `https://`).

**Hostname-Import via URL:** Im Hostnames-UI kann eine URL eingegeben werden, die eine INI-ähnliche Liste enthält (`kürzel = domain.tld`). Quasarr parsed und validiert diese automatisch.

---

## Konfiguration (intern)

Alle Einstellungen werden verschlüsselt gespeichert (AES-128-CBC) in `config.ini` + SQLite-DBs im `/config`-Verzeichnis.

Konfig-Sektionen:
- `API` → API-Key
- `JDownloader` → user, password, device
- `Settings` → hostnames_url
- `Hostnames` → ein Key pro Quelle
- `FlareSolverr` → url
- `Notifications` → discord_webhook, telegram_bot_token, telegram_chat_id
- `AL`, `DD`, `DL`, `NX`, `JUNKIES` → user + password pro Login-Quelle

---

## Download-Kategorien

Standard-Kategorien: `movies`, `shows`, `docs`  
Bis zu 10 eigene Kategorien hinzufügbar (nur Kleinbuchstaben + Zahlen, max. 20 Zeichen).

Jede Download-Kategorie kann bevorzugte **Mirrors** (Hoster) konfigurieren.

Radarr/Sonarr wählen die Kategorie beim Download automatisch. LazyLibrarian → Kategorie `docs` verwenden.

---

## Such-Kategorien (Newznab-Standard)

Quasarr meldet Radarr/Sonarr folgende Kategorien via `/api?t=caps`:
- Filme (2000)
- Serien / TV (5000 + Unterkategorien)
- Bücher (7000)
- Musik (3000)
- Anime (5070)
- Dokumentationen (5080)

Bis zu 10 benutzerdefinierte Such-Kategorien möglich (ID-Schema: `100000 + Basis-ID`).  
Jede Such-Kategorie kann auf bestimmte Quellen (Kürzel) beschränkt werden.

---

## CAPTCHA-Handling

Bestimmte Links sind CAPTCHA-geschützt (meist via Filecrypt, al.vc, hide.sx).

- Quasarr zeigt wartende Links im Web-UI unter `/captcha`
- **Manuell:** User klickt Link, löst CAPTCHA im Browser
- **Automatisch (SponsorsHelper):** Nur für GitHub-Sponsoren; kombiniert FlareSolverr + 2captcha API

Notifications werden bei neuem CAPTCHA-Bedarf verschickt (Discord/Telegram konfigurierbar).

---

## Benachrichtigungen

Zwei Provider: **Discord** (Webhook-URL) und **Telegram** (Bot-Token + Chat-ID).

Konfigurierbare Ereignisse:
- `unprotected` – neue ungeschützte Links
- `captcha` – CAPTCHA erforderlich
- `solved` – CAPTCHA gelöst
- `disabled` – SponsorsHelper deaktiviert
- `failed` – SponsorsHelper Fehler
- `quasarr_update` – neue Quasarr-Version verfügbar

Jedes Ereignis kann pro Provider aktiviert/deaktiviert und auf "silent" (ohne Ping) gesetzt werden.

---

## Quasarr Web-UI Routen

| Route | Beschreibung |
|-------|-------------|
| `/` | Dashboard (JD-Status, Hostnames, API-Key) |
| `/packages` | Aktive Download-Pakete |
| `/statistics` | Statistiken |
| `/hostnames` | Hostname-Verwaltung |
| `/categories` | Kategorie-Verwaltung |
| `/captcha` | CAPTCHA-Warteschlange |
| `/regenerate-api-key` | API-Key neu generieren |

---

## Quasarr interne API-Endpunkte

Alle Endpunkte erfordern API-Key als Query-Parameter oder Header.

```
# Newznab Indexer (für Radarr/Sonarr)
GET /api?t=caps                           → Indexer-Fähigkeiten
GET /api?t=movie&imdbid=tt1234567        → Film-Suche per IMDb-ID
GET /api?t=tvsearch&imdbid=tt1234567&season=1&ep=1  → Serien-Suche
GET /api?t=book&author=...&title=...     → Buch-Suche (LazyLibrarian)
GET /api?t=search&q=...                  → Freitext (LazyLibrarian/Lidarr)

# SABnzbd Client (für Radarr/Sonarr)
GET /api?mode=auth                        → Auth-Check
GET /api?mode=version                     → Version
GET /api?mode=get_cats                    → Kategorien-Liste
GET /api?mode=get_config                  → Konfiguration
GET /api?mode=queue                       → Download-Queue
GET /api?mode=history                     → Download-Verlauf
GET /api?mode=queue&name=delete&value=ID  → Paket löschen
POST /api                                 → Fake-NZB-Datei einreichen (Upload)
GET /api?mode=addurl&name=<encoded-url>   → URL als Download hinzufügen

# JDownloader-Konfiguration (Web-UI intern)
POST /api/jdownloader/verify              → Credentials prüfen
POST /api/jdownloader/save               → Credentials + Gerät speichern

# Hostnamen
POST /api/hostnames                       → Hostnamen speichern
POST /api/hostnames/import-url           → Hostnamen von URL importieren
POST /api/hostnames/check-credentials/<id>  → Login-Session prüfen

# Benachrichtigungen
POST /api/notifications/settings         → Einstellungen speichern
POST /api/notifications/test             → Test-Nachricht senden

# Timeouts
POST /api/timeouts/settings              → Slow-Mode konfigurieren

# Sonstiges
POST /api/restart                        → Quasarr neu starten
POST /api/flaresolverr                   → FlareSolverr-URL setzen
```

---

## Timeout / Slow-Mode

Quasarr hat für verschiedene Operationen konfigurierbare Timeouts.  
Im Slow-Mode werden Timeouts mit einem Multiplikator verlängert — für langsame Seiten sinnvoll, verlängert aber die Suche.

---

## Häufige Probleme & Lösungen

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Keine Suchergebnisse | Keine Hostnames gesetzt | Mindestens einen Hostname konfigurieren |
| AL-Seite funktioniert nicht | FlareSolverr fehlt oder falsch | FlareSolverr-URL prüfen (mit `/v1` am Ende) |
| JDownloader nicht verbunden | JD läuft nicht / nicht eingeloggt | JD starten, my.jdownloader.org Status prüfen |
| CAPTCHA-Links hängen | Manuelles Lösen nötig | `/captcha`-Route aufrufen und lösen |
| `INTERNAL_ADDRESS` falsch | Radarr/Sonarr kann Quasarr nicht erreichen | IP/Port prüfen, Firewall/Docker-Netzwerk checken |
| Sonarr findet keine Anime-Episoden | Serientyp falsch | Serientyp auf "Standard" setzen |
| Login-Fehler bei Quelle | Falsche Credentials oder Session abgelaufen | Im Hostnames-UI "Check & Save Session" |

---

## Eigene Hoster entwickeln

Quasarr erkennt neue Quellen **automatisch** per Plugin-Discovery. Es braucht zwei neue Python-Dateien:

```
quasarr/search/sources/<kürzel>.py      → Suche + Feed (AbstractSearchSource)
quasarr/downloads/sources/<kürzel>.py   → Link-Extraktion (AbstractDownloadSource)
```

Das Kürzel (`initials`) entspricht dem Dateinamen und erscheint automatisch im Hostnames-UI nach einem Neustart.

**Bei Login-Quellen zusätzlich:**
```
quasarr/providers/sessions/<kürzel>.py  → Session/Login-Provider
quasarr/storage/config.py              → "<KÜRZEL>" Section in _DEFAULT_CONFIG ergänzen
```

Vollständige Anleitung mit Templates: `references/custom_hoster_development.md`

---

## Referenz-Dateien

- `references/docker-compose-full.yml` — vollständiges Docker-Compose-Beispiel
- `references/custom_hoster_development.md` — Anleitung + Templates für eigene Hoster
