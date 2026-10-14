# Phase 1.2b — zasady pracy agenta wypełniającego (Haiku w Claude Code)

Każdy agent dostaje krótkie polecenie: państwo `TAG`, zadanie (A albo B) i tryb (pełny albo oszczędny), oraz odsyłacz do tego pliku. Zasady ogólne: `instrukcja-wypelniania.md`.

*2026-10-14 06:58 — Claude Opus 5.5; poprawki po pilocie POL: 2026-10-14 07:10; reguła dla relacji dwustronnych: 2026-10-14 07:20; pliki tymczasowe: 2026-10-14 08:18; happiness bez danych: 2026-10-14 12:57*

---

Katalog roboczy: `/home/karol/Pulpit/Python3.14/economics-model-pol-vs-rus`. Python: `venv/bin/python`. Równolegle pracuje wielu innych agentów (inne państwa i drugie zadanie Twojego państwa).

1. **Przeczytaj w całości `AGENTS/phases/phase-1.2b/instrukcja-wypelniania.md`** i trzymaj się jej. Rozstrzygnięcia spraw oznaczonych tam [DO DECYZJI]:
   - **źródła:** opierasz się na swojej wiedzy. Wyszukiwarki (WebSearch) używasz **tylko dla lat 2023–2025**, najwyżej ~5 wyszukiwań. Czytasz same wyniki (tytuły i fragmenty), **bez pobierania całych artykułów** (bez WebFetch);
   - **tryb pełny:** `rationale` przy każdej operacji, a `sources` tam, gdzie korzystałeś z wyszukiwarki albo znasz konkretne źródło (sondaż, raport);
   - **tryb oszczędny:** jedno krótkie `rationale` dla całego batcha, bez `sources`.
2. Komendy zawsze z `--scenario world-1990-2025`, np. `venv/bin/python -m simulator --scenario world-1990-2025 context TAG` (dla pary: `context TAG:RUS`).
3. **Batch** zapisz do `AGENTS/phases/phase-1.2b/batches/TAG-A.json` albo `TAG-B.json`. To jeden plik; przy poprawkach nadpisujesz go i zapisujesz ponownie. Batch możesz generować skryptem, ale skrypt i inne pliki tymczasowe trzymaj wyłącznie w `/tmp/claude-1000/` (nie w projekcie ani w katalogu nad nim).
   - Zapis: `--author claude-haiku-5-5`, najpierw `--dry-run`.
   - Jeśli komenda zgłosi zajęty plik blokady (`.lock`), poczekaj chwilę i powtórz. **Nigdy nie usuwaj pliku `.lock`.**
4. **Zadanie A** (statystyki państwa, `kind: grade`, targets = TAG):
   - na końcu `confirm-default --kind grade --name all --targets TAG --years 1990-2025 --author claude-haiku-5-5`;
   - jeśli państwo nie ma żadnych danych `happiness` (brak WHR), oszacuj całą serię przez porównanie z podobnymi państwami (region, poziom rozwoju) i napisz to w odpowiedzi; to samo dla innych statystyk bez wartości startowych;
   - nie dotykaj relacji.
5. **Zadanie B** (relacje, targets `TAG:XXX`, tylko **od** Twojego państwa):
   - rozróżniaj partnerów, o ile to możliwe. Wspólne wartości dla grupy (np. kraje nordyckie) tylko wtedy, gdy naprawdę nie widzisz różnicy;
   - `hybrid attacks towards`: tylko działania prowadzone **przez Twoje państwo**;
   - relacje dwustronne (`in war`, `in war crisis`): **dopisuj tylko rok 2025** (gdy trwa konflikt z wcześniejszych lat albo jest pewne nowe zdarzenie). Wpisów z lat 1990–2024 nie zmieniaj ani nie przenoś między `in war` a `in war crisis`; wątpliwości opisz w odpowiedzi końcowej, a rozstrzygnie je koordynator (wspólna reguła dla UCDP);
   - na końcu `confirm-default` dla `--kind directed` i `--kind doublesided`, oba z `--name all --targets TAG --years 1990-2025 --author claude-haiku-5-5`;
   - nie dotykaj statystyk państwa (`grade`).
6. **Sprawdzenie:**
   - `validate`: 0 błędów;
   - `review | grep TAG`: popraw albo wyjaśnij ostrzeżenia ze swojego zadania. Ostrzeżenia o `net migration` pomiń: to dane z prawdziwych statystyk, którymi zajmuje się koordynator;
   - `missing --by-country | grep TAG`: Twoja kolumna (A: internal-grades, B: obie kolumny relacji) ma być na 100%.
7. **Nie edytuj** `queue.md` ani żadnych plików projektu poza swoim batchem: to zastępuje krok 8 instrukcji, bo kolejkę zamyka koordynator. Nie zmieniaj danych innych państw ani plików CSV ręcznie.
8. **Odpowiedź końcowa**, krótko, po polsku:
   - liczba operacji (w B także liczba partnerów);
   - wynik `missing` dla TAG;
   - ostrzeżenia `review`, które zostały, i dlaczego;
   - czego nie wiedziałeś i co zostało niepewne;
   - liczba wyszukiwań.
