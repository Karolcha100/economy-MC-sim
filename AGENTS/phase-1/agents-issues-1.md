# Phase 1 — Nierozwiązane problemy (agents-issues)

Dokument zawiera problemy, niejasności i luki, które **nie zostały zaadresowane** w `AGENTS/phase-1/agents-instructions.md`, a które trzeba rozstrzygnąć przed implementacją (lub w trakcie) Phase 1.

Każdy punkt ma:
- **Problem** — co jest niejasne / brakuje,
- **Propozycja** — domyślne rozwiązanie, które agenci przyjmą, jeśli nie będzie innej decyzji,
- **Decyzja** — miejsce na odpowiedź autora projektu.

Priorytety: 🔴 blokujące (bez decyzji nie da się sensownie zacząć), 🟡 ważne (wpływa na format danych), 🟢 drobne / porządkowe.

---

## A. Templates i wzory (formulas)

### A1. 🔴 Liczba templates: "4" vs wymienione 3
- **Problem:** Instrukcja mówi "Obecnie są 4 Templates", ale wymienia tylko 3 (Internal Grades, Relations Directed, Relations double-sided). W `data/desc-stats-api/` istnieje dodatkowo `organisation-grades.csv` (o zupełnie innej strukturze: `grade-name, value`), a w notebooku sekcje "Country Organisation" i "International Organisation" są oznaczone `[TODO]`.
- **Propozycja:** Phase 1 obejmuje 3 templates. Organisation Grades (4. template) odkładamy do osobnej fazy, ale format plików projektujemy tak, by łatwo go dodać.
- **Decyzja:** organisation-grades to miałybyć nie template tylko poszczególne country/państwa. Nie musimy ich implementować.

### A2. 🔴 Rozróżnienie: template vs wzór (formula) — co jest w którym pliku
- **Problem:** Instrukcja mówi, że template to plik, w którym "każde pole to oddzielny wiersz", a wzory mają "kolumny takie same jak pola template". Obecne pliki w `data/desc-stats-api/*.csv` (np. `grades.csv` z wierszami `stability, corruption, ...`) to w rzeczywistości **wzory**, nie templates. Pliki templates (`simulator/common/templates/*.csv`) nie istnieją, a ich schemat (jakie kolumny opisują jedno pole) nie jest zdefiniowany.
- **Propozycja:** Plik template ma kolumny:
  `field | dtype | required | allowed_values | description`
  np. dla Internal Grades:
  ```
  field,dtype,required,allowed_values,description
  name,str,true,,Name of the grade (unique, lowercase, spaces allowed)
  type,str,true,float|int|bool|TAG,Value type of the grade
  valmin,float,false,,Lower bound (numeric types only)
  valmax,float,false,,Upper bound (numeric types only)
  ```
  Obecne pliki z `data/desc-stats-api/` zostaną przeniesione jako przykładowe wzory do `simulator/scenarios/top-100-states-1995-2025/formulas/`.
- **Decyzja:** Każda template to oddzielny plik .csv. Tutaj obecne templates:
    - Internal-Grades: "name, type, valmin, valmax"
    - Relations-Directed: "name, type, valmin, valmax, from, to"
    - Relations-doublesided: "name, type, valmin, valmax, organisation-1, organisation-2"


### A3. 🔴 Znaczenie typu / wartości `TAG`
- **Problem:** `TAG` pojawia się w dwóch rolach:
  1. jako możliwy `type` statystyki ("float"/"int"/"TAG") — czyli wartość statystyki to tag kraju (np. "okupowany przez"?),
  2. jako wartość w kolumnach `from`/`to` oraz `organisation-1`/`organisation-2` w wzorach relacji.
  Nie wiadomo, co oznacza `TAG` w drugim przypadku (placeholder "dowolny kraj"? typ encji? ograniczenie do konkretnej listy tagów?), ani jak `valmin/valmax` działa dla typu `TAG`.
- **Propozycja:** W kolumnach `from/to/organisation-*` wartość oznacza **rodzaj encji**, między którymi relacja może istnieć: `TAG` = kraj (z `tags.csv`), w przyszłości np. `ORG` = organizacja. Typ statystyki `TAG` = wartość jest tagiem z `tags.csv` (lub pusta), `valmin/valmax` ignorowane. Interpolacja dla `TAG` jest zawsze schodkowa.
- **Decyzja:** Zgadzam się że `TAG` = kraj, ale `valmin/valmax` nie są ignorowane, one mają za zadanie opisywać przedział wartości która jest między państwami w TAG-ach. Generalnie chodzi o to że Relations-* są przechowywane jako macierz incydencji ale można je wprowadzać do tej macierzy, nie tylko edytując macierz ale i także wpisując TAGi (np. w skrypcie dla modeli LLM).

### A4. 🟡 Niespójne nazwy kolumn relacji: `from/to` vs `organisation-1/organisation-2`
- **Problem:** Relations Directed używa `from, to`, a Relations double-sided `organisation-1, organisation-2`. Nazwa "organisation" sugeruje relacje z organizacjami, a dziś to relacje kraj–kraj.
- **Propozycja:** Ujednolicić: directed → `from, to`; double-sided → `side-a, side-b` (lub `entity-1, entity-2`).
- **Decyzja:** Zgoda, możesz ujednolicić.

### A5. 🟡 Skutki edycji wzorów dla istniejących danych opisowych
- **Problem:** Użytkownik może zmieniać nazwy, typy i zakresy wzorów. Nie określono, co się dzieje z już zapisanymi danymi w `narrated/`:
  - zmiana nazwy → trzeba przemianować pliki / wiersze we wszystkich latach,
  - zmiana zakresu → wartości poza nowym zakresem (przyciąć? błąd?),
  - zmiana typu (float → int) → zaokrąglenie?,
  - usunięcie wzoru → usunąć dane czy zostawić "osierocone"?,
  - dodanie wzoru → jaką wartością zainicjalizować wszystkie lata?
- **Propozycja:** Skrypt `formulas` (add / edit / remove) wykonuje migrację danych w `narrated/`: rename → przemianowanie; zmiana zakresu/typu → walidacja, a wartości niezgodne raportowane (opcja `--clip`); usunięcie → wymaga flagi `--purge`; nowy wzór → inicjalizacja wartością "brak" (patrz B1).
- **Decyzja:** Zgoda.

### A6. 🟡 Czy jest potrzebny skrypt do edycji wzorów?
- **Problem:** Instrukcja wymaga skryptów do wprowadzania **wartości** (sekcja "Sposób wprowadzania danych opisowych"), ale nie mówi wprost o skrypcie do dodawania/edycji **wzorów**, choć użytkownik ma mieć taką możliwość.
- **Propozycja:** Tak — dodajemy skrypt/API do zarządzania wzorami z walidacją względem template (A2) i migracją (A5).
- **Decyzja:** Zgoda.

### A7. 🟢 Literówki w nazwach wzorów
- **Problem:** `happines`, `imigration`, `percevied` (×2). Nazwy trafiają do nazw plików, więc później ich poprawa wymaga migracji.
- **Propozycja:** Poprawić teraz: `happiness`, `immigration`, `perceived`. Uwaga: po poprawce `immigration` (float, 0–100) i `immigration crisis` (int) — sprawdzić, czy nazwy się nie kolidują.
- **Decyzja:** Zgoda.

---

## B. Format przechowywania danych opisowych

### B1. 🔴 Wartość domyślna / "brak danych"
- **Problem:** Obecny notebook inicjalizuje relacje zerami. Dla relacji -100..100 zero to realna wartość ("neutralnie"), więc nie da się odróżnić "LLM ustalił 0" od "jeszcze nie wypełnione".
- **Propozycja:** Brak wartości = pusta komórka (`NaN`). Skrypty mają tryb raportu "co jest jeszcze niewypełnione".
- **Decyzja:** Zgoda.

### B2. 🔴 Format pliku `internal-grades.csv`
- **Problem:** Ścieżka jest zdefiniowana (`narrated/[rok]/Countries/[nazwa country]/internal-grades.csv`), ale nie format pliku (wiersz na grade? kolumny `name,value`?).
- **Propozycja:** Dwie kolumny: `name,value`, jeden wiersz na grade, kolejność jak we wzorze.
- **Decyzja:** Zgoda.

### B3. 🟡 Struktura katalogów Internal Grades: liczba plików i nazewnictwo
- **Problem:**
  - `[nazwa country]` — nazwa czy tag? Nazwy z World Banku zawierają spacje, przecinki i kropki (np. "Korea, Rep.", "Egypt, Arab Rep."), co jest problematyczne w ścieżkach.
  - `Countries` z wielkiej litery jest niespójne z resztą (kebab-case, małe litery).
  - Struktura daje 177 krajów × 36 lat ≈ 6 400 plików z kilkunastoma wartościami — wolne wczytywanie i trudne masowe edycje.
- **Propozycja:** Użyć tagu (`narrated/1995/countries/POL/internal-grades.csv`) i małych liter. Rozważyć alternatywę: jeden plik na rok `narrated/[rok]/internal-grades.csv` (wiersze = tagi, kolumny = grades) — spójną z formatem relacji i historii. Domyślnie trzymamy się instrukcji (z tagiem zamiast nazwy), chyba że zapadnie inna decyzja.
- **Decyzja:** Zgoda na użycie TAG-u. Zgoda też na to aby był jeden plik na rok.

### B4. 🟡 Przekątna macierzy relacji (kraj → ten sam kraj)
- **Problem:** Macierze relacji mają wiersze/kolumny = wszystkie tagi, więc istnieje komórka `POL → POL`. Nie określono jej znaczenia.
- **Propozycja:** Przekątna zawsze pusta (`NaN`), skrypty odrzucają zapis `A → A`.
- **Decyzja:** Zgoda.

### B5. 🟡 Konwencja macierzy relacji skierowanych
- **Problem:** Nie zapisano, czy wiersz = `from`, kolumna = `to`, czy odwrotnie.
- **Propozycja:** wiersz = `from`, kolumna = `to` (czyli `df.loc[FROM, TO]`).
- **Decyzja:** Zgoda.

### B6. 🟡 Relacje dwustronne — sposób zapisu i spójność
- **Problem:** Czy przechowujemy pełną symetryczną macierz, czy tylko trójkąt? Co jeśli ktoś ręcznie zedytuje CSV i macierz przestanie być symetryczna?
- **Propozycja:** Pełna symetryczna macierz (łatwiejsza do czytania przez LLM i pandas); skrypt zawsze zapisuje obie komórki, a walidator zgłasza asymetrię.
- **Decyzja:** Zgoda.

### B7. 🟢 Konwencje CSV
- **Problem:** Notebooki zapisują CSV z nienazwanym indeksem (`,name,type,...` → przy odczycie `Unnamed: 0`). Brak ustaleń dot. separatora, precyzji float, kodowania.
- **Propozycja:** UTF-8, separator `,`, kropka dziesiętna, bez numerycznego indeksu w plikach wzorów/templates; w macierzach indeks = tagi z nazwaną kolumną (`tag`); float zapisywane z max. 4 miejscami po przecinku.
- **Decyzja:** Zgoda.

### B8. 🟢 Zamiana znaków w nazwach plików
- **Problem:** Instrukcja mówi tylko "minus zamiast spacji". Nie określono postępowania dla innych znaków (wielkie litery, `/`, polskie znaki, apostrofy).
- **Propozycja:** Jedna funkcja `slugify`: małe litery, spacje → `-`, znaki spoza `[a-z0-9-]` odrzucane; nazwy wzorów walidowane tak, by slug był unikalny.
- **Decyzja:** Zgoda.

---

## C. Skrypty wprowadzania danych opisowych (używane przez LLM)

### C1. 🔴 Interfejs skryptów: CLI, API Pythona czy oba?
- **Problem:** "Te skrypty będą używane przez inne modele LLM" — nie określono, w jaki sposób (CLI wywoływane z powłoki, funkcje Pythona, narzędzia/MCP). Od tego zależy format wejścia i wyjścia.
- **Propozycja:** Biblioteka Pythona (`simulator/...`) + cienka warstwa CLI (`python -m simulator.narrate ...`). CLI przyjmuje także plik wsadowy JSON/CSV z wieloma operacjami, zwraca czytelny wynik i niezerowy kod wyjścia przy błędach walidacji. Tryb `--dry-run` pokazujący zmiany bez zapisu.
- **Decyzja:** Zgoda, jeśli uważasz że potrzebujesz więcej czasu aby rozplanować feel free, robisz to dla siebie/innych agentów.

### C2. 🔴 Funkcje zmiany — definicje matematyczne i parametry
- **Problem:** Wymienione są "liniowa, wykładnicza, logistyczna", ale bez definicji:
  - **wykładnicza** nie działa dla wartości startowej 0 lub zmiany znaku (relacje -100..100) — `v0 * (v1/v0)^t` jest wtedy niezdefiniowana,
  - **logistyczna** wymaga parametrów (stromość, punkt środkowy),
  - czy potrzebne są inne (schodkowa/step, stała)?
- **Propozycja:** Wszystkie funkcje jako krzywe znormalizowane `f(t)` dla `t ∈ [0,1]`, `f(0)=0`, `f(1)=1`, a wartość = `v0 + (v1 - v0) * f(t)`:
  - `linear`: `f(t) = t`,
  - `exponential`: `f(t) = (e^{k t} - 1) / (e^{k} - 1)`, parametr `k` (domyślnie 3; `k<0` = szybki start, wolny koniec),
  - `logistic`: znormalizowana sigmoida z parametrami `steepness` (domyślnie 10) i `midpoint` (domyślnie 0.5),
  - `step`: wartość `v0` do `midpoint`, potem `v1`,
  - `constant`: wartość `v0` w całym przedziale,
  - `manual`: lista wartości rok po roku.
  Dzięki normalizacji wszystkie działają także dla 0 i zmiany znaku.
- **Decyzja:** Zgoda.

### C3. 🟡 Typy całkowite / binarne i zakresy
- **Problem:** Co z interpolacją dla `int` (np. `riots` 0/1, `in war` 0/1)? Co, jeśli wartości wyjdą poza `valmin/valmax`?
- **Propozycja:** Dla `int` wynik jest zaokrąglany; dla zakresu 0–1 (flagi/zdarzenia) dopuszczalne są tylko `constant`, `step` i `manual`. Wartości poza zakresem → błąd (nie cichy clip), chyba że podano `--clip`.
- **Decyzja:** Zgoda.

### C4. 🟡 Semantyka przedziału dat i nadpisywania
- **Problem:**
  - Czy przedział `[rok_start, rok_koniec]` jest domknięty z obu stron?
  - Co z istniejącymi wartościami w przedziale — zawsze nadpisywać? Tylko puste?
  - Jak łączyć sąsiednie przedziały (koniec jednego = początek następnego)?
  - Czy można podać wartość początkową "z istniejących danych" (kontynuacja od ostatniej wartości)?
- **Propozycja:** Przedział domknięty; domyślnie nadpisywanie, z flagą `--only-empty`; opcja `start=current` bierze wartość z pierwszego roku przedziału, jeśli istnieje.
- **Decyzja:** Zgoda.

### C5. 🟡 Pochodzenie danych (provenance) i uzasadnienie
- **Problem:** Dane wypełniają LLM-y oraz użytkownik. Nie ma mechanizmu zapisu: kto ustawił wartość, kiedy, na jakiej podstawie (źródło, uzasadnienie). Bez tego trudno weryfikować i poprawiać halucynacje.
- **Propozycja:** Log operacji `simulator/scenarios/[scenariusz]/narrated/changelog.csv` (`timestamp, author, operation, target, years, params, rationale`). Kolumna `rationale` opcjonalna, ale zalecana dla LLM.
- **Decyzja:** Zgoda.

### C6. 🟢 Współbieżność
- **Problem:** Jeśli kilku agentów LLM wypełnia dane równolegle, mogą nadpisać ten sam plik (np. jedną macierz relacji dla danego roku).
- **Propozycja:** Zapis atomowy (plik tymczasowy + rename) i prosty plik blokady per scenariusz.
- **Decyzja:** Zgoda.

### C7. 🟢 Literówki w instrukcji (sekcja "Sposób wprowadzania danych opisowych")
- **Problem:** Punkty 2 i 3 mają nagłówek "Relations Directed", a wszystkie trzy mówią "dodawanie/edytowanie Internal Grades".
- **Propozycja:** Interpretujemy: pkt 1 = Internal Grades, pkt 2 = Relations Directed, pkt 3 = Relations double-sided. Warto poprawić w instrukcji.
- **Decyzja:** Zgoda. Poprawiłem.

---

## D. Dane statystyczne (prawdziwe) — `history/`

### D1. 🟡 Skrypt importu i brakujące dane
- **Problem:** Instrukcja opisuje tylko docelowy format (kolumny = tagi, wiersze = daty). Nie określono:
  - czy potrzebny jest skrypt importu (np. z formatu World Banku) — użytkownik ma móc dodawać własne dane,
  - co z brakami — obecny `extract-gdp.ipynb` robi `dropna`, czyli **usuwa kraje** z jakimkolwiek brakiem, przez co zbiór krajów zależy od jednego wskaźnika,
  - co z krajami z `tags.csv`, których nie ma w danym wskaźniku.
- **Propozycja:** Skrypt `history import` przyjmujący CSV w formacie World Banku lub już przetworzonym; wynik zawsze ma **wszystkie** tagi z `tags.csv` i wszystkie daty z `dates.csv`, braki jako `NaN`; raport kompletności po imporcie.
- **Decyzja:** Zgoda.

### D2. 🟡 Jednostki i metadane wskaźników
- **Problem:** Plik `europe-gdp-1990-2025-billion-usd.csv` ma w nazwie "billion" i "europe", a zawiera wartości w USD (nie mld) dla krajów z całego świata. Brak miejsca na jednostkę, źródło i datę pobrania.
- **Propozycja:** Plik metadanych `history/metadata.csv` (`name, unit, source, source_code, downloaded, description`). Nazwa pliku bez jednostki, np. `history/gdp-current-usd.csv`.
- **Decyzja:** Zgoda.

---

## E. Scenariusz: tagi, daty, struktura

### E1. 🔴 `dates.csv` — format i zakres
- **Problem:** Plik nie istnieje. Nie wiadomo: czy daty to tylko lata, czy też kwartały/miesiące; jaki zakres (nazwa scenariusza mówi 1995–2025, dane mają 1990–2025); czy obejmuje lata przyszłe (do predykcji), dla których dane opisowe też trzeba będzie ustalać.
- **Propozycja:** Jedna kolumna `date` z rokiem (int); zakres = zakres historii (1990–2025). Lata predykcji poza zakresem Phase 1.
- **Decyzja:** Zgoda.

### E2. 🟡 Nazwa scenariusza niezgodna z zawartością
- **Problem:** `top-100-states-1995-2025` zawiera 177 krajów i lata 1990–2025.
- **Propozycja:** Zmienić nazwę (np. `world-1990-2025`) albo dociąć dane do opisu. Pusty scenariusz `test-A1` — usunąć lub przeznaczyć na mały scenariusz testowy (kilka krajów, kilka lat) do testów automatycznych.
- **Decyzja:** Zgoda.

### E3. 🟡 Kraje, które nie istniały w danym roku / zmiany terytorialne
- **Problem:** Lista tagów jest stała dla scenariusza, ale w latach 1990–1993 część państw nie istniała (rozpad ZSRR, Jugosławii, Czechosłowacji). Brak sposobu oznaczenia "kraj nie istnieje w tym roku".
- **Propozycja:** Opcjonalne kolumny `exists_from`, `exists_to` w `tags.csv`; dla lat spoza zakresu dane = `NaN`, skrypty odrzucają zapis.
- **Decyzja:** Zgoda.

### E4. 🟢 Organizacje jako uczestnicy relacji
- **Problem:** Komentarz w notebooku: "Aliances covered as International Organisations"; kolumny `organisation-1/2` sugerują relacje z organizacjami (NATO, UE). Brak tagów dla organizacji i decyzji, czy wchodzą w Phase 1.
- **Propozycja:** Poza zakresem Phase 1 (patrz A1); tagi organizacji w przyszłości w osobnym pliku `organisations.csv`.
- **Decyzja:** Oragnizacje mają być dynamiczne i składać się z countries, generalnie poza zakresem, ale informuje już teraz.

---

## F. Kod, środowisko, organizacja repozytorium

### F1. 🟡 Zepsute ścieżki w notebookach po reorganizacji
- **Problem:** Ostatni commit przeniósł `simulator/data` → `data`, a notebooki odwołują się do `scenarios/...` (zamiast `simulator/scenarios/...`). `create-descriptive-stats.ipynb` zapisuje wzory do `data/desc-stats-api`, a nie do `formulas/` scenariusza.
- **Propozycja:** Logika z notebooków trafia do modułów w `simulator/`; notebooki zostają jako przykłady/eksploracja i korzystają z tych modułów.
- **Decyzja:** Zgoda.

### F2. 🟡 Struktura kodu, zależności, testy
- **Problem:** Brak ustaleń co do: struktury pakietu Pythona, pliku zależności (`requirements.txt` / `pyproject.toml`), wersji Pythona (katalog sugeruje 3.14), frameworka testów.
- **Propozycja:** Pakiet `simulator/` (moduły np. `templates.py`, `formulas.py`, `narrated.py`, `interpolation.py`, `history.py`, `cli.py`), `pyproject.toml` z `pandas`, `numpy`, Python ≥ 3.12, testy w `tests/` z `pytest`, operujące na małym scenariuszu testowym.
- **Decyzja:** Zgoda.

### F3. 🟢 Język
- **Problem:** "Wszystko poza komunikacją ze mną po angielsku" — ten dokument jest po polsku zgodnie z `phases-description.md`. Czy dokumentacja dla agentów (`AGENTS/*.md`) ma pozostać po polsku?
- **Propozycja:** Dokumenty w `AGENTS/` po polsku (komunikacja z autorem); kod, komentarze, nazwy plików i danych, docstringi i `README.md` po angielsku.
- **Decyzja:** Tak, dokładnie! Dziękuję za doprecyzowanie!

### F4. 🟢 Zakres "Phase 1" i kryteria ukończenia
- **Problem:** Nie zdefiniowano, co oznacza ukończenie Phase 1 (same skrypty? skrypty + testy? wypełnione dane przykładowe?) ani kolejnych podfaz (1.1, 1.2...).
- **Propozycja:** Phase 1 uznajemy za ukończoną, gdy: istnieją templates w `simulator/common/templates/`, wzory w scenariuszu, skrypty z punktu C działają dla 3 templates i przechodzą testy, istnieje import historii (D1) oraz `tags.csv` i `dates.csv` są kompletne i zwalidowane.
- **Decyzja:** Zgoda!

---

## G. Spójność między danymi (do rozważenia, poza zakresem minimalnym)

### G1. 🟢 Zależności logiczne między statystykami
- **Problem:** Niektóre wartości powinny być ze sobą spójne, np. `in war` (A↔B) a `mobilized` / `war exhaustion` w A; `real power towards` A→B a B→A. Nic tego nie wymusza.
- **Propozycja:** W Phase 1 tylko walidacja zakresów i symetrii; reguły spójności jako osobny, opcjonalny walidator (raport ostrzeżeń, nie błędy) w późniejszej fazie.
- **Decyzja:** Zauważ że państwo może się mobilizować i być wyczerpane wojną, bez wojny (np. po poprzedniej albo zmobilizować się od tak), real power towards nie musi być takie samo, to siła oddziaływania jednego państwa na drugie. Generalnie pozwalam ci zapisać te uwagi i tego typu konwersacje między mną a tobą (lub między agentami) w `AGENTS/Consversations/*.md`
