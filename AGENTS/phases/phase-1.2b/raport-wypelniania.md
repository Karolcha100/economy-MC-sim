# Phase 1.2b — Raport z wypełniania (agenci Haiku)

Wynik pracy agentów Haiku w Claude Code (@L34, start @A32). Decyzje do podjęcia: `AGENTS/phases/phase-1.2b/agents-issues-2.md` (K1–K8).

*2026-10-14 13:14 — Claude Opus 5.5*

---

## Wynik w liczbach

- **Zadania:** 392 z 392 (196 państw × A: statystyki państwa, B: relacje), wszystkie `[x]` w `AGENTS/phases/phase-1.2b/queue.md`.
- **Batche:** 395 plików w `AGENTS/phases/phase-1.2b/batches/`, łącznie 51 407 operacji. Trzy pliki są uzupełnieniami: `FJI-A-happiness.json` (agent), `BTN-A-happiness.json` i `BLR-A-happiness.json` (koordynator).
- **`missing`:** 100% we wszystkich statystykach i relacjach, dla każdego państwa.
- **`validate`:** 0 błędów, 0 ostrzeżeń.
- **`review`:** 784 skoki, w tym 315 w `net migration` (dane prawdziwe, @K6). Pozostałe skoki agenci wyjaśnili zdarzeniami: zamachy stanu, wojny, zmiany rządu, zmiany uznania Tajwanu/ChRL.
- **Tryby:** pełny (rationale + źródła przy operacjach) dla krajów referencyjnych i Tier 1, oszczędny dla reszty.
- **Wyszukiwarka:** zwykle 0–5 wyszukiwań na zadanie, tylko lata 2023–2025, bez pobierania artykułów.
- **Zużycie:** typowo 70–135 tys. tokenów i 2–6 min na zadanie (Haiku).

## Przebieg

- 06:58: pilot POL A+B. Po pilocie doprecyzowałem `AGENTS/phases/phase-1.2b/prompt-agenta.md`: kolejkę zamyka koordynator.
- Autor zgodził się uruchomić wszystkie zadania naraz (czat). Pracowało 20 agentów równocześnie (limit Claude Code).
- 07:20: nowa reguła dla relacji dwustronnych: agenci dopisują tylko rok 2025, a wpisów UCDP 1990–2024 nie zmieniają ani nie przenoszą. Powód: agenci różnie przenosili pary UCDP między `in war` a `in war crisis`.
- 08:20–12:40: przerwa, bo skończył się miesięczny limit wydatków API.
  - 16 agentów przerwało pracę.
  - 4 zadania miały już komplet danych: MCO-B, GNQ-B, SSD-A, MRT-A. Zamknąłem je po `validate`, `missing` i `review`.
  - 12 zadań (SLE A/B, TGO-B, MDV A/B, MRT-B, LIE A/B, MNE A/B, BRB A/B) uruchomiłem ponownie z informacją o przerwanej próbie. FJI-A zdążyło się tylko zarejestrować, więc ruszyło od nowa.
- Nowe reguły w trakcie, oba wpisy w `AGENTS/phases/phase-1.2b/prompt-agenta.md` z podpisem:
  - pliki tymczasowe tylko w `/tmp/claude-1000/`. Jeden agent zostawił pusty katalog `scratch-tkm` obok projektu; usunąłem go;
  - jeśli państwo nie ma żadnych danych `happiness` (brak WHR), agent szacuje całą serię przez porównanie z podobnymi państwami.
- Uzupełnienia koordynatora:
  - `happiness` BTN 2019–2025 i BLR 2022–2025: ostatnia znana wartość, stała;
  - `confirm-default neighbours` dla SGP i BHR (wyspy bez granicy lądowej).

## Audyt (`AGENTS/phases/phase-1.2b/audit/audit-2026-10-14-1312.md`)

| Porównanie | Zgodność kolejności (przed → po) | Odstające |
|---|---|---|
| `corruption` ↔ CPI / WGI | 0,98 / 1,00 → 0,98 / 1,00 | 0 |
| `violence risk` ↔ WGI | 1,00 → 1,00 | 0 |
| `civilization level` ↔ HDI / PKB pc | 1,00 / 0,93 → 1,00 / 0,93 | 0 |
| `happiness` ↔ Cantril / PKB pc | 1,00 / 0,85 → 1,00 / 0,84 | 1 (BGR) |
| `stability` ↔ PKB pc / WGI | — → 0,63 / 0,71 | 16 / 7 |
| `real power`, `perceived power` ↔ PKB | — → 0,65 | 19 / 22 |
| `economic dependence` ↔ PKB (odwrotnie) | — → **−0,08** | 75 |

- Luki wypełnione przez agentów zgadzają się z danymi startowymi; obie wartości zgodności zostały takie jak przed wypełnianiem.
- **`stability`:** zgodność umiarkowana, czego można się było spodziewać, bo to nowa definicja (instytucje). Najbardziej odstające państwa i kierunek: LAO, TZA, KIR, VNM, RWA, PRK wyżej niż wskaźnik; KWT, ITA, LBN, ISR, TUR niżej. Autorytarne państwa z przewidywalnymi rządami mają wysoką stabilność, a demokracje z częstymi kryzysami rządowymi niską. To zgodne z opisem statystyki, ale do Twojej oceny.
- **`economic dependence`:** brak związku z wielkością gospodarki (−0,08). Możliwe przyczyny: średnia po wszystkich partnerach (z zerami) zależy od liczby wpisanych partnerów, a duże państwa wpisywały wielu partnerów z małą zależnością. Raczej problem miary niż danych; sprawdzę przy przeglądzie próbki.
- **Płaskie linie:** 225. Prawie wszystkie to `government revanchism` (98) i `social revanchism` (93), czyli stała niska wartość w państwach bez roszczeń, co jest poprawne. Dalej `assimilation` (26) i `social sensitivity` (5).
- **Zatłoczenie** (jedna wartość u ponad połowy krajów w roku): 0.

## Uwagi zgłoszone przez agentów

Pogrupowane; decyzje w `agents-issues-2.md`.

### Relacje dwustronne i UCDP (K1, K2, K3)

- **Strony drugorzędne w imporcie UCDP** tworzą fałszywe pary `in war crisis`:
  - RWA × IDN/NPL/BGD (MONUSCO), KEN/UGA/SSD (EAC), ZAF/TZA/MWI (SAMIDRC) w latach 2022–2024 i MWI/ZAF/TZA w 2013 (FIB);
  - YEM × CAN/AUS/NLD/SGP/NOR/NZL/LKA w 2024;
  - koalicja przeciw IRQ 1991 (27 państw, np. NER, SLE) i NATO przeciw SRB 1999 (TUR, DEU, CZE, HUN…);
  - TCD × COG 1997, TCD × UGA/RWA 1998–99.
- **Niespójność `in war` / `in war crisis`:**
  - USA, FRA i SYR przenieśli IRQ 1991 i SRB 1999 do `in war`, pozostali zostawili `in war crisis`;
  - RUS–GEO 2008 jest w `in war`; wojna o Górski Karabach 1992–94 jest w `in war crisis`;
  - II wojna kongijska 1998–2001 (COD–RWA/UGA) jest w `in war crisis`;
  - RWA–COD 2025 ma oba (`in war` = 1 i `in war crisis` = 1). Czy `in war` wyklucza `in war crisis`?
- **Konflikty, których brakuje w UCDP** (1990–2024, reguła nie pozwalała ich dopisać):
  - Jugosławia: HRV–SRB, BIH 1991–95 (HRV 1991–95 zostało niepotwierdzone, potem domknięte przez `confirm-default` innych agentów);
  - LBN–ISR (operacje 1993, 1996, 2006, 2024; okupacja do 2000);
  - PSE–ISR (2008–09, 2014, 2021, 2023–24);
  - KOR–PRK (1999, 2002, 2010, 2015), ESP–MAR (Perejil 2002), NIC–CRI (2010–11), DJI–ERI 2008 (w UCDP jest, w danych puste);
  - wojny zastępcze: LBR–SLE (RUF 1991–2002), ERI→SOM/ETH, TCD–SDN 2003–10, TCD/SDN–CAF 2013;
  - SRB–XKX (2011, 2023), LSO 1998 (interwencja SADC/ZAF).
- **Dyskusyjne wpisy na 2025:**
  - PSE–ISR `in war` (władze palestyńskie nie są stroną walk);
  - ISR–YEM `in war crisis`, a USA–YEM i GBR–YEM mają `in war`;
  - wpisy, gdzie dwaj agenci ocenili parę różnie: QAT–ISR/IRN, CHN–IND, ARM–AZE, SDN–ARE;
  - inne wpisy z jednym źródłem albo granicznym przypadkiem: SSD–SDN (Heglig), LBN–SYR, TJK–AFG, ROU–RUS, EST–RUS, PER–COL, LBY–SDN;
  - kandydaci niedopisani: TTO–VEN, THA–KHM (sprawdzić), PRK–UKR jako `in war` (Kursk).

### Flagi państwa (K4)

- **`epidemic`:** część agentów oznaczała tylko 2020 (jak w kotwicach), część 2020–2021 (jak w opisie). Niespójnie:
  - nieoznaczone: Ebola w GAB i COG (oznaczona w SLE i LBR), HIV w BWA, SWZ i LSO;
  - oznaczone dodatkowo: cholera w YEM 2017–21, odra w WSM 2019, SARS w TWN 2003.
- **`immigration crisis`:** 2015 DEU = 1, SWE = 1, FIN = 0; 2021 (granica z BLR) LTU = 1, POL = 0; TCD 2023–25 (uchodźcy z Sudanu) = 0; AFG 2023–25 (powroty) = 0.
- **`riots` i `state collapse`:** przypadki graniczne (KGZ 2002/2010, NER 2023, COG 1993–97, SLB 2000, TLS 2025, MNE 2019–20, GNB 1998–99).
- **`mobilized`:** ERI 2020–22 (Tigraj) i PRK 2024–25 nieoznaczone.

### Tajwan i ChRL (K5)

- **Błędne daty uznania**, do poprawy:
  - KIR: odwrócone. Kiribati uznawało ChRL do 2003, ROC w latach 2003–2019, ChRL od 2019; ten sam błąd w TWN→KIR;
  - FSM: uznaje ChRL od 1989, a agent wpisał relacje z TWN;
  - LCA: uznawała ChRL w latach 1997–2007, a ma stałe TWN = 80;
  - MHL: uznawała ChRL w latach 1990–98, a CHN jest wtedy puste;
  - SLB: agent uznał, że TWN nie ma tagu, więc brak relacji SLB→TWN w latach 1990–2019;
  - GMB: zerwanie z TWN w 2013, nie w 2016.
- **Konwencja po zerwaniu stosunków:** STP wpisało −100 (słowo w słowo z opisu skali), inni −20 … −40 albo 0.

### Dane startowe (K6)

- **WGI:** stare kody ROM/ZAR/WBG/KSV/ADO/TMP nie zostały zmapowane, więc ROU, COD, PSE, XKX, AND i TLS nie miały wartości startowych `corruption`/`violence risk`. Agenci wpisali szacunki.
- **WGI CC, skoki w danych startowych `corruption`:** LCA, VCT, KNA (2004→2005), TON 2005, PLW 2014→2015, KNA 2013→2014.
- **`net migration`:** wartości obcięte do ±100 (POL 2022, UKR 2025, LBN 2012–19, MKD 1991–93, TGO 1993–94 i in.); 315 skoków w `review`.
- **Granice i sąsiedztwo:**
  - `land-borders` RWA–SSD 2022–23 = 1 (błąd, RWA nie graniczy z SSD);
  - brak ZMB–BWA (Kazungula) i SUR–FRA (Gujana Francuska);
  - `context` nie pokazuje granic NAM.
- **Brak tagów:** VAT (sąsiad SMR), Somaliland.
- **Podejrzane wartości startowe:**
  - `happiness` CAF 2011–19 (brak w `history`);
  - `happiness` LSO 2012–14 (płaskie);
  - `civilization level` CAF 2014/2019/2021;
  - `migrant-stock-share` GNQ.

### Szacunki bez danych (K7)

- **`happiness` bez WHR:** szacunki w ok. 30 państwach, głównie małych wyspiarskich. Niespójny poziom: VUT 57–61, FJI 42–54, SLB 45–52.
- **`stability`:** WSM 2021 złagodzone do 55, żeby nie przekroczyć progu `review`.
- **Dane uzupełnione przeze mnie:** BTN i BLR (stała ostatnia wartość).

### Narzędzia (dla agentów, bez decyzji autora)

- `review` w ostrzeżeniu o braku rationale pokazuje pierwszy zapis komórki zamiast ostatniego (np. GIN:LBR 2002).
- `formulas list`: linia `current:` pokazuje wartości jednego państwa.
- W README dopisać, że `start: current` wymaga wypełnionego pierwszego roku zakresu.
- Rozbieżność `instrukcja-wypelniania.md` (przegląd UCDP) i `prompt-agenta.md` (tylko 2025).
