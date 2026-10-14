# TODO dla agentów LLM

Zasady (numeracja `L…`, statusy, raporty): `INSTRUKCJA.md`. Kolejność faz: `AGENTS/plan/phases-plans.md`.

*Utworzone: 2026-10-13 23:29, numeracja dodana 2026-10-14 00:20 — Claude Opus 5.5*

---

## Phase 1.2a — prawdziwe wskaźniki (szczegóły: `AGENTS/phases/phase-1.2a/M1-wskazniki.md`)

Zgoda autora (A10) jest: 2026-10-14. Pytania o przeliczenia skal: `AGENTS/phases/phase-1.2a/agents-issues-0.md` (A13).

- [x] **L1. Import wskaźników do `history/`** (z metadanymi i sprawdzeniem licencji):
  - WGI Political Stability i Control of Corruption;
  - HDI;
  - UN DESA migrant stock + WB net migration;
  - UCDP dyadic;
  - Correlates of War Direct Contiguity;
  - World Happiness Report.

  *(zrobione: 2026-10-14 01:15, raport: raport-TODO-LLM.md)*
- [x] **L2. Konwertery formatów**, których `history import` jeszcze nie zna (HDI, UCDP, CoW, WHR). UCDP i CoW są parami krajów, więc potrzebny jest format "dyadyczny" (osobny katalog w `history/`). *(zrobione: 2026-10-14 01:15, raport: raport-TODO-LLM.md)*
- [x] **L3. Skrypt "seed"**: wskaźnik → skala wzoru → `narrated/` z `author=seed:<źródło>`. Każde przeliczenie skali opisać i dać autorowi do przejrzenia (A5). *Decyzje A13 są (W1, W2 zgoda; W3 skala bezwzględna; X1–X3 zgoda; Y1 interpolacja liniowa). Czeka jeszcze na A15 (W4, Y2). Można zacząć od W1–W3, X1–X3.* *(zrobione: 2026-10-14 02:10, raport: raport-TODO-LLM.md)*
- [x] **L4. Kolumna `sources`** w operacjach (`set`/`batch`) i w `narrated/changelog.csv` (decyzja M1). *(zrobione: 2026-10-14 01:15, raport: raport-TODO-LLM.md)*
- [x] **L5. `review`**: ostrzeżenie, gdy wartość odbiega od seeda o więcej niż X. *(zrobione: 2026-10-14 02:10, próg 15 punktów; raport: raport-TODO-LLM.md)*
- [x] **L6. PKB Korei Północnej (M2).** *(zrobione: 2026-10-14 00:20, raport: raport-TODO-LLM.md)*

- [x] **L10. Ręczne poprawki granic** (`neighbours`) dla lat sprzed dzisiejszych granic: RUS 1990 jako ZSRR, SRB jako Jugosławia, SDN przed 2011. Plik do przejrzenia przez autora. *(zrobione: 2026-10-14 02:10, `data/manual/historical-land-borders.csv`, przegląd autora: A17)*

## Porządek w plikach i narzędzia współpracy

- [x] **L11. Nowa hierarchia `AGENTS/`** (`git mv` + poprawa odnośników + `AGENTS/README.md`). *(zrobione: 2026-10-14 02:00, raport: raport-TODO-LLM.md)*
- [x] **L12. Podgląd TODO/pytań jako HTML** (etap 1: tylko odczyt, linki do plików). Etap 2 (odpisywanie z GUI) też zrobiony. *(zrobione: 2026-10-14 02:00, raport: raport-TODO-LLM.md)*

## Phase 2.0 — planowanie silnika regresji

- [x] **L7. `AGENTS/phases/phase-2/agents-issues-0.md`** — niejasności do rozstrzygnięcia przez autora. *(zrobione: 2026-10-14 00:20, raport: raport-TODO-LLM.md)*
- [?] **L9. Po odpowiedziach autora (A11, A12; odłożone przez autora)**: `AGENTS/phases/phase-2/agents-issues-1.md` z kolejnymi pytaniami albo plan implementacji Phase 2.1.

## Phase 1.2b — wypełnianie z prasy (później, według priorytetów z Phase 2)

- [x] **L8. Instrukcja dla agentów wypełniających dane z prasy.** Ma zawierać:
  - korzystanie z wyszukiwarki (zgoda autora, A3);
  - zapis źródeł (URL, tytuł, data);
  - język lokalny dla krajów Tier 1;
  - media państwowe = oficjalna postawa, nie nastroje;
  - kotwice (kraje referencyjne);
  - format batch;
  - `--dry-run` → `validate` → `review`.

## Phase 1.2a — wdrożenie decyzji A13 (razem z L3)

- [x] **L13. Decyzje A13 w danych scenariusza**:
  - W3: opis `civilization level` na skalę bezwzględną (100 × HDI);
  - X3: CZE jako kontynuacja Czechosłowacji (`exists_from` puste) w `tags.csv` i w `extract-gdp.ipynb`;
  - potem `validate`. *(dodane 2026-10-14 02:00; zrobione 2026-10-14 02:10)*
- [-] **L14. Wojna hybrydowa ze źródeł** (pytanie autora przy X1): sprawdzić dostępność bazy incydentów cybernetycznych między państwami (np. DCID) albo innego źródła; jeśli brak — tylko LLM z prasy. *Porzucone: autor nie chce tych danych; zamiast tego nowa relacja `in war crisis` (A15, 2026-10-14).*

## Phase 1.2b — przegląd danych startowych przez LLM (później)

- [ ] **L15. Przegląd 111 par UCDP poziomu 1** — od A19 są w `in war crisis`, nie w `in war` (strony wspierające, np. NATO vs Serbia 1999): zostawić / usunąć zgodnie z opisem wzoru; po decyzji A19. *(dodane 2026-10-14 02:10)*

## GUI

- [x] **L16. Poprawki GUI po A16**: kolorowe ikony statusów, edytor jak w VS Code (Tab, listy, Ctrl+Enter), przełączanie pozycji przez `#`. *(zrobione: 2026-10-14 02:10, raport: raport-TODO-LLM.md)*
- [x] **L17. Widok grafu zadań** (2D, powiązania z numerów A/L/W… w tekstach). *(zrobione: 2026-10-14 02:22, raport: raport-TODO-LLM.md)*
- [x] **L18. Wątki w wymianie zdań** (prośba autora, T002): `talk/threads/`, drzewo w GUI, archiwum A1. *(zrobione: 2026-10-14 02:22, raport: raport-TODO-LLM.md)*
- [x] **L19. Opcja (b) dla wojen** (A19): `in war` = UCDP poziom 2, `in war crisis` = poziom 1; bezpieczny reset wartości startowych. *(zrobione: 2026-10-14 02:22, raport: raport-TODO-LLM.md)*
- [x] **L20. Wątki: odgałęzienia, zamykanie, wzmianki @** (@T002). *(zrobione: 2026-10-14 02:37, raport: raport-TODO-LLM.md)*
- [x] **L21. Briefing w GUI** (@T004) + obowiązek zapisu briefingu na koniec sesji. *(zrobione: 2026-10-14 02:37, raport: raport-TODO-LLM.md)*
- [x] **L22. GUI: instrukcja, okno przypięte, regulowane rozmiary, kontekst rodzica w odgałęzieniach, skróty CRE/MOD/DEL** (@T002, @T004, @T006). *(zrobione: 2026-10-14 03:24, raport: raport-TODO-LLM.md)*

## Phase 2.0 — runda 1

- [x] **L23. `AGENTS/phases/phase-2/agents-issues-1.md`** (U1–U5: skutki R1–R5) + wątek @T008 (szum, R5) + odpowiedzi @T005, @T007. *(zrobione: 2026-10-14 03:24, raport: raport-TODO-LLM.md)*
- [x] **L24. Plan implementacji Phase 2.1** po decyzjach @A12 (R6–S3), @A20, @A21, @A22. *(zrobione: 2026-10-14 04:14 — `AGENTS/phases/phase-2/design.md` v0 + @T009, @T010; raport: raport-TODO-LLM.md)*
- [x] **L25. Nowe wzory z decyzji Phase 2.0**: `state collapse` (S2), `economic dependence` (@T007). *(zrobione: 2026-10-14 04:14)*
- [x] **L26. GUI: poprawki po @T006 i @phase-2:U5** (zamykanie okna przypiętego, przyciski, bloki kodu w listach, numeracja list). *(zrobione: 2026-10-14 04:14, raport: raport-TODO-LLM.md)*

## Phase 1.2b (całość przed 2.1 — decyzja @A23)

- [-] **L27. Pilot 1.2b** — *porzucone 2026-10-14 05:13: autor wybrał całe 1.2b zamiast pilota (@A23); zastępuje L28–L29.*
- [x] **L28. Plan Phase 1.2b**: `AGENTS/phases/phase-1.2b/agents-issues-0.md` (P1–P5). *(zrobione: 2026-10-14 05:13)*
- [x] **L29. Przygotowanie 1.2b**: instrukcja dla agentów wypełniających (@L8), `confirm-default`, `missing --by-country`, kolejka zadań. *(zrobione 2026-10-14 06:22: `confirm-default`, `missing --by-country`, `queue.md` (196 państw); wcześniej: szkic instrukcji gotowy 2026-10-14 05:38; narzędzia czekają na @phase-1.2b:P1)*
- [x] **L30. Odpowiedzi na P1–P4**: wątki @T011, @T012; `phase-1.2b/instrukcja-wypelniania.md` (szkic); `phase-1.2b/agents-issues-1.md` (Q1–Q8). *(zrobione: 2026-10-14 05:38, raport: raport-TODO-LLM.md)*
- [?] **L31. Test modeli** (Haiku/Sonnet/Opus vs WGI, 10 krajów). *Czeka na @A27.*
- [x] **L32. Q1–Q8 we wzorach** (usunięte `immigration`/`emigration`, skale 0..100, `hybrid attacks towards`, `social`/`government revanchism`, nowe opisy, wartości startowe `happiness`) + `phase-1.2b/plan.md` + instrukcja dostosowana. *(zrobione: 2026-10-14 06:03, raport: raport-TODO-LLM.md)*
- [x] **L33. GUI po @T013**: przycisk Koniec (plik + prompt w schowku), odpowiedziane pozycje zostają do Konca, przycisk Plan, klikalne ścieżki. *(zrobione: 2026-10-14 06:03, raport: raport-TODO-LLM.md)*
- [x] **L35. GUI: przy zadaniu tylko jego część raportu** (@T014). *(zrobione: 2026-10-14 06:22)*
- [x] **L36. Wątki @T015 (opis testu modeli, A27) i @T016 (wycena z ograniczeniami: ~75–105 $ przez API).** *(zrobione: 2026-10-14 06:22)*
- [?] **L34. Uruchamianie agentów 1.2b (Haiku w Claude Code)** (kolejka → zadanie → batch → `validate` → `review`; pomiar zużycia tokenów). *Czeka na sygnał autora (@A32) — nie zaczynać wcześniej.*
- [x] **L37. Test Haiku** (@T015, @A27): 10 krajów × `stability`/`corruption` × 2 serie, porównanie z WGI. `corruption` błąd ~5, `stability` ~18 (różnica definicji). *(zrobione: 2026-10-14 06:34, raport: raport-TODO-LLM.md)*
- [x] **L38. `stability` → `stability` + `violence risk`** (@A30): nowa statystyka z wartościami startowymi WGI, `stability` wyczyszczone i z nowym opisem, `seeds.csv`, instrukcja i plan 1.2b. *(zrobione: 2026-10-14 06:43, raport: raport-TODO-LLM.md)*
- [x] **L39. `audit`** — automatyczne porównanie wszystkich krajów ze wskaźnikami (`simulator/audit.py`, reguły `audit.csv`, raport w `AGENTS/phases/phase-1.2b/audit/`). *(zrobione: 2026-10-14 06:50, raport: raport-TODO-LLM.md)*
