"""Scenario: a directory with tags, dates, formulas, history and narrated data.

Layout (`simulator/scenarios/<scenario>/`):
    tags.csv                    tag,name,exists_from,exists_to
    dates.csv                   date (one year per row)
    formulas/<kind>.csv         one formula per row, columns = template fields
    history/<stat>.csv          real statistics: rows = dates, columns = tags
    history/metadata.csv        unit, source, ... per statistic
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
