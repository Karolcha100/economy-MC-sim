# Phase 1.2b — Decyzje po wypełnieniu (agents-issues-2)

Wypełnianie skończone: `missing` 100%, `validate` 0 błędów. Szczegóły i pełne listy przypadków: `AGENTS/phases/phase-1.2b/raport-wypelniania.md`. Poniżej sprawy, w których agenci postąpili niejednolicie albo napotkali błędy danych. Do każdej podaję rekomendację; wystarczy „zgoda” albo Twoja wersja. Po decyzjach poprawki zrobię jednym zadaniem (@L40). Format: **Problem / Propozycja / Decyzja**. Numeracja `K…`.

*2026-10-14 13:14 — Claude Opus 5.5*

---

### K1. 🔴 Import UCDP: strony drugorzędne i `in war` a `in war crisis`
- **Problem:**
  - Import UCDP bierze też strony drugorzędne. Powstają fałszywe pary, np. RWA × IDN/NPL/BGD/KEN/ZAF (kontyngenty misji w Kongu), YEM × CAN/AUS/NLD/SGP (2024) i 27 państw koalicji przeciw IRQ 1991.
  - Agenci różnie traktowali wielkie wojny. USA, FRA i SYR przenieśli IRQ 1991 i SRB 1999 do `in war`, reszta zostawiła `in war crisis`.
  - RWA–COD 2025 ma jednocześnie `in war` i `in war crisis`.
- **Propozycja:**
  1. Poprawić import: brać tylko strony główne (side_a/side_b primary). Pary ze stron drugorzędnych usunąć, ale tylko tam, gdzie wpisał je import, a nie agent.
  2. `in war` = wojna międzypaństwowa z regularnymi siłami obu stron, w której ginie ≥ 1000 osób rocznie. Dla konfliktów spoza tej definicji: `in war crisis`.
  3. `in war` wyklucza `in war crisis` w tej samej parze i roku.
  4. Ujednolicić według tej reguły wszystkie pary z obu list (wielkie wojny i fałszywe pary), jednym batchem koordynatora.
- **Decyzja:** Spoko, rozpisz plan na to i daj mi taska (TODO) bym to przeczytał i zatwierdził.

### K2. 🔴 Konflikty, których brakuje w UCDP (1990–2024)
- **Problem:** Reguła „tylko 2025” nie pozwoliła dopisać znanych konfliktów. Brakuje m.in.:
  - wojen w Jugosławii (HRV, BIH 1991–95);
  - par LBN–ISR i PSE–ISR;
  - incydentów KOR–PRK (1999, 2002, 2010, 2015);
  - wojen zastępczych LBR–SLE (RUF), ERI→SOM/ETH, TCD–SDN 2003–10;
  - par ESP–MAR 2002, NIC–CRI 2010–11, SRB–XKX 2011/2023;
  - pary DJI–ERI 2008, która w UCDP jest, a w danych jest pusta.
- **Propozycja:** Jeden batch koordynatora (Opus) z listą z raportu, po regule z K1. Każda para dostaje rationale i źródło. Pary z podmiotami niepaństwowymi (PSE–ISR, LBN–ISR po 2000) wpisać jako `in war crisis`, bo państwo jest stroną konfliktu na swoim terytorium.
- **Decyzja:** Proszę o TODO (taska) do tego problemu, oraz dokument wyjaśniający o co chodzi w regule 2025, jak do niej doszło i jakie środki powinno się wdrożyć aby zapobiec tego typu problemom na przyszłość (rozumiem że to coś w stylu, niezamierzonego ograniczenia). Dodatkowo, proszę o przewidywane zużycie opusa na taki plan i jakie mamy alternatywy w tym.

### K3. 🟡 Dyskusyjne wpisy na 2025
- **Problem:**
  - ISR–YEM ma `in war crisis`, a USA–YEM i GBR–YEM mają `in war`;
  - PSE–ISR ma `in war`, choć władze palestyńskie nie są stroną walk;
  - przy niektórych parach dwaj agenci ocenili sytuację różnie (np. ARM–AZE, CHN–IND, QAT–ISR/IRN, SDN–ARE);
  - THA–KHM 2025 i PRK–UKR 2025 (Kursk) wymagają sprawdzenia.
- **Propozycja:** Rozstrzygnąć według reguły z K1:
  - USA/GBR/ISR–YEM 2025: `in war crisis` (naloty bez wojny lądowej);
  - PSE–ISR 2025: `in war crisis`;
  - THA–KHM 2025: `in war crisis`;
  - PRK–UKR 2025: `in war crisis` (wojska PRK walczą na terytorium RUS);
  - pozostałe przejrzę i wyślę Ci listę z jednym zdaniem uzasadnienia przy każdej parze.
- **Decyzja:** Zgoda.

### K4. 🟡 Konwencje flag państwa
- **Problem:** Każdy agent inaczej ustawiał progi:
  - `epidemic`: 2020 czy 2020–2021; Ebola oznaczona w SLE i LBR, ale nie w GAB i COG; HIV nigdzie;
  - `immigration crisis`: 2015 DEU = 1, FIN = 0; 2021 LTU = 1, POL = 0;
  - `riots` / `state collapse` w przypadkach granicznych.
- **Propozycja:**
  - `epidemic` = 2020 i 2021 dla wszystkich (COVID) oraz epidemie z wyraźną nadumieralnością lub stanem wyjątkowym (Ebola 2014–15 w GIN, SLE, LBR; cholera w YEM; SARS w TWN). HIV nie, bo to stan przewlekły, a nie epidemia w sensie modelu.
  - `immigration crisis` = napływ ≥ 0,5% ludności w roku albo stan wyjątkowy na granicy (2015: DEU, SWE, AUT, HUN; 2021: LTU, POL, LVA).
  - Poprawki jednym batchem.
- **Decyzja:** Zgoda, rozpisz mi jak zamierzasz to zrobić w odpowiednim TODO oraz podłączonym raporcie - Ja dodam uwagi/zatwierdzę i rozpoczniesz prace.

### K5. 🟡 Tajwan i ChRL: daty uznania i wartość po zerwaniu
- **Problem:**
  - Błędne daty uznania: KIR (odwrócone), FSM (uznaje ChRL od 1989), LCA (ChRL 1997–2007), MHL (ChRL 1990–98), SLB (brak relacji z TWN 1990–2019), GMB (zerwanie z TWN w 2013).
  - Wartość `diplomatic relation towards` po zerwaniu stosunków jest różna: od −100 (STP) do 0.
- **Propozycja:** Zerwanie stosunków bez wrogości = −30; −100 tylko przy wrogości (np. groźby, sankcje). Poprawić daty i wartości jednym batchem dla wszystkich par z TWN i CHN.
- **Decyzja:** Zgoda, ale proszę o raport co to znaczy poprawić jednym batchem oraz TODO od tego.

### K6. 🟡 Błędy danych startowych
- **Problem:**
  - Stare kody WGI (ROM, ZAR, WBG, KSV, ADO, TMP) nie zostały zmapowane. Dla ROU, COD, PSE, XKX, AND i TLS agenci wpisali szacunki zamiast danych.
  - Skoki `corruption` w małych państwach (WGI CC 2004→2005 itd.).
  - `land-borders` RWA–SSD = 1 (błąd).
  - Brak granic ZMB–BWA i SUR–FRA.
  - `net migration` obcięte do ±100 (315 skoków).
- **Propozycja:**
  1. Poprawić mapowanie kodów i przeliczyć wartości startowe. W 6 państwach zastąpić szacunki agentów danymi, bo dane są lepsze.
  2. Skoki WGI CC: zostawić (to dane), ale wygładzić rok przejścia w małych państwach, gdzie WGI ma 1–2 źródła.
  3. Poprawić RWA–SSD i dodać ZMB–BWA. SUR–FRA nie dodawać, bo terytoria zamorskie nie są granicami w modelu.
  4. `net migration`: zmienić skalę na ‰ z obcięciem ±50 albo zostawić. Rekomendacja: zostawić do Phase 2.1 i ocenić, czy ekstremy szkodzą nauce.
- **Decyzja:** Poproszę o raport o co tu chodzi, oraz o plan działania które chcesz zrobić i TODO.

### K7. 🟢 Szacunki `happiness` bez danych WHR
- **Problem:** Około 30 państw, głównie małych wyspiarskich, nie ma żadnych danych WHR, więc agenci oszacowali całe serie. Poziomy są niespójne, np. VUT 57–61, a FJI 42–54. Dla BTN (2019–25) i BLR (2022–25) koordynator wpisał ostatnią znaną wartość.
- **Propozycja:** Zostawić szacunki, ale wyrównać je jednym batchem do mediany państw o podobnym PKB na mieszkańca i regionie (kontrola w `audit`).
- **Decyzja:** Poproszę o TODO i raport o tym co sądzisz aby je wyrzucić? Jakie to Państwa?

### K8. 🟢 Przegląd próbki (A31)
- **Problem:** Zgodnie z @A31 zostaje przegląd próbki (kraje referencyjne + Tier 1) przez drugiego agenta. Audyt pokazał też słabą zgodność `economic dependence` (−0,08) i umiarkowaną `stability` (0,63–0,71).
- **Propozycja:** Najpierw poprawki K1–K7 (Opus, jeden agent), potem przegląd próbki: Sonnet, ok. 30 zadań, z listą odstających z audytu. Koszt: kilka godzin limitu; uwaga na miesięczny limit wydatków (przerwa 08:20–12:40).
- **Decyzja:** Przenieść do future work, obecnie nie mamy na to zasobów.
