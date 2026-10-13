# M1 — Wskaźniki czy prasa? Wyjaśnienie i konsekwencje

Dotyczy decyzji M1 w `AGENTS/phase-1/agents-issues-4.md` ("Zgoda. Wyjaśnij mi ten punkt i jego konsekwencje").

*2026-10-13 23:29 — Claude Opus 5.5*

---

## 1. O co chodzi w jednym zdaniu

Każda statystyka opisowa dostaje **źródło pierwszej wersji wartości**: tam, gdzie istnieje porządny, publiczny wskaźnik, startujemy od niego. Tam, gdzie chodzi o **odczucia społeczne**, startujemy od prasy, a LLM w obu przypadkach poprawia i uzupełnia.

## 2. Trzy grupy statystyk

| Grupa | Statystyki | Skąd pierwsza wersja | Rola LLM |
|---|---|---|---|
| **A. Wskaźnik → start** | `stability`, `corruption`, `civilization level`, `immigration`, `emigration`, `in war`, `neighbours` | skrypt przelicza wskaźnik na skalę wzoru | koryguje, uzupełnia lata bez wskaźnika; `neighbours` bez LLM |
| **B. Prasa + kotwica** | `happiness`, `government popularity`, `social view towards` | LLM z prasy | wskaźnik/sondaż służy tylko do sprawdzenia, czy LLM nie odleciał |
| **C. Tylko prasa** | `revanchism`, `war exhaustion`, `social sensitivity`, `assimilation`, relacje dyplomatyczne i siły/zależności, flagi zdarzeń | LLM z prasy | całość |

Grupa C to właśnie "odczucia społeczne" z Twojej odpowiedzi. Grupa A to statystyki, które formalnie są opisowe, ale ktoś je już rzetelnie zmierzył, więc zgadywanie byłoby gorsze.

## 3. Jak to działa technicznie

1. **Surowy wskaźnik trafia do `history/`** w oryginalnych jednostkach, np. `history/wgi-political-stability.csv` (skala −2,5..2,5), z metadanymi źródła. To dane prawdziwe i nikt ich nie zmienia.
2. **Skrypt "seed"** przelicza wskaźnik na skalę wzoru i zapisuje go do `narrated/` jako zwykłą operację z `--author seed:wgi` i uzasadnieniem. Przykład: WGI −2,5..2,5 → `stability` 0..100. Changelog pokazuje wtedy, które wartości pochodzą ze wskaźnika, a które z LLM.
3. **LLM poprawia** wartości z grupy A tylko wtedy, gdy ma powód, i opisuje go w `rationale`. `review` dostanie nową kontrolę: ostrzeżenie, gdy wartość odbiega od wskaźnika o więcej niż X.

## 4. Konsekwencje

### Dobre
- **Mniej halucynacji i spójna skala**: `corruption` Polski i Nigerii pochodzi z tej samej metody, a nie z dwóch różnych rozmów z LLM.
- **Mniej pracy dla LLM**: grupa A pokrywa 5 z 15 statystyk wewnętrznych oraz `in war` i `neighbours` dla wszystkich par krajów.
- **Wskaźniki przydadzą się w Phase 2 bezpośrednio** jako prawdziwe zmienne regresji, niezależnie od danych opisowych.

### Na co uważać
- **Przeliczenie skali to decyzja, a nie fakt.** Np. HDI 0..1 → `civilization level` 0..100 można zrobić liniowo (HDI × 100) albo przez pozycję w rankingu (najlepszy kraj = 100). Przy każdym wskaźniku zapiszę wybór i jego powód, a sporne przypadki trafią do Ciebie.
- **Wskaźniki nie obejmują całego okresu**: WGI od 1996 (do 2002 co dwa lata), WHR od 2005, część HDI od lat 2000. Lata 1990–1995 i tak wypełni LLM, więc tam pewność będzie niższa.
- **Wskaźniki mają swoje definicje, inne niż nasze.** Przykład: UCDP koduje Rosja–Ukraina 2014–2021 jako konflikt wewnętrzny Ukrainy ze wsparciem Rosji, a nie jako wojnę między państwami. Seed dałby `in war` RUS:UKR = 0 dla tych lat, a nasz opis wzoru mówi 1 od 2014. **Takie miejsca LLM musi poprawić**, a `review` je wskaże.
- **Podwójne liczenie w Phase 2.** Jeśli regresja dostanie jednocześnie surowy WGI z `history/` i `stability` z niego wyliczone, to są prawie te same dane. Trzeba wybrać jedno; to będzie pytanie w planowaniu Phase 2.
- **Granica "prawdziwe vs opisowe" się zaciera.** Część danych opisowych będzie w dużej mierze prawdziwa. Changelog (`author = seed:...`) pozwala to zawsze rozdzielić.

### Konsekwencje dla części "prasowej" (grupy B i C)
- **Agenci potrzebują wyszukiwarki internetowej**, a to koszt (tokeny, czas). Zakres trzeba ograniczać priorytetami (tiery z propozycji P2).
- **Źródła muszą być zapisywane.** Wybrałem osobną kolumnę `sources` (URL, tytuł, data) w operacjach i w `changelog.csv`, zamiast wpychać linki do `rationale`. Artykuły znikają z sieci, więc sam tytuł i data też mają wartość.
- **Stronniczość źródeł:**
  - prasa anglojęzyczna inaczej opisuje Polskę i Rosję niż prasa lokalna, więc dla krajów Tier 1 warto czytać źródła w języku kraju;
  - media państwowe (np. rosyjskie) są dobrym sygnałem **oficjalnej postawy** (`diplomatic relation towards`), ale złym sygnałem **nastrojów społecznych** (`social view towards`);
  - zasady źródłowe trafią do instrukcji dla agentów wypełniających.
- **Powtarzalność:** dwa przebiegi LLM na tych samych artykułach dadzą trochę inne liczby. Kotwice (kraje referencyjne) i `review` ograniczają rozrzut, ale go nie usuwają.

## 5. Licencje (do sprawdzenia przed importem)

WGI (World Bank) i UCDP: CC BY 4.0. HDI (UNDP): CC BY 3.0 IGO. World Happiness Report: dane do użytku z cytowaniem. Correlates of War: darmowe do użytku z cytowaniem; warunki sprawdzę przed importem. Każde źródło dostanie wpis w `history/metadata.csv`.

## 6. Co z tego wynika dla kolejności prac

Import wskaźników (Phase 1.2a) to jedna sesja pracy agenta i przydaje się zarówno do wypełniania danych, jak i do Phase 2. Dlatego proponuję go jako **następny krok** (patrz `wymiana-zdan-A1.md`). Wypełnianie z prasy (grupy B i C) jest duże i może iść później, równolegle z Phase 2.
