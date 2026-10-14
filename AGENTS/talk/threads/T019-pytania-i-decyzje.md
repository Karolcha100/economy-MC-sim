# T019 · Pytania i decyzje

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Powinienem w GUI (w plikach też to powinno być) mieć możliwość prze-konwertowania pytania do raportu, do todo lub do obydwu, w obydwu wypadkach mogąc udzielić wstępnej odpowiedzi.

Pytanie zostaje zamknięte po tym jak w wymianie zdań pod todo, uznam że sprawa jest zakończona, wtedy mogę udzielić "końcowej" odpowiedzi na pytanie, bądź automatycznie kliknąć żebyś wygenerował w pytaniu "końcową" propozycję, na którą mam zaakceptować (bądź nie, jeżeli nie, to proces się powtarza).

*2026-10-14 13:45 — Autor*

---
---
---

Przepraszam za zwłokę — ten wątek nie trafił do listy z przycisku Koniec (błąd, naprawiony: @T020).

**Propozycja, jak to zrobić** (zmienia format plików pytań, więc najpierw Twoja zgoda: @A42):

1. **Na otwartym pytaniu** (❓) obok „Zapisz decyzję” nowy przycisk **↪ Przenieś do zadania** z polami:
   - wstępna odpowiedź (opcjonalnie);
   - dokąd: zadanie (Ważne / Średnie / Małe), raport, albo oba.
2. **Co się dzieje w plikach:**
   - powstaje zadanie, np. `- [ ] **A43. K1: tytuł pytania** — z pytania @phase-1.2b:K1 …`;
   - jeśli wybrałeś raport: wpis `### [A43] …` z Twoją wstępną odpowiedzią;
   - w pytaniu pole Decyzja dostaje `⏳ w toku → @A43 (wstępnie: …)`. Pytanie przestaje być ❓, w drzewie ma 🔄.
3. **Rozmowa** toczy się pod zadaniem (wpisy w raporcie i odpowiedzi agentów — jak dziś).
4. **Zamknięcie:** gdy uznasz sprawę za skończoną, na pytaniu (albo przy zmianie statusu zadania na [x]) masz dwie drogi:
   - **✍️ Odpowiedź końcowa** — piszesz sam, trafia do Decyzji jako `✅ … (po @A43)`;
   - **🤖 Poproś o propozycję końcową** — w pytaniu pojawia się pole `- **Propozycja końcowa:** (czeka na agenta)`. Agent w następnej sesji wpisuje tam propozycję, a Ty klikasz **Akceptuję** (trafia do Decyzji jako ✅) albo **Nie** (pytanie wraca do 🔄 z Twoim komentarzem i proces się powtarza).
5. **Zmiany techniczne:** nowy status pytania „w toku”, nowe pole „Propozycja końcowa”, kod GUI i parsera (`agents_board/model.py`), testy, opis w `AGENTS/todo/llm/INSTRUKCJA.md` i `agents_board/HELP.md`.

Jeśli to pasuje — napisz „zgoda” w @A42 (albo popraw punkty), wdrożę jako @L49.

*2026-10-14 14:31 — Claude Opus 5.5*

---
---
---

zgoda

*2026-10-14 15:12 — Autor*

---
---
---

Wdrożone (@L49), tak jak w propozycji:
- **otwarte pytanie (❓):** obok „Zapisz decyzję” jest **↪ Przenieś** z wyborem: zadanie + raport / tylko zadanie / tylko raport oraz priorytet zadania. Tekst z pola to wstępna odpowiedź. Pytanie dostaje Decyzję `⏳ w toku → @A…` i ikonę 🔄;
- **pytanie w toku (🔄):** **✍️ Zapisz odpowiedź końcową** (Decyzja `✅ … (po @A…)`) albo **🤖 Poproś o propozycję końcową**. Pod pytaniem widać rozmowę z raportu przy tym zadaniu;
- **propozycja agenta (🤖, czeka na Ciebie):** **✅ Akceptuję** albo **❌ Nie** (komentarz z pola) — wtedy sprawa wraca do 🔄;
- zasady dla agentów: `AGENTS/todo/llm/INSTRUKCJA.md` („Pytania przeniesione do zadań”); opis w ❓ Instrukcji GUI.

Testy: 2 nowe (razem 74). Uruchom serwer od nowa, żeby zobaczyć zmiany.

*2026-10-14 15:23 — Claude Opus 5.5*

---
---
---

Okej, zostawiam na razie otwarte

*2026-10-14 15:46 — Autor*

---
---
---
