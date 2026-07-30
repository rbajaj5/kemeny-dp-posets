"""Reference privacy mechanisms for small ranking spaces."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from random import Random

from .core import KemenyAnalyzer, Profile, Ranking
from .sensitivity import SensitivityAnalyzer


def _weighted_choice(
    values: tuple[Ranking, ...], weights: list[float], rng: Random
) -> Ranking:
    total = sum(weights)
    threshold = rng.random() * total
    running = 0.0
    for value, weight in zip(values, weights):
        running += weight
        if running >= threshold:
            return value
    return values[-1]


def exponential_kemeny(
    kemeny: KemenyAnalyzer,
    profile: Profile,
    epsilon: float,
    *,
    rng: Random | None = None,
) -> Ranking:
    """Pure-DP exact exponential mechanism over all rankings.

    This uses the generic ``2 * sensitivity`` denominator. It is intended as
    a correctness baseline for small candidate sets, not a scalable method.
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    rng = rng or Random()
    probabilities = exponential_kemeny_probabilities(kemeny, profile, epsilon)
    return _weighted_choice(
        kemeny.space.rankings, list(probabilities), rng
    )


def exponential_kemeny_probabilities(
    kemeny: KemenyAnalyzer,
    profile: Profile,
    epsilon: float,
) -> tuple[float, ...]:
    """Return the exact finite-output exponential-mechanism distribution.

    Probabilities are aligned with ``kemeny.space.rankings``. The score is
    negative Kemeny cost and its add/remove-one-ballot sensitivity is the
    Kendall diameter.
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    scores = kemeny.scores(profile)
    sensitivity = kemeny.space.diameter
    if sensitivity == 0:
        return (1.0,)
    log_weights = [-(epsilon * score) / (2 * sensitivity) for score in scores]
    shift = max(log_weights)
    weights = [exp(weight - shift) for weight in log_weights]
    total = sum(weights)
    return tuple(weight / total for weight in weights)


@dataclass(frozen=True)
class ScalarRelease:
    released_value: float
    exact_value: int
    smooth_sensitivity: float
    beta: float
    noise_scale: float
    explored_radius: int


def _laplace_unit(rng: Random) -> float:
    magnitude = rng.expovariate(1.0)
    return -magnitude if rng.random() < 0.5 else magnitude


def release_optimum_score(
    sensitivity: SensitivityAnalyzer,
    profile: Profile,
    epsilon: float,
    delta: float,
    *,
    rng: Random | None = None,
) -> ScalarRelease:
    """Release the scalar optimum using NRS07 smooth-sensitivity calibration.

    For one-dimensional Laplace noise, Nissim-Raskhodnikova-Smith use
    ``alpha = epsilon/2`` and ``beta = epsilon/(2 log(2/delta))``. Their
    mechanism releases ``f(x) + S_beta(x)/alpha * Laplace(1)``.
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if not 0 < delta < 1:
        raise ValueError("delta must lie strictly between zero and one")
    rng = rng or Random()
    beta = epsilon / (2 * log(2 / delta))
    smooth = sensitivity.exact_smooth_sensitivity_optimum_value(profile, beta)
    alpha = epsilon / 2
    scale = smooth.value / alpha
    exact = sensitivity.kemeny.optimum_value(profile)
    released = exact + scale * _laplace_unit(rng)
    return ScalarRelease(
        released,
        exact,
        smooth.value,
        beta,
        scale,
        smooth.explored_radius,
    )
