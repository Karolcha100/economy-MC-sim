# T011 · Co znaczy "uzupełnione" dla relacji (P1)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Wyjaśnienie @phase-1.2b:P1 prościej, na przykładzie.

**Problem w liczbach:** relacja skierowana to wartość dla każdej pary państw w każdym roku: 196 × 195 par × 36 lat ≈ 1,3 mln liczb **na jedną relację**. Relacji jest 11, więc razem **~12 mln liczb**. Żaden agent ich nie wypełni po kolei.

**Ale większość z nich to "nic":** jak Boliwia widzi Mongolię (`social view towards`)? Jaka jest `economic dependence` Islandii od Laosu? Prawdziwa odpowiedź to **0 (brak relacji)**, czyli dokładnie wartość domyślna, którą wzory już mają.

**Co chcę wprowadzić (zmiany):**
1. **Agent dla każdego państwa wybiera istotnych partnerów** (sąsiedzi, mocarstwa, sojusznicy, wrogowie, partnerzy handlowi), zwykle 10–40, i **tylko dla nich wpisuje liczby**. Np. dla Polski: Niemcy, Rosja, Ukraina, USA, Białoruś, Litwa, Czechy…
2. **Dla pozostałych par jedną komendą potwierdza, że wartość domyślna (0) jest prawidłowa.** Nowa komenda `confirm-default` zapisuje w changelogu np. "POL → wszyscy poza listą: domyślne potwierdzone przez agenta X". Plików z milionami zer nie tworzymy.
3. `missing` (raport postępu) traktuje potwierdzone domyślne jako **uzupełnione**. Dzięki temu "100% uzupełnione" ma sens.

**Co to zmienia dla silnika (2.1):** nic. Silnik i tak bierze wartość domyślną tam, gdzie nie ma wpisu, więc wyniki są takie same, jakby agent wpisał 0. Zmienia się tylko to, że wiemy, że **ktoś to sprawdził**, a nie że pole jest puste przez zapomnienie.

**Dla statystyk kraju** (`stability` itd.) bez zmian: tu wypełniamy wszystko, bo każde państwo ma np. jakąś stabilność.

Czy tak może być? Jeśli tak, odpowiedz w @phase-1.2b:P1 albo tutaj.

*2026-10-14 05:38 — Claude Opus 5.5*

---
---
---

Tak, może tak być.

*2026-10-14 05:43 — Autor*

---
---
---

Dziękuję. Zapisane w `AGENTS/phases/phase-1.2b/plan.md`. Komenda `confirm-default` i raport postępu powstaną przed startem wypełniania (@L29).

*2026-10-14 06:03 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-14 06:05 — Autor*

---
---
---
