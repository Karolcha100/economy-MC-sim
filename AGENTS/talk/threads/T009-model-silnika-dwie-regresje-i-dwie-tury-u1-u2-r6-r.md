# T009 · Model silnika: dwie regresje i dwie tury (U1, U2, R6, R7, S3)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Podsumowanie, o które prosiłeś przy @phase-2:U2, plus odpowiedzi na pytania z @phase-2:R7 i @phase-2:S3. Pełny projekt: `AGENTS/phases/phase-2/design.md`.

**Teraz rozumiem U1 i przepraszam za zamieszanie:** regresje są **dwie i wspólne dla wszystkich państw**. Obserwacją jest jedno przejście, np. POL 1990 → POL 1991. Ta sama regresja uczy się na POL, DEU i każdym innym kraju. To dobre rozwiązanie: daje ~6 900 obserwacji zamiast 35.

**Jak to działa w jednym roku (U2 + R6 + U4):**
1. **Tura 1 — regresja wewnętrzna (I):** dla każdego państwa: stan w roku t → stan w t+1 (statystyki prawdziwe i opisowe).
2. **Tura 2 — regresja zewnętrzna (E):** dla każdej pary A→B (obserwacja: para w danym roku):
   - wejście: relacje A→B i B→A, stan A i B po turze 1;
   - wyjście: zmiana relacji A→B **oraz wkład do zmian A i B** (Twoje R6).

   Wkłady od wszystkich partnerów sumują się i dodają do wyniku tury 1, ważone m.in. nową relacją `economic dependence`.
3. **Zdarzenia 0/1:** obie regresje w wersji logistycznej dają prawdopodobieństwa. Rozlewanie się kryzysów wynika z regresji E, nie ze skryptu.

**R7 — "co realnie zmienia ta decyzja?":** decyduje, **na jakich danych uczy się regresja**. Po pilocie 1.2b dane opisowe (np. `revanchism`) będą tylko dla ~25 krajów Tier 1, a reszta będzie pusta albo z wartością domyślną. Wspólna regresja uczy się na wszystkich krajach naraz, więc:
- jeśli puste komórki zastąpimy wartością domyślną (np. 0), regresja "nauczy się", że `revanchism` prawie zawsze wynosi 0 i nic nie znaczy, co jest fałszywe;
- jeśli wyrzucimy kraje bez danych, zostanie ~25 krajów, a statystyki prawdziwe stracą 170 krajów.

**Pytanie (@A23)** — moja propozycja:
- statystyki opisowe trafiają do regresji razem ze **wskaźnikiem "wypełnione/niewypełnione"**;
- regresja uczy się ich wpływu tylko tam, gdzie są wypełnione, a z resztą danych korzysta na wszystkich krajach.

Zgoda? Później, gdy LLM-y wypełnią resztę (R9), wskaźnik przestanie być potrzebny.

**S3 — "jaki panel?":** "dane panelowe" to dane wielu krajów w wielu latach (kraj × rok), czyli dokładnie nasze. `linearmodels` to biblioteka do takich regresji z efektami kraju. Skoro efektów kraju nie chcemy (R1), **nie jest potrzebna**. scikit-learn też nie: liczę wszystko w **numpy** (float32), regresje z regularyzacją i logistyczną piszę sam. Przewidywanie to wtedy jedno mnożenie macierzy na turę, czyli najszybsza możliwa forma. Optymalizacja: wiele rdzeni na paczki scenariuszy.

*2026-10-14 04:11 — Claude Opus 5.5*

---
---
---
