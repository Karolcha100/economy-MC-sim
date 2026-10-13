# Phase 2.0 — Pytania przed planowaniem silnika regresji (agents-issues-0)

Silnik z `README.md`: tuning regresji na danych historycznych, potem Monte Carlo (szum → predykcja kolejnych kroków → prawdopodobieństwa zdarzeń). Poniżej sprawy, które trzeba rozstrzygnąć, zanim powstanie plan implementacji. Format jak w Phase 1: **Problem / Propozycja / Decyzja**. Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

Numeracja `R…` (od "regresja"), żeby nie myliła się z zadaniami `A…` i `L…` w TODOs.

*2026-10-14 00:20 — Claude Opus 5.5*

---

## R. Model

### R1. 🔴 Osobna regresja dla każdego kraju czy jeden model dla wszystkich?
- **Problem:** README mówi "train regression for each country". Na kraj mamy jednak tylko **36 rocznych obserwacji** (1990–2025), a w krajach powstałych w latach 90. jeszcze mniej. Regresja z kilkoma zmiennymi na 30 punktach mocno się przeucza, a lata 90. (transformacja, rozpad ZSRR) są nietypowe.
- **Propozycja:** **Model panelowy**: jeden model uczony na wszystkich krajach naraz (~196 × 36 ≈ 7 000 obserwacji), z indywidualnym poziomem każdego kraju (efekty stałe albo losowe). Opcjonalnie współczynniki "ściągane" do średniej regionu (model hierarchiczny), żeby duże kraje miały swoje własne zależności, a małe korzystały z podobnych. Osobny model tylko dla krajów, gdzie to się uda (backtest, R8).
- **Decyzja:**

### R2. 🔴 Co dokładnie przewidujemy?
- **Problem:** Mamy PKB w **bieżących USD**. Jego zmiany mieszają realny wzrost, inflację i kursy walut (np. Rosja 2014–2015: spadek PKB w USD o ~35% przy realnym spadku ~2%). Model nauczony na tym będzie przewidywał głównie wahania kursów.
- **Propozycja:**
  - przewidywać **realny wzrost**: zaimportować PKB w stałych cenach (World Bank `NY.GDP.MKTP.KD`, ten sam format, import w minutę);
  - PKB w bieżących USD zostaje jako "rozmiar gospodarki";
  - zmienna celu = zmiana logarytmu, czyli tempo wzrostu, a nie poziom;
  - w wersji 1 przewidujemy tylko statystyki prawdziwe (PKB + wskaźniki z Phase 1.2a);
  - statystyki opisowe jako zmienne objaśniające, a w wersji 2 także jako przewidywane.
- **Decyzja:**

### R3. 🔴 Krok czasowy i horyzont
- **Problem:** Dane są roczne. Nie ustalono, na ile lat do przodu symulujemy ani ile scenariuszy (N) liczymy.
- **Propozycja:** Krok = 1 rok. Horyzont domyślnie 10 lat (2026–2035), z możliwością zmiany. Domyślnie N = 10 000 scenariuszy, zmienialne. Prognozy na więcej niż 10 lat będą bardzo niepewne i rozrzut wyników to pokaże.
- **Decyzja:**

### R4. 🟡 Zdarzenia dyskretne (wojna, zamieszki, kryzys migracyjny…)
- **Problem:** README mówi o "discrete non-linear events". Regresja liniowa ich nie przewiduje.
- **Propozycja:**
  - osobny model **prawdopodobieństwa zdarzenia** (regresja logistyczna) dla każdej flagi 0/1, np. P(`riots` w kraju X w roku t+1 | stan w roku t);
  - w Monte Carlo losujemy, czy zdarzenie zaszło;
  - zdarzenie wpływa na kolejny rok jako zmienna (np. wojna obniża wzrost);
  - zdarzeń jest mało (np. wojen międzypaństwowych), więc te modele muszą być proste.
- **Decyzja:**

### R5. 🟡 Szum w Monte Carlo (README, krok 1)
- **Problem:** README: "adding random noise to the last iteration". Nie wiadomo, jak duży ma być szum ani czy szumy różnych statystyk i krajów są ze sobą powiązane. Kryzysy są globalne (2008, 2020), więc niezależny szum zaniża ryzyko wspólnych załamań.
- **Propozycja:** Szum = **reszty modelu losowane z historii całymi latami** (bootstrap po latach). Losujemy np. "rok 2009" i bierzemy reszty wszystkich krajów z tego roku. Zachowuje to korelacje między krajami i statystykami bez dodatkowych założeń.
- **Decyzja:**

### R6. 🟡 Jak użyć relacji (macierze 196 × 196) w regresji?
- **Problem:** Macierzy relacji nie da się wrzucić do regresji wprost.
- **Propozycja:** Agregaty dla każdego kraju, np.:
  - średni wzrost sąsiadów (`neighbours`) i partnerów ważonych `real power towards`;
  - liczba wojen (`in war`) i wojen hybrydowych;
  - średnia `diplomatic relation towards` wobec mocarstw;
  - suma `real power` innych wobec kraju (presja z zewnątrz).

  Zestaw agregatów ustalimy razem.
- **Decyzja:**

### R7. 🟡 Brakujące dane opisowe w treningu
- **Problem:** Dane opisowe będą wypełniane stopniowo (Phase 1.2b). Na starcie większość komórek jest pusta.
- **Propozycja:**
  - pierwsza wersja silnika używa tylko danych prawdziwych (PKB, wskaźniki 1.2a) oraz statystyk opisowych z wartością domyślną (`effective_values`);
  - statystyka opisowa wchodzi do modelu dopiero po wypełnieniu dla ustalonej części krajów i lat (np. Tier 1 + 70% komórek);
  - kolejność wypełniania wyznaczy przydatność zmiennej w modelu.
- **Decyzja:**

### R8. 🟡 Jak sprawdzamy, czy model działa? (backtest)
- **Problem:** Bez testu na danych, których model nie widział, nie wiadomo, czy prognozy są coś warte.
- **Propozycja:**
  - uczymy na latach 1990–2015, sprawdzamy na 2016–2025;
  - porównujemy z prostymi modelami odniesienia: "wzrost jak w zeszłym roku" i "średni wzrost kraju";
  - mierzymy błąd prognozy wzrostu;
  - dla zdarzeń sprawdzamy kalibrację: czy zdarzenia z prognozowanym P = 20% zachodzą w ~20% przypadków.

  Jeśli model nie pokona modeli odniesienia, nie ma sensu go komplikować.
- **Decyzja:**

### R9. 🟢 Podwójne liczenie wskaźników i danych z nich wyliczonych
- **Problem:** Z decyzji M1: np. `stability` (opisowe) będzie wyliczone z WGI (prawdziwe). Obie zmienne w jednym modelu to prawie ta sama informacja.
- **Propozycja:** W modelu używać wersji opisowej, czyli skorygowanej przez LLM i wypełnionej dla wszystkich lat. Surowego wskaźnika używać tylko do kontroli.
- **Decyzja:**

---

## S. Wyniki i technika

### S1. 🟡 Jakie "zdarzenia" i pytania mają być wynikiem?
- **Problem:** README, krok 3: "probability of events". Nie wiadomo, o co pytamy.
- **Propozycja:** Pytania jako plik w scenariuszu (np. `questions.csv`), w których warunek dotyczy statystyk, np.:
  - "PKB POL > PKB RUS przed 2035";
  - "`in war` POL:RUS w dowolnym roku do 2030";
  - "`stability` RUS < 30 w 2030".

  Wynik: prawdopodobieństwo każdego pytania plus rozkłady (percentyle) wybranych statystyk.
- **Decyzja:**

### S2. 🟢 Nietypowe lata (lata 90., 2008, 2020)
- **Problem:** Rozpad ZSRR, kryzys 2008 i COVID mocno odbiegają od normy.
- **Propozycja:**
  - zostawić je w danych, bo właśnie pokazują ryzyko kryzysów (bootstrap z R5);
  - dodać zmienne "rok kryzysu globalnego";
  - lata 1990–1994 dla krajów postsowieckich z mniejszą wagą.
- **Decyzja:**

### S3. 🟢 Technologia i wydajność
- **Problem:** 10 000 scenariuszy × 196 krajów × 10 lat × kilkanaście statystyk to dziesiątki milionów liczb na przebieg.
- **Propozycja:**
  - obliczenia wektorowe w numpy, bez pętli po scenariuszach;
  - modele: `statsmodels` / `linearmodels` (panel), `scikit-learn` (logistyczne);
  - zapisywać tylko wyniki zagregowane (prawdopodobieństwa, percentyle), a pełne scenariusze tylko na żądanie;
  - stałe ziarno losowania dla powtarzalności;
  - nowy moduł `simulator/engine/`, w stylu narzędzi z Phase 1 (CLI + testy).
- **Decyzja:**
