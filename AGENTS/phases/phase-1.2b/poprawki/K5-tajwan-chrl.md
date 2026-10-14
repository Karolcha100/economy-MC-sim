# Phase 1.2b — K5. Tajwan i ChRL — co znaczy „jednym batchem”

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K5 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A37; wykonanie: @L45. Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022; „Co masz zrobić” i koszty: 2026-10-14 15:59)*

---

## Co masz zrobić

**Problem:** część agentów źle wpisała, w których latach małe państwa uznawały Tajwan, a w których Chiny. Przykład: Kiribati ma odwrotnie — w danych uznaje Tajwan do 2003, a naprawdę było odwrotnie (Chiny do 2003, Tajwan 2003–2019). Do tego agenci różnie wpisywali relację po zerwaniu stosunków: od −100 do 0.

**Decyzje (dwie):**
1. **Czy poprawić to automatycznie** — skrypt z tabeli dat (niżej) ustawi relacje dyplomatyczne tych państw z Tajwanem i Chinami we wszystkich latach? (tak / nie)
2. **Jaka wartość po zerwaniu stosunków:** −30 (moja propozycja: chłodno, ale bez wrogości), czy inna?

Wystarczy: „tak, −30”.

---

## Szczegóły

**Batch** to jeden plik JSON z listą operacji, zapisywany komendą `python -m simulator batch`:
- **wszystko albo nic:** jeśli jedna operacja jest błędna, nic nie zostaje zapisane;
- każda zmiana trafia do `narrated/changelog.csv` z autorem i uzasadnieniem, więc da się ją prześledzić i cofnąć;
- przed zapisem robię `--dry-run`, który pokazuje tabelę zmian bez zapisu;
- „jednym batchem” znaczy: wszystkie poprawki Tajwanu i ChRL w jednym pliku `K5-twn-chn.json`, przygotowanym skryptem z tabeli dat uznania, zamiast ręcznych zmian w wielu miejscach.

**Tabela dat uznania** (z mojej wiedzy; przed zapisem sprawdzę wyszukiwarką te, których nie jestem pewien):

| Państwo | Uznawało ROC (Tajwan) | Uwagi |
|---|---|---|
| BLZ, GTM, HTI, PRY, KNA, VCT, SWZ, TUV, MHL (od 1998), PLW (od 1999) | do 2025 | |
| LCA | 1990–96, 2007–25 | ChRL 1997–2006 |
| NRU | 1990–2001, 2005–23 | ChRL 2002–04 i od 2024 |
| KIR | 2003–19 | ChRL do 2002 i od 2019 |
| SLB | 1990–2019 | |
| GMB | 1995–2013 | ChRL od 2016 |
| STP | 1997–2016 | |
| BFA | 1994–2018 | |
| SEN | 1996–2005 | |
| TCD | 1997–2006 | |
| LBR | 1990–93, 1997–2003 | |
| NER | 1992–96 | |
| CAF | 1991–98 | |
| GNB | 1990–98 | |
| LSO | 1990–94 | |
| BHS | 1990–97 | |
| ZAF | 1990–97 | |
| MWI | 1990–2007 | |
| GRD | 1990–2004 | |
| DMA | 1990–2003 | |
| TON | 1990–98 | |
| MKD | 1999–2001 | |
| NIC | 1990–2021 | |
| CRI | 1990–2007 | |
| PAN | 1990–2017 | |
| DOM | 1990–2018 | |
| SLV | 1990–2018 | |
| HND | 1990–2023 | |
| FSM | — | ChRL od 1989; błąd w FSM-B |

**Reguła (zgoda):**
- `diplomatic relation towards`: w latach uznania X→TWN zostaje wartość agenta (jeśli ≤ 0, wpisuję 60), a X→CHN ≤ 0;
- po zerwaniu z jedną stroną wartość wobec niej = −30; −100 tylko przy wrogości;
- to samo w drugą stronę: TWN→X i CHN→X.

**Zakres:** ok. 40 państw × 4 kierunki × kilka okresów, czyli ok. 200–300 operacji. Skrypt wypisze tylko komórki, które się zmieniają.

**Koszt:** to głównie skrypt z tabeli; sprawdzenie ok. 10 dat wyszukiwarką i przejrzenie zmian — Opus ok. 0,5 $ (Haiku: kilka centów, ale tu i tak większość pracy robi skrypt).

---

## Jak liczę koszt

- Ceny API (z @T012): Haiku 5.5 — 0,10 $ / 0,50 $ za 1 mln tokenów (wejście / wyjście), Sonnet 5.5 — 2 $ / 10 $, Opus 5.5 — 4 $ / 20 $. **Haiku jest ok. 20× tańszy od Sonnet i 40× od Opus**; Opus jest 2× droższy od Sonnet. (Wcześniej napisałem tu błędnie „Opus ≈ 5× Sonnet” — poprawione.)
- W Claude Code (subskrypcja) te same tokeny zużywają limit okresowy; przez API — miesięczny limit wydatków.
- Wyszukiwarka (WebSearch) kosztuje dodatkowo ok. 0,01 $ za wyszukiwanie.
