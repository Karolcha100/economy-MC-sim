# Phase 1.2b — K4. Konwencje flag państwa

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K4 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A40; wykonanie: @L44. Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022; „Co masz zrobić” i koszty: 2026-10-14 15:59)*

---

## Co masz zrobić

**Pytanie:** czy zgadzasz się na wspólne zasady ustawiania 5 flag (epidemia, kryzys migracyjny, zamieszki, upadek państwa, mobilizacja) i na to, żeby poprawki zrobił Haiku?

- Agenci ustawiali flagi każdy po swojemu (np. Niemcy mają kryzys migracyjny w 2015, a Finlandia nie; COVID raz tylko 2020, raz 2020–2021).
- Ty: „zgoda” albo popraw konkretną zasadę.

## Kto i za ile (odpowiedź na „rozważ Haiku”)

Tak, tu Haiku pasuje dobrze: skrypt sam wyznacza kandydatów (np. państwa z napływem ≥ 0,5% ludności), a model tylko sprawdza listę według jednej zasady.

| Wariant | Kto | Koszt API |
|---|---|---|
| **Haiku (rekomendacja)** | po jednym agencie na flagę (5), każdy z całą listą kandydatów i jedną zasadą; ja sprawdzam przypadki graniczne | ok. 0,1 $ + ok. 0,3 $ |
| Opus | wszystko ja | ok. 1–2 $ |

---

## Szczegóły

**Stan dziś:**
- `epidemic`: 2020 = 192 z 196 państw, 2021 = 129 z 196; 33 wpisy w innych latach (Ebola, cholera, SARS, COVID w CHN 2022–23 itd.);
- `immigration crisis`: 36 wpisów, np. 2015 DEU, SWE, AUT, GRC, HUN, SVN, LBN, MKD; 2021 USA, LTU;
- `riots`: 233, `mobilized`: 139, `state collapse`: 37.

**Konwencje (zgoda):**
- **`epidemic`:**
  - COVID: 2020 i 2021 dla wszystkich państw, czyli +4 w 2020 i +67 w 2021;
  - inne epidemie: z nadumieralnością albo stanem wyjątkowym;
  - zostają: Ebola GIN/SLE/LBR 2014–15 i COD; cholera YEM, HTI, ZWE, SDN, AGO; SARS CHN/TWN 2003; COVID CHN 2022–23;
  - do sprawdzenia: CUB 2025, WSM 2019 (odra), MDG 2017 (dżuma);
  - HIV nie.
- **`immigration crisis`:** napływ ≥ 0,5% ludności w roku (≈ `net migration` ≥ 25 na naszej skali) albo stan wyjątkowy na granicy. Kandydaci wyznaczeni skryptem:
  - z `net migration`: np. POL, CZE, MDA, SVK 2022; TUR 2012–16; JOR 2013–15; COL 2018–19;
  - ze stanu wyjątkowego: LTU, LVA, POL 2021; HUN, HRV, MKD 2015.
- **`riots`:** przemoc z ofiarami śmiertelnymi albo godzina policyjna lub stan wyjątkowy w stolicy.
- **`state collapse`:** rząd traci kontrolę nad stolicą albo większością terytorium.
- **`mobilized`:** formalna mobilizacja albo pobór na wojnę. Do dopisania ERI 2020–22; PRK 2024–25 nie (wysłanie wojsk to nie mobilizacja).

**Co zrobię:**
1. Skrypt (poza projektem) wypisze kandydatów dla każdej konwencji do tabeli `AGENTS/phases/phase-1.2b/k4-flagi.csv`: państwo, rok, flaga, obecnie, proponowane, powód.
2. Graniczne przypadki z raportu rozstrzygam według definicji, a każdy wpis dostaje jedno zdanie uzasadnienia. Dotyczy to `riots`/`state collapse`: KGZ 2002/2010, NER 2023, COG 1993–97, SLB 2000, TLS 2025, MNE 2019–20, GNB 1998–99.
3. Ty zatwierdzasz tabelę, potem zapis jednym batchem `K4-flagi.json`.

**Koszt:** patrz „Kto i za ile” na górze (Haiku ok. 0,1 $ + moja kontrola ok. 0,3 $; Opus sam ok. 1–2 $).

---

## Jak liczę koszt

- Ceny API (z @T012): Haiku 5.5 — 0,10 $ / 0,50 $ za 1 mln tokenów (wejście / wyjście), Sonnet 5.5 — 2 $ / 10 $, Opus 5.5 — 4 $ / 20 $. **Haiku jest ok. 20× tańszy od Sonnet i 40× od Opus**; Opus jest 2× droższy od Sonnet. (Wcześniej napisałem tu błędnie „Opus ≈ 5× Sonnet” — poprawione.)
- W Claude Code (subskrypcja) te same tokeny zużywają limit okresowy; przez API — miesięczny limit wydatków.
- Wyszukiwarka (WebSearch) kosztuje dodatkowo ok. 0,01 $ za wyszukiwanie.
