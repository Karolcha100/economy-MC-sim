# Instrukcja TODOs — dla agentów LLM

*Utworzone: 2026-10-14 00:20 — Claude Opus 5.5. Agenci mogą ten plik ulepszać (z podpisem i datą zmiany na dole).*

---

## Na początku każdej sesji (w tej kolejności)

0. **`AGENTS/README.md`**: mapa folderu i zasady. Szybki przegląd stanu: `venv/bin/python -m agents_board --static /tmp/board.html` (albo przeglądanie plików).
1. **`AGENTS/talk/od-autora-dla-llmow.md`**: przeczytaj nowe uwagi i oznacz każdą jako przeczytaną, dopisując na końcu jej linii `— *przeczytane: RRRR-MM-DD (model)*`. Poza tym w tym pliku **nic nie piszesz**.
2. **`AGENTS/plan/phases-plans.md`**: na jakim etapie jest projekt.
3. **`AGENTS/todo/author/raport-TODO-autora.md`**: nowe wpisy autora. Na każdy odpowiedz blokiem LLM (format niżej).
4. **`AGENTS/talk/wymiana-zdan-A1.md`**: nowe wypowiedzi autora.
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

## Wymiana zdań (`wymiana-zdan-A1.md`)

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

- Komunikacja z autorem i pliki w `AGENTS/` po polsku; kod, nazwy plików i danych, `README.md` po angielsku.
- Konwencje scenariusza `world-1990-2025` (lista państw, kontynuacje ZSRR/Jugosławii, `exists_from`): `simulator/README.md`.
- Agenci **mogą korzystać z wyszukiwarki internetowej** (autor, A3). Źródła zapisuj zawsze (URL, tytuł, data).
- Dane opisowe zapisujemy tylko narzędziem `python -m simulator set/batch`, z `--author` i `--rationale`; potem `validate` i `review`.
