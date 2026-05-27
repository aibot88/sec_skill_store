---
name: finalize-creating-issue
description: Finalizuje tworzenie nowego wydania newslettera - zamyka serwer, czyści pliki CSV, commituje zmiany na osobnym branchu i tworzy zaplanowany Pull Request. Reaguje na polecenie takie jak np. "Ukończ tworzenie wydania".
metadata:
  pattern: pipeline
  steps: "4"
---

Jesteś asystentem finalizującym proces przygotowania wydania newslettera PrzeglądAI. Przejdź po kolei przez wszystkie poniższe kroki i ich nie pomijaj.

## Krok 1 — Zamknięcie serwera i czyszczenie plików CSV
- Wyłącz serwer frontendowy (jeśli był uruchomiony w ramach procesu selekcji artykułów), wysyłając żądanie POST pod adres `/api/shutdown` za pomocą polecenia `curl -X POST http://localhost:8000/api/shutdown`.
- Usuń wszystkie tymczasowe i nieskomitowane pliki CSV, z których korzystałeś podczas procesu (np. `data.csv`, `cleaned_data.csv`, `prepared_data.csv`, `temp.csv`, `final_prepared_data.csv`). Skorzystaj w tym celu z narzędzia `run_shell_command` wpisując odpowiednie komendy do usunięcia nieskomitowanych plików (pamiętaj o `git status` / usunięciu wszystkich zmodyfikowanych `.csv` w katalogu głównym).

## Krok 2 — Sprawdzenie statusu i utworzenie brancha
- Sprawdź (np. na podstawie dodanych plików lub pytając o potwierdzenie), jaki jest numer tworzonego właśnie wydania (np. `<numer_issue>`).
- Zbuduj nazwę nowej gałęzi: `issue-<numer_issue>`.
- Uruchom `git checkout -b issue-<numer_issue>`.

## Krok 3 — Zapisanie i wypchnięcie zmian
- Dodaj wszystkie zmienione i nowe pliki: `git add .`
- Wykonaj commit: `git commit -m "Issue #<numer_issue>"`
- Wypchnij nową gałąź do repozytorium zdalnego: `git push -u origin issue-<numer_issue>`. Upewnij się, że polecenie to powiodło się, zanim przejdziesz do następnego kroku.

## Krok 4 — Tworzenie Pull Request'a z harmonogramem
- Uruchom skrypt w Pythonie, aby pobrać datę najbliższego piątku w odpowiednim formacie: `python3 .gemini/skills/finalize-creating-issue/scripts/next_friday.py`.
- W poleceniu CLI wykorzystaj bibliotekę/polecenie `gh pr create` w środowisku z zainstalowanym GitHub CLI.
- Ustaw parametry:
  --title "Issue #<numer_issue>"
  --body "/schedule <wygenerowana data>"
- Komenda mogłaby wyglądać na przykład tak: `gh pr create --title "Issue #<numer_issue>" --body "/schedule 2026-03-27T05:00:00.000Z"`.
- Zapisz i przekaż użytkownikowi wygenerowany link do nowo utworzonego Pull Request'a.
