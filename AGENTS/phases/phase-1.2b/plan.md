# Phase 1.2b — Plan (wypełnienie wszystkich danych opisowych)

Jedno miejsce, które zbiera decyzje 1.2b i pokazuje, co dalej. Szczegóły: `agents-issues-0.md` (P1–P5), `agents-issues-1.md` (Q1–Q8), `instrukcja-wypelniania.md`, wątki @T011 i @T012.

*Aktualizuje agent; ostatnia zmiana: 2026-10-14 16:28 — Claude Opus 5.5*

---

## Cel

Przed Phase 2.1 wszystkie dane opisowe są uzupełnione (@A23):
- statystyki państw bez wartości domyślnej: wpisane dla każdego państwa i roku;
- relacje: wpisane dla istotnych partnerów, a dla reszty wartość domyślna potwierdzona przez agenta (P1, @T011).

## Ustalone

| Sprawa | Decyzja |
|---|---|
| P1 — co znaczy "uzupełnione" | lista istotnych partnerów + `confirm-default` dla reszty (@T011: "tak, może tak być") |
| P3 — instrukcja dla agentów | `instrukcja-wypelniania.md` — zaakceptowana (@A29) |
| P4 — uzasadnienia i źródła | można wyłączyć (tryb oszczędny), do ustalenia w instrukcji |
| P5 — UCDP poziom 1, nowe statystyki | zgoda |
| Q1 | `immigration`, `emigration` usunięte; zostaje `net migration` |
| Q2, Q3 | subordination i power w skali 0..100; `real subordination` = polityczna i militarna |
| Q4, Q6, Q7 | nowe opisy `social sensitivity`, `government popularity` (sondaże %), `happiness` (10 × Cantril, wartości startowe od 2011) |
| Q5 | `in hybrid war` → skierowana `hybrid attacks towards` |
| Q8 | `social revanchism` + nowa `government revanchism` |
| A30 (test Haiku) | `stability` rozdzielone: `stability` (instytucje, wypełnia LLM) + `violence risk` (z WGI, wartości startowe) |

## Otwarte

| Sprawa | Gdzie |
|---|---|
| P2 — model | Haiku w Claude Code (test @T015) — użyty; przegląd tylko próbki + `audit` dla wszystkich (@A31) |
| K1–K8 — poprawki po wypełnieniu | `agents-issues-2.md` (@A33) |

## Kroki

1. ✅ Zakres (P1–P5), definicje statystyk (Q1–Q8).
2. ✅ Instrukcja dla agentów (@A29).
3. ✅ Narzędzia (@L29):
   - `confirm-default`;
   - `missing --by-country`;
   - kolejka zadań `queue.md` (196 państw × zadanie A/B).
4. ✅ Model: **Haiku jako agenci Claude Code** (test: `AGENTS/phases/phase-1.2b/test-modeli.md`); start **na sygnał autora** (@T016).
4b. ✅ Uruchamianie agentów (@L34): koordynator w Claude Code, 20 agentów Haiku naraz.
5. ✅ Wypełnianie: wszystkie 392 zadania naraz (decyzja autora w czacie), skończone 2026-10-14 13:15; `missing` 100%. Raport: `AGENTS/phases/phase-1.2b/raport-wypelniania.md`.
5b. ⏳ Poprawki po wypełnieniu (`AGENTS/phases/phase-1.2b/plan-poprawek.md`): zrobione K3, K5, K6, K7 (31 państw usuniętych, zostało 165); K1, K2, K4 i pilot założeń czekają na wspólny start @A43 (`AGENTS/phases/phase-1.2b/poprawki/faza-edycji-danych.md`).
6. ⏳ Kontrola (A31):
   - ✅ automatyczny `audit` dla wszystkich krajów: `AGENTS/phases/phase-1.2b/audit/audit-2026-10-14-1312.md`;
   - ~~przegląd próbki~~ → `AGENTS/plan/future-work.md` (@phase-1.2b:K8);
   - potem `missing` = 100% → Phase 2.1.

## Statystyki do wypełnienia (po Q1–Q8)

- **Państwo, wszystkie lata:**
  - `violence risk`, `corruption`, `civilization level`, `happiness` — mają wartości startowe, do uzupełnienia luk;
  - `stability` (instytucje) — w całości LLM;
  - `social revanchism`, `government revanchism`, `government popularity`, `social sensitivity`, `assimilation`.
- **Państwo, tylko gdy coś się działo:** `war exhaustion`, `immigration crisis`, `riots`, `epidemic`, `mobilized`, `state collapse`; `net migration` (jest z danych).
- **Relacje skierowane** (istotni partnerzy): `diplomatic relation towards`, `social view towards`, `perceived/real subordination towards`, `perceived/real power towards`, `economic dependence`, `hybrid attacks towards`.
- **Relacje dwustronne:** `in war` i `in war crisis` (przegląd UCDP + rok 2025), `neighbours` (gotowe).
