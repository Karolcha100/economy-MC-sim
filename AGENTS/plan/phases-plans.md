# Plan faz — proponowana kolejność

*Aktualizują agenci po każdej zmianie planu (z datą). Opis zakresu faz: `phases-description.md`. Ostatnia zmiana: 2026-10-14 04:14 — Claude Opus 5.5*

Legenda: ✅ zrobione · ⏳ następne / w toku · ⏸ czeka · 💤 później

---

## Kolejność w skrócie

| # | Faza | Status | Jednym zdaniem |
|---|---|---|---|
| 1 | **Phase 1.0** — planowanie danych | ✅ | Pytania i decyzje: `AGENTS/phases/phase-1/agents-issues-1…4.md`. |
| 2 | **Phase 1.1** — narzędzia danych | ✅ | `simulator/`: templates, wzory, dane opisowe, historia, walidacja. |
| 3 | **Phase 1.2a** — prawdziwe wskaźniki | ✅ | Wskaźniki w `history/`, wartości startowe w `narrated/` (`seeds.csv`). Otwarty drobiazg: A17. |
| 4 | **Phase 2.0** — projekt silnika | ⏳ prawie gotowe | `AGENTS/phases/phase-2/design.md`; czekają A23 (@T009), A24 (@T010), A25 (zatwierdzenie). |
| 5 | **Phase 1.2b-pilot** — dane opisowe z prasy (Tier 1) | ⏸ po A25 | LLM-y z wyszukiwarką: ~25 krajów, kluczowe statystyki opisowe i relacje (w tym `economic dependence`). |
| 6 | **Phase 2.1** — szkielet silnika | 💤 | Dwie regresje, dwie tury, drzewo scenariuszy; uczony na danych prawdziwych + pilocie. |
| 7 | **Phase 1.2b** — reszta danych opisowych | 💤 | Pozostałe kraje i statystyki, w kolejności ważności z 2.1. |
| 8 | **Phase 2.2** — pełny model | 💤 | Wszystkie dane, backtest, kalibracja; potem narzędzia analizy scenariuszy. |
| — | Porządek w `AGENTS/` + GUI `agents_board` | ✅ | Podgląd, odpowiadanie, wątki, graf, wzmianki @, briefing, okno przypięte. |
| — | Później | 💤 | `future-work.md`: GUI do edycji danych, dynamiczne organizacje, LFS/Parquet. |

---|---|---|---|
| 1 | **Phase 1.0** — planowanie danych | ✅ | Pytania i decyzje: `AGENTS/phases/phase-1/agents-issues-1…4.md`. |
| 2 | **Phase 1.1** — narzędzia danych | ✅ | `simulator/`: templates, wzory, dane opisowe, historia, walidacja; 47 testów. |
| 3 | **Phase 1.2a** — prawdziwe wskaźniki | ✅ | Wskaźniki w `history/`, wartości startowe w `narrated/` (`seeds.csv`). Otwarty drobiazg: A17. |
| 4 | **Phase 2.0** — planowanie regresji | ⏳ w toku | R1–R5 rozstrzygnięte; czekają R6–S3 (A12), U1–U5 (A20), szum (A21), kolejność 1.2b (A22). |
| 5 | **Phase 2.1** — szkielet silnika | 💤 | Trening → scenariusze Monte Carlo → prawdopodobieństwa; najpierw na danych prawdziwych. |
| 6 | **Phase 1.2b** — dane opisowe z prasy | 💤 | LLM-y z wyszukiwarką, w kolejności ważności zmiennych z Phase 2.1. |
| 7 | **Phase 2.2** — pełny model | 💤 | Statystyki opisowe w modelu, zdarzenia dyskretne, relacje; backtest. |
| — | Porządek w `AGENTS/` + GUI `agents_board` | ✅ | `AGENTS/README.md`; `python -m agents_board` (podgląd, odpowiadanie, wątki z odgałęzieniami, graf, wzmianki @, briefing). |
| — | Później | 💤 | `future-work.md`: GUI do edycji danych, dynamiczne organizacje, LFS/Parquet. |

---

## Dlaczego taka kolejność (krótko)

- **1.2a przed 2.1:** regresja potrzebuje zmiennych. Bez wskaźników ma tylko PKB. Import wskaźników to jedna sesja agenta, a dane od razu przydają się w obu miejscach: jako zmienne regresji i jako wartości startowe danych opisowych.
- **Pilot 1.2b przed 2.1** (autor, @A22): silnik przewiduje też dane opisowe i relacje (R2), więc potrzebuje ich do nauki już w szkielecie.
- **Reszta 1.2b po 2.1:** wypełnienie wszystkiego to miliony komórek; szkielet silnika pokaże, które statystyki są najważniejsze.
- **2.2 na końcu:** pełny model ma sens dopiero wtedy, gdy są dane opisowe i backtest pokazał, że prosty model działa.

## Dłuższe wyjaśnienia

- Phase 1.2a, czyli co i dlaczego: `AGENTS/phases/phase-1.2a/M1-wskazniki.md`.
- Phase 2, uzasadnienie kolejności i główne ryzyka: `AGENTS/talk/wymiana-zdan-A1.md`, wpis "Re: Czy wciąż Phase-1?".
- Phase 2.0: projekt `AGENTS/phases/phase-2/design.md`, pytania `AGENTS/phases/phase-2/agents-issues-0.md` i `-1.md`.
- Bieżące zadania: `AGENTS/todo/author/` (autor, `A…`), `AGENTS/todo/llm/` (agenci, `L…`).
