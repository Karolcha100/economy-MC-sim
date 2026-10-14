

### [L50] Wyrzucenie 31 państw (oraz @L45, @L46, K3)

- **@L50:** nowa komenda `drop-tags` (`simulator/drop.py`, CLI, test `test_drop_tags_removes_country_everywhere`, opis w `simulator/README.md`). Usunięte: ERI, GNB, GNQ, TLS, FJI, SLB, CPV, BRN, BHS, VUT, BRB, STP, WSM, LCA, KIR, SYC, GRD, FSM, TON, VCT, ATG, AND, DMA, KNA, LIE, MCO, MHL, SMR, PLW, NRU, TUV (zmienione: `tags.csv`, 9 plików historii, 2 diadyczne, 429 plików `narrated/`, `confirmed-defaults.csv`). Zostało 165 państw. Kopia przed zmianą: `/home/karol/Pulpit/Python3.14/economics-model-backups/przed-drop-tags-2026-10-14-1623.tar.gz`. `queue.md`: `[-]`.
- **@L45 (K5):** `AGENTS/phases/phase-1.2b/batches-koordynator/K5-twn-chn.json`, 1413 operacji (skrypt z tabeli dat uznania; rok zmiany = nowy stan; po zerwaniu −30).
- **@L46 (K6):** `CODE_ALIASES` w `simulator/sources.py` (WGI: ROM/ZAR/WBG/KSV/ADO/TMP, OWID_KOS) + test; ponowny import `wgi-control-of-corruption`, `wgi-political-stability`, `happiness-cantril`; `K6-wgi-whr.json` (260 operacji: dane zamiast szacunków dla ROU, COD, PSE, XKX; lata poza danymi przesunięte o różnicę na granicy); granica BWA–ZMB w `data/manual/historical-land-borders.csv` + `seed --name neighbours`.
- **K3:** `K3-2025-lista.json` (14 operacji) według zaakceptowanej listy.
- `validate`: 0 błędów; `missing`: 100%; testy: 76.

*2026-10-14 16:28 — Claude Opus 5.5*

---
