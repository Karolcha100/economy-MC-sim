# Phase 1.2b — K1. Import UCDP: strony drugorzędne, `in war` a `in war crisis`

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K1 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A34; wykonanie: @L41. Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022; „Co masz zrobić” i koszty: 2026-10-14 15:59)*

---

## Co masz zrobić

**Pytanie:** czy zgadzasz się na regułę i sposób poprawy danych o wojnach z UCDP (niżej) — i kto ma zrobić przegląd par: Haiku czy Opus?

- **Problem w skrócie:** import z bazy UCDP łączy w pary każde państwo z każdym po obu stronach konfliktu, także państwa, które tylko wysłały żołnierzy misji pokojowej. Dlatego np. Indonezja „była w kryzysie wojennym” z Rwandą.
- **Do decyzji:** (1) reguła: `in war` = wojna międzypaństwowa z ≥ 1000 zabitych w roku; reszta = `in war crisis`; pary samych „pomocników” usuwamy po przeglądzie; (2) wykonawca przeglądu ok. 120 par (warianty w sekcji „Kto i za ile” na końcu).
- Wystarczy odpowiedź: „zgoda + wariant H3” albo Twoja poprawka.

## Kto i za ile (odpowiedź na „czemu nie Haiku?”)

Można Haiku — pod warunkiem, że **jeden** agent przegląda całą tabelę według jednej reguły (nie agenci krajowi, bo to oni dali niespójności). Kod importu (kategorie par) piszę ja, bo to programowanie, nie ocena.

| Wariant | Kto ocenia ok. 120 par | Koszt API | Ryzyko |
|---|---|---|---|
| O | Opus | ok. 1,5 $ | najmniejsze |
| H1 | 1 agent Haiku | ok. 0,05 $ | pojedyncze pomyłki przy mniej znanych konfliktach |
| **H3 (rekomendacja)** | 3 niezależne przebiegi Haiku, decyduje większość; tylko pary, w których się różnią, sprawdzam ja (Opus) | ok. 0,15 $ + ok. 0,3 $ | małe |

---

## Szczegóły

**Co się dzieje.**
- Import (`simulator/sources.py`, `read_ucdp_dyadic`) tworzy parę z **każdego** państwa po stronie A (główne + drugorzędne) z **każdym** po stronie B.
- Poziom 2 = obie strony główne w wojnie międzypaństwowej, trafia do `in war`. Poziom 1 = wszystko inne, trafia do `in war crisis`.
- Od 1990 jest 303 par-lat:

| Kategoria | Pary-lata | Przykłady |
|---|---|---|
| obie strony główne (PP) | 52 | ERI–ETH 1998–2000, IND–PAK, KGZ–TJK 2021–22 |
| główna × drugorzędna (PS) | 186 (89 par) | RUS–UKR 2014–21 (słusznie), IRQ × 27 państw koalicji 1991, SRB × państwa NATO 1999 |
| drugorzędna × drugorzędna (SS) | 65 | RWA × IDN/NPL/BGD (MONUSCO), RUS–TUR i IRN–TUR 2020–24 (Syria/Libia), ale też AGO/NAM/ZWE × RWA/UGA 1998–2001 (prawdziwe walki) |

**Plan.**
1. **Kod:** import zapisuje kategorię pary (PP/PS/SS) i intensywność UCDP (1 = 25–999 zabitych, 2 = ≥ 1000) do `history/dyadic/ucdp-armed-conflict.csv`. Test w `tests/test_sources.py`.
2. **Reguła (do zatwierdzenia):**
   - `in war` = PP w wojnie międzypaństwowej z intensywnością 2, albo PS z intensywnością 2, jeśli państwo drugorzędne walczyło regularną armią (lista do przeglądu, np. koalicja 1991, NATO 1999);
   - `in war crisis` = pozostałe PP i PS, SS tylko po przeglądzie;
   - `in war` wyklucza `in war crisis` w tej samej parze i roku.
3. **Tabela przeglądu:** `AGENTS/phases/phase-1.2b/ucdp-przeglad.csv` ze wszystkimi 303 parami-latami. Każdy wiersz: kategoria, intensywność, obecna wartość, proponowana wartość, krótkie uzasadnienie. Pary PS i SS (ok. 120 par) przegląda Opus.
4. **Ty** przeglądasz tabelę, wystarczy zerknąć na kolumnę „zmiana”.
5. **Zapis:** jeden batch koordynatora `AGENTS/phases/phase-1.2b/batches-koordynator/K1-ucdp.json`, nadpisujący `in war` / `in war crisis` w latach 1990–2024 dla par z tabeli. Potem skrypt zeruje `in war crisis` tam, gdzie `in war` = 1 (dziś np. COD–RWA 2025). Na końcu `validate`, `review`, `audit`.

**Koszt:**
- kod i test: ~1 h pracy Opus (mało tokenów);
- przegląd ok. 120 par: jedna sesja Opus, ~150–250 tys. tokenów, bez wyszukiwarki, bo to znane wojny;
- alternatywy: tabela „Kto i za ile” na górze (rekomendacja: 3 × Haiku z głosowaniem).

---

## Jak liczę koszt

- Ceny API (z @T012): Haiku 5.5 — 0,10 $ / 0,50 $ za 1 mln tokenów (wejście / wyjście), Sonnet 5.5 — 2 $ / 10 $, Opus 5.5 — 4 $ / 20 $. **Haiku jest ok. 20× tańszy od Sonnet i 40× od Opus**; Opus jest 2× droższy od Sonnet. (Wcześniej napisałem tu błędnie „Opus ≈ 5× Sonnet” — poprawione.)
- W Claude Code (subskrypcja) te same tokeny zużywają limit okresowy; przez API — miesięczny limit wydatków.
- Wyszukiwarka (WebSearch) kosztuje dodatkowo ok. 0,01 $ za wyszukiwanie.
