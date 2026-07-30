"""Applications of the three-voter boundary to the PDF's main ideas.

The script produces four reproducible experiments:

1. exact three-voter stability atlases for three through five candidates;
2. exact exponential-mechanism utility for the private-learning viewpoint;
3. sample-and-center utility across the two/three-voter block boundary; and
4. random-projection preservation of three-voter Kemeny optima.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations_with_replacement
import json
from math import ceil, exp
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import KemenyAnalyzer, Ranking, RankingSpace
from kemeny_dp.geometry import (
    pairwise_sign_vector,
    project_vector,
    rademacher_projection,
    squared_euclidean,
)
from kemeny_dp.sample_aggregate import sample_and_center


def triple_scores(
    space: RankingSpace, triple: tuple[int, int, int]
) -> tuple[int, ...]:
    first, second, third = triple
    first_row = space.distances[first]
    second_row = space.distances[second]
    third_row = space.distances[third]
    return tuple(
        first_row[output] + second_row[output] + third_row[output]
        for output in range(space.ranking_count)
    )


def unique_radius(
    space: RankingSpace, scores: tuple[int, ...], optimum_index: int
) -> int:
    optimum_score = scores[optimum_index]
    return min(
        ceil(
            (score - optimum_score)
            / space.distances[optimum_index][competitor]
        )
        for competitor, score in enumerate(scores)
        if competitor != optimum_index
    )


def exact_atlas(candidate_count: int) -> dict[str, object]:
    space = RankingSpace.create(candidate_count)
    multiplicities: Counter[int] = Counter()
    radii: Counter[int] = Counter()
    unique_count = 0
    profile_count = 0
    exponential_epsilons = (0.5, 1.0, 2.0, 4.0)
    exponential_totals = {
        epsilon: {
            "optimum_probability": 0.0,
            "expected_regret": 0.0,
            "worst_expected_regret": 0.0,
        }
        for epsilon in exponential_epsilons
    }

    for triple in combinations_with_replacement(
        range(space.ranking_count), 3
    ):
        profile_count += 1
        scores = triple_scores(space, triple)
        optimum_score = min(scores)
        optimum_indices = tuple(
            index for index, score in enumerate(scores) if score == optimum_score
        )
        multiplicities[len(optimum_indices)] += 1
        if len(optimum_indices) == 1:
            unique_count += 1
            radius = unique_radius(space, scores, optimum_indices[0])
            unanimous = triple[0] == triple[2]
            expected_radius = 3 if unanimous else 1
            if radius != expected_radius:
                raise AssertionError(
                    "three-voter profile violated the proved radius dichotomy"
                )
            radii[radius] += 1
        else:
            radii[0] += 1

        if candidate_count <= 4:
            for epsilon, totals in exponential_totals.items():
                weights = tuple(
                    exp(
                        -epsilon
                        * (score - optimum_score)
                        / (2 * space.diameter)
                    )
                    for score in scores
                )
                normalizer = sum(weights)
                optimum_probability = sum(
                    weights[index] for index in optimum_indices
                ) / normalizer
                expected_regret = sum(
                    weight * (score - optimum_score)
                    for weight, score in zip(weights, scores)
                ) / normalizer
                totals["optimum_probability"] += optimum_probability
                totals["expected_regret"] += expected_regret
                totals["worst_expected_regret"] = max(
                    totals["worst_expected_regret"], expected_regret
                )

    exponential_summary: dict[str, object] = {}
    if candidate_count <= 4:
        exponential_summary = {
            str(epsilon): {
                "mean_probability_of_an_optimum": (
                    totals["optimum_probability"] / profile_count
                ),
                "mean_additive_cost_regret": (
                    totals["expected_regret"] / profile_count
                ),
                "worst_additive_cost_regret": totals[
                    "worst_expected_regret"
                ],
            }
            for epsilon, totals in exponential_totals.items()
        }

    return {
        "candidate_count": candidate_count,
        "ranking_count": space.ranking_count,
        "profile_count": profile_count,
        "unique_optimum_profiles": unique_count,
        "unique_optimum_rate": unique_count / profile_count,
        "unanimous_profiles": space.ranking_count,
        "optimum_multiplicity_histogram": dict(sorted(multiplicities.items())),
        "uniqueness_radius_histogram": dict(sorted(radii.items())),
        "exponential_mechanism": exponential_summary,
    }


def _weighted_index(weights: list[float], rng: Random) -> int:
    threshold = rng.random() * sum(weights)
    running = 0.0
    for index, weight in enumerate(weights):
        running += weight
        if running >= threshold:
            return index
    return len(weights) - 1


def mallows_ballot(candidate_count: int, phi: float, rng: Random) -> Ranking:
    """Sample Mallows(phi) around the identity under Kendall distance."""
    if not 0 <= phi <= 1:
        raise ValueError("phi must lie in [0, 1]")
    ranking: list[int] = []
    for candidate in range(candidate_count):
        inversion_count = _weighted_index(
            [phi**count for count in range(candidate + 1)], rng
        )
        ranking.insert(candidate - inversion_count, candidate)
    return tuple(ranking)


def sample_and_center_experiment() -> dict[str, object]:
    candidate_count = 4
    ballot_count = 60
    trials = 100
    phis = (0.0, 0.2, 0.5, 0.8, 1.0)
    block_sizes = (1, 2, 3, 5)
    space = RankingSpace.create(candidate_count)
    kemeny = KemenyAnalyzer(space)
    ranking_index = {
        ranking: index for index, ranking in enumerate(space.rankings)
    }
    planted = tuple(range(candidate_count))
    planted_index = ranking_index[planted]
    rng = Random(20260730)
    summary: dict[str, object] = {}

    for phi in phis:
        full_distance = 0
        aggregates = {
            block_size: {
                "distance_to_planted": 0,
                "distance_to_full_kemeny": 0,
                "matches_full_kemeny": 0,
            }
            for block_size in block_sizes
        }
        for trial in range(trials):
            ballots = tuple(
                mallows_ballot(candidate_count, phi, rng)
                for _ in range(ballot_count)
            )
            profile = space.profile_from_ballots(ballots)
            full = kemeny.selected_optimum(profile)
            full_index = ranking_index[full]
            full_distance += space.distances[planted_index][full_index]

            for block_size in block_sizes:
                output = sample_and_center(
                    space,
                    ballots,
                    block_size,
                    rng=Random(10_000 * trial + 100 * block_size + int(phi * 10)),
                )
                output_index = ranking_index[output]
                metric = aggregates[block_size]
                metric["distance_to_planted"] += space.distances[
                    planted_index
                ][output_index]
                metric["distance_to_full_kemeny"] += space.distances[
                    full_index
                ][output_index]
                metric["matches_full_kemeny"] += int(output == full)

        summary[str(phi)] = {
            "mean_full_kemeny_distance_to_planted": full_distance / trials,
            "block_results": {
                str(block_size): {
                    "mean_distance_to_planted": (
                        metric["distance_to_planted"] / trials
                    ),
                    "mean_distance_to_full_kemeny": (
                        metric["distance_to_full_kemeny"] / trials
                    ),
                    "full_kemeny_match_rate": (
                        metric["matches_full_kemeny"] / trials
                    ),
                    "block_output_count": ballot_count // block_size,
                    "at_or_above_three_voter_hardness_boundary": (
                        block_size >= 3
                    ),
                }
                for block_size, metric in aggregates.items()
            },
        }

    return {
        "model": "Mallows(phi) around the identity under Kendall distance",
        "candidate_count": candidate_count,
        "ballot_count": ballot_count,
        "trials_per_phi": trials,
        "tie_breaking": {
            "full_kemeny_and_blocks_of_size_at_least_three": (
                "lexicographic among all optima"
            ),
            "two_ballot_blocks": (
                "lexicographically smaller input; exact by triangle inequality"
            ),
            "center_of_attention": (
                "lexicographic among input-restricted minimum-radius centers"
            ),
        },
        "results": summary,
    }


def _projected_distance_matrix(
    vectors: tuple[tuple[int, ...], ...],
    output_dimension: int,
    rng: Random,
) -> tuple[tuple[float, ...], ...]:
    projection = rademacher_projection(
        len(vectors[0]), output_dimension, rng=rng
    )
    projected = tuple(project_vector(projection, vector) for vector in vectors)
    return tuple(
        tuple(squared_euclidean(left, right) / 4 for right in projected)
        for left in projected
    )


def jl_experiment() -> dict[str, object]:
    candidate_count = 5
    sample_count = 400
    repetitions = 8
    dimensions = (2, 4, 6, 8, 12, 16, 24, 32)
    space = RankingSpace.create(candidate_count)
    vectors = tuple(pairwise_sign_vector(ranking) for ranking in space.rankings)
    profile_rng = Random(260725540)
    random_triples = tuple(
        tuple(profile_rng.randrange(space.ranking_count) for _ in range(3))
        for _ in range(sample_count)
    )
    unanimous_triples = tuple(
        (ranking, ranking, ranking) for ranking in range(space.ranking_count)
    )
    triples = unanimous_triples + random_triples

    profile_data: list[dict[str, object]] = []
    radius_counts: Counter[int] = Counter()
    for triple in triples:
        scores = triple_scores(space, triple)
        optimum = min(scores)
        optima = tuple(
            index for index, score in enumerate(scores) if score == optimum
        )
        if len(optima) != 1:
            continue
        optimum_index = optima[0]
        radius = unique_radius(space, scores, optimum_index)
        radius_counts[radius] += 1
        threshold = min(
            (score - optimum)
            / (score + optimum)
            for index, score in enumerate(scores)
            if index != optimum_index and score + optimum > 0
        )
        profile_data.append(
            {
                "triple": triple,
                "scores": scores,
                "optimum": optimum_index,
                "radius": radius,
                "relative_error_threshold": threshold,
            }
        )

    results: dict[str, object] = {}
    for dimension in dimensions:
        containments = 0
        exact_unique_matches = 0
        comparisons = 0
        certified = 0
        certified_violations = 0
        by_radius = defaultdict(lambda: [0, 0])
        projection_max_errors: list[float] = []

        for repetition in range(repetitions):
            projected_distances = _projected_distance_matrix(
                vectors,
                dimension,
                Random(1_000_000 * dimension + repetition),
            )
            maximum_error = 0.0
            for left in range(space.ranking_count):
                for right in range(left + 1, space.ranking_count):
                    true_distance = space.distances[left][right]
                    error = abs(
                        projected_distances[left][right] / true_distance - 1
                    )
                    maximum_error = max(maximum_error, error)
            projection_max_errors.append(maximum_error)

            for data in profile_data:
                triple = data["triple"]
                projected_scores = tuple(
                    projected_distances[triple[0]][output]
                    + projected_distances[triple[1]][output]
                    + projected_distances[triple[2]][output]
                    for output in range(space.ranking_count)
                )
                projected_optimum = min(projected_scores)
                projected_optima = tuple(
                    index
                    for index, score in enumerate(projected_scores)
                    if abs(score - projected_optimum) <= 1e-9
                )
                original_optimum = data["optimum"]
                contained = original_optimum in projected_optima
                containments += int(contained)
                exact_unique_matches += int(
                    projected_optima == (original_optimum,)
                )
                comparisons += 1
                radius = data["radius"]
                by_radius[radius][0] += int(contained)
                by_radius[radius][1] += 1

                profile_error = 0.0
                for ballot in triple:
                    for output in range(space.ranking_count):
                        true_distance = space.distances[ballot][output]
                        if true_distance:
                            profile_error = max(
                                profile_error,
                                abs(
                                    projected_distances[ballot][output]
                                    / true_distance
                                    - 1
                                ),
                            )
                if profile_error < data["relative_error_threshold"] - 1e-12:
                    certified += 1
                    if projected_optima != (original_optimum,):
                        certified_violations += 1

        if certified_violations:
            raise AssertionError("JL margin certificate was violated")
        results[str(dimension)] = {
            "unique_optimum_containment_rate": containments / comparisons,
            "unique_projected_match_rate": exact_unique_matches / comparisons,
            "mean_global_max_relative_pairwise_distortion": (
                sum(projection_max_errors) / repetitions
            ),
            "margin_certified_comparisons": certified,
            "margin_certificate_violations": certified_violations,
            "containment_rate_by_radius": {
                str(radius): successes / count
                for radius, (successes, count) in sorted(by_radius.items())
            },
        }

    return {
        "candidate_count": candidate_count,
        "ambient_pairwise_dimension": space.diameter,
        "unanimous_profiles_included": len(unanimous_triples),
        "additional_profiles_sampled_with_replacement": sample_count,
        "total_three_voter_profiles_tested": len(triples),
        "unique_profiles_in_sample": len(profile_data),
        "unique_radius_histogram": dict(sorted(radius_counts.items())),
        "projections_per_dimension": repetitions,
        "projection": "dense Rademacher +/-1/sqrt(k)",
        "results": results,
    }


def main() -> None:
    result = {
        "status": {
            "exact_atlases": "COMPUTATIONAL",
            "three_voter_radius_dichotomy": "PROVED",
            "exponential_privacy": "KNOWN_AND_EXHAUSTIVELY_TESTED",
            "sample_and_center": "NON_PRIVATE_UTILITY_EXPERIMENT",
            "jl": "COMPUTATIONAL_NO_PRIVACY_CLAIM",
        },
        "exact_three_voter_atlases": {
            str(candidate_count): exact_atlas(candidate_count)
            for candidate_count in (3, 4, 5)
        },
        "sample_and_center": sample_and_center_experiment(),
        "johnson_lindenstrauss": jl_experiment(),
    }
    result_path = ROOT / "results" / "three_voter_applications.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
