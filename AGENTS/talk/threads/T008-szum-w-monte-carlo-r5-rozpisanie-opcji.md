# T008 · Szum w Monte Carlo (R5) — rozpisanie opcji

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Rozpisanie decyzji @phase-2:R5, jak prosiłeś. Szum to niepewność, której model nie wyjaśnia: każdy nowy scenariusz = poprzedni + szum (@phase-2:R4). Dotyczy statystyk ciągłych; zdarzenia (0/1) losujemy osobno z ich prawdopodobieństw.

**1. Stały mały szum z konfiguracji** — np. ±2% zakresu statystyki (`noise_fixed_share`).
- Plusy: najprostszy, w pełni kontrolowany.
- Minusy: Szwajcaria i Somalia dostają ten sam szum, a GDP i `stability` tak samo, choć zmieniają się zupełnie inaczej. Wartość jest arbitralna.

**2. Szum ze średniej historycznej** — dla każdego kraju i statystyki osobno: typowy błąd modelu w latach 1990–2025 (odchylenie standardowe reszt).
- Plusy: Somalia dostaje większy szum niż Szwajcaria, PKB realne wahania; tani.
- Minusy: kraje losowane niezależnie, więc **wspólne kryzysy** (2008–09, 2020) są niedoszacowane. Przy 196 krajach losowe wstrząsy się znoszą.

**3. Bootstrap** — losujemy rok z historii (np. 2009) i dodajemy błędy modelu *wszystkich krajów i statystyk z tego roku*.
- Plusy: zachowuje to, że kryzysy przychodzą naraz i się korelują (Europa 2009, Rosja+Ukraina 2014). Bez założeń o kształcie rozkładu.
- Minusy: tylko ~35 wzorców wstrząsów (powtarza historię), więc nie wymyśli kombinacji, jakiej nie było.
- **Nie jest zasobożerny:** tablica błędów to 35 lat × 196 krajów × ~25 statystyk ≈ 170 tys. liczb (ok. 1 MB), a losowanie to wybór numeru roku. Koszt jest pomijalny przy samym liczeniu modelu.

**Moja propozycja:**
- wszystkie trzy w konfiguracji (`noise = "fixed" | "historical" | "bootstrap"`), jak sugerowałeś;
- domyślnie **bootstrap + mały stały szum na wierzch**, żeby scenariusze nie były dokładnymi kopiami historii;
- "historical" jako szybka alternatywa, "fixed" do testów;
- backtest porówna, która opcja daje najlepiej skalibrowane prawdopodobieństwa.

Zgoda? Odpowiedz tutaj (zadanie @A21).

*2026-10-14 03:24 — Claude Opus 5.5*

---
---
---

Zgoda, można zamykać ten wątek,

*2026-10-14 03:36 — Autor*

---
---
---

🔒 Wątek zamknięty — za zgodą autora ("Zgoda, można zamykać ten wątek"). Wybrana opcja w projekcie: bootstrap + mały stały szum, pozostałe w konfiguracji.

*2026-10-14 04:11 — Claude Opus 5.5*

---
---
---
