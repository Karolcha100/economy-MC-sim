import pandas as pd

import simulator.audit as audit
from simulator.history import import_history
from simulator.narrated import Operation, apply_operations


def test_audit_flags_outlier_flat_line_and_crowding(scenario, tmp_path, monkeypatch):
    monkeypatch.setattr(audit, "MIN_COUNTRIES", 3)
    src = tmp_path / "ref.csv"
    pd.DataFrame({"date": range(1990, 1996), "POL": [3] * 6, "RUS": [1] * 6, "DEU": [4] * 6, "UKR": [2] * 6}
                 ).to_csv(src, index=False)
    import_history(scenario, "ref", src, fmt="wide")
    (scenario.root / "audit.csv").write_text("statistic,reference,sign,note\ngrade:stability,ref,1,test\n")
    # stability follows the reference except RUS, which is put on top (outlier); everyone flat (same value every year)
    ops = [Operation(kind="grade", name="stability", targets=t, years=y, curve="constant", start=v)
           for t, y, v in [("POL", "1990-1995", 60), ("DEU", "1990-1995", 70), ("RUS", "1990-1995", 90),
                           ("UKR", "1991-1995", 40)]]
    apply_operations(scenario, ops, author="t")
    result = audit.run_audit(scenario)
    row = result["summary"].iloc[0]
    assert row["years"] == 6 and row["rank_corr"] < 0.5
    assert result["outliers"].iloc[0]["tag"] == "RUS"
    assert result["flat"].empty  # default threshold: 10 filled years, the fixture has only 6
    flat = audit.flat_lines(scenario, min_years=6)
    assert set(flat["tag"]) == {"POL", "DEU", "RUS"}  # UKR exists from 1991: only 5 filled years
    report = audit.write_report(scenario, result, tmp_path / "out")
    assert "RUS" in report.read_text()


def test_crowding(scenario, monkeypatch):
    monkeypatch.setattr(audit, "MIN_COUNTRIES", 3)
    apply_operations(scenario, [Operation(kind="grade", name="stability", targets="POL,RUS,DEU", years="1990",
                                          curve="constant", start=50)], author="t")
    c = audit.crowding(scenario)
    assert c.iloc[0][["statistic", "year", "share"]].tolist() == ["stability", 1990, 1.0]
