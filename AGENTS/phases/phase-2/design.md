# Silnik symulacji — projekt (Phase 2.0, wersja 0)

Zebrane decyzje autora z `agents-issues-0.md` (R1–S3), `agents-issues-1.md` (U1–U5) i wątków @T007, @T008, @T009, @T010. Na tym dokumencie powstaje Phase 2.1. Zmiany projektu: tylko po decyzji autora; ten plik aktualizuje agent, z datą na dole.

---

## 1. Co powstaje

Program, który na podstawie danych 1990–2025 uczy się, jak państwa zmieniają się z roku na rok. Potem z ostatniego roku (H_last) generuje drzewo przyszłych scenariuszy, czyli możliwych przyszłości z szumem. Wynik to **wszystkie scenariusze** (S1); narzędzia do analizy zbiorczej (prawdopodobieństwa zdarzeń, rozkłady statystyk w czasie) powstaną później.

## 2. Stan państwa w roku

- **Statystyki prawdziwe** (`history/`): PKB, populacja, WGI, HDI, CPI, szczęście, migracje. Także **pochodne** (R2): zmiana i tempo zmiany, logarytm, na mieszkańca.
- **Statystyki opisowe** (`narrated/internal-grades`): 17, w tym nowa `state collapse` (S2).
- **Relacje** do każdego innego państwa: 7 skierowanych (w tym nowa `economic dependence`, @T007) i 4 dwustronne (`in war`, `in war crisis`, `in hybrid war`, `neighbours`).

Silnik przewiduje **wszystko** z powyższych na rok następny (R2).

## 3. Dwie regresje (U1, R6)

Obie są **wspólne dla wszystkich państw**. Obserwacją jest jedno przejście czasowe, np. POL 1990 → POL 1991. Nie ma efektów stałych ani losowych kraju (R1): kraj zachowuje się wyłącznie według swoich danych i relacji.

| | Regresja wewnętrzna (I) | Regresja zewnętrzna (E) |
|---|---|---|
| obserwacja | państwo A, rok t → t+1 (~196 × 35 ≈ 6 900) | para skierowana A→B, rok t → t+1 (~38 000 × 35) |
| wejście | stan A w roku t | relacje A→B i B→A w roku t, stan A i B (po turze 1) |
| wyjście | stan A w t+1 (wszystkie statystyki ciągłe) | zmiana relacji A→B oraz **wkład do zmian A i B** (R6) |

Wkład z regresji E sumuje się po wszystkich partnerach i dodaje do wyniku regresji I. Siła wpływu zależy od relacji, zwłaszcza `economic dependence`, `neighbours`, `real power towards`.

## 4. Dwie tury w roku (U4, @T007)

1. **Tura 1 — wewnętrzna:** regresja I, każde państwo osobno, na podstawie własnego stanu.
2. **Tura 2 — zewnętrzna:** regresja E na wynikach tury 1. Kryzys w jednym państwie od razu (w tym samym roku) wpływa na partnerów, proporcjonalnie do zależności.

## 5. Zdarzenia 0/1 (R4, S2, @T007)

`riots`, `epidemic`, `mobilized`, `immigration crisis`, `state collapse`, `in war`, `in war crisis`, `in hybrid war`:
- obie regresje dają dla nich **prawdopodobieństwo** (regresja logistyczna), a scenariusz losuje, czy zdarzenie zaszło;
- **rozlewanie się zdarzeń wynika z regresji E** (tura 2), nie z ręcznego skryptu (@T007);
- `state collapse` działa jak każda zmienna: wpływa na państwo w turze 1 i na sąsiadów w turze 2 (S2).

## 6. Scenariusze (R3, R4, U3, @T010)

- Krok = 1 rok, horyzont z konfiguracji (domyślnie 4 lata).
- **Drzewo:** z każdego scenariusza wychodzi `b` scenariuszy-dzieci. Każde dziecko = przewidywanie z rodzica + szum (R4). Liczba scenariuszy rośnie wykładniczo (U3): b, b², b³, b⁴.
- `b` z konfiguracji, osobno dla każdego roku. Domyślnie `[10, 10, 10, 10]`, co daje **10 000 scenariuszy końcowych** (przyjęte, @T010; inne warianty: `AGENTS/plan/future-work.md`, punkt 4).
- **Zapis jako drzewo:** węzeł = dane jednego roku + numer rodzica. Pojedynczą "linię" scenariusza odtwarza się, idąc po rodzicach. Wspólne początki nie są powielane.
- **Rozmiar** (horyzont 4, float32, relacje rzadkie = ~5% par):

  | b | węzły | końcowe scenariusze | rozmiar |
  |---|---|---|---|
  | 5 | 780 | 625 | ~0,1 GB |
  | **10** | **11 110** | **10 000** | **~1 GB** |
  | 20 | 168 420 | 160 000 | ~15 GB |
  | 100 | 101 mln | 100 mln | ~9 TB (niewykonalne) |

  Z gęstymi relacjami rozmiary są ~15 razy większe.
- **float32** (U3). **Relacje rzadkie**, czyli tylko pary z wartością inną niż domyślna, jako opcja w konfiguracji (U3).
- Obliczenia w paczkach węzłów na kilku rdzeniach (R3).

## 7. Szum (R5, @T008)

Opcje w konfiguracji: `fixed` (stały odsetek zakresu), `historical` (typowy błąd modelu dla kraju i statystyki), `bootstrap` (błędy wszystkich krajów z losowego roku historii, czyli wspólne kryzysy). **Domyślnie: `bootstrap` + mały stały szum.**

## 8. Uczenie i sprawdzanie (R8)

- Lata uczenia i lata sprawdzania w konfiguracji, np. uczenie 1990–2015, sprawdzanie 2016–2025.
- Model podaje **prawdopodobieństwa i rozkłady**, nie pewność. Sprawdzamy więc kalibrację: czy zdarzenia z prognozą 20% zachodzą w ~20% przypadków i czy prawdziwe wartości mieszczą się w rozkładach.
- Porównanie z prostymi modelami odniesienia ("jak w zeszłym roku").

## 9. Dane opisowe do nauki (R7, R9, @T009)

Decyzja autora: **bez wskaźnika "wypełnione/niewypełnione"**. Przed Phase 2.1 robimy całe Phase 1.2b i uzupełniamy wszystkie wartości. Co znaczy "uzupełnione" dla relacji, ustala `AGENTS/phases/phase-1.2b/agents-issues-0.md` (P1). Silnik czyta dane przez wartości domyślne wzorów (`effective_values`).

## 10. Technologia (S3)

- **numpy (float32)**:
  - własna implementacja regresji liniowej z regularyzacją (ridge) i logistycznej;
  - przewidywanie to mnożenie macierzy, więc szybkie;
  - `multiprocessing` na paczki węzłów.
- `statsmodels` tylko do diagnostyki (istotność zmiennych); bez scikit-learn.
- Moduł `simulator/engine/`, CLI `python -m simulator engine train|run`, testy jak w Phase 1.

## 11. Konfiguracja `simulator/scenarios/<scenariusz>/engine.toml` (U5)

```toml
train_years = [1990, 2015]      # R8
test_years  = [2016, 2025]      # R8
horizon_years = 4               # R3
branching = [10, 10, 10, 10]    # U3: dzieci każdego scenariusza w kolejnych latach
turns_per_year = 2              # U4: wewnętrzna + zewnętrzna
noise = "bootstrap"             # R5: fixed | historical | bootstrap
noise_fixed_share = 0.01        # stały szum (fixed albo dodatek do bootstrap)
sparse_relations = true         # U3: tylko pary z wartością inną niż domyślna
dtype = "float32"               # U3
workers = 8                     # R3: rdzenie
seed = 42                       # powtarzalność
```

---

*Wersja 0: 2026-10-14 04:10 — Claude Opus 5.5; wersja 1 (decyzje A23, A24): 2026-10-14 05:13 — Claude Opus 5.5*
