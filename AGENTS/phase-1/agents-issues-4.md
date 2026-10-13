# Phase 1 — Nierozwiązane problemy, runda 4 (agents-issues-4)

Problemy, które wyszły przy implementacji decyzji z `agents-issues-3.md` i odpowiedzi w `AGENTS/Conversations/phase-1.2-propozycje-wypelniania.md`. Format: **Problem / Propozycja / Decyzja**. Priorytety: 🔴 blokujące, 🟡 ważne, 🟢 drobne.

---

## M. Źródła danych

### M1. 🔴 Które statystyki ze wskaźników, a które z prasy?
- **Problem:** Zgodziłeś się na P1 (prawdziwe wskaźniki jako punkt startowy), ale część statystyk chcesz wypełniać na podstawie **artykułów prasowych**, bo dane opisowe to głównie **odczucia społeczne**. Zanim zaimportuję wskaźniki, potrzebny jest podział.
- **Propozycja:**

  | Źródło | Statystyki |
  |---|---|
  | **Wskaźniki → wartości startowe**, LLM koryguje | `stability` (WGI Political Stability), `corruption` (WGI Control of Corruption / TI CPI), `civilization level` (HDI), `immigration` / `emigration` (UN DESA, WB net migration), `in war` (UCDP), `neighbours` (CoW, **bez LLM**) |
  | **Prasa + LLM**, wskaźnik tylko jako kotwica | `happiness` (World Happiness Report od 2005), `government popularity` (sondaże), `social view towards` (Pew, Eurobarometr) |
  | **Prasa + LLM** | `revanchism`, `war exhaustion`, `social sensitivity`, `assimilation`, `diplomatic relation towards`, `perceived/real power towards`, `perceived/real subordination towards`, flagi (`riots`, `epidemic`, `mobilized`, `immigration crisis`, `in hybrid war`) |

  Dla prasy agenci potrzebują dostępu do wyszukiwarki. Proponuję, żeby **źródła (URL) trafiały do `rationale`**, albo żeby w `changelog.csv` doszła osobna kolumna `sources` (mała zmiana).
- **Decyzja:** Zgoda. Wyjaśnij mi ten punkt i jego konsekwencje w `Conversations/M1-wskazniki.md`

### M2. 🟢 Korea Północna nie ma PKB w żadnym dostępnym źródle
- **Problem:** World Bank i MFW nie publikują PKB Korei Północnej. Dane ONZ (UNSD National Accounts) by je miały, ale serwer ucinał pobierany plik (próbowałem 3 razy). Ekstrapolacja nie ma od czego wyjść.
- **Propozycja:** Zostawić puste, chyba że pobierzesz plik ONZ ręcznie ("GDP and its breakdown at current prices in US Dollars" z unstats.un.org). Wtedy uzupełnię Koreę Północną z ONZ i dopiszę konwerter tego formatu.
- **Decyzja:** Dobra, zrobię to, czy możesz zrobić mi listę rzeczy do zrobienia w `Conversations/TODOs/WAZNE-TODO-dla-autora.md`? - Będę wdzięczny! Korzystaj z tego folderu, nawet dla TODOs dla LLMów (lub nawet dla siebie - jak tobie wygodnie). Zrób jeszcze `Conversations/TODOs/SREDNIE-TODO-dla-autora.md` i `Conversations/TODOs/MALE-TODO-dla-autora.md` (MALE od małe - z polskiego!)

### M3. 🟢 Jakość oszacowań PKB
- **Problem:** Niektóre ekstrapolacje są z natury słabe: **Serbia 1990–1994** (wojna, hiperinflacja), Afganistan 1990–1999, Litwa 1991, Estonia 1991–1992, Kuba 2021–2025, Syria 2023–2025. Wartości MFW za 2025 to szacunki MFW. Wszystkie oszacowania są w `history/fill-log.csv`, a `context` oznacza je `*`.
- **Propozycja:** Na razie zostawić. Jeśli te kraje będą ważne w symulacji, poprawić ręcznie przez `history import --format wide` (osobny plik z poprawkami) albo innym źródłem.
- **Decyzja:** Zgoda.

---

## N. Nowe pliki scenariusza — do przejrzenia

### N1. 🟡 Członkostwo w grupach (`groups.csv`) wpisałem z własnej wiedzy
- **Problem:** NATO, EU, CIS, CSTO, EAEU, V4 z latami członkostwa. Przyjęte uproszczenia:
  - `EU` obejmuje też **Wspólnoty Europejskie przed 1993**; GBR do 2020;
  - `CIS`: Ukraina 1991–2018 (nigdy nie ratyfikowała statutu), Turkmenistan do 2005 (później członek stowarzyszony), Gruzja 1993–2009;
  - `CSTO` od traktatu z 1992 (organizacja od 2002); Uzbekistan 1992–1999 i 2006–2012; Azerbejdżan i Gruzja 1993–1999; **Armenia nadal członkiem**, choć od 2024 zamroziła udział.
- **Propozycja:** Przejrzyj `simulator/scenarios/world-1990-2025/groups.csv` (kolumna `note`). Inne grupy (np. G7, BRICS, SCO, Trójmorze) mogę dodać na życzenie.
- **Decyzja:** Dobrze zrobię to, zapisz to do mojego MALE-TODO

### N2. 🟢 Wybór krajów referencyjnych
- **Problem:** Wybrałem 15 krajów (`reference-countries.csv`, z uzasadnieniem w kolumnie `reason`). Klucz: obie strony skali (CHE, NOR na górze; SOM, SYR, VEN na dole), strony modelu (POL, RUS, UKR, DEU, USA) i różne typy państw (CHN, IND, BRA, TUR, IRN).
- **Propozycja:** Zostawić; plik możesz edytować dowolnie, mapa (`reference-map`) pokaże nową listę.
- **Decyzja:** Zgoda.

---

## Stan realizacji decyzji z `agents-issues-3.md` i propozycji

- **K1** — dodany `TWN` (Taiwan). Jego PKB w całości pochodzi z MFW (oznaczony w `fill-log.csv`).
- **K2** — konwencje zapisane dla agentów w `simulator/README.md` i `AGENTS/Conversations/phase-1.md`.
- **K3** — nowe komendy `history gaps` i `history fill` (źródło → interpolacja → ekstrapolacja), log `history/fill-log.csv`. Luki PKB uzupełnione: 72 wartości z MFW, 44 z ekstrapolacji. Zostaje tylko Korea Północna (M2). Zrobiłem to sam, bez osobnego agenta.
- **L1** — GUI do edycji danych zapisane w `AGENTS/future-work.md`.
- **L2** — bez zmian.
- **P3 (kraje referencyjne)** — `reference-countries.csv` i komenda `python -m simulator reference-map` (mapa świata HTML z suwakiem lat; działa offline; kraje bez wartości są szare).
- **P7** — grupy (`groups.csv`, cele `@NATO:RUS`, `POL:*`, `@EU:@EU`, z uwzględnieniem lat członkostwa i istnienia), `context` (zwięzły kontekst kraju lub pary dla agenta), `review` (ostrzeżenia o skokach i brakującym uzasadnieniu). **Import wskaźników z P1 czeka na decyzję M1.**
- Testy: 47 przechodzi. `validate`: 0 błędów, 0 ostrzeżeń.
