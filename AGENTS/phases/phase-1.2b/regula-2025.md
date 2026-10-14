# Reguła „tylko 2025” — skąd się wzięła i jak uniknąć podobnych ograniczeń

Odpowiedź na @phase-1.2b:K2. Plan uzupełnienia brakujących konfliktów: `AGENTS/phases/phase-1.2b/plan-poprawek.md` (sekcja K2).

*2026-10-14 13:55 — Claude Opus 5.5*

---

## Co mówi reguła

W `AGENTS/phases/phase-1.2b/prompt-agenta.md` (pkt 5, dodane 07:20):

> relacje dwustronne (`in war`, `in war crisis`): **dopisuj tylko rok 2025** (…). Wpisów z lat 1990–2024 nie zmieniaj ani nie przenoś między `in war` a `in war crisis`; wątpliwości opisz w odpowiedzi końcowej, a rozstrzygnie je koordynator.

## Jak do niej doszło

1. **Pierwotny plan** (`AGENTS/phases/phase-1.2b/instrukcja-wypelniania.md`, pkt 6.3): każdy agent przegląda pary UCDP swojego państwa, usuwa niepasujące i dopisuje brakujące.
2. **Pierwsza godzina pracy** pokazała, że **każda para należy do dwóch państw**, więc robią ją dwaj różni agenci:
   - agent USA przeniósł IRQ 1991 i SRB 1999 z `in war crisis` do `in war`, a agenci DEU, CZE i HUN zostawili `in war crisis`;
   - agent UKR usunął parę UKR–RWA 2022, a agent RWA ją zostawił;
   - ostatni zapis nadpisywał poprzedni, więc wynik zależał od kolejności, w jakiej agenci kończyli pracę.
3. **Decyzja o 07:20:** żeby powstrzymać ten chaos, zamroziłem lata 1990–2024 i pozwoliłem tylko dopisywać 2025. Wątpliwości agenci mieli zgłaszać w raporcie, a rozstrzygnąć miał je koordynator na końcu.

## Dlaczego to było niezamierzone ograniczenie

- Reguła miała **zatrzymać zmiany sprzeczne między agentami**. W praktyce zablokowała też **dopisywanie konfliktów, których UCDP w ogóle nie notuje** (Jugosławia 1991–95, LBN–ISR, KOR–PRK, wojny zastępcze w Afryce Zachodniej). Takie przypadki nie są sporne między agentami; po prostu ich brakuje.
- Agenci karnie trzymali się reguły i zgłaszali braki w raportach. Te zgłoszenia są zebrane w `AGENTS/phases/phase-1.2b/raport-wypelniania.md`, więc nic nie zginęło. Jest jednak ok. 40 par do uzupełnienia osobnym krokiem.
- Do tego `confirm-default` zatwierdził puste komórki tych par jako wartość domyślną (0). Teraz `missing` pokazuje 100%, choć dane są niepełne. Wartość „potwierdzona domyślna” nie odróżnia „sprawdziłem, nie było konfliktu” od „nie wolno mi było wpisać”.

## Co wdrożyć, żeby tego uniknąć

1. **Komórki wspólne dla dwóch państw** (relacje dwustronne) nie powinny być zadaniem agentów krajowych. Lepiej osobne zadanie „przegląd par” robione przez jednego agenta z jedną regułą. Agenci krajowi tylko zgłaszają kandydatów.
2. **Reguła ograniczająca ma mieć ścieżkę dla wyjątków.** Każde „nie zmieniaj X” zapisujemy razem z „zamiast tego zapisz kandydata w pliku Y”. Plik zbiorczy w formacie CSV (`para, lata, typ, źródło`) pozwala potem dopisać pary skryptem, bez czytania 392 raportów.
3. **`confirm-default` nie zatwierdza komórek, których dotyczy zgłoszenie.** Agent potwierdza wartości domyślne z listą wyjątków, np. opcją `--except PAIRS`, którą trzeba by dodać do narzędzia.
4. **Plan ma przewidywać krok koordynatora** po fali agentów. Tym razem zrobiłem go ad hoc; w planie 1.2b brakowało punktu „rozstrzygnięcie zgłoszeń”.
5. **Pilotaż na różnych państwach przed pełną falą:** jedno państwo z wojnami, np. SRB lub RWA, i jedno bez. Pilot na POL nie pokazał problemu z parami.
6. **Jedno źródło zasad:** `instrukcja-wypelniania.md` i `prompt-agenta.md` mówiły co innego w sprawie UCDP, a agenci to zauważali (np. TON-B). Przy zmianie reguły w prompcie trzeba też poprawić instrukcję albo jawnie napisać, że prompt ją zastępuje.

Punkty 1–6 dopiszę do instrukcji i planów kolejnych faz po Twojej akceptacji (@A35).
