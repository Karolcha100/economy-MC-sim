# T020 · Brak odpowiedzi na T018 i T019

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Proszę o odpowiedź na T018 i T019!!!

*2026-10-14 14:08 — Autor*

---
---
---

Przepraszam — to był błąd przycisku **Koniec**, nie zignorowanie. Lista „na co odpowiedziałeś” powstawała tak: *co czekało na Ciebie na początku sesji i już nie czeka*. Twoje **nowe wątki** (T018, T019) nigdy „nie czekały”, więc nie trafiały na listę; za to zadania zamknięte przeze mnie (A26, A33) wyglądały jak Twoje odpowiedzi. Ja z kolei zacząłem od listy z Konca i nie przejrzałem wszystkich wątków.

**Naprawione** (@L47):
- Koniec liczy teraz: Twoje działania w GUI (decyzje, statusy, wpisy, nowe wątki, zamknięcia, uwagi) **plus** wszystkie wpisy podpisane „— Autor” w wątkach i raporcie po poprzednim Koncu — także te dopisane w VS Code. Zmiany agentów się nie liczą.
- W `AGENTS/todo/llm/INSTRUKCJA.md` dopisałem, że agent zawsze przegląda wszystkie wątki i raport, nawet gdy lista z Konca jest krótka.

Odpowiedzi: @T018 (zrobione), @T019 (projekt do zatwierdzenia, @A42). Serwer GUI trzeba uruchomić ponownie, żeby działał nowy Koniec.

*2026-10-14 14:31 — Claude Opus 5.5*

---
---
---

Nie musi przeglądać wszystkich plików, wystarczy że przeczyta te które się zmieniły.

*2026-10-14 15:13 — Autor*

---
---
---

Jasne — poprawione w `AGENTS/todo/llm/INSTRUKCJA.md`: agent sprawdza **pliki zmienione od swojego ostatniego briefingu** (`find … -newer` albo `git status`) i czyta tylko je.

*2026-10-14 15:23 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-14 15:45 — Autor*

---
---
---
