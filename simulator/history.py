"""Real statistics (history): `<scenario>/history/<name>.csv`, rows = dates, columns = tags.

Every imported file is reindexed to all scenario dates and tags; gaps stay NaN.
Units and sources live in `history/metadata.csv`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from simulator.io import SimulatorError, read_csv, slugify, write_csv
from simulator.scenario import Scenario

FORMATS = ("worldbank", "wide")
METADATA_COLUMNS = ["name", "unit", "source", "source_code", "downloaded", "description"]
INDEX_NAME = "date"


def _read_worldbank(path: Path) -> pd.DataFrame:
    """World Bank bulk CSV: one row per country, one column per year."""
    raw = read_csv(path, dtype={"Country Code": str})
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
) -> pd.DataFrame:
    """Import a statistic and return a per-tag completeness report."""
    slug = slugify(name)
    if not slug:
        raise SimulatorError(f"Invalid statistic name {name!r}")
    if fmt not in FORMATS:
        raise SimulatorError(f"Unknown format {fmt!r}; use one of {FORMATS}")
    df = _read_worldbank(source_path) if fmt == "worldbank" else _read_wide(source_path)
    df = df.apply(pd.to_numeric, errors="coerce") * scale

    dropped = sorted(set(df.columns) - set(scenario.tags))
    df = df.reindex(index=scenario.dates, columns=scenario.tags).astype(float)
    df.index.name = INDEX_NAME

    with scenario.lock():
        write_csv(df, scenario.history_dir / f"{slug}.csv")
        meta = load_metadata(scenario)
        meta = meta[meta["name"] != slug]
        row = {"name": slug, "unit": unit, "source": source, "source_code": source_code,
               "downloaded": downloaded, "description": description}
        meta = pd.concat([meta, pd.DataFrame([row])], ignore_index=True).sort_values("name")
        write_csv(meta, scenario.history_dir / "metadata.csv", index=False)

    report = completeness(df)
    report.attrs["ignored_columns"] = len(dropped)
    return report


def load_metadata(scenario: Scenario) -> pd.DataFrame:
    path = scenario.history_dir / "metadata.csv"
    if not path.exists():
        return pd.DataFrame(columns=METADATA_COLUMNS, dtype=str)
    return read_csv(path, dtype=str, keep_default_na=False)


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
