# Phase 1.2b — K7. Państwa bez danych WHR — moja opinia (pytanie o opinię, nic nie zmieniam)

Poprawka po wypełnieniu. Pytanie: @phase-1.2b:K7 (`AGENTS/phases/phase-1.2b/agents-issues-2.md`). Zadanie autora: @A39; wykonanie: @L50 (wyrzucenie), @L51 (`happiness` później). Spis wszystkich poprawek: `AGENTS/phases/phase-1.2b/plan-poprawek.md`.

*2026-10-14 14:29 — Claude Opus 5.5 (wydzielone z `plan-poprawek.md`, @T022)*

---

## Twoja decyzja (2026-10-14) i co z niej wynika

**Decyzja (@A39):** wyrzucić z modelu państwa bez danych WHR, poza PRK i PNG; `happiness` dla pozostałych uzupełnić w przyszłości razem z innymi zmianami danych (@L51).

**Jedna poprawka do listy — Kosowo (XKX).** Sprawdziłem: Kosowo **ma** dane WHR (2011–2024) w źródle, tylko import ich nie wczytał, bo źródło używa kodu `OWID_KOS` zamiast `XKX` (ten sam błąd kodów co w @A38). Czyli według Twojego kryterium XKX zostaje — do wyrzucenia jest **31 państw**:

ERI, GNB, GNQ, TLS, FJI, SLB, CPV, BRN, BHS, VUT, BRB, STP, WSM, LCA, KIR, SYC, GRD, FSM, TON, VCT, ATG, AND, DMA, KNA, LIE, MCO, MHL, SMR, PLW, NRU, TUV.

**Co zrobię (@L50), po Twoim „OK” w @A39:**
1. Nowa komenda `python -m simulator drop-tags …` (z testem): usuwa państwa z `tags.csv`, `groups.csv`, listy krajów referencyjnych, ze wszystkich plików `narrated/` (wiersze statystyk; wiersze i kolumny relacji) i z `confirmed-defaults.csv`; wpis w `changelog.csv`. Dane w `history/` zostają (kolumny spoza `tags.csv` są ignorowane).
2. `validate`, `missing` (ma zostać 100%), `audit`.
3. Ich batche w `AGENTS/phases/phase-1.2b/batches/` zostają jako archiwum; w `queue.md` dostaną `[-]` z notką.
4. Kopia zapasowa przed zmianą (jest commit „phase 1.2b done” + archiwum `tar.gz`).

**Skutki, o których warto wiedzieć:**
- znikają też relacje innych państw z nimi (np. które wyspy uznają Tajwan — gra dyplomatyczna Tajwan/Chiny traci część „pionków”);
- lista państw kandydujących do poprawek K1–K6 skraca się (np. skoki WGI w LCA, VCT, KNA, TON, PLW przestają nas dotyczyć).

**Koszt:** programowanie i sprawdzenie — ok. 1 $ pracy Opus.

---

## Wcześniejsza opinia (przed decyzją)

**Które to państwa** (34, od największej ludności):
PRK (26 mln), PNG (10 mln), ERI, GNB, GNQ, XKX, TLS, FJI, SLB, CPV, BRN, BHS, VUT, BRB, STP, WSM, LCA, KIR, SYC, GRD, FSM, TON, VCT, ATG, AND, DMA, KNA, LIE, MCO, MHL, SMR, PLW, NRU, TUV.
- Razem ok. 50 mln ludzi, z czego PRK i PNG to 36 mln. Pozostałe 32 państwa to ok. 14 mln.
- XKX pewnie ma dane (błąd kodu, K6).

**Czy je wyrzucić?**
- **Za:**
  - 32 mikropaństwa praktycznie nie wpływają na relację POL–RUS;
  - ich dane opisowe to w całości szacunki;
  - w uczeniu (Phase 2.1) to 1/6 obserwacji z bardzo słabymi danymi, więc dodają szum;
  - mniejsza macierz relacji (196² → 164²) daje szybsze obliczenia.
- **Przeciw:**
  - PRK jest ważne geopolitycznie (sojusz z RUS, wojska w Kursku), a PNG, ERI i XKX mają realne konflikty;
  - wyrzucenie po wypełnieniu marnuje gotowe dane;
  - trzeba by poprawić relacje innych państw (np. TWN z wyspami, a uznanie Tajwanu to część gry dyplomatycznej ChRL);
  - przy liczeniu „średniej świata” małe państwa i tak ważą mało, jeśli ważymy ludnością.

**Rekomendacja:** **nie wyrzucać ze scenariusza.**
- W Phase 2.1 dodać **wagę obserwacji** (np. ludność albo flaga „dane szacowane”).
- Ewentualnie wyłączyć z uczenia regresji `happiness` 32 mikropaństwa bez WHR (bez PRK i PNG).
- Państwa zostają w świecie symulacji, ale nie psują nauki.
- Decyzja należy do Ciebie (@A39).
