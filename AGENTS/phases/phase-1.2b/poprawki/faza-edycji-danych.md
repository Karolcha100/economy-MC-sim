# Faza edycji danych modelami LLM — wspólny start

Wspólne zadanie dla zmian w danych robionych przez modele LLM (@A34, @A35, @A40, @T021, @A39). Nic z tej listy nie rusza, dopóki nie napiszesz „start” w @A43.

*2026-10-14 16:27 — Claude Opus 5.5*

---

## Co masz zrobić

**Pytanie:** czy uruchamiamy teraz poniższe prace (wszystkie razem, w podanej kolejności)? Sprawdź też kolumnę „Model”: tak zrozumiałem Twoje odpowiedzi.

- Wystarczy: „start” (wszystko) albo „start bez …” / „zmień model w … na …”.
- Do tego czasu nie zmieniam danych w tych sprawach.

## Lista prac

| # | Praca | Plik z planem | Model (Twoja decyzja) | Koszt API (ok.) |
|---|---|---|---|---|
| 1 | Pilot założeń: spis ~20 założeń 1.2b + skrypt „co przestaje działać” | @T021 | Opus (T021: „niech będzie ten opus”) | 1 $ |
| 2 | K1: kod importu UCDP (kategorie par) + przegląd ok. 120 par według reguły | `AGENTS/phases/phase-1.2b/poprawki/K1-import-ucdp.md` | kod: Opus; przegląd: 3 × Haiku z głosowaniem, różnice sprawdza Opus (A34: „zgoda”) | 0,5 $ |
| 3 | K2: dopisanie ok. 40 brakujących konfliktów 1990–2024 (po pkt 2) | `AGENTS/phases/phase-1.2b/poprawki/K2-brakujace-konflikty.md` | Opus (A35: „wariant A”) | 3 $ |
| 4 | K4: wspólne zasady 5 flag (epidemia, kryzys migracyjny, zamieszki, upadek państwa, mobilizacja) | `AGENTS/phases/phase-1.2b/poprawki/K4-flagi.md` | Haiku, jeden agent na flagę; przypadki graniczne Opus (A40: „zgoda”) | 0,4 $ |
| 5 | Uzupełnienie `happiness` dla PRK i PNG (brak danych WHR) — opcjonalnie teraz albo później | @L51 | do ustalenia (proponuję Sonnet: 2 państwa, mało pracy) | < 0,5 $ |

Razem ok. 5 $ (API). W Claude Code — część limitu okresowego.

**Niejasność do potwierdzenia:** w @A35 napisałeś „wybieram wariant A, tak samo jak w innych zadaniach”. Zrozumiałem to jako: *w K2 Opus, a we wszystkich zadaniach najpierw wspólny task i wstrzymanie*. Jeśli chodziło o „Opus wszędzie” (także w K1 i K4 zamiast Haiku), napisz — koszt wzrośnie do ok. 7–8 $.

## Już zrobione (bez modeli, po Twojej zgodzie)

- @A39: usunięto 31 państw bez danych WHR (Kosowo zostaje, ma dane) — komenda `drop-tags`;
- @A37: relacje z Tajwanem i ChRL według dat uznania (1413 komórek);
- @A38: kody WGI/WHR naprawione, prawdziwe dane dla ROU, COD, PSE, XKX zamiast szacunków agentów; granica Zambia–Botswana; migracja bez zmian;
- @A36: ocena par na 2025 zapisana.

## Kolejność i kontrola

1 → 2 → 3 → 4 → 5. Po każdym kroku: `validate`, `missing` (100%), `audit`; batch każdego kroku w `AGENTS/phases/phase-1.2b/batches-koordynator/`. Zgłoszenia i wątpliwości — do pliku CSV, nie do raportów (wniosek z reguły 2025).
