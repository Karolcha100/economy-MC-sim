"""World map of one statistic for the reference countries (calibration anchors), with a year slider.

Reference countries are listed in `<scenario>/reference-countries.csv` (tag, reason); edit that
file to choose others. For relations pass `focus`: the map shows focus -> country values.
Output is a standalone HTML file that also works offline: the world shapes
(`simulator/common/geo/world_110m.json`, from https://cdn.plot.ly/un/) are embedded in it.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from simulator.context import reference_tags
from simulator.formulas import get_formula
from simulator.io import SimulatorError
from simulator.narrated import parse_years
from simulator.scenario import Scenario
from simulator.store import NarratedStore
from simulator.templates import INTERNAL_GRADES, resolve_kind

NOT_ISO3 = {"XKX"}  # tags plotly cannot place on the map
TOPOJSON = Path(__file__).parent / "common" / "geo" / "world_110m.json"


def build_map(
    scenario: Scenario,
    kind: str,
    name: str,
    years: str | None = None,
    focus: str | None = None,
    all_countries: bool = False,
):
    try:
        import plotly.graph_objects as go
    except ImportError:
        raise SimulatorError("plotly is needed for maps: pip install -e '.[viz]'") from None

    kind = resolve_kind(kind)
    formula = get_formula(scenario, kind, name)
    if kind != INTERNAL_GRADES:
        if not focus:
            raise SimulatorError("relations need --focus TAG (the map shows FOCUS -> country)")
        focus = focus.upper()
        scenario.check_tags([focus])
    yrs = scenario.dates if years is None else scenario.years_between(*parse_years(years))

    tags = scenario.tags if all_countries else reference_tags(scenario)
    if not tags:
        raise SimulatorError(f"No reference countries: fill {scenario.root / 'reference-countries.csv'}")
    tags = [t for t in tags if t not in NOT_ISO3 and t != focus]
    names = scenario.tags_table["name"]
    reasons = {}
    ref_path = scenario.root / "reference-countries.csv"
    if ref_path.exists():
        reasons = pd.read_csv(ref_path, dtype=str).set_index("tag")["reason"].to_dict()

    store = NarratedStore(scenario)
    alive = scenario.existence(yrs)

    def values(year: int) -> list[float]:
        v = store.values(kind, formula.slug, year)
        out = [v[t] if kind == INTERNAL_GRADES else v.at[focus, t] for t in tags]
        return [x if alive.at[year, t] else math.nan for x, t in zip(out, tags)]

    def label(v: float) -> str:
        return "not filled" if math.isnan(v) else f"{v:g}"

    def traces(year: int):
        vals = values(year)
        hover = [
            f"<b>{names[t]}</b> ({t})<br>year: {year}<br>{formula.name}: {label(v)}<br><i>{reasons.get(t, '')}</i>"
            for t, v in zip(tags, vals)
        ]
        choropleth = go.Choropleth(
            locations=tags, z=[None if math.isnan(v) else v for v in vals], zmin=formula.valmin, zmax=formula.valmax,
            colorscale="RdYlGn" if formula.valmin < 0 else "Viridis", colorbar={"title": formula.name},
            text=hover, hoverinfo="text", marker_line_color="white",
        )
        labels = go.Scattergeo(
            locations=tags, locationmode="ISO-3", mode="text", hoverinfo="skip",
            text=[f"{t} {label(v) if not math.isnan(v) else '–'}" for t, v in zip(tags, vals)],
            textfont={"size": 10, "color": "black"},
        )
        return [choropleth, labels]

    subject = formula.name if kind == INTERNAL_GRADES else f"{focus} → country: {formula.name}"
    base = go.Choropleth(  # grey shapes so unfilled reference countries stay visible
        locations=tags, z=[0] * len(tags), colorscale=[[0, "#d9d9d9"], [1, "#d9d9d9"]],
        showscale=False, hoverinfo="skip", marker_line_color="white",
    )
    fig = go.Figure(
        data=[base, *traces(yrs[0])],
        frames=[go.Frame(name=str(y), data=traces(y), traces=[1, 2],
                         layout={"title": {"text": f"{subject} — {y}"}}) for y in yrs],
    )
    fig.update_layout(
        title={"text": f"{subject} — {yrs[0]}"},
        geo={"projection": {"type": "natural earth", "rotation": {"lon": 20}}, "showcountries": True,
             "countrycolor": "white"},  # centred on Europe (Poland-Russia model)
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        sliders=[{
            "currentvalue": {"prefix": "year: "},
            "steps": [{"label": str(y), "method": "animate",
                       "args": [[str(y)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}]}
                      for y in yrs],
        }],
        updatemenus=[{
            "type": "buttons", "showactive": False, "x": 0.02, "y": 0.02,
            "buttons": [{"label": "▶", "method": "animate",
                         "args": [None, {"frame": {"duration": 400, "redraw": True}, "fromcurrent": True}]}],
        }],
    )
    return fig


def write_map(fig, path: Path) -> Path:
    """Write standalone HTML; plotly reads window.PlotlyGeoAssets before fetching shapes from its CDN."""
    html = fig.to_html(include_plotlyjs=True, full_html=True, auto_play=False)
    if TOPOJSON.exists():
        assets = f"<script>window.PlotlyGeoAssets={{topojson:{{world_110m:{TOPOJSON.read_text()}}}}};</script>"
        html = html.replace("<head>", "<head>" + assets, 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path
