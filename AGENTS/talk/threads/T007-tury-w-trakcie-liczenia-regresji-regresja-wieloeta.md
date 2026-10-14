# T007 · Tury w trakcie liczenia regresji (regresja wieloetapowa)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Zastanawiam się nadtym aby w trakcie jednego kroku (1 rok) odbywało się coś w stylu regresji turowej/wieloetapowej.

Miałoby być to w celu umożliwienia rozprzestrzeniania się zjawisk typu kryzysy.

*2026-10-14 03:11 — Autor*

---
---
---

**Tury w obrębie roku — dobry pomysł, a do kryzysów wręcz potrzebny.** Opis techniczny i decyzja: @phase-2:U4.

Jak to rozumiem:
- **Rok = kilka tur** (np. 3, z pliku konfiguracyjnego).
  - Tura 1: każdy kraj zmienia się na podstawie własnych danych z poprzedniego roku.
  - Tury 2–3: kraj reaguje na to, co *w tej samej turze roku* stało się u sąsiadów i partnerów (granice, sojusze, `real power towards`).
  - Np. załamanie gospodarcze w Rosji w turze 1 obniża wzrost Kazachstanu i Białorusi w turze 2, a to z kolei dalej, w turze 3.
- **Zdarzenia też się rozlewają:** `riots` albo `in war crisis` w turze k zwiększa prawdopodobieństwo podobnych zdarzeń u sąsiadów w turze k+1.
- **Skąd siła rozlewania:** z historii. Model porównuje zmiany kraju ze zmianami jego sąsiadów i partnerów w tym samym roku (np. 2009 dla Europy). Taki model ekonomiści nazywają "przestrzennym".
- **Ograniczenie:** z danych rocznych nie da się rozróżnić, co było pierwsze w ciągu roku. Tury są więc uproszczeniem: pozwalają kryzysowi rozejść się w tym samym roku, ale ich liczba (K) to wybór, nie fakt z danych. Dlatego K jest w konfiguracji, a backtest pokaże, jaka wartość działa najlepiej.

*2026-10-14 03:24 — Claude Opus 5.5*

---
---
---

To znaczy, wystarczą tak naprawdę 2 tury oraz relacja "zależność ekonomiczna" myślę.

 np. w pierwszej turze oceniamy co się dzieje w moim państwie, a w drugiej patrzymy na państwa wokół i ich wpływ na moje.

Tak, też tak powinno być ze zdarzenia się rozlewają ale na podstawie regresji - a nie skryptu, analogicznie jak wyżej.

*2026-10-14 03:34 — Autor*

---
---
---

Przyjęte i wpisane do projektu (`AGENTS/phases/phase-2/design.md`, punkty 3–5):
- **2 tury**: wewnętrzna (moje państwo) → zewnętrzna (wpływ państw wokół);
- **nowa relacja `economic dependence`** (0–100, jak bardzo gospodarka FROM zależy od TO: handel, energia, finanse) — dodana do wzorów, na razie bez danych (do wypełnienia w 1.2b);
- **zdarzenia rozlewają się przez regresję zewnętrzną**, nie przez skrypt.

Szczegóły i jedno pytanie zwrotne w @T009.

*2026-10-14 04:11 — Claude Opus 5.5*

---
---
---

Okej, jeżeli to wszystko, to pozwalam tobie zamknąć ten wątek.

*2026-10-14 05:00 — Autor*

---
---
---

🔒 Wątek zamknięty — za zgodą autora ("pozwalam tobie zamknąć ten wątek"). Ustalenia są w `AGENTS/phases/phase-2/design.md` (punkty 3–5).

*2026-10-14 05:12 — Claude Opus 5.5*

---
---
---
