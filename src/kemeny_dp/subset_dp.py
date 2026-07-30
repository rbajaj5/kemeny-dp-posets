"""Exact exponential-space Kemeny solver using subset dynamic programming."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .core import Ranking


@dataclass(frozen=True)
class SubsetDPResult:
    optimum_cost: int
    selected_ranking: Ranking
    optimum_count: int
    state_count: int


def exact_kemeny_subset_dp(ballots: Sequence[Ranking]) -> SubsetDPResult:
    """Solve Kemeny aggregation in ``O(m^2 2^m)`` time and ``O(m 2^m)`` space.

    This is useful beyond factorial enumeration but remains exponential, as the
    three-voter hardness theorem requires in the worst case unless P=NP.
    Lexicographic tie-breaking chooses ``selected_ranking``.
    """
    if not ballots:
        raise ValueError("at least one ballot is required")
    normalized = tuple(tuple(ballot) for ballot in ballots)
    candidate_count = len(normalized[0])
    candidates = set(range(candidate_count))
    if any(len(ballot) != candidate_count or set(ballot) != candidates for ballot in normalized):
        raise ValueError("ballots must be permutations of the same range(m)")

    preference_counts = [
        [0 for _ in range(candidate_count)] for _ in range(candidate_count)
    ]
    for ballot in normalized:
        positions = {
            candidate: position for position, candidate in enumerate(ballot)
        }
        for first in range(candidate_count):
            for second in range(candidate_count):
                if positions[first] < positions[second]:
                    preference_counts[first][second] += 1

    state_count = 1 << candidate_count
    infinity = candidate_count * candidate_count * len(normalized) + 1
    costs = [infinity] * state_count
    optimum_counts = [0] * state_count
    selected: list[Ranking | None] = [None] * state_count
    costs[0] = 0
    optimum_counts[0] = 1
    selected[0] = ()

    for mask in range(1, state_count):
        remaining = mask
        while remaining:
            last_bit = remaining & -remaining
            last = last_bit.bit_length() - 1
            previous = mask ^ last_bit
            added_cost = 0
            previous_bits = previous
            while previous_bits:
                earlier_bit = previous_bits & -previous_bits
                earlier = earlier_bit.bit_length() - 1
                added_cost += preference_counts[last][earlier]
                previous_bits ^= earlier_bit
            candidate_cost = costs[previous] + added_cost
            previous_ranking = selected[previous]
            if previous_ranking is None:
                raise AssertionError("subset DP reached an uninitialized state")
            candidate_ranking = previous_ranking + (last,)
            if candidate_cost < costs[mask]:
                costs[mask] = candidate_cost
                optimum_counts[mask] = optimum_counts[previous]
                selected[mask] = candidate_ranking
            elif candidate_cost == costs[mask]:
                optimum_counts[mask] += optimum_counts[previous]
                current_ranking = selected[mask]
                if current_ranking is None or candidate_ranking < current_ranking:
                    selected[mask] = candidate_ranking
            remaining ^= last_bit

    full = state_count - 1
    ranking = selected[full]
    if ranking is None:
        raise AssertionError("subset DP did not produce a ranking")
    return SubsetDPResult(
        costs[full],
        ranking,
        optimum_counts[full],
        state_count,
    )
