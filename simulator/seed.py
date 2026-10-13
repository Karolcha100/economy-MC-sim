"""Seed values: the first, automatic version of narrated data computed from real indicators.

Rules live in `<scenario>/seeds.csv` (kind, name, source, transform, a, b, note) so the author can
change them without code. Transforms:
    linear           value = a + b * x                      (x = history statistic)
    per-1000-linear  value = a + b * (x / population * 1000) (needs history 'population')
    pairs-at-least   pair value 1 where the dyadic history value >= a (relations only)
Values are clipped to the formula range (and rounded for int formulas). Gaps inside an indicator's
range are interpolated linearly; years before its first / after its last value stay empty (for LLMs).
Seeds never overwrite filled cells, so corrections made later by LLMs survive a re-run.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from simulator.formulas import Formula, get_formula
from simulator.history import load_dyadic, load_history
from simulator.io import SimulatorError, read_csv
from simulator.scenario import Scenario
from simulator.store import NarratedStore, append_changelog
from simulator.templates import INTERNAL_GRADES, RELATIONS_DOUBLESIDED, resolve_kind

TRANSFORMS = ("linear", "per-1000-linear", "pairs-at-least")
SEED_COLUMNS = ["kind", "name", "source", "transform", "a", "b", "note"]


@dataclass
class Rule:
    kind: str
    name: str
    source: str
    transform: str
    a: float
    b: float
    note: str

    @property
    def author(self) -> str:
        return f"seed:{self.source}"


def load_rules(scenario: Scenario, name: str | None = None) -> list[Rule]:
    path = scenario.root / "seeds.csv"
    if not path.exists():
        raise SimulatorError(f"No seed rules: {path}")
    df = read_csv(path, dtype=str, keep_default_na=False)
    missing = set(SEED_COLUMNS) - set(df.columns)
    if missing:
        raise SimulatorError(f"{path}: missing columns {sorted(missing)}")
    rules = []
    for _, r in df.iterrows():
        if r["transform"] not in TRANSFORMS:
            raise SimulatorError(f"{path}: unknown transform {r['transform']!r}; use one of {TRANSFORMS}")
        rules.append(Rule(resolve_kind(r["kind"]), r["name"], r["source"], r["transform"],
                          float(r["a"] or 0), float(r["b"] or 0), r["note"]))
    if name is not None:
        rules = [r for r in rules if r.name == name]
        if not rules:
            raise SimulatorError(f"No seed rule for {name!r}")
    return rules


def country_values(scenario: Scenario, rule: Rule, formula: Formula) -> pd.DataFrame:
    """Seed values (years x tags) for an internal-grades rule; NaN = no seed."""
    x = load_history(scenario, rule.source).reindex(index=scenario.dates, columns=scenario.tags)
    if rule.transform == "per-1000-linear":
        x = x / load_history(scenario, "population").reindex(index=scenario.dates, columns=scenario.tags) * 1000
    elif rule.transform != "linear":
        raise SimulatorError(f"{rule.name}: transform {rule.transform!r} is for relations")
    alive = scenario.existence()
    x = x.where(alive).interpolate(method="index", limit_area="inside").where(alive)  # Y1: inner gaps only
    values = rule.a + rule.b * x
    values = values.clip(formula.valmin, formula.valmax)
    return values.round() if formula.type == "int" else values


def pair_values(scenario: Scenario, rule: Rule) -> pd.DataFrame:
    """Pairs (date, side_a, side_b) that get value 1."""
    if rule.transform != "pairs-at-least":
        raise SimulatorError(f"{rule.name}: relations need the pairs-at-least transform")
    d = load_dyadic(scenario, rule.source)
    return d[d["value"] >= rule.a][["date", "side_a", "side_b"]]


def apply_seeds(scenario: Scenario, name: str | None = None, dry_run: bool = False) -> pd.DataFrame:
    """Write seed values into empty cells. Returns a report per rule."""
    rules = load_rules(scenario, name)
    report = []
    with scenario.lock():
        store = NarratedStore(scenario)
        log = []
        for rule in rules:
            formula = get_formula(scenario, rule.kind, rule.name)
            written = skipped = 0
            years: list[int] = []
            if rule.kind == INTERNAL_GRADES:
                values = country_values(scenario, rule, formula)
                for year in scenario.dates:
                    new = values.loc[year]
                    if new.isna().all():
                        continue
                    frame = store.frame(INTERNAL_GRADES, formula.slug, year)
                    current = frame[formula.slug]
                    take = new.notna() & current.isna()
                    skipped += int((new.notna() & current.notna()).sum())
                    if take.any():
                        frame.loc[take[take].index, formula.slug] = new[take]
                        store.mark_dirty(INTERNAL_GRADES, formula.slug, year)
                        written += int(take.sum())
                        years.append(year)
            else:
                if formula.valmax < 1 or formula.valmin > 1:
                    raise SimulatorError(f"{rule.name}: value 1 is outside the formula range")
                for year, rows in pair_values(scenario, rule).groupby("date"):
                    frame = store.frame(rule.kind, formula.slug, int(year))
                    touched = False
                    for a, b in zip(rows["side_a"], rows["side_b"]):
                        if not np.isnan(frame.at[a, b]):
                            skipped += 1
                            continue
                        frame.at[a, b] = 1.0
                        if rule.kind == RELATIONS_DOUBLESIDED:
                            frame.at[b, a] = 1.0
                        written += 1
                        touched = True
                    if touched:
                        store.mark_dirty(rule.kind, formula.slug, int(year))
                        years.append(int(year))
            report.append({"kind": rule.kind, "name": rule.name, "source": rule.source, "transform": rule.transform,
                           "written": written, "skipped (filled)": skipped,
                           "years": f"{min(years)}-{max(years)}" if years else ""})
            if written:
                log.append({"author": rule.author, "operation": "seed", "kind": rule.kind, "name": rule.name,
                            "targets": "*", "years": report[-1]["years"],
                            "params": {"transform": rule.transform, "a": rule.a, "b": rule.b, "written": written},
                            "rationale": rule.note, "sources": f"history: {rule.source}"})
        if not dry_run:
            store.flush()
            append_changelog(scenario, log)
    return pd.DataFrame(report)


def seed_deviations(scenario: Scenario, threshold: float) -> list[dict]:
    """Narrated values that differ from the seed of their indicator by more than `threshold` (Y2)."""
    path = scenario.root / "seeds.csv"
    if not path.exists():
        return []
    store = NarratedStore(scenario)
    rows = []
    for rule in load_rules(scenario):
        if rule.kind != INTERNAL_GRADES:
            continue  # pair seeds are 0/1 decisions reviewed by hand (e.g. UCDP level-1 cases)
        formula = get_formula(scenario, rule.kind, rule.name)
        seeds = country_values(scenario, rule, formula)
        for year in scenario.dates:
            actual = store.values(INTERNAL_GRADES, formula.slug, year)
            diff = (actual - seeds.loc[year]).abs()
            for tag in diff.index[diff > threshold]:
                rows.append({"check": "seed-deviation", "kind": rule.kind, "name": rule.name, "target": tag,
                             "year": year, "message": f"{actual[tag]:g} vs seed {seeds.at[year, tag]:g} "
                                                      f"from {rule.source} (more than {threshold:g})"})
    return rows
