---
name: source-integration
description: Fires when the task adds a new data source or changes an existing one (xtb, gold, bond, manual, future: crypto/IKE). Use proactively when user mentions a source name or /source.
---

# Source integration

## Cel

Dostarczyć spójny kontrakt źródła: wejście, normalizacja, błędy, output — plus punkt integracji w `src/vesttracker/sources/` i zsynchronizowane `docs/sources.md`.

## Constraints

- warstwa pobierania nie miesza logiki domenowej z integracją źródła
- znane pułapki, ograniczenia jakości danych i zależności od API zapisuj jawnie w `docs/sources.md` — nie ukrywaj ich w kodzie
- `Faza 1` ogranicza scope do: `xtb`, `gold`, `bond`, `manual`
- nowe źródło = dokumentacja kontraktu w `docs/sources.md` + minimalny test, nie tylko kod
- idempotentność: ponowny import tego samego pliku nie duplikuje transakcji (`source_ref` jako unikalny klucz)

## Non-goals

- nie wprowadza frameworka plugin-system dla "dowolnego źródła"
- nie buduje retry/backoff na zapas jeśli źródło realnie tego nie wymaga
- nie zmienia schematu DB razem z integracją — to osobny change set

## Gotchas

- format CSV XTB nie jest jeszcze znany — czeka na przykładowy plik; nie wymyślaj nazw kolumn przed jego analizą
- cena złota wymaga dwóch API (Yahoo Finance `GC=F` + NBP `USD/PLN`) — oba mogą nie zwrócić danych dla weekendu lub święta; obsłuż fallback gracefully
- obligacje skarbowe nie mają tickera na Catalyst — wycena wyłącznie analityczna, nigdy nie szukaj ceny rynkowej
- `price_cache` ma unikalność `(symbol, date, source)` — przy zapisie używaj `INSERT OR REPLACE`