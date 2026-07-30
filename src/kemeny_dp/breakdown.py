"""Exact zero-plus total-variation breakdown for finite Kemeny profiles."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .core import KemenyAnalyzer, Profile, Ranking


@dataclass(frozen=True)
class BreakdownComparison:
    """Compare integer cover stability with continuous contamination.

    ``exact_zero_plus_tv_breakdown`` uses the standard convention
    ``TV(p, q) = ||p - q||_1 / 2``.  It is the infimum TV distance from the
    empirical law to a law at which the original optimum is not unique.
    """

    profile_size: int
    optimum: Ranking
    cover_radius: int
    normalized_margin: Fraction
    margin_competitor: Ranking
    margin_gap: int
    margin_distance: int
    exact_zero_plus_tv_breakdown: Fraction
    tv_competitor: Ranking
    optimum_empirical_mass: Fraction
    goibert_sufficient_condition: bool
    half_margin_equality: bool

    @property
    def goibert_zero_plus_expression(self) -> Fraction:
        """Theorem 3.1's displayed expression at attack level zero-plus."""
        return self.normalized_margin

    @property
    def standard_tv_of_goibert_attack(self) -> Fraction | None:
        """TV of the paper's explicit attack when its mass condition holds."""
        if not self.goibert_sufficient_condition:
            return None
        return self.normalized_margin / 2


def _ceil_fraction(value: Fraction) -> int:
    return (value.numerator + value.denominator - 1) // value.denominator


def _competitor_tv_boundary(
    kemeny: KemenyAnalyzer,
    profile: Profile,
    optimum_index: int,
    competitor_index: int,
    gap: int,
) -> Fraction:
    """Minimum standard TV needed to make one competitor tie the optimum.

    Write ``f(rho) = d(rho, competitor) - d(rho, optimum)``.  Moving mass
    from the largest values of ``f`` to its minimum gives the greatest score
    gap reduction per unit TV.  The minimum is ``-d(optimum, competitor)``
    and is attained at the competitor itself, which always has enough
    receiving capacity for all mass outside that state.
    """
    sample_size = sum(profile)
    distance = kemeny.space.distances[optimum_index][competitor_index]
    coefficients = tuple(
        kemeny.space.distances[ballot_index][competitor_index]
        - kemeny.space.distances[ballot_index][optimum_index]
        for ballot_index in range(kemeny.space.ranking_count)
    )
    minimum = min(coefficients)
    if minimum != -distance:
        raise AssertionError("Kendall reverse-triangle endpoint was not attained")

    remaining_reduction = Fraction(gap, sample_size)
    transferred = Fraction(0)
    sources = sorted(
        (
            (coefficient, Fraction(count, sample_size))
            for coefficient, count in zip(coefficients, profile)
            if count and coefficient > minimum
        ),
        reverse=True,
    )
    for coefficient, available_mass in sources:
        reduction_per_mass = coefficient - minimum
        available_reduction = available_mass * reduction_per_mass
        if remaining_reduction <= available_reduction:
            transferred += remaining_reduction / reduction_per_mass
            remaining_reduction = Fraction(0)
            break
        transferred += available_mass
        remaining_reduction -= available_reduction

    if remaining_reduction:
        raise AssertionError("failed to reach the competitor boundary")
    return transferred


def compare_cover_radius_and_breakdown(
    kemeny: KemenyAnalyzer, profile: Profile
) -> BreakdownComparison:
    """Return an exact finite comparison for a uniquely optimized profile."""
    kemeny.space.validate_profile(profile)
    sample_size = sum(profile)
    if sample_size == 0:
        raise ValueError("breakdown comparison requires a nonempty profile")

    _, optima = kemeny.optimum(profile)
    if len(optima) != 1:
        raise ValueError("breakdown comparison requires a unique optimum")

    optimum = optima[0]
    optimum_index = kemeny.space.rankings.index(optimum)
    scores = kemeny.scores(profile)
    optimum_score = scores[optimum_index]

    margin_rows: list[tuple[Fraction, int, Ranking, int, int]] = []
    tv_rows: list[tuple[Fraction, int, Ranking]] = []
    for competitor_index, competitor in enumerate(kemeny.space.rankings):
        if competitor_index == optimum_index:
            continue
        gap = scores[competitor_index] - optimum_score
        distance = kemeny.space.distances[optimum_index][competitor_index]
        normalized_margin = Fraction(gap, sample_size * distance)
        tv_boundary = _competitor_tv_boundary(
            kemeny,
            profile,
            optimum_index,
            competitor_index,
            gap,
        )
        margin_rows.append(
            (
                normalized_margin,
                competitor_index,
                competitor,
                gap,
                distance,
            )
        )
        tv_rows.append((tv_boundary, competitor_index, competitor))

    normalized_margin, _, margin_competitor, gap, distance = min(margin_rows)
    exact_tv, _, tv_competitor = min(tv_rows)
    optimum_mass = Fraction(profile[optimum_index], sample_size)
    condition = normalized_margin <= 2 * optimum_mass
    cover_radius = _ceil_fraction(sample_size * normalized_margin)

    return BreakdownComparison(
        profile_size=sample_size,
        optimum=optimum,
        cover_radius=cover_radius,
        normalized_margin=normalized_margin,
        margin_competitor=margin_competitor,
        margin_gap=gap,
        margin_distance=distance,
        exact_zero_plus_tv_breakdown=exact_tv,
        tv_competitor=tv_competitor,
        optimum_empirical_mass=optimum_mass,
        goibert_sufficient_condition=condition,
        half_margin_equality=exact_tv == normalized_margin / 2,
    )
