"""Setting and reading narrated (descriptive) data: internal grades and relations.

One `Operation` fills one formula for a set of targets over a closed year interval,
using a change curve from `interpolation.py`. Targets:
    internal-grades        "POL"
    relations-directed     "POL:RUS"  (from POL towards RUS; row POL, column RUS)
    relations-doublesided  "POL:RUS"  (unordered; both matrix cells are written)
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields

import numpy as np
import pandas as pd

from simulator.formulas import Formula, get_formula, list_formulas
from simulator.interpolation import DISCRETE_CURVES, curve_values
from simulator.io import SimulatorError
from simulator.scenario import Scenario
from simulator.store import NarratedStore, append_changelog
from simulator.templates import INTERNAL_GRADES, KINDS, RELATIONS_DOUBLESIDED, resolve_kind

PAIR_SEPARATOR = ":"
CURRENT = "current"


def parse_years(years: str | int | list[int] | tuple[int, int]) -> tuple[int, int]:
    """'1990-2000' | '1995' | 1995 | [1990, 2000] -> (start, end)."""
    if isinstance(years, int):
        return years, years
    if isinstance(years, (list, tuple)):
        if len(years) == 1:
            return int(years[0]), int(years[0])
        if len(years) == 2:
            return int(years[0]), int(years[1])
        raise SimulatorError(f"years must be [start, end], got {years!r}")
    parts = str(years).strip().split("-")
    try:
        if len(parts) == 1:
            return int(parts[0]), int(parts[0])
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
    except ValueError:
        pass
    raise SimulatorError(f"Cannot parse years {years!r}; use e.g. '1990-2000' or '1995'")


def parse_targets(kind: str, targets: str | list[str]) -> list[str] | list[tuple[str, str]]:
    if isinstance(targets, str):
        targets = [t for t in targets.split(",") if t.strip()]
    targets = [t.strip().upper() for t in targets]
    if not targets:
        raise SimulatorError("No targets given")
    if kind == INTERNAL_GRADES:
        bad = [t for t in targets if PAIR_SEPARATOR in t]
        if bad:
            raise SimulatorError(f"Internal grades take single tags, got pairs: {bad}")
        return list(dict.fromkeys(targets))
    pairs: list[tuple[str, str]] = []
    for t in targets:
        sides = t.split(PAIR_SEPARATOR)
        if len(sides) != 2 or not all(sides):
            raise SimulatorError(f"Relation target must be 'AAA{PAIR_SEPARATOR}BBB', got {t!r}")
        a, b = sides
        if a == b:
            raise SimulatorError(f"A relation needs two different tags, got {t!r}")
        if kind == RELATIONS_DOUBLESIDED:
            a, b = sorted((a, b))
        pairs.append((a, b))
    return list(dict.fromkeys(pairs))


def _target_label(target: str | tuple[str, str]) -> str:
    return target if isinstance(target, str) else PAIR_SEPARATOR.join(target)


def _target_tags(target: str | tuple[str, str]) -> tuple[str, ...]:
    return (target,) if isinstance(target, str) else target


def _get(store: NarratedStore, kind: str, slug: str, year: int, target) -> float:
    vals = store.values(kind, slug, year)
    return float(vals[target] if isinstance(target, str) else vals.at[target[0], target[1]])


def _set(store: NarratedStore, kind: str, slug: str, year: int, target, value: float) -> None:
    df = store.frame(kind, slug, year)
    if isinstance(target, str):
        df.at[target, slug] = value
    else:
        df.at[target[0], target[1]] = value
        if kind == RELATIONS_DOUBLESIDED:
            df.at[target[1], target[0]] = value
    store.mark_dirty(kind, slug, year)


@dataclass
class Operation:
    kind: str
    name: str
    targets: str | list[str]
    years: str | int | list[int]
    curve: str = "linear"
    start: float | str | None = None
    end: float | None = None
    values: list[float] | None = None
    params: dict[str, float] = field(default_factory=dict)
    only_empty: bool = False
    clip: bool = False
    rationale: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Operation:
        allowed = {f.name for f in fields(cls)}
        unknown = set(data) - allowed
        if unknown:
            raise SimulatorError(f"Unknown operation keys {sorted(unknown)}; allowed: {sorted(allowed)}")
        return cls(**data)


@dataclass
class Result:
    operation: Operation
    formula: Formula
    written: int
    skipped: int
    preview: pd.DataFrame  # years x targets, values as computed (before only_empty)


def _apply(scenario: Scenario, store: NarratedStore, op: Operation) -> Result:
    kind = resolve_kind(op.kind)
    formula = get_formula(scenario, kind, op.name)
    years = scenario.years_between(*parse_years(op.years))
    targets = parse_targets(kind, op.targets)
    scenario.check_tags([t for target in targets for t in _target_tags(target)])

    exist = scenario.existence(years)
    for target in targets:
        for tag in _target_tags(target):
            missing = [y for y in years if not exist.at[y, tag]]
            if missing:
                raise SimulatorError(
                    f"{tag} does not exist in {missing[0]}..{missing[-1]} (see exists_from/exists_to in tags.csv)"
                )

    if formula.is_binary and op.curve not in DISCRETE_CURVES:
        raise SimulatorError(
            f"{formula.name!r} is a 0/1 flag; use one of the curves {DISCRETE_CURVES}, not {op.curve!r}"
        )

    preview = pd.DataFrame(index=pd.Index(years, name="year"), dtype=float)
    written = skipped = 0
    for target in targets:
        start = op.start
        if isinstance(start, str):
            if start.strip().lower() != CURRENT:
                start = float(start)
            else:
                start = _get(store, kind, formula.slug, years[0], target)
                if np.isnan(start):
                    raise SimulatorError(
                        f"start='{CURRENT}' but {_target_label(target)} has no {formula.name!r} value in {years[0]}"
                    )
        vals = curve_values(years, op.curve, start, op.end, op.params, op.values)
        if formula.type == "int":
            vals = np.round(vals)
        bad = formula.violations(vals)
        if bad.any():
            if not op.clip:
                raise SimulatorError(
                    f"{_target_label(target)}: values {np.round(vals[bad], 4).tolist()} in years "
                    f"{np.asarray(years)[bad].tolist()} break {formula.name!r} "
                    f"({formula.type} in [{formula.valmin}, {formula.valmax}]); pass clip to clip them"
                )
            vals = formula.coerce(vals)
        preview[_target_label(target)] = vals
        for year, value in zip(years, vals):
            if op.only_empty and not np.isnan(_get(store, kind, formula.slug, year, target)):
                skipped += 1
                continue
            _set(store, kind, formula.slug, year, target, float(value))
            written += 1
    return Result(op, formula, written, skipped, preview)


def apply_operations(
    scenario: Scenario,
    operations: list[Operation],
    author: str,
    rationale: str = "",
    dry_run: bool = False,
) -> list[Result]:
    """Apply operations in order, all-or-nothing. Later operations see earlier ones."""
    if not author:
        raise SimulatorError("author is required (who sets the values, e.g. 'user' or a model name)")
    with scenario.lock():
        store = NarratedStore(scenario)
        results: list[Result] = []
        for i, op in enumerate(operations, 1):
            try:
                results.append(_apply(scenario, store, op))
            except SimulatorError as e:
                raise SimulatorError(f"Operation {i} ({op.kind} {op.name!r}): {e}") from None
        if dry_run:
            return results
        store.flush()
        append_changelog(scenario, [
            {
                "author": author,
                "operation": "set",
                "kind": r.formula.kind,
                "name": r.formula.name,
                "targets": ";".join(r.preview.columns),
                "years": f"{r.preview.index[0]}-{r.preview.index[-1]}",
                "params": {
                    "curve": r.operation.curve, "start": r.operation.start, "end": r.operation.end,
                    "values": r.operation.values, "params": r.operation.params,
                    "only_empty": r.operation.only_empty, "clip": r.operation.clip,
                },
                "rationale": r.operation.rationale or rationale,
            }
            for r in results
        ])
    return results


def show(
    scenario: Scenario, kind: str, name: str, targets: str | list[str], years: str | int | list[int]
) -> pd.DataFrame:
    """Current values as a years x targets table (NaN = not filled)."""
    kind = resolve_kind(kind)
    formula = get_formula(scenario, kind, name)
    yrs = scenario.years_between(*parse_years(years))
    tgts = parse_targets(kind, targets)
    scenario.check_tags([t for target in tgts for t in _target_tags(target)])
    store = NarratedStore(scenario)
    return pd.DataFrame(
        {_target_label(t): [_get(store, kind, formula.slug, y, t) for y in yrs] for t in tgts},
        index=pd.Index(yrs, name="year"),
    )


def missing_report(scenario: Scenario, kind: str | None = None, name: str | None = None) -> pd.DataFrame:
    """Per formula: how many cells (existing countries/pairs x years) are filled."""
    kinds = KINDS if kind is None else (resolve_kind(kind),)
    store = NarratedStore(scenario)
    exist = scenario.existence().to_numpy()  # years x tags
    rows = []
    for k in kinds:
        formulas = list_formulas(scenario, k) if name is None else [get_formula(scenario, k, name)]
        for f in formulas:
            total = filled = 0
            first_gap = None
            for yi, year in enumerate(scenario.dates):
                alive = exist[yi]
                vals = store.values(k, f.slug, year).to_numpy(dtype=float)
                if k == INTERNAL_GRADES:
                    mask = alive
                else:
                    mask = alive[:, None] & alive[None, :]
                    np.fill_diagonal(mask, False)
                    if k == RELATIONS_DOUBLESIDED:
                        mask = np.triu(mask)
                n_total, n_filled = int(mask.sum()), int((~np.isnan(vals) & mask).sum())
                total += n_total
                filled += n_filled
                if first_gap is None and n_filled < n_total:
                    first_gap = year
            rows.append({
                "kind": k, "name": f.name, "filled": filled, "total": total,
                "percent": round(100 * filled / total, 2) if total else 100.0,
                "first_year_with_gaps": first_gap,
            })
    return pd.DataFrame(rows)
