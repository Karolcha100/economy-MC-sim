import json

import numpy as np
import pandas as pd
import pytest

from simulator.cli import main
from simulator.io import SimulatorError
from simulator.narrated import Operation, apply_operations, missing_report, show
from simulator.validate import validate


def op(**kw) -> Operation:
    return Operation(**{"kind": "grade", "name": "stability", "targets": "POL", "years": "1990-1994", **kw})


def test_internal_grade_linear_is_written_to_yearly_files(scenario):
    apply_operations(scenario, [op(start=10, end=50)], author="test")
    df = show(scenario, "internal-grades", "stability", "POL,RUS", "1990-1995")
    assert df["POL"].tolist()[:5] == [10, 20, 30, 40, 50]
    assert df["POL"].isna().tolist()[5]
    assert df["RUS"].isna().all()
    stored = pd.read_csv(scenario.year_dir(1992) / "internal-grades.csv", index_col="tag")
    assert stored.loc["POL", "stability"] == 30
    assert validate(scenario) == []


def test_slug_and_name_both_resolve(scenario):
    apply_operations(scenario, [op(name="war-exhaustion", curve="constant", start=5)], author="t")
    assert show(scenario, "grade", "war exhaustion", "POL", "1993")["POL"].tolist() == [5]


def test_directed_relation_is_one_way(scenario):
    apply_operations(scenario, [Operation(
        kind="directed", name="diplomatic relation towards", targets="POL:RUS",
        years="1990-1991", curve="constant", start=-40)], author="t")
    m = pd.read_csv(scenario.year_dir(1990) / "relations-directed" / "diplomatic-relation-towards.csv",
                    index_col="tag")
    assert m.loc["POL", "RUS"] == -40
    assert np.isnan(m.loc["RUS", "POL"])


def test_doublesided_relation_writes_both_cells(scenario):
    apply_operations(scenario, [Operation(
        kind="doublesided", name="in war", targets="RUS:UKR", years="1993-1995",
        curve="step", start=0, end=1)], author="t")
    m = pd.read_csv(scenario.year_dir(1995) / "relations-doublesided" / "in-war.csv", index_col="tag")
    assert m.loc["RUS", "UKR"] == m.loc["UKR", "RUS"] == 1
    assert validate(scenario) == []


def test_binary_formula_rejects_continuous_curve(scenario):
    with pytest.raises(SimulatorError, match="0/1 flag"):
        apply_operations(scenario, [op(name="riots", start=0, end=1)], author="t")


def test_int_formula_is_rounded(scenario):
    apply_operations(scenario, [op(name="population index", years="1990-1993", start=0, end=10)], author="t")
    assert show(scenario, "grade", "population index", "POL", "1990-1993")["POL"].tolist() == [0, 3, 7, 10]


def test_out_of_range_fails_unless_clip(scenario):
    with pytest.raises(SimulatorError, match="clip"):
        apply_operations(scenario, [op(start=50, end=150)], author="t")
    apply_operations(scenario, [op(start=50, end=150, clip=True)], author="t")
    assert show(scenario, "grade", "stability", "POL", "1994")["POL"].tolist() == [100]


def test_non_existing_country_is_rejected(scenario):
    with pytest.raises(SimulatorError, match="UKR does not exist"):
        apply_operations(scenario, [op(targets="UKR")], author="t")
    apply_operations(scenario, [op(targets="UKR", years="1991-1994", start=1, end=2)], author="t")


def test_unknown_tag_diagonal_and_bad_years(scenario):
    with pytest.raises(SimulatorError, match="Unknown tags"):
        apply_operations(scenario, [op(targets="XXX", start=1, end=2)], author="t")
    with pytest.raises(SimulatorError, match="two different tags"):
        apply_operations(scenario, [Operation(kind="directed", name="diplomatic relation towards",
                                              targets="POL:POL", years="1990", curve="constant", start=1)],
                         author="t")
    with pytest.raises(SimulatorError, match="not a scenario date"):
        apply_operations(scenario, [op(years="1980-1990", start=1, end=2)], author="t")


def test_only_empty_and_start_current(scenario):
    apply_operations(scenario, [op(years="1992", curve="constant", start=70)], author="t")
    res = apply_operations(scenario, [op(start=0, end=0, only_empty=True)], author="t")
    assert (res[0].written, res[0].skipped) == (4, 1)
    assert show(scenario, "grade", "stability", "POL", "1992")["POL"].tolist() == [70]

    apply_operations(scenario, [op(years="1992-1994", start="current", end=10)], author="t")
    assert show(scenario, "grade", "stability", "POL", "1992-1994")["POL"].tolist() == [70, 40, 10]
    with pytest.raises(SimulatorError, match="no 'stability' value"):
        apply_operations(scenario, [op(targets="RUS", start="current", end=10)], author="t")


def test_batch_is_all_or_nothing_and_dry_run_writes_nothing(scenario):
    good = op(start=1, end=2)
    bad = op(name="riots", start=0, end=1)
    with pytest.raises(SimulatorError, match="Operation 2"):
        apply_operations(scenario, [good, bad], author="t")
    assert not (scenario.year_dir(1990) / "internal-grades.csv").exists()

    res = apply_operations(scenario, [good], author="t", dry_run=True)
    assert res[0].written == 5
    assert not scenario.narrated_dir.exists()


def test_later_operation_sees_earlier_one_in_batch(scenario):
    apply_operations(scenario, [
        op(years="1990", curve="constant", start=30),
        op(years="1990-1992", start="current", end=50),
    ], author="t")
    assert show(scenario, "grade", "stability", "POL", "1990-1992")["POL"].tolist() == [30, 40, 50]


def test_changelog_records_provenance(scenario):
    apply_operations(scenario, [op(start=1, end=2, rationale="because")], author="model-x")
    log = pd.read_csv(scenario.narrated_dir / "changelog.csv")
    assert log.loc[0, "author"] == "model-x"
    assert log.loc[0, "rationale"] == "because"
    assert log.loc[0, "years"] == "1990-1994"
    assert json.loads(log.loc[0, "params"])["curve"] == "linear"


def test_missing_report(scenario):
    apply_operations(scenario, [op(targets="POL,RUS,DEU", years="1990-1995", curve="constant", start=1)],
                     author="t")
    rep = missing_report(scenario, "grade", "stability").iloc[0]
    # UKR exists only 1991-1995 -> 3*6 + 5 cells
    assert (rep["filled"], rep["total"], rep["first_year_with_gaps"]) == (18, 23, 1991)
    pair = missing_report(scenario, "doublesided", "in war").iloc[0]
    assert pair["total"] == 3 * 6 + 3 * 5  # 3 pairs without UKR every year + 3 pairs with UKR from 1991


def test_validator_finds_manual_breakage(scenario):
    apply_operations(scenario, [Operation(kind="doublesided", name="in war", targets="POL:RUS",
                                          years="1990", curve="constant", start=1)], author="t")
    path = scenario.year_dir(1990) / "relations-doublesided" / "in-war.csv"
    m = pd.read_csv(path, index_col="tag")
    m.loc["RUS", "POL"] = 0
    m.loc["UKR", "DEU"] = 1  # UKR does not exist in 1990
    m.loc["POL", "POL"] = 1
    m.to_csv(path)
    messages = " | ".join(i.message for i in validate(scenario))
    assert "not symmetric" in messages
    assert "not existing" in messages
    assert "diagonal" in messages


def test_cli_set_show_and_batch(scenario, tmp_path, capsys):
    root = str(scenario.root)
    assert main(["set", "--scenario", root, "--kind", "grade", "--name", "stability", "--targets", "POL",
                 "--years", "1990-1992", "--curve", "logistic", "--start", "0", "--end", "100",
                 "--param", "steepness=6", "--author", "cli"]) == 0
    assert main(["--json", "show", "--scenario", root, "--kind", "grade", "--name", "stability",
                 "--targets", "POL", "--years", "1991"]) == 0
    out = capsys.readouterr().out.strip().splitlines()[-1]
    assert json.loads(out) == [{"year": 1991, "POL": 50.0}]

    batch = tmp_path / "ops.json"
    batch.write_text(json.dumps({"rationale": "test", "operations": [
        {"kind": "directed", "name": "diplomatic relation towards", "targets": ["POL:RUS", "DEU:RUS"],
         "years": [1990, 1995], "curve": "manual", "values": [1, 2, 3, 4, 5, 6]},
    ]}))
    assert main(["batch", str(batch), "--scenario", root, "--author", "cli"]) == 0
    assert show(scenario, "directed", "diplomatic relation towards", "DEU:RUS", "1995")["DEU:RUS"].tolist() == [6]
    with pytest.raises(SystemExit):  # --author is required
        main(["batch", str(batch), "--scenario", root])
    assert main(["set", "--scenario", root, "--kind", "grade", "--name", "nope", "--targets", "POL",
                 "--years", "1990", "--curve", "constant", "--start", "1", "--author", "cli"]) == 1
