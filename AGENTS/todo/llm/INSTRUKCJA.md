# Instrukcja TODOs — dla agentów LLM

*Utworzone: 2026-10-14 00:20 — Claude Opus 5.5. Agenci mogą ten plik ulepszać (z podpisem i datą zmiany na dole).*

---

## Na początku każdej sesji (w tej kolejności)

0. **`AGENTS/README.md`**: mapa folderu i zasady. Szybki przegląd stanu: `venv/bin/python -m agents_board --static /tmp/board.html` (albo przeglądanie plików).
1. **`AGENTS/talk/od-autora-dla-llmow.md`**: przeczytaj nowe uwagi i oznacz każdą jako przeczytaną, dopisując na końcu jej linii `— *przeczytane: RRRR-MM-DD (model)*`. Poza tym w tym pliku **nic nie piszesz**.
2. **`AGENTS/plan/phases-plans.md`**: na jakim etapie jest projekt.
2b. **Najnowszy plik w `AGENTS/talk/koniec/`** (jeśli jest nowszy niż Twój ostatni briefing): lista tego, na co autor odpowiedział w GUI — od tego zaczynasz. **Mimo to sprawdź pliki zmienione od Twojego ostatniego briefingu** (`find AGENTS -name "*.md" -newer AGENTS/talk/briefings/<ostatni>.md` albo `git status`) i przeczytaj tylko je — lista z Konca może być niepełna (@T020).
3. **`AGENTS/todo/author/raport-TODO-autora.md`**: nowe wpisy autora. Na każdy odpowiedz blokiem LLM (format niżej).
4. **`AGENTS/talk/threads/`**: wątki, w których ostatni wpis jest od autora. Odpowiadasz w tym samym wątku. `wymiana-zdan-A1.md` to archiwum: nic tam nie dopisujemy.
5. **`TODO-dla-LLM.md`** (ten folder): wybierz zadanie.
6. Najnowsze pola **Decyzja** w `AGENTS/phases/phase-*/agents-issues-N.md`.

## Pliki w tym folderze

| Plik | Co tam jest |
|---|---|
| `TODO-dla-LLM.md` | zadania dla agentów, numeracja **L1, L2…** |
| `raport-TODO-LLM.md` | raporty z wykonania zadań `L…` (piszą tylko agenci) |
| `INSTRUKCJA.md` | ten plik |

## Numeracja i statusy

- Zadania agentów: **L…**. Nowe zadanie dostaje kolejny wolny numer (sprawdź najwyższy w `TODO-dla-LLM.md`). Numerów nie używamy ponownie.
- Zadania dla autora: **A…** w `AGENTS/todo/author/` (WAŻNE / ŚREDNIE / MAŁE). Nowe zadanie dla autora dostaje kolejny wolny numer A i trafia do pliku o właściwym priorytecie.
- Statusy jak u autora: `[ ]` do zrobienia, `[~]` w toku, `[x]` zrobione, `[?]` zablokowane (napisz na co), `[>]` przeniesione (napisz dokąd), `[-]` porzucone (napisz dlaczego).
- **Niczego nie usuwasz**, zmieniasz tylko literę i dopisujesz krótką notkę.

## Jak wziąć i zamknąć zadanie

1. Biorąc zadanie: `[~]` + `*(w toku: model, RRRR-MM-DD GG:MM)*`.
2. Po wykonaniu: `[x]` + `*(zrobione: RRRR-MM-DD GG:MM, raport: raport-TODO-LLM.md)*`.
3. W `raport-TODO-LLM.md` dopisz wpis:
   ```
   ### [L6] tytuł

   - co zrobiono, gdzie są pliki, jak sprawdzono (testy, validate),
   - co zostało / nowe problemy (→ nowe L… albo A…, albo agents-issues),

   *RRRR-MM-DD GG:MM — model*

   ---
   ```
4. Jeśli zadanie wymaga decyzji autora: status `[?]` i pytanie w odpowiednim `agents-issues-N.md` albo nowe zadanie A….

## Odpowiedzi w plikach autora

**Jeden blok odpowiedzi = jedno zadanie** (wątek @T014): GUI pokazuje przy zadaniu tylko jego blok/sekcję, więc nie łącz kilku zadań w jednym bloku.

W `raport-TODO-autora.md` (i podobnych) **nie edytujesz tekstu autora**. Wyjątek: miejsce, które autor wyraźnie zostawił do uzupełnienia, np. `[Numeracja - Tu wstaw numeracje]`. Odpowiedź dopisujesz pod jego wpisami jako blok:

```
---

> 🤖 **ODPOWIEDŹ LLM — początek** (model)
>
> ### [A2] Re: tytuł
>
> treść…
>
> *przeczytane i odpowiedziane: RRRR-MM-DD GG:MM — model*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---
```

## Wątki (`AGENTS/talk/threads/T001-….md`) — od 2026-10-14

- Jeden temat = jeden plik. Nagłówek `# T001 · tytuł`, potem wpisy oddzielone trzema liniami `---`.
- Wpis agenta: treść, pusta linia, podpis `*RRRR-MM-DD GG:MM — model*` jako **ostatnia linia**, pusta linia, `---` ×3. Wcześniejszych wpisów nie edytujesz.
- Nowy temat od agenta: nowy plik z kolejnym numerem T i nagłówkiem jak w `agents_board/model.py` (`thread_header`); odgałęzienie od innego wątku: linia `*Odgałęzienie od: T002*` pod tytułem.
- Wątek jest **zamknięty**, gdy któryś wpis zaczyna się od `🔒`. W zamkniętym wątku nie odpowiadasz; zamykasz tylko na wyraźne życzenie autora (z cytatem).
- **Wzmianki**: `@T002` (wątek), `@A12` / `@L3` (zadanie), `@phase-2:R1` (pytanie w fazie). GUI robi z nich linki i krawędzie grafu. Używaj ich w wątkach, raportach i briefingu.

## Archiwum: wymiana zdań (`wymiana-zdan-A1.md`, do 2026-10-14)

Wpis zaczyna się od `---` ×3 i `# tytuł`, kończy podpisem z datą i godziną oraz **`---` ×3 na końcu** (prośba autora). Wcześniejszych wpisów nie edytujesz.

- Jeśli plik **już kończy się** trzema `---` (np. wpis autora dodany przez GUI `agents_board`), nie dodawaj kolejnej trójki na początku: zacznij od razu od `# tytuł`.
- Podpis agenta w ostatniej linii wpisu, np. `*RRRR-MM-DD GG:MM — Claude Opus 5.5*`. Po nim GUI rozpoznaje, że wpis jest od agenta (słowa Claude/GPT/Gemini/LLM/model po myślniku), i pokazuje autorowi "Agent czeka na odpowiedź".
- Wpisy autora dodane przez GUI kończą się podpisem `— Autor*`.

## Konwencje, na których opiera się GUI (`agents_board`)

Nie zmieniaj ich bez aktualizacji `agents_board/model.py` i testów `tests/test_agents_board.py`:
- zadanie: `- [ ] **A12. tytuł** reszta…` (linie kontynuacji wcięte spacjami);
- pytanie: `### W1. 🔴 tytuł` … `- **Decyzja:**` (pole puste = czeka na autora);
- pytania tylko w plikach `AGENTS/phases/<faza>/agents-issues-N.md`;
- raport autora: wpisy `### [A13] tytuł`.

## Ustalenia, które obowiązują zawsze

- **Godzina w podpisie zawsze z `date "+%Y-%m-%d %H:%M"`**, uruchomionego tuż przed podpisem, nigdy szacowana (wątek T001).
- **Briefing** (wątek T004): na koniec każdej sesji zapisz `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md` (godzina z `date`) z **tą samą treścią**, co odpowiedź w oknie czatu; w punktach "Do odpowiedzi" użyj wzmianek `@…`. GUI pokazuje go pod przyciskiem "📋 Briefing".
- **Ścieżki plików** zawsze w backtickach i pełne (np. `AGENTS/phases/phase-1.2b/plan.md`) — GUI robi z nich linki; w okienku czatu jako linki markdown `[nazwa](ścieżka)`.
- **Odpowiedź w oknie czatu** (uwaga autora nr 2): tylko (1) **Zmiany**: ścieżki plików z oznaczeniem **CRE/MOD/DEL** (created/modified/deleted; trzy litery — wątek T004); (2) **Do odpowiedzi**: rzeczy dla autora z miejscem w drzewie GUI (np. "Co czeka na mnie → Pytania bez decyzji → …") i bardzo krótkim opisem. Reszta trafia do plików w `AGENTS/`.

- Komunikacja z autorem i pliki w `AGENTS/` po polsku; kod, nazwy plików i danych, `README.md` po angielsku.
- Konwencje scenariusza `world-1990-2025` (lista państw, kontynuacje ZSRR/Jugosławii, `exists_from`): `simulator/README.md`.
- Agenci **mogą korzystać z wyszukiwarki internetowej** (autor, A3). Źródła zapisuj zawsze (URL, tytuł, data).
- Dane opisowe zapisujemy tylko narzędziem `python -m simulator set/batch`, z `--author` i `--rationale`; potem `validate` i `review`.

## Pytania o opinię (uwaga autora, wątek T017)

"Co ty na to…?", "jak widzisz…?", "co sądzisz…?" to **pytania o opinię, nie zgoda na działanie**. Odpowiadasz plusami, minusami i rekomendacją, dodajesz zadanie A z decyzją i niczego nie uruchamiasz, dopóki autor wyraźnie nie zdecyduje ("robimy", "zgoda", "wybieram…").

## Plany i raporty: jeden plik na zadanie (@T022)

Plan poprawki, raport albo propozycja dla konkretnego zadania lub pytania = **osobny plik** (np. `AGENTS/phases/phase-1.2b/poprawki/K1-import-ucdp.md`), podlinkowany w tym zadaniu. Plik zbiorczy może istnieć, ale tylko jako spis z linkami.

**Każdy plik dla autora zaczyna się od sekcji „Co masz zrobić”** (uwaga autora 2026-10-14, @A36/@A37/@A38): jednym-dwoma zdaniami problem prostymi słowami, potem **pytanie albo decyzja do podjęcia** z gotowymi opcjami (np. „wystarczy: tak, −30”). Szczegóły techniczne dopiero niżej. To samo w blokach odpowiedzi w raporcie autora.

## Praca wielu agentów naraz (wnioski z reguły „tylko 2025”, zaakceptowane: @A35)

Szczegóły: `AGENTS/phases/phase-1.2b/regula-2025.md`.
1. **Komórki wspólne dla dwóch państw** (relacje dwustronne) nie są zadaniem agentów krajowych. Robi je jeden agent w osobnym zadaniu „przegląd par”; agenci krajowi tylko zgłaszają kandydatów.
2. **Każde ograniczenie ma ścieżkę dla wyjątków**: „nie zmieniaj X” zawsze razem z „zgłoś kandydata do pliku CSV Y” (np. `para, lata, typ, źródło`), żeby koordynator dopisał je skryptem, a nie z 392 raportów.
3. **`confirm-default` nie potwierdza zgłoszonych wyjątków** (opcja `--except`, @L48).
4. **Plan fazy ma krok koordynatora** po fali agentów: rozstrzygnięcie zgłoszeń, zanim `missing` = 100% zamknie fazę.
5. **Pilot na zróżnicowanych przypadkach** (np. państwo z wojnami i państwo bez) przed pełną falą.
6. **Jedno źródło zasad**: zmiana reguły w prompcie agenta = zmiana w instrukcji fazy (albo wyraźny zapis, że prompt ją zastępuje).

*Dopisane 2026-10-14 14:30 — Claude Opus 5.5*

## Pytania przeniesione do zadań (@T019)

- Pytanie z Decyzją `⏳ w toku → @A43` to sprawa przeniesiona do zadania (i/lub raportu): rozmowa toczy się pod zadaniem, odpowiadasz w raporcie jak zwykle.
- `- **Propozycja końcowa:** (czeka na agenta)` = autor prosi o propozycję końcową: zastąp `(czeka na agenta)` swoją propozycją (zwięzłą, tak by mogła stać się decyzją). Autor w GUI ją akceptuje (Decyzja `✅ …`) albo odrzuca (`❌ odrzucona …: komentarz`) — wtedy rozmowa wraca do zadania.
- Pola Decyzja `⏳ …` nie zmieniasz; `✅ …` wpisuje autor (GUI).

*Dopisane 2026-10-14 15:23 — Claude Opus 5.5*
