"""Exact finite audits for the sample-and-center utility components."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement, permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import KemenyAnalyzer, Ranking, RankingSpace
from kemeny_dp.poset import profiles_of_size
from kemeny_dp.sample_aggregate import (
    borda_ranking,
    center_of_attention_certificate,
    two_ballot_kemeny,
    unrestricted_attention_certificate,
)


def _relabel(ranking: Ranking, relabeling: tuple[int, ...]) -> Ranking:
    return tuple(relabeling[candidate] for candidate in ranking)


def _point_label(space: RankingSpace, points: tuple[Ranking, ...]) -> str:
    counts = Counter(points)
    return " ".join(
        f"{space.ranking_label(ranking)}:{counts[ranking]}"
        for ranking in space.rankings
        if counts[ranking]
    )


def center_audit(max_point_count: int = 7) -> dict[str, object]:
    """Exhaust finite input multisets and every admissible step."""
    space = RankingSpace.create(3)
    candidate_relabelings = tuple(permutations(range(space.candidate_count)))
    certificates_examined = 0
    input_center_failures = 0
    target_count_failures = 0
    two_approximation_failures = 0
    minimizer_equivariance_failures = 0
    selected_center_equivariance_failures = 0
    exact_unrestricted_count = 0
    factor_two_count = 0
    maximum_ratio = Fraction(1)
    first_factor_two_example: dict[str, object] | None = None
    by_point_count: dict[str, object] = {}

    ranking_index = {
        ranking: index for index, ranking in enumerate(space.rankings)
    }
    for point_count in range(2, max_point_count + 1):
        point_multisets = 0
        point_certificates = 0
        point_factor_two = 0
        for indices in combinations_with_replacement(
            range(space.ranking_count), point_count
        ):
            point_multisets += 1
            points = tuple(space.rankings[index] for index in indices)
            for step in range(1, point_count):
                target = (point_count + step) // 2 + 1
                if target > point_count:
                    continue
                restricted = center_of_attention_certificate(
                    space, points, step=step
                )
                unrestricted = unrestricted_attention_certificate(
                    space, points, step=step
                )
                certificates_examined += 1
                point_certificates += 1
                input_center_failures += int(
                    restricted.center not in set(points)
                )
                center_index = ranking_index[restricted.center]
                witness_count = sum(
                    space.distances[center_index][ranking_index[point]]
                    <= restricted.radius
                    for point in points
                )
                target_count_failures += int(
                    witness_count < restricted.target_count
                )
                two_approximation_failures += int(
                    restricted.radius > 2 * unrestricted.radius
                )
                exact_unrestricted_count += int(
                    restricted.radius == unrestricted.radius
                )
                is_factor_two = (
                    unrestricted.radius > 0
                    and restricted.radius == 2 * unrestricted.radius
                )
                factor_two_count += int(is_factor_two)
                point_factor_two += int(is_factor_two)
                ratio = (
                    Fraction(restricted.radius, unrestricted.radius)
                    if unrestricted.radius
                    else Fraction(1)
                )
                maximum_ratio = max(maximum_ratio, ratio)

                if is_factor_two and first_factor_two_example is None:
                    first_factor_two_example = {
                        "points": _point_label(space, points),
                        "step": step,
                        "target_count": restricted.target_count,
                        "restricted_center": space.ranking_label(
                            restricted.center
                        ),
                        "restricted_radius": restricted.radius,
                        "unrestricted_center": space.ranking_label(
                            unrestricted.center
                        ),
                        "unrestricted_radius": unrestricted.radius,
                    }

                original_minimizers = set(restricted.minimizers)
                for relabeling in candidate_relabelings:
                    transformed = center_of_attention_certificate(
                        space,
                        tuple(_relabel(point, relabeling) for point in points),
                        step=step,
                    )
                    expected_minimizers = {
                        _relabel(center, relabeling)
                        for center in original_minimizers
                    }
                    minimizer_equivariance_failures += int(
                        set(transformed.minimizers) != expected_minimizers
                    )
                    selected_center_equivariance_failures += int(
                        transformed.center
                        != _relabel(restricted.center, relabeling)
                    )

        by_point_count[str(point_count)] = {
            "point_multisets": point_multisets,
            "certificates": point_certificates,
            "factor_two_cases": point_factor_two,
        }

    return {
        "candidate_count": 3,
        "maximum_point_count": max_point_count,
        "certificates_examined": certificates_examined,
        "input_center_failures": input_center_failures,
        "target_count_failures": target_count_failures,
        "two_approximation_failures": two_approximation_failures,
        "candidate_relabeling_checks": (
            certificates_examined * len(candidate_relabelings)
        ),
        "minimum_radius_equivariance_failures": (
            minimizer_equivariance_failures
        ),
        "lexicographic_selector_equivariance_failures": (
            selected_center_equivariance_failures
        ),
        "restricted_radius_equals_unrestricted_count": (
            exact_unrestricted_count
        ),
        "factor_two_count": factor_two_count,
        "maximum_restricted_to_unrestricted_ratio": str(maximum_ratio),
        "first_factor_two_example": first_factor_two_example,
        "by_point_count": by_point_count,
    }


def two_ballot_audit() -> dict[str, object]:
    total = 0
    optimum_failures = 0
    input_support_failures = 0
    selector_difference_count = 0
    by_candidate_count: dict[str, object] = {}

    for candidate_count in (3, 4):
        space = RankingSpace.create(candidate_count)
        kemeny = KemenyAnalyzer(space)
        local_total = 0
        local_differences = 0
        for first in space.rankings:
            for second in space.rankings:
                output = two_ballot_kemeny(space, first, second)
                profile = space.profile_from_ballots((first, second))
                local_total += 1
                total += 1
                optimum_failures += int(
                    kemeny.score(profile, output)
                    != kemeny.optimum_value(profile)
                )
                input_support_failures += int(
                    output not in (first, second)
                )
                differs = output != kemeny.selected_optimum(profile)
                selector_difference_count += int(differs)
                local_differences += int(differs)
        by_candidate_count[str(candidate_count)] = {
            "ordered_pairs": local_total,
            "different_from_factorial_lexicographic_selector": (
                local_differences
            ),
        }

    return {
        "ordered_pairs_examined": total,
        "optimum_failures": optimum_failures,
        "input_support_failures": input_support_failures,
        "different_from_factorial_lexicographic_selector": (
            selector_difference_count
        ),
        "by_candidate_count": by_candidate_count,
    }


def borda_audit(max_profile_size: int = 8) -> dict[str, object]:
    space = RankingSpace.create(3)
    kemeny = KemenyAnalyzer(space)
    profiles_examined = 0
    five_approximation_failures = 0
    optimum_matches = 0
    maximum_ratio = Fraction(1)
    first_maximum_example: dict[str, object] | None = None
    by_size: dict[str, object] = {}

    for size in range(1, max_profile_size + 1):
        local_count = 0
        local_matches = 0
        for profile in profiles_of_size(space, size):
            ballots = tuple(
                ranking
                for count, ranking in zip(profile, space.rankings)
                for _ in range(count)
            )
            borda = borda_ranking(space, ballots)
            optimum = kemeny.optimum_value(profile)
            borda_cost = kemeny.score(profile, borda)
            profiles_examined += 1
            local_count += 1
            is_match = borda_cost == optimum
            optimum_matches += int(is_match)
            local_matches += int(is_match)
            five_approximation_failures += int(borda_cost > 5 * optimum)
            ratio = (
                Fraction(borda_cost, optimum)
                if optimum
                else Fraction(1)
            )
            if ratio > maximum_ratio:
                maximum_ratio = ratio
                first_maximum_example = {
                    "profile": space.profile_label(profile),
                    "profile_size": size,
                    "borda_ranking": space.ranking_label(borda),
                    "borda_cost": borda_cost,
                    "optimum_cost": optimum,
                    "ratio": str(ratio),
                }
        by_size[str(size)] = {
            "profiles": local_count,
            "borda_optimum_cost_matches": local_matches,
        }

    return {
        "candidate_count": 3,
        "maximum_profile_size": max_profile_size,
        "profiles_examined": profiles_examined,
        "borda_optimum_cost_matches": optimum_matches,
        "five_approximation_failures": five_approximation_failures,
        "maximum_cost_ratio": str(maximum_ratio),
        "first_maximum_example": first_maximum_example,
        "by_profile_size": by_size,
    }


def main() -> None:
    result = {
        "status": {
            "center_two_approximation": "PROVED_STANDARD_METRIC_LEMMA",
            "two_ballot_shortcut": "PROVED_EXACT",
            "borda_audit": "KNOWN_APPROXIMATION_EXACT_FINITE_AUDIT",
            "privacy": "NOT_CLAIMED",
        },
        "center_of_attention": center_audit(),
        "two_ballot_kemeny": two_ballot_audit(),
        "borda": borda_audit(),
    }
    output = ROOT / "results" / "sample_aggregate_audit.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
