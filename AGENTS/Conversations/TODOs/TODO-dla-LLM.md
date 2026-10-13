# TODO dla agentów LLM

Zadania dla agentów (także dla mnie w kolejnych sesjach). Kto bierze zadanie, dopisuje przy nim `[w toku: model, data]`, a po skończeniu oznacza `[x]` z datą.

*Utworzone: 2026-10-13 23:29 — Claude Opus 5.5*

---

## Phase 1.2a — prawdziwe wskaźniki (czeka na decyzję autora o kolejności; szczegóły: `Conversations/M1-wskazniki.md`)
- [ ] Import do `history/` (z metadanymi i sprawdzeniem licencji):
  - WGI Political Stability i Control of Corruption;
  - HDI;
  - UN DESA migrant stock + WB net migration;
  - UCDP dyadic;
  - Correlates of War Direct Contiguity;
  - World Happiness Report.
- [ ] Konwertery formatów, których `history import` jeszcze nie zna (HDI, UCDP, CoW, WHR). Relacje UCDP i CoW są parami krajów, więc potrzebny jest format "dyadyczny" (osobny katalog w `history/`).
- [ ] Skrypt "seed": wskaźnik → skala wzoru → `narrated/` z `author=seed:<źródło>`. Każde przeliczenie skali opisać i dać autorowi do przejrzenia.
- [ ] Kolumna `sources` w operacjach (`set`/`batch`) i w `narrated/changelog.csv` (decyzja M1).
- [ ] `review`: ostrzeżenie, gdy wartość odbiega od seeda o więcej niż X.
- [ ] Po pobraniu przez autora pliku ONZ (`data/un/gdp-current-usd.xlsx`): konwerter UNSD AMA i `history fill` dla PRK.

## Phase 2.0 — planowanie silnika regresji
- [ ] `AGENTS/phase-2/agents-issues-1.md`: niejasności do rozstrzygnięcia przez autora:
  - model panelowy czy osobny dla każdego kraju;
  - co przewidujemy;
  - zdarzenia dyskretne;
  - skala szumu Monte Carlo;
  - backtest;
  - podwójne liczenie wskaźników i danych z nich wyliczonych.

## Phase 1.2b — wypełnianie z prasy (później, według priorytetów z Phase 2)
- [ ] Instrukcja dla agentów wypełniających: zasady źródeł (język lokalny dla Tier 1, media państwowe = oficjalna postawa, nie nastroje), kotwice, format batch, `--dry-run` → `validate` → `review`.
