"""Consistency checks of a whole scenario. Errors break rules; warnings are suspicious only."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from simulator.formulas import list_formulas
from simulator.history import load_metadata
from simulator.io import SimulatorError, read_csv, slugify
from simulator.scenario import Scenario
from simulator.store import NarratedStore
from simulator.templates import INTERNAL_GRADES, KINDS, RELATION_KINDS, RELATIONS_DOUBLESIDED


@dataclass
class Issue:
    level: str  # "error" | "warning"
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.where}: {self.message}"


def validate(scenario: Scenario) -> list[Issue]:
    issues: list[Issue] = []

    def err(where: str, msg: str) -> None:
        issues.append(Issue("error", where, msg))

    def warn(where: str, msg: str) -> None:
        issues.append(Issue("warning", where, msg))

    # tags / dates ------------------------------------------------------------------
    try:
        tags = scenario.tags_table
        dates = scenario.dates
    except SimulatorError as e:
        err("scenario", str(e))
        return issues
    if tags.index.duplicated().any():
        err("tags.csv", f"duplicated tags: {sorted(tags.index[tags.index.duplicated()])}")
    both = tags["exists_from"].notna() & tags["exists_to"].notna()
    for tag in tags.index[both & (tags["exists_from"] > tags["exists_to"])]:
        err("tags.csv", f"{tag}: exists_from > exists_to")
    if dates != sorted(set(dates)):
        err("dates.csv", "dates must be unique and sorted")

    # formulas ------------------------------------------------------------------------
    formulas = {}
    for kind in KINDS:
        try:
            formulas[kind] = {f.slug: f for f in list_formulas(scenario, kind)}
        except SimulatorError as e:
            err(f"formulas/{kind}.csv", str(e))
            formulas[kind] = {}
        if not (scenario.formulas_dir / f"{kind}.csv").exists():
            warn(f"formulas/{kind}.csv", "missing (no formulas of this kind)")

    # history -------------------------------------------------------------------------
    meta = load_metadata(scenario)
    if scenario.history_dir.exists():
        for path in sorted(scenario.history_dir.glob("*.csv")):
            if path.name == "metadata.csv":
                continue
            where = f"history/{path.name}"
            if path.stem != slugify(path.stem):
                err(where, "file name is not a slug (lowercase, '-' instead of spaces)")
            df = read_csv(path, index_col=0)
            if [int(i) for i in df.index] != dates:
                err(where, "rows do not match dates.csv")
            extra = sorted(set(df.columns) - set(tags.index))
            if extra:
                err(where, f"unknown tag columns: {extra[:10]}")
            if path.stem not in set(meta["name"]):
                warn(where, "no entry in history/metadata.csv")

    # narrated ------------------------------------------------------------------------
    store = NarratedStore(scenario)
    exist = scenario.existence()
    if scenario.narrated_dir.exists():
        for ydir in sorted(p for p in scenario.narrated_dir.iterdir() if p.is_dir()):
            if not ydir.name.isdigit() or int(ydir.name) not in dates:
                err(f"narrated/{ydir.name}", "directory is not a scenario date")
                continue
            year = int(ydir.name)
            alive = exist.loc[year].to_numpy()

            for path in sorted(ydir.rglob("*.csv")):
                df = read_csv(path, index_col=0, dtype=str)
                unknown = sorted(set(df.index) - set(tags.index))
                if path.parent != ydir:
                    unknown += sorted(set(df.columns) - set(tags.index))
                if unknown:
                    err(str(path.relative_to(scenario.root)), f"unknown tags (dropped on next write): {unknown[:10]}")

            grades_path = ydir / f"{INTERNAL_GRADES}.csv"
            if grades_path.exists():
                cols = read_csv(grades_path, nrows=0).columns[1:]
                for col in cols:
                    if col not in formulas[INTERNAL_GRADES]:
                        warn(f"narrated/{year}/{grades_path.name}", f"column {col!r} has no formula")
            for kind in RELATION_KINDS:
                kdir = ydir / kind
                if kdir.exists():
                    for p in kdir.glob("*.csv"):
                        if p.stem not in formulas[kind]:
                            warn(f"narrated/{year}/{kind}/{p.name}", "file has no formula")

            for kind in KINDS:
                for slug, f in formulas[kind].items():
                    if not store.has_file(kind, slug, year):
                        continue
                    where = f"narrated/{year}/{kind}" + ("" if kind == INTERNAL_GRADES else f"/{slug}.csv")
                    vals = store.values(kind, slug, year).to_numpy(dtype=float)
                    filled = ~np.isnan(vals)
                    bad = f.violations(vals)
                    if bad.any():
                        err(where, f"{f.name!r}: {int(bad.sum())} value(s) outside {f.type} [{f.valmin}, {f.valmax}]")
                    if kind == INTERNAL_GRADES:
                        dead = filled & ~alive
                    else:
                        dead = filled & ~(alive[:, None] & alive[None, :])
                        if filled.diagonal().any():
                            err(where, "diagonal (country towards itself) must be empty")
                        if kind == RELATIONS_DOUBLESIDED:
                            same = (vals == vals.T) | (np.isnan(vals) & np.isnan(vals.T))
                            if not same.all():
                                err(where, f"matrix is not symmetric ({int((~same).sum()) // 2} pair(s))")
                    if dead.any():
                        err(where, f"{f.name!r}: {int(dead.sum())} value(s) for countries not existing in {year}")
    return issues
