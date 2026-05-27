---
name: codex-flow-project-wrap-up
description: >
  Użyj, gdy kończysz sesję pracy nad projektem i chcesz uporządkować stan
  dokumentacji operacyjnej bez implementacji nowych zmian: zaktualizować
  ROADMAP.md, STATUS.md oraz w razie potrzeby README.md, a następnie upewnić
  się, że bieżący stan jest zapisany w repo. Ten skill nie służy do wdrażania
  funkcji ani do tworzenia nowego planu.
---

Zrób porządek w projekcie.

Przebieg pracy:
1. Zaktualizuj `ROADMAP.md`:
   - statusy milestone'ów zgodnie z rzeczywistością
2. Zaktualizuj `STATUS.md`:
   - aktualny stan projektu
   - istotne ograniczenia
   - najbliższy sensowny następny krok, jeśli wynika z obecnego stanu
3. Sprawdź `README.md` i zaktualizuj go tylko wtedy, gdy ostatnie zmiany wpływają na informacje istotne dla człowieka:
   - sposób uruchamiania
   - wymagania
   - komendy developerskie
   - opis działania funkcji
   - ograniczenia lub ważne zachowania systemu
4. Upewnij się, że stan repo jest zapisany:
   - jeśli są niezapisane zmiany dokumentacyjne wynikające z wrap-up, przygotuj commit
   - jeśli nie ma zmian, nie twórz pustych commitów

Zasady:
- nie zmieniaj kodu
- nie aktualizuj `README.md` kosmetycznie ani bez realnej potrzeby
- dokumentacja ma odzwierciedlać faktyczny stan repo
- jeśli potrzebujesz doprecyzowania zasad wrap-up albo README, użyj plików z `references/`
- jeśli potrzebujesz technicznie sprawdzić stan repo, użyj skryptów z `scripts/`

Wynik:
- podsumuj, które dokumenty zostały zaktualizowane
- zaznacz, czy powstał commit dokumentacyjny
- jeśli nic nie wymagało zmian, napisz to wprost
