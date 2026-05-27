---
name: lessons-update
description: Wspólna nauka — po każdym fix-phase / multi-file change / non-trivial task przejrzyj sesję i zdecyduj czy warto zapisać lekcję (nową lub update istniejącej). Triggeruj proaktywnie po PR-ach, fazach audytu, zamknięciu commit'u, każdej okazji gdy coś poszło nie tak / fix wprowadził nowy bug / wykryłem powtarzający się pattern. Skip dla trivial reads, pure refactors bez błędów, doc updates. ALWAYS-CONFIRM przed zapisem.
---

# Lessons Update — wspólny skill nauki

Cel: po każdym non-trivial task wyciągnąć to czego się nauczyliśmy i zachować jako persistent memory, żeby kolejne sesje nie powtarzały tych samych błędów. Memory ładuje się przez SessionStart hook (project-scoped), więc każda zapisana lekcja zwiększa baseline competence wszystkich przyszłych sesji.

## Kiedy uruchamiać

**Triggery proaktywne** (sam to wywołaj, nie czekaj):
- Po `gh pr merge` / commit zakończonym
- Po fazie audytu (Faza 1/3/4/5/...)
- Po multi-file change (≥3 pliki) lub multi-step task
- Po wykryciu fix-induced regression (najgorszy signal — fix wprowadził nowy bug)
- Po backtracking (musiałeś cofnąć decyzję)
- Po surprise (kod zachowywał się inaczej niż zakładałeś)

**Skip rules**:
- Trivial reads (sprawdzanie statusu, ls, grep do informacji)
- Pure refactors bez napotkania błędów
- Documentation updates
- Akcje które tylko klikają w UI / ustawiają flagi
- Powtarzanie znanego procesu bez nowych wniosków

**Jawny trigger od usera**: `/lessons-update` lub "zaktualizuj lessons" / "co się nauczyliśmy?".

## Workflow

### Krok 1: Recap

Streszcz w 1-3 zdaniach co właśnie zostało zrobione. To context dla decyzji "warto / nie warto".

### Krok 2: Reflection — 5 pytań

Przejdź po sesji i odpowiedz uczciwie. Każde "tak" = kandydat na lesson:

1. **Czy coś się nie udało lub zaskoczyło?** (TS error po commit, edge case który zignorowałem, fail w MCP call)
2. **Czy musiałem backtrack'ować lub fix'ować fix?** ⚠️ **Najwyższy signal** — fix-induced regressions.
3. **Czy coś założyłem co się okazało nieprawdą?** (np. "bonus_analyses jest w migracjach", "invokeEdge zwraca FunctionsHttpError shape")
4. **Czy widzę pattern który może się powtórzyć?** (np. "subagent zaraportował clean ale nie sprawdził callerów")
5. **Co bym chciał wiedzieć upfront następnym razem?**

### Krok 3: Detect duplicates

Dla każdego kandydata, **najpierw sprawdź czy już istnieje lesson** w `memory/`:

```bash
# Cwd guard — wykryj projekt
PROJ_MEM="$HOME/.claude/projects/$(pwd | sed 's|/|-|g' | sed 's|^-||')/memory"
# fallback: kto-ma-racje
[ -d "$PROJ_MEM" ] || PROJ_MEM="$HOME/.claude/projects/D--Projects-kto-ma-racje/memory"

# Search by keyword from candidate
grep -li "<keyword>" "$PROJ_MEM"/lesson_*.md
```

Jeśli istnieje pasująca lekcja:
- **Update path** (krok 5) — append nowy case do istniejącej
- NIE twórz duplikatu

Jeśli nie istnieje:
- **Create path** (krok 4) — nowa lekcja

### Krok 4: Create new lesson

**Filename convention**: `lesson_<short_topic>.md` (lub `feedback_*` jeśli to feedback procesowy, nie technical anti-pattern).

**Template**:

```markdown
---
name: <short title — pasuje do MEMORY.md one-linera>
description: <jednozdaniowy trigger phrase — keyword który mam zobaczyć w przyszłym kodzie>
type: lesson | feedback
---

**Reguła**: <jednozdaniowa zasada do zapamiętania>

**Why**:
<konkretny case z sesji — co się stało, dlaczego, jaki był koszt (wasted hours, regresja, security gap, RODO leak). MUSI być specyficzny: file:line, error message, exact symptom. Bez "uważaj na bugi".>

**How to apply**:
- <konkretny check do wykonania w przyszłości — bullet point>
- <grep / pattern / file path do sprawdzania>
- <link do related lesson jeśli pasuje>

**Occurrences**:
- <data> — <session ID jeśli masz, inaczej krótki opis>: <co się stało>
```

### Krok 5: Update existing lesson

Jeśli pattern się powtórzył, dopisz **nowy occurrence** do istniejącej lekcji:

```markdown
**Occurrences**:
- 2026-04-25 — original case: <opis>
- 2026-05-02 — <new case>: <co się stało, czemu pattern się powtórzył mimo lekcji>
```

Plus jeśli reflection ujawnia **nową fasetę patternu** której wcześniej nie było:
- Dopisz do **How to apply** nowy bullet
- Update **Reguła** jeśli się rozjeżdża (rzadko — większość patternów jest stała)

### Krok 6: ALWAYS-CONFIRM gate

**Zanim zapiszesz**, pokaż userowi:

```
Proponuję [nową lekcję | update lesson_X]:

═══════════════════════════════════
<draft content>
═══════════════════════════════════

Decyzja:
- ok / save → zapisuję
- skip / nie warto → pomijam
- change <co zmienić> → poprawiam
```

User decyduje. NIE zapisuj automatycznie.

### Krok 7: MEMORY.md index update (jeśli nowa lekcja)

Po zapisie nowej lekcji:
1. Read `MEMORY.md`
2. Dodaj one-liner w odpowiedniej sekcji (Lessons / Process / Project)
3. Format: `- [<title>](<file>.md) — <hook keyword + jednozdaniowa esencja>`
4. **Optymalizuj pod recognition** — keyword który mam zobaczyć w kodzie aby skojarzyć z lekcją

Limity: MEMORY.md ≤ 200 linii / ≤ 10KB. Jeśli przekracza, zaproponuj `/anthropic-skills:consolidate-memory`.

### Krok 8: Confirm save + close

Po zapisie potwierdź userowi:
```
✅ Saved: <path>
Index updated: <one-liner added/refreshed>
Active in next session via SessionStart hook (~/.claude/hooks/auto-load-lessons-kmr.sh).
```

## Heuristyki jakości lekcji

**DOBRA lekcja**:
- Specyficzna: file:line, error code, exact pattern
- Trigger-friendly: keyword w opisie który ja zobaczę w przyszłym kodzie
- Actionable: "How to apply" ma checks/greps/triggers, nie ogólne rady
- Bounded: jedna lekcja = jeden pattern (nie kombo 3 niezwiązanych)

**ZŁA lekcja** (nie zapisuj):
- "Uważaj na bugi" / "Pisz dobre testy"
- Restating dokumentacji frameworka (znajdę w docs)
- Trivia o jednym pliku które nie powtarza się (use comment in code, not memory)
- Duplikaty istniejących lekcji bez nowego signal

## Self-check przed wywołaniem

Zanim invoke'uję ten skill, zadaj sobie:
- Czy jest cokolwiek z 5 pytań reflection do zachowania? Jeśli **wszystkie nie** → skip skill, NIE wywołuj.
- Jeśli jest 1+ kandydat → invoke i przejdź workflow.

## Integracja z innymi skillami

- **`full-audit` v2**: na końcu każdej fazy audytu (Faza 1/3/4/5/...) explicit wskazuje "now invoke lessons-update". Dodaj sentence do report sekcji "PLAN NAPRAWY" w full-audit.
- **`anthropic-skills:consolidate-memory`**: gdy MEMORY.md > 200 linii, ten skill prosi o uruchomienie consolidate-memory zamiast dalej dorzucać.
- **`session-summary`**: na koniec sesji może wywołać lessons-update jako ostatni step.

## Auto-detect project

Hook ładuje lessons na podstawie cwd. Ten skill MUSI zapisywać do tego samego folderu memory:

```bash
# Detect project memory dir
CWD_LOWER=$(pwd | tr '[:upper:]' '[:lower:]')
case "$CWD_LOWER" in
  *kto-ma-racje*) PROJ_MEM="$HOME/.claude/projects/D--Projects-kto-ma-racje/memory" ;;
  *) PROJ_MEM="$HOME/.claude/projects/$(pwd | sed -e 's|^/c|C-|' -e 's|/|-|g' -e 's|^-||' -e 's|^C--|D--|')/memory" ;;
esac
```

Dla nowych projektów: jeśli memory dir nie istnieje, `mkdir -p` plus utworzenie pustego MEMORY.md indexu.

## Output do user (final summary)

Po skończonym workflow, podsumuj:
```
Lessons review:
- Reflected on N kandydatów
- Saved: M nowych / K updated existing
- Skipped: J (reasons listed)

MEMORY.md: <linecount> linii (limit 200), <KB>KB

Co poszło najlepiej w tej sesji: <jedna fraza>
Co najbardziej kosztowało: <jedna fraza>
```

To zamyka pętlę nauki — user widzi jakie lekcje wpadły do długoterminowej pamięci.
