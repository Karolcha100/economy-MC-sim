# Phase 1.2b — K6. Błędy danych startowych — o co chodzi

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K6 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A38; wykonanie: @L46. Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022; „Co masz zrobić” i koszty: 2026-10-14 15:59)*

---

## Co masz zrobić (wyjaśnienie od nowa)

To są **błędy w prawdziwych danych, które importujemy z zewnątrz** (Bank Światowy, WGI, GeoNames), a nie w pracy agentów. Są cztery; przy każdym odpowiedz tak / nie:

1. **Kody państw w WGI (tak / nie):** plik WGI ma stare kody (np. Rumunia = ROM zamiast ROU). Przez to 6 państw (ROU, COD, PSE, XKX, AND, TLS) nie dostało prawdziwych danych o korupcji i przemocy — agenci je zgadywali. Propozycja: poprawić kody i wstawić prawdziwe dane w miejsce zgadywanych. To samo z Kosowem w danych o szczęściu (WHR).
2. **Skoki w danych o korupcji małych państw (tak / nie):** dla kilku małych wysp (LCA, VCT, KNA, TON, PLW) WGI ma nagłe skoki o 15–30 pkt z roku na rok, bo zmienia się liczba źródeł. Propozycja: wygładzić tylko te skoki (średnia z 3 lat).
3. **Brakująca granica Zambia–Botswana (tak / nie):** mają 150 m wspólnej granicy, której nie ma w GeoNames. Propozycja: dopisać ręcznie.
4. **Migracja (tak / nie):** saldo migracji ma ucięte wartości skrajne (np. Polska 2022). Propozycja: na razie zostawić i sprawdzić w Phase 2.1, czy to przeszkadza.

Wystarczy np. „1 tak, 2 tak, 3 tak, 4 tak”. Po @A39 punkty 1–2 dotyczą tylko państw, które zostają w modelu.

---

## Szczegóły

1. **Kody WGI.** Plik WGI używa starych kodów: ROM (Rumunia), ZAR (Kongo DR), WBG (Palestyna), KSV (Kosowo), ADO (Andora), TMP (Timor Wschodni). Dlatego ROU, COD, PSE, XKX, AND i TLS nie dostały wartości startowych `corruption` i `violence risk`, a agenci wpisali szacunki.
   - **Plan:** słownik aliasów w `simulator/sources.py` i test. Przeliczam wartości startowe tylko dla tych 6 państw. W latach z danymi WGI (1996–2022) dane zastępują szacunki agentów, a lata 1990–95 i 2023–25 wygładzam do nowych wartości. To samo sprawdzę dla WHR: XKX nie ma tam `happiness`, choć Kosowo jest w raporcie WHR, więc to pewnie ten sam problem z kodem.
2. **Skoki `corruption` w małych państwach** (LCA, VCT, KNA 2004→2005; TON 2005; PLW 2014→2015; KNA 2013→2014). WGI dla małych państw opiera się na 1–3 źródłach, więc wejście albo wypadnięcie jednego źródła daje skok o 15–30 punktów.
   - **Plan:** te 5 państw dostaje średnią kroczącą z 3 lat w miejscu skoku. Reszta danych WGI bez zmian.
3. **Granice.**
   - Para RWA–SSD w `land-borders` to **fałszywy alarm**: plik jej nie zawiera; agent pomylił ją z parą UCDP.
   - ZMB–BWA (Kazungula, ok. 150 m granicy na Zambezi): GeoNames jej nie ma, więc dopisuję ją do `data/manual` (ręczne granice).
   - SUR–FRA (Gujana Francuska): nie dopisuję, bo terytoria zamorskie nie są granicami w modelu.
4. **`net migration` obcięte do ±100.** Skala: 5 × saldo na 1000 mieszkańców, więc ±100 odpowiada ±20‰. Wartości przekraczają ten zakres przy falach uchodźców i powrotów (POL 2022, UKR 2022–25, LBN 2012–19, MKD 1991–93, TGO 1993–94…); `review` pokazuje 315 skoków.
   - **Plan:** zostawić do Phase 2.1 i zobaczyć, czy ekstremalne wartości przeszkadzają nauce. Ewentualnie później skala logarytmiczna.
5. **Do sprawdzenia przy okazji:**
   - `happiness` CAF 2011–19 (skąd, skoro w `history` brak danych);
   - płaskie `happiness` LSO 2012–14;
   - skoki `civilization level` CAF (2014, 2019, 2021);
   - udział migrantów GNQ (0,7% → 14,4%).

**Koszt:** to programowanie (kod importu + test) i przeliczenie skryptem — ok. 1–2 $ pracy Opus; model tańszy nic tu nie zaoszczędzi, bo nie ma czego oceniać.

---

## Jak liczę koszt

- Ceny API (z @T012): Haiku 5.5 — 0,10 $ / 0,50 $ za 1 mln tokenów (wejście / wyjście), Sonnet 5.5 — 2 $ / 10 $, Opus 5.5 — 4 $ / 20 $. **Haiku jest ok. 20× tańszy od Sonnet i 40× od Opus**; Opus jest 2× droższy od Sonnet. (Wcześniej napisałem tu błędnie „Opus ≈ 5× Sonnet” — poprawione.)
- W Claude Code (subskrypcja) te same tokeny zużywają limit okresowy; przez API — miesięczny limit wydatków.
- Wyszukiwarka (WebSearch) kosztuje dodatkowo ok. 0,01 $ za wyszukiwanie.
