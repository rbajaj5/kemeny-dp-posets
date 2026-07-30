"""Finite-sample summaries for reproducible Bernoulli experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt


@dataclass(frozen=True)
class BernoulliSummary:
    successes: int
    trials: int
    rate: float
    standard_error: float
    wilson_95_lower: float
    wilson_95_upper: float
    plugin_berry_esseen_ratio_without_constant: float | None

    def as_dict(self) -> dict[str, int | float | None]:
        return asdict(self)


def bernoulli_summary(successes: int, trials: int) -> BernoulliSummary:
    """Summarize a Bernoulli rate without hiding the finite sample size.

    The Wilson interval uses the 0.975 standard-normal quantile. The
    Berry-Esseen field is the plug-in standardized third-moment ratio divided
    by ``sqrt(trials)``; the theorem's absolute constant is not included, and
    estimating ``p`` means this field is a diagnostic rather than a rigorous
    error bound.
    """
    if trials < 1:
        raise ValueError("trials must be positive")
    if not 0 <= successes <= trials:
        raise ValueError("successes must lie between zero and trials")

    rate = successes / trials
    standard_error = sqrt(rate * (1 - rate) / trials)
    z = 1.959963984540054
    denominator = 1 + z * z / trials
    center = (rate + z * z / (2 * trials)) / denominator
    radius = (
        z
        * sqrt(
            rate * (1 - rate) / trials
            + z * z / (4 * trials * trials)
        )
        / denominator
    )

    if 0 < rate < 1:
        berry_esseen_ratio = (
            rate * rate + (1 - rate) * (1 - rate)
        ) / sqrt(trials * rate * (1 - rate))
    else:
        berry_esseen_ratio = None

    return BernoulliSummary(
        successes,
        trials,
        rate,
        standard_error,
        max(0.0, center - radius),
        min(1.0, center + radius),
        berry_esseen_ratio,
    )
