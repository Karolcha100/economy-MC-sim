# ŚREDNIE — TODO dla autora

Ważne, ale nie blokują agentów.

*Utworzone: 2026-10-13 23:29 — Claude Opus 5.5*

---

- [ ] **Przejrzeć opisy statystyk** (`agents-issues-3.md` L1), kolumna `description` w `simulator/scenarios/world-1990-2025/formulas/*.csv`. Najmniej pewne:
  - `social sensitivity`;
  - `civilization level`;
  - `immigration` / `emigration`;
  - ujemna połowa skali przy `perceived/real subordination towards` i `perceived/real power towards`;
  - czy `in hybrid war` ma być relacją dwustronną;
  - czy `neighbours` liczy tylko granicę lądową.

  Edycja: bezpośrednio w CSV albo `python -m simulator formulas edit --kind ... --name ... --description "..."`.
- [ ] **Przejrzeć przeliczenia skal wskaźników** (np. HDI → `civilization level`), gdy agent je zaproponuje w Phase 1.2a.
- [ ] **Obejrzeć kraje referencyjne na mapie**, gdy pojawią się pierwsze wartości: `python -m simulator --scenario world-1990-2025 reference-map --kind grade --name stability`.
