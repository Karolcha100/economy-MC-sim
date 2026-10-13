# Phase 1 — notatki z rozmów (autor ↔ agenci)

Zapis ustaleń, które nie są oczywiste z kodu ani z `agents-instructions.md`. Pełne decyzje: `AGENTS/phases/phase-1/agents-issues-*.md`.

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

---

## 2026-10-13 — Lista państw scenariusza `world-1990-2025` (agents-issues-3 K1, K2) — **ważne dla wszystkich agentów**

Autor zatwierdził i prosi, by wszyscy agenci o tym wiedzieli:
- 196 państw: wszystkie suwerenne gospodarki World Banku **bez 22 terytoriów zależnych** (m.in. Hongkong, Portoryko, Makau, Grenlandia, Wyspy Owcze, Guam, Bermudy) **plus Tajwan (`TWN`)**.
- Włączone państwa o ograniczonym uznaniu: Kosowo (`XKX`, od 2008), Palestyna (`PSE`, od 1994).
- Kontynuacje: Rosja = ZSRR, Serbia = Jugosławia (obie od 1990); Niemcy od 1990 (NRD nie modelujemy); Jemen od 1990.
- `exists_from` = rok uzyskania niepodległości (dowolny moment roku). Przed tym rokiem kraj nie ma danych opisowych.
- To samo, po angielsku, jest w `simulator/README.md` (sekcja "Scenario `world-1990-2025`").

## 2026-10-13 — Luki w danych historycznych (agents-issues-3 K3)

- Autor: luki uzupełniać — najpierw inne źródła, potem interpolacja/ekstrapolacja; zawsze z logiem.
- Zrobione: `history gaps` / `history fill`; log w `history/fill-log.csv`. Kolejność dla PKB: MFW (IMF DataMapper) → interpolacja → ekstrapolacja. Dane ONZ (UNSD AMA) nie dały się pobrać (serwer ucinał plik).

## 2026-10-13 — Odpowiedzi autora na propozycje wypełniania (phase-1.2-propozycje-wypelniania.md)

- **P1 (prawdziwe wskaźniki jako start)**: tak, ale autor myślał też o uzupełnianiu części statystyk **na podstawie artykułów prasowych**. Dane opisowe to przede wszystkim **odczucia społeczne**. Podział "wskaźniki vs prasa" → `agents-issues-4.md` M1.
- **Tier 1**: autor ufa proponowanej liście.
- **Kraje referencyjne**: tak — jako skrypt, w którym użytkownik wybiera kraje z pliku CSV, a narzędzie pokazuje rok, położenie na mapie świata i wartość statystyki → `python -m simulator reference-map`, lista w `reference-countries.csv`.
- **Narzędzia P7**: wszystkie zaakceptowane (grupy, `context`, `review`, konwertery źródeł).
