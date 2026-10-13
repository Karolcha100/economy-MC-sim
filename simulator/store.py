"""Read/write access to narrated (descriptive, LLM-filled) data of a scenario.

Missing files mean "nothing filled yet": they read as all-NaN frames and are created on
first write. Frames are cached and written only on `flush()`, so a batch of operations
either reaches disk as a whole or not at all.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from simulator.io import ENCODING, read_csv, write_csv
from simulator.scenario import Scenario
from simulator.templates import INTERNAL_GRADES

INDEX_NAME = "tag"
CHANGELOG_COLUMNS = [
    "timestamp", "author", "operation", "kind", "name", "targets", "years", "params", "rationale", "sources",
]

Key = tuple[str, str | None, int]


class NarratedStore:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self._cache: dict[Key, pd.DataFrame] = {}
        self._dirty: set[Key] = set()

    # --- locations -------------------------------------------------------------
    def path(self, kind: str, slug: str | None, year: int):
        if kind == INTERNAL_GRADES:
            return self.scenario.year_dir(year) / f"{INTERNAL_GRADES}.csv"
        return self.scenario.year_dir(year) / kind / f"{slug}.csv"

    @staticmethod
    def _key(kind: str, slug: str | None, year: int) -> Key:
        # All internal grades of a year share one file, so they share one cache entry.
        return (kind, None if kind == INTERNAL_GRADES else slug, year)

    # --- reading ---------------------------------------------------------------
    def frame(self, kind: str, slug: str | None, year: int) -> pd.DataFrame:
        """Cached frame. Internal grades: tags x grade slugs. Relations: tags x tags."""
        key = self._key(kind, slug, year)
        if key not in self._cache:
            path = self.path(kind, slug, year)
            tags = self.scenario.tags
            if path.exists():
                df = read_csv(path, index_col=INDEX_NAME, dtype={INDEX_NAME: str})
                df = df.reindex(index=tags) if kind == INTERNAL_GRADES else df.reindex(index=tags, columns=tags)
                df = df.astype(float)
            elif kind == INTERNAL_GRADES:
                df = pd.DataFrame(index=pd.Index(tags), dtype=float)
            else:
                df = pd.DataFrame(np.nan, index=tags, columns=tags)
            df.index.name = INDEX_NAME
            self._cache[key] = df
        df = self._cache[key]
        if kind == INTERNAL_GRADES and slug is not None and slug not in df.columns:
            df[slug] = np.nan
        return df

    def values(self, kind: str, slug: str, year: int) -> pd.Series | pd.DataFrame:
        """Series (tag -> value) for internal grades, matrix for relations."""
        df = self.frame(kind, slug, year)
        return df[slug] if kind == INTERNAL_GRADES else df

    def has_file(self, kind: str, slug: str, year: int) -> bool:
        path = self.path(kind, slug, year)
        if kind != INTERNAL_GRADES:
            return path.exists()
        return path.exists() and slug in read_csv(path, nrows=0).columns

    # --- writing ---------------------------------------------------------------
    def mark_dirty(self, kind: str, slug: str | None, year: int) -> None:
        self._dirty.add(self._key(kind, slug, year))

    def set_values(self, kind: str, slug: str, year: int, data: pd.Series | pd.DataFrame) -> None:
        if isinstance(data, pd.Series):
            self.frame(kind, slug, year)[slug] = data
        else:
            self._cache[self._key(kind, slug, year)] = data
        self.mark_dirty(kind, slug, year)

    def drop(self, kind: str, slug: str, year: int) -> None:
        """Remove a grade column / all values of a relation for a year (applied on flush)."""
        df = self.frame(kind, slug, year)
        if kind == INTERNAL_GRADES:
            df.drop(columns=slug, inplace=True, errors="ignore")
        else:
            df.loc[:, :] = np.nan
        self.mark_dirty(kind, slug, year)

    def flush(self) -> int:
        """Write all modified frames. Returns the number of files touched."""
        for kind, slug, year in sorted(self._dirty, key=lambda k: (k[0], k[1] or "", k[2])):
            path = self.path(kind, slug, year)
            df = self._cache[(kind, slug, year)]
            # A relation without any value and a year without grade columns have no file.
            if df.columns.empty or (kind != INTERNAL_GRADES and df.isna().all().all()):
                path.unlink(missing_ok=True)
            else:
                write_csv(df, path)
        touched = len(self._dirty)
        self._dirty.clear()
        return touched

    def discard(self) -> None:
        self._cache.clear()
        self._dirty.clear()


def append_changelog(scenario: Scenario, rows: list[dict]) -> None:
    if not rows:
        return
    path = scenario.narrated_dir / "changelog.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = []
    for row in rows:
        rec = {col: row.get(col, "") for col in CHANGELOG_COLUMNS}
        rec["timestamp"] = rec["timestamp"] or now
        if isinstance(rec["params"], dict):
            rec["params"] = json.dumps(rec["params"], ensure_ascii=False, sort_keys=True)
        records.append(rec)
    if path.exists():
        header = read_csv(path, nrows=0).columns.tolist()
        if header != CHANGELOG_COLUMNS:  # older file without newer columns: rewrite once with the full header
            old = read_csv(path, dtype=str, keep_default_na=False).reindex(columns=CHANGELOG_COLUMNS, fill_value="")
            write_csv(old, path, index=False)
    pd.DataFrame(records, columns=CHANGELOG_COLUMNS).to_csv(
        path, mode="a", header=not path.exists(), index=False, encoding=ENCODING
    )
