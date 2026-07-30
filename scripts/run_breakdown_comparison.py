"""Exhaust the three-candidate cover-radius/TV-breakdown comparison."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.breakdown import compare_cover_radius_and_breakdown
from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.poset import profiles_of_size
from kemeny_dp.sensitivity import SensitivityAnalyzer


def _fraction_text(value) -> str:
    return str(value)


def three_candidate_audit(max_profile_size: int = 8) -> dict[str, object]:
    space = RankingSpace.create(3)
    kemeny = KemenyAnalyzer(space)
    sensitivity = SensitivityAnalyzer(kemeny)
    by_size: dict[str, object] = {}
    first_strict_example: dict[str, object] | None = None
    identity_failures = 0
    lower_bound_failures = 0

    for size in range(1, max_profile_size + 1):
        unique_count = 0
        condition_count = 0
        half_margin_count = 0
        strict_count = 0
        cover_radii: Counter[int] = Counter()

        for profile in profiles_of_size(space, size):
            if len(kemeny.optima(profile)) != 1:
                continue
            unique_count += 1
            result = compare_cover_radius_and_breakdown(kemeny, profile)
            condition_count += int(result.goibert_sufficient_condition)
            half_margin_count += int(result.half_margin_equality)
            is_strict = (
                result.exact_zero_plus_tv_breakdown
                > result.normalized_margin / 2
            )
            strict_count += int(is_strict)
            cover_radii[result.cover_radius] += 1
            identity_failures += int(
                result.cover_radius
                != sensitivity.uniqueness_radius(profile)
            )
            lower_bound_failures += int(
                result.exact_zero_plus_tv_breakdown
                < result.normalized_margin / 2
            )

            if is_strict and first_strict_example is None:
                first_strict_example = {
                    "profile": space.profile_label(profile),
                    "profile_size": size,
                    "optimum": space.ranking_label(result.optimum),
                    "cover_radius": result.cover_radius,
                    "normalized_margin": _fraction_text(
                        result.normalized_margin
                    ),
                    "half_margin_lower_bound": _fraction_text(
                        result.normalized_margin / 2
                    ),
                    "exact_standard_tv_breakdown": _fraction_text(
                        result.exact_zero_plus_tv_breakdown
                    ),
                    "margin_competitor": space.ranking_label(
                        result.margin_competitor
                    ),
                    "tv_competitor": space.ranking_label(
                        result.tv_competitor
                    ),
                    "optimum_empirical_mass": _fraction_text(
                        result.optimum_empirical_mass
                    ),
                }

        by_size[str(size)] = {
            "unique_profile_count": unique_count,
            "goibert_sufficient_condition_count": condition_count,
            "half_margin_equality_count": half_margin_count,
            "strictly_above_half_margin_count": strict_count,
            "cover_radius_histogram": dict(sorted(cover_radii.items())),
        }

    return {
        "candidate_count": 3,
        "maximum_profile_size": max_profile_size,
        "unique_profiles_examined": sum(
            row["unique_profile_count"] for row in by_size.values()
        ),
        "half_margin_equalities": sum(
            row["half_margin_equality_count"] for row in by_size.values()
        ),
        "tv_convention": "TV(p,q) = ||p-q||_1 / 2",
        "cover_identity_failures": identity_failures,
        "half_margin_lower_bound_failures": lower_bound_failures,
        "first_strict_example": first_strict_example,
        "by_profile_size": by_size,
    }


def four_candidate_strict_example() -> dict[str, object]:
    """Record a finite case where the universal lower bound is strict."""
    space = RankingSpace.create(4)
    kemeny = KemenyAnalyzer(space)
    ballots = (
        (0, 1, 2, 3),
        (0, 1, 3, 2),
        (1, 0, 2, 3),
        (1, 0, 3, 2),
        (1, 2, 3, 0),
        (2, 1, 3, 0),
        (2, 3, 1, 0),
        (3, 0, 1, 2),
        (3, 0, 2, 1),
        (3, 2, 0, 1),
    )
    profile = space.profile_from_ballots(ballots)
    result = compare_cover_radius_and_breakdown(kemeny, profile)
    return {
        "profile": space.profile_label(profile),
        "optimum": space.ranking_label(result.optimum),
        "cover_radius": result.cover_radius,
        "normalized_margin": _fraction_text(result.normalized_margin),
        "half_margin_lower_bound": _fraction_text(
            result.normalized_margin / 2
        ),
        "exact_standard_tv_breakdown": _fraction_text(
            result.exact_zero_plus_tv_breakdown
        ),
        "goibert_sufficient_condition": (
            result.goibert_sufficient_condition
        ),
        "half_margin_equality": result.half_margin_equality,
    }


def main() -> None:
    result = {
        "status": "exact finite computation",
        "source_comparison": (
            "Goibert et al. (ICML 2023), Theorems 3.1 and 3.2, "
            "with the standard half-L1 total-variation convention"
        ),
        "audit": three_candidate_audit(),
        "strict_four_candidate_example": four_candidate_strict_example(),
    }
    output = ROOT / "results" / "breakdown_comparison.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
