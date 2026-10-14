# T016 · Wycena propozycji 1.2b z ograniczeniami

*Odgałęzienie od: T012*

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Ponowna wycena mojej propozycji z @T012 (test → Haiku wypełnia + Sonnet przegląda → wariant B → tryb pełny tylko dla ważnych krajów), z jawnymi założeniami i ograniczeniami. Ceny API Anthropic z dokumentacji (2026-10-14).

**Wycena etapami (ceny API):**

| Etap | Założenia | Koszt |
|---|---|---|
| 1. Test modeli (@T015) | 10 krajów × 3 modele × 2 powtórzenia, bez wyszukiwarki | ~5 $ |
| 2. Wypełnianie — Haiku, wariant B | 392 zadania; ~5 wyszukiwań/zadanie (tylko 2023–2025); ~160 tys. tokenów wejścia i ~30 tys. wyjścia (z myśleniem) na zadanie | ~12 $ tokeny + ~20 $ wyszukiwania |
| 3. Tryb pełny dla krajów Tier 1 | 25 krajów × 2 zadania: +10 wyszukiwań, uzasadnienia i źródła | ~6 $ |
| 4. Przegląd — Sonnet | 392 przeglądy, każdy czyta gotowe liczby z uzasadnieniami (~15 tys. tokenów) i pisze uwagi | ~27 $ |
| 5. Poprawki po przeglądzie | ~20% zadań ponownie (Haiku) | ~6 $ |
| **Razem** | | **~75–80 $** (gorszy przypadek ~105 $) |

Dla porównania, samo wypełnianie (etap 2) innym modelem zamiast Haiku: **Sonnet ~160 $, Opus ~300 $**.

**Ograniczenia i ryzyka wyceny:**
1. **Zgrubne założenia o tokenach.** Liczba tokenów na zadanie to szacunek; realnie może być ±50%. Dlatego po pierwszych ~10 zadaniach zmierzę faktyczne zużycie i przeliczę.
2. **Próg Haiku 100 tys. tokenów:** zapytanie dłuższe niż 100 tys. tokenów kosztuje 5 razy więcej. Długie pętle agenta mogą go przekraczać; to jest "gorszy przypadek" (~105 $). Zapobiega temu krótka pętla: jedno państwo na zadanie, bez czytania całych artykułów.
3. **Wyszukiwarka przy Haiku jest prostsza:** bez filtrowania wyników, które mają Sonnet i Opus, więc trafia więcej tekstu. Założenia już to podwajają.
4. **Bez oszczędności z pamięci podręcznej** (powtarzana instrukcja i opisy statystyk byłyby ~10× tańsze przy kolejnych zapytaniach). Wycena jest więc raczej zawyżona.
5. **Tryb wsadowy (−50%) nie wchodzi w grę** dla pętli agenta krok po kroku, więc go nie liczę.
6. **Limity szybkości API:** ile agentów naraz zależy od poziomu konta; to wpływa na czas, nie na koszt.
7. **Wariant B opiera się na wiedzy modelu** dla lat do 2022. Przy małych krajach i latach 90. ta wiedza jest słabsza, a Haiku zna mniej niż Sonnet. Właśnie to ma pokazać test.
8. **Jeśli agentami będą sesje Claude Code w ramach Twojego planu** zamiast API, nie płacisz za tokeny, tylko zużywasz limity planu. Przy ~800 zadaniach (wypełnianie + przegląd) trzeba je rozłożyć na wiele dni.
9. **Potrzebny jest program uruchamiający agentów** (kolejka → zadanie → batch → `validate`), który muszę napisać przed startem. Jego koszt to moja praca, nie tokeny.

**Podsumowanie:** propozycja kosztuje **~75–105 $ przez API** (z czego najwięcej przegląd Sonnetem i wyszukiwania), czyli wyraźnie taniej niż wypełnianie Sonnetem (~160 $ + przegląd) czy Opusem (~300 $).

*2026-10-14 06:21 — Claude Opus 5.5*

---
---
---

Dobra, co ty na to aby wyrzucić 4. oraz 5. ? Jak widzisz taką sytuację?

*2026-10-14 06:40 — Autor*

---
---
---

**Opinia (bez działania)** o wyrzuceniu etapów 4 (przegląd Sonnetem) i 5 (poprawki po przeglądzie):

**Liczby:**
- etap 5 zależy od 4: bez przeglądu nie ma czego poprawiać, więc wyrzucenie 4 usuwa też 5;
- oszczędność: ~27 $ + ~6 $ = **~33 $**, czyli koszt spada z ~77 $ do **~44 $** (−43%).

**Co tracimy:**
- drugie spojrzenie na statystyki **bez obiektywnego odniesienia** (`social revanchism`, `government revanchism`, `social sensitivity`, relacje). Dla nich test niczego nie sprawdził;
- wyłapanie **systematycznych błędów** Haiku (jak przesunięcie +17 w `stability` z testu, tylko że tam akurat była to różnica definicji).

**Co zostaje nawet bez przeglądu (za darmo):**
- `validate`: zakresy, istnienie państw, symetria;
- `review`: skoki ponad 25% zakresu w rok i odchylenia o ponad 15 punktów od wartości startowych (`violence risk`, `corruption`, `civilization level`, `happiness`);
- Twoje wyrywkowe sprawdzenie na mapie (`reference-map`).

**Moje zdanie:**
- wyrzucenie pełnego przeglądu jest rozsądne, bo test pokazał, że Haiku jest stały i dobrze ustawia kolejność krajów;
- zostawiłbym jednak **przegląd próbki**: tylko kraje referencyjne i Tier 1 (~40 państw, ~80 zadań). Koszt to ~6 $ + ~2 $ poprawek, czyli razem **~52 $** zamiast ~77 $. Te kraje najbardziej ważą w modelu Polska–Rosja;
- do tego mogę zrobić automatyczne porównanie wyników dla wszystkich krajów (rozkłady, kolejność względem PKB, HDI, WGI), za darmo, bo to tylko obliczenia.

Decyzja należy do Ciebie (@A31): wyrzucamy całkiem, zostawiamy próbkę, czy zostaje jak było?

*2026-10-14 06:43 — Claude Opus 5.5*

---
---
---

zostawiamy próbkę, zrób automatyczne porównywanie wyników dla wszystkich krajów. Powiem ci kiedy masz uruchomić agentów na claude code.

*2026-10-14 06:46 — Autor*

---
---
---

Przyjęte: **przegląd próbki** (kraje referencyjne + Tier 1). Agentów Claude Code **nie uruchamiam**, dopóki nie dasz znać.

**Automatyczne porównanie wszystkich krajów jest gotowe**: `python -m simulator --scenario world-1990-2025 audit`. Tylko liczy, niczego nie zmienia w danych.
1. **Zgodność ze wskaźnikami.** Dla każdej statystyki z odniesieniem w prawdziwych danych sprawdza, czy kolejność krajów się zgadza; skala od −1 do 1, gdzie 1 = ta sama kolejność. Odniesienia są w `simulator/scenarios/world-1990-2025/audit.csv` i możesz je zmieniać. Przykłady:
   - `corruption` ↔ CPI i WGI;
   - `civilization level` ↔ HDI i PKB na mieszkańca;
   - `happiness` ↔ Cantril;
   - `violence risk` ↔ WGI;
   - `stability` ↔ PKB na mieszkańca (luźno);
   - siła wpływu (`real power towards`) ↔ PKB;
   - `economic dependence` ↔ PKB (odwrotnie).
2. **Kraje odstające**, których średnia pozycja różni się od wskaźnika o ponad 40% skali. To lista do przejrzenia w próbce albo do poprawki.
3. **Płaskie linie**: ta sama wartość we wszystkich latach, czyli oznaka bezmyślnego przepisania.
4. **Zatłoczenie**: jedna wartość u ponad połowy krajów w danym roku, czyli oznaka zgadywania.

**Pierwszy raport** (przed wypełnianiem, jako punkt odniesienia): `AGENTS/phases/phase-1.2b/audit/audit-2026-10-14-0650.md`. Wartości startowe zgadzają się ze swoimi wskaźnikami (0,93–1,00), co jest oczywiste. Prawdziwą wartość narzędzie pokaże po wypełnieniu przez Haiku.

*2026-10-14 06:50 — Claude Opus 5.5*

---
---
---

Uruchom.

*2026-10-14 06:54 — Autor*

---
---
---

**Start wstrzymany: brak uprawnienia.** Przygotowałem pilota: Polska, zadania A i B, dwóch agentów Haiku naraz, prompt w `AGENTS/phases/phase-1.2b/prompt-agenta.md`. Claude Code (tryb automatycznych uprawnień) **zablokował uruchomienie agentów**, bo zapisywaliby wspólne dane scenariusza. Nic nie zostało zapisane, a kolejka jest bez zmian.

Żeby ruszyć, potrzebuję Twojej zgody w Claude Code na narzędzie `Agent` (uruchamianie podagentów). Do wyboru:
1. przełącz tryb uprawnień z automatycznego na zwykły (pytanie przy każdym uruchomieniu) i zatwierdź pilota;
2. albo dodaj `"Agent"` do `permissions.allow` w `.claude/settings.local.json`.

Potem napisz „uruchom” jeszcze raz. Plan, gdy już ruszy:
- **pilot** (POL A+B): sprawdzę zapis, `validate`, `review` i zużycie tokenów;
- **pozostałe 14 krajów referencyjnych** (28 zadań, partiami);
- **przerwa na Twój przegląd na mapie** (@A6), potem Tier 1 i reszta.

*2026-10-14 06:57 — Claude Opus 5.5*

---
---
---

**Wypełnianie 1.2b skończone.** Wszystkie 392 zadania (196 państw × statystyki i relacje), 20 agentów Haiku naraz.
- `missing` 100%, `validate` 0 błędów; 395 batchy, 51 407 operacji w `AGENTS/phases/phase-1.2b/batches/`.
- Przerwa 08:20–12:40: skończył się miesięczny limit wydatków API; przerwane zadania dokończone po wznowieniu.
- Audyt: `AGENTS/phases/phase-1.2b/audit/audit-2026-10-14-1312.md` — luki we wskaźnikach zgodne z danymi (0,93–1,00); `stability` 0,63–0,71; `economic dependence` bez związku z PKB (do sprawdzenia).
- Raport z przebiegiem i wszystkimi uwagami agentów: `AGENTS/phases/phase-1.2b/raport-wypelniania.md`.
- Decyzje dla Ciebie: `AGENTS/phases/phase-1.2b/agents-issues-2.md` (@phase-1.2b:K1 … @phase-1.2b:K8, @A33). Najważniejsze: wspólna reguła UCDP (@phase-1.2b:K1) i brakujące konflikty 1990–2024 (@phase-1.2b:K2). Po decyzjach: poprawki (@L40) i przegląd próbki (@A31).

*2026-10-14 13:15 — Claude Opus 5.5*

---
---
---

Dobra, gdzie zostały zapisane Dane?

*2026-10-14 13:29 — Autor*

---
---
---

To znaczy, pije do tego że powinniśmy mieć ich kopię zapasową.

*2026-10-14 13:29 — Autor*

---
---
---

**Gdzie są dane:**
- wartości: `simulator/scenarios/world-1990-2025/narrated/` (rocznie: `RRRR/internal-grades.csv`, `RRRR/relations-directed/*.csv`, `RRRR/relations-doublesided/*.csv`), historia zmian w `narrated/changelog.csv`, potwierdzone wartości domyślne w `narrated/confirmed-defaults.csv`;
- skąd wartości: batche agentów w `AGENTS/phases/phase-1.2b/batches/` (395 plików) i koordynatora w `AGENTS/phases/phase-1.2b/batches-koordynator/`. Z batchy da się odtworzyć dane od zera (`python -m simulator batch`).

**Kopia zapasowa — zrobiona:** `/home/karol/Pulpit/Python3.14/economics-model-backups/phase-1.2b-2026-10-14-1353.tar.gz` (4,4 MB, `narrated/` + cały `AGENTS/phases/phase-1.2b/`), poza projektem.

**Ważne:** nic z tego nie jest jeszcze w gicie (ostatni commit: „pre 1.2b”). Polecam commit teraz — to najlepsza kopia, z historią. Zrobię go, jeśli napiszesz „commit” (sam z siebie nie commituję).

*2026-10-14 13:56 — Claude Opus 5.5*

---
---
---
