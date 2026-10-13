"""Scenario: a directory with tags, dates, formulas, history and narrated data.

Layout (`simulator/scenarios/<scenario>/`):
    tags.csv                    tag,name,exists_from,exists_to
    dates.csv                   date (one year per row)
    groups.csv                  group,tag,from,to,note (membership years; a tag may have several rows)
    reference-countries.csv     tag,reason (calibration anchors for LLMs, see `reference_map.py`)
    formulas/<kind>.csv         one formula per row, columns = template fields
    history/<stat>.csv          real statistics: rows = dates, columns = tags
    history/metadata.csv        unit, source, ... per statistic
    history/fill-log.csv        every history value that was estimated (source/interpolate/extrapolate)
    narrated/<year>/internal-grades.csv               rows = tags, columns = grade slugs
    narrated/<year>/relations-directed/<slug>.csv     matrix, row = from, column = to
    narrated/<year>/relations-doublesided/<slug>.csv  symmetric matrix
    narrated/changelog.csv      provenance of every narrated write
"""

from __future__ import annotations

from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import Generator

import numpy as np
import pandas as pd

from simulator.io import SimulatorError, file_lock, read_csv

SCENARIOS_DIR = Path(__file__).parent / "scenarios"
TAGS_COLUMNS = ["tag", "name", "exists_from", "exists_to"]
GROUPS_COLUMNS = ["group", "tag", "from", "to", "note"]


class Scenario:
    def __init__(self, root: Path):
        self.root = Path(root)
        if not self.root.is_dir():
            raise SimulatorError(f"Scenario directory not found: {self.root}")

    @classmethod
    def open(cls, name_or_path: str | Path) -> Scenario:
        path = Path(name_or_path)
        if not path.is_dir():
            path = SCENARIOS_DIR / str(name_or_path)
        return cls(path)

    @property
    def name(self) -> str:
        return self.root.name

    # --- paths -----------------------------------------------------------------
    @property
    def formulas_dir(self) -> Path:
        return self.root / "formulas"

    @property
    def history_dir(self) -> Path:
        return self.root / "history"

    @property
    def narrated_dir(self) -> Path:
        return self.root / "narrated"

    def year_dir(self, year: int) -> Path:
        return self.narrated_dir / str(year)

    @contextmanager
    def lock(self) -> Generator[None]:
        with file_lock(self.root / ".lock"):
            yield

    # --- tags ------------------------------------------------------------------
    @cached_property
    def tags_table(self) -> pd.DataFrame:
        path = self.root / "tags.csv"
        if not path.exists():
            raise SimulatorError(f"Missing {path}")
        df = read_csv(path, dtype={"tag": str, "name": str})
        missing = [c for c in TAGS_COLUMNS if c not in df.columns]
        if missing:
            raise SimulatorError(f"{path}: missing columns {missing}")
        return df.set_index("tag")

    @property
    def tags(self) -> list[str]:
        return self.tags_table.index.tolist()

    def check_tags(self, tags: list[str]) -> None:
        unknown = sorted(set(tags) - set(self.tags))
        if unknown:
            raise SimulatorError(f"Unknown tags: {', '.join(unknown)} (see {self.root / 'tags.csv'})")

    def exists(self, tag: str, year: int) -> bool:
        return bool(self.existence([year]).at[year, tag])

    def existence(self, years: list[int] | None = None) -> pd.DataFrame:
        """Boolean frame (years x tags): does the tag exist in that year."""
        years = self.dates if years is None else years
        t = self.tags_table
        y = np.asarray(years)[:, None]
        lo = t["exists_from"].to_numpy(dtype=float)[None, :]
        hi = t["exists_to"].to_numpy(dtype=float)[None, :]
        mask = (np.isnan(lo) | (y >= lo)) & (np.isnan(hi) | (y <= hi))
        return pd.DataFrame(mask, index=years, columns=t.index)

    # --- dates -----------------------------------------------------------------
    @cached_property
    def dates(self) -> list[int]:
        path = self.root / "dates.csv"
        if not path.exists():
            raise SimulatorError(f"Missing {path}")
        return [int(d) for d in read_csv(path)["date"]]

    def years_between(self, start: int, end: int) -> list[int]:
        """Dates in the closed interval [start, end]; both ends must be scenario dates."""
        for y in (start, end):
            if y not in self.dates:
                raise SimulatorError(
                    f"Year {y} is not a scenario date ({self.dates[0]}..{self.dates[-1]})"
                )
        if start > end:
            raise SimulatorError(f"Start year {start} is after end year {end}")
        return [d for d in self.dates if start <= d <= end]

    # --- groups ----------------------------------------------------------------
    @cached_property
    def groups_table(self) -> pd.DataFrame:
        path = self.root / "groups.csv"
        if not path.exists():
            return pd.DataFrame(columns=GROUPS_COLUMNS)
        df = read_csv(path, dtype={"group": str, "tag": str, "note": str})
        missing = [c for c in GROUPS_COLUMNS if c not in df.columns]
        if missing:
            raise SimulatorError(f"{path}: missing columns {missing}")
        df["group"] = df["group"].str.upper()
        return df

    @property
    def groups(self) -> list[str]:
        return sorted(self.groups_table["group"].unique())

    def membership(self, group: str, years: list[int]) -> pd.DataFrame:
        """Boolean frame (years x tags): is the tag a member of `group` in that year."""
        group = group.upper()
        rows = self.groups_table[self.groups_table["group"] == group]
        if rows.empty:
            raise SimulatorError(f"Unknown group {group!r}. Known: {', '.join(self.groups) or 'none'} (groups.csv)")
        mask = pd.DataFrame(False, index=years, columns=self.tags)
        y = np.asarray(years)
        for _, r in rows.iterrows():
            if r["tag"] not in mask.columns:
                raise SimulatorError(f"groups.csv: unknown tag {r['tag']!r} in group {group}")
            lo = -np.inf if pd.isna(r["from"]) else float(r["from"])
            hi = np.inf if pd.isna(r["to"]) else float(r["to"])
            mask[r["tag"]] |= (y >= lo) & (y <= hi)
        return mask
