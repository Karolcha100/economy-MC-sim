"""Real statistics (history): `<scenario>/history/<name>.csv`, rows = dates, columns = tags.

Every imported file is reindexed to all scenario dates and tags; gaps stay NaN.
Units and sources live in `history/metadata.csv`. Gaps (missing values in years a country
exists) can be filled from another source, by interpolation or by extrapolation; every
filled value is logged in `history/fill-log.csv` so real and estimated values stay distinguishable.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from simulator import sources
from simulator.io import ENCODING, SimulatorError, read_csv, slugify, write_csv
from simulator.scenario import Scenario

FORMATS = ("worldbank", "wide", "imf-datamapper", "owid", "wgi-xlsx")
DYADIC_FORMATS = ("geonames-neighbours", "ucdp-dyadic", "pair-ranges")
METADATA_COLUMNS = ["name", "unit", "source", "source_code", "downloaded", "description", "shape"]
SHAPES = ("country", "dyad-symmetric")  # country-year table / pairs of countries (history/dyadic/)
FILL_LOG_COLUMNS = ["timestamp", "author", "name", "tag", "year", "value", "method", "source"]
FILL_METHODS = ("source", "interpolate", "extrapolate")
INDEX_NAME = "date"
RESERVED_FILES = ("metadata.csv", "fill-log.csv")  # history/ files that are not statistics
# IMF country codes that differ from the World Bank / scenario tags.
IMF_TO_TAG = {"UVK": "XKX", "WBG": "PSE"}


def _read_worldbank(path: Path) -> pd.DataFrame:
    """World Bank bulk CSV: one row per country, one column per year."""
    try:
        raw = read_csv(path, dtype={"Country Code": str})
    except pd.errors.ParserError:  # preamble lines have fewer fields than the table
        raw = pd.DataFrame()
    if "Country Code" not in raw.columns:
        # Original downloads start with 4 lines of preamble.
        raw = read_csv(path, skiprows=4, dtype={"Country Code": str})
    if "Country Code" not in raw.columns:
        raise SimulatorError(f"{path}: no 'Country Code' column; is this a World Bank CSV?")
    year_cols = [c for c in raw.columns if str(c).strip().isdigit()]
    df = raw.set_index("Country Code")[year_cols].T
    df.index = df.index.astype(int)
    return df


def _read_wide(path: Path) -> pd.DataFrame:
    """Already in target shape: first column = date, other columns = tags."""
    df = read_csv(path, index_col=0)
    df.index = df.index.astype(int)
    return df


def _read_imf_datamapper(path: Path) -> pd.DataFrame:
    """JSON from https://www.imf.org/external/datamapper/api/v1/<INDICATOR> (one indicator)."""
    try:
        values = json.loads(path.read_text(encoding=ENCODING))["values"]
    except (OSError, ValueError, KeyError) as e:
        raise SimulatorError(f"{path}: not an IMF DataMapper JSON ({e})") from None
    values = {k: v for k, v in values.items() if k and v}  # the API adds an empty "" entry
    if len(values) != 1:
        raise SimulatorError(f"{path}: expected one indicator, got {sorted(values)}")
    df = pd.DataFrame(next(iter(values.values())))
    df.index = df.index.astype(int)
    return df.rename(columns=IMF_TO_TAG).sort_index()


def read_source(path: Path, fmt: str, column: str | None = None, sheet: str | None = None) -> pd.DataFrame:
    """Read a source file into a dates x country-codes frame.

    `column`: value column of an OWID file (needed when it has several); `sheet`: WGI sheet (pv, cc, ...).
    """
    path = Path(path)
    if fmt == "owid":
        df = sources.read_owid(path, column)
    elif fmt == "wgi-xlsx":
        if not sheet:
            raise SimulatorError(f"format wgi-xlsx needs a sheet: one of {sorted(sources.WGI_SHEETS)}")
        df = sources.read_wgi_xlsx(path, sheet)
    else:
        readers = {"worldbank": _read_worldbank, "wide": _read_wide, "imf-datamapper": _read_imf_datamapper}
        if fmt not in readers:
            raise SimulatorError(f"Unknown format {fmt!r}; use one of {FORMATS}")
        df = readers[fmt](path)
    return df.apply(pd.to_numeric, errors="coerce")


def import_history(
    scenario: Scenario,
    name: str,
    source_path: Path,
    fmt: str = "worldbank",
    unit: str = "",
    source: str = "",
    source_code: str = "",
    downloaded: str = "",
    description: str = "",
    scale: float = 1.0,
    column: str | None = None,
    sheet: str | None = None,
) -> pd.DataFrame:
    """Import a statistic and return a per-tag completeness report."""
    slug = slugify(name)
    if not slug:
        raise SimulatorError(f"Invalid statistic name {name!r}")
    df = read_source(source_path, fmt, column, sheet) * scale

    dropped = sorted(set(df.columns) - set(scenario.tags))
    df = df.reindex(index=scenario.dates, columns=scenario.tags).astype(float)
    df.index.name = INDEX_NAME

    with scenario.lock():
        write_csv(df, scenario.history_dir / f"{slug}.csv")
        _save_metadata(scenario, {"name": slug, "unit": unit, "source": source, "source_code": source_code,
                                  "downloaded": downloaded, "description": description, "shape": "country"})
        # A fresh import replaces earlier gap fills of this statistic.
        log = load_fill_log(scenario)
        if (log["name"] == slug).any():
            write_csv(log[log["name"] != slug], scenario.history_dir / "fill-log.csv", index=False)

    report = completeness(df)
    report.attrs["ignored_columns"] = len(dropped)
    return report


def load_metadata(scenario: Scenario) -> pd.DataFrame:
    path = scenario.history_dir / "metadata.csv"
    if not path.exists():
        return pd.DataFrame(columns=METADATA_COLUMNS, dtype=str)
    meta = read_csv(path, dtype=str, keep_default_na=False)
    if "shape" not in meta.columns:  # files written before dyadic data existed
        meta["shape"] = "country"
    return meta[METADATA_COLUMNS]


def _save_metadata(scenario: Scenario, row: dict) -> None:
    meta = load_metadata(scenario)
    meta = meta[meta["name"] != row["name"]]
    meta = pd.concat([meta, pd.DataFrame([row])], ignore_index=True).sort_values("name")
    write_csv(meta[METADATA_COLUMNS], scenario.history_dir / "metadata.csv", index=False)


def import_dyadic(
    scenario: Scenario,
    name: str,
    source_path: Path,
    fmt: str,
    unit: str = "",
    source: str = "",
    source_code: str = "",
    downloaded: str = "",
    description: str = "",
) -> pd.DataFrame:
    """Import pair data into `history/dyadic/<name>.csv` (date, side_a, side_b, value; side_a < side_b).

    Only scenario dates, known tags and years in which both countries exist are kept.
    Returns the kept rows.
    """
    slug = slugify(name)
    if fmt == "geonames-neighbours":
        df = sources.read_geonames_neighbours(Path(source_path), scenario.dates)
    elif fmt == "ucdp-dyadic":
        df = sources.read_ucdp_dyadic(Path(source_path), min_year=scenario.dates[0])
    elif fmt == "pair-ranges":
        df = sources.read_pair_ranges(Path(source_path))
    else:
        raise SimulatorError(f"Unknown dyadic format {fmt!r}; use one of {DYADIC_FORMATS}")
    df = df[df["date"].isin(scenario.dates) & df["side_a"].isin(scenario.tags) & df["side_b"].isin(scenario.tags)]
    alive = scenario.existence()
    both = [bool(alive.at[d, a] and alive.at[d, b]) for d, a, b in zip(df["date"], df["side_a"], df["side_b"])]
    df = df[both].sort_values(["date", "side_a", "side_b"]).reset_index(drop=True)
    with scenario.lock():
        write_csv(df, scenario.history_dir / "dyadic" / f"{slug}.csv", index=False)
        _save_metadata(scenario, {"name": slug, "unit": unit, "source": source, "source_code": source_code,
                                  "downloaded": downloaded, "description": description, "shape": "dyad-symmetric"})
    return df


def load_dyadic(scenario: Scenario, name: str) -> pd.DataFrame:
    path = scenario.history_dir / "dyadic" / f"{slugify(name)}.csv"
    if not path.exists():
        raise SimulatorError(f"No dyadic history {name!r} ({path})")
    return read_csv(path, dtype={"side_a": str, "side_b": str})


def load_history(scenario: Scenario, name: str) -> pd.DataFrame:
    path = scenario.history_dir / f"{slugify(name)}.csv"
    if not path.exists():
        raise SimulatorError(f"No history statistic {name!r} ({path})")
    return read_csv(path, index_col=INDEX_NAME, dtype={INDEX_NAME: int})


def completeness(df: pd.DataFrame) -> pd.DataFrame:
    """Per tag: number of filled dates, first and last filled date."""
    filled = df.notna()
    return pd.DataFrame({
        "filled": filled.sum(),
        "total": len(df),
        "first": filled.idxmax().where(filled.any()),
        "last": filled[::-1].idxmax().where(filled.any()),
    })


# --- gaps ----------------------------------------------------------------------------

def gaps_mask(scenario: Scenario, df: pd.DataFrame) -> pd.DataFrame:
    """True where a value is missing in a year the country exists."""
    return df.isna() & scenario.existence(list(df.index)).reindex(columns=df.columns, fill_value=False)


def find_gaps(scenario: Scenario, name: str) -> pd.DataFrame:
    """Per tag with gaps: number of missing years and their list."""
    mask = gaps_mask(scenario, load_history(scenario, name))
    rows = [
        {"tag": tag, "missing": int(mask[tag].sum()), "years": compress_years(mask.index[mask[tag]].tolist())}
        for tag in mask.columns if mask[tag].any()
    ]
    return pd.DataFrame(rows, columns=["tag", "missing", "years"]).sort_values("missing", ascending=False)


def compress_years(years: list[int]) -> str:
    """[1990, 1991, 1992, 1995] -> '1990-1992,1995'."""
    parts, start = [], None
    for i, y in enumerate(years):
        if start is None:
            start = y
        if i + 1 == len(years) or years[i + 1] != y + 1:
            parts.append(str(start) if start == y else f"{start}-{y}")
            start = None
    return ",".join(parts)


def load_fill_log(scenario: Scenario) -> pd.DataFrame:
    path = scenario.history_dir / "fill-log.csv"
    if not path.exists():
        return pd.DataFrame(columns=FILL_LOG_COLUMNS)
    return read_csv(path, dtype={"tag": str, "name": str})


def _interpolate(series: pd.Series, alive: pd.Series) -> pd.Series:
    """Fill inner gaps; log-linear when the series is positive (growth-like data)."""
    s = series[alive]
    positive = bool((s.dropna() > 0).all())
    work = np.log(s) if positive else s
    filled = work.interpolate(method="index", limit_area="inside")
    return (np.exp(filled) if positive else filled).reindex(series.index)


def _extrapolate(series: pd.Series, alive: pd.Series, window: int) -> pd.Series:
    """Fill leading/trailing gaps with the average growth of the `window` nearest observed years.

    Positive series grow geometrically, others linearly; with a single observation it is held flat.
    """
    s = series[alive].copy()
    obs = s.dropna()
    if obs.empty:
        return series
    positive = bool((obs > 0).all())
    work = np.log(s) if positive else s.copy()
    known = work.dropna()
    head, tail = known.iloc[: window + 1], known.iloc[-(window + 1):]
    slope_head = (head.iloc[-1] - head.iloc[0]) / (head.index[-1] - head.index[0]) if len(head) > 1 else 0.0
    slope_tail = (tail.iloc[-1] - tail.iloc[0]) / (tail.index[-1] - tail.index[0]) if len(tail) > 1 else 0.0
    first, last = known.index[0], known.index[-1]
    for year in work.index[work.isna()]:
        if year < first:
            work[year] = known.iloc[0] - slope_head * (first - year)
        elif year > last:
            work[year] = known.iloc[-1] + slope_tail * (year - last)
    return (np.exp(work) if positive else work).reindex(series.index)


def fill_gaps(
    scenario: Scenario,
    name: str,
    method: str,
    source_path: Path | None = None,
    source_format: str = "wide",
    source_scale: float = 1.0,
    source_label: str = "",
    window: int = 3,
    author: str = "",
    tags: list[str] | None = None,
    dry_run: bool = False,
) -> pd.DataFrame:
    """Fill gaps of a history statistic. Existing values are never changed.

    method: 'source' (values from another file for the same years), 'interpolate'
    (inner gaps) or 'extrapolate' (leading/trailing gaps). Returns the log rows written.
    """
    if method not in FILL_METHODS:
        raise SimulatorError(f"Unknown method {method!r}; use one of {FILL_METHODS}")
    if not author:
        raise SimulatorError("author is required")
    df = load_history(scenario, name)
    mask = gaps_mask(scenario, df)
    if tags is not None:
        scenario.check_tags(tags)
        mask.loc[:, ~mask.columns.isin(tags)] = False
    alive = scenario.existence(list(df.index))

    if method == "source":
        if source_path is None:
            raise SimulatorError("method 'source' needs a source file")
        src = (read_source(source_path, source_format) * source_scale).reindex(index=df.index, columns=df.columns)
        candidate = src
        label = source_label or f"{Path(source_path).name} ({source_format})"
    else:
        candidate = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)
        for tag in df.columns[mask.any()]:
            if method == "interpolate":
                candidate[tag] = _interpolate(df[tag], alive[tag])
            else:
                candidate[tag] = _extrapolate(df[tag], alive[tag], window)
        label = f"{method} (log-linear for positive series)" + (f", window={window}" if method == "extrapolate" else "")

    take = mask & candidate.notna()
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = [
        {"timestamp": stamp, "author": author, "name": slugify(name), "tag": tag, "year": int(year),
         "value": float(candidate.at[year, tag]), "method": method, "source": label}
        for tag in take.columns[take.any()] for year in take.index[take[tag]]
    ]
    log_rows = pd.DataFrame(rows, columns=FILL_LOG_COLUMNS)
    if dry_run or log_rows.empty:
        return log_rows
    with scenario.lock():
        df = df.mask(take, candidate)
        df.index.name = INDEX_NAME
        write_csv(df, scenario.history_dir / f"{slugify(name)}.csv")
        log = pd.concat([load_fill_log(scenario), log_rows], ignore_index=True)
        write_csv(log, scenario.history_dir / "fill-log.csv", index=False)
    return log_rows
