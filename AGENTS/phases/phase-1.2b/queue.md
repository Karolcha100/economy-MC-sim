# Phase 1.2b — kolejka zadań

Zasady: `instrukcja-wypelniania.md`. Bierzesz zadanie: w kolumnie wpisz `[~] model, RRRR-MM-DD GG:MM`;
kończysz: `[x]` + krótka notka w kolumnie Uwagi (liczba operacji, ostrzeżenia `review`, czego brakuje).
Postęp liczbowo: `python -m simulator --scenario world-1990-2025 missing --by-country`.

| # | tag | państwo | grupa | A: statystyki | B: relacje | uwagi |
|---|---|---|---|---|---|---|
| 1 | CHE | Switzerland | referencyjny | [x] 2026-10-14 07:13 | [x] 2026-10-14 07:14 | A: 27 op., review 0; B: 239 op., 24 partnerów, review 0 |
| 2 | NOR | Norway | referencyjny | [x] 2026-10-14 07:13 | [x] 2026-10-14 07:14 | A: 28 op., review 0; B: 183 op., 22 partnerów, review 0 |
| 3 | USA | United States | referencyjny | [x] 2026-10-14 07:14 | [x] 2026-10-14 07:20 | A: 56 op., review 1 (popularity 1992, uzasadnione); B: 566 op., 35 partnerów, review 0; in war 1991 IRQ / 1999 SRB / 2025 IRN, YEM — do przeglądu |
| 4 | DEU | Germany | referencyjny | [x] 2026-10-14 07:14 | [x] 2026-10-14 07:16 | A: 62 op., review 0; B: 202 op., 32 partnerów; review 3 (RUS 2014/2022, USA 2025, uzasadnione) |
| 5 | POL | Poland | referencyjny | [x] 2026-10-14 07:08 | [x] 2026-10-14 07:08 | pilot; A: 45 op., B: 207 op., 23 partnerów; review: tylko `net migration` 2022–23 (dane) |
| 6 | RUS | Russian Federation | referencyjny | [x] 2026-10-14 07:15 | [x] 2026-10-14 07:17 | A: 97 op., review 0; B: 365 op., 40 partnerów; review: skoki 2008/2014/2022 (zdarzenia); in war 2025 dodane |
| 7 | UKR | Ukraine | referencyjny | [x] 2026-10-14 07:14 | [x] 2026-10-14 07:16 | A: 69 op., review: skoki 2014/2019/2022 uzasadnione; B: 570 op., 21 partnerów; review: skoki 2014/2022 uzasadnione; in war 2025 dodane |
| 8 | CHN | China | referencyjny | [x] 2026-10-14 07:15 | [x] 2026-10-14 07:16 | A: 40 op., review 0; riots 2019 (HK) do przeglądu; B: 570 op., 30 partnerów, review 0; in war crisis/hybrid do przeglądu |
| 9 | IND | India | referencyjny | [x] 2026-10-14 07:15 | [x] 2026-10-14 07:18 | A: 53 op., review 0; B: 369 op., 24 partnerów; review 3 skoki (AFG 2002/2021, CAN 2023) |
| 10 | BRA | Brazil | referencyjny | [x] 2026-10-14 07:14 | [x] 2026-10-14 07:14 | A: 44 op., review 0; B: 195 op., 28 partnerów; review 2 (VEN 2019, ISR 2023, uzasadnione) |
| 11 | TUR | Turkiye | referencyjny | [x] 2026-10-14 07:14 | [x] 2026-10-14 07:17 | A: 53 op., review 0; riots 2024–25 do przeglądu; B: 328 op., 29 partnerów; review 9 skoków (zdarzenia) |
| 12 | IRN | Iran, Islamic Rep. | referencyjny | [x] 2026-10-14 07:18 | [x] 2026-10-14 07:21 | A: 61 op., review 0; B: 352 op., 30 partnerów; review: skoki 2002/2003/2011/2023/2025 (zdarzenia) |
| 13 | VEN | Venezuela, RB | referencyjny | [x] 2026-10-14 07:20 | [x] 2026-10-14 07:21 | A: 71 op., review 0; B: 392 op., 21 partnerów; review: skoki 2022/2024 (zdarzenia) |
| 14 | SYR | Syrian Arab Republic | referencyjny | [x] 2026-10-14 07:19 | [x] 2026-10-14 07:22 | A: 51 op., review: skoki 2011/2013/2025 (zdarzenia); B: 314 op., 16 partnerów; review: skoki 2011/2025 (zdarzenia) |
| 15 | SOM | Somalia, Fed. Rep. | referencyjny | [x] 2026-10-14 07:22 | [x] 2026-10-14 07:23 | A: 63 op., review 0; B: 381 op., 19 partnerów; review: ETH 2024, ISR 2025 (zdarzenia) |
| 16 | BLR | Belarus | Tier 1 | [x] 2026-10-14 07:20 | [x] 2026-10-14 07:20 | B: 226 op., 17 partnerów; review 3 (USA/GBR 2020, RUS 1995); A: 53 op., review 0; luka: happiness 2022–25 (brak WHR) |
| 17 | LTU | Lithuania | Tier 1 | [x] 2026-10-14 07:20 | [x] 2026-10-14 07:21 | A: 41 op., review 0; B: 267 op., 17 partnerów, review 0 |
| 18 | LVA | Latvia | Tier 1 | [x] 2026-10-14 07:19 | [x] 2026-10-14 07:20 | A: 45 op., review 0; B: 490 op., 14 partnerów; review 1 (RUS 1995, wycofanie wojsk) |
| 19 | EST | Estonia | Tier 1 | [x] 2026-10-14 07:20 | [x] 2026-10-14 07:20 | A: 40 op., review 0; B: 166 op., 13 partnerów, review 0; crisis RUS 2025 |
| 20 | MDA | Moldova | Tier 1 | [x] 2026-10-14 07:22 | [x] 2026-10-14 07:23 | A: 62 op., review 0; B: 185 op., 13 partnerów, review 0 |
| 21 | GEO | Georgia | Tier 1 | [x] 2026-10-14 07:23 | [x] 2026-10-14 07:25 | A: 53 op., review: skoki 1992/2004 (zdarzenia); B: 266 op., 17 partnerów, review 0 |
| 22 | FRA | France | Tier 1 | [x] 2026-10-14 07:23 | [x] 2026-10-14 07:28 | A: 68 op., review 0; B: 426 op., 40 partnerów; review 18 skoków (zdarzenia) |
| 23 | GBR | United Kingdom | Tier 1 | [x] 2026-10-14 07:25 | [x] 2026-10-14 07:28 | A: 60 op., review 0; immigration crisis 2022–23 granicznie; B: 577 op., 26 partnerów; review 1 (SYR 2025) |
| 24 | FIN | Finland | Tier 1 | [x] 2026-10-14 07:24 | [x] 2026-10-14 07:25 | A: 33 op., review 0; B: 194 op., 20 partnerów, review 0 |
| 25 | SWE | Sweden | Tier 1 | [x] 2026-10-14 07:24 | [x] 2026-10-14 07:26 | A: 38 op., review 0; B: 213 op., 22 partnerów; review 5 skoków (zdarzenia) |
| 26 | CZE | Czechia | Tier 1 | [x] 2026-10-14 07:25 | [x] 2026-10-14 07:26 | A: 66 op., review 0; B: 279 op., 26 partnerów, review 0 |
| 27 | SVK | Slovak Republic | Tier 1 | [x] 2026-10-14 07:25 | [x] 2026-10-14 07:26 | A: 55 op., review 0; B: 150 op., 18 partnerów, review 0 |
| 28 | HUN | Hungary | Tier 1 | [x] 2026-10-14 07:26 | [x] 2026-10-14 07:28 | A: 53 op., review 0; B: 249 op., 20 partnerów, review 0 |
| 29 | ROU | Romania | Tier 1 | [x] 2026-10-14 07:28 | [x] 2026-10-14 07:29 | A: 83 op., review 0; brak WGI (błąd importu) — estymacja; B: 186 op., 18 partnerów, review 0; crisis RUS 2025 |
| 30 | KAZ | Kazakhstan | Tier 1 | [x] 2026-10-14 07:27 | [x] 2026-10-14 07:27 | A: 33 op., review 0; B: 273 op., 20 partnerów, review 0 |
| 31 | ARM | Armenia | Tier 1 | [x] 2026-10-14 07:29 | [x] 2026-10-14 07:30 | A: 68 op., review 0; B: 231 op., 21 partnerów, review 0; crisis AZE 2025 |
| 32 | AZE | Azerbaijan | Tier 1 | [x] 2026-10-14 07:29 | [x] 2026-10-14 07:31 | A: 63 op., review 0; B: 525 op., 20 partnerów, review 0 |
| 33 | ITA | Italy | Tier 1 | [x] 2026-10-14 07:29 | [x] 2026-10-14 07:32 | A: 47 op., review 0; B: 728 op., 31 partnerów; review 1 (LBY 2011) |
| 34 | JPN | Japan |  | [x] 2026-10-14 07:29 | [x] 2026-10-14 07:29 | B: 179 op., 21 partnerów; review 1 (RUS 2022); A: 44 op., review: popularity 2001/2013 (zdarzenia) |
| 35 | CAN | Canada |  | [x] 2026-10-14 07:28 | [x] 2026-10-14 07:31 | A: 33 op., review 0; B: 109 op., 25 partnerów; review 3 skoki (zdarzenia) |
| 36 | ESP | Spain |  | [x] 2026-10-14 07:29 | [x] 2026-10-14 07:31 | A: 43 op., review 0; B: 127 op., 21 partnerów, review 0 |
| 37 | KOR | Korea, Rep. |  | [x] 2026-10-14 07:30 | [x] 2026-10-14 07:31 | A: 47 op., review: popularity 1993/1998 (zdarzenia); B: 126 op., 15 partnerów, review 0; crisis PRK 2025 |
| 38 | MEX | Mexico |  | [x] 2026-10-14 07:30 | [x] 2026-10-14 07:32 | A: 37 op., review: popularity 2019 (zdarzenie); B: 182 op., 22 partnerów, review 0 |
| 39 | AUS | Australia |  | [x] 2026-10-14 07:31 | [x] 2026-10-14 07:33 | A: 37 op., review 0; B: 385 op., 24 partnerów, review 0 |
| 40 | IDN | Indonesia |  | [x] 2026-10-14 07:32 | [x] 2026-10-14 07:34 | A: 50 op., review 2 (1998, zdarzenie); B: 348 op., 21 partnerów, review 0 |
| 41 | NLD | Netherlands |  | [x] 2026-10-14 07:32 | [x] 2026-10-14 07:32 | B: 185 op., 23 partnerów; review 2 (RUS 2014, MH17); A: 35 op., review 0 |
| 42 | SAU | Saudi Arabia |  | [x] 2026-10-14 07:32 | [x] 2026-10-14 07:33 | A: 36 op., review 0; B: 509 op., 25 partnerów; review: QAT 2017/2021, IRN 2023 (zdarzenia) |
| 43 | BEL | Belgium |  | [x] 2026-10-14 07:36 | [x] 2026-10-14 07:33 | B: 247 op., 30 partnerów; review 3 skoki (zdarzenia); A: 45 op., review 0 |
| 44 | IRL | Ireland |  | [x] 2026-10-14 07:32 | [x] 2026-10-14 07:34 | A: 52 op., review 0; B: 143 op., 17 partnerów; review 1 (ISR 2023) |
| 45 | ARG | Argentina |  | [x] 2026-10-14 07:34 | [x] 2026-10-14 07:35 | A: 64 op., review 0; B: 155 op., 20 partnerów; review 1 (VEN 2024) |
| 46 | ISR | Israel |  | [x] 2026-10-14 07:34 | [x] 2026-10-14 07:39 | A: 64 op., review 0; B: 249 op., 35 partnerów; review 4 (zdarzenia) |
| 47 | SGP | Singapore |  | [x] 2026-10-14 07:33 | [x] 2026-10-14 07:35 | A: 24 op., review 0; B: 202 op., 25 partnerów, review 0; neighbours do potwierdzenia |
| 48 | AUT | Austria |  | [x] 2026-10-14 07:34 | [x] 2026-10-14 07:35 | A: 50 op., review 0; B: 378 op., 21 partnerów; review 1 (SRB 1992) |
| 49 | THA | Thailand |  | [x] 2026-10-14 07:36 | [x] 2026-10-14 07:36 | A: 65 op., review 1 (2006 zamach); B: 533 op., 19 partnerów, review 0; in war KHM 2025 |
| 50 | ARE | United Arab Emirates |  | [x] 2026-10-14 07:35 | [x] 2026-10-14 07:37 | A: 27 op., review 0; B: 296 op., 31 partnerów; review: skoki (zdarzenia); crisis YEM 2025 |
| 51 | VNM | Viet Nam |  | [x] 2026-10-14 07:35 | [x] 2026-10-14 07:36 | A: 35 op., review 0; B: 208 op., 18 partnerów, review 0 |
| 52 | PHL | Philippines |  | [x] 2026-10-14 07:37 | [x] 2026-10-14 07:37 | A: 62 op., review 0; B: 195 op., 20 partnerów, review 0 |
| 53 | MYS | Malaysia |  | [x] 2026-10-14 07:37 | [x] 2026-10-14 07:37 | A: 41 op., review 1 (2018 zmiana rządu); B: 221 op., 27 partnerów, review 0 |
| 54 | DNK | Denmark |  | [x] 2026-10-14 07:37 | [x] 2026-10-14 07:39 | A: 30 op., review 0; B: 230 op., 22 partnerów, review 0 |
| 55 | COL | Colombia |  | [x] 2026-10-14 07:39 | [x] 2026-10-14 07:39 | B: 167 op., 23 partnerów; review 3 skoki (zdarzenia); A: 49 op., review 0 |
| 56 | BGD | Bangladesh |  | [x] 2026-10-14 07:38 | [x] 2026-10-14 07:39 | A: 41 op., review 0; B: 172 op., 16 partnerów, review 0 |
| 57 | ZAF | South Africa |  | [x] 2026-10-14 07:38 | [x] 2026-10-14 07:39 | A: 40 op., review 0; B: 358 op., 22 partnerów; review 6 skoków (zdarzenia); crisis RWA 2025 |
| 58 | PAK | Pakistan |  | [x] 2026-10-14 07:39 | [x] 2026-10-14 07:40 | A: 48 op., review 0; B: 168 op., 14 partnerów; review 2 (zdarzenia); in war AFG 2025 |
| 59 | EGY | Egypt, Arab Rep. |  | [x] 2026-10-14 07:40 | [x] 2026-10-14 07:41 | A: 38 op., review 1 (2011 rewolucja); B: 293 op., 27 partnerów; review: skoki (zdarzenia) |
| 60 | CHL | Chile |  | [x] 2026-10-14 07:38 | [x] 2026-10-14 07:41 | A: 36 op., review 0; B: 83 op., 26 partnerów, review 0 |
| 61 | PRT | Portugal |  | [x] 2026-10-14 07:41 | [x] 2026-10-14 07:41 | A: 38 op., review 0; B: 82 op., 43 partnerów (grupy), review 0 |
| 62 | PER | Peru |  | [x] 2026-10-14 07:42 | [x] 2026-10-14 07:42 | B: 332 op., 21 partnerów; review 3 (zdarzenia); crisis COL 2025; A: 52 op., review 0 |
| 63 | NGA | Nigeria |  | [x] 2026-10-14 07:40 | [x] 2026-10-14 07:42 | A: 44 op., review 0; B: 399 op., 24 partnerów, review 0 |
| 64 | DZA | Algeria |  | [x] 2026-10-14 07:42 | [x] 2026-10-14 07:43 | A: 58 op., review 0; B: 200 op., 20 partnerów; review 1 (ESP 2022); crisis MLI 2025 |
| 65 | GRC | Greece |  | [x] 2026-10-14 07:42 | [x] 2026-10-14 07:43 | A: 67 op., review 0; B: 114 op., 18 partnerów; review 1 (DEU 2010) |
| 66 | NZL | New Zealand |  | [x] 2026-10-14 07:42 | [x] 2026-10-14 07:43 | A: 36 op., review 0; B: 99 op., 30 partnerów, review 0 |
| 67 | IRQ | Iraq |  | [x] 2026-10-14 07:44 | [x] 2026-10-14 07:45 | A: 65 op., review: skoki 1991/2003 (zdarzenia); B: 264 op., 22 partnerów; review 4 (zdarzenia) |
| 68 | QAT | Qatar |  | [x] 2026-10-14 07:42 | [x] 2026-10-14 07:44 | A: 31 op., review 0; B: 688 op., 25 partnerów; review: skoki (zdarzenia); crisis ISR/IRN 2025 |
| 69 | MAR | Morocco |  | [x] 2026-10-14 07:43 | [x] 2026-10-14 07:45 | A: 37 op., review 0; B: 129 op., 23 partnerów, review 0; hybrid ESP 2021 |
| 70 | KWT | Kuwait |  | [x] 2026-10-14 07:44 | [x] 2026-10-14 07:44 | A: 41 op., review 0; B: 213 op., 24 partnerów; review: skoki 1992 (zdarzenia) |
| 71 | UZB | Uzbekistan |  | [x] 2026-10-14 07:44 | [x] 2026-10-14 07:46 | A: 30 op., review 0; B: 128 op., 23 partnerów; review 1 (USA 2005) |
| 72 | KEN | Kenya |  | [x] 2026-10-14 07:45 | [x] 2026-10-14 07:46 | A: 47 op., review 0; B: 206 op., 23 partnerów, review 0 |
| 73 | BGR | Bulgaria |  | [x] 2026-10-14 07:45 | [x] 2026-10-14 07:45 | B: 136 op., 13 partnerów, review 0; A: 35 op., review 1 (2013, zdarzenie) |
| 74 | ECU | Ecuador |  | [x] 2026-10-14 07:46 | [x] 2026-10-14 07:47 | A: 41 op., review 1 (popularity 2024); B: 214 op., 21 partnerów; review: skoki (zdarzenia) |
| 75 | DOM | Dominican Republic |  | [x] 2026-10-14 07:45 | [x] 2026-10-14 07:46 | A: 34 op., review 0; B: 194 op., 17 partnerów, review 0 |
| 76 | ETH | Ethiopia |  | [x] 2026-10-14 07:48 | [x] 2026-10-14 07:47 | B: 234 op., 24 partnerów; review 2 (ERI 1998/2018); crisis ERI 2025; A: 75 op., review 5 skoków (zdarzenia) |
| 77 | GTM | Guatemala |  | [x] 2026-10-14 07:47 | [x] 2026-10-14 07:47 | A: 47 op., review 0; B: 148 op., 24 partnerów, review 0 |
| 78 | AGO | Angola |  | [x] 2026-10-14 07:47 | [x] 2026-10-14 07:49 | A: 44 op., review 0; B: 136 op., 27 partnerów, review 0 |
| 79 | GHA | Ghana |  | [x] 2026-10-14 07:47 | [x] 2026-10-14 07:47 | A: 33 op., review 1 (2025 zmiana rządu); B: 217 op., 30 partnerów, review 0 |
| 80 | OMN | Oman |  | [x] 2026-10-14 07:48 | [x] 2026-10-14 07:48 | A: 28 op., review 0; B: 71 op., 21 partnerów, review 0 |
| 81 | LKA | Sri Lanka |  | [x] 2026-10-14 07:49 | [x] 2026-10-14 07:50 | A: 52 op., review 0; B: 230 op., 20 partnerów, review 0 |
| 82 | CUB | Cuba |  | [x] 2026-10-14 07:51 | [x] 2026-10-14 07:50 | B: 225 op., 24 partnerów, review 0; A: 38 op., review 0 |
| 83 | HRV | Croatia |  | [x] 2026-10-14 07:50 | [x] 2026-10-14 07:51 | A: 50 op., review 0; B: 426 op., 20 partnerów, review 0; doublesided 1991–95 luka (decyzja) |
| 84 | CRI | Costa Rica |  | [x] 2026-10-14 07:49 | [x] 2026-10-14 07:50 | A: 32 op., review 0; B: 78 op., 23 partnerów; review 1 (VEN 2020) |
| 85 | LUX | Luxembourg |  | [x] 2026-10-14 07:49 | [x] 2026-10-14 07:52 | A: 35 op., review 0; B: 128 op., 36 partnerów, review 0 |
| 86 | SRB | Serbia |  | [x] 2026-10-14 07:52 | [x] 2026-10-14 07:52 | B: 679 op., 23 partnerów; review: skoki 1992/1999/2000 (zdarzenia); A: 65 op., review 0 |
| 87 | CIV | Cote d'Ivoire |  | [x] 2026-10-14 07:51 | [x] 2026-10-14 07:53 | A: 55 op., review 0; B: 193 op., 23 partnerów; review 1 (BFA 2002) |
| 88 | COD | Congo, Dem. Rep. |  | [x] 2026-10-14 07:53 | [x] 2026-10-14 07:53 | A: 73 op., review 0; brak WGI — estymacja; B: 203 op., 20 partnerów; review: skoki (zdarzenia); crisis RWA 2025 |
| 89 | PAN | Panama |  | [x] 2026-10-14 07:51 | [x] 2026-10-14 07:55 | A: 35 op., review 0; B: 194 op., 24 partnerów, review 0 |
| 90 | TZA | Tanzania |  | [x] 2026-10-14 07:51 | [x] 2026-10-14 07:53 | A: 27 op., review 0; B: 177 op., 22 partnerów, review 0; crisis RWA 2025 |
| 91 | URY | Uruguay |  | [x] 2026-10-14 07:53 | [x] 2026-10-14 07:52 | B: 71 op., 14 partnerów, review 0; A: 28 op., review 0 |
| 92 | MMR | Myanmar |  | [x] 2026-10-14 07:54 | [x] 2026-10-14 07:54 | B: 225 op., 18 partnerów, review 0; A: 43 op., review 2 (2021 zamach) |
| 93 | SVN | Slovenia |  | [x] 2026-10-14 07:53 | [x] 2026-10-14 07:54 | A: 51 op., review 0; B: 142 op., 15 partnerów, review 0 |
| 94 | BOL | Bolivia |  | [x] 2026-10-14 07:54 | [x] 2026-10-14 07:59 | A: 56 op., review 4 skoki (zdarzenia); B: 193 op., 18 partnerów, review 0 |
| 95 | UGA | Uganda |  | [x] 2026-10-14 07:54 | [x] 2026-10-14 08:00 | A: 41 op., review 0; B: 241 op., 21 partnerów; review 1 (SOM 2007) |
| 96 | JOR | Jordan |  | [x] 2026-10-14 07:54 | [x] 2026-10-14 07:59 | A: 37 op., review 0; B: 314 op., 20 partnerów; review 2 (KWT 1993, ISR 1994) |
| 97 | SDN | Sudan |  | [x] 2026-10-14 07:58 | [x] 2026-10-14 08:01 | A: 52 op., review 1 (2023 wojna); B: 277 op., 22 partnerów; review 6 (zdarzenia); crisis ARE 2025 |
| 98 | CMR | Cameroon |  | [x] 2026-10-14 07:58 | [x] 2026-10-14 07:59 | A: 35 op., review 0; B: 66 op., 14 partnerów, review 0 |
| 99 | TUN | Tunisia |  | [x] 2026-10-14 07:58 | [x] 2026-10-14 08:01 | A: 33 op., review 0; B: 420 op., 20 partnerów, review 0 |
| 100 | KHM | Cambodia |  | [x] 2026-10-14 08:00 | [x] 2026-10-14 08:02 | A: 49 op., review 0; B: 175 op., 12 partnerów; review 1 (THA 2025) |
| 101 | ZWE | Zimbabwe |  | [x] 2026-10-14 08:00 | [x] 2026-10-14 08:01 | A: 51 op., review 0; B: 233 op., 21 partnerów; review 3 (zdarzenia); crisis RWA 2025 |
| 102 | TKM | Turkmenistan |  | [x] 2026-10-14 08:00 | [x] 2026-10-14 08:02 | A: 33 op., review 0; B: 132 op., 20 partnerów, review 0 |
| 103 | PRY | Paraguay |  | [x] 2026-10-14 08:01 | [x] 2026-10-14 08:02 | A: 43 op., review 0; B: 197 op., 23 partnerów, review 0 |
| 104 | BHR | Bahrain |  | [x] 2026-10-14 08:02 | [x] 2026-10-14 08:03 | A: 34 op., review 0; B: 183 op., 25 partnerów; review: skoki (zdarzenia); neighbours luka |
| 105 | LBY | Libya |  | [x] 2026-10-14 08:02 | [x] 2026-10-14 08:03 | A: 51 op., review 1 (2011); B: 927 op., 22 partnerów, review 0; crisis SDN 2025 |
| 106 | NPL | Nepal |  | [x] 2026-10-14 08:02 | [x] 2026-10-14 08:02 | A: 53 op., review 0; B: 193 op., 22 partnerów, review 0 |
| 107 | CYP | Cyprus |  | [x] 2026-10-14 08:02 | [x] 2026-10-14 08:05 | A: 40 op., review 0; B: 156 op., 17 partnerów, review 0 |
| 108 | HND | Honduras |  | [x] 2026-10-14 08:03 | [x] 2026-10-14 08:04 | A: 38 op., review 0; B: 94 op., 19 partnerów; review 2 (zdarzenia) |
| 109 | ISL | Iceland |  | [x] 2026-10-14 08:03 | [x] 2026-10-14 08:04 | A: 33 op., review 0; B: 174 op., 21 partnerów, review 0 |
| 110 | SEN | Senegal |  | [x] 2026-10-14 08:04 | [x] 2026-10-14 08:05 | A: 43 op., review 0; B: 250 op., 32 partnerów; review 1 (MRT 1992) |
| 111 | SLV | El Salvador |  | [x] 2026-10-14 08:05 | [x] 2026-10-14 08:05 | B: 125 op., 15 partnerów; review 2 (zdarzenia); A: 43 op., review 0 |
| 112 | BIH | Bosnia and Herzegovina |  | [x] 2026-10-14 08:04 | [x] 2026-10-14 08:07 | A: 40 op., review 0; B: 177 op., 15 partnerów, review 0 |
| 113 | PNG | Papua New Guinea |  | [x] 2026-10-14 08:06 | [x] 2026-10-14 08:06 | B: 194 op., 12 partnerów, review 0; A: 37 op., review 0 |
| 114 | HTI | Haiti |  | [x] 2026-10-14 08:06 | [x] 2026-10-14 08:07 | A: 56 op., review 0; B: 177 op., 10 partnerów; review 1 (USA 1995) |
| 115 | ALB | Albania |  | [x] 2026-10-14 08:06 | [x] 2026-10-14 08:06 | B: 140 op., 15 partnerów; review 1 (IRN 2022); A: 56 op., review 2 (1997, zdarzenie) |
| 116 | MLI | Mali |  | [x] 2026-10-14 08:07 | [x] 2026-10-14 08:07 | A: 60 op., review 1 (2012 zamach); B: 264 op., 21 partnerów; review: FRA 2022, UKR 2024 (zdarzenia) |
| 117 | ZMB | Zambia |  | [x] 2026-10-14 08:07 | [x] 2026-10-14 08:07 | B: 201 op., 20 partnerów, review 0; A: 48 op., review 1 (1991) |
| 118 | GIN | Guinea |  | [x] 2026-10-14 08:07 | [x] 2026-10-14 08:08 | A: 56 op., review 0; B: 194 op., 20 partnerów; review 1 (no-rationale, artefakt) |
| 119 | MLT | Malta |  | [x] 2026-10-14 08:07 | [x] 2026-10-14 08:07 | A: 31 op., review 0; B: 102 op., 13 partnerów, review 0 |
| 120 | BFA | Burkina Faso |  | [x] 2026-10-14 08:08 | [x] 2026-10-14 08:09 | A: 45 op., review 0; B: 215 op., 21 partnerów, review 0 |
| 121 | GUY | Guyana |  | [x] 2026-10-14 08:09 | [x] 2026-10-14 08:10 | A: 47 op., review 0; B: 183 op., 16 partnerów, review 0 |
| 122 | LBN | Lebanon |  | [x] 2026-10-14 08:11 | [x] 2026-10-14 08:11 | A: 48 op., review 0; B: 183 op., 20 partnerów, review 5 (2005/2011 SYR, 2001 ISR — uzasadnione) |
| 123 | TTO | Trinidad and Tobago |  | [x] 2026-10-14 08:09 | [x] 2026-10-14 08:11 | A: 43 op., review 0; B: 84 op., 28 partnerów, review 0 |
| 124 | MNG | Mongolia |  | [x] 2026-10-14 08:09 | [x] 2026-10-14 08:10 | A: 44 op., review 0; B: 122 op., 14 partnerów, review 0 |
| 125 | BEN | Benin |  | [x] 2026-10-14 08:10 | [x] 2026-10-14 08:11 | A: 32 op., review 0; B: 194 op., 26 partnerów, review 0 |
| 126 | JAM | Jamaica |  | [x] 2026-10-14 08:11 | [x] 2026-10-14 08:11 | A: 30 op., review 0; B: 152 op., 22 partnerów, review 0 |
| 127 | KGZ | Kyrgyz Republic |  | [x] 2026-10-14 08:11 | [x] 2026-10-14 08:11 | B: 164 op., 14 partnerów, review 0; A: 50 op., review 1 (rewolucja 2020, uzasadnione) |
| 128 | MOZ | Mozambique |  | [x] 2026-10-14 08:11 | [x] 2026-10-14 08:12 | A: 39 op., review 0; B: 261 op., 26 partnerów, review 0 |
| 129 | NIC | Nicaragua |  | [x] 2026-10-14 08:11 | [x] 2026-10-14 08:13 | A: 44 op., review 0; B: 213 op., 17 partnerów, review 1 (TWN 2021, uzasadnione) |
| 130 | NER | Niger |  | [x] 2026-10-14 08:11 | [x] 2026-10-14 08:14 | A: 64 op., review 2 (zamach 2023, uzasadnione); B: 112 op., 15 partnerów, review: skoki 2023 (zamach) i DZA 2025 — uzasadnione |
| 131 | YEM | Yemen, Rep. |  | [x] 2026-10-14 08:12 | [x] 2026-10-14 08:15 | A: 63 op., review 2 (1994, 2015 — uzasadnione); B: 287 op., 27 partnerów, review 0 |
| 132 | TCD | Chad |  | [x] 2026-10-14 08:12 | [x] 2026-10-14 08:13 | A: 34 op., review 0; B: 89 op., 13 partnerów, review 2 (FRA 2024, CMR 2003 — uzasadnione) |
| 133 | GAB | Gabon |  | [x] 2026-10-14 08:13 | [x] 2026-10-14 08:13 | B: 45 op., 16 partnerów, review 0; A: 43 op., review 0 |
| 134 | BWA | Botswana |  | [x] 2026-10-14 08:14 | [x] 2026-10-14 08:15 | A: 32 op., review 0; B: 105 op., 14 partnerów, review 0 |
| 135 | MDG | Madagascar |  | [x] 2026-10-14 08:15 | [x] 2026-10-14 08:16 | A: 57 op., review 3 (2009, 1993 — uzasadnione); B: 347 op., 17 partnerów, review 0 |
| 136 | MKD | North Macedonia |  | [x] 2026-10-14 08:15 | [x] 2026-10-14 08:15 | A: 51 op., review 0; B: 145 op., 13 partnerów, review 0 |
| 137 | LAO | Lao PDR |  | [x] 2026-10-14 08:14 | [x] 2026-10-14 08:14 | A: 26 op., review 0; B: 165 op., 18 partnerów, review 0 |
| 138 | AFG | Afghanistan |  | [x] 2026-10-14 08:16 | [x] 2026-10-14 08:17 | A: 61 op., review 2 (1996, 2002 — uzasadnione); B: 494 op., 21 partnerów, review ~70 (zmiany reżimu 1992/1996/2002/2021/2025 — uzasadnione) |
| 139 | TJK | Tajikistan |  | [x] 2026-10-14 08:15 | [x] 2026-10-14 08:15 | A: 41 op., review 2 (1992 wojna domowa — uzasadnione); B: 153 op., 15 partnerów, review 4 (AFG 1996/2001/2021, KGZ 2022 — uzasadnione) |
| 140 | PSE | West Bank and Gaza |  | [x] 2026-10-14 08:16 | [x] 2026-10-14 08:16 | A: 85 op., review 0; corruption/violence risk w całości szacunek (brak WGI); B: 177 op., 20 partnerów, review 1 (USA 2017 — uzasadnione) |
| 141 | RWA | Rwanda |  | [x] 2026-10-14 08:16 | [x] 2026-10-14 08:19 | A: 40 op., review 2 (1994 ludobójstwo — uzasadnione); B: 203 op., 17 partnerów, review 1 (COD 1996 — uzasadnione) |
| 142 | COG | Congo, Rep. |  | [x] 2026-10-14 08:16 | [x] 2026-10-14 08:17 | A: 39 op., review 0; B: 175 op., 22 partnerów, review 0 |
| 143 | MUS | Mauritius |  | [x] 2026-10-14 08:16 | [x] 2026-10-14 08:18 | A: 38 op., review 0; B: 131 op., 18 partnerów, review 0 |
| 144 | BHS | Bahamas, The |  | [x] 2026-10-14 08:17 | [x] 2026-10-14 08:18 | A: 30 op., review 0; B: 47 op., 11 partnerów, review 0 |
| 145 | NAM | Namibia |  | [x] 2026-10-14 08:17 | [x] 2026-10-14 08:18 | A: 37 op., review 0; B: 119 op., 14 partnerów, review 0 |
| 146 | BRN | Brunei Darussalam |  | [x] 2026-10-14 08:18 | [x] 2026-10-14 08:18 | A: 24 op., review 0; B: 156 op., 19 partnerów, review 1 (CHN 1991 — uzasadnione) |
| 147 | MWI | Malawi |  | [x] 2026-10-14 08:19 | [x] 2026-10-14 08:19 | B: 203 op., 17 partnerów, review 0; A: 43 op., review 0 |
| 148 | GNQ | Equatorial Guinea |  | [x] 2026-10-14 08:19 | [x] 2026-10-14 12:51 | A: 41 op., review 0; B: agent przerwany limitem API na końcu; dane 100%, validate 0, review 0 (bez raportu agenta) |
| 149 | XKX | Kosovo |  | [x] 2026-10-14 12:51 | [x] 2026-10-14 12:51 | A: 40 op., review 0; corruption/violence risk/HDI/happiness w całości szacunek; B: 111 op., 15 partnerów, review 0 |
| 150 | SSD | South Sudan |  | [x] 2026-10-14 12:51 | [x] 2026-10-14 08:20 | B: 161 op., 19 partnerów, review 0; A: agent przerwany limitem API na końcu; dane 100%, validate 0, review 0 (bez raportu agenta) |
| 151 | TGO | Togo |  | [x] 2026-10-14 08:19 | [x] 2026-10-14 12:54 | A: 37 op., review 0; B: 145 op., 17 partnerów, review 0 (ponowione po limicie API) |
| 152 | MRT | Mauritania |  | [x] 2026-10-14 12:51 | [x] 2026-10-14 12:57 | A: agent przerwany limitem API na końcu; dane 100%, validate 0, review 0 (bez raportu agenta); B: 107 op., 14 partnerów, review 0 (ponowione po limicie API) |
| 153 | MCO | Monaco |  | [x] 2026-10-14 12:51 | [x] 2026-10-14 12:51 | A: 24 op., review 0; B: agent przerwany limitem API na końcu; dane 100%, validate 0, review 0 (bez raportu agenta) |
| 154 | MNE | Montenegro |  | [x] 2026-10-14 12:56 | [x] 2026-10-14 12:56 | A: 20 op., review 0; B: 139 op., 17 partnerów, review 0 |
| 155 | LIE | Liechtenstein |  | [x] 2026-10-14 12:54 | [x] 2026-10-14 12:57 | A: 24 op., review 0 (ponowione po limicie API); B: 96 op., 12 partnerów, review 0 |
| 156 | BRB | Barbados |  | [x] 2026-10-14 12:54 | [x] 2026-10-14 12:56 | A: 34 op., review 0 (ponowione po limicie API); B: 189 op., 23 partnerów, review 0 |
| 157 | MDV | Maldives |  | [x] 2026-10-14 12:55 | [x] 2026-10-14 12:56 | A: 57 op., review 1 (2019 zmiana rządu — uzasadnione); B: 150 op., 18 partnerów, review 0 |
| 158 | SLE | Sierra Leone |  | [x] 2026-10-14 12:56 | [x] 2026-10-14 12:57 | A: 57 op., review 3 (1996/1997/2018 — uzasadnione); B: 164 op., 20 partnerów, review 0 |
| 159 | FJI | Fiji |  | [x] 2026-10-14 12:59 | [x] 2026-10-14 12:57 | A: 32 op., review 0; LUKA: happiness puste 1990–2025 (brak WHR) — missing 94.1%; B: 127 op., 15 partnerów, review 0; A: happiness uzupełnione (FJI-A-happiness.json, 7 op.) — missing 100% |
| 160 | LBR | Liberia |  | [x] 2026-10-14 12:57 | [x] 2026-10-14 12:57 | B: 119 op., 13 partnerów, review 0; A: 43 op., review 0 |
| 161 | SWZ | Eswatini |  | [x] 2026-10-14 12:55 | [x] 2026-10-14 12:56 | A: 31 op., review 0; B: 114 op., 14 partnerów, review 0 |
| 162 | DJI | Djibouti |  | [x] 2026-10-14 12:56 | [x] 2026-10-14 12:57 | A: 42 op., review 0; B: 151 op., 20 partnerów, review 4 (ERI 2008/2018, IRN 2016/2023 — uzasadnione) |
| 163 | SUR | Suriname |  | [x] 2026-10-14 12:58 | [x] 2026-10-14 12:58 | B: 146 op., 17 partnerów, review 0; A: 40 op., review 0 |
| 164 | AND | Andorra |  | [x] 2026-10-14 12:58 | [x] 2026-10-14 12:58 | A: 37 op., review 0; corruption/violence risk w całości szacunek (brak WGI); B: 76 op., 10 partnerów, review 0 |
| 165 | BTN | Bhutan |  | [x] 2026-10-14 12:58 | [x] 2026-10-14 12:59 | A: 28 op., review 0; happiness 2019–25 uzupełnione przez koordynatora (stała 50.82); B: 110 op., 14 partnerów, review 0 |
| 166 | BDI | Burundi |  | [x] 2026-10-14 13:00 | [x] 2026-10-14 13:01 | A: 54 op., review 0; B: 229 op., 20 partnerów, review 0 |
| 167 | BLZ | Belize |  | [x] 2026-10-14 12:59 | [x] 2026-10-14 12:59 | B: 77 op., 11 partnerów, review 0 (wartości stałe 1990–2025); A: 30 op., review 0 |
| 168 | CAF | Central African Republic |  | [x] 2026-10-14 13:00 | [x] 2026-10-14 13:01 | A: 39 op., review 0; B: 191 op., 20 partnerów, review 0 |
| 169 | CPV | Cabo Verde |  | [x] 2026-10-14 13:00 | [x] 2026-10-14 13:00 | A: 31 op., review 0; B: 138 op., 19 partnerów, review 0 |
| 170 | LCA | St. Lucia |  | [x] 2026-10-14 13:00 | [x] 2026-10-14 13:00 | B: 133 op., 19 partnerów, review 0; A: 31 op., review 0 |
| 171 | GMB | Gambia, The |  | [x] 2026-10-14 13:00 | [x] 2026-10-14 13:01 | A: 39 op., review 3 (1994, 2016, 2017 — uzasadnione); B: 211 op., 22 partnerów, review 5 (CHN/TWN 1995 i 2016, IRN 2010 — uzasadnione) |
| 172 | LSO | Lesotho |  | [x] 2026-10-14 13:01 | [x] 2026-10-14 13:01 | A: 35 op., review 3 (1994, 2014 — uzasadnione); B: 53 op., 7 partnerów, review 1 (CHN 1994 — uzasadnione) |
| 173 | GNB | Guinea-Bissau |  | [x] 2026-10-14 13:02 | [x] 2026-10-14 13:02 | B: 774 op., 18 partnerów, review 1 (PRT 2025 75→−40 — do przejrzenia); A: 70 op., review 1 (war exhaustion 1999 — uzasadnione) |
| 174 | SYC | Seychelles |  | [x] 2026-10-14 13:01 | [x] 2026-10-14 13:03 | A: 39 op., review 0; B: 152 op., 18 partnerów, review 0 |
| 175 | ATG | Antigua and Barbuda |  | [x] 2026-10-14 13:02 | [x] 2026-10-14 13:02 | A: 40 op., review 0; B: 180 op., 23 partnerów, review 0 |
| 176 | ERI | Eritrea |  | [x] 2026-10-14 13:02 | [x] 2026-10-14 13:04 | A: 42 op., review 0; B: 195 op., 20 partnerów, review 18 (ETH 1998/2018/2022, SOM 2007/2018, DJI 2008/2018, YEM 1999 — uzasadnione) |
| 177 | SMR | San Marino |  | [x] 2026-10-14 13:03 | [x] 2026-10-14 13:02 | B: 91 op., 11 partnerów, review 0; A: 38 op., review 0 |
| 178 | TLS | Timor-Leste |  | [x] 2026-10-14 13:03 | [x] 2026-10-14 13:03 | B: 141 op., 19 partnerów, review 0; A: 35 op., review 0; corruption/violence risk/happiness w całości szacunek (brak WGI/WHR) |
| 179 | COM | Comoros |  | [x] 2026-10-14 13:04 | [x] 2026-10-14 13:04 | A: 35 op., review 0; B: 560 op., 16 partnerów, review 0 |
| 180 | SLB | Solomon Islands |  | [x] 2026-10-14 13:04 | [x] 2026-10-14 13:04 | A: 60 op., review 0; B: 125 op., 13 partnerów, review 2 (AUS 2003 RAMSI — uzasadnione) |
| 181 | GRD | Grenada |  | [x] 2026-10-14 13:04 | [x] 2026-10-14 13:03 | B: 161 op., 26 partnerów, review 0; A: 33 op., review 0 |
| 182 | VUT | Vanuatu |  | [x] 2026-10-14 13:04 | [x] 2026-10-14 13:04 | A: 32 op., review 0; B: 83 op., 14 partnerów, review 0 |
| 183 | WSM | Samoa |  | [x] 2026-10-14 13:05 | [x] 2026-10-14 13:05 | B: 176 op., 21 partnerów, review 0 (wartości głównie stałe); A: 29 op., review 0 |
| 184 | VCT | St. Vincent and the Grenadines |  | [x] 2026-10-14 13:05 | [x] 2026-10-14 13:06 | A: 32 op., review 0; B: 209 op., 23 partnerów, review 0 |
| 185 | KNA | St. Kitts and Nevis |  | [x] 2026-10-14 13:06 | [x] 2026-10-14 13:06 | B: 160 op., 22 partnerów, review 0; A: 30 op., review 0 |
| 186 | STP | Sao Tome and Principe |  | [x] 2026-10-14 13:05 | [x] 2026-10-14 13:06 | A: 37 op., review 0; B: 161 op., 19 partnerów, review 8 (CHN/TWN 1997 i 2016 — uzasadnione) |
| 187 | DMA | Dominica |  | [x] 2026-10-14 13:06 | [x] 2026-10-14 13:06 | A: 36 op., review 0; B: 182 op., 22 partnerów, review 1 (TWN 2004 — uzasadnione) |
| 188 | TON | Tonga |  | [x] 2026-10-14 13:06 | [x] 2026-10-14 13:08 | A: 30 op., review 1 (corruption 2005 — seed WGI); B: 55 op., 19 partnerów, review 0 |
| 189 | FSM | Micronesia, Fed. Sts. |  | [x] 2026-10-14 13:06 | [x] 2026-10-14 13:07 | A: 20 op., review 0; B: 47 op., 19 partnerów, review 0 (wartości stałe) |
| 190 | KIR | Kiribati |  | [x] 2026-10-14 13:07 | [x] 2026-10-14 13:08 | A: 33 op., review 0; B: 76 op., 15 partnerów, review 4 (TWN/CHN 2003/2005/2019) |
| 191 | PLW | Palau |  | [x] 2026-10-14 13:07 | [x] 2026-10-14 13:09 | A: 29 op., review 0; B: 91 op., 12 partnerów, review 1 (TWN 1999 — uzasadnione) |
| 192 | MHL | Marshall Islands |  | [x] 2026-10-14 13:08 | [x] 2026-10-14 13:07 | B: 98 op., 14 partnerów, review 0; A: 36 op., review 0 |
| 193 | NRU | Naoero |  | [x] 2026-10-14 13:08 | [x] 2026-10-14 13:08 | B: 67 op., 16 partnerów, review 14 (TWN/CHN 2002/2005/2024 — uzasadnione); A: 39 op., review 0 |
| 194 | TUV | Tuvalu |  | [x] 2026-10-14 13:08 | [x] 2026-10-14 13:08 | A: 21 op., review 0; B: 37 op., 17 partnerów, review 0 |
| 195 | PRK | Korea, Dem. People's Rep. |  | [x] 2026-10-14 13:08 | [x] 2026-10-14 13:12 | A: 39 op., review 0; happiness/civilization w całości szacunek; B: 275 op., 22 partnerów, review 2 (KOR 2020, UKR 2022 — uzasadnione) |
| 196 | TWN | Taiwan |  | [x] 2026-10-14 13:09 | [x] 2026-10-14 13:11 | A: 41 op., review 2 (2008, 2016 zmiana rządu — uzasadnione); B: 196 op., 40 partnerów, review 20 (zmiany uznania ROC/ChRL — uzasadnione) |
