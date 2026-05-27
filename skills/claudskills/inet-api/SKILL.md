---
name: inet-api
description: >-
  Internet.nl batch API voor het geautomatiseerd testen van meerdere
  domeinen op internetstandaarden. Authenticatie, batch requests,
  polling, resultaten JSON, dashboard-integratie.
  Triggers: internet.nl API, batch API, bulk scan, compliance dashboard,
  internet.nl batch, API credentials, geautomatiseerd testen,
  domeinenscan, monitoring dashboard
model: sonnet
allowed-tools:
  - Bash(gh api *)
  - Bash(curl -s *)
  - WebFetch(*)
metadata:
  created-with-ai: "true"
  created-with-model: claude-opus-4-20250514
  created-date: "2025-02-22"
  status: concept
---

> **CONCEPT — Let op:** Deze skill is geen officieel product van internet.nl. De beschrijvingen zijn informatieve samenvattingen — niet de officiële standaarden zelf. De testcriteria op [internet.nl](https://internet.nl) en de definities op [forumstandaardisatie.nl](https://www.forumstandaardisatie.nl/open-standaarden) zijn altijd leidend. Overheidsorganisaties die generatieve AI inzetten dienen te voldoen aan het [Overheidsbreed standpunt voor de inzet van generatieve AI](https://open.overheid.nl/documenten/bc03ce31-0cf1-4946-9c94-e934a62ebe73/file). Zie onze [verantwoording](https://github.com/developer-overheid-nl/skills-marketplace/blob/main/docs/verantwoording.md) en [DISCLAIMER.md](../../DISCLAIMER.md).

**Gebruik deze skill wanneer een gebruiker vraagt over de internet.nl batch API,
het geautomatiseerd scannen van meerdere domeinen, of het bouwen van een
compliance dashboard. Genereer werkende API-calls en scripts.**

## Overzicht

De [internet.nl batch API](https://github.com/internetstandards/Internet.nl-API-docs)
maakt het mogelijk om meerdere domeinen tegelijk te testen op internetstandaarden.
Dit is nuttig voor organisaties die veel domeinen beheren of een compliance-dashboard
willen bouwen.

## API-documentatie verkennen

```bash
# Bestanden in de API-docs repository
gh api repos/internetstandards/Internet.nl-API-docs/git/trees/main?recursive=1 \
  --jq '.tree[] | select(.type=="blob") | .path'

# README ophalen
gh api repos/internetstandards/Internet.nl-API-docs/contents/README.md \
  --jq '.content' | base64 -d
```

## Toegang verkrijgen

1. Ga naar [internet.nl](https://internet.nl) en registreer voor API-toegang
2. Je ontvangt een gebruikersnaam en wachtwoord voor de API
3. Authenticatie gaat via HTTP Basic Auth

**Let op:** De API is bedoeld voor legitiem gebruik. Respecteer rate limits
en de gebruiksvoorwaarden.

## API-workflow

De batch API werkt met een poll-model:

```
1. Dien batch in (POST)  ->  Ontvang request-ID
2. Poll status (GET)     ->  Wacht tot status "done"
3. Haal resultaten op    ->  JSON met scores per domein
```

## API-endpoints

| Actie | Methode | Endpoint |
|-------|---------|----------|
| Batch indienen (web of mail) | `POST` | `/api/batch/v2/requests` |
| Overzicht eigen requests | `GET` | `/api/batch/v2/requests` |
| Status opvragen | `GET` | `/api/batch/v2/requests/{request_id}` |
| Batch annuleren | `PATCH` | `/api/batch/v2/requests/{request_id}` |
| Resultaten ophalen | `GET` | `/api/batch/v2/requests/{request_id}/results` |
| Technische resultaten | `GET` | `/api/batch/v2/requests/{request_id}/results_technical` |
| Rapportage-metadata | `GET` | `/api/batch/v2/metadata/report` |

Base URL: `https://batch.internet.nl`

Het testtype (`"web"` of `"mail"`) wordt meegegeven in de request body, niet in het URL-pad.
Het `request_id` is een 32-karakter hexadecimale string.

## Batch indienen

### Webtest

```bash
curl -s -X POST https://batch.internet.nl/api/batch/v2/requests \
  -u "gebruiker:wachtwoord" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mijn webscan 2026-02",
    "type": "web",
    "domains": [
      "example.nl",
      "example2.nl",
      "example3.nl"
    ]
  }'
```

**Respons:**

```json
{
  "success": true,
  "data": {
    "request_id": "abcdef1234567890abcdef1234567890",
    "request_type": "web",
    "status": "registering"
  }
}
```

### Mailtest

```bash
curl -s -X POST https://batch.internet.nl/api/batch/v2/requests \
  -u "gebruiker:wachtwoord" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mijn mailscan 2026-02",
    "type": "mail",
    "domains": [
      "example.nl",
      "example2.nl"
    ]
  }'
```

## Status opvragen en resultaten ophalen

```bash
# Status opvragen
curl -s https://batch.internet.nl/api/batch/v2/requests/abcdef1234567890abcdef1234567890 \
  -u "gebruiker:wachtwoord"

# Resultaten ophalen (als status "done" is)
curl -s https://batch.internet.nl/api/batch/v2/requests/abcdef1234567890abcdef1234567890/results \
  -u "gebruiker:wachtwoord"
```

**Mogelijke statussen:**

| Status | Betekenis |
|--------|-----------|
| `registering` | Batch wordt geregistreerd |
| `running` | Tests worden uitgevoerd |
| `generating` | Resultaten worden gegenereerd |
| `done` | Resultaten beschikbaar |
| `error` | Er is een fout opgetreden |
| `cancelled` | Batch is geannuleerd |

## Poll-script (Bash)

```bash
#!/bin/bash
# poll_results.sh - Wacht op resultaten en download ze
API_URL="https://batch.internet.nl"
USER="gebruiker"
PASS="wachtwoord"
REQUEST_ID="$1"

if [ -z "$REQUEST_ID" ]; then
  echo "Gebruik: $0 <request-id>"
  exit 1
fi

echo "Wachten op resultaten voor $REQUEST_ID..."

while true; do
  STATUS_RESPONSE=$(curl -s "${API_URL}/api/batch/v2/requests/${REQUEST_ID}" \
    -u "${USER}:${PASS}")

  STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")

  echo "Status: $STATUS"

  if [ "$STATUS" = "done" ]; then
    curl -s "${API_URL}/api/batch/v2/requests/${REQUEST_ID}/results" \
      -u "${USER}:${PASS}" | python3 -m json.tool > "resultaten_${REQUEST_ID}.json"
    echo "Resultaten opgeslagen in resultaten_${REQUEST_ID}.json"
    break
  elif [ "$STATUS" = "error" ] || [ "$STATUS" = "cancelled" ]; then
    echo "Fout: batch heeft status $STATUS"
    echo "$STATUS_RESPONSE" | python3 -m json.tool
    exit 1
  fi

  sleep 30
done
```

## Python-voorbeeld

```python
"""Internet.nl batch API client."""

import time

import requests


def submit_batch(api_url: str, credentials: tuple, test_type: str, name: str, domains: list) -> str:
    """Dien een batch test in en retourneer het request-ID."""
    response = requests.post(
        f"{api_url}/api/batch/v2/requests",
        auth=credentials,
        json={"name": name, "type": test_type, "domains": domains},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"]["request_id"]


def poll_results(api_url: str, credentials: tuple, request_id: str, interval: int = 30) -> dict:
    """Poll tot resultaten beschikbaar zijn."""
    status_url = f"{api_url}/api/batch/v2/requests/{request_id}"
    results_url = f"{api_url}/api/batch/v2/requests/{request_id}/results"
    while True:
        response = requests.get(status_url, auth=credentials, timeout=30)
        response.raise_for_status()
        data = response.json()
        status = data["data"]["status"]
        print(f"Status: {status}")

        if status == "done":
            results = requests.get(results_url, auth=credentials, timeout=30)
            results.raise_for_status()
            return results.json()
        if status in ("error", "cancelled"):
            raise RuntimeError(f"Batch mislukt met status: {status}")

        time.sleep(interval)


def main():
    api_url = "https://batch.internet.nl"
    credentials = ("gebruiker", "wachtwoord")

    # Webtest indienen
    request_id = submit_batch(
        api_url=api_url,
        credentials=credentials,
        test_type="web",
        name="Scan februari 2026",
        domains=["example.nl", "example2.nl"],
    )
    print(f"Batch ingediend: {request_id}")

    # Wachten op resultaten
    results = poll_results(api_url, credentials, request_id)

    # Resultaten verwerken
    for domain, result in results["data"]["domains"].items():
        score = result.get("scoring", {}).get("percentage", "?")
        print(f"{domain}: {score}%")


if __name__ == "__main__":
    main()
```

## Resultaten interpreteren

De resultaten bevatten per domein een gedetailleerd JSON-object met scores
per categorie en individuele tests.

### Scorestructuur

```json
{
  "data": {
    "status": "done",
    "domains": {
      "example.nl": {
        "status": "ok",
        "scoring": {
          "percentage": 87
        },
        "results": {
          "categories": {
            "ipv6": {
              "verdict": "passed",
              "tests": {}
            },
            "dnssec": {
              "verdict": "passed",
              "tests": {}
            },
            "tls": {
              "verdict": "warning",
              "tests": {}
            },
            "appsecpriv": {
              "verdict": "failed",
              "tests": {}
            }
          }
        },
        "report": {
          "url": "https://internet.nl/site/example.nl/12345/"
        }
      }
    }
  }
}
```

### Verdicts

| Verdict | Betekenis |
|---------|-----------|
| `passed` | Voldoet aan de standaard |
| `warning` | Gedeeltelijk voldaan, verbetering mogelijk |
| `failed` | Voldoet niet aan de standaard |
| `info` | Informatief, geen score-impact |
| `not_tested` | Test niet uitgevoerd |

### Categorieen (webtest)

| Categorie | Standaarden |
|-----------|-------------|
| `ipv6` | IPv6-bereikbaarheid (AAAA, nameservers) |
| `dnssec` | DNSSEC-validatie |
| `tls` | TLS-versie, cipher suites, HSTS, certificaat |
| `appsecpriv` | Security headers, security.txt |
| `rpki` | RPKI Route Origin Validation |

### Categorieen (mailtest)

| Categorie | Standaarden |
|-----------|-------------|
| `ipv6` | IPv6 op MX-servers |
| `dnssec` | DNSSEC op maildomein en MX |
| `auth` | SPF, DKIM, DMARC |
| `tls` | STARTTLS, DANE, certificaat |
| `rpki` | RPKI Route Origin Validation |

## Dashboard-integratie

### CSV-export genereren

```python
"""Genereer CSV van batch-resultaten."""

import csv
import json
import sys


def results_to_csv(results: dict, output_file: str) -> None:
    """Schrijf resultaten naar CSV."""
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Domein", "Score", "IPv6", "DNSSEC", "TLS", "Security", "Rapport"])

        for domain, data in results["data"]["domains"].items():
            cats = data.get("results", {}).get("categories", {})
            writer.writerow([
                domain,
                data.get("scoring", {}).get("percentage", ""),
                cats.get("ipv6", {}).get("verdict", ""),
                cats.get("dnssec", {}).get("verdict", ""),
                cats.get("tls", {}).get("verdict", ""),
                cats.get("appsecpriv", {}).get("verdict", ""),
                data.get("report", {}).get("url", ""),
            ])


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        results = json.load(f)
    results_to_csv(results, "rapport.csv")
    print("CSV geschreven naar rapport.csv")
```

### Periodieke monitoring

Combineer de batch API met een cron-job of CI/CD pipeline om domeinen
regelmatig te scannen en trends bij te houden.

## Repositories

| Repository | Beschrijving | Licentie |
|-----------|-------------|--------|
| [Internet.nl-API-docs](https://github.com/internetstandards/Internet.nl-API-docs) | Officieel API-documentatie | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |
| [Internet.nl](https://github.com/internetstandards/Internet.nl) | Testsuite broncode | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) (code), [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) (vertalingen) |

## Veelvoorkomende problemen

| Probleem | Oorzaak | Oplossing |
|----------|---------|-----------|
| HTTP 401 | Ongeldige credentials | Controleer gebruikersnaam en wachtwoord |
| HTTP 429 | Rate limit bereikt | Wacht en probeer later opnieuw |
| Status `error` | Ongeldige domeinen of serverfout | Controleer de domeinnamen in de batch |
| Lege resultaten | Test nog niet afgerond | Verhoog het poll-interval, controleer status |
| Timeout bij grote batch | Te veel domeinen tegelijk | Splits in kleinere batches (max 5.000 per batch) |

## Achtergrondinfo

Zie [reference.md](./reference.md) voor gedetailleerde API-response schema's,
rate limits en foutcodes.

