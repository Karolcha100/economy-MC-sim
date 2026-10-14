# Test modeli przed 1.2b — wyniki (Haiku w Claude Code)

Opis testu: @T015. Dane surowe: `AGENTS/phases/phase-1.2b/test-modeli/haiku-run1.jsonl`, `haiku-run2.jsonl`; miary: `AGENTS/phases/phase-1.2b/test-modeli/wyniki.json`.

*2026-10-14 06:33 — Claude Opus 5.5*

---

## Jak przeprowadzony

- **Model:** Haiku jako agent Claude Code (decyzja autora w @T015: tylko Haiku, przez Claude Code). Bez narzędzi i bez wyszukiwarki, czyli wariant B: sama wiedza modelu.
- **Zadanie:** 10 krajów (CHE, NOR, POL, DEU, RUS, UKR, BRA, IND, NGA, SOM) × `stability` i `corruption` za lata 1996–2022.
  - Model dostał opisy statystyk z `formulas/` i kotwice z dwóch krajów spoza testu (Finlandia, Afganistan, lata 2000/2010/2020).
  - Nie dostał wartości startowych.
- **Dwie niezależne serie** (20 agentów, ~26 tys. tokenów każdy, ~10 s każdy).
- **Porównanie z wartościami z WGI** przeliczonymi tak jak wartości startowe (W1, W2); 24 lata z pomiarem WGI.

## Wyniki

| Miara | `stability` | `corruption` |
|---|---|---|
| średni błąd (punkty 0–100), seria 1 / 2 | 18,1 / 18,8 | **4,3 / 5,9** |
| średnie przesunięcie (Haiku − WGI) | **+16,4 / +18,0** | +1,2 / +3,4 |
| zgodność kolejności krajów (pary różniące się o ≥5 pkt) | 85% / 90% | **99% / 96%** |
| różnica między dwiema seriami | 3,8 | 3,5 |
| zgodność zmian w czasie w obrębie kraju (korelacja) | 0,41 / 0,30 | 0,19 / 0,20 |

Średni błąd w poszczególnych krajach (`stability`):
- małe: POL 4, UKR 9, BRA 10, SOM 10;
- średnie: CHE 16, NOR 18;
- duże: DEU 22, NGA 24, RUS 29, **IND 41**.

## Wnioski

1. **`corruption`: Haiku bardzo dobry.** Błąd ~5 punktów, prawie idealna kolejność krajów i stabilne odpowiedzi.
2. **`stability`: duża, systematyczna różnica (+17), ale wynika głównie z definicji.**
   - WGI "Political Stability and **Absence of Violence/Terrorism**" mierzy ryzyko przemocy, stąd niskie Indie (~30) i Rosja (~30).
   - Nasz opis ("stabilność polityczna i instytucjonalna", 100 = w pełni stabilne instytucje) prowadzi Haiku do wysokich ocen Indii (~70) i Niemiec (~89).
   - Dodatkowo nasze przeliczenie WGI (50 + 20 × WGI) daje stabilnym demokracjom tylko 64–77, a według opisu powinny mieć ~90.
   - To problem **wartości startowych lub opisu**, a nie Haiku.
3. **Powtarzalność dobra:** dwie serie różnią się średnio o ~4 punkty.
4. **Zmiany rok do roku słabo zgodne** z WGI (korelacja 0,2–0,4). WGI ma jednak duży szum między latami, więc to słaba miara.
5. **Według progu bezwzględnego** (błąd ≤ 10 i kolejność ≥ 85%): `corruption` zdaje, `stability` nie zdaje, ale z powodu definicji.

## Rekomendacja

- **Haiku nadaje się do wypełniania** (wariant B). Przegląd Sonnetem nadal jest wskazany dla trudnych statystyk.
- **Przed startem trzeba rozstrzygnąć `stability`** (@A30): czy definicja ma obejmować przemoc i terroryzm jak WGI, czy przeliczenie WGI trzeba zmienić.
- Ograniczenia testu:
  - 10 krajów to mała próba;
  - sprawdzone tylko 2 statystyki z obiektywnym odniesieniem;
  - Haiku w Claude Code to model wybrany przez Claude Code; wersji nie da się tu potwierdzić.

## Decyzja po teście (2026-10-14 06:43)

Autor wybrał opcję (c), @A30: `stability` rozdzielone na `stability` (instytucje, wypełnia LLM) i `violence risk` (wartości startowe z WGI: 50 − 20 × WGI).
