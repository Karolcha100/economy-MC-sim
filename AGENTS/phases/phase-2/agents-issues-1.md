# Phase 2.0 — Pytania, runda 1 (agents-issues-1): skutki decyzji R1–R5

Twoje decyzje R1–R5 z `agents-issues-0.md` (i wątek @T007 o turach) wyznaczają kształt silnika. Poniżej sprawy techniczne, które z nich wynikają i które trzeba rozstrzygnąć przed implementacją. Format: **Problem / Propozycja / Decyzja**. Numeracja `U…`. Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

Liczby dla scenariusza `world-1990-2025`: 196 państw, 16 statystyk wewnętrznych, 6 relacji skierowanych, 4 dwustronne, 9 statystyk prawdziwych, 35 przejść rok→rok.

*2026-10-14 03:24 — Claude Opus 5.5*

---

## U. Model

### U1. 🔴 Regresja dla każdego kraju: 35 obserwacji na wiele zmiennych
- **Problem:** Decyzja R1: osobna regresja dla każdego kraju, bez efektów losowych. Kraj ma jednak tylko **35 przejść rok→rok** (kraje powstałe po 1990 mniej). Jeśli model kraju ma brać pod uwagę inne państwa (R2) bezpośrednio, to zmiennych jest więcej niż obserwacji (np. 196 krajów × 25 statystyk). Regresja wtedy "zapamięta" historię i nic nie przewidzi.
- **Propozycja:** Zostaje model **dla każdego kraju osobno**, ale:
  1. **mało zmiennych**:
     - własne statystyki z poprzedniego roku;
     - **agregaty innych krajów** zamiast każdego kraju osobno, np. średni wzrost sąsiadów, średnia stabilność sojuszników, presja mocarstw ważona `real power towards`, liczba wojen wokół;
  2. **regularyzacja** (ridge/lasso), która automatycznie wycisza słabe zmienne;
  3. **backtest** (uczymy do 2015, sprawdzamy 2016–2025) decyduje, ile zmiennych model może mieć.

  Bez efektów losowych, zgodnie z R1: kraj zachowuje się wyłącznie według swoich danych i relacji.
- **Decyzja:** Ale nie nie. Nie zrozumieliśmy się!

  Regresja jest jedna! (no dwie są, bo jedna jest na wszystkie interakcje między państwami, a druga na wszystkie państwa).

  Chodzi mi o to że regresja ma jako dane oddzielnie krok czasowy każdego państwa, a nie że każde państwo ma własną.

  Innymi słowy: POL-1990 -> POL-1991 to jedno przejście czasowe. Ta sama regresja trenuje się i na POL i na GER i jakimkolwiek innym państwie i jego przejściach czasowych.

### U2. 🔴 Jak przewidywać relacje (R2: "wszystkie dane państwa, w tym relacje")
- **Problem:** Relacje skierowane jednego kraju to 6 × 195 wartości na rok. Osobny model dla każdej pary (A→B) miałby 35 obserwacji, a modeli byłoby 230 tysięcy.
- **Propozycja:** **Jeden model na kraj A i typ relacji**, w którym obserwacją jest para (A→B) w danym roku (35 × 195 ≈ 6800 obserwacji). Zmienne: wartość A→B z poprzedniego roku, wartość B→A, statystyki B, granica, wojna, sojusz. Relacje dwustronne (`in war`, `in war crisis`) przez model zdarzeń (R4).
- **Decyzja:** Generalnie się zgadzam z tym rozwiązaniem, jako że chyba już o nim pisałem, to proszę o podsumowanie tego w wątku.

### U3. 🔴 Liczba scenariuszy: rozgałęzianie wybucha
- **Problem:** Decyzja R3: z każdego scenariusza wychodzi N (albo N/10, albo √N) kolejnych.
  - **Rozgałęzianie:** przy N = 10 000 i horyzoncie 4 lat to 10 000⁴ = **10¹⁶** ścieżek; nawet N/10 daje 10¹². Tego nie da się policzyć.
  - **Pamięć:** jeden scenariusz to ok. **310 tys. wartości na rok**, prawie wszystko relacje. 10 000 scenariuszy to ok. **25 GB na każdy rok** (float64).
- **Propozycja:**
  - **Rozgałęzianie z przycinaniem:**
    - z każdego scenariusza wychodzi `b` dzieci (z pliku konfiguracyjnego, np. 10);
    - potem losowo zostawiamy N scenariuszy na kolejny rok ("filtr cząsteczkowy");
    - liczba żywych scenariuszy jest stała (N), a rozgałęzianie nadal działa;
    - `b = 1` to klasyczne Monte Carlo.
  - **Relacje rzadko:** symulujemy tylko pary, które mają wartość różną od domyślnej albo dotyczą krajów Tier 1/2; reszta zostaje na wartości domyślnej. To zmniejsza pamięć mniej więcej 10–50 razy.
  - **float32** zamiast float64 (2× mniej) i **obliczenia w paczkach** scenariuszy na kilku rdzeniach (Twoja sugestia o wielowątkowości), np. 8 rdzeni × paczki po 1250.
- **Decyzja:** Float32 - tak.
  Relacje Rzadkie - Można o tym pomyśleć jako opcji w ustawieniach.
  Rozpisz mi w wątku to Rozgałęzienie z przycinaniem.

  Dodatkowo, liczba scenariuszy powinna rosnąć wykładniczo a nie że jest ciągle po 10 000, bo od każdego scenariusza powinno wychodzić N scenariuszy. (można zmniejszyć te liczbę do 100?) a nie że mamy cały czas tyle samo ich.

  Pamiętaj że scenariusze się nie przecinają, a my możemy je zapisać jakoś sprytnie by ważyły mniej - można robić pojedyncze linie scenariuszy a nie wszystkie razem.

### U4. 🟡 Tury w obrębie roku (R2, R3, @T007)
- **Problem:** Kryzys w jednym kraju ma od razu działać na inne (R2). Przy kroku rocznym zwykła regresja widzi skutek dopiero rok później.
- **Propozycja:**
  - Każdy rok liczymy w **K turach** (z konfiguracji, domyślnie 3):
    1. tura 1: każdy kraj liczy zmianę ze swoich danych z poprzedniego roku;
    2. tury 2..K: kraj dostaje "wstrząs" od sąsiadów i partnerów, ważony relacjami (granice, `real power towards`, sojusze), z wyników poprzedniej tury.
  - Zdarzenia (np. `riots`, `in war crisis`) w turze k podnoszą prawdopodobieństwo zdarzeń u sąsiadów w turze k+1.
  - Skąd siła rozlewania się: z danych historycznych, przez porównanie zmian sąsiadów w tym samym roku (w ekonometrii to model "przestrzenny"). Szczegóły w @T007.
- **Decyzja:** Już chyba na to odpowiadałem? Tury mają być 2.

  Jedna na regresje wewnętrzną, druga na regresje zewnętrzną.

### U5. 🟢 Plik konfiguracyjny silnika
- **Propozycja:** `simulator/scenarios/<scenariusz>/engine.toml`, czytany przez standardowy `tomllib` Pythona:
  ```toml
  horizon_years = 4
  n_scenarios = 10000
  branching = 10            # dzieci każdego scenariusza na rok; potem przycięcie do n_scenarios
  turns_per_year = 3
  noise = "historical"      # fixed | historical | bootstrap — patrz @T008
  noise_fixed_share = 0.02  # dla "fixed": odsetek zakresu statystyki
  workers = 8               # rdzenie
  seed = 42                 # powtarzalność
  ```
- **Decyzja:** Obawiam się że coś jest nie tak z formatowaniem w przeglądarce - napraw to!

---

## Otwarte z rundy 0

R6–R9 i S1–S3 w `agents-issues-0.md` nadal czekają (zadanie @A12). R5 (szum) rozpisany w wątku @T008, jak prosiłeś.
