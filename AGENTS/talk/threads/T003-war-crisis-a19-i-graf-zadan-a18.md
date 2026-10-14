# T003 · War crisis (A19) i graf zadań (A18)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

> *Skopiowane z archiwum `AGENTS/talk/wymiana-zdan-A1.md` (linia 375).*

# Re: O wartościach Startowych — wartości startowe zapisane, GUI poprawione, opinia o grafie

## odpowiedzi:

#### 2. War crisis

Użyjmy opcji (b) (1 do in war crisis, 2 do in war).

#### Graf 3D

Generalnie zgoda, na odwołania możesz ustawić oczywiście inny kolor krawędzi jeśli uznasz to za stosowne.

Zrobiłbym możliwość otwierania i chowania tego drzewa 2D.

*2026-10-14 02:08 — Autor*

---
---
---

Oba punkty zrobione.

**War crisis, opcja (b):**
- `in war` = tylko UCDP poziom 2 (klasyczne wojny między państwami): 52 par-lat, np. RUS–UKR 2022–2024, IRQ–KWT 1990–91;
- `in war crisis` = UCDP poziom 1 (strona wspierająca): 251 par-lat, np. **RUS–UKR 2014–2021**, ARM–AZE, NATO vs Serbia 1999;
- stare wartości `in war` wyczyściłem i przeliczyłem. Było to bezpieczne, bo pisały je tylko wartości startowe; narzędzie odmówi, gdyby były ręczne poprawki;
- przepisy są w `seeds.csv`.

**Graf (widok "Graf" w GUI):**
- drzewo 2D od lewej do prawej: Pytania i decyzje / Zadania autora / Zadania agentów / Wątki;
- **klik w grupę zwija/rozwija** (pamięta się po odświeżeniu), są też przyciski "Zwiń wszystko" / "Rozwiń wszystko";
- kolor węzła = status (pomarańczowy otwarte, zielony zrobione, niebieski w toku / agent odpowiedział, szary czeka);
- **czerwone krawędzie = odwołania**, wyciągane automatycznie z numerów w tekstach (np. A13 → L3, W4 → A15); po najechaniu widać numer. Krawędzie drzewa są szare, żeby czerwone było widać;
- klik w węzeł otwiera ten sam panel z tekstem i polem odpowiedzi.

*2026-10-14 02:20 — Claude Opus 5.5*

---
---
---

Dobra dziękuję, to wszystko w tym wątku.

*2026-10-14 02:30 — Autor*

---
---
---

🔒 Wątek zamknięty — autor: "to wszystko w tym wątku".

*2026-10-14 02:37 — Claude Opus 5.5*

---
---
---
