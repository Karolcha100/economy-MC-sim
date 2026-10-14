"""Task queue for Phase 1.2b: one row per country, task A (country statistics) and B (relations).

Agents mark tasks in the markdown file by hand (see AGENTS/phases/phase-1.2b/instrukcja-wypelniania.md).
Order: reference countries, then the `first` list (e.g. Tier 1), then the rest in tags.csv order.
"""

from __future__ import annotations

from pathlib import Path

from simulator.context import reference_tags
from simulator.io import SimulatorError
from simulator.scenario import Scenario


def write_queue(scenario: Scenario, out: Path, first: str = "") -> Path:
    out = Path(out)
    if out.exists():
        raise SimulatorError(f"{out} exists — the queue holds agents' progress; edit it instead of regenerating")
    first_tags = [t.strip().upper() for t in first.split(",") if t.strip()]
    scenario.check_tags(first_tags)
    refs = reference_tags(scenario)
    order = list(dict.fromkeys(refs + first_tags + scenario.tags))
    names = scenario.tags_table["name"]
    group = {t: "referencyjny" for t in refs} | {t: "Tier 1" for t in first_tags if t not in refs}
    lines = [
        "# Phase 1.2b — kolejka zadań",
        "",
        "Zasady: `instrukcja-wypelniania.md`. Bierzesz zadanie: w kolumnie wpisz `[~] model, RRRR-MM-DD GG:MM`;",
        "kończysz: `[x]` + krótka notka w kolumnie Uwagi (liczba operacji, ostrzeżenia `review`, czego brakuje).",
        "Postęp liczbowo: `python -m simulator --scenario world-1990-2025 missing --by-country`.",
        "",
        "| # | tag | państwo | grupa | A: statystyki | B: relacje | uwagi |",
        "|---|---|---|---|---|---|---|",
    ]
    lines += [f"| {i} | {t} | {names[t]} | {group.get(t, '')} | [ ] | [ ] | |" for i, t in enumerate(order, 1)]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
