# T010 · Rozgałęzianie scenariuszy i zapis (U3, S1)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Rozpisanie @phase-2:U3, jak prosiłeś. Liczby dla horyzontu 4 lat, float32.

**Rozgałęzianie z przycinaniem (moja pierwsza propozycja):** z każdego scenariusza wychodzi `b` dzieci, potem losowo zostawiamy stałe N na kolejny rok. Odrzucam ją jednak, bo napisałeś, że liczba scenariuszy ma **rosnąć wykładniczo**, a scenariusze się nie przecinają. Zostaje czyste drzewo.

**Drzewo bez przycinania:** z każdego scenariusza `b` dzieci, więc rok 1: b, rok 2: b², …, rok 4: b⁴ scenariuszy.

| b (dzieci na rok) | węzły drzewa | scenariusze końcowe | rozmiar (relacje rzadkie) | rozmiar (relacje gęste) |
|---|---|---|---|---|
| 5 | 780 | 625 | 0,1 GB | 1,1 GB |
| **10** | **11 110** | **10 000** | **1 GB** | 15 GB |
| 20 | 168 420 | 160 000 | 15 GB | 235 GB |
| 100 | 101 mln | 100 mln | 9 TB | 141 TB |

- **b = 100 jest niewykonalne:** 9 TB danych i lata liczenia.
- **b = 10 daje dokładnie 10 000 scenariuszy końcowych**, czyli Twoje N z R3, z wykładniczym wzrostem po drodze.
- **Sprytny zapis** (Twoja uwaga o "pojedynczych liniach"):
  - zapisujemy **węzły drzewa**: dane jednego roku + numer rodzica;
  - "linię" scenariusza odtwarza się, idąc po rodzicach;
  - wspólne początki zapisują się raz, co daje ~3,6 razy mniej niż osobne linie (1 GB zamiast 3,6 GB przy b=10).

**Propozycja do konfiguracji:** `branching = [10, 10, 10, 10]`, osobno na każdy rok. Można np. `[20, 10, 5, 5]`: dużo różnorodności na starcie, mniej potem (20 → 200 → 1000 → 5000). Dłuższy horyzont tylko z mniejszym `b`.

**S1 (wynik = wszystkie scenariusze):** jeden przebieg zapisuje się do `simulator/scenarios/<scenariusz>/runs/<data-godzina>/`: dla każdego roku plik z węzłami i numerami rodziców + kopia konfiguracji. Narzędzia do analizy zbiorczej (prawdopodobieństwa, rozkłady w czasie) czytają ten katalog.

Zgoda na drzewo z `branching` na rok i domyślne `[10, 10, 10, 10]`? (@A24)

*2026-10-14 04:11 — Claude Opus 5.5*

---
---
---

Myślę że się zgadzam, ale warto tutaj dodać wpis do planów na przyszłość, że były różne pomysły które warto rozważyć.

*2026-10-14 05:10 — Autor*

---
---
---

Dziękuję. Przyjęte do projektu: drzewo, `branching` na każdy rok, domyślnie [10, 10, 10, 10] (`design.md`, punkt 6).

Pozostałe pomysły są zapisane w `AGENTS/plan/future-work.md` (punkt 4), z opisem, kiedy warto do nich wrócić:
- rozgałęzianie z przycinaniem do stałego N (filtr cząsteczkowy);
- N/10 i √N dzieci na scenariusz;
- klasyczne Monte Carlo (b = 1);
- zapis osobnych "linii" zamiast drzewa.

*2026-10-14 05:12 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-14 05:33 — Autor*

---
---
---
