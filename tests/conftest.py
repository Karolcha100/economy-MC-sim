from pathlib import Path

import pandas as pd
import pytest

from simulator.scenario import Scenario


@pytest.fixture
def scenario(tmp_path: Path) -> Scenario:
    """Small scenario: 4 countries (UKR exists from 1991), years 1990-1995."""
    root = tmp_path / "mini"
    (root / "formulas").mkdir(parents=True)
    pd.DataFrame({
        "tag": ["POL", "RUS", "UKR", "DEU"],
        "name": ["Poland", "Russia", "Ukraine", "Germany"],
        "exists_from": [None, None, 1991, None],
        "exists_to": [None, None, None, None],
    }).to_csv(root / "tags.csv", index=False)
    pd.DataFrame({"date": range(1990, 1996)}).to_csv(root / "dates.csv", index=False)
    (root / "formulas" / "internal-grades.csv").write_text(
        "name,type,valmin,valmax\n"
        "stability,float,0,100\n"
        "war exhaustion,float,0,100\n"
        "riots,int,0,1\n"
        "population index,int,0,1000\n"
    )
    (root / "formulas" / "relations-directed.csv").write_text(
        "name,type,valmin,valmax,from,to\n"
        "diplomatic relation towards,float,-100,100,TAG,TAG\n"
    )
    (root / "formulas" / "relations-doublesided.csv").write_text(
        "name,type,valmin,valmax,side-a,side-b\n"
        "in war,int,0,1,TAG,TAG\n"
    )
    return Scenario(root)
