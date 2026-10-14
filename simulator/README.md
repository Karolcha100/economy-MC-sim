# simulator — scenario data tools

Tools for the data the Monte-Carlo simulator is built on:

- **history**: real statistics (e.g. World Bank GDP), `rows = dates, columns = country tags`;
- **narrated**: descriptive statistics filled in by LLMs or the user (internal grades and relations).

Everything runs through one CLI (`python -m simulator`) or the same functions from Python.

## Setup

```bash
python3 -m venv venv
venv/bin/pip install -e ".[dev]"      # pandas, numpy, pytest
venv/bin/python -m pytest             # tests
```

## Concepts

| Term | Where | Who edits |
|---|---|---|
| Template | `simulator/common/templates/<kind>.csv` — one row per field | developers only |
| Formula | `scenarios/<scenario>/formulas/<kind>.csv` — one row per statistic, columns = template fields | user (via `formulas` commands) |
| Narrated data | `scenarios/<scenario>/narrated/<year>/...` | LLMs / user (via `set` / `batch`) |
| History | `scenarios/<scenario>/history/<stat>.csv` + `metadata.csv` | `history import` |
| Tags | `scenarios/<scenario>/tags.csv` — `tag,name,exists_from,exists_to` | user |
| Dates | `scenarios/<scenario>/dates.csv` — `date` (years) | user |
| Groups | `scenarios/<scenario>/groups.csv` — `group,tag,from,to,note` (membership years) | user |
| Reference countries | `scenarios/<scenario>/reference-countries.csv` — `tag,reason` (calibration anchors) | user |

Kinds (`--kind`, short aliases in brackets):

- `internal-grades` (`grade`) — a value per country and year, e.g. `stability`.
  Stored in `narrated/<year>/internal-grades.csv`: rows = tags, columns = grade slugs.
- `relations-directed` (`directed`) — a value from one country towards another, e.g.
  `diplomatic relation towards`. Stored in `narrated/<year>/relations-directed/<slug>.csv`:
  row = **from**, column = **to**.
- `relations-doublesided` (`doublesided`) — a symmetric relation, e.g. `in war`.
  Stored in `narrated/<year>/relations-doublesided/<slug>.csv`; both cells are always written.

Rules:

- Empty cell = **not filled yet** (never 0). Missing files read as empty.
- Every formula has a `description` (meaning and scale — **read it before filling**) and an optional
  `default`: the value the simulator assumes for an unfilled cell (e.g. `in war` = 0). Formulas without
  a default (e.g. `stability`) have to be filled for every existing country.
- 0/1 flags (`riots`, `epidemic`, `mobilized`, `in war`, …) mean "happened **at any time during the year**".
  Only serious, nationally significant events count (e.g. `riots` = large-scale violent unrest, not protests).
- The diagonal of relation matrices (a country towards itself) is always empty.
- A country can only get values in years it exists (`exists_from`/`exists_to` in `tags.csv`, empty = always).
- Values must fit the formula: `float`/`int` within `[valmin, valmax]`. `int` values are rounded.
- Slug = lowercase name with spaces replaced by `-` (`war exhaustion` → `war-exhaustion`); names and slugs are both accepted.
- Every write is logged to `narrated/changelog.csv` (author, targets, years, curve, rationale).

## Scenario `world-1990-2025` — conventions every agent must know

- **196 countries**: all sovereign World Bank economies (22 dependent territories such as Hong Kong,
  Puerto Rico, Macao, Greenland are **not** in the scenario) plus **Taiwan (`TWN`)**. Kosovo (`XKX`,
  from 2008) and Palestine (`PSE`, from 1994) are included.
- **Continuity**: Russia (`RUS`) continues the USSR, Serbia (`SRB`) continues Yugoslavia and Czechia (`CZE`)
  continues Czechoslovakia — all exist from 1990 (Slovakia from 1993). Germany (`DEU`) exists from 1990 (the GDR is not modelled); Yemen from 1990.
- **Existence** (`exists_from`) = year of independence, any time during that year
  (former USSR republics 1991, CZE/SVK 1993, BIH 1992, MNE 2006, ...). No values before that year.
- **GDP gaps** were filled (IMF, then interpolation/extrapolation); every estimated value is listed in
  `history/fill-log.csv` and marked `*` by `context`. North Korea (`PRK`) has no GDP at all.

## Seed values (first version of narrated data from real indicators)

Rules: `scenarios/<scenario>/seeds.csv` (`kind,name,source,transform,a,b,note`), editable without code.

| transform | value |
|---|---|
| `linear` | `a + b * x` (x = history statistic) |
| `per-1000-linear` | `a + b * (x / population * 1000)` |
| `pairs-at-least` | pair value 1 where the dyadic history value >= `a` |

Values are clipped to the formula range; gaps inside an indicator's range are interpolated linearly;
years before its first / after its last value stay empty (for LLMs). Seeds are written with author
`seed:<source>` and **never overwrite filled cells**, so re-running keeps LLM corrections.

```bash
python -m simulator seed --dry-run          # what would be written
python -m simulator seed                    # all rules (or --name stability)
python -m simulator review                  # also warns when a value is > 15 points from its seed
```

Current rules in `world-1990-2025`: `stability` (WGI PV), `corruption` (WGI CC), `civilization level`
(100 x HDI), `net migration` (5 x per 1000), `in war` (UCDP levels 1-2), `neighbours` (GeoNames +
`data/manual/historical-land-borders.csv`).

## Filling narrated data (for LLM agents)

Workflow: `context` (read) → `set`/`batch` with `--dry-run` → write → `validate` → `review`.

Set the scenario once: `export SIMULATOR_SCENARIO=world-1990-2025` (or pass `--scenario`).

```bash
# What is there to fill, and what does each statistic mean?
python -m simulator formulas list
python -m simulator missing --kind grade

# Stability of Poland rising from 40 to 70 between 1990 and 2000 (S-curve)
python -m simulator set --kind grade --name stability --targets POL --years 1990-2000 \
    --curve logistic --start 40 --end 70 \
    --author claude-opus-5-5 --rationale "post-1989 transition, EU accession talks"

# Directed relation: POL towards RUS and UKR towards RUS, worsening exponentially
python -m simulator set --kind directed --name "diplomatic relation towards" \
    --targets POL:RUS,UKR:RUS --years 2014-2022 --curve exponential --start -20 --end -90 \
    --param k=2 --author claude-opus-5-5 --rationale "Crimea 2014, invasion 2022"

# Double-sided 0/1 flag: only constant, step or manual curves are allowed
python -m simulator set --kind doublesided --name "in war" --targets RUS:UKR \
    --years 2014-2025 --curve constant --start 1 --author claude-opus-5-5

# Continue from the value already stored in the first year, fill only empty cells
python -m simulator set --kind grade --name stability --targets POL --years 2000-2010 \
    --start current --end 75 --only-empty --author claude-opus-5-5

# Sources the values are based on (repeatable; stored in narrated/changelog.csv)
python -m simulator set ... --sources "https://example.org/article" --sources "Title, Outlet, 2014-03-18"

# Year-by-year values
python -m simulator set --kind grade --name "war exhaustion" --targets UKR --years 2022-2025 \
    --curve manual --values 20,45,60,70 --author claude-opus-5-5

# Groups and wildcards: every NATO member towards RUS (only in years of membership and existence)
python -m simulator set --kind directed --name "diplomatic relation towards" --targets @NATO:RUS \
    --years 2014-2025 --curve constant --start -60 --author claude-opus-5-5 --rationale "..."
python -m simulator set --kind directed --name "social view towards" --targets POL:* ...   # POL towards everyone
python -m simulator groups                                    # NATO, EU, CIS, CSTO, EAEU, V4

# Everything an agent needs about a country or a pair, in one compact text
python -m simulator context POL
python -m simulator context POL:RUS

# Check before writing, then read back
python -m simulator set ... --dry-run
python -m simulator --json show --kind grade --name stability --targets POL,UKR --years 1990-2000
```

### Curves

`value = start + (end - start) * f(t)`, `t` goes from 0 (first year) to 1 (last year), so every curve
works with 0 and with sign changes.

| Curve | Shape | Params (default) |
|---|---|---|
| `linear` | straight line | — |
| `exponential` | slow start, fast end (`k<0`: fast start, slow end) | `k=3` |
| `logistic` | S-curve | `steepness=10`, `midpoint=0.5` |
| `step` | `start` before `midpoint`, `end` from it on | `midpoint=0.5` |
| `constant` | `start` in every year (`--end` not needed) | — |
| `manual` | `--values`, exactly one per year | — |

A single year (`--years 1995`) gets the end value; prefer `constant` for it.

### Batches (all-or-nothing)

```bash
python -m simulator batch ops.json --author claude-opus-5-5
```

```json
{
  "rationale": "Visegrad states 1993-2004",
  "operations": [
    {"kind": "grade", "name": "stability", "targets": ["CZE", "SVK", "HUN"],
     "years": "1993-2004", "curve": "logistic", "start": 30, "end": 75},
    {"kind": "directed", "name": "social view towards", "targets": "CZE:RUS,HUN:RUS",
     "years": [1993, 2004], "curve": "linear", "start": -30, "end": -50,
     "rationale": "per-operation rationale overrides the batch one"}
  ]
}
```

Operation keys: `kind, name, targets, years, curve, start, end, values, params, only_empty, clip, rationale, sources`.
Group/wildcard targets (`@NATO`, `*`) cannot use `start: "current"`.
If any operation fails, nothing is written. Later operations see values set by earlier ones.

Errors are printed as `error: ...` with exit code 1; fix the input and retry.
`--clip` clips out-of-range values instead of failing — use it only on purpose.

## Editing formulas (user)

```bash
python -m simulator formulas template --kind directed          # which fields exist
python -m simulator formulas add --kind grade --name "inflation pressure" --type float --valmin 0 --valmax 100 \
    --description "Pressure of inflation on households: 0 = none, 100 = hyperinflation" --default 0
python -m simulator formulas edit --kind grade --name stability --default ""     # remove the default
python -m simulator formulas edit --kind grade --name stability --rename "political stability"
python -m simulator formulas edit --kind grade --name stability --valmax 50 --clip
python -m simulator formulas remove --kind grade --name riots --purge
```

`edit` also changes `--default` and `--description`. It migrates existing data (renames columns/files; range/type changes fail on conflicting
values unless `--clip`). `remove` refuses to delete existing data without `--purge`.

## History (real statistics)

```bash
python -m simulator history import --name gdp-current-usd \
    --source-file data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv \
    --format worldbank --unit USD --source "World Bank WDI" --source-code NY.GDP.MKTP.CD
python -m simulator history list
```

Formats: `worldbank` (WDI bulk CSV), `wide` (`date,<TAG>,<TAG>,...`), `imf-datamapper` (IMF API JSON),
`owid` (Our World in Data grapher CSV; `--column` if it has several value columns), `wgi-xlsx`
(official WGI workbook; `--sheet pv|cc|va|ge|rq|rl`). Raw files and their origin: `data/README.md`.

Statistics currently imported into `world-1990-2025` (see `history list`): GDP, WGI political stability and
control of corruption, HDI, TI CPI, happiness (Cantril ladder), net migration, migrant stock share.

Pair data (`history/dyadic/<name>.csv`: `date,side_a,side_b,value`, symmetric, `side_a < side_b`):

```bash
python -m simulator history import-dyadic --name land-borders --format geonames-neighbours \
    --source-file data/geonames/countryInfo.txt
python -m simulator history import-dyadic --name ucdp-armed-conflict --format ucdp-dyadic \
    --source-file data/ucdp/Dyadic_v25_1.csv     # 2 = interstate war, 1 = opposite sides incl. secondary party
```

`--format pair-ranges` reads hand-made pairs valid for year ranges (`side_a,side_b,from,to,note`), e.g.
`data/manual/historical-land-borders.csv`. `context POL:RUS` shows the pair data. `wgi-xlsx` and `ucdp-dyadic` need `pip install -e ".[sources]"`.

The `wide` format takes a CSV already shaped `date,<TAG>,<TAG>,...`. The output always has every
scenario tag and date (gaps = empty); a completeness report is printed.

Gaps (missing values in years a country exists) and filling them — existing values are never changed,
every filled value is logged in `history/fill-log.csv`:

```bash
python -m simulator history gaps --name gdp-current-usd
curl -o data/imf/NGDPD.json https://www.imf.org/external/datamapper/api/v1/NGDPD      # IMF, billions USD
python -m simulator history fill --name gdp-current-usd --method source --source-file data/imf/NGDPD.json \
    --source-format imf-datamapper --source-scale 1e9 --source-label "IMF WEO NGDPD" --author user
python -m simulator history fill --name gdp-current-usd --method interpolate --author user   # inner gaps
python -m simulator history fill --name gdp-current-usd --method extrapolate --author user   # edge gaps
```

Interpolation/extrapolation is log-linear for positive series (growth), linear otherwise. A new
`history import` of a statistic replaces the file and drops its fill-log entries — re-run the fills.

## Review and reference map

```bash
python -m simulator review                    # warnings: jumps > 25% of the range in one year, no rationale
python -m simulator reference-map --kind grade --name stability             # opens an HTML world map
python -m simulator reference-map --kind directed --name "social view towards" --focus POL
```

`audit` compares **all countries** with real indicators (read-only; rules in `scenarios/<scenario>/audit.csv`):
rank agreement per statistic, outlier countries, flat lines (same value every year) and crowding (one value
for most countries in a year). The report goes to `--out DIR` (default `scenarios/<scenario>/views/`).

```bash
python -m simulator audit --out AGENTS/phases/phase-1.2b/audit
```

The map shows the reference countries (`reference-countries.csv`) with a year slider and works
offline. Needs `pip install -e ".[viz]"` (plotly). Files go to `scenarios/<scenario>/views/` (not in git).

## Validation

```bash
python -m simulator validate
```

Checks tags, dates, formulas against templates, history shape, and narrated data
(ranges, types, diagonal, symmetry, non-existing countries, unknown files/columns).

## Concurrency

Writes take a lock file `scenarios/<scenario>/.lock` and replace files atomically. If a process
crashed while holding the lock, delete that file.

## Values for the simulator

`simulator.narrated.effective_values(scenario, kind, name, year)` returns the values later phases
should use: unfilled cells get the formula `default`; non-existing countries, the relation diagonal
and unfilled cells of formulas without a default stay empty.
