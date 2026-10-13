opis phases dla agentów

# Phase 1 (Metody Generowania Danych Statystycznych)

### Phase 1.0 (Planowanie)

1. Należy uwzględnić co nie zostało doprecyzowane w `AGENTS/phase-1/agents-instructions.md`.

2. Agent/Agenci mają stworzyć dokument `AGENTS/phase-1/agents-issues.md` w języku Polskim.
    - Ten dokument ma zawierać problemy które nie zostały zaadresowane w `AGENTS/phase-1/agents-instructions.md` i które wymagają zaadresowania w tej fazie.

### Phase 1.1 (Implementacja)

1. Implementacja decyzji z `AGENTS/phase-1/agents-issues-*.md` (narzędzia w `simulator/`, opis w `simulator/README.md`).
2. Problemy wykryte w trakcie implementacji agenci zapisują w kolejnym pliku `AGENTS/phase-1/agents-issues-N.md`.
3. Kryteria ukończenia: zgodnie z decyzją F4 w `agents-issues-1.md` (templates, wzory, skrypty dla 3 templates z testami, import historii, kompletne i zwalidowane `tags.csv` oraz `dates.csv`).

### Phase 1.2 (Wypełnianie danych opisowych przez LLM)

1. Sposób wypełniania danych do uzgodnienia z autorem — propozycje agentów: `AGENTS/Conversations/phase-1.2-propozycje-wypelniania.md`.
2. Dane wypełniane wyłącznie przez `python -m simulator set/batch` (z `--author` i `--rationale`), po każdej partii `python -m simulator validate`.
