# T013 · GUI - Znikanie zadań/wątków dopiero po przycisku koniec

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Proszę o dodanie do GUI przycisku [Koniec] który automatycznie pisze do ciebie prompta że odpowiedziałem na to co chciałem.

Do kliknięcia tego przycisku, wszelkie pliki z `Co czeka na mnie` powinny nie zniknąć (można je skreślić albo dać emotke oznaczającą wypełnienie - ale mają pozostać).

Dodatkowo przesuń przyciski Briefing i Instrukcja na Prawo, robiąc miejsce na przycisk "Plan" który otwiera generalny plan faz.

Na koniec, jeżeli podajesz mi jakiś plik do przeczytania/ocenienia, to go oznacz w taki sposób bym mógł kliknąć w jego ścieżkę i go otworzyć.

*2026-10-14 05:58 — Autor*

---
---
---

Zrobione (w kolejności z Twojej wiadomości):

1. **Przycisk "✅ Koniec"** (prawy górny róg):
   - pokazuje listę rzeczy, na które odpowiedziałeś w tej sesji;
   - po "Zakończ sesję" zapisuje ją do `AGENTS/talk/koniec/RRRR-MM-DD-GGMM.md`;
   - **kopiuje do schowka gotowy prompt**, np. "Odpowiedziałem w AGENTS board. Podsumowanie: AGENTS/talk/koniec/…md…". Wklejasz go w okno czatu.
   - **Ograniczenie:** przeglądarka nie może sama wysłać wiadomości do mojego okna czatu w VS Code, bo VS Code nie daje stronie takiej możliwości. Dlatego schowek + wklejenie (Ctrl+V, Enter). Agenci przy starcie sesji czytają najnowszy plik z `AGENTS/talk/koniec/` (dopisane do ich instrukcji).
2. **Nic nie znika przed "Koniec":** odpowiedziane pytania, zadania i wątki zostają w "Co czeka na mnie", skreślone i z ✔️. Znikają dopiero po zakończeniu sesji. Sprawdzone w Firefoksie: zadanie po zmianie statusu zostało ze ✔️ i zniknęło dopiero po "Koniec".
3. **Przyciski po prawej:** 🗺️ Plan (otwiera `AGENTS/plan/phases-plans.md`), 📋 Briefing, ❓ Instrukcja, Odśwież, ✅ Koniec.
4. **Klikalne ścieżki plików:**
   - każda ścieżka w tekście (np. `AGENTS/phases/phase-1.2b/plan.md`) jest linkiem;
   - pliki z `AGENTS/` otwierają się w GUI, inne (np. `simulator/scenarios/world-1990-2025/seeds.csv`) w VS Code;
   - w okienku czatu też podaję teraz pliki jako klikalne linki.

*2026-10-14 06:03 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-14 06:15 — Autor*

---
---
---
