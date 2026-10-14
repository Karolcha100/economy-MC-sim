# Phase 1.2b — Niejasne statystyki (agents-issues-1)

Zgodnie z Twoją odpowiedzią do P3: statystyki, których opisy uważam za niejasne. LLM-y wypełniające dane będą się opierać tylko na opisach, więc każda niejasność da niespójne liczby w ~196 krajach. Przy każdej statystyce: obecny opis (skrót), problem i propozycja. Wystarczy "zgoda" albo Twoja wersja. Format: **Problem / Propozycja / Decyzja**. Numeracja `Q…`.

*Pełne opisy: `python -m simulator --scenario world-1990-2025 formulas list` albo `simulator/scenarios/world-1990-2025/formulas/*.csv`.*

---

### Q1. 🔴 `immigration` i `emigration` wobec nowego `net migration`
- **Problem:** Dziś są trzy statystyki migracji. `net migration` (z danych, przyjazdy minus wyjazdy) i dwie opisowe "natężenia". Nie jest jasne, co LLM ma ocenić w `immigration`/`emigration`, czego nie mówi `net migration`.
- **Propozycja:** `immigration` / `emigration` = **przepływy brutto** (ile osób przyjeżdża i wyjeżdża na rok, względem ludności) **i ich widoczność społeczna**, 0–100. Przykład: Polska 2004–2008 — `emigration` wysokie (~60), `net migration` tylko lekko ujemne. Alternatywa: usunąć obie i zostawić tylko `net migration`.
- **Decyzja:** usunąć obie i zostawić tylko net migration

### Q2. 🔴 Ujemna połowa skali przy `perceived/real subordination towards` i `perceived/real power towards`
- **Problem:** Skala −100..100. Dla zależności (subordination) przyjąłem: −100 = "FROM uważa TO za swojego wasala". Dla siły (power): ujemne = "działania FROM wobec TO przynoszą odwrotny skutek". To moje wymysły; ten drugi zwłaszcza będzie oceniany losowo.
- **Propozycja:** **Zmienić skalę obu na 0..100** (0 = brak zależności / brak wpływu, 100 = całkowita). Kierunek wyraża para: A→B to zależność A od B, a B→A to odwrotna. Jest prościej i nic nie ginie.
- **Decyzja:** Zgadzam się

### Q3. 🟡 `economic dependence` a `real subordination towards`
- **Problem:** Obie mówią o zależności A od B. Nowa `economic dependence` jest czysto gospodarcza, a `real subordination` ogólna (polityka, wojsko, gospodarka). LLM-y mogą wpisywać to samo dwa razy.
- **Propozycja:** Doprecyzować `real subordination towards` jako **polityczną i militarną** (bez gospodarki, która jest w `economic dependence`).
- **Decyzja:** Zgoda

### Q4. 🟡 `social sensitivity`
- **Problem:** Opis "jak mocno społeczeństwo reaguje na trudności, ofiary i straty" jest szeroki. Nie wiadomo, czy chodzi o odporność na straty wojenne, na kryzys gospodarczy, czy o skłonność do protestów.
- **Propozycja:** **Wrażliwość na koszty**: jak szybko straty (ofiary, spadek dochodów, wzrost cen) przekładają się na sprzeciw wobec władzy i jej polityki. 0 = społeczeństwo znosi duże straty bez reakcji, 100 = małe straty wywołują silny sprzeciw.
- **Decyzja:** Zgoda - Bardzo dobra interpretacja!

### Q5. 🟡 `in hybrid war` jako relacja dwustronna
- **Problem:** Działania hybrydowe są często jednostronne (np. RUS → POL: dezinformacja, sabotaż, migracja jako broń z Białorusi 2021), a relacja dwustronna wymusza symetrię.
- **Propozycja:** Przenieść do relacji **skierowanych**: `hybrid attacks towards` (0/1), FROM prowadzi działania hybrydowe wobec TO. Obecne wartości są puste, więc zmiana nic nie kosztuje.
- **Decyzja:** Zgoda.

### Q6. 🟢 `government popularity` — sondaże w procentach?
- **Problem:** Skala 0–100 jest bliska procentowemu poparciu w sondażach, ale nie identyczna (opis: "0 = powszechnie odrzucany, 100 = niemal powszechne poparcie").
- **Propozycja:** Wprost: **procent poparcia dla rządu / przywódcy w sondażach** (jeśli są), a w krajach bez wiarygodnych sondaży ocena LLM na tej samej skali.
- **Decyzja:** Zgoda.

### Q7. 🟢 `happiness` a dane Gallupa (Cantril 0–10)
- **Propozycja:** Od 2005 roku `happiness` ≈ 10 × Cantril (kotwica z danych), a LLM koryguje tylko z powodem. Przed 2005 ocena LLM spójna z tą skalą.
- **Decyzja:** Zgoda.

### Q8. 🟢 `revanchism` — czyj?
- **Problem:** Nie wiadomo, czy chodzi o politykę państwa, nastroje społeczeństwa, czy jedno i drugie.
- **Propozycja:** **Najsilniejszy z dwóch**: oficjalna polityka albo masowe nastroje (np. Rosja po 2008 roku: polityka ~80; Węgry: nastroje wokół Trianon ~30, polityka ~20 → 30).
- **Decyzja:** Chodziło mi o revanchism społeczeństwa, można zmienić na `social-revanchism` i `government-revanchism`.
