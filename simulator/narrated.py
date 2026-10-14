"""Setting and reading narrated (descriptive) data: internal grades and relations.

One `Operation` fills one formula for a set of targets over a closed year interval,
using a change curve from `interpolation.py`. Targets:
    internal-grades        "POL"
    relations-directed     "POL:RUS"  (from POL towards RUS; row POL, column RUS)
    relations-doublesided  "POL:RUS"  (unordered; both matrix cells are written)
Each side may also be a group from groups.csv ("@NATO") or "*" (all countries). Such
targets are written only in years the country is a member and exists; other years are skipped.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from datetime import datetime, timezone

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
        if a == b and _is_explicit(a):
            raise SimulatorError(f"A relation needs two different tags, got {t!r}")
        if kind == RELATIONS_DOUBLESIDED:
            a, b = sorted((a, b))
        pairs.append((a, b))
    return list(dict.fromkeys(pairs))


GROUP_PREFIX = "@"
WILDCARD = "*"

Target = str | tuple[str, str]
Mask = np.ndarray | None  # active years of a target; None = explicit tag, must exist in every year


def _is_explicit(side: str) -> bool:
    return not side.startswith(GROUP_PREFIX) and side != WILDCARD


def _expand_side(scenario: Scenario, side: str, years: list[int]) -> dict[str, Mask]:
    if _is_explicit(side):
        scenario.check_tags([side])
        return {side: None}
    alive = scenario.existence(years)
    member = alive if side == WILDCARD else scenario.membership(side[1:], years) & alive
    return {tag: member[tag].to_numpy() for tag in member.columns if member[tag].any()}


def _and(a: Mask, b: Mask) -> Mask:
    if a is None:
        return b
    return a if b is None else a & b


def expand_targets(scenario: Scenario, kind: str, targets: str | list[str], years: list[int]) -> dict[Target, Mask]:
    """Expand groups and wildcards. Returns target -> active-year mask (None = explicit target)."""
    out: dict[Target, Mask] = {}
    for parsed in parse_targets(kind, targets):
        if isinstance(parsed, str):
            out.update(_expand_side(scenario, parsed, years))
            continue
        side_a, side_b = (_expand_side(scenario, s, years) for s in parsed)
        for a, mask_a in side_a.items():
            for b, mask_b in side_b.items():
                if a == b:
                    continue  # a group may contain the other side; explicit A:A is rejected in parse_targets
                pair = tuple(sorted((a, b))) if kind == RELATIONS_DOUBLESIDED else (a, b)
                mask = _and(mask_a, mask_b)
                if mask is not None and not mask.any():
                    continue
                if pair in out:  # listed twice: explicit wins, otherwise union of active years
                    prev = out[pair]
                    mask = None if prev is None or mask is None else prev | mask
                out[pair] = mask
    if not out:
        raise SimulatorError(f"Targets {targets!r} expand to nothing in {years[0]}..{years[-1]}")
    return out


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
    sources: str | list[str] = ""  # URLs / "title, outlet, date" of what the values are based on

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
    targets = expand_targets(scenario, kind, op.targets, years)

    exist = scenario.existence(years)
    for target, mask in targets.items():
        for tag in _target_tags(target):
            missing = [y for y in years if not exist.at[y, tag]]
            if missing and mask is None:
                raise SimulatorError(
                    f"{tag} does not exist in {missing[0]}..{missing[-1]} (see exists_from/exists_to in tags.csv)"
                )

    if formula.is_binary and op.curve not in DISCRETE_CURVES:
        raise SimulatorError(
            f"{formula.name!r} is a 0/1 flag; use one of the curves {DISCRETE_CURVES}, not {op.curve!r}"
        )

    preview = pd.DataFrame(index=pd.Index(years, name="year"), dtype=float)
    written = skipped = 0
    for target, mask in targets.items():
        start = op.start
        if isinstance(start, str):
            if start.strip().lower() != CURRENT:
                start = float(start)
            elif mask is not None:
                raise SimulatorError(f"start='{CURRENT}' is not allowed with group/wildcard targets")
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
        active = np.ones(len(years), dtype=bool) if mask is None else mask
        preview[_target_label(target)] = np.where(active, vals, np.nan)
        for year, value, on in zip(years, vals, active):
            if not on:
                continue
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
                "sources": r.operation.sources if isinstance(r.operation.sources, str)
                else " | ".join(r.operation.sources),
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
    tgts = expand_targets(scenario, kind, targets, yrs)
    store = NarratedStore(scenario)
    return pd.DataFrame(
        {_target_label(t): [_get(store, kind, formula.slug, y, t) for y in yrs] for t in tgts},
        index=pd.Index(yrs, name="year"),
    )


CONFIRMED_COLUMNS = ["timestamp", "author", "kind", "name", "tag", "from_year", "to_year", "note"]


def _confirmed_path(scenario: Scenario):
    return scenario.narrated_dir / "confirmed-defaults.csv"


def load_confirmed(scenario: Scenario) -> pd.DataFrame:
    path = _confirmed_path(scenario)
    if not path.exists():
        return pd.DataFrame(columns=CONFIRMED_COLUMNS)
    return pd.read_csv(path, dtype={"tag": str, "kind": str, "name": str}, keep_default_na=False)


def confirm_default(
    scenario: Scenario,
    kind: str,
    names: str | list[str],
    tags: str | list[str],
    years: str | int | list[int],
    author: str,
    note: str = "",
) -> int:
    """Record that unfilled cells are deliberately left at the formula default (decision P1, thread T011).

    Internal grades: the cells of `tags` in `years`. Relations: every pair where a tag is FROM
    (directed) or a side (double-sided). Existing values are untouched; nothing is written to the
    data files. Only formulas with a default can be confirmed. Returns the number of rows recorded.
    """
    if not author:
        raise SimulatorError("author is required")
    kind = resolve_kind(kind)
    if names == "all":
        formulas = [f for f in list_formulas(scenario, kind) if f.default is not None]
    else:
        names = [n.strip() for n in names.split(",")] if isinstance(names, str) else names
        formulas = [get_formula(scenario, kind, n) for n in names]
    no_default = [f.name for f in formulas if f.default is None]
    if no_default:
        raise SimulatorError(f"No default value, must be filled: {', '.join(no_default)}")
    tag_list = [t.strip().upper() for t in (tags.split(",") if isinstance(tags, str) else tags) if t.strip()]
    scenario.check_tags(tag_list)
    y0, y1 = parse_years(years)
    scenario.years_between(y0, y1)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = [{"timestamp": stamp, "author": author, "kind": kind, "name": f.name, "tag": t,
             "from_year": y0, "to_year": y1, "note": note} for f in formulas for t in tag_list]
    with scenario.lock():
        path = _confirmed_path(scenario)
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows, columns=CONFIRMED_COLUMNS).to_csv(path, mode="a", header=not path.exists(), index=False)
        append_changelog(scenario, [{"author": author, "operation": "confirm-default", "kind": kind,
                                     "name": ",".join(f.name for f in formulas), "targets": ";".join(tag_list),
                                     "years": f"{y0}-{y1}", "rationale": note}])
    return len(rows)


def _confirmed_matrix(scenario: Scenario, confirmed: pd.DataFrame, kind: str, name: str) -> np.ndarray:
    """years x tags: True where the formula's default is confirmed for that tag and year."""
    tags, years = scenario.tags, np.asarray(scenario.dates)
    out = np.zeros((len(years), len(tags)), dtype=bool)
    rows = confirmed[(confirmed["kind"] == kind) & (confirmed["name"] == name)]
    index = {t: i for i, t in enumerate(tags)}
    for _, r in rows.iterrows():
        if r["tag"] in index:
            out[(years >= int(r["from_year"])) & (years <= int(r["to_year"])), index[r["tag"]]] = True
    return out


def missing_report(
    scenario: Scenario, kind: str | None = None, name: str | None = None, by_country: bool = False
) -> pd.DataFrame:
    """How much is filled: per formula (default) or per country and kind (`by_country`).

    A cell counts as filled when it has a value or its default was confirmed (`confirm_default`).
    Per country, relations count the pairs where the country is FROM (directed) or a side (double-sided).
    """
    kinds = KINDS if kind is None else (resolve_kind(kind),)
    store = NarratedStore(scenario)
    exist = scenario.existence().to_numpy()  # years x tags
    confirmed = load_confirmed(scenario)
    rows = []
    per_tag = {k: (np.zeros(len(scenario.tags)), np.zeros(len(scenario.tags))) for k in kinds}
    for k in kinds:
        formulas = list_formulas(scenario, k) if name is None else [get_formula(scenario, k, name)]
        for f in formulas:
            conf = _confirmed_matrix(scenario, confirmed, k, f.name)
            total = filled = confirmed_cells = 0
            first_gap = None
            for yi, year in enumerate(scenario.dates):
                alive = exist[yi]
                vals = store.values(k, f.slug, year).to_numpy(dtype=float)
                has = ~np.isnan(vals)
                if k == INTERNAL_GRADES:
                    mask, covered = alive, has | conf[yi]
                else:
                    mask = alive[:, None] & alive[None, :]
                    np.fill_diagonal(mask, False)
                    row_conf = conf[yi][:, None]
                    covered = has | (row_conf if k != RELATIONS_DOUBLESIDED else (row_conf | row_conf.T))
                n_total, n_filled = int(mask.sum()), int((covered & mask).sum())
                if k == RELATIONS_DOUBLESIDED:  # each unordered pair once in the per-formula totals
                    upper = np.triu(mask)
                    n_total, n_filled = int(upper.sum()), int((covered & upper).sum())
                confirmed_cells += n_filled - int((has & (np.triu(mask) if k == RELATIONS_DOUBLESIDED else mask)).sum())
                total += n_total
                filled += n_filled
                if first_gap is None and n_filled < n_total:
                    first_gap = year
                t_all, t_ok = per_tag[k]
                t_all += mask.sum(axis=1) if k != INTERNAL_GRADES else mask
                t_ok += (covered & mask).sum(axis=1) if k != INTERNAL_GRADES else (covered & mask)
            rows.append({
                "kind": k, "name": f.name, "filled": filled, "total": total,
                "percent": round(100 * filled / total, 2) if total else 100.0,
                "confirmed_default": confirmed_cells,
                "first_year_with_gaps": first_gap,
            })
    if not by_country:
        return pd.DataFrame(rows)
    table = pd.DataFrame(index=pd.Index(scenario.tags, name="tag"))
    table["name"] = scenario.tags_table["name"]
    for k, (t_all, t_ok) in per_tag.items():
        table[k] = np.where(t_all > 0, np.round(100 * t_ok / np.maximum(t_all, 1), 1), 100.0)
    table["all"] = table[list(per_tag)].mean(axis=1).round(1)
    return table.sort_values("all")


def effective_values(scenario: Scenario, kind: str, name: str, year: int) -> pd.Series | pd.DataFrame:
    """Values the simulator should use: unfilled cells get the formula default.

    Cells of countries that do not exist in `year` and the relation diagonal stay NaN;
    so do unfilled cells of formulas without a default (they have to be filled).
    """
    kind = resolve_kind(kind)
    formula = get_formula(scenario, kind, name)
    if year not in scenario.dates:
        raise SimulatorError(f"Year {year} is not a scenario date")
    vals = NarratedStore(scenario).values(kind, formula.slug, year).copy()
    alive = scenario.existence([year]).loc[year].to_numpy()
    if kind == INTERNAL_GRADES:
        valid = alive
    else:
        valid = alive[:, None] & alive[None, :]
        np.fill_diagonal(valid, False)
    if formula.default is not None:
        vals = vals.fillna(formula.default)
    return vals.where(valid)
