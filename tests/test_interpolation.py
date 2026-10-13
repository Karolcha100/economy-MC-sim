import numpy as np
import pytest

from simulator.interpolation import curve_values
from simulator.io import SimulatorError

YEARS = [2000, 2001, 2002, 2003, 2004]


@pytest.mark.parametrize("curve", ["linear", "exponential", "logistic"])
def test_curves_hit_both_ends(curve):
    v = curve_values(YEARS, curve, start=-50, end=80)
    assert v[0] == pytest.approx(-50)
    assert v[-1] == pytest.approx(80)
    assert np.all(np.diff(v) > 0)


def test_linear_values():
    assert curve_values(YEARS, "linear", 0, 100).tolist() == [0, 25, 50, 75, 100]


def test_exponential_works_from_zero_and_is_convex():
    v = curve_values(YEARS, "exponential", 0, 100, {"k": 3})
    assert v[2] < 50  # slow start
    assert curve_values(YEARS, "exponential", 0, 100, {"k": -3})[2] > 50  # fast start
    assert curve_values(YEARS, "exponential", 0, 100, {"k": 0}).tolist() == [0, 25, 50, 75, 100]


def test_logistic_midpoint():
    v = curve_values(YEARS, "logistic", 0, 100, {"midpoint": 0.5})
    assert v[2] == pytest.approx(50)


def test_step_constant_manual():
    assert curve_values(YEARS, "step", 0, 1).tolist() == [0, 0, 1, 1, 1]
    assert curve_values(YEARS, "step", 0, 1, {"midpoint": 1}).tolist() == [0, 0, 0, 0, 1]
    assert curve_values(YEARS, "constant", 7).tolist() == [7] * 5
    assert curve_values(YEARS, "manual", values=[1, 2, 3, 4, 5]).tolist() == [1, 2, 3, 4, 5]


def test_single_year_uses_end_value():
    assert curve_values([2000], "linear", 10, 20).tolist() == [20]


@pytest.mark.parametrize("kwargs", [
    {"curve": "manual", "values": [1, 2]},
    {"curve": "linear", "start": 0},
    {"curve": "linear", "start": 0, "end": 1, "params": {"k": 2}},
    {"curve": "spline", "start": 0, "end": 1},
    {"curve": "linear", "start": 0, "end": 1, "values": [1, 2, 3, 4, 5]},
])
def test_invalid_input(kwargs):
    with pytest.raises(SimulatorError):
        curve_values(YEARS, **kwargs)
