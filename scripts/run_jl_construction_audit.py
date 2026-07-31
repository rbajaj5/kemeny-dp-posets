"""Compare binary-coin and spherical JL on finite ranking geometry."""

from __future__ import annotations

import json
from math import exp
from pathlib import Path
from random import Random
from statistics import mean, median
from typing import Callable

from kemeny_dp.core import RankingSpace
from kemeny_dp.geometry import (
    Projection,
    jl_sufficient_dimension,
    pairwise_sign_vector,
    project_vector,
    rademacher_projection,
    spherical_column_projection,
    squared_euclidean,
)


ROOT = Path(__file__).resolve().parents[1]
ProjectionConstructor = Callable[[int, int, Random], Projection]


def binary_projection(
    input_dimension: int,
    output_dimension: int,
    rng: Random,
) -> Projection:
    return rademacher_projection(
        input_dimension,
        output_dimension,
        rng=rng,
    )


def spherical_projection(
    input_dimension: int,
    output_dimension: int,
    rng: Random,
) -> Projection:
    return spherical_column_projection(
        input_dimension,
        output_dimension,
        rng=rng,
    )


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    index = round(probability * (len(ordered) - 1))
    return ordered[index]


def all_pair_metrics(
    projection: Projection,
    vectors: tuple[tuple[int, ...], ...],
    pair_data: tuple[tuple[int, int, float], ...],
    epsilon: float,
) -> dict[str, float | bool]:
    projected = tuple(
        project_vector(projection, vector) for vector in vectors
    )
    distortions = [
        abs(
            squared_euclidean(projected[left], projected[right])
            / true_squared_distance
            - 1
        )
        for left, right, true_squared_distance in pair_data
    ]
    return {
        "mean_absolute_relative_distortion": mean(distortions),
        "p95_absolute_relative_distortion": percentile(
            distortions, 0.95
        ),
        "maximum_absolute_relative_distortion": max(distortions),
        "pair_fraction_within_epsilon": (
            sum(distortion <= epsilon for distortion in distortions)
            / len(distortions)
        ),
        "all_pairs_within_epsilon": all(
            distortion <= epsilon for distortion in distortions
        ),
    }


def audit_construction(
    constructor: ProjectionConstructor,
    *,
    construction_index: int,
    input_dimension: int,
    dimensions: tuple[int, ...],
    vectors: tuple[tuple[int, ...], ...],
    pair_data: tuple[tuple[int, int, float], ...],
    epsilon: float,
    all_pair_trials: int,
    fixed_vector_trials: int,
) -> dict[str, object]:
    fixed_vector = tuple(
        left - right
        for left, right in zip(vectors[0], vectors[-1])
    )
    fixed_norm_squared = sum(value * value for value in fixed_vector)
    by_dimension: dict[str, object] = {}
    for dimension in dimensions:
        trial_metrics = [
            all_pair_metrics(
                constructor(
                    input_dimension,
                    dimension,
                    Random(
                        10_000_000 * construction_index
                        + 100_000 * dimension
                        + trial
                    ),
                ),
                vectors,
                pair_data,
                epsilon,
            )
            for trial in range(all_pair_trials)
        ]
        fixed_distortions: list[float] = []
        for trial in range(fixed_vector_trials):
            projection = constructor(
                input_dimension,
                dimension,
                Random(
                    100_000_000 * construction_index
                    + 10_000 * dimension
                    + trial
                ),
            )
            projected = project_vector(projection, fixed_vector)
            fixed_distortions.append(
                abs(
                    sum(value * value for value in projected)
                    / fixed_norm_squared
                    - 1
                )
            )
        by_dimension[str(dimension)] = {
            "all_pair_trials": all_pair_trials,
            "mean_pair_fraction_within_epsilon": mean(
                metric["pair_fraction_within_epsilon"]
                for metric in trial_metrics
            ),
            "all_pairs_successful_trials": sum(
                metric["all_pairs_within_epsilon"]
                for metric in trial_metrics
            ),
            "mean_global_maximum_distortion": mean(
                metric["maximum_absolute_relative_distortion"]
                for metric in trial_metrics
            ),
            "best_global_maximum_distortion": min(
                metric["maximum_absolute_relative_distortion"]
                for metric in trial_metrics
            ),
            "mean_pairwise_absolute_distortion": mean(
                metric["mean_absolute_relative_distortion"]
                for metric in trial_metrics
            ),
            "mean_pairwise_p95_distortion": mean(
                metric["p95_absolute_relative_distortion"]
                for metric in trial_metrics
            ),
            "fixed_vector_trials": fixed_vector_trials,
            "fixed_vector_empirical_failure_rate": (
                sum(
                    distortion > epsilon
                    for distortion in fixed_distortions
                )
                / fixed_vector_trials
            ),
            "fixed_vector_median_distortion": median(
                fixed_distortions
            ),
            "proposition_8_tail_upper_bound_capped_at_one": min(
                1.0,
                2 * exp(-dimension * epsilon**2 / 64),
            ),
        }
    return by_dimension


def main() -> None:
    candidate_count = 5
    epsilon = 0.4
    delta = 0.05
    dimensions = (2, 4, 6, 8, 10, 16, 24, 32, 64)
    all_pair_trials = 16
    fixed_vector_trials = 2048
    space = RankingSpace.create(candidate_count)
    vectors = tuple(
        pairwise_sign_vector(ranking) for ranking in space.rankings
    )
    pair_data = tuple(
        (
            left,
            right,
            squared_euclidean(vectors[left], vectors[right]),
        )
        for left in range(space.ranking_count)
        for right in range(left + 1, space.ranking_count)
    )
    pair_count = len(pair_data)
    fixed_bound = jl_sufficient_dimension(epsilon, delta)
    finite_bound = jl_sufficient_dimension(
        epsilon,
        delta,
        finite_set_size=pair_count,
    )
    constructions = {
        "binary_coin": binary_projection,
        "spherical_independent_columns": spherical_projection,
    }
    result = {
        "status": {
            "proposition_8": "KNOWN_SOURCE_THEOREM",
            "projection_implementations": "TESTED",
            "ranking_geometry_comparison": "MONTE_CARLO",
            "privacy_claim": "NONE",
            "kemeny_argmin_theorem": "NONE",
        },
        "source": {
            "title": (
                "Simple, unified analysis of "
                "Johnson-Lindenstrauss with applications"
            ),
            "author": "Yingru Li",
            "arxiv": "2402.10232v4",
            "url": "https://arxiv.org/abs/2402.10232",
        },
        "ranking_geometry": {
            "candidate_count": candidate_count,
            "rankings": space.ranking_count,
            "ambient_pairwise_dimension": space.diameter,
            "unordered_ranking_pairs": pair_count,
            "identity": (
                "squared Euclidean pairwise-sign distance "
                "= 4 * Kendall distance"
            ),
        },
        "parameters": {
            "epsilon": epsilon,
            "delta": delta,
            "output_dimensions": dimensions,
            "all_pair_trials_per_dimension": all_pair_trials,
            "fixed_vector_trials_per_dimension": fixed_vector_trials,
        },
        "explicit_sufficient_dimensions": {
            "one_fixed_vector_proposition_8": fixed_bound,
            "all_unordered_ranking_pairs_by_union_bound": finite_bound,
            "ambient_dimension": space.diameter,
            "fixed_vector_bound_is_dimension_reduction": (
                fixed_bound < space.diameter
            ),
            "all_pair_bound_is_dimension_reduction": (
                finite_bound < space.diameter
            ),
        },
        "constructions": {
            name: audit_construction(
                constructor,
                construction_index=index,
                input_dimension=space.diameter,
                dimensions=dimensions,
                vectors=vectors,
                pair_data=pair_data,
                epsilon=epsilon,
                all_pair_trials=all_pair_trials,
                fixed_vector_trials=fixed_vector_trials,
            )
            for index, (name, constructor) in enumerate(
                constructions.items(),
                start=1,
            )
        },
        "claim_boundary": (
            "Proposition 8 is a fixed-vector norm guarantee. The finite-set "
            "bound uses a union bound. Neither result makes a projected "
            "Kemeny optimizer private or guarantees argmin preservation "
            "without a separate score-margin argument."
        ),
    }
    output = ROOT / "results" / "jl_construction_audit.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["status"], indent=2, sort_keys=True))
    print(
        "Sufficient dimensions:",
        fixed_bound,
        "(fixed),",
        finite_bound,
        "(all ranking pairs), ambient",
        space.diameter,
    )
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
