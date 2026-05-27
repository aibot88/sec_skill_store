---
name: crypto-tracker
description: Krypto-Preis-Tracking für Bitcoin (BTC) und Ripple (XRP) via CoinGecko API. Zeigt aktuelle Kurse in USD/EUR mit 24h Änderungen.
---

# Crypto Tracker Skill

Überwacht Kryptowährungs-Kurse (BTC, XRP) in Echtzeit via kostenloser CoinGecko API.

## Features

- 💰 **Aktuelle Preise** in USD und EUR
- 📊 **24h Veränderung** in Prozent
- 🔄 **Kein API-Key nötig** - CoinGecko ist kostenlos
- 🤖 **Automatische Updates** möglich via Cron

## Schnellstart

### Aktuelle Preise anzeigen
```bash
python3 skills/crypto-tracker/scripts/crypto_tracker.py
```

### Spezifische Coins
```bash
python3 skills/crypto-tracker/scripts/crypto_tracker.py --coins bitcoin,ethereum
```

### Als JSON (für Automation)
```bash
python3 skills/crypto-tracker/scripts/crypto_tracker.py --json
```

## Unterstützte Coins

| Symbol | Name | ID für Script |
|--------|------|---------------|
| BTC | Bitcoin | `bitcoin` |
| XRP | Ripple | `ripple` |
| ETH | Ethereum | `ethereum` |
| SOL | Solana | `solana` |

## API

**CoinGecko** - Kostenlos, keine Authentifizierung nötig
- Rate Limit: 10-30 Calls/Minute (ohne API-Key)
- Dokumentation: https://www.coingecko.com/en/api

## In Python nutzen

```python
from skills.crypto_tracker.scripts.crypto_tracker import get_prices

prices = get_prices(['bitcoin', 'ripple'])
print(f"BTC: {prices['bitcoin']['eur']}€")
print(f"XRP: {prices['ripple']['usd']}$")
```

---
*Skill erstellt für Eure Lordschaft* 🎩
