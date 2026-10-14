"""Automatic comparison of narrated data across all countries (decision A31, thread T016).

Read-only: computes, never writes scenario data. Three checks:
  1. agreement with real indicators — per year, the rank correlation between a narrated statistic
     and its reference across countries (rules in `<scenario>/audit.csv`), plus the countries whose
     position differs most;
  2. flat lines — a country with the same value in every filled year of a statistic (copy-paste fill);
  3. crowding — one value shared by most countries in a year (default-like guessing).
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from simulator.formulas import get_formula, list_formulas
from simulator.history import load_history
from simulator.io import SimulatorError, read_csv
from simulator.narrated import effective_values
from simulator.scenario import Scenario
from simulator.store import NarratedStore
from simulator.templates import INTERNAL_GRADES, RELATIONS_DIRECTED

AUDIT_COLUMNS = ["statistic", "reference", "sign", "note"]
MIN_COUNTRIES = 10        # a year needs this many countries with both values to count
OUTLIER_GAP = 0.4         # |percentile in narrated - percentile in reference| above this is an outlier
CROWDING_SHARE = 0.5      # one value shared by more than half of the countries in a year


def load_rules(scenario: Scenario) -> pd.DataFrame:
    path = scenario.root / "audit.csv"
    if not path.exists():
        raise SimulatorError(f"No audit rules: {path}")
    rules = read_csv(path, dtype=str, keep_default_na=False)
    missing = set(AUDIT_COLUMNS) - set(rules.columns)
    if missing:
        raise SimulatorError(f"{path}: missing columns {sorted(missing)}")
    return rules


def statistic_frame(scenario: Scenario, spec: str) -> pd.DataFrame:
    """years x tags for 'grade:<name>' or 'directed-out-mean:<name>' (mean of FROM's row, defaults included)."""
    kind, _, name = spec.partition(":")
    if kind == "grade":
        f = get_formula(scenario, INTERNAL_GRADES, name)
        store = NarratedStore(scenario)
        return pd.DataFrame({y: store.values(INTERNAL_GRADES, f.slug, y) for y in scenario.dates}).T
    if kind == "directed-out-mean":
        get_formula(scenario, RELATIONS_DIRECTED, name)
        return pd.DataFrame({y: effective_values(scenario, RELATIONS_DIRECTED, name, y).mean(axis=1)
                             for y in scenario.dates}).T
    raise SimulatorError(f"Unknown statistic spec {spec!r}; use grade:<name> or directed-out-mean:<name>")


def reference_frame(scenario: Scenario, spec: str) -> pd.DataFrame:
    """years x tags for a history statistic or 'gdp-per-capita'."""
    if spec == "gdp-per-capita":
        return load_history(scenario, "gdp-current-usd") / load_history(scenario, "population")
    return load_history(scenario, spec)


def _percentiles(row: pd.Series) -> pd.Series:
    return (row.rank() - 1) / max(row.count() - 1, 1)


def compare(stat: pd.DataFrame, ref: pd.DataFrame, sign: int) -> tuple[dict, pd.DataFrame]:
    """Rank agreement per year and per-country percentile gaps."""
    ref = ref.reindex(index=stat.index, columns=stat.columns) * sign
    corrs, gaps = [], []
    for year in stat.index:
        both = stat.loc[year].notna() & ref.loc[year].notna()
        if both.sum() < MIN_COUNTRIES:
            continue
        if stat.loc[year][both].nunique() < 2 or ref.loc[year][both].nunique() < 2:
            continue  # e.g. a relation still at its default everywhere: no information to compare
        a, b = _percentiles(stat.loc[year][both]), _percentiles(ref.loc[year][both])
        corrs.append(float(np.corrcoef(a, b)[0, 1]))
        gaps.append((a - b).rename(year))
    summary = {"years": len(corrs), "rank_corr": round(float(np.mean(corrs)), 2) if corrs else None}
    gap = pd.concat(gaps, axis=1).mean(axis=1) if gaps else pd.Series(dtype=float)
    return summary, gap


def flat_lines(scenario: Scenario, min_years: int = 10) -> pd.DataFrame:
    """Countries whose continuous statistic never changes over >= min_years filled years."""
    store = NarratedStore(scenario)
    rows = []
    for f in list_formulas(scenario, INTERNAL_GRADES):
        if f.type != "float":
            continue
        frame = pd.DataFrame({y: store.values(INTERNAL_GRADES, f.slug, y) for y in scenario.dates}).T
        counts, spread = frame.count(), frame.max() - frame.min()
        for tag in frame.columns[(counts >= min_years) & (spread == 0)]:
            rows.append({"statistic": f.name, "tag": tag, "years": int(counts[tag]), "value": frame[tag].dropna().iloc[0]})
    return pd.DataFrame(rows, columns=["statistic", "tag", "years", "value"])


def crowding(scenario: Scenario) -> pd.DataFrame:
    """Years in which one value is shared by more than CROWDING_SHARE of the countries filled."""
    store = NarratedStore(scenario)
    rows = []
    for f in list_formulas(scenario, INTERNAL_GRADES):
        if f.type != "float":
            continue
        for y in scenario.dates:
            vals = store.values(INTERNAL_GRADES, f.slug, y).dropna()
            if len(vals) < MIN_COUNTRIES:
                continue
            top = vals.round(1).value_counts()
            if top.iloc[0] / len(vals) > CROWDING_SHARE:
                rows.append({"statistic": f.name, "year": y, "value": top.index[0],
                             "share": round(top.iloc[0] / len(vals), 2), "countries": len(vals)})
    return pd.DataFrame(rows, columns=["statistic", "year", "value", "share", "countries"])


def run_audit(scenario: Scenario) -> dict:
    names = scenario.tags_table["name"]
    summary, outliers = [], []
    for _, r in load_rules(scenario).iterrows():
        stat = statistic_frame(scenario, r["statistic"])
        ref = reference_frame(scenario, r["reference"])
        info, gap = compare(stat, ref, int(r["sign"]))
        flagged = gap[gap.abs() > OUTLIER_GAP].sort_values(key=abs, ascending=False)
        summary.append({"statistic": r["statistic"], "reference": r["reference"], "sign": int(r["sign"]),
                        **info, "outliers": len(flagged)})
        outliers += [{"statistic": r["statistic"], "reference": r["reference"], "tag": t, "name": names[t],
                      "gap": round(float(g), 2), "direction": "wyżej niż wskaźnik" if g > 0 else "niżej niż wskaźnik"}
                     for t, g in flagged.items()]
    return {"summary": pd.DataFrame(summary), "outliers": pd.DataFrame(outliers),
            "flat": flat_lines(scenario), "crowding": crowding(scenario)}


def write_report(scenario: Scenario, result: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now()
    path = out_dir / f"audit-{stamp:%Y-%m-%d-%H%M}.md"

    def table(df: pd.DataFrame, limit: int = 60) -> str:
        if df.empty:
            return "_brak_\n"
        df = df.head(limit)
        head = "| " + " | ".join(df.columns) + " |\n|" + "---|" * len(df.columns) + "\n"
        return head + "".join("| " + " | ".join(str(v) for v in row) + " |\n" for row in df.itertuples(index=False))

    text = [
        f"# Audyt danych opisowych — {stamp:%Y-%m-%d %H:%M}",
        "",
        "Automatyczne porównanie wszystkich krajów (decyzja A31). Tylko obliczenia, dane bez zmian.",
        "Reguły: `simulator/scenarios/<scenariusz>/audit.csv`. Komenda: `python -m simulator --scenario "
        f"{scenario.name} audit`.",
        "",
        "## 1. Zgodność ze wskaźnikami",
        "",
        "`rank_corr`: średnia (po latach) zgodność kolejności krajów, od −1 do 1 (1 = ta sama kolejność). "
        f"`outliers`: kraje, których średnia pozycja różni się o więcej niż {OUTLIER_GAP:.0%} skali.",
        "",
        table(result["summary"]),
        "## 2. Kraje najbardziej odstające od wskaźników",
        "",
        table(result["outliers"]),
        "## 3. Płaskie linie (ta sama wartość we wszystkich latach)",
        "",
        table(result["flat"]),
        f"## 4. Zatłoczenie (jedna wartość u ponad {CROWDING_SHARE:.0%} krajów w roku)",
        "",
        table(result["crowding"]),
    ]
    path.write_text("\n".join(text), encoding="utf-8")
    return path
