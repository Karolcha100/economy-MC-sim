import json

import numpy as np
import pandas as pd
import pytest

from simulator.context import compress_series, context
from simulator.history import fill_gaps, find_gaps, import_history, load_fill_log, load_history
from simulator.io import SimulatorError
from simulator.narrated import Operation, apply_operations, show
from simulator.review import review
from simulator.validate import validate


@pytest.fixture
def grouped(scenario):
    pd.DataFrame({
        "group": ["BLOC", "BLOC", "BLOC"],
        "tag": ["POL", "DEU", "UKR"],
        "from": [1992, None, None],
        "to": [None, 1993, None],
        "note": ["", "", ""],
    }).to_csv(scenario.root / "groups.csv", index=False)
    return scenario


def test_group_targets_follow_membership_and_existence(grouped):
    res = apply_operations(grouped, [Operation(kind="directed", name="diplomatic relation towards",
                                               targets="@BLOC:RUS", years="1990-1995", curve="constant",
                                               start=50)], author="t")
    df = show(grouped, "directed", "diplomatic relation towards", "POL:RUS,DEU:RUS,UKR:RUS", "1990-1995")
    assert df["POL:RUS"].notna().tolist() == [False, False, True, True, True, True]  # member from 1992
    assert df["DEU:RUS"].notna().tolist() == [True, True, True, True, False, False]  # member until 1993
    assert df["UKR:RUS"].notna().tolist() == [False, True, True, True, True, True]  # exists from 1991
    assert res[0].written == 4 + 4 + 5
    assert validate(grouped) == []


def test_wildcard_and_group_self_pairs_are_skipped(grouped):
    apply_operations(grouped, [Operation(kind="doublesided", name="in war", targets="@BLOC:@BLOC",
                                         years="1992-1993", curve="constant", start=1)], author="t")
    m = pd.read_csv(grouped.year_dir(1992) / "relations-doublesided" / "in-war.csv", index_col="tag")
    assert m.loc["POL", "DEU"] == m.loc["DEU", "UKR"] == 1
    assert np.isnan(m.loc["POL", "POL"])
    res = apply_operations(grouped, [Operation(kind="grade", name="war exhaustion", targets="*",
                                               years="1990", curve="constant", start=3)], author="t")
    assert res[0].written == 3  # UKR does not exist in 1990
    with pytest.raises(SimulatorError, match="not allowed with group"):
        apply_operations(grouped, [Operation(kind="grade", name="war exhaustion", targets="@BLOC",
                                             years="1992-1993", start="current", end=5)], author="t")
    with pytest.raises(SimulatorError, match="Unknown group"):
        apply_operations(grouped, [Operation(kind="grade", name="stability", targets="@NOPE",
                                             years="1992", curve="constant", start=5)], author="t")


@pytest.fixture
def gdp(scenario, tmp_path):
    src = tmp_path / "gdp.csv"
    pd.DataFrame({
        "date": range(1990, 1996),
        "POL": [10, np.nan, 40, 80, 160, 320],   # inner gap -> log-linear 20
        "RUS": [np.nan, np.nan, 100, 110, 121, np.nan],  # edge gaps
        "UKR": [5, np.nan, np.nan, 8, 9, 10],    # 1990 value although UKR exists from 1991
        "DEU": [np.nan] * 6,
    }).to_csv(src, index=False)
    import_history(scenario, "gdp", src, fmt="wide")
    return scenario


def test_gap_detection_respects_existence(gdp):
    gaps = find_gaps(gdp, "gdp").set_index("tag")
    assert gaps.loc["UKR", "years"] == "1991-1992"
    assert gaps.loc["RUS", "years"] == "1990-1991,1995"
    assert gaps.loc["DEU", "missing"] == 6


def test_fill_source_then_interpolate_then_extrapolate(gdp, tmp_path):
    imf = tmp_path / "imf.json"
    imf.write_text(json.dumps({"values": {"NGDPD": {"DEU": {"1993": 0.5}}, "": None}}))
    rows = fill_gaps(gdp, "gdp", "source", imf, "imf-datamapper", source_scale=100, author="t")
    assert rows[["tag", "year", "value"]].values.tolist() == [["DEU", 1993, 50.0]]

    fill_gaps(gdp, "gdp", "interpolate", author="t")
    h = load_history(gdp, "gdp")
    assert h.at[1991, "POL"] == pytest.approx(20)  # log-linear between 10 and 40


def test_interpolation_ignores_years_before_existence(gdp):
    fill_gaps(gdp, "gdp", "interpolate", author="t")
    h = load_history(gdp, "gdp")
    assert np.isnan(h.at[1991, "UKR"])
    rows = fill_gaps(gdp, "gdp", "extrapolate", window=2, author="t")
    h = load_history(gdp, "gdp")
    assert h.at[1995, "RUS"] == pytest.approx(133.1)  # +10% a year
    assert h.at[1991, "RUS"] == pytest.approx(100 / 1.1)
    assert h.at[1990, "UKR"] == 5  # existing values are never touched
    assert set(rows["method"]) == {"extrapolate"}
    assert len(load_fill_log(gdp)) == len(rows) + 1  # + POL 1991 from interpolation
    assert find_gaps(gdp, "gdp")["tag"].tolist() == ["DEU"]  # nothing to extrapolate from


def test_reimport_clears_fill_log(gdp, tmp_path):
    fill_gaps(gdp, "gdp", "interpolate", author="t")
    pd.DataFrame({"date": range(1990, 1996), "POL": range(6)}).to_csv(tmp_path / "x.csv", index=False)
    import_history(gdp, "gdp", tmp_path / "x.csv", fmt="wide")
    assert load_fill_log(gdp).empty


def test_context_and_compress(scenario):
    assert compress_series({1990: 1.0, 1991: 1.0, 1992: np.nan, 1993: 2.0}) == "1990-1991: 1; 1993: 2"
    apply_operations(scenario, [Operation(kind="grade", name="stability", targets="POL", years="1990-1991",
                                          curve="constant", start=60)], author="t")
    text = context(scenario, "pol")
    assert "## POL — Poland" in text and "1990-1991: 60" in text and "Stability 0-100" in text
    assert "POL->RUS: not filled" in context(scenario, "POL:RUS")


def test_review_flags_jumps_and_missing_rationale(scenario):
    apply_operations(scenario, [Operation(kind="grade", name="stability", targets="POL", years="1990-1991",
                                          curve="manual", values=[10, 90])], author="t")
    w = review(scenario)
    assert set(w["check"]) == {"jump", "no-rationale"}
    assert w[w["check"] == "jump"].iloc[0]["target"] == "POL"


def test_reference_map(scenario):
    pytest.importorskip("plotly")
    from simulator.reference_map import build_map

    pd.DataFrame({"tag": ["POL", "RUS"], "reason": ["a", "b"]}).to_csv(
        scenario.root / "reference-countries.csv", index=False)
    apply_operations(scenario, [Operation(kind="grade", name="stability", targets="POL", years="1990-1995",
                                          start=10, end=60, rationale="r")], author="t")
    fig = build_map(scenario, "grade", "stability")
    assert len(fig.frames) == 6
    assert list(fig.frames[-1].data[0].z) == [60, None]
    with pytest.raises(SimulatorError, match="focus"):
        build_map(scenario, "directed", "diplomatic relation towards")
