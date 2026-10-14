import pandas as pd
import pytest

from simulator.history import import_dyadic, import_history, load_dyadic, load_history, load_metadata
from simulator.narrated import Operation, apply_operations
from simulator.store import CHANGELOG_COLUMNS
from simulator.validate import validate


def test_owid_import_drops_aggregates(scenario, tmp_path):
    src = tmp_path / "owid.csv"
    pd.DataFrame({
        "entity": ["Poland", "Poland", "World", "Russia"],
        "code": ["POL", "POL", "OWID_WRL", "RUS"],
        "year": [1990, 1991, 1990, 1991],
        "hdi": [0.7, 0.71, 0.6, 0.73],
        "owid_region": ["Europe"] * 4,
    }).to_csv(src, index=False)
    import_history(scenario, "hdi", src, fmt="owid")
    h = load_history(scenario, "hdi")
    assert h.at[1991, "POL"] == 0.71 and h.at[1991, "RUS"] == 0.73
    assert load_metadata(scenario).set_index("name").at["hdi", "shape"] == "country"


def test_wgi_xlsx(scenario, tmp_path):
    pytest.importorskip("openpyxl")
    rows = [["title"] + [None] * 6,
            [None, None, 1996, 1996, 1998, 1998, None],
            ["Country/Territory", "Code", "Estimate", "StdErr", "Estimate", "StdErr", None],
            ["Poland", "POL", 0.7, 0.2, "#N/A", 0.2, None],
            ["Russia", "RUS", -1.0, 0.2, -0.9, 0.2, None]]
    path = tmp_path / "wgi.xlsx"
    pd.DataFrame(rows).to_excel(path, sheet_name="Political StabilityNoViolence", header=False, index=False)
    pd.DataFrame({"date": range(1994, 2000)}).to_csv(scenario.root / "dates.csv", index=False)
    import_history(scenario, "wgi", path, fmt="wgi-xlsx", sheet="pv")
    h = load_history(scenario, "wgi")
    assert (h.at[1996, "POL"], h.at[1996, "RUS"], h.at[1998, "RUS"]) == (0.7, -1.0, -0.9)
    assert pd.isna(h.at[1998, "POL"])  # "#N/A" in the workbook
    assert h.loc[1997].isna().all()  # WGI was biennial until 2002


def test_geonames_neighbours_respect_existence(scenario, tmp_path):
    src = tmp_path / "countryInfo.txt"
    src.write_text(
        "#ISO\tISO3\n"
        + "\t".join(["PL", "POL"] + [""] * 15 + ["DE,UA,RU"]) + "\n"
        + "\t".join(["DE", "DEU"] + [""] * 15 + ["PL"]) + "\n"
        + "\t".join(["UA", "UKR"] + [""] * 15 + ["PL,RU"]) + "\n"
        + "\t".join(["RU", "RUS"] + [""] * 15 + ["PL,UA"]) + "\n"
    )
    rows = import_dyadic(scenario, "borders", src, "geonames-neighbours")
    pairs_1990 = set(map(tuple, rows[rows["date"] == 1990][["side_a", "side_b"]].values))
    assert pairs_1990 == {("DEU", "POL"), ("POL", "RUS")}  # UKR exists from 1991
    assert ("POL", "UKR") in set(map(tuple, rows[rows["date"] == 1991][["side_a", "side_b"]].values))
    assert load_metadata(scenario).set_index("name").at["borders", "shape"] == "dyad-symmetric"
    assert validate(scenario) == []


def test_ucdp_levels(scenario, tmp_path):
    pytest.importorskip("country_converter")
    src = tmp_path / "ucdp.csv"
    pd.DataFrame({
        "year": [1992, 1993, 1993],
        "type_of_conflict": ["4", "2", "2"],
        "gwno_a": ["369", "290", "290"],
        "gwno_a_2nd": ["", "", ""],
        "gwno_b": ["", "365", "365"],       # rebels have no code
        "gwno_b_2nd": ["365", "", ""],
    }).to_csv(src, index=False)
    rows = import_dyadic(scenario, "war", src, "ucdp-dyadic")
    got = {(r.date, r.side_a, r.side_b): r.value for r in rows.itertuples()}
    assert got == {(1992, "RUS", "UKR"): 1.0, (1993, "POL", "RUS"): 2.0}
    assert len(load_dyadic(scenario, "war")) == 2


def test_sources_are_logged_and_old_changelog_is_upgraded(scenario):
    log = scenario.narrated_dir / "changelog.csv"
    log.parent.mkdir(parents=True)
    pd.DataFrame([["t0", "old", "set", "internal-grades", "stability", "POL", "1990", "{}", "r"]],
                 columns=CHANGELOG_COLUMNS[:-1]).to_csv(log, index=False)
    apply_operations(scenario, [Operation(kind="grade", name="stability", targets="POL", years="1990",
                                          curve="constant", start=5, sources=["https://a", "Title, Outlet, 2020"])],
                     author="t")
    df = pd.read_csv(log, keep_default_na=False)
    assert list(df.columns) == CHANGELOG_COLUMNS
    assert df["sources"].tolist() == ["", "https://a | Title, Outlet, 2020"]


def test_old_country_codes_are_mapped(tmp_path):
    from simulator.sources import read_owid
    src = tmp_path / "h.csv"
    src.write_text("entity,code,year,score\nKosovo,OWID_KOS,2011,5.4\nWorld,OWID_WRL,2011,5.0\nPoland,POL,2011,5.8\n")
    df = read_owid(src)
    assert sorted(df.columns) == ["POL", "XKX"] and df.loc[2011, "XKX"] == 5.4
