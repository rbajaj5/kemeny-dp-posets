"""Utility-side pieces for sample-and-aggregate in Kendall space.

This module does not, by itself, provide differential privacy. It implements
the efficient metric center used by Nissim-Raskhodnikova-Smith so experiments
do not accidentally replace it with an NP-hard permutation median.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from random import Random
from typing import Literal

from .core import KemenyAnalyzer, Ranking, RankingSpace


@dataclass(frozen=True)
class AttentionCertificate:
    """Exact finite certificate for a center-of-attention calculation."""

    center: Ranking
    radius: int
    target_count: int
    point_count: int
    minimizers: tuple[Ranking, ...]
    restricted_to_input_points: bool


def _normalized_points(
    space: RankingSpace, points: Sequence[Ranking]
) -> tuple[Ranking, ...]:
    if not points:
        raise ValueError("points must not be empty")
    normalized = tuple(tuple(point) for point in points)
    expected_candidates = set(range(space.candidate_count))
    if any(
        len(point) != space.candidate_count
        or set(point) != expected_candidates
        for point in normalized
    ):
        raise ValueError("every point must be a ranking in the supplied space")
    return normalized


def _target_count(point_count: int, step: int) -> int:
    if not 1 <= step < point_count:
        raise ValueError("step must satisfy 1 <= step < len(points)")
    target = (point_count + step) // 2 + 1
    if target > point_count:
        raise ValueError("step is too large for a strict-majority center")
    return target


def _attention_certificate(
    space: RankingSpace,
    points: Sequence[Ranking],
    *,
    step: int,
    restrict_to_inputs: bool,
) -> AttentionCertificate:
    normalized = _normalized_points(space, points)
    target = _target_count(len(normalized), step)
    ranking_index = {
        ranking: index for index, ranking in enumerate(space.rankings)
    }
    candidate_points = (
        tuple(sorted(set(normalized)))
        if restrict_to_inputs
        else space.rankings
    )

    scored: list[tuple[int, Ranking]] = []
    for candidate in candidate_points:
        candidate_index = ranking_index[candidate]
        distances = sorted(
            space.distances[candidate_index][ranking_index[other]]
            for other in normalized
        )
        scored.append((distances[target - 1], candidate))

    radius = min(row[0] for row in scored)
    minimizers = tuple(
        candidate for candidate_radius, candidate in scored
        if candidate_radius == radius
    )
    return AttentionCertificate(
        center=min(minimizers),
        radius=radius,
        target_count=target,
        point_count=len(normalized),
        minimizers=minimizers,
        restricted_to_input_points=restrict_to_inputs,
    )


def center_of_attention_certificate(
    space: RankingSpace,
    points: Sequence[Ranking],
    *,
    step: int = 1,
) -> AttentionCertificate:
    """Certify the input-restricted NRS center and its minimizing set."""
    return _attention_certificate(
        space,
        points,
        step=step,
        restrict_to_inputs=True,
    )


def unrestricted_attention_certificate(
    space: RankingSpace,
    points: Sequence[Ranking],
    *,
    step: int = 1,
) -> AttentionCertificate:
    """Return the exact best ranking center, for small-instance audits."""
    return _attention_certificate(
        space,
        points,
        step=step,
        restrict_to_inputs=False,
    )


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
    return center_of_attention_certificate(space, points, step=step).center


def two_ballot_kemeny(
    space: RankingSpace, first: Ranking, second: Ranking
) -> Ranking:
    """Return an exact two-ballot Kemeny optimum in linear input time.

    Either endpoint minimizes the sum of distances to two points by the
    triangle inequality.  Returning the lexicographically smaller input makes
    the shortcut deterministic without enumerating the ranking space.
    """
    normalized = _normalized_points(space, (first, second))
    return min(normalized)


def borda_ranking(
    space: RankingSpace, ballots: Sequence[Ranking]
) -> Ranking:
    """Return the deterministic Borda ranking of a nonempty ballot block."""
    normalized = _normalized_points(space, ballots)
    position_sums = [0] * space.candidate_count
    for ballot in normalized:
        for position, candidate in enumerate(ballot):
            position_sums[candidate] += position
    return tuple(
        sorted(
            range(space.candidate_count),
            key=lambda candidate: (position_sums[candidate], candidate),
        )
    )


def _complete_blocks(
    space: RankingSpace,
    ballots: Iterable[Ranking],
    block_size: int,
    rng: Random | None,
) -> tuple[tuple[Ranking, ...], ...]:
    if block_size < 1:
        raise ValueError("block_size must be positive")
    normalized = tuple(tuple(ballot) for ballot in ballots)
    if not normalized:
        raise ValueError("not enough ballots for one complete block")
    _normalized_points(space, normalized)
    shuffled = list(normalized)
    (rng or Random()).shuffle(shuffled)
    complete_count = len(shuffled) // block_size
    if complete_count == 0:
        raise ValueError("not enough ballots for one complete block")
    return tuple(
        tuple(shuffled[start : start + block_size])
        for start in range(0, complete_count * block_size, block_size)
    )


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
    blocks = _complete_blocks(space, ballots, block_size, rng)
    kemeny = KemenyAnalyzer(space)
    outputs: list[Ranking] = []
    for block in blocks:
        if block_size == 2:
            outputs.append(two_ballot_kemeny(space, block[0], block[1]))
        else:
            profile = space.profile_from_ballots(block)
            outputs.append(kemeny.selected_optimum(profile))
    return tuple(outputs)


def borda_block_outputs(
    space: RankingSpace,
    ballots: Iterable[Ranking],
    block_size: int,
    *,
    rng: Random | None = None,
) -> tuple[Ranking, ...]:
    """Shuffle into complete blocks and return polynomial-time Borda outputs."""
    return tuple(
        borda_ranking(space, block)
        for block in _complete_blocks(space, ballots, block_size, rng)
    )


def sample_and_center(
    space: RankingSpace,
    ballots: Iterable[Ranking],
    block_size: int,
    *,
    step: int = 1,
    estimator: Literal["exact", "borda"] = "exact",
    rng: Random | None = None,
) -> Ranking:
    """Utility prototype: block estimates plus center of attention."""
    if estimator == "exact":
        outputs = exact_block_outputs(space, ballots, block_size, rng=rng)
    elif estimator == "borda":
        outputs = borda_block_outputs(space, ballots, block_size, rng=rng)
    else:
        raise ValueError("estimator must be 'exact' or 'borda'")
    return center_of_attention(space, outputs, step=step)
