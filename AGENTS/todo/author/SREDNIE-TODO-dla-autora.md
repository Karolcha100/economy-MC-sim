# ŚREDNIE — TODO dla autora

Ważne, ale nie blokują agentów. Zasady: `INSTRUKCJA.md`.

*Utworzone: 2026-10-13 23:29, numeracja dodana 2026-10-14 00:20 — Claude Opus 5.5*

---

- [ ] **A4. Przejrzeć opisy statystyk** (`agents-issues-3.md` L1): kolumna `description` w `simulator/scenarios/world-1990-2025/formulas/*.csv`. Najmniej pewne:
  - `social sensitivity`;
  - `civilization level`;
  - `immigration` / `emigration`;
  - ujemna połowa skali przy `perceived/real subordination towards` i `perceived/real power towards`;
  - czy `in hybrid war` ma być relacją dwustronną;
  - czy `neighbours` liczy tylko granicę lądową.

  Edycja: bezpośrednio w CSV albo `python -m simulator formulas edit --kind ... --name ... --description "..."`.
- [ ] **A5. Przejrzeć przeliczenia skal wskaźników** (np. HDI → `civilization level`), gdy agent je zaproponuje w Phase 1.2a.
- [ ] **A6. Obejrzeć kraje referencyjne na mapie**, gdy pojawią się pierwsze wartości: `python -m simulator --scenario world-1990-2025 reference-map --kind grade --name stability`.
- [ ] **A11. Opisać pomysł na Phase 2** w `AGENTS/phases/phase-2/agents-instructions.md`. *(przeniesione z WAŻNE 2026-10-14: autor odkłada, jeden cel naraz)*
- [x] **A12. Odpowiedzieć na `AGENTS/phases/phase-2/agents-issues-0.md`** (pola **Decyzja**). *(przeniesione z WAŻNE 2026-10-14 razem z A11; 2026-10-14 03:24: R1–R5 odpowiedziane, zostały R6–R9, S1–S3; 2026-10-14 04:14: wszystkie odpowiedziane)*
- [ ] **A17. Przejrzeć ręczne granice historyczne**: `data/manual/historical-land-borders.csv` (15 par: ZSRR, Czechosłowacja, Jugosławia, Sudan przed 2011), każda z notatką. *(dodane 2026-10-14 02:10)*
- [x] **A19. `in war` a `in war crisis` z UCDP**: zostawić `in war` = poziomy 1 i 2 UCDP (obecnie), czy poziom 1 (strona wspierająca, np. RUS–UKR 2014–2021) przenieść do `in war crisis`? Opis w `AGENTS/talk/wymiana-zdan-A1.md`. *(dodane 2026-10-14 02:10; odpowiedź: opcja (b) — zrobione 2026-10-14 02:22, wątek T003)*
