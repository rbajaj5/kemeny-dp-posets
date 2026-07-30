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


@dataclass(frozen=True)
class SubsetDPStabilityCertificate:
    """Exact optimum, score-gap, and cover-instability witnesses."""

    solution: SubsetDPResult
    second_ranking: Ranking
    second_cost: int
    second_score_gap: int
    second_distance: int
    destabilizing_ranking: Ranking
    destabilizing_cost: int
    destabilizing_score_gap: int
    destabilizing_distance: int
    uniqueness_radius: int
    added_witness_copies: int
    augmented_state_count: int
    minimum_cost_by_distance: tuple[int | None, ...]


def _normalize_and_count_preferences(
    ballots: Sequence[Ranking],
) -> tuple[tuple[Ranking, ...], int, list[list[int]]]:
    if not ballots:
        raise ValueError("at least one ballot is required")
    normalized = tuple(tuple(ballot) for ballot in ballots)
    candidate_count = len(normalized[0])
    candidates = set(range(candidate_count))
    if any(
        len(ballot) != candidate_count or set(ballot) != candidates
        for ballot in normalized
    ):
        raise ValueError("ballots must be permutations of the same range(m)")

    preference_counts = [
        [0 for _ in range(candidate_count)]
        for _ in range(candidate_count)
    ]
    for ballot in normalized:
        positions = {
            candidate: position for position, candidate in enumerate(ballot)
        }
        for first in range(candidate_count):
            for second in range(candidate_count):
                if positions[first] < positions[second]:
                    preference_counts[first][second] += 1
    return normalized, candidate_count, preference_counts


def exact_kemeny_subset_dp(ballots: Sequence[Ranking]) -> SubsetDPResult:
    """Solve Kemeny aggregation in ``O(m^2 2^m)`` time and ``O(m 2^m)`` space.

    This is useful beyond factorial enumeration but remains exponential, as the
    three-voter hardness theorem requires in the worst case unless P=NP.
    Lexicographic tie-breaking chooses ``selected_ranking``.
    """
    normalized, candidate_count, preference_counts = (
        _normalize_and_count_preferences(ballots)
    )

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


def exact_kemeny_stability_subset_dp(
    ballots: Sequence[Ranking],
) -> SubsetDPStabilityCertificate:
    """Return exact score-gap and uniqueness-radius witnesses.

    After solving Kemeny once, a second subset DP is stratified by Kendall
    distance from the selected optimum. For each distance ``d`` it finds the
    least-cost competing ranking at exactly that distance. These minima give
    both the second-best score and

    ``min_d ceil((best_cost_at_distance[d] - optimum_cost) / d)``.

    If several competitors have the second-best cost, ``second_ranking`` is
    selected from their largest occupied distance layer, which gives the
    smallest repeated-addition radius available at that cost.

    The minimizing competitor is also a constructive cover-path witness:
    adding ``uniqueness_radius`` copies of that ranking makes the selected
    optimum lose uniqueness. Tied inputs have radius and witness-copy count
    zero.
    """
    normalized, candidate_count, preference_counts = (
        _normalize_and_count_preferences(ballots)
    )
    if candidate_count < 2:
        raise ValueError("a stability certificate needs at least two candidates")
    solution = exact_kemeny_subset_dp(normalized)
    optimum = solution.selected_ranking
    optimum_positions = {
        candidate: position for position, candidate in enumerate(optimum)
    }
    diameter = candidate_count * (candidate_count - 1) // 2
    state_count = 1 << candidate_count
    infinity = candidate_count * candidate_count * len(normalized) + 1

    transition_cost = [
        [0 for _ in range(candidate_count)] for _ in range(state_count)
    ]
    transition_distance = [
        [0 for _ in range(candidate_count)] for _ in range(state_count)
    ]
    for mask in range(1, state_count):
        remaining = mask
        while remaining:
            last_bit = remaining & -remaining
            last = last_bit.bit_length() - 1
            previous = mask ^ last_bit
            previous_bits = previous
            while previous_bits:
                earlier_bit = previous_bits & -previous_bits
                earlier = earlier_bit.bit_length() - 1
                transition_cost[mask][last] += preference_counts[last][earlier]
                transition_distance[mask][last] += int(
                    optimum_positions[last] < optimum_positions[earlier]
                )
                previous_bits ^= earlier_bit
            remaining ^= last_bit

    costs = [
        [infinity for _ in range(diameter + 1)]
        for _ in range(state_count)
    ]
    parent_last = [
        [-1 for _ in range(diameter + 1)]
        for _ in range(state_count)
    ]
    costs[0][0] = 0

    for mask in range(1, state_count):
        remaining = mask
        while remaining:
            last_bit = remaining & -remaining
            last = last_bit.bit_length() - 1
            previous = mask ^ last_bit
            added_cost = transition_cost[mask][last]
            added_distance = transition_distance[mask][last]
            for previous_distance, previous_cost in enumerate(costs[previous]):
                if previous_cost == infinity:
                    continue
                distance = previous_distance + added_distance
                candidate_cost = previous_cost + added_cost
                if candidate_cost < costs[mask][distance]:
                    costs[mask][distance] = candidate_cost
                    parent_last[mask][distance] = last
            remaining ^= last_bit

    full = state_count - 1

    def reconstruct(distance: int) -> Ranking:
        mask = full
        reversed_ranking: list[int] = []
        while mask:
            last = parent_last[mask][distance]
            if last < 0:
                raise AssertionError(
                    "distance-stratified subset DP lost its witness"
                )
            reversed_ranking.append(last)
            distance -= transition_distance[mask][last]
            mask ^= 1 << last
        return tuple(reversed(reversed_ranking))

    finite_distances = tuple(
        distance
        for distance in range(1, diameter + 1)
        if costs[full][distance] != infinity
    )
    if not finite_distances:
        raise AssertionError("a ranking space with one candidate has no competitor")

    second_distance = min(
        finite_distances,
        key=lambda distance: (costs[full][distance], -distance),
    )
    second_cost = costs[full][second_distance]
    second_ranking = reconstruct(second_distance)
    second_gap = second_cost - solution.optimum_cost

    if solution.optimum_count > 1:
        tied_distances = tuple(
            distance
            for distance in finite_distances
            if costs[full][distance] == solution.optimum_cost
        )
        destabilizing_distance = min(tied_distances)
        uniqueness_radius = 0
    else:
        destabilizing_distance = min(
            finite_distances,
            key=lambda distance: (
                (
                    costs[full][distance]
                    - solution.optimum_cost
                    + distance
                    - 1
                )
                // distance,
                costs[full][distance] - solution.optimum_cost,
                distance,
            ),
        )
        destabilizing_gap = (
            costs[full][destabilizing_distance] - solution.optimum_cost
        )
        uniqueness_radius = (
            destabilizing_gap
            + destabilizing_distance
            - 1
        ) // destabilizing_distance

    destabilizing_cost = costs[full][destabilizing_distance]
    destabilizing_ranking = reconstruct(destabilizing_distance)
    destabilizing_gap = destabilizing_cost - solution.optimum_cost
    augmented_state_count = sum(
        cost != infinity for row in costs for cost in row
    )
    return SubsetDPStabilityCertificate(
        solution=solution,
        second_ranking=second_ranking,
        second_cost=second_cost,
        second_score_gap=second_gap,
        second_distance=second_distance,
        destabilizing_ranking=destabilizing_ranking,
        destabilizing_cost=destabilizing_cost,
        destabilizing_score_gap=destabilizing_gap,
        destabilizing_distance=destabilizing_distance,
        uniqueness_radius=uniqueness_radius,
        added_witness_copies=uniqueness_radius,
        augmented_state_count=augmented_state_count,
        minimum_cost_by_distance=tuple(
            None if cost == infinity else cost for cost in costs[full]
        ),
    )
