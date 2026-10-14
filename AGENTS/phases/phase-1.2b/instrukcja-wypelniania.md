# Phase 1.2b — Instrukcja dla agentów wypełniających dane opisowe (zaakceptowana przez autora, A29)

*Statystyki zgodne z decyzjami Q1–Q8 (`agents-issues-1.md`). Plan i stan: `plan.md`.*

Tę instrukcję dostaje każdy agent, który wypełnia dane jednego państwa. Zaakceptowana (@A29); dwie sprawy **[DO DECYZJI]** zależą od wyboru modelu (@T015, @T016).

---

## 1. Twoje zadanie

Dostajesz **jedno państwo** (tag, np. `POL`) i **jedno z dwóch zadań**:

- **Zadanie A — statystyki państwa:** wszystkie statystyki wewnętrzne (`internal-grades`) za lata 1990–2025, w latach, w których państwo istnieje.
- **Zadanie B — relacje państwa:** relacje skierowane **od tego państwa** do jego istotnych partnerów + relacje dwustronne z jego udziałem.

Zadania bierzesz z kolejki `AGENTS/phases/phase-1.2b/queue.md` (wpisujesz się przy zadaniu, potem oznaczasz jako zrobione).

## 2. Zanim zaczniesz

1. `python -m simulator --scenario world-1990-2025 context POL`:
   - lata istnienia i grupy (NATO, UE…);
   - dane prawdziwe (PKB, WGI, HDI…);
   - obecne wartości;
   - **kotwice**, czyli wartości krajów referencyjnych.
2. `python -m simulator --scenario world-1990-2025 formulas list`: **opis każdej statystyki i jej skala**. Liczby muszą odpowiadać opisowi, nie Twojemu wyczuciu.
3. Konwencje scenariusza (lista państw, ZSRR = RUS, Jugosławia = SRB, Czechosłowacja = CZE, `exists_from`): `simulator/README.md`.

## 3. Źródła

- **Wyszukiwarka internetowa jest dozwolona** (decyzja autora). Do tego Twoja wiedza o historii.
- Szukaj **artykułów prasowych i opracowań**: wydarzenia, sondaże, nastroje.
- **[DO DECYZJI — @T012]** czy czytamy tylko wyniki wyszukiwania (tytuły i fragmenty), czy też całe artykuły; i czy dla lat dobrze znanych modelowi szukamy w ogóle.
- Zasady oceny źródeł:
  - dla krajów ważnych dla modelu (Polska, Rosja, Ukraina, sąsiedzi) szukaj też w **prasie lokalnej** (po polsku, rosyjsku, ukraińsku…);
  - **media państwowe** (np. rosyjskie) są dobrym źródłem **oficjalnej postawy** (`diplomatic relation towards`), ale **nie** nastrojów społecznych (`social view towards`, `government popularity`);
  - Wikipedia wystarcza do dat i przebiegu wydarzeń; do ocen (nastroje, popularność) szukaj sondaży i prasy.
- Lata po Twojej dacie odcięcia wiedzy: **zawsze** sprawdź w wyszukiwarce.

## 4. Jak wypełniać

- **Okresami, nie rok po roku.** Historię każdej statystyki opisz w **3–8 okresach**. Każdy okres to jedna operacja z krzywą (`linear`, `logistic`, `exponential`, `step`, `constant`), a `manual` tylko dla gwałtownych lat. Przykład:
  1. `stability` POL 1990–1993: 40 → 55 (logistic) — transformacja;
  2. 1994–2004: 55 → 70;
  3. … i tak dalej.
- **Flagi 0/1** (`riots`, `epidemic`, `mobilized`, `immigration crisis`, `state collapse`): ustaw 1 tylko w latach poważnych zdarzeń (opis statystyki mówi, co się liczy). Resztę zostaw: wartość domyślna 0 obowiązuje.
- **Skala bezwzględna**: patrz opisy. Porównuj się z kotwicami: jeśli Szwajcaria 2010 ma `stability` 77, to Polska 2010 nie może mieć 90 bez mocnego powodu.
- **Wartości startowe ze wskaźników** (`violence risk`, `corruption`, `civilization level`, `happiness` od 2011, `net migration`):
  - już są; **uzupełnij brakujące lata** (zwykle 1990–1995 i 2023–2025) tak, żeby łączyły się płynnie z istniejącymi (`start: "current"`);
  - **zmieniaj istniejące** tylko z konkretnym powodem. Różnica powyżej 15 punktów wyskoczy w `review`.
- **Nie nadpisuj** cudzej pracy: zadanie A tylko dla Twojego państwa; zadanie B tylko relacje **od** Twojego państwa (dwustronne: tylko pary z Twoim państwem).

## 5. Zadanie A — statystyki państwa

Wypełnij **każdą** statystykę bez wartości domyślnej dla **każdego** roku istnienia państwa:
`stability` (bez wartości startowych: tylko instytucje, bez przemocy — patrz opis), `violence risk`, `corruption`, `happiness`, `social revanchism`, `government revanchism`, `government popularity`, `social sensitivity`, `civilization level`, `assimilation`.

Statystyki z wartością domyślną (`war exhaustion`, flagi, `net migration`) wypełnij tam, gdzie coś się działo.

## 6. Zadanie B — relacje państwa

1. **Lista istotnych partnerów** (zwykle 10–40):
   - sąsiedzi (`context` pokazuje granice);
   - mocarstwa (USA, CHN, RUS, DEU, FRA, GBR…);
   - sojusznicy i członkowie tych samych grup;
   - przeciwnicy;
   - główni partnerzy handlowi i źródła energii.
2. Dla **każdego partnera** wypełnij 8 relacji skierowanych **od Twojego państwa**:
   - `diplomatic relation towards`, `social view towards` (skala −100..100);
   - `perceived/real subordination towards`, `perceived/real power towards`, `economic dependence` (skala 0..100);
   - `hybrid attacks towards` (0/1).
3. **Relacje dwustronne** z Twoim udziałem:
   - `in war crisis`: przejrzyj pary z UCDP (poziom 1) i usuń te, które nie pasują do opisu; dodaj brakujące, np. 2025;
   - `in war` (tylko lata poza UCDP, czyli 2025).
4. **Pozostałe pary** potwierdź jako domyślne jedną komendą (@phase-1.2b:P1):
   ```
   python -m simulator --scenario world-1990-2025 confirm-default --kind directed --name all \
       --targets POL --years 1990-2025 --author MODEL --note "pozostali partnerzy: brak istotnej relacji"
   ```
   To samo dla `--kind doublesided`. Wpisane wartości zostają; potwierdzenie dotyczy tylko pustych komórek.
   Dla statystyk państwa z wartością domyślną (flagi, `war exhaustion`) w zadaniu A: `confirm-default --kind grade --name all --targets POL --years …`.

## 7. Format zapisu

Jeden plik batch na zadanie (`batch` = wszystko albo nic):

```json
{
  "rationale": "POL, zadanie A",
  "operations": [
    {"kind": "grade", "name": "social revanchism", "targets": "POL", "years": "1990-2004",
     "curve": "linear", "start": 10, "end": 8,
     "rationale": "brak roszczeń terytorialnych; marginalne ugrupowania",
     "sources": ["https://…", "Tytuł, gazeta, 2001-05-03"]}
  ]
}
```

- `--author` = nazwa modelu (np. `claude-haiku-5-5`).
- **Uzasadnienia i źródła [DO DECYZJI — P4]:**
  - **tryb pełny:** `rationale` i `sources` przy każdym okresie;
  - **tryb oszczędny:** bez nich (taniej, ale bez możliwości sprawdzenia, skąd liczba).

  Propozycja: oszczędny dla małych krajów, pełny dla krajów ważnych dla modelu.

## 8. Kolejność pracy

1. `context` + `formulas list`.
2. Zbierz informacje (wyszukiwarka, wiedza).
3. Napisz batch.
4. `python -m simulator --scenario world-1990-2025 batch plik.json --author MODEL --dry-run`, przejrzyj tabelę.
5. Zapisz (bez `--dry-run`).
6. `validate` (0 błędów) i `review` dla swojego państwa: wyjaśnij albo popraw ostrzeżenia.
7. Sprawdź postęp: `missing --by-country` (Twoje państwo powinno mieć 100% w swoim zadaniu).
8. Oznacz zadanie w kolejce `AGENTS/phases/phase-1.2b/queue.md` jako zrobione: krótka notka, liczba operacji i ostrzeżeń.

## 9. Czego nie robisz

- Nie edytujesz plików CSV ręcznie; tylko przez `set` / `batch`.
- Nie zmieniasz wzorów (`formulas`), danych prawdziwych (`history/`) ani wartości innych państw.
- Nie zgadujesz, gdy nie wiesz: zostaw puste i zapisz w kolejce, czego brakuje. Lepsza luka niż wymyślona liczba.
