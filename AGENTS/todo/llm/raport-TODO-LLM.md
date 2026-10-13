# Raporty z wykonania TODO — agenci LLM

Każdy wpis: `### [L…] tytuł`, co zrobiono, gdzie, jak sprawdzono, co zostało; podpis z datą i godziną; `---`. Zasady: `INSTRUKCJA.md`.

---
---
---

### [L6] PKB Korei Północnej (M2, A2)

- Serwer ONZ (unstats.un.org) ucina plik `.xlsx`; wznawianie pobierania (`curl -C -`) też nie działa.
- Źródło zastępcze, wskazane przez autora: worldometers.info, tabela "GDP Nominal (Current USD)" 1970–2023. Worldometers podaje jako źródło UN Statistics Division, National Accounts.
- Pliki:
  - `data/worldometers/prk-gdp-current-usd.csv` — dane;
  - `data/worldometers/README.md` — pochodzenie.
- Uzupełnienie Korei Północnej w historii PKB:
  - `history fill --method source --tags PRK` (1990–2023);
  - `history fill --method extrapolate --tags PRK` (2024–2025).

  Log: `history/fill-log.csv`. Kroki dopisane do `extract-gdp.ipynb`, więc notebook odtwarza plik PKB.
- Sprawdzenie: `history gaps` → 0 braków; `validate` → 0 błędów. Wartości: 1990 14,7 mld USD, 2023 16,4 mld USD.
- Co zostało: jeśli kiedyś uda się pobrać plik ONZ, warto zastąpić dane z drugiej ręki oryginałem.

*2026-10-14 00:20 — Claude Opus 5.5*

---

### [L7] Phase 2.0 — `AGENTS/phases/phase-2/agents-issues-0.md`

- Utworzone:
  - `AGENTS/phases/phase-2/agents-issues-0.md` — pytania R1–R9 (model) i S1–S3 (wyniki, technika) w formacie Problem / Propozycja / Decyzja;
  - `AGENTS/phases/phase-2/agents-instructions.md` — szkielet do uzupełnienia przez autora (A11).
- Co zostało: czekamy na decyzje autora (A12), potem L9.

*2026-10-14 00:20 — Claude Opus 5.5*

---

### [L1] Import wskaźników do `history/`

- Zaimportowane do `world-1990-2025` (lista: `python -m simulator history list`; pochodzenie i licencje: `data/README.md`):
  - `wgi-political-stability`, `wgi-control-of-corruption` (oficjalny plik WGI, 1996–2022);
  - `hdi`, `ti-cpi`, `happiness-cantril` (Our World in Data);
  - `net-migration`, `migrant-stock-share`, `population` (World Bank).
- Pary krajów (`history/dyadic/`):
  - `land-borders` (GeoNames, dzisiejsze granice, tylko lata, w których oba kraje istnieją);
  - `ucdp-armed-conflict` (UCDP v25.1: 2 = wojna międzypaństwowa, 1 = przeciwne strony z udziałem strony wspierającej).
- Populacja Tajwanu uzupełniona z MFW (`data/imf/LP.json`), więc populacja nie ma luk.
- **Problem znaleziony:** seria WGI z archiwum World Banku (API, source 3) ma złą skalę (około ×25 i niespójna w czasie). Dlatego oficjalny plik WGI (2023 update, do 2022). Zapisane w `data/README.md`.
- Sprawdzenie: wartości 2015 dla POL/RUS/UKR/CHE/SOM wyglądają sensownie (np. WGI PV: POL 0,86, RUS −1,03, UKR −1,96); `validate` → 0 błędów.
- Nie zrobione: UN DESA w pełnej wersji (macierz migracji między krajami) i World Happiness Report bezpośrednio, bo OWID wystarcza jako kotwica.

*2026-10-14 01:15 — Claude Opus 5.5*

---

### [L2] Konwertery formatów i dane par krajów

- `simulator/sources.py`: czytniki OWID, oficjalnego WGI (`.xlsx`), GeoNames (sąsiedzi), UCDP Dyadic (kody Gleditscha-Warda → tagi przez `country_converter`, z ręcznymi wyjątkami, np. Wietnam, Czechy).
- `history import --format owid|wgi-xlsx` (opcje `--column`, `--sheet`), nowa komenda `history import-dyadic`, nowy katalog `history/dyadic/` (`date,side_a,side_b,value`), kolumna `shape` w `history/metadata.csv`.
- `context POL:RUS` pokazuje dane par; `validate` sprawdza pliki par.
- **Błąd naprawiony po drodze:** `country_converter` dla nieznanego kodu zwraca sam kod, więc Czechy (316) po cichu wypadały z danych UCDP. Teraz nieznany kod = błąd.
- Testy: `tests/test_sources.py` (5 nowych), razem 52, wszystkie przechodzą.

*2026-10-14 01:15 — Claude Opus 5.5*

---

### [L4] Kolumna `sources`

- `set --sources ...` (można powtarzać) i klucz `sources` w `batch`; zapis w `narrated/changelog.csv` (oddzielone ` | `).
- Starszy changelog bez tej kolumny jest jednorazowo przepisywany z nowym nagłówkiem (test).
- Opis w `simulator/README.md`.

*2026-10-14 01:15 — Claude Opus 5.5*

---

### [L11] Nowa hierarchia `AGENTS/`

- Struktura: `plan/`, `phases/<faza>/`, `todo/author|llm/`, `talk/` + `AGENTS/README.md` (mapa, zasady, tabela "stare → nowe ścieżki").
- Nazwy plików bez zmian (`agents-issues-N.md` itd.), poza `od-autora-dla-llmów.md` → `talk/od-autora-dla-llmow.md` (bez polskich znaków).
- Odnośniki poprawione w żywych dokumentach (instrukcje, listy TODO, plan, notatki, `simulator/README.md`, `simulator/review.py`). **Nie** zmieniane: wcześniejsze wpisy w wymianie zdań, decyzje autora i raport autora (zasada: nie edytujemy wcześniejszych wypowiedzi); tekst autora o Phase 1.0 w `phases-description.md` przywrócony po automatycznej zamianie.
- W `todo/author/INSTRUKCJA.md` (plik autora) zmienione tylko ścieżki przy przenosinach.

*2026-10-14 02:00 — Claude Opus 5.5*

---

### [L12] GUI `agents_board` (etap 1: podgląd, etap 2: odpowiadanie)

- `python -m agents_board` → lokalna strona (127.0.0.1:8765), tylko biblioteka standardowa Pythona.
  - Trzy drzewa do wyboru: "Co czeka na mnie", "Według rodzaju", "Według plików".
  - Po prawej pełny tekst wybranej pozycji (przewijany osobno), a pod nim pole odpowiedzi, więc tekst jest cały czas widoczny.
- Odpowiadanie:
  - decyzja w pytaniu — tylko gdy pole puste;
  - wpis do raportu autora + zmiana statusu zadania A;
  - nowy wpis w wymianie zdań (z podpisem i separatorami);
  - nowa uwaga dla agentów.
- Szkice zapisują się w przeglądarce (localStorage), więc odświeżenie albo błąd nie kasuje tekstu.
- Bezpieczeństwo:
  - zapis tylko z tokenem z tej strony;
  - tylko pliki `.md` w `AGENTS/`;
  - jeśli plik zmienił się od otwarcia strony (np. edycja w VS Code), zapis jest odrzucany i nic nie jest nadpisywane.
- `--read-only` (sam podgląd), `--static plik.html` (plik bez serwera).
- Sprawdzenie:
  - 8 testów (`tests/test_agents_board.py`): parsowanie, wszystkie zapisy, konflikt wersji, ścieżki spoza `AGENTS/`, token przez prawdziwy serwer HTTP;
  - zrzuty ekranu w Firefoksie (podgląd, formularz zadania, wymiana zdań);
  - składnia JS sprawdzona silnikiem JS.
- **Niesprawdzone:** kliknięcie "Zapisz" w prawdziwej przeglądarce (tryb bez okna nie klika). Logika zapisu po stronie serwera jest przetestowana. Prośba do autora: A16.

*2026-10-14 02:00 — Claude Opus 5.5*

---

### [L3] [L5] [L10] [L13] Wartości startowe Phase 1.2a

- Decyzje A13/A15 w danych:
  - CZE jako kontynuacja Czechosłowacji (od 1990; także w `extract-gdp.ipynb` i V4 od 1991);
  - opis `civilization level` w skali bezwzględnej (100 × HDI);
  - nowe wzory `net migration` (−100..100) i `in war crisis` (0/1, bez wartości startowych — dla LLM).
- `simulator/seed.py` + `python -m simulator seed`. Przepisy w `scenarios/world-1990-2025/seeds.csv`:
  - transformacje `linear`, `per-1000-linear`, `pairs-at-least`;
  - interpolacja liniowa luk wewnątrz zakresu (Y1);
  - nigdy nie nadpisuje wypełnionych komórek (Y2).
- Zapisane: stability 5035, corruption 4979, civilization level 5890, net migration 6920 wartości; in war 303 par-lat; neighbours 10 974 + 89 (granice historyczne).
- Przykłady 2015: stability POL 67, RUS 29, UKR 11, SOM 3; net migration 2022: POL +100, UKR −100.
- `review`: nowe ostrzeżenie `seed-deviation` (> 15 punktów od wartości startowej).
- Granice historyczne (L10): `data/manual/historical-land-borders.csv` (15 par z notatkami) + format `pair-ranges`; przegląd autora: A17.
  - GeoNames już dziś liczy granicę ALB–SRB (przez Kosowo), więc ta ręczna para jest zbędna, ale nieszkodliwa.
- Testy: `tests/test_seed.py` (3), razem 63; `validate` 0 błędów; notebook odtwarza `tags.csv` i PKB bajt w bajt.

*2026-10-14 02:10 — Claude Opus 5.5*

---

### [L16] Poprawki GUI po A16

- Ikony statusów: kolorowe znaczki (🟠 do zrobienia, 🔵 w toku, ✅, ⏸️, ➡️, ❌) zamiast ☐, który wyglądał jak brakujący znak.
- Edytor: Tab / Shift+Tab (też dla zaznaczonych linii), Enter kontynuuje listę `-` i `1.` (pusty punkt kończy listę), Tab w punkcie listy tworzy podlistę od `1.`, Ctrl+Enter wysyła, Ctrl+Z działa.
- Przełączanie pozycji przez zmianę `#` w adresie bez przeładowania. Błąd wyszedł w teście: wpis trafił do niewłaściwego formularza, na kopii plików.
- Podpis "— Autor" z datą i godziną był już wcześniej. Dopisałem to w podpowiedzi pod polem.
- Sprawdzenie: prawdziwy Firefox sterowany przez Selenium na kopii `AGENTS/`:
  - pisanie list, Tab, Shift+Tab, Ctrl+Z;
  - zapis raportu i decyzji kliknięciem / Ctrl+Enter;
  - zachowanie szkicu przy przełączaniu pozycji.

  Selenium i jego sterownik usunięte po teście.

*2026-10-14 02:10 — Claude Opus 5.5*

---
