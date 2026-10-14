# Phase 1.2b — Wypełnienie danych opisowych przez LLM: pytania przed startem (agents-issues-0)

Decyzja autora (@T009, @A23): bez wskaźnika "wypełnione/niewypełnione"; **całe 1.2b przed Phase 2.1, uzupełniamy wszystkie wartości**. Poniżej to, co trzeba ustalić, zanim agenci zaczną. Format: **Problem / Propozycja / Decyzja**. Numeracja `P…`. Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

Stan dziś (`python -m simulator missing`): statystyki kraju 17 × 6 956 komórek (196 państw × lata istnienia). Wypełnione tylko te z wartościami startowymi (`stability`, `corruption`, `civilization level`, `net migration`). Relacje: 0–2% wypełnione.

---

## P. Zakres i sposób pracy

### P1. 🔴 Co znaczy "uzupełnić wszystkie wartości"?
- **Problem:** Statystyki kraju to ~95 tys. pustych komórek, do zrobienia. **Relacje to ~12 mln komórek** (196 × 195 par × 36 lat × 11 relacji). Dla ogromnej większości par, np. Boliwia → Mongolia, prawdziwa odpowiedź to "brak relacji" = wartość domyślna 0. Wpisywanie milionów zer nic nie wnosi, a zajmuje miejsce i czas.
- **Propozycja — "kompletne" znaczy, że każda wartość jest albo wpisana, albo świadomie potwierdzona jako domyślna:**
  - **Statystyki kraju bez wartości domyślnej** (`stability`, `corruption`, `happiness`, `revanchism`, `government popularity`, `social sensitivity`, `civilization level`, `immigration`, `emigration`, `assimilation`): wpisane dla **każdego** państwa i roku.
  - **Statystyki kraju z wartością domyślną** (flagi 0/1, `war exhaustion`, `net migration`): wpisane tam, gdzie coś się działo; reszta potwierdzona jako domyślna.
  - **Relacje:** dla każdego państwa agent ustala listę **partnerów, z którymi relacja jest istotna** (zwykle 10–40: sąsiedzi, mocarstwa, sojusznicy, wrogowie, partnerzy handlowi) i wypełnia te pary. Dla pozostałych **jedną operacją potwierdza wartość domyślną**. To nowa komenda `confirm-default`, która zapisuje potwierdzenie w changelogu, bez fizycznego wpisywania zer.
  - Silnik używa wartości domyślnej dla niewypełnionych (jak dziś `effective_values`), więc wyniki są takie same jak przy wpisanych zerach.
- **Decyzja:** Proszę o wątek jakie zmiany zamierzasz tutaj wprowadzić, bo nie rozumiem o co tobie chodzi.

### P2. 🔴 Skala, jednostka pracy, koszt
- **Problem:** To największa praca w projekcie i trzeba ją świadomie zaplanować.
- **Propozycja:**
  - **Jednostka pracy = jedno państwo**, w dwóch zadaniach:
    - (a) wszystkie statystyki kraju 1990–2025, opisane okresami (krzywe) zamiast rok po roku;
    - (b) relacje tego państwa do jego istotnych partnerów + potwierdzenie domyślnych.
  - Razem **~392 zadania** (196 × 2) + przeglądy.
  - **Szacunek** (bardzo zgrubny, z wyszukiwaniem w prasie): 30–60 minut pracy agenta na zadanie, czyli **200–400 godzin agentów**. Przy 5–10 agentach równolegle to dni do kilku tygodni. Koszt tokenów jest znaczący. Proszę o decyzję o budżecie i liczbie agentów naraz.
  - **Kolejność:** najpierw kraje referencyjne (kalibracja skali, Twój przegląd na mapie, @A6), potem Tier 1, potem reszta. Skończone będzie wszystko, zgodnie z Twoją decyzją, ale ważne kraje będą gotowe najwcześniej.
- **Decyzja:** Nie możemy użyć jakiegoś ultra taniego modelu? np haiku? Proszę o wątek w tej sprawie. 

  Agenci mogą czytać same nagłówki na przykład.

### P3. 🟡 Co musi być gotowe przed startem
- **Propozycja:**
  1. **Opisy statystyk przejrzane przez Ciebie** (@A4). LLM-y będą się na nich opierać przy każdej liczbie, a dziś kilka jest moich i niepewnych (`social sensitivity`, ujemna połowa skali subordination/power). Proponuję przenieść A4 do WAŻNYCH.
  2. **Instrukcja dla agentów wypełniających** (@L8):
     - wyszukiwarka i zapis źródeł (`--sources`);
     - prasa lokalna dla ważnych krajów;
     - media państwowe = postawa oficjalna, nie nastroje;
     - kotwice z krajów referencyjnych;
     - format batch;
     - `--dry-run` → `validate` → `review`.
  3. **Narzędzia:**
     - `confirm-default` (P1);
     - `missing --by-country` (postęp per państwo);
     - lista zadań 1.2b do brania przez agentów (np. `AGENTS/phases/phase-1.2b/queue.md`: państwo, zadanie, status, agent).
- **Decyzja:** Okej, jeżeli chcesz to zrobić to okej, jeżeli uważasz że jakieś statystyki są niejasne, podaj je w następnej serii `agents-issues-*.md`

  Generalnie Proszę o dokładny raport z Instrukcji dla agentów wypełniających

### P4. 🟡 Kontrola jakości
- **Propozycja:**
  - **przegląd przez drugiego agenta**: każde państwo czyta inny agent, sprawdza ostrzeżenia `review`, uzasadnienia i źródła;
  - **Twoje wyrywkowe sprawdzenie** krajów referencyjnych na mapie (`reference-map`);
  - **wartości startowe z prawdziwych wskaźników** zostają, a odchylenia ponad 15 punktów wymagają uzasadnienia (Y2).
- **Decyzja:** Nie do końca tak musi być, możemy wyłączyć uzasadnienia oraz źródła.

### P5. 🟢 Wcześniejsze ustalenia, które trzeba uwzględnić
- 111 par UCDP poziomu 1 w `in war crisis` do przejrzenia (@L15) — część zadań (b).
- `economic dependence` i `state collapse` (nowe) — bez wartości startowych, w całości z prasy.
- **Decyzja:** Zgoda.
