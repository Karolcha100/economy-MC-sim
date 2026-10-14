"""Remove countries from a scenario (decision A39 / K7, Phase 1.2b): every file that lists tags.

Touches tags.csv, groups.csv, reference-countries.csv, history/<stat>.csv (columns),
history/dyadic/*.csv (rows with the tag on either side), narrated/<year>/** (rows; relation
matrices also columns) and narrated/confirmed-defaults.csv. Values are copied as text, so nothing
else is reformatted. history/fill-log.csv and narrated/changelog.csv are logs and keep their rows.
Re-importing a source later is safe: import_history ignores columns that are not in tags.csv.
"""

from __future__ import annotations

from pathlib import Path

from simulator.history import RESERVED_FILES
from simulator.io import SimulatorError, read_csv, write_csv
from simulator.scenario import Scenario
from simulator.store import append_changelog


def drop_tags(scenario: Scenario, tags: str | list[str], author: str, note: str = "") -> dict[str, int]:
    """Delete `tags` everywhere in the scenario; returns how many files changed per area."""
    if not author:
        raise SimulatorError("author is required")
    drop = [t.strip().upper() for t in (tags.split(",") if isinstance(tags, str) else tags) if t.strip()]
    if not drop:
        raise SimulatorError("no tags given")
    scenario.check_tags(drop)
    gone = set(drop)
    changed = {"tables": 0, "history": 0, "dyadic": 0, "narrated": 0, "confirmed": 0}

    def rewrite(path: Path, frame, area: str, index: bool) -> None:
        write_csv(frame, path, index=index)
        changed[area] += 1

    with scenario.lock():
        for name in ("tags.csv", "groups.csv", "reference-countries.csv"):
            path = scenario.root / name
            if path.exists():
                df = read_csv(path, dtype=str, keep_default_na=False)
                if df["tag"].isin(gone).any():
                    rewrite(path, df[~df["tag"].isin(gone)], "tables", index=False)
        for path in sorted(scenario.history_dir.glob("*.csv")):
            if path.name in RESERVED_FILES:
                continue
            df = read_csv(path, index_col=0, dtype=str, keep_default_na=False)
            cols = [c for c in df.columns if c in gone]
            if cols:
                rewrite(path, df.drop(columns=cols), "history", index=True)
        for path in sorted((scenario.history_dir / "dyadic").glob("*.csv")):
            df = read_csv(path, dtype=str, keep_default_na=False)
            mask = df["side_a"].isin(gone) | df["side_b"].isin(gone)
            if mask.any():
                rewrite(path, df[~mask], "dyadic", index=False)
        if scenario.narrated_dir.exists():
            for ydir in sorted(p for p in scenario.narrated_dir.iterdir() if p.is_dir()):
                for path in sorted(ydir.rglob("*.csv")):
                    df = read_csv(path, index_col=0, dtype=str, keep_default_na=False)
                    rows = [r for r in df.index if r in gone]
                    cols = [c for c in df.columns if c in gone] if path.parent != ydir else []
                    if rows or cols:
                        rewrite(path, df.drop(index=rows, columns=cols), "narrated", index=True)
            path = scenario.narrated_dir / "confirmed-defaults.csv"
            if path.exists():
                df = read_csv(path, dtype=str, keep_default_na=False)
                if df["tag"].isin(gone).any():
                    rewrite(path, df[~df["tag"].isin(gone)], "confirmed", index=False)
        append_changelog(scenario, [{"author": author, "operation": "drop-tags", "targets": ";".join(drop),
                                     "rationale": note}])
    for cached in ("tags_table", "groups_table"):   # cached_property: re-read on next use
        scenario.__dict__.pop(cached, None)
    return changed
