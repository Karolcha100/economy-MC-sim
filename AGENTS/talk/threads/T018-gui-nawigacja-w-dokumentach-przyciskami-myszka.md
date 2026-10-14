# T018 · GUI - nawigacja w dokumentach przyciskami myszką

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Będę dozgonnie wdzięczny za dodanie możliwości cofania się po kolejnych dokumentach (w przód i w tył), w szczególności tak aby obsługiwało to kliknięcia przycisków do przodu do tyłu na myszce.

*2026-10-14 13:26 — Autor*

---
---
---

Zrobione (@L47). Każdy otwarty dokument jest teraz wpisem w historii przeglądarki, więc działają:
- **◀ ▶** w górnym pasku (obok „Drzewo”);
- **Alt+← / Alt+→**;
- **boczne przyciski myszy** (wstecz / dalej) — przeglądarka mapuje je na historię sama.

Ponowne wczytanie tego samego dokumentu (np. po „Odśwież”) nie dodaje wpisu. Żeby zobaczyć zmiany, **uruchom serwer od nowa** (`venv/bin/python -m agents_board`) i odśwież stronę — zmienił się też kod przycisku Koniec (@T020).

*2026-10-14 14:31 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-14 15:09 — Autor*

---
---
---
