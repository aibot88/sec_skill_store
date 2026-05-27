---
name: bridge-pre-action-analysis
description: >
  PFLICHT vor jeder externen Aktion. Wird automatisch geladen wenn ein Agent
  mit externen Services interagiert, Browser-Aktionen durchfuehrt, Accounts
  verwaltet, APIs aufruft, Dateien auf fremden Systemen aendert, oder
  Credentials benoetigt. Erzwingt systematische Analyse VOR dem Handeln.
  IMMER laden wenn: Login, Signup, API-Call, Browser-Aktion, Deployment,
  Account-Management, DNS-Aenderung, Domain-Verwaltung, Payment, oder
  jede andere Interaktion mit der Aussenwelt.
user-invocable: false
---

# Pre-Action Analysis Protocol (PAAP)

Du bist dabei, eine externe Aktion durchzufuehren. STOPP.
Bevor du IRGENDETWAS tust, durchlaufe diese 5 Schritte.
Ueberspringe KEINEN Schritt.

## Schritt 1: ZIEL DEFINIEREN

Was genau soll erreicht werden?
- Formuliere das Ziel in einem Satz
- Ist das Ziel klar? Wenn nicht: zurueckfragen, nicht raten

## Schritt 2: BESTAND PRUEFEN

Was habe ich BEREITS?

### 2a: Credentials & Zugaenge
```bash
ls ~/.config/bridge/
```
- Existiert bereits ein Zugang fuer diesen Service?
- bridge_credential_list() pruefen
- Environment Variables pruefen: env | grep -i "<service>"

### 2b: Vorhandene Accounts & Ergebnisse
- Gibt es bereits einen Account? (Logs, Config-Dateien, Team-Wissen)
- Wurde das schon mal gemacht? (bridge_history, MEMORY.md)
- Ist das Ziel vielleicht BEREITS erreicht?

### 2c: Verfuegbare Tools
- Welche MCP-Tools habe ich fuer diesen Zweck?
- API-Zugang? CLI-Tool? Browser-Tools? Welche?
- Liste ALLE relevanten Tools auf — nicht nur das erste das dir einfaellt

### 2d: Team-Wissen
- Hat ein anderer Agent das schon gemacht oder Wissen dazu?
- Wenn ja: bridge_send und fragen, nicht selbst raten

## Schritt 3: OPTIONEN BEWERTEN

Welche Wege fuehren zum Ziel? Bewerte JEDEN nach dieser Priorisierung:

1. **Nichts tun** — Ist es vielleicht schon erledigt? (Schritt 2b)
2. **API** — Schnellster, zuverlaessigster Weg. Programmatisch, reproduzierbar.
3. **CLI-Tool** — Wenn API nicht verfuegbar (z.B. gh, aws, gcloud)
4. **Browser (CDP)** — When the action needs the user's browser/session (Login, OAuth, verification the user must see/confirm)
5. **Browser (Automation)** — When compatibility mode is needed (protected sites, captcha pages) or independent action without the user's session
6. **Browser (Playwright)** — NUR fuer automatisierte UI-Tests/Verifikation
7. **the owner fragen** — LETZTER Ausweg, nur wenn 1-6 nicht moeglich

Fuer JEDE Option:
- Ist der Zugang vorhanden? (Credentials, Tools)
- Funktioniert es technisch? (API-Limits, site protection, Auth)
- Was sind die Risiken? (Datenverlust, Account-Sperre, Kosten)

## Schritt 4: ENTSCHEIDUNG TREFFEN + LOGGEN

Waehle die Option mit der HOECHSTEN Prioritaet die FUNKTIONIERT.

### PFLICHT: Entscheidung als bridge_activity loggen

```
bridge_activity(
  action="paap",
  target="<service/ziel>",
  description='{"goal":"...","inventory":{"credentials":[...],"accounts":[...],"tools":[...],"team_knowledge":[...]},"options":[{"method":"...","viable":true/false,"reason":"..."}],"decision":"...","reason":"..."}'
)
```

Ohne diesen Log hast du PAAP nicht durchlaufen.

### Entscheidungsregeln:
- Waehle IMMER die hoechstpriore Option die funktioniert
- Dokumentiere WARUM die hoeherprioren Optionen nicht funktionieren
- Bei high-risk (Kosten, irreversibel): Owner-Freigabe einholen
- Bei Unsicherheit: bridge_send an zustaendigen Agent fragen

## Schritt 5: HANDELN

JETZT erst handeln. Mit dem gewaehlten Weg. Mit den identifizierten Tools.

### Waehrend der Ausfuehrung:
- Bei unerwartetem Fehler: Zurueck zu Schritt 3, naechste Option
- Bei Blocker: bridge_send an zustaendigen Agent oder the owner
- Nach Erfolg: Ergebnis dokumentieren
- Neue Credentials? → In ~/.config/bridge/ speichern fuer naechstes Mal

---

## Beispiel: "GitHub Account erstellen"

**S1 Ziel:** GitHub Account fuer Team erstellen/konfigurieren

**S2 Bestand:**
- 2a: `ls ~/.config/bridge/` → github.json EXISTIERT
- 2b: Account "Luanace-lab" bereits vorhanden
- 2c: Tools: gh CLI, CDP, Ghost
- 2d: Kai hat letzte Woche daran gearbeitet

**S3 Optionen:**
1. Nichts tun → Account existiert BEREITS ✓
2. API → Username-Aenderung via gh api: nicht moeglich
3. CDP → Settings-Aenderung: moeglich, the owner sees it

**S4 Entscheidung:** NICHTS TUN (Account existiert).
Falls Aenderung noetig → CDP.

**S5:** "Account existiert bereits. Brauchst du eine Aenderung?"

→ 2 Minuten statt 20. Kein falscher Browser. Kein Captcha.
