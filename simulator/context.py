"""Compact text context for an LLM agent about to fill narrated data.

For a country: existence, group memberships, history statistics, every internal grade
(meaning, current values) and the values of the reference countries as calibration anchors.
For a pair: the same for every directed (both directions) and double-sided relation.
"""

from __future__ import annotations

import math

import pandas as pd

from simulator.formulas import Formula, list_formulas
from simulator.history import compress_years, load_dyadic, load_fill_log, load_history, load_metadata
from simulator.io import read_csv
from simulator.narrated import PAIR_SEPARATOR
from simulator.scenario import Scenario
from simulator.store import NarratedStore
from simulator.templates import INTERNAL_GRADES, RELATIONS_DIRECTED, RELATIONS_DOUBLESIDED

HISTORY_STEP = 5


def reference_tags(scenario: Scenario) -> list[str]:
    path = scenario.root / "reference-countries.csv"
    if not path.exists():
        return []
    return [t for t in read_csv(path, dtype=str)["tag"] if t in scenario.tags]


def _fmt(v: float) -> str:
    if math.isnan(v):
        return "-"
    if abs(v) >= 1e9:
        return f"{v / 1e9:,.1f}bn"
    return f"{v:g}"


def compress_series(values: dict[int, float]) -> str:
    """Runs of equal values -> '1990-1994: 10; 1995: 12'. Unfilled years are left out."""
    runs: list[tuple[int, int, float]] = []
    for year, v in values.items():
        if math.isnan(v):
            continue
        if runs and runs[-1][2] == v and runs[-1][1] == year - 1:
            runs[-1] = (runs[-1][0], year, v)
        else:
            runs.append((year, year, v))
    if not runs:
        return "not filled"
    return "; ".join(f"{a}: {_fmt(v)}" if a == b else f"{a}-{b}: {_fmt(v)}" for a, b, v in runs)


def _formula_header(f: Formula) -> str:
    default = "none (must be filled)" if f.default is None else _fmt(f.default)
    return f"### {f.name} ({f.type} {_fmt(f.valmin)}..{_fmt(f.valmax)}, default {default})\n{f.description}"


def _country_header(scenario: Scenario, tag: str) -> list[str]:
    row = scenario.tags_table.loc[tag]
    lo = "" if pd.isna(row["exists_from"]) else int(row["exists_from"])
    hi = "" if pd.isna(row["exists_to"]) else int(row["exists_to"])
    exists = f"{lo or scenario.dates[0]}-{hi or scenario.dates[-1]}"
    memberships = []
    for group in scenario.groups:
        m = scenario.membership(group, scenario.dates)[tag]
        if m.any():
            memberships.append(f"{group} {compress_years(m.index[m].tolist())}")
    return [f"## {tag} — {row['name']}", f"exists: {exists}; groups: {', '.join(memberships) or 'none'}"]


def _history_lines(scenario: Scenario, tag: str) -> list[str]:
    meta = load_metadata(scenario).set_index("name")
    log = load_fill_log(scenario)
    years = scenario.dates[::HISTORY_STEP] + ([scenario.dates[-1]] if (len(scenario.dates) - 1) % HISTORY_STEP else [])
    lines = []
    for name in meta.index[meta["shape"] == "country"]:
        series = load_history(scenario, name)[tag]
        estimated = set(log[(log["name"] == name) & (log["tag"] == tag)]["year"].astype(int))
        cells = [f"{y}: {_fmt(series[y])}{'*' if y in estimated else ''}" for y in years]
        lines.append(f"- {name} [{meta.at[name, 'unit']}]: " + ", ".join(cells))
    if any("*" in line for line in lines):
        lines.append("  (* = estimated, see history/fill-log.csv)")
    return lines


def _anchors(store: NarratedStore, f: Formula, refs: list[str], exclude: set[str]) -> str:
    years = store.scenario.dates[::HISTORY_STEP]
    parts = []
    for ref in refs:
        if ref in exclude:
            continue
        vals = [store.values(f.kind, f.slug, y)[ref] for y in years]
        if any(not math.isnan(v) for v in vals):
            parts.append(f"{ref} " + "/".join(_fmt(v) for v in vals))
    if not parts:
        return "anchors: none filled yet"
    return f"anchors ({'/'.join(map(str, years))}): " + "; ".join(parts)


def country_context(scenario: Scenario, tag: str) -> str:
    scenario.check_tags([tag])
    store = NarratedStore(scenario)
    refs = reference_tags(scenario)
    lines = _country_header(scenario, tag) + ["", "History:"] + _history_lines(scenario, tag) + ["", "Internal grades:"]
    for f in list_formulas(scenario, INTERNAL_GRADES):
        values = {y: store.values(INTERNAL_GRADES, f.slug, y)[tag] for y in scenario.dates}
        lines += [_formula_header(f), f"current: {compress_series(values)}", _anchors(store, f, refs, {tag}), ""]
    return "\n".join(lines)


def pair_context(scenario: Scenario, a: str, b: str) -> str:
    scenario.check_tags([a, b])
    store = NarratedStore(scenario)
    lines = _country_header(scenario, a) + _country_header(scenario, b) + [""]
    meta = load_metadata(scenario).set_index("name")
    dyadic = meta.index[meta["shape"] == "dyad-symmetric"]
    if len(dyadic):
        lines.append("History (pairs, real data):")
        x, y = sorted((a, b))
        for name in dyadic:
            d = load_dyadic(scenario, name)
            d = d[(d["side_a"] == x) & (d["side_b"] == y)]
            values = {yr: float("nan") for yr in scenario.dates} | dict(zip(d["date"], d["value"]))
            lines.append(f"- {name} [{meta.at[name, 'unit']}]: {compress_series(values)}")
        lines.append("")
    for kind in (RELATIONS_DIRECTED, RELATIONS_DOUBLESIDED):
        lines.append(f"Relations ({kind}):")
        for f in list_formulas(scenario, kind):
            lines.append(_formula_header(f))
            directions = [(a, b), (b, a)] if kind == RELATIONS_DIRECTED else [(a, b)]
            for x, y in directions:
                values = {yr: store.values(kind, f.slug, yr).at[x, y] for yr in scenario.dates}
                arrow = "->" if kind == RELATIONS_DIRECTED else "<->"
                lines.append(f"{x}{arrow}{y}: {compress_series(values)}")
            lines.append("")
    return "\n".join(lines)


def context(scenario: Scenario, target: str) -> str:
    target = target.strip().upper()
    if PAIR_SEPARATOR in target:
        a, b = target.split(PAIR_SEPARATOR, 1)
        return pair_context(scenario, a, b)
    return country_context(scenario, target)
