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
- The diagonal of relation matrices (a country towards itself) is always empty.
- A country can only get values in years it exists (`exists_from`/`exists_to` in `tags.csv`, empty = always).
- Values must fit the formula: `float`/`int` within `[valmin, valmax]`. `int` values are rounded.
- Slug = lowercase name with spaces replaced by `-` (`war exhaustion` → `war-exhaustion`); names and slugs are both accepted.
- Every write is logged to `narrated/changelog.csv` (author, targets, years, curve, rationale).

## Filling narrated data (for LLM agents)

Set the scenario once: `export SIMULATOR_SCENARIO=world-1990-2025` (or pass `--scenario`).

```bash
# What is there to fill?
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

# Year-by-year values
python -m simulator set --kind grade --name "war exhaustion" --targets UKR --years 2022-2025 \
    --curve manual --values 20,45,60,70 --author claude-opus-5-5

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

Operation keys: `kind, name, targets, years, curve, start, end, values, params, only_empty, clip, rationale`.
If any operation fails, nothing is written. Later operations see values set by earlier ones.

Errors are printed as `error: ...` with exit code 1; fix the input and retry.
`--clip` clips out-of-range values instead of failing — use it only on purpose.

## Editing formulas (user)

```bash
python -m simulator formulas template --kind directed          # which fields exist
python -m simulator formulas add --kind grade --name "inflation pressure" --type float --valmin 0 --valmax 100
python -m simulator formulas edit --kind grade --name stability --rename "political stability"
python -m simulator formulas edit --kind grade --name stability --valmax 50 --clip
python -m simulator formulas remove --kind grade --name riots --purge
```

`edit` migrates existing data (renames columns/files; range/type changes fail on conflicting
values unless `--clip`). `remove` refuses to delete existing data without `--purge`.

## History (real statistics)

```bash
python -m simulator history import --name gdp-current-usd \
    --source-file data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv \
    --format worldbank --unit USD --source "World Bank WDI" --source-code NY.GDP.MKTP.CD
python -m simulator history list
```

`--format wide` takes a CSV already shaped `date,<TAG>,<TAG>,...`. The output always has every
scenario tag and date (gaps = empty); a completeness report is printed.

## Validation

```bash
python -m simulator validate
```

Checks tags, dates, formulas against templates, history shape, and narrated data
(ranges, types, diagonal, symmetry, non-existing countries, unknown files/columns).

## Concurrency

Writes take a lock file `scenarios/<scenario>/.lock` and replace files atomically. If a process
crashed while holding the lock, delete that file.
