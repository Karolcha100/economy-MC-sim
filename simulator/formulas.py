"""Formulas: user-editable definitions of descriptive statistics (one row per statistic).

Stored in `<scenario>/formulas/<kind>.csv`; columns are the fields of the matching template.
Editing a formula migrates the narrated data that already uses it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from simulator.io import SimulatorError, read_csv, slugify, write_csv
from simulator.scenario import Scenario
from simulator.store import NarratedStore, append_changelog
from simulator.templates import INTERNAL_GRADES, load_template, resolve_kind, validate_formulas


@dataclass(frozen=True)
class Formula:
    kind: str
    name: str
    type: str
    valmin: float
    valmax: float
    default: float | None = None  # assumed for unfilled cells; None = must be filled
    description: str = ""

    @classmethod
    def from_row(cls, kind: str, row: pd.Series) -> Formula:
        default = str(row["default"]).strip()
        return cls(kind, row["name"], row["type"], float(row["valmin"]), float(row["valmax"]),
                   float(default) if default else None, str(row["description"]).strip())

    @property
    def slug(self) -> str:
        return slugify(self.name)

    @property
    def is_binary(self) -> bool:
        return self.type == "int" and self.valmin == 0 and self.valmax == 1

    def violations(self, values: np.ndarray) -> np.ndarray:
        """Boolean mask of filled values that break the range or the integer type."""
        bad = (values < self.valmin) | (values > self.valmax)
        if self.type == "int":
            bad |= ~np.isclose(values, np.round(values))
        return bad & ~np.isnan(values)

    def coerce(self, values: np.ndarray) -> np.ndarray:
        """Round (int formulas) and clip into [valmin, valmax]; NaN stays NaN."""
        out = np.round(values) if self.type == "int" else values
        return np.clip(out, self.valmin, self.valmax)


def _fmt_number(x: float | str | None) -> str:
    """Number as written in formula files; None/'' -> empty cell."""
    if x is None or (isinstance(x, str) and not x.strip()):
        return ""
    x = float(x)
    return str(int(x)) if x.is_integer() else repr(x)


def load_table(scenario: Scenario, kind: str) -> pd.DataFrame:
    kind = resolve_kind(kind)
    path = scenario.formulas_dir / f"{kind}.csv"
    template = load_template(kind)
    if not path.exists():
        return pd.DataFrame(columns=template.field_names, dtype=str)
    return read_csv(path, dtype=str, keep_default_na=False)


def _save_table(scenario: Scenario, kind: str, table: pd.DataFrame) -> None:
    errors = validate_formulas(load_template(kind), table)
    if errors:
        raise SimulatorError("Invalid formulas:\n  " + "\n  ".join(errors))
    write_csv(table, scenario.formulas_dir / f"{kind}.csv", index=False)


def list_formulas(scenario: Scenario, kind: str) -> list[Formula]:
    kind = resolve_kind(kind)
    table = load_table(scenario, kind)
    errors = validate_formulas(load_template(kind), table)
    if errors:
        raise SimulatorError("Invalid formulas file:\n  " + "\n  ".join(errors))
    return [Formula.from_row(kind, r) for _, r in table.iterrows()]


def get_formula(scenario: Scenario, kind: str, name: str) -> Formula:
    """Find a formula by its name or slug."""
    kind = resolve_kind(kind)
    wanted = slugify(name)
    for f in list_formulas(scenario, kind):
        if f.slug == wanted:
            return f
    known = ", ".join(f.name for f in list_formulas(scenario, kind))
    raise SimulatorError(f"No {kind} formula named {name!r}. Known: {known}")


def _row_index(table: pd.DataFrame, name: str) -> int:
    slugs = table["name"].map(slugify)
    hits = table.index[slugs == slugify(name)]
    if hits.empty:
        raise SimulatorError(f"No formula named {name!r}")
    return int(hits[0])


def _data_years(store: NarratedStore, formula: Formula) -> list[int]:
    return [y for y in store.scenario.dates if store.has_file(formula.kind, formula.slug, y)]


def add_formula(
    scenario: Scenario,
    kind: str,
    name: str,
    type: str,
    valmin: float,
    valmax: float,
    description: str,
    default: float | None = None,
    entities: dict[str, str] | None = None,
    author: str = "",
    rationale: str = "",
) -> Formula:
    kind = resolve_kind(kind)
    template = load_template(kind)
    row = {"name": name.strip(), "type": type, "valmin": _fmt_number(valmin), "valmax": _fmt_number(valmax),
           "default": _fmt_number(default), "description": description.strip()}
    for field in template.entity_fields:
        row[field] = (entities or {}).get(field, "TAG")
    with scenario.lock():
        table = load_table(scenario, kind)
        table = pd.concat([table, pd.DataFrame([row])], ignore_index=True)[template.field_names]
        _save_table(scenario, kind, table)
        append_changelog(scenario, [{
            "author": author, "operation": "formula-add", "kind": kind, "name": row["name"],
            "params": row, "rationale": rationale,
        }])
    # New formulas start empty: missing data reads as NaN, nothing to initialise.
    return get_formula(scenario, kind, name)


def edit_formula(
    scenario: Scenario,
    kind: str,
    name: str,
    new_name: str | None = None,
    type: str | None = None,
    valmin: float | None = None,
    valmax: float | None = None,
    clip: bool = False,
    author: str = "",
    rationale: str = "",
    default: float | str | None = None,
    description: str | None = None,
) -> Formula:
    """Edit a formula and migrate narrated data. None = leave a field unchanged.

    Rename -> files/columns are renamed in every year. Type/range change -> existing values
    are checked; violations raise unless `clip` (round for int + clip into the new range).
    `default=""` removes the default.
    """
    kind = resolve_kind(kind)
    with scenario.lock():
        old = get_formula(scenario, kind, name)
        table = load_table(scenario, kind)
        i = _row_index(table, name)
        if new_name is not None:
            table.at[i, "name"] = new_name.strip()
        if type is not None:
            table.at[i, "type"] = type
        if valmin is not None:
            table.at[i, "valmin"] = _fmt_number(valmin)
        if valmax is not None:
            table.at[i, "valmax"] = _fmt_number(valmax)
        if default is not None:
            table.at[i, "default"] = _fmt_number(default)
        if description is not None:
            table.at[i, "description"] = description.strip()
        errors = validate_formulas(load_template(kind), table)
        if errors:
            raise SimulatorError("Invalid formula after edit:\n  " + "\n  ".join(errors))
        new = Formula.from_row(kind, table.loc[i])

        store = NarratedStore(scenario)
        years = _data_years(store, old)
        if kind != INTERNAL_GRADES and new.slug != old.slug:
            for year in years:
                if store.path(kind, new.slug, year).exists():
                    raise SimulatorError(f"Cannot rename: {store.path(kind, new.slug, year)} exists")
        problems: list[str] = []
        for year in years:
            vals = store.values(kind, old.slug, year).copy()
            arr = vals.to_numpy(dtype=float)
            bad = new.violations(arr)
            if bad.any():
                if not clip:
                    problems.append(f"{year}: {int(bad.sum())} value(s) outside new definition")
                    continue
                vals[:] = np.where(np.isnan(arr), np.nan, new.coerce(arr))
            if new.slug != old.slug or bad.any():
                store.drop(kind, old.slug, year)
                store.set_values(kind, new.slug, year, vals)
        if problems:
            store.discard()
            raise SimulatorError(
                f"Existing data of {old.name!r} breaks the new definition (use clip to fix):\n  "
                + "\n  ".join(problems)
            )
        _save_table(scenario, kind, table)
        store.flush()
        append_changelog(scenario, [{
            "author": author, "operation": "formula-edit", "kind": kind, "name": old.name,
            "params": {"new_name": new.name, "type": new.type, "valmin": new.valmin,
                       "valmax": new.valmax, "default": new.default, "clip": clip,
                       "description_changed": description is not None},
            "rationale": rationale,
        }])
    return new


def remove_formula(
    scenario: Scenario, kind: str, name: str, purge: bool = False, author: str = "", rationale: str = ""
) -> Formula:
    """Remove a formula. If narrated data exists, `purge` must be set to delete it too."""
    kind = resolve_kind(kind)
    with scenario.lock():
        formula = get_formula(scenario, kind, name)
        store = NarratedStore(scenario)
        years = _data_years(store, formula)
        filled = [y for y in years if store.values(kind, formula.slug, y).notna().to_numpy().any()]
        if filled and not purge:
            raise SimulatorError(
                f"{formula.name!r} has data in {len(filled)} year(s) ({filled[0]}..{filled[-1]}); "
                "pass purge to delete it together with the formula"
            )
        for year in years:
            store.drop(kind, formula.slug, year)
        table = load_table(scenario, kind)
        table = table.drop(index=_row_index(table, name)).reset_index(drop=True)
        _save_table(scenario, kind, table)
        store.flush()
        append_changelog(scenario, [{
            "author": author, "operation": "formula-remove", "kind": kind, "name": formula.name,
            "params": {"purge": purge, "years_with_data": len(filled)}, "rationale": rationale,
        }])
    return formula
