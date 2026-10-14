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

### [L17] [L18] [L19] Graf, wątki, wojny (opcja b)

- **L19:**
  - nowa transformacja `pairs-between` (wartości od a do b) i `python -m simulator seed --name … --reset`. Reset czyści wzór tylko wtedy, gdy w changelogu są wyłącznie zapisy wartości startowych; inaczej odmawia;
  - `in war` po resecie: 52 par-lat (UCDP poziom 2); `in war crisis`: 251 par-lat (poziom 1, np. RUS–UKR 2014–2021).
- **L18:**
  - wątki `AGENTS/talk/threads/T001-….md` (nagłówek `# T001 · tytuł`, wpisy oddzielone `---` ×3, podpis w ostatniej linii);
  - GUI: drzewo "Wymiana zdań (wątki)", rozmowa jako karty, odpowiedź w wątku, nowy wątek;
  - "Co czeka na mnie" pokazuje każdy wątek z ostatnim wpisem agenta;
  - `wymiana-zdan-A1.md` = archiwum, tylko odczyt, z notką na końcu;
  - trwające tematy przeniesione do T001–T003, wpisy autora skopiowane dosłownie.
- **L17:** widok "Graf":
  - drzewo 2D z zwijaniem i rozwijaniem; przy pierwszym otwarciu zwinięte są grupy bez otwartych spraw;
  - czerwone krawędzie odwołań wyciągane z numerów w tekstach: A…/L… → zadania, T… → wątki, inne litery → pytania;
  - kolor węzła = status.
- Sprawdzenie:
  - 64 testy;
  - Firefox przez Selenium na kopii `AGENTS/`: odpowiedź w wątku, nowy wątek, zwinięcie grupy w grafie (118 → 43 węzły), brak błędów w konsoli;
  - zrzuty ekranu.

  Selenium i jego sterownik usunięte po teście.

*2026-10-14 02:22 — Claude Opus 5.5*

---

### [L20] [L21] Wątki (odgałęzienia, zamykanie, @) i briefing

- **Odgałęzienia:**
  - `create_thread(..., parent)` → linia `*Odgałęzienie od: T…*`;
  - GUI: przycisk "↳ Nowy wątek od tego", w drzewie wątki-dzieci wiszą pod rodzicem.
- **Zamykanie:**
  - wpis zaczynający się od `🔒`; przycisk "🔒 Zamknij wątek";
  - zamknięte wątki trafiają do grupy "Zamknięte" i nigdy nie czekają w "Co czeka na mnie";
  - T001 i T003 zamknięte zgodnie z ostatnimi wpisami autora.
- **Wzmianki `@`:**
  - podpowiadanie w każdym polu tekstowym (lista z numerem, statusem i tytułem; strzałki, Enter/Tab, Esc);
  - w tekście klikalne linki;
  - w grafie krawędzie, `@phase-2:R1` łączy się tylko z pytaniem z tej fazy.
- **Briefing:**
  - pliki `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md`;
  - przycisk "📋 Briefing" pokazuje najnowszy, a wcześniejsze są jako linki;
  - obowiązek dopisany do instrukcji agentów.
- Sprawdzenie:
  - 65 testów (w tym odgałęzienie, zamykanie, kolejność briefingów);
  - Firefox przez Selenium na kopii: podpowiedź `@R1` → `@phase-2:R1`, wysłany wpis z linkami, odgałęzienie T006, zamknięcie wątku, przycisk Briefing i klik we wzmiankę.

  Narzędzia testowe usunięte.

*2026-10-14 02:37 — Claude Opus 5.5*

---

### [L22] GUI: instrukcja, okna, odgałęzienia

- "❓ Instrukcja": treść w `agents_board/HELP.md` (edytowalna), dołączona do stanu GUI.
- "📌 Przypnij obok": druga kolumna tylko do czytania (dowolna pozycja, np. briefing); pole odpowiedzi zawsze dla okna głównego.
- Przeciągane paski: szerokość menu (osobno dla widoku Graf), szerokość okna przypiętego, wysokość pola odpowiedzi; zapamiętywane w przeglądarce.
- Odgałęzienie pokazuje wpisy rodzica do chwili odgałęzienia (po dacie pierwszego wpisu), rekurencyjnie.
- Skróty zmian: CRE/MOD/DEL (pamięć, instrukcja agentów, briefing).
- Sprawdzenie:
  - Firefox przez Selenium na kopii: instrukcja; T006 z 5 wpisami T002; przypięcie briefingu; przeciąganie pasków; zachowanie po odświeżeniu;
  - zrzut ekranu;
  - 65 testów.

*2026-10-14 03:24 — Claude Opus 5.5*

---

### [L23] Phase 2.0 — runda 1

- `agents-issues-1.md`, U1–U5:
  - regularyzacja i agregaty zamiast pełnej listy krajów (U1);
  - model relacji na parach (U2);
  - rozgałęzianie z przycinaniem do N, rzadkie relacje, float32, wiele rdzeni (U3 — 10¹⁶ ścieżek i ~25 GB/rok bez tego);
  - tury w obrębie roku (U4);
  - `engine.toml` (U5).
- Wątki:
  - @T008 — trzy opcje szumu; bootstrap nie jest zasobożerny (~1 MB);
  - @T005 — kolejność: 2.0 → pilot 1.2b → 2.1;
  - @T007 — tury.
- Zamknięte za zgodą autora: @T002, @T004.

*2026-10-14 03:24 — Claude Opus 5.5*

---

### [L24] [L25] [L26] Projekt silnika, nowe wzory, poprawki GUI

- `AGENTS/phases/phase-2/design.md` v0 — wszystkie decyzje Phase 2.0 w jednym miejscu:
  - dwie wspólne regresje (wewnętrzna i par), dwie tury;
  - zdarzenia przez regresję logistyczną;
  - drzewo scenariuszy z `branching` na rok, szum, uczenie i sprawdzanie;
  - numpy float32;
  - `engine.toml`.
- Wątki:
  - @T009 — podsumowanie modelu (U2), odpowiedzi R7 i S3, pytanie o brakujące dane opisowe;
  - @T010 — rozgałęzianie z liczbami: b=10 → 10 000 scenariuszy, ~1 GB; b=100 niewykonalne (~9 TB).
- Wzory: `state collapse` (0/1), `economic dependence` (0–100, skierowana).
- GUI:
  - `[hidden]` wygrywa z regułami układu (po zamknięciu okna przypiętego pole odpowiedzi skakało na środek);
  - przyciski okna przypiętego na środku, zielony i czerwony;
  - bloki kodu wewnątrz list (formatowanie U5);
  - listy numerowane zachowują numer z tekstu.
- Sprawdzenie:
  - Firefox przez Selenium: pozycja pola odpowiedzi przed i po zamknięciu okna przypiętego = 481 px w obu przypadkach;
  - zrzut ekranu U5;
  - 66 testów.

*2026-10-14 04:14 — Claude Opus 5.5*

---
