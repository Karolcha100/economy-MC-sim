import pandas as pd
import pytest

from simulator.formulas import add_formula, edit_formula, get_formula, list_formulas, remove_formula
from simulator.io import SimulatorError
from simulator.narrated import Operation, apply_operations, show
from simulator.scenario import SCENARIOS_DIR, Scenario
from simulator.templates import KINDS, load_template, validate_formulas
from simulator.validate import validate


def fill(scenario, name="stability", start=10, end=90, kind="grade", targets="POL"):
    apply_operations(scenario, [Operation(kind=kind, name=name, targets=targets, years="1990-1994",
                                          start=start, end=end)], author="t")


def test_add_formula_validates_against_template(scenario):
    f = add_formula(scenario, "grade", "inflation pressure", "float", 0, 10)
    assert f.slug == "inflation-pressure"
    assert get_formula(scenario, "grade", "inflation-pressure") == f
    with pytest.raises(SimulatorError, match="collides"):
        add_formula(scenario, "grade", "Inflation-Pressure".lower(), "float", 0, 10)
    with pytest.raises(SimulatorError, match="valmin"):
        add_formula(scenario, "grade", "broken", "float", 10, 0)
    with pytest.raises(SimulatorError, match="type"):
        add_formula(scenario, "grade", "broken", "str", 0, 1)
    with pytest.raises(SimulatorError, match="side-a"):
        add_formula(scenario, "doublesided", "trade", "float", 0, 1, entities={"side-a": "ORG"})


def test_rename_migrates_internal_grade_column(scenario):
    fill(scenario)
    edit_formula(scenario, "grade", "stability", new_name="political stability")
    cols = pd.read_csv(scenario.year_dir(1990) / "internal-grades.csv", index_col="tag").columns
    assert "political-stability" in cols and "stability" not in cols
    assert show(scenario, "grade", "political stability", "POL", "1994")["POL"].tolist() == [90]


def test_rename_migrates_relation_files(scenario):
    fill(scenario, name="diplomatic relation towards", kind="directed", targets="POL:RUS", start=-10, end=10)
    edit_formula(scenario, "directed", "diplomatic relation towards", new_name="diplomacy towards")
    d = scenario.year_dir(1992) / "relations-directed"
    assert (d / "diplomacy-towards.csv").exists()
    assert not (d / "diplomatic-relation-towards.csv").exists()
    assert show(scenario, "directed", "diplomacy towards", "POL:RUS", "1992")["POL:RUS"].tolist() == [0]
    assert validate(scenario) == []


def test_range_change_needs_clip(scenario):
    fill(scenario)  # 10..90
    with pytest.raises(SimulatorError, match="clip"):
        edit_formula(scenario, "grade", "stability", valmax=50)
    assert get_formula(scenario, "grade", "stability").valmax == 100  # unchanged
    edit_formula(scenario, "grade", "stability", valmax=50, clip=True)
    assert show(scenario, "grade", "stability", "POL", "1990-1994")["POL"].tolist() == [10, 30, 50, 50, 50]


def test_type_change_to_int_rounds_with_clip(scenario):
    fill(scenario, start=10.4, end=11.6)
    with pytest.raises(SimulatorError):
        edit_formula(scenario, "grade", "stability", type="int")
    edit_formula(scenario, "grade", "stability", type="int", clip=True)
    assert show(scenario, "grade", "stability", "POL", "1990-1994")["POL"].tolist() == [10, 11, 11, 11, 12]


def test_remove_needs_purge_when_data_exists(scenario):
    fill(scenario)
    with pytest.raises(SimulatorError, match="purge"):
        remove_formula(scenario, "grade", "stability")
    remove_formula(scenario, "grade", "stability", purge=True)
    assert "stability" not in [f.name for f in list_formulas(scenario, "grade")]
    # stability was the only grade with data, so the yearly file is gone
    assert not (scenario.year_dir(1990) / "internal-grades.csv").exists()
    remove_formula(scenario, "grade", "riots")  # no data -> no purge needed


def test_shipped_templates_and_scenario_are_valid():
    for kind in KINDS:
        assert load_template(kind).field_names[:4] == ["name", "type", "valmin", "valmax"]
    scenario = Scenario(SCENARIOS_DIR / "world-1990-2025")
    for kind in KINDS:
        table = pd.read_csv(scenario.formulas_dir / f"{kind}.csv", dtype=str, keep_default_na=False)
        assert validate_formulas(load_template(kind), table) == []
    assert [i for i in validate(scenario) if i.level == "error"] == []
