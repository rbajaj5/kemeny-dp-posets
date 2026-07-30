"""Exact finite-poset analogue of a law-characterizing hierarchy."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import RankingSpace
from kemeny_dp.law_hierarchy import (
    expected_profile,
    invert_upper_set_probabilities,
    upper_set_probabilities,
)
from kemeny_dp.poset import children, profiles_up_to


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    space = RankingSpace.create(3)
    states = profiles_up_to(space, 3)

    weights = {
        state: 1 + sum(
            (index + 1) * count
            for index, count in enumerate(state)
        )
        for state in states
    }
    total_weight = sum(weights.values())
    reference_mass = {
        state: Fraction(weight, total_weight)
        for state, weight in weights.items()
    }
    upper = upper_set_probabilities(states, reference_mass)
    reconstructed = invert_upper_set_probabilities(states, upper)

    point = (1, 1, 1, 0, 0, 0)
    left = (2, 1, 0, 0, 0, 0)
    right = (0, 1, 2, 0, 0, 0)
    point_mass = {point: Fraction(1)}
    mixture = {
        left: Fraction(1, 2),
        right: Fraction(1, 2),
    }
    point_upper = upper_set_probabilities(states, point_mass)
    mixture_upper = upper_set_probabilities(states, mixture)

    layer_counts = {
        str(size): sum(sum(state) == size for state in states)
        for size in range(4)
    }
    state_set = set(states)
    cover_count = sum(
        child in state_set
        for state in states
        for child in children(state)
    )

    result = {
        "status": {
            "bourgade_huang_random_matrix_results": "KNOWN_SOURCE",
            "finite_poset_characterization": (
                "KNOWN_MOBIUS_INVERSION_SPECIALIZATION"
            ),
            "reconstruction": "EXACT_COMPUTATIONAL",
            "random_matrix_or_privacy_claim": "NONE",
        },
        "bounded_profile_poset": {
            "ranking_types": space.ranking_count,
            "maximum_ballots": 3,
            "state_count": len(states),
            "cover_count": cover_count,
            "layer_counts": layer_counts,
        },
        "exact_reconstruction": {
            "input_mass_total": fraction_text(sum(reference_mass.values())),
            "upper_probability_at_empty": fraction_text(
                upper[space.empty_profile()]
            ),
            "recovered_exactly": reconstructed == reference_mass,
            "maximum_absolute_error": fraction_text(
                max(
                    abs(reconstructed[state] - reference_mass[state])
                    for state in states
                )
            ),
        },
        "three_voter_first_moment_collision": {
            "point_mass_profile": point,
            "mixture_profiles": [left, right],
            "mixture_weights": ["1/2", "1/2"],
            "shared_expected_profile": [
                fraction_text(value)
                for value in expected_profile(states, point_mass)
            ],
            "same_first_moments": (
                expected_profile(states, point_mass)
                == expected_profile(states, mixture)
            ),
            "full_hierarchies_equal": point_upper == mixture_upper,
            "separating_upper_set": left,
            "point_mass_upper_probability": fraction_text(
                point_upper[left]
            ),
            "mixture_upper_probability": fraction_text(
                mixture_upper[left]
            ),
        },
    }

    result_path = ROOT / "results" / "profile_law_hierarchy.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
