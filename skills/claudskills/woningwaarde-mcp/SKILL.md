---
name: woningwaarde-mcp
description: Gebruik deze skill wanneer de gebruiker de huidige (geschatte) waarde van een woning wil berekenen op basis van aankoopprijs, aankoopjaar, aankoopkwartaal en provincie. Activeer ook wanneer gevraagd wordt naar waardeontwikkeling van een huis, hoeveel een woning nu waard is ten opzichte van de aankoop, of wanneer termen vallen als woningwaarde, waardestijging, WOZ-schatting, huizenprijsindex of vastgoedwaarde berekenen. Claude roept de Kadaster vastgoedcalculator API direct aan — geen MCP-tool nodig.
---

# Woningwaarde Skill

Schat de huidige waarde van een Nederlandse woning op basis van aankoopgegevens, via de **Kadaster Vastgoeddashboard API**. Geen API-sleutel nodig.

---

## API Endpoint

```
GET https://vastgoeddashboard.kadaster.nl/woningwaardecalculatorproxy/api/v1/propertyvalue/calculate
```

### Parameters

| Parameter | Type | Omschrijving |
|-----------|------|--------------|
| `province` | string | Provincienaam in **hoofdletters** (zie lijst hieronder) |
| `startquarter` | int | Aankoopkwartaal als kwartaalcode (zie formule) |
| `endquarter` | int | Huidig kwartaal als kwartaalcode (zie formule) |
| `startprice` | int | Aankoopprijs in euro's (heel getal) |

### Kwartaalcode formule

```
kwartaalcode = (jaar * 100) + kwartaal + 12
```

Voorbeelden:
- Q1 2020 → (2020 × 100) + 1 + 12 = **202013**
- Q3 2018 → (2018 × 100) + 3 + 12 = **201815**
- Q4 2023 → (2023 × 100) + 4 + 12 = **202316**

### Geldige provincienamen (altijd HOOFDLETTERS)

```
GRONINGEN, FRIESLAND, DRENTHE, OVERIJSSEL, FLEVOLAND,
GELDERLAND, UTRECHT, NOORD-HOLLAND, ZUID-HOLLAND,
ZEELAND, NOORD-BRABANT, LIMBURG
```

---

## URL opbouwen

De logica om de URL samen te stellen:

```python
from datetime import datetime

# Kwartaalcode: (jaar * 100) + kwartaal + 12
startquarter = (aankoopjaar * 100) + aankoopkwartaal + 12

now = datetime.now()
huidig_kwartaal = (now.month - 1) // 3 + 1
endquarter = (now.year * 100) + huidig_kwartaal + 12

url = (
    "https://vastgoeddashboard.kadaster.nl/woningwaardecalculatorproxy"
    "/api/v1/propertyvalue/calculate"
    f"?province={provincienaam.upper()}"
    f"&startquarter={startquarter}"
    f"&endquarter={endquarter}"
    f"&startprice={aankoopprijs}"
)
```

---

## Claude roept de URL direct aan

Gebruik `web_fetch` om de berekening uit te voeren. Bereken eerst de kwartaalcodes (zie formule hierboven), bouw de URL, en fetch het resultaat.

**Voorbeeld URL** (woning gekocht Q1 2020, €250.000, Gelderland, huidig kwartaal Q1 2026):
```
https://vastgoeddashboard.kadaster.nl/woningwaardecalculatorproxy/api/v1/propertyvalue/calculate?province=GELDERLAND&startquarter=202013&endquarter=202613&startprice=250000
```

---

## Verwacht response formaat

```json
{
  "success": true, 
  "message": "(Nog) geen prijsindex informatie beschikbaar voor het door u gekozen peilmoment. Er is gerekend met de prijsindex van het 4e kwartaal 2025.", 
  "priceChange": "125,7%", 
  "priceNew": "€ 789.845"
}
```

| Veld | Omschrijving |
|------|--------------|
| `estimatedValue` | Geschatte huidige waarde in € |
| `startPrice` | Ingevoerde aankoopprijs |
| `indexFactor` | Waardestijgingsfactor (bijv. 1.55 = +55%) |

---

## Resultaat presenteren

Presenteer de uitkomst altijd als:
- **Aankoopprijs**: €X
- **Geschatte huidige waarde**: €Y
- **Waardestijging**: Z% (op basis van Kadaster prijsindex voor [provincie])

Vermeld altijd dat het een **schatting** betreft op basis van de provinciale prijsindex — geen officiële WOZ-waarde.

---

## Tips & valkuilen

- `province` moet **altijd volledig in hoofdletters** — `GELDERLAND` werkt, `Gelderland` niet
- `endquarter` altijd **dynamisch** berekenen op basis van de huidige datum
- Aankoopprijs als **heel getal** in euro's (geen decimalen of scheidingstekens)
- Bij een onbekende provincie: vraag de gebruiker om de provincie te specificeren
