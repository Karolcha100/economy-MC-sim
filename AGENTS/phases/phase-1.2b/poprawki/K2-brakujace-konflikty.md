# Phase 1.2b — K2. Brakujące konflikty 1990–2024

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K2 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A35; wykonanie: @L42. Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022; „Co masz zrobić” i koszty: 2026-10-14 15:59)*

---

## Co masz zrobić

**Pytanie:** kto i jak ma dopisać ok. 40 konfliktów z lat 1990–2024, których brakuje w danych (lista niżej) — wybierz wariant z tabeli na końcu.

- **Zależności od innych zadań (aktualizacja):**
  - najpierw @A34 (reguła UCDP), bo ona mówi, co jest `in war`, a co `in war crisis`;
  - @A39: z modelu wypadają 32 małe państwa — żadna para z listy niżej ich nie dotyczy, z wyjątkiem SRB–XKX; Kosowo jednak **ma** dane WHR (błąd importu), więc proponuję je zostawić (@A39);
  - @A34 i @A40: rozważamy Haiku — tu też dodałem wariant Haiku.
- Wystarczy: „wariant H” (albo inny). Wszystkie warianty kosztują poniżej 3–4 $ — różnica jest głównie w ryzyku pomyłek.

---

## Szczegóły

Wyjaśnienie reguły „tylko 2025” i środki zapobiegawcze: `AGENTS/phases/phase-1.2b/regula-2025.md`.

**Lista kandydatów** (z raportów agentów, ok. 40 par; do uzupełnienia przy pracy):

| Grupa | Pary (lata) |
|---|---|
| Jugosławia | HRV–SRB 1991–95, BIH–SRB 1992–95, BIH–HRV 1993–94, SVN–SRB 1991 |
| Bliski Wschód | LBN–ISR 1990–2000 (okupacja), 1993, 1996, 2006, 2023–24; PSE–ISR 2000–05, 2008–09, 2012, 2014, 2021, 2023–24; EGY–ISR 2023–24 (incydenty) |
| Azja | KOR–PRK 1999, 2002, 2010, 2015; IND–CHN 2017, 2020; THA–KHM 2008–11 |
| Afryka | LBR–SLE 1991–2002 (RUF), ERI–SOM 2006–17, ERI–ETH 2023–24, TCD–SDN 2005–10, TCD–CAF i SDN–CAF 2013, DJI–ERI 2008 (jest w UCDP, w danych puste), LSO 1998 (interwencja SADC/ZAF) |
| Inne | ESP–MAR 2002 (Perejil), NIC–CRI 2010–11, SRB–XKX 2011, 2023, GEO–RUS 2008 (sprawdzić, czy jest), TUR–GRC 1996 (Imia) |

**Plan.**
1. Najpierw K1, bo reguła decyduje o tym, co jest `in war`, a co `in war crisis`.
2. Opus z wyszukiwarką sprawdza daty każdej pary. Sprawdzenie jest krótkie, bo większość to dobrze znane konflikty. Wynik trafia do tabeli `AGENTS/phases/phase-1.2b/k2-konflikty.csv` (para, lata, typ, źródło, uzasadnienie).
3. Ty przeglądasz tabelę.
4. Jeden batch `K2-konflikty.json` z `rationale` i `sources` przy każdej operacji. Nadpisuje wartości domyślne potwierdzone przez `confirm-default` (narzędzie na to pozwala).

**Przewidywane zużycie i alternatywy:**

| Wariant | Kto | Koszt API (ok.) | Ryzyko |
|---|---|---|---|
| A | Opus robi wszystko (ok. 40 par, 1–2 wyszukiwania na parę) | 2,5 $ + 0,6 $ wyszukiwania | najmniejsze |
| B | Opus ustala listę i regułę, Sonnet sprawdza daty i źródła, Opus sprawdza różnice | 1,5 $ + 0,6 $ | małe |
| **H (rekomendacja po Twojej uwadze o Haiku)** | Opus (ja) ustalam listę par i regułę; **jeden** agent Haiku z wyszukiwarką sprawdza daty i źródła całej listy; ja sprawdzam wynik | 0,1 $ + 0,6 $ + ok. 0,5 $ (ja) | małe–średnie (Haiku przy datach bywa nieprecyzyjny, ale sprawdzam) |
| C | Sonnet bez kontroli Opus | 1,2 $ + 0,6 $ | średnie |
| D | Haiku, po jednym agencie na region, bez kontroli | 0,1 $ + 0,6 $ | duże (niespójność jak w fali 1.2b) |
| E | Ty poprawiasz tabelę ręcznie, a ja tylko zapisuję batch | ~0 $ | Twój czas |

---

## Jak liczę koszt

- Ceny API (z @T012): Haiku 5.5 — 0,10 $ / 0,50 $ za 1 mln tokenów (wejście / wyjście), Sonnet 5.5 — 2 $ / 10 $, Opus 5.5 — 4 $ / 20 $. **Haiku jest ok. 20× tańszy od Sonnet i 40× od Opus**; Opus jest 2× droższy od Sonnet. (Wcześniej napisałem tu błędnie „Opus ≈ 5× Sonnet” — poprawione.)
- W Claude Code (subskrypcja) te same tokeny zużywają limit okresowy; przez API — miesięczny limit wydatków.
- Wyszukiwarka (WebSearch) kosztuje dodatkowo ok. 0,01 $ za wyszukiwanie.
