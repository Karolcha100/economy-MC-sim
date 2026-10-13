"""Automatic review of narrated data: warnings only, never errors (see AGENTS/Conversations/phase-1.md, G1).

Checks: large year-to-year jumps of continuous statistics and changelog entries without a rationale.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from simulator.formulas import get_formula, list_formulas
from simulator.scenario import Scenario
from simulator.store import NarratedStore
from simulator.templates import INTERNAL_GRADES, KINDS, RELATIONS_DOUBLESIDED, resolve_kind

DEFAULT_JUMP = 0.25  # share of the formula range
COLUMNS = ["check", "kind", "name", "target", "year", "message"]


def _jumps(scenario: Scenario, store: NarratedStore, f, threshold: float) -> list[dict]:
    limit = threshold * (f.valmax - f.valmin)
    rows = []
    prev = None
    for year in scenario.dates:
        cur = store.values(f.kind, f.slug, year)
        if prev is not None:
            delta = (cur - prev).abs()
            arr = delta.to_numpy(dtype=float)
            if f.kind == RELATIONS_DOUBLESIDED:
                arr = np.triu(arr)
            hits = np.argwhere(np.nan_to_num(arr) > limit)
            for hit in hits:
                if f.kind == INTERNAL_GRADES:
                    target = cur.index[hit[0]]
                    before, after = prev.iloc[hit[0]], cur.iloc[hit[0]]
                else:
                    target = f"{cur.index[hit[0]]}:{cur.columns[hit[1]]}"
                    before, after = prev.iat[hit[0], hit[1]], cur.iat[hit[0], hit[1]]
                rows.append({"check": "jump", "kind": f.kind, "name": f.name, "target": target, "year": year,
                             "message": f"{before:g} -> {after:g} (more than {limit:g} in one year)"})
        prev = cur
    return rows


def review(
    scenario: Scenario, kind: str | None = None, name: str | None = None, jump: float = DEFAULT_JUMP
) -> pd.DataFrame:
    store = NarratedStore(scenario)
    rows: list[dict] = []
    kinds = KINDS if kind is None else (resolve_kind(kind),)
    for k in kinds:
        formulas = list_formulas(scenario, k) if name is None else [get_formula(scenario, k, name)]
        for f in formulas:
            if f.type == "float":
                rows += _jumps(scenario, store, f, jump)

    log_path = scenario.narrated_dir / "changelog.csv"
    if log_path.exists():
        log = pd.read_csv(log_path, keep_default_na=False)
        for _, r in log[(log["operation"] == "set") & (log["rationale"].str.strip() == "")].iterrows():
            rows.append({"check": "no-rationale", "kind": r["kind"], "name": r["name"], "target": r["targets"],
                         "year": r["years"], "message": f"set by {r['author']} at {r['timestamp']} without rationale"})
    return pd.DataFrame(rows, columns=COLUMNS)
