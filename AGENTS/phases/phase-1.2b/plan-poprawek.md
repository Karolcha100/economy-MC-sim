# Phase 1.2b — Plan poprawek po wypełnieniu (K1–K8)

Odpowiedzi na Twoje decyzje w `AGENTS/phases/phase-1.2b/agents-issues-2.md`. Każda sekcja: co się dzieje, co chcę zrobić, ile to kosztuje. Zadania do zatwierdzenia: @A34 (K1), @A35 (K2), @A36 (K4), @A37 (K5), @A38 (K6), @A39 (K7). Wykonanie: @L41–@L46. **Nic poza K3 nie zostało jeszcze zmienione w danych.**

*2026-10-14 13:55 — Claude Opus 5.5*

---

## Jak liczę koszt

- Szacunki w tokenach, bo to one zużywają limit (w Claude Code subskrypcja ma limity okresowe; przez API dochodzi miesięczny limit wydatków, który skończył się dziś o 08:20).
- Orientacyjnie: Opus ≈ 5× droższy od Sonnet, Sonnet ≈ 3× droższy od Haiku (na token).

---

## K1. Import UCDP: strony drugorzędne, `in war` a `in war crisis`

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
- alternatywa: Sonnet, ok. 5× taniej, a jakość przy tak znanych konfliktach powinna wystarczyć.

---

## K2. Brakujące konflikty 1990–2024

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

| Wariant | Kto | Zużycie | Ryzyko |
|---|---|---|---|
| A | Opus robi wszystko | ~250–400 tys. tokenów (ok. 40 par × 1–2 wyszukiwania + zapis), ok. 1–1,5 h | najmniejsze |
| B (**rekomendacja**) | Opus ustala listę i regułę (ok. 50 tys.), Sonnet sprawdza daty i źródła (ok. 300 tys. tokenów Sonnet ≈ 60 tys. „Opus”), Opus sprawdza różnice (ok. 50 tys.) | ok. 1/3 wariantu A | małe |
| C | Sonnet bez kontroli Opus | ok. 1/5 wariantu A | średnie (daty, interpretacja reguły) |
| D | Haiku, po jednym agencie na region | najtańsze | duże; to ten sam model, który dał niespójności |
| E | Ty poprawiasz tabelę ręcznie, a ja tylko zapisuję batch | prawie zero | Twój czas |

---

## K3. Wpisy na 2025 — zrobione częściowo

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

---

## K4. Konwencje flag państwa

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

**Koszt:** Opus ok. 80–120 tys. tokenów. Bez wyszukiwarki poza sprawdzeniem kilku epidemii.

---

## K5. Tajwan i ChRL — co znaczy „jednym batchem”

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

**Koszt:** Opus ok. 60–100 tys. tokenów (z ok. 10 wyszukiwaniami).

---

## K6. Błędy danych startowych — o co chodzi

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

**Koszt:** kod i test ok. 1–2 h pracy Opus; przeliczenie to skrypt, a sprawdzenie ok. 50 tys. tokenów.

---

## K7. Państwa bez danych WHR — moja opinia (pytanie o opinię, nic nie zmieniam)

**Które to państwa** (34, od największej ludności):
PRK (26 mln), PNG (10 mln), ERI, GNB, GNQ, XKX, TLS, FJI, SLB, CPV, BRN, BHS, VUT, BRB, STP, WSM, LCA, KIR, SYC, GRD, FSM, TON, VCT, ATG, AND, DMA, KNA, LIE, MCO, MHL, SMR, PLW, NRU, TUV.
- Razem ok. 50 mln ludzi, z czego PRK i PNG to 36 mln. Pozostałe 32 państwa to ok. 14 mln.
- XKX pewnie ma dane (błąd kodu, K6).

**Czy je wyrzucić?**
- **Za:**
  - 32 mikropaństwa praktycznie nie wpływają na relację POL–RUS;
  - ich dane opisowe to w całości szacunki;
  - w uczeniu (Phase 2.1) to 1/6 obserwacji z bardzo słabymi danymi, więc dodają szum;
  - mniejsza macierz relacji (196² → 164²) daje szybsze obliczenia.
- **Przeciw:**
  - PRK jest ważne geopolitycznie (sojusz z RUS, wojska w Kursku), a PNG, ERI i XKX mają realne konflikty;
  - wyrzucenie po wypełnieniu marnuje gotowe dane;
  - trzeba by poprawić relacje innych państw (np. TWN z wyspami, a uznanie Tajwanu to część gry dyplomatycznej ChRL);
  - przy liczeniu „średniej świata” małe państwa i tak ważą mało, jeśli ważymy ludnością.

**Rekomendacja:** **nie wyrzucać ze scenariusza.**
- W Phase 2.1 dodać **wagę obserwacji** (np. ludność albo flaga „dane szacowane”).
- Ewentualnie wyłączyć z uczenia regresji `happiness` 32 mikropaństwa bez WHR (bez PRK i PNG).
- Państwa zostają w świecie symulacji, ale nie psują nauki.
- Decyzja należy do Ciebie (@A39).

---

## K8. Przegląd próbki

Przeniesione do `AGENTS/plan/future-work.md` (Twoja decyzja: brak zasobów).
