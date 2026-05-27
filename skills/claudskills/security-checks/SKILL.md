---
name: security-checks
description: "Przegląd bezpieczeństwa zmian w kodzie i konfiguracji."
user-invocable: true
argument-hint: "[pliki / fragmenty do sprawdzenia]"
---

## Zakres

- frontend (XSS, niebezpieczne użycie HTML, brak sanitizacji),
- backend/API (walidacja danych, uprawnienia, wycieki sekretów),
- konfiguracja (nagłówki bezpieczeństwa, użycie zmiennych środowiskowych).

## Procedura

1. Zidentyfikuj newralgiczne miejsca:
   - generowanie HTML z danych użytkownika,
   - operacje na danych wrażliwych (logowanie, płatności, dane osobowe),
   - użycie sekretów i kluczy API.
2. Sprawdź:
   - czy dane wejściowe są walidowane,
   - czy dane są odpowiednio kodowane przed wstrzyknięciem do HTML,
   - czy logi nie zawierają danych wrażliwych,
   - czy używane są bezpieczne domyślne konfiguracje (CSP, cookies, sesje).
3. Wypisz znalezione problemy i rekomendacje poprawy.

## Format odpowiedzi

- „Podsumowanie bezpieczeństwa” – krótki opis ogólnego poziomu ryzyka.
- Lista problemów z priorytetem (`high`, `medium`, `low`) oraz proponowanymi poprawkami.
