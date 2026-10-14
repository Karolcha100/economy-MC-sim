# T005 · Co teraz robimy?

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Potrzebuję krótkiego raportu ze stanu prac, co teraz zostało zrobione i co będziemy robić.

*2026-10-14 02:32 — Autor*

---
---
---

**Stan prac — krótko**

**Zrobione:**
- **Narzędzia danych (Phase 1.0–1.1):**
  - pakiet `simulator/`: templates, wzory, dane opisowe z krzywymi zmian, historia, walidacja, CLI;
  - 65 testów.
- **Dane (scenariusz `world-1990-2025`):**
  - 196 państw (z Tajwanem), lata 1990–2025;
  - dane prawdziwe: PKB (luki uzupełnione, z logiem), stabilność i korupcja (WGI), HDI, CPI, szczęście, migracja netto, odsetek migrantów, populacja;
  - pary krajów: granice, konflikty (UCDP).
- **Phase 1.2a:** wartości startowe danych opisowych z tych wskaźników: `stability`, `corruption`, `civilization level`, `net migration`, `in war`, `in war crisis`, `neighbours`.
- **Współpraca:**
  - porządek w `AGENTS/`;
  - GUI `agents_board`: drzewa, wątki z odgałęzieniami, graf, wzmianki @, briefing.

**Teraz — czeka na Ciebie (Phase 2.0, planowanie silnika regresji):**
- @A11 — Twój pomysł na Phase 2 (`phases/phase-2/agents-instructions.md`);
- @A12 — 12 decyzji, najważniejsze @phase-2:R1 (jeden model dla wszystkich krajów?), @phase-2:R2 (realny wzrost zamiast PKB w USD?), @phase-2:R3 (horyzont i liczba scenariuszy).

**Potem (plan w `AGENTS/plan/phases-plans.md`):**
1. **Phase 2.1** — szkielet silnika na danych prawdziwych: trening → scenariusze Monte Carlo → prawdopodobieństwa zdarzeń.
2. **Phase 1.2b** — LLM-y z wyszukiwarką wypełniają dane opisowe (np. `revanchism`, `social view towards`), w kolejności ważności zmiennych z 2.1.
3. **Phase 2.2** — pełny model: dane opisowe, zdarzenia dyskretne, relacje, backtest.

Drobiazgi bez pośpiechu: @A4–@A9, @A17.

*2026-10-14 02:37 — Claude Opus 5.5*

---
---
---

Co sądzisz o tym aby przed Phase 2.0, zrobić jeszcze Phase 1.2b?

*2026-10-14 02:52 — Autor*

---
---
---

**Phase 1.2b przed Phase 2.0? — moje zdanie: 2.0 dokończyć (to już niewiele), a 1.2b zrobić przed 2.1, nie przed 2.0.**

- **Phase 2.0 to planowanie:** Twoje decyzje i moje pytania, bez kodu i bez danych. R1–R5 już są; zostały R6–S3 i nowa runda @phase-2:U1–@phase-2:U5. To kilka godzin Twojej pracy, a ustala, *jakich danych opisowych silnik potrzebuje*.
- **Twoja decyzja R2 zmienia moje wcześniejsze założenie:** silnik ma przewidywać *wszystkie* dane państwa, także opisowe i relacje. Do nauki potrzebuje więc tych danych *już* przy budowie szkieletu (2.1). Dlatego 1.2b nie może czekać na koniec 2.1, jak proponowałem wcześniej.
- **Propozycja kolejności:**
  1. **2.0** — dokończyć decyzje (@A12, @A20);
  2. **1.2b-pilot** — LLM-y z wyszukiwarką wypełniają kilka kluczowych statystyk opisowych (np. `revanchism`, `war exhaustion`, `government popularity`, `social view towards`, `diplomatic relation towards`) dla krajów Tier 1 (~25), za lata 1990–2025. Przy okazji sprawdzamy, czy proces wypełniania działa i ile kosztuje;
  3. **2.1** — szkielet silnika uczony na danych prawdziwych + pilocie;
  4. **1.2b-reszta** — pozostałe kraje i statystyki, w kolejności tego, co okaże się ważne w 2.1;
  5. **2.2** — pełny model.

Jeśli się zgadzasz, poprawię plan w `AGENTS/plan/phases-plans.md` (@A22).

*2026-10-14 03:24 — Claude Opus 5.5*

---
---
---

Zgadzam się

*2026-10-14 03:29 — Autor*

---
---
---

Dziękuję. Plan zmieniony w `AGENTS/plan/phases-plans.md`: **2.0 (dokończyć) → 1.2b-pilot → 2.1 → 1.2b-reszta → 2.2.** Phase 2.0 jest prawie gotowa: projekt silnika w `AGENTS/phases/phase-2/design.md`, otwarte już tylko @A23 i @A24.

*2026-10-14 04:11 — Claude Opus 5.5*

---
---
---
