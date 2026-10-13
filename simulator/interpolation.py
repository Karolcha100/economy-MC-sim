"""Change functions used to fill a value between a start and an end year.

Every curve is a normalised shape f(t), t in [0, 1], with f(0) = 0 and f(1) = 1, and
value(year) = start + (end - start) * f(t). Thanks to the normalisation each curve
works for start = 0 and for sign changes (e.g. relations in -100..100).
"""

from __future__ import annotations

import numpy as np

from simulator.io import SimulatorError

CURVES = ("linear", "exponential", "logistic", "step", "constant", "manual")
# Curves that never produce intermediate values; the only ones allowed for 0/1 flags.
DISCRETE_CURVES = ("step", "constant", "manual")

DEFAULT_PARAMS = {
    "linear": {},
    "exponential": {"k": 3.0},
    "logistic": {"steepness": 10.0, "midpoint": 0.5},
    "step": {"midpoint": 0.5},
    "constant": {},
    "manual": {},
}


def _fraction(curve: str, t: np.ndarray, params: dict[str, float]) -> np.ndarray:
    if curve == "linear":
        return t
    if curve == "exponential":
        k = params["k"]
        if k == 0:
            return t
        return np.expm1(k * t) / np.expm1(k)
    if curve == "logistic":
        s, m = params["steepness"], params["midpoint"]
        if s <= 0:
            raise SimulatorError("logistic steepness must be > 0")
        sig = 1.0 / (1.0 + np.exp(-s * (t - m)))
        lo = 1.0 / (1.0 + np.exp(s * m))
        hi = 1.0 / (1.0 + np.exp(-s * (1.0 - m)))
        return (sig - lo) / (hi - lo)
    if curve == "step":
        return (t >= params["midpoint"]).astype(float)
    if curve == "constant":
        return np.zeros_like(t)
    raise SimulatorError(f"Unknown curve {curve!r}. Use one of: {', '.join(CURVES)}")


def curve_values(
    years: list[int],
    curve: str,
    start: float | None = None,
    end: float | None = None,
    params: dict[str, float] | None = None,
    values: list[float] | None = None,
) -> np.ndarray:
    """Values for each year in `years` (sorted). For a single year t = 1 (end value)."""
    if curve not in CURVES:
        raise SimulatorError(f"Unknown curve {curve!r}. Use one of: {', '.join(CURVES)}")

    if curve == "manual":
        if values is None or len(values) != len(years):
            raise SimulatorError(
                f"manual curve needs exactly {len(years)} values (one per year {years[0]}..{years[-1]}), "
                f"got {0 if values is None else len(values)}"
            )
        return np.asarray(values, dtype=float)
    if values is not None:
        raise SimulatorError("values are only allowed with the manual curve")

    if start is None:
        raise SimulatorError(f"curve {curve!r} needs a start value")
    if curve == "constant":
        end = start
    elif end is None:
        raise SimulatorError(f"curve {curve!r} needs an end value")

    unknown = set(params or {}) - set(DEFAULT_PARAMS[curve])
    if unknown:
        raise SimulatorError(
            f"Unknown params {sorted(unknown)} for curve {curve!r}; "
            f"allowed: {sorted(DEFAULT_PARAMS[curve]) or 'none'}"
        )
    merged = {**DEFAULT_PARAMS[curve], **(params or {})}

    y = np.asarray(years, dtype=float)
    span = y[-1] - y[0]
    t = (y - y[0]) / span if span > 0 else np.ones_like(y)
    return start + (end - start) * _fraction(curve, t, merged)
