Odpowiedzi Autora do TODOs.

(dla modelu LLM: Pamiętaj aby dodać numeracje mi tych TODOs, żebym mógł tutaj się do nich odnosić - Dzięki!)

Model LLM powinien składać podpis z datą i godziną przeczytania. 

Odpowiedzi proszę dawać Analogicznie jak moje wpisy (z tym że oznaczone od góry i dołu że LLM odpowiedział) w tym pliku, jeżeli jakiś TODO jest przezemnie zostawiony/przerzucany jako mniej/bardziej ważny/wykonany, nie usuwamy gom tylko wpisujemy inną literkę (x - wykonany np.)

Generalnie w sumie to napisz instrukcje do korzystania z TODOs (może być oddzielna dla agentów i dla mnie - zastrzegam że swoją mogę edytować).

---
---
---

### [A2] Pobrać Dane Korei Północnej z ONZ

Nie działa mi ta strona, ładuje sie w nieskonczoność.

Masz tutaj jakąś znalazłem: `https://www.worldometers.info/pl/pkb/korea-polnocna-pkb/`.

Generalnie pozwalam poszukać tobie w internecie tego, jeśli nie znajdziesz, to daj mi znać w odpowiednim TODO.

---

### [A3] Czy Agenci mają korzystać w wyszukiwarki

Tak, dokładnie, mają korzystać w wyszukiwarki - potwierdzam.

---

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A2] Re: Pobrać Dane Korei Północnej z ONZ — zrobione
>
> - Serwer ONZ (unstats.un.org) nadal ucina plik; wznawianie pobierania też nie działa.
> - Użyłem Twojego tropu: worldometers.info (wersja angielska), tabela "GDP Nominal (Current USD)" 1970–2023. Strona podaje jako źródło **United Nations Statistics Division, National Accounts**, więc to te same dane ONZ, tylko z drugiej ręki.
> - Surowe dane: `data/worldometers/prk-gdp-current-usd.csv` (+ `README.md` z opisem pochodzenia).
> - Korea Północna w `history/gdp-current-usd.csv`: lata 1990–2023 z tego źródła, 2024–2025 ekstrapolacją. Wszystko jest zapisane w `history/fill-log.csv`. W PKB nie ma już żadnych luk.
> - Raport po stronie LLM: `TODOs-LLM/raport-TODO-LLM.md`, L6.
>
> ### [A3] Re: Czy Agenci mają korzystać z wyszukiwarki — przyjęte
>
> - Zapisane w instrukcji dla agentów (`TODOs-LLM/INSTRUKCJA.md`) i w zadaniu L8 (zasady korzystania ze źródeł prasowych).
>
> *przeczytane i odpowiedziane: 2026-10-14 00:20 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A16] Wypróbować GUI

Działa bardzo dobrze, poza tym że ikonki Twoje Zadania (otwarte) się nie wyświetlają. Tzn. są puste kwadraty.

*2026-10-14 01:43 — Autor*

---

### [A15] Dwa pytania zwrotne do Phase 1.2a

Oznaczam jako "W toku" bo może coś jeszcze dodasz od siebie, odpowiedziałem w Wymianie Zdań.

*2026-10-14 01:44 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A16] Re: Wypróbować GUI — dzięki, poprawione
>
> - Puste kwadraty to była ikona ☐ dla zadań "do zrobienia". Wyglądała jak brakujący znak, więc teraz są kolorowe znaczki: 🟠 do zrobienia, 🔵 w toku, ✅ zrobione, ⏸️ czeka, ➡️ przeniesione, ❌ porzucone.
> - Przy okazji (Twoja prośba z wymiany zdań): edytor działa jak w VS Code — Tab / Shift+Tab, Enter kontynuuje listę, Ctrl+Enter wysyła. Sprawdzone w prawdziwym Firefoksie.
>
> ### [A15] Re: Dwa pytania zwrotne — wdrożone
>
> - Wszystko z Twojej odpowiedzi jest w danych:
>   - Y2 → wartości startowe zapisane;
>   - `net migration` dodane;
>   - `in war crisis` dodane;
>   - danych o wojnie hybrydowej nie pobieram.
> - Jedno pytanie uzupełniające o `in war crisis` → **A19**. Z mojej strony A15 można zamknąć.
>
> *przeczytane i odpowiedziane: 2026-10-14 02:10 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A21] Szum w Monte Carlo

Odpowiedziałem, podałeś dobrą propozycję

*2026-10-14 03:37 — Autor*

---

### [A22] Kolejność: 1.2b przed 2.1?

Tak, zgadzam się.

*2026-10-14 03:38 — Autor*

---

### [A20] Odpowiedzieć na AGENTS/phases/phase-2/agents-issues-1.md

Chyba odpowiedziałem, zamknij jeśli jest okej.

*2026-10-14 04:08 — Autor*

---

### [A26] Plan Phase 1.2b

Generalnie jeszcze nadtym pracujemy

*2026-10-14 05:24 — Autor*

---

### [A25] Zatwierdzić projekt silnika

w podanym pliku jest:

`Model podaje prawdopodobieństwa i rozkłady, nie pewność. Sprawdzamy więc kalibrację: czy zdarzenia z prognozą 20% zachodzą w ~20% przypadków [...]` - tego nie da się sprawdzić mając tylko faktyczne dane. Generalnie można sprawdzać przede wszystkim `czy prawdziwe wartości mieszczą się w rozkładach`.

Oraz (wyżej):

Zapis jako drzewo: węzeł = dane jednego roku + numer rodzica. Pojedynczą "linię" scenariusza odtwarza się, idąc po rodzicach. Wspólne początki nie są powielane.

Wystarczy chyba zapisywać tylko poszczególne scenariusze z informacją jaki jest ich rodzic.

*2026-10-14 05:31 — Autor*

---
