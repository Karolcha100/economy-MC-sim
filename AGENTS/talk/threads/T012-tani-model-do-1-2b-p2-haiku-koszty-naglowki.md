# T012 · Tani model do 1.2b (P2): Haiku, koszty, nagłówki

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Odpowiedź na @phase-1.2b:P2. Ceny z dokumentacji Anthropic (dziś):

| Model | wejście / 1 mln tokenów | wyjście / 1 mln tokenów |
|---|---|---|
| **Claude Haiku 5.5** | **0,10 $** (powyżej 100 tys. tokenów zapytania: 0,50 $) | **0,50 $** (2,50 $) |
| Claude Sonnet 5.5 | 2 $ | 10 $ |
| Claude Opus 5.5 | 4 $ | 20 $ |

Do tego: **wyszukiwanie w sieci 10 $ za 1000 wyszukiwań**, czytanie stron bez dopłaty (płaci się tylko za tokeny), tryb wsadowy −50%.

**Szacunek dla ~392 zadań** (bardzo zgrubny: ~350 tys. tokenów wejścia i ~10 tys. wyjścia na zadanie z wyszukiwaniem; ~80 tys. bez):

| Wariant | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 |
|---|---|---|---|
| **A** — prasa dla wszystkich lat (~25 wyszukiwań na zadanie) | **~115–175 $** | ~410 $ | ~725 $ |
| **B** — wiedza modelu dla 1990–2022, prasa tylko dla 2023–2025 (~5 wyszukiwań) | **~25–45 $** | ~120 $ | ~225 $ |

Wnioski:
- **Przy Haiku najdroższe są wyszukiwania** (~100 $ w wariancie A), a nie sam model. Dlatego wariant B tak bardzo obniża koszt.
- **"Czytanie samych nagłówków"** (Twój pomysł): agent korzysta tylko z wyników wyszukiwania (tytuły i fragmenty), bez pobierania całych artykułów. Szacunek wyżej już to zakłada. Wyniki wyszukiwania i tak liczą się jako tokeny wejścia, ale całe artykuły dałyby ich kilka razy więcej.
- **Jeśli agentami będą sesje Claude Code w ramach Twojego planu** (jak ja teraz), nie płacisz za tokeny osobno, tylko zużywasz limit planu. Szacunek dotyczy uruchamiania przez API.

**Jakość — jak wybrać uczciwie:** Haiku jest najtańszy, ale najsłabszy w ocenach wymagających wyczucia (`revanchism`, relacje). Mamy jednak **obiektywny test**:
1. dla 10 krajów niech każdy model (Haiku, Sonnet, Opus) oceni `stability` i `corruption` **bez dostępu do wartości startowych**;
2. porównujemy z wartościami z WGI (prawdziwy wskaźnik): kto jest bliżej, ten lepiej rozumie skalę;
3. koszt testu: kilka dolarów.

**Moja propozycja:**
- najpierw ten test;
- potem **Haiku do wypełniania + Sonnet do przeglądu** (przegląd czyta gotowe liczby, więc jest tani), jeśli Haiku wypadnie przyzwoicie;
- **wariant B** (wiedza modelu + prasa dla ostatnich lat);
- tryb pełny (uzasadnienia, źródła) tylko dla krajów ważnych dla modelu (@phase-1.2b:P4).

Zgoda na test? (@A27)

*2026-10-14 05:38 — Claude Opus 5.5*

---
---
---

Nie, jeszcze nie.

*2026-10-14 05:43 — Autor*

---
---
---

Przyjęte: testu modeli na razie nie robimy, a model wybierzemy później (@A27 czeka). Do tego czasu przygotowuję narzędzia i kolejkę, które od modelu nie zależą.

*2026-10-14 06:03 — Claude Opus 5.5*

---
---
---

Proszę o nowy wątek z ponowną wyceną (włączającą ograniczenia) dla Twojej propozycji.

Tj.

`Moja propozycja:

najpierw ten test;
potem Haiku do wypełniania + Sonnet do przeglądu (przegląd czyta gotowe liczby, więc jest tani), jeśli Haiku wypadnie przyzwoicie;
wariant B (wiedza modelu + prasa dla ostatnich lat);
tryb pełny (uzasadnienia, źródła) tylko dla krajów ważnych dla modelu (@phase-1.2b:P4).`

*2026-10-14 06:18 — Autor*

---
---
---

Nowa wycena z ograniczeniami: @T016 (odgałęzienie od tego wątku). Opis testu modeli: @T015.

*2026-10-14 06:21 — Claude Opus 5.5*

---
---
---
