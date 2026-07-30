"""Audit distance-stratified subset-DP stability certificates."""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import RankingSpace
from kemeny_dp.subset_dp import exact_kemeny_stability_subset_dp


def three_candidate_atlas(max_profile_size: int = 8) -> dict[str, object]:
    """Exhaust every multiset profile through ``max_profile_size``."""
    space = RankingSpace.create(3)
    by_size: dict[str, object] = {}
    strict_denominator_examples = 0
    first_example: dict[str, object] | None = None

    for profile_size in range(1, max_profile_size + 1):
        radii: Counter[int] = Counter()
        profile_count = 0
        tied_count = 0
        larger_gap_faster_count = 0

        for indices in combinations_with_replacement(
            range(space.ranking_count), profile_size
        ):
            ballots = tuple(space.rankings[index] for index in indices)
            certificate = exact_kemeny_stability_subset_dp(ballots)
            profile_count += 1
            radii[certificate.uniqueness_radius] += 1
            tied_count += int(certificate.solution.optimum_count > 1)

            if certificate.second_score_gap == 0:
                best_second_radius = 0
            else:
                best_second_radius = (
                    certificate.second_score_gap
                    + certificate.second_distance
                    - 1
                ) // certificate.second_distance

            larger_gap_is_faster = (
                certificate.destabilizing_score_gap
                > certificate.second_score_gap
                and certificate.uniqueness_radius < best_second_radius
            )
            larger_gap_faster_count += int(larger_gap_is_faster)
            strict_denominator_examples += int(larger_gap_is_faster)

            if larger_gap_is_faster and first_example is None:
                label = space.ranking_label
                first_example = {
                    "profile_size": profile_size,
                    "ballots": [label(ballot) for ballot in ballots],
                    "selected_optimum": label(
                        certificate.solution.selected_ranking
                    ),
                    "optimum_cost": certificate.solution.optimum_cost,
                    "minimum_cost_by_kendall_distance": list(
                        certificate.minimum_cost_by_distance
                    ),
                    "second_ranking": label(certificate.second_ranking),
                    "second_score_gap": certificate.second_score_gap,
                    "second_distance": certificate.second_distance,
                    "second_attack_radius": best_second_radius,
                    "destabilizing_ranking": label(
                        certificate.destabilizing_ranking
                    ),
                    "destabilizing_score_gap": (
                        certificate.destabilizing_score_gap
                    ),
                    "destabilizing_distance": (
                        certificate.destabilizing_distance
                    ),
                    "exact_uniqueness_radius": (
                        certificate.uniqueness_radius
                    ),
                    "added_witness_copies": (
                        certificate.added_witness_copies
                    ),
                }

        by_size[str(profile_size)] = {
            "profile_count": profile_count,
            "tied_profile_count": tied_count,
            "unique_profile_count": profile_count - tied_count,
            "uniqueness_radius_histogram": dict(sorted(radii.items())),
            "larger_gap_faster_destabilizer_count": (
                larger_gap_faster_count
            ),
        }

    return {
        "candidate_count": 3,
        "maximum_profile_size": max_profile_size,
        "profiles_examined": sum(
            row["profile_count"] for row in by_size.values()
        ),
        "strict_denominator_example_count": strict_denominator_examples,
        "first_strict_denominator_example": first_example,
        "by_profile_size": by_size,
    }


def main() -> None:
    result = {
        "method": (
            "subset dynamic programming stratified by Kendall distance "
            "from the selected optimum"
        ),
        "status": "exact finite computation",
        "atlas": three_candidate_atlas(),
    }
    output = ROOT / "results" / "subset_dp_certificates.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
