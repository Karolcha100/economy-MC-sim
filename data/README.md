# Raw data sources

Raw downloads, kept unchanged. Imported into scenarios with `python -m simulator history import / import-dyadic`
(the exact commands are in `simulator/README.md`). Check the licence before redistributing.

| Directory / file | What | Source URL | Downloaded | Licence |
|---|---|---|---|---|
| `API_NY.GDP.MKTP.CD_*` | GDP, current USD | World Bank WDI bulk CSV | 2026-10-08 | CC BY 4.0 |
| `imf/NGDPD.json` | GDP, current USD (billions), incl. Taiwan | https://www.imf.org/external/datamapper/api/v1/NGDPD | 2026-10-13 | IMF terms (free reuse with attribution) |
| `imf/LP.json` | Population (millions), used for Taiwan | https://www.imf.org/external/datamapper/api/v1/LP | 2026-10-14 | IMF terms (free reuse with attribution) |
| `worldometers/prk-gdp-current-usd.csv` | GDP of North Korea (UN National Accounts, second hand) | https://www.worldometers.info/gdp/north-korea-gdp/ | 2026-10-14 | see `worldometers/README.md` |
| `wgi/wgidataset.xlsx` | Worldwide Governance Indicators, 2023 update (1996-2022) | https://www.worldbank.org/content/dam/sites/govindicators/doc/wgidataset.xlsx | 2026-10-14 | CC BY 4.0 |
| `owid/human-development-index.csv` | HDI (UNDP) | https://ourworldindata.org/grapher/human-development-index.csv | 2026-10-14 | CC BY 4.0 (OWID), UNDP CC BY 3.0 IGO |
| `owid/happiness-cantril-ladder.csv` | Life evaluation (World Happiness Report) | https://ourworldindata.org/grapher/happiness-cantril-ladder.csv | 2026-10-14 | CC BY 4.0 (OWID), WHR terms |
| `owid/ti-corruption-perception-index.csv` | Corruption Perceptions Index | https://ourworldindata.org/grapher/ti-corruption-perception-index.csv | 2026-10-14 | CC BY 4.0 (OWID), TI terms (non-commercial) |
| `worldbank/API_SM.POP.NETM_*` | Net migration | https://api.worldbank.org/v2/en/indicator/SM.POP.NETM?downloadformat=csv | 2026-10-14 | CC BY 4.0 |
| `worldbank/API_SP.POP.TOTL_*` | Population | https://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv | 2026-10-14 | CC BY 4.0 |
| `worldbank/API_SM.POP.TOTL.ZS_*` | International migrant stock, % of population | https://api.worldbank.org/v2/en/indicator/SM.POP.TOTL.ZS?downloadformat=csv | 2026-10-14 | CC BY 4.0 |
| `geonames/countryInfo.txt` | Countries and their land neighbours (today's borders) | https://download.geonames.org/export/dump/countryInfo.txt | 2026-10-14 | CC BY 4.0 |
| `ucdp/Dyadic_v25_1.csv` | UCDP Dyadic Dataset v25.1 (armed conflicts 1946-2024) | https://ucdp.uu.se/downloads/dyadic/ucdp-dyadic-251-csv.zip | 2026-10-14 | CC BY 4.0 |

Notes:
- The WGI series in the World Bank *WDI Database Archives* bulk download (`PV.EST`, source 3) is **not** on the
  documented -2.5..2.5 scale and is inconsistent over time; the official WGI workbook above is used instead.
- UN national accounts (unstats.un.org) could not be downloaded (the server truncates the file).
