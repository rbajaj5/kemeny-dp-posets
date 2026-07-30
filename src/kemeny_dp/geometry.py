"""Pairwise-vector geometry for ranking experiments."""

from __future__ import annotations

from math import sqrt
from random import Random
from typing import Sequence

from .core import Ranking

Vector = tuple[float, ...]
Projection = tuple[Vector, ...]


def pairwise_sign_vector(ranking: Ranking) -> tuple[int, ...]:
    """Embed a ranking using one sign for each unordered candidate pair.

    Coordinates are ordered lexicographically by candidate label. A coordinate
    is ``+1`` when the smaller-labeled candidate appears first and ``-1``
    otherwise.
    """
    if len(set(ranking)) != len(ranking):
        raise ValueError("ranking entries must be distinct")
    if set(ranking) != set(range(len(ranking))):
        raise ValueError("ranking must be a permutation of range(len(ranking))")
    positions = {candidate: index for index, candidate in enumerate(ranking)}
    return tuple(
        1 if positions[first] < positions[second] else -1
        for first in range(len(ranking))
        for second in range(first + 1, len(ranking))
    )


def squared_euclidean(left: Sequence[float], right: Sequence[float]) -> float:
    """Return squared Euclidean distance between equal-length vectors."""
    if len(left) != len(right):
        raise ValueError("vectors must have equal length")
    return sum((a - b) ** 2 for a, b in zip(left, right))


def rademacher_projection(
    input_dimension: int,
    output_dimension: int,
    *,
    rng: Random,
) -> Projection:
    """Draw a dense sign JL matrix with entries ``+/-1/sqrt(k)``."""
    if input_dimension < 1 or output_dimension < 1:
        raise ValueError("projection dimensions must be positive")
    scale = 1 / sqrt(output_dimension)
    return tuple(
        tuple(scale if rng.random() < 0.5 else -scale for _ in range(input_dimension))
        for _ in range(output_dimension)
    )


def project_vector(projection: Projection, vector: Sequence[float]) -> Vector:
    """Apply a projection matrix to a vector."""
    if not projection:
        raise ValueError("projection must not be empty")
    if any(len(row) != len(vector) for row in projection):
        raise ValueError("projection rows and vector have incompatible dimensions")
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        for row in projection
    )
