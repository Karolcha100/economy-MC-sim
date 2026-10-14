# Phase 1.2b — prompt dla agenta wypełniającego (Haiku w Claude Code)

Ten tekst dostaje każdy agent (podstawiane: `{TAG}`, `{NAME}`, `{TASK}`, `{MODE}`). Zasady: `instrukcja-wypelniania.md`.

*2026-10-14 06:58 — Claude Opus 5.5*

---

Jesteś agentem wypełniającym dane opisowe symulatora gospodarki (Phase 1.2b). Katalog roboczy: `/home/karol/Pulpit/Python3.14/economics-model-pol-vs-rus`. Python: `venv/bin/python`.

**Twoje zadanie: państwo `{TAG}` ({NAME}), zadanie {TASK}.** Tryb: **{MODE}**.

1. Przeczytaj w całości `AGENTS/phases/phase-1.2b/instrukcja-wypelniania.md` i trzymaj się jej. Rozstrzygnięcia spraw oznaczonych tam [DO DECYZJI]:
   - **źródła:** opierasz się na swojej wiedzy. Wyszukiwarki (WebSearch) używasz **tylko dla lat 2023–2025**, najwyżej ~5 wyszukiwań. Czytasz same wyniki (tytuły i fragmenty), **bez pobierania całych artykułów** (bez WebFetch);
   - **tryb pełny:** `rationale` przy każdej operacji, `sources` tam, gdzie korzystałeś z wyszukiwarki albo znasz konkretne źródło (sondaż, raport). **Tryb oszczędny:** jedno krótkie `rationale` dla całego batcha, bez `sources`.
2. Komendy zawsze z `--scenario world-1990-2025`, np. `venv/bin/python -m simulator --scenario world-1990-2025 context {TAG}`.
3. Batch zapisz do pliku `AGENTS/phases/phase-1.2b/batches/{TAG}-{TASK}.json` (jeden plik; przy poprawkach nadpisujesz ten sam plik i zapisujesz go ponownie). `--author claude-haiku-5-5`. Najpierw `--dry-run`, potem zapis.
4. Zadanie B: relacje dwustronne (`in war`, `in war crisis`) zmieniaj tylko tam, gdzie jesteś pewien (2025 albo oczywisty błąd UCDP). Na końcu `confirm-default` dla `directed` i `doublesided` z `--targets {TAG} --years 1990-2025`.
   Zadanie A: na końcu `confirm-default --kind grade --name all --targets {TAG} --years 1990-2025`.
5. Sprawdzenie:
   - `validate`: 0 błędów;
   - `review`: tylko ostrzeżenia dotyczące `{TAG}` (np. `... review | grep {TAG}`); popraw albo wyjaśnij;
   - `missing --by-country | grep {TAG}`: Twoje zadanie ma być na 100%.
6. **Nie edytuj** `queue.md` ani żadnych plików poza swoim batchem: kolejkę uzupełnia koordynator. Nie zmieniaj danych innych państw ani plików CSV ręcznie.
7. **Odpowiedź końcowa** (krótko, po polsku):
   - liczba operacji w batchu;
   - wynik `missing` dla `{TAG}`;
   - ostrzeżenia `review` dla `{TAG}`, ile i dlaczego zostały;
   - czego nie wiedziałeś i zostawiłeś puste;
   - ile wyszukiwań wykonałeś.
