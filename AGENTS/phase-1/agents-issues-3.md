# Phase 1 — Nierozwiązane problemy, runda 3 (agents-issues-3)

Problemy, które wyszły przy implementacji decyzji z `agents-issues-2.md`. Format: **Problem / Propozycja / Decyzja**. Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

Propozycje dotyczące wypełniania danych przez LLM (J1) są w osobnym pliku: `AGENTS/Conversations/phase-1.2-propozycje-wypelniania.md`. Na końcu tamtego pliku są 4 pytania.

---

## K. Lista państw (H1, H2)

### K1. 🟡 Brak Tajwanu
- **Problem:** World Bank nie publikuje danych dla Tajwanu, więc nowa lista (195 państw z WB) go nie zawiera. Tajwan jest ważny dla relacji CHN–USA i dla gospodarki światowej (~20. PKB świata).
- **Propozycja:** Dodać tag `TWN` (`Taiwan`). PKB uzupełnić z IMF World Economic Outlook przez `history import --format wide` (wymaga ręcznego pobrania pliku z IMF).
- **Decyzja:** Absolutna Zgoda! W pełni się zgadzam! Bardzo dziękuję za zauważenie tego.

### K2. 🟡 Sporne decyzje na liście państw — do potwierdzenia
- **Problem:** Przy budowie `tags.csv` przyjąłem kilka założeń merytorycznych:
  - **odrzucone terytoria zależne (22)**: m.in. Hongkong (`HKG`) i Portoryko (`PRI`), które były na poprzedniej liście, a także Makau, Grenlandia, Wyspy Owcze, Guam i Bermudy;
  - **włączone państwa o ograniczonym uznaniu**: Kosowo (`XKX`, od 2008) i Palestyna (`PSE`, od 1994, czyli od powstania Autonomii Palestyńskiej);
  - **kontynuacje**: Rosja = kontynuacja ZSRR, Serbia = kontynuacja Jugosławii (obie od 1990); Niemcy od 1990 (NRD nie jest modelowana); Jemen od 1990 (zjednoczenie);
  - **rok istnienia** = rok uzyskania niepodległości (wystarczy dowolny moment roku, np. UKR 1991, CZE/SVK 1993).

  Pełna, odtwarzalna logika jest w `extract-gdp.ipynb` (komórka "tags.csv of world-1990-2025").
- **Propozycja:** Zostawić jak jest; ewentualne poprawki to jedna linijka w notebooku.
- **Decyzja:** Zgoda, poinformuj o tym inne agenty.

### K3. 🟢 Luki w PKB w latach istnienia państw
- **Problem:** 18 państw ma braki PKB w latach, w których istnieją. Najważniejsze dla modelu: **LTU, LVA 1991–1994, EST 1991–1992, SRB 1990–1994**. Poza tym: PRK cały okres, AFG, ERI, SSD, YEM, CUB, SYR w ostatnich latach, kilka państw w 2025. Symulator (Phase 2) będzie potrzebował wartości.
- **Propozycja:** W Phase 1 zostawić puste (to prawdziwe braki danych). Przed Phase 2 zdecydować: uzupełnienie z innego źródła (IMF, UN), interpolacja/ekstrapolacja oznaczona w metadanych, albo obsługa braków w samym modelu.
- **Decyzja:** Uzupełnij je, spróbuj inne źródła, jeżeli się nie uda to interpolacja/ekstrapolacja. Generalnie napisz skrypty które zauważają braki oraz które te braki uzupełniają i informują o tych zmianach w jakimś logu (możesz to przydzielić innemu agentowi do zrobienia)

---

## L. Opisy i wartości domyślne wzorów (H4, I3)

### L1. 🔴 Opisy statystyk — proszę o przegląd
- **Problem:** Napisałem opisy wszystkich 24 statystyk (kolumna `description` w `formulas/*.csv`). LLM-y będą się na nich opierać, więc każda nieścisłość zostanie powielona. Najmniej pewne są:
  - `social sensitivity` — przyjąłem: "jak mocno społeczeństwo reaguje na straty, ofiary i trudności";
  - `civilization level` — przyjąłem: "ogólny poziom rozwoju (edukacja, technologia, zdrowie, instytucje)", czyli coś w rodzaju HDI;
  - `immigration` / `emigration` — przyjąłem: "natężenie migracji względem liczby ludności";
  - **ujemna połowa skali** dla `perceived/real subordination towards` (−100 = "FROM uważa TO za swojego wasala") i `perceived/real power towards` (ujemne = "działania FROM wobec TO przynoszą odwrotny skutek"). Tę interpretację wymyśliłem, bo skala −100..100 jej wymaga;
  - `in hybrid war` jest relacją **dwustronną**, a działania hybrydowe są często jednostronne (np. RUS → POL);
  - `neighbours` — przyjąłem **tylko granicę lądową** (bez morskiej, np. POL–SWE = 0).
- **Propozycja:** Przejrzyj `simulator/scenarios/world-1990-2025/formulas/*.csv` (kolumna `description`) i popraw bezpośrednio w pliku albo komendą `python -m simulator formulas edit --description ...`. Jeśli `in hybrid war` ma być jednostronna, przeniosę ją do relacji skierowanych.
- **Decyzja:** Dobra, przejrzę potem, to nie jest na tyle ważne w tym momencie - Generalnie zapisz gdzieś że w przyszłości trzeba zrobić skrypt z GUI do edycji tych danych.

### L2. 🟡 Przyjęte wartości domyślne
- **Problem:** Ustawiłem:
  - relacje skierowane: wszystkie `0` (neutralnie / brak wpływu / brak zależności);
  - relacje dwustronne: wszystkie `0` (brak wojny, brak sąsiedztwa);
  - flagi wewnętrzne (`immigration crisis`, `riots`, `epidemic`, `mobilized`): `0`;
  - `war exhaustion`: `0`;
  - pozostałe ciągłe internal grades (np. `stability`, `corruption`): **brak wartości domyślnej**, czyli trzeba je wypełnić dla każdego kraju.
- **Propozycja:** Zostawić jak jest. Brak wartości domyślnej dla cech wewnętrznych wymusza ich wypełnienie i nie ukrywa luk pod sztuczną średnią.
- **Decyzja:** Zgoda.

---

## Stan realizacji decyzji z `agents-issues-2.md`

- **H1** — `tags.csv` zawiera **195 państw** (wszystkie gospodarki WB bez terytoriów zależnych), posortowanych wg ostatniego dostępnego PKB. Litwa, Łotwa, Estonia, Serbia, PRK i inne są teraz w scenariuszu.
- **H2** — `exists_from` wypełnione dla 27 państw (patrz K2). PKB ponownie zaimportowany dla nowej listy.
- **H3** — bez zmian (CSV); Git LFS / Parquet dopiero przy realnym problemie.
- **H4** — templates mają pole `default`; brak wartości = trzeba wypełnić. Nowa funkcja `simulator.narrated.effective_values(...)` zwraca wartości z podstawionymi wartościami domyślnymi (dla kolejnych faz).
- **I1** — typ `TAG` nie jest implementowany.
- **I2** — flagi 0/1 = "w dowolnym momencie roku, tylko poważne zdarzenia" (opisy wzorów + `simulator/README.md`). Dla `riots` wprost: poważne, gwałtowne zamieszki o znaczeniu ogólnokrajowym; pokojowe protesty się nie liczą.
- **I3** — `epidemy` → `epidemic`; templates mają wymagane pole `description`, a wszystkie wzory mają opisy (patrz L1).
- **J1** — dopisane Phase 1.1 i 1.2 w `phases-description.md`; propozycje wypełniania danych są w `AGENTS/Conversations/phase-1.2-propozycje-wypelniania.md`.
- **J2** — usunięto `data/desc-stats-api/organisation-grades.csv`.
- Uwaga autora nr 1 (`agents-issues.md` → `agents-issues-1.md`) — odwołania w moich dokumentach poprawione; uwaga oznaczona jako przeczytana.
- Testy: 38 przechodzi; `validate` scenariusza: 0 błędów, 0 ostrzeżeń.
