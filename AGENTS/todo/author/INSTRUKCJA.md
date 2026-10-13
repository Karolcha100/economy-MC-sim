# Instrukcja TODOs — dla autora

*Ten plik możesz dowolnie edytować. Agenci go czytają, ale nie zmieniają. Wersja początkowa: 2026-10-14 00:20 — Claude Opus 5.5*

---

## Pliki

| Plik | Co tam jest | Kto pisze |
|---|---|---|
| `WAZNE-TODO-dla-autora.md` | zadania, które blokują agentów | agenci dodają, Ty odhaczasz |
| `SREDNIE-TODO-dla-autora.md` | ważne, ale nie blokują | j.w. |
| `MALE-TODO-dla-autora.md` | drobiazgi | j.w. |
| `raport-TODO-autora.md` | Twoje odpowiedzi i raporty do zadań `A…` + odpowiedzi LLM | Ty; agenci dopisują oznaczone bloki |

Zadania dla agentów są w `AGENTS/todo/llm/` (tam piszą agenci; Ty możesz je czytać i komentować w swoim raporcie).

## Numeracja

- Twoje zadania: **A1, A2, A3…**, jedna numeracja dla wszystkich trzech plików.
- Numer nie zmienia się, gdy zadanie przechodzi do innego priorytetu, i nigdy nie jest używany ponownie.
- Zadania agentów mają osobną numerację: **L1, L2…**.

## Statusy (litera w nawiasie)

| Zapis | Znaczenie |
|---|---|
| `[ ]` | do zrobienia |
| `[~]` | w toku |
| `[x]` | zrobione |
| `[?]` | czeka na odpowiedź / zablokowane (dopisz na co) |
| `[>]` | przeniesione do innego pliku (dopisz dokąd, np. `[>] → MALE`) |
| `[-]` | porzucone (dopisz krótko dlaczego) |

Zadań **nie usuwamy**, tylko zmieniamy literę.

## Jak odpowiadać

1. W `raport-TODO-autora.md` dodaj wpis:
   ```
   ### [A7] tytuł zadania

   treść…

   ---
   ```
2. Zmień status zadania w pliku WAŻNE / ŚREDNIE / MAŁE.
3. Agent przy następnej sesji przeczyta wpis i odpowie pod nim blokiem oznaczonym "🤖 ODPOWIEDŹ LLM — początek / koniec", z datą, godziną i podpisem.

## Gdzie jeszcze piszemy

- `AGENTS/talk/wymiana-zdan-A1.md`: dłuższa rozmowa (wpisy oddzielone `---` ×3, każdy zaczyna się od `# tytuł`).
- `AGENTS/talk/od-autora-dla-llmow.md`: Twoje ogólne uwagi; agent tylko oznacza je jako przeczytane.
- `AGENTS/phases/phase-*/agents-issues-N.md`: pytania agentów z polami **Decyzja**.
- `AGENTS/plan/phases-plans.md`: aktualna kolejność faz.
