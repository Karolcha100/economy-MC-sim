# Phase 1.2b — K3. Wpisy na 2025 — zrobione częściowo

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K3 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A36; wykonanie: @L43. Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022; „Co masz zrobić” i koszty: 2026-10-14 15:59)*

---

## Co masz zrobić

**Pytanie:** czy zgadzasz się z moją oceną 41 par państw, które agenci oznaczyli jako będące w wojnie albo w kryzysie wojennym w 2025?

- Agenci wpisali je pojedynczo i niespójnie. Przejrzałem wszystkie i przy każdej proponuję: **zostaw**, **zmień** (`in war` → `in war crisis`) albo **usuń**.
- Ty: przeczytaj tabele niżej i odpisz „zgoda” albo wypisz pary, które oceniasz inaczej (np. „ARM–AZE zostaw”).
- Po Twojej odpowiedzi zapiszę zmiany jednym plikiem i zamknę zadanie.

---

## Szczegóły

**Zapisane** (zgoda): `AGENTS/phases/phase-1.2b/batches-koordynator/K3-2025.json`. USA–YEM, GBR–YEM, ISR–PSE i KHM–THA 2025 przeniesione z `in war` do `in war crisis`. ISR–YEM i PRK–UKR już były `in war crisis`. `validate`: 0 błędów.

**Lista pozostałych par na 2025** do Twojego przeglądu: zostaw / zmień / usuń. Bez Twojej odpowiedzi nic nie zmieniam.

`in war` (6):

| Para | Obecnie | Rekomendacja |
|---|---|---|
| RUS–UKR | `in war` | zostaw |
| COD–RWA | `in war` + `in war crisis` | zostaw `in war`, zdejmij `in war crisis` (reguła K1) |
| IRN–ISR | `in war` | zostaw (wojna 12-dniowa, VI 2025) |
| IRN–USA | `in war` | → `in war crisis` (jednorazowe uderzenia i odwet, bez wojny) |
| IND–PAK | `in war` | → `in war crisis` (4 dni, V 2025, poniżej progu 1000 zabitych) |
| AFG–PAK | `in war` | → `in war crisis` (walki graniczne X 2025, zawieszenie broni) |

`in war crisis` (35, po K3):
- **zostaw (26):** AFG–TJK, CHN–PHL, CHN–TWN, DZA–MLI, ERI–ETH, EST–RUS, GBR–YEM, GUY–VEN, IRN–QAT, ISR–LBN, ISR–PSE, ISR–QAT, ISR–SYR, ISR–YEM, KHM–THA, KOR–PRK, LBN–SYR, POL–RUS, PRK–UKR, ROU–RUS, RWA–TZA, RWA–ZAF, SAU–YEM, SDN–SSD, USA–VEN, USA–YEM;
- **usuń (7):**
  - ARM–AZE: porozumienie pokojowe VIII 2025, bez starć;
  - CHN–IND: odprężenie w 2025;
  - COL–PER: spór o wyspę bez użycia siły;
  - LBY–SDN: słabe źródła;
  - RWA–ZWE: ZWE nie walczyło w misji SAMIDRC;
  - BDI–RWA: zamknięta granica, bez starć w 2025;
  - ARE–SDN: oskarżenia, bez bezpośredniego starcia;
- **do decyzji (1):** ARE–YEM. W XII 2025 Arabia Saudyjska uderzyła na transport ZEA w Mukalli; ZEA jest sojusznikiem rządu YEM, więc to konflikt ZEA–SAU, a nie ZEA–YEM.
- **brakuje (1):** TTO–VEN. Rekomendacja: nie dopisywać (spór dyplomatyczny i gazowy).
