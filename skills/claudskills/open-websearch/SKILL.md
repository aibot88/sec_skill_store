---
description: 'Użyj tego skilla do wieloźródłowego researchu w sieci: wyszukiwania jednego lub wielu tematów, pobierania wielu stron przez fetchWebContent i zapisywania oczyszczonych plików Markdown do research_data/<folder-badania>/zrodla_i_analiza przed analizą.'
name: 'open-websearch'
argument-hint: 'Temat badawczy, lista zapytań lub polecenie zapisania wielu źródeł do research_data/<folder-badania>/zrodla_i_analiza'
---

<!-- user-language: pl -->

# Skill: Open-WebSearch MCP (Wyszukiwanie i Pobieranie Danych)

## Opis
To narzędzie zastępuje komercyjne silniki, wykorzystując wielosilnikowe serwery proxy (np. Bing, DuckDuckGo) w celu dostarczania wyników bez autoryzacji i API. Serwer integruje zarówno przeglądanie wyników wyszukiwania w formacie JSON, jak i ekstrakcję (scrapowanie) czytelnych treści z docelowych artykułów.

## Kiedy używać
- Gdy użytkownik podaje temat, a nie pojedynczy URL, i oczekuje zebrania wielu źródeł.
- Gdy trzeba wykonać kilka zapytań wyszukiwawczych dla jednego raportu.
- Gdy wynik `fetchWebContent` ma zostać zapisany lokalnie jako oczyszczone pliki `.md` w `research_data/<folder-badania>/zrodla_i_analiza/`.
- Gdy agent ma najpierw zbudować lokalną bazę źródeł, a dopiero potem przejść do analizy.

## Zasoby skilla
- [Skrypt kolekcjonujący wiele źródeł](./scripts/collect-web-research.mjs)
- [Workflow i przykłady użycia](./references/multi-source-workflow.md)

## Jak korzystać z funkcji
1. **Wyszukiwanie (Narzędzie `search`):**
   - Parametr `query`: Precyzyjne zapytanie.
   - Parametr `limit`: Liczba wyników (zalecane: do 5).
   - Parametr `engines`: Opcjonalna lista silników (np. `["duckduckgo", "bing"]`).

2. **Ekstrakcja treści (Narzędzia `fetch*`):**
   Po otrzymaniu wyników wyszukiwania, użyj dedykowanego narzędzia do pobrania treści:
   - `fetchLinuxDoArticle`: Dla artykułów z Linux.do.
   - `fetchCsdnArticle`: Dla artykułów z CSDN.
   - `fetchGithubReadme`: Dla plików README z GitHub.
   - `fetchJuejinArticle`: Dla artykułów z Juejin.
   - `fetchWebContent`: Dla dowolnych stron (wspiera Markdown).

## Dostępne narzędzia (Tools)
| Narzędzie | Opis |
| :--- | :--- |
| `search` | Wyszukiwanie w sieci. |
| `fetchLinuxDoArticle` | Pobiera artykuł z Linux.do. |
| `fetchCsdnArticle` | Pobiera artykuł z CSDN. |
| `fetchGithubReadme` | Pobiera README z GitHub. |
| `fetchJuejinArticle` | Pobiera artykuł z Juejin. |
| `fetchWebContent` | Pobiera treść dowolnej strony. |

## Procedura dla wielu zapytań
1. Zdefiniuj temat główny i 2-5 zapytań pomocniczych.
2. Uruchom [skrypt kolekcjonujący wiele źródeł](./scripts/collect-web-research.mjs), przekazując wiele flag `--query` lub plik z listą zapytań.
3. Skrypt powinien wykonać `search`, odfiltrować duplikaty URL, pobrać każdą stronę przez `fetchWebContent` i zapisać oczyszczone pliki `.md` do `research_data/<folder-badania>/zrodla_i_analiza/`.
4. Po zakończeniu przeczytaj plik indeksu źródeł `source-index.md` oraz właściwe pliki Markdown przed przystąpieniem do syntezy.
5. Jeśli skrypt zgłosi częściowe błędy pobierania, kontynuuj analizę na podstawie zapisanych źródeł i odnotuj braki.

## Przykładowe uruchomienia
```bash
node .github/skills/open-websearch/scripts/collect-web-research.mjs \
   --query "MicroPython ESP32" \
   --query "MicroPython ESP32 Wi-Fi" \
   --limit 3 \
   --output-dir research_data/micropython-esp32/zrodla_i_analiza
```

```bash
node .github/skills/open-websearch/scripts/collect-web-research.mjs \
   --queries-file research_data/queries.txt \
   --limit 2 \
   --engines duckduckgo,bing \
   --output-dir research_data/session-01/zrodla_i_analiza
```

## Najlepsze praktyki
- **Weryfikacja jakości wyników:** Opisy (snippets) z Open-WebSearch potrafią być krótkie. Nie odrzucaj z góry wyników o krótkim opisie, jeśli źródło (domena) jest powszechnie uznane za technicznie rzetelne (np. docs.python.org, github.com).
- **Zarządzanie kontekstem:** Zawsze zapisuj wynik ekstrakcji bezpośrednio do pliku w systemie lokalnym (`Filesystem MCP`) przed przystąpieniem do analizy kolejnego linku. Ograniczy to obciążenie Twojej wewnętrznej pamięci kontekstowej.
- **Odporność na błędy:** Open-WebSearch scrapuje dane na żywo. Jeżeli strona zablokuje bota (np. błąd 403 lub CAPTCHA przy ekstrakcji artykułu), przejdź płynnie do następnego wyniku z listy badawczej i odnotuj ten fakt w `Sequential Thinking`.
- **Dobór trybu pracy:** Dla pojedynczego, znanego URL można użyć `fetchWebContent` bezpośrednio. Dla researchu wieloźródłowego preferuj skrypt z tego skilla, bo zapisuje wiele stron i tworzy indeks źródeł.