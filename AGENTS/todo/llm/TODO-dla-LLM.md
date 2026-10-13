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

- [ ] **L8. Instrukcja dla agentów wypełniających dane z prasy.** Ma zawierać:
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

- [ ] **L15. Przegląd 111 par UCDP poziomu 1** w `in war` (strony wspierające, np. NATO vs Serbia 1999): zostawić / usunąć zgodnie z opisem wzoru; po decyzji A19. *(dodane 2026-10-14 02:10)*

## GUI

- [x] **L16. Poprawki GUI po A16**: kolorowe ikony statusów, edytor jak w VS Code (Tab, listy, Ctrl+Enter), przełączanie pozycji przez `#`. *(zrobione: 2026-10-14 02:10, raport: raport-TODO-LLM.md)*
- [?] **L17. Widok grafu zadań** (2D, powiązania z numerów A/L/W… w tekstach). *Czeka na A18.*
