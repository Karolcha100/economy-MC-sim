# Phase 1.2 — Propozycje efektywnego wypełniania danych opisowych przez LLM

Odpowiedź na decyzję J1 w `AGENTS/phase-1/agents-issues-2.md`. Na końcu są pytania do autora.

---

## 1. Skala problemu

Scenariusz `world-1990-2025`: 195 państw, 36 lat.

| Rodzaj | Komórek (ok.) | Czy LLM da radę "komórka po komórce"? |
|---|---|---|
| Internal grades (15 statystyk) | ~105 tys. | na granicy |
| Relations directed (6) | ~8,2 mln | nie |
| Relations double-sided (3) | ~2 mln (z symetrii połowa) | nie |

Wniosek: LLM nie może wypełniać komórek. Ma opisywać **okresy** (krzywe), **zdarzenia** i **ważne pary krajów**, a resztę mają pokryć wartości domyślne (H4) i dane z prawdziwych źródeł.

---

## 2. Propozycje

### P1. Nie każ LLM-owi zgadywać tego, co da się zmierzyć

Część statystyk ma dobre, publiczne odpowiedniki. Proponuję zaimportować je jako **dane historyczne** (`history/`) i na ich podstawie skryptem wygenerować **wartości startowe**, które LLM tylko koryguje i uzupełnia tam, gdzie danych brakuje (np. lata przed 1996):

| Statystyka | Źródło | Zakres lat |
|---|---|---|
| `neighbours` | Correlates of War — Direct Contiguity (granice lądowe) | cały okres, **bez LLM** |
| `in war` | UCDP/PRIO Armed Conflict / UCDP Dyadic Dataset | 1946–2024 |
| `corruption` | WGI Control of Corruption, TI CPI | 1996+ / 1995+ |
| `stability` | WGI Political Stability and Absence of Violence | 1996+ |
| `civilization level` | UNDP Human Development Index | 1990+ |
| `happiness` | World Happiness Report (Gallup) | 2005+ |
| `immigration` / `emigration` | UN DESA International Migrant Stock, WB net migration | co 5 lat / roczne |
| `diplomatic relation towards` (wskazówka) | UN General Assembly voting agreement (Voeten) | 1946+ |

Zalety: mniej halucynacji, spójna skala między krajami, a LLM zajmuje się tylko tym, co naprawdę opisowe (revanchism, war exhaustion, perceived power, social view…).

### P2. Priorytety krajów (tiery)

- **Tier 1 (~25 krajów)** — rdzeń modelu PL–RU: POL, RUS, UKR, BLR, LTU, LVA, EST, MDA, GEO, DEU, FRA, GBR, USA, CHN, FIN, SWE, CZE, SVK, HUN, ROU, TUR, KAZ, ARM, AZE, ITA. Pełne internal grades i **wszystkie relacje skierowane między nimi** (25 × 24 = 600 par).
- **Tier 2 (~40)**: reszta Europy, G20, kluczowe państwa Bliskiego Wschodu. Internal grades w grubszych okresach, relacje tylko **wobec Tier 1** (i od Tier 1 do nich).
- **Tier 3 (reszta)**: internal grades z P1 + korekta regionalna, relacje = wartości domyślne.

To redukuje relacje skierowane z ~37,8 tys. par do ~2,6 tys. (600 + 40 × 25 × 2), czyli ~1 300 zadań (nieuporządkowanych par A–B) zamiast milionów komórek.

### P3. Okresy zamiast lat

Agent opisuje każdą statystykę kraju jako **3–8 okresów** w latach 1990–2025 (np. "1991–1994 transformacja: stability 40→55, logistic"). Jedna linia JSON na okres, a narzędzie `set`/`batch` samo rozpisuje lata. Szacunek dla internal grades: 195 krajów × 11 statystyk ciągłych × ~5 okresów ≈ **10 tys. operacji**, zamiast 105 tys. komórek.

### P4. Jednostka pracy jednego agenta

- **Kraj** → wszystkie internal grades jednego kraju w jednym zadaniu (spójny obraz kraju), wynik = 1 plik batch.
- **Para krajów (A, B)** → wszystkie relacje A→B i B→A w jednym zadaniu, bo agent widzi wtedy asymetrię (np. `real power towards` POL→RUS ≠ RUS→POL, zgodnie z G1).
- **Zdarzenia** (flagi 0/1: `riots`, `epidemic`, `mobilized`, `immigration crisis`, `in hybrid war`) → osobne zadanie "globalna lista zdarzeń" na okres, np. jedna lista wszystkich mobilizacji 1990–2025. Tak łatwiej o kompletność i spójny próg "poważności" (I2).

### P5. Kalibracja skali (żeby 70 znaczyło to samo u każdego agenta)

1. Najpierw wypełnić **5–8 krajów referencyjnych** (np. POL, RUS, UKR, DEU, USA, CHN, SOM, CHE).
2. **Ty je przeglądasz** i poprawiasz.
3. Stają się **kotwicami** w każdym kolejnym zadaniu: agent dostaje wartości referencyjne ("stability: CHE 2010 = 95, POL 2010 = 75, UKR 2014 = 30, SOM 1995 = 5") i ma się do nich odnosić.

Uzupełnieniem są opisy skal w kolumnie `description` wzorów (już dodane; trzeba je przejrzeć, patrz `agents-issues-3.md`).

### P6. Dwa przebiegi: wypełniający i recenzent

- **Agent wypełniający** tworzy batch z `rationale` (wydarzenia, lata, źródła), robi `--dry-run` i zapisuje.
- **Agent recenzent** (inna instancja) dostaje batch i `show`, szuka skoków rok do roku, odstępstw od P1 i kotwic oraz niezgodnych uzasadnień. Zgłasza uwagi, ale nie poprawia danych sam.
- **Ty** robisz wyrywkową kontrolę Tier 1. `narrated/changelog.csv` pozwala ustalić, kto i dlaczego wpisał daną wartość.

### P7. Narzędzia, które warto dodać przed startem (po Twojej akceptacji)

1. **Grupy krajów**: `groups.csv` (np. `EU`, `NATO`, `CIS`, `CSTO` z latami członkostwa) i cele typu `@NATO:RUS` oraz `POL:*`. Jedna operacja ustawia wtedy relację całego bloku. To też pierwszy krok do dynamicznych organizacji (E4).
2. **`context` — eksport kontekstu dla agenta**: zwięzły tekst z opisami statystyk, kotwicami, PKB kraju, istniejącymi wartościami i wartościami z P1. Mniej tokenów i mniej pomyłek.
3. **`review` — automatyczne ostrzeżenia**: duże skoki rok do roku, wartości daleko od danych z P1, brak `rationale`. Wyłącznie ostrzeżenia (zgodnie z G1).
4. **Import wskaźników z P1** w formacie, który już obsługuje `history import` (World Bank / szeroki CSV); dla UCDP, CoW i HDI trzeba dopisać mały konwerter.

### P8. Ograniczenia wiedzy LLM

- Lata 2024–2025 mogą być słabo znane modelom (data odcięcia wiedzy). Proponuję oznaczać w `rationale` niską pewność i w razie potrzeby dawać agentowi notatki od Ciebie o wydarzeniach z ostatnich lat.
- Lata 1990–1995 dla mniejszych państw: dane z P1 są tu skąpe. Wartości z tego okresu traktować jako najmniej pewne.

### P9. Kolejność prac (propozycja)

1. Przegląd opisów i wartości domyślnych (`agents-issues-3.md`).
2. Narzędzia P7 (grupy, context, review) oraz import danych z P1.
3. Kraje referencyjne (P5), a potem Twój przegląd.
4. Tier 1: internal grades, potem relacje par, potem zdarzenia.
5. Tier 2, potem Tier 3.
6. `validate` + `missing` jako raport postępu po każdym etapie.

---

## 3. Pytania do autora

1. Czy zgadzasz się na **P1**, czyli import prawdziwych wskaźników jako punktu startowego? Zmienia to podział "prawdziwe vs opisowe" dla części statystyk.
2. Czy lista **Tier 1** jest dobra? Co dodać lub usunąć?
3. Czy chcesz przeglądać **kraje referencyjne** (P5) przed dalszym wypełnianiem?
4. Które narzędzia z **P7** zrobić przed startem? Moja rekomendacja: wszystkie cztery, a grupy przede wszystkim.

## 4. Odpowiedzi dla LLMów

1. Tak, aczkolwiek myślałem nadtym aby uzupełniać część tych statystyk z artykułów prasowych w internecie (one mają być opisowe) - Generalnie chodziło mi o to że opisowe to takie odczucia społeczne raczej.

2. Nie wiem czym są te kraje, ale generalnie ufam że jest okej.

3. W sumie okej, ale poproszę to w formie skryptu w którym użytkownik wybiera państwa referencyjne z pliku .csv (możesz go uzupełnić o te - chociaż zastanów się jakie by były najlepsze) i które wyświetlają mu datę, lokalizację na mapie świata i daną wartość statystyki.

4. Zgadzam się.
