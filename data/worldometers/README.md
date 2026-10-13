# worldometers

`prk-gdp-current-usd.csv` — GDP of North Korea (PRK), current USD, 1970-2023.

- Scraped 2026-10-14 from https://www.worldometers.info/gdp/north-korea-gdp/ (table "GDP Nominal (Current USD)").
- Worldometers cites: United Nations Statistics Division, National Accounts (the UN source itself could not be
  downloaded — unstats.un.org truncated the file). Secondary source: prefer the UN file if it becomes available.
- Used to fill the PRK gap in `simulator/scenarios/world-1990-2025/history/gdp-current-usd.csv`
  (see `history/fill-log.csv`).
