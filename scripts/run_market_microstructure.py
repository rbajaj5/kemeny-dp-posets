"""Synthetic market-design tests at the three-ranking hardness boundary.

The experiment contrasts:

* independent price, time, and size priority rankings, which can encode an
  arbitrary three-voter Kemeny instance; and
* single-peaked rankings over a one-dimensional price menu, where majority
  structure removes the generic obstruction.

This is a mechanism-design laboratory, not a calibrated financial model.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import Ranking
from kemeny_dp.finite_sample import bernoulli_summary
from kemeny_dp.subset_dp import exact_kemeny_subset_dp


def pairwise_counts(ballots: tuple[Ranking, ...]) -> list[list[int]]:
    candidate_count = len(ballots[0])
    counts = [
        [0 for _ in range(candidate_count)] for _ in range(candidate_count)
    ]
    for ballot in ballots:
        positions = {
            candidate: position for position, candidate in enumerate(ballot)
        }
        for first in range(candidate_count):
            for second in range(first + 1, candidate_count):
                if positions[first] < positions[second]:
                    counts[first][second] += 1
                else:
                    counts[second][first] += 1
    return counts


def pairwise_lower_bound(ballots: tuple[Ranking, ...]) -> int:
    counts = pairwise_counts(ballots)
    return sum(
        min(counts[first][second], counts[second][first])
        for first in range(len(counts))
        for second in range(first + 1, len(counts))
    )


def independent_priority_ballots(
    order_count: int, rng: Random
) -> tuple[Ranking, Ranking, Ranking]:
    """Model independent price, time, and size order priorities."""
    rankings: list[Ranking] = []
    for _ in ("price_descending", "time_ascending", "size_descending"):
        ranking = list(range(order_count))
        rng.shuffle(ranking)
        rankings.append(tuple(ranking))
    return rankings[0], rankings[1], rankings[2]


def single_peaked_ballot(
    proposal_count: int, ideal: int, *, prefer_lower_on_ties: bool
) -> Ranking:
    """Rank a one-dimensional price menu by distance from an ideal point."""
    tie_direction = 1 if prefer_lower_on_ties else -1
    return tuple(
        sorted(
            range(proposal_count),
            key=lambda proposal: (
                abs(proposal - ideal),
                tie_direction * proposal,
            ),
        )
    )


def single_peaked_ballots(
    proposal_count: int, rng: Random
) -> tuple[Ranking, Ranking, Ranking]:
    return tuple(
        single_peaked_ballot(
            proposal_count,
            rng.randrange(proposal_count),
            prefer_lower_on_ties=bool(rng.randrange(2)),
        )
        for _ in range(3)
    )


def domain_experiment(
    *,
    domain: str,
    candidate_counts: tuple[int, ...],
    trials: int,
    rng: Random,
) -> dict[str, object]:
    results: dict[str, object] = {}
    for candidate_count in candidate_counts:
        cycle_count = 0
        unique_count = 0
        consensus_is_input = 0
        radius_counts: Counter[int] = Counter()
        optimum_counts: Counter[int] = Counter()

        for _ in range(trials):
            if domain == "independent_price_time_size":
                ballots = independent_priority_ballots(candidate_count, rng)
            elif domain == "single_peaked_price_menu":
                ballots = single_peaked_ballots(candidate_count, rng)
            else:
                raise ValueError(f"unknown domain: {domain}")

            result = exact_kemeny_subset_dp(ballots)
            lower_bound = pairwise_lower_bound(ballots)
            cycle_count += int(result.optimum_cost > lower_bound)
            optimum_counts[result.optimum_count] += 1
            if result.optimum_count == 1:
                unique_count += 1
                unanimous = ballots[0] == ballots[1] == ballots[2]
                radius_counts[3 if unanimous else 1] += 1
            else:
                radius_counts[0] += 1
            consensus_is_input += int(result.selected_ranking in ballots)

        results[str(candidate_count)] = {
            "subset_dp_states": 1 << candidate_count,
            "majority_cycle_rate": cycle_count / trials,
            "majority_cycle_finite_sample": bernoulli_summary(
                cycle_count, trials
            ).as_dict(),
            "unique_kemeny_rate": unique_count / trials,
            "unique_kemeny_finite_sample": bernoulli_summary(
                unique_count, trials
            ).as_dict(),
            "selected_consensus_is_one_of_three_inputs_rate": (
                consensus_is_input / trials
            ),
            "selected_consensus_is_input_finite_sample": bernoulli_summary(
                consensus_is_input, trials
            ).as_dict(),
            "optimum_count_histogram": dict(sorted(optimum_counts.items())),
            "cover_radius_histogram": dict(sorted(radius_counts.items())),
        }
    return results


def main() -> None:
    trials = 500
    candidate_counts = (5, 8, 10, 12)
    result = {
        "status": {
            "market_priority_hardness": "PROVED_BY_ENCODING",
            "market_statistics": "COMPUTATIONAL",
            "economic_equilibrium_claim": "NONE",
        },
        "carroll_connection": {
            "paper": "Informationally Robust Trade and Limits to Contagion",
            "scope": (
                "A Kemeny selection layer is proposed only for Carroll's "
                "multiple-proposal extension in Section 5.3, before bilateral "
                "accept/reject. It does not alter the single-deal theorem."
            ),
        },
        "trials_per_candidate_count": trials,
        "candidate_counts": candidate_counts,
        "independent_price_time_size": domain_experiment(
            domain="independent_price_time_size",
            candidate_counts=candidate_counts,
            trials=trials,
            rng=Random(314159),
        ),
        "single_peaked_price_menu": domain_experiment(
            domain="single_peaked_price_menu",
            candidate_counts=candidate_counts,
            trials=trials,
            rng=Random(271828),
        ),
    }
    result_path = ROOT / "results" / "market_microstructure.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
