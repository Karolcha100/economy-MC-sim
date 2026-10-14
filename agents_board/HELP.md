# Jak korzystać z AGENTS board

Uruchomienie: `venv/bin/python -m agents_board` (otwiera przeglądarkę). Tylko podgląd: `--read-only`. Plik HTML bez serwera: `--static plik.html`.

Wszystko, co tu piszesz, trafia do zwykłych plików `.md` w `AGENTS/`, więc dalej możesz je też edytować w VS Code. Jeśli plik zmienił się od otwarcia strony, zapis jest odrzucany, a Twój szkic zostaje. Wtedy kliknij **Odśwież**.

## Górny pasek

- **Drzewo** wybiera, co widać w menu po lewej:
  - **Co czeka na mnie**: pytania bez decyzji, Twoje otwarte zadania, wątki z odpowiedzią agenta, ➕ Nowy wątek, uwagi dla agentów;
  - **Wymiana zdań (wątki)**: wszystkie wątki z wpisami (🧑 Ty, 🤖 agent), odgałęzienia pod rodzicem, grupy „Zamknięte” i „Archiwum”;
  - **Według rodzaju**: pytania (fazy → pliki), zadania autora (Ważne / Średnie / Małe), zadania agentów, wątki;
  - **Według plików**: wszystkie pliki `AGENTS/`;
  - **Graf**: to samo co „Według rodzaju” jako drzewo 2D. Klik w kółko grupy zwija/rozwija, klik w węzeł otwiera szczegóły. Kolor = status, **czerwone krawędzie** = odwołania (numery i wzmianki @ w tekstach).
- **📋 Briefing**: podsumowanie ostatniej sesji agenta, czyli to samo, co w okienku czatu. Wcześniejsze briefingi są jako linki nad tekstem.
- **❓ Instrukcja**: ten tekst.
- **Odśwież**: wczytuje pliki ponownie (np. po pracy agenta).

## Okna

- **Menu po lewej**, **okno główne** w środku i opcjonalne **okno przypięte** po prawej (przycisk **📌 Przypnij obok** w nagłówku dowolnej pozycji; ✕ zamyka). Dzięki temu możesz np. czytać briefing obok wątku.
- **Pole odpowiedzi jest jedno** i zawsze dotyczy okna głównego.
- Szerokość menu i okna przypiętego oraz wysokość pola odpowiedzi zmieniasz, przeciągając szare paski między nimi. Ustawienia się zapamiętują.

## Odpowiadanie

| Co zaznaczysz | Co możesz zrobić |
|---|---|
| pytanie bez decyzji (❓) | wpisać **decyzję**; trafia do pola „Decyzja” w pliku pytań |
| Twoje zadanie (A…) | dodać **wpis do raportu** i/lub zmienić **status** |
| wątek | **odpowiedzieć**, **🔒 zamknąć** (tekst z pola jako uwaga), **↳ założyć nowy wątek od tego** |
| ➕ Nowy wątek | założyć nowy temat (tytuł + treść) |
| Uwagi dla LLM | dodać uwagę dla wszystkich agentów |

- Odgałęzienie pokazuje najpierw rozmowę z wątku-rodzica do momentu odgałęzienia, a potem własne wpisy.
- Podpis (Autor, data, godzina) dodaje się sam. Szkic zapisuje się sam w przeglądarce.

## Klawisze w polu tekstowym

- **Tab / Shift+Tab**: wcięcie (też dla kilku zaznaczonych linii);
- **Enter** w punkcie listy (`-` albo `1.`): następny punkt; Enter na pustym punkcie kończy listę; Tab w punkcie listy tworzy podlistę;
- **Ctrl+Enter**: wyślij;
- **@**: wzmianka, czyli lista do wyboru (strzałki, Enter/Tab, Esc):
  - `@T002`: wątek;
  - `@A12` / `@L3`: zadanie;
  - `@phase-2:R1`: pytanie.

  W tekście wzmianka jest linkiem, a w grafie krawędzią.

## Statusy zadań

🟠 do zrobienia · 🔵 w toku · ⏸️ czeka · ✅ zrobione · ➡️ przeniesione · ❌ porzucone. Zadań się nie usuwa, tylko zmienia status.
