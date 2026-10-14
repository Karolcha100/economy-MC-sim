import numpy as np
import pandas as pd
import pytest

from simulator.history import import_dyadic, import_history
from simulator.narrated import Operation, apply_operations, show
from simulator.review import review
from simulator.seed import apply_seeds
from simulator.validate import validate


@pytest.fixture
def seeded(scenario, tmp_path):
    src = tmp_path / "wgi.csv"
    pd.DataFrame({
        "date": range(1990, 1996),
        "POL": [np.nan, 0.5, np.nan, 1.0, np.nan, np.nan],  # inner gap 1992, edges stay empty
        "UKR": [2.0, -1.0, -1.0, -1.0, -1.0, -1.0],         # 1990 value although UKR exists from 1991
        "RUS": [-3.0, -1, -1, -1, -1, -1],                  # below the scale -> clipped to 0
    }).to_csv(src, index=False)
    import_history(scenario, "wgi", src, fmt="wide")
    pop = tmp_path / "pop.csv"
    pd.DataFrame({"date": range(1990, 1996), "POL": [1000.0] * 6}).to_csv(pop, index=False)
    import_history(scenario, "population", pop, fmt="wide")
    net = tmp_path / "net.csv"
    pd.DataFrame({"date": range(1990, 1996), "POL": [2.0, 4, 10, 30, -2, 0]}).to_csv(net, index=False)
    import_history(scenario, "net-migration", net, fmt="wide")
    pairs = tmp_path / "pairs.csv"
    pd.DataFrame({"side_a": ["UKR", "RUS"], "side_b": ["POL", "POL"], "from": [1990, 1993], "to": [1995, 1994],
                  "note": ["", ""]}).to_csv(pairs, index=False)
    import_dyadic(scenario, "borders", pairs, "pair-ranges")
    (scenario.root / "formulas" / "internal-grades.csv").write_text(
        (scenario.root / "formulas" / "internal-grades.csv").read_text()
        + "net migration,float,-100,100,0,Net migration\n"
    )
    (scenario.root / "seeds.csv").write_text(
        "kind,name,source,transform,a,b,note\n"
        "internal-grades,stability,wgi,linear,50,20,W1\n"
        "internal-grades,net migration,net-migration,per-1000-linear,0,5,W4\n"
        "relations-doublesided,in war,borders,pairs-at-least,1,,test\n"
    )
    return scenario


def test_country_seeds_interpolate_inner_gaps_and_respect_existence(seeded):
    report = apply_seeds(seeded).set_index("name")
    s = show(seeded, "grade", "stability", "POL,UKR,RUS", "1990-1995")
    assert (s.at[1991, "POL"], s.at[1993, "POL"]) == (60, 70)
    assert s.at[1992, "POL"] == pytest.approx(65)            # interpolated
    assert np.isnan(s.at[1990, "POL"]) and np.isnan(s.at[1994, "POL"])  # edges stay empty
    assert np.isnan(s.at[1990, "UKR"]) and s.at[1991, "UKR"] == 30       # UKR exists from 1991
    assert s.at[1990, "RUS"] == 0                            # clipped
    m = show(seeded, "grade", "net migration", "POL", "1990-1995")["POL"].tolist()
    assert m == [10, 20, 50, 100, -10, 0]                    # 5 x per 1000, clipped at 100
    assert report.at["in war", "written"] == 5 + 2           # UKR 1991-1995 (exists from 1991) + RUS 1993-1994
    assert validate(seeded) == []


def test_seeds_never_overwrite_and_log_author(seeded):
    apply_operations(seeded, [Operation(kind="grade", name="stability", targets="POL", years="1991",
                                        curve="constant", start=20, rationale="LLM correction")], author="llm")
    report = apply_seeds(seeded).set_index("name")
    assert show(seeded, "grade", "stability", "POL", "1991")["POL"].tolist() == [20]
    assert report.at["stability", "skipped (filled)"] == 1
    again = apply_seeds(seeded).set_index("name")
    assert again["written"].sum() == 0                       # re-run changes nothing
    log = pd.read_csv(seeded.narrated_dir / "changelog.csv", keep_default_na=False)
    assert set(log[log["operation"] == "seed"]["author"]) == {"seed:wgi", "seed:net-migration", "seed:borders"}


def test_review_flags_deviation_from_seed(seeded):
    apply_seeds(seeded)
    apply_operations(seeded, [Operation(kind="grade", name="stability", targets="POL", years="1993",
                                        curve="constant", start=40, rationale="r")], author="llm")
    # 1993 was seeded (70) before the LLM overwrote it with 40
    w = review(seeded)
    dev = w[w["check"] == "seed-deviation"]
    assert dev[["target", "year"]].values.tolist() == [["POL", 1993]]


def test_pairs_between_and_safe_reset(seeded, tmp_path):
    from simulator.io import SimulatorError
    from simulator.seed import reset_seeded

    levels = tmp_path / "levels.csv"
    pd.DataFrame({"side_a": ["POL", "DEU"], "side_b": ["RUS", "RUS"], "from": [1990, 1990], "to": [1990, 1990],
                  "note": ["", ""]}).to_csv(levels, index=False)
    import_dyadic(seeded, "levels", levels, "pair-ranges")  # all value 1
    (seeded.root / "seeds.csv").write_text(
        "kind,name,source,transform,a,b,note\n"
        "relations-doublesided,in war,levels,pairs-between,2,2,only level 2\n"
    )
    assert apply_seeds(seeded).set_index("name").at["in war", "written"] == 0
    (seeded.root / "seeds.csv").write_text(
        "kind,name,source,transform,a,b,note\n"
        "relations-doublesided,in war,levels,pairs-between,1,1,level 1\n"
    )
    assert apply_seeds(seeded).set_index("name").at["in war", "written"] == 2
    assert reset_seeded(seeded, "doublesided", "in war") == 4  # 2 pairs x 2 cells
    assert show(seeded, "doublesided", "in war", "POL:RUS", "1990")["POL:RUS"].isna().all()
    apply_operations(seeded, [Operation(kind="doublesided", name="in war", targets="POL:RUS", years="1991",
                                        curve="constant", start=1, rationale="manual")], author="llm")
    with pytest.raises(SimulatorError, match="non-seed"):
        reset_seeded(seeded, "doublesided", "in war")
