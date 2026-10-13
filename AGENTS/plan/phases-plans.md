# Plan faz — proponowana kolejność

*Aktualizują agenci po każdej zmianie planu (z datą). Opis zakresu faz: `phases-description.md`. Ostatnia zmiana: 2026-10-14 02:10 — Claude Opus 5.5*

Legenda: ✅ zrobione · ⏳ następne / w toku · ⏸ czeka · 💤 później

---

## Kolejność w skrócie

| # | Faza | Status | Jednym zdaniem |
|---|---|---|---|
| 1 | **Phase 1.0** — planowanie danych | ✅ | Pytania i decyzje: `AGENTS/phases/phase-1/agents-issues-1…4.md`. |
| 2 | **Phase 1.1** — narzędzia danych | ✅ | `simulator/`: templates, wzory, dane opisowe, historia, walidacja; 47 testów. |
| 3 | **Phase 1.2a** — prawdziwe wskaźniki | ✅ | Wskaźniki w `history/`, wartości startowe w `narrated/` (`seeds.csv`). Otwarte drobiazgi: A17, A19. |
| 4 | **Phase 2.0** — planowanie regresji | ⏳ następne | A11 (pomysł autora), A12 (decyzje w `AGENTS/phases/phase-2/agents-issues-0.md`). |
| 5 | **Phase 2.1** — szkielet silnika | 💤 | Trening → scenariusze Monte Carlo → prawdopodobieństwa; najpierw na danych prawdziwych. |
| 6 | **Phase 1.2b** — dane opisowe z prasy | 💤 | LLM-y z wyszukiwarką, w kolejności ważności zmiennych z Phase 2.1. |
| 7 | **Phase 2.2** — pełny model | 💤 | Statystyki opisowe w modelu, zdarzenia dyskretne, relacje; backtest. |
| — | Porządek w `AGENTS/` + GUI `agents_board` | ✅ | `AGENTS/README.md`; `python -m agents_board` (podgląd + odpowiadanie). |
| — | Później | 💤 | `future-work.md`: GUI do edycji danych, dynamiczne organizacje, LFS/Parquet. |

---

## Dlaczego taka kolejność (krótko)

- **1.2a przed 2.1:** regresja potrzebuje zmiennych. Bez wskaźników ma tylko PKB. Import wskaźników to jedna sesja agenta, a dane od razu przydają się w obu miejscach: jako zmienne regresji i jako wartości startowe danych opisowych.
- **2.0 po 1.2a:** autor woli jeden cel naraz (2026-10-14); pytania do Phase 2 czekają gotowe.
- **1.2b po 2.1:** wypełnienie danych opisowych to miliony komórek i duży koszt pracy LLM. Działający szkielet silnika pokaże, które statystyki naprawdę wpływają na wynik, i te wypełnimy najpierw.
- **2.2 na końcu:** pełny model ma sens dopiero wtedy, gdy są dane opisowe i backtest pokazał, że prosty model działa.

## Dłuższe wyjaśnienia

- Phase 1.2a, czyli co i dlaczego: `AGENTS/phases/phase-1.2a/M1-wskazniki.md`.
- Phase 2, uzasadnienie kolejności i główne ryzyka: `AGENTS/talk/wymiana-zdan-A1.md`, wpis "Re: Czy wciąż Phase-1?".
- Pytania Phase 2.0: `AGENTS/phases/phase-2/agents-issues-0.md`.
- Bieżące zadania: `AGENTS/todo/author/` (autor, `A…`), `AGENTS/todo/llm/` (agenci, `L…`).
