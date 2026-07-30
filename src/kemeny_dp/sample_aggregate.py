"""Utility-side pieces for sample-and-aggregate in Kendall space.

This module does not, by itself, provide differential privacy. It implements
the efficient metric center used by Nissim-Raskhodnikova-Smith so experiments
do not accidentally replace it with an NP-hard permutation median.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from random import Random

from .core import KemenyAnalyzer, Ranking, RankingSpace


def center_of_attention(
    space: RankingSpace,
    points: Sequence[Ranking],
    *,
    step: int = 1,
) -> Ranking:
    """Return the constrained NRS center of attention.

    For ``q=len(points)`` and step size ``s``, the target neighbor count is
    ``floor((q+s)/2)+1``. Each input point is scored by the radius of its
    target-th nearest input point. The minimum-radius input point is returned,
    with lexicographic tie-breaking.
    """
    if not points:
        raise ValueError("points must not be empty")
    if not 1 <= step < len(points):
        raise ValueError("step must satisfy 1 <= step < len(points)")
    ranking_index = {ranking: index for index, ranking in enumerate(space.rankings)}
    normalized = tuple(tuple(point) for point in points)
    if any(point not in ranking_index for point in normalized):
        raise ValueError("every point must be a ranking in the supplied space")

    target = (len(normalized) + step) // 2 + 1
    if target > len(normalized):
        raise ValueError("step is too large for a strict-majority center")

    candidates: list[tuple[int, Ranking]] = []
    for candidate in set(normalized):
        candidate_index = ranking_index[candidate]
        distances = sorted(
            space.distances[candidate_index][ranking_index[other]]
            for other in normalized
        )
        radius = distances[target - 1]
        candidates.append((radius, candidate))
    return min(candidates)[1]


def exact_block_outputs(
    space: RankingSpace,
    ballots: Iterable[Ranking],
    block_size: int,
    *,
    rng: Random | None = None,
) -> tuple[Ranking, ...]:
    """Shuffle ballots, solve complete blocks exactly, and return their optima.

    This is a utility experiment. Exact blocks of size three or more inherit
    the worst-case hardness identified by Peters (2026), even though the
    enumeration oracle here is usable for small candidate sets.
    """
    if block_size < 1:
        raise ValueError("block_size must be positive")
    rng = rng or Random()
    shuffled = [tuple(ballot) for ballot in ballots]
    rng.shuffle(shuffled)
    complete_count = len(shuffled) // block_size
    if complete_count == 0:
        raise ValueError("not enough ballots for one complete block")

    kemeny = KemenyAnalyzer(space)
    outputs: list[Ranking] = []
    for block_index in range(complete_count):
        start = block_index * block_size
        block = shuffled[start : start + block_size]
        profile = space.profile_from_ballots(block)
        outputs.append(kemeny.selected_optimum(profile))
    return tuple(outputs)


def sample_and_center(
    space: RankingSpace,
    ballots: Iterable[Ranking],
    block_size: int,
    *,
    step: int = 1,
    rng: Random | None = None,
) -> Ranking:
    """Utility prototype: exact block estimates plus center of attention."""
    outputs = exact_block_outputs(space, ballots, block_size, rng=rng)
    return center_of_attention(space, outputs, step=step)
