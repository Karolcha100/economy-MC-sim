# Przyszłe prace (backlog)

Rzeczy zgłoszone przez autora lub agentów, których nie robimy w bieżącej fazie. Każdy punkt: data, źródło, opis.

1. **GUI do edycji danych** (uwaga 2026-10-14: GUI do zadań i odpowiedzi już jest — `agents_board`; tu chodzi o dane scenariusza, może trafić do tej samej aplikacji) (2026-10-13, autor, `agents-issues-3.md` L1) — skrypt z interfejsem graficznym do przeglądania i edycji wzorów (w tym opisów `description` i wartości `default`) oraz danych opisowych, zamiast ręcznej edycji CSV / komend CLI.
2. **Organizacje dynamiczne** (2026-10-13, autor, `agents-issues-1.md` E4) — organizacje (sojusze, UE, NATO…) złożone z państw, zmieniające się w czasie. Pierwszy krok już jest: `groups.csv` (członkostwo z latami).
3. **Git LFS / Parquet dla `narrated/`** (2026-10-13, `agents-issues-2.md` H3) — gdy rozmiar CSV zacznie przeszkadzać.
4. **Inne sposoby rozgałęziania scenariuszy** (2026-10-14, wątek T010; wybrane: drzewo z `branching` na rok, domyślnie [10, 10, 10, 10]). Warto wrócić, gdy będzie potrzebny dłuższy horyzont albo więcej różnorodności:
   - **rozgałęzianie z przycinaniem** (filtr cząsteczkowy): b dzieci, potem losowo zostaje stałe N — liczba scenariuszy nie rośnie, horyzont może być długi;
   - **N/10 albo √N dzieci** na scenariusz (pomysł autora z R3) — przy dużym N tylko z przycinaniem;
   - **klasyczne Monte Carlo** (b = 1, N niezależnych ścieżek) — najtańsze, dobre do backtestu;
   - **zapis osobnych linii** zamiast drzewa — prostszy odczyt pojedynczego scenariusza, ~3,6× więcej miejsca przy b = 10.

