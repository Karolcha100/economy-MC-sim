# AGENTS — mapa

Wszystko, co dotyczy współpracy autora z agentami LLM: plany, fazy, pytania i decyzje, zadania, rozmowy.
Najszybciej przejrzysz to w przeglądarce: `python -m agents_board` (drzewo + odpowiadanie, patrz niżej).

*Struktura ustalona 2026-10-14 (decyzja autora A14). Agenci aktualizują ten plik przy każdej zmianie struktury.*

---

## Struktura

```
AGENTS/
  README.md                       ← ten plik
  plan/
    phases-plans.md               kolejność faz i statusy (aktualizują agenci)
    phases-description.md         zakres faz
    future-work.md                backlog na później
  phases/
    phase-1/                      instrukcje, pytania agentów (agents-issues-1…4), notatki (notes.md), propozycje
    phase-1.2a/                   pytania o wskaźniki (agents-issues-0), wyjaśnienie M1
    phase-2/                      instrukcje (dla autora), pytania o silnik regresji
  todo/
    author/                       zadania autora A… (WAŻNE / ŚREDNIE / MAŁE), raport autora, instrukcja
    llm/                          zadania agentów L…, raport agentów, instrukcja
  talk/
    od-autora-dla-llmow.md        ogólne uwagi autora (agenci tylko oznaczają jako przeczytane)
    wymiana-zdan-A1.md            dłuższa rozmowa
```

## Zasady

1. **Wszystko o jednej fazie leży w jej folderze** w `phases/`. W `todo/` i `talk/` są tylko rzeczy wspólne dla wielu faz.
2. **Pytania agentów**: `phases/<faza>/agents-issues-N.md`, każde z polem **Decyzja** dla autora. Każda nowa runda pytań to kolejny numer N.
3. **Zadania**: autor `A…`, agenci `L…`. Statusy `[ ]` `[~]` `[x]` `[?]` `[>]` `[-]`, nic nie jest usuwane. Szczegóły: `todo/author/INSTRUKCJA.md`, `todo/llm/INSTRUKCJA.md`.
4. **Wcześniejszych wypowiedzi się nie edytuje** (wymiana zdań, raporty, decyzje). Nowe dopisuje się na końcu.
5. **Bez polskich znaków w nazwach plików** (treść po polsku jak dotąd).
6. Kod i dane po angielsku: `simulator/README.md`, `data/README.md`.

## GUI: `python -m agents_board`

- Drzewo: co czeka na autora (pytania bez decyzji, zadania A, wymiana zdań), zadania agentów, wszystkie pliki.
- Po kliknięciu pozycji widać jej pełny tekst, a pod nim pole odpowiedzi. Tekst zostaje na ekranie podczas pisania.
- Odpowiedzi trafiają do właściwych plików `.md` (pole Decyzja, raport autora, wymiana zdań), a pliki dalej można edytować ręcznie.
- `python -m agents_board --read-only` — tylko podgląd.
- Pole tekstowe jak w VS Code: Tab / Shift+Tab — wcięcie, Enter na liście — następny punkt (pusty punkt kończy listę), Ctrl+Enter — wyślij. Podpis (Autor, data, godzina) dodaje się sam.

## Stare ścieżki (przed 2026-10-14)

Starsze wpisy (wymiana zdań, decyzje, raporty) odwołują się do dawnych ścieżek, a te wpisy się nie zmienia. Tłumaczenie:

| Dawniej | Teraz |
|---|---|
| `AGENTS/phase-1/…`, `AGENTS/phase-1.2a/…`, `AGENTS/phase-2/…` | `AGENTS/phases/phase-…/…` |
| `AGENTS/phases-plans.md`, `phases-description.md`, `future-work.md` | `AGENTS/plan/…` |
| `Conversations/TODOs/…`, `Conversations/TODOs-Author/…` | `AGENTS/todo/author/…` |
| `Conversations/TODOs-LLM/…` | `AGENTS/todo/llm/…` |
| `Conversations/od-autora-dla-llmów.md` | `AGENTS/talk/od-autora-dla-llmow.md` |
| `Conversations/wymiana-zdan-A1.md` | `AGENTS/talk/wymiana-zdan-A1.md` |
| `Conversations/phase-1.md` | `AGENTS/phases/phase-1/notes.md` |
| `Conversations/phase-1.2-propozycje-wypelniania.md` | `AGENTS/phases/phase-1/propozycje-wypelniania.md` |
| `Conversations/M1-wskazniki.md` | `AGENTS/phases/phase-1.2a/M1-wskazniki.md` |
