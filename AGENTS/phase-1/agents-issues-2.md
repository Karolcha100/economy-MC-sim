# Phase 1 — Nierozwiązane problemy, runda 2 (agents-issues-2)

Problemy, które wyszły podczas implementacji decyzji z `agents-issues.md`. Format jak poprzednio: **Problem / Propozycja / Decyzja**. Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

Stan implementacji jest opisany na końcu dokumentu.

---

## H. Dane scenariusza

### H1. 🔴 W scenariuszu brakuje 40 krajów, w tym Litwy, Łotwy i Estonii
- **Problem:** `tags.csv` powstał w `extract-gdp.ipynb` przez `dropna()` na PKB z lat 1990–2025, więc **każdy kraj z choćby jednym brakującym rokiem został pominięty**. Z 217 gospodarek World Banku brakuje 40, m.in.:
  - Europa: **Litwa, Łotwa, Estonia** (dane od 1993–1995), **Serbia**, Czarnogóra, Kosowo, Liechtenstein, Monako, San Marino,
  - inne ważne politycznie: **Korea Północna** (brak jakichkolwiek danych), **Syria**, **ZEA**, **Afganistan**, Kuba, Liban, Palestyna, Jemen, Erytrea, Sudan Południowy,
  - terytoria zależne (Guam, Grenlandia, Bermudy, Kajmany…).

  Dla modelu "Polska vs Rosja" brak państw bałtyckich jest poważną luką. Scenariusz nazywa się teraz `world-1990-2025` (decyzja E2), a nie obejmuje całego świata.
- **Propozycja:** Zbudować `tags.csv` z listy suwerennych państw (np. 217 gospodarek WB bez terytoriów zależnych), niezależnie od kompletności PKB. Braki w historii zostają jako puste komórki, a `exists_from/exists_to` (H2) opisują, kiedy dany kraj istnieje. Narzędzia już to obsługują: import historii uzupełnia brakujące lata pustymi wartościami i drukuje raport kompletności.
- **Decyzja:**

### H2. 🟡 `exists_from` / `exists_to` są puste dla wszystkich krajów
- **Problem:** Kolumny dodano (decyzja E3), ale nie wypełniono, bo to decyzja merytoryczna. World Bank **rekonstruuje wstecz** PKB państw-sukcesorów (np. UKR, CZE, SVK, KAZ mają dane za 1990), więc dane historyczne nie mówią, kiedy państwo istniało.
- **Propozycja:** Wypełnić według daty uzyskania niepodległości, np. republiki byłego ZSRR (UKR, BLR, KAZ, UZB, …) → `1991`, CZE/SVK → `1993`, HRV/SVN/BIH/MKD → `1991`/`1992`. **Rosja (RUS) od 1990**, traktowana jako kontynuacja ZSRR (inaczej rok 1990 nie ma żadnego odpowiednika ZSRR). Dane historyczne (realne) mogą zawierać wartości dla lat sprzed istnienia państwa, ponieważ walidator sprawdza istnienie państwa tylko dla danych opisowych.
- **Decyzja:**

### H3. 🟡 Wielkość repozytorium przy pełnym wypełnieniu relacji
- **Problem:** Pliki danych opisowych są tworzone dopiero przy pierwszym zapisie (brak pliku = nic nie wypełniono), więc na razie repozytorium nie rośnie. Przy pełnym wypełnieniu: 177 × 177 komórek × 9 relacji × 36 lat ≈ 10 mln wartości, czyli **ok. 60–100 MB CSV** w gicie. Przy 217 krajach (H1) będzie to ~1,5 raza więcej.
- **Propozycja:** Na razie zostać przy CSV (czytelne dla LLM i dla Ciebie). Jeśli rozmiar zacznie przeszkadzać: Git LFS dla `narrated/` albo format Parquet z eksportem do CSV na żądanie.
- **Decyzja:**

### H4. 🟡 Jak symulator ma traktować niewypełnione komórki?
- **Problem:** Puste = "nie wypełniono" (decyzja B1). LLM-y realnie nie wypełnią wszystkich ~31 tys. par krajów w każdym roku, a symulator (kolejne fazy) potrzebuje wartości dla każdej pary.
- **Propozycja:** Ustalić wartość domyślną **na poziomie wzoru**, np. kolumna `default` (`in war` → 0, `diplomatic relation towards` → 0, `stability` → brak/średnia). To wymaga zmiany templates, a templates może zmieniać tylko programista, więc pytam o zgodę. Alternatywa: decyzja dopiero w Phase 2.
- **Decyzja:**

---

## I. Wzory i typy

### I1. 🟡 Typ wartości `TAG` nie jest zaimplementowany
- **Problem:** Instrukcja wymienia `type` = `"float"/"int"/"TAG"`. Według decyzji A3 `TAG` oznacza kraj i występuje w kolumnach `from/to/side-a/side-b`. Nie wiadomo, czy potrzebna jest też **statystyka, której wartością jest tag** (np. "okupowany przez", "główny sojusznik"). Obecnie `type` przyjmuje tylko `float` i `int`.
- **Propozycja:** Nie implementować, dopóki nie ma konkretnej statystyki tego typu. Takie zależności da się zapisać relacją (np. `occupied by` jako relacja skierowana 0/1).
- **Decyzja:**

### I2. 🟢 Znaczenie flag 0/1 w skali roku
- **Problem:** Daty to lata. Dla `riots`, `epidemy`, `mobilized`, `in war` nie wiadomo, czy 1 oznacza "w jakimkolwiek momencie roku", "przez większą część roku", czy "stan na koniec roku".
- **Propozycja:** "W jakimkolwiek momencie roku". Zapisać to w opisie dla LLM (`simulator/README.md`).
- **Decyzja:**

### I3. 🟢 Nazwy / znaczenie kilku wzorów
- **Problem:**
  - `epidemy` → poprawnie po angielsku `epidemic` (nie poprawiłem, bo nie było tego na liście A7),
  - `immigration` / `emigration` (float 0–100): nie wiadomo, co oznacza ta skala (natężenie? odczucie społeczne?). Migracja jest też mierzalna (dane ONZ/WB), więc może powinna trafić do **danych historycznych**, a nie opisowych,
  - `civilization level`, `social sensitivity`: brak opisu znaczenia. LLM-y wypełniające dane potrzebują jednozdaniowej definicji każdej statystyki.
- **Propozycja:** Poprawić `epidemy` → `epidemic` (komenda `formulas edit --rename`). Dodać **opisy statystyk**, np. kolumnę `description` w templates (zmiana programistyczna, wymaga Twojej zgody) albo osobny plik `formulas/descriptions.csv`.
- **Decyzja:**

---

## J. Porządkowe

### J1. 🟢 Zakres fazy w `phases-description.md`
- **Problem:** `phases-description.md` opisuje tylko Phase 1.0 (planowanie). Wiadomość "Uzupełniłem" potraktowałem jako zgodę na implementację Phase 1 według decyzji. Ta faza nie ma jeszcze opisu w pliku.
- **Propozycja:** Dopisać "Phase 1.1 (Implementacja)" oraz kolejną fazę, np. "Phase 1.2 (Wypełnianie danych przez LLM)".
- **Decyzja:**

### J2. 🟢 Pozostałości w `data/`
- **Problem:** `data/desc-stats-api/grades.csv`, `relations-*.csv` i `data/stats/europe-gdp-…csv` zostały przeniesione do scenariusza (`formulas/`, `history/gdp-current-usd.csv`) i usunięte. Został `data/desc-stats-api/organisation-grades.csv`, który jest poza zakresem (A1).
- **Propozycja:** Zostawić do czasu implementacji organizacji albo usunąć.
- **Decyzja:**

### J3. 🟢 Nazwa folderu rozmów
- **Problem:** W decyzji G1 padła nazwa `AGENTS/Consversations/`, która wygląda na literówkę.
- **Propozycja:** Utworzyłem `AGENTS/Conversations/phase-1.md`. Daj znać, jeśli nazwa miała być inna.
- **Decyzja:**

---

## Stan implementacji (dla autora i kolejnych agentów)

Zrobione według decyzji z `agents-issues.md`:

- **Templates** `simulator/common/templates/{internal-grades,relations-directed,relations-doublesided}.csv`. Kolumny relacji dwustronnych to `side-a, side-b` (A4).
- **Scenariusz** `top-100-states-1995-2025` → `world-1990-2025` (E2). `tags.csv` = `tag,name,exists_from,exists_to`. Utworzono `dates.csv` z latami 1990–2025. Usunięto pusty katalog `test-A1`; testy budują własny mini-scenariusz.
- **Wzory** przeniesione z `data/desc-stats-api` do `formulas/`, z poprawionymi literówkami (A7).
- **Historia:** `history/gdp-current-usd.csv` zaimportowany z surowego pliku World Banku, metadane w `history/metadata.csv` (D1, D2).
- **Pakiet `simulator/`:** `templates`, `scenario`, `formulas` (add/edit/remove z migracją danych, A5/A6), `interpolation` (krzywe C2), `store` (zapis atomowy, blokada, changelog, C5/C6), `narrated` (operacje set/batch/show/missing), `history`, `validate`, `cli`.
- **CLI:** `python -m simulator --help`. Instrukcja dla LLM-ów (po angielsku) jest w `simulator/README.md`.
- **Testy:** `venv/bin/python -m pytest` (36 testów).
- **Notebooki** korzystają z modułów (F1). `create-descriptive-stats.ipynb` zawiera teraz same przykłady użycia.
- Danych opisowych jeszcze **nie wypełniono**. To zadanie dla agentów LLM w kolejnym kroku.
