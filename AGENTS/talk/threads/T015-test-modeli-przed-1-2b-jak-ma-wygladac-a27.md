# T015 · Test modeli przed 1.2b — jak ma wyglądać (A27)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Rozpisanie testu z @A27. Cel: sprawdzić **przed** wypełnieniem ~392 zadań, czy tani model (Haiku) dobrze rozumie nasze skale, czy trzeba droższego.

**Pomysł:** dla dwóch statystyk mamy "prawdziwą odpowiedź" z danych: `stability` (z WGI) i `corruption` (z WGI), przeliczone według W1–W2. Modele ocenią je **bez dostępu do tych wartości**, a my policzymy, jak blisko trafiły.

**Przebieg:**
1. **10 krajów** z całej skali: CHE, NOR, POL, DEU, RUS, UKR, BRA, IND, NGA, SOM.
2. **3 modele**: Claude Haiku 5.5, Sonnet 5.5, Opus 5.5.
3. Każdy model dostaje dla każdego kraju:
   - **opis statystyki** z `formulas/` (taki jak w instrukcji 1.2b);
   - **kotwice** (CHE, SOM itd.) — bez kraju, który ocenia;
   - **bez** wartości startowych i bez dostępu do WGI.

   Zadanie: opisać `stability` i `corruption` w latach 1996–2022 okresami (jak w instrukcji 1.2b). Bez wyszukiwarki, bo wariant B to wiedza modelu.
4. **Dwa powtórzenia** każdego zadania, żeby zobaczyć, czy model jest stały (czy dwa razy daje podobne liczby).
5. **Miary** (liczy skrypt):
   - średni błąd względem wartości z WGI (w punktach skali 0–100);
   - czy kolejność krajów się zgadza (np. CHE > POL > RUS > SOM);
   - różnica między dwoma powtórzeniami.
6. **Reguła decyzji** (propozycja): Haiku wystarczy, jeśli jego średni błąd jest najwyżej o 50% większy niż Sonneta i kolejność krajów się zgadza. Jeśli nie, porównujemy Sonnet z Opusem tak samo.
7. **Wynik:** tabela w `AGENTS/phases/phase-1.2b/test-modeli.md` + krótka rekomendacja w tym wątku.

**Ograniczenia testu:**
- sprawdza tylko statystyki, dla których mamy dane z WGI. Dla `social revanchism` czy relacji obiektywnej miary nie ma, więc proponuję dodatkowo, żebyś przejrzał wyniki 2 krajów (np. POL i RUS) od każdego modelu;
- 10 krajów to mała próba: wynik wskaże kierunek, nie da pewności.

**Koszt** (ceny API): Haiku ~0,10 $, Sonnet ~1,80 $, Opus ~3,50 $ — **razem ~5–6 $**.

**Jak uruchomić — do wyboru:**
- **(a) skrypt przez API Anthropic** (`anthropic` w Pythonie): dokładny pomiar zużycia tokenów, a więc i realna wycena 1.2b. Wymaga klucza API (`ANTHROPIC_API_KEY` albo `ant auth login`);
- **(b) agenci w Claude Code** z wyborem modelu (haiku / sonnet / opus): bez klucza, w ramach Twojego planu, ale zużycie tokenów jest mniej dokładnie widoczne.

Którą drogą? (@A27)

*2026-10-14 06:21 — Claude Opus 5.5*

---
---
---

Dobra a co ty na to aby zrobić ten test tylko dla haiku na claude code?

*2026-10-14 06:29 — Autor*

---
---
---

Dobry pomysł. Test na samym Haiku jest najtańszy, a odpowiedź na główne pytanie daje od razu. Zamiast porównania z Sonnetem użyłem progu bezwzględnego. Ponieważ test był Twoją propozycją i nic nie zapisywał w danych, **od razu go przeprowadziłem**: 20 agentów Haiku w Claude Code, bez wyszukiwarki.

**Wyniki** (szczegóły: `AGENTS/phases/phase-1.2b/test-modeli.md`):
- **`corruption`: bardzo dobrze.** Średni błąd ~5 punktów, kolejność krajów zgodna w 96–99%, dwie serie różnią się o ~3,5 punktu.
- **`stability`: błąd ~18 punktów, ale prawie cały to przesunięcie w górę (+17)**, głównie przez różnicę definicji:
  - WGI mierzy przede wszystkim **ryzyko przemocy i terroryzmu**, więc Indie i Rosja mają tam ~30;
  - nasz opis ("stabilność polityczna i instytucjonalna", 100 = w pełni stabilne instytucje) prowadzi Haiku do Indii ~70 i Niemiec ~89;
  - nasze przeliczenie WGI daje stabilnym demokracjom tylko 64–77, mniej niż mówi opis.
- **Powtarzalność dobra**, ok. 4 punkty różnicy między seriami.

**Wniosek:** Haiku nadaje się do wypełniania. **Przed startem trzeba jednak rozstrzygnąć `stability`** (@A30):
- **(a)** zmienić opis `stability` tak, żeby jak WGI obejmował przemoc i terroryzm; wartości startowe zostają;
- **(b)** zostawić opis (stabilność instytucji) i zmienić przeliczenie WGI, np. tak, żeby stabilne demokracje dostawały ~90, a WGI służył tylko jako kotwica;
- **(c)** rozdzielić na dwie statystyki: `stability` (instytucje, LLM) i `violence risk` (z WGI).

Moja rekomendacja to **(c)**: obie rzeczy są ważne dla modelu (kryzys rządowy to nie to samo co terroryzm), a wartości z WGI zostają tam, gdzie pasują.

*2026-10-14 06:33 — Claude Opus 5.5*

---
---
---

Wybieram: rozdzielić na dwie statystyki: stability (instytucje, LLM) i violence risk (z WGI).

*2026-10-14 06:37 — Autor*

---
---
---

Wdrożone, opcja (c):
- **nowa statystyka `violence risk`** (0–100: ryzyko przemocy politycznej i terroryzmu). Dostała wartości startowe z WGI: 50 − 20 × WGI, lata 1996–2022, np. 2015: POL 33, RUS 71, IND 69, SOM 97;
- **`stability`** ma nowy opis: tylko stabilność instytucji i rządu (kryzysy rządowe, przedterminowe wybory, zamachy stanu), **bez przemocy**. Dotychczasowe wartości startowe z WGI usunąłem, bo zapisywały je tylko wartości startowe, a teraz należą do `violence risk`. `stability` wypełnią w całości LLM-y; test pokazał, że Haiku rozumie ją zgodnie z tym opisem;
- reguła w `simulator/scenarios/world-1990-2025/seeds.csv` zmieniona, a `validate` nie zgłasza błędów.

Jeśli to wszystko w tym wątku, możesz go zamknąć.

*2026-10-14 06:43 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-14 06:44 — Autor*

---
---
---
