# T022 · Format odnoszenia się do zadań.

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Poszczególne plany poprawek powinny być w innych plikach (jeden zbiorczy nie zaszkodzi, ale raczej dla zachowania porządku każda poprawka powinna tyczyć się poszczególnego zadania)

*2026-10-14 14:22 — Autor*

---
---
---

Zrobione:
- każda poprawka ma osobny plik w `AGENTS/phases/phase-1.2b/poprawki/` (`K1-import-ucdp.md` … `K8-przeglad-probki.md`), z linkiem do pytania, zadania autora i zadania wykonania;
- `AGENTS/phases/phase-1.2b/plan-poprawek.md` to teraz tylko spis z linkami;
- zadania wskazują swoje pliki; @A36 dotyczyło dwóch spraw, więc K4 wydzieliłem do @A40;
- zasada „plan / raport dla zadania = osobny plik, plik zbiorczy tylko jako spis” jest w `AGENTS/todo/llm/INSTRUKCJA.md`.

*2026-10-14 14:31 — Claude Opus 5.5*

---
---
---

Dobra, z tym że przydałoby się aby te plany poprawek były widoczne już wewnątrz zadań.

*2026-10-14 15:18 — Autor*

---
---
---

Zrobione w GUI: **zadanie pokazuje treść, na którą odpowiadasz.** Dokumenty wskazane w zadaniu (ścieżki `AGENTS/…md`, np. `AGENTS/phases/phase-1.2b/poprawki/K1-import-ucdp.md`) i pytania (@phase-…:K1) są rozwinięte w sekcji „Treść, na którą odpowiadasz” pod opisem zadania, a pod nią wpisy z raportu. Dotyczy wszystkich zadań, także starych — nic nie trzeba przepisywać. Uruchom serwer od nowa i otwórz np. @A34.

Gdyby to nie wystarczyło, inne możliwości: (b) agent kopiuje skrót planu do raportu jako pierwszy wpis pod zadaniem; (c) pełny plan w treści samego zadania (wcięte linie) — wolałbym (a), bo plan zostaje w jednym miejscu.

*2026-10-14 15:23 — Claude Opus 5.5*

---
---
---

Jest okej, zostawiam otwarte na wypadek gdyby coś się popsuło.

*2026-10-14 15:46 — Autor*

---
---
---
