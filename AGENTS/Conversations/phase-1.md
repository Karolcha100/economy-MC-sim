# Phase 1 — notatki z rozmów (autor ↔ agenci)

Zapis ustaleń, które nie są oczywiste z kodu ani z `agents-instructions.md`. Pełne decyzje: `AGENTS/phase-1/agents-issues.md`.

---

## 2026-10-13 — Spójność między statystykami (agents-issues G1)

**Propozycja agenta:** wymuszać spójność logiczną, np. `in war` (A↔B) ↔ `mobilized` / `war exhaustion` w A, oraz `real power towards` A→B ↔ B→A.

**Odpowiedź autora:**
- Państwo może być **zmobilizowane** i **wyczerpane wojną bez trwającej wojny** (np. po poprzedniej wojnie albo mobilizacja "od tak"). `in war` nie implikuje ani nie jest implikowane przez `mobilized` / `war exhaustion`.
- `real power towards` **nie musi być symetryczne** — to siła oddziaływania jednego państwa na drugie (A→B ≠ B→A).

**Wniosek dla agentów:**
- Nie dodawać reguł wymuszających te zależności. W Phase 1 walidator sprawdza tylko zakresy, typy, przekątną, symetrię relacji dwustronnych i istnienie państw.
- Ewentualne reguły spójności w przyszłości wyłącznie jako **ostrzeżenia** i tylko po uzgodnieniu z autorem.
- Agenci LLM wypełniający dane powinni oceniać każdą statystykę osobno, nie wyprowadzać jej mechanicznie z innej.

---

## 2026-10-13 — Organizacje (agents-issues A1, E4)

- `organisation-grades` to nie template, tylko dane poszczególnych państw/organizacji — **nie implementujemy w Phase 1**.
- Organizacje (sojusze, UE, NATO…) mają być **dynamiczne i składać się z countries**. Poza zakresem Phase 1, ale formaty danych nie powinny tego blokować (kolumny encji w wzorach relacji przyjmują dziś tylko `TAG`; w przyszłości dojdzie np. rodzaj encji organizacji).

---

## 2026-10-13 — `TAG` i `valmin/valmax` w relacjach (agents-issues A3)

- `TAG` = kraj z `tags.csv`.
- `valmin/valmax` relacji opisują przedział wartości relacji **między państwami** (wartość komórki macierzy).
- Relacje są przechowywane jako macierz, ale wprowadza się je także **podając tagi** (np. `POL:RUS`) w skryptach dla LLM — tak działa `python -m simulator set --kind directed --targets POL:RUS ...`.

---

## 2026-10-13 — Język (agents-issues F3)

- `AGENTS/**` po polsku (komunikacja z autorem).
- Kod, komentarze, docstringi, nazwy plików i danych, `README.md`, `simulator/README.md` — po angielsku.
