# Phase 1.2a — Pytania przed wyliczeniem wartości startowych (agents-issues-0)

Surowe wskaźniki są już zaimportowane (L1, L2; lista w `simulator/README.md`, sekcja History). Zanim skrypt "seed" (L3) zamieni je na wartości startowe danych opisowych, potrzebuję Twoich decyzji o **przeliczeniu skal** i kilku definicjach. Format: **Problem / Propozycja / Decyzja**. Numeracja `W…` (od "wskaźniki"). Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

Wszystkie przykłady liczbowe poniżej to prawdziwe dane po proponowanym przeliczeniu.

*2026-10-14 01:10 — Claude Opus 5.5*

---

## W. Przeliczenia skal

### W1. 🔴 `stability` ← WGI Political Stability (−2,5..2,5)
- **Problem:** Skala WGI jest inna niż nasza 0..100. Dodatkowo WGI mierzy głównie ryzyko przemocy i terroryzmu, a nasz opis obejmuje też kryzysy rządowe.
- **Propozycja:** Liniowo: `stability = 50 + 20 × WGI`, przycięte do 0..100 (−2,5 → 0, 0 → 50, 2,5 → 100). Przykłady:

  | | POL | RUS | UKR | DEU | CHE | SOM |
  |---|---|---|---|---|---|---|
  | 2000 | 56 | 22 | 42 | 78 | 82 | 11 |
  | 2015 | 67 | 29 | 11 | 64 | 77 | 3 |
  | 2022 | 60 | 32 | 10 | 62 | 73 | 0 |

  Alternatywa: ranking procentowy WGI (najlepszy kraj = 100). Jest jednak względny: wynik kraju zmienia się, gdy inne kraje się poprawią. Odradzam.
- **Decyzja:** Zgoda

### W2. 🔴 `corruption` ← WGI Control of Corruption (wyższe = mniej korupcji)
- **Propozycja:** `corruption = 50 − 20 × WGI`, przycięte do 0..100. TI CPI (`100 − CPI`, porównywalne od 2012) służy tylko jako kontrola, bo wychodzi bardzo podobnie:

  | 2015 | POL | RUS | UKR | DEU | CHE | SOM |
  |---|---|---|---|---|---|---|
  | z WGI | 36 | 69 | 71 | 14 | 8 | 83 |
  | z CPI | 37 | 71 | 73 | 19 | 14 | 92 |
- **Decyzja:** Zgoda

### W3. 🔴 `civilization level` ← HDI (0..1)
- **Problem:** Nasz opis mówi "0 = najsłabiej rozwinięty kraj świata, 100 = najlepiej". To skala **względna**, a HDI jest bezwzględny: najniższy HDI w 2015 to 0,32, najwyższy 0,96.
- **Propozycja:** `civilization level = 100 × HDI` (POL 2015: 88, RUS 83, UKR 78, CHE 96, najsłabsze kraje ~32–40) i **zmiana opisu wzoru** na bezwzględny: "100 × HDI-like development; ~30 = least developed countries today, ~95 = most developed". Skala względna (min–max w danym roku) ukrywałaby postęp, np. wzrost Polski z 72 w 1990 do 90 w 2022.
- **Decyzja:** Zmieńmy naszą skalę na bezwzględną

### W4. 🟡 `immigration` / `emigration` ← migracja netto na 1000 mieszkańców
- **Problem:** Dostępna jest tylko migracja **netto** (przyjazdy minus wyjazdy). Nie da się z niej odczytać, że w kraju jednocześnie dużo osób przyjeżdża i wyjeżdża (np. Polska po 2004). Rozkład w 2015: 5% krajów poniżej −15,6‰, mediana −0,5‰, 95% poniżej +18,9‰; skrajności: Katar +75,7‰, Ukraina 2022 −138,8‰ (uchodźcy).
- **Propozycja (słaba, ale lepsza niż nic):**
  - `immigration = min(100, 5 × max(stopa, 0))`;
  - `emigration = min(100, 5 × max(−stopa, 0))`;
  - czyli +10‰ → 50, +20‰ → 100.

  Wartości startowe dla migracji muszą być **szczególnie poprawiane przez LLM**, który zna przepływy brutto. Udział migrantów w ludności (`migrant-stock-share`, co 5 lat) zostaje jako kotwica.
- **Decyzja:** Wpiszmy migrację netto

### W5. 🟢 `happiness` ← Cantril (0..10), tylko kotwica
- **Propozycja:** Zgodnie z M1 (grupa B) bez wartości startowych. `context` pokaże `10 × Cantril` jako punkt odniesienia dla LLM (dane od ~2005).
- **Decyzja:** Oki, zgoda

---

## X. Definicje dla relacji

### X1. 🔴 `in war` ← UCDP: które przypadki liczyć?
- **Problem:** UCDP rozróżnia dwa poziomy (w danych: `ucdp-armed-conflict`):
  - **2** = obie strony są głównymi stronami wojny międzypaństwowej. 20 par, np. Irak–Kuwejt 1990–91, Indie–Pakistan, Erytrea–Etiopia 1998–2000, **Rosja–Ukraina 2022–2024**;
  - **1** = rządy po przeciwnych stronach, ale co najmniej jeden jako strona wspierająca (z wojskiem). 111 par, w tym:
    - trafne: **Rosja–Ukraina 2014–2021** (Donbas), Armenia–Azerbejdżan, Rosja–Gruzja 2008;
    - dyskusyjne: wszyscy członkowie NATO vs Serbia 1999 (np. **Polska–Serbia**), cała koalicja vs Irak 1991, państwa misji ONZ vs Rwanda 2022–23.
- **Propozycja:** Wartość startowa `in war = 1` dla poziomów 1 i 2. Pary z poziomu 1 (111) LLM przegląda jedna po drugiej i usuwa te, które nie pasują do naszego opisu ("open armed conflict between the two states"). Rok 2025 (poza UCDP) uzupełnia LLM.
- **Decyzja:** A co z wojną hybrydową? Nie możemy z niej skorzystać tutaj?

### X2. 🟡 `neighbours` ← GeoNames: dzisiejsze granice dla wszystkich lat
- **Problem:** GeoNames podaje **dzisiejsze** granice lądowe. Dla wcześniejszych lat brakuje m.in.:
  - **RUS 1990** (jako ZSRR) z IRN, AFG, TUR, ROU, HUN;
  - SRB (jako Jugosławia) z ALB do 2008;
  - SDN z KEN, UGA, COD do 2010 (przed powstaniem Sudanu Południowego).
- **Propozycja:** Wartość startowa z GeoNames dla wszystkich lat, w których oba kraje istnieją, plus **mały plik ręcznych poprawek** (`neighbours` jest bez LLM, decyzja M1). Poprawki przygotuję i dam Ci do przejrzenia jako zadanie A.
- **Decyzja:** Oki jasne!

### X3. 🔴 Czechosłowacja 1990–1992 nie istnieje w scenariuszu
- **Problem:** Przy granicach wyszła luka w liście państw (K2): Rosja i Serbia są kontynuacjami ZSRR i Jugosławii, ale **Czechosłowacja nie ma żadnego odpowiednika**. CZE i SVK istnieją od 1993, więc w latach 1990–1992 obszaru między Polską, Niemcami, Austrią i Węgrami w modelu nie ma.
- **Propozycja:** CZE jako kontynuacja Czechosłowacji: `exists_from` puste (od 1990); SVK zostaje od 1993. Tak samo jak RUS i SRB. Zmiana jednej linijki w `tags.csv` i w `extract-gdp.ipynb`.
- **Decyzja:** Zgoda.

---

## Y. Zasady wartości startowych (seed)

### Y1. 🟡 Lata bez wskaźnika
- **Problem:** WGI: 1996–2022, do 2002 co dwa lata. HDI: od 1990, ale nie dla wszystkich. UCDP: do 2024.
- **Propozycja:**
  - luki **wewnątrz** zakresu (1997, 1999, 2001) wypełnić interpolacją liniową;
  - lat **przed** pierwszą i **po** ostatniej wartości nie wypełniać: zostają dla LLM (np. 1990–1995 i 2023–2025 dla `stability`).
- **Decyzja:** Interpolacja Liniowa

### Y2. 🟡 Seed nie może nadpisać poprawek LLM
- **Propozycja:**
  - seed zapisuje z `author=seed:<źródło>` i z `--only-empty` (ponowne uruchomienie nie niszczy poprawek);
  - `review` (L5) porównuje dane z wartością wyliczoną na nowo ze wskaźnika i ostrzega przy różnicy większej niż 15 punktów;
  - przeliczenia z W1–W4 trafią do pliku konfiguracyjnego scenariusza `seeds.csv` (wzór, źródło, przekształcenie, parametry), żebyś mógł je zmieniać bez programisty.
- **Decyzja:** Chwila czym są wartości startowe? (odpowiedzi udziel w `wymiana-zdan-A1.md`)
